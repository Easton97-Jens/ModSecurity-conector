# ModSecurity Connector Monorepo

This repository contains connector-focused code and integration scaffolding for
libmodsecurity v3 based server connectors. The reusable test framework lives in
the `modules/ModSecurity-test-Framework` module; this repository keeps the
connector source trees, connector metadata, harness integration, and generated
connector evidence.

## Connector Architecture

The repository is split into a connector-neutral C layer and adapter-owned
connector trees:

- `common/include/msconnector/` defines shared directive, option/default,
  rule-load-stat, request, response, transaction, intervention, capability,
  origin, logging, and status data shapes.
- `common/src/` contains small connector-neutral helper implementations.
- `connectors/apache/` contains the Apache connector adapter, Autotools/APXS
  build inputs, harness files, metadata, and productive source under
  `connectors/apache/src/`.
- `connectors/nginx/` contains the NGINX connector adapter, module `config`,
  harness files, metadata, and productive source under `connectors/nginx/src/`.
- `connectors/haproxy/` contains a production SPOA/SPOP runtime path,
  examples, harness files, metadata, and productive source under
  `connectors/haproxy/src/`.
- `connectors/{envoy,lighttpd}/` are scaffolded future connector areas with
  documentation and TODOs; `connectors/traefik/` adds a local decision-service
  starter without runtime verification.

Connector source is repo-local. Apache and NGINX connector repositories are not
fetched as runtime defaults.

## Supported Connectors

| Connector | Status | Primary path |
| --- | --- | --- |
| Apache | adapter-owned source tree with real-world smoke harness; evidence-scoped, not blanket stable | `connectors/apache/` |
| NGINX | adapter-owned source tree with real-world smoke harness; evidence-scoped, not blanket stable | `connectors/nginx/` |
| HAProxy | production SPOA/SPOP runtime with live HAProxy smoke evidence; evidence-scoped and partial | `connectors/haproxy/` |
| Envoy | deferred placeholder scaffold | `connectors/envoy/` |
| Lighttpd | deferred placeholder scaffold | `connectors/lighttpd/` |
| Traefik | local decision-service starter; runtime not verified | `connectors/traefik/` |

Apache, NGINX, and HAProxy pass claims must be tied to a specific smoke result.
Current generated default runtime evidence is Apache `54/54 PASS`, NGINX
`60/60 PASS`, and HAProxy `55/55 PASS`. Force-all runtime evidence remains
separate: Apache `133 attempted / 100 PASS / 27 FAIL / 0 BLOCKED /
6 NOT_EXECUTABLE`, NGINX `140 attempted / 95 PASS / 39 FAIL / 0 BLOCKED /
6 NOT_EXECUTABLE`, and HAProxy `133 attempted / 104 PASS / 23 FAIL /
0 BLOCKED / 6 NOT_EXECUTABLE`. API-only smokes are not connector proof.

## Merge Readiness / Current Status

Current merge-readiness evidence for PR #13:

- SonarCloud Quality Gate: `OK`
- SonarCloud ratings: Reliability `A`, Security `A`
- SonarCloud Bugs/Vulnerabilities: `0`
- SonarCloud Security Hotspots: `0 open / 100% reviewed`
- Full-Matrix: `3074 PASS / 782 FAIL / 0 BLOCKED`
- Final consistency audit: `recommended_next_fix_cluster: none`
- Active runtime-fixable clusters: none
- Reports refreshed through the Make/generator targets
- Framework and MRTS submodules: clean

The 782 Full-Matrix failures are not ignored and are not manually flipped. They
remain classified in the generated work queues and analysis reports as semantic
differences, capability gaps, report-only cases, or `not_next` areas that should
not be solved by changing Expected statuses or PASS/FAIL values. The canonical
merge-readiness reports are:

