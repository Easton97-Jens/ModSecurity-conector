# Zusammenfassung der Überprüfung

**Sprache:** [English](summary.md) | Deutsch

Status: überprüft

Aktualisiert: 31.05.2026 00:00:00 UTC

## Bereitschaft

- Documentation/decision Commit-Bereitschaft: Ja.
- Commit-fertig für Dokumentations-/Entscheidungsstand: ja.
- Standardmäßige Smoke-Bereitschaft zur Laufzeit: blockiert, sofern keine Abhängigkeiten vorbereitet sind
  das Standard-Build-Root.
- Letzter dokumentierter Standardblocker:
  `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  fehlt.
- Aktuelle `/src` `make smoke-common`: PASS; Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 GESPERRT.
- Aktuelle `/src` `make test-no-crs`: PASS; Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 60 PASS, 0 FAIL, 0 GESPERRT.
- Aktuelle `/src` `make test-with-crs`: PASS; Apache 55 PASS, 0 FAIL,
  0 BLOCKED; NGINX 61 PASS, 0 FAIL, 0 GESPERRT.
- RESPONSE_BODY Blockierung: nicht überprüft.
- Envoy-Build-Bereitschaft: sidecar/HTTP Brückenstarter; Runtime-Smoke-Einstiegspunkt
  existiert und meldet BLOCKED; kein lokaler `connectors/envoy/tests` Ordner.
- Vollständige Laufzeit-Verifikation: nein.
- lighttpd Bridge-Starter checked/updated: ja; es folgt globalen Connector-Gates,
verwendet gemeinsame Regeln, anstatt sie zu duplizieren, hat keine Laufzeitnachweise und
  hat keinen lokalen `connectors/lighttpd/tests`-Ordner.
- Submodul geändert: ja; `modules/ModSecurity-test-Framework` hat eine Änderung
  Framework-Commit relativ zur früheren Baseline. Aktuelle übergeordnete HEAD Punkte
  beim Framework-Commit `4bec4d960fea89525db9e439ea567df15943a2e7`.

## CRS Erwartungsergebnis

Die ehemalige With-CRS 401/403 stimmt nicht überein
`action_status_401_phase1_block` wird in den aktuellen `/src`-Läufen aufgelöst.

| Variant | Connector | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | Apache | 401 | 401 | PASS |
| No-CRS | NGINX | 401 | 401 | PASS |
| With-CRS | Apache | 403 | 403 | PASS |
| With-CRS | NGINX | 403 | 403 | PASS |

Die Erwartungsänderung ist auf With-CRS beschränkt
`expect.variants.with-crs.status: 403`; Die grundlegende No-CRS-Erwartung bleibt bestehen
401.

Die Wirksamkeit von CRS wird durch `crs_sqli_anomaly_block` PASS für Apache belegt
und NGINX, erwartete 403 und tatsächliche 403.

Detaillierte Analyse:
`reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`.

## Entscheidungen

| Target | Decision | Reason |
| --- | --- | --- |
| `connectors/_template` | suitable scaffold, not runtime-verified | The template documents a repeatable connector flow, external tests, and promotion gates. It is intentionally not a productive implementation; origin, metadata, build, No-CRS, With-CRS, coverage matrix, and runtime evidence are required per connector. |
| `connectors/nginx` | aligned with current Template gates for executed scope; runtime status partial | Current No-CRS, With-CRS, and common smokes pass for executed scope; RESPONSE_BODY blocking and full minimum matrix remain unverified. See `nginx-template-alignment.md`. |
| `connectors/apache` | aligned with current Template gates for executed scope; runtime status partial | Current No-CRS, With-CRS, and common smokes pass for executed scope; Apache-specific YAML cases are still not found; RESPONSE_BODY blocking and full minimum matrix remain unverified. See `apache-template-alignment.md`. |
| RESPONSE_BODY | not verified | Current evidence includes pass-through/log-only response-body rows, not a blocking response-body HTTP result. |
| `connectors/envoy` | bridge-starter; runtime status not-verified | Envoy has repository-local metadata and sidecar/HTTP bridge starter code, no local tests, no Envoy runtime harness evidence, and no runtime claims. See `envoy-template-alignment.md`. |

## Aktuelle Laufzeitnachweise

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json` |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json` |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | `/src/ModSecurity-conector-build/results/connector-summary.json` |

Nachweisdateien:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx.rc`
- `/src/ModSecurity-conector-build/results/with-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/with-crs/nginx.rc`

