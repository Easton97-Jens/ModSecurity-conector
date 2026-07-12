> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Offene Fragen

**Sprache:** [English](open-questions.md) | Deutsch

Diese Datei trennt gelöste scaffold/runtime-Entscheidungen von Fragen, die
benötigen noch Nachweise. Die vollständigen Entscheidungsdetails finden Sie hier
`connector-scaffold-decisions.md`.

## Aktuelle Bereitschaft

- Documentation/decision Commit-Bereitschaft: Ja.
- Commit-fertig für Dokumentations-/Entscheidungsstand: ja.
- Standardmäßige Smoke-Bereitschaft zur Laufzeit: blockiert, bis der Standard-Build-Root dies getan hat
  ModSecurity V3 Quellen.
- Letzter dokumentierter Standardblocker:
  `<local-state-root>/sources/ModSecurity_V3`
  fehlt.
- Aktuelle `/src` `make smoke-common`: PASS; Apache 54 PASS und NGINX 54 PASS,
  sowohl 0 FAIL als auch 0 BLOCKED.
- Aktuelle `/src` `make test-no-crs`: PASS; Apache 54 PASS und NGINX 60 PASS,
  sowohl 0 FAIL als auch 0 BLOCKED.
- Aktuelle `/src` `make test-with-crs`: PASS; Apache 55 PASS und NGINX 61 PASS,
  sowohl 0 FAIL als auch 0 BLOCKED.
- Aktuelle With-CRS CRS-Nachweise: `crs_sqli_anomaly_block` PASS für Apache und
  NGINX, erwarteter 403 und tatsächlicher 403.
- RESPONSE_BODY Blockierung: nicht überprüft.
- Vollständige Laufzeit-Verifikation: nein.

## Gelöste Entscheidungen

- Die Dokumentation des übergeordneten Connectors muss darauf verweisen
  `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md` wenn es
  verweist auf das gemeinsame Roadmap-Inventar. Framework-interne relative Roadmap
  Referenzen werden nicht geändert.
- Neue Konnektoren dürfen keinen lokalen `connectors/<name>/tests`-Ordner hinzufügen.
  Ausführbare Tests sind Eigentum des Frameworks und werden referenziert
  `modules/ModSecurity-test-Framework/tests/cases/`,
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`,
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`, und
  Repository Erstellen Sie Ziele, sofern vorhanden.
- NGINX-spezifische Framework-YAML-Fälle sind unter verfügbar
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- Der aktuelle NGINX Bauvertrag ist
  `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`.
- Der aktuelle NGINX docroot work-parent Vertrag ist
  `NGINX_HARNESS_PARENT=$(BUILD_ROOT)`.
- Historische NGINX 11 BLOCKED Zeilen werden als environment/docroot klassifiziert.
  Berechtigungsblocker und werden in aktuellen `/src`-Wiederholungen behoben.
- `make test-no-crs` ist ein dokumentiertes Ziel und wird derzeit für Apache übergeben
  und NGINX unter `/src`.
