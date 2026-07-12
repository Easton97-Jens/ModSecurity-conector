# Verkehrsvalidierung

**Sprache:** [English](validation.md) | Deutsch


Status: minimal_runtime_smoke nur für den ForwardAuth-Anforderungspfad
Laufzeitstatus: Nur überprüft, wenn eine lokale, von common.sh verwaltete Traefik-Binärdatei den HTTP-Smoke ausführt

Die Traefik-Laufzeitvalidierung ist an Bedingungen geknüpft. Ohne eine lokale Binärdatei von
`TRAEFIK_BIN` oder von common.sh verwaltete Caches, `make smoke-traefik` beendet 77 mit
BLOCKIERTE Beweise. Mit einer aufgelösten lokalen Binärdatei startet der Smoke Runner a
minimaler Upstream, minimaler ForwardAuth-Entscheidungsdienst und Traefik mit einem
generierte lokale Konfiguration. Globale Validierungsgates und Statusvokabular sind in definiert
`reports/archive/template-verification-nginx-apache/connector-scaffold-decisions.md` und
`connectors/_template/docs/coverage-decision-matrix.md`.

Metadaten der Laufzeitkomponente werden zentral in `common.sh` angeheftet:
`TRAEFIK_VERSION=3.7.5`, `TRAEFIK_SOURCE_URL`, `TRAEFIK_INSTALL_DOCS_URL`,
`TRAEFIK_DOWNLOAD_URL`, `TRAEFIK_SHA256_URL` und `TRAEFIK_SHA256`. Das erwartete
Die lokale Binärdatei bleibt `$CONNECTOR_COMPONENT_CACHE/traefik/bin/traefik`.
Downloads sind deaktiviert, sofern keine explizite `ALLOW_RUNTIME_DOWNLOADS=1`-Vorbereitung erfolgt
Die Ausführung überprüft den angehefteten SHA256, extrahiert nur die `traefik`-Binärdatei und
schreibt nur in den lokalen Komponentencache:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
make smoke-traefik
```

## Aktuelle Traefik-Beweise

- Metadaten-Build-Starter: PASS für Metadaten-Kompilierungsrauch.
- Decision-Service-Starter-Build: PASS für lokalen Kompilierungsrauch.
- Entscheidungsdienst-Selbsttest: PASS für In-Memory-Zulassungs-/Blockierungsentscheidungen.
- Connector-Dienst: C17-Kompilierungs-/Link-Ziel mit expliziter lokaler libmodsecurity
  Include- und Bibliothekspfade.
- Konfiguration laden: `make -C connectors/traefik check-config` wird aufgerufen
  `--check-config` für den integrierten Dienst.
- Smoke-Test starten: `make -C connectors/traefik start-smoke` ruft `--serve` auf und startet
  echtes Traefik mit einer temporären ForwardAuth-Dateianbieterkonfiguration, überprüft beides
  Prozesslebenszyklen und bereinigt, ohne Anfragen zu senden.
- Connector-Laufzeit: `make -C connectors/traefik runtime-smoke` erfordert eine echte
  Traefik -> forwardAuth -> Gemeinsamer Laufzeitpfad mit erlaubtem 200 und blockiertem 403.
- Anforderungskörper-Kompatibilitätsprüfung: bedingt durch
  `make smoke-traefik-request-body`; Es verwendet eine separat generierte Middleware
  Konfiguration mit aktiviertem `forwardBody`. Es handelt sich nicht um ein kanonisches No-CRS
  Beweis für den eingecheckten `request_body_mode=none`-Pfad.
- Minimaler CRS-Smoke-Test: bedingt über `make smoke-traefik-crs`; PASS nur mit
  lokales CRS und CRS-gestützte 403-Beweise.
- Sekundärer CRS-Smoke-Test: bedingt über `make smoke-traefik-crs-secondary`; PASS
  nur mit lokalem CRS und sekundärem CRS-gestütztem 403-Nachweis.
- CRS vollständig: nicht beansprucht.
- RESPONSE_BODY: `unsupported_by_host_model` für den ausgewählten `forwardAuth`
  Integration.
- Negativ/Pass-Through: Nur durch einen lokalen Runtime-Smoke belegt, wenn
  eine zulässige Anfrage 200 zurückgibt.
- Audit/Protokoll: nicht überprüft.

Frameworkeigene Pfade und Ziele für die zukünftige Validierung:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

Der lokale Entscheidungsdienst-Selbsttest bleibt ein Nicht-Laufzeitbeweis. Das Echte
Servicequelle und lokaler gezielter Smoke-Test führen immer noch nicht zur Produktion,
Vollmatrix-, CRS-vollständiger, Antworttext- oder beibehaltener CI-Verifizierung.

## Connector-eigene Service-Einstiegspunkte

```sh
make -C connectors/traefik build-connector
make -C connectors/traefik check-config
make -C connectors/traefik start-smoke
make -C connectors/traefik runtime-smoke
```

Diese Stufen rufen einander nicht implizit hervor. Der Laufzeit-Harness schreibt
temporäre konkrete Dienst- und Traefik-Dateianbieterkonfigurationen außerhalb des
Checkout und bereinigt jeden Vorgang. Es fehlen vorab ausgeführte lokale ausführbare Dateien
GESPERRT/77; Behobene Konfigurations-, Start-, Zuordnungs- oder Statusfehler sind FAIL.

## Überprüfung des Native Go-Middleware-Hosts (nicht gefördert)

Das Repository-eigene `native_middleware/`-Paket hat sich auf Unit-Tests konzentriert
Begrenzte Anfrage-/Antwortblöcke, `io.ReaderFrom`-Delegierung, optional
`ResponseWriter`-Schnittstellenerhaltung, Pre-Commit-Ablehnung und die
konservatives Post-Commit-Ergebnis `log_only`:

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

Diese Befehle führen nur Go-Quellenprüfungen durch. Der separate Host-Befehl unten
Stellt das Paket in einem verfügbaren lokalen Plugin-Verzeichnis bereit und startet angeheftet
Traefik benötigt eine Bestätigung des Plugin-Ladens und leitet ein Body-Lager weiter
Anfrage über die konfigurierte Middleware:

```sh
TRAEFIK_BIN=/absolute/local/traefik \
TRAEFIK_NATIVE_RUNTIME_ROOT=/absolute/runtime-root \
make -C connectors/traefik runtime-smoke-traefik-native
```

`passthrough` bleibt der reine Quell-Standard, aber der ausgewählte native Host
check konfiguriert `engineMode: uds` und startet eine private Persistente
Common/libmodsecurity-Dienst. Der eigentliche Host-Lauf verwendet das Framework no-CRS
Regeln für P1/P2/P3 und das sichere P4-Protokollergebnis nach dem Commit. Das tut es immer noch
beanspruchen keinen strikten späten Abbruch, First-Byte-before-EOS, No-Full-Response-Pufferung,
oder eine eingecheckte Fähigkeitserhöhung ohne das passende kanonische Artefakt.
Der Validierungspfad C `forwardAuth` und sein vorhandener Status bleiben unverändert.

## Framework-eigener Starternachweis

`make connector-starter-checks` führt den Traefik-Metadaten- und Entscheidungsdienst aus
Anlasserprüfungen ab
`modules/ModSecurity-test-Framework/ci/runtime/run-connector-starter-checks.sh`.
Ergebnisse werden geschrieben
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` und
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

