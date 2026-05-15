# Shared Case Origin Map

Status: implemented

Only connector-neutral rule/request/expectation fragments are mapped here. The
original Apache and NGINX harness mechanics remain connector-specific.

| Shared case | Original test path | Source | Why portable | Known limitations |
| --- | --- | --- | --- | --- |
| `phase1_header_block.yaml` | `ModSecurity-apache/tests/regression/rule/15-json.t`; `ModSecurity-nginx/tests/modsecurity.t` | apache/nginx | Adapts Apache's phase:1 `REQUEST_HEADERS:Content-Type` pattern to a neutral header and combines it with NGINX phase:1 deny/status behavior | Does not test connector config inheritance or JSON parsing |
| `phase2_args_block.yaml` | `ModSecurity-apache/tests/regression/rule/00-basics.t`; `ModSecurity-nginx/tests/modsecurity.t` | apache/nginx | Uses query ARGS, phase:2, deny, and HTTP 403 | Does not assert audit/debug log contents |
| `request_body_urlencoded_block.yaml` | `ModSecurity-apache/tests/regression/target/00-targets.t`; `ModSecurity-nginx/tests/modsecurity-request-body.t` | apache/nginx | Uses form POST body and ARGS_POST semantics | Does not cover request body limits, chunking, or methods beyond POST |
| `request_body_json_block.yaml` | `ModSecurity-apache/tests/regression/rule/15-json.t`; `ModSecurity-nginx/tests/modsecurity-request-body.t` | apache/nginx | Uses raw REQUEST_BODY content and Content-Type header | Does not require JSON parser collections such as `ARGS:foo` |
| `response_header_basic.yaml` | `ModSecurity-apache/tests/regression/misc/00-phases.t`; `ModSecurity-nginx/src/ngx_http_modsecurity_header_filter.c` | apache/nginx | Uses standard response header phase behavior | Depends on a static response exposing `Last-Modified`; fail/blocked is acceptable if not proven |

Observed locally on 2026-05-15 with `BUILD_ROOT=/src/ModSecurity-conector-build`:

| Shared case | Apache PoC | NGINX PoC |
| --- | --- | --- |
| `phase1_header_block.yaml` | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_block.yaml` | pass, HTTP 403 | pass, HTTP 403 |
| `request_body_json_block.yaml` | pass, HTTP 403 | pass, HTTP 403 |
| `request_body_urlencoded_block.yaml` | pass, HTTP 403 | pass, HTTP 403 |
| `response_header_basic.yaml` | pass, HTTP 403 | pass, HTTP 403 |
