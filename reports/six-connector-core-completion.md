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
