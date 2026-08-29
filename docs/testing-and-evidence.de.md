# Tests und Nachweise

**Sprache:** [English](testing-and-evidence.md) | Deutsch

## Geltungsbereich

Tests unterscheiden Strukturprüfungen, Build-/Konfigurationsprüfungen,
fokussierten Hostverkehr, Full-Lifecycle-Ausführung und Evidence-Validierung.
Das Bestehen einer Ebene bedeutet nicht, dass eine andere bestanden hat. Die
ausgewählte Dokumentation ist auf die sechs HTTP/1.1-Kernpfade begrenzt und
behauptet keine Produktionsreife, kein CRS, keine vollständige Matrix, kein
HTTP/2, kein HTTP/3 und kein Strict-Verhalten für alle Connectoren.

Die allgemeinen Make-Targets in diesem Leitfaden behalten ihren
Sechs-Connector-Scope. Der zeitgesteuerte/manuelle Workflow
<code>all-connectors-no-crs.yml</code> ist enger: Sein geschlossenes Profil
<code>no-crs</code> führt nur Apache, HAProxy, Envoy, Traefik und lighttpd aus.
Es weist unbekannte Profile und Zeilen außerhalb dieser Zuordnung ab; NGINX ist
kein Ergebnis dieses Workflows. Das Profile-Aggregate validiert je ein
gebundenes Ergebnis und einen Receipt pro ausgewähltem Connector, einschließlich
Run-/Commit-Identität und Cleanup-Status. Diese Validierung ist kein Nachweis
eines bestandenen gehosteten Runtime-Laufs und liefert keine CRS-, MRTS-,
HTTP/2-, HTTP/3-, Full-Matrix- oder Produktions-Claims.

## Testebenen

| Ebene | Typisches Target | Belegt | Belegt nicht |
| --- | --- | --- | --- |
| Dokumentation und Verträge | <code>make quick-check</code>, <code>make lint</code> | Konsistenz von Quelle, Schema, Links, Sprache und Verträgen | Live-Hostverkehr |
| Build | <code>make build-&lt;connector&gt;</code> | Einen ausgewählten Buildschritt | Konfigurationsladen oder Request-/Response-Verhalten |
| Konfiguration | <code>make check-config-&lt;connector&gt;</code> | Dass die ausgewählte Konfiguration geparst oder geladen werden kann | Laufzeitverhalten |
| Fokussierter Smoke | <code>make runtime-smoke-&lt;connector&gt;</code> | Die vom Target dokumentierte enge Hostübung | Full Lifecycle oder Katalogvollständigkeit |
| Full Lifecycle | <code>make full-lifecycle-&lt;connector&gt;</code> | Ausgewähltes Profil plus Artefakterzeugung | Produktionsreife oder alle Protokolle |
| Evidence-Validierung | <code>make evidence-check-&lt;connector&gt;</code> | Dass vorhandene Laufartefakte den Vertrag dieses Validators erfüllen | Einen neuen Hostlauf |

Der Platzhalter <code>&lt;connector&gt;</code> ist genau einer von Apache,
NGINX, HAProxy, Envoy, Traefik oder lighttpd in der kleingeschriebenen
Target-Form.

## Kernbefehle

| Ziel | Befehlsmuster | Grenze |
| --- | --- | --- |
| Schnelle Repository-Validierung | <code>make quick-check</code> | Startet nicht jeden Host und erstellt keine kanonische Evidence |
| Ein ausgewählter aggregierter Kandidat | <code>NO_CRS_RUN_ID=&lt;run-id&gt; make full-lifecycle-all-connectors</code> | Erzeugt nur Kandidatenartefakte |
| Aggregierte Kernvalidierung | <code>NO_CRS_RUN_ID=&lt;run-id&gt; make check-six-connector-core-completion</code> | Liest finalisierte Evidence für diese Run-ID |
| Eine Konfigurationsprüfung | <code>make check-config-&lt;connector&gt;</code> | Sendet keinen Verkehr |

<code>NO_CRS_RUN_ID</code> ist ein dateisystemsicherer, nicht geheimer
Bezeichner. Er bindet Artefakte an eine Invocation; er ist kein Ergebnislabel
und kein Promotion-Mechanismus.

## Cases, Regeln und Protokollgrenzen

Das Framework besitzt wiederverwendbare YAML-Cases, Katalogauswahl, Schemata
und Normalisierung. Das Connector-Repository besitzt Hostintegration und seine
ausgewählten Regel-/Konfigurationsinputs. Repository-eigene No-CRS-Regeln und
IDs sind vom OWASP CRS getrennt. Ein vorbereitetes CRS-Input oder ein
quellbasierter Protokollpfad verifiziert weder CRS-Verhalten noch HTTP/2 oder
HTTP/3.

