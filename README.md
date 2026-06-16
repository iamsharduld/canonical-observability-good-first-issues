# Canonical Observability — Good First Issues

A repo-by-repo hunt for beginner-friendly issues across **all 58 repositories** owned by
Canonical's Observability team (the `canonical/observability` manifest + team extras),
each candidate **reproduced/verified** and recorded in a CSV.

Generated 2026-06-16.

## Deliverables
- `results/<repo>.csv` — one file per repo, 1–2 candidates each (17 columns; see `meta/CSV_SCHEMA.md`).
- `results/_master_index.csv` — all 104 candidates in one file.
- `meta/` — the repo universe (`repos.tsv`), active/archived split, validation, and the
  `compile.py` / `normalize.py` tooling.

## Coverage
| | count |
|---|---|
| Repos covered | **58 / 58** (0 missed) |
| Candidates | **104** |
| Active repos (full hunt) | 47 |
| Archived repos (documented, not actionable) | 11 |

By source: 65 self-identified · 39 from existing open issues
By type: 29 bug · 22 cleanup · 21 docs · 11 archived-notice · 8 version-bump · 6 goss-gap · 3 enhancement · 2 metadata · 1 test · 1 build
By reproduction tier: **79 inspection · 16 unit-reproduced · 8 integration (need live deploy) · 1 static**

## Methodology
- **Find:** No `good first issue` labels are populated org-wide (only traefik/cos-lib had a few),
  so candidates were chosen by judgment — preferring genuine open issues, otherwise
  self-identified from the code. Obsolete/already-fixed labeled issues were explicitly skipped
  (e.g. cos-lib #145/#100/#119, parca-scrape-target #55, cos-proxy #165, pyroscope #285, loki-operators #66).
- **Reproduce (tiered):** all work ran in the existing `cos` Multipass VM.
  - *inspection* — prove the issue in code with exact `file:line` evidence.
  - *unit* — clone + run the repo's unit tests (`tox -e unit`) and capture the failing test / behaviour.
  - *integration* — needs a live Juju deploy; **not** executed (see below), but the bug is code-confirmed and a runtime repro plan is recorded.
- **Read-only:** no outbound writes — no issue/PR comments, no PRs, nothing pushed. GitHub was read via `gh` only; the live `cos` Juju model was never touched.
- Go and Terraform are not installed on the VM, so Go repos (cos-tool, nrpe_exporter, signal-studio) and Terraform (observability-stack) were verified at inspection tier.

## A few standout beginner picks
| Repo | Issue | Type | Why it's a good first issue |
|---|---|---|---|
| cos-lib | #29 (GFI label) | cleanup | add a shared `get_host_architecture()` helper; also fixes a real arm64 bug (unit-reproduced) |
| loki-k8s-operator | #460 | bug | alert rule aggregates `by (le)` but title uses `{{ $labels.instance }}` → mangled title |
| prometheus-k8s-operator | #758 | cleanup | replace truthiness guard with explicit `is not None` on an Optional relation |
| grafana-agent-k8s-operator | #339 | enhancement | add a `log_level` config option (currently hardcoded "info") |
| cos-configuration-k8s-operator | #153 | cleanup | default `git_branch` is still `master`; change to `main` |
| script-exporter-operator | #12 (GFI label) | cleanup | move the generated executable out of `/etc` |
| tempo-operators | #257 (GFI label) | bug | lower a noisy `logger.warning` + bump LIBPATCH |
| traefik-k8s-operator | #600 | docs | how-to uses `self.ingress.ready` (AttributeError); correct form is `.on.ready` |
| observability-stack | #189 | bug | catalogue page has no title/tagline/description (unbranded) |
| cos-tool | #21 | bug | stop printing Go stack traces — three exact `%+v` sites |
| cos-alerter | self-identified | bug | `_validate_hashes` accepts any 128-char string as SHA-512 (not hex) — unit-reproduced |
| parca-agent-operator | self-identified | bug | uses `platform.processor()` (often "") instead of `platform.machine()` — unit-reproduced |

## Integration-tier escalations (8) — live reproduction attempted
Deployed in throwaway Juju models on the existing `cos` VM (microk8s + lxd), never touching the
live `cos` model; all repro models torn down and istio cluster artifacts scrubbed afterwards.
Full log: `results/_live_repro_log.md`.

**Reproduced live (5):**
- istio-beacon-k8s #166 — config-changed crashes with `httpx 404` on absent `gateway.networking.k8s.io` CRD ✅
- istio-ingress-k8s #52 — leader-elected crashes with `httpx 404` on absent `security.istio.io` CRD, before the readiness guard ✅
- prometheus-scrape-target-k8s #53 — `labels=1bad:value` → charm stays **Active** while `promtool` rejects the config (`"1bad" is not a valid label name`) ✅
- script-exporter #16 — malformed `config_file` wedges config-changed (unit stuck "awaiting error resolution"); found a 2nd unguarded crash point at charm.py:186 ✅
- loki-operators #80 — on a **dedicated VM** with the full loki coordinator+worker+minio+s3 stack, the coordinator's `lokitool rules sync <valid> <invalid>` aborts the whole batch (`unable to parse rules files`) while a valid-only sync proceeds — one bad rule blocks all ✅

**Not reproducible on microk8s (2)** — environment-specific, need Charmed Kubernetes' stricter RBAC:
- istio-k8s #38 / istio-ingress-k8s #34 — both charms deploy fine *without* `--trust` on microk8s, so the missing-RBAC path never triggers here.

**Code-confirmed, runtime race not deterministically forceable (1):**
- istio-beacon-k8s #42 — sets Active before confirming the metrics-proxy is up; the bug only fires when the proxy container's pebble is unreachable (`!can_connect()`), which can't be forced at runtime without breaking the container. Logic confirmed in code.

## Caveats
- **Archived repos (11):** bundles, `karma-*`, `mimir-k8s`, `parca-operator`, and the old
  `tempo-k8s/worker/coordinator` are read-only (superseded by the `*-operators` monorepos /
  Terraform in observability-stack). Each has a one-row CSV pointing to its successor.
- **`cos-configuration-rules-dashboards`** is an empty stub — advertises sample rules/dashboards
  but ships only LICENSE + README.
- **Rock version-bumps** (e.g. s3proxy 2.0.0→3.2.0, prometheus 3.11.3→3.12.0) may be handled by
  the repos' update-automation bots; flagged in each CSV's notes.
