# lighttpd-Abdeckungsentscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: `minimal_runtime_smoke` / `partial_runtime_path`

Diese Matrix beschreibt ausschließlich den belegten nativen lighttpd-Pfad.
Die globalen Promotion- und Response-Body-Gates gelten weiterhin.

## Aktueller Status

| Prüfstufe | Status | Nachweis oder Grenze |
| --- | --- | --- |
| Herkunft/Quellkarte | dokumentiert | `ORIGIN.md`, `SOURCE_MAP.json` |
| Common-SDK-Anbindung | implementiert | Konfiguration, Mapper-Verträge, Laufzeit, Entscheidungen, Limits, Ereignisse |
| Nativer Modul-Lebenszyklus | implementiert | Initialisierung, Vorgaben, Hooks, Reset und Aufräumen |
| C17-Kompilierung/Linken | PASS | lighttpd 1.4.84, PIC, gemeinsames Objekt, `-Werror` |
| Konfigurations-/Modulladen | PASS | echtes `lighttpd -tt` |
| Gepatchtes Core/Modul-Paar | Build-/Ladepfad vorhanden | kopierter 1.4.84-Core, ABI-getaggtes passendes Modul, Patch-/Artefakt-Manifeste; keine Capability-Promotion |
| Start-Smoke | PASS | echter Prozess, sauberer Stop, null Requests |
| Request-Metadaten/Header | enger PASS | echte 200-Baseline und regelbasierte 403 |
| Request-Body | nicht implementiert / nicht verifiziert | kein Body wird gemappt |
| Response-Metadaten/Header | IMPLEMENTED, NOT ASSERTED | Response-Start-Hook vorhanden; noch keine echte verhaltensseitige Phase-3-Assertion |
| Response-Body | nicht implementiert / nicht verifiziert | kein Body-Hook und keine Payload |
| Entscheidung/Sperrstatus | Phase-1-PASS | kanonische Regel `1100001`, HTTP 403 über `http_status_set_err()` |
| Ereignisse | enger PASS | JSONL mit Connector/Regel-ID, ohne Body-Payload-Feld |
| Transaktions-Aufräumen | implementiert | Abschluss/Zerstörung und Mapper-Aufräumen beim Reset |
| Gezielter No-CRS-Smoke | NOT EXECUTED | der minimale 200/403-Laufzeitkern ist von der 53-Fall-Baseline getrennt |
| CRS | nicht ausgeführt / nicht behauptet | kein nativer CRS-Nachweis |
| Produktion/Sicherheit/vollständige Matrix | nicht behauptet | Härtung und breite Nachweise fehlen |

## Gate-Checkliste

- [x] Gepinnte lighttpd-Quelle, Binary und erzeugter ABI-Header vorhanden.
- [x] Natives Modul und Host-Mapper vorhanden.
- [x] Build und Bridge-Self-Test getrennt.
- [x] Config-Check lädt das echte Modul.
- [x] Start-Smoke sendet keine Requests.
- [x] Separater Runtime-Smoke durchläuft lighttpd und Modul.
- [x] Baseline-Request wird mit 200 erlaubt.
- [x] Phase-1-Headerregel blockiert mit 403.
- [x] Decision-Event enthält Connector- und Regelmetadaten.
- [ ] Request-Body-Mapping und Phase-2-Nachweis.
- [ ] Response-Body-Mapping, Phase 4 und Late Intervention.
- [ ] Redirect-, Drop- und Abort-Nachweise.
- [ ] Nativer CRS-Nachweis.
- [ ] Stress-, Resilienz-, Security- und Produktionshärtungsnachweise.

## Promotion-Entscheidung

Zulässig ist nur `minimal_runtime_smoke` für den engen nativen Headerpfad.
Nicht zulässig sind Aussagen zu Response-Body, CRS, Sicherheitsverifikation,
Produktionsreife oder vollständiger Matrix.

## Kanonische Entscheidung für Phase 4

Das native Modul besitzt bewusst keinen dekodierten Response-Body-Hook. Der
vom separaten Full-Lifecycle-Profil ausgewählte Callback des Patches sieht
HTTP/1.x-Wire-Output vor dem Socket-Write und bleibt deshalb für
Response-Body-Inspektion ein No-op. Diese Zustände sind
aktuelle Implementierungslücken des Moduls und keine Aussage über eine
grundsätzliche Unmöglichkeit im Host-Modell.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered`, `phase4` und `phase4_rule_evaluation` | `not_implemented` | Keine Response-Body-Daten erreichen ModSecurity. |
| `phase4_pre_commit_deny` | `not_implemented` | Im Modul gibt es keinen Phase-4-Zeitpunkt vor dem Commit. |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `not_implemented` | Es gibt keine Policy für Response-Bodies nach dem Commit. |
| `late_intervention_status_metadata` | `not_implemented` | Noch kein Phase-4-Ereignis kann ursprünglichen, angeforderten und sichtbaren Status sowie Aktionen trennen. |

Phase-4-Zeilen sind `NOT_EXECUTED` (oder werden durch die Capability-Auswahl
ausgelassen), nicht `UNSUPPORTED`. Der vorhandene Header-Hook und der
Phase-1-Deny sind getrennt; Nachweise bleiben metadatenbasiert.
