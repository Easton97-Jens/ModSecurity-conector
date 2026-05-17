# ModSecurity Connector Monorepo

Status: scaffolded

This repository is a monorepo scaffold and evidence workspace for future
libmodsecurity v3 based connectors. It is based on ModSecurity v2/v3 regression
and API evidence plus controlled Apache and NGINX connector imports, and it
validates real connector paths through source-derived YAML smokes.

Implemented now:

- Connector-neutral headers under `common/include/msconnector/`, including
  C-first request, response, transaction, intervention, status, origin, logging,
  and capability data shapes.
- Documentation that separates local v3/libmodsecurity facts from v2 historical
  and regression-test material.
- Connector directories for Apache, NGINX, HAProxy, Envoy, Lighttpd, and
  Traefik.
- Test layout, normalizer skeletons, runner skeletons, and CI structure checks.
- A shared YAML case runner used by Apache and NGINX PoC smokes.
- A connector-free libmodsecurity v3 C API smoke probe build harness under
  `src/v3-api-smoke/`; see `docs/testing/v3-api-smoke-test.md`.
- A local `/src` default v3 smoke run has observed `primary_args_phase2`
  returning intervention status `403`.
- Explicit `real-world-connector-path` validation metadata for Apache and
  NGINX smoke summaries; see `docs/connectors/real-world-connector-validation.md`.
- An Apache PoC build helper that can source-build httpd under `BUILD_ROOT`, plus
  a runtime smoke harness scaffold; see `docs/connectors/apache-poc.md`.
- A local source-built Apache PoC has observed the YAML-expected HTTP behavior
  for all current shared minimal cases.
- A scaffolded NGINX PoC build helper and runtime harness use the same shared
  YAML case and source NGINX from the official `nginx/nginx` GitHub release
  archive flow.
- A local source-built NGINX PoC has observed the YAML-expected HTTP behavior
  for all current shared minimal cases.
- Formal connector smoke targets:
  `make smoke-common`, `make smoke-apache`, `make smoke-nginx`, and
  `make smoke-all`.
- Maintenance targets: `make lint`, `make summary`, and `make case-matrix`.
- Finalized capability/status/result model documentation:
  `docs/architecture/capability-model.md`, `docs/architecture/status-model.md`,
  `docs/architecture/connector-adapter-interface.md`, and `docs/testing/case-matrix.md`.
- Source-derived imported YAML cases from the local Apache and NGINX connector
  test suites, with origin mapping in `docs/testing/test-import-plan.md`.
- Source-derived V2/V3 compatibility cases under
  `tests/common/cases/v2-imported/` and `tests/common/cases/v3-imported/`,
  covering initial operator, transformation, multipart FILES, XML body
  processor, and v3 action/operator behavior.
- Central license and attribution index under `licenses/`, with Apache and
  NGINX connector license mirrors plus ModSecurity V2/V3 read-only reference
  notes.

Not implemented:

- No complete connector runtime.
- No complete connector regression suite.
- No claim that any connector is complete, reload-safe, production-ready, or
  covered beyond the documented local PoC smokes.
- No claim that the v3 API smoke probe passes until `primary_args_phase2`
  observes status `403`.
- No claim that the Apache PoC is complete beyond the documented shared
  minimal HTTP `403` smokes.
- No claim that the NGINX PoC is complete beyond the documented shared minimal
  HTTP `403` smokes.

## Source References

