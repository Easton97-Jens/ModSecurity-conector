> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Erkenntnisse

**Sprache:** [English](findings.md) | Deutsch

Alle unten aufgeführten Erkenntnisse basieren auf Dateien, Pfaden, Befehlen oder lokalen `/src`
In diesem Repository überprüfte Laufzeitergebnisse.

## Repository- und Framework-Status

- Pfad des übergeordneten Repositorys: `<repository-root>`.
- Pfad des Framework-Submoduls: `modules/ModSecurity-test-Framework`.
- Basis-Commit des Framework-Submoduls:
  `b7f9bdc9831f9a8d14294cfb8fcb129a183d5d18`.
- Der Arbeitsbaum des Framework-Submoduls wird für die Erwartungsarbeit CRS geändert.
- Für diese Aufgabe wurden keine Apache- oder NGINX-Adapter-Quelldateien geändert.

## CRS Erwartungsänderung

- Testfallpfad:
  `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`.
- Grunderwartung bleibt No-CRS: erwartet 401.
- Die With-CRS-Erwartung ist jetzt variantenspezifisch:
  `expect.variants.with-crs.status: 403`.
- Framework-Runner-Pfade aktualisiert, um Variantenerwartungen zu erfüllen:
  `modules/ModSecurity-test-Framework/tests/runners/runner_core.py` und
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- Aktualisierte Framework-Dokumente:
  `modules/ModSecurity-test-Framework/tests/README.md` und
  `modules/ModSecurity-test-Framework/tests/runners/README.md`.

## Aktuelle Laufzeitergebnisse

| Command | Result | Evidence |
| --- | --- | --- |
| `make generate-test-matrix` | PASS | Generator exited 0; generated reporting is not runtime proof. |
| `make check-test-matrix` | FAIL | Exited 2 because generated reports intentionally differ from HEAD in this uncommitted HAProxy matrix update. |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Framework-local lint exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Framework-local matrix check exited 0 with a warning about missing `config/testing/import-status.json`. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS; NGINX 61 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |

Nachweisdateien:

- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/nginx-summary.txt`

## Aktionsstatus 401 Fall

- No-CRS Apache: `action_status_401_phase1_block` PASS, erwartet 401, tatsächlich
  401.
- Kein CRS NGINX: `action_status_401_phase1_block` PASS, erwartet 401, tatsächlich
  401.
- With-CRS Apache: `action_status_401_phase1_block` PASS, erwartet 403, tatsächlich
  403.
- With-CRS NGINX: `action_status_401_phase1_block` PASS, erwartet 403, tatsächlich
  403.

Ausführlicher Bericht:
`reports/archive/template-verification-nginx-apache/crs-action-status-401-analysis.md`.

## CRS Nachweise

- Framework `ci/lib/common.sh` pinnt CRS an `CRS_GIT_REF=v4.26.0`.
- Aktueller With-CRS-Lauf beobachtet CRS Quelle bei `/src/coreruleset`.
- Aktueller With-CRS-Lauf beobachtet CRS Präambel bei
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml`
  existiert.
- `crs_sqli_anomaly_block` PASS für Apache und NGINX im aktuellen With-CRS
  ausgeführt, erwartet 403 und tatsächlich 403.

## Vorlage

- `connectors/_template/README.md` dokumentiert jetzt einen wiederholbaren Connector-Flow,
  Erforderliche Nachweise, No-CRS/With-CRS Validierung, Abdeckungsmatrix, Promotion
  Tore und Ansprüche, die nicht geltend gemacht werden dürfen.
- `connectors/_template/TODO.md` ist in die Phasen 0 bis 7 unterteilt.
- `connectors/_template/docs/coverage-decision-matrix.md` trennt das Framework
  Fälle, No-CRS-Status, With-CRS-Status, Nachweispfad und Entscheidung.
- `connectors/_template/tests` fehlt. Ausführbare Vorlagentests sind nicht möglich
  Connector-lokal gepflegt.

## Externe Tests

- Framework-Testfälle sind unter `modules/ModSecurity-test-Framework/tests/cases/`.
- Konnektorspezifische Framework-Pfade finden Sie weiter unten
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`.
- NGINX-spezifische YAML-Dateien sind unter vorhanden
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- Apache-spezifische YAML-Dateien wurden unter nicht gefunden
`modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  dort wurde nur `README.md` gefunden.
- Neue Verbindungsgerüste dürfen keine lokalen `connectors/<name>/tests` erstellen
  Verzeichnisse.

## NGINX

