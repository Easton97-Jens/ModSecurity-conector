# Connector Parallel Runtime Smoke Plan

**Language:** English | [Deutsch](connector-parallel-runtime-smoke-plan.de.md)

Status: parallel phase started for Envoy, Traefik, and lighttpd; lighttpd
Phase 1 now selects `sidecar_proxy`.

## Why Common msconnector Contracts Are Used

`common/include/msconnector/` is the connector-neutral contract boundary for all
open connectors. Envoy, Traefik, and lighttpd must translate their own runtime
inputs into these shared shapes instead of creating connector-local copies of
request, response, intervention, status, logging, capability, origin,
transaction, or decision models.

The shared contracts currently used or reserved for the open connectors are:

| Area | Global component |
| --- | --- |
| Request mapping | `msconnector/request.h`, `msconnector/request.hpp` |
| Response mapping | `msconnector/response.h`, `msconnector/response.hpp` |
| Intervention/block decisions | `msconnector/intervention.h`, `msconnector/intervention.hpp` |
| Status values | `msconnector/status.h`, `msconnector/status.hpp` |
| Logging | `msconnector/logging.h`, `msconnector/logging.hpp` |
| Options/directives | `msconnector/options.h`, `msconnector/directives.h` |
| Capabilities | `msconnector/capabilities.h`, `msconnector/capabilities.hpp` |
| Origin/metadata | `msconnector/origin.h`, `msconnector/origin.hpp` |
| Transaction lifecycle and decision view | `msconnector/transaction.h`, `msconnector/transaction.hpp` |
| Rule-load stats | `msconnector/rule_load_stats.h` |

## Shared Logic

The parallel runtime-smoke entrypoints share result/evidence writing through:

- `common/scripts/write_smoke_result.py`
- `common/scripts/run_blocked_runtime_smoke.sh`
- `common/scripts/run_local_runtime_smoke.py`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `modules/ModSecurity-test-Framework/ci/connector-smoke-common.sh`

These helpers centralize:

- `result.json`, `summary.json`, `summary.txt`, and `results.jsonl` writing;
- the common `runtime_verified=false` / `production_ready=false` /
  `full_matrix_ready=false` / `crs_complete=false` claim defaults;
- `claims_not_allowed`;
- `missing_dependencies`;
- Exit-77 BLOCKED result semantics when local dependencies are absent;
- conditional local Envoy/Traefik/lighttpd HTTP smoke execution when local binaries are
  resolved from common.sh-managed paths;
- optional targeted Envoy/Traefik/lighttpd libmodsecurity-backed smoke execution when
  `DECISION_BACKEND=libmodsecurity` is selected and local libmodsecurity
  headers/libraries are resolved from common.sh-managed paths;
- optional minimal and secondary CRS smoke execution for Envoy, Traefik, and lighttpd when
  `DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs` is selected and
  local CRS plus local libmodsecurity are resolved from common.sh-managed paths;
- the `msconnector_decision` status/intervention/reason shape used by open C
  adapters;
- local runtime binary lookup without global `PATH` fallback;
- compatibility summary files under `$RESULTS_DIR`.

No connector-specific runtime terms are encoded in the common helpers. Each
connector passes its own connector name, integration mode, skipped reason,
missing dependency description, and architecture decision text.

## Runtime Dependency Policy

Runtime dependencies are never installed globally by connector smokes. The
smokes must not run `apt install`, `apt-get install`, `yum install`,
`dnf install`, `apk add`, `brew install`, `go install`, or `npm install -g`, and
they must not write runtime artifacts under `/usr/local`, `/usr/bin`, or `/opt`.

`modules/ModSecurity-test-Framework/ci/common.sh` is the source of truth for
runtime, build, log, cache, source, and component-cache paths. The open
connector smoke wrappers source `connector-smoke-common.sh`, which sources
`common.sh` and provides the connector-neutral lookup helpers.

`common.sh` defines the open-connector local runtime components:

- Envoy: `ENVOY_COMPONENT_ROOT`, `ENVOY_RUNTIME_ROOT`, `ENVOY_CONFIG_ROOT`,
  `ENVOY_LOG_ROOT`, `ENVOY_RESULT_ROOT`, `ENVOY_BIN`, `ENVOY_SMOKE_PORT`,
  `ENVOY_UPSTREAM_PORT`, `ENVOY_AUTHZ_PORT`, and `ENVOY_INTEGRATION_MODE`.
- Traefik: `TRAEFIK_COMPONENT_ROOT`, `TRAEFIK_RUNTIME_ROOT`,
  `TRAEFIK_CONFIG_ROOT`, `TRAEFIK_LOG_ROOT`, `TRAEFIK_RESULT_ROOT`,
  `TRAEFIK_BIN`, `TRAEFIK_SMOKE_PORT`, `TRAEFIK_UPSTREAM_PORT`,
  `TRAEFIK_AUTHZ_PORT`, and `TRAEFIK_INTEGRATION_MODE`.