Bei den Traefik-Einträgen handelt es sich lediglich um Connector-Starter-Build-/Selbsttestnachweise:
`runtime_verified` ist `false`, `runtime_status` ist `not-verified` und
`response_body_verified` ist `false`.

## Runtime-Smoke-Einstiegspunkt

`make smoke-traefik` ruft den Framework-eigenen Traefik Runtime-Smoke Runner auf.
`connectors/traefik/harness/run_traefik_smoke.sh` löst `TRAEFIK_BIN` oder auf
lokale, von common.sh verwaltete Cache-Artefakte über die gemeinsam genutzten Helfer. Wenn ein Einheimischer
Wenn die Traefik-Binärdatei gefunden wird, sendet der Läufer eine zulässige und eine blockierte Anfrage
Anfrage über Traefik und zeichnet die beobachteten HTTP-Status auf. Wenn kein Einheimischer
Binärdatei gefunden wird, wird 77 mit dem Beweis BLOCKED beendet.

Dieser Einstiegspunkt führt keine Entscheidungsservice-Starter-Selbsttests zur Laufzeit aus
Beweise. RESPONSE_BODY ist `unsupported_by_host_model` für die Auswahl
`forwardAuth`-Integration.

Das optionale gezielte ModSecurity-Backend verwendet denselben Laufzeiteinstiegspunkt mit
ein expliziter Backend-Selektor:

