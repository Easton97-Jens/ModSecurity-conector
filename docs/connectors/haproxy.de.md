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

## libModSecurity-Binding-Kompatibilität

Das gemeinsame Binding unterstützt `libModSecurity >= 3.0.14`, wobei `3.0.14`
die öffentliche C-API-Mindestbaseline ist. Es kompiliert und linkt die
erforderliche Baseline-API gegen ein explizit ausgewähltes passendes Header- /
Library-Paar. Ein Deklarations- oder Library-Mismatch schlägt mit einer
Baseline-API-Diagnose fehl; die optionale API
`msc_get_rules_messages_rule_ids` ist niemals der Grund, warum eine gültige
`3.0.14`-Baseline abgelehnt wird.

Die optionale API wird nur aktiviert, wenn ihre exakte Deklaration gegen
dasselbe Paar kompiliert und ihr Symbol linkt. Die resultierende Compile-Time-
Capability wird konsistent von den unabhängigen SPOP- und nativen HTX-Builds
verwendet. Ohne sie kann eine begrenzte Rule-ID für Diagnosen aus einem
Interventionslog gewonnen werden; andernfalls ist `rule_id=0` ein expliziter
Wert für nicht verfügbare Metadaten. Disruptive-State, Status, Redirect-/Deny-
Aktion, Cleanup und jede Host-Durchsetzung werden weiterhin aus
`msc_intervention` abgeleitet, niemals aus Rule-ID-Metadaten. Der code-nahe
[Kompatibilitätsvertrag und die Befehle](../../connectors/haproxy/README.de.md#libmodsecurity-kompatibilitätsvertrag)
beschreiben die exakten Probes, den Feature-State in `paths.env` und die
getrennten Validierungsziele.

## Konfiguration

Vollständige native HTX-Syntax und getrennte SPOE/SPOP-Kompatibilitätseinträge
stehen in der [HAProxy-Konfigurationsreferenz](../../examples/haproxy/configuration-reference.de.md).
Hostfilter-Konfiguration, Common-Runtime-Key/Value-Einstellungen und
ModSecurity-Engine-Regeln bleiben getrennte Ebenen.

## Richtlinie für HTX-Payload-Append-Fehler

Das HTX-Binding behandelt einen nativen Body-Append nur dann als erfolgreich,
wenn sein Adapter `0` liefert (wofür die zugrunde liegende C-API exakten Erfolg
melden muss). Jedes andere Ergebnis bedeutet, dass die aktuell geliehene
HTX-Slice nicht mehr als inspiziert bestätigt ist. Der Filter bricht nur die
betroffene Transaktion ab und liefert `-1` an HAProxy; er darf nicht die
positive Slice-Länge liefern und damit einen nicht inspizierten Pass-through
autorisieren.

| Fehlerklasse | Fail-Modus und Hostaktion | Event-Evidence | Cleanup und Folgeanfrage |
| --- | --- | --- | --- |
| Request-Body-Append-Fehler (V10, pre-commit) | Fail closed. HAProxy erhält `-1`; der aufbewahrte HTTP/1.1-HAProxy-`3.2.22`-Control beobachtete `400` und null Backend-Dispatches. | Für diesen nativen Callback-Fehler wird kein dediziertes strukturiertes Connector-Error-Event ausgegeben. Payload-freie Evidence sind Client-Status, Upstream-Count null und aufbewahrter Host-Receipt. | Die Transaktion wird einmal abgebrochen. Derselbe HAProxy-Prozess akzeptierte einen One-Byte-POST-Allow-Control mit `200`; beide task-eigenen Listener fehlten nach Cleanup. |
| Response-Body-Append-Fehler (V11, Response-Pfad) | Fail closed an der Transportgrenze. HAProxy erhält `-1` und beendet nur den betroffenen Response-Stream. Sobald die Response-Behandlung begonnen hat, wird kein synthetischer Ersatz-HTTP-Status versprochen. Der aufbewahrte Control beobachtete keine HTTP-Response (`000`) und `curl_exit=52`. | Für diesen nativen Callback-Fehler wird kein dediziertes strukturiertes Connector-Error-Event ausgegeben. Payload-freie Evidence sind Client-Transportergebnis, ein Upstream-Fehlerrequest und aufbewahrter Host-Receipt. | Die Transaktion wird einmal abgebrochen. Derselbe HAProxy-Prozess akzeptierte einen HEAD-Allow-Control mit `200`; beide task-eigenen Listener fehlten nach Cleanup. |

Dies ist eine dokumentierte HTX-spezifische Sicherheitsentscheidung: Ein aus
`ProcessPartial` abgeleiteter nativer Append-Fehler ist für die geliehene Slice
terminal, weil dieses Binding ihre Inspektion nicht bestätigen kann. Es wählt
nicht stillschweigend die abweichende Semantik eines anderen Connectors. Der
aufbewahrte begrenzte Run ist
`haproxy-htx-append-failure-20260825T131500Z`, SHA-256
`12e4d30c68ff46f45f2f8481d810eb53099f6512f384520e3942fadb0434da9c`; er belegt
nur diese V10/V11-HTTP/1.1-Fälle, nicht HTTP/2, HTTP/3, Reload, einen
vollständigen FD-Audit oder die vollständige Fehlermatrix.

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

## Logische Grenze der SPOE/SPOP-Response-Begleitkomponente

Der getrennte SPOE/SPOP-Prozess kann die Request-seitige P1/P2-Transaktion
besitzen; sein Request-Protokoll überträgt jedoch weder den HTX-Response-Body-
Stream noch Response-EOS. Deshalb modelliert das Repository die
Response-Verarbeitung als eine logische Transaktion über zwei Hostkomponenten:
SPOP erzeugt nach P2 ein begrenztes opakes `response_handle`, und der native
HTX-Filter verwendet die private Response-Begleitkomponente, um dieses Handle
zu übernehmen, P3 zu verarbeiten, begrenzte P4-Chunks weiterzugeben und P4 bei
HTX-EOS abzuschließen. Fehlende, abgelaufene, fehlerhafte oder nicht
übernommene Korrelation muss fail-closed behandelt und bereinigt werden; sie
darf nicht stillschweigend zu einem reinen Request-Ergebnis werden.

Der repository-native kombinierte Harness baut den aktuellen MRC1-v2-SPOP-
Agenten und das HTX-Overlay und hat geordnete P1/P2-Bestätigung, P3-Claim,
P4-DATA/EOS, Cancel, TTL, fehlende Korrelation und Cleanup lokal beobachtet.
Dies ist qualifizierte lokale Runtime-Evidenz, keine Behauptung allgemeiner
Produktionsreife oder breiter Deployment-Eignung. Die Produktivaktivierung
bleibt ausdrücklich: privater Companion-Socket, passende UID/GID und ein
begrenztes Response-Body-Limit größer null sind verpflichtend. Der Standardpfad
`response-companion=none` weist Response-Body-Aktivierung weiterhin zurück,
weil er kein Response-EOS transportieren kann. Der oben ausgewählte native
HTX-Pfad bleibt davon unabhängig verfügbar.

### Byte-Grenze für die SPOP-Request-ID

Die SPOP-`request_id` ist ein Korrelationsschlüssel, kein Display-String. Die
Runtime validiert ihre ursprünglichen längenbegrenzten Bytes, bevor sie in
einen C-String kopiert werden. Leere, eingebettete-NUL-, Control-Byte-, Nicht-
ASCII- und zu lange Werte werden abgewiesen; zum Beispiel kann `A\0X` niemals
zu `A` kollabieren und denselben Transaktions-Cache-Slot adressieren. Eine
nichtleere druckbare ASCII-ID, einschließlich der normalen UUID-Form, bleibt
zulässig. Eine fehlerhafte `request_id` lässt die Notification-Extraktion
fehlschlagen und erzeugt, ersetzt oder claimt keine Transaktion.

## Historische SPOE/SPOP-Kompatibilität

Die Dateien unter <code>examples/haproxy/compatibility-spoe/</code> sind
historische Request-/Header-Kompatibilitätsbeispiele. Sie sind weder die oben
beschriebene logische Response-Companion-Bridge noch der ausgewählte native
HTX-Pfad. Insbesondere übertragen ihre `http-response send-spoe-group`-
Beispiele keine Response-Body-Chunks und kein Response-EOS. Sie dürfen daher
nicht als Nachweis für natives HTX-Verhalten, P4-Response-Body,
Safe-/Strict-Late-Verhalten, First-Byte-Verhalten oder No-Full-Response-
Buffering verwendet werden.

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
