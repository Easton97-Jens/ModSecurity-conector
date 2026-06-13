# Next Fix Plan

Generated at: `2026-06-13T15:03:34Z`

Native MRTS Apache/NGINX remains separate infrastructure evidence; this plan targets connector Full-Matrix leftovers only.

## P0
- None.

## P1
- None.

## P2
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| response_header_backend_setup | 56 | apache, nginx | specialized Phase 3 response-header probes need deterministic backend headers before connector behavior can be judged | add or route deterministic Content-Type, Location, and Set-Cookie response headers in the harness/backend path | low to medium | targeted response-header cases, make smoke-apache, make smoke-nginx |
| response_header_multi_value_gap | 12 | haproxy | HAProxy proves response-header visibility for single-value controls but still misses Set-Cookie multi-value matches | trace SPOE response-header argument population for repeated Set-Cookie values | medium | targeted HAProxy Set-Cookie response-header cases, make smoke-haproxy |
| request_body_processor / multipart_files / xml_processor | 189 | apache, nginx, haproxy | high combined volume, but likely multiple true processor gaps | split by body type first; avoid one broad fix | medium to high | targeted body processor cases, connector smoke for touched connector, full matrix if parser behavior changes |

## P3
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| phase4_hard_abort_capability | 116 | apache, nginx, haproxy | Phase 4/RESPONSE_BODY now requires hard-abort evidence, not status-only denial | stabilize NGINX strict evidence; classify Apache/HAProxy gaps until real transport abort evidence exists | high if promoted prematurely or faked | phase4 hard-abort report regeneration, targeted strict Phase 4 connector evidence, native report regeneration |
| transformation_semantics | 144 | apache, nginx, haproxy | largest semantic cluster; likely needs native/libmodsecurity comparison before any fix | deeper semantic evidence, not harness routing | high | targeted transformation cases, native comparison where available |

## P4
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| rule_chain_semantics and small single-connector leftovers | 13 | mostly nginx for connector-only leftovers | smaller count; useful after high-signal evidence clusters | focused per-case triage | low to medium | targeted single-case smokes |
