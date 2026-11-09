# Expected output

Every command below was run on 2026-11-09 in a fresh clone of development commit [`08707a5`](https://github.com/martinbon39/ComputerUseHackaton/commit/08707a532478b8d7d6516cf3a584fa8ccc0520c3) (branch
`paper-repo` of the development repository). This repository's tree is that commit's tree plus the regenerated
`reproduce/EXPECTED_OUTPUT.md` and `docs/PROVENANCE.md`; only the link check reads them, and its output below is
that of the final tree. System Python 3.14.4, Linux x86-64,
CPU only, nothing installed. Every command exited 0 and `git status` stayed clean. CI runs the same checks on every
change to their inputs ([`reproduce.yml`](../.github/workflows/reproduce.yml), [`links.yml`](../.github/workflows/links.yml)).

```bash
git clone https://github.com/martinbon39/cogito-ergo-feci && cd cogito-ergo-feci
```

## `python3 reproduce/verify_results.py`, exit 0
The columns "92.5 vs 89.3" are sums of per-task scores over the n tasks.
```
== PRIMARY VERDICT (rule fixed before reading results): merge vs Modal-served original, Modal vs Modal ==
merge_cua_b050 vs orig_modal, reserve + test               n=165    92.5 vs   89.3  delta +1.94 pt  CI95 [ -4.3 ;  +8.0]  18 wins / 14 losses
  test only (120)                                          n=120    70.5 vs   70.3  delta +0.18 pt  CI95 [ -6.5 ;  +7.5]  11 wins / 10 losses
  reserve only (45)                                        n=45     22.0 vs   19.0  delta +6.64 pt  CI95 [ -6.7 ; +22.1]  7 wins / 4 losses

== Other arms and noise references ==
AlphaEdit broad_residual_p100 vs orig_modal, reserve       n=45     20.0 vs   19.0  delta +2.22 pt  CI95 [-13.3 ; +17.8]  7 wins / 6 losses
ExPO lambda=1.25 vs orig_pod, test                         n=120    70.3 vs   72.1  delta -1.50 pt  CI95 [ -8.9 ;  +5.7]  11 wins / 12 losses
merge_cua_b050 vs orig_pod, test                           n=120    70.5 vs   72.1  delta -1.33 pt  CI95 [ -8.9 ;  +6.4]  12 wins / 13 losses
-- noise: the same original model served by two backends --
orig_pod vs orig_modal, test                               n=120    72.1 vs   70.3  delta +1.51 pt  CI95 [ -4.5 ;  +7.6]  9 wins / 8 losses
orig_pod vs orig_modal, reserve                            n=45     21.0 vs   19.0  delta +4.44 pt  CI95 [ -6.7 ; +17.8]  5 wins / 3 losses

checks against the published values:
  OK  merge_cua_b050 vs orig_modal, reserve + test: +1.94 (expected +1.94, n=165)
  OK    test only (120): +0.18 (expected +0.18, n=120)
  OK    reserve only (45): +6.64 (expected +6.64, n=45)

Verdict rule: a gain is claimed only if the CI95 lower bound is > 0. Lower bound = -4.3 pt -> NO DETECTABLE GAIN
```

