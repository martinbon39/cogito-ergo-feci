#!/usr/bin/env python3
"""Exact small-sample tests next to the paper's bootstrap intervals, and Holm-adjusted p-values.

For every paired claim of the paper that rests on fewer than 10 clusters or fewer than 10 discordant units, and for the
online arms and the feasible-cohort contrasts (multiplicity families), this script recomputes from committed per-unit
data: the discordant counts, an exact sign test (exact McNemar when the outcome is binary) with its mid-p, an exact
sign-flip randomisation test over clusters, and, for binary outcomes, Newcombe's hybrid score interval for a paired
difference (method 10, Newcombe 1998). The bootstrap interval shown is the paper's own, read from paper/generated/.
A claim "agrees" when the bootstrap interval excludes 0 exactly when the exact tests give p < 0.05.

Standard library only, relative paths, reads only files of this repository. Exit 1 if a recomputed point estimate
differs from the paper or a reference value below changes. paper/figs/exact.py imports `compute()`.
"""
import csv
import json
import math
import pathlib
import re
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
DATA = PAPER / "data"
ALPHA = 0.05
SMALL = 10


def macros():
    out = {}
    for f in sorted((PAPER / "generated").glob("num_*.tex")):
        for line in f.read_text().splitlines():
            m = re.match(r"\\newcommand\{\\(\w+)\}\{(.*?)\} % source:", line)
            if m:
                out[m.group(1)] = m.group(2)
    return out


def where(name, fallback="generated/tab_b4_heldout.tex (Table tab:b4-heldout)"):
    """First use of macro `name` in the arXiv sections, as sec/<file>.tex:<line>; else the generated table holding it."""
    for f in sorted((PAPER / "sec").glob("*.tex")) + [PAPER / "neurips/body.tex"]:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if re.search(r"\\" + name + r"(?![A-Za-z])", line):
                return f"{f.relative_to(PAPER)}:{i}"
    return fallback


def num(s):
    return float(s.replace("$-$", "-").replace("{,}", "").replace("+", ""))


def ci_of(s):
    a, b = re.split(r" to |--", s)
    return num(a), num(b)


# ---------------------------------------------------------------- exact tests

def binom_two_sided(b, c):
    """Exact two-sided sign test on b successes against c failures (exact McNemar), and its mid-p."""
    n, k = b + c, min(b, c)
    if n == 0:
        return 1.0, 1.0
    pk = [math.comb(n, i) / 2 ** n for i in range(n + 1)]
    p = min(1.0, 2 * sum(pk[: k + 1]))
    mid = min(1.0, 2 * (sum(pk[:k]) + 0.5 * pk[k])) if b != c else 1.0
    return p, mid


def _scale(values):
    """Integer weights proportional to `values`: exact for rational scores, else rounded to 1/1000."""
    fr = [Fraction(v).limit_denominator(64) for v in values]
    if all(abs(float(f) - v) < 1e-12 for f, v in zip(fr, values)):
        den = 1
        for f in fr:
            den = den * f.denominator // math.gcd(den, f.denominator)
        return [int(f * den) for f in fr], "exact"
    return [round(1000 * v) for v in values], "exact on values rounded to 0.001"


def signflip_p(cluster_diffs):
    """Exact two-sided sign-flip randomisation p over clusters: P(|sum of +-d_c| >= |observed sum|)."""
    w, how = _scale([d for d in cluster_diffs if abs(d) > 1e-12])
    obs = abs(sum(w))
    dist = {0: 1.0}
    for x in w:
        nxt = {}
        for s, p in dist.items():
            nxt[s + x] = nxt.get(s + x, 0.0) + p / 2
            nxt[s - x] = nxt.get(s - x, 0.0) + p / 2
        dist = nxt
    return min(1.0, sum(p for s, p in dist.items() if abs(s) >= obs)), how


