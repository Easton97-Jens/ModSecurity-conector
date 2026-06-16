> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:27:09Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/run-verified-report-run.py`
> Make target: `verified-report-run`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `blocked`

# Verified Run Manifest

## Summary

| Field | Value |
|---|---|
| Verified run id | `2026-06-15T21-01-39Z-9391a8d0` |
| Data source policy | `verified-inputs-only` |
| Profile | `full` |
| Start time UTC | `2026-06-16T16:22:07Z` |
| End time UTC | `2026-06-16T16:27:09Z` |
| Duration seconds | `302.0` |
| Input status | `blocked` |

## Runtime Environment

| Field | Value |
|---|---|
| Connector SHA | `efac6d66d0e165af8d6e1b5404083d5f50601327` |
| Framework SHA | `04e31a60676eebba86be2a4c1510ff596e37ba2f` |
| MRTS SHA | `13aa91291adea12d5c607fdd165d010fcfb1da78` |
| Connector branch | `master` |
| Framework branch | `master` |
| Dirty status | `dirty` / `dirty` |
| Runtime matrix timeout seconds | `1800` |
| Full matrix runtime timeout seconds | `7200` |
| Report refresh timeout seconds | `1800` |
| Native MRTS timeout seconds | `1800` |

## Runtime Paths

| Variable | Value | Status | Notes |
|---|---|---|---|
| `VERIFIED_RUN_ROOT` | `/var/tmp/ModSecurity-conector-verified` | PASS | ok |
| `VERIFIED_BUILD_ROOT` | `/var/tmp/ModSecurity-conector-verified/build` | PASS | ok |
| `VERIFIED_SOURCE_ROOT` | `/var/tmp/ModSecurity-conector-verified/src` | PASS | ok |
| `VERIFIED_TMP_ROOT` | `/var/tmp/ModSecurity-conector-verified/tmp` | PASS | ok |
| `VERIFIED_LOG_ROOT` | `/var/tmp/ModSecurity-conector-verified/logs` | PASS | ok |
| `VERIFIED_COMPONENT_CACHE` | `/var/tmp/ModSecurity-conector-verified/component-cache` | PASS | ok |
| `NGINX_HARNESS_PARENT` | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | PASS | ok |
| `BUILD_ROOT` | `/var/tmp/ModSecurity-conector-verified/build` | PASS | ok |
| `SOURCE_ROOT` | `/var/tmp/ModSecurity-conector-verified/src` | PASS | ok |
| `TMP_ROOT` | `/var/tmp/ModSecurity-conector-verified/tmp` | PASS | ok |
| `LOG_ROOT` | `/var/tmp/ModSecurity-conector-verified/logs` | PASS | ok |
| `CONNECTOR_COMPONENT_CACHE` | `/var/tmp/ModSecurity-conector-verified/component-cache` | PASS | ok |

## Worker Accessibility / Preflight

| Check | Status | Path | Notes |
|---|---|---|---|
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | outside /root |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | current process can traverse; per-case worker checks are recorded in nginx-worker-preflight.jsonl |

## Runtime Producer Readiness

- Status: `BLOCKED`
- Runtime env loaded: `False`
- Runtime env path: `/var/tmp/ModSecurity-conector-verified/component-cache/runtime-env.sh`

| Component | Required | Status | Path | Fix |
|---|---|---|---|---|
| common.sh | True | present | `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/common.sh` | `ensure FRAMEWORK_ROOT points at modules/ModSecurity-test-Framework` |
| NGINX binary | True | missing | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/sbin/nginx` | `run make prepare-runtime-components` |
| NGINX ModSecurity module | True | missing | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so` | `run make prepare-runtime-components` |
| NGINX libmodsecurity | True | missing | `/root/git/ModSecurity-conector/libmodsecurity.so` | `run make prepare-runtime-components` |
| Apache/httpd | True | missing | `` | `run make prepare-runtime-components` |
| Apache/APXS | True | missing | `` | `run make prepare-runtime-components` |
| Apache ModSecurity module | True | missing | `` | `run make prepare-runtime-components` |
| HAProxy binary | True | missing | `/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime/haproxy/sbin/haproxy` | `run make prepare-runtime-components` |
| HAProxy SPOA runtime | True | missing | `` | `run make prepare-runtime-components` |
| HAProxy binding metadata | True | missing | `` | `run make prepare-runtime-components` |
| go-ftw | False | missing | `` | `optional native MRTS: install or cache go-ftw` |
| albedo | False | missing | `` | `optional native MRTS: install or cache albedo` |

## NGINX Runtime Module Readiness

| Field | Value |
|---|---|
| NGINX_BIN | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/modules` |
| ModSecurity module path | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so` |
| Module exists | `false` |
| How to prepare | `make prepare-runtime-components` |

## Runtime Network / Cache Readiness

| Source | Status | Path | Notes |
|---|---|---|---|
| nginx latest release | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx/nginx-latest-release.json` | network may be required unless this cache is prefilled |
| nginx archive cache | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx` | network may be required unless this cache is prefilled |
| go-ftw git cache | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/git/go-ftw` | network may be required unless this cache is prefilled |
| albedo git cache | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/git/albedo` | network may be required unless this cache is prefilled |

## Producer Commands

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `-` | not_run | - | - | - | - | `-` |

## Consumer / Refresh Commands

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `-` | not_run | - | - | - | - | `-` |

## Checks

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `make check-generated-report-layout` | FAIL | 2 | 0.77 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/01-make-check-generated-report-layout.log` |
| `make lint` | FAIL | 2 | 2.425 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/02-make-lint.log` |
| `make quick-check` | FAIL | 2 | 2.425 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/03-make-quick-check.log` |
| `make check-generated-report-layout` | FAIL | 2 | 0.769 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/04-make-check-generated-report-layout.log` |
| `make lint` | FAIL | 2 | 2.424 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/05-make-lint.log` |
| `make quick-check` | FAIL | 2 | 2.374 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/06-make-quick-check.log` |
| `make check-generated-report-layout` | FAIL | 2 | 0.768 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/07-make-check-generated-report-layout.log` |
| `make lint` | FAIL | 2 | 2.374 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/08-make-lint.log` |
| `make quick-check` | FAIL | 2 | 2.375 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/09-make-quick-check.log` |
| `make check-generated-report-layout` | FAIL | 2 | 0.769 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/10-make-check-generated-report-layout.log` |
| `make lint` | FAIL | 2 | 2.425 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/11-make-lint.log` |
| `make quick-check` | FAIL | 2 | 2.425 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/logs/12-make-quick-check.log` |

## Full-Matrix Job Completeness

| Field | Value |
|---|---|
| Completeness | `0/0` |
| Overall status | `unknown` |
| Missing jobs | `-` |
| Timeout jobs | `-` |

| Slowest Job | Duration Seconds | Status |
|---|---:|---|
| `-` | - | unknown |

## Runtime Mismatch Summary

| Field | Value |
|---|---|
| Total mismatches | `unknown` |
| Critical mismatches | `unknown` |
| Top connector | `unknown` |
| Primary blocker | `unknown` |
| Merge readiness | `unknown` |

## Blocked / Stale Inputs

| Item | Status | Reason | Affected Reports |
|---|---|---|---|
| `BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl` | missing | input file missing | - |
| `BUILD_ROOT:mrts-native/apache2_ubuntu/job.json` | missing | input file missing | - |
| `BUILD_ROOT:mrts-native/nginx-pr24/job.json` | missing | input file missing | - |
| `full_runtime_matrix` | skipped_missing_input | required input missing or empty | reports/testing/generated/canonical/full-runtime-matrix.generated.json, reports/testing/generated/canonical/full-runtime-matrix.generated.md |
| `full_matrix_job_completeness` | skipped_missing_input | required input missing or empty | reports/testing/generated/manifest/full-matrix-job-completeness.generated.json, reports/testing/generated/manifest/full-matrix-job-completeness.generated.md |
| `verified_runtime_mismatch_analysis` | skipped_missing_input | required input missing or empty | reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json, reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md |
| `native_mrts_reports` | skipped_missing_input | required input missing or empty | reports/testing/generated/mrts-native/mrts-native-full.generated.json, reports/testing/generated/mrts-native/mrts-native-full.generated.md, reports/testing/generated/mrts-native/mrts-native-apache.generated.json, reports/testing/generated/mrts-native/mrts-native-apache.generated.md, reports/testing/generated/mrts-native/mrts-native-nginx.generated.json, reports/testing/generated/mrts-native/mrts-native-nginx.generated.md, reports/testing/generated/mrts-native/mrts-native-summary.generated.json, reports/testing/generated/mrts-native/mrts-native-summary.generated.md |
| `nginx_mrts_http500_cluster_analysis` | blocked | required generated input is blocked | reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json, reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md |
| `connector_work_queue` | blocked | required generated input is blocked | reports/testing/generated/work-queues/connector-work-queue.generated.json, reports/testing/generated/work-queues/connector-work-queue.generated.md |
| `phase_work_queue` | blocked | required generated input is blocked | reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `nolog_audit_evidence` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json, reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `response_header_hook_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json, reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `phase4_hard_abort_capability` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json, reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `remaining_failure_analysis` | blocked | required generated input is blocked | reports/testing/generated/canonical/remaining-failure-analysis.generated.json, reports/testing/generated/canonical/remaining-failure-analysis.generated.md, reports/testing/generated/canonical/next-fix-plan.generated.json, reports/testing/generated/canonical/next-fix-plan.generated.md, reports/testing/generated/canonical/full-run-evidence.generated.json, reports/testing/generated/canonical/full-run-evidence.generated.md |
| `intervention_blocking_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json, reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md |
| `no_mrts_intervention_nomatch_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json, reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md |
| `body_processor_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/body-processor-analysis.generated.json, reports/testing/generated/focused-analysis/body-processor-analysis.generated.md |
| `rule_chain_semantics_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json, reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md |
| `final_consistency_audit` | blocked | required generated input is blocked | reports/testing/generated/canonical/final-consistency-audit.generated.json, reports/testing/generated/canonical/final-consistency-audit.generated.md |
| `runtime_cache_reports` | blocked | required generated input is blocked | reports/testing/generated/cache/runtime-component-cache.generated.json, reports/testing/generated/cache/runtime-component-cache.generated.md, reports/testing/generated/cache/runtime-build-cache.generated.json, reports/testing/generated/cache/runtime-build-cache.generated.md |

