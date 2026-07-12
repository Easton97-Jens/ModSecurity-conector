> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Vorlagenüberprüfung: NGINX und Apache

**Sprache:** [English](README.md) | Deutsch

Status: überprüft

In dieser Berichtsmappe werden die Nachweisarbeiten zum Drehen des Verbinders dokumentiert
Vorlage in Apache- und NGINX-Connector-Dokumentation, externe Testregeln,
Laufzeitnachweise, CRS/No-CRS Testzielergebnisse und Gerüstentscheidungen.

## Aktueller Stand

- Documentation/decision Commit-Bereitschaft: Ja.
- Testordner für lokale Connectors fehlen:
  `connectors/_template/tests`, `connectors/apache/tests` und
  `connectors/nginx/tests`, `connectors/envoy/tests` und
  `connectors/haproxy/tests`.
- Ausführbare Connector-Tests sind Framework-eigene und nicht Connector-lokale Tests.
- Tatsächlicher Framework-Pfad: `modules/ModSecurity-test-Framework`.
- Aktuelles Framework-Commit, auf das vom übergeordneten Element verwiesen wird:
  `4bec4d960fea89525db9e439ea567df15943a2e7`.
- Framework-local `make lint`: PASS.
- Framework-local `make quick-check`: Ziel nicht gefunden; Framework-lokal
  `make check-test-matrix` wurde ausgeführt und beendet 0.
- Aktuelle `/src` `make smoke-common`: Apache 54 PASS, 0 FAIL, 0 BLOCKED;
  NGINX 54 PASS, 0 FAIL, 0 GESPERRT.
- Aktuelle `/src` `make smoke-nginx` Gesamtbereich: NGINX 60 PASS, 0 FAIL,
  0 GESPERRT.
- Aktuelle `/src` `make test-no-crs`: PASS; Apache 54 PASS und NGINX 60 PASS.
- Aktuelle `/src` `make test-with-crs`: PASS; Apache 55 PASS und NGINX
  61 PASS, beide 0 FAIL und 0 BLOCKIERT.
- `action_status_401_phase1_block`: für aktuelle `/src`-Läufe von a behoben
  begrenzte With-CRS-Erwartung. No-CRS bleibt 401/401 PASS; With-CRS ist
  403/403 PASS.
- Aktuelles With-CRS `crs_sqli_anomaly_block`: PASS für Apache und NGINX.
- Aktuelle HAProxy-Matrix: `make runtime-matrix-haproxy` zeichnet 141 YAML-Zeilen auf
  mit 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE und 10 MAPPED_ONLY
  Einträge; geteilte no-CRS/with-CRS Artefakte werden separat erfasst.
- Historische NGINX 11 BLOCKED Zeilen waren ein Docroot permission/environment
  Blocker und werden in den aktuellen `/src`-Läufen behoben.
- RESPONSE_BODY Blockierung bleibt nicht verifiziert.
- Eine vollständige Laufzeitüberprüfung bleibt bestehen.
- `connectors/lighttpd` verfügt jetzt über einen Repo-eigenen Decision-Service-Bridge-Starter,
  verwendet global/shared Connector-Gates, hat keinen Laufzeitnachweis und keinen lokalen
  `connectors/lighttpd/tests` Ordner.

## Wichtige Berichte

- `connector-scaffold-decisions.md`: Akzeptierte und zurückgestellte Gerüstentscheidungen.
- `template-evaluation.md`: Eignungsbewertung der Vorlage.
- `apache-evaluation.md`: Apache-Connector-Evaluierung.
- `nginx-evaluation.md`: NGINX Connector-Auswertung.
- `apache-template-alignment.md`: Phasenweise Ausrichtung von Apache gegenüber dem
  aktuelle Template-Tore.
- `nginx-template-alignment.md`: NGINX Phasenweise Ausrichtung gegen die
  aktuelle Template-Tore.
- `envoy-template-alignment.md`: Envoy Bridge-Starter-Ausrichtung gegen die
  aktuelle Template-Tore.
- `lighttpd-template-alignment.md`: Lighttpd Bridge-Starter-Ausrichtung gegen
  die aktuellen Template-Gates.
- `verified-runtime-run.md`: aktuelle `/src` Laufzeitnachweise, einschließlich
  Abschnitte ohne CRS und mit CRS.
- `nginx-docroot-permission-analysis.md`: NGINX Ursache und Behebung des Docroot-Blockers.
- `nginx-blocked-runtime-cases.md`: historische 11 BLOCKED Zeilen und aktuell
  Auflösung.
- `crs-action-status-401-analysis.md`: With-CRS 401/403 Erwartung aufgelöst
  Analyse für `action_status_401_phase1_block`.
- `nginx-build-fail-analysis.md`: früherer NGINX Include-Pfad-Build-Fehler und
  Überprüfung des Bauvertrags.
- `summary.md`: Endgültige Zusammenfassung und Bereitschaftsstatus.
- `findings.md`: Repository-gestützte Ergebnisse.
- `open-questions.md`: verbleibende zurückgestellte Posten.
- `files-reviewed.md`: überprüfte Dateien und Nachweispfade.

