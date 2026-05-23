# Shared Features

Diese Dokumentation beschreibt die gemeinsamen Funktionen und Konzepte des
ModSecurity-Connector-Monorepos. Sie basiert auf dem aktuellen Repository-Stand
und auf den vorhandenen Quellen und Dokumenten. Wo die Codebasis keine
gemeinsame Runtime-Implementierung belegt, wird das ausdrücklich so benannt.

## Überblick

Mit „Shared Features“ sind in diesem Projekt nicht alle Apache- und
Nginx-Laufzeitpfade gemeint. Die gemeinsame Schicht liegt vor allem in
connector-neutralen Datenformen, Direktivenamen, Optionswerten,
Rule-Load-Statistiken, Metadaten und Test-/Reporting-Konzepten. Die echten
Server-Integrationen bleiben adapter-eigen:

- Apache besitzt eigene Hooks, Filter, APXS-/Autotools-Buildlogik und
  Konfigurationsparser unter `connectors/apache/`.
- Nginx besitzt eigene Nginx-Phasenhandler, Header-/Body-Filter,
  Third-Party-Module-Buildlogik und Konfigurationsparser unter
  `connectors/nginx/`.
- `common/` enthält neutrale Header und kleine Hilfsfunktionen, aber keine
  Apache- oder Nginx-SDK-Typen und keine libmodsecurity-Transaktionslogik.

Gemeinsame Features sind wichtig, weil beide produktiven Connectoren dieselben
ModSecurity-Konzepte bereitstellen sollen: Aktivierung, Rules-Dateien,
Inline-Regeln, Remote-Regeln, Transaktions-ID, Error-Log-Policy,
Rule-Load-Metadaten und eine vergleichbare Testauswertung. Gemeinsame
Metadaten vermeiden, dass Direktivenamen oder Statusbegriffe zwischen
Connectoren auseinanderlaufen, ohne die sehr unterschiedlichen Server-APIs zu
vermischen.

Relevante projektübergreifende Teile:

| Pfad | Rolle |
| --- | --- |
| `common/include/msconnector/directives.h` | Gemeinsame Direktivenamen |
| `common/include/msconnector/options.h` | Gemeinsame boolsche Werte, Defaults und Optionsnamen |
| `common/include/msconnector/rule_load_stats.h` | Gemeinsame Datenform für geladene Regeln |
| `common/include/msconnector/request.h` | Neutrale Request-Datenform |
| `common/include/msconnector/response.h` | Neutrale Response-Datenform |
| `common/include/msconnector/transaction.h` | Neutrale Phasen- und Transaktionssicht |
| `common/include/msconnector/intervention.h` | Neutrale Interventionsdatenform |
| `common/include/msconnector/status.h` | Neutrale Statuswerte |
| `common/include/msconnector/capabilities.h` | Neutrale Capability-Flags |
| `common/include/msconnector/origin.h` | Neutrale Herkunfts-/Provenance-Datenform |
| `common/src/` | Kleine Implementierungen für Status, Intervention, Origin und Capabilities |
| `modules/ModSecurity-test-Framework/` | Gemeinsame YAML-Fälle, Runner, Normalizer und Smoke-Helfer |

## Gemeinsame Architektur

Die Architektur ist bewusst zweigeteilt:

1. `common/` definiert neutrale Formen und Konstanten.
2. `connectors/apache/` und `connectors/nginx/` übersetzen konkrete
   Serverzustände in libmodsecurity-Aufrufe.

Die Datei `docs/architecture/architecture.md` beschreibt den Zielablauf:

1. Ein Server-Hook oder Filter erhält Request-/Response-Zustand.
2. Der Connector-Adapter übersetzt diesen Zustand in eine Form, die an
   libmodsecurity übergeben werden kann.
3. Der Adapter ruft die libmodsecurity-v3-C-API in Phasen auf.
4. Interventions werden zurück in Serververhalten übersetzt.
5. Connector-spezifische Tests belegen Timing, Artefakte und HTTP-Verhalten.

