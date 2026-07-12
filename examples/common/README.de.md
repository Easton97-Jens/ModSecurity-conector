# Gemeinsame Beispiel-Konfigurationsreferenz

**Sprache:** [English](README.md) | Deutsch

Diese zentrale Referenz trennt vier Ebenen: Host-/Connector-Konfiguration, Common Runtime, ModSecurity Engine und Beispielplatzhalter. Die sechs Connector-Referenzen verlinken hierher, ohne Common-Schlüssel als nicht registrierte Hostdirektiven auszugeben.

| Material | Ebene | Zweck |
| --- | --- | --- |
| [Common-Runtime-Konfiguration](common-connector-configuration.de.md) | Common Runtime | Vollständige aktuelle `key=value`-Parseroptionen. |
| [ModSecurity-Engine-Direktiven](modsecurity-directives.de.md) | ModSecurity Engine | Tatsächlich in Beispielregeldateien verwendete `Sec*`-Direktiven. |
| [Regelbeispiele](rule-examples.de.md) | ModSecurity Engine | On, DetectionOnly, Off sowie P1/P4-Erklärung. |
| [Zentrale Variablenreferenz](../../docs/reference/variables.de.md) | Umgebung/Laufzeit | Repository- und Harness-Variablen. |

## Umgebungs- und Laufzeitwerte

`BUILD_ROOT`, `NO_CRS_RUN_ID`, `EVIDENCE_ROOT`, `CACHE_ROOT` und connector-spezifische Materializerwerte gehören zur Laufzeit/CI, nicht in Hostdirektiven. Der Envoy-Template-Materializer verwendet die explizit dokumentierten `@...@`-Platzhalter; generierte Dateien müssen außerhalb des Checkouts liegen.