## `python3 reproduce/replay_guard.py --show 2`, exit 0
```
--- refusal 1: chrome/47543840
TASK: On the current website, show me the cars available for pickup at Boston Logan Intl Airport from the 10th to the 11th of next month, sorted by the number of seats to find the largest capacity.
  [v] Pickup location is Boston Logan Intl Airport: Pick-Up shows Boston Logan Intl Airport, BOS.
  [x] Dates are the 10th to 11th of next month (December, since today is Nov 8): Pick-up Tue, Nov 10 and return Wed, Nov 11 are shown. These are in the current month, not December.
  [v] Results sorted by number of seats, largest first: Sort by: Number of Seats (High to Low). The 12-Passenger Van is listed first, then the 7-seat Minivan.
  [v] Car list is displayed: Vehicle list with 21 vehicles is shown.
FEEDBACK TO THE AGENT: Verifier: requirement 'Rental dates must be the 10th to 11th of next month (December), not November.' is not satisfied on screen: The screen shows Pick-Up Tue, Nov 10, 12:00 PM and Return Wed, Nov 11, 12:00 PM. The current date is Nov 8, so next month is December. Click Modify Rental Details, set pick-up to Dec 10 and return to Dec 11 at Boston Logan, search again, and keep the sort on Number of Seats (High to Low). Continue the task.

--- refusal 2: chrome/9f3f70fc
TASK: Browse the list of women's Nike jerseys over $60.
  [v] Viewing Nike women's jerseys list: Nike FR search 'maillot femme (1115)' results page.
  [x] Price filter over $60 applied (or list limited to items > 60): URL has only q=maillot femme, no price filter; visible prices include 42,99 € (below 60); no price filter visible.
  [x] Results visible to browse: Page scrolled to footer; product grid is mostly empty/not visible.
FEEDBACK TO THE AGENT: Verifier: requirement 'Filter the women's jerseys to prices over $60 (about 60 €+)' is not satisfied on screen: URL is only q=maillot femme with no price filter, and a 42,99 € item is shown; the view is scrolled to the footer. Scroll up, open the Prix filter in the sidebar, select the over-60 range (or sort by price), and show the filtered product list. Continue the task.

Feci Guard replay: frozen feci_guard.check on 268 recorded final screens, recorded Claude Sonnet verdicts
  verifier sha 0af76fdb   decision kinds: {'complete': 202, 'incomplete': 66}
  false successes rejected (detection) : 45/66 = 68 %  Wilson95 [56-78]
  true successes rejected (false alarm): 21/202 = 10 %  Wilson95 [7-15]
  gap detection - false alarm         : +58 pts  task-bootstrap95 [+41, +74]
  OK  detected: 45 (expected 45)
  OK  false_success: 66 (expected 66)
  OK  wrongly_rejected: 21 (expected 21)
  OK  true_success: 202 (expected 202)
  OK  verifier_sha: 0af76fdb (expected 0af76fdb)
Matches the published judge-bench numbers.
```

## `python3 reproduce/recount_judges.py`, exit 0
```
manifest 268 268 90
A t0 lines 268 unique 268 in manifest 268
B lines 268 268 True
C lines 268 268 True
A FS 35 66 0.5303 [0.4116, 0.6457] TS 97 202 0.4802 [0.4123, 0.5488] invalid 3 3 gap 0.0501
  groups 90 boot CI -0.1341 0.2288
B FS 31 66 0.4697 [0.3543, 0.5884] TS 63 202 0.3119 [0.252, 0.3788] invalid 1 4 gap 0.1578
  groups 90 boot CI -0.0191 0.3388
C FS 45 66 0.6818 [0.5621, 0.7815] TS 21 202 0.104 [0.069, 0.1537] invalid 0 0 gap 0.5779
  groups 90 boot CI 0.4067 0.7366

judge                         detected      wrongly rejected   gap CI95 (task bootstrap, pts)
OK  Holo-3.1-4B (self-judge)    35/66         97/202             [-13, +23]  published [-13, +23]
OK  Holo4-27B                   31/66         63/202             [-2, +34]  published [-3, +33]
OK  Claude Sonnet (Feci Guard)  45/66         21/202             [+41, +74]  published [+41, +74]
268 episodes from 90 tasks; the bootstrap resamples tasks. Counts must match exactly; the CI bounds within 2 pts
(this recount uses its own seed, the published CIs come from judge_bench/analyze.py).
```

## `python3 reproduce/verify_online_guard.py`, exit 0
```
Online Feci Guard test, OSWorld test split, paired by task (bootstrap 10,000, seed 0)
  tasks: 120, excluded: 0
  false 'done' rate : original 22.5 % -> Guard 10.8 %   diff -11.7 pts CI95 [-19.2, -4.2]
  OSWorld score     : original 58.6 -> Guard 60.2   diff +1.6 pts CI95 [-4.4, +7.7]
  repaired B=8  true successes lost C=4  net=+4  false done avoided E=19
  criterion 1 (false done down): True   criterion 2 (score gain): False -> NO SCORE GAIN CLAIMED   rule 5 useful: True
Matches ONLINE_GUARD_RESULT.json exactly.
```

