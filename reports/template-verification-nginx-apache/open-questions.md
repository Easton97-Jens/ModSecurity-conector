# Open Questions

This file separates resolved scaffold/runtime decisions from questions that
still need evidence. Full decision details are in
`connector-scaffold-decisions.md`.

## Current Readiness

- Documentation/decision commit readiness: yes.
- Commit-fertig fuer Dokumentations-/Entscheidungsstand: ja.
- Default runtime smoke readiness: blocked until the default build root has
  ModSecurity V3 sources.
- Last documented default blocker:
  `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  missing.
- Current `/src` runtime evidence: Apache 54 PASS and NGINX 54 PASS in
  `make smoke-common`.
- Current `/src` NGINX all-scope evidence: 60 PASS, 0 FAIL, 0 BLOCKED.
- RESPONSE_BODY blocking: not verified.
- Vollstaendige Runtime-Verifikation: nein.

## Resolved Decisions

- Parent connector documentation must reference
  `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md` when it
  points to the shared roadmap inventory. Framework-internal relative roadmap
  references are not changed.
- New connectors must not add a local `connectors/<name>/tests` folder.
  Executable tests are framework-owned and referenced through
  `modules/ModSecurity-test-Framework/tests/cases/`,
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`,
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`, and the
  repository `smoke-*` Make targets.
- NGINX-specific framework YAML cases are available under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- The current NGINX build contract is
  `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`.
- The current NGINX docroot work-parent contract is
  `NGINX_HARNESS_PARENT=$(BUILD_ROOT)`.
- The historical NGINX 11 BLOCKED rows are classified as an environment/docroot
  permission blocker and are resolved in the current `/src` reruns.
- The shared scaffold status vocabulary is: `template`, `scaffolded`,
  `adapter-owned`, `runtime-smoke-verified`, `partial`, and `not-verified`.

## Still Open / Deferred

- Apache-specific YAML cases remain deferred. Needed evidence: YAML files under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`
  plus runtime command output showing expected results. Currently only
  `README.md` was found there.
- RESPONSE_BODY blocking remains deferred. Needed evidence: a repository-backed
  runtime testcase, expected blocking response-body trigger, actual blocking
  result such as HTTP 403, log/report evidence, executed command, affected
  connector, and separate Apache/NGINX documentation for any shared claim.
- The alternative of generating a materialized `common/include` layout remains
  deferred. Needed evidence: implemented materialization behavior, generated
  path evidence, compiler lines using that path, and runtime smoke results.
- More-than-`partial` Apache/NGINX completeness remains deferred. Needed
  evidence: documented runtime results for `phase1_header_block`,
  request-body blocking, response-header blocking when framework-supported,
  response-body blocking, audit/log evidence, connector startup/reload
  validation, and a negative/pass-through case.
- Default `make smoke-common` without explicit `/src` environment remains
  deferred for this workspace. Needed evidence: run `make fetch-deps` for the
  default `BUILD_ROOT`/`SOURCE_ROOT`, or provide a valid
  `MODSECURITY_SOURCE_DIR`/`MODSECURITY_V3_SOURCE_DIR`, then rerun
  `make smoke-common` and record the result.
