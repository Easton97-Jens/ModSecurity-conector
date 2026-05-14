# NGINX Regression Map

Status: scaffolded

Source: `/root/conecter/ModSecurity-nginx/tests/`

| Original test path | Purpose | Category | Portable | Capabilities | Known problems | Recommended target |
| --- | --- | --- | --- | --- | --- | --- |
| `modsecurity.t` | Basic NGINX connector behavior | connector-specific | no | NGINX module, request processing | nginx-tests harness required | `tests/nginx/` |
| `modsecurity-config.t` | NGINX config directives | connector-specific | no | NGINX config | Directive syntax is connector-specific | `tests/nginx/` |
| `modsecurity-config-auditlog.t` | Audit log config behavior | audit-log/connector-specific | no | NGINX runtime, audit artifacts | Log paths and format are connector-specific | `tests/nginx/` |
| `modsecurity-config-debuglog.t` | Debug log config behavior | audit-log/connector-specific | no | NGINX runtime, debug artifacts | Debug text is volatile | `tests/nginx/` |
| `modsecurity-config-merge.t` | Config merge behavior | connector-specific | no | NGINX location merge | NGINX-specific | `tests/nginx/` |
| `modsecurity-request-body.t` | Request body behavior | request-body/connector-specific | no | NGINX request body handling | Hook/buffering behavior is connector-specific | `tests/nginx/` |
| `modsecurity-response-body.t` | Response body behavior | response-body/connector-specific | no | NGINX response filter | Filter ordering is connector-specific | `tests/nginx/` |
| `modsecurity-h2.t` | HTTP/2 behavior | connector-specific | no | NGINX HTTP/2 | NGINX-specific | `tests/nginx/` |
| `modsecurity-proxy*.t` | Proxy behavior | connector-specific | no | NGINX proxy | Requires NGINX upstream setup | `tests/nginx/` |
| `modsecurity-limits.t` | Limits behavior | request-body/connector-specific | partial | request body limits | Engine semantics may be portable after extraction | split after review |
| `modsecurity-scoring.t` | Rule scoring behavior | engine-core/connector-specific | partial | rules, NGINX runtime | Extract engine-only expectations if possible | common or `tests/nginx/` after review |
| `modsecurity-transaction-id.t` | Transaction ID behavior | connector-specific | no | custom transaction ID | NGINX variable support | `tests/nginx/` |
