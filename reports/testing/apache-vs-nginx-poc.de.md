# Apache vs. NGINX PoC

**Sprache:** [English](apache-vs-nginx-poc.md) | Deutsch

Status: eingerüstet

## Geteiltes Verhalten

Beide Connector-PoCs verwenden die gleichen tragbaren Fall:

```text
modules/ModSecurity-test-Framework/tests/cases/*.yaml
modules/ModSecurity-test-Framework/tests/cases/*.yaml
modules/ModSecurity-test-Framework/tests/cases/*.yaml
modules/ModSecurity-test-Framework/tests/cases/*.yaml
```

Geteilte Stücke:

- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py materialize` schreibt Connector-Laufzeitregeldateien
  und Anforderungsvariablen aus dem YAML-Fall.
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py assert-status` vergleicht den beobachteten HTTP-Status
  mit `expect.status`.
- Der erwartete Nachweis ist der HTTP-Status, der derzeit in jeder YAML-Datei codiert ist
  HTTP `403` für alle minimalen Blockierungsfälle.

Der gemeinsame Fall ist ein rule/request/expectation-Modell. Es ist kein Nachweis für a
Connector, bis der Laufzeitkabelbaum dieses Connectors die erwarteten HTTP einhält
Status.

`make smoke-common` führt nur diese häufigen Fälle sowohl auf Apache als auch auf NGINX aus.
`make smoke-all` führt auch Connector-spezifische importierte Fälle bei ihrem Abgleich aus
Connector.

Der Proof-Modus für beide PoCs ist `real-world-connector-path`: ein echter HTTP Client
kommuniziert mit einem realen Serverprozess, der Server lädt das reale Connector-Modul, das
Das Modul ruft libmodsecurity auf und die beobachtete HTTP-Antwort muss mit der YAML-Antwort übereinstimmen.
Erwartung. Direkte libmodsecurity API Smoke-Ergebnisse sind separat und nicht
als Connector-Erfolg gezählt.

## Connector-spezifische Teile

Apache:

- Build-Integration verwendet APXS/Autotools aus dem lokalen `ModSecurity-apache`
  Quellkopie.
- Die Laufzeit lädt `mod_security3.so` mit `LoadModule security3_module`.
- Die Konfiguration ermöglicht `modsecurity on` und verweist auf `modsecurity_rules_file`
  die materialisierte Regeldatei.
- Ein von einer lokalen Quelle erstellter Apache-httpd-Smoke hat den von YAML erwarteten HTTP beobachtet.
  Status für alle aktuell freigegebenen Minimalfälle.

NGINX:

- Die Build-Integration verwendet den dynamischen Modulpfad ModSecurity-nginx eines Drittanbieters
  mit `--with-compat --add-dynamic-module=...`.
- Die Laufzeit lädt `ngx_http_modsecurity_module.so` mit `load_module`.
- Die Konfiguration ermöglicht `modsecurity on` und verweist auf `modsecurity_rules_file`
  die materialisierte Regeldatei.
- Ein von einer lokalen Quelle erstellter NGINX-Smoke hat den von YAML erwarteten HTTP-Status beobachtet
  für alle aktuellen gemeinsamen Minimalfälle.
