# 05 — Live integration reproduction summary

8 integration-tier bugs; live repro attempted in throwaway Juju models on the `cos` VM (never touching the live model). Full evidence: `results/_live_repro_log.md`.

| repo | issue | outcome | summary |
|---|---|---|---|
| istio-beacon-k8s-operator | [166](https://github.com/canonical/istio-beacon-k8s-operator/issues/166) | ✅ reproduced | On config-changed, the charm reconciles waypoint resources via KubernetesResourc |
| istio-ingress-k8s-operator | [52](https://github.com/canonical/istio-ingress-k8s-operator/issues/52) | ✅ reproduced | When istio-ingress-k8s is deployed on a cluster without istio (no Gateway API /  |
| loki-operators | [80](https://github.com/canonical/loki-operators/issues/80) | ✅ reproduced | The coordinator's `_set_alerts` (coordinator/src/charm.py:272) writes EVERY aler |
| prometheus-scrape-target-k8s-operator | [53](https://github.com/canonical/prometheus-scrape-target-k8s-operator/issues/53) | ✅ reproduced | When prometheus rejects the charm's scrape config (e.g. unquoted label values, i |
| script-exporter-operator | [16](https://github.com/canonical/script-exporter-operator/issues/16) | ✅ reproduced | If a bad config_file makes the systemd service fail to start, the next config-ch |
| istio-beacon-k8s-operator | [42](https://github.com/canonical/istio-beacon-k8s-operator/issues/42) | ⏸ assessed (risk) | _sync_all_resources() calls _setup_proxy_pebble_service() and then unconditional |
| istio-ingress-k8s-operator | [34](https://github.com/canonical/istio-ingress-k8s-operator/issues/34) | ⚠️ needs Charmed K8s | Deploying istio-ingress-k8s can fail with an uncaught httpx.HTTPStatusError 403  |
| istio-k8s-operator | [38](https://github.com/canonical/istio-k8s-operator/issues/38) | ⚠️ needs Charmed K8s | When deployed on Charmed Kubernetes, istio-k8s fails with lightkube ApiError: 'c |