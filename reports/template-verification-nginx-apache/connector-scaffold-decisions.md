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
- `runtime-smoke-verified`: only specific smoke cases with recorded command and
  result are verified.
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
Apache has 54 PASS and 0 BLOCKED in the final common summary, and NGINX now
has 54 PASS and 0 BLOCKED in the final common summary. The current NGINX
all-scope smoke also has 60 PASS and 0 BLOCKED. These runs improve the NGINX
runtime status, but RESPONSE_BODY blocking is not verified and generated
reports are not runtime PASS proof.

Evidence/paths:

- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/nginx-docroot-permission-analysis.md`
- `reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`
- `reports/template-verification-nginx-apache/summary.md`
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
