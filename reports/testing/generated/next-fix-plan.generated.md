# Next Fix Plan

Generated at: `2026-06-13T11:44:02Z`

Native MRTS Apache/NGINX remains separate infrastructure evidence; this plan targets connector Full-Matrix leftovers only.

## P0
- None.

## P1
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| harness_evidence_issue / tfn_chain_lowercase_trim_pass_through | 12 | apache, nginx, haproxy | small, clear evidence-missing/actual_status 0 cluster; safest quick-win candidate | inspect result creation/log matching for the transformation pass-through case; report-only or harness evidence fix if confirmed | low to medium | targeted smoke for the case on all connectors, make lint quick-check, make full-matrix-parallel if harness behavior changes |
| audit_log_evidence / v3_action_nolog_pass_no_audit | 6 | apache, nginx, haproxy | HTTP behavior passes; remaining failure is evidence/assertion semantics | verify whether audit-log expectation is correct for nolog and classify/report accordingly | low to medium | targeted smoke for v3_action_nolog_pass_no_audit, make lint quick-check |

## P2
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| response_header_hook | 94 | apache, nginx, haproxy | large phase 3 cluster with clear response-header surface | trace response header visibility and blocking hooks per connector | medium | targeted response-header cases, make smoke-apache, make smoke-nginx, make smoke-haproxy |
| request_body_processor / multipart_files / xml_processor | 189 | apache, nginx, haproxy | high combined volume, but likely multiple true processor gaps | split by body type first; avoid one broad fix | medium to high | targeted body processor cases, connector smoke for touched connector, full matrix if parser behavior changes |

## P3
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| phase4_response_body_non_promoted | 116 | apache, nginx, haproxy | known non-promoted phase 4/RESPONSE_BODY surface; native 100003-1 remains separate native semantics evidence | report/classification work or long-term promotion policy, not a quick connector fix | high if promoted prematurely | native report regeneration, response-body promotion guard |
| transformation_semantics | 144 | apache, nginx, haproxy | largest semantic cluster; likely needs native/libmodsecurity comparison before any fix | deeper semantic evidence, not harness routing | high | targeted transformation cases, native comparison where available |

## P4
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| rule_chain_semantics and small single-connector leftovers | 13 | mostly nginx for connector-only leftovers | smaller count; useful after high-signal evidence clusters | focused per-case triage | low to medium | targeted single-case smokes |
