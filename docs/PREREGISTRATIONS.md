# Pre-registrations of the follow-up studies (public commitments)

The follow-up studies of the paper are planned and pre-registered in the authors' private lab repository (to be
published with their results). To fix the content and the date of each registration in public before any confirmatory
data exist, this file records the sha256 of the registration and of its analysis script, and the commit of the private
repository where the complete registration first appears. When the private files are published, anyone can check that
their sha256 match this table and that the commit dates precede every result.

Rules the registrations follow: amendments are appended and dated, never rewritten above the "Amendments" heading;
the analysis script and its tests on synthetic data are committed before any result; held-out data is listed in a
SEALED file that only confirmatory runs may read (lab toolkit checks, gate G3).

| study | question | first complete commit (UTC) | latest registration commit | sha256 PREREG.md (latest) | sha256 analysis/primary.py |
|---|---|---|---|---|---|
| E2 `cogito-e2-evidence` | Does the agent's stop decision depend on the final screen? Screen-swap and instruction-swap minimal pairs | 4218c45, 2026-11-09 11:35 | 367c812, 2026-11-09 11:45 (amendment A1, no design change) | 589138932c546171c858c16d83a622815b49ee92f1f67dec8cffa77c3c9a2635 | 4726d3dc5ccc1b3afdd2a9f3f3d0b04185b1703a20ff77cecd353b01177b520c |
| E3 `cogito-e3-knowing` | Can the agent answer, when asked, the requirement it claimed done (per-requirement questions on the 268 frozen final screens)? | 032573c, 2026-11-09 12:08 | 032573c, 2026-11-09 12:08 | acaf085cebfb7f68930ba8f8716b17b84c600c4f68e457b3da2a6a9736d54da9 | 3faf3b8daeee535110c9af0094a825003470a0eeaf84fc152f6840522dc044d0 |
| Z2 `cogito-z2-labels` | What share of the paper's false "done" labels are not agent errors, and how many have the unmet requirement invisible on the final screen? (human rating) | cf192a1, 2026-11-09 11:24 | f7a89d7, 2026-11-09 11:40 | 0b9df3f63dcbbeda995f93e4081dc003fd317d6657bf4ba230ecefd13abfc329 | 73e08e69258b5bcddd1e94180c4a2fd83d7ec168dc0e8be363b539df7631e401 |

Also registered, in public: the three-arm guard attribution study
([experiments/online_guard/PREREG_GUARD_ATTRIBUTION.md](../experiments/online_guard/PREREG_GUARD_ATTRIBUTION.md)) and
its placebo-refusal supplement (`PREREG_GUARD_PLACEBO.md`, ComputerUseHackaton commit 8fc9c3e), and the one-shot use of
the never-read tasks (docs/FRESH_REGISTRATION.md, PR #1).

No confirmatory data of E2, E3 or Z2 existed when this file was written (2026-11-09): only CPU plumbing pilots on
development contexts with random or small models (E2, E3) and a model-rater pass that the human labels will be
compared to (Z2).
