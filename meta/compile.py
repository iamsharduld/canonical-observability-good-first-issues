#!/usr/bin/env python3
"""Validate per-repo CSVs, check coverage vs repos.tsv, compile master_index.csv, print report."""
import csv, sys, pathlib

WD = pathlib.Path("/home/shardul.deshpande@canonical.com/projects-shared/observability-good-first-issue")
RES = WD / "results"
COLS = ["repo","category","issue_number","issue_url","title","source","type",
        "suggested_labels","difficulty","summary","why_good_first_issue",
        "affected_files","repro_tier","repro_steps","repro_result","fix_hint","notes"]

# expected universe
expected = {}
with (WD/"meta/repos.tsv").open() as f:
    r = csv.reader(f, delimiter="\t"); next(r)
    for cat, repo in r:
        expected[repo] = cat

# non-csv clutter
clutter = [p.name for p in RES.iterdir() if p.suffix != ".csv"]

rows = []
bad = []
per_repo = {}
csv_files = sorted(p for p in RES.glob("*.csv") if not p.name.startswith("_"))
for p in csv_files:
    stem = p.name[:-4]
    try:
        with p.open(newline="") as f:
            rd = csv.DictReader(f)
            if rd.fieldnames != COLS:
                bad.append(f"{p.name}: header mismatch -> {rd.fieldnames}")
                continue
            n = 0
            for row in rd:
                rows.append(row); n += 1
            per_repo[stem] = n
    except Exception as e:
        bad.append(f"{p.name}: parse error {e}")

# coverage: filename stem vs expected (repo names in tsv have no owner; csv 'repo' col may have canonical/ prefix)
covered = set(per_repo)
missing = [r for r in expected if r not in covered]
extra = [r for r in covered if r not in expected]

# write master
master = WD/"results"/"_master_index.csv"
with master.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
    for row in rows: w.writerow({k: row.get(k,"") for k in COLS})

# stats
def tally(key):
    d={}
    for row in rows: d[row.get(key,"").strip()] = d.get(row.get(key,"").strip(),0)+1
    return dict(sorted(d.items(), key=lambda x:-x[1]))

integ = [(row["repo"],row.get("issue_number",""),row["title"]) for row in rows if row.get("repro_tier","").strip()=="integration"]
obsolete = [(row["repo"],row["title"]) for row in rows if "obsolete" in (row.get("notes","")+row.get("repro_result","")).lower() or "already" in row.get("notes","").lower()]

print("="*70)
print(f"CSV files: {len(csv_files)}   | candidate rows: {len(rows)}")
print(f"Coverage: {len(covered)}/{len(expected)} repos have a CSV")
print(f"MISSING (no CSV): {missing or 'none'}")
print(f"EXTRA (csv not in universe): {extra or 'none'}")
print(f"Non-CSV clutter in results/: {clutter or 'none'}")
print(f"Malformed CSVs: {bad or 'none'}")
print(f"Repos with !=2 rows: {[ (k,v) for k,v in per_repo.items() if v!=2 ] or 'none'}")
print("-"*70)
print("by category:", tally("category"))
print("by source  :", tally("source"))
print("by type    :", tally("type"))
print("by tier    :", tally("repro_tier"))
print("by difficulty:", tally("difficulty"))
print("-"*70)
print(f"INTEGRATION-tier (need live deploy): {len(integ)}")
for r in integ: print("   ", r[0], r[1], "-", r[2][:70])
print(f"OBSOLETE/already-done flags: {len(obsolete)}")
for r in obsolete: print("   ", r[0], "-", r[1][:70])
print("="*70)
print("master written:", master)