- [Full runtime matrix](./reports/testing/generated/canonical/full-runtime-matrix.generated.md)
- [Final consistency audit](./reports/testing/generated/canonical/final-consistency-audit.generated.md)
- [Next fix plan](./reports/testing/generated/canonical/next-fix-plan.generated.md)
- [Remaining failure analysis](./reports/testing/generated/canonical/remaining-failure-analysis.generated.md)
- [Testing report index](./reports/testing/README.md)

## Connector Feature Status

The Apache and NGINX connectors share connector-neutral metadata in `common/`,
but keep server runtime behavior in their adapter-owned trees. The tables below
describe the current implemented state only.

### Shared Features

| Feature | Apache | NGINX | Notes |
| --- | --- | --- | --- |
| <code>modsecurity on&#124;off</code> | Supported | Supported | Shared directive name from `common/include/msconnector/directives.h`; server-specific directive registration remains adapter-owned. |
| Inline rules | Supported | Supported | `modsecurity_rules`; rules loading and error paths remain connector-specific. |
| Rules file | Supported | Supported | `modsecurity_rules_file`; values count toward rule-load metadata after successful loads. |
| Remote rules | Supported | Supported | `modsecurity_rules_remote`; remote loading remains connector-specific. |
| Transaction ID | Supported | Supported | Apache accepts a static string or a separate Apache expression directive; NGINX accepts an NGINX complex value. |
| Error-log forwarding policy | Supported | Supported | <code>modsecurity_use_error_log on&#124;off</code>; default is on. Audit logs, interventions, and request/response handling are unchanged. |
| Rule-load stats metadata | Supported | Supported | Common data shape in `common/include/msconnector/rule_load_stats.h`; metadata only. |
| Common directive metadata | Used | Used | Shared directive-name constants are used by both connectors. |
| Common option metadata | Partial | Partial | Apache and NGINX use common defaults for enablement, error-log forwarding, and bounded phase-4 options where implemented. |

### Apache

