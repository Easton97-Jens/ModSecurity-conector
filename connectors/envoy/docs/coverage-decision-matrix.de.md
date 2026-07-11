# Envoy-Coverage-Entscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Connector-Metadaten: `minimal_runtime_smoke` / `connector-gap`

| Prüfstufe | Aktuelle Nachweisgrenze |
|---|---|
| Hostintegration | Connector-eigenes HTTP-`ext_authz`-Serviceprofil |
| Gemeinsames SDK | Echte dünne Mapper-Rückrufe plus Common-Runtime-Lebenszyklus |
| Konfiguration | `key=value`-Vorlage, konkrete Pfadersetzung, echtes Laden von Konfiguration und Regeln |
| Request-Header | Im echten Envoy-Hostpfad-Smoke begrenzt und gemappt |
| Request-Body | Gepufferter/begrenzter Pfad implementiert; kein hochgestufter Body-Fall |
| Response-Header | Vom gewählten HTTP-Autorisierungsprotokoll nicht unterstützt |
| Response-Body | Im gewählten Host-Modell nicht unterstützt; `response_body_verified=false` |
| Entscheidung | Common-Entscheidung auf ext_authz-Zulassen/Sperren gemappt; gezieltes 403 beobachtet |
| Ereignisse | Common-JSONL nur mit Metadaten beobachtet; keine Body-Payload |
| Kompilierung | C17-Kompilierung und Linken mit Warnungen als Fehler verifiziert |
| Konfigurationsprüfung | Mit lokaler libmodsecurity und gezielter Regel verifiziert |
| Start | Lokaler Start und Stopp des Dienstes ohne Request verifiziert |
| Minimale Laufzeit | Lokaler Envoy-200/403-Hostpfad-Smoke beobachtet |
| CRS/vollständige Matrix | Nicht verifiziert |
| Produktion/Sicherheit | Nicht verifiziert |

Der Laufzeitnachweis bleibt auf den gezielten lokalen Smoke begrenzt, bis
Root-CI, Framework-Nachweislayout und Repository-Berichte das neue
Connector-Binary verwenden. Daraus folgt keine breitere Metadaten-Hochstufung.

## Kanonische Entscheidung für Phase 4

Das ausgewählte Envoy-HTTP-`ext_authz`-Modell wird vor der Upstream-Antwort
ausgeführt. Die Response-Body- und Late-Intervention-Facetten sind deshalb
Architekturgrenzen und keine noch ausstehenden Laufzeitaufgaben.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered`, `phase4` und `phase4_rule_evaluation` | `unsupported_by_host_model` | `UNSUPPORTED`: ext_authz erhält keinen Upstream-Response-Body. |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Es ist kein Commit-Zeitpunkt der Response-Phase verfügbar. |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `unsupported_by_host_model` | Keine spätere Upstream-Antwort erreicht den Autorisierungsdienst. |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | In diesem Hostpfad gibt es keinen ursprünglichen/sichtbaren Upstream-Status und keine späte Aktion. |

Request-seitige 200/403-Nachweise sind für diese Zeilen bewusst ausgeschlossen.
`UNSUPPORTED` zählt nie als `PASS`; Ereignisse enthalten nur Metadaten.