| Thema | Erforderlicher Nachweis |
| --- | --- |
| P1/P2/P3 | Ausgewählter Hostverkehr, passende Ergebnisdatensätze und profilgerechte Events |
| P4 | Phasenspezifische Artefakte plus tatsächliche Commit-/EOS-Grenze |
| First Byte vor EOS | Synchronisierte Timing- oder Transportbeobachtung, nicht nur eine abgeschlossene Response |
| Kein vollständiges Response-Buffering | Quell- und/oder Hostbeobachtung, die einen connector-eigenen vollständigen Response-Puffer ausschließt |
| Protokollclaims | Explizite Protocol-Client-, Host- und Artefaktnachweise für das genannte Protokoll |

## Evidence-Modell

Kanonische Evidence ist laufbezogen. Sie identifiziert Connector, ausgewähltes
Profil, Regeln, Run-ID, effektive Konfiguration, Status und erforderliche
Result-/Eventdatensätze. Rohe invocation-lokale Ausgabe wird nicht automatisch
befördert: Normalisierung und Validierung müssen Provenienz und die ausgewählte
Fähigkeitsgrenze erhalten.

| Artefaktklasse | Zweck | Datenschutz- und Aufbewahrungsregel |
| --- | --- | --- |
| Result-Datensätze | Case-Status und beobachtbare Response-Fakten aufzeichnen | Payload-freie Felder und begrenzte IDs behalten |
| Event-Datensätze | Phase, Aktion, Limits und Late-/Commit-Kontext erklären | Keine Request- oder Response-Bodies enthalten |
| Effektive Konfiguration | Einen Lauf an ausgewählte nicht geheime Inputs binden | Secrets und host-private Werte redigieren |
| Logs und Transportbeobachtungen | Einen angegebenen Debugging- oder Timing-Claim stützen | Nur die minimal nötigen Metadaten behalten |

Zugangsdaten, Cookies, Authorization-Werte, private Schlüssel, Zertifikate,
rohe Request-Bodies, rohe Response-Bodies oder lokale Runtime-Ausgabe werden
nicht eingecheckt.

### HAProxy-Hosted-Evidence-Projektion

Die feste HAProxy-Runtime-Zelle `with-crs/no-mrts` darf Evidence erst hochladen,
nachdem ihre Runtime beendet ist und ihr Cleanup-Ergebnis geprüft wurde. Sie
lädt weder den Runtime-Root, Build-Root, Cache-Root, Prozesslogs noch eine
Kopie eines dieser Roots hoch. Stattdessen wird ein Source-Receipt für den
festen HAProxy-P2-Case strikt geparst, mit vertrauenswürdigen Workflowwerten
verglichen und anschließend ausschließlich in
`haproxy-runtime-evidence.json` und `manifest.json` neu serialisiert. Beide
Dateien enthalten nur begrenzte Allowlist-Metadaten und SHA-256-Digests; sie
enthalten keinen Body, Headerwert, Cookie, Token, Credential, opaque Handle,
absoluten Pfad, rohen Log oder freien Runtime-Fehlertext.

Receipt-Bytes passieren eine feste unprivilegierte Stream-Grenze
`head --bytes=16385` und danach den Evidence-Projektor nur über Standard-
Eingabe nach der Privilegabgabe. Der Projektor akzeptiert höchstens 16 KiB und
weist das 16.385. Byte zurück; der Workflow puffert daher keine untrusted
Receipt-Ausgabe in einer Shell-Variablen. Receipt-Bytes sind niemals
Kommandozeilen-Argumente für `sudo`, `unshare` oder `setpriv`.

Projektion und Verifier weisen unerwartete Namen, Pfade, JSON-Schlüssel,
Typen, Special Files, Symlinks, Größenlimitverletzungen und Digest-Mismatches
zurück. Ihr Staging-Paket entsteht unterhalb eines neuen root-besessenen
`RUNNER_TEMP`-Childs. Das Paketverzeichnis gehört der getrennten Evidence-UID
und hat die Runtime-GID des Upload-Lesers als Gruppe: Es beginnt mit `0700`,
danach versiegelt der Projektor es mit `0550`. Die zwei festen Dateien der
Evidence-Identität bleiben `0444`, aber eine nicht zugehörige Identität kann
das `0550`-Verzeichnis nicht traversieren; der effektive lesbare Pfadzugriff
ist auf den Evidence-Owner und diese Upload-Leser-Gruppe begrenzt. Der
Runtime-/Upload-Leser erhält nur Lesen/Traversieren, niemals Verzeichnis-
Schreiben, Umbenennen, Unlink oder chmod. Der Verifier prüft diesen Ownership-
und Modusvertrag unmittelbar vor der gepinnten Upload-Action. Checkout-Code
für Runtime, Source-Export, Projektion, Verifikation und die abschließende
Workflow-Summary läuft nur nach privatem PID-/Mount-Namespace und
Privilegabgabe mit `no_new_privs`; privilegierte Operationen haben feste
nur-Staging-Pfade und führen keinen Checkout-Code aus.

