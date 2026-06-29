# Entscheidungen zum Connectorgerüst

**Sprache:** [English](connector-scaffold-decisions.md) | Deutsch

Status: überprüft

Diese Datei verwandelt die offenen Fragen aus `open-questions.md` in Repository-
unterstützte Gerüstregeln für zukünftige Connector. Entscheidungen beschränken sich auf Nachweise
in diesem Repository gefundene Informationen, das Framework-Modul oder tatsächlich ausgeführte Prüfungen.

## Commit-Bereitschaftsentscheidung

Frage: Verhindert die blockierte Standardeinstellung `make smoke-common` das Festschreiben?
Dokumentation und Scaffold-Entscheidungen?

Entscheidung: angenommen.

Grund: Die angeforderten letzten statischen Prüfungen wurden bestanden, lokale Connector-Testordner
bleiben abwesend und der standardmäßige Runtime-Smoke-Blocker ist als dokumentiert
Dies ist eher eine Umgebungsvoraussetzung als ein Dokumentationsfehler. Dies ist nicht der Fall
Fordern Sie eine Standardlaufzeit PASS oder eine vollständige Laufzeitüberprüfung an.

Evidence/paths:

- `reports/template-verification-nginx-apache/summary.md`
- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/findings.md`
- Tatsächlicher Framework-Pfad: `modules/ModSecurity-test-Framework`.
- Aktuelles Framework-Commit, auf das vom übergeordneten Element verwiesen wird:
  `4bec4d960fea89525db9e439ea567df15943a2e7`.
- Standardmäßige Runtime-Smoke-Bereitschaft: blockiert.
- Grund: `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
fehlen.
- `/src` Laufzeitnachweis: Apache und NGINX `phase1_header_block` PASS.
- Aktuelle `/src` gemeinsame Runtime-Nachweise:
  `reports/template-verification-nginx-apache/verified-runtime-run.md`
  zeichnet Apache 54 PASS und NGINX 54 PASS auf, beide mit 0 FAIL und 0 BLOCKED.
- Aktuelle `/src` NGINX Gesamtbeweise:
  `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx`
  zeichnet NGINX 60 PASS, 0 FAIL und 0 BLOCKIERT auf.
- Aktuelle `/src` No-CRS-Nachweis:
  `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs`
  zeichnet Apache 54 PASS und NGINX 60 PASS auf, beide mit 0 FAIL und 0 BLOCKED.
- Aktuelle `/src` With-CRS-Nachweis:
  `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs`
  zeichnet Apache 55 PASS und NGINX 61 PASS auf, beide mit 0 FAIL und 0 BLOCKED.
- Aktuelle With-CRS CRS Fallbeweise: `crs_sqli_anomaly_block` PASS für
  Apache und NGINX, erwarteter 403 und tatsächlicher 403.
- Framework-local `make lint`: PASS.
- Framework-local `make quick-check`: Ziel im Framework nicht gefunden
  Makefile.
- Framework-local `make check-test-matrix`: PASS, mit einer Warnung, dass
  Framework-Local `config/testing/import-status.json` wurde nicht gefunden.
- Historische NGINX 11 BLOCKED Zeilen werden in den aktuellen `/src` Wiederholungen aufgelöst
und als environment/docroot Berechtigungsblocker eingestuft.
- RESPONSE_BODY: nicht verifiziert.

Auswirkungen auf neue Konnektoren: Dokumentations- und Entscheidungsaktualisierungen können festgeschrieben werden
wenn Laufzeiteinschränkungen explizit dokumentiert sind. Laufzeitabschluss immer noch
erfordert separat aufgezeichnete Laufzeitnachweise.

Folgeänderung: Behalten Sie das Standardelement `make smoke-common` bis open/deferred bei
Das Standard-Build-Stammverzeichnis verfügt über einen gültigen ModSecurity v3-Quellbaum oder der Befehl lautet
mit explizit gültigen Laufzeitquellpfaden ausführen.

Commit-fertig für Dokumentations-/Entscheidungsstand: ja.

Vollständige Laufzeit-Verifikation: nein.

## Entscheidung über die Abdeckungsmatrix

Frage: Wie sollten generierte Abdeckungsberichte für Vorlage verwendet werden?
Apache und NGINX Gerüstentscheidungen?

Entscheidung: angenommen.

Grund: `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md` ist
Framework-eigene generierte Berichte und gibt ausdrücklich an, dass es sich nicht um Laufzeit handelt
Nachweis. Es zeichnet die Framework-Abdeckung, die Anzahl der Laufzeit-Snapshots und PASS/FAIL auf
dass `runtime_verified=true` 0 bleibt. Separate Abdeckungsentscheidungsmatrizen
Machen Sie diese Unterscheidung für Template, Apache und NGINX sichtbar.

