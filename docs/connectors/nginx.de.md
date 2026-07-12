# NGINX-Connector

**Sprache:** [English](nginx.md) | Deutsch

## Überblick

NGINX verwendet den ausgewählten Pfad <code>native-nginx-http-module</code>.
Das dynamische HTTP-Modul mappt NGINX-Request-/Response-Zustand über
connector-eigene Phasen und Filter auf libmodsecurity v3. Dieser Guide deckt
nur den ausgewählten HTTP/1.1-P1--P4-Kern ab und behauptet weder Produktion,
CRS, vollständige Matrix, HTTP/2, HTTP/3 noch Strict für alle Connectoren.

## Architektur und Ownership

Produktiver Quellcode liegt unter <code>connectors/nginx/src/</code>;
Modul-Build-Metadaten liegen unter <code>connectors/nginx/config</code>. NGINX
besitzt Main-/Location-Konfiguration create/merge, Access- und Log-Phasen,
Header-/Body-Filter, Subrequest-/End-of-Stream-Behandlung, dynamisches
Modulladen und Hostaktions-Mapping. Common liefert neutrale Konfigurations-,
Parser-, Mapping-, Limit-, Event- und Metadatenverträge, ohne
<code>ngx_http_request_t</code> oder einen NGINX-Filter zu besitzen.

| Lifecycle-Bereich | Ausgewählte NGINX-Verantwortung | Grenze |
| --- | --- | --- |
| P1/P2 | Access-Phase-Request-Mapping und Body-Abschluss | Einen Body nicht vor seinem ausgewählten End-of-Stream abschließen |
| P3 | Response-Header-Filter-Mapping | Pre-Commit-Zustand aus der Hostresponse bestimmen |
| P4 | Begrenzte Body-Filter-Aufnahme und einmaliger EOS-Abschluss | Tatsächliche Aktion und sichtbaren Status nach Commit erhalten |
| Logging | Payload-freie Event-/Result-Metadaten | JSON-/Event-Trunkierung ist von Body-Trunkierung getrennt |

## Build

Der [NGINX-Compiler-Guide](../build/compilers/nginx.de.md) beschreibt
Source-Build, Dynamic-Module-Inputs, Komponentenroots und Diagnose. Erforderliche
C17-Prüfungen sind Struktur-/Compile-Nachweise; optionale neuere
Sprachprüfungen bedeuten keine Laufzeitverifikation. Der
[NGINX-Source-Guide](../../connectors/nginx/README.de.md) bleibt der
code-nahe Einstieg.

## Konfiguration

Vollständige NGINX-Syntax, Werte, Defaults, Kontexte, Merge-Verhalten,
Validierungshinweise und Profilbeispiele stehen in der
[NGINX-Konfigurationsreferenz](../../examples/nginx/configuration-reference.de.md).
NGINX-Variablen werden nur verwendet, wo die registrierte Direktive sie
dokumentiert. <code>modsecurity_transaction_id_expr</code> ist
Apache-spezifisch und keine NGINX-Direktive.

## P1--P4-Lifecycle und Protokollgrenze

P3-Entscheidungen gehören in den Response-Header-Pfad vor dem Header-Commit.
Der Response-Body-Filter ist ein separates P4-Timing-Modell. Ein P4-Regelmatch
belegt ohne passende Host-/Client-Artefakte weder sichtbares 403 noch Abort oder
HTTP/2-Ergebnis.

| P4-Frage | Erforderliche Beobachtung |
| --- | --- |
| Regel beobachtet | Ausgewählte native Regel und Phase-4-Metadaten |
| Deny vor Commit | Ein Hostpfad, der für die ausgewählte Response tatsächlich vor Commit liegt |
| Safe Late Result | Angeforderte Aktion, tatsächliches <code>log_only</code>, unveränderter sichtbarer Status und Late-Flag |
| Strict Late Result | Tatsächliche Abort-Aktion, erhaltener bereits sichtbarer Status und Client-/Hostnachweis |

Ein HTTP/2-Build-Flag ist kein Transportnachweis. Wenn ein Hostlauf ein
HTTP/2-Applicability-Artefakt schreibt, bleibt ein nicht verfügbares Feature
nicht anwendbar und ein nicht ausgeführter Protocol-Case nicht ausgeführt.

## Tests und Nachweise

<code>make check-config-nginx</code> validiert die Konfiguration,
<code>make full-lifecycle-nginx</code> führt einen ausgewählten nativen
Hostlauf aus. Result, Event, effektive Konfiguration, Hostversion und
Protocol-Applicability-Artefakte der ausgewählten Run-ID sind zu prüfen. Das
gemeinsame Modell steht unter [Tests und Nachweise](../testing-and-evidence.de.md).

## Betrieb und Fehlerbehebung

Verwenden Sie einen externen Build-/Runtime-/Evidence-Root. Bei Modul- oder
Konfigurationsfehlern sind Source-Build-Inputs, Dynamic-Module-Kompatibilität
und Config-Check-Ausgabe zu prüfen. Bei P4- oder Protocol-Fragen ist der
aufgezeichnete Commit-/EOS-Kontext des Response-Filters zu prüfen, statt aus
einer Source-Option oder einem HTTP-Status allein zu extrapolieren.

## Grenzen und Kompatibilität

NGINX-Syntax, Kontexte, Vererbung und Ausdruckssemantik sind hostspezifisch.
Apache-Ausdrucksdirektiven dürfen nicht nach NGINX kopiert werden. Response-
Body, Strict Late Action, First Byte, No-Full-Buffer und Protocol-Eigenschaften
bleiben einzeln evidence-gesteuert.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [NGINX-Konfigurationsreferenz](../../examples/nginx/configuration-reference.de.md)
