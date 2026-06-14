# Next Fix Plan

Generated at: `2026-06-14T10:52:24Z`

Native MRTS Apache/NGINX remains separate infrastructure evidence; this plan targets connector Full-Matrix leftovers only.

## P0
- None.

## P1
- None.

## P2
- None.

## P3
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| phase4_hard_abort_capability | 116 | apache, nginx, haproxy | Phase 4/RESPONSE_BODY now requires hard-abort evidence, not status-only denial | stabilize NGINX strict evidence; classify Apache/HAProxy gaps until real transport abort evidence exists | high if promoted prematurely or faked | phase4 hard-abort report regeneration, targeted strict Phase 4 connector evidence, native report regeneration |
| transformation_semantics | 36 | apache, nginx, haproxy | largest semantic cluster; likely needs native/libmodsecurity comparison before any fix | deeper semantic evidence, not harness routing | high | targeted transformation cases, native comparison where available |

## P4
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| rule_chain_semantics and small single-connector leftovers | 7 | mostly nginx for connector-only leftovers | smaller count; useful after high-signal evidence clusters | focused per-case triage | low to medium | targeted single-case smokes |
