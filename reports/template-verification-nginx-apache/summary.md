# Verification Summary

Status: reviewed

Updated: 2026-05-31 00:00:00 UTC

## Readiness

- Documentation/decision commit readiness: yes.
- Commit-fertig fuer Dokumentations-/Entscheidungsstand: ja.
- Default runtime smoke readiness: blocked unless dependencies are prepared in
  the default build root.
- Last documented default blocker:
  `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  missing.
- Current `/src` `make smoke-common`: PASS; Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make test-no-crs`: PASS; Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 60 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make test-with-crs`: PASS; Apache 55 PASS, 0 FAIL,
  0 BLOCKED; NGINX 61 PASS, 0 FAIL, 0 BLOCKED.
- RESPONSE_BODY blocking: not verified.
- Envoy build readiness: sidecar/HTTP bridge-starter; runtime-smoke entrypoint
  exists and reports BLOCKED; no local `connectors/envoy/tests` folder.
- Vollstaendige Runtime-Verifikation: nein.
- lighttpd bridge-starter checked/updated: yes; it follows global connector gates,
  uses shared rules instead of duplicating them, has no runtime evidence, and
  has no local `connectors/lighttpd/tests` folder.
- Submodule changed: yes; `modules/ModSecurity-test-Framework` has a modified
  framework commit relative to the earlier baseline. Current parent HEAD points
  at framework commit `4bec4d960fea89525db9e439ea567df15943a2e7`.

## CRS Expectation Result

The former With-CRS 401/403 mismatch for
`action_status_401_phase1_block` is resolved in the current `/src` runs.

| Variant | Connector | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | Apache | 401 | 401 | PASS |
| No-CRS | NGINX | 401 | 401 | PASS |
| With-CRS | Apache | 403 | 403 | PASS |
| With-CRS | NGINX | 403 | 403 | PASS |

The expectation change is scoped to With-CRS through
`expect.variants.with-crs.status: 403`; the base No-CRS expectation remains
401.

CRS effectiveness is evidenced by `crs_sqli_anomaly_block` PASS for Apache
and NGINX, expected 403 and actual 403.

Detailed analysis:
`reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`.

## Decisions

| Target | Decision | Reason |
| --- | --- | --- |
| `connectors/_template` | suitable scaffold, not runtime-verified | The template documents a repeatable connector flow, external tests, and promotion gates. It is intentionally not a productive implementation; origin, metadata, build, No-CRS, With-CRS, coverage matrix, and runtime evidence are required per connector. |
| `connectors/nginx` | aligned with current Template gates for executed scope; runtime status partial | Current No-CRS, With-CRS, and common smokes pass for executed scope; RESPONSE_BODY blocking and full minimum matrix remain unverified. See `nginx-template-alignment.md`. |
| `connectors/apache` | aligned with current Template gates for executed scope; runtime status partial | Current No-CRS, With-CRS, and common smokes pass for executed scope; Apache-specific YAML cases are still not found; RESPONSE_BODY blocking and full minimum matrix remain unverified. See `apache-template-alignment.md`. |
| RESPONSE_BODY | not verified | Current evidence includes pass-through/log-only response-body rows, not a blocking response-body HTTP result. |
| `connectors/envoy` | bridge-starter; runtime status not-verified | Envoy has repository-local metadata and sidecar/HTTP bridge starter code, no local tests, no Envoy runtime harness evidence, and no runtime claims. See `envoy-template-alignment.md`. |

## Current Runtime Evidence

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json` |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json` |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | `/src/ModSecurity-conector-build/results/connector-summary.json` |

Evidence files:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx.rc`
- `/src/ModSecurity-conector-build/results/with-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/with-crs/nginx.rc`

## lighttpd Bridge-Starter Alignment

- `connectors/lighttpd` is bridge-starter only.
- Build status: bridge-starter.
- Runtime status: not-verified.
- No local `connectors/lighttpd/tests` folder is used.
- No lighttpd runtime, adapter, RESPONSE_BODY, audit/log, or No-CRS/With-CRS
  PASS claim is made.
- Bridge-starter code uses shared `common/` origin/status/intervention/capability helpers only.
- `connectors/lighttpd/build/build_starter.sh` and bridge-starter Make targets
  passed for local compile/self-test only; the bridge probe reports its local
  decision as blocked/not-verified.
- Missing dependencies: selected production integration path, lighttpd
  headers/SDK/source or FastCGI/SCGI/bridge dependencies, ModSecurity
  integration code, and a framework-owned lighttpd runtime harness.
