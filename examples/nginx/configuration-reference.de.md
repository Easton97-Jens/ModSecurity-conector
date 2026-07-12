# NGINX-Konfigurationsreferenz

**Sprache:** [English](configuration-reference.md) | Deutsch

## Geltungsbereich und maßgebliche Quellen

Ausgewählter Integrationsmodus: `native-nginx-http-module`. Diese Datei wird aus registrierten Parsern, Konfigurationsstrukturen, geprüften Service-Verträgen und aktiven Beispielen erzeugt.
Kompatibilitätseinträge sind ausdrücklich als solche markiert und gehören nicht zum ausgewählten Kernpfad.

## Konfigurationsinventar

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`access_log`](#access-log) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`error_log`](#error-log) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`gzip`](#gzip) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`listen`](#listen) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`load_module`](#load-module) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`modsecurity`](#modsecurity) | Host / Connector | Boolescher Wert | nein | off | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Schaltet die Erstellung von Connector-Transaktionen frei; dies ist nicht SecRuleEngine. |
| [`modsecurity_phase4_body_limit`](#modsecurity-phase4-body-limit) | Host / Connector | positive dezimale Byteanzahl | nein | 1048576 | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Begrenzt die vom nativen Connector der P4-Verarbeitung angebotenen Response-Bytes. |
| [`modsecurity_phase4_content_types_file`](#modsecurity-phase4-content-types-file) | Host / Connector | Pfad | nein | Host-Standardwerte bei Auslassung | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Beschränkt die P4-Response-Body-Inspektion auf konfigurierte MIME-Typen. |
| [`modsecurity_phase4_log`](#modsecurity-phase4-log) | Host / Connector | Pfad | nein | none | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Setzt einen Connector-Ereignispfad; aktuelle Apache- und NGINX-Pfade verwenden ihn auch für frühere Regel-/Interventionsmetadaten, nicht nur für P4. |
| [`modsecurity_phase4_mode`](#modsecurity-phase4-mode) | Host / Connector | Aufzählung | nein | safe | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Bevor Response-Header/-Body committet sind, lösen minimal, safe und strict eine P4-Intervention jeweils als deny_if_possible auf; NGINX kann daher noch den angeforderten Engine-Status (oder den Fallback 403) zurückgeben. Sobald Header committet sind oder der Body begonnen hat, verwenden minimal und safe beide die gemeinsame Aktion log_only; sie protokollieren die späte Entscheidung ohne nachträgliche Statusumschreibung. Strict löst dagegen zu abort_connection auf: Der native Body-Filter markiert die Verbindung als fehlerhaft, protokolliert connection_aborted und gibt NGX_ERROR zurück. Die bekannte Hostgrenze ist, dass NGINX das P4-Engine-Finish erst bei last_buf/last_in_chain nach der begrenzten Sammlung von Body-Bytes im Geltungsbereich aufruft; eine Antwort kann deshalb bereits sichtbar sein. Strict kann somit eine Verbindung beenden, aber keine spätere 403 garantieren oder eine bereits gesendete Statuszeile ersetzen. |
| [`modsecurity_rules`](#modsecurity-rules) | Host / Connector | Zeichenkette | nein | kein Wert; optional | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Lädt während des Konfigurationsladens Inline-Inhalt über libmodsecurity. |
| [`modsecurity_rules_file`](#modsecurity-rules-file) | Host / Connector | Pfad | nein | kein Wert; optional | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Beim Laden der NGINX-Konfiguration übergibt ngx_conf_set_rules_file den bereitgestellten Pfad an msc_rules_add_file von libmodsecurity. Der NGINX-Setter kanonisiert den Pfad nicht und verlangt keinen absoluten Pfad; ein absoluter Pfad vermeidet eine Abhängigkeit vom Arbeitsverzeichnis des Prozesses. Eine fehlende, unlesbare oder ungültige Regeldatei der obersten Ebene liefert den Loader-Fehler von libmodsecurity und lässt Konfigurationsprüfung/Reload fehlschlagen. Include und IncludeOptional in dieser Datei werden anschließend von libmodsecurity interpretiert, nicht durch den NGINX-Parser expandiert. Anders als modsecurity_rules, das eine Inline-Konfigurationszeichenkette an msc_rules_add sendet, übergibt diese Direktive einen Dateipfad an msc_rules_add_file; beide tragen zum konfigurierten Regelsatz und seinem normalen Eltern-/Kind-Merge bei. |
| [`modsecurity_rules_remote`](#modsecurity-rules-remote) | Host / Connector | zwei Zeichenketten | nein | kein Wert; optional | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader von libmodsecurity. |
| [`modsecurity_transaction_id`](#modsecurity-transaction-id) | Host / Connector | Zeichenkette/Ausdruck | nein | kein Wert; der Connector erzeugt eine Ersatzkennung | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Liefert die Engine- und Ereigniskorrelationskennung für eine Transaktion. |
| [`modsecurity_use_error_log`](#modsecurity-use-error-log) | Host / Connector | Boolescher Wert | nein | on | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Steuert die Weiterleitung von libmodsecurity-Meldungen an das Host-Fehlerlog; die Regelauswertung wird dadurch nicht umgeschaltet. |
| [`proxy_pass`](#proxy-pass) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server`](#server) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server_name`](#server-name) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |

## Trennung der Ebenen

Host-/Connector-Schalter binden oder konfigurieren die Hostintegration. Sie sind nicht identisch mit `SecRuleEngine`.

- [Common-Runtime-Konfiguration](../common/common-connector-configuration.de.md) beschreibt nur die `key=value`-Runtime-Datei und wird nicht als nicht registrierte Hostdirektive ausgegeben.
- [ModSecurity-Engine-Direktiven](../common/modsecurity-directives.de.md) beschreibt die `Sec*`-Direktiven der geladenen Regeldatei.
- [Regelbeispiele](../common/rule-examples.de.md) erklären DetectionOnly und das Abschalten der Engine.

## Common-Runtime-Relevanz

Der ausgewählte native Pfad parst keine Common-Runtime-`key=value`-Datei; gemeinsame Modellfelder werden nur über registrierte Hostdirektiven angeboten.

## Von Profilen verwendete Engine-Direktiven

Die lokalen Regelprofile verwenden `SecRuleEngine` für On, DetectionOnly und Off. Wo Body-Inspektion gewählt wird, bleiben `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME-Scope, Limits und `SecRule` ModSecurity-Engine-Direktiven.

Siehe [Engine-Referenz](../common/modsecurity-directives.de.md).

## Profile

| Profil | Datei | Status |
| --- | --- | --- |
| Minimal | [minimal/nginx.conf](minimal/nginx.conf) | Aktive Startkonfiguration |
| Sicherer vollständiger Lebenszyklus | [safe/nginx.conf](safe/nginx.conf) | Ausgewählte begrenzte Referenz |
| Strikt | [strict/nginx.conf](strict/nginx.conf) | Parserunterstützte oder ausdrücklich optionale Grenze |
| DetectionOnly | [detection-only/nginx.conf](detection-only/nginx.conf) | Engine wertet aus/protokolliert ohne disruptive Aktion |
| Deaktiviert | [disabled/nginx.conf](disabled/nginx.conf) | Connector- oder Engine-Pfad deaktiviert |

## Konfigurationskombinationen

| Connector | Engine | Request-Body | Response-Body | Ergebnis |
| --- | --- | --- | --- | --- |
| off | On | beliebig | beliebig | Keine Connector-Transaktion; die Engine-Einstellung wird nicht erreicht. |
| on | Off | beliebig | beliebig | Der Connector erreicht die Engine, aber deren Regelauswertung ist deaktiviert. |
| on | DetectionOnly | aktiviert | aktiviert | Regeln können ohne disruptive Durchsetzung treffen/protokollieren. |
| on | On | Off | On | Der P2-Body steht der Engine nicht zur Verfügung; P4 bleibt host-/fähigkeitsabhängig. |
| on | On | On | Off | Der P4-Body steht der Engine nicht zur Verfügung. |
| on | On | On | On + safe | Späte P4-Ergebnisse nach dem Commit werden ohne zugesagte spätere Statusänderung aufgezeichnet. |
| on | On | On | On + strict | Ein hostspezifisches strict-Ergebnis nur verwenden, wenn Quelle/Nachweis es stützen; keine künstliche spätere 403. |
| on | On | über Limit + process_partial | über Limit + reject | Die Body-Policy bestimmt die begrenzte Engine-Eingabe; die genaue Host-Response-Behandlung bleibt connectorspezifisch. |

## Validierung

```sh
nginx -t
```

Repository-Ziele: `make check-config-nginx` und `make check-config-all-connectors`.

## Optionsdetails

## `access_log`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
access_log <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `error_log`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
error_log <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `gzip`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
gzip <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `listen`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
listen <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `load_module`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
load_module <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `modsecurity`

### Kurzbeschreibung

Schaltet die Erstellung von Connector-Transaktionen frei; dies ist nicht SecRuleEngine.

### Syntax

```text
modsecurity on | off;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | on \| off (der gemeinsame Parser akzeptiert zusätzlich true/false/1/0/yes/no, sofern der Host diese Werte durchreicht) | nein |

### Standardwert

off

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_ENABLE`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Schaltet die Erstellung von Connector-Transaktionen frei; dies ist nicht SecRuleEngine.

### Validierung und Fehler

ngx_conf_set_common_flag_slot weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_FLAG ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/minimal/nginx.conf](../../examples/nginx/minimal/nginx.conf).

### Sicherheit und Betrieb

off umgeht die Connector-Verarbeitung P1–P4, auch wenn eine Regeldatei konfiguriert ist.

## `modsecurity_phase4_body_limit`

### Kurzbeschreibung

Begrenzt die vom nativen Connector der P4-Verarbeitung angebotenen Response-Bytes.

### Syntax

```text
modsecurity_phase4_body_limit <positive-bytes>;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

1048576

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Begrenzt die vom nativen Connector der P4-Verarbeitung angebotenen Response-Bytes.

### Validierung und Fehler

ngx_conf_set_phase4_body_limit weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1 ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Ein größeres Limit erhöht die Speicher-/CPU-Exposition; null ist in den nativen Settern ungültig.

## `modsecurity_phase4_content_types_file`

### Kurzbeschreibung

Beschränkt die P4-Response-Body-Inspektion auf konfigurierte MIME-Typen.

### Syntax

```text
modsecurity_phase4_content_types_file <value>;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | eine lesbare Datei mit MIME-Token | nein |

### Standardwert

Host-Standardwerte bei Auslassung

Quelle: `connectorspezifischer Standard-Content-Type-Loader`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Beschränkt die P4-Response-Body-Inspektion auf konfigurierte MIME-Typen.

### Validierung und Fehler

ngx_conf_set_phase4_content_types_file weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1 ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Den Geltungsbereich eng halten und validieren, dass der Host die beabsichtigte Repräsentation der Response-Bytes bereitstellt.

## `modsecurity_phase4_log`

### Kurzbeschreibung

Setzt einen Connector-Ereignispfad; aktuelle Apache- und NGINX-Pfade verwenden ihn auch für frühere Regel-/Interventionsmetadaten, nicht nur für P4.

### Syntax

```text
modsecurity_phase4_log <value>;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | ein Pfad für das Connector-JSONL-Ereignis-/Interventionslog | nein |

### Standardwert

none

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Setzt einen Connector-Ereignispfad; aktuelle Apache- und NGINX-Pfade verwenden ihn auch für frühere Regel-/Interventionsmetadaten, nicht nur für P4.

### Validierung und Fehler

ngx_conf_set_phase4_log weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1 ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

JSONL-Metadaten als sensible Betriebsdaten behandeln und sichere Eigentümerschaft/Rotation festlegen.

## `modsecurity_phase4_mode`

### Kurzbeschreibung

Bevor Response-Header/-Body committet sind, lösen minimal, safe und strict eine P4-Intervention jeweils als deny_if_possible auf; NGINX kann daher noch den angeforderten Engine-Status (oder den Fallback 403) zurückgeben. Sobald Header committet sind oder der Body begonnen hat, verwenden minimal und safe beide die gemeinsame Aktion log_only; sie protokollieren die späte Entscheidung ohne nachträgliche Statusumschreibung. Strict löst dagegen zu abort_connection auf: Der native Body-Filter markiert die Verbindung als fehlerhaft, protokolliert connection_aborted und gibt NGX_ERROR zurück. Die bekannte Hostgrenze ist, dass NGINX das P4-Engine-Finish erst bei last_buf/last_in_chain nach der begrenzten Sammlung von Body-Bytes im Geltungsbereich aufruft; eine Antwort kann deshalb bereits sichtbar sein. Strict kann somit eine Verbindung beenden, aber keine spätere 403 garantieren oder eine bereits gesendete Statuszeile ersetzen.

### Syntax

```text
modsecurity_phase4_mode minimal | safe | strict;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Aufzählung | minimal \| safe \| strict; vor dem Commit verwenden alle deny_if_possible, nach dem Commit verwenden minimal/safe log_only und strict abort_connection | nein |

### Standardwert

safe

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur P4. Der Response-Body-Filter sammelt begrenzte Bytes im Geltungsbereich und beendet die Engine bei EOS (last_buf/last_in_chain); das Committen von Headern/Body bestimmt, ob ein Status oder nur noch eine späte Transportaktion möglich ist.

Bevor Response-Header/-Body committet sind, lösen minimal, safe und strict eine P4-Intervention jeweils als deny_if_possible auf; NGINX kann daher noch den angeforderten Engine-Status (oder den Fallback 403) zurückgeben. Sobald Header committet sind oder der Body begonnen hat, verwenden minimal und safe beide die gemeinsame Aktion log_only; sie protokollieren die späte Entscheidung ohne nachträgliche Statusumschreibung. Strict löst dagegen zu abort_connection auf: Der native Body-Filter markiert die Verbindung als fehlerhaft, protokolliert connection_aborted und gibt NGX_ERROR zurück. Die bekannte Hostgrenze ist, dass NGINX das P4-Engine-Finish erst bei last_buf/last_in_chain nach der begrenzten Sammlung von Body-Bytes im Geltungsbereich aufruft; eine Antwort kann deshalb bereits sichtbar sein. Strict kann somit eine Verbindung beenden, aber keine spätere 403 garantieren oder eine bereits gesendete Statuszeile ersetzen.

### Validierung und Fehler

ngx_conf_set_phase4_mode akzeptiert während nginx -t nur minimal|safe|strict. Das späte Runtime-Verhalten ist quellendefiniert: Nicht-strict-Pfade nach dem Commit geben log_only aus; strict markiert die Verbindung als fehlerhaft und gibt NGX_ERROR zurück, ohne eine spätere 403 zu erfinden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

safe/minimal bewahren Nachweise später Entscheidungen, ohne eine bereits gestartete Antwort zu unterbrechen. strict fordert nach dem Commit einen Verbindungsabbruch an, der Clients einer Teilantwort aussetzen kann; dies ist kein verlässlicher Modus zur Durchsetzung eines HTTP-Status nach dem Commit.

## `modsecurity_rules`

### Kurzbeschreibung

Lädt während des Konfigurationsladens Inline-Inhalt über libmodsecurity.

### Syntax

```text
modsecurity_rules <value>;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette | eine Inline-Zeichenkette für ModSecurity-Regel/Konfiguration | nein |

### Standardwert

kein Wert; optional

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Lädt während des Konfigurationsladens Inline-Inhalt über libmodsecurity.

### Validierung und Fehler

ngx_conf_set_rules weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1 ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Inline-Regeln sind ausführbare Policy; einschränken, wer die Hostkonfiguration ändern darf.

## `modsecurity_rules_file`

### Kurzbeschreibung

Beim Laden der NGINX-Konfiguration übergibt ngx_conf_set_rules_file den bereitgestellten Pfad an msc_rules_add_file von libmodsecurity. Der NGINX-Setter kanonisiert den Pfad nicht und verlangt keinen absoluten Pfad; ein absoluter Pfad vermeidet eine Abhängigkeit vom Arbeitsverzeichnis des Prozesses. Eine fehlende, unlesbare oder ungültige Regeldatei der obersten Ebene liefert den Loader-Fehler von libmodsecurity und lässt Konfigurationsprüfung/Reload fehlschlagen. Include und IncludeOptional in dieser Datei werden anschließend von libmodsecurity interpretiert, nicht durch den NGINX-Parser expandiert. Anders als modsecurity_rules, das eine Inline-Konfigurationszeichenkette an msc_rules_add sendet, übergibt diese Direktive einen Dateipfad an msc_rules_add_file; beide tragen zum konfigurierten Regelsatz und seinem normalen Eltern-/Kind-Merge bei.

### Syntax

```text
modsecurity_rules_file <value>;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | ein lesbarer libmodsecurity-Konfigurations-/Regelpfad; absolute Pfade werden empfohlen, während die Auflösung relativer Pfade libmodsecurity überlassen wird | nein |

### Standardwert

kein Wert; optional

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Beim Laden der NGINX-Konfiguration übergibt ngx_conf_set_rules_file den bereitgestellten Pfad an msc_rules_add_file von libmodsecurity. Der NGINX-Setter kanonisiert den Pfad nicht und verlangt keinen absoluten Pfad; ein absoluter Pfad vermeidet eine Abhängigkeit vom Arbeitsverzeichnis des Prozesses. Eine fehlende, unlesbare oder ungültige Regeldatei der obersten Ebene liefert den Loader-Fehler von libmodsecurity und lässt Konfigurationsprüfung/Reload fehlschlagen. Include und IncludeOptional in dieser Datei werden anschließend von libmodsecurity interpretiert, nicht durch den NGINX-Parser expandiert. Anders als modsecurity_rules, das eine Inline-Konfigurationszeichenkette an msc_rules_add sendet, übergibt diese Direktive einen Dateipfad an msc_rules_add_file; beide tragen zum konfigurierten Regelsatz und seinem normalen Eltern-/Kind-Merge bei.

### Validierung und Fehler

ngx_conf_set_rules_file ruft msc_rules_add_file während nginx -t/des Konfigurationsladens auf. Eine fehlende, unlesbare oder syntaktisch ungültige Regeldatei der obersten Ebene (einschließlich eines fehlgeschlagenen Engine-Include) liefert den Loader-Fehler und weist die NGINX-Konfiguration ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/minimal/nginx.conf](../../examples/nginx/minimal/nginx.conf).

### Sicherheit und Betrieb

Die Datei, ihre übergeordneten Verzeichnisse und alle von der Engine eingebundenen Dateien für nicht vertrauenswürdige Identitäten nicht schreibbar halten. Einen absoluten Pfad bevorzugen, damit ein geändertes Arbeitsverzeichnis keine unbeabsichtigte Policy wählen kann.

## `modsecurity_rules_remote`

### Kurzbeschreibung

Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader von libmodsecurity.

### Syntax

```text
modsecurity_rules_remote <key> <url>;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| zwei Zeichenketten | Schlüssel und URL | nein |

### Standardwert

kein Wert; optional

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader von libmodsecurity.

### Validierung und Fehler

ngx_conf_set_rules_remote weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE2 ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Remote-Policy wird von den ausgewählten no-CRS-Beispielen nicht verwendet; nicht als Ersatz für eine lokale Datei behandeln.

## `modsecurity_transaction_id`

### Kurzbeschreibung

Liefert die Engine- und Ereigniskorrelationskennung für eine Transaktion.

### Syntax

```text
modsecurity_transaction_id <value>;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Ausdruck | nichtleere hostspezifische Transaktionskennung | nein |

### Standardwert

kein Wert; der Connector erzeugt eine Ersatzkennung

Quelle: `Connector-Pfad zur Transaktionserzeugung`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Liefert die Engine- und Ereigniskorrelationskennung für eine Transaktion.

### Validierung und Fehler

ngx_conf_set_transaction_id weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_1MORE ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Keine Zugangsdaten oder sensiblen Request-Daten in eine Korrelationskennung aufnehmen.

## `modsecurity_use_error_log`

### Kurzbeschreibung

Steuert die Weiterleitung von libmodsecurity-Meldungen an das Host-Fehlerlog; die Regelauswertung wird dadurch nicht umgeschaltet.

### Syntax

```text
modsecurity_use_error_log on | off;
```

### Gültige Kontexte

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | on \| off | nein |

### Standardwert

on

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG`.

### Vererbung und Zusammenführung

http → server → location; ein Kind erbt, wenn es keinen Wert setzt.

Zusammenführung: ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Steuert die Weiterleitung von libmodsecurity-Meldungen an das Host-Fehlerlog; die Regelauswertung wird dadurch nicht umgeschaltet.

### Validierung und Fehler

ngx_conf_set_common_flag_slot weist ungültige Werte während nginx -t ab; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_FLAG ist die registrierte Kontextmaske.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Fehlerlogs können Sicherheitsmetadaten enthalten; sie schützen und rotieren.

## `proxy_pass`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
proxy_pass <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `server`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `server_name`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server_name <host-specific-value>
```

### Gültige Kontexte

- Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| hosteigenes Konfigurationsfeld | der explizite Wert im ausgewählten eingecheckten Beispiel | nein |

### Standardwert

Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.

Quelle: `aktive Beispielkonfiguration`.

### Vererbung und Zusammenführung

Hostdefiniert; nicht durch diesen Connector implementiert.

Zusammenführung: Hostdefiniert; nicht durch diesen Connector implementiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.

Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.

### Validierung und Fehler

nginx -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.
