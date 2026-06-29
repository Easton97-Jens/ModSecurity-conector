# lighttpd-Abdeckungsentscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: Brückenstarter
Laufzeitstatus: nicht überprüft

Diese Datei zeichnet nur den lighttpd-spezifischen Status auf. Die globale Matrix, Status
Vokabular, Promotion-Gates, No-CRS/With-CRS-Trennung, Laufzeitbeweis
Anforderungen und RESPONSE_BODY Mindestnachweise bleiben in definiert
`connectors/_template/docs/coverage-decision-matrix.md` und
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Aktueller Lighttpd-Status

| Gate | Status |
| --- | --- |
| Scaffold | OK |
| Origin/Metadata | bridge-starter documented |
| Metadata/probe build | PASS |
| Bridge-starter build | PASS |
| Bridge-starter self-test | PASS |
| Native lighttpd module | not implemented |
| FastCGI/SCGI implementation | not implemented |
| Adapter implementation | not implemented |
| Harness | contract only |
| No-CRS | not-run |
| With-CRS | not-run |
| RESPONSE_BODY | not-verified |
| Promotion | not allowed beyond bridge-starter/partial |

## Gate-Checkliste

- [x] Scaffold-Dokumentation ist vorhanden.
- [x] Es wird kein lokaler `connectors/lighttpd/tests`-Ordner verwendet.
- [x] Origin/license Status für aktuellen Repo-eigenen Brückenstarter vorhanden.
- [x] Quellkarte für den aktuellen Repo-eigenen Bridge-Starter ist vorhanden.
- [x] Für den Bridge-Starter-Status sind Metadaten vorhanden.
- [x] Metadata/probe Build-Starter-Nachweispfad vorhanden.
- [x] Bridge-Starter-Quelle existiert.
- [x] Bridge-Starter-Selbsttest vorhanden.
- [ ] lighttpd API/SDK/source ausgewählt.
- [ ] FastCGI/SCGI Protokolladapter existiert.
- [ ] Lighttpd-Adapter-Implementierung vorhanden.
- [ ] Nachweise für die Lighttpd-Laufzeitnutzung liegen vor.
- [ ] Kein CRS-Laufzeitnachweis vorhanden.
- [ ] With-CRS-Laufzeitnachweis vorhanden.
- [ ] RESPONSE_BODY Sperrbeweis vorhanden.
- [ ] Negative/pass-through Nachweise liegen vor.
- [ ] Audit/log Nachweise liegen vor.

## Phasenmatrix

| Phase / Gate | lighttpd status | Evidence |
| --- | --- | --- |
| Phase 0 Scaffold | OK | `connectors/lighttpd/` scaffold files |
| Phase 1 Origin/Metadata | bridge-starter documented | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Phase 2 Build | bridge-starter | `connectors/lighttpd/Makefile`, `build/build_starter.sh`, `build/bridge_starter.sh` |
| Phase 3 Harness | contract only | `connectors/lighttpd/harness/README.md` |
| Phase 4 No-CRS | not-run | no lighttpd runtime evidence |
| Phase 5 With-CRS | not-run | no lighttpd runtime evidence |
| Phase 6 Coverage Matrix | bridge-starter documented | this file references the global matrix |
| Phase 7 RESPONSE_BODY | not-verified | no lighttpd runtime evidence |
| Phase 8 Negative/pass-through | not-verified | no lighttpd runtime evidence |
| Phase 9 Audit/log | not-verified | no lighttpd runtime evidence |
| Phase 10 Promotion | not allowed beyond bridge-starter/partial | blocked by missing adapter and runtime evidence |
