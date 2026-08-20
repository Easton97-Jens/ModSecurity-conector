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

## Geschlossener no-CRS/with-MRTS-Runtimepfad

Der aktuelle Master-Task ergänzt einen separaten, geschlossenen
<code>no-crs/with-mrts</code>-Runtimepfad genau für Envoy, Traefik und lighttpd.
Der Einstieg ist
<code>ci/runtime/lifecycle/run-no-crs-with-mrts-target.py</code>; er verlangt
<code>--execute-stage</code> und weist jeden Connector außerhalb dieser drei
Einträge zurück. Apache und HAProxy verwenden im Fünf-Connector-Workflow
weiterhin ihren bestehenden MRTS-Hostpfad; dieser Abschnitt ändert deren
Vertrag nicht.

Der Pfad erzeugt einen privaten Run-Root, prüft den Parent-Gitlink auf das
Framework und den Framework-Gitlink auf MRTS und importiert die MRTS-Cases über
das exakt ausgecheckte Framework. Die aktuell gepinnte Kette lautet:

| Repository | Vom Pfad verwendete Revision |
| --- | --- |
| Parent | aktuelle Task-Basis `b42907ca410da69843c80d0c4376193b6ab3801b` |
| Framework-Gitlink | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| MRTS-Gitlink | `615b13bacbd008562c17408246c41ab27dca3104` |

Der erzeugte Plan zeichnet die drei Revisionen, das importierte Case-Inventar
und seine Hashes, die erzeugte Load-Datei, das Profil sowie den geschlossenen
Case-Satz auf. Der Executor
<code>ci/runtime/lifecycle/execute-no-crs-mrts-cases.py</code> sendet echte
Requests durch den ausgewählten laufenden Host und korreliert Request-,
Transaktions-, Case-, erwartete Regel- und beobachtete Event-IDs. Er verlangt
HTTP 200 im DetectionOnly-Modus, einen echten Detection-Case, einen legitimen
Kontrollfall und einen gutartigen Bypass-Kontrollfall, bevor er das begrenzte
Ergebnis atomar schreibt.

Dieses Profil ist ausdrücklich no-CRS. Der Pfad weist CRS-Referenzen in der
erzeugten MRTS-Load-Datei zurück und übergibt als aktive Nicht-CRS-Eingabe nur
die repository-eigenen no-CRS-Regeln. OWASP CRS wird weder aktiviert noch
beschafft, gecacht oder wiederverwendet. Erzeugter Plan, Resultat, Event-Log,
Host-Zusammenfassung und Cleanup-Status verbleiben im privaten Run-Root; sie
sind Runtime-Evidence und keine einzucheckenden Quelldateien.

Die drei Hostadapter müssen ihren echten Connector starten und den Plan
ausführen, solange dieser Connector läuft:

- Envoy verwendet den bestehenden ext-proc-Hostpfad;
- Traefik verwendet den bestehenden nativen Middleware-Hostpfad; und
- lighttpd verwendet den bestehenden gepatchten nativen Hostpfad.

Der Task ändert weder die negativen <code>with-crs/with-mrts</code>-Ziele für
diese Connectoren noch NGINX. Ebenso wird keine Framework- oder MRTS-Quelle
geändert; die oben genannten Framework- und MRTS-Revisionen werden als exakte
Gitlinks verwendet.

### Evidence-Status dieses Tasks

Zum Zeitpunkt dieser Dokumentationsänderung sind Pfad und Verträge im
Task-Worktree vorhanden; die echten Hostläufe für alle drei Connectoren,
gehostete Actions, Required Checks, SonarQube-Cloud-Analyse und PR-Head-
Gleichheit wurden durch diese Dokumentationsänderung noch nicht beobachtet.
Sie bleiben <code>NOT EXECUTED</code> beziehungsweise <code>PENDING</code>,
bis die entsprechende Exact-Head-Evidence vorliegt. Ein statischer Plan, ein
Inventar, ein Parser-Test oder ein Workflow-Vertrag darf nicht zu einem
Runtime-<code>PASS</code> befördert werden. Der gepaarte
[Change Record](../reports/audits/change-records/CR-20260820-no-crs-with-mrts-runtime.de.md)
beschreibt den begrenzten Lieferstatus und die Einschränkungen.

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
