# Envoy-Connector

**Sprache:** [English](envoy.md) | Deutsch

## Überblick

Envoy verwendet den ausgewählten gestreamten <code>ext_proc</code>-Pfad mit
einem lokalen Common/libmodsecurity-Service. Er unterscheidet sich vom
beibehaltenen <code>ext_authz</code>-Kompatibilitätsbeispiel. Dieser Guide
beschreibt die ausgewählte HTTP/1.1-P1--P4-Safe-Architektur und behauptet keine
Produktionsreife, keine CRS-Verifikation, keine vollständige Matrix-/
Protokollabdeckung, keine Strict-Post-Commit-Aktion und kein universelles
Envoy-Deployment.

## Architektur und Ownership

Envoy besitzt Filterkettenkonfiguration, Transport, Stream-Callbacks und
Host-Response-Verhalten. Der ext_proc-Service besitzt sein begrenztes
Protokoll-/Session-Mapping und ruft die Common/libmodsecurity-Runtime auf.
Common bleibt frei von Envoy-SDK-Typen und besitzt nur neutrale Konfiguration,
Mappingverträge, Limits, Decision-/Eventdaten und Engine-nahe Helfer.

| Lifecycle-Bereich | Ausgewählte ext_proc-Verantwortung | Grenze |
| --- | --- | --- |
| P1/P2 | Gestreamte Request-Header-/Body-Nachrichten auf die ausgewählte Service-Session mappen | Request-Fluss ist Protokoll-/Konfigurationsabhängig |
| P3 | Response-Header über den ext_proc-Service mappen | Host-sichtbares Verhalten hängt vom Commit-Zustand ab |
| P4 | Ausgewählte Response-Body-Stream-Nachrichten verarbeiten und bei EOS abschließen | Safe-Post-Commit-Verhalten bleibt konservativ |
| Events | Payload-freie Service-/Runtime-Metadaten schreiben | Ein Service-Record ist keine Client-Transportbehauptung |

## Build

Der [Envoy-Compiler-Guide](../build/compilers/envoy.de.md) beschreibt
Service-Build, Runtime-Komponentenauswahl, explizite Vorbereitung und Diagnose.
Der code-nahe [Envoy-Source-Guide](../../connectors/envoy/README.de.md) und
<code>connectors/envoy/ext_proc/</code> beschreiben das Source-Layout. Ein
Service-Build oder Request-freier Startsmoke ist kein Full-Lifecycle-Nachweis.

## Konfiguration

Die vollständige Envoy-YAML-/Service-/CLI-Konfigurationsoberfläche, Platzhalter,
Defaults und Kompatibilitätseinträge stehen in der
[Envoy-Konfigurationsreferenz](../../examples/envoy/configuration-reference.de.md).
Das ausgewählte <code>ext_proc</code>-Profil und das
<code>compatibility-ext-authz</code>-Beispiel haben getrennte Semantik.
ext_authz-Response-Sichtbarkeit darf nicht als ext_proc-P4-Unterstützung
dargestellt werden.


## ext_authz als logischer Response-Companion

Das <code>ext_authz</code>-Request-Protokoll transportiert keinen Response-
Stream. Für den gemeinsamen Vertrag übergibt es deshalb die lebende
Common-/native Transaktion nach abgeschlossenem P1/P2 an einen festen,
TTL-begrenzten Response-Companion mit 64 Einträgen. Der Authorization-Service
erzeugt dafür mit der Kernel-Zufallsschnittstelle einen opaken 256-Bit-
Response-Handle; er legt niemals Transaktions-ID, Connector-ID oder Host-ID
für die Korrelation offen. Der Handle wird genau einmal über die private MRC1-
UDS akzeptiert, danach bleibt die lebende Transaktion intern in der Common
Runtime.

Die mitgelieferte <code>envoy-ext-authz-smoke.yaml.in</code> verdrahtet dies als
eine logische Connectorlösung: <code>ext_authz</code> darf ausschließlich
<code>x-msconnector-response-handle</code> auf Envoys internen Upstream-Header-
Pfad zum unmittelbar folgenden privaten UDS-<code>ext_proc</code>-Response-
Observer kopieren. Dieser Observer beansprucht und entfernt den Header sofort vor
dem tatsächlichen Anwendungs-Upstream. Er erhält keinen Request-Body. Er sendet P3
vor dem Response-Commit, P4-Chunks/EOS danach, zeichnet die tatsächliche
Hostaktion auf und gibt den Handle deterministisch frei oder cancelt ihn. Seine
Standard-UDS und die C-Companion-UDS liegen unter <code>/run/modsecurity</code>;
Operatoren müssen dieses Parent als kanonisches, owner-only Verzeichnis mit
<code>0700</code> bereitstellen. Für keine der privaten Bindungen gibt es einen
TCP-Fallback.

