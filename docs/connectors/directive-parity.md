# Connector Directive Parity

**Language:** English | [Deutsch](directive-parity.de.md)


Status: current adapter-owned Apache and NGINX code, plus HAProxy SPOA config

This document records directive and configuration support in the local
connector implementations. Runtime promotion is still evidence-scoped; a
directive existing in code does not by itself promote full behavior.

## Directive Matrix

| Directive / Config Surface | Apache | NGINX | HAProxy | Notes / Risk |
| --- | --- | --- | --- | --- |
| `modsecurity` | Supported | Supported | Not applicable | HAProxy uses HAProxy/SPOE/SPOA config, not server `modsecurity_*` directives. |
| `modsecurity_rules` | Supported | Supported | Not applicable | Rule loading remains connector-owned. HAProxy loads rules through the SPOA agent `rules-file`. |
| `modsecurity_rules_file` | Supported | Supported | Not applicable | HAProxy equivalent is `rules-file=/etc/modsecurity/haproxy-rules.conf`. |
| `modsecurity_rules_remote` | Supported | Supported | Not applicable | Remote rule loading is connector-owned for Apache/NGINX; HAProxy agent config does not expose this server directive. |
| `modsecurity_use_error_log` | Supported | Supported | Not applicable | Logging policy only; audit and intervention behavior are separate. |
| `modsecurity_transaction_id` | Supported | Supported | Not applicable | Apache uses static string semantics; NGINX uses complex values; HAProxy correlates through HAProxy `unique-id` / SPOE `request_id`. |
| `modsecurity_transaction_id_expr` | Supported | Not supported | Not applicable | Apache-only expression directive. |
| `modsecurity_phase4_mode` | Supported | Supported | Not applicable | Bounded Phase 4 control. This does not promote full RESPONSE_BODY support. |
| `modsecurity_phase4_content_types_file` | Supported | Supported | Not applicable | Bounded response content-type allow-list. |
| `modsecurity_phase4_log` | Supported | Supported | Not applicable | JSONL Phase 4 decision/evidence log for Apache/NGINX. |
| `modsecurity_phase4_body_limit` | Supported | Not supported | Not applicable | Apache connector response-buffer bound. NGINX uses libmodsecurity limits and strict-abort controls instead. |
| `filter spoe engine modsecurity` | Not applicable | Not applicable | Supported | HAProxy SPOE entry point. |
| `http-request send-spoe-group` | Not applicable | Not applicable | Supported | Sends request phases 1/2 evidence to `haproxy-modsecurity-spoa`. |
| `http-response send-spoe-group` | Not applicable | Not applicable | Supported | Sends response headers and bounded response-body evidence. |
| `decision-log` | Not applicable | Not applicable | Supported | SPOA agent JSONL decision log, usually `/var/log/haproxy-modsecurity/decision.jsonl`. |
| `audit-log` | Not applicable | Not applicable | Supported | SPOA/libmodsecurity audit-log plumbing. |

## Apache Directives

The Apache connector currently registers:

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

`modsecurity_transaction_id` keeps static-string semantics.
`modsecurity_transaction_id_expr` is a separate opt-in Apache string
expression. Static and expression transaction IDs are mutually exclusive in the
same Apache context, and normal child-context overrides apply during config
merge.

Apache Phase 4 support is bounded. The connector can inspect buffered response
bytes, log Phase 4 decisions, and record strict-abort evidence when a disruptive
intervention arrives after response commit. It is not a full RESPONSE_BODY
promotion.

## NGINX Directives

The NGINX connector currently registers:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

NGINX `modsecurity_transaction_id` uses an NGINX complex value and may evaluate
per-request variables. Apache expression transaction IDs use
`modsecurity_transaction_id_expr` instead. NGINX Phase 4 support is bounded
strict-abort evidence and not full RESPONSE_BODY promotion.

## HAProxy Configuration Surface

HAProxy does not implement Apache/NGINX `modsecurity_*` directives. The current
production path is:

```text
HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity
```

Supported configuration is split across:

- HAProxy config: `filter spoe engine modsecurity`,
  `http-request send-spoe-group`, `http-response send-spoe-group`, and
  enforcement rules that read `txn.modsec.*` variables.
- SPOE config: request and response message argument mapping in
  `spoe-modsecurity.conf`.
- SPOA agent config: `listen`, `rules-file`, `decision-log`, `audit-log`,
  `mode`, `fail-mode`, `request-body-limit`, `response-body-limit`, and
  `response-body-timeout`.

HAProxy runtime evidence includes request phases 1/2, implemented phase 3
response headers, decision/audit logs, and bounded Phase 4 strict-abort
evidence. There is no synthetic matrix writer.

## Deferred And Risky Areas

Bucket brigades, input and output filters, body buffering, intervention runtime
paths, hook/filter ordering, transaction ownership, and request/response
lifecycle behavior remain connector-specific. They must not be moved into
`common/` without a separate design and runtime evidence.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.

## Common Metadata

`common/include/msconnector/directives.h` contains shared directive-name
metadata used by Apache and NGINX.

`common/include/msconnector/options.h` contains shared option/default metadata
for enablement, logging policy, and bounded Phase 4 options. These headers
contain no Apache types, no NGINX types, no HAProxy types, no hooks, no filters,
no bucket brigades, no transaction ownership, and no request or response-body
runtime behavior.
