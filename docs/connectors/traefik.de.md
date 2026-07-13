# Traefik-Connector

**Sprache:** [English](traefik.md) | Deutsch

## Überblick

Traefik verwendet den ausgewählten <code>native-traefik-middleware</code>-Pfad:
einen Local-Plugin-/Middleware-Pfad mit einem privaten UDS-
Common/libmodsecurity-Engine-Service. Der beibehaltene forwardAuth-Service ist
ein getrennter Kompatibilitätspfad. Dieser Guide beschreibt die ausgewählte
HTTP/1.1-P1--P4-Safe-Grenze und behauptet keine Produktionsreife, keine
CRS-Vollständigkeit, keine vollständige Protokollabdeckung, keinen Strict-Late-
Abort, kein First-Byte-Verhalten, kein No-Full-Response-Buffering und keine
vollständige Matrix.

## Architektur und Ownership

Die native Middleware besitzt Traefik-artige Request-/Response-Behandlung,
ResponseWriter-Verhalten, Plugin-Lifecycle und UDS-Client-Interaktion. Der
lokale Engine-Service besitzt begrenztes Protokoll-Framing pro Transaktion und
explizites Finish-/Destroy-Handling. Common besitzt neutrale Runtime-
Konfiguration, Engine-Aufrufe, Limits, Entscheidungen und payload-sichere
Events; es besitzt weder Traefik-Objekte noch Commit-Semantik.

| Lifecycle-Bereich | Ausgewählte native Verantwortung | Grenze |
| --- | --- | --- |
| P1/P2 | Ausgewählten Requestpfad auf eine private Engine-Session mappen | Body-Modus und Hostverhalten bleiben profilspezifisch |
| P3 | Response-Header vor/an der Host-Writer-Grenze verarbeiten | Tatsächlicher Writer-Commit bestimmt Interventionsmöglichkeiten |
| P4 | Begrenzte Response-Ranges mit konservativem Post-Commit-Ergebnis verarbeiten | Ausgewähltes Safe-Ergebnis ist <code>log_only</code> |
| Service-Cleanup | Genau eine Transaktion pro ausgewähltem Request finish/destroy | Fokussierte Sourcetests sind kein Hostverkehrsclaim |

## Build

Der [Traefik-Compiler-Guide](../build/compilers/traefik.de.md) beschreibt
ausgewählte Build-/Service-/Runtime-Komponentenverfahren. Der code-nahe
[Traefik-Source-Guide](../../connectors/traefik/README.de.md) und
<code>connectors/traefik/native_middleware/</code> dokumentieren das lokale
Source-Layout. Unit-/Build-/Self-Test-Stufen bleiben von einem echten Hostlauf
getrennt.

## Konfiguration

Die vollständige statische/dynamische/native-Plugin-/Common-Runtime-
Konfigurationsoberfläche, Defaults, Platzhalter und forwardAuth-
Kompatibilitätsfelder stehen in der
[Traefik-Konfigurationsreferenz](../../examples/traefik/configuration-reference.de.md).
Der ausgewählte native UDS-Pfad und forwardAuth haben verschiedene Response-
Sichtbarkeit; ein forwardAuth-Request-Ergebnis darf nicht als nativer P3-/P4-
Nachweis befördert werden.

## P1--P4-Lifecycle und lokaler Engine-Service

Der ausgewählte native Hostcheck staged die Middleware in einem isolierten
Local-Plugin-Workspace, startet den privaten Engine-Service und zeichnet
ausgewählte P1-/P2-/P3- und Safe-P4-Metadaten auf. Das Service-Protokoll ist
begrenzt und pro Transaktion; sein lokaler Self-Test begründet kein globales
Hostverhalten.

| Frage | Erforderlicher Nachweis |
| --- | --- |
| Nativer Hostpfad | Plugin-Load-Bestätigung, ausgewählter Verkehr und passende Integrationsmetadaten |
| P3 | Response-Header-Timing-/Commit-Metadaten und tatsächliches sichtbares Ergebnis |
| Safe P4 | Ursprüngliche sichtbare Response, <code>log_only</code> und Post-Commit-Metadaten |
| Strict P4 | Ein getrennt bewiesener Host-/Client-Abort, kein konfigurierter Service-Modus |

## Tests und Nachweise

Führen Sie nur die für die Frage benötigte Target-Ebene aus: Konfiguration,
Request-freier Start, lokales Service-Protokoll, native Middleware-Sourcetests
oder ausgewählter Hostverkehr. Fehlende optionale Traefik-Binaries bleiben
Blocked-Prerequisites. Ein realer Hostclaim braucht die Result-/Event-/
Effective-Configuration-Artefakte des ausgewählten Laufs gemäß
[Tests und Nachweise](../testing-and-evidence.de.md).

## Betrieb und Fehlerbehebung

Service-Socket, Runtime-Roots, Component-Cache und Evidence-Roots bleiben
außerhalb des Checkouts und privat für den beabsichtigten lokalen Lauf.
Plugin-Load, UDS-Service-Start, Request-Mapping und Writer-Commit werden
getrennt diagnostiziert. Engine-Service-Control-Endpunkte oder
secret-haltige Konfiguration gehören nicht in eingecheckte Beispiele oder Logs.

## Grenzen und Kompatibilität

forwardAuth ist nur Kompatibilität und hat seine eigene request-orientierte
Grenze. Die ausgewählte native Middleware bleibt für P4 Safe evidence-
scoped; Strict Abort/Cancellation, First Byte vor EOS, vollständige
Response-Buffer-Eigenschaften, HTTP/2/HTTP/3 und CRS-Claims brauchen
dedizierte ausgewählte Artefakte.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [Traefik-Konfigurationsreferenz](../../examples/traefik/configuration-reference.de.md)