## Bewertungsergebnisse

| Target | Rating |
| --- | --- |
| `connectors/_template` | suitable scaffold, not runtime-verified |
| `connectors/apache` | aligned with Template gates for executed scope; runtime status partial |
| `connectors/nginx` | aligned with Template gates for executed scope; runtime status partial |
| `connectors/envoy` | bridge-starter; runtime status not-verified |
| `connectors/haproxy` | spoa-agent-starter; runtime status partial HAProxy matrix |
| `connectors/lighttpd` | bridge-starter only; runtime status not-verified |

Für die Vorlage bedeutet `suitable scaffold, not runtime-verified`, dass es sich um eine handelt
nutzbares Gerüst für neue Konnektoren, keine produktive Konnektorimplementierung.
Ursprung, Metadaten, Build, No-CRS, With-CRS, Coverage-Matrix und Laufzeit
Je konkrete Connector sind Nachweise erforderlich. Für Apache und NGINX, `partial`
bedeutet nicht, dass es gescheitert ist. Dies bedeutet, dass einige Laufzeitnachweise vorhanden sind, jedoch nur das Minimum
Die Matrix für die Promotion über den Teilbereich hinaus ist nicht vollständig.

## CRS Und No-CRS

No-CRS- und With-CRS-Ergebnisse werden separat dokumentiert:

- No-CRS: aktuelles `/src` Ziel PASS für Apache und NGINX.
- With-CRS: aktuelles `/src` Ziel PASS für Apache und NGINX.
- Detaillierte 401/403-Analyse: `crs-action-status-401-analysis.md`.
- CRS SQLi-Anomalie: aktueller With-CRS-Fall PASS für beide Konnektoren.

Die frühere Nichtübereinstimmung des With-CRS-Status wird nicht als Adapterfehler behandelt. Es ist
gelöst durch variantenspezifische Framework-Erwartungen.

## RESPONSE_BODY

RESPONSE_BODY Blockierung ist nicht verifiziert. Die aktuellen `response_body_pass` Zeilen
sind nur Pass-Through-Nachweise und NGINX-spezifische Phase-4-Zeilen in der aktuellen Version
Zusammenfassungen sind pass-through/log-only Nachweise. Ein Sperranspruch bedarf weiterhin a
echter Antwortkörper-Blockierungstestfall, erwarteter Blockierungsauslöser, tatsächlich
Blockierungsergebnis wie HTTP 403, logs/reports, Befehl und pro Connector
Nachweise.

## Envoy Scaffold-Nachtrag

- `connectors/envoy` wurde vom reinen Metadaten-Build-Starter zu einem lokalen sidecar/HTTP-Bridge-Starter erweitert.
- Envoy folgt den gemeinsamen Connectortoren
  `connector-scaffold-decisions.md` und die globale Matrixsemantik in
  `connectors/_template/docs/coverage-decision-matrix.md`.
- Envoy verfügt über Bridge-Starter-Code und Metadaten, noch keine Runtime-Nachweise und nein
  lokaler `connectors/envoy/tests`-Ordner.
- Envoy-spezifische Dateien enthalten Connector-spezifische Bridge-Starter-Status und
  Verweise auf global/shared-Regeln, anstatt diese Regeln zu duplizieren.

## Envoy Build-Starter-Nachtrag

- Envoy-Build-Status: `bridge-starter` für lokale sidecar/HTTP Bridge-Kompilierung.
- Envoy-Laufzeitstatus: `not-verified`; Es wurde kein Envoy-Laufzeit-Harness ausgeführt.
- Ausgewählter minimaler Pfad: Repository-lokales Bridge-Entscheidungsmodell, kompiliert mit
  `common/` Hilfscode.
- Zurückgestellte Produktionspfade: nativer Envoy HTTP-Filter, ext_proc-Dienst,
  Proxy-Wasm-Modul und sidecar/bridge Integration bis zu ihrer tatsächlichen
  Es bestehen Abhängigkeiten und Nutzungsnachweise.

## Envoy Bridge-Starter-Nachtrag

- Status der Envoy-Brücke: lokaler CLI Selbsttest PASS für allow/block Entscheidungslogik.
- Envoy-Laufzeitstatus: `not-verified`; Es wurde kein Envoy-Laufzeit-Harness ausgeführt.
- Ausgewählter Integrationspfad: sidecar/HTTP Bridge-Starter, weil nativer Envoy,
  ext_proc- und Proxy-Wasm-Abhängigkeiten fehlen in diesem Repository.
- Fehlende Laufzeitnachweise: Envoy-Konfiguration, Bridge-Integrationspunkt, Framework
Ergebnis JSON, No-CRS/With-CRS aufgeteilt, CRS wirksame Nachweise und RESPONSE_BODY
  Nachweise.
## Aktueller HAProxy-Status

- `connectors/haproxy` enthält jetzt vom Repo erstellte Metadaten und einen lokalen SPOA
  Agentenstarter unter `connectors/haproxy/src/`.
