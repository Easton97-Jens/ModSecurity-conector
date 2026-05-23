# Verification Summary

Status: reviewed

## Readiness

- Documentation/decision commit readiness: yes.
- Commit-fertig fuer Dokumentations-/Entscheidungsstand: ja.
- Default runtime smoke readiness: blocked unless dependencies are prepared in
  the default build root.
- Last documented default blocker:
  `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  missing.
- Current `/src` runtime evidence: Apache and NGINX `phase1_header_block` PASS.
- Current `/src` `make smoke-common` evidence: Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make smoke-nginx` all-scope evidence: NGINX 60 PASS,
  0 FAIL, 0 BLOCKED.
- RESPONSE_BODY blocking: not verified.
- Vollstaendige Runtime-Verifikation: nein.

## Decisions

| Target | Decision | Reason |
| --- | --- | --- |
| Scaffold rules | documented | `connector-scaffold-decisions.md` separates accepted and deferred decisions. |
| `connectors/_template` | partially suitable | Structure and warnings exist; local Template tests were removed; concrete runtime claims remain external evidence only. |
| `connectors/nginx` | partial with current `/src` smoke PASS scope | Adapter-owned structure exists; local tests were removed; include/docroot runtime issues are resolved in the current `/src` run; full matrix and RESPONSE_BODY blocking are not verified. |
| `connectors/apache` | partial with current `/src` smoke PASS scope | Adapter-owned structure exists; local tests were removed; current `/src` common smoke passed; Apache-specific YAML files were not found; RESPONSE_BODY blocking is not verified. |

## Current Runtime Evidence

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED. |

Evidence files:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/nginx.rc`

## NGINX Docroot Blocker

The prior NGINX 11 BLOCKED rows are now classified as an environment/docroot
permission blocker. The current parent contract sets:

```make
NGINX_HARNESS_PARENT ?= $(BUILD_ROOT)
export NGINX_HARNESS_PARENT
```

The current `/src` runs use:

```text
NGINX_HARNESS_WORK_ROOT=/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0
```

That path is traversable by the NGINX worker. Details are in
`nginx-docroot-permission-analysis.md` and `nginx-blocked-runtime-cases.md`.

## Removed Local Test Folders

- `connectors/_template/tests/`
- `connectors/nginx/tests/`
- `connectors/apache/tests/`

Executable connector tests are framework-owned and are not maintained in local
`connectors/*/tests` directories.

## Checks

| Check | Result | Note |
| --- | --- | --- |
| `test ! -d connectors/_template/tests` | PASS | Template test folder is absent. |
| `test ! -d connectors/apache/tests` | PASS | Apache test folder is absent. |
| `test ! -d connectors/nginx/tests` | PASS | NGINX test folder is absent. |
| `make lint` | PASS | `actionlint unavailable` was informational; command exited 0. |
| `make quick-check` | PASS | Lint, Python compile checks, doc links, helper checks, metadata drift, and `git diff --check` passed. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |

## Not Verified

- RESPONSE_BODY blocking for Apache and NGINX.
- Full runtime matrix promotion beyond `partial`.
- Apache-specific connector YAML cases under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there during this verification.
- Default `make smoke-common` without preparing the default build root.

## Report Files

- `connector-scaffold-decisions.md`
- `template-evaluation.md`
- `nginx-evaluation.md`
- `apache-evaluation.md`
- `component-download-check.md`
- `runtime-test-run-src.md`
- `verified-runtime-run.md`
- `nginx-build-fail-analysis.md`
- `nginx-docroot-permission-analysis.md`
- `nginx-blocked-runtime-cases.md`
- `summary.md`
- `findings.md`
- `files-reviewed.md`
- `open-questions.md`