Evidence/paths:

- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `connectors/apache/docs/coverage-decision-matrix.md`
- `connectors/nginx/docs/coverage-decision-matrix.md`

Auswirkungen auf neue Konnektoren: Neue Konnektordokumente müssen unterscheiden
`framework-covered` Fälle aus `runtime-smoke-verified` Connector-Verhalten.
Generierte PASS/FAIL-Snapshot-Zählungen können zitiert werden, fördern jedoch nicht a
Connector über `partial` hinaus.

Folgeänderung: Template-, Apache- und NGINX README/TODO-Dateien verlinken jetzt oder
siehe Anforderungen an die Deckungsentscheidungsmatrix. Apache und NGINX bleiben bestehen
`partial`; RESPONSE_BODY bleibt `not-verified`; mehr als `partial` erfordert
Vollständiger Matrixbeweis.

## Vorlage-Gerüst-Entscheidung

Frage: Soll `connectors/_template` als abgeschlossen ausgewertet werden?
Connector?

Entscheidung: Nur als Gerüst akzeptiert.

Grund: `connectors/_template` dokumentiert die erwartete Connector-Struktur,
Externe Framework-Testverantwortung, Statusvokabular und Promotion-Gates. Es
enthält bewusst keine produktive Connector-Implementierung, keine lokalen Tests,
und keine Runtime-Nachweise.

Evidence/paths:

- `connectors/_template/README.md`
- `connectors/_template/TODO.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `reports/template-verification-nginx-apache/template-evaluation.md`

Auswirkungen auf neue Konnektoren: origin/license Nachweis, Metadaten, Build-Nachweis,
No-CRS, With-CRS, Abdeckungsmatrix, RESPONSE_BODY-Blockierung und Laufzeitnachweise
werden pro Connector benötigt. Fehlende konkrete Connector-Nachweise liegen nicht vor
Vorlagendefekt.

Nachträgliche Änderung oder erforderliche Nachweise: konkrete Connectors müssen diese erfüllen
Tore, bevor sie über `partial` hinaus bewertet werden können.

## Testvariantenentscheidung

Frage: Wie sollen sich die Ziele `test-no-crs` und `test-with-crs` auswirken?
Verbindungsgerüst und Abdeckungsentscheidungen?

Entscheidung: Übernahme des Zielbesitzes und getrennter Berichterstattung.

Grund: Beide Ziele sind im übergeordneten `Makefile` vorhanden. `test-no-crs` und
`test-with-crs` wurde im aktuellen `/src`-Lauf für Apache und NGINX übergeben. Die
Durch den With-CRS-Lauf wurde auch der CRS SQLi-Anomaliefall für beide Konnektoren überprüft.

Evidence/paths:

- `Makefile`
- `modules/ModSecurity-test-Framework/README.md`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml`
- `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`

Auswirkungen auf neue Connectors: Neue Connector-Dokumente müssen No-CRS und With-CRS melden
separat. Ein CRS-spezifischer PASS kann nur für Fälle beantragt werden, die unter fallen
`test-with-crs`.

Nachträgliche Änderung oder erforderliche Nachweise: Volle Werbung über `partial` hinaus beibehalten
verschoben bis RESPONSE_BODY Blockierung und die vollständige Mindestmatrix vorliegen
dokumentiert.

## Entscheidung 1: Roadmap-Referenzen

Frage: Mehrere Connector-Dateien verweisen auf `docs/roadmap/todo-inventory.md`,
aber dieser Pfad wurde im übergeordneten Repository nicht gefunden.

Entscheidung: angenommen.

Grund: Der übergeordnete Pfad `docs/roadmap/todo-inventory.md` wurde nicht gefunden. Die
Framework-Pfad `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
existiert. Die Dokumentation zum übergeordneten Connector sollte die Datei „Repository-Valid“ verwenden
Framework-Pfad. Framework-interne Referenzen werden nicht geändert, wenn sie geändert werden
relativ zum Framework-Baum.

Evidence/paths:

- `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
- `connectors/apache/TODO.md`
- `connectors/nginx/TODO.md`
- `connectors/*/docs/build.md`
- `connectors/*/docs/architecture.md`
- `connectors/*/docs/public-sources.md`

Auswirkungen auf neue Konnektoren: Die Dokumentation neuer Konnektoren muss auf Folgendes verweisen
vorhandener Framework-Roadmap-Pfad, wenn auf das gemeinsame Roadmap-Inventar verwiesen wird.

Folgeänderung: Die Dokumentation des übergeordneten Connectors wurde auf das Framework aktualisiert
Pfad. Es wurde keine neue übergeordnete Roadmap-Datei erstellt.