- `connectors/nginx/` ist vorhanden und gehört dem Adapter.
- `connectors/nginx/tests` fehlt.
- Aktuelle `/src` NGINX gemeinsamer Smoke-Test bestanden: 54 PASS, 0 FAIL, 0 GESPERRT.
- Aktuelle `/src` NGINX No-CRS-Ziel erreicht: 60 PASS, 0 FAIL, 0 BLOCKIERT.
- Aktuelles `/src` NGINX With-CRS-Ziel übergeben: 61 PASS, 0 FAIL, 0 BLOCKIERT.
- `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` bleibt akzeptiert
  NGINX Build-Include-Vertrag.
- RESPONSE_BODY Blockierung bleibt für NGINX nicht verifiziert. Aktueller Antworttext
  Zeilen sind Pass-Through- oder Nur-Log-Nachweise.

## Apache

- `connectors/apache/` ist vorhanden und gehört dem Adapter.
- `connectors/apache/tests` fehlt.
- Aktueller `/src` Apache Common Smoke bestanden: 54 PASS, 0 FAIL, 0 BLOCKIERT.
- Aktuelles `/src` Apache No-CRS-Ziel übergeben: 54 PASS, 0 FAIL, 0 BLOCKIERT.
- Aktuelles `/src` Apache With-CRS-Ziel übergeben: 55 PASS, 0 FAIL, 0 BLOCKIERT.
- Apache-spezifische Framework-YAML-Dateien wurden nicht gefunden.
- RESPONSE_BODY Blockierung bleibt für Apache nicht verifiziert. `response_body_pass`
handelt es sich lediglich um Durchgangsbeweise.

## Entscheidungen

- `connectors/_template`: geeignetes Gerüst, nicht laufzeitverifiziert; nicht ein
  Produktive Connector-Implementierung.
- `connectors/apache`: abgestimmt auf aktuelle Template-Gates für Gerüst,
  origin/license, Metadaten, Build, Nutzung, externe Tests und ausgeführt
  No-CRS/With-CRS Geltungsbereich; Der Laufzeitstatus bleibt teilweise. Siehe
  `apache-template-alignment.md`.
- `connectors/nginx`: abgestimmt auf aktuelle Template-Gates für Gerüst,
  origin/license, Metadaten, Build, Nutzung, externe Tests und ausgeführt
  No-CRS/With-CRS Geltungsbereich; Der Laufzeitstatus bleibt teilweise. Siehe
  `nginx-template-alignment.md`.
- Kein CRS-Laufzeitnachweis: PASS für beide Konnektoren im aktuellen `/src`-Lauf.
- With-CRS-Laufzeitnachweis: PASS für beide Konnektoren im aktuellen `/src`-Lauf.
- CRS SQLi-Anomaliefall: PASS für beide Konnektoren.
- RESPONSE_BODY Blockierung: nicht überprüft.
- Vollständige Laufzeitüberprüfung: Nein.

## Envoy-Gerüstfund

- `connectors/envoy` existiert als sidecar/HTTP Bridge-Starter-Connector.
- Envoy folgt global/shared Connector Gates aus
  `reports/archive/template-verification-nginx-apache/connector-scaffold-decisions.md`
  und Verweise `connectors/_template/docs/coverage-decision-matrix.md` für
gemeinsame Matrixsemantik.
- Es existiert kein lokaler `connectors/envoy/tests`-Ordner.
- Keine Envoy-Laufzeitnachweise, produktive Quelle im Besitz des Adapters, Produktions-Build
  Nachweise oder die Implementierung des Harnesses werden dokumentiert.
- Der Envoy-Laufzeitstatus ist `not-verified`; Promotion über Brückenstarter hinaus
  ist ohne zukünftige Nachweise nicht zulässig.

## Envoy Build-Starter-Ergebnis

- Envoy hat `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h`, einen Einheimischen
  `Makefile`, `build/build_metadata.sh` und `src/envoy_bridge*` für lokal
  Bridge-Starter-Kompilierung.
- Der Brückenstarter verwendet `common/include/msconnector/request.h`,
  `intervention.h`, `status.h`, `origin.h` und `capabilities.h` sowie die
  entsprechende gemeinsame Hilfsquellen.
- Es wird kein echter Envoy API verwendet, da in keine Envoy SDK/API-Abhängigkeit vorhanden ist
  dieses Repository.
- ModSecurity Bridge, Envoy Runtime Harness, No-CRS, With-CRS und RESPONSE_BODY
  Validierung bleibt bestehen blocked/deferred.

## Envoy Build-Starter-Ergebnis

- `make -C connectors/envoy build-starter` für Bridge-Starter-Kompilierung bestanden.
- `make -C connectors/envoy self-test` für lokale allow/block Entscheidungslogik übergeben.
- Das Ergebnis verwendet Envoy API nicht und beweist nicht die Laufzeitkompatibilität.

