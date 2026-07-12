# Six-connector HTTP/1.1 core completion

**Language:** English | [Deutsch](six-connector-core-completion.de.md)

## Evidence boundary

This compact matrix covers only the selected real HTTP/1.1 host paths and
existing core catalog cases. It records canonical run evidence; it does not
claim a complete catalog, a capability promotion, or a production outcome.
Strict transport enforcement, HTTP/2, HTTP/3, and extended catalog cases
remain separate work.

| Connector | P1 | P2 | P3 | P4 rule | P4 Safe | First byte | No full buffer | Cleanup | Current blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | None for the compact core |
| NGINX | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | None for the compact core |
| HAProxy | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | None for the compact core |
| Envoy | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | None for the compact core |
| Traefik | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | None for the compact core |
| lighttpd | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | None for the compact core |

## Canonical shared evidence

- Shared run ID: `six-connectors-core-final-20260712T164725Z-e16e7f1`
- Aggregate target `full-lifecycle-all-connectors`: exit `0`; every selected
  connector runner exited `0`.
- `make check-six-connector-core-completion`: `PASS`.
- Each aggregate connector result remains `NOT_EXECUTED` only for the
  non-core extended catalog cases; the compact core rows above are `PASS` and
  no run reported `FAIL` or `BLOCKED`.

## Selected real host paths

| Connector | Selected HTTP/1.1 host path | Integration mode | Final run ID | Core evidence |
| --- | --- | --- | --- | --- |
| Apache | native httpd module | `native-httpd-module` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/alternative, P2 403, P3 403, P4 rule 1100301 Safe, EOS, barrier, cleanup |
| NGINX | native HTTP module | `native-nginx-http-module` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/alternative, P2 403, P3 403, P4 rule 1100301 Safe, EOS, barrier, cleanup |
| HAProxy | native HTX filter | `native-htx-filter` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/429, P2 403, P3 403, P4 rule 1100301 Safe, EOS, barrier, cleanup |
| Envoy | ext_proc listener and service | `ext_proc` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403, P2 403, P3 403/302 redirect, P4 rule 1100301 Safe, EOS, barrier, cleanup |
| Traefik | native local-plugin middleware | `native-traefik-middleware` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/429, P2 403, P3 403, P4 rule 1100301 Safe, EOS, barrier, cleanup |
| lighttpd | patched native Entity-Body host | `patched-native-lighttpd` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/alternative, P2 403, P3 403, P4 rule 1100301 Safe, EOS, barrier, cleanup |

For every selected path, the P4 Safe event is a post-commit requested `deny`
with actual `log_only`, a visible HTTP 200, sent headers/body, and no
connection abort. The synchronized first-byte artifact is a payload-free
real-host PASS: the client received a body byte while the upstream was paused,
before upstream EOS, and without connector-owned full-response buffering.
Lifecycle counters are balanced and the selected P2/P4 EOS paths are recorded
once per transaction. The evidence records bounded transaction and rule IDs,
not body payloads.

The result does not assert per-chunk Phase-4 decisions: response-body chunks
are ingested incrementally and the selected P4 rule is evaluated at
end-of-stream where the host/runtime reports it.

## Connector configuration references

This is a source-to-documentation completion record, not additional runtime,
lifecycle, security, or production evidence. The generated
[configuration inventory](../connector-configuration-inventory.json) currently
contains 341 rows. The six local references and the central
[Common Runtime](../../examples/common/common-connector-configuration.md),
[ModSecurity engine](../../examples/common/modsecurity-directives.md), and
[rule examples](../../examples/common/rule-examples.md) keep connector switches
separate from engine directives.

| Connector | Source-backed findings and documented scope | Reference and remaining gap |
| --- | --- | --- |
| Apache | 11 registered Apache directives; 14 documented rows including 3 host-example fields; 12 engine directives are used by example rules. | [Reference](../../examples/apache/configuration-reference.md); available configuration gate passed; 0 undocumented registered directives. |
| NGINX | 10 `ngx_command_t` directives; 18 documented rows including 8 host-example fields; 4 Phase-4 directives are separated from `SecRuleEngine`. | [Reference](../../examples/nginx/configuration-reference.md); available configuration gate passed; 0 undocumented registered directives. |
| HAProxy | 3 native HTX filter options; 30 compatibility rows are separate (28 SPOP parser keys plus the compatibility filter and retired legacy row); 41 documented rows in total. | [Reference](../../examples/haproxy/configuration-reference.md); available configuration gate passed; 0 undocumented native or compatibility options. |
| Envoy | 66 selected `ext_proc` YAML fields, 14 service-JSON fields, 5 service CLI flags, and 5 materializer placeholders; 51 `ext_authz` compatibility fields are separate; 141 documented rows in total. | [Reference](../../examples/envoy/configuration-reference.md); available configuration gate passed; 0 undocumented extracted fields. |
| Traefik | 16 static and 25 dynamic/native fields, including 7 native middleware fields; 30 `forwardAuth` compatibility fields are separate; 71 documented rows in total. | [Reference](../../examples/traefik/configuration-reference.md); available configuration gate passed; 0 undocumented extracted fields. |
| lighttpd | 2 registered plugin keys, 10 selected patched-host fields, and 7 sidecar compatibility fields; 19 documented rows in total. | [Reference](../../examples/lighttpd/configuration-reference.md); available configuration gate passed; 0 undocumented plugin keys. |
| Common Runtime | 25 current `key=value` parser keys, all 25 documented with source-verified defaults where the parser/configuration source establishes one. | [Reference](../../examples/common/common-connector-configuration.md); 0 undocumented keys. |
| ModSecurity engine | 12 directives used by checked-in example rules, all 12 documented; the rule walkthrough distinguishes variable, operator, actions, and host commit boundaries. | [Reference](../../examples/common/modsecurity-directives.md); connector/engine distinction verified; 0 undocumented used directives. |

| Validation | Result and boundary |
| --- | --- |
| Source-to-documentation checker | `make check-connector-config-reference`: PASS; parser/registration, configuration contract, example, generated-reference, and inventory parity are checked together. |
| Bilingual parity | `make check-bilingual-docs` and the configuration-reference section parity check: PASS; directive names, syntax, values, defaults, contexts, examples, paths, IDs, and targets are kept technically equal. |
| Configuration parse checks | `make check-config-all-connectors`: PASS for the available selected host checks; this does not turn the documentation profiles into new lifecycle evidence. |
| Placeholder checker | PASS through the source-backed Envoy materializer contract: all five `@...@` placeholders are inventoried and unresolved/template drift fails the check. |
| Profile and local-path checker | PASS: required minimal, safe, strict-boundary, DetectionOnly, and disabled profile material is present; DetectionOnly/Off rules are asserted; example files contain no checked development-local path. |
