# NGINX Regression Map

Status: scaffolded

Source: `/root/conecter/ModSecurity-nginx/tests/`

| Original test path | Purpose | Category | Portable | Capabilities | Known problems | Recommended target |
| --- | --- | --- | --- | --- | --- | --- |
| `modsecurity.t` | Basic NGINX connector behavior | connector-specific | no | NGINX module, request processing | nginx-tests harness required | `tests/nginx/` |
| `modsecurity.t` phase 1/2 block and "nothing to detect" snippets | ARGS-based deny/status and pass-through behavior | engine-core via NGINX runtime | yes | query args, phase:1/2, intervention, pass-through | Redirect, custom status, phase:4, and nginx-tests harness logic remain connector-specific | `tests/common/cases/minimal/phase1_header_block.yaml`; `tests/common/cases/minimal/phase2_args_block.yaml`; `tests/common/cases/minimal/phase2_args_pass.yaml` |
| `modsecurity-config.t` | NGINX config directives | connector-specific | no | NGINX config | Directive syntax is connector-specific | `tests/nginx/` |
| `modsecurity-config-auditlog.t` | Audit log config behavior | audit-log/connector-specific | no | NGINX runtime, audit artifacts | Log paths and format are connector-specific | `tests/nginx/` |
| `modsecurity-config-auditlog.t` root audit log fragment | Serial audit log creation and stable content checks | audit-log/engine-core via NGINX runtime | partial | serial audit log, rule ID, request URI, message | Location inheritance and multiple audit-log files remain connector-specific | `tests/common/cases/minimal/audit_log_phase1_block.yaml` |
| `modsecurity-config-debuglog.t` | Debug log config behavior | audit-log/connector-specific | no | NGINX runtime, debug artifacts | Debug text is volatile | `tests/nginx/` |
| `modsecurity-config-merge.t` | Config merge behavior | connector-specific | no | NGINX location merge | NGINX-specific | `tests/nginx/` |
| `modsecurity-request-body.t` | Request body behavior | request-body/connector-specific | partial | NGINX request body handling | Limit, auth_request, method matrix, and proxy mechanics are connector-specific | `tests/nginx/`; portable fragments in `tests/common/cases/minimal/request_body_json_block.yaml` and `tests/common/cases/minimal/request_body_urlencoded_block.yaml` |
| `modsecurity-response-body.t` | Response body behavior | response-body/connector-specific | no | NGINX response filter | Filter ordering is connector-specific | `tests/nginx/` |
| `src/ngx_http_modsecurity_header_filter.c` | NGINX response header hook integration | connector-specific implementation source | partial | header filter lifecycle | Source file is not imported; shared case only validates a portable response-header intervention | `tests/common/cases/minimal/response_header_basic.yaml` |
| `modsecurity-h2.t` | HTTP/2 behavior | connector-specific | no | NGINX HTTP/2 | NGINX-specific | `tests/nginx/` |
| `modsecurity-proxy*.t` | Proxy behavior | connector-specific | no | NGINX proxy | Requires NGINX upstream setup | `tests/nginx/` |
| `modsecurity-limits.t` | Limits behavior | request-body/connector-specific | partial | request body limits | Engine semantics may be portable after extraction | split after review |
| `modsecurity-scoring.t` | Rule scoring behavior | engine-core/connector-specific | partial | rules, NGINX runtime | Extract engine-only expectations if possible | common or `tests/nginx/` after review |
| `modsecurity-transaction-id.t` | Transaction ID behavior | connector-specific | no | custom transaction ID | NGINX variable support | `tests/nginx/` |