## Envoyr-Brückenstarter-Fund

- Der ausgewählte Envoy-Pfad ist ein sidecar/HTTP Bridge-Starter, kein nativer Envoy
  Filter, ext_proc-Dienst oder Proxy-Wasm-Modul.
- Der lokale Bridge-Selbsttest kann Anforderungsheader und URI/query-Daten modellieren und
  Gibt einen 403 `msconnector_intervention` zurück.
- Der Selbsttest verwendet weder Envoy API, libmodsecurity API, CRS noch Framework
  YAML-Fälle.
## HAProxy

- Die HAProxy-Implementierung bleibt ein Starter, kein produktiver Adapter.
- Aktueller Status ist `spoa-agent-starter`; Laufzeitstatus ist
  `runtime-smoke-verified` für `haproxy_phase1_header_block` und
  `haproxy_crs_sqli_anomaly_block`.
- Der lokale SPOA-Agentenstarter kompiliert und testet die Synthese selbst
  Anfrage-Entscheidungslogik unter Verwendung gemeinsamer request/intervention/status-Datenformen.
- Der synthetische Starter enthält keine HAProxy-Header oder das Laden von CRS. Lebe
  HAProxy-erzwungene ModSecurity-Entscheidungsbeweise liegen nur durch die vor
  separater Laufzeit-Harness für `haproxy_phase1_header_block` und
  `haproxy_crs_sqli_anomaly_block`.
- Eine separate minimale Diagnose-Handshake-Teilmenge SPOP führt jetzt lokale Selbsttests durch
  HELLO/AGENT-HELLO, NOTIFY Argumentparsing, verifizierte Set-Var ACK Codierung,
  und DISCONNECT Handhabung. Es handelt sich nicht um eine vollständige SPOA-Agentenimplementierung.
- Framework `ci/provisioning/prepare-haproxy-runtime.sh` kann jetzt HAProxy `3.2.19` vorbereiten
  lokal unter `/src/ModSecurity-conector-build` nach Überprüfung durch den Beamten
Prüfsumme und `TARGET=linux-glibc` Unterstützung aus dem heruntergeladenen Quell-Makefile.
- `make smoke-haproxy` übergibt nun die bereichsbezogenen `haproxy_phase1_header_block` und
  `haproxy_crs_sqli_anomaly_block` Laufzeit führt Smoke-Tests aus und zeichnet Nachweise auf
  `/src/ModSecurity-conector-build/results/haproxy-summary.json`.
- `make runtime-matrix-haproxy` zeichnet eine HAProxy-Zeile pro vorhandenem Framework auf
  YAML Fall: 141 versuchte Zeilen, 1 PASS, 0 FAIL, 59 BLOCKED, 81
  NOT_EXECUTABLE und 10 MAPPED_ONLY Einträge. Der YAML PASS ist nur
  `crs_sqli_anomaly_block`.
- `make test-haproxy-no-crs` zeichnet die No-CRS-Aufteilung auf: 141 versucht YAML
  Zeilen, 0 YAML PASS, 0 FAIL, 59 BLOCKED, 82 NOT_EXECUTABLE und 10
  MAPPED_ONLY Einträge. Der `haproxy_phase1_header_block` Smoke-Test bleibt lebendig
  Diagnosealias und wird nicht in das Framework `phase1_header_block` hochgestuft
  YAML Fall.
- `make test-haproxy-with-crs` zeichnet die With-CRS-Aufteilung auf: 141 versucht YAML
  Zeilen, 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE und 10 MAPPED_ONLY
  Einträge.
- Die generierte SPOE-Konfiguration ist syntaxgültig durch `haproxy -c`; lokaler HAProxy
  SPOE/SPOP docs/source Überprüfen Sie den Set-Var-Aktionstyp 1, die Anzahl der Argumente 3 und die Transaktion
  Bereich 2 und bool true `0x11`.
- Der Live-Laufzeitbeweis zeichnet neue NOTIFY auf, fordert die Argumentextraktion an,
  libmodsecurity-Störungsstatus 403, set-var ACK, block-probe 403 und
  Pass-Probe 200.
