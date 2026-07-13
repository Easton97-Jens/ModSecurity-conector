# HAProxy-Connector

**Sprache:** [English](haproxy.md) | Deutsch

## Überblick

HAProxy verwendet den ausgewählten Pfad <code>native-htx-filter</code> mit dem
Repository-Overlay. Er ist die ausgewählte HTTP/1.1-P1--P4-Safe-Referenz.
Dieser Guide behauptet keine Produktionsreife, keine CRS-Verifikation, keine
vollständige Protokollabdeckung, keine vollständige Matrix, keinen First-Byte-
Nachweis, keinen No-Full-Buffer-Nachweis und kein Strict-Late-Verhalten für
jeden Case.

## Architektur und Ownership

Der native Pfad besitzt HTX-Filterregistrierung, HAProxy-Prozess-/Build-Kleber,
HTX-Nachrichtenübersetzung, Pre-Commit-Reply-Mapping und Host-Lifecycle.
Common liefert neutrale Config-/Default-/Merge-/Validierungssemantik,
Parserverträge, Mappingverträge, Limits, nur Metadaten enthaltende Events,
Regel-IDs und Redaktionshelfer. Es besitzt weder HAProxy-Frame-Behandlung noch
Prozesszustand.

| Lifecycle-Bereich | Ausgewählte native HTX-Verantwortung | Grenze |
| --- | --- | --- |
| P1 | Request-Metadaten vor einer zulässigen lokalen Reply verarbeiten | Eine Reply ist nur Nachweis für ihren ausgewählten Case |
| P2 | Den ausgewählten Request-Body-Probe bei Request-EOS verarbeiten | Sie beweist kein allgemeines inkrementelles Request-Forwarding |
| P3 | Response-Header vor dem Forwarding der ausgewählten Upstream-Headerresponse verarbeiten | Tatsächlich host-sichtbare Response erhalten |
| P4 | Begrenzte Response-Chunks leihen und bei HTX-EOS abschließen | Safe-Ergebnis ist ausdrücklich <code>log_only</code> |
| Events | Payload-freie Metadaten schreiben | Metadaten nicht in einen Transportclaim verwandeln |

## Build

Der [HAProxy-Compiler-Guide](../build/compilers/haproxy.de.md) beschreibt das
ausgewählte HTX-Overlay, Source-Inputs, Build-Roots und Konfigurationsprüfungen.
Der [HAProxy-Source-Guide](../../connectors/haproxy/README.de.md) bleibt der
code-nahe Einstieg. Compile-/Link-Prüfungen sind kein Laufzeitnachweis.

## Konfiguration

Vollständige native HTX-Syntax und getrennte SPOE/SPOP-Kompatibilitätseinträge
stehen in der [HAProxy-Konfigurationsreferenz](../../examples/haproxy/configuration-reference.de.md).
Hostfilter-Konfiguration, Common-Runtime-Key/Value-Einstellungen und
ModSecurity-Engine-Regeln bleiben getrennte Ebenen.

## P1--P4-Lifecycle und Safe-Grenze

Der ausgewählte native Hostsmoke kann P1, P2, P3 und P4 über den HTX-Pfad
beobachten. P1/P3 können eine zulässige lokale Reply vor Commit ausgeben. Der
ausgewählte One-Block-P2-Probe zeichnet seinen eigenen beobachteten
Upstream-Count auf, belegt aber keine allgemeine Forwarding- oder
Buffering-Eigenschaft. P4 Safe erhält die Ursprungsresponse und zeichnet
<code>host_action=log_only</code> auf; P4 Strict bleibt
<code>host_action=not_attempted</code>, bis ein ausgewählter Lauf getrennte
Host-/Client-Evidence liefert.

| P4-Frage | Erforderliche Beobachtung |
| --- | --- |
| Regel beobachtet | Native HTX-P4-Regelmetadaten und ausgewählter Lauf/Profil |
| Safe Late Result | Ursprüngliche sichtbare Response plus aufgezeichnete <code>log_only</code>-Aktion |
| Strict Late Result | Explizite Hostaktion und Client-/Transportnachweis, kein Legacy-Sample |
| Streaming-/First-Byte-Eigenschaft | Dedizierte Quell- und Transportartefakte für diese Eigenschaft |

## Historische SPOE/SPOP-Kompatibilität

Das frühere SPOE/SPOP-Material ist **nur Dokumentation**:
<code>implementation_status: not_started</code> und
<code>runtime_verified: false</code>. Es ist nicht der ausgewählte native
HTX-Pfad. Seine historischen Beispieldateien bleiben getrennt unter
<code>examples/haproxy/compatibility-spoe/</code>; sie dürfen nicht für Claims
zu nativem HTX-Verhalten, P4-Response-Body, Safe-/Strict-Late-Verhalten,
First-Byte-Verhalten oder No-Full-Response-Buffering verwendet werden.

## Tests und Nachweise

<code>make check-config-haproxy</code> prüft die ausgewählte Konfiguration; das
passende Full-Lifecycle-Target führt einen echten Hostlauf aus. Laufbezogene
Result-Datensätze, HTX-/Hostbeobachtungen, effektive Konfiguration und nur
Metadaten enthaltende Events sind zu prüfen. Statusvokabular und
Promotion-Grenze stehen unter [Tests und Nachweise](../testing-and-evidence.de.md).

## Betrieb und Fehlerbehebung

Verwenden Sie explizite extern beschreibbare Build-/Runtime-/Evidence-Roots.
Bei einem nativen Konfigurationsproblem sind zuerst ausgewähltes HTX-Overlay
und Hostkonfiguration zu prüfen. Bei einer Interventionsfrage wird die
angeforderte WAF-Aktion von der tatsächlichen HAProxy-Hostaktion und dem
sichtbaren Clientergebnis unterschieden.

## Grenzen und Kompatibilität

Native HTX- und historische SPOE/SPOP-Integration sind verschieden. Ihre
Direktiven, Nachweise oder Grenzen dürfen nicht kombiniert werden. Kein Pfad
hier begründet breite Streaming-, vollständige Response-Body-, Strict-Abort-,
CRS- oder Produktionsclaims ohne die passenden ausgewählten Hostartefakte.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [HAProxy-Konfigurationsreferenz](../../examples/haproxy/configuration-reference.de.md)
