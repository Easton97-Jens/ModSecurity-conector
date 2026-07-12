# Dokumentationsindex

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis ist der Dokumentationseinstieg für den ausgewählten
Sechs-Connector-HTTP/1.1-Kern. Es beschreibt aktuelle Repository-Grenzen ohne
Produktionsreife, CRS-Verifikation, vollständige HTTP/2-/HTTP/3-Verifikation,
vollständige Matrix oder Strict-Verhalten für jeden Connector zu behaupten.

## Einstieg

| Bedarf | Kanonisches Dokument | Source-of-Truth-Grenze |
| --- | --- | --- |
| Einen Checkout initialisieren | [Einstieg](getting-started.de.md) | Framework-Setup und begrenzter erster Validierungsweg |
| Repository-Architektur | [Architektur](architecture.de.md) | Eingecheckte Source-Ownership und dokumentierte Lifecycle-Grenze |
| Host-, Runtime- und Engine-Konfiguration | [Konfiguration](configuration.de.md) | Vollständige Connector-Syntax bleibt in <code>examples/</code> |
| Variablen und Begriffe | [Variablen](reference/variables.de.md) / [Glossar](reference/glossary.de.md) | Root-Makefile, Wrapper und dokumentierte Verträge |
| Einen Host bauen | [Build](build/README.de.md) | Root-/Connector-Build-Inputs und Compiler-Guides |
| Tests oder Artefakte deuten | [Tests und Nachweise](testing-and-evidence.de.md) | Ausgewählte Run-Records und Framework-Schemata |
| Sicher betreiben | [Betrieb und Sicherheit](operations-and-security.de.md) | Explizite Deployment-, Limit-, Datenschutz- und Provenienzgrenze |
| Einen Connector wählen | [Connector-Index](connectors/README.de.md) | Ausgewählter Integrationsmodus und Connector-Guide |

## Connector-Guides

| Connector | Ausgewählter Modus | Kanonischer Guide |
| --- | --- | --- |
| Apache | <code>native-httpd-module</code> | [Apache](connectors/apache.de.md) |
| NGINX | <code>native-nginx-http-module</code> | [NGINX](connectors/nginx.de.md) |
| HAProxy | <code>native-htx-filter</code> | [HAProxy](connectors/haproxy.de.md) |
| Envoy | <code>ext_proc</code> | [Envoy](connectors/envoy.de.md) |
| Traefik | <code>native-traefik-middleware</code> | [Traefik](connectors/traefik.de.md) |
| lighttpd | <code>patched-native-lighttpd</code> | [lighttpd](connectors/lighttpd.de.md) |

Ausgewähltes Profil und aufgezeichneter Integrationsmodus sind verwandte, aber
getrennte Identitäten. Der kanonische Zustand einer Fähigkeit beginnt in jedem
<code>capabilities.json</code> des Connectors; Profil, Build, Source-Tree oder
generiertes Inventar sind kein PASS-Ergebnis.

## Aktueller Scope und Evidence

Das Repository zeichnet ausgewählte Lifecycle-Evidence nach Run-ID auf. Ein
enger <code>minimal_runtime_smoke</code>, ein Konfigurationsladen oder ein
Source-Level-Contract-Check belegt nur seine angegebene Ebene. Lesen Sie
[Reports](../reports/README.de.md), bevor Sie einen zeitabhängigen
Statusclaim formulieren.

## Unterstützendes Material

- [Compiler-Guides](build/compilers/README.de.md)
- [Lizenz, Origin und Betriebsgrenze](operations-and-security.de.md)
- [Common-Source-Tree-Guide](../common/README.de.md)
- [Konfigurationsbeispiele](../examples/README.de.md)
- [Framework-Modul](../modules/ModSecurity-test-Framework/README.de.md)

Repository-eigene englische/deutsche Dokumentation wird mit
<code>make check-bilingual-docs</code> geprüft. Generierte Ausgaben werden über
Generator und Source-Vertrag geändert, nicht durch manuelle Änderungen.