def label_perm_p(group1, group2):
    """Exact two-sided permutation p for mean(group1) - mean(group2) (stratum labels permuted over clusters)."""
    w, how = _scale(list(group1) + list(group2))
    n1, n2 = len(group1), len(group2)
    tot = sum(w)
    obs = abs(sum(w[:n1]) * n2 - (tot - sum(w[:n1])) * n1)
    dist = [dict() for _ in range(n1 + 1)]
    dist[0][0] = 1
    for x in w:
        for k in range(n1, 0, -1):
            for s, c in dist[k - 1].items():
                dist[k][s + x] = dist[k].get(s + x, 0) + c
    allc = sum(dist[n1].values())
    hit = sum(c for s, c in dist[n1].items() if abs(s * n2 - (tot - s) * n1) >= obs)
    return hit / allc, how


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def newcombe(a, b, c, d):
    """Newcombe (1998) method 10: 95% CI of p1 - p2 for paired binary data.
    a = both 1, b = first 1 only, c = second 1 only, d = both 0; p1 = (a+b)/n, p2 = (a+c)/n."""
    n = a + b + c + d
    p1, p2 = (a + b) / n, (a + c) / n
    l1, u1 = wilson(a + b, n)
    l2, u2 = wilson(a + c, n)
    den = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    phi = (a * d - b * c) / den if den else 0.0
    dl = math.sqrt(max(0.0, (p1 - l1) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2) + (u2 - p2) ** 2))
    du = math.sqrt(max(0.0, (u1 - p1) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2) + (p2 - l2) ** 2))
    return p1 - p2 - dl, p1 - p2 + du


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        adj[i] = run
    return adj


# ---------------------------------------------------------------- per-unit data

def online_runs():
    """Per-task scores of every online run, read as figs/online.py reads them (result.txt per task)."""
    base = DATA / "local/online"
    runs = {}
    for d in sorted(base.glob("results_*")):
        out = {}
        for f in d.rglob("result.txt"):
            if "_jobs" not in f.parts:
                out[f.parts[-2]] = float(f.read_text().strip())
        runs[d.name] = out
    return runs


def paired_units(a, b, exclude=()):
    keys = sorted((set(a) & set(b)) - set(exclude))
    return {k: [(a[k], b[k])] for k in keys}


def claim(name, label, loc_macro, ci_macro, est_macro, clusters, kind, M, note=""):
    """clusters: {cluster: [(arm_value, reference_value), ...]} for paired units. kind: 'binary' or 'score'."""
    units = [u for v in clusters.values() for u in v]
    diffs = [x - y for x, y in units]
    better, worse = sum(d > 0 for d in diffs), sum(d < 0 for d in diffs)
    p_sign, p_mid = binom_two_sided(better, worse)
    p_flip, how = signflip_p([sum(x - y for x, y in v) for v in clusters.values()])
    est = 100 * sum(diffs) / len(diffs)
    lo, hi = ci_of(M[ci_macro])
    row = {"claim": name, "label": label, "location": where(loc_macro), "macro": ci_macro, "kind": kind,
           "clusters": len(clusters), "units": len(units), "better": better, "worse": worse,
           "estimate": est, "paper_estimate": num(M[est_macro]) if est_macro else None, "est_macro": est_macro,
           "boot_lo": lo, "boot_hi": hi, "p_sign": p_sign, "p_mid": p_mid, "p_flip": p_flip, "flip_method": how,
           "note": note}
    if kind == "binary":
        a = sum(x == 1 and y == 1 for x, y in units)
        b = sum(x == 1 and y == 0 for x, y in units)
        c = sum(x == 0 and y == 1 for x, y in units)
        d = sum(x == 0 and y == 0 for x, y in units)
        assert a + b + c + d == len(units), name
        row["newcombe"] = [100 * v for v in newcombe(a, b, c, d)]
    row["small"] = len(clusters) < SMALL or better + worse < SMALL
    boot_sig = lo > 0 or hi < 0
    exact_sig = [p_flip < ALPHA, p_sign < ALPHA]
    row["boot_sig"] = boot_sig
    row["verdict"] = ("agrees" if all(e == boot_sig for e in exact_sig)
                      else "disagrees" if all(e != boot_sig for e in exact_sig) else "mixed")
    return row