## `python3 reproduce/exact_reanalysis.py`, exit 0
Added 2026-11-09 with the exact re-analysis (branch `lab/z1-exact-reanalysis`), same machine and Python. "disagrees"
marks a claim whose bootstrap interval excludes 0 while both exact tests give p >= 0.05.
```
== Exact tests next to the paper's bootstrap intervals (points; p two-sided) ==
small = fewer than 10 clusters or fewer than 10 discordant units. flip = exact sign-flip randomisation over clusters;
sign = exact sign test on better/worse units (= exact McNemar when binary); Newcombe = paired score interval (binary only).

-- small-n claims --
claim                        location                      clu     b/w    est     bootstrap CI  p flip  p sign   mid-p         Newcombe  verdict
escalation_prim              sec/guard.tex:27                9     5/0  +50.0   [+22.0, +78.0]  0.0625  0.0625  0.0312                -  disagrees
escalation_strict            sec/guard.tex:27                8     4/0  +50.0   [+13.0, +88.0]  0.1250  0.1250  0.0625                -  disagrees
escalation_all               sec/guard.tex:27               12     5/1  +33.3    [+4.0, +63.0]  0.0938  0.2188  0.1250                -  disagrees
repair                       sec/guard.tex:25                9     2/0  +16.7    [+0.0, +44.0]  0.5000  0.5000  0.2500                -  agrees
repair_all                   sec/guard.tex:25               12     2/0  +12.5    [+0.0, +33.0]  0.5000  0.5000  0.2500                -  agrees
guard_v2_det                 sec/guard.tex:10               16     4/0  +13.8    [+3.0, +30.0]  0.1250  0.1250  0.0625    [+1.3, +25.6]  disagrees
onReserveExpo                sec/interventions.tex:101      44     3/4   -2.3    [-13.6, +9.1]  1.0000  1.0000  0.7266                -  agrees
onReserveLmrow               generated/tab_b4_heldout.tex   14     2/4  -14.3   [-50.0, +21.4]  0.6875  0.6875  0.4531                -  agrees
onReservePrompt              generated/tab_b4_heldout.tex   20     1/2   -5.0   [-20.0, +10.0]  1.0000  1.0000  0.6250                -  agrees
onTestPrompt                 generated/tab_b4_heldout.tex   38     4/1   +5.3    [-5.1, +15.9]  0.3750  0.3750  0.2188                -  agrees
onNoise                      sec/interventions.tex:101      44     3/4   -2.3    [-13.6, +9.1]  1.0000  1.0000  0.7266                -  agrees
onNoiseServer                sec/interventions.tex:101      45     5/3   +4.4    [-6.7, +17.8]  0.7266  0.7266  0.5078                -  agrees
cohort_B-A_fs+               sec/interventions.tex:96       19     1/4  -10.5    [-25.0, +0.0]  0.2500  0.3750  0.2188                -  agrees
cohort_B-A_fs-               sec/interventions.tex:96       20     0/5  -11.2    [-22.5, -2.5]  0.0625  0.0625  0.0312                -  disagrees
cohort_C-A_fs-               sec/interventions.tex:96       20     1/5   -8.8    [-18.8, +0.0]  0.1562  0.2188  0.1250                -  agrees
cohort_D-A_fs+               sec/interventions.tex:96       19     7/0  +15.8    [+5.3, +27.6]  0.0156  0.0156  0.0078                -  agrees
cohort_D-A_fs-               sec/interventions.tex:96       20     1/1   +0.0     [-3.7, +3.7]  1.0000  1.0000  1.0000                -  agrees

-- other paired claims (multiplicity families) --
claim                        location                      clu     b/w    est     bootstrap CI  p flip  p sign   mid-p         Newcombe  verdict
guard_v2_rej                 sec/guard.tex:10               40    10/5   +4.3    [-5.0, +15.0]  0.5391  0.3018  0.2101    [-2.4, +11.3]  agrees
onReserveCua                 sec/interventions.tex:101      45     7/4   +6.6    [-6.7, +22.1]  0.5488  0.5488  0.3877                -  agrees
onReserveBroad               sec/interventions.tex:101      45     7/6   +2.2   [-13.3, +17.8]  1.0000  1.0000  0.7905                -  agrees
onTestExpo                   sec/interventions.tex:104     120   11/12   -1.5     [-8.9, +5.7]  0.7217  1.0000  0.8388                -  agrees
onTestCua                    sec/interventions.tex:103     120   11/10   +0.2     [-6.5, +7.5]  0.8841  1.0000  0.8318                -  agrees
onAllCua                     sec/interventions.tex:81      165   18/14   +1.9     [-4.3, +8.0]  0.5068  0.5966  0.4869                -  agrees
onTestNoiseServer            sec/interventions.tex:103     120     9/8   +1.5     [-4.5, +7.6]  0.7185  1.0000  0.8145                -  agrees
guard_online_fd_orig_modal   sec/guard.tex:12              120    5/19  -11.7    [-19.2, -4.2]  0.0066  0.0066  0.0041    [-19.7, -3.9]  agrees
guard_online_score_orig_moda sec/guard.tex:12              120    10/7   +1.6     [-4.4, +7.7]  0.6148  0.6291  0.4807                -  agrees
guard_online_fd_orig_pod     sec/guard.tex:12              120    4/20  -13.3    [-20.8, -5.8]  0.0015  0.0015  0.0009    [-21.2, -5.7]  agrees
guard_online_score_orig_pod  sec/guard.tex:12              120    10/9   +0.1     [-6.5, +6.6]  0.9755  1.0000  0.8238                -  agrees
cohort_B-A_selectivity       sec/interventions.tex:96       39       -   +0.7   [-16.1, +16.3]  1.0000     -       -                  -  agrees
cohort_C-A_fs+               sec/interventions.tex:96       19     1/9  -17.1    [-28.9, -6.6]  0.0137  0.0215  0.0117                -  agrees
cohort_C-A_selectivity       sec/interventions.tex:96       39       -   -8.4    [-22.6, +5.9]  0.3154     -       -                  -  agrees
cohort_D-A_selectivity       sec/interventions.tex:96       39       -  +15.8    [+5.3, +27.7]  0.0088     -       -                  -  agrees
cohort_C-D_fs+               sec/interventions.tex:96       19    0/12  -32.9   [-47.4, -19.7]  0.0005  0.0005  0.0002                -  agrees

== Holm-adjusted p-values (exact sign-flip / permutation p) ==
-- family A_online_arms (9 tests) --
  onReserveExpo                    p 1.0000  Holm 1.0000
  onReserveLmrow                   p 0.6875  Holm 1.0000
  onReservePrompt                  p 1.0000  Holm 1.0000
  onReserveCua                     p 0.5488  Holm 1.0000
  onReserveBroad                   p 1.0000  Holm 1.0000
  onTestExpo                       p 0.7217  Holm 1.0000
  onTestPrompt                     p 0.3750  Holm 1.0000
  onTestCua                        p 0.8841  Holm 1.0000
  onAllCua                         p 0.5068  Holm 1.0000
-- family B_cohort_false_completions (4 tests) --
  cohort_B-A_fs+                   p 0.2500  Holm 0.2500
  cohort_C-A_fs+                   p 0.0137  Holm 0.0410
  cohort_D-A_fs+                   p 0.0156  Holm 0.0410
  cohort_C-D_fs+                   p 0.0005  Holm 0.0020
-- family C_cohort_selectivity (3 tests) --
  cohort_B-A_selectivity           p 1.0000  Holm 1.0000
  cohort_C-A_selectivity           p 0.3154  Holm 0.6308
  cohort_D-A_selectivity           p 0.0088  Holm 0.0263

Disagreements (bootstrap interval vs exact tests): escalation_prim, escalation_strict, escalation_all, guard_v2_det, cohort_B-A_fs-
  OK  escalation primary: 5 better, 0 worse, exact p = 0.0625
  OK  guard v2 detection: 4 against 0 discordant, exact McNemar p = 0.125
  OK  guard v2 false rejection: 10 against 5 discordant
  OK  every recomputed point estimate equals the paper's
EXACT RE-ANALYSIS OK
```