## Entscheidung 2: Externe Testeigentümerschaft

Frage: Wie sollen zukünftige Konnektoren extern gepflegte Tests referenzieren?
ohne lokales Template oder Connector `tests` Ordner?

Entscheidung: angenommen.

Grund: Die lokalen Testordner `connectors/_template/tests`,
`connectors/apache/tests` und `connectors/nginx/tests` wurden entfernt. Die
Framework besitzt ausführbare YAML-Fälle und den von Apache und NGINX verwendeten Runner
Harnesses.

Evidence/paths:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `Makefile` Ziele: `smoke-apache`, `smoke-nginx`, `smoke-common`,
  `smoke-all`, `runtime-matrix-all`

Auswirkungen auf neue Connectors: Neue Connectors dürfen nicht hinzugefügt werden
`connectors/<name>/tests`. Sie müssen Framework-eigene Tests dokumentieren
Laufzeitziel, das sie ausführt.

Folgeänderung: In der Dokumentation zu Template, Apache und NGINX heißt es nun
Connector-Tests sind Framework-eigene Tests und nicht Connector-lokal.

## Entscheidung 3: Apache-spezifische YAML-Fälle

Frage: Sind nur Apache-YAML-Fälle unter dem Connector-spezifischen verfügbar
Framework-Pfad?

Entscheidung: verschoben.

Grund: Der Pfad existiert, aber dort wurde nur `README.md` gefunden. Kein Apache-only
YAML-Fälle wurden gefunden, und keiner ist hier erfunden.

Evidence/paths:

- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/README.md`
- `modules/ModSecurity-test-Framework/docs/testing/test-import-plan.md`

Auswirkungen auf neue Konnektoren: Apache-spezifische Ansprüche dürfen sich nicht auf Nichtexistente stützen
Nur Apache-YAML-Fälle. Sie können sich nur auf ausgeführte generische oder zukünftige Fälle verlassen
Apache-spezifische Fälle sind einmal vorhanden und werden ausgeführt.

Benötigte Nachweise: Apache-spezifische YAML-Falldateien unter dem Framework-Pfad plus
Laufzeitbefehlsausgabe, die das erwartete Ergebnis zeigt.

## Entscheidung 4: NGINX-spezifische YAML-Fälle

Frage: Sind NGINX-spezifische YAML-Fälle unter dem Connector-spezifischen verfügbar
Framework-Pfad?

Entscheidung: angenommen.

Grund: Der Connector-spezifische Framework-Pfad NGINX enthält README plus YAML
Fallakten.

Evidence/paths:

- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/*.yaml`