Local paths are examples from the current workspace. The upstream repositories
are the portable references for GitHub, CI, pull requests, and external
maintainers.

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `/root/conecter/ModSecurity_V2` | https://github.com/owasp-modsecurity/ModSecurity | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Apache-2.0 |
| ModSecurity v3 | `/root/conecter/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Apache-2.0 |
| ModSecurity-apache | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |
| ModSecurity-nginx | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

These paths are read-only references, not required build locations. Smoke
builds use `MODSECURITY_V3_SOURCE_DIR`, `MODSECURITY_V3_DIR`, `BUILD_ROOT`, and
`LOG_DIR`; local defaults build under `/src`, while CI can use `$RUNNER_TEMP`.

## Architecture Map

- `connectors/apache/upstream/` and `connectors/nginx/upstream/` are temporary
  reference/import bases. They may shrink only after functionality has moved to
  maintained project code, origin is still documented, and smokes still pass.
- `licenses/` is the durable attribution index for imported connector code and
  read-only ModSecurity engine references.
- `common/` is the future connector-neutral basis. It currently contains
  C-first data shapes only; it does not own Apache or NGINX hook/filter logic.
- `connectors/<name>/` remains server-specific implementation, harness, and
  build documentation.

Apache PoC source-build defaults are also overrideable:

```sh
BUILD_HTTPD_FROM_SOURCE=1
HTTPD_VERSION=2.4.67
APR_VERSION=1.7.6
APR_UTIL_VERSION=1.6.3
BUILD_PCRE2_FROM_SOURCE=1
PCRE2_VERSION=10.47
```

NGINX PoC source-build defaults are overrideable:

```sh
BUILD_NGINX_FROM_SOURCE=1
NGINX_SOURCE_MODE=github-release
NGINX_GITHUB_REPO=https://github.com/nginx/nginx
NGINX_RELEASE_TAG=latest
```

When `NGINX_RELEASE_TAG=latest`, the actual tag is resolved at build time and
recorded under `$BUILD_ROOT/logs/nginx/`.

## Shared Smoke Targets

The connector smoke targets reuse build artifacts under `BUILD_ROOT` unless
`REFRESH=1` is set. They never write generated files into this checkout.

```sh
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-apache
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-nginx
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-common
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
```

`SMOKE_CASES` can restrict the run by case name or file path:

```sh
BUILD_ROOT=/src/ModSecurity-conector-build \
SMOKE_CASES="phase1_header_block phase2_args_block request_body_json_block" \
make smoke-all
```

Current shared minimal cases:

| Case | Source-derived origin | Local Apache | Local NGINX |
| --- | --- | --- | --- |
| `audit_log_phase1_block.yaml` | Apache logging actions and NGINX serial audit-log tests | pass, HTTP 403, audit fields | pass, HTTP 403, audit fields |
| `phase1_header_block.yaml` | Apache request-header/JSON gating and NGINX phase-1 block tests | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_block.yaml` | Apache `00-basics.t` and NGINX `modsecurity.t` ARGS phase-2 tests | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_pass.yaml` | Apache non-matching ARGS rule and NGINX "nothing to detect" tests | pass, HTTP 200, origin body | pass, HTTP 200, origin body |
| `request_body_json_block.yaml` | Apache JSON/body handling and NGINX request-body tests | pass, HTTP 403 | pass, HTTP 403 |
| `request_body_urlencoded_block.yaml` | Apache `ARGS_POST` and NGINX request-body/ARGS_POST tests | pass, HTTP 403 | pass, HTTP 403 |
| `response_header_basic.yaml` | Apache phase tests and NGINX header-filter path | pass, HTTP 403 | pass, HTTP 403 |

These pass observations were made locally on 2026-05-15 with
`BUILD_ROOT=/src/ModSecurity-conector-build`. Other environments must run the
same targets before claiming pass there.

Useful maintenance commands:

```sh
BUILD_ROOT=/src/ModSecurity-conector-build make lint
BUILD_ROOT=/src/ModSecurity-conector-build make summary
BUILD_ROOT=/src/ModSecurity-conector-build make case-matrix
```

Imported source-derived cases are split by scope:

- `tests/common/cases/imported/`: portable cases that Apache and NGINX both
  must run for `smoke-common` and `smoke-all`.
- `tests/apache/cases/imported/`: Apache-specific cases only.
- `tests/nginx/cases/imported/`: NGINX-specific cases only.

Current imported common candidates cover phase actions, query-argument
collections, form-body collection names, raw request-body matching, raw JSON
body matching, simple multipart text fields, and response-body pass-through.
Additional V2/V3-derived common candidates cover v2 operator/transformation
semantics plus v3 multipart FILES variables, XML body processing, `@rx`, trim,
and `SecAction`.
Current imported NGINX-specific cases cover redirect and TX scoring behavior
from the local NGINX suite. Response-body blocking is mapped as xfail rather
than counted as common PASS because the local NGINX source marks that behavior
TODO and local probing did not produce stable HTTP 403. See
`docs/testing/test-import-plan.md` and
`tests/common/shared-case-origin-map.md` before promoting or moving a case.

Observed locally on 2026-05-15 after the stabilization pass, `make smoke-all`
reported 43 Apache passes (7 minimal + 12 Apache/NGINX-derived common + 10
V2-derived common + 14 V3-derived common) and 46 NGINX passes (the same common
cases plus 3 NGINX-specific imported). The body/filter additions from the
previous pass are:

| Case | Source-derived origin | Local Apache | Local NGINX |
| --- | --- | --- | --- |
| `json_request_body_block.yaml` | Apache JSON/body coverage and NGINX request-body tests | pass, HTTP 403 | pass, HTTP 403 |
| `multipart_basic_block.yaml` | Apache multipart parser and NGINX request-body tests | pass, HTTP 403 | pass, HTTP 403 |
| `response_body_pass.yaml` | Apache response directives and NGINX response-body access tests | pass, HTTP 200 | pass, HTTP 200 |

`response_body_basic_block` remains mapped/xfail until both connectors return
stable HTTP 403 for the same YAML case.

Observed locally on 2026-05-15, targeted `make smoke-common` runs also reported
these V2/V3-derived active cases as `PASS` on both Apache and NGINX:

| Case group | Cases | Local Apache | Local NGINX |
| --- | --- | --- | --- |
| V2 operators/transformations | `v2_operator_streq_block`, `v2_operator_contains_block`, `v2_transformation_lowercase_block`, `v2_transformation_trim_block` | pass, HTTP 403 | pass, HTTP 403 |
| V3 multipart FILES | `multipart_files_value_block`, `multipart_files_names_block`, `multipart_files_combined_size`, `multipart_filename_block` | pass, HTTP 403 | pass, HTTP 403 |
| V3 XML/operator/action | `xml_request_body_block`, `v3_operator_rx_block`, `v3_transformation_trim_block`, `v3_secaction_block` | pass, HTTP 403 | pass, HTTP 403 |

`v3_action_nolog_pass_no_audit` remains probeable by explicit `SMOKE_CASES`,
but it is no longer an active Common-PASS case. Local Apache and NGINX probes
observed HTTP 200 and an empty audit log, while GitHub Actions reported a
non-empty audit log for the same semantic expectation. That difference is
classified as `xfail` until local and CI behavior are stable in both
connectors.

V2/V3 import inventory is documented in
`tests/common/v2-regression-map.md`, `tests/common/v3-regression-map.md`, and
`docs/testing/v2-vs-v3-test-compatibility.md`.

Boundary rule:

- `common/` contains connector-neutral code only.
- `connectors/<name>/` contains server/proxy-specific integration only.
- `tests/common/` contains only portable engine/rule/behavior tests.
- `tests/<connector>/` contains connector-specific behavior tests.

## Documentation Entry Points

- `docs/README.md`: documentation index.
- `docs/architecture/`: common model, C-first decision, and adapter boundaries.
- `docs/connectors/`: Apache/NGINX PoCs, real-world validation, and future
  connector planning.
- `docs/testing/`: source-derived YAML cases, compatibility, xfail evidence,
  and v3 API smoke notes.
- `docs/imports/`: source inventories, import analyses, and upstream pruning.
- `docs/roadmap/`: roadmap and TODO inventory.
- `docs/licensing/license-and-origin.md` and `licenses/README.md`: origin and
  license attribution.

## API Smoke vs Connector Smoke

The connector-free API smoke under `src/v3-api-smoke/` proves only the public
libmodsecurity v3 C API path. It is not counted as Apache or NGINX connector
success.

Apache and NGINX `pass` means `real-world-connector-path`: a real HTTP client
talked to a source-built server process, the real connector module loaded, the
YAML rules evaluated in libmodsecurity, and the server returned the
YAML-expected HTTP status. Connector summaries record the server binary, module
path, libmodsecurity path, and verified variable families such as `ARGS`,
`REQUEST_HEADERS`, `REQUEST_BODY`, `FILES`, `XML`, `AUDIT_LOG`, and
`RESPONSE_HEADERS`.