## `python3 reproduce/fresh_tasks.py`, exit 0
Added 2026-11-09 with the FRESH-115 registration ([`docs/FRESH_REGISTRATION.md`](../docs/FRESH_REGISTRATION.md)).
```
OSWorld test_nogdrive 361 tasks = DIAG 120 + TEST 120 + unsplit 121 (splits regenerated by the frozen rule: identical)
unsplit tasks named by a project file (pilot runs): 6
FRESH-115: 115 tasks, sha256 0e76f29147e6c1d45983a8b4d01e728c81047cf3f107a44ab06f18abc35d16a7
  domains: multi_apps 31, libreoffice_impress 17, libreoffice_calc 16, chrome 15, gimp 7, os 7, libreoffice_writer 6, vs_code 6, thunderbird 5, vlc 5
  OK  equals docs/FRESH_TASKS.json
```

## `python3 reproduce/check_links.py`, exit 0
```
231 relative links checked in 161 documents, 0 broken
```

## `bash reproduce/run_all.sh`, exit 0
Steps (5) and (6) added 2026-11-09.
```
== (1) OSWorld paired comparisons of the weight edits, recomputed from per-task scores ==
== PRIMARY VERDICT (rule fixed before reading results): merge vs Modal-served original, Modal vs Modal ==
merge_cua_b050 vs orig_modal, reserve + test               n=165    92.5 vs   89.3  delta +1.94 pt  CI95 [ -4.3 ;  +8.0]  18 wins / 14 losses
  test only (120)                                          n=120    70.5 vs   70.3  delta +0.18 pt  CI95 [ -6.5 ;  +7.5]  11 wins / 10 losses
  reserve only (45)                                        n=45     22.0 vs   19.0  delta +6.64 pt  CI95 [ -6.7 ; +22.1]  7 wins / 4 losses

== Other arms and noise references ==
AlphaEdit broad_residual_p100 vs orig_modal, reserve       n=45     20.0 vs   19.0  delta +2.22 pt  CI95 [-13.3 ; +17.8]  7 wins / 6 losses
ExPO lambda=1.25 vs orig_pod, test                         n=120    70.3 vs   72.1  delta -1.50 pt  CI95 [ -8.9 ;  +5.7]  11 wins / 12 losses
merge_cua_b050 vs orig_pod, test                           n=120    70.5 vs   72.1  delta -1.33 pt  CI95 [ -8.9 ;  +6.4]  12 wins / 13 losses
-- noise: the same original model served by two backends --
orig_pod vs orig_modal, test                               n=120    72.1 vs   70.3  delta +1.51 pt  CI95 [ -4.5 ;  +7.6]  9 wins / 8 losses
orig_pod vs orig_modal, reserve                            n=45     21.0 vs   19.0  delta +4.44 pt  CI95 [ -6.7 ; +17.8]  5 wins / 3 losses

checks against the published values:
  OK  merge_cua_b050 vs orig_modal, reserve + test: +1.94 (expected +1.94, n=165)
  OK    test only (120): +0.18 (expected +0.18, n=120)
  OK    reserve only (45): +6.64 (expected +6.64, n=45)

Verdict rule: a gain is claimed only if the CI95 lower bound is > 0. Lower bound = -4.3 pt -> NO DETECTABLE GAIN

== (2) Feci Guard replayed on 268 recorded episodes (frozen decision code, recorded verdicts) ==
--- refusal 1: chrome/47543840
TASK: On the current website, show me the cars available for pickup at Boston Logan Intl Airport from the 10th to the 11th of next month, sorted by the number of seats to find the largest capacity.
  [v] Pickup location is Boston Logan Intl Airport: Pick-Up shows Boston Logan Intl Airport, BOS.
  [x] Dates are the 10th to 11th of next month (December, since today is Nov 8): Pick-up Tue, Nov 10 and return Wed, Nov 11 are shown. These are in the current month, not December.
  [v] Results sorted by number of seats, largest first: Sort by: Number of Seats (High to Low). The 12-Passenger Van is listed first, then the 7-seat Minivan.
  [v] Car list is displayed: Vehicle list with 21 vehicles is shown.
FEEDBACK TO THE AGENT: Verifier: requirement 'Rental dates must be the 10th to 11th of next month (December), not November.' is not satisfied on screen: The screen shows Pick-Up Tue, Nov 10, 12:00 PM and Return Wed, Nov 11, 12:00 PM. The current date is Nov 8, so next month is December. Click Modify Rental Details, set pick-up to Dec 10 and return to Dec 11 at Boston Logan, search again, and keep the sort on Number of Seats (High to Low). Continue the task.

Feci Guard replay: frozen feci_guard.check on 268 recorded final screens, recorded Claude Sonnet verdicts
  verifier sha 0af76fdb   decision kinds: {'complete': 202, 'incomplete': 66}
  false successes rejected (detection) : 45/66 = 68 %  Wilson95 [56-78]
  true successes rejected (false alarm): 21/202 = 10 %  Wilson95 [7-15]
  gap detection - false alarm         : +58 pts  task-bootstrap95 [+41, +74]
  OK  detected: 45 (expected 45)
  OK  false_success: 66 (expected 66)
  OK  wrongly_rejected: 21 (expected 21)
  OK  true_success: 202 (expected 202)
  OK  verifier_sha: 0af76fdb (expected 0af76fdb)
Matches the published judge-bench numbers.

== (3) the three judges recounted from their raw responses ==
judge                         detected      wrongly rejected   gap CI95 (task bootstrap, pts)
OK  Holo-3.1-4B (self-judge)    35/66         97/202             [-13, +23]  published [-13, +23]
OK  Holo4-27B                   31/66         63/202             [-2, +34]  published [-3, +33]
OK  Claude Sonnet (Feci Guard)  45/66         21/202             [+41, +74]  published [+41, +74]
268 episodes from 90 tasks; the bootstrap resamples tasks. Counts must match exactly; the CI bounds within 2 pts
(this recount uses its own seed, the published CIs come from judge_bench/analyze.py).

== (4) online Feci Guard test, 120 OSWorld tasks ==
Online Feci Guard test, OSWorld test split, paired by task (bootstrap 10,000, seed 0)
  tasks: 120, excluded: 0
  false 'done' rate : original 22.5 % -> Guard 10.8 %   diff -11.7 pts CI95 [-19.2, -4.2]
  OSWorld score     : original 58.6 -> Guard 60.2   diff +1.6 pts CI95 [-4.4, +7.7]
  repaired B=8  true successes lost C=4  net=+4  false done avoided E=19
  criterion 1 (false done down): True   criterion 2 (score gain): False -> NO SCORE GAIN CLAIMED   rule 5 useful: True
Matches ONLINE_GUARD_RESULT.json exactly.

== (5) exact small-sample tests and Holm-adjusted p-values next to the paper's bootstrap intervals ==
== Exact tests next to the paper's bootstrap intervals (points; p two-sided) ==
small = fewer than 10 clusters or fewer than 10 discordant units. flip = exact sign-flip randomisation over clusters;
sign = exact sign test on better/worse units (= exact McNemar when binary); Newcombe = paired score interval (binary only).

-- small-n claims --
claim                        location                      clu     b/w    est     bootstrap CI  p flip  p sign   mid-p         Newcombe  verdict
escalation_prim              sec/guard.tex:27                9     5/0  +50.0   [+22.0, +78.0]  0.0625  0.0625  0.0312                -  disagrees
escalation_strict            sec/guard.tex:27                8     4/0  +50.0   [+13.0, +88.0]  0.1250  0.1250  0.0625                -  disagrees
escalation_all               sec/guard.tex:27               12     5/1  +33.3    [+4.0, +63.0]  0.0938  0.2188  0.1250                -  disagrees
repair                       sec/guard.tex:25                9     2/0  +16.7    [+0.0, +44.0]  0.5000  0.5000  0.2500                -  agrees
repair_all                   sec/guard.tex:25               12     2/0  +12.5    [+0.0, +33.0]  0.5000  0.5000  0.2500                -  agrees
guard_v2_det                 sec/guard.tex:10               16     4/0  +13.8    [+3.0, +30.0]  0.1250  0.1250  0.0625    [+1.3, +25.6]  disagrees
onReserveExpo                sec/interventions.tex:101      44     3/4   -2.3    [-13.6, +9.1]  1.0000  1.0000  0.7266                -  agrees
onReserveLmrow               generated/tab_b4_heldout.tex   14     2/4  -14.3   [-50.0, +21.4]  0.6875  0.6875  0.4531                -  agrees
onReservePrompt              generated/tab_b4_heldout.tex   20     1/2   -5.0   [-20.0, +10.0]  1.0000  1.0000  0.6250                -  agrees
onTestPrompt                 generated/tab_b4_heldout.tex   38     4/1   +5.3    [-5.1, +15.9]  0.3750  0.3750  0.2188                -  agrees
onNoise                      sec/interventions.tex:101      44     3/4   -2.3    [-13.6, +9.1]  1.0000  1.0000  0.7266                -  agrees
onNoiseServer                sec/interventions.tex:101      45     5/3   +4.4    [-6.7, +17.8]  0.7266  0.7266  0.5078                -  agrees
cohort_B-A_fs+               sec/interventions.tex:96       19     1/4  -10.5    [-25.0, +0.0]  0.2500  0.3750  0.2188                -  agrees
cohort_B-A_fs-               sec/interventions.tex:96       20     0/5  -11.2    [-22.5, -2.5]  0.0625  0.0625  0.0312                -  disagrees
cohort_C-A_fs-               sec/interventions.tex:96       20     1/5   -8.8    [-18.8, +0.0]  0.1562  0.2188  0.1250                -  agrees
cohort_D-A_fs+               sec/interventions.tex:96       19     7/0  +15.8    [+5.3, +27.6]  0.0156  0.0156  0.0078                -  agrees
cohort_D-A_fs-               sec/interventions.tex:96       20     1/1   +0.0     [-3.7, +3.7]  1.0000  1.0000  1.0000                -  agrees

-- other paired claims (multiplicity families) --
claim                        location                      clu     b/w    est     bootstrap CI  p flip  p sign   mid-p         Newcombe  verdict
guard_v2_rej                 sec/guard.tex:10               40    10/5   +4.3    [-5.0, +15.0]  0.5391  0.3018  0.2101    [-2.4, +11.3]  agrees
onReserveCua                 sec/interventions.tex:101      45     7/4   +6.6    [-6.7, +22.1]  0.5488  0.5488  0.3877                -  agrees
onReserveBroad               sec/interventions.tex:101      45     7/6   +2.2   [-13.3, +17.8]  1.0000  1.0000  0.7905                -  agrees
onTestExpo                   sec/interventions.tex:104     120   11/12   -1.5     [-8.9, +5.7]  0.7217  1.0000  0.8388                -  agrees
onTestCua                    sec/interventions.tex:103     120   11/10   +0.2     [-6.5, +7.5]  0.8841  1.0000  0.8318                -  agrees
onAllCua                     sec/interventions.tex:81      165   18/14   +1.9     [-4.3, +8.0]  0.5068  0.5966  0.4869                -  agrees
onTestNoiseServer            sec/interventions.tex:103     120     9/8   +1.5     [-4.5, +7.6]  0.7185  1.0000  0.8145                -  agrees
guard_online_fd_orig_modal   sec/guard.tex:12              120    5/19  -11.7    [-19.2, -4.2]  0.0066  0.0066  0.0041    [-19.7, -3.9]  agrees
guard_online_score_orig_moda sec/guard.tex:12              120    10/7   +1.6     [-4.4, +7.7]  0.6148  0.6291  0.4807                -  agrees
guard_online_fd_orig_pod     sec/guard.tex:12              120    4/20  -13.3    [-20.8, -5.8]  0.0015  0.0015  0.0009    [-21.2, -5.7]  agrees
guard_online_score_orig_pod  sec/guard.tex:12              120    10/9   +0.1     [-6.5, +6.6]  0.9755  1.0000  0.8238                -  agrees
cohort_B-A_selectivity       sec/interventions.tex:96       39       -   +0.7   [-16.1, +16.3]  1.0000     -       -                  -  agrees
cohort_C-A_fs+               sec/interventions.tex:96       19     1/9  -17.1    [-28.9, -6.6]  0.0137  0.0215  0.0117                -  agrees
cohort_C-A_selectivity       sec/interventions.tex:96       39       -   -8.4    [-22.6, +5.9]  0.3154     -       -                  -  agrees
cohort_D-A_selectivity       sec/interventions.tex:96       39       -  +15.8    [+5.3, +27.7]  0.0088     -       -                  -  agrees
cohort_C-D_fs+               sec/interventions.tex:96       19    0/12  -32.9   [-47.4, -19.7]  0.0005  0.0005  0.0002                -  agrees

== Holm-adjusted p-values (exact sign-flip / permutation p) ==
-- family A_online_arms (9 tests) --
  onReserveExpo                    p 1.0000  Holm 1.0000
  onReserveLmrow                   p 0.6875  Holm 1.0000
  onReservePrompt                  p 1.0000  Holm 1.0000
  onReserveCua                     p 0.5488  Holm 1.0000
  onReserveBroad                   p 1.0000  Holm 1.0000
  onTestExpo                       p 0.7217  Holm 1.0000
  onTestPrompt                     p 0.3750  Holm 1.0000
  onTestCua                        p 0.8841  Holm 1.0000
  onAllCua                         p 0.5068  Holm 1.0000
-- family B_cohort_false_completions (4 tests) --
  cohort_B-A_fs+                   p 0.2500  Holm 0.2500
  cohort_C-A_fs+                   p 0.0137  Holm 0.0410
  cohort_D-A_fs+                   p 0.0156  Holm 0.0410
  cohort_C-D_fs+                   p 0.0005  Holm 0.0020
-- family C_cohort_selectivity (3 tests) --
  cohort_B-A_selectivity           p 1.0000  Holm 1.0000
  cohort_C-A_selectivity           p 0.3154  Holm 0.6308
  cohort_D-A_selectivity           p 0.0088  Holm 0.0263

Disagreements (bootstrap interval vs exact tests): escalation_prim, escalation_strict, escalation_all, guard_v2_det, cohort_B-A_fs-
  OK  escalation primary: 5 better, 0 worse, exact p = 0.0625
  OK  guard v2 detection: 4 against 0 discordant, exact McNemar p = 0.125
  OK  guard v2 false rejection: 10 against 5 discordant
  OK  every recomputed point estimate equals the paper's
EXACT RE-ANALYSIS OK

== (6) FRESH-115: the never-read OSWorld tasks kept for one confirmatory run ==
OSWorld test_nogdrive 361 tasks = DIAG 120 + TEST 120 + unsplit 121 (splits regenerated by the frozen rule: identical)
unsplit tasks named by a project file (pilot runs): 6
FRESH-115: 115 tasks, sha256 0e76f29147e6c1d45983a8b4d01e728c81047cf3f107a44ab06f18abc35d16a7
  domains: multi_apps 31, libreoffice_impress 17, libreoffice_calc 16, chrome 15, gimp 7, os 7, libreoffice_writer 6, vs_code 6, thunderbird 5, vlc 5
  OK  equals docs/FRESH_TASKS.json

ALL CHECKS OK: (1)-(6) match the numbers reported in the paper.
```