- Aktueller HAProxy-Status: `spoa-agent-starter`.
- Build-Status: Metadaten-Build PASS; lokaler SPOA Starter-Build PASS; lokal
  ModSecurity-verbindlicher Selbsttest PASS; Produktiver Adapteraufbau GESPERRT.
- Selbstteststatus: Lokaler Selbsttest zur synthetischen Anforderung und Entscheidung PASS.
- Laufzeitstatus: `runtime-smoke-verified` für
  `haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`.
- Der Starter verwendet gemeinsame request/intervention/status/origin-Formen. Die
  Der Diagnosepfad verfügt jetzt auch über einen Live-HAProxy für die Diagnose SPOA für libmodsecurity
  Durchsetzungsbeweise für den Header-Block-Fall und den CRS SQLi-Anomaliefall,
  Es wird jedoch keine vollständige SPOE/SPOA-Kompatibilität implementiert oder überprüft
  RESPONSE_BODY.
- CRS-Status: Nur für `haproxy_crs_sqli_anomaly_block` überprüft.
- Es wird kein lokaler `connectors/haproxy/tests`-Ordner verwendet.
- Fehlender breiterer Laufzeitnachweis: vollständige SPOA-Implementierung, breiteres Framework
  Falllaufzeit, breitere CRS Runtime-Nachweise, RESPONSE_BODY Nachweise,
  negative/pass-through-Nachweis, audit/log-Nachweis und Vollmatrix-Nachweis.
- Ausrichtungsbericht: `reports/archive/template-verification-nginx-apache/haproxy-template-alignment.md`.
## lighttpd Bridge-Starter

`connectors/lighttpd` enthält eine Repo-eigene metadata/probe-Quelle sowie eine lokale
Entscheidungsservice-Brückenstarter. Dieser Starter verwendet gemeinsame `common/`
origin/status/intervention/capability Helfer und beinhaltet nicht lighttpd
Header, Lighttpd-APIs aufrufen, FastCGI/SCGI implementieren, ModSecurity-APIs aufrufen oder
Bereitstellung von Laufzeitnachweisen. Ein echter LightTPD-Adapter-Build bleibt blockiert
Fehlender ausgewählter Produktionsintegrationspfad, lighttpd headers/SDK/source oder
Bridge-Abhängigkeiten, ModSecurity-Integrationscode und eine Framework-eigene Laufzeit
Harness.
## Traefik Decision-Service Starter

- `connectors/traefik` wurde vom Metadaten-Build-Starter zu einem erweitert
  Repo-eigener lokaler Entscheidungsservice-Starter.
- Traefik folgt den gemeinsamen Connector-Gates in `connector-scaffold-decisions.md`
  und `connectors/_template/docs/coverage-decision-matrix.md`.
- Traefik verfügt über Selbsttestnachweise für lokale Entscheidungsdienste, keine Laufzeitnachweise und
  kein lokaler `connectors/traefik/tests` Ordner.
- Build/self-test Befehle: `connectors/traefik/build/build-starter.sh` und
  `make -C connectors/traefik self-test-decision-service`.
- Der Laufzeitintegrationspfad bleibt zurückgestellt, bis Traefik API/source/SDK oder HTTP
  Bridge-Laufzeit- und Harnessnachweise werden ausgewählt und dokumentiert.
- Detaillierte Ausrichtung: `traefik-template-alignment.md`.

## Framework Connector-Starter-Prüfungen

`make connector-starter-checks` führt den Framework-eigenen Starter-Check-Runner unter aus
`modules/ModSecurity-test-Framework/ci/runtime/run-connector-starter-checks.sh`.
Der Befehl schreibt lokale Nachweise in
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` und
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

Diese Ergebnisse sind lediglich build/self-test Nachweise. Sie sind nicht Apache/NGINX-style
Runtime-Smoke-Validierung, keine globalen Artefakte installieren, keine lokalen erstellen
`connectors/<name>/tests` Verzeichnisse und verlassen Sie den Laufzeitstatus
`not-verified` für Starterbeweis. RESPONSE_BODY bleibt nicht verifiziert.

## Neue Connector Runtime-Smoke-Einstiegspunkte

Das Framework stellt jetzt Runtime-Smoke-Einstiegspunkte für Envoy, HAProxy,
lighttpd und Traefik über `make smoke-envoy`, `make smoke-haproxy`,
`make smoke-lighttpd` und `make smoke-traefik`. Diese Ziele schreiben Laufzeit
Nachweisdateien gemäß `/src/ModSecurity-conector-build/results/`.

Der aktuelle Status ist PASS für HAProxys bereichsbezogene `haproxy_phase1_header_block` und
`haproxy_crs_sqli_anomaly_block` Runtime-Smoke und BLOCKED für Envoy,
lighttpd und Traefik. Das Aggregat
`make smoke-new-connectors` bleibt diagnosefähig und beendet BLOCKED, während alle neuen
Die Connector-Laufzeit bleibt ungeprüft, anstatt blockierte Zustände als zusammenzufassen
PASS.
