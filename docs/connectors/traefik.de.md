# Traefik-Connector

**Sprache:** [English](traefik.md) | Deutsch

## Go-Composite-Common-Runtime und beobachteter Lifecycle

Das separat gebaute `msconnector-composite --mode traefik` wählt die
kanonische Identität `traefik / forwardAuth / traefik-forwardauth` mit
gepufferten Requests und gestreamten Responses. Es verwendet den additiven
gepufferten Header-Start, explizites Request-Append/EOS und eine private
Common-Response-Companion-Session für P3/P4. Direktes Envoy ext_proc bleibt
in beiden Richtungen gestreamt.

Go-Lease, Kontext und Deadline werden vor dem nativen Claim geprüft. Nativer
Ablauf konsumiert die Ownership; konsumierte Cleanup-Fehler werden nicht
wiederholt. Unaufgelöstes Cleanup versetzt den Coordinator dauerhaft in einen
Fehlerzustand und sperrt die Aufnahme für kontrollierten Neustart. Terminales
Cleanup ist einmalig geschützt und behält die Entry-Ownership bis zum
Abschluss. Ein echter Common-Body-Limit-Fehler wird mit tatsächlichen
Host-Aktionsmetadaten auf 413 abgebildet; terminales Cleanup eines
unvollständigen Bodys erfindet weder EOS noch P2-Regelauswertung.

Am 2026-10-03 prüfte der externe Lauf `p370t.T4wJJ8kA` den echten
Traefik-Host, lokale Composite-Middleware und den Go-Common/libmodsecurity-Dienst.
Zehn Fälle lieferten `LIFECYCLE_ONLY`: P1 allow/deny, P2 allow/deny/oversize,
P3 deny/redirect, P4 Safe, fehlende Metadaten und P2-to-P3-Timeout. P4 Strict
lieferte das erwartete `NON_PASS`, weil kein unabhängiger Host-Reset/Abort
nachgewiesen wurde. Alle Fälle behalten `catalog_acceptance=false`.

Das finale Source-Manifest war unverändert, Cleanup meldete keine Probleme und
temporäre Testschlüssel wurden entfernt. Executable-/Bibliothekshashes,
Beobachtungen geladener Bibliotheken, Ressourcenmessungen und
Upstream-Beobachtungen bleiben in der externen Evidence. Diese Evidence gilt
für die Go-Composite-Route und stuft weder die Legacy-C-Dienststatus
`implemented_not_asserted` oder `configured_not_exercised` noch das separate
native UDS-Profil hoch.

Vollständige G1–G9-Abnahme aller neun Nicht-NGINX-Profile bleibt offen;
Produktionsreife wird nicht behauptet. Siehe
[Change Record](../../reports/audits/change-records/CR-20261003-pr370-composite-common-runtime.de.md)
für Umfang, Befehle und verbleibende Lücken.

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

## forwardAuth als logischer Response-Companion

Das <code>forwardAuth</code>-Request-Protokoll kann P3/P4 nicht selbst
transportieren. Sein Authorization-Service übergibt dieselbe lebende
Common-/native Transaktion nach abgeschlossenem P1/P2 an einen festen,
TTL-begrenzten Response-Companion mit 64 Einträgen. Er gibt genau einen
serverseitig erzeugten opaken 256-Bit-Response-Handle aus, niemals eine
Transaktions-ID, Connector-ID oder Host-ID. Der private MRC1-Listener
akzeptiert diesen Handle genau einmal; damit bleibt jeder zurückgehaltene
native State in der Common Runtime.

Das mitgelieferte Response-Observer-Plugin sowie die Artefakte
<code>traefik-response-observer-{static,dynamic}.yaml</code> machen forwardAuth
und seinen Response-Observer zu einer logischen Connectorlösung. Die dynamische
Kette lautet <code>forwardAuth -&gt; response observer -&gt; upstream</code> und
erlaubt aus der Authorization-Antwort ausschließlich
<code>X-Msconnector-Response-Handle</code>. Der Observer claimed und entfernt
diesen Header vor dem Upstream-Handler. Er sendet P3 vor dem Writer-Commit,
P4-Chunks/EOS danach, zeichnet die tatsächliche Hostaktion auf und gibt
deterministisch frei oder cancelt. Er verwendet ausschließlich private UDS;
der Standard-Companion-Pfad liegt unter <code>/run/modsecurity</code>, dessen
kanonisches owner-only Parent mit <code>0700</code> der Operator bereitstellen
muss. Es gibt keinen TCP-Fallback.

Fehlende, fehlerhafte, abgelaufene, doppelte, wiederverwendete oder nicht
erreichbare Handles werden vor dem Upstream-Response-Commit fail-closed
behandelt. Ein fehlerhaftes MRC1-Ergebnis, ein Deadline-Ablauf oder ein
Cleanup-Fehler folgt demselben Fehler-/Cancel-Pfad; TTL-Ablauf zeichnet Timeout
auf und zerstört zurückgehaltenen State. Disruptive Engine-Ergebnisse nach dem
Commit werden als Log-only aufgezeichnet, weil Traefik die Response nicht
rückwirkend umschreiben kann. Das lokale Plugin bietet weder
<code>Unwrap</code> noch <code>Hijacker</code> und umgeht diese Grenze damit
nicht.

Die obige Legacy-C-Route und ihre Component-Tests sind Source-Level-Evidence. Eine
eingesetzte Traefik-Instanz benötigt weiterhin Plugin-Load-, Konfigurations-
und Traffic-Evidence, bevor sie als Host-Runtime-Evidence beschrieben wird.

Der [gemeinsame Transaktions- und Phasenvertrag](../../common/docs/transaction-phase-contract.de.md)
definiert Zustandsmaschine und einheitliche Entscheidungsrichtlinie.

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