Die gemeinsamen Header enthalten keine Apache-Typen wie `request_rec`, keine
Nginx-Typen wie `ngx_http_request_t` und keine Ownership-Regeln für
`ModSecurity`, `RulesSet` oder `Transaction`. Diese Grenze ist in
`docs/architecture/common-runtime-boundaries.md` ausdrücklich dokumentiert.

### Beziehung zu libmodsecurity

Beide Connectoren verwenden libmodsecurity v3 über die öffentliche C-API. In
den lokalen Quellen sind unter anderem diese Aufrufarten sichtbar:

- Initialisierung mit `msc_init`,
- Connector-Information über `msc_set_connector_info`,
- Log-Callback über `msc_set_log_cb`,
- Rules-Erzeugung über `msc_create_rules_set`,
- Rules-Laden über `msc_rules_add`, `msc_rules_add_file` und
  `msc_rules_add_remote`,
- Rules-Merge über `msc_rules_merge`,
- Transaktion über `msc_new_transaction` oder
  `msc_new_transaction_with_id`,
- Request-Phasen über `msc_process_connection`, `msc_process_uri`,
  `msc_add_request_header`/`msc_add_n_request_header`,
  `msc_process_request_headers`, `msc_append_request_body` und
  `msc_process_request_body`,
- Response-Phasen über `msc_add_response_header`/
  `msc_add_n_response_header`, `msc_process_response_headers`,
  `msc_append_response_body` und `msc_process_response_body`,
- Logging über `msc_process_logging`,
- Interventions über `msc_intervention`.

Diese API-Nutzung ist konzeptionell gemeinsam, aber die konkreten Hooks,
Zeitpunkte, Buffer und Fehlerpfade sind connector-spezifisch.

### Gemeinsame Initialisierung

Beide produktiven Connectoren erzeugen eine ModSecurity-Instanz und setzen
Connector-Informationen:

- Apache verwendet in `connectors/apache/src/mod_security3.c`
  `msc_apache_init`, `msc_init`, `msc_set_connector_info` und
  `msc_set_log_cb`.
- Nginx verwendet in `connectors/nginx/src/ngx_http_modsecurity_module.c`
  `ngx_http_modsecurity_create_main_conf`, `msc_init`,
  `msc_set_connector_info` und `msc_set_log_cb`.

Die Initialisierung ist also fachlich vergleichbar, aber nicht als gemeinsame
Funktion in `common/src/` implementiert.

### Gemeinsames Laden von Konfigurationen und Regeln

Beide Connectoren registrieren gemeinsame Direktivenamen aus
`common/include/msconnector/directives.h`:

