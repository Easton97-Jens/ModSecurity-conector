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
| P4 | Jeden begrenzten Daten-Bucket genau einmal anhängen und das normalisierte Präfix vor EOS sofort an den nächsten Filter weiterreichen | Nur das terminale EOS-Fragment wartet auf ein Phase-4-Finish; Next-Filter-Forwarding ist die Source-Commit-Grenze |
| Logging | Nur Metadaten enthaltende Events ausgeben und Transaktionszustand freigeben | Event-Payloads enthalten keine Response-Bodies |

Jede erfolgreich erzeugte native <code>Transaction</code> gehört der primären
Apache-Anfrage, die sie erzeugt hat. Der Adapter veröffentlicht sie erst nach
erfolgreicher Erzeugung, registriert ein normales Cleanup am
<code>r-&gt;pool</code> dieser Anfrage und löscht die Owner-Notiz sowie den
nativen Pointer, bevor <code>msc_transaction_cleanup</code> ausgeführt wird.
Dies ist ein Lifecycle-Vertrag auf Quellcodeebene und kein Runtime-Nachweis.
Getrennte Top-Level-Anfragen auf einer Keepalive-Verbindung erhalten getrennte
Request-Pools und Transaktionen. Subrequests behalten ihre bestehende
absichtliche Wiederverwendung des primären Kontexts. Normale interne Redirects
und ErrorDocuments vor Output schlagen fail-closed fehl: Die Transaktion kann von Quell-URI,
Headern und Body nicht über die öffentliche libModSecurity-C-API sicher an eine
Target-Anfrage gebunden werden. Die einzige Ausnahme ist genau ein synchroner,
von Apache Core markierter lokaler ErrorDocument-Hop, während der Terminal-
Output-Guard <code>EMITTING</code> ist, mit Apache-Marker
<code>no_local_copy</code> und passendem unmittelbaren
Vorgängerstatus/<code>REDIRECT_STATUS</code>; der Guard weist einen zweiten Hop
ab.

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
Hostzustand es erlauben. P4 bleibt für die Regelauswertung EOS-only, ist nun
aber ein progressiver Ausgabepfad: Jeder Response-Daten-Bucket wird genau
einmal angehängt, FLUSH und andere Apache-Metadaten vor EOS bleiben erhalten,
und das normalisierte Präfix vor EOS wird sofort an den nächsten Filter
weitergereicht. Der Filter hält keine vollständige Response-Brigade; nur das
terminale EOS-Fragment wartet auf den einmaligen Aufruf von
`msc_process_response_body` und die Late-Action-Auflösung.

Die C-API gibt keine sichere Antwort auf die wirksame
`SecResponseBodyMimeType`-Auswahl von libModSecurity. Apache gate't deshalb
jeden Response-MIME-Typ; die Engine-Direktive wählt weiterhin die Inspektion,
aber das veraltete `modsecurity_phase4_content_types_file` kann keinen
Pass-through-Pfad öffnen. Das Connector-Standardlimit ist ein hartes Limit von
1048576 Byte (1 MiB); die Grenze wird geprüft, bevor ein weiterer Daten-Bucket
angehängt wird. Ein Fehler nach einem weitergereichten Präfix kann dieses nicht
umschreiben; die terminale Aktion wird darum über die gemeinsame
Post-Commit-Policy abgebildet. `r->sent_bodyct` und `eos_sent` sind kein
Commit-Nachweis, weil Upstream-/Core-Pfade sie setzen können, bevor dieser
Filter Ausgabe freigibt. Der Next-Filter-Aufruf ist die monotone
Commit-Grenze des Source-Contracts; zusätzlich behält der Filter seinen
EOS-Release-Guard und Apaches `r->bytes_sent`-Metadaten.

P4-Regelauswertung erfolgt nicht pro Chunk, sondern nur bei EOS. Ein
progressiver P4-Pfad behauptet darum keinen verlässlichen Deny oder Redirect
vor Commit, nachdem ein Response-Präfix weitergereicht wurde; P3 bleibt der
Entscheidungspunkt vor dem Response-Header-Commit. Safe/Minimal ordnet ein
disruptives EOS-Ergebnis als `log_only` zu und erhält die bereits
weitergereichte Response. Strict verwendet `abort_connection`. Source-Wiring
für diesen Abort beweist weiterhin keinen client-sichtbaren Abbruch.

| P4-Frage | Erforderliche Beobachtung |
| --- | --- |
| Regel beobachtet | Reale Host-Phase-4-Regelbeobachtung mit ausgewählter Regel/Profil |
| Progressives Präfix | Ein client-sichtbares erstes Byte vor Response-EOS, erhaltenes FLUSH/Metadaten und genau ein Append pro Daten-Bucket |
| P4-Deny vor Commit | Ein host-spezifischer Commit-Nachweis; dieser progressive Apache-Source-Path behauptet keinen nach einem weitergereichten Präfix |
| Safe Late Result | Angeforderte Aktion, tatsächliches <code>log_only</code>, unveränderter sichtbarer Status und Late-Flag |
| Strict Late Result | Tatsächliche Abort-Aktion und Host-/Client-Nachweis des aufgezeichneten Abbruchs |

## Tests und Nachweise

<code>make check-config-apache</code> prüft die ausgewählte Konfiguration,
<code>make full-lifecycle-apache</code> führt einen ausgewählten Lifecycle-Lauf
aus. Laufbezogene Result-, Assertion-, Hostlog- und nur Metadaten enthaltende
Phase-Event-Artefakte sind zu prüfen, statt Laufzeitverhalten aus Quelle oder
Build abzuleiten. Der fokussierte H1/H2-Evidence-Platzhalter ist
<code>ci/runtime/lifecycle/run-apache-phase4-response-regression.sh</code>;
erst nach der Ausführung wird dessen laufbezogene Ausgabe erfasst. Dieser Guide
behauptet keinen H1- oder H2-Pass, nur weil Source-Contract oder Runner
vorhanden sind.

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
keine Promotion. Der progressive Apache-Pfad ist eine begrenzte
Adapterübersetzung, kein generisches Connector-Buffering-Modell und keine
Behauptung eines client-sichtbaren späten Abbruchs.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [Apache-Konfigurationsreferenz](../../examples/apache/configuration-reference.de.md)