- `make test-with-crs` ist ein dokumentiertes Ziel und wird derzeit für Apache übergeben
und NGINX unter `/src`.
- Das Laden von CRS wird für das aktuelle With-CRS nachgewiesen, das von `/src/coreruleset` ausgeführt wird.
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`, und
  `crs_sqli_anomaly_block` PASS für beide Connectors.
- `action_status_401_phase1_block` ist nun für den aktuellen `/src` aufgelöst
  läuft nach einer With-CRS-spezifischen Erwartung: No-CRS bleibt expected/actual 401,
  With-CRS ist expected/actual 403.
- Framework-local `make quick-check` wird als nicht verfügbar im aufgelöst
  Framework-Makefile für diesen Arbeitsbereich; Framework-Local `make lint` und
  Stattdessen wurden `make check-test-matrix` ausgeführt und beendet 0.
- Das Vokabular für den gemeinsamen Gerüststatus lautet: `template`, `scaffolded`,
  `adapter-owned`, `runtime-smoke-verified`, `crs-verified`, `partial` und
  `not-verified`.
- Vorlagen-Promotion-Gates sind dokumentiert: `scaffolded`, `adapter-owned`,
  `runtime-smoke-verified`, `crs-verified` und `more-than-partial`.
- Der Vorlagenstatus wird als geeignetes Gerüst normalisiert und nicht zur Laufzeit überprüft.
  Herkunft, Metadaten, Build, No-CRS, With-CRS, Abdeckungsmatrix, Laufzeitnachweis,
  und RESPONSE_BODY-Blockierung sind Gates pro Connector, keine Template-Defekte.
- Apache- und NGINX-Phase-für-Phase-Template-Alignment-Berichte wurden hinzugefügt:
  `apache-template-alignment.md` und `nginx-template-alignment.md`.
  Beide sind auf Gerüst, origin/license, Metadaten, Build, Harness, ausgerichtet.
  externe Tests und ausgeführter No-CRS/With-CRS Umfang; beide bleiben `partial`.

## Noch offen/aufgeschoben

- Apache-spezifische YAML-Fälle bleiben zurückgestellt. Benötigte Nachweise: YAML Dateien unter
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`
  plus Laufzeitbefehlsausgabe, die die erwarteten Ergebnisse anzeigt. Derzeit nur
  `README.md` wurde dort gefunden.
- RESPONSE_BODY Sperrung bleibt aufgeschoben. Erforderlicher Nachweis: ein Repository-gestützter Nachweis
  Laufzeittestfall, erwarteter Blockierungs-Antworttext-Trigger, tatsächliche Blockierung
  Ergebnis wie HTTP 403, log/report Nachweise, ausgeführter Befehl, betroffen
  Connector und separate Apache/NGINX Dokumentation für jeden gemeinsamen Anspruch.
- Genauer CRS/default-action oder ModSecurity-Aktionszusammenführungsgrund für die
  With-CRS 403 Antwort bleibt zurückgestellt. Erforderliche Nachweise: Audit pro Connector
  Nachweise oder gezielte Isolierung, die den endgültigen Störfaktor belegen rule/action
  Mechanik. Die Laufzeitinkongruenz selbst wird durch bereichsbezogene Erwartungen behoben.
- Der NGINX-spezifische `nginx_phase4_strict_connection_abort` Laufzeitstatus bleibt bestehen
  für die aktuellen Zielzusammenfassungen zurückgestellt. Benötigter Nachweis: ein aktueller
  summary/result Eintrag für diesen Fall und sein Befehlsergebnis. Die YAML-Datei
  existiert, war aber in den aktuellen No-CRS- oder With-CRS-Zusammenfassungen nicht vorhanden.
- Die Alternative, ein materialisiertes `common/include`-Layout zu generieren, bleibt bestehen
  aufgeschoben. Benötigter Nachweis: implementiertes Materialisierungsverhalten, generiert
  Pfadnachweise, Compilerzeilen, die diesen Pfad verwenden, und Runtime-Smoke-Ergebnisse.
- Mehr als `partial` Apache/NGINX Vollständigkeit bleibt zurückgestellt. Benötigt
  Nachweis: dokumentierte Laufzeitergebnisse für `phase1_header_block`,
Blockierung des Anforderungshauptteils, Blockierung des Antwortheaders, wenn dies vom Framework unterstützt wird,
  Blockierung des Antworttextes, audit/log Nachweise, Konnektor startup/reload
  Validierung und ein negative/pass-through-Fall ohne offene FAIL/BLOCKED-Zeilen
  in der beanspruchten Minimalmatrix.
- Die Standard-`make smoke-common` ohne explizite `/src`-Umgebung bleibt bestehen
  für diesen Arbeitsbereich zurückgestellt. Erforderlicher Nachweis: Führen Sie `make fetch-deps` für die aus
  Standardwert `BUILD_ROOT`/`SOURCE_ROOT`, oder geben Sie einen gültigen Wert an
  `MODSECURITY_SOURCE_DIR`/`MODSECURITY_V3_SOURCE_DIR`, dann erneut ausführen
  `make smoke-common` und notieren Sie das Ergebnis.

