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
| Phase 4 / RESPONSE_BODY | `not_implemented` | Das frühere `wait-for-body`-Sample ist deaktiviert; der gewählte SPOP-Pfad besitzt keinen verdrahteten nativen Response-Chunk-Pfad |
| Vollständiger RESPONSE_BODY | nicht hochgestuft | erfordert einen getrennten Nachweis |

## Promotion-Regeln

- `PASS` bedeutet, dass die Live-HAProxy-Ausführung das erwartete Fallergebnis erbracht hat.
- `FAIL` bedeutet, dass die Live-HAProxy-Ausführung zu einem anderen Ergebnis geführt hat.
- `NOT_EXECUTABLE` bedeutet außerhalb des aktuellen HAProxy-Laufzeitbereichs.
- Alle Force-All-Zeilen bleiben in
  `reports/testing/generated/haproxy-runtime-results.generated.md` erhalten.
- Zusammenfassungen auf Root-Ebene bleiben connector-neutral.
- Es gibt keinen Generator für synthetische Matrizen.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Das frühere begrenzte
Sample ist deaktiviert, weil es `wait-for-body` statt eines echten
Host-Response-Streams verwendete.

## Kanonische Entscheidung für Phase 4

Der frühere begrenzte SPOA/SPOP-Response-Zweig ist deaktiviert, weil er
`wait-for-body` benötigte. Der gewählte Hostpfad besitzt keinen verdrahteten
nativen Response-Body-Callback; Response-Body-Verfügbarkeit, `phase4` und
`phase4_rule_evaluation` sind daher `not_implemented`. Auch die semantischen
Durchsetzungs- und Late-Intervention-Facetten sind `not_implemented`. Das
separate Profil `full-lifecycle-haproxy-htx` wählt einen HAProxy-3.2.21-
HTX-Overlay mit isolierter P1–P4-Transport-Evidence. Er nutzt geliehene
Chunks/EOS; sein einblockiger P2-403-Probe protokolliert null oder eine
beobachtete Upstream-Anfrage ohne deren Reihenfolge zu belegen. Das belegt kein
inkrementelles Request-Forwarding; P4-Safe wird als `log_only` aufgezeichnet. Er wird nicht
durch diesen SPOP-Pfad konfiguriert und stuft diese Zustände nicht hoch. Für Strict
gibt es keinen client-sichtbaren Abort-Nachweis.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered` und `phase4` | `not_implemented` | Vollständige native HAProxy-Response-Chunk-Transaktion in den gewählten Pfad verdrahten; niemals `wait-for-body` verwenden. |
| `phase4_rule_evaluation` | `not_implemented` | Benötigt einen echten ausgewählten End-of-Stream-Pfad und beobachtete Regel `1100301`. |
| `phase4_pre_commit_deny` | `not_implemented` | Aktuelle Felder sind policy-abgeleitet; kein Host-Runner erfasst sichtbaren Client-Status und Commit-Zeitpunkt. |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `not_implemented` | HTX-Safe-Source/Harness zeichnet `log_only` auf, aber es gibt kein client-validiertes spätes Ergebnis und keinen Strict-Abort. |
| `late_intervention_status_metadata` | `not_implemented` | Es gibt keinen hostbeobachteten ursprünglichen/sichtbaren Status mit Zeitpunkt; policy-abgeleitete Werte reichen nicht aus. |

Fehlt dieser Nachweis, wird `NOT_EXECUTED` und kein künstliches 403-`PASS`
gemeldet. Alle Nachweise enthalten ausschließlich Metadaten.
