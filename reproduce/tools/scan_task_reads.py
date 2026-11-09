"""Maintainers only: find every file on the project's server that names one of the unsplit OSWorld tasks.

The unsplit tasks are those of src/osworld/test_nogdrive.json in neither src/osworld/split_diag.json nor
split_test.json. For each, this lists the result directories named after it and the text files that mention its id,
under the roots given (default: ~/osw, the development checkout, this repository and the lab repository), and writes reproduce/results/unsplit_task_reads.json.
This repository's own copies of the task list and of this tool's outputs are skipped. Files tracked by the RealtimeGUI harness checkout (git ls-files, committed by its authors before this project started)
are reported apart: they are the harness's own data, not a read by this project.
Usage: python3 reproduce/tools/scan_task_reads.py [ROOT ...]
"""
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OSW = pathlib.Path.home() / "osw"
HARNESS = OSW / "rtg"
roots = [pathlib.Path(r) for r in sys.argv[1:]] or [OSW, pathlib.Path.home() / "projects/ComputerUseHackaton", ROOT,
                                                   pathlib.Path.home() / "projects/lab"]
SKIP_DIRS = {".git", "node_modules", "evaluation_examples", "evaluation_examples_windows", "__pycache__", ".venv"}
OWN = {ROOT / "src/osworld/test_nogdrive.json", ROOT / "reproduce/results/unsplit_task_reads.json", ROOT / "docs/FRESH_TASKS.json"}
TEXT = {".json", ".jsonl", ".md", ".txt", ".py", ".csv", ".log", ".tex", ".sh"}

split = lambda n: json.loads((ROOT / "src/osworld" / n).read_text())
allt = split("test_nogdrive.json")
used = {i for v in list(split("split_diag.json").values()) + list(split("split_test.json").values()) for i in v}
unsplit = {i: d for d, ids in allt.items() for i in ids if i not in used}
tracked = set(subprocess.run(["git", "-C", str(HARNESS), "ls-files", "-z"], capture_output=True, text=True, check=True).stdout.split("\0"))
hits = {i: {"result_dirs": [], "files": [], "harness_files": []} for i in unsplit}
for root in roots:
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = list(d.iterdir())
        except OSError:
            continue
        for e in entries:
            if e.is_symlink():
                continue
            if e.is_dir():
                if e.name in SKIP_DIRS:
                    continue
                if e.name in hits:
                    hits[e.name]["result_dirs"].append(str(e))
                stack.append(e)
            elif e.suffix in TEXT and e not in OWN and e.stat().st_size < 200_000_000:
                try:
                    txt = e.read_text(errors="ignore")
                except OSError:
                    continue
                for i in unsplit:
                    if i in txt:
                        rel = str(e.relative_to(HARNESS)) if HARNESS in e.parents else None
                        (hits[i]["harness_files"] if rel in tracked else hits[i]["files"]).append(str(e))
for i in hits:
    for k in hits[i]:
        hits[i][k] = sorted(set(hits[i][k]))
out = {"scanned_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
       "roots": [str(r) for r in roots], "skipped_dirs": sorted(SKIP_DIRS), "skipped_files": sorted(str(f.relative_to(ROOT)) for f in OWN), "text_suffixes": sorted(TEXT),
       "harness_checkout": str(HARNESS),
       "harness_commit": subprocess.run(["git", "-C", str(HARNESS), "log", "-1", "--format=%H %aI"], capture_output=True, text=True).stdout.strip(),
       "n_unsplit": len(unsplit),
       "tasks": {f"{unsplit[i]}/{i}": hits[i] for i in sorted(unsplit, key=lambda i: (unsplit[i], i))}}
(ROOT / "reproduce/results/unsplit_task_reads.json").write_text(json.dumps(out, indent=1) + "\n")
read = [t for t, h in out["tasks"].items() if h["result_dirs"] or h["files"]]
print(f"unsplit {len(unsplit)}, named in a project file {len(read)}: {read}")
