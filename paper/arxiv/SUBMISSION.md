# arXiv submission: Cogito, Ergo Feci

Everything to paste into the arXiv submission form, and the steps for the submitter.
Build the package first: see "Build" below. Values marked TO APPROVE need Martin's decision.

## Build

```bash
# TeX Live 2025, the version arXiv compiles with (pdfLaTeX). A user install from the TUG historic mirror works:
#   https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2025/tlnet-final/
PATH=/path/to/texlive/2025/bin/x86_64-linux:$PATH paper/arxiv/make_arxiv.sh arxiv-submission.tar.gz
```

The script compiles `main.tex` with `-recorder`, keeps only the files pdfLaTeX read, strips `%` comments
(`strip_comments.py`), adds `main.bbl` and `\pdfoutput=1`, checks arXiv's file rules, writes a deterministic
tarball (same sources give the same sha256), then extracts it into an empty directory and compiles it with
pdfLaTeX as arXiv's AutoTeX does. It fails on any LaTeX error or undefined reference or citation.

Rebuild after any change to `paper/` (numbers in `generated/` included). The page and figure counts in the
Comments field below must match the PDF that arXiv shows in its preview.

## Form fields

**License.** CC BY 4.0 (Creative Commons Attribution 4.0). Same license as the Zenodo record
(DOI 10.5281/zenodo.24061167). The code repository stays Apache-2.0; the arXiv license covers the paper only.

**Primary category.** cs.LG (Machine Learning).
Reason: the core contributions are interpretability, activation steering and training-free weight editing of a
model, with statistical evaluation, which is cs.LG's scope. cs.AI as primary is also defensible (agents).

**Cross-lists.** cs.AI (agents, verification of agent actions), cs.CL (the model is a vision-language LLM; probes
and steering of its residual stream).

**Title.**
```
Cogito, Ergo Feci: False Success, the Limits of Weight Surgery, and What an External Verifier Catches in a Computer-Use Agent
```

**Authors** (Zenodo order):
```
Émile Jouannet, Souad Boukhedenna, Martin Bonan
```
If the form rejects the accent, use `\'Emile Jouannet`. Affiliations go in the PDF only (EPITA; SKEMA Business
School; Independent), not in this field. TO APPROVE: the source comments say these affiliations were inferred
from e-mail domains and must be confirmed by Martin.

**Abstract** (TO APPROVE). The paper's abstract is 2134 characters as plain text; arXiv's limit is 1920. This
shortened version keeps every number and the attribution caveat; it drops the pilot screens' exact power
(8/8 to 4/8), the closed-form edit clause, "perhaps carried by the success claim in the retained reasoning", the
CLI-alias note and "formally meeting the registered criterion". 1764 characters, ASCII only:
```
Computer-use agents often fail by announcing that a task is finished when it is not. We diagnose it in Holo-3.1-4B on OSWorld and test whether editing activations or weights, without training, removes it. The agent scores 56.7% on 119 diagnostic tasks; a false "done" is 57% of its failures, and re-sampled it answers "done" on most false completions too (72%, against 94% on true ones). With a replay that rebuilds each step's input and a gate fixed in advance, we find three traps that would each have produced a positive result: a false-success direction that adds at most 0.04 AUROC to position, run-to-run noise under which only 50% of false successes recur, and a loop direction in a smaller model that beats position yet reduces loops only at a large cost to healthy actions. No steering arm or weight edit passes the gate in pilot screens that detect only large effects, and no edited or prompted arm run online beats the run-to-run noise of the original. The tool call leans on a thought that already declares success: on 39 feasible contexts, neutral text in its place removes 80-82% of the answer margin, yet answer stays preferred in 37. A model merge that moves the call shows no detectable selectivity (+0.7 points, 95% CI -16.1 to +16.3). An external verifier, Claude Sonnet checking each requirement on the final screen, detects 68% of false successes and rejects 10% of true ones offline (the agent judging itself: 53% and 48%). Online, on 120 held-out tasks, the guarded agent's false "done" rate fell from 22.5% to 10.8% (-11.7 points, 95% CI -19.2 to -4.2), but about two thirds of the drop come from episodes in which the guard never ran, so we do not attribute it to the guard; the score did not change measurably (+1.6, 95% CI -4.4 to +7.7).
```
Every number above is the value printed in the compiled abstract (`shared/abstract.tex` with `generated/num_*.tex`)
as of commit 8715f4a. If a merged change alters a generated number, update this text from the new PDF.