The Apache connector is an adapter-owned Apache module under
`connectors/apache/`. It currently supports:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` keeps the existing static-string semantics.
`modsecurity_transaction_id_expr` is an opt-in Apache string expression, for
example `%{REQUEST_URI}`, evaluated per request. Static and expression
transaction IDs are mutually exclusive in the same Apache context; normal
child-context overrides apply during config merge. If neither directive is set,
or if the expression evaluates to an empty value or fails, Apache keeps the
existing `UNIQUE_ID` fallback and then creates a transaction without an
explicit ID if no usable `UNIQUE_ID` value is available.

`modsecurity_use_error_log off` suppresses Apache error-log forwarding from the
libmodsecurity log callback only. It does not change audit logging,
interventions, hooks, filters, buckets, transaction ownership, or request and
response handling.

Apache tracks rule-load stats internally in `msc_conf_t`. It does not currently
report those stats in the post-config log. Apache bounded Phase 4 support is
evidence-scoped and does not promote full RESPONSE_BODY behavior.

### NGINX

The NGINX connector is an adapter-owned dynamic NGINX module under
`connectors/nginx/`. It currently supports:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

`modsecurity_transaction_id` uses an NGINX complex value and may evaluate
per-request NGINX variables. NGINX exposes rule-load stats in its existing
startup log through the common rule-load-stats helper without changing the log
text, format, level, or order.

The phase-4 directives are bounded runtime controls. They are not a common
promotion contract and do not promote full RESPONSE_BODY behavior.

### HAProxy

The HAProxy connector uses a production SPOA/SPOP path under
`connectors/haproxy/`. It currently supports:

- `haproxy-modsecurity-spoa`
- HAProxy SPOE/SPOP integration
- libmodsecurity rule loading and decision processing
- `decision.jsonl` runtime decision evidence
- audit-log plumbing
- request phases 1/2
- implemented phase 3 response-header evidence
- bounded Phase 4 strict-abort evidence

HAProxy is configured through HAProxy, SPOE, and SPOA-agent configuration files,
not Apache/NGINX-style `modsecurity_*` directives. There is no synthetic matrix
writer; generated HAProxy reports consume live runtime summaries and the runtime
validation snapshot.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.

### Known Differences And Deferred Areas

| Area | Current state |
| --- | --- |
| Transaction ID mapping | Apache supports static strings plus opt-in Apache string expressions through `modsecurity_transaction_id_expr`; NGINX supports complex values through `modsecurity_transaction_id`. |
| Phase-4 directives | Apache and NGINX implement bounded phase-4 controls; full RESPONSE_BODY behavior remains non-promoted. |
| HAProxy directive model | HAProxy uses HAProxy config, SPOE config, and `haproxy-modsecurity-spoa` agent config rather than `modsecurity_*` server directives. |
| RESPONSE_BODY behavior | Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is documented/reported as runtime evidence only. |
| Apache bucket/filter/intervention paths | Intentionally not refactored in this common-metadata work. |
| Common layer | Contains connector-neutral metadata and data shapes only; it does not own Apache or NGINX runtime APIs. |
| Rule-load stats reporting | NGINX reports via its existing startup log; Apache keeps stats as internal metadata until display aggregation and merge semantics are explicitly designed. |

## Connector Metadata

Adapter metadata is owned by each connector:

- `connectors/apache/metadata.c`
- `connectors/nginx/metadata.c`
- `connectors/*/ORIGIN.md`
- `licenses/*/ORIGIN.md`
- `config/testing/import-status.json`

The metadata drift checks compare connector source attribution with the
connector and framework documentation without linking connector runtime code.

## Build And Runtime Integration

The public connector target names remain unchanged and delegate to the
framework module where appropriate:

```sh
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
make summary
make case-matrix
make runtime-matrix-all
make smoke-common
make smoke-apache
make smoke-nginx
make smoke-haproxy
make smoke-all
make runtime-matrix-haproxy
```

CRS variants are available through the framework module:

```sh
make test-no-crs
make test-with-crs
make test
```

`test-no-crs` loads only the generated local YAML-case rules. `test-with-crs`
fetches/prepares OWASP CRS using the central pin in
`modules/ModSecurity-test-Framework/ci/common.sh` and loads CRS before the
local case rules. `test` runs both variants.

## MRTS Tests

MRTS is integrated in the framework as a required framework submodule. The
connector repository does not copy MRTS generator logic; these targets delegate
to `FRAMEWORK_ROOT`.

Initialize connector submodules recursively so the nested framework MRTS
submodule is available:

```sh
git submodule update --init --recursive
```

The delegated targets use `modules/ModSecurity-test-Framework/tools/MRTS` by
default. You can still point at a separate checkout:

```sh
MRTS_ROOT=/path/to/MRTS make mrts-generate
```

Delegated targets:

```sh
make mrts-generate
make test-no-mrts
make test-with-mrts
make test-with-mrts-feature-demo
make test-mrts-matrix
make mrts-ftw
```

The framework reads upstream MRTS inputs directly from `$MRTS_ROOT`, writes
generated rules, go-ftw YAML, framework cases, and `mrts.load` under
`$MRTS_BUILD_ROOT`, and uses `upstream-config-tests` as the default runnable
MRTS corpus. Feature-demo tests are reported as optional/demo coverage and can
be attempted only through the explicit opt-in target or
`MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1`. Golden references under the MRTS
submodule are drift/report inputs only and are never runtime inputs.

Native MRTS infrastructure evidence is separate from connector smoke evidence:

```sh
make mrts-upstream-infra-check
make mrts-native-apache-full
make mrts-native-nginx-pr24-full
make mrts-native-full-run
```

Native outputs are staged under `$MRTS_NATIVE_ROOT` and reported as separate
native infrastructure evidence:

- Apache native: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

These native MRTS reports are separate from connector full-matrix evidence.
Missing local dependencies such as `go-ftw`, `albedo`, `apachectl`, `nginx`, or
the NGINX ModSecurity module are reported as `BLOCKED`; nothing is installed
globally.

Runtime tool source URLs, expected release refs, binary defaults, and candidate
lists are centralized in `modules/ModSecurity-test-Framework/ci/common.sh`.
Runtime preparation and proof scripts load that framework environment and read
values such as `GO_FTW_SOURCE_URL`, `ALBEDO_SOURCE_URL`, and
`EXPAT_SOURCE_URL` from it. Local overrides can be supplied through environment
variables before invoking the Make targets.

MRTS/CRS result paths are separated by variant:

```text
$BUILD_ROOT/results/no-crs/no-mrts
$BUILD_ROOT/results/no-crs/with-mrts
$BUILD_ROOT/results/with-crs/no-mrts
$BUILD_ROOT/results/with-crs/with-mrts
```

Source-build variables remain configurable:

```sh
VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified
BUILD_ROOT=$VERIFIED_RUN_ROOT/build
SOURCE_ROOT=$VERIFIED_RUN_ROOT/src
MODSECURITY_GIT_REF=v3/master
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3
```

`BUILD_ROOT` is a local build/output location, not a cache contract. Full
runtime validation is local and evidence-based; `make smoke-all` is
authoritative only when it is actually executed successfully.

Verified-run and report-refresh workflows default to
`${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified`, with
`NGINX_HARNESS_PARENT` below that root so worker processes can traverse the
generated docroot. See
[Verified Run Environment](./docs/testing/verified-run-environment.md) for the
runtime path contract, NGINX docroot preflight, and generated artifact rules.

GitHub Actions artifacts are pruned by the root
[cleanup-artifacts](./.github/workflows/cleanup-artifacts.yml) workflow on
manual dispatch and nightly schedule. The vendored framework module has the
same cleanup workflow when it runs as its own GitHub repository. In both
repositories, cleanup keeps only the newest artifact per logical artifact group
and at most the newest 20 artifacts overall. Uploading workflows clean their
matching logical group before upload. Report and log artifacts are best-effort
diagnostics with one-day retention.

GitHub Actions workflow versions are maintained separately from build and test
logic. Dependabot checks root GitHub Actions weekly. The
[check-actions-versions](./.github/workflows/check-actions-versions.yml)
workflow reports outdated `uses:` entries, while
[update-actions-versions](./.github/workflows/update-actions-versions.yml)
updates workflow action refs on `automation/update-github-actions-versions` and
opens a pull request instead of pushing to the default branch. The updater scans
both the root workflows and `modules/ModSecurity-test-Framework`; because the
framework is a submodule, module workflow changes are reported unless
`SUBMODULE_UPDATE_TOKEN` is available to create the separate module branch/PR
and update the submodule pointer. SHA-pinned, local, Docker, and dynamic
`uses:` entries are not changed automatically. Reports are written to the step
summary and uploaded as a best-effort one-day artifact.

## Framework Module Integration

Initialize the framework module before running framework-backed targets:

```sh
git submodule update --init --recursive
```

The default module path is:

```sh
modules/ModSecurity-test-Framework
```

Override it when using a separate checkout:

```sh
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make runtime-matrix-all
```

The framework owns YAML cases, runners, normalizers, runtime-matrix logic,
coverage generation, v3 API smoke helpers, and reusable testing documentation.
Connector-specific generated evidence is written in this repository under
`reports/testing/`. The root coverage summary is framework-owned at
`modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`; the parent
repository does not maintain a separate coverage-summary source of truth.

## Report Refresh

Generated reports must be updated through their generators, not patched by hand.
The connector refresh target updates the connector-owned report catalog,
including the full runtime matrix, work queues, remaining-failure analysis,
capability/gap reports, and the final consistency audit:

```sh
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make refresh-all-reports
```

The framework refresh target updates framework-owned generated documentation:

```sh
make -C modules/ModSecurity-test-Framework refresh-framework-reports
```

Before merge, rerun the lint and quick checks in both repositories, then verify
that the generated report manifest and final consistency audit agree with the
current branch state. Runtime caches, generated MRTS rules, FTW YAML, load
files, and temporary job output are local artifacts and must not be committed.

## Documentation Links

- Build / prepare docs: [Compile Apache](./COMPILE_APACHE.md),
  [Compile HAProxy](./COMPILE_HAPROXY.md),
  [Compile NGINX](./COMPILE_NGINX.md),
  [Prepare Envoy](./COMPILE_ENVOY.md),
  [Prepare Traefik](./COMPILE_TRAEFIK.md),
  [Compile Lighttpd](./COMPILE_LIGHTTPD.md),
  [Open connectors](./COMPILE_OPEN_CONNECTORS.md)
- Example configs: [Apache examples](./examples/apache/README.md), [NGINX examples](./examples/nginx/README.md), [HAProxy examples](./examples/haproxy/README.md)
- Shared connector feature docs: [Shared Features](./SHARED_FEATURES.md)
- Roadmap: [docs/roadmap/roadmap.md](./docs/roadmap/roadmap.md)
- Architecture docs: [docs/architecture/](./docs/architecture/)
- Capability model: [docs/architecture/capability-model.md](./docs/architecture/capability-model.md)
- Status model: [docs/architecture/status-model.md](./docs/architecture/status-model.md)
- Connector adapter interface: [docs/architecture/connector-adapter-interface.md](./docs/architecture/connector-adapter-interface.md)
- Connector docs: [docs/connectors/](./docs/connectors/)
- Rule-load stats: [docs/connectors/rule-load-stats.md](./docs/connectors/rule-load-stats.md)
- YAML schema notes: [modules/ModSecurity-test-Framework/docs/imports/common/schema.md](./modules/ModSecurity-test-Framework/docs/imports/common/schema.md)
- Shared fixtures: [modules/ModSecurity-test-Framework/docs/imports/common/fixtures.md](./modules/ModSecurity-test-Framework/docs/imports/common/fixtures.md)
- Smoke target semantics: [modules/ModSecurity-test-Framework/docs/testing/fast-checks.md](./modules/ModSecurity-test-Framework/docs/testing/fast-checks.md)
- Testing report index: [reports/testing/README.md](./reports/testing/README.md)
- Real-world connector validation: [reports/testing/real-world-connector-validation.md](./reports/testing/real-world-connector-validation.md)
- HAProxy PoC evidence: [reports/testing/haproxy-poc.md](./reports/testing/haproxy-poc.md)
- Full runtime matrix: [reports/testing/generated/canonical/full-runtime-matrix.generated.md](./reports/testing/generated/canonical/full-runtime-matrix.generated.md)
- Final consistency audit: [reports/testing/generated/canonical/final-consistency-audit.generated.md](./reports/testing/generated/canonical/final-consistency-audit.generated.md)
- Next fix plan: [reports/testing/generated/canonical/next-fix-plan.generated.md](./reports/testing/generated/canonical/next-fix-plan.generated.md)
- Remaining failure analysis: [reports/testing/generated/canonical/remaining-failure-analysis.generated.md](./reports/testing/generated/canonical/remaining-failure-analysis.generated.md)
- Case matrix reports: [reports/testing/case-matrix.md](./reports/testing/case-matrix.md), [reports/testing/generated/coverage/case-matrix.generated.md](./reports/testing/generated/coverage/case-matrix.generated.md)
- PR/source evidence: [reports/testing/evidence/pr-evidence-summary.md](./reports/testing/evidence/pr-evidence-summary.md), [reports/testing/evidence/raw-args-pr3564.md](./reports/testing/evidence/raw-args-pr3564.md)
- Licensing and origin index: [docs/licensing/license-and-origin.md](./docs/licensing/license-and-origin.md)
- Framework docs: `modules/ModSecurity-test-Framework/README.md`
- Connector test evidence: `reports/testing/`
- Framework-owned coverage summary: `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

## Local Development

Typical local setup:

```sh
git submodule update --init --recursive
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
```

Runtime and coverage evidence must not be inferred from generated metadata
alone. XFAIL, pending, future, connector-gap, and runtime-difference cases stay
evidence classes until explicitly promoted by documented runtime proof.
Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