## Tool Versions

| Tool | Status | Version / Output |
|---|---|---|
| git | present | `git version 2.53.0` |
| python3 | present | `Python 3.14.4` |
| python | present | `Python 3.14.4` |
| make | present | `GNU Make 4.4.1` |
| bash | present | `GNU bash, version 5.3.9(1)-release (x86_64-pc-linux-gnu)` |
| sh | present | `POSIX shell available (/usr/bin/dash)` |
| gcc | present | `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0` |
| clang | present | `Ubuntu clang version 21.1.8 (6ubuntu1)` |
| go | present | `go version go1.26.0 linux/amd64` |
| go-ftw | missing | `command not found` |
| albedo | missing | `command not found` |
| actionlint | missing | `command not found` |
| jq | present | `jq-1.8.1` |
| curl | present | `curl 8.18.0 (x86_64-pc-linux-gnu) libcurl/8.18.0 OpenSSL/3.5.5 zlib/1.3.1 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.68.0 librtmp/2.3 mit-krb5/1.22.1 OpenLDAP/2.6.10` |
| docker | missing | `command not found` |
| apachectl | missing | `no candidate found: apachectl` |
| apache/httpd | missing | `no candidate found: apache2 httpd apachectl` |
| nginx | missing | `no candidate found: nginx` |
| haproxy | configured_missing | `file not found` |
| apxs | missing | `no candidate found: apxs apxs2` |

## Git Evidence

| Repository | SHA | Branch | Dirty Status |
|---|---|---|---|
| connector | `efac6d66d0e165af8d6e1b5404083d5f50601327` | `master` | `dirty` |
| framework | `04e31a60676eebba86be2a4c1510ff596e37ba2f` | `master` | `dirty` |
| MRTS | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | `dirty` |

## Proof Summary

| Claim | Status | Evidence |
|---|---|---|
| Runtime paths outside /root by default | `PASS` | `VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified` |
| NGINX docroot preflight evidence | `PASS` | `nginx-worker-preflight.jsonl` rows are included when NGINX smoke ran |
| Verified inputs only | `PASS` | `verified-inputs-only` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | `1f5f002a2b16fd89d9081a24fbcc571218b25741dd63afa2fc961cdbeb17c2e5` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `ae5644b7e45dc2fedaa289b57881489257e53a99bc341d1ad853fb3a84eda33a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/system-environment-proof.generated.json` | `af1f5050459472dad60121188db7c99f396141e628e44c4d0198bb7faabea1cf` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `63c224e072428210f66b357e0b6bcdaffaf8435ba571277d625452943e31eed9` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | input file available |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/system-environment-proof.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
