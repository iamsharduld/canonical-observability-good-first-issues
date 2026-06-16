# 02 — Top starter issues (ranked)

Heuristic score favours: real open issues, trivial/easy, doc/cleanup/bug, test- or code-verified; penalises obsolete/archived/needs-live-deploy.

| # | repo | issue | type | diff | tier | summary |
|--:|---|---|---|---|---|---|
| 1 | grafana-agent-operator | [179](https://github.com/canonical/grafana-agent-operator/issues/179) | bug | easy | unit | In _update_config, after writing the config the code calls self.restart() and wraps it in  |
| 2 | cos-tool | [21](https://github.com/canonical/cos-tool/issues/21) | bug | easy | inspection | When alert-rule validation fails, cos-tool prints the full Go stack trace to stderr (which |
| 3 | grafana-k8s-operator | [528](https://github.com/canonical/grafana-k8s-operator/issues/528) | bug | easy | inspection | grafana_version() in src/grafana.py is a TOCTOU race: it guards with self._container.can_c |
| 4 | grafana-k8s-operator | [508](https://github.com/canonical/grafana-k8s-operator/issues/508) | bug | easy | inspection | lib/charms/grafana_k8s/v0/grafana_dashboard.py declares PYDEPS = ["cosl >= 0.0.50"] (line  |
| 5 | loki-k8s-operator | [460](https://github.com/canonical/loki-k8s-operator/issues/460) | bug | easy | inspection | The LokiRequestLatency alert renders 'Loki request latency (instance ) (LokiRequestLatency |
| 6 | mimir-operators | [18](https://github.com/canonical/mimir-operators/issues/18) | bug | easy | inspection | The nginx reverse-proxy in the coordinator does not expose the per-component ring status/h |
| 7 | observability-stack | [189](https://github.com/canonical/observability-stack/issues/189) | bug | easy | inspection | The catalogue application deployed by the cos-lite (and cos) Terraform module is given no  |
| 8 | prometheus-k8s-operator | [686](https://github.com/canonical/prometheus-k8s-operator/issues/686) | bug | easy | inspection | GrafanaSourceProvider is constructed at import/init time with source_url=self.most_externa |
| 9 | tempo-operators | [257](https://github.com/canonical/tempo-operators/issues/257) | bug | easy | inspection | The deprecated charm_tracing charm library logs a WARNING ('charm tracing buffer exceeds m |
| 10 | prometheus-scrape-target-k8s-operator | [55](https://github.com/canonical/prometheus-scrape-target-k8s-operator/issues/55) | enhancement | easy | unit | The charm exposes per-target prometheus options (metrics_path, scheme, params, tls_config_ |
| 11 | cos-configuration-k8s-operator | [146](https://github.com/canonical/cos-configuration-k8s-operator/issues/146) | bug | medium | unit | The sync-now action handler _on_sync_now_action runs git-sync directly via self._exec_sync |
| 12 | cos-configuration-k8s-operator | [153](https://github.com/canonical/cos-configuration-k8s-operator/issues/153) | cleanup | easy | inspection | The git_branch config option defaults to 'master' in charmcraft.yaml. Since most repositor |
| 13 | grafana-agent-operator | [77](https://github.com/canonical/grafana-agent-operator/issues/77) | documentation | easy | inspection | The cos_agent.py library docstrings show `refresh_events=["update-status", "upgrade-charm" |
| 14 | loki-k8s-operator | [629](https://github.com/canonical/loki-k8s-operator/issues/629) | cleanup | easy | inspection | _check_alert_rules (src/charm.py:959) is misnamed and does too much: the name implies a fi |
| 15 | mimir-operators | [25](https://github.com/canonical/mimir-operators/issues/25) | cleanup | easy | inspection | The worker declares a `recovery-data` filesystem storage mounted at `/recovery-data` (work |
| 16 | observability-stack | [250](https://github.com/canonical/observability-stack/issues/250) | documentation | easy | inspection | docs/explanation/operations/index.md advertises (in its html_meta description) 'Operationa |
| 17 | polar-signals-cloud-integrator-operator | [38](https://github.com/canonical/polar-signals-cloud-integrator-operator/issues/38) | documentation | easy | inspection | Tracking issue to deprecate the charm as it converges with grafana-cloud-integrator. The f |
| 18 | prometheus-k8s-operator | [758](https://github.com/canonical/prometheus-k8s-operator/issues/758) | cleanup | easy | inspection | In lib/charms/prometheus_k8s/v1/prometheus_remote_write.py, _push_alerts_to_relation_datab |
| 19 | tempo-operators | [324](https://github.com/canonical/tempo-operators/issues/324) | cleanup | easy | inspection | The top-level product Terraform module's terraform/outputs.tf hardcodes most of the coordi |
| 20 | traefik-k8s-operator | [600](https://github.com/canonical/traefik-k8s-operator/issues/600) | documentation | easy | inspection | The integrate how-to (docs/how-to/integrate.md) shows an IngressPerAppRequirer example tha |
| 21 | traefik-k8s-operator | [640](https://github.com/canonical/traefik-k8s-operator/issues/640) | documentation | easy | inspection | IngressPerAppRequirer.__init__ in lib/charms/traefik_k8s/v2/ingress.py accepts port, strip |
| 22 | istio-beacon-k8s-operator | [166](https://github.com/canonical/istio-beacon-k8s-operator/issues/166) | bug | medium | integration-REPRODUCED-live | On config-changed, the charm reconciles waypoint resources via KubernetesResourceManager.r |
| 23 | istio-ingress-k8s-operator | [52](https://github.com/canonical/istio-ingress-k8s-operator/issues/52) | bug | medium | integration-REPRODUCED-live | When istio-ingress-k8s is deployed on a cluster without istio (no Gateway API / istio CRDs |
| 24 | prometheus-scrape-target-k8s-operator | [53](https://github.com/canonical/prometheus-scrape-target-k8s-operator/issues/53) | bug | medium | integration-REPRODUCED-live | When prometheus rejects the charm's scrape config (e.g. unquoted label values, issue #52), |
| 25 | script-exporter-operator | [16](https://github.com/canonical/script-exporter-operator/issues/16) | bug | medium | integration-REPRODUCED-live | If a bad config_file makes the systemd service fail to start, the next config-changed (eve |
| 26 | script-exporter-operator | [12](https://github.com/canonical/script-exporter-operator/issues/12) | enhancement | easy | inspection | The user-supplied script is written as an executable to /etc/script-exporter-script (src/c |
| 27 | cos-alerter | self-identified | bug | easy | unit | Config._validate_hashes (cos_alerter/alerter.py) is documented as 'Validate that keys in t |
| 28 | cos-coordinated-workers | self-identified | bug | easy | unit | PR #150 (commit 31265e9, 'feat!: migrate nginx module to charmlibs.nginx_k8s') deleted src |
| 29 | cos-lib | self-identified | bug | easy | unit | CosTool._get_tool_path (src/cosl/cos_tool.py:184-186) aliases x86_64->amd64 but does NOT a |
| 30 | observability-charm-tools | self-identified | cleanup | trivial | unit | pyproject.toml's [tool.pytest.ini_options] sets `asyncio_mode = "auto"`, but pytest-asynci |