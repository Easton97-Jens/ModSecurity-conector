# Entscheidungsmatrix für die HAProxy-Abdeckung

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: teilweise; historische SPOA-Laufzeitnachweise sind keine kanonische
Phase-4-Hochstufung

Die HAProxy-Matrix fasst historische Laufzeitnachweise des
SPOE/SPOP-Pfads mit `haproxy-modsecurity-spoa` und libmodsecurity zusammen.
Nicht ausführbare oder Force-All-Zeilen werden nicht in den Standard-Smoke-
Status hochgestuft.

## Aktuelle Laufzeitzählungen

| Ziel | Ausgeführt | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Nachweis |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Standard-Smoke (historisch) | 55 | 55 | 0 | 0 | 0 | Schnappschuss der Laufzeitvalidierung |
| Force-All-Matrix (historisch) | 133 | 104 | 23 | 0 | 6 | erzeugter HAProxy-Detailbericht |

## Historische Abdeckungsangaben

| Bereich | Status | Einordnung |
| --- | --- | --- |
| Request-Phasen 1/2 | historisch belegt | Request-SPOE-Gruppe und ModSecurity-Entscheidungen |
| Phase-3-Response-Header | implementiert, historisch belegt | Response-SPOE-Gruppe und Entscheidungsprotokolle |
| Audit/Protokoll | für historische Fälle belegt | Audit-Protokollierung und Fallartefakte |
| CRS-SQLi-Anomaliesperre | historisch belegt | Laufzeitzusammenfassung mit CRS |
| Phase 4 / RESPONSE_BODY | `implemented_not_asserted` | `wait-for-body`, Response-Body-Limits und Protokolle sind keine kanonische Facetten-Evidence |
| Vollständiger RESPONSE_BODY | nicht hochgestuft | erfordert einen getrennten Nachweis |

## Promotion-Regeln

- `PASS` bedeutet, dass die Live-HAProxy-Ausführung das erwartete Fallergebnis erbracht hat.
- `FAIL` bedeutet, dass die Live-HAProxy-Ausführung zu einem anderen Ergebnis geführt hat.
- `NOT_EXECUTABLE` bedeutet außerhalb des aktuellen HAProxy-Laufzeitbereichs.
- Alle Force-All-Zeilen bleiben in
  `reports/testing/generated/haproxy-runtime-results.generated.md` erhalten.
- Zusammenfassungen auf Root-Ebene bleiben connector-neutral.
- Es gibt keinen Generator für synthetische Matrizen.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft; begrenzte Nachweise für einen
strikten Abbruch sind nur Laufzeitnachweise.

## Kanonische Entscheidung für Phase 4

Der begrenzte SPOA/SPOP-Response-Zweig ist ausschließlich eine Quellfähigkeit.
Er belegt weder Antwortzeitpunkt noch Transportverhalten. Nur
Response-Body-Verfügbarkeit, `phase4` und `phase4_rule_evaluation` bleiben
`implemented_not_asserted`; die semantischen Durchsetzungs- und
Late-Intervention-Facetten sind `not_implemented`.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered` und `phase4` | `implemented_not_asserted` | Einen gemeinsamen Lauf über HAProxy und Agent belegen. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | Regel `1100301` beobachten, unabhängig von einem 403. |
| `phase4_pre_commit_deny` | `not_implemented` | Aktuelle Felder sind policy-abgeleitet; kein Host-Runner erfasst sichtbaren Client-Status und Commit-Zeitpunkt. |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `not_implemented` | Es gibt keinen HAProxy-Hostpunkt nach dem Commit und keine sichere oder strikte späte Aktion. |
| `late_intervention_status_metadata` | `not_implemented` | Es gibt keinen hostbeobachteten ursprünglichen/sichtbaren Status mit Zeitpunkt; policy-abgeleitete Werte reichen nicht aus. |

Fehlt dieser Nachweis, wird `NOT_EXECUTED` und kein künstliches 403-`PASS`
gemeldet. Alle Nachweise enthalten ausschließlich Metadaten.
