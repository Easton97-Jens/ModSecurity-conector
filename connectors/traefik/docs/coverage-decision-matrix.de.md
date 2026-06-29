# Entscheidungsmatrix für die Traefik-Abdeckung

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: Entscheidungsdienststarter
Laufzeitstatus: nicht überprüft

Diese Datei zeichnet nur den Traefik-spezifischen Status auf. Globale Matrixregeln und
Promotion-Gates sind in definiert
`connectors/_template/docs/coverage-decision-matrix.md` und
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Aktueller Traefik-Status

| Gate | Status | Evidence |
| --- | --- | --- |
| Scaffold | OK | `connectors/traefik/README.md`, `connectors/traefik/TODO.md` |
| Origin/Metadata | starter-present | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Build | decision-service-starter | metadata and decision-service starter compile |
| Self-test | pass-local | `make -C connectors/traefik self-test-decision-service` |
| Harness | contract only | `connectors/traefik/harness/README.md` |
| No-CRS | not-run | No Traefik runtime command was run |
| With-CRS | not-run | No Traefik runtime command was run |
| RESPONSE_BODY | not-verified | No blocking runtime evidence exists |
| Promotion | not allowed | Runtime gates are open |

## Gate-Checkliste

- [x] Scaffold-Dateien dokumentiert
- [x] Kein lokaler `connectors/traefik/tests`-Ordner
- [x] Herkunft des Repo-eigenen Starters dokumentiert
- [x] Repo-eigene Starter-Metadaten dokumentiert
- [x] Metadaten-Build-Starter-Nachweise dokumentiert
- [x] Decision-Service-Starter-Build dokumentiert
- [x] Lokaler Selbsttest des Decision-Service-Starters dokumentiert
- [ ] Produktionstraefik origin/license Nachweis dokumentiert
- [ ] Produktions-Traefik-Baunachweise dokumentiert
- [ ] Harness implementiert und dokumentiert
- [ ] Kein CRS-Laufzeitbeweis dokumentiert
- [ ] With-CRS-Laufzeitnachweis dokumentiert
- [ ] RESPONSE_BODY Sperrbeweise dokumentiert
- [ ] Negative/pass-through Nachweise dokumentiert
- [ ] Audit/log Nachweise dokumentiert

## Phasenmatrix

| Phase / Gate | Traefik status | Decision |
| --- | --- | --- |
| Phase 0 / Scaffold | OK | scaffold-aligned |
| Phase 1 / Origin and metadata | starter-present | production origin remains open |
| Phase 2 / Build | decision-service-starter | local compile and self-test only |
| Phase 3 / Harness | contract only | do not claim runtime |
| Phase 4 / No-CRS | not-run | no runtime claim |
| Phase 5 / With-CRS | not-run | no CRS claim |
| Phase 6 / Coverage matrix | starter-documented | keep runtime statuses separate |
| RESPONSE_BODY blocking | not-verified | no blocking claim |
| Negative/pass-through | not-verified | no pass-through claim |
| Audit/log evidence | not-verified | no audit/log claim |
| Promotion | not allowed | remains decision-service-starter at most |
