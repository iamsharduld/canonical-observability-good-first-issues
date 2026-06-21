# 07 — Independent verification & final curated list

_Verified 2026-06-22 by re-checking every claim against the **current upstream `main`/HEAD**
of each `canonical/*` repo via `gh api` (raw file contents, issue state, repo flags).
The original dataset was generated 2026-06-16; this pass questions its assumptions and
separates genuine, still-open issues from stale / fixed / misclassified ones._

## What was verified, and how

| Scope | Coverage | Method |
|---|---|---|
| `type=bug` candidates | **29 / 29** | fetched the cited source file at HEAD; matched the claim by **content**, not line number (lines had drifted) |
| Referenced GitHub issues | **39 / 39** | `gh api .../issues/N` → state + state_reason |
| Archived-repo claims | **11 / 11** | `gh api repos/... --jq .archived` |
| Self-identified non-bug (docs/cleanup) | sampled **14** across 12 repos | fetched cited file:line |
| README "standout picks" | **12 / 12** | fetched cited evidence |

Bottom line: **the dataset is accurate and well-evidenced.** Of 104 candidates, **2 are no
longer actionable** and **3 need reclassification / corrected evidence**. Everything else I
checked held up against live code.

---

## A. Corrections — candidates that are NOT what the dataset says (5)

### 1. `loki-k8s-operator` #460 (bug) — **FIXED; no longer reproduces** ⛔
The dataset (and the README "standout picks" table) describe an `expr` aggregating `by (le)`
with a summary using `{{ $labels.instance }}`. The **current** rule file is already corrected:
```
expr: ... by (namespace, job, route, le)   # labels preserved
summary: Loki request latency for route {{ $labels.route }} (job {{ $labels.job }})
```
Fixed by **PR #563 / commit `c280fd16` on 2026-06-16** — the same day the dataset was generated,
so it captured the pre-fix state. The GitHub issue is still _open_ (maintainers haven't closed
it), but the bug as described cannot reproduce. **Remove from the actionable list / verify-and-close.**

### 2. `cos-coordinated-workers` #11 (cleanup) — **now CLOSED (not_planned)** ⛔
The dataset already flagged this as "obsolete / already-implemented" and recommended closing.
It has since been **closed as not_planned**. The dataset's call was correct; it is no longer actionable.

