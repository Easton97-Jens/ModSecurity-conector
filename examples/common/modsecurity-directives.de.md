# Von Beispielen verwendete ModSecurity-Engine-Direktiven

**Sprache:** [English](modsecurity-directives.md) | Deutsch

## Geltungsbereich

Aufgeführt werden nur Direktiven, die tatsächlich in eingecheckten Beispielregeldateien verwendet werden. Sie gehören zu libmodsecurity und nicht zu einem Apache-, NGINX-, HAProxy-, Envoy-, Traefik- oder lighttpd-Hostparser.

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`IncludeOptional`](#includeoptional) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Lädt optionale Engine-Konfiguration/Regeln, sofern vorhanden. |
| [`SecAuditEngine`](#secauditengine) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Aktiviert die ausgewählte Audit-Log-Policy. |
| [`SecAuditLog`](#secauditlog) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Setzt den Engine-Audit-Log-Pfad. |
| [`SecAuditLogParts`](#secauditlogparts) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Wählt Audit-Log-Teile aus. |
| [`SecAuditLogType`](#secauditlogtype) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Setzt den ausgewählten Schreibmodus für das Audit-Log. |
| [`SecRequestBodyAccess`](#secrequestbodyaccess) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | On stellt der Engine P2 eine Request-Body-Eingabe nur bereit, wenn der Host sie liefert; Off lässt P1-Header verfügbar, entfernt aber die Body-Eingabe aus P2. Die Direktive setzt weder ein Body-Größenlimit noch einen Request-MIME-Geltungsbereich: Diese bleiben Zuordnungsentscheidungen von Host/Engine und, sofern ausgewählt, Steuerungen über Common-Runtime-request_body_limit/Body-Modus. Das Aktivieren der Body-Verarbeitung kann Buffering-, Speicher-, CPU- und Logging-Exposition hinzufügen; daher Hosteingaben begrenzen. |
| [`SecResponseBodyAccess`](#secresponsebodyaccess) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | On ermöglicht P4 nur, wenn der Host Response-Bytes im Geltungsbereich bereitstellt; Off entfernt die Response-Body-Eingabe aus P4. Es erweitert SecResponseBodyMimeType nicht, überschreibt SecResponseBodyLimit/SecResponseBodyLimitAction nicht und erzwingt keine Statusänderung nach dem Header-Commit. Mit der ausgewählten sicheren Late-Intervention-Policy wird ein disruptives Ergebnis nach dem Commit als log_only statt als versprochene spätere 403 protokolliert; das Erfassen der Response kann begrenzte Speicher-, CPU- und Sensitivdaten-Exposition hinzufügen. |
| [`SecResponseBodyLimit`](#secresponsebodylimit) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Begrenzt die Response-Body-Eingabe der Engine. |
| [`SecResponseBodyLimitAction`](#secresponsebodylimitaction) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Definiert das Engine-Verhalten, wenn der Response-Body das Engine-Limit überschreitet. |
| [`SecResponseBodyMimeType`](#secresponsebodymimetype) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Beschränkt die Engine-Response-Body-Inspektion nach MIME-Typ. |
| [`SecRule`](#secrule) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Aus den Beispielen wird kein Standardwert abgeleitet. | geladene ModSecurity-Konfigurations-/Regeldatei | Definiert eine Regel aus Variable, Operator und durch Komma getrennten Actions. Die lokale Illustration verwendet RESPONSE_BODY, @contains, id, phase, deny, log und status; redirect und Transformationen sind separate Action-Formen, deren Gültigkeit und beobachtbare Wirkung von Engine/Host und Commit-Grenze abhängen. |
| [`SecRuleEngine`](#secruleengine) | ModSecurity Engine | ModSecurity-Engine-Direktive | nein | Die verwendeten Beispiele wählen On; keine Repository-Quelle legt einen globalen Engine-Standardwert fest. | geladene ModSecurity-Konfigurations-/Regeldatei | Steuert Regelausführung/disruptive Aktion innerhalb von libmodsecurity, unabhängig vom Hostconnector-Schalter. |

## Regel-Syntax im Detail

```apache
SecRule RESPONSE_BODY "@contains response-attack" \
    "id:1100301,phase:4,deny,log,status:403"
```

`RESPONSE_BODY` ist die Variable, `@contains` der Operator und `response-attack` dessen Argument. Die Actions setzen eine eindeutige `id`, wählen `phase:4`, verlangen `deny`, schreiben mit `log` ein Ereignis und wünschen `status:403` vor dem Host-Commit.
Nach dem Response-Commit kann ein Connector die sichtbare Statuszeile nicht zuverlässig ersetzen. `SecResponseBodyAccess On` und eine P4-Regel bedeuten daher keine garantierte spätere 403-Antwort.
`VARIABLE` wählt die zu prüfenden Daten, `OPERATOR` bestimmt den Vergleich und `ACTIONS` ist die durch Kommas getrennte Steuerliste. `id` identifiziert die Regel eindeutig, `phase` legt den Auswertungszeitpunkt fest, `deny` fordert eine disruptive Entscheidung an und `log` zeichnet den Treffer auf. `status` gilt nur, solange der Host den HTTP-Status noch ändern kann; `redirect` benötigt zusätzlich ein Ziel und ist an dieselbe Commit-Grenze gebunden. Transformationen sind explizite Actions, die Eingaben vor dem Operator verändern; sie sollten sparsam und nachvollziehbar eingesetzt werden. Das gezeigte Beispiel verwendet keine Redirect- oder Transformations-Action.

## Optionsdetails

## `IncludeOptional`

### Kurzbeschreibung

Lädt optionale Engine-Konfiguration/Regeln, sofern vorhanden.

### Syntax

```text
IncludeOptional <path-or-glob>
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | Pfad oder Glob | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Lädt optionale Engine-Konfiguration/Regeln, sofern vorhanden.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecAuditEngine`

### Kurzbeschreibung

Aktiviert die ausgewählte Audit-Log-Policy.

### Syntax

```text
SecAuditEngine RelevantOnly
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | Engine-Auditmodus | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Aktiviert die ausgewählte Audit-Log-Policy.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecAuditLog`

### Kurzbeschreibung

Setzt den Engine-Audit-Log-Pfad.

### Syntax

```text
SecAuditLog <path>
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | Pfad | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Setzt den Engine-Audit-Log-Pfad.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecAuditLogParts`

### Kurzbeschreibung

Wählt Audit-Log-Teile aus.

### Syntax

```text
SecAuditLogParts <parts>
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | Audit-Log-Teilbuchstaben | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Wählt Audit-Log-Teile aus.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecAuditLogType`

### Kurzbeschreibung

Setzt den ausgewählten Schreibmodus für das Audit-Log.

### Syntax

```text
SecAuditLogType Serial
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | Audit-Log-Typ | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Setzt den ausgewählten Schreibmodus für das Audit-Log.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecRequestBodyAccess`

### Kurzbeschreibung

On stellt der Engine P2 eine Request-Body-Eingabe nur bereit, wenn der Host sie liefert; Off lässt P1-Header verfügbar, entfernt aber die Body-Eingabe aus P2. Die Direktive setzt weder ein Body-Größenlimit noch einen Request-MIME-Geltungsbereich: Diese bleiben Zuordnungsentscheidungen von Host/Engine und, sofern ausgewählt, Steuerungen über Common-Runtime-request_body_limit/Body-Modus. Das Aktivieren der Body-Verarbeitung kann Buffering-, Speicher-, CPU- und Logging-Exposition hinzufügen; daher Hosteingaben begrenzen.

### Syntax

```text
SecRequestBodyAccess On | Off
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | On \| Off | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P2. On erlaubt Body-Inspektion erst, nachdem der Connector Request-Bytes bereitgestellt hat; ausgewählter Host-/Runtime-Body-Modus und Limit bestimmen, wie viele Bytes die Engine erreichen können.

On stellt der Engine P2 eine Request-Body-Eingabe nur bereit, wenn der Host sie liefert; Off lässt P1-Header verfügbar, entfernt aber die Body-Eingabe aus P2. Die Direktive setzt weder ein Body-Größenlimit noch einen Request-MIME-Geltungsbereich: Diese bleiben Zuordnungsentscheidungen von Host/Engine und, sofern ausgewählt, Steuerungen über Common-Runtime-request_body_limit/Body-Modus. Das Aktivieren der Body-Verarbeitung kann Buffering-, Speicher-, CPU- und Logging-Exposition hinzufügen; daher Hosteingaben begrenzen.

### Validierung und Fehler

Der Host/libmodsecurity weist beim Laden der Regeldatei ungültige Engine-Syntax ab. Ein syntaktisch gültiges On kann dennoch keine P2-Eingabe erzeugen, wenn der ausgewählte Hostpfad keinen Request-Body bereitstellt.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Sicherheit und Betrieb

Request-Bodys können Zugangsdaten oder personenbezogene Daten enthalten. Begrenzte Body-Limits, passende MIME-/Parser-Policy und geschützte Audit-/Debug-Logs verwenden; hier wird keine Leistungskennzahl abgeleitet.

## `SecResponseBodyAccess`

### Kurzbeschreibung

On ermöglicht P4 nur, wenn der Host Response-Bytes im Geltungsbereich bereitstellt; Off entfernt die Response-Body-Eingabe aus P4. Es erweitert SecResponseBodyMimeType nicht, überschreibt SecResponseBodyLimit/SecResponseBodyLimitAction nicht und erzwingt keine Statusänderung nach dem Header-Commit. Mit der ausgewählten sicheren Late-Intervention-Policy wird ein disruptives Ergebnis nach dem Commit als log_only statt als versprochene spätere 403 protokolliert; das Erfassen der Response kann begrenzte Speicher-, CPU- und Sensitivdaten-Exposition hinzufügen.

### Syntax

```text
SecResponseBodyAccess On | Off
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | On \| Off | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: P4. On ist notwendig, aber nicht hinreichend: Der Connector muss Response-Bytes bereitstellen, der MIME-Typ muss im Geltungsbereich von SecResponseBodyMimeType liegen, und Host-/Engine-Response-Limits gelten.

On ermöglicht P4 nur, wenn der Host Response-Bytes im Geltungsbereich bereitstellt; Off entfernt die Response-Body-Eingabe aus P4. Es erweitert SecResponseBodyMimeType nicht, überschreibt SecResponseBodyLimit/SecResponseBodyLimitAction nicht und erzwingt keine Statusänderung nach dem Header-Commit. Mit der ausgewählten sicheren Late-Intervention-Policy wird ein disruptives Ergebnis nach dem Commit als log_only statt als versprochene spätere 403 protokolliert; das Erfassen der Response kann begrenzte Speicher-, CPU- und Sensitivdaten-Exposition hinzufügen.

### Validierung und Fehler

Der Host/libmodsecurity weist beim Laden der Regeldatei ungültige Engine-Syntax ab. Zur Laufzeit können ein MIME-Typ außerhalb des Geltungsbereichs, ein deaktivierter Host-Body-Pfad oder ein überschrittenes Limit P4 ohne die erwartete vollständige Body-Eingabe lassen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Sicherheit und Betrieb

Response-Bodys können groß und sensibel sein. MIME-Geltungsbereich und Response-Limits eng halten, Logs schützen und sichere Nachweise nach dem Commit nicht mit einer für Clients sichtbaren späteren 403 gleichsetzen.

## `SecResponseBodyLimit`

### Kurzbeschreibung

Begrenzt die Response-Body-Eingabe der Engine.

### Syntax

```text
SecResponseBodyLimit <bytes>
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | positive Byteanzahl | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Begrenzt die Response-Body-Eingabe der Engine.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecResponseBodyLimitAction`

### Kurzbeschreibung

Definiert das Engine-Verhalten, wenn der Response-Body das Engine-Limit überschreitet.

### Syntax

```text
SecResponseBodyLimitAction ProcessPartial | Reject
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | ProcessPartial \| Reject | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Definiert das Engine-Verhalten, wenn der Response-Body das Engine-Limit überschreitet.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecResponseBodyMimeType`

### Kurzbeschreibung

Beschränkt die Engine-Response-Body-Inspektion nach MIME-Typ.

### Syntax

```text
SecResponseBodyMimeType <type/subtype> [...]
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | ein oder mehrere MIME-Typen | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Beschränkt die Engine-Response-Body-Inspektion nach MIME-Typ.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.

## `SecRule`

### Kurzbeschreibung

Definiert eine Regel aus Variable, Operator und durch Komma getrennten Actions. Die lokale Illustration verwendet RESPONSE_BODY, @contains, id, phase, deny, log und status; redirect und Transformationen sind separate Action-Formen, deren Gültigkeit und beobachtbare Wirkung von Engine/Host und Commit-Grenze abhängen.

### Syntax

```text
SecRule VARIABLE "OPERATOR" "id:<id>,phase:<n>,actions"
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | Regelausdruck | nein |

### Standardwert

Aus den Beispielen wird kein Standardwert abgeleitet.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die Phasen-Action wählt den Auswertungspunkt; das lokale RESPONSE_BODY-Beispiel verwendet P4. Eine disruptive Action kann das sichtbare HTTP-Ergebnis nur beeinflussen, solange der Host noch eingreifen kann.

Definiert eine Regel aus Variable, Operator und durch Komma getrennten Actions. Die lokale Illustration verwendet RESPONSE_BODY, @contains, id, phase, deny, log und status; redirect und Transformationen sind separate Action-Formen, deren Gültigkeit und beobachtbare Wirkung von Engine/Host und Commit-Grenze abhängen.

### Validierung und Fehler

Der Host/libmodsecurity weist beim Laden der Regeldatei fehlerhafte Variablen-/Operator-/Action-Syntax, doppelte oder ungültige Kennungen und ungültige Action-Kombinationen ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Sicherheit und Betrieb

Regeln sind ausführbare Sicherheits-Policy. Jeder Regel eine stabile id geben, Transformationen explizit und minimal halten, Eigentümerschaft der Regeldatei schützen und disruptives/Redirect-Verhalten auf dem ausgewählten Host prüfen, bevor man sich darauf verlässt.

## `SecRuleEngine`

### Kurzbeschreibung

Steuert Regelausführung/disruptive Aktion innerhalb von libmodsecurity, unabhängig vom Hostconnector-Schalter.

### Syntax

```text
SecRuleEngine On | Off | DetectionOnly
```

### Gültige Kontexte

- geladene ModSecurity-Konfigurations-/Regeldatei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| ModSecurity-Engine-Direktive | On \| Off \| DetectionOnly | nein |

### Standardwert

Die verwendeten Beispiele wählen On; keine Repository-Quelle legt einen globalen Engine-Standardwert fest.

Quelle: `nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen`.

### Vererbung und Zusammenführung

Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.

Zusammenführung: Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung der Direktive.

Steuert Regelausführung/disruptive Aktion innerhalb von libmodsecurity, unabhängig vom Hostconnector-Schalter.

### Validierung und Fehler

Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Sicherheit und Betrieb

Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.