- lighttpd: `LIGHTTPD_COMPONENT_ROOT`, `LIGHTTPD_RUNTIME_ROOT`,
  `LIGHTTPD_CONFIG_ROOT`, `LIGHTTPD_LOG_ROOT`, `LIGHTTPD_RESULT_ROOT`,
  `LIGHTTPD_BIN`, `LIGHTTPD_SMOKE_PORT`, `LIGHTTPD_UPSTREAM_PORT`,
  `LIGHTTPD_AUTHZ_PORT`, and `LIGHTTPD_INTEGRATION_MODE`.

The machine-readable source inventory for Envoy, Traefik, and lighttpd is
`modules/ModSecurity-test-Framework/ci/runtime-components.manifest.json`.
`common.sh` pins the current official component metadata:

- Envoy `1.38.2`, from the official Envoy GitHub releases.
- Traefik `3.7.5`, from the official Traefik GitHub releases.
- lighttpd `1.4.84`, from the official lighttpd 1.4.x release index.

The manifest mirrors the version, source URL, download URL, SHA256 URL, and
expected `$CONNECTOR_COMPONENT_CACHE/.../bin/...` path for each component.
Download execution remains disabled by default and requires explicit
`ALLOW_RUNTIME_DOWNLOADS=1` prepare execution with SHA256 verification.

Passive inventory output is available through:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Dependency lookup order:

1. explicit binary environment variable, such as `ENVOY_BIN`, `TRAEFIK_BIN`, or
   `LIGHTTPD_BIN`;
2. local common.sh-managed caches and runtime roots:
   `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
   `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT`, and
   `$SOURCE_ROOT`;
3. connector/project-defined local dependency directories under those roots;
4. Exit 77 with BLOCKED evidence if no local binary is found.

Local component staging targets are available for the open connectors:

```sh
make prepare-envoy-runtime
make prepare-traefik-runtime
make prepare-lighttpd-runtime
make prepare-lighttpd-runtime-build
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-lighttpd-runtime
ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
```

Without opt-in, they report an already staged local binary when present and
otherwise exit 77 while printing the source URL, fixed version, download URL,
SHA256 status, and expected binary path. With opt-in, Envoy downloads and
stages the direct binary, Traefik downloads the tarball and stages only the
`traefik` binary after SHA256 verification, and lighttpd stages verified source
under `$CONNECTOR_COMPONENT_CACHE/lighttpd/src`. With explicit
`ALLOW_RUNTIME_BUILDS=1`, lighttpd configures, builds, and installs the pinned
source under `$CONNECTOR_COMPONENT_CACHE/lighttpd`, with the expected binary at
`$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd`. They do not install global
packages, do not write system paths, and do not use global PATH fallback.

Examples:

```sh
ENVOY_BIN=/lokaler/pfad/envoy make smoke-envoy
TRAEFIK_BIN=/lokaler/pfad/traefik make smoke-traefik
LIGHTTPD_BIN=/lokaler/pfad/lighttpd make smoke-lighttpd
```

Optional targeted libmodsecurity-backed smokes are available for Envoy, Traefik,
and lighttpd. They use the same resolved proxy runtime binary, but switch the
auth/sidecar decision backend from the simple local decision service to a local
libmodsecurity C-API evaluator that loads
`common/rules/modsecurity_targeted_smoke.conf`:

```sh
DECISION_BACKEND=libmodsecurity make smoke-envoy
DECISION_BACKEND=libmodsecurity make smoke-traefik
DECISION_BACKEND=libmodsecurity make smoke-lighttpd
make smoke-envoy-modsecurity
make smoke-traefik-modsecurity
make smoke-lighttpd-modsecurity
```

The targeted result adds `decision_backend`, `modsecurity_backend_verified`,
`modsecurity_rule_file`, `modsecurity_rule_id`, `modsecurity_rule_loaded`,
`intervention_status`, and `decision_log_path`. It may set
`modsecurity_backend_verified=true` only when libmodsecurity loads rule
`1000001` and returns the 403 intervention for `X-Modsec-Smoke: block`.
Missing local libmodsecurity dependencies exit 77 with
`decision_backend=libmodsecurity`, `modsecurity_backend_verified=false`, and
`missing_dependencies=["libmodsecurity"]`.
The shared resolver lives in
`modules/ModSecurity-test-Framework/ci/connector-smoke-common.sh` and searches
only explicit local overrides plus common.sh-managed component, build, run, tmp,
log, and source roots. It can reuse local verified component caches under
`/tmp/ModSecurity-conector-verified` or `/var/tmp/ModSecurity-conector-verified`
without falling back to global libmodsecurity or global `pkg-config`.

Minimal CRS smokes are available for the same three open connectors:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-envoy
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-traefik
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-lighttpd
make smoke-envoy-crs
make smoke-traefik-crs
make smoke-lighttpd-crs
make smoke-open-connectors-crs
```