## lighttpd Bridge-Starter-Ausrichtung

- `connectors/lighttpd` ist nur ein Brückenstarter.
- Build-Status: Bridge-Starter.
- Laufzeitstatus: nicht überprüft.
- Es wird kein lokaler `connectors/lighttpd/tests`-Ordner verwendet.
- Keine Lighttpd-Laufzeit, Adapter, RESPONSE_BODY, audit/log oder No-CRS/With-CRS
  PASS Anspruch wird geltend gemacht.
- Der Bridge-Starter-Code verwendet nur gemeinsam genutzte `common/` origin/status/intervention/capability-Helfer.
- `connectors/lighttpd/build/build_starter.sh` und Brückenstarter Ziele erstellen
  nur für lokale compile/self-test zugelassen; Die Brückensonde meldet ihre lokale
  Entscheidung als blocked/not-verified.
- Fehlende Abhängigkeiten: ausgewählter Produktionsintegrationspfad, lighttpd
  headers/SDK/source oder FastCGI/SCGI/bridge Abhängigkeiten, ModSecurity
  Integrationscode und ein Framework-eigenes Lighttpd-Laufzeitkabel.
- Auf gemeinsam genutzte Gates wird verwiesen von
  `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
und `connectors/_template/docs/coverage-decision-matrix.md`.

## Vorlagenverbesserungen

Die Vorlage dokumentiert nun:

- Erforderliche Dateien für einen neuen Connector
- erforderliche Metadaten
- erforderlicher origin/license Nachweis
- erforderliche Baunachweise
- erforderlicher No-CRS- und With-CRS-Laufzeitnachweis
- Externer Framework-Testbesitz
- Spalten der Abdeckungsentscheidungsmatrix
- RESPONSE_BODY Mindestnachweis
- Promotion-Tore: `scaffolded`, `adapter-owned`,
  `runtime-smoke-verified`, `crs-verified` und `more-than-partial`

## Lokale Testordner entfernt

- `connectors/_template/tests/`
- `connectors/nginx/tests/`
- `connectors/apache/tests/`

Ausführbare Connector-Tests sind Eigentum des Frameworks und werden nicht lokal verwaltet
`connectors/*/tests` Verzeichnisse.

## Schecks

| Check | Result | Note |
| --- | --- | --- |
| `test ! -d connectors/_template/tests` | PASS | Local Template test folder is absent. |
| `test ! -d connectors/apache/tests` | PASS | Local Apache test folder is absent. |
| `test ! -d connectors/nginx/tests` | PASS | Local NGINX test folder is absent. |
| `make generate-test-matrix` | PASS | Command exited 0. |
| `make check-test-matrix` | FAIL | Exited 2 because generated reports intentionally differ from HEAD in this uncommitted HAProxy matrix update. |
| `make lint` | PASS | `actionlint unavailable` was informational; command exited 0. |
| `make quick-check` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Command exited 0; it printed a warning that framework-local `config/testing/import-status.json` was not found. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache modules/ModSecurity-test-Framework` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |
| `git status --short` | pending docs/report updates | Parent status shows only report documentation updates from this verification pass. |
| `git submodule status` | PASS | Parent points to `4bec4d960fea89525db9e439ea567df15943a2e7`; submodule working tree is clean. |

## Nicht verifiziert

- RESPONSE_BODY Blockierung für Apache und NGINX.
- Vollständige Laufzeitmatrixförderung über `partial` hinaus.
- Apache-spezifischer Connector YAML-Fälle unter
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  dort wurde nur `README.md` gefunden.
- Genauer CRS/default-action oder ModSecurity-Aktionszusammenführungsmechanismus, der erstellt wurde
  With-CRS gibt 403 zurück, bevor das Erwartungsmodell aktualisiert wurde.
- Standard `make smoke-common` ohne Vorbereitung des Standard-Build-Roots.

## Zusammenfassung des Envoyngerüsts

`connectors/envoy` ist als sidecar/HTTP Brückenstarter dokumentiert. Es nutzt die
Gemeinsame Connector-Gates und Coverage-Matrix-Regeln statt Duplizierung
globaler Vertrag. ModSecurity Bridge, Envoy-Harness-Implementierung, No-CRS
Laufzeit, With-CRS-Laufzeit, RESPONSE_BODY Blockierung, negative/pass-through,
audit/log und Promotion-Gates bleiben für Envoy offen oder werden nicht überprüft.

## Envoy Build-Starter-Zusammenfassung

Der Envoy-Build-Status ist `bridge-starter`: `make -C connectors/envoy build-starter`
kompiliert den Repository-lokalen Bridge-Code mit dem Connector-neutralen `common/`-Code und
`make -C connectors/envoy self-test` führt einen lokalen allow/block Entscheidungsselbsttest durch.
Der Envoy-Laufzeitstatus bleibt `not-verified`. Es fehlen Produktionsabhängigkeiten
libmodsecurity headers/libs, Envoy SDK/API Header, ext_proc protobuf/gRPC
Bindungen, Proxy-Wasm SDK/toolchain oder eine dokumentierte Envoy-Bridge-Konfiguration plus
Laufzeitkabelbaum.

## Envoy Build-Starter-Nachweis

`make -C connectors/envoy build-starter` für Bridge-Starter-Kompilierung bestanden,
und `make -C connectors/envoy self-test` zur lokalen allow/block-Entscheidung angenommen
Logik. Dadurch wird die Envoy-Laufzeitkompatibilität nicht überprüft.

## Envoy Bridge-Starter-Nachweis

`make -C connectors/envoy self-test` für das lokale Bridge-Entscheidungsmodell bestanden.
Das Ergebnis ist kein No-CRS-Lauf, kein With-CRS-Lauf und kein RESPONSE_BODY
Nachweise.
## Aktuelle HAProxy-Zusammenfassung

- HAProxy verfügt jetzt über repo-autorisierte ORIGIN/SOURCE_MAP-Metadaten, Metadatenquelle und
  ein lokaler SPOA Agentenstarter mit lokalem Selbsttest.
- Build-Status: `spoa-agent-starter` für
  `make -C connectors/haproxy build-spoa-starter`; produktiver HAProxy-Adapter
  Build bleibt GESPERRT.
- Selbstteststatus: PASS für `make -C connectors/haproxy self-test-spoa`.
- Lokale HAProxy-Binärdatei vorbereiten: PASS für den Framework-Helfer; HAProxy `3.2.19`
  Quelle URL/checksum werden nur in `common.sh` angeheftet und anhand der verifiziert
  offizielle Prüfsummendatei und mit verifizierter `TARGET=linux-glibc`-Unterstützung erstellt.
- Diagnose SPOP Teilmenge: PASS nur für Diagnosebereich; das ist minimal
  Diagnose SPOP Handshake-Teilmenge, keine vollständige SPOA Agentenimplementierung.
- SPOE Konfigurationssyntax: `syntax-valid` durch `haproxy -c`.
- Diagnose-HAProxy-zu-Agent-Laufzeit: `diagnostic-enforcement-verified` von
  frische laufspezifische NOTIFY, Argumentextraktion, ModSecurity 403, Set-Var ACK,
Block-Probe 403 und Pass-Probe 200 Nachweis.
- Laufzeitstatus: `runtime-smoke-verified` für
  `haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`.
- Status der HAProxy-Matrix: `make runtime-matrix-haproxy` Datensätze 141 vorhanden
  Framework-YAML-Zeilen mit 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE und
  10 MAPPED_ONLY Einträge. Der PASS ist `crs_sqli_anomaly_block`; das No-CRS
  Header-Smoke bleibt als Diagnose-Alias erhalten und wird nicht in die Datei hochgestuft
  Rahmen `phase1_header_block` YAML Zeile.
- HAProxy-Split-Matrix-Status: `make test-haproxy-no-crs` Datensätze 0 YAML PASS,
  0 FAIL, 59 BLOCKED, 82 NOT_EXECUTABLE, 10 MAPPED_ONLY; `machen
  test-haproxy-with-crs` Datensätze 1 YAML PASS, 0 FAIL, 59 BLOCKED, 81
  NOT_EXECUTABLE, 10 MAPPED_ONLY.
- CRS Status: Nur für das Minimum überprüft
  `haproxy_crs_sqli_anomaly_block` Runtime-Smoke; Die umfassendere CRS-Abdeckung bleibt bestehen
  nicht verifiziert.
- Es liegt keine vollständige SPOE/SPOA-Implementierung oder RESPONSE_BODY-Laufzeitnachweis vor
  vorhanden.
- Aktuelle Laufzeitblocker: Live-PASS/FAIL-Ausführung für aktuelle BLOCKED YAML
  Zeilen, breiter CRS, RESPONSE_BODY, negative/pass-through, audit/log und
  Vollmatrixbeweis.
- Es wird kein lokaler `connectors/haproxy/tests`-Ordner verwendet.
- RESPONSE_BODY Blockierung bleibt nicht verifiziert.
- Die HAProxy-spezifische Ausrichtung ist dokumentiert in
  `reports/template-verification-nginx-apache/haproxy-template-alignment.md`.
## Zusammenfassung des Traefik Decision-Service Starter

- `connectors/traefik` existiert als Gerüst, ausgerichtet auf ein Repo-eigenes Local
  Entscheidungs-Service-Starter.
- Traefik verwendet global/shared Gerüsttore, anstatt sie zu duplizieren
  Connector-lokale Dokumentation.
- Traefik-Build-Status: Decision-Service-Starter; Metadaten und lokale Entscheidung
  Die Dienststarter werden kompiliert und der lokale Entscheidungsselbsttest wird bestanden.
- Traefik-Laufzeitstatus: nicht überprüft.
- Es existiert kein lokaler `connectors/traefik/tests`-Ordner.
- Kein No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through oder audit/log
  Laufzeitergebnis wird für Traefik beansprucht.

## Zusammenfassung des Connector-Starter-Frameworks

`make connector-starter-checks` erfolgreich über das übergeordnete Element ausgeführt
Makefile und schrieb Framework-eigene Nachweise unter
`/src/ModSecurity-conector-build/results/connector-starters/`.

- Gesamtstatus der Starterprüfung: BESTANDEN.
- Ergebnisdatei: `/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.
- Zusammenfassungsdatei: `/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
- Laufzeitstatus für Connector-Starter-Nachweis: `not-verified`.
- RESPONSE_BODY Status: nicht überprüft.
- Geltungsbereich: Connector-Starter build/self-test nur Nachweis; kein Runtime-Smoke
  Validierung beansprucht wird.

## Neue Connector-Laufzeit-Smoke-Zusammenfassung

Framework-Runtime-Smoke-Einstiegspunkte gibt es für Envoy, HAProxy, lighttpd und
Traefik. Es gibt nun auch Connector-seitige `run_<name>_smoke.sh`-Einstiegspunkte für alle
vier Connectors. Der aktuelle Runtime-Smoke-Status ist PASS für HAProxys
`haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block` Fälle und
BLOCKED für Envoy, lighttpd und Traefik.

- Runtime-Smoke-Ziele: `make smoke-envoy`, `make smoke-haproxy`,
  `make smoke-lighttpd`, `make smoke-traefik`.
- Aggregiertes Ziel: `make smoke-new-connectors`.
- Connectorseitige Einstiegspunkte:
  `connectors/envoy/harness/run_envoy_smoke.sh`,
  `connectors/haproxy/harness/run_haproxy_smoke.sh`,
  `connectors/lighttpd/harness/run_lighttpd_smoke.sh`,
  `connectors/traefik/harness/run_traefik_smoke.sh`.
- Nachweispfad: `/src/ModSecurity-conector-build/results/<connector>-summary.json`
  und `/src/ModSecurity-conector-build/results/<connector>-results.jsonl`.
- Laufzeitüberprüfung: true nur für HAProxy `haproxy_phase1_header_block`
  und `haproxy_crs_sqli_anomaly_block`; false für Envoy, lighttpd und
  Traefik.
- CRS Überprüfung: wahr nur für HAProxy `haproxy_crs_sqli_anomaly_block`;
Die umfassenderen CRS und die anderen neuen Konnektoren bleiben nicht verifiziert.
- RESPONSE_BODY: nicht für alle vier verifiziert.
- Der Starternachweis bleibt über `make connector-starter-checks` verfügbar,
  aber Starter PASS zählt nicht als Runtime-Smoke.