## `python3 reproduce/check_paths.py`, exit 0
```
59 cross-folder script paths checked, 0 unresolved
```

## Level 2
Run on 2026-11-08 at about 10:05 UTC in a fresh clone of development commit [`6bb899f`](https://github.com/martinbon39/ComputerUseHackaton/commit/6bb899f4b2d824237c6d1f42700a21dfdd33ad24), before the repository was restructured
(`reproduce/guard_live.py` was then at its old path; its logic is unchanged).
`python3 reproduce/guard_live.py` uses the `claude` CLI (Claude Code, logged in) for fresh verifier calls. Both live
decisions matched the recorded ones. The `--api` path (Anthropic key through the OpenAI-compatible endpoint) was
**not run**, because no key was on the machine.

Default episode (a false success), exit 0:
```
episode  : diag1__chrome__47543840-672a-467d-80df-8f7c3b9788c9
label    : false_success (official OSWorld evaluator)
TASK     : On the current website, show me the cars available for pickup at Boston Logan Intl Airport from the 10th to the 11th of next month, sorted by the number of seats to find the largest capacity.
live     : REJECT (incomplete)  [claude:sonnet, 7.6 s, error=None]
  [v] Pickup location is Boston Logan Intl Airport: Pick-Up shows Boston Logan Intl Airport, BOS.
  [x] Dates are the 10th to the 11th of NEXT month (today is Nov 8, so Dec 10 to Dec 11): The page shows Tue, Nov 10, 12:00 PM to Wed, Nov 11, 12:00 PM. That is the current month, not next month.
  [v] Results sorted by number of seats, largest first: Sort by: Number of Seats (High to Low). The 12-Passenger Van is listed first.
  [v] Car list is displayed: The list shows All Vehicles (21), starting with the 12-Passenger Van and the Minivan.
feedback : Verifier: requirement 'The rental dates must be the 10th to the 11th of next month (Dec 10 to Dec 11), not Nov 10 to Nov 11.' is not satisfied on screen: The pick-up is Tue, Nov 10 and the return is Wed, Nov 11. Today is Nov 8, so these dates fall in the current month. Click Modify Rental Details, set pickup to Dec 10 and return to Dec 11 at Boston Logan, then search again. Keep the sort on Number of Seats (High to Low). Continue the task.
recorded : INCOMPLETE -> reject   same decision: True
```

`--episode diag1__chrome__0d8b7de3-e8de-4d86-b9fd-dd2dce58a217` (a true success), exit 0:
```
episode  : diag1__chrome__0d8b7de3-e8de-4d86-b9fd-dd2dce58a217
label    : true_success (official OSWorld evaluator)
TASK     : Browse the natural products database.
live     : ACCEPT (complete)  [claude:sonnet, 4.7 s, error=None]
  [v] Browser shows a natural products database: Chrome is on drugs.com/npc/ with the heading 'Natural Product Information (Consumer)'.
  [v] Browsing content (A-Z listing) is visible: The 'Browse A-Z' letter links and the product listings (5-Hydroxytryptophan, Acai, Aortic Extract) are visible.
recorded : COMPLETE -> accept   same decision: True
```

## Oldest supported Python
Same clone, Python 3.9.25 (`uv run --python 3.9 --no-project`): `bash reproduce/run_all.sh` ended with "ALL CHECKS OK",
and `python reproduce/check_links.py` reported 0 broken links.
