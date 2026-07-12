# lighttpd-Abdeckungsentscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch


Status: `minimal_runtime_smoke` / `partial_runtime_path`

Diese Matrix zeichnet nur die nativen Lighttpd-Connector-Beweise auf. Global
Promotion- und Response-Body-Gates bleiben im gesamten Repository definiert
Connector-Richtlinie.

## Aktueller Status

| Tor | Status | Beweis oder Grenze |
| --- | --- | --- |
| Ursprungs-/Quellenkarte | dokumentiert | `ORIGIN.md`, `SOURCE_MAP.json` |
| Gemeinsame SDK-Einführung | implementiert | Allgemeine Konfiguration, Mapper-Verträge, Laufzeit, Entscheidungen, Grenzwerte, Ereignisse |
| Lebenszyklus des nativen Moduls | implementiert | init/defaults/hooks/reset/cleanup in `module/mod_msconnector.c` |
| C17 kompilieren/verknüpfen | PASS | angepinnt lighttpd 1.4.84, PIC, gemeinsames Objekt, `-Werror` |
| Konfiguration/Modul laden | PASS | echt `lighttpd -tt` |
| Gepatchtes Kern-/Modulpaar | Build-/Ladepfad verfügbar | kopierter 1.4.84-Kern, passendes ABI-getaggtes Modul, Patch-/Artefaktmanifeste; keine Fähigkeitsförderung |
| Smoke-Test starten | PASS | echter Prozess, sauberer Stopp, keine Anfragen |
| Metadaten/Header anfordern | PASS, schmal | echte Basislinie 200 und regelgestützte 403 |
| Anforderungstext | gepatchter Quellvertrag, ungeprüft | Entliehene HTTP/1.1-Anforderungsbereiche sind nur im übereinstimmenden 1.4.84-ABI vorhanden. keine Fähigkeitsförderung |
| Antwortmetadaten/Header | UMGESETZT, NICHT BESTÄTIGT | Antwortstart-Hook vorhanden; noch keine echte Phase-3-Verhaltensbehauptung |
| Antworttext | gepatchter Identitätsquellenvertrag, nicht überprüft | entliehene HTTP/1.1-Entitätsbereiche vor dem Transfer-Framing; Kein Streaming-Host-Ergebnis oder Werbung |
| Entscheidungs-/Sperrstatus | PASS, Phase 1 | kanonische Regel `1100001`, HTTP 403 über `http_status_set_err()` |
| Veranstaltungen | PASS, schmal | JSONL-Connector/Regel-Metadaten; kein Körpernutzlastfeld |
| Transaktionsbereinigung | implementiert | Beenden/Zerstören und Bereinigen des Mapper-Speichers beim Zurücksetzen |
| No-CRS gezielter Smoke-Test | NICHT AUSGEFÜHRT | Der minimale 200/403-Laufzeitkern ist von der 53-Gehäuse-Basislinie getrennt |
| CRS | nicht ausgeführt / nicht beansprucht | kein nativer CRS-Beweis |
| Produktion/Sicherheit/vollständige Matrix | nicht beansprucht | breitere Verhärtung und Beweise fehlen |

## Gate-Checkliste

- [x] Angepinnte Lighttpd-Quelle, Binärdatei und generierter ABI-Header verfügbar.
- [x] Natives Modul und Host-Mapper vorhanden.
- [x] Build- und Bridge-Selbsttest sind getrennt.
- [x] Config Check lädt das reale Modul.
- [x] Smoke-Test starten sendet keine Anfragen.
- [x] Separater Laufzeitrauch durchquert Lighttpd und das Modul.
- [x] Baseline-Anfrage ist mit 200 zulässig.
- [x] Phase-1-Header-Regelblöcke mit 403.
- [x] Das Entscheidungsereignis enthält Konnektor- und Regelmetadaten.
- [x] Gepatchtes HTTP/1.1-Anfrage-/Entitäts-Callback-ABI mit geliehenen Bereichen und EOS.
- [ ] Streaming-Anfragetext/Phase-2-Hostnachweise.
- [ ] Response-Body/Phase-4-Laufzeit und Spätinterventionsnachweise.
- [ ] Verhaltensnachweise zum Umleiten/Löschen/Abbrechen.
- [ ] Native CRS-Beweise.
- [ ] Beweise für Stress, Belastbarkeit, Sicherheit und Produktionsverhärtung.

## Beförderungsentscheidung

Der Connector beansprucht möglicherweise nur `minimal_runtime_smoke` für den Narrow Native
Header-Pfad. Es darf keine Verifizierung des Antwortkörpers, keine CRS-Verifizierung oder
Sicherheitsüberprüfung, Produktionsbereitschaft oder Vollmatrixbereitschaft.

## Kanonische Phase-4-Entscheidung

Das Standardmodul verfügt über keinen Response-Body-Hook. Der von ausgewählter gepatchter Rückruf
Das separate Full-Lifecycle-Profil erhält die aktuelle HTTP/1.1-Identität
Entitätsbereich in `http_chunk.c` vor HTTP/1-Transfer-Framing, nicht Socket-Wire
Ausgabe. Es leiht sich die Bytes synchron aus, verfolgt den Offset und gibt EOS aus
am meisten einmal. Es bleibt keine Warteschlangenkopie erhalten. Es treten kurze Socket-Schreibvorgänge und `EAGAIN` auf
nach dem Rückruf und kann daher einen Anhang nicht strukturell duplizieren. Dies
ist nur ein Quell-/Build-Vertrag: Kein echter Streaming-Host-Lauf validiert ihn und
gzip/br, HTTP/2 und ungeprüfte Datei-/Zero-Copy-Routen sind ausgeschlossen.

| Facette | Deklarierter Zustand | Deckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered`, `phase4` und `phase4_rule_evaluation` | `not_implemented` | Der Quellpfad der Identitätsentität wird ohne ein echtes Streaming-Host-Ergebnis nicht hochgestuft. kein Anspruch auf Regelauswertung pro Chunk |
| `phase4_pre_commit_deny` | `not_implemented` | Es existiert keine vom Client validierte Precommit-Disposition |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `not_implemented` | sichere Quellenverhaltensdatensätze `log_only`; Beim strikten Abbruch fehlen für den Client sichtbare Beweise und es bleibt bestehen `NOT EXECUTED` |
| `late_intervention_status_metadata` | `not_implemented` | Kein Client-Artefakt trennt den ursprünglichen/angeforderten/sichtbaren Status und die tatsächliche Aktion nach der Zusage |

Phase-4-Zeilen lauten `NOT_EXECUTED` (oder werden bei der Funktionsauswahl weggelassen), nicht
`UNSUPPORTED`. Der vorhandene Header-Hook und die Phase-1-Deny sind getrennt;
Beweise bleiben nur Metadaten.