- `modsecurity`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log`

Nginx registriert zusätzlich Nginx-spezifische Phase-4-Direktiven:

- `modsecurity_phase4_mode`
- `modsecurity_phase4_content_types_file`
- `modsecurity_phase4_log`

Das Laden der Regeln erfolgt in beiden Connectoren über libmodsecurity, aber in
eigenen Parserfunktionen:

- Apache: `connectors/apache/src/msc_config.c`
- Nginx: `connectors/nginx/src/ngx_http_modsecurity_module.c`

## Konfigurationshandling

Die gemeinsame Konfigurationsebene ist eine Metadaten- und
Direktivenamen-Ebene. Die eigentliche Server-Konfiguration bleibt
connector-spezifisch.

### Gemeinsame Direktiven

`common/include/msconnector/directives.h` definiert die Namen der Direktiven.
Dadurch verwenden Apache und Nginx dieselben Schreibweisen im Code:

```c
#define MSCONNECTOR_DIRECTIVE_MODSECURITY "modsecurity"
#define MSCONNECTOR_DIRECTIVE_RULES "modsecurity_rules"
#define MSCONNECTOR_DIRECTIVE_RULES_FILE "modsecurity_rules_file"
#define MSCONNECTOR_DIRECTIVE_RULES_REMOTE "modsecurity_rules_remote"
#define MSCONNECTOR_DIRECTIVE_TRANSACTION_ID "modsecurity_transaction_id"
#define MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG "modsecurity_use_error_log"
```

Die Registrierung ist trotzdem unterschiedlich:

- Apache nutzt `AP_INIT_TAKE1` und `AP_INIT_TAKE2` in
  `connectors/apache/src/msc_config.c`.
- Nginx nutzt ein `ngx_command_t`-Array in
  `connectors/nginx/src/ngx_http_modsecurity_module.c`.

### Aktivieren und Deaktivieren

Die Direktive `modsecurity on|off` ist in beiden Connectoren vorhanden.
Der gemeinsame Default aus `common/include/msconnector/options.h` ist:

```c
#define MSCONNECTOR_DEFAULT_ENABLE MSCONNECTOR_BOOL_OFF
```

Das bedeutet: Ohne Aktivierung verarbeitet der Connector Requests nicht als
ModSecurity-geschützte Requests. Der konkrete Scope unterscheidet sich:

- Apache registriert die Direktive für Server- und Directory-Kontexte
  (`RSRC_CONF | ACCESS_CONF`).
- Nginx registriert sie für Main-, Server- und Location-Kontexte
  (`NGX_HTTP_MAIN_CONF`, `NGX_HTTP_SRV_CONF`, `NGX_HTTP_LOC_CONF`).

### Rules-Dateien und Inline-Regeln

Beide Connectoren unterstützen:

- `modsecurity_rules` für Inline-Regeln,
- `modsecurity_rules_file` für lokale Regeldateien,
- `modsecurity_rules_remote` für Remote-Regeln.

Die geladenen Regeln werden in einem RulesSet gehalten und bei
Konfigurations-Merges zusammengeführt. Fehler beim Laden werden nicht
verschluckt:

- Apache gibt bei einem negativen Rückgabewert von `msc_rules_add*` den
  libmodsecurity-Fehlerstring an Apache zurück.
- Nginx gibt bei Fehlern im Konfigurationspfad ebenfalls eine Fehlermeldung
  zurück, wodurch `nginx -t` oder der Start fehlschlägt.

### Rule-Load-Statistiken

`common/include/msconnector/rule_load_stats.h` definiert:

```c
typedef struct msconnector_rule_load_stats {
    unsigned inline_rules;
    unsigned file_rules;
    unsigned remote_rules;
} msconnector_rule_load_stats;
```

Diese Werte zählen geladene Regeln, nicht die Anzahl der Direktiven. Sie werden
nur nach erfolgreichen `msc_rules_add*`-Aufrufen erhöht.

Aktueller Stand:

- Apache speichert die Werte in `msc_conf_t` und addiert sie beim
  Directory-Config-Merge. Sie werden derzeit nicht im Post-Config-Log
  ausgegeben.
- Nginx hält lokale Counter `rules_inline`, `rules_file` und `rules_remote` und
  kopiert sie über einen kleinen Helper in `msconnector_rule_load_stats`.
  Nginx gibt diese Werte im Startup-Log aus.

Die Statistiken ändern keine Runtime-Entscheidung. Sie sind Metadaten.

### Transaktions-ID

Beide Connectoren unterstützen `modsecurity_transaction_id`, aber mit
unterschiedlicher Semantik:

- Apache akzeptiert eine statische Zeichenkette. Wird keine Direktive gesetzt,
  versucht der Connector `UNIQUE_ID` zu verwenden und fällt danach auf eine
  Transaktion ohne explizite ID zurück.
- Nginx verwendet eine Nginx Complex Value. Dadurch können Nginx-Variablen pro
  Request ausgewertet werden.

Das ist ein bekanntes, dokumentiertes Unterschiedsmerkmal und keine
gemeinsame Runtime-Implementierung.

### Error-Log-Policy

`modsecurity_use_error_log on|off` ist in beiden Connectoren vorhanden. Der
Default aus `common/include/msconnector/options.h` ist:

```c
#define MSCONNECTOR_DEFAULT_USE_ERROR_LOG MSCONNECTOR_BOOL_ON
```

`off` unterdrückt die Weiterleitung des libmodsecurity-Log-Callbacks in das
jeweilige Server-Error-Log. Es deaktiviert nicht:

- Audit Logging,
- Interventions,
- Request-Verarbeitung,
- Response-Verarbeitung,
- Rules-Laden,
- Transaktionsanlage.

## Request Processing

Beide Connectoren bilden eingehende Requests auf libmodsecurity-Transaktionen
ab. Die gemeinsamen fachlichen Schritte sind:

1. Transaktion erstellen.
2. Connection-Metadaten verarbeiten.
3. URI, Methode und HTTP-Version verarbeiten.
4. Request-Header an libmodsecurity übergeben.
5. Request-Body an libmodsecurity übergeben, wenn vorhanden und zugänglich.
6. Nach relevanten Phasen Interventions prüfen.

### Apache

Apache registriert in `connectors/apache/src/mod_security3.c` unter anderem:

- `ap_hook_pre_config`,
- `ap_hook_post_config`,
- `ap_hook_post_read_request`,
- `ap_hook_fixups`,
- `ap_hook_insert_filter`,
- `ap_hook_log_transaction`,
- Input-Filter `MODSECURITY_IN`,
- Output-Filter `MODSECURITY_OUT`.

Die Transaktion wird in `create_tx_context` erzeugt. Request-Header werden in
`process_request_headers` über `r->headers_in` iteriert und an
libmodsecurity übergeben. Request-Body-Daten laufen über den Input-Filter in
`connectors/apache/src/msc_filters.c`, der `msc_append_request_body` und
`msc_process_request_body` aufruft.

### Nginx

Nginx registriert in `ngx_http_modsecurity_init` Handler für:

- `NGX_HTTP_ACCESS_PHASE`,
- `NGX_HTTP_LOG_PHASE`,
- Header-Filter,
- Body-Filter.

Die Transaktion wird in `ngx_http_modsecurity_create_ctx` erzeugt. Im
Access-Handler verarbeitet Nginx:

- Client-/Server-Adresse und Ports,
- Hostname, soweit verfügbar und libmodsecurity-Version passend,
- URI, Methode und HTTP-Version,
- Request-Header über `r->headers_in.headers`,
- Request-Body über `ngx_http_read_client_request_body`, In-Memory-Buffer oder
  temporäre Datei.

### Gemeinsamkeiten und Unterschiede

Gemeinsam ist die libmodsecurity-Phasenidee. Unterschiedlich sind Timing,
Buffering und Server-APIs:

- Apache arbeitet mit `request_rec`, APR-Tabellen und Bucket Brigades.
- Nginx arbeitet mit `ngx_http_request_t`, Nginx-Listen, Chains und
  Request-Body-Callbacks.
- Apache besitzt eine statische Transaktions-ID-Option mit `UNIQUE_ID`-Fallback.
- Nginx kann Transaktions-IDs über Nginx-Variablen pro Request erzeugen.

`common/include/msconnector/request.h` definiert zwar eine neutrale
Request-Datenform, aber die produktiven Connectoren verwenden aktuell ihre
eigenen Serverdaten direkt in ihren Adapterpfaden. Die neutrale Datenform ist
keine vollständig extrahierte Runtime-API.

## Response Processing

Beide Connectoren enthalten Code, der Response-Header und Response-Body an
libmodsecurity weitergibt. Dieser Bereich ist im Projekt besonders vorsichtig
dokumentiert, weil Response-Body-Blocking und späte Interventions stark vom
Server-Filtermodell abhängen.

### Apache

Der Apache-Output-Filter in `connectors/apache/src/msc_filters.c`:

- liest `r->err_headers_out`,
- liest `r->headers_out`,
- ruft `msc_add_response_header`,
- ruft `msc_process_response_headers`,
- iteriert über die Bucket Brigade,
- ruft `msc_append_response_body`,
- ruft `msc_process_response_body`,
- prüft Interventions.

Die README weist darauf hin, dass Apache-Response-Body-Verhalten nicht
promoted ist und `RESPONSE_BODY` nicht als verifizierte Blocking-Capability
behandelt wird.

### Nginx

Der Nginx-Header-Filter in
`connectors/nginx/src/ngx_http_modsecurity_header_filter.c` übergibt
Standard- und Listenheader an libmodsecurity und ruft
`msc_process_response_headers`.

Der Nginx-Body-Filter in
`connectors/nginx/src/ngx_http_modsecurity_body_filter.c` übergibt
Response-Body-Chunks an `msc_append_response_body` und ruft am Ende
`msc_process_response_body`. Zusätzlich gibt es Nginx-spezifische Phase-4-
Direktiven für spätes Interventionsverhalten:

- `modsecurity_phase4_mode minimal|safe|strict`,
- `modsecurity_phase4_content_types_file <path>`,
- `modsecurity_phase4_log <path>`.

Diese Direktiven sind ausdrücklich Nginx-spezifisch und nicht Teil eines
gemeinsamen Apache/Nginx-Vertrags.

### Gemeinsame Limitierungen

Aus den vorhandenen Dokumenten ergibt sich:

- Response-Header-Verarbeitung ist in beiden Connectoren implementiert.
- Response-Body-Pfade existieren in beiden Connectoren.
- Stabiles Response-Body-Blocking ist nicht als gemeinsame verifizierte
  Capability promotet.
- Unterschiede im Filterzeitpunkt können zu unterschiedlichem Verhalten führen,
  besonders wenn Header bereits gesendet wurden.

## Logging und Audit Logging

Beide Connectoren setzen einen libmodsecurity-Log-Callback:

- Apache: `modsecurity_log_cb`,
- Nginx: `ngx_http_modsecurity_log`.

Diese Callbacks schreiben in das jeweilige Server-Error-Log, sofern
`modsecurity_use_error_log` nicht auf `off` gesetzt wurde.

Audit Logging wird nicht durch eine eigene gemeinsame Connector-Schicht
erzeugt. Es wird über libmodsecurity und die geladenen ModSecurity-Regeln
gesteuert, zum Beispiel über Direktiven wie:

```apache
SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog /var/log/modsec_audit.log
```

Die Smoke-Harnesses materialisieren Audit-Log-Pfade in generierten
Runtime-Verzeichnissen:

- Nginx-Harness: `connectors/nginx/harness/run_nginx_smoke.sh`,
- Apache-Harness: `connectors/apache/harness/run_apache_smoke.sh`.

Debugging-Hinweise:

- Bei fehlenden Error-Log-Meldungen zuerst `modsecurity_use_error_log` prüfen.
- Bei fehlenden Audit-Logs zuerst `SecAuditEngine`, `SecAuditLog`,
  Dateirechte und Worker-Benutzer prüfen.
- Bei Nginx zusätzlich prüfen, ob `modsecurity_phase4_log` gesetzt ist, wenn
  Phase-4-Diagnosen erwartet werden.
- Bei Helper-Builds liegen Build-Logs und Runtime-Logs unter `BUILD_ROOT`.

## Error Handling

Fehlerbehandlung ist fachlich ähnlich, aber technisch connector-spezifisch.

### Fehlerhafte Regeln

Beim Laden von Regeln geben `msc_rules_add`, `msc_rules_add_file` und
`msc_rules_add_remote` einen negativen Wert und einen Fehlerstring zurück, wenn
libmodsecurity die Regel nicht akzeptiert.

- Apache gibt diesen Fehlerstring aus dem Config-Handler zurück. Dadurch kann
  der Apache-Configtest fehlschlagen.
- Nginx gibt im Konfigurationsparser einen Fehler zurück. Dadurch schlägt
  `nginx -t` oder der Start fehl.

Rule-Load-Stats werden nur bei erfolgreichen Ladevorgängen erhöht.

### Fehlende oder ungültige Konfiguration

Wenn `modsecurity` nicht aktiviert ist, lehnen die Runtime-Pfade die
Verarbeitung ab und lassen den Request durch den normalen Serverpfad laufen.
Das ist kein Fehler, sondern der dokumentierte Default.

Wenn eine Rules-Datei nicht lesbar ist, eine Remote-Regel nicht geladen werden
kann oder eine Regel syntaktisch ungültig ist, wird die Server-Konfiguration
typischerweise nicht erfolgreich geladen.

### Interne ModSecurity-Fehler

Interventions werden in beiden Connectoren nach relevanten Phasen geprüft:

- Apache verwendet `process_intervention` und gibt bei disruptiven
  Interventions HTTP-Status oder Redirect-Verhalten an Apache zurück.
- Nginx verwendet `ngx_http_modsecurity_process_intervention` und übersetzt
  Status oder Redirect in Nginx-Verhalten. Bei spät erkannten
  Response-Body-Interventions gelten zusätzlich Nginx-spezifische Phase-4-
  Regeln.

Bei internen Fehlern im Connector, zum Beispiel fehlendem Transaktionskontext,
können beide Connectoren mit Serverfehlern oder Filterfehlern reagieren. Diese
Pfade sind nicht in `common/` vereinheitlicht.

## Build- und Runtime-Abhängigkeiten

Gemeinsame Abhängigkeiten:

- C-Compiler,
- Make,
- libmodsecurity-v3-Header,
- `libmodsecurity.so`,
- ModSecurity-Regeln,
- passende Runtime-Library-Suchpfade.

Nginx-spezifisch:

- Nginx-Quellcode,
- Nginx-Build-Abhängigkeiten wie PCRE/PCRE2, zlib und optional OpenSSL,
- Nginx-Third-Party-Module-Konfiguration `connectors/nginx/config`,
- dynamische Modulkompatibilität zwischen Modul und Ziel-Nginx.

Apache-spezifisch:

- Apache/httpd,
- Apache-Development-Paket,
- `apxs` oder `apxs2`,
- APR/APR-util,
- Autotools für den Build aus `connectors/apache/`.

Die vorhandenen Makefile-Ziele delegieren an das Test-Framework:

```sh
make smoke-nginx
make smoke-apache
make smoke-all
make runtime-matrix-all
```

Die Default-Buildpfade liegen unter:

```text
$HOME/.local/state/ModSecurity-conector-build
```

oder unter einem explizit gesetzten `BUILD_ROOT`.

## Sicherheitsrelevante Hinweise

Der Connector allein schützt keine Anwendung. Wirksamer Schutz entsteht erst
durch:

- aktivierten Connector,
- geladene Regeln,
- korrekten `SecRuleEngine`-Modus,
- passende Request-/Response-Body-Einstellungen,
- korrekt schreibbare Audit-Logs,
- getestete False-Positive-Ausnahmen.

`SecRuleEngine DetectionOnly` und `SecRuleEngine On` müssen bewusst gewählt
werden:

- `DetectionOnly` protokolliert Treffer, blockiert aber nicht disruptiv.
- `On` erlaubt disruptives Verhalten wie `deny,status:403`.

Für neue Regelwerke empfiehlt sich:

1. In einer Testumgebung starten.
2. Audit-Logs prüfen.
3. False Positives identifizieren.
4. Ausnahmen dokumentieren.
5. Erst danach Blocking aktivieren.

Da Apache und Nginx unterschiedliche Hook- und Filtermodelle haben, kann das
Verhalten bei Randfällen unterschiedlich sein. Das gilt besonders für
Response-Body-Verarbeitung, Header, die spät durch andere Module ergänzt
werden, und Interventions nachdem Header bereits an den Client gesendet wurden.

## Feature-Matrix

Die folgende Tabelle beschreibt den aktuellen, aus Repository-Code und
Dokumentation ableitbaren Stand. „Teilweise“ bedeutet, dass Code oder Tests
vorhanden sind, aber keine vollständige gemeinsame oder produktiv verallgemeinerte
Garantie dokumentiert ist.

| Feature | Nginx | Apache | Hinweise |
| --- | --- | --- | --- |
| Request Header Inspection | Ja | Ja | Beide Connectoren übergeben eingehende Header an libmodsecurity und rufen Request-Header-Verarbeitung auf. |
| Request Body Inspection | Ja | Ja | Beide Connectoren übergeben Request-Body-Daten an libmodsecurity. Details zu Buffering und Timing sind server-spezifisch. |
| Response Header Inspection | Ja | Ja | Beide Connectoren enthalten Response-Header-Pfade und rufen `msc_process_response_headers`. |
| Response Body Inspection | Teilweise | Teilweise | Codepfade existieren, aber `RESPONSE_BODY` ist laut Projektdokumentation nicht als verifizierte Blocking-Capability promotet. |
| Audit Logging | Teilweise | Teilweise | Audit-Logs werden über libmodsecurity-Regeln konfiguriert; stabile Audit-Feld-Parität ist nicht als gemeinsame Runtime-Schicht implementiert. |
| Rules File Loading | Ja | Ja | `modsecurity_rules_file` ist in beiden Connectoren vorhanden und nutzt libmodsecurity. |
| Inline Rules Loading | Ja | Ja | `modsecurity_rules` ist in beiden Connectoren vorhanden. |
| Remote Rules Loading | Ja | Ja | `modsecurity_rules_remote` ist in beiden Connectoren vorhanden. |
| Blocking Mode | Ja | Ja | Disruptive Interventions werden in beiden Connectoren ausgewertet; Response-Body-Blocking bleibt gesondert vorsichtig zu betrachten. |
| DetectionOnly Mode | Ja | Ja | Wird über ModSecurity-Regeln und libmodsecurity gesteuert, nicht über eine eigene Connector-Direktive. |
| Transaction ID | Ja | Ja | Nginx unterstützt Complex Values; Apache unterstützt statische Strings mit `UNIQUE_ID`-Fallback. |
| Error-Log-Forwarding-Policy | Ja | Ja | `modsecurity_use_error_log on|off`; wirkt nur auf den Error-Log-Callback. |
| Rule-Load-Stats Metadata | Ja | Ja | Gemeinsame Datenform; Nginx loggt die Werte beim Start, Apache hält sie intern. |
| Phase-4 Mode Controls | Ja | Nein | Nginx-spezifische Direktiven; keine Apache-Parität im aktuellen Code. |

## Bekannte Unterschiede zwischen Nginx und Apache

### Transaktions-ID

Apache akzeptiert bei `modsecurity_transaction_id` eine statische Zeichenkette.
Nginx akzeptiert eine Nginx Complex Value und kann dadurch Nginx-Variablen pro
Request auswerten.

### Konfigurations-Scope

Apache verwendet Apache-Kontexte über `RSRC_CONF | ACCESS_CONF`. Nginx
registriert die Direktiven für Main-, Server- und Location-Kontexte. Die
Merge-Logik ist entsprechend unterschiedlich.

### Rule-Load-Stats-Ausgabe

Nginx gibt Rule-Load-Statistiken im Startup-Log aus. Apache speichert die
Statistiken aktuell intern in `msc_conf_t`, gibt sie aber nicht im Post-Config-
Log aus.

### Phase-4-Direktiven

Nur Nginx unterstützt:

- `modsecurity_phase4_mode`,
- `modsecurity_phase4_content_types_file`,
- `modsecurity_phase4_log`.

Diese Direktiven steuern Nginx-spezifisches Verhalten bei späten
Response-Body-Interventions. Apache implementiert sie nicht.

### Response Body

Beide Connectoren haben Response-Body-Codepfade. Die Projektdokumentation
kennzeichnet Response-Body-Blocking jedoch nicht als gemeinsam verifizierte
Capability. Bei Unsicherheit müssen echte Runtime-Smokes und Audit-/Error-Logs
herangezogen werden.

## Troubleshooting für Shared Features

### Rules werden nicht geladen

Prüfen:

```sh
nginx -t
apachectl configtest
```

Typische Ursachen:

- falscher Pfad in `modsecurity_rules_file`,
- fehlende Leserechte,
- ungültige Regel-Syntax,
- nicht eindeutige Rule-ID,
- libmodsecurity-Version unterstützt eine verwendete Regelkonstruktion nicht.

Bei Nginx kann der Startup-Log zusätzlich die Anzahl geladener Inline-/File-/
Remote-Regeln zeigen. Bei Apache ist diese Statistik aktuell intern.

### Requests werden nicht blockiert

Prüfen:

- Ist `modsecurity on` im passenden Scope gesetzt?
- Ist `SecRuleEngine On` gesetzt oder nur `DetectionOnly`?
- Matcht die Regel tatsächlich auf den Request?
- Läuft der Test gegen den erwarteten `server`-/`location`- oder
  Directory-Scope?
- Wird ein Request-Body erwartet, aber nicht gesendet oder anders codiert?
- Wird eine Response-Body-Regel getestet, obwohl dieser Bereich nicht als
  gemeinsame Blocking-Capability promotet ist?

Ein minimaler Testfall mit `ARGS:test` ist oft besser als direkt ein großes
Regelwerk zu debuggen.

### Audit-Logs erscheinen nicht

Prüfen:

- `SecAuditEngine` ist gesetzt,
- `SecAuditLog` zeigt auf einen schreibbaren Pfad,
- der Server-Worker hat Schreibrechte,
- SELinux/AppArmor blockiert den Pfad nicht,
- die Regel erzeugt überhaupt ein audit-relevantes Ereignis,
- `nolog` ist nicht in der Regel gesetzt.

`modsecurity_use_error_log off` betrifft nicht das Audit-Log. Wenn Error-Log-
Meldungen fehlen, kann diese Direktive relevant sein; bei Audit-Logs ist sie
nicht die Ursache.

### Unterschiedliches Verhalten zwischen Nginx und Apache

Mögliche Ursachen:

- unterschiedliche Hook-Zeitpunkte,
- unterschiedliches Request-Body-Buffering,
- unterschiedliche Header-Normalisierung oder Reihenfolge,
- Nginx-Complex-Value bei Transaktions-ID gegenüber statischem Apache-Wert,
- Nginx-spezifischer Phase-4-Modus,
- verschiedene libmodsecurity-Versionen oder Regeldateien,
- verschiedene Servermodule, die Header vor oder nach ModSecurity ändern.

Zur Eingrenzung sollten beide Connectoren mit derselben libmodsecurity-Version,
derselben Rules-Datei und einem minimalen reproduzierbaren Request getestet
werden.

### Fehlende Runtime-Abhängigkeiten

Wenn ein Modul gebaut wurde, aber nicht lädt, prüfe:

```sh
ldd /pfad/zu/ngx_http_modsecurity_module.so
ldd /pfad/zu/mod_security3.so
```

Fehlt `libmodsecurity.so`, muss der Library-Suchpfad angepasst werden. Bei
lokalen Helper-Runs setzen die Harnesses `LD_LIBRARY_PATH` auf die staged
libmodsecurity-Verzeichnisse unter `BUILD_ROOT`.

## Weiterführende Hinweise

- [Nginx kompilieren](./COMPILE_NGINX.md)
- [Apache kompilieren](./COMPILE_APACHE.md)
- `README.md`
- `docs/architecture/architecture.md`
- `docs/architecture/common-runtime-boundaries.md`
- `docs/connectors/directive-parity.md`
- `docs/connectors/rule-load-stats.md`
- `connectors/nginx/README.md`
- `connectors/apache/README.md`
- `connectors/nginx/harness/README.md`
- `connectors/apache/harness/README.md`