## Envoyr öffnet Tore

Envoy Bridge-Starter-Arbeit nutzt stattdessen die vorhandenen global/shared-Connector-Gates
als sie in Envoy-spezifische Dateien zu kopieren. Die folgenden Envoy-Tore bleiben bestehen
geöffnet:

- Produktion vorgeschaltet origin/license Auswahl über lokalen Brückenstarter hinaus.
- libmodsecurity headers/libs und Envoy Bridge-Integration build/runtime Protokolle.
- Nutzen Sie Implementierungs- und Nachweispfade.
- Separate No-CRS- und With-CRS-Laufzeitnachweise.
- RESPONSE_BODY Nachweise sperren.
- Negative/pass-through und audit/log Nachweise.
- Promotion über den Brückenstarter hinaus.

## Envoy Build-Starter Offene Abhängigkeiten

Der Bridge-Starter ist verfügbar, die produktive Envoy-Integration jedoch schon
weiterhin blockiert, bis ein Pfad echte Abhängigkeiten bereitstellt:

- nativer Envoy HTTP Filter: Envoy C++ SDK/API Header und Build-Integration;
- externe Verarbeitung: ext_proc protobuf/gRPC generierter Code und Service-Abhängigkeiten;
- Proxy-Wasm: Proxy-Wasm SDK und WASM Build-Toolchain;
- sidecar/bridge: dokumentiertes Protokoll, Prozessvertrag und Laufzeitnutzung.

## Envoy Bridge-Starter Offene Tore

- Definieren Sie einen echten Envoy-Laufzeitintegrationspunkt: sidecar HTTP route, ext_authz,
  ext_proc, nativer Filter oder Proxy-Wasm.
- Fügen Sie echte libmodsecurity headers/libs hinzu und implementieren Sie den Transaktionslebenszyklus.
- Erzeugen Sie das Framework-eigene No-CRS- und With-CRS-Ergebnis JSON mit PASS/FAIL/BLOCKED
  zählt.
- Nachweisen Sie CRS loaded/effective Verhalten für Envoy.
- Behalten Sie RESPONSE_BODY als separates, nicht verifiziertes Gate bei, bis ein blockierender Laufzeitfall auftritt
  geht vorbei.
## Offene HAProxy-Elemente

- Erweitern oder ersetzen Sie die minimale Diagnose-Handshake-Teilmenge SPOP durch eine vollständige
  SPOA Agentenimplementierung vor Beanspruchung der HAProxy-Laufzeitkompatibilität.
- Konvertieren Sie aktuelle BLOCKED HAProxy-Matrixzeilen in live ausgeführte PASS/FAIL
  Zeilen, bevor eine breitere Framework-Abdeckung beansprucht wird.
- Halten Sie die diagnostische HAProxy-zu-Agent-Teilmenge vom vollständigen Adapter getrennt
  Werbung; aktuelle `spoe_runtime_status` ist
  `diagnostic-enforcement-verified` nur für den bereichsbezogenen Header-Block und CRS
SQLi-Anomalie führt Smoke-Tests aus.
- Fügen Sie Laufzeitnachweise für eine umfassendere No-CRS-Live-Ausführung und eine umfassendere With-CRS-Ausführung hinzu
  Live YAML Ausführung über `crs_sqli_anomaly_block`, RESPONSE_BODY Blockierung hinaus,
  negative/pass-through Verhalten, audit/log Artefakte und vollständige Matrix
  Promotion.
- Heraufstufen über `spoa-agent-starter` hinaus erst nach produktivem Adapter-Build und
  Laufzeitnachweise werden aufgezeichnet.
## lighttpd Offene Tore

Der Lighttpd-Bridge-Starter ist created/checked, aber Adapter- und Laufzeit-Gates
bleiben offen oder nicht verifiziert:

- Upstream lighttpd source/version und ein konkreter Integrationspfad gibt es nicht
  ausgewählt.
