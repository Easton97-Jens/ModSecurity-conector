# Traefik-Abdeckungsentscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch


Status: minimal_runtime_smoke (nur ForwardAuth-Anfragepfad)
Laufzeitstatus: Verhalten des breiteren Connectors nicht überprüft

Diese Datei zeichnet nur den Traefik-spezifischen Status auf. Globale Matrixregeln und
Promotion-Gates sind in definiert
`connectors/_template/docs/coverage-decision-matrix.md` und
`reports/archive/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Aktueller Traefik-Status

| Tor | Status | Beweise |
| --- | --- | --- |
| Gerüst | OK | `connectors/traefik/README.md`, `connectors/traefik/TODO.md` |
| Herkunft/Metadaten | Starter-Geschenk | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Bauen | Link-verifiziert-lokal | C17 Common-Runtime-Backed-Service-Kompilierungs-/Link-Ziel |
| Selbsttest | pass-local | `make -C connectors/traefik self-test-decision-service` |
| Harness | target-pass-local | real Traefik -> ForwardAuth -> Service 200/403 Pfad |
| Kein CRS | nicht ausgeführt | Es wurde kein Traefik-Laufzeitbefehl ausgeführt |
| Mit-CRS | nicht ausgeführt | Es wurde kein Traefik-Laufzeitbefehl ausgeführt |
| RESPONSE_BODY | `unsupported_by_host_model` | ForwardAuth empfängt den späteren Upstream-Antworttext nicht |
| Werbung | nicht erlaubt | Laufzeittore sind geöffnet |

## Gate-Checkliste

- [x] Scaffold-Dateien dokumentiert
- [x] Kein lokaler `connectors/traefik/tests`-Ordner
- [x] Herkunft des Repo-eigenen Starters dokumentiert
- [x] Repo-eigene Starter-Metadaten dokumentiert
- [x] Metadaten-Build-Starter-Beweise dokumentiert
- [x] Decision-Service-Starter-Build dokumentiert
- [x] Lokaler Selbsttest des Decision-Service-Starters dokumentiert
- [ ] Produktions-Traefik-Ursprungs-/Lizenznachweis dokumentiert
- [ ] Produktions-Traefik-Baunachweise dokumentiert
- [x] Connector-eigener Harness implementiert und dokumentiert
- [ ] Kein CRS-Laufzeitbeweis dokumentiert
- [ ] With-CRS-Laufzeitnachweis dokumentiert
- [ ] RESPONSE_BODY-Blockierungsbeweis dokumentiert
- [x] Lokale gezielte Negativ-/Pass-Through-Beweise wurden erstellt
- [ ] Audit-/Protokollnachweise dokumentiert

## Phasenmatrix

| Phase/Gate | Traefik-Status | Entscheidung |
| --- | --- | --- |
| Phase 0 / Gerüst | OK | Gerüstausgerichtet |
| Phase 1 / Herkunft und Metadaten | Starter-Geschenk | Produktionsherkunft bleibt offen |
| Phase 2 / Bauen | Link-verifiziert-lokal | echte Service-Artefakt-Links zu Common runtime/libmodsecurity |
| Phase 3 / Harness | target-pass-local | echter Traefik 200/403-Pfad; Einbehaltene CI-Beweise sind noch offen |
| Phase 4 / Kein CRS | nicht ausgeführt | kein Laufzeitanspruch |
| Phase 5 / Mit-CRS | nicht ausgeführt | kein CRS-Anspruch |
| Phase 6 / Abdeckungsmatrix | starterdokumentiert | Laufzeitstatus getrennt halten |
| RESPONSE_BODY-Blockierung | nicht verifiziert | kein Sperranspruch |
| Negativ/Durchgang | pass-local | nur gezielte lokale Beweise |
| Audit-/Protokollnachweise | nicht verifiziert | kein Audit-/Protokollanspruch |
| Werbung | nicht erlaubt | bleibt not_verified / Connector-Gap, bis die CI-Beweise aufbewahrt werden |

## Kanonische Phase-4-Entscheidung

Das ausgewählte Traefik `forwardAuth`-Modell wird vor der Upstream-Antwort ausgeführt.
Seine Reaktionskörper- und Spätinterventionsaspekte sind Architekturgrenzen, nicht
ausstehende Laufzeitarbeiten.

| Facette | Deklarierter Zustand | Deckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered`, `phase4` und `phase4_rule_evaluation` | `unsupported_by_host_model` | `UNSUPPORTED`: ForwardAuth erhält keinen späteren Upstream-Antworttext |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Es wird kein Commitment-Punkt für die Reaktionsphase angezeigt |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `unsupported_by_host_model` | Keine spätere Upstream-Antwort erreicht forwardAuth |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | In diesem Hostpfad ist kein ursprünglicher/sichtbarer Upstream-Antwortstatus oder eine verspätete Aktion vorhanden |

Antragsseitige 200/403- und `forwardBody`-Beweise werden bewusst ausgeschlossen.
`UNSUPPORTED` zählt nie als `PASS`; Ereignisse und Berichte bleiben nur Metadaten.