```sh
DECISION_BACKEND=libmodsecurity make smoke-traefik
make smoke-traefik-modsecurity
```

Dieser Modus lädt `common/rules/modsecurity_targeted_smoke.conf` über einen lokalen
libmodsecurity C-API-Evaluator. Die zulässige Anfrage muss 200 zurückgeben und die
Anfrage mit `X-Modsec-Smoke: block` muss 403 von Regel `1000001` zurückgeben.
`result.json` fügt `decision_backend`, `modsecurity_backend_verified` hinzu,
`modsecurity_rule_file`, `modsecurity_rule_id`, `modsecurity_rule_loaded`,
`intervention_status` und `decision_log_path`. Fehlende lokale libmodsecurity
Header/Bibliotheken werden als Exit 77/BLOCKED gemeldet, nicht als Fehler oder Erfolg.

Der Legacy-Request-Body-Fähigkeitstest verwendet denselben Traefik `forwardAuth`
Architektur, aber nicht die kanonische eingecheckte Konfiguration: Sie erstellt eine
Separate lokale Middleware mit aktiviertem `forwardBody` und wählt die aus
Anfrage-Body-Smoke-Fall:

```sh
MODSECURITY_SMOKE_CASE=request_body DECISION_BACKEND=libmodsecurity make smoke-traefik
make smoke-traefik-request-body
make smoke-open-connectors-request-body
```

Dieser Modus lädt `common/rules/modsecurity_request_body_smoke.conf` und sendet POST
Anfragen mit `Content-Type: application/x-www-form-urlencoded` und erfordert
der blockierte Körpermarker `modsec-request-body-block`, um 403 von der Regel zurückzugeben
`1000002`. Erfolgreiche Beweise schreiben
`$TRAEFIK_RESULT_ROOT/request-body-result.json`,
`$TRAEFIK_LOG_ROOT/request-body-decision.log` und
`$TRAEFIK_LOG_ROOT/request-body-request-transcript.jsonl`. Es kann untergehen
`request_body_smoke_verified` für diesen isolierten Kompatibilitätslauf; die
Der kanonische No-CRS-Writer importiert dieses Flag nicht und behält es bei
`request_body_verified=false`. `response_body_verified` bleibt falsch.

Der minimale CRS-Smoke-Test verwendet denselben Laufzeiteinstiegspunkt mit ausgewähltem CRS:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-traefik
make smoke-traefik-crs
make smoke-traefik-crs-secondary
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

Dieser Modus lädt CRS von common.sh-verwalteten lokalen Pfaden und schreibt das generierte
CRS Smoke-Konfiguration unter `$TRAEFIK_RESULT_ROOT/crs-smoke` und Aufzeichnungen
CRS-spezifische Beweise in `$TRAEFIK_RESULT_ROOT/crs-result.json` und
`$TRAEFIK_LOG_ROOT/crs-decision.log`. Die zulässige Anfrage muss 200 zurückgeben
blockierte Anfrage verwendet `/?id=1%20UNION%20SELECT%20password%20FROM%20users` und
muss 403 vom CRS zurückgeben, nicht von der Regel `1000001`.