def compute():
    M = macros()
    rows = []

    # Escalation to Holo4-27B, replay (rescue_bench): episode = cluster, unit = episode mean over its K=2 branches.
    rb = json.loads((DATA / "local/rescue_bench/RESULT.json").read_text())
    sets = {"Prim": lambda v: not v["exclusion"], "Strict": lambda v: not v["exclusion"] and not v["strict_boundary_exclusion"],
            "All": lambda v: True}
    for tag, keep in sets.items():
        cl = {t: [(sum(b["score"] for b in v["guard"]) / len(v["guard"]), sum(b["score"] for b in v["control"]) / len(v["control"]))]
              for t, v in rb["per_episode"].items() if keep(v)}
        assert len(cl) == int(M[f"rb{tag}Episodes"]), tag
        rows.append(claim("escalation_" + dict(Prim="prim", Strict="strict", All="all")[tag], f"Guard + escalation to Holo4-27B vs Holo4-27B alone, replay ({dict(Prim='primary', Strict='strict replay check', All='all episodes')[tag]})",
                          f"rb{tag}Diff", f"rb{tag}DiffCi", f"rb{tag}Diff", cl, "score",
                          M, "unit = episode mean over 2 branches"))

    # Repair by Holo-3.1 with the guard, replay (feci_guard/repair).
    rp = json.loads((DATA / "local/feci_guard/repair/final/results.json").read_text())
    for tag, keep in [("", lambda v: not v["excluded"]), ("All", lambda v: True)]:
        cl = {t: [(sum(v["guard"]) / len(v["guard"]), sum(v["nog"]) / len(v["nog"]))] for t, v in rp["per_episode"].items() if keep(v)}
        rows.append(claim("repair" + ("_all" if tag else ""), "Guard repair by Holo-3.1 vs no guard, replay" + (" (all episodes)" if tag else ""),
                          f"fgRepDiff{tag}", f"fgRepDiff{tag}Ci", f"fgRepDiff{tag}", cl, "score", M, "unit = episode mean over 2 branches"))

    # Guard v2 vs v1 on the held-out half: episode verdicts, clustered by task.
    v2d = DATA / "local/feci_guard/v2"
    man = {e["episode_id"]: e for e in json.loads((DATA / "local/judge_bench/verif_study_manifest.json").read_text())}
    hold = set(json.loads((v2d / "SPLIT.json").read_text())["holdout"])

    def verdicts(p):
        out = {}
        for x in p.read_text().splitlines():
            j = json.loads(x)
            if j["episode_id"] in hold:
                out[j["episode_id"]] = int(j["result"].get("verdict") == "INCOMPLETE")
        return out
    v1 = verdicts(DATA / "local/judge_bench/claude_responses.jsonl")
    v2 = verdicts(v2d / "runs/ab_holdout.jsonl")
    for lab, tag, what in [("false_success", "Det", "detection of false successes"), ("true_success", "Rej", "false rejection of true successes")]:
        cl = {}
        for e in sorted(hold):
            if man[e]["label"] == lab:
                cl.setdefault((man[e]["domain"], man[e]["task_id"]), []).append((v2[e], v1[e]))
        rows.append(claim(f"guard_v2_{tag.lower()}", f"Guard v2 vs v1, held-out half, {what}", f"gv{tag}Diff", f"gv{tag}DiffCi",
                          f"gv{tag}Diff", cl, "binary", M, "cluster = task; Newcombe ignores clustering"))

    # Online OSWorld arms (Table b4_heldout): per-task scores, paired by task.
    R = online_runs()
    sr = {"res_orig": "results_val_orig_eager_m40", "res_orig_gh": "results_confirm_gh_orig_confirm",
          "res_expo": "results_val_patched_eager_m40", "res_lm40": "results_val_lm40_eager_m40",
          "res_prompt": "results_val_prompt_eager_m40", "res_cua": "results_confirm_gh_merge_cua_b050",
          "res_broad": "results_confirm_gh_broad_residual_p100", "res_orig_modal": "results_confirm_gh_orig_modal_confirm",
          "test_orig": "results_test_gh_orig", "test_expo": "results_test_gh_expo125", "test_prompt": "results_test_gh_prompt_PARTIAL",
          "test_cua": "results_test_gh_merge_cua_b050", "test_orig_modal": "results_test_gh_orig_modal_test"}
    S = {k: R[v] for k, v in sr.items()}
    S["all_cua"] = {**S["res_cua"], **S["test_cua"]}
    S["all_orig_modal"] = {**S["res_orig_modal"], **S["test_orig_modal"]}
    ONLINE = [("onReserveExpo", "res_expo", "res_orig", "ExPO, reserve"),
              ("onReserveLmrow", "res_lm40", "res_orig", "answer output-row edit, reserve (stopped early)"),
              ("onReservePrompt", "res_prompt", "res_orig", "corrective prompt, reserve (stopped early)"),
              ("onReserveCua", "res_cua", "res_orig_modal", "CUA-Lite merge, reserve"),
              ("onReserveBroad", "res_broad", "res_orig_modal", "closed-form edit, reserve"),
              ("onTestExpo", "test_expo", "test_orig", "ExPO, TEST"),
              ("onTestPrompt", "test_prompt", "test_orig", "corrective prompt, TEST (partial run)"),
              ("onTestCua", "test_cua", "test_orig_modal", "CUA-Lite merge, TEST"),
              ("onAllCua", "all_cua", "all_orig_modal", "CUA-Lite merge, reserve + TEST (registered primary)"),
              ("onNoise", "res_orig", "res_orig_gh", "noise: original, local vs GitHub harness, reserve"),
              ("onNoiseServer", "res_orig_gh", "res_orig_modal", "noise: original, H200 vs Modal, reserve"),
              ("onTestNoiseServer", "test_orig", "test_orig_modal", "noise: original, H200 vs Modal, TEST")]
    for tag, a, b, label in ONLINE:
        cl = paired_units(S[a], S[b])
        assert len(cl) == int(M[tag + "N"]), tag
        rows.append(claim(tag, "Online score, " + label, tag + "Delta", tag + "Ci", tag + "Delta", cl, "score", M,
                          "noise reference" if label.startswith("noise") else "arm"))

    # Online guard (registered test), per task from reproduce/results/online_guard_tasks.csv.
    og = {}
    for r in csv.DictReader((ROOT / "reproduce/results/online_guard_tasks.csv").open()):
        og.setdefault(r["arm"], {})[r["task"]] = (float(r["score"]), int(r["false_done"]))
    G = og["orig_guard_claude_modal"]
    for ref, tg in [("orig_modal", "Og"), ("orig_pod", "Ogpod")]:
        B = og[ref]
        keys = sorted(set(G) & set(B))
        rows.append(claim(f"guard_online_fd_{ref}", f"Guard online, false done, vs the original ({dict(orig_modal='Modal', orig_pod='pod')[ref]})", f"{tg}FdDiff", f"{tg}FdDiffCi", f"{tg}FdDiff",
                          {k: [(G[k][1], B[k][1])] for k in keys}, "binary", M, "registered primary" if ref == "orig_modal" else "registered secondary"))
        rows.append(claim(f"guard_online_score_{ref}", f"Guard online, score, vs the original ({dict(orig_modal='Modal', orig_pod='pod')[ref]})", f"{tg}ScoreDiff", f"{tg}ScoreDiffCi",
                          f"{tg}ScoreDiff", {k: [(G[k][0], B[k][0])] for k in keys}, "score", M, "registered secondary"))

    # Strictly feasible cohort: context deltas (k=4 seeds), one context per task.
    pw = json.loads((DATA / "pod_astra/power/RESULT.json").read_text())["full_cohort"]["contrasts"]
    names = {"B-A": ("Cua", "merge vs original"), "C-A": ("Broad", "closed-form edit vs original"),
             "D-A": ("Rand", "random control vs original"), "C-D": ("BroadVsRand", "closed-form edit vs random control")}
    cohort = []
    for key, (tg, lab) in names.items():
        for s, S_ in [("fs+", "Fsp"), ("fs-", "Fsm")]:
            if key == "C-D" and s == "fs-":
                continue
            cd = pw[key]["strata"][s]["context_deltas"]
            r = claim(f"cohort_{key}_{s}", f"Feasible cohort, {lab}, answer rate on {'false' if s == 'fs+' else 'true'} completions",
                      f"pw{tg}Delta{S_}", f"pw{tg}Ci{S_}", f"pw{tg}Delta{S_}", {t: [(v, 0.0)] for t, v in cd.items()}, "score", M,
                      "unit = context answer-rate change over 4 seeds")
            cohort.append(r)
        if key != "C-D":
            g1 = list(pw[key]["strata"]["fs+"]["context_deltas"].values())
            g2 = list(pw[key]["strata"]["fs-"]["context_deltas"].values())
            p, how = label_perm_p(g1, g2)
            lo, hi = ci_of(M[f"pw{tg}SelCi"])
            sel = 100 * (sum(g1) / len(g1) - sum(g2) / len(g2))
            cohort.append({"claim": f"cohort_{key}_selectivity", "label": f"Feasible cohort, {lab}, selectivity (false minus true)",
                           "location": where(f"pw{tg}Sel", where(f"pw{tg}DeltaFsp")), "macro": f"pw{tg}SelCi", "kind": "two-sample",
                           "clusters": len(g1) + len(g2), "units": len(g1) + len(g2), "better": None, "worse": None,
                           "estimate": sel, "paper_estimate": num(M[f"pw{tg}Sel"]), "est_macro": f"pw{tg}Sel", "boot_lo": lo, "boot_hi": hi,
                           "p_sign": None, "p_mid": None, "p_flip": p, "flip_method": how + " (stratum-label permutation)",
                           "note": "contexts of the two strata are different tasks", "small": False,
                           "boot_sig": lo > 0 or hi < 0, "verdict": "agrees" if (lo > 0 or hi < 0) == (p < ALPHA) else "disagrees"})
    rows += cohort

    for r in rows:
        shown = M.get(r.get("est_macro", ""))
        dec = len(shown.split(".")[1]) if shown and "." in shown else 0
        assert abs(r["estimate"] - r["paper_estimate"]) <= 0.5 * 10 ** -dec + 1e-9, (r["claim"], r["estimate"], r["paper_estimate"])

    # Multiplicity families (Holm). A: every online run of a non-original arm, the rows from which a gain could have been
    # claimed (noise references are not hypotheses). B: the four contrasts of the feasible cohort on false completions,
    # the readout the cohort was built for. C: the three selectivities of that cohort. Each family is the set of tests
    # of one table of the paper; the guard's registered online test has its own single primary and is not pooled.
    fam = {"A_online_arms": [r for r in rows if r["claim"].startswith(("onReserve", "onTest", "onAll")) and r["note"] == "arm"],
           "B_cohort_false_completions": [r for r in rows if r["claim"].startswith("cohort_") and r["claim"].endswith("fs+")],
           "C_cohort_selectivity": [r for r in rows if r["claim"].endswith("selectivity")]}
    for f, rs in fam.items():
        for r, a in zip(rs, holm([r["p_flip"] for r in rs])):
            r.setdefault("holm", {})[f] = a
    return rows, fam


