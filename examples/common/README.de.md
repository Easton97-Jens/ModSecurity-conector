# Gemeinsame Beispiel-Konfigurationsreferenz

**Sprache:** [English](README.md) | Deutsch

## Hier beginnen

Diese Seiten erklären Konfiguration, die mehrere Beispiel-Familien gemeinsam
nutzen. Lesen Sie [Common-Connector-Konfiguration](common-connector-configuration.de.md)
für die gemeinsame Runtime-`key=value`-Oberfläche,
[ModSecurity-Direktiven](modsecurity-directives.de.md) für in Beispielen
verwendete Engine-Einstellungen und [Regelbeispiele](rule-examples.de.md) für
den Unterschied zwischen Enforcement, DetectionOnly und Engine Off.

Hostspezifische Parser-Syntax bleibt im passenden Host-Beispiel-Guide und in
der generierten Konfigurationsreferenz.

Diese zentrale Referenz trennt vier Ebenen: Host-/Connector-Konfiguration, Common Runtime, ModSecurity Engine und Beispielplatzhalter. Die sechs Connector-Referenzen verlinken hierher, ohne Common-Schlüssel als nicht registrierte Hostdirektiven auszugeben.

| Material | Ebene | Zweck |
| --- | --- | --- |
| [Common-Runtime-Konfiguration](common-connector-configuration.de.md) | Common Runtime | Vollständige aktuelle `key=value`-Parseroptionen. |
| [ModSecurity-Engine-Direktiven](modsecurity-directives.de.md) | ModSecurity Engine | Tatsächlich in Beispielregeldateien verwendete `Sec*`-Direktiven. |
| [Regelbeispiele](rule-examples.de.md) | ModSecurity Engine | On, DetectionOnly, Off sowie P1/P4-Erklärung. |
| [Zentrale Variablenreferenz](../../docs/reference/variables.de.md) | Umgebung/Laufzeit | Repository- und Harness-Variablen. |

## Umgebungs- und Laufzeitwerte

`BUILD_ROOT`, `NO_CRS_RUN_ID`, `EVIDENCE_ROOT`, `CACHE_ROOT` und connector-spezifische Materializerwerte gehören zur Laufzeit/CI, nicht in Hostdirektiven. Der Envoy-Template-Materializer verwendet die explizit dokumentierten `@...@`-Platzhalter; generierte Dateien müssen außerhalb des Checkouts liegen.
