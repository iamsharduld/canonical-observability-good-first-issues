# 04 — Confirmed bug inventory

29 candidates are typed `bug`.

## tier: integration-REPRODUCED-live (5)

| repo | issue | summary | evidence (repro_result) |
|---|---|---|---|
| istio-beacon-k8s-operator | [166](https://github.com/canonical/istio-beacon-k8s-operator/issues/166) | On config-changed, the charm reconciles waypoint resources via KubernetesResourc | LIVE-REPRODUCED 2026-06-16 (cos VM, throwaway model, no Gateway CRDs): deploy istio-beacon-k8s 1/edge --trust  |
| istio-ingress-k8s-operator | [52](https://github.com/canonical/istio-ingress-k8s-operator/issues/52) | When istio-ingress-k8s is deployed on a cluster without istio (no Gateway API /  | LIVE-REPRODUCED 2026-06-16: deploy istio-ingress-k8s 1/edge --trust, no istio -> hook failed leader-elected; h |
| loki-operators | [80](https://github.com/canonical/loki-operators/issues/80) | The coordinator's `_set_alerts` (coordinator/src/charm.py:272) writes EVERY aler | LIVE-REPRODUCED 2026-06-16 (gfi-repro VM; full loki coordinator+worker+minio+s3 stack): ran the coordinator's  |
| prometheus-scrape-target-k8s-operator | [53](https://github.com/canonical/prometheus-scrape-target-k8s-operator/issues/53) | When prometheus rejects the charm's scrape config (e.g. unquoted label values, i | LIVE-REPRODUCED 2026-06-16: prometheus-k8s + scrape-target 2/stable; labels=1bad:value -> scrape-target ACTIVE |
| script-exporter-operator | [16](https://github.com/canonical/script-exporter-operator/issues/16) | If a bad config_file makes the systemd service fail to start, the next config-ch | LIVE-REPRODUCED 2026-06-16 (lxd: ubuntu+script-exporter dev/edge): malformed config_file -> unit stuck 'hook f |

## tier: unit (9)

| repo | issue | summary | evidence (repro_result) |
|---|---|---|---|
| cos-alerter | self-identified | Config._validate_hashes (cos_alerter/alerter.py) is documented as 'Validate that | reproduced: `tox -e unit` => 54 passed, 1 deselected in 1.84s (green baseline). Isolating the validation logic |
| cos-configuration-k8s-operator | [146](https://github.com/canonical/cos-configuration-k8s-operator/issues/146) | The sync-now action handler _on_sync_now_action runs git-sync directly via self. | reproduced-by-inspection + green baseline: `tox -e unit` => unit: OK (8.5s), coverage 74%. Call trace confirms |
| cos-coordinated-workers | self-identified | PR #150 (commit 31265e9, 'feat!: migrate nginx module to charmlibs.nginx_k8s') d | REPRODUCED at runtime. Accessing each name raised: "NginxConfig access FAILED: ModuleNotFoundError -> No modul |
| cos-lib | self-identified | CosTool._get_tool_path (src/cosl/cos_tool.py:184-186) aliases x86_64->amd64 but  | confirmed: with platform.machine mocked to 'aarch64', CosTool searches for 'cos-tool-aarch64', tool.path is No |
| grafana-agent-operator | [179](https://github.com/canonical/grafana-agent-operator/issues/179) | In _update_config, after writing the config the code calls self.restart() and wr | Confirmed on HEAD ad6f720. src/grafana_agent.py:644 calls `self.restart()`; src/grafana_agent.py:647 `except G |
| juju-introspect-operator | self-identified | JujuIntrospect.install (src/jujuintrospect.py:23-24) does shutil.copy('src/confi | Confirmed at current HEAD. `grep -rn daemon_reload src/` returns nothing, so the charm writes/removes /etc/sys |
| parca-agent-operator | self-identified | get_system_arch() in src/parca_agent.py:26 reads the host architecture with plat | confirmed: baseline tox -e unit = 22 passed, 76% coverage in ~6s. On the cos VM platform.processor()=='x86_64' |
| parca-k8s-operator | self-identified | The charm declares config option memory-storage-limit with default 4096 (charmcr | confirmed-by-inspection+unit: baseline tox -e unit = 132 passed, 93% coverage in ~6s (clean tree). Observed-vs |
| prometheus-scrape-config-k8s-operator | [31](https://github.com/canonical/prometheus-scrape-config-k8s-operator/issues/31) | Setting scrape_interval="" (empty string) via juju config returns exit 0 and sho | REPRODUCED (unit). Output: 'RENDERED scrape_interval repr: ""' — i.e. jobs[0]['scrape_interval'] == '' (empty  |

## tier: inspection (12)

| repo | issue | summary | evidence (repro_result) |
|---|---|---|---|
| cos-tool | [21](https://github.com/canonical/cos-tool/issues/21) | When alert-rule validation fails, cos-tool prints the full Go stack trace to std | confirmed-by-inspection: `grep -rn '%+v'` returns exactly 3 hits -- pkg/tool/promql_transform.go:26, pkg/tool/ |
| grafana-k8s-operator | [528](https://github.com/canonical/grafana-k8s-operator/issues/528) | grafana_version() in src/grafana.py is a TOCTOU race: it guards with self._conta | Confirmed by inspection: src/grafana.py line 92 `if not self._container.can_connect(): return ""` then line 94 |
| grafana-k8s-operator | [508](https://github.com/canonical/grafana-k8s-operator/issues/508) | lib/charms/grafana_k8s/v0/grafana_dashboard.py declares PYDEPS = ["cosl >= 0.0.5 | Confirmed by inspection: line 191 `from cosl import DashboardPath40UID, LZMABase64`, line 192 `from cosl.types |
| loki-k8s-operator | [460](https://github.com/canonical/loki-k8s-operator/issues/460) | The LokiRequestLatency alert renders 'Loki request latency (instance ) (LokiRequ | Confirmed by inspection: line 6 expr = `(histogram_quantile(0.99, sum(rate(loki_request_duration_seconds_bucke |
| mimir-operators | [18](https://github.com/canonical/mimir-operators/issues/18) | The nginx reverse-proxy in the coordinator does not expose the per-component rin | Confirmed by inspection at HEAD. coordinator/src/nginx_config.py contains exactly one `/ring` route: line 33 ` |
| nrpe_exporter | self-identified | In main(), nrpe_exporter.go:206-211 wraps the server startup as `if err := http. | confirmed-by-inspection: nrpe_exporter.go:206 `if err := http.ListenAndServe(*listenAddress, nil); err != nil  |
| observability-stack | [189](https://github.com/canonical/observability-stack/issues/189) | The catalogue application deployed by the cos-lite (and cos) Terraform module is | Confirmed by inspection: catalogue config default is {} in terraform/cos-lite/variables.tf and no title/taglin |
| parca-scrape-target-operator | self-identified | In _on_collect_unit_status (src/charm.py:203-205) the BlockedStatus shown when n | confirmed-by-inspection: src/charm.py:204 contains f"Please run: `juju config {self.app.name} " and src/charm. |
| polar-signals-cloud-integrator-operator | self-identified | README.md:21 instructs users to run `juju config polar-signals-cloud bearer-toke | Confirmed at current HEAD. README.md:21 = `juju config polar-signals-cloud bearer-token="<your token>"`. The o |
| prometheus-k8s-operator | [686](https://github.com/canonical/prometheus-k8s-operator/issues/686) | GrafanaSourceProvider is constructed at import/init time with source_url=self.mo | Confirmed at HEAD 14e9a3a. Observed mismatch: src/charm.py:254 `source_url=self.most_external_url` at GrafanaS |
| signal-studio | self-identified | In backend/internal/api/handlers.go handleAnalyzeConfig parses SIGNAL_STUDIO_MAX | Confirmed by inspection: handlers.go:42-49 assigns maxSize=n with no >0 guard, unlike serve.go:38-42 (n>=5 &&  |
| tempo-operators | [257](https://github.com/canonical/tempo-operators/issues/257) | The deprecated charm_tracing charm library logs a WARNING ('charm tracing buffer | confirmed-by-inspection. The offending call is in _prune() at coordinator/lib/charms/tempo_coordinator_k8s/v0/ |

## tier: integration-assessed (1)

| repo | issue | summary | evidence (repro_result) |
|---|---|---|---|
| istio-beacon-k8s-operator | [42](https://github.com/canonical/istio-beacon-k8s-operator/issues/42) | _sync_all_resources() calls _setup_proxy_pebble_service() and then unconditional | LIVE-ASSESSED 2026-06-16: not force-reproduced (needs istio installed + manually stopping the metrics-proxy pe |

## tier: integration-not-reproducible-here (2)

| repo | issue | summary | evidence (repro_result) |
|---|---|---|---|
| istio-ingress-k8s-operator | [34](https://github.com/canonical/istio-ingress-k8s-operator/issues/34) | Deploying istio-ingress-k8s can fail with an uncaught httpx.HTTPStatusError 403  | LIVE-ATTEMPTED 2026-06-16: NOT reproducible on microk8s (istio-ingress-k8s deployed without --trust still went |
| istio-k8s-operator | [38](https://github.com/canonical/istio-k8s-operator/issues/38) | When deployed on Charmed Kubernetes, istio-k8s fails with lightkube ApiError: 'c | LIVE-ATTEMPTED 2026-06-16: NOT reproducible on microk8s (istio-k8s deployed without --trust still went active) |
