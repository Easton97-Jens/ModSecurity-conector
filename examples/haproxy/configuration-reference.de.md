# HAProxy-Konfigurationsreferenz

**Sprache:** [English](configuration-reference.md) | Deutsch

## Geltungsbereich und maßgebliche Quellen

Ausgewählter Integrationsmodus: `native-htx-filter`. Diese Datei wird aus registrierten Parsern, Konfigurationsstrukturen, geprüften Service-Verträgen und aktiven Beispielen erzeugt.
Kompatibilitätseinträge sind ausdrücklich als solche markiert und gehören nicht zum ausgewählten Kernpfad.

## Konfigurationsinventar

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`bind`](#bind) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`default_backend`](#default-backend) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`filter modsecurity-htx`](#filter-modsecurity-htx) | Host / Connector | HAProxy-Filterdeklaration | ja | nicht anwendbar; ein Filter ist nur aktiv, wenn er deklariert ist | Die ausgewählte und eingecheckte native Nutzung ist ein HAProxy-Frontend. Der lokale Parser legt keine weiteren Host-Geltungsbereiche fest. | Native HTX-Filterdeklaration für den vollständigen Lebenszyklus. |
| [`log`](#log) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`mode`](#mode) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`phase4-mode`](#phase4-mode) | Host / Connector | Aufzählung | nein | safe | Die ausgewählte und eingecheckte native Nutzung ist ein HAProxy-Frontend. Der lokale Parser legt keine weiteren Host-Geltungsbereiche fest. | Native HTX-Argument für die späte P4-Policy. |
| [`rules-file`](#rules-file) | Host / Connector | Pfad | ja | kein Wert; erforderlich | Die ausgewählte und eingecheckte native Nutzung ist ein HAProxy-Frontend. Der lokale Parser legt keine weiteren Host-Geltungsbereiche fest. | Erforderliches rules-file-Argument des nativen HTX. |
| [`server`](#server) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`timeout client`](#timeout-client) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`timeout connect`](#timeout-connect) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`timeout server`](#timeout-server) | Host | hosteigenes Konfigurationsfeld | nein | Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt. | Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich. | Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive. |
| [`filter spoe`](#filter-spoe) | Kompatibilität | Kompatibilitätsfilter | nein | nicht Teil des nativen HTX-Pfads | nur Kompatibilitäts-Frontend | SPOE-Filter nur für die Kompatibilität. |
| [`legacy-phase4-strict-abort`](#legacy-phase4-strict-abort) | Kompatibilität | historische Konfiguration | nein | nicht verfügbar | nur historische Kompatibilitätsdokumentation | Deaktiviertes historisches Kompatibilitätsmaterial. |
| [`spoe-agent:audit-log`](#spoe-agent-audit-log) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:case`](#spoe-agent-case) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:crs-root`](#spoe-agent-crs-root) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:debug`](#spoe-agent-debug) | Kompatibilität | Boolescher Wert | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:decision-log`](#spoe-agent-decision-log) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:enable-response-headers`](#spoe-agent-enable-response-headers) | Kompatibilität | Boolescher Wert | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung. |
| [`spoe-agent:expected-status`](#spoe-agent-expected-status) | Kompatibilität | Ganzzahl | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:fail-mode`](#spoe-agent-fail-mode) | Kompatibilität | Kompatibilitäts-Policy-Zeichenkette | nein | closed | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:host`](#spoe-agent-host) | Kompatibilität | Zeichenkette/Pfad | nein | 127.0.0.1 | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:listen`](#spoe-agent-listen) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:log-file`](#spoe-agent-log-file) | Kompatibilität | Zeichenkette/Pfad | nein | - | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:max-transactions`](#spoe-agent-max-transactions) | Kompatibilität | Ganzzahl | nein | 4096 | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:mode`](#spoe-agent-mode) | Kompatibilität | Kompatibilitäts-Policy-Zeichenkette | nein | block | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:modsecurity-conf`](#spoe-agent-modsecurity-conf) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:pid-file`](#spoe-agent-pid-file) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:port`](#spoe-agent-port) | Kompatibilität | Ganzzahl | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:port-file`](#spoe-agent-port-file) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:ready-file`](#spoe-agent-ready-file) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:request-body-limit`](#spoe-agent-request-body-limit) | Kompatibilität | Ganzzahl | nein | 65532 | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:response-body-limit`](#spoe-agent-response-body-limit) | Kompatibilität | Ganzzahl | nein | 0 | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung. |
| [`spoe-agent:response-body-timeout`](#spoe-agent-response-body-timeout) | Kompatibilität | Ganzzahl | nein | 0 | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung. |
| [`spoe-agent:response-phases`](#spoe-agent-response-phases) | Kompatibilität | Boolescher Wert | nein | false | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung. |
| [`spoe-agent:rules-dir`](#spoe-agent-rules-dir) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:rules-file`](#spoe-agent-rules-file) | Kompatibilität | Zeichenkette/Pfad | nein | nicht gesetzt, sofern nicht konfiguriert | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:runtime-mode`](#spoe-agent-runtime-mode) | Kompatibilität | Kompatibilitäts-Policy-Zeichenkette | nein | production | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:spoe-timeout`](#spoe-agent-spoe-timeout) | Kompatibilität | Ganzzahl | nein | 2000 | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:variant`](#spoe-agent-variant) | Kompatibilität | Zeichenkette/Pfad | nein | - | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |
| [`spoe-agent:worker-count`](#spoe-agent-worker-count) | Kompatibilität | Ganzzahl | nein | 1 | SPOE/SPOP-Kompatibilitätsagent-key=value-Datei | SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption. |

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
| Minimal | [minimal/haproxy-htx.cfg](minimal/haproxy-htx.cfg) | Aktive Startkonfiguration |
| Sicherer vollständiger Lebenszyklus | [safe/haproxy-htx.cfg](safe/haproxy-htx.cfg) | Ausgewählte begrenzte Referenz |
| Strikt | [strict/README.de.md](strict/README.de.md) | Parserunterstützte oder ausdrücklich optionale Grenze |
| DetectionOnly | [detection-only/haproxy-htx.cfg](detection-only/haproxy-htx.cfg) | Engine wertet aus/protokolliert ohne disruptive Aktion |
| Deaktiviert | [disabled/haproxy-htx.cfg](disabled/haproxy-htx.cfg) | Connector- oder Engine-Pfad deaktiviert |

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
haproxy -c -f <config>
```

Repository-Ziele: `make check-config-haproxy` und `make check-config-all-connectors`.

## Optionsdetails

## `bind`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
bind <host-specific-value>
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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `default_backend`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
default_backend <host-specific-value>
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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `filter modsecurity-htx`

### Kurzbeschreibung

Native HTX-Filterdeklaration für den vollständigen Lebenszyklus.

### Syntax

```text
filter modsecurity-htx rules-file <path> [phase4-mode minimal|safe|strict]
```

### Gültige Kontexte

- Die ausgewählte und eingecheckte native Nutzung ist ein HAProxy-Frontend. Der lokale Parser legt keine weiteren Host-Geltungsbereiche fest.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| HAProxy-Filterdeklaration | ein erforderliches rules-file-Argument; phase4-mode ist optional | ja |

### Standardwert

nicht anwendbar; ein Filter ist nur aktiv, wenn er deklariert ist

Quelle: `nativer HTX-Schlüsselwortparser`.

### Vererbung und Zusammenführung

Es ist kein Connector-lokaler Vererbungs-Callback registriert; jede Filterdeklaration besitzt eine Filterkonfiguration.

Zusammenführung: Kein Connector-lokaler Merge; Filterargumente initialisieren eine Common-Konfiguration pro Filter.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Native HTX-Callbacks für P1–P4 werden nur angehängt, wenn dieser Filter deklariert ist.

Registriert den nativen HTX-Filter des Repositorys und erzeugt die an die Lebenszyklus-Callbacks übergebene Konfiguration.

### Validierung und Fehler

Der gepatchte HAProxy-Parser weist fehlende/unbekannte Argumente ab; mit haproxy -c -f <config> validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Ein ungepatchtes HAProxy-Binärprogramm bietet dieses Schlüsselwort nicht; SPOE nicht stillschweigend ersetzen.

## `log`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
log <host-specific-value>
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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `mode`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
mode <host-specific-value>
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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `phase4-mode`

### Kurzbeschreibung

Native HTX-Argument für die späte P4-Policy.

### Syntax

```text
phase4-mode minimal | safe | strict
```

### Gültige Kontexte

- Die ausgewählte und eingecheckte native Nutzung ist ein HAProxy-Frontend. Der lokale Parser legt keine weiteren Host-Geltungsbereiche fest.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Aufzählung | minimal \| safe \| strict | nein |

### Standardwert

safe

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Vererbung und Zusammenführung

Es ist kein Connector-lokaler Vererbungs-Callback registriert; jede Filterdeklaration besitzt eine Filterkonfiguration.

Zusammenführung: Kein Connector-lokaler Merge; Filterargumente initialisieren eine Common-Konfiguration pro Filter.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur P4. Die aktuelle HTX-Hostaktion unterscheidet strict von nicht-strict; minimal und safe teilen den späten nicht-strict-log_only-Pfad.

Initialisiert common_config.phase4_mode für den Filter.

### Validierung und Fehler

Ein unbekannter Modus lässt das Parsen fehlschlagen. Der ausgewählte Host verwendet haproxy -c -f <config>.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

strict protokolliert eine Policy-Anforderung zum Abbruch, aber der native HTX-Pfad protokolliert derzeit die Hostaktion not_attempted; dies ist keine Abbruchgarantie.

## `rules-file`

### Kurzbeschreibung

Erforderliches rules-file-Argument des nativen HTX.

### Syntax

```text
rules-file <path>
```

### Gültige Kontexte

- Die ausgewählte und eingecheckte native Nutzung ist ein HAProxy-Frontend. Der lokale Parser legt keine weiteren Host-Geltungsbereiche fest.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | ein lesbarer Regel-/Konfigurationspfad | ja |

### Standardwert

kein Wert; erforderlich

Quelle: `nativer HTX-Parser verlangt rules-file`.

### Vererbung und Zusammenführung

Es ist kein Connector-lokaler Vererbungs-Callback registriert; jede Filterdeklaration besitzt eine Filterkonfiguration.

Zusammenführung: Kein Connector-lokaler Merge; Filterargumente initialisieren eine Common-Konfiguration pro Filter.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Regeln können P1–P4 über den deklarierten HTX-Filter auswerten.

Lädt bei der Filterinitialisierung Regeln mit msc_rules_add_file.

### Validierung und Fehler

Ein fehlendes Argument oder ein Fehler beim Laden der Regeln lässt die native Filterinitialisierung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Eigentümerschaft und Berechtigungen der Policy-Datei schützen.

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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `timeout client`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
timeout client <host-specific-value>
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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `timeout connect`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
timeout connect <host-specific-value>
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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `timeout server`

### Kurzbeschreibung

Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.

### Syntax

```text
timeout server <host-specific-value>
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

haproxy -c -f <config>

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Sicherheit und Betrieb

Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.

## `filter spoe`

### Kurzbeschreibung

SPOE-Filter nur für die Kompatibilität.

### Syntax

```text
filter spoe engine <name> config <file>
```

### Gültige Kontexte

- nur Kompatibilitäts-Frontend

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kompatibilitätsfilter | nur HAProxy-SPOE-Syntax | nein |

### Standardwert

nicht Teil des nativen HTX-Pfads

Quelle: `Kompatibilitätsbeispiel`.

### Vererbung und Zusammenführung

nicht als native Vererbung dokumentiert

Zusammenführung: nicht Teil des nativen HTX-Merge

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Kompatibilitäts-Requestpfad; keine native HTX-P3/P4-Konfiguration.

Leitet an den separaten SPOE/SPOP-Kompatibilitätsservice weiter.

### Validierung und Fehler

Nur separater Kompatibilitäts-Smoke-/Konfigurationscheck.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/haproxy-request-only.cfg](../../examples/haproxy/compatibility-spoe/haproxy-request-only.cfg).

### Sicherheit und Betrieb

Diesen historischen Pfad nicht als ausgewählten nativen Kern hochstufen.

## `legacy-phase4-strict-abort`

### Kurzbeschreibung

Deaktiviertes historisches Kompatibilitätsmaterial.

### Syntax

```text
legacy / disabled example
```

### Gültige Kontexte

- nur historische Kompatibilitätsdokumentation

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| historische Konfiguration | keine aktive ausgewählte Option | nein |

### Standardwert

nicht verfügbar

Quelle: `Kopf des Legacy-Beispiels`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: nicht anwendbar

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Kein ausgewählter P4-Pfad für den Response-Body.

Nur zur Erklärung außer Dienst gestellten Kompatibilitätsmaterials beibehalten.

### Validierung und Fehler

Nicht für die native Validierung verwenden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg](../../examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg).

### Sicherheit und Betrieb

Niemals als Nachweis für P4 oder einen strict-Abbruch verwenden.

## `spoe-agent:audit-log`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
audit-log=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:case`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
case=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:crs-root`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
crs-root=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:debug`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
debug=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | Kompatibilitäts-Boolean im on/off-Stil | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:decision-log`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
decision-log=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:enable-response-headers`

### Kurzbeschreibung

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Syntax

```text
enable-response-headers=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | Kompatibilitäts-Boolean im on/off-Stil | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:expected-status`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
expected-status=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:fail-mode`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
fail-mode=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kompatibilitäts-Policy-Zeichenkette | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

closed

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:host`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
host=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

127.0.0.1

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:listen`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
listen=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:log-file`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
log-file=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

-

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:max-transactions`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
max-transactions=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

4096

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:mode`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
mode=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kompatibilitäts-Policy-Zeichenkette | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

block

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:modsecurity-conf`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
modsecurity-conf=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:pid-file`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
pid-file=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:port`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
port=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:port-file`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
port-file=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:ready-file`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
ready-file=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:request-body-limit`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
request-body-limit=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

65532

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:response-body-limit`

### Kurzbeschreibung

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Syntax

```text
response-body-limit=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

0

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:response-body-timeout`

### Kurzbeschreibung

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Syntax

```text
response-body-timeout=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

0

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:response-phases`

### Kurzbeschreibung

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Syntax

```text
response-phases=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | Kompatibilitäts-Boolean im on/off-Stil | nein |

### Standardwert

false

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:rules-dir`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
rules-dir=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:rules-file`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
rules-file=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

nicht gesetzt, sofern nicht konfiguriert

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:runtime-mode`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
runtime-mode=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kompatibilitäts-Policy-Zeichenkette | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

production

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:spoe-timeout`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
spoe-timeout=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

2000

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:variant`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
variant=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette/Pfad | vom Parser unterstützter Kompatibilitätswert | nein |

### Standardwert

-

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.

## `spoe-agent:worker-count`

### Kurzbeschreibung

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Syntax

```text
worker-count=<value>
```

### Gültige Kontexte

- SPOE/SPOP-Kompatibilitätsagent-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | dezimale Ganzzahl | nein |

### Standardwert

1

Quelle: `config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten`.

### Vererbung und Zusammenführung

Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.

Zusammenführung: Kein Merge; config_set übernimmt einen geparsten Wert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.

SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.

### Validierung und Fehler

Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Sicherheit und Betrieb

Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.
