# lighttpd-Konfigurationsreferenz

**Sprache:** [English](configuration-reference.md) | Deutsch

## Geltungsbereich und maßgebliche Quellen

Ausgewählter Integrationsmodus: `patched-native-lighttpd`. Diese Datei wird aus registrierten Parsern, Konfigurationsstrukturen, geprüften Service-Verträgen und aktiven Beispielen erzeugt.
Kompatibilitätseinträge sind ausdrücklich als solche markiert und gehören nicht zum ausgewählten Kernpfad.

## Konfigurationsinventar

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`msconnector.config-file`](#msconnector-config-file) | Host / Connector | Pfad | ja | none | T_CONFIG_SCOPE_SERVER | Pfad zur Common-Runtime-Konfiguration, die das native Plugin verwendet. |
| [`msconnector.enabled`](#msconnector-enabled) | Host / Connector | lighttpd-Boolean | nein | off | T_CONFIG_SCOPE_SERVER | Aktiviert das native lighttpd-Plugin. |
| [`proxy.server`](#proxy-server) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.bind`](#server-bind) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.compat-module-load`](#server-compat-module-load) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.document-root`](#server-document-root) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.errorlog`](#server-errorlog) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.modules`](#server-modules) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.pid-file`](#server-pid-file) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.port`](#server-port) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.stream-response-body`](#server-stream-response-body) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`server.upload-dirs`](#server-upload-dirs) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`compatibility.accesslog.filename`](#compatibility-accesslog-filename) | Kompatibilität | lighttpd-Kompatibilitäts-Hostfeld | nein | nicht Teil von nativem mod_msconnector | lighttpd-Sidecar-Kompatibilitätskonfiguration | lighttpd-Hostfeld nur für die Kompatibilität. |
| [`compatibility.proxy.server`](#compatibility-proxy-server) | Kompatibilität | lighttpd-Kompatibilitäts-Hostfeld | nein | nicht Teil von nativem mod_msconnector | lighttpd-Sidecar-Kompatibilitätskonfiguration | lighttpd-Hostfeld nur für die Kompatibilität. |
| [`compatibility.server.document-root`](#compatibility-server-document-root) | Kompatibilität | lighttpd-Kompatibilitäts-Hostfeld | nein | nicht Teil von nativem mod_msconnector | lighttpd-Sidecar-Kompatibilitätskonfiguration | lighttpd-Hostfeld nur für die Kompatibilität. |
| [`compatibility.server.errorlog`](#compatibility-server-errorlog) | Kompatibilität | lighttpd-Kompatibilitäts-Hostfeld | nein | nicht Teil von nativem mod_msconnector | lighttpd-Sidecar-Kompatibilitätskonfiguration | lighttpd-Hostfeld nur für die Kompatibilität. |
| [`compatibility.server.modules`](#compatibility-server-modules) | Kompatibilität | lighttpd-Kompatibilitäts-Hostfeld | nein | nicht Teil von nativem mod_msconnector | lighttpd-Sidecar-Kompatibilitätskonfiguration | lighttpd-Hostfeld nur für die Kompatibilität. |
| [`compatibility.server.port`](#compatibility-server-port) | Kompatibilität | lighttpd-Kompatibilitäts-Hostfeld | nein | nicht Teil von nativem mod_msconnector | lighttpd-Sidecar-Kompatibilitätskonfiguration | lighttpd-Hostfeld nur für die Kompatibilität. |
| [`sidecar proxy`](#sidecar-proxy) | Kompatibilität | Kompatibilitäts-Hosteinrichtung | nein | keine native Connector-Option | Kompatibilitätsbeispiel | Sidecar-Proxy-Einrichtung nur für die Kompatibilität. |

## Trennung der Ebenen

Host-/Connector-Schalter binden oder konfigurieren die Hostintegration. Sie sind nicht identisch mit `SecRuleEngine`.

- [Common-Runtime-Konfiguration](../common/common-connector-configuration.de.md) beschreibt nur die `key=value`-Runtime-Datei und wird nicht als nicht registrierte Hostdirektive ausgegeben.
- [ModSecurity-Engine-Direktiven](../common/modsecurity-directives.de.md) beschreibt die `Sec*`-Direktiven der geladenen Regeldatei.
- [Regelbeispiele](../common/rule-examples.de.md) erklären DetectionOnly und das Abschalten der Engine.

## Common-Runtime-Relevanz

| Schlüssel | Lokale Verwendung | Detailreferenz |
| --- | --- | --- |
| `enabled` | Schlüssel des ausgewählten Runtime-Profils | [enabled](../common/common-connector-configuration.de.md#enabled) |
| `use_error_log` | Schlüssel des ausgewählten Runtime-Profils | [use_error_log](../common/common-connector-configuration.de.md#use-error-log) |
| `rules_inline` | Schlüssel des ausgewählten Runtime-Profils | [rules_inline](../common/common-connector-configuration.de.md#rules-inline) |
| `rules_file` | Schlüssel des ausgewählten Runtime-Profils | [rules_file](../common/common-connector-configuration.de.md#rules-file) |
| `rules_remote_key` | Schlüssel des ausgewählten Runtime-Profils | [rules_remote_key](../common/common-connector-configuration.de.md#rules-remote-key) |
| `rules_remote_url` | Schlüssel des ausgewählten Runtime-Profils | [rules_remote_url](../common/common-connector-configuration.de.md#rules-remote-url) |
| `transaction_id` | Schlüssel des ausgewählten Runtime-Profils | [transaction_id](../common/common-connector-configuration.de.md#transaction-id) |
| `transaction_id_header` | Schlüssel des ausgewählten Runtime-Profils | [transaction_id_header](../common/common-connector-configuration.de.md#transaction-id-header) |
| `phase4_mode` | Schlüssel des ausgewählten Runtime-Profils | [phase4_mode](../common/common-connector-configuration.de.md#phase4-mode) |
| `phase4_content_types_file` | Schlüssel des ausgewählten Runtime-Profils | [phase4_content_types_file](../common/common-connector-configuration.de.md#phase4-content-types-file) |
| `event_path` | Schlüssel des ausgewählten Runtime-Profils | [event_path](../common/common-connector-configuration.de.md#event-path) |
| `phase4_event_log` | Schlüssel des ausgewählten Runtime-Profils | [phase4_event_log](../common/common-connector-configuration.de.md#phase4-event-log) |
| `request_body_mode` | Schlüssel des ausgewählten Runtime-Profils | [request_body_mode](../common/common-connector-configuration.de.md#request-body-mode) |
| `response_body_mode` | Schlüssel des ausgewählten Runtime-Profils | [response_body_mode](../common/common-connector-configuration.de.md#response-body-mode) |
| `request_body_limit` | Schlüssel des ausgewählten Runtime-Profils | [request_body_limit](../common/common-connector-configuration.de.md#request-body-limit) |
| `response_body_limit` | Schlüssel des ausgewählten Runtime-Profils | [response_body_limit](../common/common-connector-configuration.de.md#response-body-limit) |
| `body_limit_action` | Schlüssel des ausgewählten Runtime-Profils | [body_limit_action](../common/common-connector-configuration.de.md#body-limit-action) |
| `late_intervention_timeout` | Schlüssel des ausgewählten Runtime-Profils | [late_intervention_timeout](../common/common-connector-configuration.de.md#late-intervention-timeout) |
| `default_block_status` | Schlüssel des ausgewählten Runtime-Profils | [default_block_status](../common/common-connector-configuration.de.md#default-block-status) |
| `default_error_status` | Schlüssel des ausgewählten Runtime-Profils | [default_error_status](../common/common-connector-configuration.de.md#default-error-status) |
| `max_header_count` | Schlüssel des ausgewählten Runtime-Profils | [max_header_count](../common/common-connector-configuration.de.md#max-header-count) |
| `max_header_name_size` | Schlüssel des ausgewählten Runtime-Profils | [max_header_name_size](../common/common-connector-configuration.de.md#max-header-name-size) |
| `max_header_value_size` | Schlüssel des ausgewählten Runtime-Profils | [max_header_value_size](../common/common-connector-configuration.de.md#max-header-value-size) |
| `max_total_header_bytes` | Schlüssel des ausgewählten Runtime-Profils | [max_total_header_bytes](../common/common-connector-configuration.de.md#max-total-header-bytes) |
| `max_event_json_bytes` | Schlüssel des ausgewählten Runtime-Profils | [max_event_json_bytes](../common/common-connector-configuration.de.md#max-event-json-bytes) |

## Von Profilen verwendete Engine-Direktiven

Die lokalen Regelprofile verwenden `SecRuleEngine` für On, DetectionOnly und Off. Wo Body-Inspektion gewählt wird, bleiben `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME-Scope, Limits und `SecRule` ModSecurity-Engine-Direktiven.

Siehe [Engine-Referenz](../common/modsecurity-directives.de.md).

## Profile

| Profil | Datei | Status |
| --- | --- | --- |
| Minimal | [minimal/lighttpd.conf](minimal/lighttpd.conf) | Aktive Startkonfiguration |
| Sicherer vollständiger Lebenszyklus | [safe/lighttpd-http1-identity.conf](safe/lighttpd-http1-identity.conf) | Ausgewählte begrenzte Referenz |
| Strikt | [README.de.md#strict-profilgrenze](README.de.md#strict-profilgrenze) | Parserunterstützte oder ausdrücklich optionale Grenze |
| DetectionOnly | [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Engine wertet aus/protokolliert ohne disruptive Aktion |
| Deaktiviert | [disabled/lighttpd.conf](disabled/lighttpd.conf) | Connector- oder Engine-Pfad deaktiviert |

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
lighttpd -tt -f <config>
```

Repository-Ziele: `make check-config-lighttpd` und `make check-config-all-connectors`.

## Optionsdetails

<a id="msconnector-config-file"></a>
## `msconnector.config-file`

### Kurzbeschreibung

Pfad zur Common-Runtime-Konfiguration, die das native Plugin verwendet.

### Syntax

```text
msconnector.config-file = "<runtime-key-value-file>"
```

### Gültige Kontexte

- T_CONFIG_SCOPE_SERVER

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | nichtleere lesbare Common-Runtime-key=value-Datei | ja |

### Standardwert

none

Quelle: `plugin config_file hat den Standardwert NULL`.

### Vererbung und Zusammenführung

Es werden nur Standardwerte geladen; keine dokumentierte bedingte Überschreibung zur Request-Zeit.

Zusammenführung: Plugin-Standardwerte behalten die konfigurierte Zeichenkette.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die referenzierte Common-Runtime-Datei wählt Body-Modi und die P1–P4-Policy.

Lädt und erzeugt die connectorneutrale Runtime, bevor Requests bedient werden.

### Validierung und Fehler

Nur bei msconnector.enabled=true erforderlich; eine fehlende, unlesbare oder ungültige Runtime-Konfiguration liefert beim Start HANDLER_ERROR.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/minimal/lighttpd.conf](../../examples/lighttpd/minimal/lighttpd.conf).

### Sicherheit und Betrieb

Die Runtime-Datei enthält ausführbare Regelpfade und Limits; vertrauenswürdige Eigentümerschaft und Berechtigungen verwenden.

<a id="msconnector-enabled"></a>
## `msconnector.enabled`

### Kurzbeschreibung

Aktiviert das native lighttpd-Plugin.

### Syntax

```text
msconnector.enabled = "enable" | "disable"
```

### Gültige Kontexte

- T_CONFIG_SCOPE_SERVER

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| lighttpd-Boolean | lighttpd-Boolean-Werte; die Beispiele verwenden enable/disable | nein |

### Standardwert

off

Quelle: `ck_calloc-Allocation von plugin_data und Standardkonfiguration`.

### Vererbung und Zusammenführung

Es werden nur Standardwerte geladen; das Modul besitzt keinen bedingten Patch-Pfad zur Request-Zeit.

Zusammenführung: config_plugin_values_init belegt Standardwerte; kein dokumentierter Merge pro Request.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: off deaktiviert die P1/P3-Callbacks des Moduls und alle gepatchten P2/P4-Callbacks.

Wählt, ob mod_msconnector die Common Runtime initialisiert.

### Validierung und Fehler

Bei Aktivierung validiert lighttpd die Runtime-Datei während set-defaults; Hostsyntax mit lighttpd -tt -f <config> validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/minimal/lighttpd.conf](../../examples/lighttpd/minimal/lighttpd.conf).

### Sicherheit und Betrieb

Das Deaktivieren des Moduls umgeht die Connector-Verarbeitung, auch wenn eine Regeldatei existiert.

<a id="proxy-server"></a>
## `proxy.server`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
proxy.server <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-bind"></a>
## `server.bind`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.bind <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-compat-module-load"></a>
## `server.compat-module-load`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.compat-module-load <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-document-root"></a>
## `server.document-root`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.document-root <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-errorlog"></a>
## `server.errorlog`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.errorlog <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-modules"></a>
## `server.modules`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.modules <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-pid-file"></a>
## `server.pid-file`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.pid-file <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-port"></a>
## `server.port`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.port <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-stream-response-body"></a>
## `server.stream-response-body`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.stream-response-body <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="server-upload-dirs"></a>
## `server.upload-dirs`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
server.upload-dirs <host-specific-value>
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

lighttpd -tt -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

<a id="compatibility-accesslog-filename"></a>
## `compatibility.accesslog.filename`

### Kurzbeschreibung

lighttpd-Hostfeld nur für die Kompatibilität.

### Syntax

```text
accesslog.filename = <value>
```

### Gültige Kontexte

- lighttpd-Sidecar-Kompatibilitätskonfiguration

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| lighttpd-Kompatibilitäts-Hostfeld | expliziter Wert des Kompatibilitätsbeispiels | nein |

### Standardwert

nicht Teil von nativem mod_msconnector

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

Hostdefiniertes Kompatibilitätsverhalten; keine native Plugin-Vererbung.

Zusammenführung: Hostdefiniertes Kompatibilitätsverhalten; nicht Teil von mod_msconnector.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Keine Aussage zum nativen Connector-Lebenszyklus.

Konfiguriert das beibehaltene Sidecar-Kompatibilitätsbeispiel.

### Validierung und Fehler

Als normale lighttpd-Proxy-Konfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Sicherheit und Betrieb

Host-Routing nur für die Kompatibilität; nicht als native ModSecurity-Konfiguration darstellen.

<a id="compatibility-proxy-server"></a>
## `compatibility.proxy.server`

### Kurzbeschreibung

lighttpd-Hostfeld nur für die Kompatibilität.

### Syntax

```text
proxy.server = <value>
```

### Gültige Kontexte

- lighttpd-Sidecar-Kompatibilitätskonfiguration

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| lighttpd-Kompatibilitäts-Hostfeld | expliziter Wert des Kompatibilitätsbeispiels | nein |

### Standardwert

nicht Teil von nativem mod_msconnector

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

Hostdefiniertes Kompatibilitätsverhalten; keine native Plugin-Vererbung.

Zusammenführung: Hostdefiniertes Kompatibilitätsverhalten; nicht Teil von mod_msconnector.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Keine Aussage zum nativen Connector-Lebenszyklus.

Konfiguriert das beibehaltene Sidecar-Kompatibilitätsbeispiel.

### Validierung und Fehler

Als normale lighttpd-Proxy-Konfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Sicherheit und Betrieb

Host-Routing nur für die Kompatibilität; nicht als native ModSecurity-Konfiguration darstellen.

<a id="compatibility-server-document-root"></a>
## `compatibility.server.document-root`

### Kurzbeschreibung

lighttpd-Hostfeld nur für die Kompatibilität.

### Syntax

```text
server.document-root = <value>
```

### Gültige Kontexte

- lighttpd-Sidecar-Kompatibilitätskonfiguration

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| lighttpd-Kompatibilitäts-Hostfeld | expliziter Wert des Kompatibilitätsbeispiels | nein |

### Standardwert

nicht Teil von nativem mod_msconnector

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

Hostdefiniertes Kompatibilitätsverhalten; keine native Plugin-Vererbung.

Zusammenführung: Hostdefiniertes Kompatibilitätsverhalten; nicht Teil von mod_msconnector.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Keine Aussage zum nativen Connector-Lebenszyklus.

Konfiguriert das beibehaltene Sidecar-Kompatibilitätsbeispiel.

### Validierung und Fehler

Als normale lighttpd-Proxy-Konfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Sicherheit und Betrieb

Host-Routing nur für die Kompatibilität; nicht als native ModSecurity-Konfiguration darstellen.

<a id="compatibility-server-errorlog"></a>
## `compatibility.server.errorlog`

### Kurzbeschreibung

lighttpd-Hostfeld nur für die Kompatibilität.

### Syntax

```text
server.errorlog = <value>
```

### Gültige Kontexte

- lighttpd-Sidecar-Kompatibilitätskonfiguration

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| lighttpd-Kompatibilitäts-Hostfeld | expliziter Wert des Kompatibilitätsbeispiels | nein |

### Standardwert

nicht Teil von nativem mod_msconnector

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

Hostdefiniertes Kompatibilitätsverhalten; keine native Plugin-Vererbung.

Zusammenführung: Hostdefiniertes Kompatibilitätsverhalten; nicht Teil von mod_msconnector.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Keine Aussage zum nativen Connector-Lebenszyklus.

Konfiguriert das beibehaltene Sidecar-Kompatibilitätsbeispiel.

### Validierung und Fehler

Als normale lighttpd-Proxy-Konfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Sicherheit und Betrieb

Host-Routing nur für die Kompatibilität; nicht als native ModSecurity-Konfiguration darstellen.

<a id="compatibility-server-modules"></a>
## `compatibility.server.modules`

### Kurzbeschreibung

lighttpd-Hostfeld nur für die Kompatibilität.

### Syntax

```text
server.modules = <value>
```

### Gültige Kontexte

- lighttpd-Sidecar-Kompatibilitätskonfiguration

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| lighttpd-Kompatibilitäts-Hostfeld | expliziter Wert des Kompatibilitätsbeispiels | nein |

### Standardwert

nicht Teil von nativem mod_msconnector

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

Hostdefiniertes Kompatibilitätsverhalten; keine native Plugin-Vererbung.

Zusammenführung: Hostdefiniertes Kompatibilitätsverhalten; nicht Teil von mod_msconnector.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Keine Aussage zum nativen Connector-Lebenszyklus.

Konfiguriert das beibehaltene Sidecar-Kompatibilitätsbeispiel.

### Validierung und Fehler

Als normale lighttpd-Proxy-Konfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Sicherheit und Betrieb

Host-Routing nur für die Kompatibilität; nicht als native ModSecurity-Konfiguration darstellen.

<a id="compatibility-server-port"></a>
## `compatibility.server.port`

### Kurzbeschreibung

lighttpd-Hostfeld nur für die Kompatibilität.

### Syntax

```text
server.port = <value>
```

### Gültige Kontexte

- lighttpd-Sidecar-Kompatibilitätskonfiguration

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| lighttpd-Kompatibilitäts-Hostfeld | expliziter Wert des Kompatibilitätsbeispiels | nein |

### Standardwert

nicht Teil von nativem mod_msconnector

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

Hostdefiniertes Kompatibilitätsverhalten; keine native Plugin-Vererbung.

Zusammenführung: Hostdefiniertes Kompatibilitätsverhalten; nicht Teil von mod_msconnector.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Keine Aussage zum nativen Connector-Lebenszyklus.

Konfiguriert das beibehaltene Sidecar-Kompatibilitätsbeispiel.

### Validierung und Fehler

Als normale lighttpd-Proxy-Konfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Sicherheit und Betrieb

Host-Routing nur für die Kompatibilität; nicht als native ModSecurity-Konfiguration darstellen.

<a id="sidecar-proxy"></a>
## `sidecar proxy`

### Kurzbeschreibung

Sidecar-Proxy-Einrichtung nur für die Kompatibilität.

### Syntax

```text
proxy.server = (...)
```

### Gültige Kontexte

- Kompatibilitätsbeispiel

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kompatibilitäts-Hosteinrichtung | normale lighttpd-Proxy-Felder | nein |

### Standardwert

keine native Connector-Option

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

nicht auf das native Plugin anwendbar

Zusammenführung: nicht Teil von mod_msconnector

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Keine Aussage zum Lebenszyklus von nativem mod_msconnector.

Proxy-Routing nur für die Kompatibilität.

### Validierung und Fehler

Als normale lighttpd-Proxy-Konfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Sicherheit und Betrieb

Einen Proxy-Endpunkt nicht als konfigurierte native ModSecurity-Integration behandeln.