- Shared gates are referenced from
  `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
  and `connectors/_template/docs/coverage-decision-matrix.md`.

## Template Improvements

The template now documents:

- required files for a new connector
- required metadata
- required origin/license evidence
- required build evidence
- required No-CRS and With-CRS runtime evidence
- external framework test ownership
- coverage decision matrix columns
- RESPONSE_BODY minimum evidence
- promotion gates: `scaffolded`, `adapter-owned`,
  `runtime-smoke-verified`, `crs-verified`, and `more-than-partial`

## Removed Local Test Folders

- `connectors/_template/tests/`
- `connectors/nginx/tests/`
- `connectors/apache/tests/`

Executable connector tests are framework-owned and are not maintained in local
`connectors/*/tests` directories.

## Checks

| Check | Result | Note |
| --- | --- | --- |
| `test ! -d connectors/_template/tests` | PASS | Local Template test folder is absent. |
| `test ! -d connectors/apache/tests` | PASS | Local Apache test folder is absent. |
| `test ! -d connectors/nginx/tests` | PASS | Local NGINX test folder is absent. |
| `make generate-test-matrix` | PASS | Command exited 0. |
| `make check-test-matrix` | FAIL | Exited 2 because generated reports intentionally differ from HEAD in this uncommitted HAProxy matrix update. |
| `make lint` | PASS | `actionlint unavailable` was informational; command exited 0. |
| `make quick-check` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Command exited 0; it printed a warning that framework-local `config/testing/import-status.json` was not found. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache modules/ModSecurity-test-Framework` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |
| `git status --short` | pending docs/report updates | Parent status shows only report documentation updates from this verification pass. |
| `git submodule status` | PASS | Parent points to `4bec4d960fea89525db9e439ea567df15943a2e7`; submodule working tree is clean. |

## Not Verified

- RESPONSE_BODY blocking for Apache and NGINX.
- Full runtime matrix promotion beyond `partial`.
- Apache-specific connector YAML cases under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there.
- Exact CRS/default-action or ModSecurity action-merging mechanism that made
  With-CRS return 403 before the expectation model was updated.
- Default `make smoke-common` without preparing the default build root.

## Envoy Scaffold Summary

`connectors/envoy` is documented as a sidecar/HTTP bridge starter. It uses the
shared connector gates and coverage matrix rules instead of duplicating the
global contract. ModSecurity bridge, Envoy harness implementation, No-CRS
runtime, With-CRS runtime, RESPONSE_BODY blocking, negative/pass-through,
audit/log, and promotion gates remain open or not verified for Envoy.

## Envoy Build-Starter Summary

Envoy build status is `bridge-starter`: `make -C connectors/envoy build-starter`
compiles repository-local bridge code with connector-neutral `common/` code, and
`make -C connectors/envoy self-test` runs a local allow/block decision self-test.
Envoy runtime status remains `not-verified`. Missing production dependencies are
libmodsecurity headers/libs, Envoy SDK/API headers, ext_proc protobuf/gRPC
bindings, proxy-wasm SDK/toolchain, or a documented Envoy bridge config plus
runtime harness.

## Envoy Build-Starter Evidence

`make -C connectors/envoy build-starter` passed for bridge-starter compilation,
and `make -C connectors/envoy self-test` passed for local allow/block decision
logic. This does not verify Envoy runtime compatibility.

## Envoy Bridge-Starter Evidence

`make -C connectors/envoy self-test` passed for the local bridge decision model.
The result is not a No-CRS run, not a With-CRS run, and not RESPONSE_BODY
evidence.
## HAProxy Current Summary

- HAProxy now has repo-authored ORIGIN/SOURCE_MAP metadata, metadata source, and
  a local SPOA agent starter with a local self-test.
- Build status: `spoa-agent-starter` for
  `make -C connectors/haproxy build-spoa-starter`; productive HAProxy adapter
  build remains BLOCKED.
- Self-test status: PASS for `make -C connectors/haproxy self-test-spoa`.
- Local HAProxy binary prepare: PASS for the framework helper; HAProxy `3.2.19`
  source URL/checksum are pinned only in `common.sh`, verified against the
  official checksum file, and built with verified `TARGET=linux-glibc` support.
- Diagnostic SPOP subset: PASS for diagnostic scope only; this is a minimal
  diagnostic SPOP handshake subset, not a full SPOA agent implementation.
- SPOE config syntax: `syntax-valid` by `haproxy -c`.
- Diagnostic HAProxy-to-agent runtime: `diagnostic-enforcement-verified` from
  fresh run-specific NOTIFY, argument extraction, ModSecurity 403, set-var ACK,
  block-probe 403, and pass-probe 200 evidence.
- Runtime status: `runtime-smoke-verified` for
  `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`.
- HAProxy matrix status: `make runtime-matrix-haproxy` records 141 existing
  framework YAML rows with 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, and
  10 MAPPED_ONLY entries. The PASS is `crs_sqli_anomaly_block`; the No-CRS
  header smoke is preserved as a diagnostic alias, not promoted to the
  framework `phase1_header_block` YAML row.
- HAProxy split matrix status: `make test-haproxy-no-crs` records 0 YAML PASS,
  0 FAIL, 59 BLOCKED, 82 NOT_EXECUTABLE, 10 MAPPED_ONLY; `make
  test-haproxy-with-crs` records 1 YAML PASS, 0 FAIL, 59 BLOCKED, 81
  NOT_EXECUTABLE, 10 MAPPED_ONLY.
- CRS status: verified only for the minimal
  `haproxy_crs_sqli_anomaly_block` runtime smoke; broader CRS coverage remains
  not verified.
- No complete SPOE/SPOA implementation or RESPONSE_BODY runtime evidence is
  present.
- Current runtime blockers: live PASS/FAIL execution for currently BLOCKED YAML
  rows, broader CRS, RESPONSE_BODY, negative/pass-through, audit/log, and
  full-matrix evidence.
- No local `connectors/haproxy/tests` folder is used.
- RESPONSE_BODY blocking remains not verified.
- HAProxy-specific alignment is documented in
  `reports/template-verification-nginx-apache/haproxy-template-alignment.md`.
## Traefik Decision-Service Starter Summary

- `connectors/traefik` exists as scaffold-aligned with a repo-owned local
  decision-service starter.
- Traefik uses global/shared scaffold gates instead of duplicating them in
  connector-local documentation.
- Traefik build status: decision-service-starter; metadata and local decision
  service starters compile, and the local decision self-test passes.
- Traefik runtime status: not-verified.
- No local `connectors/traefik/tests` folder exists.
- No No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through, or audit/log
  runtime result is claimed for Traefik.

## Connector-Starter Framework Summary

`make connector-starter-checks` executed successfully through the parent
Makefile and wrote framework-owned evidence under
`/src/ModSecurity-conector-build/results/connector-starters/`.

- Overall starter-check status: PASS.
- Results file: `/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.
- Summary file: `/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
- Runtime status for connector-starter evidence: `not-verified`.
- RESPONSE_BODY status: not verified.
- Scope: connector starter build/self-test evidence only; no runtime smoke
  validation is claimed.

## New Connector Runtime-Smoke Summary

Framework runtime-smoke entrypoints exist for Envoy, HAProxy, lighttpd, and
Traefik. Connector-side `run_<name>_smoke.sh` entrypoints now also exist for all
four connectors. Current runtime-smoke status is PASS for HAProxy's
`haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block` cases and
BLOCKED for Envoy, lighttpd, and Traefik.

- Runtime-smoke targets: `make smoke-envoy`, `make smoke-haproxy`,
  `make smoke-lighttpd`, `make smoke-traefik`.
- Aggregate target: `make smoke-new-connectors`.
- Connector-side entrypoints:
  `connectors/envoy/harness/run_envoy_smoke.sh`,
  `connectors/haproxy/harness/run_haproxy_smoke.sh`,
  `connectors/lighttpd/harness/run_lighttpd_smoke.sh`,
  `connectors/traefik/harness/run_traefik_smoke.sh`.
- Evidence path: `/src/ModSecurity-conector-build/results/<connector>-summary.json`
  and `/src/ModSecurity-conector-build/results/<connector>-results.jsonl`.
- Runtime verification: true only for HAProxy `haproxy_phase1_header_block`
  and `haproxy_crs_sqli_anomaly_block`; false for Envoy, lighttpd, and
  Traefik.
- CRS verification: true only for HAProxy `haproxy_crs_sqli_anomaly_block`;
  broader CRS and the other new connectors remain not verified.
- RESPONSE_BODY: not verified for all four.
- Starter evidence remains available through `make connector-starter-checks`,
  but starter PASS does not count as runtime smoke.
