#!/usr/bin/env python3
"""Fold live-reproduction outcomes back into the per-repo CSVs (repro_tier + repro_result prefix)."""
import csv, pathlib
RES = pathlib.Path("/home/shardul.deshpande@canonical.com/projects-shared/observability-good-first-issue/results")
COLS = ["repo","category","issue_number","issue_url","title","source","type",
        "suggested_labels","difficulty","summary","why_good_first_issue",
        "affected_files","repro_tier","repro_steps","repro_result","fix_hint","notes"]

# file -> issue_number -> (new_tier, prefix added to repro_result)
U = {
 "istio-beacon-k8s-operator.csv": {
   "166": ("integration-REPRODUCED-live", "LIVE-REPRODUCED 2026-06-16 (cos VM, throwaway model, no Gateway CRDs): deploy istio-beacon-k8s 1/edge --trust -> hook failed config-changed; httpx 404 on /apis/gateway.networking.k8s.io/v1/gateways, unhandled in _sync_waypoint_resources. || "),
   "42": ("integration-assessed", "LIVE-ASSESSED 2026-06-16: not force-reproduced (needs istio installed + manually stopping the metrics-proxy pebble service; avoided repeat istio cluster-webhook churn on the shared cos node). Code-confirmed. || "),
 },
 "istio-ingress-k8s-operator.csv": {
   "52": ("integration-REPRODUCED-live", "LIVE-REPRODUCED 2026-06-16: deploy istio-ingress-k8s 1/edge --trust, no istio -> hook failed leader-elected; httpx 404 on /apis/security.istio.io/v1/authorizationpolicies in _sync_ext_authz_auth_policy, before the readiness guard. || "),
   "34": ("integration-not-reproducible-here", "LIVE-ATTEMPTED 2026-06-16: NOT reproducible on microk8s (istio-ingress-k8s deployed without --trust still went active; microk8s grants enough cluster perms). Needs Charmed Kubernetes' stricter RBAC. || "),
 },
 "istio-k8s-operator.csv": {
   "38": ("integration-not-reproducible-here", "LIVE-ATTEMPTED 2026-06-16: NOT reproducible on microk8s (istio-k8s deployed without --trust still went active). Needs Charmed Kubernetes' stricter RBAC. || "),
 },
 "script-exporter-operator.csv": {
   "16": ("integration-REPRODUCED-live", "LIVE-REPRODUCED 2026-06-16 (lxd: ubuntu+script-exporter dev/edge): malformed config_file -> unit stuck 'hook failed config-changed / awaiting error resolution'; unguarded yaml.safe_load at charm.py:186 (a 2nd unguarded point besides service_resume). || "),
 },
 "prometheus-scrape-target-k8s-operator.csv": {
   "53": ("integration-REPRODUCED-live", "LIVE-REPRODUCED 2026-06-16: prometheus-k8s + scrape-target 2/stable; labels=1bad:value -> scrape-target ACTIVE (no error) while promtool check config FAILED: '1bad is not a valid label name'. Charm sets Active from local jobs only, never reads scrape_job_errors (charm.py:91-92). || "),
 },
 "loki-operators.csv": {
   "80": ("integration-assessed", "LIVE-ASSESSED 2026-06-16: not deployed (loki coordinator+worker+S3 stack would add memory pressure risking eviction of live cos pods on this single 15GB node). Code-confirmed; run on a dedicated VM. || "),
 },
}

for fname, issues in U.items():
    p = RES/fname
    rows = list(csv.DictReader(p.open(newline="")))
    changed = 0
    for r in rows:
        num = r.get("issue_number","").strip().lstrip("#")
        if num in issues:
            tier, prefix = issues[num]
            r["repro_tier"] = tier
            if not r["repro_result"].startswith("LIVE-"):
                r["repro_result"] = prefix + r["repro_result"]
            changed += 1
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
        for r in rows: w.writerow({k:r.get(k,"") for k in COLS})
    print(f"{fname}: updated {changed} row(s)")
