#!/usr/bin/env python3
"""One-shot: normalize source/type/difficulty across per-repo CSVs to a controlled vocabulary.
Evidence columns are never touched."""
import csv, pathlib

RES = pathlib.Path("/home/shardul.deshpande@canonical.com/projects-shared/observability-good-first-issue/results")
COLS = ["repo","category","issue_number","issue_url","title","source","type",
        "suggested_labels","difficulty","summary","why_good_first_issue",
        "affected_files","repro_tier","repro_steps","repro_result","fix_hint","notes"]

TYPE_MAP = {
    "type: bug":"bug","type: cleanup":"cleanup","type: documentation":"documentation",
    "type: enhancement":"enhancement","type: refactor":"refactor",
    "good first issue, type: enhancement":"enhancement",
    "docs":"documentation","docs/bug":"documentation","cleanup/docs":"cleanup",
    "bug/cleanup":"bug","cleanup/housekeeping":"cleanup","testing":"test",
    "goss-gap":"goss-test-gap","build-recipe":"build",
}
def norm_type(v):
    k = v.strip().lower()
    if k in TYPE_MAP: return TYPE_MAP[k]
    if k.startswith("type: "): return k[6:]
    return k

def norm_source(v):
    return "self-identified" if v.strip().lower()=="self-identified" else "existing-open-issue"

def norm_diff(v):
    k=v.strip().lower()
    return {"beginner":"easy"}.get(k,k)

for p in sorted(RES.glob("*.csv")):
    if p.name.startswith("_"): continue
    with p.open(newline="") as f:
        rd=csv.DictReader(f)
        if rd.fieldnames!=COLS:
            print("skip (header)",p.name); continue
        rows=list(rd)
    for r in rows:
        r["source"]=norm_source(r.get("source",""))
        r["type"]=norm_type(r.get("type",""))
        r["difficulty"]=norm_diff(r.get("difficulty",""))
    with p.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=COLS); w.writeheader()
        for r in rows: w.writerow({k:r.get(k,"") for k in COLS})
print("normalized", len(list(RES.glob('*.csv')))-1, "per-repo CSVs")
