# NGINX Blocked Runtime Cases

**Language:** English | [Deutsch](nginx-blocked-runtime-cases.de.md)

Status: historical blocker resolved in current `/src` run

## Current Result

The latest verified `/src` runs no longer reproduce the 11 BLOCKED NGINX
runtime rows.

| Command | Result | Summary |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | NGINX 61 PASS, 0 FAIL, 0 BLOCKED |

Current evidence:

- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/nginx.rc`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`

## Historical BLOCKED Cases

The prior report state recorded NGINX as 43 PASS, 0 FAIL, and 11 BLOCKED. The
current result files were overwritten by the successful rerun, so the exact
prior per-case JSON rows are not available in the current results directory.
The historical blocked case names below are preserved from the earlier
`verified-runtime-run.md` report content.

| Case | Expected status in current YAML summary | Current NGINX status | Current actual status | Current Apache status | Area | Current path |
| --- | ---: | --- | ---: | --- | --- | --- |
| `pr70_phase3_audit_response_header` | 403 | PASS | 403 | PASS | audit-log, phase3, response-headers | `modules/ModSecurity-test-Framework/tests/cases/audit-log/pr70-phases/pr70_phase3_audit_response_header.yaml` |
| `v2_transformation_url_decode_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-uri, transformations | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v2_transformation_url_decode_pass_no_match.yaml` |
| `v3_args_names_get_pass_no_match` | 200 | PASS | 200 | PASS | args-names, pass-through, phase2, query-args | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_args_names_get_pass_no_match.yaml` |
| `v3_request_cookies_names_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-cookies | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_request_cookies_names_pass_no_match.yaml` |
| `v3_request_cookies_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-cookies | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_request_cookies_pass_no_match.yaml` |
| `v3_request_headers_names_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-headers | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_request_headers_names_pass_no_match.yaml` |
| `action_allow_phase1_pass` | 200 | PASS | 200 | PASS | pass-through, phase1 | `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_allow_phase1_pass.yaml` |
| `phase2_args_pass` | 200 | PASS | 200 | PASS | pass-through, phase2, query-args | `modules/ModSecurity-test-Framework/tests/cases/phases/phase2/phase2_args_pass.yaml` |
| `response_body_pass` | 200 | PASS | 200 | PASS | pass-through, phase4, response-body | `modules/ModSecurity-test-Framework/tests/cases/response/body/response_body_pass.yaml` |
| `rule_chain_first_only_pass` | 200 | PASS | 200 | PASS | pass-through, phase2, query-args, rule-parser | `modules/ModSecurity-test-Framework/tests/cases/security/rule-chain/rule_chain_first_only_pass.yaml` |
| `rule_chain_second_only_pass` | 200 | PASS | 200 | PASS | pass-through, phase2, query-args, rule-parser | `modules/ModSecurity-test-Framework/tests/cases/security/rule-chain/rule_chain_second_only_pass.yaml` |

## Pattern

The historical list is dominated by pass-through cases that require NGINX to
serve `index.html` from the generated docroot. The blocker was therefore
consistent with a docroot read problem rather than a ModSecurity rule failure.

The current analysis in `nginx-docroot-permission-analysis.md` shows why:
when `NGINX_HARNESS_PARENT` falls back to `/tmp` in this environment, the
worker cannot traverse `/tmp` because it is mode `700`. The current parent
contract points `NGINX_HARNESS_PARENT` at `BUILD_ROOT`, and the reruns pass.

## Comparison With Apache

Apache was not affected by the same docroot parent problem in the documented
run. The latest common summary records Apache 54 PASS, 0 FAIL, 0 BLOCKED.

## Decision

Historical classification: environment/docroot permission blocker.

Current classification: resolved for `/src` runs with
`NGINX_HARNESS_PARENT=$(BUILD_ROOT)`.

No historical blocked case is counted as PASS for the old run. The PASS status
comes only from the new reruns listed above.

The former With-CRS expectation mismatch is resolved in the current `/src`
run. It was not a recurrence of the docroot BLOCKED issue.

RESPONSE_BODY blocking remains `not verified`: `response_body_pass` is a
pass-through case, not a blocking response-body testcase.