Ein fehlender, fehlerhafter, abgelaufener, doppelter oder bereits geclaimter
Handle ist ein Protokollfehler. Ein nicht erreichbarer Observer, ein
fehlerhaftes MRC1-Ergebnis, ein Deadline-Ablauf oder ein Cleanup-Fehler ist
fail-closed: Der konfigurierte <code>ext_proc</code>-Filter hat
<code>failure_mode_allow: false</code> und verhindert Routing, statt still
P3/P4-Abdeckung zu behaupten. TTL-Ablauf zeichnet Timeout auf und zerstört die
zurückgehaltene Transaktion; Cancel und Observer-Shutdown verwenden denselben
kanonischen Cleanup-Pfad. Das lokale Harness startet den erforderlichen
Observer mit isolierten owner-only Sockets und übergibt den Companion-Socket
explizit an den Authorization-Service.

Dies ist nur Source- und Component-Evidence. Eine eingesetzte Envoy-Instanz
benötigt weiterhin einen Konfigurationsvalidierungs- und Traffic-Run, bevor
sie als Host-Runtime-Evidence beschrieben wird.

Der [gemeinsame Transaktions- und Phasenvertrag](../../common/docs/transaction-phase-contract.de.md)
definiert dazu die exakte Zustandsmaschine und Entscheidungsrichtlinie.

## P1--P4-Lifecycle und Transport-Hardening

Der ausgewählte Service muss begrenzte Nachrichtenbehandlung, expliziten
Session-Abschluss und payload-sichere Metadaten erhalten. Ein Eingriff nach
Commit ist eine evidence-gesteuerte Host-/Transportfrage: Safe zeichnet das
tatsächliche konservative Ergebnis auf; Strict ist nicht allein durch einen
konfigurierten Modus oder eine Serviceentscheidung etabliert.

| Frage | Erforderlicher Nachweis |
| --- | --- |
| Ausgewählter P1--P3-Pfad | Reeller Envoy-Verkehr, ausgewählte Service-Records und passende effektive Konfiguration |
| P4-Regelbeobachtung | Response-Body-Stream-/EOS-Metadaten für das ausgewählte Profil |
| Safe Late Behavior | Tatsächliche sichtbare Response plus aufgezeichnete Late-/Actual-Action |
| Strict-/Cancellation-Verhalten | Explizite Host-/Client-Transportbeobachtung, keine API-/Source-Inspektion |

## Tests und Nachweise

Ausgewählte Build-/Config-/Start-/Runtime-Targets werden nur für die vom Target
genannte Ebene verwendet. Fehlende optionale Envoy-Komponenten bleiben
deklarierte Blocked-Prerequisites, statt stillschweigend eine System-Binary zu
wählen. Für einen Lifecycle-Claim sind Run-ID, ausgewählter Integrationsmodus,
Result-/Event-Records, effektive Konfiguration und Hostbeobachtungen gemäß
[Tests und Nachweise](../testing-and-evidence.de.md) zu prüfen.

## Betrieb und Fehlerbehebung

Verwenden Sie explizite externe Komponenten-, Runtime-, Log- und Evidence-
Roots. Konfiguration und Servicestart werden getrennt von echtem Envoy-Verkehr
diagnostiziert. Bei einer Response- oder Late-Intervention-Frage sind
Stream-/Commit-Grenze und tatsächliche Aktion vor der Deutung eines
zurückgegebenen Status zu prüfen.

## Grenzen und Kompatibilität

<code>ext_authz</code> bleibt ein Kompatibilitätspfad und ersetzt keine
ausgewählte Full-Lifecycle-ext_proc-Response-Verarbeitung. HTTP/2, HTTP/3,
CRS, Strict Reset/Cancellation, First Byte und No-Full-Response-Buffer-
Eigenschaften benötigen eigene ausgewählte Hostnachweise.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [Envoy-Konfigurationsreferenz](../../examples/envoy/configuration-reference.de.md)
