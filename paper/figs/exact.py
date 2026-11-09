"""Exact small-sample tests, Holm-adjusted p-values and the FRESH-115 registration (Appendix app:exact).

Imports compute() from reproduce/exact_reanalysis.py (repository, outside paper/data), which reads the per-unit data in
data/ and the bootstrap intervals of the other generated macros: run last in build.sh. FRESH-115 from
docs/FRESH_TASKS.json (reproduce/fresh_tasks.py checks it).
"""
import importlib.util
import json

from common import PAPER, Macros, write_table

ROOT = PAPER.parent
spec = importlib.util.spec_from_file_location("exact_reanalysis", ROOT / "reproduce/exact_reanalysis.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)
rows, fam = ex.compute()
by = {r["claim"]: r for r in rows}
SRC = "reproduce/exact_reanalysis.py"
m = Macros("exact")


def p3(p):
    return "1" if p >= 0.9995 else f"{p:.3g}" if p >= 0.001 else f"{p:.1g}"


def tag(claim):
    return "".join(w.capitalize() for w in claim.replace("+", "p").replace("-", "").replace("_", " ").split())


for c, t in [("escalation_prim", "RbPrim"), ("escalation_strict", "RbStrict"), ("escalation_all", "RbAll"),
             ("guard_v2_det", "GvDet"), ("guard_v2_rej", "GvRej"), ("cohort_B-A_fs-", "CuaFsm"), ("cohort_C-A_fs+", "BroadFsp"),
             ("cohort_D-A_fs+", "RandFsp"), ("cohort_C-D_fs+", "BroadVsRandFsp"), ("cohort_B-A_fs+", "CuaFsp"), ("repair", "Rep")]:
    r = by[c]
    m.add(f"ex{t}P", p3(r["p_flip"]), SRC + f" {c} exact sign-flip p over {r['clusters']} clusters (two-sided)")
    if r["p_sign"] is not None:
        m.add(f"ex{t}SignP", p3(r["p_sign"]), SRC + f" {c} exact sign test / McNemar p on {r['better']} vs {r['worse']} (two-sided)")
        m.add(f"ex{t}Better", r["better"], SRC + f" {c} units better with the first arm")
        m.add(f"ex{t}Worse", r["worse"], SRC + f" {c} units worse with the first arm")
    if "newcombe" in r:
        m.add(f"ex{t}Newcombe", " to ".join(f"{x:+.1f}".replace("-", "$-$") for x in r["newcombe"]), SRC + f" {c} Newcombe 95% interval (points)")
small = [r for r in rows if r["small"]]
m.add("exNSmall", len(small), SRC + " claims with fewer than 10 clusters or 10 discordant units")
m.add("exNRows", len(rows), SRC + " paired claims re-analysed")
dis = [r for r in rows if r["verdict"] != "agrees"]
m.add("exNDisagree", len(dis), SRC + " claims whose bootstrap interval and exact tests disagree on p < 0.05")
for f, short in [("A_online_arms", "Online"), ("B_cohort_false_completions", "Cohort"), ("C_cohort_selectivity", "Sel")]:
    rs = fam[f]
    m.add(f"exHolm{short}N", len(rs), SRC + f" family {f}: number of tests")
    m.add(f"exHolm{short}Min", p3(min(r["holm"][f] for r in rs)), SRC + f" family {f}: smallest Holm-adjusted p")
    m.add(f"exHolm{short}Below", sum(r["holm"][f] < 0.05 for r in rs), SRC + f" family {f}: tests with Holm-adjusted p < 0.05")
for c, t in [("cohort_C-A_fs+", "BroadFsp"), ("cohort_D-A_fs+", "RandFsp"), ("cohort_C-D_fs+", "BroadVsRandFsp"),
             ("cohort_B-A_fs+", "CuaFsp"), ("cohort_C-A_selectivity", "BroadSel"), ("cohort_D-A_selectivity", "RandSel"),
             ("cohort_B-A_selectivity", "CuaSel")]:
    m.add(f"exHolm{t}", p3(list(by[c]["holm"].values())[0]), SRC + f" {c} Holm-adjusted p within its family")
fr = json.loads((ROOT / "docs/FRESH_TASKS.json").read_text())
m.add("exFreshN", fr["n"], "docs/FRESH_TASKS.json n")
m.add("exFreshAll", fr["n_all"], "docs/FRESH_TASKS.json n_all (src/osworld/test_nogdrive.json)")
m.add("exFreshUnsplit", fr["n_unsplit"], "docs/FRESH_TASKS.json n_unsplit")
m.add("exFreshPilot", len(fr["excluded_as_read"]), "docs/FRESH_TASKS.json excluded_as_read (pilot runs)")
m.add("exFreshSha", fr["sha256_of_task_list"][:12], "docs/FRESH_TASKS.json sha256_of_task_list (first 12 hex)")
m.add("exFreshMulti", fr["domains"]["multi_apps"], "docs/FRESH_TASKS.json domains.multi_apps")
res = {i for ids in json.loads((ROOT / "src/osworld/confirm_tasks.json").read_text())["tasks"].values() for i in ids}
man = json.loads((PAPER / "data/local/judge_bench/verif_study_manifest.json").read_text())
m.add("exReserveJudge", sum(e["task_id"] in res for e in man), "src/osworld/confirm_tasks.json tasks x data/local/judge_bench/verif_study_manifest.json: episodes of the 268 on reserve tasks")
m.add("exReserveJudgeFalse", sum(e["task_id"] in res and e["label"] == "false_success" for e in man), "same, labelled false_success")
rbe = json.loads((PAPER / "data/local/rescue_bench/RESULT.json").read_text())["per_episode"]
m.add("exReserveRescue", sum(t.split("/")[-1] in res for t in rbe), "src/osworld/confirm_tasks.json tasks x data/local/rescue_bench/RESULT.json per_episode: replayed episodes on reserve tasks")
m.write()


def esc(s):
    return s.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


def ptex(p):
    return "--" if p is None else p3(p)


def line(r):
    mn = lambda t: t.replace("-", "$-$")
    bw = "--" if r["better"] is None else f"{r['better']}/{r['worse']}"
    nc = "--" if "newcombe" not in r else mn("[" + ", ".join(f"{x:+.1f}" for x in r["newcombe"]) + "]")
    est = mn(f"{r['estimate']:+.1f} [{r['boot_lo']:+.1f}, {r['boot_hi']:+.1f}]")
    loc = esc(r["location"].split(" (")[0].replace("generated/", ""))
    return (f"{esc(r['label'])} & \\texttt{{{loc}}} & {r['clusters']} & {bw} & {est} & {ptex(r['p_flip'])} & "
            f"{ptex(r['p_sign'])} & {ptex(r['p_mid'])} & {nc} & {r['verdict']} \\\\")


hdr = ("\\begin{tabular}{p{5.6cm}lcccccccl}\n\\toprule\nClaim & Location & clusters & better/worse & $\\Delta$ points [bootstrap 95\\%] & "
       "$p$ flip & $p$ sign & mid-$p$ & Newcombe 95\\% & verdict \\\\\n\\midrule\n")
body = ("\\multicolumn{10}{l}{\\emph{Fewer than 10 clusters or fewer than 10 discordant units}} \\\\\n"
        + "\n".join(line(r) for r in rows if r["small"])
        + "\n\\midrule\\multicolumn{10}{l}{\\emph{Other paired claims (members of the multiplicity families)}} \\\\\n"
        + "\n".join(line(r) for r in rows if not r["small"]) + "\n\\bottomrule\n\\end{tabular}\n")
write_table("exact", hdr + body, "exact")
FAMN = {"A_online_arms": "A: online runs of non-original arms (Table~\\ref{tab:b4-heldout})",
        "B_cohort_false_completions": "B: feasible cohort, change on false completions",
        "C_cohort_selectivity": "C: feasible cohort, selectivity"}
hl = []
for f, rs in fam.items():
    hl.append(f"\\multicolumn{{3}}{{l}}{{\\emph{{Family {FAMN[f]}, {len(rs)} tests}}}} \\\\")
    for r in rs:
        hl.append(f"{esc(r['label'])} & {p3(r['p_flip'])} & {p3(r['holm'][f])} \\\\")
write_table("holm", "\\begin{tabular}{p{9cm}cc}\n\\toprule\nTest & exact $p$ & Holm-adjusted $p$ \\\\\n\\midrule\n"
            + "\n".join(hl) + "\n\\bottomrule\n\\end{tabular}\n", "exact")
print("exact ok", len(rows), "rows,", len(small), "small,", len(dis), "disagree")
