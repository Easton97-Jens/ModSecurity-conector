# Apache-Konfigurationsreferenz

**Sprache:** [English](configuration-reference.md) | Deutsch

## Geltungsbereich und maßgebliche Quellen

Ausgewählter Integrationsmodus: `native-httpd-module`. Diese Datei wird aus registrierten Parsern, Konfigurationsstrukturen, geprüften Service-Verträgen und aktiven Beispielen erzeugt.
Kompatibilitätseinträge sind ausdrücklich als solche markiert und gehören nicht zum ausgewählten Kernpfad.

## Konfigurationsinventar

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`CustomLog`](#customlog) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`ErrorLog`](#errorlog) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`LoadModule`](#loadmodule) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`modsecurity`](#modsecurity) | Host / Connector | Boolescher Wert | nein | off | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Schaltet die Erstellung von Connector-Transaktionen frei; dies ist nicht SecRuleEngine. |
| [`modsecurity_phase4_body_limit`](#modsecurity-phase4-body-limit) | Host / Connector | positive dezimale Byteanzahl | nein | 1048576 | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Begrenzt die vom nativen Connector der P4-Verarbeitung angebotenen Response-Bytes. |
| [`modsecurity_phase4_content_types_file`](#modsecurity-phase4-content-types-file) | Host / Connector | Pfad | nein | Host-Standardwerte bei Auslassung | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Beschränkt die P4-Response-Body-Inspektion auf konfigurierte MIME-Typen. |
| [`modsecurity_phase4_log`](#modsecurity-phase4-log) | Host / Connector | Pfad | nein | none | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Setzt einen Connector-Ereignispfad; aktuelle Apache- und NGINX-Pfade verwenden ihn auch für frühere Regel-/Interventionsmetadaten, nicht nur für P4. |
| [`modsecurity_phase4_mode`](#modsecurity-phase4-mode) | Host / Connector | Aufzählung | nein | safe | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Wählt die angeforderte späte P4-Policy. Vor dem Response-Commit kann ein deny angewendet werden; nach dem Commit unterscheiden die aktuellen Apache-/NGINX-/HTX-Pfade nur strict von nicht-strict. Minimal und safe teilen daher den aktuellen nicht-strict-log_only-Pfad. |
| [`modsecurity_rules`](#modsecurity-rules) | Host / Connector | Zeichenkette | nein | kein Wert; optional | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Lädt während des Konfigurationsladens Inline-Inhalt über libmodsecurity. |
| [`modsecurity_rules_file`](#modsecurity-rules-file) | Host / Connector | Pfad | nein | kein Wert; optional | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Lädt während des Konfigurationsladens eine lokale Regeldatei über libmodsecurity. |
| [`modsecurity_rules_remote`](#modsecurity-rules-remote) | Host / Connector | zwei Zeichenketten | nein | kein Wert; optional | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader von libmodsecurity. |
| [`modsecurity_transaction_id`](#modsecurity-transaction-id) | Host / Connector | Zeichenkette/Ausdruck | nein | kein Wert; der Connector erzeugt eine Ersatzkennung | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Liefert die Engine- und Ereigniskorrelationskennung für eine Transaktion. |
| [`modsecurity_transaction_id_expr`](#modsecurity-transaction-id-expr) | Host / Connector | Apache-Zeichenausdruck | nein | none | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Wertet pro Request einen Apache-Ausdruck für die Transaktionskennung aus. |
| [`modsecurity_use_error_log`](#modsecurity-use-error-log) | Host / Connector | Boolescher Wert | nein | on | Apache RSRC_CONF \| ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln) | Steuert die Weiterleitung von libmodsecurity-Meldungen an das Host-Fehlerlog; die Regelauswertung wird dadurch nicht umgeschaltet. |

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
| Minimal | [minimal/httpd.conf](minimal/httpd.conf) | Aktive Startkonfiguration |
| Sicherer vollständiger Lebenszyklus | [safe/httpd.conf](safe/httpd.conf) | Ausgewählte begrenzte Referenz |
| Strikt | [strict/README.de.md](strict/README.de.md) | Parserunterstützte oder ausdrücklich optionale Grenze |
| DetectionOnly | [detection-only/httpd.conf](detection-only/httpd.conf) | Engine wertet aus/protokolliert ohne disruptive Aktion |
| Deaktiviert | [disabled/httpd.conf](disabled/httpd.conf) | Connector- oder Engine-Pfad deaktiviert |

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
apachectl -t
```

Repository-Ziele: `make check-config-apache` und `make check-config-all-connectors`.

## Optionsdetails

## `CustomLog`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
CustomLog <host-specific-value>
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

apachectl -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `ErrorLog`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
ErrorLog <host-specific-value>
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

apachectl -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `LoadModule`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
LoadModule <host-specific-value>
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

apachectl -t

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `modsecurity`

### Kurzbeschreibung

Schaltet die Erstellung von Connector-Transaktionen frei; dies ist nicht SecRuleEngine.

### Syntax

```text
modsecurity On | Off
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | on \| off (der gemeinsame Parser akzeptiert zusätzlich true/false/1/0/yes/no, sofern der Host diese Werte durchreicht) | nein |

### Standardwert

off

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_ENABLE`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Schaltet die Erstellung von Connector-Transaktionen frei; dies ist nicht SecRuleEngine.

### Validierung und Fehler

msc_config_modsec_state liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/minimal/httpd.conf](../../examples/apache/minimal/httpd.conf).

### Sicherheit und Betrieb

off umgeht die Connector-Verarbeitung P1–P4, auch wenn eine Regeldatei konfiguriert ist.

## `modsecurity_phase4_body_limit`

### Kurzbeschreibung

Begrenzt die vom nativen Connector der P4-Verarbeitung angebotenen Response-Bytes.

### Syntax

```text
modsecurity_phase4_body_limit <positive-bytes>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

1048576

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Begrenzt die vom nativen Connector der P4-Verarbeitung angebotenen Response-Bytes.

### Validierung und Fehler

msc_config_phase4_body_limit liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Ein größeres Limit erhöht die Speicher-/CPU-Exposition; null ist in den nativen Settern ungültig.

## `modsecurity_phase4_content_types_file`

### Kurzbeschreibung

Beschränkt die P4-Response-Body-Inspektion auf konfigurierte MIME-Typen.

### Syntax

```text
modsecurity_phase4_content_types_file <value>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | eine lesbare Datei mit MIME-Token | nein |

### Standardwert

Host-Standardwerte bei Auslassung

Quelle: `connectorspezifischer Standard-Content-Type-Loader`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Beschränkt die P4-Response-Body-Inspektion auf konfigurierte MIME-Typen.

### Validierung und Fehler

msc_config_phase4_content_types_file liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Den Geltungsbereich eng halten und validieren, dass der Host die beabsichtigte Repräsentation der Response-Bytes bereitstellt.

## `modsecurity_phase4_log`

### Kurzbeschreibung

Setzt einen Connector-Ereignispfad; aktuelle Apache- und NGINX-Pfade verwenden ihn auch für frühere Regel-/Interventionsmetadaten, nicht nur für P4.

### Syntax

```text
modsecurity_phase4_log <value>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | ein Pfad für das Connector-JSONL-Ereignis-/Interventionslog | nein |

### Standardwert

none

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Setzt einen Connector-Ereignispfad; aktuelle Apache- und NGINX-Pfade verwenden ihn auch für frühere Regel-/Interventionsmetadaten, nicht nur für P4.

### Validierung und Fehler

msc_config_phase4_log liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

JSONL-Metadaten als sensible Betriebsdaten behandeln und sichere Eigentümerschaft/Rotation festlegen.

## `modsecurity_phase4_mode`

### Kurzbeschreibung

Wählt die angeforderte späte P4-Policy. Vor dem Response-Commit kann ein deny angewendet werden; nach dem Commit unterscheiden die aktuellen Apache-/NGINX-/HTX-Pfade nur strict von nicht-strict. Minimal und safe teilen daher den aktuellen nicht-strict-log_only-Pfad.

### Syntax

```text
modsecurity_phase4_mode minimal | safe | strict
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Aufzählung | minimal \| safe \| strict | nein |

### Standardwert

safe

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Wählt die angeforderte späte P4-Policy. Vor dem Response-Commit kann ein deny angewendet werden; nach dem Commit unterscheiden die aktuellen Apache-/NGINX-/HTX-Pfade nur strict von nicht-strict. Minimal und safe teilen daher den aktuellen nicht-strict-log_only-Pfad.

### Validierung und Fehler

msc_config_phase4_mode liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

strict darf nicht als garantierte spätere 403 beschrieben werden; hostspezifische Nachweise für den Abbruch sind erforderlich.

## `modsecurity_rules`

### Kurzbeschreibung

Lädt während des Konfigurationsladens Inline-Inhalt über libmodsecurity.

### Syntax

```text
modsecurity_rules <value>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette | eine Inline-Zeichenkette für ModSecurity-Regel/Konfiguration | nein |

### Standardwert

kein Wert; optional

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Lädt während des Konfigurationsladens Inline-Inhalt über libmodsecurity.

### Validierung und Fehler

msc_config_load_rules liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Inline-Regeln sind ausführbare Policy; einschränken, wer die Hostkonfiguration ändern darf.

## `modsecurity_rules_file`

### Kurzbeschreibung

Lädt während des Konfigurationsladens eine lokale Regeldatei über libmodsecurity.

### Syntax

```text
modsecurity_rules_file <value>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | lesbarer ModSecurity-Konfigurations-/Regeldateipfad | nein |

### Standardwert

kein Wert; optional

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Lädt während des Konfigurationsladens eine lokale Regeldatei über libmodsecurity.

### Validierung und Fehler

msc_config_load_rules_file liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/minimal/httpd.conf](../../examples/apache/minimal/httpd.conf).

### Sicherheit und Betrieb

Die Datei und ihre übergeordneten Verzeichnisse für nicht vertrauenswürdige Identitäten nicht schreibbar halten.

## `modsecurity_rules_remote`

### Kurzbeschreibung

Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader von libmodsecurity.

### Syntax

```text
modsecurity_rules_remote <key> <url>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| zwei Zeichenketten | Schlüssel und URL | nein |

### Standardwert

kein Wert; optional

Quelle: `Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader von libmodsecurity.

### Validierung und Fehler

msc_config_load_rules_remote liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Remote-Policy wird von den ausgewählten no-CRS-Beispielen nicht verwendet; nicht als Ersatz für eine lokale Datei behandeln.

## `modsecurity_transaction_id`

### Kurzbeschreibung

Liefert die Engine- und Ereigniskorrelationskennung für eine Transaktion.

### Syntax

```text
modsecurity_transaction_id <value>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Ausdruck | nichtleere hostspezifische Transaktionskennung | nein |

### Standardwert

kein Wert; der Connector erzeugt eine Ersatzkennung

Quelle: `Connector-Pfad zur Transaktionserzeugung`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Liefert die Engine- und Ereigniskorrelationskennung für eine Transaktion.

### Validierung und Fehler

msc_config_transaction_id liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Keine Zugangsdaten oder sensiblen Request-Daten in eine Korrelationskennung aufnehmen.

## `modsecurity_transaction_id_expr`

### Kurzbeschreibung

Wertet pro Request einen Apache-Ausdruck für die Transaktionskennung aus.

### Syntax

```text
modsecurity_transaction_id_expr <apache-string-expression>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Apache-Zeichenausdruck | ein nichtleerer Apache-Ausdruck | nein |

### Standardwert

none

Quelle: `Die Apache-Parserregistrierung hat keinen Standardwert`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Wertet pro Request einen Apache-Ausdruck für die Transaktionskennung aus.

### Validierung und Fehler

msc_config_transaction_id_expr liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Sicherheit und Betrieb

Ausdruckseingaben als Metadaten behandeln; Geheimnisse nicht in Logs offenlegen.

## `modsecurity_use_error_log`

### Kurzbeschreibung

Steuert die Weiterleitung von libmodsecurity-Meldungen an das Host-Fehlerlog; die Regelauswertung wird dadurch nicht umgeschaltet.

### Syntax

```text
modsecurity_use_error_log <value>
```

### Gültige Kontexte

- Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | on \| off | nein |

### Standardwert

on

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG`.

### Vererbung und Zusammenführung

Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.

Zusammenführung: Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.

Steuert die Weiterleitung von libmodsecurity-Meldungen an das Host-Fehlerlog; die Regelauswertung wird dadurch nicht umgeschaltet.

### Validierung und Fehler

msc_config_use_error_log liefert für die dokumentierte ungültige Eingabe einen Apache-Konfigurationsfehler; die installierte Konfiguration mit apachectl -t validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/minimal/httpd.conf](../../examples/apache/minimal/httpd.conf).

### Sicherheit und Betrieb

Fehlerlogs können Sicherheitsmetadaten enthalten; sie schützen und rotieren.