Auswirkungen auf neue Konnektoren: Konnektorspezifische YAML-Fälle gehören darunter
`modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
wenn sie existieren. NGINX kann auf den vorhandenen NGINX-spezifischen Pfad verweisen.

Folgeänderung: Apache/NGINX Validierungsdokumente unterscheiden bestehende NGINX YAML
Fälle aus fehlenden Apache-spezifischen YAML-Fällen.

## Entscheidung 5: Statusvokabular

Frage: README-Dateien beschreiben Apache/NGINX als Adapter-eigene Dateien, während einige Dokumente
Verwenden Sie weiterhin gerüstorientierte Statuswerte.

Entscheidung: angenommen.

Grund: Das Repository verwendet mehrere Statusbezeichnungen. Die Gerüstentscheidung muss getroffen werden
ein gemeinsames Vokabular, um zu vermeiden, dass Teilbeweise als vollständige Validierung dargestellt werden.

Evidence/paths:

- `connectors/_template/README.md`
- `connectors/apache/README.md`
- `connectors/nginx/README.md`
- `reports/template-verification-nginx-apache/nginx-evaluation.md`
- `reports/template-verification-nginx-apache/apache-evaluation.md`

Statusvokabular:

- `template`: generischer Ausgangspunkt, keine Implementierung.
- `scaffolded`: Struktur vorhanden, aber kein Repository-gestützter Adapter
Die Umsetzung ist nachgewiesen.
- `adapter-owned`: Produktiver Connector-Code lebt im Connector-Baum mit
  Herkunft und Metadaten.
- `runtime-smoke-verified`: nur bestimmte Smoke-Fälle mit aufgezeichnetem Befehl,
  Ergebnis und expliziter `verified_case`-Bereich werden überprüft; das bedeutet nicht
  CRS, RESPONSE_BODY oder Vollmatrixverifizierung.
- `crs-verified`: With-CRS-Ziel- oder Fallanspruch hat Befehl aufgezeichnet, CRS
  Nachweise und Ergebnis.
- `partial`: Struktur oder teilweiser Laufzeitnachweis vorhanden, aber vollständige Validierung
  ist nicht bewiesen.
- `not-verified`: Unzureichender Laufzeitnachweis.

Auswirkungen auf neue Konnektoren: Neue Dokumente müssen dieses Vokabular verwenden und dürfen kein a markieren
Der Connector ist allein aufgrund der Strukturprüfungen vollständig.

Folgeänderung: Vorlagen- und Validierungsdokumente wurden dadurch aktualisiert
Wortschatz.

## Entscheidung 6: RESPONSE_BODY Nachweise blockieren

Frage: Welche Nachweise sind erforderlich, bevor eine `RESPONSE_BODY`-Sperrung erfolgen kann?
als verifiziert behandelt?

Entscheidung: verschoben.

Grund: Repository-Nachweise deuten darauf hin, dass die Weitergabe des Antworttexts nicht der Fall ist
Überprüfung der Blockierung des Antworttexts und `RESPONSE_BODY` bleibt nicht hochgestuft.

Evidence/paths:

- `reports/testing/real-world-connector-validation.md`
- `modules/ModSecurity-test-Framework/docs/real-world-connector-validation.md`
- `modules/ModSecurity-test-Framework/docs/roadmap.md`
- `modules/ModSecurity-test-Framework/docs/testing/test-import-plan.md`

Auswirkungen auf neue Konnektoren: Kein Konnektor kann eine `RESPONSE_BODY`-Sperre beanspruchen
Unterstützung, bis die unten aufgeführten Mindestnachweise vorliegen.

Benötigte Nachweise:

- ein Repository-gestützter Laufzeittestfall im Framework
- erwarteter blockierender Response-Body-Trigger
- tatsächliches Sperrergebnis, z. B. HTTP 403
- log/report Nachweise
- ausgeführter Befehl
- betroffenen Connector
- Apache und NGINX werden separat dokumentiert, wenn ein gemeinsamer Anspruch geltend gemacht wird

## Entscheidung 7: NGINX Bauvertrag einschließen

Frage: Sollen `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` bestehen bleiben?
der aktuelle NGINX Bauvertrag?

Entscheidung: angenommen.

Grund: `connectors/nginx/config` verwendet `MSCONNECTOR_COMMON_INC`. Die
Aktuelle Framework-Vorbereitungsskriptdurchläufe
`MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` und das Postfix NGINX
Smoke-Test bestand `phase1_header_block` mit HTTP 403.

Evidence/paths:

- `connectors/nginx/config`
- `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh`
- `reports/template-verification-nginx-apache/nginx-build-fail-analysis.md`
- `/src/ModSecurity-conector-build/logs/nginx/commands.txt`
- `/src/ModSecurity-conector-build/logs/nginx/nginx-make.log`

Auswirkungen auf neue Konnektoren: NGINX Build-Dokumentation kann diese Umgebung behandeln
Variable als aktuell unterstützter Common-Header-Include-Vertrag.

Folgeänderung: In der Dokumentation wird diese als aktueller Vertrag vermerkt.

## Entscheidung 8: Materialisiertes `common/include`-Layout

Frage: Sollten materialisierte Build-Bäume einen generierten `common/include` tragen?
Layout statt `MSCONNECTOR_COMMON_INC` übergeben?

Entscheidung: verschoben.

Grund: Der aktuell akzeptierte Bauvertrag besteht `MSCONNECTOR_COMMON_INC` und
hat vorübergehende Smoke-Spuren. Keine Repository-Datei beweist ein generiertes gemeinsames Layout
Vertrag für materialisierte Verbindungsbäume.

Evidence/paths:

- `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh`
- `reports/template-verification-nginx-apache/nginx-build-fail-analysis.md`

Auswirkungen auf neue Konnektoren: Erfinden Sie kein materialisiertes gemeinsames Include-Layout.
Verwenden Sie einen expliziten, dokumentierten Include-Vertrag, bis eine zukünftige Implementierung erfolgt
bewiesen.

Erforderliche Nachweise: ein implementierter Materialisierungsvertrag, generierter Pfad
Nachweise, Compilerzeilen, die diesen Pfad verwenden, und Runtime-Smoke-Ergebnisse.

## Entscheidung 9: Breitere Laufzeitmatrix

Frage: Welche Laufzeitmatrix ist erforderlich, bevor Apache oder NGINX sein können
als mehr als teilweise vollständig behandelt?

Entscheidung: verschoben.

Grund: Der aktuelle gemeinsame Laufzeitlauf `/src` liefert nur teilweise Nachweise.
Apache hat 54 PASS und 0 BLOCKED in der endgültigen gemeinsamen Zusammenfassung, und NGINX hat
54 PASS und 0 BLOCKED in der abschließenden gemeinsamen Zusammenfassung. Das aktuelle No-CRS-Ziel
für Apache und NGINX übergeben, und das aktuelle With-CRS-Ziel wurde ebenfalls übergeben
Apache und NGINX. Diese Läufe verbessern den dokumentierten Laufzeitstatus, aber
RESPONSE_BODY Blockierung wird nicht überprüft und generierte Berichte sind nicht zur Laufzeit verfügbar
PASS Nachweis.

Evidence/paths:

- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/nginx-docroot-permission-analysis.md`
- `reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`
- `reports/template-verification-nginx-apache/summary.md`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `modules/ModSecurity-test-Framework/docs/testing/test-import-plan.md`
- `reports/testing/generated/apache-runtime-results.generated.md`
- `reports/testing/generated/nginx-runtime-results.generated.md`

