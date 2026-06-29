# NGINX Vorlagenausrichtung

**Sprache:** [English](nginx-template-alignment.md) | Deutsch

## Gesamtentscheidung

- Vorlagenausrichtung: ausgerichtet.
- Laufzeitstatus: teilweise.
- Ausgeführte Laufzeitgatter: runtime-smoke-verified für die aktuellen `/src`
  No-CRS/common-Bereich und CRS-verifiziert für den aktuellen `/src` With-CRS-Bereich.
- Grund: `connectors/nginx` stimmt mit dem aktuellen Template-Gerüst überein,
  origin/license, Metadaten, Build, Harness, externer Test, No-CRS und
  With-CRS-Gates für den ausgeführten Bereich. Es bleibt `partial` weil
  RESPONSE_BODY Blockierung und die vollständige Mindestmatrix werden nicht überprüft.

## Gate-Checkliste

- [x] Gerüststruktur vorhanden.
- [x] Origin/license Nachweise vorhanden.
- [x] Metadaten vorhanden.
- [x] Baubeweis vorhanden.
- [x] Harness-Vertrag vorhanden.
- [x] Kein lokaler `connectors/nginx/tests`-Ordner.
- [x] Referenzierte externe Framework-Tests.
- [x] No-CRS-Laufzeit PASS dokumentiert.
- [x] With-CRS-Laufzeit PASS dokumentiert.
- [ ] RESPONSE_BODY Blockierung überprüft.
- [ ] Vollständige Mindestmatrix überprüft.
- [ ] Der Connector kann über `partial` hinaus hochgestuft werden.

## Phasenmatrix

| Phase / Gate | Template requirement | NGINX evidence | No-CRS status | With-CRS status | Decision |
| --- | --- | --- | --- | --- | --- |
| Phase 0: Scaffold | README/TODO/docs/harness/src present | `connectors/nginx/README.md`, `TODO.md`, `docs/`, `harness/`, `src/` | n/a | n/a | OK |
| Phase 1: Origin/Metadata | ORIGIN, SOURCE_MAP, metadata present | `connectors/nginx/ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` | n/a | n/a | OK |
| Phase 2: Build | build command, include/lib paths, artifact evidence | `connectors/nginx/docs/build.md`, `connectors/nginx/config`, `/src/ModSecurity-conector-build/logs/nginx/`, `/src/ModSecurity-conector-build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so`; current build contract: `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` | n/a | n/a | OK for current `/src` evidence |
| Phase 3: Harness | connector harness present and documented | `connectors/nginx/harness/README.md`, `run_nginx_smoke.sh`, `nginx_smoke.conf` | n/a | n/a | OK |
| Phase 4: No-CRS Runtime | `make test-no-crs` PASS | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt`: 60 PASS, 0 FAIL, 0 BLOCKED | PASS | n/a | OK; runtime-smoke-verified for executed scope |
| Phase 5: With-CRS Runtime | `make test-with-crs` PASS and CRS evidence | `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt`: 61 PASS, 0 FAIL, 0 BLOCKED; `/src/coreruleset`; `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf` | n/a | PASS | OK; crs-verified for executed scope |
| Phase 6: Coverage Matrix | Phase 1/2/3/4 documented separately | `connectors/nginx/docs/coverage-decision-matrix.md` | PASS for executed rows | PASS for executed rows | partial unless complete |
| Phase 7: RESPONSE_BODY | blocking evidence required | `response_body_pass` is PASS/pass-through only; NGINX phase-4 connector-specific rows are pass-through/log-only evidence | not verified for blocking | not verified for blocking | not verified |
| Phase 8: Negative/pass-through | pass-through evidence required | `v2_transformation_url_decode_pass_no_match` PASS in current result files | PASS for executed row | PASS for executed row | partial until full matrix documented |
| Phase 9: Audit/log | audit/log evidence required | audit-log rows are present and PASS in current summaries; full audit/log evidence is not separately complete | PASS for executed rows | PASS for executed rows | partial |
| Phase 10: Promotion | full matrix required | current evidence excludes RESPONSE_BODY blocking and full minimum matrix | partial | partial | partial |

## Laufzeitnachweis

- `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common`: 54 PASS / 0 FAIL / 0 GESPERRT.
- `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs`: 60 PASS / 0 FAIL / 0 GESPERRT.
- `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs`: 61 PASS / 0 FAIL / 0 GESPERRT.
- Kein CRS `action_status_401_phase1_block`: erwartet 401, tatsächlich 401, PASS.
- With-CRS `action_status_401_phase1_block`: erwartet 403, tatsächlich 403, PASS.
- With-CRS `crs_sqli_anomaly_block`: erwartet 403, tatsächlich 403, PASS.
- `response_body_pass`: erwartet 200, tatsächlich 200, PASS; Nur Pass-Through, kein RESPONSE_BODY blockierender Nachweis.
- `response_header_basic`: erwartet 403, tatsächlich 403, PASS.
- `v2_transformation_url_decode_pass_no_match`: erwartet 200, tatsächlich 200, PASS.

Nachweisdateien:

- `/src/ModSecurity-conector-build/results/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl`

## Offene Tore

- RESPONSE_BODY Blockierung.
- Vollständige Mindestmatrix.
- Audit/log vollständige Nachweise über die ausgeführten Zeilen hinaus.
- Negative/pass-through vollständige Nachweise über die ausgeführten Zeilen hinaus.
- `nginx_phase4_strict_connection_abort` bleibt in aktuellen Berichten zurückgestellt
  weil für diesen Fall kein aktueller summary/result-Eintrag gefunden wurde.

Apache-spezifische YAML-Fälle sind kein NGINX-Gate.

## Entscheidung

NGINX ist auf die aktuelle Vorlage für Gerüst, Metadaten, Build abgestimmt.
Harness-, No-CRS- und With-CRS-ausgeführter Laufzeitbereich.

NGINX bleibt `partial`, da RESPONSE_BODY blockierend und das volle Minimum
Matrix sind nicht verifiziert.
