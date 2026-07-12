# Envoy-Coverage-Entscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch


Connector-Metadaten: `minimal_runtime_smoke` / `connector-gap`

| Tor | Aktuelle Evidenzgrenze |
|---|---|
| Host-Integration | Connectoreigenes HTTP-Dienstprofil `ext_authz` |
| Gemeinsames SDK | Echte Thin-Mapper-Rückrufe plus gemeinsamer Laufzeitlebenszyklus |
| Konfiguration | Schlüssel=Wert-Vorlage, konkrete Pfadersetzung, echtes Laden der Konfiguration/Regel |
| Anforderungsheader | Kartiert und begrenzt im echten Envoy-Host-Pfad-Smoke-Test |
| Anforderungstext | Gepufferter/begrenzter Pfad implementiert; Fall der gezielten Körperverletzung wird hier nicht beworben |
| Antwortheader | Wird vom ausgewählten HTTP-Autorisierungsprotokoll nicht unterstützt |
| Antworttext | Nicht unterstützt; `response_body_verified=false` |
| Entscheidung | Allgemeine Entscheidung, zugeordnet zu ext_authz erlauben/verweigern; gezielt 403 beobachtet |
| Veranstaltungen | Nur Metadaten. Gemeinsames JSONL-Ereignis beobachtet; keine Körpernutzlast |
| Bauen | C17-Kompilierung/Link mit Warnungen als Fehler überprüft |
| Konfigurationsprüfung | Verifiziert gegen lokale libmodsecurity- und Zielregeln |
| Start | Anforderungsfreier Dienststart/-stopp lokal verifiziert |
| Minimale Laufzeit | Local Envoy 200/403 Smoke-Test im Wirtsweg beobachtet |
| CRS/vollständige Matrix | Nicht verifiziert |
| Produktion/Sicherheit | Nicht verifiziert |

Der Laufzeitnachweis bleibt bis zum Root-CI auf den gezielten lokalen Smoke-Test beschränkt.
Framework-Beweislayout und Repository-Berichte nutzen den neuen Connector
binär. Dies rechtfertigt keine umfassendere Metadatenförderung.

## Kanonische Phase-4-Entscheidung

Das ausgewählte Envoy HTTP `ext_authz`-Modell wird vor der Upstream-Antwort ausgeführt.
Die Facetten „Response-Body“ und „Late-Intervention“ sind daher Architektur
Grenzen, keine ausstehende Laufzeitarbeit.

| Facette | Deklarierter Zustand | Deckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered`, `phase4` und `phase4_rule_evaluation` | `unsupported_by_host_model` | `UNSUPPORTED`: ext_authz empfängt keinen Upstream-Antworttext |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Es wird kein Commitment-Punkt für die Reaktionsphase angezeigt |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `unsupported_by_host_model` | keine spätere Upstream-Antwort erreicht den Autorisierungsdienst |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | In diesem Hostpfad ist kein ursprünglicher/sichtbarer Upstream-Antwortstatus oder eine verspätete Aktion vorhanden |

200/403-Beweise auf der Anfrageseite werden in diesen Zeilen bewusst ausgeschlossen.
`UNSUPPORTED` zählt nie als `PASS` und Ereignisse enthalten nur Metadaten.