Auswirkungen auf neue Konnektoren: Neue Konnektoren bleiben bis zum Minimum `partial` bestehen
Die folgende Matrix wird ausgeführt und dokumentiert.

Benötigte Nachweise:

- `phase1_header_block`
- Blockierung des Anforderungstexts
- Antwort-Header-Blockierung, wenn Framework-unterstützt
- Blockierung des Antwortkörpers
- audit/log Nachweise
- Connector startup/reload Validierung
- negative/pass-through Fall
- Apache und NGINX werden separat mit Befehlen und Ergebnissen dokumentiert
  Connector sind Bestandteil des Anspruchs

## Envoy Scaffold-Entscheidung

Frage: Wie soll das bestehende `connectors/envoy`-Verzeichnis ergänzt werden?
ohne gemeinsame Connector-Regeln zu duplizieren oder unbestätigtes Verhalten zu beanspruchen?

Entscheidung: als erste Gerüstbasislinie akzeptiert; erweitert durch die Envoy Build-Starter-Entscheidung unten.

Grund: Envoy verfügte ursprünglich über keinen Repository-gestützten Adapter-eigenen Quell-Build
Nachweise, Harness-Implementierung oder Runtime-Nachweise. Connector-spezifische Envoy
Dateien dokumentieren nur den Envoynstatus und offene Tore und verweisen gleichzeitig auf gemeinsame Regeln
in dieser Datei und in `connectors/_template/docs/coverage-decision-matrix.md`.

Evidence/paths:

- `connectors/envoy/README.md`
- `connectors/envoy/TODO.md`
- `connectors/envoy/docs/architecture.md`
- `connectors/envoy/docs/build.md`
- `connectors/envoy/docs/validation.md`
- `connectors/envoy/docs/coverage-decision-matrix.md`
- `connectors/envoy/harness/README.md`
- `connectors/envoy/src/README.md`
- `reports/template-verification-nginx-apache/envoy-template-alignment.md`

Auswirkungen auf neue Konnektoren: gemeinsame Gerüstregeln, Promotion-Gates, Status
Vokabular, No-CRS/With-CRS Trennung, Semantik der Abdeckungsmatrix und Laufzeit
Nachweisanforderungen global/shared. Envoy-spezifische Akten dürfen nicht geltend gemacht werden
Laufzeitverhalten bis ein Envoy build/harness und Envoy-Ziele ausgeführt werden
Nachweise vorlegen.

Envoynstatus:

- Gerüst: OK.
- Origin/metadata: Build-Starter-Metadaten vorhanden.
- Build: Nur Build-Starter.
- Harness: nur Vertrag.
- No-CRS: nicht ausgeführt.
- With-CRS: nicht ausgeführt.
- RESPONSE_BODY: nicht verifiziert.
- Lokal `connectors/envoy/tests`: abwesend.
- Promotion: nicht über build-starter/partial. hinaus zulässig

## Envoy Build-Starter-Entscheidung

Frage: Kann `connectors/envoy` über das reine Dokumentationsgerüst ohne hinausgehen?
Envoy API, ModSecurity API, Build-Logik oder Laufzeitergebnisse erfinden?

Entscheidung: Als Nur-Metadaten-Build-Starter akzeptiert.

Grund: Das Repository enthält Connector-neutrale `common/`-Header und Helper
Quelle plus Apache/NGINX Metadatenmuster. Es enthält nicht Envoy SDK/API
Header, Proxy-Wasm SDK, ext_proc protobuf/gRPC Bindungen oder eine Envoy-Laufzeit
Harness. Daher ist der einzige Repository-gestützte Build-Pfad die lokale Kompilierung
Envoy-Metadaten gegen konnektorneutralen gemeinsamen Code.

Evidence/paths:

