# Apache-Connector

**Sprache:** [English](apache.md) | Deutsch

## Überblick

Apache verwendet den ausgewählten Pfad <code>native-httpd-module</code>: ein
über APXS gebautes Apache-HTTPD-Modul mit Bindung an die öffentlichen
libmodsecurity-v3-APIs. Dieser Guide beschreibt nur den ausgewählten
HTTP/1.1-P1--P4-Kern. Er behauptet keine Produktionsreife, keine
CRS-Verifikation, keine vollständige HTTP/2-/HTTP/3-Abdeckung, keine
vollständige Matrix und keine Strict-Verifikation für jede Phase.

## Architektur und Ownership

Produktiver Quellcode liegt unter <code>connectors/apache/src/</code>;
Autotools-/APXS-Inputs und hostspezifischer Build-Kleber bleiben unter
<code>connectors/apache/</code>. Apache besitzt Konfigurationshooks und Merge,
Request-Hooks, Input-/Output-Filter, Log-Transaction-Behandlung,
Bucket-Brigades, APR-Lebensdauern und Host-Intervention-Mapping. Common liefert
connector-neutrale Konfigurations-, Parser-, Mapper- und Regelmetadaten sowie
payload-sichere Event-Primitiven; es besitzt keine Apache-Objekte.

| Lifecycle-Bereich | Ausgewählte Apache-Verantwortung | Grenze |
| --- | --- | --- |
| P1/P2 | Request-Metadaten mappen und Request-Bodies über den Inputpfad verarbeiten | Request-Body-Verarbeitung bei EOS abschließen |
| P3 | Response-Header vor der Commit-Grenze mappen | Ursprungs- und sichtbaren Statuskontext erhalten |
| P4 | Aktuelle Output-Buckets inkrementell aufnehmen und bei EOS abschließen | Kein connector-eigener vollständiger Response-Puffer über Aufrufe hinweg |
| Logging | Nur Metadaten enthaltende Events ausgeben und Transaktionszustand freigeben | Event-Payloads enthalten keine Response-Bodies |

## Build

Der [Apache-Compiler-Guide](../build/compilers/apache.de.md) beschreibt APXS,
libmodsecurity-Discovery, Build-Roots, Toolchain-Voraussetzungen und
Fehlerbehebung. Build- und Config-Load-Erfolg unterscheiden sich von
Verkehrsausführung. Code-lokale Source-Ownership und enge Harness-Hinweise
bleiben im [Apache-Source-Guide](../../connectors/apache/README.de.md).

## Konfiguration

Apache-Hostdirektiven werden vom Modul registriert und unterscheiden sich von
ModSecurity-Engine-Direktiven. Vollständige quellenbasierte Syntax, Defaults,
Kontexte, Merge-Regeln, Beispiele und Validierungshinweise stehen in der
[Apache-Konfigurationsreferenz](../../examples/apache/configuration-reference.de.md).

Minimal-, Safe-, Strict-, DetectionOnly- und Disabled-Profile werden nur für
ihren dokumentierten Zweck verwendet. <code>SecRuleEngine</code> ist eine
Engine-Einstellung und nicht identisch mit einer Apache-Connector-
Enable/Disable-Direktive.

## P1--P4-Lifecycle und spätes Verhalten

Das native Modul verarbeitet P1 bis P4 in seinen Host-Hooks und Filtern. P3
kann handeln, bevor die Response committed ist, wenn ausgewählter Case und
Hostzustand es erlauben. P4 ist anders: Safe-Verhalten nach Commit wird
konservativ als Metadatum aufgezeichnet und muss das tatsächlich sichtbare
Ergebnis erhalten. Strict-Source-Wiring beweist keinen client-sichtbaren
Abbruch.

| P4-Frage | Erforderliche Beobachtung |
| --- | --- |
| Regel beobachtet | Reale Host-Phase-4-Regelbeobachtung mit ausgewählter Regel/Profil |
| Deny vor Commit | Angeforderter Deny, nicht committe Header und passender sichtbarer Status |
| Safe Late Result | Angeforderte Aktion, tatsächliches <code>log_only</code>, unveränderter sichtbarer Status und Late-Flag |
| Strict Late Result | Tatsächliche Abort-Aktion und Host-/Client-Nachweis des aufgezeichneten Abbruchs |

## Tests und Nachweise

<code>make check-config-apache</code> prüft die ausgewählte Konfiguration,
<code>make full-lifecycle-apache</code> führt einen ausgewählten Lifecycle-Lauf
aus. Laufbezogene Result-, Assertion-, Hostlog- und nur Metadaten enthaltende
Phase-Event-Artefakte sind zu prüfen, statt Laufzeitverhalten aus Quelle oder
Build abzuleiten.

Testmodell, Statusvokabular, Datenschutzregeln und Aggregatgrenzen stehen unter
[Tests und Nachweise](../testing-and-evidence.de.md).

## Betrieb und Fehlerbehebung

Apache läuft mit einem expliziten externen Build-/Runtime-/Evidence-Root;
Hostlogs und Regelinputs werden geschützt. Bei einem Konfigurationsfehler werden
zuerst APXS-/libmodsecurity-Discovery und die ausgewählte Config-Check-Ausgabe
geprüft. Bei einer P4-Frage sind Phase-Event und Commit-/EOS-Kontext vor der
Deutung eines HTTP-Status zu prüfen.

## Grenzen und Kompatibilität

Apache-v2-artige Namen sind nicht automatisch native Apache-v3-Connector-
Direktiven. Verwenden Sie die registrierte Modulsyntax und die vollständige
Referenz, statt eine Legacy-Direktive, Merge-Regel oder Ausdruckssyntax als
portabel anzunehmen. P4-Response-Body- und Post-Commit-Verhalten bleiben
evidence-gesteuert; ein Regelmatch, Quellzweig oder historische Matrix ist
keine Promotion.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [Apache-Konfigurationsreferenz](../../examples/apache/configuration-reference.de.md)
