#!/usr/bin/env python3
"""Data-analysis reports over the GFI dataset (results/_master_index.csv) -> reports/*.md + aggregates.csv.
Stdlib only. ASCII bar charts."""
import csv, pathlib, collections, re, datetime

WD = pathlib.Path("/home/shardul.deshpande@canonical.com/projects-shared/observability-good-first-issue")
MASTER = WD/"results/_master_index.csv"
REP = WD/"reports"; REP.mkdir(exist_ok=True)
rows = list(csv.DictReader(MASTER.open(newline="")))
N = len(rows)
repos = {r["repo"] for r in rows}
today = "2026-06-16"

def bar(n, mx, w=34):
    return "█"*max(1, round(n/mx*w)) if n else ""

def tally(key, rowset=None):
    rs = rowset if rowset is not None else rows
    c = collections.Counter((r.get(key,"").strip() or "(blank)") for r in rs)
    return c.most_common()

def tbl(title, counts, total=None):
    total = total or sum(n for _,n in counts)
    mx = max((n for _,n in counts), default=1)
    out = [f"### {title}", "", "| value | count | % | |", "|---|--:|--:|:--|"]
    for k,n in counts:
        out.append(f"| {k} | {n} | {100*n/total:.0f}% | {bar(n,mx)} |")
    out.append("")
    return "\n".join(out)

# ---------- 01 overview ----------
active = [r for r in rows if r["category"]!="archived"]
arch = [r for r in rows if r["category"]=="archived"]
percat_repo = collections.Counter(r["category"] for r in rows)
repo_counts = collections.Counter(r["repo"] for r in rows)

o = [f"# 01 — Dataset overview", "",
     f"_Generated {today} from `results/_master_index.csv`._","",
     f"- **Repositories covered:** {len(repos)}",
     f"- **Candidate issues:** {N}",
     f"- **Active-repo candidates:** {len(active)}  |  **Archived-repo rows:** {len(arch)}",
     f"- **Avg candidates/repo:** {N/len(repos):.2f}", "",
     tbl("By category", tally("category")),
     tbl("By type", tally("type")),
     tbl("By source", tally("source")),
     tbl("By difficulty", tally("difficulty")),
     tbl("By reproduction tier", tally("repro_tier")),
    ]
(REP/"01_overview.md").write_text("\n".join(o))

# ---------- 02 top starter issues ----------
def score(r):
    s=0.0
    if r["source"]=="existing-open-issue": s+=2
    d=r["difficulty"]
    s+= {"trivial":2,"easy":1.5,"beginner":1.5,"medium":0.3}.get(d,0)
    s+= {"bug":1.5,"documentation":1,"cleanup":1,"test":1,"enhancement":0.5}.get(r["type"],0)
    t=r["repro_tier"]
    if t=="unit": s+=1.5
    elif t=="inspection": s+=0.7
    elif t.startswith("integration-REPRODUCED"): s+=1.2
    blob=(r["notes"]+r["repro_result"]).lower()
    if any(w in blob for w in ["obsolete","already fixed","already-done","already done","superseded","likely already"]): s-=3
    if r["category"]=="archived": s-=10
    if t.startswith("integration") and "REPRODUCED" not in t: s-=1.5
    return s
ranked = sorted(rows, key=score, reverse=True)
def link(r):
    return f"[{r['issue_number'] or 'self'}]({r['issue_url']})" if r["issue_url"].startswith("http") else "self-identified"
m=["# 02 — Top starter issues (ranked)","",
   "Heuristic score favours: real open issues, trivial/easy, doc/cleanup/bug, test- or code-verified; penalises obsolete/archived/needs-live-deploy.","",
   "| # | repo | issue | type | diff | tier | summary |","|--:|---|---|---|---|---|---|"]
for i,r in enumerate(ranked[:30],1):
    m.append(f"| {i} | {r['repo'].replace('canonical/','')} | {link(r)} | {r['type']} | {r['difficulty']} | {r['repro_tier']} | {r['summary'][:90].replace(chr(10),' ')} |")
(REP/"02_top_starter_issues.md").write_text("\n".join(m))

# ---------- 03 cross-repo patterns ----------
THEMES = {
 "Ambiguous `requires-python = \"~=3.x\"` (uv warns)": ["requires-python","requires_python"],
 "Deprecated `from ops.main import main`": ["ops.main","ops main import"],
 "Host architecture detection bug (processor vs machine)": ["platform.processor","platform.machine","aarch64","get_host_architecture"],
 "Dead formatter/tool config (black/codespell vs ruff)": ["[tool.black]","black","codespell","asyncio_mode"],
 "Terraform outputs hardcoded / missing descriptions": ["outputs.tf","terraform module","hardcod"],
 "goss smoke-test gaps (rocks)": ["goss"],
 "Outdated upstream version pin (rocks)": ["version-bump","upstream latest","source-tag"],
 "Stale / placeholder / wrong docstrings": ["docstring"],
 "Unguarded lightkube reconcile (404/RBAC crash)": ["lightkube","httpx","reconcile","404"],
 "README / how-to doc inaccuracies": ["readme.md","how-to/","docs/how-to","how-to guide"],
 "Obsolete / already-fixed labelled issues caught": ["obsolete","already fixed","superseded","already exists","now obsolete","verify-and-close","verify and close"],
}
def blob(r): return " ".join(r[k] for k in ("title","summary","why_good_first_issue","fix_hint","notes","type","suggested_labels","repro_result","affected_files")).lower()
theme_hits=collections.OrderedDict()
for name,kws in THEMES.items():
    hit={}
    for r in rows:
        b=blob(r)
        if any(k in b for k in kws):
            hit.setdefault(r["repo"].replace("canonical/",""), []).append(r["issue_number"] or "self")
    theme_hits[name]=hit
