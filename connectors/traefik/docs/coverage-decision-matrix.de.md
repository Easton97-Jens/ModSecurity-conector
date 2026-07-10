# Entscheidungsmatrix für die Traefik-Abdeckung

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: minimal_runtime_smoke (nur forwardAuth-Request-Pfad)
Laufzeitstatus: breiteres Connector-Verhalten nicht verifiziert

Diese Datei zeichnet nur den Traefik-spezifischen Status auf. Globale Matrixregeln und
Promotion-Gates sind in definiert
`connectors/_template/docs/coverage-decision-matrix.md` und
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Aktueller Traefik-Status

| Gate | Status | Evidence |
| --- | --- | --- |
| Scaffold | OK | `connectors/traefik/README.md`, `connectors/traefik/TODO.md` |
| Origin/Metadata | starter-present | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Build | link-verified-local | C17-Service mit Common Runtime lokal kompiliert und gelinkt |
| Self-test | pass-local | `make -C connectors/traefik self-test-decision-service` |
| Harness | targeted-pass-local | realer Traefik -> forwardAuth -> Service 200/403-Pfad |
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
- [x] Connector-eigener Harness implementiert und dokumentiert
- [ ] Kein CRS-Laufzeitbeweis dokumentiert
- [ ] With-CRS-Laufzeitnachweis dokumentiert
- [ ] RESPONSE_BODY Sperrbeweise dokumentiert
- [x] Lokale gezielte Negative-/Pass-through-Evidence erzeugt
- [ ] Audit/log Nachweise dokumentiert

## Phasenmatrix

| Phase / Gate | Traefik status | Decision |
| --- | --- | --- |
| Phase 0 / Scaffold | OK | scaffold-aligned |
| Phase 1 / Origin and metadata | starter-present | production origin remains open |
| Phase 2 / Build | link-verified-local | echtes Service-Artefakt gegen Common Runtime/libmodsecurity gelinkt |
| Phase 3 / Harness | targeted-pass-local | realer Traefik-200/403-Pfad; persistierte CI-Evidence noch offen |
| Phase 4 / No-CRS | not-run | no runtime claim |
| Phase 5 / With-CRS | not-run | no CRS claim |
| Phase 6 / Coverage matrix | starter-documented | keep runtime statuses separate |
| RESPONSE_BODY blocking | not-verified | no blocking claim |
| Negative/pass-through | pass-local | nur gezielte lokale Evidence |
| Audit/log evidence | not-verified | no audit/log claim |
| Promotion | not allowed | bleibt not_verified / connector-gap bis zu persistierter CI-Evidence |
