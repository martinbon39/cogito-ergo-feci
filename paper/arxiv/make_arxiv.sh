#!/usr/bin/env bash
# Build arxiv-submission.tar.gz from paper/main.tex, the way arXiv's AutoTeX will compile it (pdfLaTeX).
#
# Usage: paper/arxiv/make_arxiv.sh [OUTPUT.tar.gz]      (default: ./arxiv-submission.tar.gz)
# Needs a TeX Live with pdflatex and bibtex on PATH. arXiv uses TeX Live 2025; to match it,
#   PATH=/path/to/texlive/2025/bin/x86_64-linux:$PATH paper/arxiv/make_arxiv.sh
# Set SKIP_TEST=1 to skip the final test compile of the extracted tarball.
#
# Steps: copy the sources to a stage, compile with -recorder, keep only the files pdflatex actually
# read, strip % comments, add main.bbl, check arXiv's file rules, write a deterministic tarball,
# then extract it into an empty directory and compile it twice with pdflatex as AutoTeX does.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PAPER="$(dirname "$HERE")"
OUT="$(realpath -m "${1:-arxiv-submission.tar.gz}")"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1794182400}"

for tool in pdflatex bibtex python3 tar gzip; do
  command -v "$tool" >/dev/null || { echo "make_arxiv: $tool not found on PATH" >&2; exit 1; }
done
echo "make_arxiv: $(pdflatex --version | head -1)"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
STAGE="$WORK/stage" PKG="$WORK/pkg" TEST="$WORK/test"
mkdir -p "$STAGE" "$PKG" "$TEST"

(cd "$PAPER" && cp -r main.tex arxiv.sty refs.bib shared sec fig generated figs "$STAGE/")

latex() { pdflatex -recorder -interaction=nonstopmode -halt-on-error "$@" main.tex >/dev/null; }
(cd "$STAGE" && latex && bibtex -terse main >/dev/null && latex && latex) || {
  echo "make_arxiv: staging compile failed, see the log:" >&2; tail -40 "$STAGE/main.log" >&2; exit 1; }

# Files pdflatex read that belong to the paper (relative paths, or absolute paths inside the stage).
mapfile -t USED < <(
  sed -n 's/^INPUT //p' "$STAGE/main.fls" \
    | sed "s#^$STAGE/##; s#^\./##" \
    | grep -v '^/' \
    | grep -vE '\.(aux|out|toc|bbl|lof|lot|nav|snm)$' \
    | sort -u)
for f in "${USED[@]}"; do
  mkdir -p "$PKG/$(dirname "$f")"
  cp "$STAGE/$f" "$PKG/$f"
done
cp "$STAGE/main.bbl" "$PKG/main.bbl"

mapfile -t TEXFILES < <(cd "$PKG" && find . -name '*.tex' | sort)
(cd "$PKG" && python3 "$HERE/strip_comments.py" "${TEXFILES[@]}")
# arXiv picks pdfLaTeX from this flag when it is in the first five lines.
{ printf '%s\n' '\pdfoutput=1'; cat "$PKG/main.tex"; } > "$WORK/main.tex" && mv "$WORK/main.tex" "$PKG/main.tex"

# arXiv file rules: allowed characters, no hidden files, no build outputs, no oversized images.
bad=$(cd "$PKG" && find . -mindepth 1 | sed 's#^\./##' | grep -vE '^[a-zA-Z0-9_+.,=/-]+$' || true)
[ -z "$bad" ] || { echo "make_arxiv: filenames arXiv rejects: $bad" >&2; exit 1; }
hidden=$(cd "$PKG" && find . -name '.*' -not -name . || true)
[ -z "$hidden" ] || { echo "make_arxiv: hidden files: $hidden" >&2; exit 1; }
outputs=$(cd "$PKG" && find . -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.fls' -o -name 'main.pdf' \) || true)
[ -z "$outputs" ] || { echo "make_arxiv: build outputs in package: $outputs" >&2; exit 1; }
python3 - "$PKG" <<'EOF'
import struct, sys, pathlib
for p in pathlib.Path(sys.argv[1]).rglob("*.png"):
    w, h = struct.unpack(">II", p.read_bytes()[16:24])
    if w * h > 34_000_000:
        sys.exit(f"make_arxiv: {p.name} has {w*h/1e6:.1f} MP, above arXiv's 34 MP warning")
EOF

find "$PKG" -exec touch -h -d "@$SOURCE_DATE_EPOCH" {} +
(cd "$PKG" && tar --sort=name --mtime="@$SOURCE_DATE_EPOCH" --owner=0 --group=0 --numeric-owner \
  --format=gnu -cf - $(find . -type f | sed 's#^\./##' | sort)) | gzip -9n > "$OUT"

echo "make_arxiv: wrote $OUT ($(du -k "$OUT" | cut -f1) KB, $(tar -tzf "$OUT" | wc -l) files)"
tar -tzf "$OUT" | sed 's/^/  /'

[ "${SKIP_TEST:-0}" = 1 ] && exit 0
# Test as AutoTeX does: fresh directory, the .bbl already present, pdflatex until references settle.
tar -xzf "$OUT" -C "$TEST"
(cd "$TEST" && for i in 1 2 3; do pdflatex -interaction=nonstopmode main.tex >/dev/null || true; done)
LOG="$TEST/main.log"
errors=$(grep -c '^!' "$LOG" || true)
undef=$(grep -cE 'undefined (references|citations)|Citation .* undefined|Reference .* undefined' "$LOG" || true)
pages=$(grep -oE 'Output written on main.pdf \([0-9]+ pages' "$LOG" | grep -oE '[0-9]+ pages' || echo "no output")
overfull=$(grep -c '^Overfull' "$LOG" || true)
echo "make_arxiv: test compile: $pages, $errors errors, $undef undefined refs/citations, $overfull overfull boxes"
cp "$LOG" "${OUT%.tar.gz}.test.log"
cp "$TEST/main.pdf" "${OUT%.tar.gz}.test.pdf" 2>/dev/null || true
[ "$errors" = 0 ] && [ "$undef" = 0 ] && [ -f "$TEST/main.pdf" ] || { echo "make_arxiv: test compile FAILED" >&2; exit 1; }
echo "make_arxiv: OK"
