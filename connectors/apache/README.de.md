**Sprache:** [English](README.md) | Deutsch

# Apache-Connector

Status: Apache-adaptereigene Common-SDK-Adoption für Konfiguration,
Direktiven, Mapper-Contracts und metadata-only Events.

Der Apache-Connector bettet jetzt `msconnector_config` für
connector-neutrale Konfigurationswerte ein, nutzt Common-Direktivennamen und
Common-Parser für die übernommenen Direktiven und stellt Apache-eigene dünne
Mapper von `request_rec` zu `msconnector_request` sowie von Apache-Response-
Metadaten zu `msconnector_response` bereit. Die Mapper validieren gegen die
Common `request_mapper_contract`- und `response_mapper_contract`-Modelle.

Apache-spezifisch bleiben `command_rec`-Registrierung, `request_rec`-Zugriff,
Hooks, Filter, APR-Pools, Bucket Brigades, APLOG-Logging, Apache-Return-Codes
und APXS/autotools-Buildlogik.

Phase-4-Ereignisse verwenden den Common `msconnector_event`-/JSONL-Pfad für
Metadaten. Request- und Response-Body-Payloads werden nicht in diese Events
oder Logs geschrieben.

Diese Änderung behauptet keine Produktionsreife, keine CRS-Abdeckung, keine
Full-Matrix-Abdeckung und keine neue Runtime-Verifikation.

## Kanonische Grenze für Phase 4

Apache verwendet einen nativen httpd-Ausgabefilterpfad, der den aktuellen
Bucket nur leiht, die aktuelle Brigade vor EOS weitergibt und Phase 4 bei EOS
finalisiert. Das ist inkrementelles Ingest mit End-of-Stream-Auswertung, keine
Regelauswertung pro Chunk. Das eingecheckte Manifest deklariert
`response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` jedoch bewusst als
`implemented_not_asserted`. Kein aktueller kanonischer Lauf über den echten
Host erhöht einen dieser Zustände.

`phase4_pre_commit_deny` ist bewusst `not_implemented`: Die Body-Entscheidung
fällt bei EOS nach dem Response-Header-Pfad, daher besitzt der native Host
keinen deterministischen, noch nicht festgeschriebenen Entscheidungspunkt für
den Antwortkörper. Ein Deny-Zweig im Quelltext rechtfertigt keinen behaupteten
sichtbaren Phase-4-HTTP-Statuswechsel.

Ein Phase-4-Regeltreffer ist kein Nachweis für ein beim Client sichtbares 403.
Ein kanonisches Ereignis muss `original_http_status`, den angeforderten
WAF-Status, `visible_http_status`, `requested_action`, `actual_action`,
Commit-Metadaten der Antwort und `connection_aborted` getrennt führen. Vor dem
Commit kann eine Sperre möglich sein; nach dem Commit darf die gemeinsame
Policy im sicheren Modus nur `log_only` protokollieren oder im strikten Modus
`abort_connection` auslösen. Keines dieser Ergebnisse darf ohne passenden
Host-Nachweis als erfolgreiche Sperre vor dem Commit gemeldet werden.

Die anwendbaren Fälle `phase4_rule_observed`,
`phase4_deny_after_commit_log_only`, `phase4_deny_after_commit_abort` sowie
die beiden Metadatenfälle bleiben nachweisgebunden.
`phase4_deny_before_commit` wird für dieses Hostmodell nicht ausgewählt.
Ereignisse enthalten nur Metadaten und niemals Response-Body-Payloads.