Der sekundäre CRS-Smoke-Test verwendet denselben Läufer mit `CRS_SMOKE_CASE=secondary`.
Es schreibt die generierte Konfiguration unter `$TRAEFIK_RESULT_ROOT/crs-secondary-smoke`,
Datensätze `$TRAEFIK_RESULT_ROOT/crs-secondary-result.json`,
`$TRAEFIK_LOG_ROOT/crs-secondary-decision.log` und
`$TRAEFIK_LOG_ROOT/crs-secondary-audit.log` und sendet
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`. Ein PASS erfordert HTTP 200 für
zulässige Anfrage, HTTP 403 für die sekundäre Probe und eine tatsächliche CRS-Regel
Aus Beweismitteln extrahierte ID/Nachricht. Wenn CRS, libmodsecurity und Traefik vorhanden sind
verfügbar, aber die Sekundärsonde nicht blockiert ist, ist das Ergebnis FAIL.

## Unterscheidung des Laufzeitstatus

Die Connector-Metadaten bleiben `runtime_status: not_verified` und `verification_status: connector-gap`. Die pro Lauf generierten `result.json`-Dateien können unterschiedlich sein: Der lokale Starter-Smoke-PASS kann `runtime_verified: true` und `runtime_status: verified` melden; no-local-binary oder fehlende Laufzeitfälle können `status: BLOCKED`, `runtime_verified: false` und `runtime_status: blocked` melden. Diese Felder pro Lauf bedeuten nicht Produktion, CRS, RESPONSE_BODY oder vollständige Matrixüberprüfung.

## Gemeinsames Ergebnisschema

`make smoke-traefik` verwendet jetzt den gemeinsamen Smoke-Result-Writer in
`common/scripts/write_smoke_result.py`. Das generierte `result.json` enthält die
allgemeine Schemafelder `connector`, `integration_mode`, `runtime_verified`,
`full_matrix_ready`, `production_ready`, `crs_complete`,
`response_body_verified`, `allowed_request_status`, `blocked_request_status`,
`request_body_smoke_verified`, `request_body_access_enabled`,
`request_body_rule_file`, `request_body_rule_id`, `request_method`,
`blocked_body_marker`, `evidence_root`, `timestamp`, `skipped_reason`,
`missing_dependencies` und `claims_not_allowed`.

Aktuell erwartetes Ergebnis ohne lokale Binärdatei:

- Integrationsmodus: `forwardAuth`
- Status: `BLOCKED`
- Exit-Code: 77
- Laufzeitstatus: Generierte, keine lokale Binärdatei oder fehlende Laufzeit-`result.json`-Dateien melden möglicherweise `runtime_status: blocked`; Connector-Metadaten bleiben `runtime_status: not_verified` und `verification_status: connector-gap`.
- Beweisstamm: `$VERIFIED_RUN_ROOT/traefik-smoke/`, zurückgreifen auf
  `$BUILD_ROOT/results/traefik-smoke/`
- Binäre Umgebungsvariable: `TRAEFIK_BIN`
- Lokale Suchpfade: `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
  `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT` und
  `$SOURCE_ROOT`, alle bereitgestellt von `common.sh`
- Fehlende Abhängigkeiten, wenn keine lokale Binärdatei gefunden wird: `["traefik"]`
- skipped_reason, wenn keine lokale Binärdatei gefunden wird:
  `traefik runtime dependency not available in local common.sh-managed paths`
- Für BLOCKIERTE Beweise: `runtime_verified`, `production_ready`,
  `full_matrix_ready`, `crs_complete` und `response_body_verified` bleiben alle erhalten
  falsch.

Erwartetes PASS-Ergebnis mit einer lokalen Binärdatei:

- Laufzeitstatus: generierte lokale Starter-PASS-`result.json`-Dateien können `runtime_verified: true` und `runtime_status: verified` für die Ausführung dieser einzelnen lokalen Starter verwenden; Die Connector-Metadaten bleiben `runtime_status: not_verified` und `verification_status: connector-gap`, bis echte Traefik-Connector-Laufzeitnachweise vorliegen.
- Zulässiger Anforderungsstatus: `200`
- Blockierter Anforderungsstatus: `403`
- Aufgelöste Laufzeitbinärdatei: lokaler Pfad von `TRAEFIK_BIN` oder einer von common.sh verwalteten Datei
  Suchstammverzeichnis
- `production_ready`, `full_matrix_ready`, `crs_complete` und
  `response_body_verified` bleibt falsch.
- Dieser lokale Starter-PASS-Status ist nicht Produktion, CRS, RESPONSE_BODY oder vollständige Matrixüberprüfung.

Erwartetes gezieltes ModSecurity PASS-Ergebnis mit lokalem Traefik und lokalem
libmodsecurity:

- Entscheidungs-Backend: `libmodsecurity`
- ModSecurity-Backend überprüft: `true`
- ModSecurity-Regeldatei: `common/rules/modsecurity_targeted_smoke.conf`
- ModSecurity-Regel-ID: `1000001`
- ModSecurity-Regel geladen: `true`
- Interventionsstatus: `403`
- Entscheidungsprotokollpfad: `$TRAEFIK_LOG_ROOT/modsecurity-decision.log`
- `production_ready`, `full_matrix_ready`, `crs_complete` und
  `response_body_verified` bleibt falsch.
- Dieser lokale Starter-PASS-Status ist nicht Produktion, CRS, RESPONSE_BODY oder vollständige Matrixüberprüfung.

Erwartetes PASS-Ergebnis des Legacy-Request-Body-Capability-Tests mit lokalem Traefik
und lokale libmodsecurity (keine kanonischen No-CRS-Beweise):- Entscheidungs-Backend: `libmodsecurity`
- ModSecurity Smoke-Case: `request_body`
- Anforderungsmethode: `POST`
- Anforderungstextzugriff aktiviert: `true`
- Regeldatei für Anforderungstext: `common/rules/modsecurity_request_body_smoke.conf`
- Anforderungshauptregel-ID: `1000002`
- Anforderungshauptregel geladen: `true`
- Blockierter Körpermarker: `modsec-request-body-block`
- Zulässiger Anforderungsstatus: `200`
- Blockierter Anforderungsstatus: `403`
- `request_body_smoke_verified=true`
- `production_ready`, `full_matrix_ready`, `crs_complete` und
  `response_body_verified` bleibt falsch.

Erwartetes minimales CRS-PASS-Ergebnis mit lokalem Traefik, lokaler libmodsecurity und
lokales CRS:

- Entscheidungs-Backend: `libmodsecurity`
- Regelsatz: `crs`
- CRS-Version/Referenz: aus der von common.sh verwalteten CRS-Quelle, zum Beispiel `v4.26.0`
- CRS-Laufzeitverzeichnis: `$TRAEFIK_RESULT_ROOT/crs-smoke`
- Zulässiger Anforderungsstatus: `200`
- Blockierter Anforderungsstatus: `403`
- Beobachtete CRS-Regel-ID/-Nachricht: aus libmodsecurity-Eingriffsnachweisen
- `crs_minimal_smoke_verified=true`
- `production_ready`, `full_matrix_ready`, `crs_complete` und
  `response_body_verified` bleibt falsch.

Erwartetes sekundäres CRS-PASS-Ergebnis mit lokalem Traefik, lokaler libmodsecurity,
und lokales CRS:

- Entscheidungs-Backend: `libmodsecurity`
- Regelsatz: `crs`
- CRS-Smoke-Case: `secondary`
- CRS-Laufzeitverzeichnis: `$TRAEFIK_RESULT_ROOT/crs-secondary-smoke`
- Zulässiger Anforderungsstatus: `200`
- Blockierter Anforderungsstatus: `403`
- Beobachtete CRS-Regel-ID/-Nachricht: extrahiert aus Audit-/Interventionsnachweisen
- `crs_secondary_smoke_verified=true`
- `production_ready`, `full_matrix_ready`, `crs_complete` und
  `response_body_verified` bleibt falsch.

Es wird keine globale Installation versucht. So führen Sie eine vorbereitete lokale Binärdatei aus:

```sh
TRAEFIK_BIN=/lokaler/pfad/traefik make smoke-traefik
```

## Kanonische Phase-4-Validierung

Traefik `forwardAuth` wird vor der Upstream-Verarbeitung ausgeführt und kann die nicht überprüfen
später vorgelagerte Antwortstelle.  Daher `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` sind hierfür `unsupported_by_host_model`
Integration.

Alle gemeinsam genutzten Phase-4-Fälle müssen als `UNSUPPORTED` mit dem expliziten ausgegeben werden
ForwardAuth-Grenze.  Anforderungsseitige 200/403-Ergebnisse, `forwardBody`-Probes und
Entscheidungsdienst-Selbsttests begründen keine Reaktion-Körper-Inspektion,
Pre-Commit-Antwort verweigern, späte Protokollierung, später Abbruch oder Original/sichtbar
Antwortstatus-Metadaten.  `UNSUPPORTED` zählt nie als `PASS` und Ereignisse
und Berichte bestehen weiterhin nur aus Metadaten.
