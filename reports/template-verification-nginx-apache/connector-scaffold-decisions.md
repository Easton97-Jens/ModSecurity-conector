# Connector Scaffold Decisions

Status: reviewed

This file turns the open questions from `open-questions.md` into repository-
backed scaffold rules for future connectors. Decisions are limited to evidence
found in this repository, the framework module, or actually executed checks.

## Commit Readiness Decision

Question: Does the blocked default `make smoke-common` prevent committing the
documentation and scaffold decisions?

Decision: accepted.

Reason: The requested final static checks passed, local connector test folders
remain absent, and the default runtime-smoke blocker is documented as an
environment prerequisite rather than a documentation failure. This does not
claim a default runtime PASS or full runtime verification.

Evidence/paths:

- `reports/template-verification-nginx-apache/summary.md`
- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/findings.md`
- Actual framework path: `modules/ModSecurity-test-Framework`.
- Current framework commit referenced by the parent:
  `4bec4d960fea89525db9e439ea567df15943a2e7`.
- Default runtime smoke readiness: blocked.
- Reason: `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  missing.
- `/src` runtime evidence: Apache and NGINX `phase1_header_block` PASS.
- Current `/src` common runtime evidence:
  `reports/template-verification-nginx-apache/verified-runtime-run.md`
  records Apache 54 PASS and NGINX 54 PASS, both with 0 FAIL and 0 BLOCKED.
- Current `/src` NGINX all-scope evidence:
  `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx`
  records NGINX 60 PASS, 0 FAIL, and 0 BLOCKED.
- Current `/src` No-CRS evidence:
  `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs`
  records Apache 54 PASS and NGINX 60 PASS, both with 0 FAIL and 0 BLOCKED.
- Current `/src` With-CRS evidence:
  `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs`
  records Apache 55 PASS and NGINX 61 PASS, both with 0 FAIL and 0 BLOCKED.
- Current With-CRS CRS case evidence: `crs_sqli_anomaly_block` PASS for
  Apache and NGINX, expected 403 and actual 403.
- Framework-local `make lint`: PASS.
- Framework-local `make quick-check`: target not found in the framework
  Makefile.
- Framework-local `make check-test-matrix`: PASS, with a warning that
  framework-local `config/testing/import-status.json` was not found.
- Historical NGINX 11 BLOCKED rows are resolved in the current `/src` reruns
  and classified as an environment/docroot permission blocker.
- RESPONSE_BODY: not verified.

Impact on new connectors: documentation and decision updates may be committed
when runtime limitations are explicitly documented. Runtime completion still
requires separately recorded runtime evidence.

Follow-up change: keep the default `make smoke-common` item open/deferred until
the default build root has a valid ModSecurity v3 source tree or the command is
run with explicit valid runtime source paths.

Commit-fertig für Dokumentations-/Entscheidungsstand: ja.

Vollständige Runtime-Verifikation: nein.

## Coverage Matrix Decision

Question: How should generated coverage reporting be used for Template,
Apache, and NGINX scaffold decisions?

Decision: accepted.

Reason: `TEST-COVERAGE-SUMMARY.md` is generated reporting and explicitly says
it is not runtime proof. It records framework coverage, runtime snapshot
PASS/FAIL counts, and that `runtime_verified=true` remains 0. Separate
coverage decision matrices make that distinction visible for Template, Apache,
and NGINX.

Evidence/paths:

- `TEST-COVERAGE-SUMMARY.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `connectors/apache/docs/coverage-decision-matrix.md`
- `connectors/nginx/docs/coverage-decision-matrix.md`

Impact on new connectors: new connector docs must distinguish
`framework-covered` cases from `runtime-smoke-verified` connector behavior.
Generated PASS/FAIL snapshot counts may be cited, but they do not promote a
connector beyond `partial`.

Follow-up change: Template, Apache, and NGINX README/TODO files now link or
refer to coverage-decision matrix requirements. Apache and NGINX remain
`partial`; RESPONSE_BODY remains `not-verified`; more than `partial` requires
complete matrix evidence.

## Template Scaffold Decision

Question: Should `connectors/_template` be evaluated like a completed
connector?

Decision: accepted as scaffold only.

Reason: `connectors/_template` documents the expected connector structure,
external framework test ownership, status vocabulary, and promotion gates. It
intentionally contains no productive connector implementation, no local tests,
and no runtime evidence.

Evidence/paths:

- `connectors/_template/README.md`
- `connectors/_template/TODO.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `reports/template-verification-nginx-apache/template-evaluation.md`