- NGINX-spezifische importierte Fälle derzeit unter `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
  Cover-Umleitung und TX-Scoring-Verhalten aus der lokalen NGINX-Suite. Sie bleiben
  Nur NGINX, bis die Apache-Äquivalenz explizit getestet wird.

## Unterschiede im Lebenszyklus

Apache und NGINX stellen unterschiedliche Hook-Modelle bereit. Der geteilte Runner absichtlich
modelliert keine Haken; es stellt nur die tragbaren Testdaten bereit.

Beobachtete NGINX lokale Quellenfakten:

- Die Zugriffsverwaltung wird in `NGX_HTTP_ACCESS_PHASE` registriert.
- Die Protokollierung wird in `NGX_HTTP_LOG_PHASE` registriert.
- Header- und Body-Filter werden separat installiert.
- Die Verarbeitung des Antworttexts hängt von der Filterreihenfolge NGINX ab.

Apache-Hook-Details bleiben Connector-spezifisch und werden in dokumentiert
`modules/ModSecurity-test-Framework/docs/imports/import-analysis-apache.md` und `reports/testing/apache-poc.md`.

## Unterschiede aufbauen

Der Apache-Source-Build-Modus lädt httpd, APR und APR-util unter herunter und erstellt sie
`BUILD_ROOT`. NGINX Der Source-Build-Modus lädt die offizielle GitHub-Version herunter
Archiv aus `nginx/nginx`, erstellt NGINX unter `BUILD_ROOT` und schreibt das
dynamisches Modul unter:

```text
$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so
```

Keiner von PoC schreibt an `/usr`, `/usr/local`, `/etc/apache2`, `/etc/nginx` oder
`<external-source-root>/*`.

## Aktueller lokaler Vergleich

Beobachtet am 15.05.2026 mit `BUILD_ROOT=/src/ModSecurity-conector-build`:

| Shared case | Apache, httpd 2.4.67 | NGINX, nginx 1.31.0 from `release-1.31.0` |
| --- | --- | --- |
| `audit_log_phase1_block.yaml` | HTTP 403 plus audit fields | HTTP 403 plus audit fields |
| `phase1_header_block.yaml` | HTTP 403 | HTTP 403 |
| `phase2_args_block.yaml` | HTTP 403 | HTTP 403 |
| `phase2_args_pass.yaml` | HTTP 200 plus origin body | HTTP 200 plus origin body |
| `request_body_json_block.yaml` | HTTP 403 | HTTP 403 |
| `request_body_urlencoded_block.yaml` | HTTP 403 | HTTP 403 |
| `response_header_basic.yaml` | HTTP 403 | HTTP 403 |

Dies beweist, dass diese gemeinsamen PoC-Fälle nur für diesen Arbeitsbereich gelten. Breiter
Für die Kompatibilität ist weiterhin eine steckerspezifische Regressionsabdeckung erforderlich.

Importierte häufige Fälle fügen Phasenaktion, Sammlung und Anforderungstextabdeckung hinzu.
Ihre Quellpfade und Portabilitätsentscheidungen sind in dokumentiert
`docs/imports/common/shared-case-origin-map.md` und `framework test import plan`.
Die lokalen `make smoke-all` laufen am 15.05.2026 nach dem V2/V3-Importdurchlauf
gemeldet, dass 30 Apache erfolgreich ist und 33 NGINX erfolgreich ist. Der Unterschied liegt in der 3
NGINX-spezifische importierte Fälle, die nicht auf Apache ausgeführt werden.

V2/V3-derived Häufige Fälle fügen Semantik- und Regressionsabdeckung hinzu, ohne zu kopieren
Upstream-Tests:

| Shared group | Apache | NGINX | Notes |
| --- | --- | --- | --- |
| V2 operators/transformations | HTTP 403 | HTTP 403 | Derived from `ModSecurity_V2/tests/op` and `tests/tfn` |
| V3 multipart FILES variables | HTTP 403 | HTTP 403 | Derived from v3 `variable-FILES*` and `variable-MULTIPART_FILENAME` JSON cases |
| V3 XML body processor | HTTP 403 | HTTP 403 | Basic XML collection check only; schema/DTD remains mapped |
| V3 operator/action basics | HTTP 403 | HTTP 403 | Derived from `operator-rx.json`, `transformations.json`, and `secruleengine.json` |

## Body- und Multipart-Import

Der Shared Runner materialisiert nun deterministische mehrteilige Körper und pro Fall
Antwortvorrichtungen unter jedem Connector-Laufzeitverzeichnis. Das aktive Gemeinsame
body/filter Ergänzungen sind:

| Shared case | Apache | NGINX | Notes |
| --- | --- | --- | --- |
| `json_request_body_block.yaml` | HTTP 403 | HTTP 403 | Raw `REQUEST_BODY` match; parsed JSON collections remain mapped |
| `multipart_basic_block.yaml` | HTTP 403 | HTTP 403 | Simple multipart text-field match through `ARGS:name` |
| `response_body_pass.yaml` | HTTP 200 | HTTP 200 | Response-body access pass-through only |

`response_body_basic_block` ist kein aktiver gemeinsamer PASS. NGINX hat das erkannt
Antwortkörperregel bei der lokalen Prüfung, aber die HTTP-Antwort war nicht stabil
403 und der Upstream-Test NGINX markiert den Blockfall TODO. Es bleibt dokumentiert
als xfail/mapped-only, bis beide Konnektoren den gleichen stabilen HTTP 403 zurückgeben.

## Zusammenfassende Metadaten

Zu den Apache- und NGINX-Zusammenfassungen unter `$BUILD_ROOT/results/` gehören:

- `connector_path: real-world`
- `validation_mode: real-world-connector-path`
- Binärpfad des Servers
- Pfad des Connectormoduls
- Pfad der gemeinsam genutzten libmodsecurity-Bibliothek
- `verified_variables` werden nur aus dem Bestehen von YAML-Fällen abgeleitet

Die derzeit verifizierten realen Variablenfamilien sind `ARGS`,
`REQUEST_HEADERS`, `REQUEST_BODY`, `FILES`, `XML`, `AUDIT_LOG` und
`RESPONSE_HEADERS`. `RESPONSE_BODY` bleibt bis zu einem Antworttext ausgeschlossen
Regelvariable case übergibt beide Konnektoren.
