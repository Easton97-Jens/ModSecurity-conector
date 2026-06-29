# Entscheidungsmatrix für die HAProxy-Abdeckung

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: teilweise, Produktion SPOA Laufzeitnachweis

Die HAProxy-Matrix wird aus Live-Runtime-Nachweisen durch HAProxy generiert.
SPOE/SPOP, `haproxy-modsecurity-spoa` und libmodsecurity. Nicht unterstützt oder
Force-All-Zeilen werden nicht in die standardmäßige Smoke-Zusammenfassung hochgestuft.

## Aktuelle Laufzeitzählungen

| Target | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Default smoke | 55 | 55 | 0 | 0 | 0 | runtime validation snapshot |
| Force-all matrix | 133 | 104 | 23 | 0 | 6 | generated HAProxy detail report |

## Versorgungsgebiete

| Area | Status | Evidence |
| --- | --- | --- |
| Request phases 1/2 | live evidenced | request SPOE group and ModSecurity decisions |
| Phase 3 response headers | implemented, live evidenced | response SPOE group and decision logs |
| Audit/log | live evidenced for current cases | audit-log plumbing and case artifacts |
| CRS SQLi anomaly block | live evidenced | with-CRS runtime summary |
| Phase 4 / RESPONSE_BODY | bounded strict-abort evidence only | `wait-for-body`, response-body limits, and decision logs |
| Full-body RESPONSE_BODY | not promoted | requires separate proof |

## Promotion-Regeln

- `PASS` bedeutet, dass die Live-HAProxy-Ausführung das erwartete Fallergebnis erbracht hat.
- `FAIL` bedeutet, dass die Live-HAProxy-Ausführung zu einem anderen Ergebnis geführt hat.
- `NOT_EXECUTABLE` bedeutet außerhalb des aktuellen HAProxy-Laufzeitbereichs.
- Erzwingen Sie, dass alle Zeilen drin bleiben
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- Stammzusammenfassungen bleiben konnektorneutral.
- Es gibt keinen Writer für synthetische Matrizen.

Phase 4 / RESPONSE_BODY bleibt nicht promoted; begrenzte strikte Abbruchbeweise sind
documented/reported nur als Laufzeitbeweis.
