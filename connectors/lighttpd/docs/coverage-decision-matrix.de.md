# lighttpd-Abdeckungsentscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: `minimal_runtime_smoke` / `partial_runtime_path`

Diese Matrix beschreibt ausschließlich den belegten nativen lighttpd-Pfad.
Die globalen Promotion- und Response-Body-Gates gelten weiterhin.

## Aktueller Status

| Gate | Status | Nachweis oder Grenze |
| --- | --- | --- |
| Origin/Source Map | dokumentiert | `ORIGIN.md`, `SOURCE_MAP.json` |
| Common-SDK-Anbindung | implementiert | Config, Mapper-Verträge, Runtime, Decisions, Limits, Events |
| Nativer Modul-Lifecycle | implementiert | Init, Defaults, Hooks, Reset und Cleanup |
| C17 Compile/Link | PASS | lighttpd 1.4.84, PIC, Shared Object, `-Werror` |
| Config-/Modul-Load | PASS | echtes `lighttpd -tt` |
| Start-Smoke | PASS | echter Prozess, sauberer Stop, null Requests |
| Request-Metadaten/Header | enger PASS | echte 200-Baseline und regelbasierte 403 |
| Request-Body | nicht unterstützt / nicht verifiziert | kein Body wird gemappt |
| Response-Metadaten/Header | im Smoke ausgeführt | Response-Start-Hook und Common-Verarbeitung |
| Response-Body | nicht unterstützt / nicht verifiziert | kein Body-Hook und keine Payload |
| Decision/Blockstatus | Phase-1-PASS | Regel `1000001`, HTTP 403 über `http_status_set_err()` |
| Events | enger PASS | JSONL mit Connector/Regel-ID, ohne Body-Payload-Feld |
| Transaction-Cleanup | implementiert | Finish/Destroy und Mapper-Cleanup beim Reset |
| Targeted No-CRS-Smoke | PASS | nur gezielte Repo-Regel, kein CRS |
| CRS | nicht ausgeführt / nicht behauptet | kein nativer CRS-Nachweis |
| Produktion/Security/Full Matrix | nicht behauptet | Härtung und breite Nachweise fehlen |

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
Nicht zulässig sind Claims zu Response Body, CRS, Security-Verifikation,
Produktionsreife oder Full Matrix.