- Der With-CRS-Unterbereich wird geladen
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`, sendet
  der SQLi URI aus `crs_sqli_anomaly_block`, zeichnet CRS Entscheidungsbeweise auf,
  und verifiziert Block-Probe 403 plus Pass-Probe 200.
- Der produktive Adapter-Build bleibt BLOCKED, da im Repository noch ein fehlt
  Vollständige SPOA-Implementierung und Live-PASS/FAIL-Ausführung für die aktuelle Version
  BLOCKED Framework-YAML-Zeilen.
- Es wird kein lokaler `connectors/haproxy/tests`-Ordner verwendet.
- RESPONSE_BODY Blockierung bleibt nicht verifiziert.
## lighttpd Bridge-Starter Finding

- `connectors/lighttpd` ist nur Bridge-Starter und der Laufzeitstatus ist
  nicht verifiziert.
- Repo-eigene metadata/probe-Quelle, Bridge-Starter-Quelle, `build/*.sh` und
  Lokale Make-Ziele stellen compile/self-test-Prüfungen mithilfe gemeinsam genutzter `common/` bereit.
  Helfer.
- `connectors/lighttpd/build/build_starter.sh`, `make -C connectors/lighttpd
  build-bridge-starter`, and `make -C connectors/lighttpd self-test-bridge`
  PASS beweisen nur lokalen Starter compilation/self-test; meldet die Brückensonde
  eine blockierte lokale Entscheidung.
- Die Lighttpd-Dokumente verweisen auf globale Connector-Gates, anstatt den Status zu kopieren
  Vokabular, Promotion-Gates, No-CRS/With-CRS-Trennung, Laufzeitbeweis
  Regeln und RESPONSE_BODY Anforderungen in Connector-spezifische Dokumente.
- Es ist kein lokaler `connectors/lighttpd/tests`-Ordner vorhanden oder erforderlich.
- Keine lighttpd API, FastCGI/SCGI Protokollimplementierung, ModSecurity API,
  Laufzeit-Harness, Laufzeit-Nachweis, Adapter-Implementierung oder Laufzeit
  PASS/FAIL/BLOCKED Anzahl wird beansprucht.
## Traefik Decision-Service Starter Finding

- `connectors/traefik` verfügt jetzt über einen Repo-eigenen lokalen Entscheidungsdienst-Starter.
- Die Traefik-Dokumente verweisen stattdessen auf gemeinsame Connector-Gates und Abdeckungsregeln
  globale Regeln lokal zu duplizieren.
- Traefik verfügt nur über lokale Selbsttestnachweise, keine implementierte Laufzeitumgebung, nein
  Produktions-Traefik-Adapter-Build und kein lokaler `connectors/traefik/tests`
  Ordner.
- Fehlende Produktionsabhängigkeiten umfassen einen ausgewählten Traefik API/source/SDK oder
  HTTP Bridge-Laufzeitstrategie, libmodsecurity-Laufzeitintegrationspunkt, Traefik
  Konfiguration und Nutzung von configuration/evidence Pfaden.

## Finden des Connector-Starter-Frameworks

- `modules/ModSecurity-test-Framework/ci/runtime/run-connector-starter-checks.sh`
  Bietet einen Framework-eigenen lokalen Runner für Envoy, HAProxy, lighttpd und
  Traefik-Starter build/self-test prüft.
- `make connector-starter-checks` schreibt `summary.json`, `results.jsonl` und
  pro-check stdout/stderr Protokolle unter
  `/src/ModSecurity-conector-build/results/connector-starters/`.
- Jeder `results.jsonl`-Eintrag zeichnet `test_type: connector-starter` auf,
`runtime_verified: false`, `runtime_status: not-verified`,
  `response_body_verified: false` und `installs_global_artifacts: false`.
- Der Framework-Runner ist kein server/proxy-Harness und weist kein No-CRS nach.
  With-CRS, CRS, RESPONSE_BODY, audit/log oder Runtime-Smokeverhalten.

## Neuer Connector Runtime-Smoke Finding

- Das Framework verfügt jetzt über Runtime-Smoke-Einstiegspunkte für Envoy, HAProxy, lighttpd,
  und Traefik.
- Die Envoy/HAProxy/lighttpd/Traefik-Harness-Ordner enthalten jetzt ausführbare Dateien
  `run_<name>_smoke.sh` Einstiegspunkte. HAProxy schreibt nun PASS-Nachweise nur für
  `haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`; Envoyr,
  lighttpd und Traefik schreiben noch BLOCKED diagnostische Nachweise mit
  `runtime_verified: false`.
- `smoke-new-connectors` darf blockierte Diagnosen nicht in PASS umwandeln;
  Da Envoy, lighttpd und Traefik weiterhin blockiert sind, bleibt der Gesamtstatus bestehen
  GESPERRT. HAProxy ist nur zur Laufzeit verifiziert
  `haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`; das Neue
  Der Connector-Satz ist nicht vollständig zur Laufzeit verifiziert.
- Alle Runtime-Smoke-Nachweispfade befinden sich unter `/src/ModSecurity-conector-build`.