**Comments.**
```
35 pages, 10 figures, 17 tables. Also archived at Zenodo, DOI 10.5281/zenodo.24061167. Code, data and reproduction scripts: https://github.com/martinbon39/cogito-ergo-feci
```
Counts are from the TeX Live 2025 pdfLaTeX build of commit 8715f4a (the tectonic build in `paper/main.pdf` has 36
pages because floats land differently). Recount after a rebuild.

**Journal-ref.** Leave empty (not published in a journal).

**DOI.** Leave empty. arXiv's DOI field is for the published version of record; the Zenodo DOI is cited in Comments.

**MSC / ACM classes.** Optional. ACM: `I.2.6; I.2.8` if wanted.

**Report number.** Empty.

## Steps for the submitter

1. The submitter must have an arXiv account with endorsement for cs.LG (first-time submitters in a category may
   need an endorser; check at submission start).
2. Rebuild the tarball with `make_arxiv.sh` on the merged `main` of the paper repository and check it ends with
   `make_arxiv: OK`.
3. arxiv.org > Start new submission. Choose license CC BY 4.0, primary cs.LG.
4. Upload `arxiv-submission.tar.gz` as one file. arXiv unpacks it; it must list `main.tex`, `main.bbl`, `arxiv.sty`
   and the `fig/ figs/ generated/ sec/ shared/` files, nothing else. Leave the processor on automatic.
5. Process. Open arXiv's PDF preview and check: 35 pages, title page and the teaser figure, the reference list,
   no `??`. The date under the title is the date arXiv compiles (`\today`); see the note below.
6. Fill metadata from the fields above (title, authors, abstract, comments, cross-lists cs.AI and cs.CL).
7. Preview the abstract page, then submit. Announcement follows the next daily mailing cutoff (14:00 US Eastern).
8. After the announcement, add the arXiv ID to the README, `CITATION.cff` and the Zenodo record (related identifier,
   "is identical to"). Commit with the arXiv ID.

## Notes

- **Date on the title page.** `main.tex` prints `Preprint · \today`. On arXiv that is the date AutoTeX compiles the
  source, so it shows the submission date and changes if arXiv regenerates the PDF. The paper shows no fixed date
  elsewhere (the Zenodo record is dated 2026-11-08), so it is left as is. To freeze it, replace `\today` with a date.
- **AI use (TO APPROVE).** arXiv asks that significant use of generative AI tools be reported in the paper and does
  not accept AI tools as authors. The paper already says, in `sec/repro.tex` line 7:
  "The experiments were planned, run and reviewed by AI agents (Claude Code sessions, and GPT-6 Astra through the
  Codex CLI) under human supervision; Appendix~\ref{sec:method} describes the organisation, the safeguards and the
  rules that were not respected." Appendix `sec/app_method.tex` ("Organisation", "Human team") gives the details.
  This discloses AI use for the research clearly. It does not say who wrote the paper text: in the development
  repository, all 28 commits that touch `holo-neurochir/paper/sec` or `main.tex` carry a
  "Co-Authored-By: Claude" trailer. Proposed addition, at the end of that paragraph in `sec/repro.tex`:

  > The text of this paper, its figures and the scripts that generate its numbers were also drafted by these agents
  > and revised by the authors, who checked the claims against the recorded data and take full responsibility for
  > the content. No AI system is an author.

- **Font warnings** (harmless, also present on arXiv): `T1/ptm/m/scit` and `TS1/ptm/m/sc` are substituted in the
  small-caps running head of `arxiv.sty`.