c=["# 03 — Cross-repo recurring patterns","",
   "Systemic issues that recur across multiple repositories — each is a candidate for a **single fleet-wide fix / sweep**.","",
   "| pattern | #repos | repos (issues) |","|---|--:|---|"]
for name,hit in sorted(theme_hits.items(), key=lambda x:-len(x[1])):
    if not hit: continue
    repolist="; ".join(f"{rp} ({','.join(iss)})" for rp,iss in sorted(hit.items()))
    c.append(f"| {name} | {len(hit)} | {repolist[:160]} |")
c.append("")
c.append("> The top rows (recurring in 3+ repos) are the highest-leverage: e.g. the ambiguous `requires-python`, the `ops.main` deprecation, and the Terraform-output patterns can each be fixed identically across every affected repo.")
(REP/"03_cross_repo_patterns.md").write_text("\n".join(c))

# ---------- 04 bug inventory ----------
bugs=[r for r in rows if r["type"]=="bug"]
byt=collections.defaultdict(list)
for r in bugs: byt[r["repro_tier"]].append(r)
b=["# 04 — Confirmed bug inventory",f"","{} candidates are typed `bug`.".format(len(bugs)),""]
for tier in sorted(byt, key=lambda t:(not t.startswith('integration-REPRO'), t!='unit', t)):
    b.append(f"## tier: {tier} ({len(byt[tier])})")
    b.append("")
    b.append("| repo | issue | summary | evidence (repro_result) |")
    b.append("|---|---|---|---|")
    for r in byt[tier]:
        b.append(f"| {r['repo'].replace('canonical/','')} | {link(r)} | {r['summary'][:80].replace(chr(10),' ')} | {r['repro_result'][:110].replace(chr(10),' ')} |")
    b.append("")
(REP/"04_bug_inventory.md").write_text("\n".join(b))

# ---------- 05 live repro summary ----------
live=[r for r in rows if r["repro_tier"].startswith("integration")]
l=["# 05 — Live integration reproduction summary","",
   "8 integration-tier bugs; live repro attempted in throwaway Juju models on the `cos` VM (never touching the live model). Full evidence: `results/_live_repro_log.md`.","",
   "| repo | issue | outcome | summary |","|---|---|---|---|"]
for r in sorted(live,key=lambda r:r["repro_tier"]):
    out={"integration-REPRODUCED-live":"✅ reproduced","integration-not-reproducible-here":"⚠️ needs Charmed K8s","integration-assessed":"⏸ assessed (risk)"}.get(r["repro_tier"],r["repro_tier"])
    l.append(f"| {r['repo'].replace('canonical/','')} | {link(r)} | {out} | {r['summary'][:80].replace(chr(10),' ')} |")
(REP/"05_live_repro_summary.md").write_text("\n".join(l))

# ---------- 06 per-category ----------
pc=["# 06 — Per-category breakdown",""]
for cat in ["charm","extra","rock","lib","archived"]:
    rs=[r for r in rows if r["category"]==cat]
    if not rs: continue
    nrepo=len({r["repo"] for r in rs})
    pc.append(f"## {cat} — {nrepo} repos, {len(rs)} candidates")
    pc.append("")
    pc.append(tbl("types", tally("type", rs), total=len(rs)))
(REP/"06_by_category.md").write_text("\n".join(pc))

# ---------- aggregates.csv ----------
with (REP/"aggregates.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["dimension","value","count"])
    for dim in ["category","type","source","difficulty","repro_tier"]:
        for v,n in tally(dim): w.writerow([dim,v,n])

# ---------- index ----------
idx=["# Data analysis reports","",f"_Generated {today} from {N} candidates across {len(repos)} repos._","",
 "- [01 — Overview & distributions](01_overview.md)",
 "- [02 — Top starter issues (ranked)](02_top_starter_issues.md)",
 "- [03 — Cross-repo recurring patterns](03_cross_repo_patterns.md)",
 "- [04 — Confirmed bug inventory](04_bug_inventory.md)",
 "- [05 — Live integration reproduction summary](05_live_repro_summary.md)",
 "- [06 — Per-category breakdown](06_by_category.md)",
 "- `aggregates.csv` — machine-readable aggregate tables",
 ]
(REP/"00_index.md").write_text("\n".join(idx))

print(f"OK: {N} candidates, {len(repos)} repos -> {len(list(REP.glob('*.md')))} md reports + aggregates.csv")
print("themes (>=2 repos):", [(k,len(v)) for k,v in theme_hits.items() if len(v)>=2])
