# Change Record: Parent-CI-No-CRS-Missing-Case-Diagnostikliteral-Deduplizierung für SonarQube Cloud S1192

**Sprache:** [English](CR-20260730-sonar-ci-no-crs-diagnostic-literal.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260730-sonar-ci-no-crs-diagnostic-literal |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f |
| Tracking | Parent-SonarQube-Cloud-Issue `AZ9cRycZHhV2CayPTPw4`, `shelldre:S1192`, OPEN, MINOR: ein Owner für `FAIL: capability-selected No-CRS runner cases are missing`, das zuvor fünfmal in `ci/runtime/lifecycle/run-connector-stage.sh` wiederholt war. Die aktuelle Master-Analyse vom `2026-07-30T02:04:34+0000` ist an diese Basis-Revision gebunden. |
| Grenze | Parent `ci/runtime/lifecycle/run-connector-stage.sh`, sein direkter Parent-Test, dieses englisch/deutsche Change-Record-Paar und seine additiven Indexeinträge. `.github`, `scripts`, Framework, MRTS, Gitlinks, Connector-Quellen, SonarQube-Cloud-Konfiguration, Suppressions, Quality Gates, externer Issue-Status, Push, Pull Request und Merge sind zum Zeitpunkt der Record-Erstellung unverändert. |

## Motivation und Problemstellung

Die fünf generischen No-CRS-Zweige geben dieselbe Missing-Selected-Cases-
Diagnose aus. Der SonarQube-Cloud-Befund ist ein echtes
Maintainability-Duplikat, doch diese Diagnosen stehen neben
Evidence-Integrity-Kontrollen: Ein generischer No-CRS-Lauf muss vor dem
Dispatch stoppen, wenn seine kanonische Selected-Case-Liste fehlt. Der
Refaktor darf daher nicht den Guard selbst zentralisieren, verschieben oder
abschwächen.

## Akzeptanzkriterien

- Die fünf doppelten Diagnostikliterale durch einen statischen Shell-Owner
  ersetzen.
- Jeden vorhandenen `[ -n "${NO_CRS_SELECTED_CASES:-}" ]`-Guard, die
  stderr-Umleitung, den Exit-Status `1` und das generische Dispatch-Target
  erhalten.
- Den Full-Lifecycle-Pfad erhalten, der sein natives Target ohne die generische
  Selected-Case-Liste wählen muss.
- Hermetische Regressionsabdeckung für alle generischen Connector-Routen ohne
  Selected Cases sowie je einen generischen und einen Full-Lifecycle-legitimen
  Control hinzufügen.
- Anwendbare Shell-Syntax, direkte Parent-Tests, Whitespace-Review und direkte
  Bilingual-Dokumentationsvalidierung bestehen, ohne Scanner-Policy zu ändern;
  Repository-Dokumentationschecks, die nur durch den nicht initialisierten
  Framework-Gitlink blockiert sind, festhalten.
- Den SonarQube-Cloud-Issue erst nach einer frischen Analyse eines exakten
  ausgelieferten PR-Heads als behoben bezeichnen.

## Implementierungsentscheidung und Begründung

`NO_CRS_SELECTED_CASES_MISSING_MESSAGE` wird einmal als readonly statischer
Shell-Wert gesetzt. Jeder vorhandene fehlschlagende Zweig führt weiterhin
seinen eigenen Non-Empty-Test aus und schreibt danach denselben Wert auf stderr
vor `exit 1`. Der Refaktor extrahiert keinen Helper und verschiebt keinen Guard
über die Trennung zwischen generic und full_lifecycle.

Der direkte Test erzeugt nur einen temporären Framework-Presence-Marker und
ein temporäres Target-Recorder-Skript. Er ruft den echten Dispatcher auf, ohne
Framework oder eine Connector-Runtime zu initialisieren. Der Test beweist, dass
sechs Missing-Case-Routen `1` mit der exakten stderr-Diagnose zurückgeben,
eine generische Envoy-Route für einen Selected Case `no-crs-baseline-envoy`
erreicht und die Full-Lifecycle-Envoy-Route ohne Selected Case
`runtime-smoke-envoy-ext-proc` erreicht.

## Geänderte Dateien

- ci/runtime/lifecycle/run-connector-stage.sh
- tests/test_no_crs_selected_runner_wiring.py
- reports/audits/change-records/CR-20260730-sonar-ci-no-crs-diagnostic-literal.md
- reports/audits/change-records/CR-20260730-sonar-ci-no-crs-diagnostic-literal.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

- `sh -n ci/runtime/lifecycle/run-connector-stage.sh`
- `shellcheck --severity=error ci/runtime/lifecycle/run-connector-stage.sh`
- `/root/git/ModSecurity-conector/.venv/bin/python -m pip check`
- `/root/git/ModSecurity-conector/.venv/bin/python -m py_compile tests/test_no_crs_selected_runner_wiring.py`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_no_crs_selected_runner_wiring.NoCrsSelectedRunnerWiringTest.test_stage_rejects_missing_selected_cases_and_preserves_dispatch_controls`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_no_crs_selected_runner_wiring.NoCrsSelectedRunnerWiringTest.test_remaining_connectors_keep_compatibility_and_native_targets_distinct`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_no_crs_selected_runner_wiring`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_bilingual_docs`
- `make check-bilingual-docs`
- `make check-doc-links`
- `git diff --check`

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| POSIX-Shell-Parsing | bestanden: `sh -n` endete 0 für den geänderten Dispatcher. |
| ShellCheck-Error-Level | bestanden: `shellcheck --severity=error` fand keinen Fehler auf Error-Level. Der uneingeschränkte Befehl meldet weiterhin nur die vorhandenen Nicht-Error-Hinweise SC1007/SC2016 an unveränderten Zeilen 7, 162 und 185. |
| Python-Environment-Integrität | bestanden: `pip check` meldete keine defekten Requirements, und der geänderte Test kompilierte. |
| Neue hermetische Dispatch-Regression | bestanden: ein Test deckt sechs generische Missing-Case-Routen, einen generischen Selected-Case-Control und einen Full-Lifecycle-Native-Target-Control über den echten Dispatcher ab. |
| Bestehender Target-Separation-Control | bestanden: der direkte Wiring-Test erhält die Trennung zwischen Native-/Compatibility-Targets und das Diagnostikliteral. |
| Vollständiges direktes Testmodul | blocked external dependency: Es lief mit sieben Tests und endete 1 ausschließlich wegen zwei Apache-Fixture-Subtests, die den nicht initialisierten read-only-Framework-Gitlink benötigen (`git submodule status` beginnt mit `-`). Die neue Regression und der Target-Separation-Control bestanden separat; C12 initialisierte oder änderte Framework nicht, um die Bedingung zu umgehen. |
| Direkter Bilingual-Dokumentationstest | bestanden: `tests.test_bilingual_docs` lief mit 21 Tests erfolgreich. |
| Repository-Dokumentationschecks | blocked external dependency: `make check-bilingual-docs` und `make check-doc-links` stoppten ausschließlich bei unveränderten fehlenden Targets unter dem bewusst nicht initialisierten Framework-Gitlink (jeweils 20 beziehungsweise 16 Diagnosen); ihre Ausgabe nennt keinen C12-Change-Record-, Test- oder Quellpfad. |
| Whitespace | bestanden: das finale `git diff --check` meldete nach allen C12-Dokumentationsupdates keinen Fehler. |

## Security-Auswirkung

Dies ist sicherheitsrelevante CI-Evidence-Integrity-Wartung, keine Behebung
eines Security-Findings. Kontrollierte Connector-/Stage-Argumente und
No-CRS-Environment-Werte behalten ihre vorhandenen Allowlists und den
fail-closed generischen Guard. Die nächsten Sinks bleiben der gequotete
generische Framework-Smoke-Handoff und die Remaining-Connector-Target-
Invocation. Ein defekter Refaktor könnte eine leere Auswahl einen
unbeabsichtigten Smoke-Pfad erreichen lassen oder einen gültigen nativen
Full-Lifecycle-Pfad blockieren; die hinzugefügten hermetischen negativen und
legitimen Controls decken beide Risiken ab. Keine Änderung an Command-
Konstruktion, Pfadkontrolle, Credential-Handling oder CI-Berechtigungen.

## Dokumentationsstatus

Dieses vollständige englisch/deutsche Change-Record-Paar ist die einzige
benutzergerichtete Dokumentationsänderung. Keine generierte Dokumentation und
kein Report änderten sich. Der direkte Check `tests.test_bilingual_docs` lief
mit 21 Tests erfolgreich. Die Repository-Make-Targets sind nur durch
unveränderte fehlende Targets unter dem bewusst nicht initialisierten
Framework-Gitlink blockiert: `make check-bilingual-docs` meldete 20 und
`make check-doc-links` 16 Diagnosen, keine für einen C12-Pfad.

## Runtime-Evidence

Kein Connector-Build, keine Framework-Initialisierung, keine vollständige
Lifecycle-Matrix und keine Report-produzierende Runtime-Ausführung fanden
statt. Der hermetische Test prüft nur den Dispatch-Vertrag und ist keine
Evidence eines echten Connector-Lifecycles.

## Nicht ausgeführte Prüfungen mit Begründung

- `shfmt -d` wurde nicht ausgeführt, weil `shfmt` nicht verfügbar ist; keine
  automatische Formatierung wurde versucht.
- Eine vollständige Connector-/Runtime-Matrix wurde nicht ausgeführt, weil sie
  externe Komponentenquellen benötigt und Runtime-Artefakte erzeugt, die für
  diesen einen Diagnostik-Owner-Refaktor nicht relevant sind.
- Zum Zeitpunkt der Record-Erstellung existierten für diesen uncommitteten
  Kandidaten noch keine gehosteten GitHub Actions, SonarQube-Cloud-PR-Analyse,
  Reviews, Commits, Pushes, Pull Requests oder Merges.

## Bekannte Einschränkungen

Das vollständige direkte Testmodul ist durch die Apache-Fixtures des bewusst
nicht initialisierten Framework-Gitlinks blockiert. Die Aufgabe erhält diese
Grenze und verwendet den unabhängigen hermetischen Test statt Framework-Inhalt
zu erzeugen oder zu ändern. Zum Zeitpunkt der Record-Erstellung hatte
SonarQube Cloud den Kandidaten-Head noch nicht analysiert.

## Verbleibende Risiken

Nur ein statischer Diagnostik-Owner änderte sich, doch das Verschieben eines
generischen Guards oder seine Anwendung auf Full-Lifecycle-Pfade wäre eine
Verhaltensregression. Zum Zeitpunkt der Record-Erstellung blieben finales
Diff-Review, Exact-Head-Hosted-Checks und eine frische SonarQube-Cloud-Analyse
erforderlich, bevor der Issue als behoben gelten konnte.

## Finaler Diff- und Review-Status

Zum Zeitpunkt der Record-Erstellung enthielt der Task-Worktree nur die
abgegrenzte Parent-Shell/Test-Änderung und sein erforderliches bilinguales
Traceability-Material. Parent `master`, Framework, MRTS, Gitlinks,
Scanner-Kontrollen und Hosted-Delivery-Status waren unverändert.