The CRS source-of-truth stays in `common.sh`: `CRS_REPO_URL`, `CRS_GIT_REF`,
`CRS_SOURCE_DIR`, and `CRS_RUNTIME_DIR`. The runner creates only
connector-local smoke configuration under `$<CONNECTOR>_RESULT_ROOT/crs-smoke`.
It reuses the existing minimal SQLi CRS payload
`/?id=1%20UNION%20SELECT%20password%20FROM%20users`; the blocked request must
return HTTP 403 from CRS intervention evidence, not from targeted rule
`1000001`. Successful CRS smoke writes `crs-result.json` and
`crs-decision.log`, and may set only `crs_minimal_smoke_verified=true`.
`crs_complete`, production readiness, full-matrix readiness, and response-body
verification remain false.

The secondary CRS smoke uses the same local CRS/libmodsecurity/runtime path and
only switches the CRS smoke case:

```sh
MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary make smoke-envoy
MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary make smoke-traefik
MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary make smoke-lighttpd
make smoke-envoy-crs-secondary
make smoke-traefik-crs-secondary
make smoke-lighttpd-crs-secondary
make smoke-open-connectors-crs-secondary
```

The secondary probe is
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`; it must not use the targeted rule
`1000001` or the minimal SQLi probe. Successful secondary evidence writes
`crs-secondary-result.json`, `crs-secondary-decision.log`, and
`crs-secondary-audit.log`, extracts the actual CRS rule ID/message from the
evidence, and may set only `crs_secondary_smoke_verified=true`. If CRS,
libmodsecurity, and the runtime are present but the secondary probe is not
blocked, the result is FAIL (`secondary_crs_probe_not_blocked` in inventory),
not PASS and not BLOCKED. Missing CRS, libmodsecurity, or runtime dependencies
remain Exit 77/BLOCKED.

## Connector-Specific Logic

Envoy keeps only Envoy-specific ext_authz design, configuration, smoke harness
entrypoint, and bridge-starter code. The Phase 1 runtime target is
`integration_mode=ext_authz`. When a local Envoy binary is resolved, the smoke
runner starts a minimal upstream, a minimal ext_authz decision service, and
Envoy with generated local config, then requires HTTP 200 for an allowed request
and HTTP 403 for a blocked request. `ext_proc` is deferred to a later phase.
With `DECISION_BACKEND=libmodsecurity`, the same ext_authz path uses the
targeted libmodsecurity evaluator instead of the simple decision backend. With
`MODSECURITY_RULESET=crs`, it uses the same ext_authz path for the minimal and
secondary CRS smokes and records CRS evidence separately.

Traefik keeps only Traefik-specific forwardAuth design, configuration, smoke
harness entrypoint, and local decision-service starter code. The Phase 1 runtime
target is `integration_mode=forwardAuth`. When a local Traefik binary is
resolved, the smoke runner starts a minimal upstream, a minimal forwardAuth
decision service, and Traefik with generated local config, then requires HTTP
200 for an allowed request and HTTP 403 for a blocked request. A Go plugin is
out of scope for Phase 1.
With `DECISION_BACKEND=libmodsecurity`, the same forwardAuth path uses the
targeted libmodsecurity evaluator instead of the simple decision backend. With
`MODSECURITY_RULESET=crs`, it uses the same forwardAuth path for the minimal
and secondary CRS smokes and records CRS evidence separately.

lighttpd keeps lighttpd-specific sidecar/proxy documentation, generated local
configuration, smoke harness entrypoint, and bridge starter code. The Phase 1
mode is `integration_mode=sidecar_proxy`. Native module, FastCGI/SCGI, and
mod_magnet/Lua remain deferred. When a local lighttpd binary is resolved, the
smoke runner starts lighttpd as the local upstream and a sidecar decision proxy
as the selected decision boundary, then requires HTTP 200 for an allowed request
and HTTP 403 for `X-Modsec-Smoke: block`. With `DECISION_BACKEND=libmodsecurity`,
the same sidecar path uses the targeted libmodsecurity evaluator and may set
`modsecurity_backend_verified=true` only after rule `1000001` produces the 403
intervention. With `MODSECURITY_RULESET=crs`, the same sidecar_proxy path runs
the minimal and secondary CRS smokes and records CRS evidence separately. This
remains Phase 1 sidecar_proxy evidence, not a native lighttpd module claim.

## Claims Still Forbidden

Starter/self-test evidence and BLOCKED smoke evidence must not claim:

- `runtime_verified=true`
- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`
- `crs_minimal_smoke_verified=true` without CRS-backed 200/403 evidence
- `crs_secondary_smoke_verified=true` without secondary CRS-backed 200/403 evidence
- `response_body_verified=true`

