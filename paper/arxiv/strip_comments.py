#!/usr/bin/env python3
"""Remove LaTeX % comments from .tex files in place, keeping TeX semantics.

A % is a comment only if it is preceded by an even number of backslashes
(\\% is a line break followed by a comment, \\\\% is an escaped percent sign after one).
A line that held only a comment is dropped. A line with content before the comment keeps
a bare trailing % so the end-of-line space stays suppressed, as in arxiv_latex_cleaner.
Files that contain verbatim-like environments, \\verb, comment environments or \\iffalse
are refused: this stripper does not parse them.
"""
import re
import sys

UNSAFE = re.compile(r"\\begin\{(verbatim|Verbatim|lstlisting|minted|comment)\}|\\verb|\\iffalse|\\url\{[^}]*%|\\href\{[^}]*%")


def comment_start(line):
    i = 0
    while True:
        j = line.find("%", i)
        if j < 0:
            return -1
        k = j
        while k > 0 and line[k - 1] == "\\":
            k -= 1
        if (j - k) % 2 == 0:
            return j
        i = j + 1


def strip(text):
    out = []
    for line in text.split("\n"):
        j = comment_start(line)
        if j < 0:
            out.append(line.rstrip())
            continue
        before = line[:j]
        if before.strip():
            out.append(before + "%")
    while len(out) > 1 and out[-1] == "" and out[-2] == "":
        out.pop()
    return "\n".join(out)


def main(paths):
    for p in paths:
        with open(p, encoding="utf-8") as f:
            text = f.read()
        m = UNSAFE.search(text)
        if m:
            sys.exit(f"strip_comments: {p} contains {m.group(0)!r}; extend the stripper before packaging it")
        new = strip(text)
        with open(p, "w", encoding="utf-8") as f:
            f.write(new if new.endswith("\n") else new + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
