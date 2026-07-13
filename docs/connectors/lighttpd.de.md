# lighttpd-Connector

**Sprache:** [English](lighttpd.md) | Deutsch

## Überblick

lighttpd verwendet den ausgewählten <code>patched-native-lighttpd</code>-Pfad
mit <code>mod_msconnector.so</code>. Das ausgewählte Profil ist
HTTP/1.1-fokussiert und verwendet eine versionierte Patched-Host-Grenze für
geliehene Body-Ranges. Es behauptet keine Produktionsreife, keine
Sicherheitsverifikation, keine CRS-Verifikation, keine vollständige Matrix,
keine HTTP/2-/HTTP/3-Abdeckung und keine kanonische P4-Runtime-Evidence.

## Architektur und Ownership

Die Plugin-Lifecycle-Schicht ist host-eigen, und der Mapper ist die einzige
lighttpd-API-Übersetzungsschicht. Common Runtime und Common-SDK-Typen bleiben
frei von lighttpd-Callback-Typen. Eine Runtime wird aus server-scoped
Konfiguration initialisiert; jeder Request erhält bis zum Request-Reset seine
eigene Transaktion und Mapper-Storage.

| Lifecycle-Bereich | Ausgewählte lighttpd-Verantwortung | Grenze |
| --- | --- | --- |
| P1 | URI-/Request-Header mappen und eine zulässige Request-Entscheidung anwenden | Der enge Smoke ist keine breite Hostgarantie |
| P2 | Gepatchte geliehene Request-Body-Range nur im ausgewählten Modus verwenden | Buffered-Request-Modus liegt außerhalb des ausgewählten Pfads |
| P3 | Response-Metadaten bei Response-Start mappen | Response-Status-/Action-Semantik bleibt hostspezifisch |
| P4 | Identity-Entity-Ranges vor HTTP/1-Transfer-Framing empfangen und einmal bei EOS abschließen | Kein Socket-Queue-Callback und keine connector-eigene Body-Queue |
| Cleanup | Mapper-Storage und Transaktion bei Request-Reset freigeben | Statische Lifetime-Checks sind kein Nachweis für Langzeitresilienz |

## Build

Der [lighttpd-Compiler-Guide](../build/compilers/lighttpd.de.md) beschreibt
natives Modul, gepatchten Host, ABI-Prüfungen, Source-Inputs und
Konfigurationsladen. Der [lighttpd-Source-Guide](../../connectors/lighttpd/README.de.md)
bleibt der code-nahe Einstieg. Build-/Load-/Start-Stufen sind von Request-
Verkehr und Evidence-Promotion getrennt.

## Konfiguration

Vollständige Server-/Plugin-/Common-Runtime-Syntax, Defaults, Scopes,
Kompatibilitätsfelder, Profile und Validierungsdetails stehen in der
[lighttpd-Konfigurationsreferenz](../../examples/lighttpd/configuration-reference.de.md).
Das ausgewählte native Profil ist vom beibehaltenen Sidecar-Proxy-
Kompatibilitätsbeispiel getrennt.

## P1--P4-Lifecycle und Entity-Body-Grenze

Der gepatchte Host ruft den ausgewählten Response-Callback auf synchronen
geliehenen Identity-Entity-Ranges vor dem Transfer-Framing auf. Er erhöht einen
monotonen Entity-Offset und signalisiert EOS einmal. Spätere Socket-Kurzschreib-
oder Retry-Behandlung darf keine bereits aufgenommene Entity-Range duplizieren;
dies ist ein Source-/Static-Vertrag, kein Fault-Injection-Runtime-Claim.

| P4-Frage | Aktuelle Grenze |
| --- | --- |
| Response-Body-Hook | Gepatchter Identity-Entity-Body-Source-Pfad existiert |
| Safe-/Minimal-Ergebnis | Sichtbare Response erhalten und konservatives <code>log_only</code>-Verhalten aufzeichnen |
| Strict-Ergebnis | Ausdrücklich nicht ausgeführt ohne client-validierte Host-Abort-Primitive |
| Streaming/Limits | Braucht ein reales ausgewähltes Host-/Client-Artefakt zur Promotion |

gzip/br, HTTP/2, nicht untersuchte File-/Zero-Copy-Ausgabe, Short-Write-
Fault-Injection und nicht ausgewählte Buffering-Modi liegen außerhalb des
ausgewählten Vertrags.

## Tests und Nachweise

<code>make check-lighttpd-config</code> prüft reales Modul-/Konfigurationsladen;
das ausgewählte Lifecycle-Target führt eine laufbezogene Hostübung aus. Der
enge native Smoke kann nur seine angegebene Request-Pfad-Beobachtung belegen.
P4- und Late-Intervention-Facets bleiben nicht ausgeführt oder
capability-selected, bis reale Host-/Client-Artefakte Timing und sichtbares
Ergebnis belegen. Siehe [Tests und Nachweise](../testing-and-evidence.de.md).

## Betrieb und Fehlerbehebung

Matching gepatchter Core und Modul werden gemeinsam in einem externen Build-Root
gestaged. Bei Loader-/Config-Fehlern sind ABI-Marker, Modulverzeichnis,
Common-Runtime-Konfiguration, Rule-Load und die reale
<code>lighttpd -tt</code>-Ausgabe zu prüfen. Modul-, Runtime-, Log- und
Evidence-Pfade bleiben außerhalb des Checkouts.

## Grenzen und Kompatibilität

Der Legacy-Sidecar-Proxy ist nur Kompatibilität und wird nicht zu nativem
lighttpd-Verhalten. Das ausgewählte Evidence-Profil belegt ohne dedizierte
Artefakte weder P4-Regelauswertung noch sichtbare Late-Action, Abort,
Response-Trunkierung, vollständiges CRS-Verhalten oder Produktionshärtung.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [lighttpd-Konfigurationsreferenz](../../examples/lighttpd/configuration-reference.de.md)
