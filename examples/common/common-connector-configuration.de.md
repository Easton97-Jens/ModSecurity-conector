# Gemeinsame Connector-Konfiguration

**Sprache:** [English](common-connector-configuration.md) | Deutsch

## Geltungsbereich

Dies ist die vollständige aktuelle `key=value`-Parseroberfläche von `common/runtime/msconnector_runtime.c`. Daraus folgt nicht, dass jeder Host jeden Schlüssel als Hostdirektive anbietet.

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`body_limit_action`](#body-limit-action) | Common Runtime | Aufzählung | nein | reject | Common-Runtime-key=value-Datei | Steuert, ob ein Chunk über dem Limit vor der Engine-Eingabe abgewiesen oder gekürzt wird. |
| [`default_block_status`](#default-block-status) | Common Runtime | HTTP-Status | nein | 403 | Common-Runtime-key=value-Datei | Fallback-Status für unterstützte Sperraktionen vor dem Commit. |
| [`default_error_status`](#default-error-status) | Common Runtime | HTTP-Fehlerstatus | nein | 500 | Common-Runtime-key=value-Datei | Fallback-Status für Runtime-Fehler. |
| [`enabled`](#enabled) | Common Runtime | Boolescher Wert | nein | off | Common-Runtime-key=value-Datei | Aktiviert die Common Runtime; eine aktivierte Runtime benötigt eine Inline-, Datei- oder Remote-Regelquelle. |
| [`event_path`](#event-path) | Common Runtime | Pfad | nein | none | Common-Runtime-key=value-Datei | Hängt bei Konfiguration JSONL-Ereignisse an, die nur Metadaten enthalten. |
| [`late_intervention_timeout`](#late-intervention-timeout) | Common Runtime | nichtnegative dezimale Millisekundenanzahl | nein | 0 | Common-Runtime-key=value-Datei | Speichert ein optionales Budget für späte Interventionen; Common besitzt keine Timer-/Abbruchprimitive. |
| [`max_event_json_bytes`](#max-event-json-bytes) | Common Runtime | positive dezimale Byteanzahl | nein | 16384 | Common-Runtime-key=value-Datei | Begrenzt die Größe serialisierter Metadatenereignisse. |
| [`max_header_count`](#max-header-count) | Common Runtime | positive dezimale Anzahl | nein | 256 | Common-Runtime-key=value-Datei | Begrenzt die akzeptierte Headeranzahl. |
| [`max_header_name_size`](#max-header-name-size) | Common Runtime | positive dezimale Byteanzahl | nein | 256 | Common-Runtime-key=value-Datei | Begrenzt die Größe jedes Headernamens. |
| [`max_header_value_size`](#max-header-value-size) | Common Runtime | positive dezimale Byteanzahl | nein | 8192 | Common-Runtime-key=value-Datei | Begrenzt die Größe jedes Headerwerts. |
| [`max_total_header_bytes`](#max-total-header-bytes) | Common Runtime | positive dezimale Byteanzahl | nein | 65536 | Common-Runtime-key=value-Datei | Begrenzt die gesamte Header-Byteanzahl. |
| [`phase4_content_types_file`](#phase4-content-types-file) | Common Runtime | Pfad | nein | none | Common-Runtime-key=value-Datei | Speichert einen Content-Type-Dateipfad; die Verwendung ist connectorspezifisch. |
| [`phase4_event_log`](#phase4-event-log) | Common Runtime | Pfad-Alias | nein | none | Common-Runtime-key=value-Datei | Alias für event_path. |
| [`phase4_mode`](#phase4-mode) | Common Runtime | Aufzählung | nein | safe | Common-Runtime-key=value-Datei | Speichert die späte P4-Policy. Common allein besitzt keine Host-Abbruchprimitive. |
| [`request_body_limit`](#request-body-limit) | Common Runtime | positive dezimale Byteanzahl | nein | 1048576 | Common-Runtime-key=value-Datei | Begrenzt die der Engine angebotenen Request-Bytes. |
| [`request_body_mode`](#request-body-mode) | Common Runtime | Aufzählung | nein | buffered | Common-Runtime-key=value-Datei | Wählt den Common-Modus zur Request-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge. |
| [`response_body_limit`](#response-body-limit) | Common Runtime | positive dezimale Byteanzahl | nein | 1048576 | Common-Runtime-key=value-Datei | Begrenzt die der Engine angebotenen Response-Bytes. |
| [`response_body_mode`](#response-body-mode) | Common Runtime | Aufzählung | nein | none | Common-Runtime-key=value-Datei | Wählt den Common-Modus zur Response-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge. |
| [`rules_file`](#rules-file) | Common Runtime | Pfad | nein | none | Common-Runtime-key=value-Datei | Lädt Regeln aus einer lokalen Datei. |
| [`rules_inline`](#rules-inline) | Common Runtime | Zeichenkette | nein | none | Common-Runtime-key=value-Datei | Fügt eine Inline-Regelkonfiguration hinzu. |
| [`rules_remote_key`](#rules-remote-key) | Common Runtime | Zeichenkette | nein | none | Common-Runtime-key=value-Datei | Liefert eine Hälfte eines Remote-Regelpaares. |
| [`rules_remote_url`](#rules-remote-url) | Common Runtime | URL | nein | none | Common-Runtime-key=value-Datei | Liefert den Remote-Regelendpunkt; die ausgewählten Beispiele verwenden ihn nicht. |
| [`transaction_id`](#transaction-id) | Common Runtime | Zeichenkette | nein | none | Common-Runtime-key=value-Datei | Setzt eine statische Runtime-Transaktionskennung. |
| [`transaction_id_header`](#transaction-id-header) | Common Runtime | Headername | nein | x-request-id | Common-Runtime-key=value-Datei | Wählt den Fallback-Namen des Korrelations-Headers. |
| [`use_error_log`](#use-error-log) | Common Runtime | Boolescher Wert | nein | on | Common-Runtime-key=value-Datei | Speichert die Common-Logging-Präferenz. Ein Connector muss sie verwenden, bevor eine Logging-Wirkung beim Host behauptet werden kann. |

## Optionsdetails

## `body_limit_action`

### Kurzbeschreibung

Steuert, ob ein Chunk über dem Limit vor der Engine-Eingabe abgewiesen oder gekürzt wird.

### Syntax

```text
body_limit_action=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Aufzählung | reject \| process_partial (akzeptierte Schreibvarianten sind parserspezifisch) | nein |

### Standardwert

reject

Quelle: `common/src/config.c:msconnector_config_apply_defaults`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Steuert, ob ein Chunk über dem Limit vor der Engine-Eingabe abgewiesen oder gekürzt wird.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Steuert, ob ein Chunk über dem Limit vor der Engine-Eingabe abgewiesen oder gekürzt wird.

## `default_block_status`

### Kurzbeschreibung

Fallback-Status für unterstützte Sperraktionen vor dem Commit.

### Syntax

```text
default_block_status=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| HTTP-Status | zulässiger Sperrstatus | nein |

### Standardwert

403

Quelle: `common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_BLOCK_STATUS`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Fallback-Status für unterstützte Sperraktionen vor dem Commit.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Fallback-Status für unterstützte Sperraktionen vor dem Commit.

## `default_error_status`

### Kurzbeschreibung

Fallback-Status für Runtime-Fehler.

### Syntax

```text
default_error_status=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| HTTP-Fehlerstatus | gültiger HTTP-Fehlerstatus | nein |

### Standardwert

500

Quelle: `common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_ERROR_STATUS`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Fallback-Status für Runtime-Fehler.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Fallback-Status für Runtime-Fehler.

## `enabled`

### Kurzbeschreibung

Aktiviert die Common Runtime; eine aktivierte Runtime benötigt eine Inline-, Datei- oder Remote-Regelquelle.

### Syntax

```text
enabled=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | on \| off \| true \| false \| 1 \| 0 \| yes \| no | nein |

### Standardwert

off

Quelle: `common/src/config.c:msconnector_config_apply_defaults`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Aktiviert die Common Runtime; eine aktivierte Runtime benötigt eine Inline-, Datei- oder Remote-Regelquelle.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Aktiviert die Common Runtime; eine aktivierte Runtime benötigt eine Inline-, Datei- oder Remote-Regelquelle.

## `event_path`

### Kurzbeschreibung

Hängt bei Konfiguration JSONL-Ereignisse an, die nur Metadaten enthalten.

### Syntax

```text
event_path=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | Pfad ohne übergeordnetes Verzeichnissegment | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Hängt bei Konfiguration JSONL-Ereignisse an, die nur Metadaten enthalten.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Hängt bei Konfiguration JSONL-Ereignisse an, die nur Metadaten enthalten.

## `late_intervention_timeout`

### Kurzbeschreibung

Speichert ein optionales Budget für späte Interventionen; Common besitzt keine Timer-/Abbruchprimitive.

### Syntax

```text
late_intervention_timeout=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| nichtnegative dezimale Millisekundenanzahl | 0 oder positive Ganzzahl | nein |

### Standardwert

0

Quelle: `common/src/config.c:msconnector_config_apply_defaults`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Speichert ein optionales Budget für späte Interventionen; Common besitzt keine Timer-/Abbruchprimitive.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Speichert ein optionales Budget für späte Interventionen; Common besitzt keine Timer-/Abbruchprimitive.

## `max_event_json_bytes`

### Kurzbeschreibung

Begrenzt die Größe serialisierter Metadatenereignisse.

### Syntax

```text
max_event_json_bytes=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

16384

Quelle: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_EVENT_JSON_BYTES`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Begrenzt die Größe serialisierter Metadatenereignisse.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Begrenzt die Größe serialisierter Metadatenereignisse.

## `max_header_count`

### Kurzbeschreibung

Begrenzt die akzeptierte Headeranzahl.

### Syntax

```text
max_header_count=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Anzahl | positive Ganzzahl | nein |

### Standardwert

256

Quelle: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_COUNT`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Begrenzt die akzeptierte Headeranzahl.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Begrenzt die akzeptierte Headeranzahl.

## `max_header_name_size`

### Kurzbeschreibung

Begrenzt die Größe jedes Headernamens.

### Syntax

```text
max_header_name_size=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

256

Quelle: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_NAME_LENGTH`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Begrenzt die Größe jedes Headernamens.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Begrenzt die Größe jedes Headernamens.

## `max_header_value_size`

### Kurzbeschreibung

Begrenzt die Größe jedes Headerwerts.

### Syntax

```text
max_header_value_size=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

8192

Quelle: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_VALUE_LENGTH`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Begrenzt die Größe jedes Headerwerts.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Begrenzt die Größe jedes Headerwerts.

## `max_total_header_bytes`

### Kurzbeschreibung

Begrenzt die gesamte Header-Byteanzahl.

### Syntax

```text
max_total_header_bytes=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

65536

Quelle: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_TOTAL_HEADER_BYTES`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Begrenzt die gesamte Header-Byteanzahl.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Begrenzt die gesamte Header-Byteanzahl.

## `phase4_content_types_file`

### Kurzbeschreibung

Speichert einen Content-Type-Dateipfad; die Verwendung ist connectorspezifisch.

### Syntax

```text
phase4_content_types_file=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | ein Konfigurationspfad | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Speichert einen Content-Type-Dateipfad; die Verwendung ist connectorspezifisch.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Speichert einen Content-Type-Dateipfad; die Verwendung ist connectorspezifisch.

## `phase4_event_log`

### Kurzbeschreibung

Alias für event_path.

### Syntax

```text
phase4_event_log=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad-Alias | gleiche Grammatik wie event_path | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Alias für event_path.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Alias für event_path.

## `phase4_mode`

### Kurzbeschreibung

Speichert die späte P4-Policy. Common allein besitzt keine Host-Abbruchprimitive.

### Syntax

```text
phase4_mode=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Aufzählung | minimal \| safe \| strict | nein |

### Standardwert

safe

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Speichert die späte P4-Policy. Common allein besitzt keine Host-Abbruchprimitive.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Speichert die späte P4-Policy. Common allein besitzt keine Host-Abbruchprimitive.

## `request_body_limit`

### Kurzbeschreibung

Begrenzt die der Engine angebotenen Request-Bytes.

### Syntax

```text
request_body_limit=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

1048576

Quelle: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_BODY_BUFFER_SIZE`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Begrenzt die der Engine angebotenen Request-Bytes.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Begrenzt die der Engine angebotenen Request-Bytes.

## `request_body_mode`

### Kurzbeschreibung

Wählt den Common-Modus zur Request-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.

### Syntax

```text
request_body_mode=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Aufzählung | none \| buffered \| streaming | nein |

### Standardwert

buffered

Quelle: `common/runtime/msconnector_runtime.c:runtime_defaults`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Wählt den Common-Modus zur Request-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Wählt den Common-Modus zur Request-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.

## `response_body_limit`

### Kurzbeschreibung

Begrenzt die der Engine angebotenen Response-Bytes.

### Syntax

```text
response_body_limit=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| positive dezimale Byteanzahl | positive Ganzzahl | nein |

### Standardwert

1048576

Quelle: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Begrenzt die der Engine angebotenen Response-Bytes.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Begrenzt die der Engine angebotenen Response-Bytes.

## `response_body_mode`

### Kurzbeschreibung

Wählt den Common-Modus zur Response-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.

### Syntax

```text
response_body_mode=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Aufzählung | none \| buffered \| streaming | nein |

### Standardwert

none

Quelle: `common/runtime/msconnector_runtime.c:runtime_defaults`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Wählt den Common-Modus zur Response-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Wählt den Common-Modus zur Response-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.

## `rules_file`

### Kurzbeschreibung

Lädt Regeln aus einer lokalen Datei.

### Syntax

```text
rules_file=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Pfad | eine lesbare Regel-/Konfigurationsdatei | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Lädt Regeln aus einer lokalen Datei.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Lädt Regeln aus einer lokalen Datei.

## `rules_inline`

### Kurzbeschreibung

Fügt eine Inline-Regelkonfiguration hinzu.

### Syntax

```text
rules_inline=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette | eine Inline-Zeichenkette für Regel/Konfiguration | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Fügt eine Inline-Regelkonfiguration hinzu.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Fügt eine Inline-Regelkonfiguration hinzu.

## `rules_remote_key`

### Kurzbeschreibung

Liefert eine Hälfte eines Remote-Regelpaares.

### Syntax

```text
rules_remote_key=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette | Remote-Schlüssel, der mit rules_remote_url gepaart wird | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Liefert eine Hälfte eines Remote-Regelpaares.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Liefert eine Hälfte eines Remote-Regelpaares.

## `rules_remote_url`

### Kurzbeschreibung

Liefert den Remote-Regelendpunkt; die ausgewählten Beispiele verwenden ihn nicht.

### Syntax

```text
rules_remote_url=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| URL | Remote-URL, die mit rules_remote_key gepaart wird | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Liefert den Remote-Regelendpunkt; die ausgewählten Beispiele verwenden ihn nicht.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Liefert den Remote-Regelendpunkt; die ausgewählten Beispiele verwenden ihn nicht.

## `transaction_id`

### Kurzbeschreibung

Setzt eine statische Runtime-Transaktionskennung.

### Syntax

```text
transaction_id=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette | nichtleerer Text | nein |

### Standardwert

none

Quelle: `Runtime-Parser hat keinen Standardwert`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Setzt eine statische Runtime-Transaktionskennung.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Setzt eine statische Runtime-Transaktionskennung.

## `transaction_id_header`

### Kurzbeschreibung

Wählt den Fallback-Namen des Korrelations-Headers.

### Syntax

```text
transaction_id_header=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Headername | nichtleerer HTTP-Headername | nein |

### Standardwert

x-request-id

Quelle: `common/runtime/msconnector_runtime.c:runtime_defaults`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Wählt den Fallback-Namen des Korrelations-Headers.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Wählt den Fallback-Namen des Korrelations-Headers.

## `use_error_log`

### Kurzbeschreibung

Speichert die Common-Logging-Präferenz. Ein Connector muss sie verwenden, bevor eine Logging-Wirkung beim Host behauptet werden kann.

### Syntax

```text
use_error_log=<value>
```

### Gültige Kontexte

- Common-Runtime-key=value-Datei

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Boolescher Wert | on \| off \| true \| false \| 1 \| 0 \| yes \| no | nein |

### Standardwert

on

Quelle: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG`.

### Vererbung und Zusammenführung

Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.

Zusammenführung: Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.

Speichert die Common-Logging-Präferenz. Ein Connector muss sie verwenden, bevor eine Logging-Wirkung beim Host behauptet werden kann.

### Validierung und Fehler

Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Sicherheit und Betrieb

Limits begrenzen den Ressourcenverbrauch. Speichert die Common-Logging-Präferenz. Ein Connector muss sie verwenden, bevor eine Logging-Wirkung beim Host behauptet werden kann.
