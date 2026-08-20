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

Der Plan wird durch einen SHA-256-Digest über die exakten Planbytes versiegelt
und durch jede Hostadapter-Grenze weitergereicht. Vor dem Hoststart liest der
Validator die versiegelten Bytes erneut, weist doppelte JSON-Schlüssel zurück,
prüft den Plan-Digest und rekonstruiert die ausgewählten Cases aus dem exakten
Framework-Inventar. Die ausgewählten Case-Hashes und der Inventar-Hash müssen
mit dem Plan übereinstimmen; eine Änderung an URI, erwarteter Event-ID oder
Case-Quelle führt daher zu einem fail-closed-Abbruch. Der Executor erhält
denselben Digest explizit und zeichnet ihn im Receipt auf.

Die Rule-Match-Evidence verwendet einen typisierten nativen
`RuleMessage`-Observer. Standardmäßig ist er deaktiviert und wird nur für das
versiegelte MRTS-Runtimeprofil aktiviert. Der Observer erzeugt begrenzte,
metadatenbasierte JSONL-Datensätze mit Request-/Transaktionskorrelation; er
liest keine Audit-Logs, Error-Logs, stderr- oder Request-/Response-Payloads.
Native Integritäts- und Verkettungsprüfungen erfolgen, bevor das Ergebnis
akzeptiert wird.

Das versiegelte `mrts.load` enthält absichtlich den vollständigen gepinnten
MRTS-Korpus. Daher verwendet DetectionOnly dasselbe kanonische Orakel wie
Apache und HAProxy: Jede vom Case deklarierte erwartete Regel-ID muss in ihrer
exakt korrelierten Phase beobachtet werden, während zusätzliche vollständig
validierte native Treffer derselben Phase nur bei Mitgliedschaft im erneut
validierten gepinnten Regel-ID-Inventar im Receipt erhalten bleiben. Sie
können keine erwartete ID ersetzen. Eine erwartete ID in einer anderen Phase
führt fail-closed zum Fehler; jeder korrelierte Regeltreffer lässt weiterhin
einen Kontroll- oder Bypass-Case fehlschlagen.

Die Parent-Python-Grenze erhält den geprüften task-lokalen venv-Interpreter,
ohne dessen letzten Symlink aufzulösen. Symlinkte übergeordnete Verzeichnisse
werden zurückgewiesen; die Shell-Dispatcher reichen vor MRTS-Materialisierung
und Child-Prozess-Ausführung denselben genehmigten Interpreter durch ihre
geschlossene Grenze weiter. Die Behebung behauptet keine Umschreibung des
aufrufenden `PATH`; der Framework-Generator verwendet die explizite
`PYTHON`-Auswahl. Damit wird der diagnostizierte Fehler `FND-PARENT-0194`
behoben, bei dem System-Python während der Regelerzeugung die PyYAML-
Abhängigkeit der venv verlor. Das Finding bleibt bis zur frischen
Runtime-Validierung der Behebung
release-blockierend.

Frisches Envoy `r10` erreichte gepinnte Provisionierung, echten Hoststart und
Readiness, stoppte aber vor der MRTS-Case-Ausführung mit HTTP 500. Im
versiegelten MRTS-Evidence-Modus verlangt Common ausschließlich den
Korrelations-Header `x-mrts-transaction-id`; der Readiness-Probe sendete noch
den Normalmodus-Header `X-Request-Id`. Dieser rein diagnostische Versuch
erzeugte keinen MRTS-Receipt und ist kein Runtime-Nachweis. Die enge aktuelle
Parent-Korrektur wählt das Literal `x-mrts-transaction-id` nur für MRTS-
Readiness und bewahrt `x-request-id` für den normalen Envoy-Modus. Separat
routet der Lighttpd-Dispatcher `MSCONNECTOR_MRTS_RUNTIME=1` nun ausschließlich
zu seinem versiegelten Full-Lifecycle-Hostexecutor und erhält den Nicht-MRTS-
Kompatibilitäts-Smoke-Pfad. Keine der beiden Quellkorrekturen begründet ein
Host-Runtime-Ergebnis.

