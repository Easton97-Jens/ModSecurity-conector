# Entscheidungsmatrix für die Traefik-Abdeckung

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: `minimal_runtime_smoke` (nur der forwardAuth-Request-Pfad)
Laufzeitstatus: breiteres Connector-Verhalten ist nicht verifiziert

Diese Datei beschreibt nur den Traefik-spezifischen Status. Globale
Matrixregeln und Hochstufungsbedingungen stehen in
`connectors/_template/docs/coverage-decision-matrix.md` und
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Aktueller Traefik-Status

| Prüfstufe | Status | Nachweis |
| --- | --- | --- |
| Gerüst | OK | `connectors/traefik/README.md`, `connectors/traefik/TODO.md` |
| Herkunft/Metadaten | starter-present | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Kompilierung | link-verified-local | C17-Dienst mit Common Runtime lokal kompiliert und gelinkt |
| Selbsttest | pass-local | `make -C connectors/traefik self-test-decision-service` |
| Testumgebung | targeted-pass-local | echter Pfad Traefik -> forwardAuth -> Dienst mit 200/403 |
| No-CRS | not-run | Es wurde kein Traefik-Laufzeitbefehl ausgeführt. |
| Mit CRS | not-run | Es wurde kein Traefik-Laufzeitbefehl ausgeführt. |
| RESPONSE_BODY | not-verified | Es gibt keinen Laufzeitnachweis für eine Sperre. |
| Hochstufung | not allowed | Die Laufzeitbedingungen sind offen. |

## Gate-Checkliste

- [x] Scaffold-Dateien dokumentiert
- [x] Kein lokaler `connectors/traefik/tests`-Ordner
- [x] Herkunft des Repo-eigenen Starters dokumentiert
- [x] Repo-eigene Starter-Metadaten dokumentiert
- [x] Metadaten-Build-Starter-Nachweise dokumentiert
- [x] Build des Starters für den Entscheidungsdienst dokumentiert
- [x] Lokaler Selbsttest des Starters für den Entscheidungsdienst dokumentiert
- [ ] Herkunfts-/Lizenznachweis für produktives Traefik dokumentiert
- [ ] Produktions-Traefik-Baunachweise dokumentiert
- [x] Connector-eigener Harness implementiert und dokumentiert
- [ ] Kein CRS-Laufzeitbeweis dokumentiert
- [ ] Laufzeitnachweis mit CRS dokumentiert
- [ ] RESPONSE_BODY Sperrbeweise dokumentiert
- [x] Lokale gezielte Nachweise für negative und durchgelassene Fälle erzeugt
- [ ] Audit-/Protokollnachweise dokumentiert

## Phasenmatrix

| Phase / Prüfstufe | Traefik-Status | Entscheidung |
| --- | --- | --- |
| Phase 0 / Gerüst | OK | dem Gerüst entsprechend |
| Phase 1 / Herkunft und Metadaten | starter-present | produktive Herkunft ist weiter offen |
| Phase 2 / Kompilierung | link-verified-local | echtes Dienst-Artefakt gegen Common Runtime/libmodsecurity gelinkt |
| Phase 3 / Testumgebung | targeted-pass-local | echter Traefik-200/403-Pfad; persistierter CI-Nachweis steht noch aus |
| Phase 4 / No-CRS | not-run | keine Laufzeitbehauptung |
| Phase 5 / Mit CRS | not-run | keine CRS-Behauptung |
| Phase 6 / Abdeckungsmatrix | starter-documented | Laufzeitstatus getrennt halten |
| RESPONSE_BODY-Sperre | not-verified | keine Behauptung über eine Sperre |
| Negative/durchgelassene Fälle | pass-local | nur gezielter lokaler Nachweis |
| Audit-/Protokollnachweis | not-verified | keine Audit-/Protokollbehauptung |
| Hochstufung | not allowed | bleibt `not_verified` / `connector-gap` bis zu einem persistierten CI-Nachweis |

## Kanonische Entscheidung für Phase 4

Das gewählte Traefik-`forwardAuth`-Modell wird vor der Upstream-Antwort
ausgeführt. Seine Response-Body- und Late-Intervention-Facetten sind
Architekturgrenzen und keine ausstehenden Laufzeitaufgaben.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered`, `phase4` und `phase4_rule_evaluation` | `unsupported_by_host_model` | `UNSUPPORTED`: forwardAuth erhält keinen späteren Upstream-Response-Body. |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Es ist kein Commit-Zeitpunkt der Response-Phase verfügbar. |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `unsupported_by_host_model` | Keine spätere Upstream-Antwort erreicht forwardAuth. |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | In diesem Hostpfad gibt es keinen ursprünglichen/sichtbaren Upstream-Status und keine späte Aktion. |

Request-seitige 200/403- und `forwardBody`-Nachweise sind bewusst
ausgeschlossen. `UNSUPPORTED` zählt nie als `PASS`; Ereignisse und Berichte
bleiben metadatenbasiert.
