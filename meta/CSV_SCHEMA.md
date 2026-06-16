# Per-repo CSV schema

One CSV per repo at `results/<repo>.csv`. Header row + 1-2 data rows (one per good-first-issue).

## Columns (exact order)

1. `repo` — e.g. `prometheus-k8s-operator`
2. `category` — charm | bundle | rock | lib | extra
3. `issue_number` — GitHub issue number, or empty if self-identified & not filed
4. `issue_url` — full URL, or `self-identified` if no existing issue
5. `title` — short issue title
6. `source` — `existing-open-issue` | `self-identified`
7. `type` — bug | docs | cleanup | refactor | test | enhancement | build
8. `suggested_labels` — e.g. `good first issue; Type: Cleanup`
9. `difficulty` — trivial | easy | moderate
10. `summary` — 1-2 sentences: what the issue is
11. `why_good_first_issue` — why it's beginner-friendly (small scope, well-defined, no deep arch knowledge)
12. `affected_files` — semicolon-separated paths
13. `repro_tier` — inspection | unit | integration
14. `repro_steps` — exact commands run (in the cos VM) or inspection method
15. `repro_result` — `confirmed` | `confirmed-by-inspection` | `could-not-reproduce` + short detail (e.g. failing test name / observed vs expected)
16. `fix_hint` — concrete pointer to how a newcomer would fix it
17. `notes` — anything else (e.g. "needs live deploy", "flaky")

## How to write it (use Python csv for correct quoting)

```python
import csv, pathlib
rows = [ {...}, {...} ]  # dict per issue with the keys above
cols = ["repo","category","issue_number","issue_url","title","source","type",
        "suggested_labels","difficulty","summary","why_good_first_issue",
        "affected_files","repro_tier","repro_steps","repro_result","fix_hint","notes"]
p = pathlib.Path("results/<repo>.csv")
with p.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
```

Never hand-roll CSV with string concatenation — text fields contain commas/quotes.