Jeder eingebettete Immutable-Git-Object-Launcher verifiziert den exakten
Git-Blob-Preimage `b"blob " + Dezimallänge + b"\0" + source`, bevor `compile`
ihn ausführen kann. `\0` ist hier Git's einzelnes NUL-Trennbyte und nicht ein
druckbarer Backslash plus Null; ein abweichender Preimage lässt den Job
fehlschlagen, bevor ausgewählter Checkout-Code ausgeführt wird.

Für eine Evidence-Receipt-Runtime fordert das Cleanup zuerst den `setsid`-
Leader zum Stoppen auf, gibt ihm ein begrenztes Reaping-Fenster, beendet dann
eine verbleibende Prozessgruppe und eskaliert nur nach Ablauf des begrenzten
Termination-Fensters auf `KILL`. Es wartet weiterhin auf den aufgezeichneten
Leader und verifiziert eine leere Prozessgruppe. Jeder fehlgeschlagene Stop-,
Wait- oder Residual-Group-Check verhindert Receipt, Projektion und Upload.

Diese Grenze zeichnet nur den festen P2-Receipt auf und beansprucht weder
P3/P4 noch Produktionsreife oder ein erfolgreiches Hosted-Ergebnis, bevor der
exakte Workflow-Lauf und sein hochgeladenes Artefakt beobachtet wurden.

## Status und Promotion

| Status | Bedeutung |
| --- | --- |
| <code>PASS</code> | Die ausgewählte Prüfung erfüllte ihre aufgezeichneten Bedingungen |
| <code>FAIL</code> | Eine erforderliche Bedingung wurde nicht erfüllt |
| <code>BLOCKED</code> | Eine deklarierte Voraussetzung war nicht verfügbar oder unsicher |
| <code>NOT EXECUTED</code> | Der Case/Pfad wurde absichtlich nicht ausgeführt |
| <code>NOT APPLICABLE</code> | Der Case/Pfad liegt außerhalb des dokumentierten Scope des ausgewählten Jobs oder Profils |
| <code>UNSUPPORTED</code> | Das ausgewählte Hostmodell kann die erforderliche Fähigkeit nicht bereitstellen |

Promotion ist Evidence-gesteuert. Ein Build, Konfigurationsladen,
Capability-Manifest, generierter Bericht oder statisches Inventar macht einen
nicht ausgeführten Case nicht zu PASS. Aktuelle Readiness und laufbezogener
Status gehören in die aktuellen Reports; dieser Guide erklärt das Modell statt
historische Statusmatrizen zu bewahren.

CI-Steuerungsdatensätze können die entsprechenden kleingeschriebenen Werte
`passed`, `failed`, `blocked`, `not_executed` und `not_applicable` verwenden.
Sie erhalten das Ergebnis der direkten Prüfung, bevor eine rekursive
Orchestrierungsschicht ihren Exitcode ersetzen kann; sie sind keine
Runtime-Evidence-Datensätze. Ein `blocked`- oder `not_applicable`-
Steuerungsdatensatz erlaubt Workflow-Erfolg nur dort, wo der konkrete
Workflow-Vertrag ihn ausdrücklich zulässt.

## Historischer Kontext

Frühere Connector-spezifische Proof-of-Concept-Zusammenfassungen,
Planungsnotizen und Zwischenstände der Evidence wurden in die
Connector-Guides, aktuellen Reports und den Architektur-/Evidence-Audit
überführt. Sie begründeten keine eigene Source of Truth und bleiben über die
Git-Historie verfügbar. Die oben beschriebene aktuelle Evidence-Grenze bleibt
unverändert.

## Lokale Entwicklung und Sicherheit

Verwenden Sie extern beschreibbare Runtime-, Cache-, Build-, Log- und
Evidence-Roots, die über dokumentierte Variablen ausgewählt werden. Das
Repository schreibt keinen Entwickler-Checkout-Ort vor. Fehlende optionale
Komponenten sollen das deklarierte Blocked-/Prerequisite-Exit-Verhalten nutzen,
statt stillschweigend eine nicht zusammenhängende System-Binary herunterzuladen,
zu installieren oder zu verwenden.

Format, Defaults, Setter und Sicherheitshinweise der Variablen stehen unter
[Variablen](reference/variables.de.md). Host-/Profilsyntax steht unter
[Konfiguration](configuration.de.md).

## Verwandte Referenzen

- [Architektur](architecture.de.md)
- [Connector-Guides](connectors/README.de.md)
- [Betrieb und Sicherheit](operations-and-security.de.md)
- [Aktuelle Reports](../reports/README.de.md)