Impact on new connectors: origin/license proof, metadata, build evidence,
No-CRS, With-CRS, coverage matrix, RESPONSE_BODY blocking, and runtime evidence
are required per connector. Missing concrete connector evidence is not a
Template defect.

Follow-up change or needed evidence: concrete connectors must satisfy those
gates before they can be rated beyond `partial`.

## Test Variant Decision

Question: How should the `test-no-crs` and `test-with-crs` targets affect
connector scaffold and coverage decisions?

Decision: accepted for target ownership and separated reporting.

Reason: Both targets are present in the parent `Makefile`. `test-no-crs` and
`test-with-crs` passed in the current `/src` run for Apache and NGINX. The
With-CRS run also verified the CRS SQLi anomaly case for both connectors.

Evidence/paths:

- `Makefile`
- `modules/ModSecurity-test-Framework/README.md`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml`
- `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`

Impact on new connectors: new connector docs must report No-CRS and With-CRS
separately. A CRS-specific PASS may be claimed only for cases that passed under
`test-with-crs`.

Follow-up change or needed evidence: keep full promotion beyond `partial`
deferred until RESPONSE_BODY blocking and the complete minimum matrix are
documented.

## Decision 1: Roadmap References

Question: Several connector files referenced `docs/roadmap/todo-inventory.md`,
but that path was not found in the parent repository.

Decision: accepted.

Reason: The parent path `docs/roadmap/todo-inventory.md` was not found. The
framework path `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
exists. Parent connector documentation should use the repository-valid
framework path. Framework-internal references are not changed when they are
relative to the framework tree.

Evidence/paths:

- `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
- `connectors/apache/TODO.md`
- `connectors/nginx/TODO.md`
- `connectors/*/docs/build.md`
- `connectors/*/docs/architecture.md`
- `connectors/*/docs/public-sources.md`

Impact on new connectors: new connector documentation must point to the
existing framework roadmap path when referring to the shared roadmap inventory.

Follow-up change: parent connector documentation was updated to the framework
path. No new parent roadmap file was created.

## Decision 2: External Test Ownership

Question: How should future connectors reference externally maintained tests
without a local Template or connector `tests` folder?

Decision: accepted.

Reason: The local test folders `connectors/_template/tests`,
`connectors/apache/tests`, and `connectors/nginx/tests` were removed. The
framework owns executable YAML cases and the runner used by Apache and NGINX
harnesses.

Evidence/paths:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `Makefile` targets: `smoke-apache`, `smoke-nginx`, `smoke-common`,
  `smoke-all`, `runtime-matrix-all`

Impact on new connectors: new connectors must not add
`connectors/<name>/tests`. They must document framework-owned tests and the
runtime target that executes them.

Follow-up change: Template, Apache, and NGINX documentation now state that
connector tests are framework-owned and not connector-local.

## Decision 3: Apache-Specific YAML Cases

Question: Are Apache-only YAML cases available under the connector-specific
framework path?

Decision: deferred.

Reason: The path exists, but only `README.md` was found there. No Apache-only
YAML cases were found, and none are invented here.

Evidence/paths:

- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/README.md`
- `modules/ModSecurity-test-Framework/docs/testing/test-import-plan.md`

Impact on new connectors: Apache-specific claims must not rely on nonexistent
Apache-only YAML cases. They may rely only on executed generic cases or future
Apache-specific cases once present and run.

Needed evidence: Apache-specific YAML case files under the framework path plus
runtime command output showing the expected result.

## Decision 4: NGINX-Specific YAML Cases

Question: Are NGINX-specific YAML cases available under the connector-specific
framework path?

Decision: accepted.

Reason: The NGINX connector-specific framework path contains README plus YAML
case files.

Evidence/paths:

- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/*.yaml`

Impact on new connectors: connector-specific YAML cases belong under
`modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
when they exist. NGINX can reference the existing NGINX-specific path.

Follow-up change: Apache/NGINX validation docs distinguish existing NGINX YAML
cases from missing Apache-specific YAML cases.

## Decision 5: Status Vocabulary

Question: README files describe Apache/NGINX as adapter-owned while some docs
still use scaffold-oriented status values.

Decision: accepted.

Reason: The repository uses several status labels. The scaffold decision needs
a shared vocabulary to avoid presenting partial evidence as full validation.

Evidence/paths:

- `connectors/_template/README.md`
- `connectors/apache/README.md`
- `connectors/nginx/README.md`
- `reports/template-verification-nginx-apache/nginx-evaluation.md`
- `reports/template-verification-nginx-apache/apache-evaluation.md`

Status vocabulary:

- `template`: generic starting point, not an implementation.
- `scaffolded`: structure exists, but no repository-backed adapter
  implementation is proven.
- `adapter-owned`: productive connector code lives in the connector tree with
  provenance and metadata.
- `runtime-smoke-verified`: only specific smoke cases with recorded command,
  result, and explicit `verified_case` scope are verified; this does not imply
  CRS, RESPONSE_BODY, or full-matrix verification.
- `crs-verified`: With-CRS target or case claim has recorded command, CRS
  evidence, and result.
- `partial`: structure or partial runtime evidence exists, but full validation
  is not proven.
- `not-verified`: insufficient runtime evidence.

Impact on new connectors: new docs must use this vocabulary and must not mark a
connector complete from structure checks alone.

Follow-up change: Template and validation docs were updated with this
vocabulary.

## Decision 6: RESPONSE_BODY Blocking Evidence

Question: What evidence is required before `RESPONSE_BODY` blocking can be
treated as verified?

Decision: deferred.

Reason: Repository evidence states that response-body pass-through is not
response-body blocking verification, and `RESPONSE_BODY` remains non-promoted.

Evidence/paths:

- `reports/testing/real-world-connector-validation.md`
- `modules/ModSecurity-test-Framework/docs/real-world-connector-validation.md`
- `modules/ModSecurity-test-Framework/docs/roadmap.md`
- `modules/ModSecurity-test-Framework/docs/testing/test-import-plan.md`

Impact on new connectors: no connector may claim `RESPONSE_BODY` blocking
support until the minimum evidence below exists.

Needed evidence:

- a repository-backed runtime testcase in the framework
- expected blocking response-body trigger
- actual blocking result, such as HTTP 403
- log/report evidence
- executed command
- affected connector
- Apache and NGINX separately documented if a shared claim is made

## Decision 7: NGINX Include Build Contract

Question: Should `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` remain
the current NGINX build contract?

Decision: accepted.

Reason: `connectors/nginx/config` consumes `MSCONNECTOR_COMMON_INC`. The
current framework prepare script passes
`MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`, and the post-fix NGINX
smoke passed `phase1_header_block` with HTTP 403.

Evidence/paths:

- `connectors/nginx/config`
- `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh`
- `reports/template-verification-nginx-apache/nginx-build-fail-analysis.md`
- `/src/ModSecurity-conector-build/logs/nginx/commands.txt`
- `/src/ModSecurity-conector-build/logs/nginx/nginx-make.log`

Impact on new connectors: NGINX build documentation may treat this environment
variable as the current supported common-header include contract.

Follow-up change: documentation records this as the current contract.

## Decision 8: Materialized `common/include` Layout

Question: Should materialized build trees carry a generated `common/include`
layout instead of passing `MSCONNECTOR_COMMON_INC`?

Decision: deferred.

Reason: The current accepted build contract passes `MSCONNECTOR_COMMON_INC` and
has passing smoke evidence. No repository file proves a generated common layout
contract for materialized connector trees.

Evidence/paths:

- `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh`
- `reports/template-verification-nginx-apache/nginx-build-fail-analysis.md`

Impact on new connectors: do not invent a materialized common include layout.
Use an explicit, documented include contract until a future implementation is
proven.

Needed evidence: an implemented materialization contract, generated path
evidence, compiler lines using that path, and runtime smoke results.

## Decision 9: Broader Runtime Matrix

Question: Which runtime matrix is required before Apache or NGINX can be
treated as more than partially complete?

Decision: deferred.

Reason: The current `/src` common runtime run provides partial evidence only.
Apache has 54 PASS and 0 BLOCKED in the final common summary, and NGINX has
54 PASS and 0 BLOCKED in the final common summary. The current No-CRS target
passed for Apache and NGINX, and the current With-CRS target also passed for
Apache and NGINX. These runs improve the documented runtime status, but
RESPONSE_BODY blocking is not verified and generated reports are not runtime
PASS proof.

Evidence/paths:

- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/nginx-docroot-permission-analysis.md`
- `reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`
- `reports/template-verification-nginx-apache/summary.md`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `modules/ModSecurity-test-Framework/docs/testing/test-import-plan.md`
- `reports/testing/generated/apache-runtime-results.generated.md`
- `reports/testing/generated/nginx-runtime-results.generated.md`

Impact on new connectors: new connectors remain `partial` until the minimum
matrix below is executed and documented.

Needed evidence:

- `phase1_header_block`
- request-body blocking
- response-header blocking, when framework-supported
- response-body blocking
- audit/log evidence
- connector startup/reload validation
- negative/pass-through case
- Apache and NGINX separately documented with commands and results when those
  connectors are part of the claim

## Envoy Scaffold Decision

Question: How should the existing `connectors/envoy` directory be completed
without duplicating shared connector rules or claiming unverified behavior?

Decision: accepted as initial scaffold baseline; extended by the Envoy Build-Starter Decision below.

Reason: Envoy initially had no repository-backed adapter-owned source, build
evidence, harness implementation, or runtime evidence. Connector-specific Envoy
files document only Envoy status and open gates, while referencing shared rules
in this file and in `connectors/_template/docs/coverage-decision-matrix.md`.

Evidence/paths:

- `connectors/envoy/README.md`
- `connectors/envoy/TODO.md`
- `connectors/envoy/docs/architecture.md`
- `connectors/envoy/docs/build.md`
- `connectors/envoy/docs/validation.md`
- `connectors/envoy/docs/coverage-decision-matrix.md`
- `connectors/envoy/harness/README.md`
- `connectors/envoy/src/README.md`
- `reports/template-verification-nginx-apache/envoy-template-alignment.md`

Impact on new connectors: shared scaffold rules, promotion gates, status
vocabulary, No-CRS/With-CRS separation, coverage matrix semantics, and runtime
evidence requirements stay global/shared. Envoy-specific files must not claim
runtime behavior until an Envoy build/harness and executed Envoy-scoped targets
produce evidence.

Envoy status:

- Scaffold: OK.
- Origin/metadata: build-starter metadata present.
- Build: build-starter only.
- Harness: contract only.
- No-CRS: not-run.
- With-CRS: not-run.
- RESPONSE_BODY: not-verified.
- Local `connectors/envoy/tests`: absent.
- Promotion: not allowed beyond build-starter/partial.

## Envoy Build-Starter Decision

Question: Can `connectors/envoy` move beyond documentation-only scaffold without
inventing Envoy API, ModSecurity API, build logic, or runtime results?

Decision: accepted as metadata-only build starter.

Reason: The repository contains connector-neutral `common/` headers and helper
source plus Apache/NGINX metadata patterns. It does not contain Envoy SDK/API
headers, proxy-wasm SDK, ext_proc protobuf/gRPC bindings, or an Envoy runtime
harness. Therefore the only repository-backed build path is compiling local
Envoy metadata against connector-neutral common code.

Evidence/paths:

- `common/include/msconnector/origin.h`
- `common/include/msconnector/capabilities.h`
- `common/src/origin.c`
- `common/src/capabilities.c`
- `connectors/envoy/ORIGIN.md`
- `connectors/envoy/SOURCE_MAP.json`
- `connectors/envoy/metadata.c`
- `connectors/envoy/metadata.h`
- `connectors/envoy/Makefile`
- `connectors/envoy/build/build_metadata.sh`

Impact: Envoy build status may be reported as `build-starter` only after
`make -C connectors/envoy build-starter` passes. Runtime status remains
`not-verified`. RESPONSE_BODY blocking remains `not-verified`. Envoy is not
`adapter-owned` until real Envoy integration source, dependencies, build logs,
and harness/runtime evidence are added.

## Envoy Bridge-Starter Decision

Question: Can `connectors/envoy` move beyond metadata-only compilation toward a
real connector path without faking Envoy or ModSecurity APIs?

Decision: accepted as sidecar/HTTP bridge starter.

Reason: Native Envoy filter, ext_proc, and proxy-wasm paths still lack required
repository dependencies. A local sidecar/HTTP bridge starter can be built with
repository-owned C code and connector-neutral `common/` request/intervention
shapes. This gives Envoy a concrete request-to-decision integration seam without
claiming Envoy runtime compatibility or ModSecurity rule execution.

Evidence/paths:

- `connectors/envoy/src/envoy_bridge.h`
- `connectors/envoy/src/envoy_bridge.c`
- `connectors/envoy/src/envoy_bridge_main.c`
- `connectors/envoy/Makefile`
- `connectors/envoy/build/build_metadata.sh`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`

Impact: Envoy may be rated `bridge-starter` after `make -C connectors/envoy
build-starter` and `make -C connectors/envoy self-test` pass. It is not
`modsecurity-bridge-starter`, `runtime-smoke-verified`, `crs-verified`, or
`partial` until real libmodsecurity and Envoy runtime harness evidence exists.
## Decision 10: HAProxy Uses Shared Gates With Local SPOA Agent Starter

Question: Should the HAProxy connector duplicate global connector gates while
adding a minimal SPOE/SPOA-oriented next step?

Decision: rejected for duplication; accepted for a local SPOA agent starter.

Reason: The Template coverage matrix and this decision file already define the
shared status vocabulary, scaffold rules, promotion gates, No-CRS/With-CRS
separation, RESPONSE_BODY minimum evidence, external framework ownership, and
runtime-evidence expectations. HAProxy-specific files should reference those
rules and record only HAProxy-specific status. The repository has reusable
common request, intervention, status, and origin shapes, so a local starter can
compile and self-test synthetic request-decision logic without inventing HAProxy
API ownership or full SPOP frame handling. A separate local libmodsecurity
binding verifies the local C API and can be exercised by the diagnostic SPOP
runtime for the scoped `haproxy_phase1_header_block` and
`haproxy_crs_sqli_anomaly_block` smokes.

HAProxy-specific application:

- `connectors/haproxy` is `spoa-agent-starter`.
- Runtime status is `runtime-smoke-verified` for
  `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`.
- Template alignment is `scaffold-aligned plus local SPOA agent starter`.
- No local `connectors/haproxy/tests` folder is used.
- `connectors/haproxy/src/haproxy_spoa_agent_starter.*` and
  `connectors/haproxy/src/haproxy_spoa_main.c` are repo-authored local starter
  files, not productive adapter code.
- `make -C connectors/haproxy build-spoa-starter` may compile the local starter
  binary only; it does not build HAProxy, a HAProxy module, a complete SPOA
  service, HAProxy-enforced libmodsecurity integration, or runtime adapter
  logic.
- `make -C connectors/haproxy self-test-spoa` may verify local synthetic
  request allow/block decisions only; it is not a HAProxy runtime smoke.
- `make -C connectors/haproxy self-test-modsecurity-binding` may verify a
  local libmodsecurity phase-1 header block self-test only; it may not set
  `runtime_verified` to true by itself.
- `make -C connectors/haproxy self-test-modsecurity-binding-crs` may verify a
  local CRS SQLi binding self-test only; it may not set `runtime_verified` to
  true by itself.
- `make smoke-haproxy` may set `runtime_verified: true` only when live HAProxy
  sends NOTIFY to the diagnostic agent, the agent extracts request arguments,
  libmodsecurity produces a disruptive 403, the verified set-var ACK is sent,
  the block probe returns 403, and the clean probe returns 200. CRS may be
  marked verified only for `haproxy_crs_sqli_anomaly_block` when the local CRS
  preamble is loaded and the SQLi probe blocks while the pass probe returns
  200.
- Productive HAProxy adapter build remains BLOCKED until a full SPOP parser or
  SPOE/SPOA protocol library, broader HAProxy runtime harness, broader CRS
  evidence, RESPONSE_BODY evidence, negative/pass-through evidence, audit/log
  evidence, and full-matrix evidence are selected and recorded.
- No broader CRS behavior or RESPONSE_BODY blocking result is claimed.
- Future executable tests remain framework-owned under
  `modules/ModSecurity-test-Framework/tests/cases/` and runner paths such as
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- Broader evidence may reference parent targets `make test-no-crs`,
  `make test-with-crs`, and `make smoke-common` only after an explicit
  HAProxy runtime scope exists and is executed.

Impact: HAProxy may be documented as a local SPOA agent starter without
creating duplicated connector-local gates or YAML test cases. Promotion beyond
partial scoped runtime smoke is not allowed until HAProxy-specific productive
source origin, runtime build, broader harness, No-CRS, With-CRS, RESPONSE_BODY,
negative/pass-through, audit/log, and full-matrix evidence is recorded.
## lighttpd Bridge-Starter Decision

Question: Can `connectors/lighttpd` move beyond metadata/probe build-starter
without inventing a lighttpd API, FastCGI/SCGI protocol compatibility,
ModSecurity API integration, or runtime claim?

Decision: accepted as decision-service bridge-starter only.

Reason: The repository has connector-neutral `common/` origin, status,
intervention, request, and capability helpers and existing Apache/NGINX metadata
patterns. It does not have selected lighttpd headers/SDK/source, a lighttpd
module build configuration, FastCGI/SCGI protocol adapter,
ModSecurity-to-lighttpd integration code, or a lighttpd runtime harness.
Therefore the only safe concrete next step is a repo-owned local decision
service bridge starter that proves local compile/self-test behavior, not adapter
ownership or runtime compatibility.

Evidence/paths:

- `connectors/lighttpd/ORIGIN.md`
- `connectors/lighttpd/SOURCE_MAP.json`
- `connectors/lighttpd/metadata.c`
- `connectors/lighttpd/metadata.h`
- `connectors/lighttpd/Makefile`
- `connectors/lighttpd/build/build_starter.sh`
- `connectors/lighttpd/build/bridge_starter.sh`
- `connectors/lighttpd/src/lighttpd_build_starter.c`
- `connectors/lighttpd/src/lighttpd_bridge.h`
- `connectors/lighttpd/src/lighttpd_bridge.c`
- `connectors/lighttpd/src/lighttpd_bridge_main.c`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/TODO.md`
- `connectors/lighttpd/docs/architecture.md`
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
- `connectors/lighttpd/docs/coverage-decision-matrix.md`
- `connectors/lighttpd/harness/README.md`
- `connectors/lighttpd/src/README.md`
- `reports/template-verification-nginx-apache/lighttpd-template-alignment.md`
- Global matrix: `connectors/_template/docs/coverage-decision-matrix.md`
- Framework tests: `modules/ModSecurity-test-Framework/tests/cases/`
- Framework runner: `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- Public lighttpd references: `modules/ModSecurity-test-Framework/docs/imports/sources.md`
- Future connector contract: `modules/ModSecurity-test-Framework/docs/future-connectors.md`

Impact on lighttpd: Phase 0 scaffold is OK. Origin/metadata for the bridge
starter is present. The metadata/probe and bridge-starter compile/self-test
checks are available. Native lighttpd, FastCGI, and SCGI production integration
remain blocked until a concrete runtime path and its dependencies are selected.
Harness, No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through, audit/log, and
promotion gates remain open/not verified until per-connector runtime evidence
exists. No local `connectors/lighttpd/tests` folder may be used.

Runtime claim: none.
## Decision 10: Traefik Decision-Service Starter

Question: How should `connectors/traefik` advance beyond compile-time metadata
without inventing a Traefik API or claiming runtime verification?

Decision: accepted as a local decision-service starter.

Reason: `connectors/traefik` now contains repo-owned metadata, source-map,
origin, compile-time starter source, and local decision-service starter source
that builds against connector-neutral `common/` helpers. The repository does not
contain a selected Traefik plugin API, middleware API, Go module, Traefik runtime
source, HTTP bridge runtime, or Traefik harness. Therefore the implemented next
step is a local in-memory request-to-decision model with self-test, not a
Traefik runtime adapter or verified `forwardAuth` service.

Evidence/paths:

- `connectors/traefik/README.md`
- `connectors/traefik/TODO.md`
- `connectors/traefik/ORIGIN.md`
- `connectors/traefik/SOURCE_MAP.json`
- `connectors/traefik/metadata.c`
- `connectors/traefik/metadata.h`
- `connectors/traefik/Makefile`
- `connectors/traefik/build/build-starter.sh`
- `connectors/traefik/src/traefik_build_starter.c`
- `connectors/traefik/src/traefik_decision_service.h`
- `connectors/traefik/src/traefik_decision_service.c`
- `connectors/traefik/src/traefik_decision_service_main.c`
- `connectors/traefik/docs/coverage-decision-matrix.md`
- `reports/template-verification-nginx-apache/traefik-template-alignment.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `common/include/msconnector/`
- `common/src/`
- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Impact on new connectors: connector-specific starters may model local decision
logic only when they avoid fake server APIs and make their non-runtime status
explicit. Runtime claims require executed connector-specific runtime commands and
evidence.

Follow-up change or needed evidence: Traefik remains not runtime-verified until
a production integration path, upstream/license evidence, runtime build, harness,
No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through, and audit/log evidence
are produced and documented.
