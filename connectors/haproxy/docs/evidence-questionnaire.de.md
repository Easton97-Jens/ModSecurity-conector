# HAProxy-Integrationsnachweis-Fragebogen

**Sprache:** [English](evidence-questionnaire.md) | Deutsch

Status: für den aktuellen Produktionsumfang SPOA beantwortet

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

## Offene Fragen

- Welche zusätzlichen Nachweise sind vor der Ganzkörper-RESPONSE_BODY-Promotion erforderlich?
- Welcher Produktionsservice-Manager und welches Paketlayout sollten dokumentiert werden?
- Welche Multi-Worker- und Langzeit-Transaktions-Cache-Validierung ist erforderlich?
- Welche dynamischen Statuszuordnungen sollten über den festen HAProxy hinaus promoted werden?
  Regeln in den Beispielen?

Phase 4 / RESPONSE_BODY bleibt nicht promoted; begrenzte strikte Abbruchbeweise sind
documented/reported nur als Laufzeitbeweis.