- Die Erstellung eines echten nativen Moduls wird durch das Fehlen von lighttpd headers/SDK/source. blockiert.
- Die echte FastCGI/SCGI-Brücke wird durch fehlenden Protokolladapter und Lighttpd blockiert
  Laufzeitkonfiguration.
- Der ModSecurity-Integrationscode für lighttpd ist nicht implementiert.
- Harness verfügt derzeit nur über einen blockierten Runtime-Smoke-Einstiegspunkt.
- Die No-CRS- und With-CRS-Laufzeit wurde für lighttpd nicht ausgeführt.
- RESPONSE_BODY Sperrung, negative/pass-through und audit/log Nachweise sind nicht vorhanden
  für lighttpd verifiziert.
- Werbung über bridge-starter/partial hinaus ist ohne Pro-Connector nicht zulässig
  Runtime-Nachweise.
## Offene Fragen zu Traefik

- Welcher Traefik-Integrationsansatz für die Produktion wird gegebenenfalls implementiert?
  bleibt offen.
- Traefik Upstream origin/license, Produktionsaufbau, Harness, No-CRS, With-CRS,
  RESPONSE_BODY, negative/pass-through und audit/log Nachweise bleiben offen.
- Der aktuelle Decision-Service-Starter wählt kein Traefik-Plugin aus,
  Middleware, sidecar/proxy, benutzerdefiniertes Modul oder Go-Service-Pfad; `forwardAuth`
  bleibt nur für Starter ohne HTTP/Traefik Laufzeitnachweis.
- Traefik darf nicht über den Decision-Service-Starter hinaus promoted werden, bis Connector-
  Es werden spezifische Laufzeitnachweise erstellt und dokumentiert.

## Connector-Starter Open Gates

Der Framework-Connector-Starter-Runner schließt nur lokale build/self-test
Starterbeweise für Envoy, HAProxy, lighttpd und Traefik. Diese Laufzeittore
bleiben offen für Envoy, lighttpd und Traefik und bleiben offen für HAProxy darüber hinaus
`haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`:

- Ein echtes server/proxy-Harness.
- breitere No-CRS- und With-CRS-Laufzeitausführung.
- breitere CRS wirksame Sperrbeweise.
- RESPONSE_BODY Nachweise sperren.
- Negative/pass-through und audit/log Nachweise.
- Promotion über den Starterstatus hinaus.

## Laufzeit-Smoke-Test öffnet Tore

Die neuen Runtime-Smoke-Einstiegspunkte sind vorhanden, diese Tore bleiben jedoch offen
Envoy, lighttpd und Traefik sowie für HAProxy über den einzelnen Header-Block hinaus
und CRS SQLi-Anomalie führt Smoke-Tests aus:

- Implementieren Sie einen echten ausführbaren server/proxy-Harness unter dem Connectorkabelbaum
  Vertrag, der die derzeit blockierten `run_<name>_smoke.sh`-Einstiegspunkte ersetzt.
- Führen Sie Framework-eigene YAML-Fälle über diesen Harness aus.
- Erzielen Sie umfassendere No-CRS- und With-CRS-Laufzeitergebnisse.
- Nachweisen Sie, dass eine umfassendere CRS wirksame Sperrung erfolgt, wenn dies behauptet wird.
- Nachweisen Sie die Blockierung durch RESPONSE_BODY mit einem echten Laufzeittest, bevor Sie Änderungen vornehmen
  RESPONSE_BODY Status.
- Bewahren Sie build/self-test Starterbeweise getrennt von Runtime-Smoke-Nachweisen auf.

Speziell für HAProxy: Framework-eigene lokale HAProxy-Quellenerfassung,
binäre Vorbereitung, diagnostischer SPOP Kontakt, verifizierte Set-Var ACK Codierung und
Die beiden bereichsbezogenen Live-ModSecurity-Durchsetzungspfade sind keine offenen Tore mehr. Die
Die verbleibenden offenen HAProxy-Laufzeit-Gates werden derzeit live ausgeführt
BLOCKED Framework-Zeilen, breitere CRS Abdeckung, RESPONSE_BODY,
negative/pass-through Verhalten, audit/log Nachweise und Vollmatrix-Promotion.