Commit `6e63fb52` enthält diese Korrekturen für den versiegelten MRTS-
Readiness-Header und den Lighttpd-Dispatcher. Frisches Envoy `r11` erreichte
danach echten Envoy-/ext-proc-Start und den korrigierten Readiness-Pfad, ist
aber nur diagnostisch: Der Lauf stoppte vor MRTS-Case-Receipts, weil gültige
unabhängige Readiness-Events vor der Transaktions-/URI-Korrelation auf ihre
Phase geprüft wurden. Die gültige unabhängige Transaktion
`envoy-ext-proc-readiness-1` enthält `request_body`-, `response_headers`- und
`response_body`-Records; ihre Existenz ist keine Runtime-Erfolgsbehauptung.

Die enge Executor-Korrektur erhält Duplicate-safe-Parsing, exaktes Schema,
native Hash- und globale Chain-Validierung für jede Event-Zeile. Sie verwendet
eine endliche native Phasenzuordnung, ignoriert nur vollständig gültige
unabhängige Transaktions-/URI-Records nach dieser Validierung und behält ein
relevantes Event mit falscher Phase fail-closed. `FND-PARENT-0198` verfolgt
diesen Parent-eigenen Reihenfolgenfehler. Frische Envoy-Receipts nach dem Fix
und eine unabhängige Wiederholung bleiben erforderlich.

Frisches Envoy `r12c` erreichte den gepinnten Build, echten ext-proc-Hoststart,
Readiness und einen DetectionOnly-Request, erzeugte aber keinen gültigen
MRTS-Receipt. Ein zweites Executor-Klassifikationsproblem behandelte gültige
`response_headers`- und `response_body`-Rule-Matches derselben Transaktion als
ungültig, nur weil sie außerhalb des ausgewählten Request-Body-Profils liegen.
Diese nicht erwarteten Response-Phasen derselben Request-Transaktion müssen
weiter integritätsvalidiert werden und liegen danach außerhalb des ausgewählten
Request-Body-Akzeptanzprofils. Demgegenüber bleiben eine erwartete Regel-ID in
falscher Phase sowie alle Kontroll-/Bypass-Erwartungen fail-closed. Vor jeder
Runtime-Klassifikation ist weiterhin ein frischer Hostlauf nach dem Fix nötig.

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

Zum Zeitpunkt dieser Dokumentationsänderung ist der Pfad mit seinen Verträgen
im Task-Worktree vorhanden. Die beobachtete lokale Validierung umfasst 97
fokussierte Python-Contract-Tests, Shell-Syntaxprüfungen für die geänderten
Runner, Python-Kompilierung, `check-common-security-contract.py`,
`check-adapter-contracts.py`, `check-remaining-connectors-build-wiring.py`
und `git diff --check`. Die Go-Prüfungen für Envoy und Traefik verwendeten
`/usr/local/go/bin/go` `go1.26.6` mit `GOTOOLCHAIN=local`: `gofmt`,
`go mod verify`, `go list -deps ./...`, `go test ./...`, `go vet ./...` und
`govulncheck ./...` bestanden (das Traefik-Modul wurde aus
`connectors/traefik/native_middleware` ausgeführt; der erste längere
temporäre Socket-Pfad wurde durch einen privaten kurzen Test-Root ersetzt).
C/C++-Syntaxprüfungen und der repository-native C17-Check für die übrigen
Connectoren bestanden ebenfalls. Der breite C++-Security-Scan behielt die
ursprüngliche C/H-Baseline bei und ergänzte nur die neue typisierte Observer-
`.cc`-Datei; die bestehende
`common/scripts/modsecurity_targeted_eval.cc` wurde nicht ausgenommen. Vier
vorbestehende ShellCheck-SC1007-Warnungen verbleiben im Envoy-
Konfigurationshelfer.
Das anschließende fokussierte Envoy-/Lighttpd-Contract-Paar bestand 50 Tests,
und `sh -n` bestand für die beiden geänderten Dispatch-Skripte. Dies sind nur
lokale Contract-Prüfungen. Die fokussierte Target-Runner-Suite für die r11-
Phasenkorrektur bestand 28 Tests; ihr Security-Review fand keinen konkreten
Blocker. Keines der Ergebnisse ersetzt frische Realhost-Evidence.

Die echten Hostläufe für alle drei Connectoren, gehostete Actions, Required
Checks, SonarQube-Cloud-Analyse und PR-Head-Gleichheit wurden durch diese
Dokumentationsänderung noch nicht beobachtet. Sie bleiben
<code>NOT EXECUTED</code> beziehungsweise <code>PENDING</code>, bis die
entsprechende Exact-Head-Evidence vorliegt. Ein statischer Plan, ein Inventar,
ein Parser-Test oder ein Workflow-Vertrag darf nicht zu einem
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
