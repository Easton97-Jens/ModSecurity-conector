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
| Request-Body | gepatchter Source-Vertrag, nicht verifiziert | geliehene HTTP/1.1-Request-Ranges gibt es nur im passenden 1.4.84-ABI; keine Capability-Promotion |
| Response-Metadaten/Header | IMPLEMENTED, NOT ASSERTED | Response-Start-Hook vorhanden; noch keine echte verhaltensseitige Phase-3-Assertion |
| Response-Body | Identity-Source-Vertrag gepatcht, nicht verifiziert | geliehene HTTP/1.1-Entity-Ranges vor Transfer-Framing; kein Streaming-Hostresultat und keine Promotion |
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
- [x] Gepatchtes HTTP/1.1-Request-/Entity-Callback-ABI mit geliehenen Ranges und EOS.
- [ ] Streaming-Request-Body-/Phase-2-Hostnachweis.
- [ ] Response-Body-/Phase-4-Runtime- und Late-Intervention-Nachweis.
- [ ] Redirect-, Drop- und Abort-Nachweise.
- [ ] Nativer CRS-Nachweis.
- [ ] Stress-, Resilienz-, Security- und Produktionshärtungsnachweise.

## Promotion-Entscheidung

Zulässig ist nur `minimal_runtime_smoke` für den engen nativen Headerpfad.
Nicht zulässig sind Aussagen zu Response-Body, CRS, Sicherheitsverifikation,
Produktionsreife oder vollständiger Matrix.

## Kanonische Entscheidung für Phase 4

Das Stock-Modul besitzt keinen Response-Body-Hook. Der vom separaten
Full-Lifecycle-Profil ausgewählte Callback des Patches erhält in `http_chunk.c`
den aktuellen HTTP/1.1-Identity-Entity-Range vor HTTP/1-Transfer-Framing, nicht
Socket-Wire-Output. Er leiht die Bytes synchron aus, verfolgt den Offset und
sendet EOS höchstens einmal. Er behält keine Queue-Kopie; Socket-Short-Writes
und `EAGAIN` treten danach auf und können daher strukturell kein Append
duplizieren. Das ist nur ein Source-/Build-Vertrag: kein echter Streaming-
Hostlauf validiert ihn, und gzip/br, HTTP/2 sowie nicht untersuchte Datei- und
Zero-Copy-Routen sind ausgeschlossen.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered`, `phase4` und `phase4_rule_evaluation` | `not_implemented` | Identity-Entity-Sourcepfad ist ohne echten Streaming-Hostlauf nicht promotet; keine Behauptung einer Regelauswertung pro Chunk. |
| `phase4_pre_commit_deny` | `not_implemented` | Kein client-validiertes Precommit-Dispositionsergebnis. |
| `late_intervention`, `late_intervention_log_only` und `late_intervention_abort` | `not_implemented` | Safe-Sourceverhalten zeichnet `log_only` auf; Strict-Abort hat keine client-sichtbare Evidence und bleibt `NOT EXECUTED`. |
| `late_intervention_status_metadata` | `not_implemented` | Kein Clientartefakt trennt ursprünglichen, angeforderten, sichtbaren Status und tatsächliche Aktion nach dem Commit. |

Phase-4-Zeilen sind `NOT_EXECUTED` (oder werden durch die Capability-Auswahl
ausgelassen), nicht `UNSUPPORTED`. Der vorhandene Header-Hook und der
Phase-1-Deny sind getrennt; Nachweise bleiben metadatenbasiert.
