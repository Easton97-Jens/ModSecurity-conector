# Change Record: Parent-Lighttpd-Lifecycle-Literal-Deduplizierung für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-lighttpd-lifecycle-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-lighttpd-lifecycle-literals |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Grenze | Ausschließlich der Parent-Lighttpd-Full-Lifecycle-Runner und sein direkter Contract-Test, dieses englische/deutsche Change-Record-Paar und beide Indizes. Framework, MRTS, Gitlinks, Workflows, Scanner-Policies, generierte Reports und `master` bleiben unverändert. |
| Tracking | Live-Baseline-Parent-SonarQube-Cloud-Items `AZ9cRynjHhV2CayPTPzV` (`shelldre:S1192`, `%{http_code}`, 8 Verwendungen) und `AZ9cRynjHhV2CayPTPzW` (`shelldre:S1192`, `1,200p`, 6 Verwendungen). Keines der Items wird vor einer frischen Exact-Head-Pull-Request-Analyse als extern geschlossen behauptet. |

## Motivation und Problemstellung

Der Parent-Lighttpd-Full-Lifecycle-Runner wiederholte zwei feste
Command-Literale: den HTTP-Status-Formatter seiner bestehenden
`curl --write-out`-Probes und das begrenzte `sed -n`-Diagnoseprogramm seiner
bestehenden Fehlerpfade. Die Wiederholung ist die Live-Baseline der beiden
ausgewählten `shelldre:S1192`-Items.

Dies ist ein Literal-only-Maintenance-Refactor. Er muss jede Anfrage, jeden
erwarteten Statusvergleich, jeden Fehlerzweig, Trap, Cleanup-Schritt und
fail-closed Exit bewahren und zugleich jedem festen String einen file-lokalen
Owner geben.

## Akzeptanzkriterien

- Der Runner besitzt genau eine bedingungslose, nicht exportierte Deklaration
  jedes festen Literals, und alle ausgewählten Verwendungen expandieren den
  Wert nur als ein quotiertes Command-Argument.
- Der direkte Source-Contract beweist je eine Deklaration, acht
  `--write-out "$HTTP_STATUS_FORMAT"`-Verwendungen, sechs
  `sed -n "$DIAGNOSTIC_LINES"`-Verwendungen, keine Legacy-Verwendung der
  ausgewählten Literale, keinen Export sowie die bestehenden Lifecycle-Controls
  und Status-Erwartungen.
- Shell-Syntax, die fokussierte No-Host-Contract-Suite und die scoped
  Source/Test-Whitespace-Validierung berichten ausschließlich ihre beobachteten
  erfolgreichen Ergebnisse.
- Dieses vollständige englische/deutsche Change-Record-Paar und beide Indizes
  beschreiben dieselben Fakten, technischen Literale, Einschränkungen und den
  Delivery-Status.
- Es werden weder externe Item-Closure noch Hosted-Check,
  Ready-for-review-Transition, Framework-/MRTS-/Gitlink-/Workflow- /
  Scanner-Policy-/Generated-Report-Änderung, Merge oder `master`-Update
  behauptet.

## Implementierungsentscheidung und Begründung

Der Runner initialisiert diese nicht exportierten Werte bedingungslos vor
seinen Helper-Funktionen:

```sh
HTTP_STATUS_FORMAT='%{http_code}'
DIAGNOSTIC_LINES='1,200p'
```

Jede ausgewählte Status-Probe verwendet nun
`--write-out "$HTTP_STATUS_FORMAT"`, und jede ausgewählte begrenzte
Fehlerdiagnose verwendet `sed -n "$DIAGNOSTIC_LINES"`. Die Werte bleiben
feste interne Shell-Daten; sie sind weder Caller-Environment-Inputs noch aus
Request/Status abgeleitete Werte. Der Refactor ändert weder Request-Konstruktion
noch Status-Erwartung, Control-Flow, Redirection, Trap, Cleanup oder
Fehlerverhalten.

Der direkte Contract-Test pinnt die Deklarationen vor ihren Verwendungen, die
exakten Acht/Sechs-Verwendungszahlen, die nur quotierte Verwendungsform, das
Fehlen eines Exports, das Fehlen der Legacy-Verwendungen der ausgewählten
Literale, bestehende Traps und alle bestehenden Statusvergleiche.

## Geänderte Dateien

- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `reports/audits/change-records/CR-20260728-sonar-lighttpd-lifecycle-literals.md`
- `reports/audits/change-records/CR-20260728-sonar-lighttpd-lifecycle-literals.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `sh -n connectors/lighttpd/harness/run_patched_full_lifecycle.sh` | bestanden. |
| `env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -B -m unittest -v connectors.lighttpd.tests.test_patched_host_contract` | bestanden: 17 Tests; der Root-Rerun endete in 0.244 Sekunden und der Worker-Run in 0.251 Sekunden. |
| Scoped Source/Test `git diff --check` | bestanden. |
| Direkter Source-Readback | bestanden: je eine Deklaration der Werte, acht `--write-out "$HTTP_STATUS_FORMAT"`-Verwendungen und sechs `sed -n "$DIAGNOSTIC_LINES"`-Verwendungen. |
| Unabhängiger fokussierter Shell/HTTP-Review | `already_safe` für den Fixed-Literal-Refactor. |
| Exact-Candidate-Dokumentations-Overlay | bestanden: Parent-Bilingual- und Repository-Pfad-Prüfungen sowie Framework-Dokumentations-Link-Prüfungen gegen eine wegwerfbare Parent-Kopie und ein Read-only-Archiv der Parent-gepinnten Framework-Revision. |

## Tests und tatsächliche Ergebnisse

Die fokussierte 17-Test-Suite ist No-Host-Source-Contract-Evidence. Ihr
hinzugefügter Contract prüft, dass beide Deklarationen bedingungslos und nicht
exportiert sind, allen ausgewählten Verwendungen vorausgehen und nach dem
Entfernen der Deklarationen die einzige Vorkommnis ihres jeweiligen Literals
bleiben. Außerdem bewahrt er das bestehende `set -eu`, die Cleanup-Traps, den
synchronisierten Client-Fehlerpfad, den Result-Failure-Check und alle acht
erwarteten Statusvergleiche.

Die Syntax- und scoped Whitespace-Ergebnisse sind ausschließlich lokale
statische Evidence. Sie führen keinen gepatchten Lighttpd-Host aus und
ersetzen keine zukünftige Exact-Head-SonarQube-Cloud-Analyse.

## Security-Auswirkung

Der ausgewählte Runner enthält Shell-Commands, HTTP-Requests, Diagnostik und
Lifecycle-Cleanup, doch dieser Record ändert diese Sicherheitsgrenze nicht.
Der Fixed-Literal-Refactor bewahrt das Invariant, dass `%{http_code}` und
`1,200p` bedingungslose, interne, nicht exportierte Werte sind, die nur als
quotierte Command-Argumente expandiert werden. Weder Caller-Environment,
Request, Response-Status noch Control-Daten können einen der Werte wählen.

Der unabhängige fokussierte Shell/HTTP-Review klassifizierte den Refactor als
`already_safe`. Er fand weder ein neues Security-Finding noch eine Änderung an
Requests, Status-Handling, Control-Flow, Cleanup oder fail-closed Verhalten.

## Runtime-Evidence

Es wurde keine reale gepatchte-Lighttpd-Host-Runtime ausgeführt. Die lokale
Suite liest und prüft Source-Contracts, ohne Lighttpd zu starten, ein Modul zu
laden oder einen Host-HTTP-Lifecycle auszuüben. Es wurde kein generierter
Report und keine Runtime-Evidence erzeugt oder geändert.

## Bekannte Einschränkungen

Die statische Source-Contract-Evidence kann Runtime-Verhalten auf einem realen
gepatchten Lighttpd-Host nicht beweisen. Exact-Candidate-Bilingual-,
Repository-Pfad- und Framework-Link-Validierung bestanden in einem
wegwerfbaren Overlay, das die Parent-gepinnte Framework-Revision verwendete,
ohne einen Framework-Checkout zu verändern. Für diesen Kandidaten existieren
noch keine Evidence zu Task-Delivery-Branch, Commit, Push, Pull Request,
Ready-for-review-Transition, Merge oder `master`.

## Verbleibende Risiken

Eine Exact-Head-External-Analyse ist weiterhin erforderlich, bevor eines der
Live-Baseline-SonarQube-Cloud-Items als abwesend oder extern geschlossen
beschrieben werden kann. Ein künftiger realer gepatchter-Lighttpd-Host-Run ist
weiterhin nötig, um Runtime-Evidence hinzuzufügen; die vorliegenden lokalen
Checks erheben diesen Claim bewusst nicht.

## Nicht ausgeführte Prüfungen mit Begründung

- Die reale gepatchte-Lighttpd-Host-Runtime wurde nicht ausgeführt. Sie
  benötigt die getrennten gepatchten Host-/Modulvoraussetzungen und liegt
  außerhalb dieses Literal-only-No-Host-Validierungsumfangs.
- `make check-doc-links` bleibt `not_run`: Es hängt von `check-framework` ab
  und würde das Framework materialisieren, was außerhalb des zugewiesenen
  Parent-Dokumentationsumfangs liegt. Seine zugrundeliegenden Parent-Bilingual-
  /Pfad- und Framework-Link-Prüfungen bestanden stattdessen im
  Exact-Candidate-wegwerfbaren Overlay mit dem Read-only-Archiv des
  Parent-gepinnten Frameworks.
- Es wurde kein Exact-Head-Hosted-Check und keine SonarQube-Cloud-Analyse
  ausgeführt, weil noch keine Evidence zu Task-Delivery-Branch, Commit, Push
  oder Pull Request existiert.

## Finaler Diff- und Review-Status

Dieser Record wird vor jeder Task-Delivery-Evidence geschrieben. Die
beobachtete lokale Runner/Test-Validierung und der fokussierte Shell/HTTP-
Review bestanden wie oben erfasst. Der Record behauptet nicht, dass
`AZ9cRynjHhV2CayPTPzV` oder `AZ9cRynjHhV2CayPTPzW` extern geschlossen ist,
und er behauptet keinen Branch-, Commit-, Push-, Pull-Request-,
Ready-for-review-, Merge- oder `master`-Status. Ausschließlich der scoped
Parent-Runner/Test und dieses bilinguale Traceability-/Index-Set liegen im
Umfang.