Envoy, Traefik, and lighttpd may set `runtime_verified=true` only when the local
runtime smoke observes the real HTTP 200/403 statuses through the resolved local
runtime and selected integration mode. They still must not claim production
readiness, full matrix readiness, CRS completeness, or response-body
verification. The open connectors also must not generate full-matrix reports,
production-readiness reports, or CRS-complete claims from starter/self-test
evidence.

`modsecurity_backend_verified=true` is forbidden unless the targeted
libmodsecurity smoke loaded rule `1000001` and produced the blocking
intervention through libmodsecurity. The simple decision-service smoke never
claims ModSecurity compatibility by itself.

`crs_minimal_smoke_verified=true` is forbidden unless the CRS smoke loaded CRS
from local common.sh-managed paths and observed a CRS-backed HTTP 403 with a
CRS rule ID/message. Even then, `crs_complete=true` remains forbidden.

`crs_secondary_smoke_verified=true` is forbidden unless the secondary CRS smoke
loaded CRS from local common.sh-managed paths, sent the secondary XSS probe, and
observed a CRS-backed HTTP 403 with an extracted CRS rule ID/message. Even
then, `crs_complete=true` remains forbidden.

## Parallel Runtime-Smoke Artifacts

Each connector writes connector-specific artifacts:

| Connector | Evidence root | Fallback |
| --- | --- | --- |
| Envoy | `$VERIFIED_RUN_ROOT/envoy-smoke/` | `$BUILD_ROOT/results/envoy-smoke/` |
| Traefik | `$VERIFIED_RUN_ROOT/traefik-smoke/` | `$BUILD_ROOT/results/traefik-smoke/` |
| lighttpd | `$VERIFIED_RUN_ROOT/lighttpd-smoke/` | `$BUILD_ROOT/results/lighttpd-smoke/` |

Each `result.json` contains at least:

- `connector`
- `integration_mode`
- `runtime_verified`
- `full_matrix_ready`
- `production_ready`
- `crs_complete`
- `response_body_verified`
- `allowed_request_status`
- `blocked_request_status`
- `evidence_root`
- `timestamp`
- `skipped_reason`
- `missing_dependencies`
- `claims_not_allowed`
- `crs_secondary_smoke_verified`
- `crs_smoke_case`

The manual workflow `.github/workflows/open-connectors-smoke.yml` runs the open
connector runtime path with `TMPDIR=/tmp`, prepares shared runtime components
through `make prepare-runtime-components` for local libmodsecurity and CRS
inputs, then prepares Envoy, Traefik, and Lighttpd runtime components. It
executes simple, targeted libmodsecurity, minimal CRS, and secondary CRS smokes,
and uploads `ci-artifacts/open-connectors/` as
`open-connectors-smoke-evidence` even when an earlier prepare or smoke step
fails. The temporary narrow `push` trigger on the workflow file is only a
diagnosis aid. The artifact is a copied evidence bundle from
`/tmp/ModSecurity-conector-verified/` plus runtime inventory output; it is not a
production, full-matrix, CRS-complete, or response-body claim.

## Current Expected Outcomes

`make smoke-envoy`, `make smoke-traefik`, and `make smoke-lighttpd` are targeted
runtime-smoke entrypoints. In environments without the selected local runtime
binaries, they must exit 77 with BLOCKED evidence rather than reporting success.
With local Envoy or Traefik binaries, success is allowed only after a real local
HTTP smoke produces the expected 200/403 statuses.

Current blockers:

- Envoy: BLOCKED when local `envoy` binary is not available through `ENVOY_BIN`
  or common.sh-managed local paths.
- Traefik: BLOCKED when local `traefik` binary is not available through
  `TRAEFIK_BIN` or common.sh-managed local paths.
- lighttpd: BLOCKED when local `lighttpd` binary is not available through
  `LIGHTTPD_BIN` or common.sh-managed local paths, or when the pinned source
  build cannot run locally. Source download and local build both require
  explicit opt-in.

## Duplicate Avoidance

The previous connector-local inline JSON writers in the Envoy, Traefik, and
lighttpd harnesses have been replaced by common helpers. The connector harnesses
now provide adapter parameters only. The small connector-local decision result
structs have also been replaced with aliases to `msconnector_decision`, leaving
only connector-specific adapter function names. Request, response, status,
intervention, capability, origin, logging, transaction, and decision contracts
remain in `common/include/msconnector/`.

Apache, HAProxy, and Nginx are not modified by this parallel phase.
