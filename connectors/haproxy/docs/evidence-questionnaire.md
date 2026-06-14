# HAProxy Integration Evidence Questionnaire

Status: answered for the current production SPOA scope

| Question | Current answer | Evidence |
| --- | --- | --- |
| Can HAProxy pass requests to an external component? | Yes, through SPOE/SPOP. | HAProxy examples and runtime harness. |
| Is the external component implemented in this repository? | Yes, as `haproxy-modsecurity-spoa`. | `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`. |
| Does the component use libmodsecurity? | Yes. | `connectors/haproxy/src/haproxy_modsecurity_binding.c`. |
| Are request phases 1/2 live evidenced? | Yes for current default scope. | `55/55 PASS` default smoke. |
| Are CRS decisions live evidenced? | Yes for current with-CRS scope. | HAProxy runtime summary and detail report. |
| Are response headers implemented? | Yes. | `response-check` SPOE group and decision logs. |
| Is RESPONSE_BODY promoted? | No. | Bounded strict-abort evidence only. |
| Are decision logs produced? | Yes. | `decision.jsonl`. |
| Is audit logging plumbed? | Yes. | `audit-log` config and runtime artifacts. |
| Is there a synthetic matrix writer? | No. | Reports consume runtime summaries and snapshots. |

## Open Questions

- What additional evidence is required before full-body RESPONSE_BODY promotion?
- What production service-manager and package layout should be documented?
- What multi-worker and long-running transaction-cache validation is required?
- Which dynamic status mappings should be promoted beyond the fixed HAProxy
  rules in the examples?

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
