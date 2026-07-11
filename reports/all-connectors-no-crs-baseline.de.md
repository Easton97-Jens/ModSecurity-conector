> Generierter Capability-Snapshot — Runtime-Status nicht manuell bearbeiten.

# No-CRS-Baseline für alle Connectoren

**Sprache:** [English](all-connectors-no-crs-baseline.md) | Deutsch

Am `2026-07-10` aus den eingecheckten Manifesten `connectors/<name>/capabilities.json` erzeugt. Es wurde kein kanonisches No-CRS-`result.json` verwendet, weil noch kein kanonischer Lauf ausgeführt wurde.

Kanonischer Gesamtstatus: `NOT EXECUTED`

| Connector | Build | Config | Start | Minimale Runtime | No-CRS-Baseline | P1 | P2 | P3 | P4 | Events | Lifecycle | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Apache | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| NGINX | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| HAProxy | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| Envoy | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | UNSUPPORTED | UNSUPPORTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| Traefik | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | UNSUPPORTED | UNSUPPORTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| lighttpd | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |

## Interpretation

`IMPLEMENTED, NOT ASSERTED` ist eine Source-/Capability-Aussage und kein
Runtime-PASS. `UNSUPPORTED` ist eine ehrliche Host-Modell-Grenze und wird
weder als PASS noch als FAIL gezählt. `NOT IMPLEMENTED` ist eine
Connector-Lücke. `NOT EXECUTED` bedeutet, dass kein kanonisches Ergebnis
vorliegt.

- Envoy-Phase 2 ist konfiguriert, aber nicht ausgeübt.
- Envoy und Traefik können im gewählten Autorisierungsmodell die spätere Upstream-Antwort nicht beobachten.
- Traefik-Phase 2 ist in der gewählten nativen Konfiguration nicht implementiert.
- lighttpd-Phase 3 ist implementiert, aber nicht verhaltensseitig belegt.
- lighttpd-Request- und -Response-Bodies sind nicht implementiert.
- Ältere Smoke-, Body-, CRS-, Bridge-, Sidecar- und Self-Test-Ergebnisse sind ausgeschlossen.

## Kanonische Phase-4-Facetten und Fallergebnisse

Die folgenden Werte sind Fähigkeitszustände und keine Ergebnisse des
fehlenden kanonischen Laufs. Sie trennen Antwortkörper-Verfügbarkeit,
Regelauswertung, Deny vor dem Commit, späte Intervention und Statusmetadaten,
anstatt jeden Phase-4-Treffer als sichtbaren HTTP-`403` zu behandeln.

| Connector | `response_body_buffered` | `phase4` | `phase4_rule_evaluation` | `phase4_pre_commit_deny` |
|---|---|---|---|---|
| Apache | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| NGINX | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| HAProxy | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| Envoy | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| Traefik | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| lighttpd | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |

| Connector | `late_intervention` | `late_intervention_log_only` | `late_intervention_abort` | `late_intervention_status_metadata` |
|---|---|---|---|---|
| Apache | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| NGINX | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| HAProxy | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| Envoy | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| Traefik | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| lighttpd | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |

`implemented_not_asserted` macht eine Fähigkeit für die fähigkeitsgesteuerte
Fallauswahl zulässig; daraus wird kein PASS. Ohne aktuellen Lauf besitzen
Apache, NGINX und HAProxy in dieser Übersicht kein Phase-4-PASS-Ergebnis. Der
ausgewählte SPOP-Pfad von HAProxy besitzt keine Response-Body-/Phase-4-/
Regelbeobachtungsfacetten. Seine optionale HTX-Observer-Quelle ist nicht
ausgewählt, nur bodylos und stuft die Capability-Tabelle nicht hoch; die
Phase-4- und semantischen Fälle sind `NOT_EXECUTED`, weil der Runner kein
hostbeobachtetes Client-Ergebnis, keinen Commit-Zeitpunkt und keinen
Hostpunkt nach dem Commit besitzt. Envoy und Traefik müssen
Antwortphasen-Fälle als `UNSUPPORTED` ausweisen: Ihre gewählten `ext_authz`-
und `forwardAuth`-Integrationen laufen vor der Upstream-Antwort und können
deren Körper nicht inspizieren. lighttpd-Antwortphasen-Fälle sind
`NOT EXECUTED` und nicht `UNSUPPORTED`, weil dem aktuellen nativen Modul die
Implementierung fehlt, ohne dass eine Unmöglichkeit durch das Hostmodell
belegt ist.

Die gemeinsamen Fälle sind `phase4_rule_observed`,
`phase4_deny_before_commit`, `phase4_deny_after_commit_log_only`,
`phase4_deny_after_commit_abort`, `phase4_event_contains_original_status` und
`phase4_event_contains_late_intervention_action`. Der veraltete Alias
`deny_response_body_marker_403` darf nur über den Deny-vor-dem-Commit-Fall PASS
werden; er darf kein Ergebnis reiner Protokollierung oder eines Abbruchs zu
einem `403`-PASS machen.

In einem echten Phase-4-Ergebnis ist `http_status` der von der WAF angeforderte
Status, `original_http_status` der Status vor der Intervention und
`visible_http_status` der für den Client sichtbare Status. Auch
`requested_action` und `actual_action` müssen getrennt bleiben.
`headers_sent`, `body_started`, `response_committed`, `late_intervention`,
`connection_aborted` und, soweit vorhanden, `transport_result` beschreiben
Zeitpunkt und Transport, ohne einen HTTP-Status zu erfinden. Eine sichere späte
Intervention kann daher mit sichtbarem `200` und `actual_action=log_only` PASS
sein; ein strikter Abbruch verlangt keinen sichtbaren `403`.

Die gemeinsame Richtlinie für späte Interventionen lautet: Vor dem Commit
`DENY_IF_POSSIBLE`; nach dem Commit im normalen oder sicheren Modus `LOG_ONLY`;
nach dem Commit im strikten Modus `ABORT_CONNECTION`. Ereignisse,
Fallergebnisse, Manifeste und Berichte dürfen nur Metadaten enthalten, niemals
Anfrage- oder Antwortkörperinhalte, Trefferwerte, Regelmeldungen oder
Interventionsprotokolle.

## Erwartete kanonische Evidence

Jeder Connector-Lauf schreibt nach
`$EVIDENCE_ROOT/<connector>/<run-id>/`. Das Aggregat darf ausschließlich die
sechs kanonischen `result.json`-Dateien lesen. Fehlende oder mehrdeutige Dateien
bleiben `NOT EXECUTED` oder führen zu einem Fehler; sie können nicht zu PASS
werden.

## Bewusst nicht erhobene Claims

- Production Readiness oder Production Hardening
- Runtime Security oder Security Verification
- CRS-Verifikation oder CRS-Vollständigkeit
- Extended-/Full-Matrix-Verifikation
- über alle Connectoren verifizierter Response Body
- alle Connectoren vollständig verifiziert