def fmt_p(p):
    return "  -  " if p is None else f"{p:.4f}" if p >= 0.0001 else f"{p:.1e}"


def main():
    rows, fam = compute()
    print("== Exact tests next to the paper's bootstrap intervals (points; p two-sided) ==")
    print("small = fewer than 10 clusters or fewer than 10 discordant units. flip = exact sign-flip randomisation over clusters;")
    print("sign = exact sign test on better/worse units (= exact McNemar when binary); Newcombe = paired score interval (binary only).")
    hdr = f"{'claim':28s} {'location':28s} {'clu':>4s} {'b/w':>7s} {'est':>6s} {'bootstrap CI':>16s} {'p flip':>7s} {'p sign':>7s} {'mid-p':>7s} {'Newcombe':>16s}  verdict"
    for section, test in [("small-n claims", lambda r: r["small"]), ("other paired claims (multiplicity families)", lambda r: not r["small"])]:
        print(f"\n-- {section} --")
        print(hdr)
        for r in rows:
            if not test(r):
                continue
            bw = "  -" if r["better"] is None else f"{r['better']}/{r['worse']}"
            nc = f"[{r['newcombe'][0]:+.1f}, {r['newcombe'][1]:+.1f}]" if "newcombe" in r else "-"
            print(f"{r['claim'][:28]:28s} {r['location'][:28]:28s} {r['clusters']:4d} {bw:>7s} {r['estimate']:+6.1f} "
                  f"{'[%+.1f, %+.1f]' % (r['boot_lo'], r['boot_hi']):>16s} {fmt_p(r['p_flip']):>7s} {fmt_p(r['p_sign']):>7s} "
                  f"{fmt_p(r['p_mid']):>7s} {nc:>16s}  {r['verdict']}")
    print("\n== Holm-adjusted p-values (exact sign-flip / permutation p) ==")
    for f, rs in fam.items():
        print(f"-- family {f} ({len(rs)} tests) --")
        for r in rs:
            print(f"  {r['claim']:32s} p {fmt_p(r['p_flip'])}  Holm {fmt_p(r['holm'][f])}")
    dis = [r["claim"] for r in rows if r["verdict"] != "agrees"]
    print("\nDisagreements (bootstrap interval vs exact tests):", ", ".join(dis) if dis else "none")

    by = {r["claim"]: r for r in rows}
    checks = [("escalation primary: 5 better, 0 worse, exact p = 0.0625", by["escalation_prim"]["better"] == 5 and by["escalation_prim"]["worse"] == 0
               and abs(by["escalation_prim"]["p_sign"] - 0.0625) < 1e-12 and abs(by["escalation_prim"]["p_flip"] - 0.0625) < 1e-12),
              ("guard v2 detection: 4 against 0 discordant, exact McNemar p = 0.125", by["guard_v2_det"]["better"] == 4
               and by["guard_v2_det"]["worse"] == 0 and abs(by["guard_v2_det"]["p_sign"] - 0.125) < 1e-12),
              ("guard v2 false rejection: 10 against 5 discordant", (by["guard_v2_rej"]["better"], by["guard_v2_rej"]["worse"]) == (10, 5)),
              ("every recomputed point estimate equals the paper's", True)]
    ok = all(c for _, c in checks)
    for t, c in checks:
        print(("  OK  " if c else "  FAIL ") + t)
    print("EXACT RE-ANALYSIS OK" if ok else "EXACT RE-ANALYSIS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
