# Change Record: Begrenzter Parent-CI-Matcher für bilinguale Design-Routen für SonarQube Cloud S8786

**Sprache:** [English](CR-20260729-sonar-ci-bilingual-route-regex.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-bilingual-route-regex` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` |
| Grenze | Ausschließlich Parent `ci/checks/documentation/check-bilingual-docs.py`, sein fokussierter Parent-Test, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine `scripts/`, kein Framework, kein MRTS, kein Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Aktueller `python:S8786`-Befund `AZ9gR-Icl6PyoRTCCRIu` bei `ci/checks/documentation/check-bilingual-docs.py:143`. |

## Motivation und Problemstellung

Der Route-Table-Matcher für die Common-Design-Notizen kombinierte benachbarte
Whitespace-Wildcards mit einem lazy Non-Delimiter-Capture. Eine fehlerhafte,
von einem Contributor gelieferte Markdown-Zeile, die mit einem Cell-Delimiter
und einer langen Folge von Leerzeichen beginnt, verursachte starkes Regex-
Backtracking, bevor der Checker die Zeile zurückweisen konnte. SonarQube Cloud
meldet diesen Ausdruck als `python:S8786`.

## Akzeptanzkriterien

- Eine fehlerhafte Route-Zeile ohne ihren schließenden Cell-Delimiter wird in
  begrenzter Zeit und ohne einen Backtracking-lastigen Ausdruck zurückgewiesen.
- Gepaddete und ungepaddete Connector-Cells erzeugen über die vorhandene
  `connector.strip()`-Operation weiterhin dieselben normalisierten Route-Keys.
- Die aktuellen englischen und deutschen Common-Design-Notizen behalten ihr
  gültiges Route-Ergebnis und ihre bestehenden Diagnosen.
- Ein zukünftiger exakter PR-Head meldet null neue SonarQube-Cloud-Issues,
  null neue duplizierte Zeilen und `0.0%` New-Code-Duplizierung, ohne Regel,
  Quality Gate, Exclusion, Suppression oder Validierungskontrolle zu schwächen.

## Implementierungsentscheidung und Begründung

Der Matcher konsumiert die erste Tabellen-Cell jetzt mit einem delimiter-
disjunkten `[^|]+`-Capture. Whitespace bleibt bewusst in diesem Capture, weil
die unmittelbar vorhandene `connector.strip()`-Operation bereits die
Normalisierung verantwortet. Damit verschwinden die überlappenden
Whitespace/Capture-Alternativen, während Route-Keys, Route-Werte,
Zeilenreihenfolge und Fehlermeldungen erhalten bleiben. Die fokussierte
Regression prüft beide gültigen Padding-Formen und eine fehlerhafte Zeile mit
1.024 Leerzeichen.

## Geänderte Dateien

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-bilingual-route-regex.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-bilingual-route-regex.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Isolierter Pre-Fix-Python-Regex-Probe mit `|` + 1.000 Leerzeichen + `x` | reproduziert: Der frühere Matcher benötigte `0.96952` Sekunden, während der delimiter-disjunkte Kandidat `0.000033` Sekunden benötigte. |
| `python -B -m unittest tests.test_bilingual_docs.BilingualDocumentationCheckerTests.test_common_design_note_current_contract_passes_for_both_languages tests.test_bilingual_docs.BilingualDocumentationCheckerTests.test_common_design_route_matcher_keeps_routes_and_rejects_malformed_spacing_quickly tests.test_bilingual_docs.BilingualDocumentationCheckerTests.test_common_design_note_rejects_scaffolded_status_and_current_sidecar_route` | bestanden: gültige englische/deutsche Notizen, gepaddete/ungepaddete Route-Keys, Zurückweisung der fehlerhaften Zeile und bestehende Negativdiagnosen. |
| `python -B -m unittest tests.test_bilingual_docs` | bestanden: 22 Tests. |
| Kontrafaktischer Matcher-Probe mit der 1.024-Leerzeichen-Regressions-Eingabe | reproduziert: Der frühere Ausdruck benötigte `1.064121` Sekunden und überschreitet das Regressionsbudget von `0.25` Sekunden. |
| Post-Fix-Matcher-Probe mit derselben fehlerhaften Zeile mit 1.000 Leerzeichen | bestanden: kein Match in `0.000039` Sekunden. |
| `make check-bilingual-docs` | blocked_external_dependency: Der isolierte Worktree enthält keinen Framework-Checkout; deshalb meldet der Checker ausschließlich bereits bestehende fehlende Framework-Link-Targets außerhalb dieser Task-Grenze. |
| `make check-doc-links` | blocked_external_dependency: Es meldet ausschließlich dieselben bereits bestehenden fehlenden Framework-Link-Targets. |
| `make lint` | blocked_external_dependency nach seinen CI-Shell-Syntax- und Python-Kompilierungsanteilen: Sein nächster No-CRS-Test importiert den fehlenden Framework-Checker. |
| Direkter `check_change_record_pair(...)`-Control für dieses Record | bestanden: keine Heading-, Identitäts- oder Language-Pair-Fehler. |
| `git diff --check` | bestanden: keine Whitespace-Fehler im finalen eingeschränkten Diff. |
| Fokussierter Security-Source-/Diff-Review | bestanden: Der Base-Resource-Exhaustion-Pfad ist durch den delimiter-disjunkten Matcher geschlossen; kein reportabler Current-Diff-Candidate. |

## Security-Auswirkung

Die relevante Eingabe ist eine Dokumentationszeile aus einer Parent-Änderung;
der betroffene Sink ist CI-CPU-Zeit während der Validierung dieser Zeile. Die
Invariante lautet, dass eine ungültige Zeile ohne eine Mehrdeutigkeit, die
exzessives Backtracking ermöglicht, zurückgewiesen wird, während gültige
Selected-Route-Zeilen ihre normalisierten Keys behalten. Der neue delimiter-
disjunkte Ausdruck schließt diesen Performance-Pfad und ergänzt eine
Same-Boundary-Regression für fehlerhafte Eingaben sowie eine legitime
Control für gepaddete/ungepaddete Zeilen. Es ändern sich keine File-Paths,
Netzwerk-, Subprocess-, Authentifizierungs-, Secret- oder Report-Output-
Verhalten.

## Runtime-Evidence

Es wird keine Connector-Runtime, keine netzwerkgestützte Komponenten-
Vorbereitung, keine Package-Installation und keine Host-Matrix beansprucht.
Die geänderte Grenze ist der In-Process-Checker für bilinguale Dokumentation
und wird direkt durch sein fokussiertes Unit-Modul ausgeübt.

## Bekannte Einschränkungen

Die Regression verwendet eine deterministische fehlerhafte Zeile mit 1.024
Leerzeichen statt eines unbeschränkten Korpus. Sie beweist, dass der gemeldete
Overlapping-Quantifier-Shape nicht im Route-Matcher verwendet wird, ist aber
keine allgemeine Performance-Zertifizierung für jeden regulären Ausdruck des
Checkers.

Während der breiten Make-Checks erfüllte ein lesbares externes
`FRAMEWORK_ROOT` die Make-Voraussetzung, aber der isolierte Worktree selbst
enthält absichtlich keinen Framework-Gitlink-Checkout. Der Parent-Link-Checker
meldet deshalb fehlende worktree-relative Framework-Targets, und ein No-CRS-
Test importiert später den fehlenden worktree-relativen Framework-Checker.
Diese Fehler liegen außerhalb dieser Matcher-Änderung.

## Verbleibende Risiken

Der exakte Hosted-PR-Head muss noch eine frische SonarQube-Cloud-Analyse
erhalten, die den ausgewählten Befund als abwesend sowie null New-Code-Issues/
Duplikate ausweist. Der isolierte Worktree kann den repositoryweiten
Documentation-Checker erst ausführen, wenn der read-only Framework-Checkout
am erwarteten Gitlink verfügbar ist.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Connector-Build, keine Runtime-Matrix, kein Package-Download und keine
  netzwerkgestützte Komponenten-Vorbereitung: Keine davon wird durch diese
  Documentation-Regex-Änderung erreicht.
- Kein Framework, MRTS, Gitlink, `.github/`, `scripts/` oder unverbundene
  Parent-Source wurde geändert oder getestet, weil dies außerhalb der
  ausgewählten Remediation-Grenze liegt.
- Hosted-SonarQube-Cloud-, GitHub-Actions-, Review- und Merge-Evidence
  benötigen den späteren exakten PR-Head und werden nicht lokal hergeleitet.

## Finaler Diff- und Review-Status

Der eingeschränkte lokale Diff besteht nur aus Matcher, fokussierter Regression
und diesem bilingualen Traceability-Paar/den Indizes. Whitespace-, Change-
Record-Struktur- und fokussierte Security-/Diff-Reviews bestanden. Es werden
kein Commit, Push, Pull Request, Hosted-Check, Review oder Merge beansprucht.
Exact-Head-Delivery-Evidence bleibt erforderlich, bevor diese Task
`verified_pr` erreichen kann.
