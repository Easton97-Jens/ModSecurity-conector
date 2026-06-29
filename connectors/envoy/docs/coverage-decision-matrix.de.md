# Envoy-Coverage-Entscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: Brückenstarter
Laufzeitstatus: nicht überprüft

Diese Envoy-Matrix hat nur einen Connector-spezifischen Status. Globale Matrixsemantik,
Statusvokabular und Promotion-Gates sind in definiert
`connectors/_template/docs/coverage-decision-matrix.md` und
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Aktueller Envoynstatus

| Gate | Status |
| --- | --- |
| Scaffold | OK |
| Origin/Metadata | bridge-starter metadata present |
| Build | bridge-starter PASS |
| CLI self-test | PASS |
| Harness | Envoy runtime harness missing |
| No-CRS | not-run |
| With-CRS | not-run |
| RESPONSE_BODY | not-verified |
| Promotion | not allowed beyond bridge-starter |

## Gate-Checkliste

- [x] Connector-Gerüst vorhanden.
- [x] Es wird kein lokaler `connectors/envoy/tests`-Ordner verwendet.
- [x] Framework-eigene Testpfade werden referenziert.
- [x] Origin/source-map Nachweise belegen, dass es keine vorgelagerte Envoy-Quelle gab
      importiert.
- [x] Bridge-Starter-Quelle existiert.
- [x] Bridge-Starter-Build existiert.
- [x] Bridge CLI Selbsttest existiert und besteht.
- [ ] Envoy SDK/API Abhängigkeit existiert.
- [ ] Nachweise für den Aufbau der libmodsecurity-Brücke liegen vor.
- [ ] Es liegen Nachweise für den Laufzeitkabelbaum des Produktionsadapters vor.
- [ ] Kein CRS-Laufzeitnachweis vorhanden.
- [ ] With-CRS-Laufzeitnachweis vorhanden.
- [ ] CRS loaded/effective Nachweise liegen vor.
- [ ] RESPONSE_BODY Sperrbeweis vorhanden.

## Phasenmatrix

| Phase | Envoy status | Evidence |
| --- | --- | --- |
| Phase 0 Scaffold | OK | `connectors/envoy/` scaffold files |
| Phase 1 Origin/Metadata | bridge-starter | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Phase 2 Build | bridge-starter PASS | `make -C connectors/envoy build-starter` |
| Phase 3 Bridge Self-Test | PASS | `make -C connectors/envoy self-test` |
| Phase 4 ModSecurity Bridge | blocked | libmodsecurity headers/libs not found in checked `/src` paths |
| Phase 5 Envoy Harness | missing | `connectors/envoy/harness/README.md` |
| Phase 6 No-CRS Runtime | not-run | no Envoy runtime run |
| Phase 7 With-CRS Runtime | not-run | no Envoy runtime run |
| Phase 8 CRS Evidence | not-verified | no Envoy With-CRS run |
| Phase 9 RESPONSE_BODY | not-verified | no runtime evidence |
| Phase 10 Negative/pass-through | not-verified | local self-test only |
| Phase 11 Audit/log | not-verified | no runtime evidence |
| Phase 12 Promotion | not allowed beyond bridge-starter | runtime gates are open |