- `common/include/msconnector/origin.h`
- `common/include/msconnector/capabilities.h`
- `common/src/origin.c`
- `common/src/capabilities.c`
- `connectors/envoy/ORIGIN.md`
- `connectors/envoy/SOURCE_MAP.json`
- `connectors/envoy/metadata.c`
- `connectors/envoy/metadata.h`
- `connectors/envoy/Makefile`
- `connectors/envoy/build/build_metadata.sh`

Auswirkung: Der Envoy-Build-Status kann erst danach als `build-starter` gemeldet werden
`make -C connectors/envoy build-starter` besteht. Der Laufzeitstatus bleibt bestehen
`not-verified`. RESPONSE_BODY Sperrung bleibt bestehen `not-verified`. Envoy ist es nicht
`adapter-owned` bis zur echten Envoy-Integrationsquelle, Abhängigkeiten, Build-Protokolle,
und harness/runtime Nachweise wurden hinzugefügt.

## Envoy Bridge-Starter-Entscheidung

Frage: Kann `connectors/envoy` über die reine Metadaten-Kompilierung hinausgehen in Richtung a
echter Connector-Pfad ohne gefälschte Envoy- oder ModSecurity-APIs?

Entscheidung: als sidecar/HTTP Brückenstarter angenommen.

Grund: Native Envoy-Filter, ext_proc und Proxy-Wasm-Pfade fehlen immer noch
Repository-Abhängigkeiten. Mit kann ein lokaler sidecar/HTTP Brückenstarter aufgebaut werden
Repository-eigener C-Code und Connector-neutral `common/` request/intervention
Formen. Dies gibt Envoy eine konkrete Integrationsnaht von der Anfrage zur Entscheidung ohne
Anspruch auf Envoy-Laufzeitkompatibilität oder ModSecurity-Regelausführung.

Evidence/paths:

- `connectors/envoy/src/envoy_bridge.h`
- `connectors/envoy/src/envoy_bridge.c`
- `connectors/envoy/src/envoy_bridge_main.c`
- `connectors/envoy/Makefile`
- `connectors/envoy/build/build_metadata.sh`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`

Auswirkung: Envoy kann nach `make -C connectors/envoy mit `bridge-starter` bewertet werden
build-starter` and `make -C connectors/envoy Selbsttest` bestanden. Das ist es nicht
`modsecurity-bridge-starter`, `runtime-smoke-verified`, `crs-verified`, oder
`partial` bis echte libmodsecurity- und Envoy-Laufzeitnutzungsbeweise vorliegen.
## Entscheidung 10: HAProxy verwendet Shared Gates mit lokalem SPOA Agent Starter

Frage: Sollte der HAProxy-Connector gleichzeitig globale Connector-Gates duplizieren?
Hinzufügen eines minimalen SPOE/SPOA-oriented nächsten Schritts?

Entscheidung: wegen Vervielfältigung abgelehnt; akzeptiert für einen lokalen SPOA Agentenstarter.

Grund: Die Vorlagenabdeckungsmatrix und diese Entscheidungsdatei definieren bereits
Gemeinsames Statusvokabular, Gerüstregeln, Promotion-Gates, No-CRS/With-CRS
Trennung, RESPONSE_BODY Mindestnachweis, externes Framework-Eigentum und
Laufzeit-Evidenz-Erwartungen. HAProxy-spezifische Dateien sollten darauf verweisen
Regeln und zeichnen nur den HAProxy-spezifischen Status auf. Das Repository ist wiederverwendbar
Gemeinsame Anforderungs-, Interventions-, Status- und Ursprungsformen, sodass ein lokaler Starter dies tun kann
Kompilieren und testen Sie synthetische Anforderungs- und Entscheidungslogik, ohne HAProxy zu erfinden
API Eigentum oder vollständige SPOP Frame-Verarbeitung. Eine separate lokale libmodsecurity
Die Bindung überprüft das lokale C API und kann durch die Diagnose SPOP ausgeübt werden.
Laufzeit für die bereichsbezogenen `haproxy_phase1_header_block` und
`haproxy_crs_sqli_anomaly_block` führt Smoke-Tests aus.

HAProxy-spezifische Anwendung:

- `connectors/haproxy` ist `spoa-agent-starter`.
- Laufzeitstatus ist `runtime-smoke-verified` für
  `haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`.
- Die Vorlagenausrichtung ist `scaffold-aligned plus local SPOA agent starter`.
- Es wird kein lokaler `connectors/haproxy/tests`-Ordner verwendet.
- `connectors/haproxy/src/haproxy_spoa_agent_starter.*` und
  `connectors/haproxy/src/haproxy_spoa_main.c` sind repo-autorisierte lokale Starter
  Dateien, kein produktiver Adaptercode.
- `make -C connectors/haproxy build-spoa-starter` kann den lokalen Starter kompilieren
  nur binär; Es wird kein HAProxy erstellt, kein HAProxy-Modul, kein vollständiger SPOA
  Dienst, HAProxy-erzwungene libmodsecurity-Integration oder Laufzeitadapter
  Logik.
- `make -C connectors/haproxy self-test-spoa` kann lokale synthetische überprüfen
  Nur allow/block-Entscheidungen anfordern; Es handelt sich nicht um einen HAProxy-Runtime-Smoke.
- `make -C connectors/haproxy self-test-modsecurity-binding` kann a. überprüfen
  Nur lokaler libmodsecurity Phase-1-Headerblock-Selbsttest; es kann sein, dass es nicht eingestellt wird
  `runtime_verified` wird von selbst auf true gesetzt.
- `make -C connectors/haproxy self-test-modsecurity-binding-crs` kann a. überprüfen
  lokaler CRS Nur SQLi-Bindungsselbsttest; Es darf `runtime_verified` nicht auf gesetzt werden
  an sich wahr.
- `make smoke-haproxy` darf `runtime_verified: true` nur setzen, wenn HAProxy aktiv ist
  sendet NOTIFY an den Diagnoseagenten, der Agent extrahiert Anforderungsargumente,
libmodsecurity erzeugt einen störenden 403, der verifizierte Set-Var ACK wird gesendet,
  Die Block-Probe gibt 403 zurück und die Clean-Probe gibt 200 zurück. CRS kann sein
  Nur für `haproxy_crs_sqli_anomaly_block` als verifiziert markiert, wenn die lokalen CRS
  Die Präambel wird geladen und der SQLi-Probe blockiert, während der Pass-Probe zurückkehrt
  200.
- Der produktive HAProxy-Adapter-Build bleibt BLOCKED bis ein vollständiger SPOP Parser oder
  SPOE/SPOA Protokollbibliothek, umfassender HAProxy-Laufzeitumgebung, umfassender CRS
  Nachweis, RESPONSE_BODY Nachweis, negative/pass-through Nachweis, audit/log
  Nachweise und Vollmatrixbeweise werden ausgewählt und aufgezeichnet.
- Es wird kein weitergehendes CRS-Verhalten oder RESPONSE_BODY-Sperrergebnis beansprucht.
- Zukünftige ausführbare Tests bleiben weiterhin im Besitz des Frameworks
  `modules/ModSecurity-test-Framework/tests/cases/` und Runner-Pfade wie z
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- Eine umfassendere Evidenz kann auf übergeordnete Ziele verweisen `make test-no-crs`,
  `make test-with-crs` und `make smoke-common` nur nach einem expliziten
  Der HAProxy-Laufzeitbereich ist vorhanden und wird ausgeführt.

Auswirkung: HAProxy kann ohne SPOA als lokaler Agent-Starter dokumentiert werden
Erstellen duplizierter Connector-Local-Gates oder YAML-Testfälle. Werbung darüber hinaus
Teilweiser Runtime-Smoke ist erst zulässig, wenn HAProxy-spezifisch produktiv ist
Quellursprung, Laufzeit-Build, breitere Nutzung, No-CRS, With-CRS, RESPONSE_BODY,
negative/pass-through, audit/log und vollständige Matrixbeweise werden aufgezeichnet.
## lighttpd Bridge-Starter-Entscheidung

Frage: Kann `connectors/lighttpd` über metadata/probe Build-Starter hinausgehen?
ohne eine Lighttpd API, FastCGI/SCGI Protokollkompatibilität zu erfinden,
ModSecurity API Integration oder Laufzeitanspruch?

Entscheidung: Nur als Entscheidungsdienst-Brückenstarter akzeptiert.

Grund: Das Repository hat konnektorneutralen `common/` Ursprung, Status,
Interventions-, Anforderungs- und Fähigkeitshelfer sowie vorhandene Apache/NGINX-Metadaten
Muster. Es wurde kein Lighttpd headers/SDK/source ausgewählt, ein Lighttpd
Modul-Build-Konfiguration, FastCGI/SCGI Protokolladapter,
ModSecurity-to-lightpd-Integrationscode oder ein Lighttpd-Laufzeit-Harness.
Daher ist der einzig sichere konkrete nächste Schritt eine repoeigene lokale Entscheidung
Service-Bridge-Starter, der das lokale compile/self-test-Verhalten nachweist, nicht den Adapter
Besitz oder Laufzeitkompatibilität.

Evidence/paths:

- `connectors/lighttpd/ORIGIN.md`
- `connectors/lighttpd/SOURCE_MAP.json`
- `connectors/lighttpd/metadata.c`
- `connectors/lighttpd/metadata.h`
- `connectors/lighttpd/Makefile`
- `connectors/lighttpd/build/build_starter.sh`
- `connectors/lighttpd/build/bridge_starter.sh`
- `connectors/lighttpd/src/lighttpd_build_starter.c`
- `connectors/lighttpd/src/lighttpd_bridge.h`
- `connectors/lighttpd/src/lighttpd_bridge.c`
- `connectors/lighttpd/src/lighttpd_bridge_main.c`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/TODO.md`
- `connectors/lighttpd/docs/architecture.md`
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
- `connectors/lighttpd/docs/coverage-decision-matrix.md`
- `connectors/lighttpd/harness/README.md`
- `connectors/lighttpd/src/README.md`
- `reports/template-verification-nginx-apache/lighttpd-template-alignment.md`
- Globale Matrix: `connectors/_template/docs/coverage-decision-matrix.md`
- Framework-Tests: `modules/ModSecurity-test-Framework/tests/cases/`
- Framework-Runner: `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- Öffentliche Lighttpd-Referenzen: `modules/ModSecurity-test-Framework/docs/imports/sources.md`
- Zukünftiger Connectorvertrag: `modules/ModSecurity-test-Framework/docs/future-connectors.md`

Auswirkungen auf lighttpd: Phase-0-Gerüst ist in Ordnung. Origin/metadata für die Brücke
Starter ist vorhanden. Die metadata/probe und Brückenstarter compile/self-test
Schecks sind verfügbar. Native Lighttpd-, FastCGI- und SCGI-Produktionsintegration
bleiben blockiert, bis ein konkreter Laufzeitpfad und seine Abhängigkeiten ausgewählt werden.
Harness, No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through, audit/log und
Promotion-Gates bleiben open/not bis zum Laufzeitnachweis pro Connector verifiziert
existiert. Es darf kein lokaler `connectors/lighttpd/tests`-Ordner verwendet werden.

Laufzeitanspruch: keiner.
## Entscheidung 10: Traefik Decision-Service Starter

Frage: Wie soll `connectors/traefik` über Metadaten zur Kompilierungszeit hinausgehen?
ohne einen Traefik API zu erfinden oder eine Laufzeitüberprüfung zu beanspruchen?

Entscheidung: als lokaler Entscheidungsdienststarter akzeptiert.

Grund: `connectors/traefik` enthält jetzt Repo-eigene Metadaten, Quellzuordnung,
Ursprung, Startquelle zur Kompilierungszeit und Startquelle für den lokalen Entscheidungsdienst
das baut auf konnektorneutralen `common/`-Helfern auf. Das Repository nicht
enthalten ein ausgewähltes Traefik-Plugin API, Middleware API, Go-Modul, Traefik-Laufzeit
Quelle, HTTP Bridge-Laufzeit oder Traefik-Harness. Deshalb das nächste Mal umgesetzt
Schritt ist ein lokales In-Memory-Request-to-Decision-Modell mit Selbsttest, kein
Traefik-Laufzeitadapter oder verifizierter `forwardAuth`-Dienst.

Evidence/paths:

- `connectors/traefik/README.md`
- `connectors/traefik/TODO.md`
- `connectors/traefik/ORIGIN.md`
- `connectors/traefik/SOURCE_MAP.json`
- `connectors/traefik/metadata.c`
- `connectors/traefik/metadata.h`
- `connectors/traefik/Makefile`
- `connectors/traefik/build/build-starter.sh`
- `connectors/traefik/src/traefik_build_starter.c`
- `connectors/traefik/src/traefik_decision_service.h`
- `connectors/traefik/src/traefik_decision_service.c`
- `connectors/traefik/src/traefik_decision_service_main.c`
- `connectors/traefik/docs/coverage-decision-matrix.md`
- `reports/template-verification-nginx-apache/traefik-template-alignment.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `common/include/msconnector/`
- `common/src/`
- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Auswirkungen auf neue Konnektoren: Konnektorspezifische Starter können lokale Entscheidungen modellieren
Logik nur, wenn sie gefälschte Server-APIs vermeiden und ihren Nicht-Laufzeitstatus festlegen
explizit. Laufzeitansprüche erfordern ausgeführte Connector-spezifische Laufzeitbefehle und
Nachweise.

Nachträgliche Änderung oder erforderliche Nachweise: Traefik bleibt bis zur Laufzeit nicht verifiziert
ein Produktionsintegrationspfad, upstream/license Nachweise, Laufzeitaufbau, Nutzung,
No-CRS-, With-CRS-, RESPONSE_BODY-, negative/pass-through- und audit/log-Nachweis
werden erstellt und dokumentiert.