### 3. `parca-k8s-operator` — `memory-storage-limit` (typed **bug**) → **trivial cleanup, not a runtime bug** ⚠️
`charmcraft.yaml` defaults the option to `4096`, and `src/charm.py:178` always passes that config
value into `Parca(...)`. So the `(memory_storage_limit or 1024)` fallback at `src/parca.py:208`
is **unreachable in a normal deploy** — the deployed charm uses 4096, matching the README. This is
a latent code-consistency nit (the function's internal default 1024 ≠ the charm default 4096),
worth tidying but **not a user-facing bug**. Down-classify bug → cleanup, low priority.

### 4. `prometheus-k8s-operator` #758 (cleanup) — **location accurate, but the "AttributeError" cannot occur** ⚠️
Correctly located at `lib/charms/prometheus_k8s/v1/prometheus_remote_write.py:508`:
`{unit.name for unit in peer_relations.units} if peer_relations else set()`. But `if peer_relations`
(truthiness) **already** handles the `None` return from `get_relation` (None → `set()`), and an ops
`Relation` object is always truthy — so the `AttributeError` the (Copilot-sourced) issue warns about
**cannot actually be raised**. It is a readability/explicitness nit, not a latent crash. Still a valid
trivial cleanup since the maintainer filed it, but the "bug" framing is overstated.

### 5. `grafana-k8s-operator` #508 (bug) — **real bug, but the dataset's evidence is wrong** ⚠️
The dataset blames `DashboardPath40UID` as "only available in newer cosl." Verified against cosl tags:
`DashboardPath40UID` **is present in cosl 0.0.50** (the PYDEPS floor `cosl >= 0.0.50`), so that
reasoning is incorrect. The **actual** culprit (confirmed by the maintainer's issue body and by tag
inspection) is `from cosl.types import type_convert_stored`, which requires **cosl ≥ 1.3.0**
(`cosl.types.type_convert_stored` exists in no 0.0.x release). The under-constrained PYDEPS is a
**genuine bug** — keep it — but cite `type_convert_stored`, not `DashboardPath40UID`.

### Also note (not a correction, a caveat)
- `polar-signals-cloud-integrator-operator` README `bearer-token` vs `bearer_token` (bug): the mismatch
  is real, **but the charm is slated for deprecation** (open issue #38 "Deprecate this charm"), which
  lowers the value of fixing its docs.

---

## B. Confirmed real bugs — higher value (16)

**Live-reproduced by the dataset; code path re-confirmed present at HEAD (5):**
| Repo | Issue | One-line |
|---|---|---|
| istio-beacon-k8s-operator | #166 | `config-changed` reconcile lists Gateway CRDs with no 404 guard → error state (paths `_sync_waypoint_resources`→`reconcile`, no httpx guard) |
| istio-ingress-k8s-operator | #52 | reconcile calls at `charm.py:922/946` run **before** the `_is_ready()` guard at `:1032` → uncaught httpx 404 with no CRDs |
| loki-operators | #80 | `_set_alerts` runs one atomic `lokitool rules sync <all files>` (`charm.py:296`) — one bad rule blocks the whole batch |
| prometheus-scrape-target-k8s-operator | #53 | `_update_prometheus_jobs` sets `ActiveStatus()` (`charm.py:92`) without reading back `scrape_job_errors` from the databag |
| script-exporter-operator | #16 | `_create_systemd_service` calls `service_restart`+`service_resume` (`charm.py:301/304`) with no guard → `SystemdError` wedges the unit |

**Code-confirmed at HEAD (11):**
| Repo | Issue | One-line |
|---|---|---|
| cos-alerter | self | `_validate_hashes` (`alerter.py:43`) checks only `len==128`, no hex → accepts `'z'*128` as a SHA-512 |
| cos-configuration-k8s-operator | #146 | `_on_sync_now_action` calls `_exec_sync_repo()` (`:285`) then `_common_exit_hook()` (`:300`) which calls it again (`:257`) → git-sync runs twice |
| cos-coordinated-workers | self | `__init__.py` still lazy-maps `Nginx*` to the **deleted** `.nginx` module → `ModuleNotFoundError` on attribute access; `README.md:8` links the deleted file |
| cos-lib | #29 / self | `_get_tool_path` (`cos_tool.py:184-186`) aliases only `x86_64`→`amd64`; on arm64 `platform.machine()`=`aarch64` → looks for `cos-tool-aarch64` (binary is `-arm64`) |
| cos-tool | #21 | `%+v` on `pkg/errors` values at `promql_transform.go:26`, `logql_transform.go:22`, `compat.go:23` → Go stack traces into `juju debug-log` |
| grafana-agent-operator | #179 | `_update_config` catches `GrafanaAgentReloadError`/`APIError`, but the snap `restart()` (`charm.py:438`) raises `GrafanaAgentServiceError` → real failures uncaught |
| grafana-k8s-operator | #528 | `grafana_version()` (`grafana.py:92-94`) guards `can_connect()` then `exec().wait_output()` with no try/except → TOCTOU `FileNotFoundError` |
| grafana-k8s-operator | #508 | PYDEPS `cosl >= 0.0.50` but imports `cosl.types.type_convert_stored` (needs ≥1.3.0) — see correction A.5 |
| mimir-operators | #18 | `nginx_config.py` exposes only `/ruler/ring`; `/compactor/ring`, `/ingester/ring`, `/store-gateway/ring` blocks are absent |
| prometheus-scrape-config-k8s-operator | #31 | `_prometheus_configurations` pushes every config item (incl. `scrape_interval=""`) verbatim into jobs (`charm.py:136/143`) |
| prometheus-k8s-operator | #686 | `GrafanaSourceProvider` built with `most_external_url` (`charm.py:254`), only later `update_source(internal_url)` (`:693`) — external URL window when ingress set |
| observability-stack | #189 | catalogue Terraform module gets `config = var.catalogue.config` defaulting to `{}` → unbranded landing page |

> RBAC pair (istio-ingress #34, istio-k8s #38): code paths confirmed (cluster-scoped lightkube
> list/patch), maintainer issues open, but the dataset honestly notes they are **not reproducible on
> microk8s** (need Charmed Kubernetes' stricter RBAC). Real, but environment-gated.

---

## C. Confirmed real, but minor / cosmetic / latent (7)

| Repo | Issue | Why it's low-severity |
|---|---|---|
| istio-beacon-k8s-operator | #42 | logic confirmed (Active set after a proxy setup that early-returns on `!can_connect`), but the race can't be force-triggered at runtime |
| nrpe_exporter | self | `nrpe_exporter.go:210` "Listening" log is unreachable (after blocking `ListenAndServe`) — cosmetic log ordering |
| parca-scrape-target-operator | self | `BlockedStatus` f-string (`charm.py:202-205`) opens a backtick it never closes — cosmetic markdown |
| juju-introspect-operator | self | `install`/`remove` write/remove a unit file with no `daemon_reload` — latent/version-dependent robustness |
| parca-agent-operator | self | `get_system_arch` uses `platform.processor()` (`:26`), which returns `""` on many distros → empty ARCH; env-dependent (didn't fire on the test VM) |
| signal-studio | self | `handleAnalyzeConfig` `maxSize` has no `>0` guard (unlike `serve.go:40`'s `n>=5 && n<=30`) — needs env misconfiguration to bite |
| tempo-operators | #257 | deprecated `charm_tracing` lib logs a repeated WARNING on buffer overflow — log noise only (vendored; needs LIBPATCH bump) |

---

## D. Non-bug, still-actionable — maintainer-filed (open issues), inherently valid

These reference **real open GitHub issues** (all confirmed `open` on 2026-06-22), so their existence
is maintainer-acknowledged; the dataset just frames them as good-first-issues. Spot-checks that
touched code all matched:

- `cos-configuration-k8s` **#153** — `git_branch` default still `master` (charmcraft.yaml:122) ✔ verified
- `grafana-agent-k8s` **#339** — add `log_level` config; value hardcoded at `grafana_agent.py:896` `{"log_level": "info"}` ✔ verified
- `traefik-k8s` **#600** — how-to uses `self.ingress.ready` (should be `.on.ready`) at `integrate.md:62-63` ✔ verified
- `script-exporter` **#12** — script written to `/etc/script-exporter-script` (charm.py:52) ✔ verified
- plus #629, #25, #324, #23, #77, #94, #81, #61, #250, #55, #44, #640 (open; not deep-checked — the open issue is the verification).

## E. Non-bug self-identified docs/cleanup — sampled, reliable

Every one I fetched matched live source: `alertmanager-k8s` README `run-action --wait` (l.96);
`avalanche` dead `_on_alertmanager_config_changed` (l.278, never observed) + stale `_update_layer`
docstring; `catalogue` README `dashboard_info` (l.14, should be `catalogue`) + dead
`_is_valid_unit_address`; `cos-proxy` `requires-python = "~=3.8"` (l.6) + `cs:` deploy docs;
`cos-alerter` README docker-filename mismatch; `cos-configuration-rules-dashboards` is genuinely a
2-file stub (LICENSE + README only); `o11y-tester` broken docs URL (charmcraft.yaml:10);
`parca-k8s` placeholder `"""Model ."""` (models.py:44); `prometheus-pushgateway` / `prometheus-scrape-config`
old `from ops.main import main` idiom. **No discrepancies found in this tier.**

## F. Archived (11) — correctly documented, not actionable

All confirmed `archived=true`: cos-lite-bundle, mimir-bundle, tempo-bundle,
karma-k8s-operator, karma-alertmanager-proxy-k8s-operator, mimir-k8s-operator, parca-operator,
tempo-k8s-operator, tempo-worker-k8s-operator, tempo-coordinator-k8s-operator, traefik-route-k8s-operator.

---

## Final tally

| Verdict | Count |
|---|---|
| Confirmed real bug — higher value | 16 |
| Confirmed real bug — minor/cosmetic/latent | 7 |
| **Total still-valid bugs** | **23** (of 29) |
| Fixed / closed — drop | 2 (loki-k8s #460, cos-coordinated-workers #11) |
| Reclassify (bug→cleanup / overstated) | 2 (parca-k8s mem-limit, prometheus-k8s #758) |
| Evidence-correction (still valid) | 1 (grafana-k8s #508) |
| Non-bug actionable (docs/cleanup/enh/test/version) verified or open-issue-backed | ~62 |
| Archived (documented, not actionable) | 11 |
</content>
</invoke>
