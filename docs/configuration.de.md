# Konfiguration

**Sprache:** [English](configuration.md) | Deutsch

## Geltungsbereich

Konfiguration hat drei getrennte Ebenen. Eine Einstellung auf einer Ebene ist
keine implizite Einstellung auf einer anderen Ebene, und keine Einstellung
allein beweist ein Laufzeitergebnis.

| Ebene | Zweck | Maßgebliches Detail |
| --- | --- | --- |
| Host oder Connector | Registriert und konfiguriert eine ausgewählte Hostintegration | Der passende Connector-Guide und seine vollständige Beispielreferenz |
| Common Runtime | Parst die ausgewählte lokale Key/Value-Servicekonfiguration, wenn ein Pfad sie verwendet | [Common-Runtime-Referenz](../examples/common/common-connector-configuration.de.md) |
| ModSecurity Engine | Lädt und wertet <code>Sec*</code>-Regeln aus | [Engine-Direktivenreferenz](../examples/common/modsecurity-directives.de.md) |

## Konfigurationsprinzipien

Ein Konfigurationsprofil darf nur mit dem Connector und der Hostsyntax verwendet
werden, für die es geschrieben wurde. Build-, Cache-, Runtime-, Log- und
Evidence-Ausgaben bleiben außerhalb des Repository-Checkouts. Secrets werden
über einen geeigneten externen Secret-Mechanismus bereitgestellt; sie gehören
nicht in eingecheckte Beispiele, Regeln oder generierte Nachweise.

<code>SecRuleEngine</code>, ein Host-Connector-Enable/Disable-Schalter,
Body-Access-Kontrollen und ein P4-Modus sind unterschiedliche Kontrollen.
Insbesondere kann ein aktivierter Hostconnector ein Regelwerk mit
<code>SecRuleEngine Off</code> laden, und <code>DetectionOnly</code> wertet aus
und protokolliert ohne disruptive Regelaktionen anzuwenden.

## Profile und spätes Verhalten

| Profil | Vorgesehene Verwendung | Grenze |
| --- | --- | --- |
| Minimal | Kleinste ausgewählte Host-/Serviceform | Es ist ein Syntax-/Konfigurationsausgangspunkt, kein Lifecycle-Nachweis |
| Safe | Ausgewählte P1--P4-Safe-Referenz | Beobachtungen nach Commit bleiben konservativ und payload-sicher |
| Strict | Ausdrücklich separates optionales Profil | Es beweist keinen client-sichtbaren späten Abbruch |
| DetectionOnly | Regeln werten aus und protokollieren | Disruptive Regelaktionen werden nicht angewendet |
| Disabled | Engine oder Hostintegration ist wie dokumentiert deaktiviert | Es testet nicht den aktivierten Connectorpfad |

Die eingecheckten Profildateien sind maßgeblich. Ihre vollständige
Connectorsyntax, Defaults, Kontexte, Merge-Regeln, Platzhalter und
Validierungshinweise werden aus Quellverträgen und Beispielen generiert.

## Vollständige Connector-Referenzen

| Connector | Vollständige Direktiven-/Konfigurationsreferenz |
| --- | --- |
| Apache | [Apache](../examples/apache/configuration-reference.de.md) |
| NGINX | [NGINX](../examples/nginx/configuration-reference.de.md) |
| HAProxy | [HAProxy](../examples/haproxy/configuration-reference.de.md) |
| Envoy | [Envoy](../examples/envoy/configuration-reference.de.md) |
| Traefik | [Traefik](../examples/traefik/configuration-reference.de.md) |
| lighttpd | [lighttpd](../examples/lighttpd/configuration-reference.de.md) |

Kompatibilitätseinträge in diesen Referenzen sind absichtlich markiert. Sie
ändern nicht den ausgewählten Integrationsmodus und begründen keine
Unterstützung für einen nicht ausgewählten Pfad.

## Variablen, Platzhalter und Validierung

Die ausführliche Referenz für Repository- und Harness-Variablen ist
[Variablen](reference/variables.de.md). Sie definiert erlaubtes Format,
Default, Setter, Scope, Wirkung, Beispiele und Sicherheitshinweise für jede
dokumentierte Variable oder jeden Platzhalter.

Eine ausgewählte Hostkonfiguration wird mit
<code>make check-config-&lt;connector&gt;</code> validiert, soweit dieses Target
existiert. Erfolgreiches Konfigurationsladen führt keinen Verkehr aus,
validiert Regeln nicht über den Scope dieser Prüfung hinaus und befördert kein
Laufzeitergebnis. Die [Test- und Evidence-Anleitung](testing-and-evidence.de.md)
erklärt die Unterscheidung.

## Direktivenparität und Kompatibilität

Direktivnamen können geteilt sein, während Hostparser-Syntax, Kontext,
Vererbung und Auswertungssemantik verschieden sind. Apache-Ausdruckssyntax ist
keine NGINX-Direktive, und Common-Runtime-Schlüssel dürfen nicht als nicht
registrierte Hostdirektiven dokumentiert werden. Kompatibilitätspfade bleiben
vom ausgewählten nativen Pfad getrennt; ihre Beispiele beschreiben nur ihre
angegebene Grenze.

| Oberfläche | Apache | NGINX | Grenze |
| --- | --- | --- |
| <code>modsecurity</code>, Regeln, Regelfiles, Remote-Regeln | Registrierte Hostdirektiven | Registrierte Hostdirektiven | Rule-Load bleibt connector-eigen |
| <code>modsecurity_transaction_id</code> | Statische-String-Semantik | Per-Request-Complex-Value-Semantik | Gleicher Name bedeutet nicht gleiche Auswertung |
| <code>modsecurity_transaction_id_expr</code> | Registrierte Apache-Ausdrucksdirektive | Nicht registriert | Apache-Ausdruckssyntax nicht nach NGINX kopieren |
| Begrenzte P4-Kontrollen | Registrierte Hostdirektiven | Registrierte Hostdirektiven | Body-Limit/Scope befördert keine vollständige Response-Body-Unterstützung |
| HAProxy-Konfiguration | Native HTX-Hostkonfiguration | Nicht anwendbar | Historisches SPOE/SPOP bleibt eine getrennte Kompatibilitätsoberfläche |

Geteilte Direktivenmetadaten sind connector-neutral; Hostregistrierung, Merge,
Lebensdauern, Hooks, Filter und tatsächliche Laufzeitwirkung bleiben
connector-eigen.

## Verwandte Referenzen

- [Architektur](architecture.de.md)
- [Connector-Guides](connectors/README.de.md)
- [Gemeinsame Regelbeispiele](../examples/common/rule-examples.de.md)
- [Glossar](reference/glossary.de.md)
