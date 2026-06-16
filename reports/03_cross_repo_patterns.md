# 03 — Cross-repo recurring patterns

Systemic issues that recur across multiple repositories — each is a candidate for a **single fleet-wide fix / sweep**.

| pattern | #repos | repos (issues) |
|---|--:|---|
| Obsolete / already-fixed labelled issues caught | 21 | cos-coordinated-workers (11); cos-lib (29); cos-lite-bundle (self); cos-proxy-operator (self); cos-tool (44); grafana-agent-k8s-operator (339,self); grafana-k8s |
| README / how-to doc inaccuracies | 16 | alertmanager-k8s-operator (self); alertmanager-rock (self); catalogue-k8s-operator (self); cos-alerter (self); cos-configuration-rules-dashboards (self,self); c |
| Stale / placeholder / wrong docstrings | 12 | avalanche-k8s-operator (self,self); catalogue-k8s-operator (self); cos-alerter (self); grafana-agent-k8s-operator (self); grafana-agent-operator (77); istio-k8s |
| Outdated upstream version pin (rocks) | 10 | alertmanager-rock (self); grafana-agent-rock (self); grafana-rock (self); loki-rock (self); mimir-rock (self); observability-libs (self); prometheus-rock (self) |
| Terraform outputs hardcoded / missing descriptions | 9 | cos-lite-bundle (self); grafana-agent-k8s-operator (339); grafana-rock (94); mimir-bundle (self); observability-stack (189,250); pyroscope-operators (self,self) |
| goss smoke-test gaps (rocks) | 7 | alertmanager-rock (self,self); grafana-agent-rock (self,self); grafana-rock (self); loki-rock (81,self); mimir-rock (61,self); prometheus-rock (self); s3proxy-r |
| Deprecated `from ops.main import main` | 6 | avalanche-k8s-operator (self); juju-introspect-operator (self); prometheus-pushgateway-k8s-operator (self); prometheus-scrape-config-k8s-operator (self); promet |
| Unguarded lightkube reconcile (404/RBAC crash) | 6 | grafana-k8s-operator (528); istio-beacon-k8s-operator (166); istio-ingress-k8s-operator (52,34); istio-k8s-operator (38); o11y-tester-operator (self); pyroscope |
| Ambiguous `requires-python = "~=3.x"` (uv warns) | 5 | cos-proxy-operator (self); loki-operators (self); mimir-operators (25); o11y-tester-operator (self); prometheus-pushgateway-k8s-operator (self,self) |
| Dead formatter/tool config (black/codespell vs ruff) | 4 | cos-alerter (self); o11y-tester-operator (self); observability-charm-tools (self,self); observability-libs (self) |
| Host architecture detection bug (processor vs machine) | 2 | cos-lib (29,self); parca-agent-operator (self) |

> The top rows (recurring in 3+ repos) are the highest-leverage: e.g. the ambiguous `requires-python`, the `ops.main` deprecation, and the Terraform-output patterns can each be fixed identically across every affected repo.