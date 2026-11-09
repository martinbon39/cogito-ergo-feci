#!/usr/bin/env bash
# Regenerate every number, table and figure from paper/data/, then compile main.pdf.
# exact.py runs last: it reads the bootstrap intervals the other scripts write to generated/.
set -euo pipefail
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1794182400}"  # fixed timestamp: PDFs and figures are byte-reproducible
[ -x .venv/bin/python ] || { uv venv -q .venv && uv pip install -q --python .venv/bin/python matplotlib numpy pillow; }
cd figs
for f in osw_diag miniwob b4 teaser pipeline traps causal perceive expo attractor broad closures online infeasible power moonleak proofanchor guard exact; do ../.venv/bin/python "$f.py"; done
cd ..
TECTONIC=${TECTONIC:-$(command -v tectonic || echo "$HOME/.local/bin/tectonic")}
for doc in main neurips; do
  "$TECTONIC" -X compile --keep-logs "$doc.tex"
  undef=$(grep -E "(Reference|Citation) .* undefined" "$doc.log" || true)
  rm -f "$doc.log"
  [ -z "$undef" ] || { echo "$doc.tex: undefined references or citations:"; echo "$undef"; exit 1; }
done
