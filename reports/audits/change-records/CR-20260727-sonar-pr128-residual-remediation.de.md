# Change Record: Parent-PR #128 Rest-SonarQube-Cloud- und Workflow-Remediation

**Sprache:** [English](CR-20260727-sonar-pr128-residual-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-pr128-residual-remediation |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-PR-#128-Follow-up für SonarQube Cloud `python:S5843` AZ-jvTOkjjNxyah3ylvp, `python:S1192` AZ-jvTBTjjNxyah3ylvn, `python:S1172` AZ-jvTPajjNxyah3ylvq und `python:S1481` AZ-jvTJijjNxyah3ylvo; zusätzlich der Parent-Change-Record-Vertrag, durch den die PR- und Push-Lint-Workflows fehlschlugen. |
| Grenze | Ausschließlich Parent-Python-Quelltext, Parent-Tests, Parent-Change-Records und PR #128. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, Connector-/Runtime-Verhalten und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Problemstellung

Die exakte SonarQube-Cloud-Abfrage für PR #128 meldete vier neue Code-Smell-
Zeilen. Derselbe Kandidat ließ den Parent-Lint-Workflow fehlschlagen, weil
sieben neu hinzugefügten Change-Record-Paaren die vom Repository verlangten
Überschriften fehlten. Die Korrektur muss die lokalen Code- und
Dokumentationsursachen entfernen, ohne Scanner, Test, Workflow oder
Repository-Grenze zu schwächen.

## Akzeptanzkriterien

- Das Variable-Matching der Repository-Organisation bewahren und zugleich den
  hochkomplexen regulären Ausdruck durch begrenzte Komponenten-Patterns
  ersetzen.
- Den englischen/deutschen Markdown-Suffixen jeweils einen statischen Owner
  geben und die Gegenstück-Konstruktion sowie das Link-Validierungsverhalten
  bewahren.
- Nur das ungenutzte Compiler-Guide-Dispatcher-Argument und das ungenutzte
  Native-Comparison-Lokal entfernen, während die unterstützte CLI-Option
  `--build-root` erhalten bleibt.
- Alle sieben betroffenen Change-Record-Paare in den erforderlichen
  bilingualen Überschriftenvertrag überführen und dabei wahrheitsgemäße
  Delivery- und Validierungsgrenzen festhalten.
- Fokussierte Parent-Tests und Whitespace-Review bestehen lassen, soweit der
  uninitialisierte Framework-Gitlink den Check nicht verhindert; keinen
  gehosteten Sonar- oder GitHub-Workflow-Erfolg vor Beobachtung für den
  ausgelieferten Head behaupten.

## Implementierungsentscheidung und Begründung

`variable_matches()` führt zwei einfache kompilierte Patterns in Quellreihenfolge
zusammen und bewahrt das frühere linksstehende, nicht überlappende
Match-Verhalten des Scanners. Der Dokumentationschecker besitzt jetzt beide
Suffix-Konstanten, statt das deutsche Suffix zu wiederholen.
`validation_section()` erhält nur noch die gelesenen Werte, und der
Native-Comparison-Runner entfernt nur seine tote lokale Zuweisung; sein Parser
akzeptiert weiterhin `--build-root`, weil vorhandene Make-Targets diese Option
übergeben.

Die bestehenden Change Records behalten ihre faktische ursprüngliche Evidence
und erhalten die kanonischen Abschnittsüberschriften plus explizite
Statusgrenzen. Dieser Record deckt die vier neuen PR-Zeilen und ihre
Workflow-Reparatur ab; eine Framework- oder MRTS-Änderung ist nicht nötig.

## Geänderte Dateien

- scripts/generate_repository_organization_inventory.py
- tests/test_repository_organization_inventory.py
- ci/checks/documentation/check-bilingual-docs.py
- scripts/generate_compiler_guides.py
- ci/runtime/lifecycle/run-native-case-comparison.py
- sieben bestehende englische/deutsche `CR-20260727-sonar-*`-Change-Record-Paare
  mit erforderlichen kanonischen Überschriften
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Fokussierte Kommandos verwenden Parent-.venv-Python mit
`PYTHONDONTWRITEBYTECODE=1` und `PYTHONNOUSERSITE=1`:

- rtk proxy env ... `<Parent .venv python>` -B -m unittest -v tests.test_repository_organization_inventory tests.test_bilingual_docs tests.test_compiler_guides tests.test_runtime_env_snapshot_contract
- rtk proxy env ... `<Parent .venv python>` -B ci/checks/documentation/check-bilingual-docs.py
- rtk proxy git diff --check

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussierte Inventory-, bilinguale Dokumentations- und Compiler-Guide-Module | bestanden: 38 Tests. |
| Fokussierter Native-Comparison-Reduced-Context-Test | bestanden: `test_native_summary_and_mismatch_helpers_keep_outputs_with_reduced_context_parameters`. |
| Kombiniertes Runtime-Environment-Modul | blocked_environment: Ein ansonsten unabhängiger Test fand die bewusst uninitialisierte `modules/ModSecurity-test-Framework/ci/lib/common.sh` nicht; der direkte Native-Comparison-Test bestand. |
| Vollständiger bilingualer Dokumentationschecker | blocked_environment: 20 vorhandene fehlende Framework-Gitlink-Linkziele; er meldete keine fehlende Change-Record-Section für ein repariertes Paar. |
| `git diff --check` | bestanden: kein Whitespace-Fehler. |
| Veröffentlichter Remediation-Commit `b09588c63b21be2e62fe374b15f63980e6d6293d` | bestanden: Sein lokaler Branch, der `origin`-Branch und der PR-#128-Head wurden als gleich beobachtet; alle sichtbaren GitHub-PR-Checks bestanden. |
| SonarQube-Cloud-Analyse für den veröffentlichten Remediation-Commit `b09588c63b21be2e62fe374b15f63980e6d6293d` | bestanden: Quality Gate bestanden mit 0 New issues, 0 Security Hotspots und 0,0 % Duplication on New Code; die PR-Issue-Abfrage lieferte 0 ungelöste Zeilen. |

## Security-Auswirkung

Die fokussierte Bewertung ergab keinen validierten Sicherheitsbefund. Der
Regex-Scanner verarbeitet Repository-Text; daher sind begrenztes Matching und
die bestehende Regressionsmenge wichtig. Der Ersatz erweitert jedoch weder eine
Trust-Boundary noch ändert er einen Sink. Die übrigen Änderungen entfernen nur
toten oder ungenutzten Code beziehungsweise reparieren die
Dokumentationsstruktur. Kein Sicherheitscontrol, Scanner, Quality Gate,
Suppression, keine Authentifizierung, kein Pfad-Guard, Connector oder
Runtime-Verhalten wird geschwächt.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll- oder Produktions-Runtime-Verhalten
geändert oder behauptet. Die Tests prüfen ausschließlich Source- und
Dokumentationsverträge; sie sind keine Runtime-Evidence.

## Bekannte Einschränkungen

Der Parent-Task-Worktree besitzt bewusst keinen initialisierten
Framework-Gitlink. Deshalb können der vollständige Dokumentationschecker und
ein unabhängiger Runtime-Environment-Test lokal nicht vollständig laufen. Für
den oben genannten veröffentlichten Remediation-Commit liegt gehostete
PR-Evidence vor; diese historische Evidence ersetzt keine frischen Checks für
einen späteren Kandidaten-Head oder für Parent-`master`.

## Verbleibende Risiken

Das Aufteilen des Variable-Matchers könnte versehentlich eine Randform
auslassen. Die fokussierte Inventory-Regression-Suite einschließlich eines
Assignment-Overlap-Falls mindert dieses Risiko; der veröffentlichte
Remediation-Commit erhielt außerdem die oben genannten gehosteten PR-Checks
und die Sonar-Analyse. Jeder spätere Kandidaten-Head benötigt weiterhin seine
eigene Exact-Head-Verifikation.

## Nicht ausgeführte Prüfungen mit Begründung

- Der vollständige `make quick-check` und Framework-abhängige Aggregate-Checks
  werden lokal nicht ausgeführt, weil der uninitialisierte Framework-Gitlink
  bereits ihre gemeinsame Dokumentationsvoraussetzung blockiert.
- Connector-Builds, Runtime-Smokes, Protokollmatrizen, Framework-Checks und
  MRTS-Checks sind nicht anwendbar: Es änderte sich keine Connector-/Runtime-
  Implementierung und kein Cross-Repository-Inhalt.
- Es wird hier kein Connector-/Runtime-Workflow, kein späteres PR-Head-Ergebnis
  und kein Parent-`master`-Ergebnis behauptet. Die beobachteten gehosteten
  Ergebnisse gelten nur für den oben identifizierten veröffentlichten
  Remediation-Commit.

## Finaler Diff- und Review-Status

Der lokale Pre-Commit-Diff-Review zeigte nur die aufgeführten Parent-Source-,
Test- und Traceability-Änderungen und keinen Whitespace-Fehler. Sein Status
„uncommittet“ ist eine historische Momentaufnahme: Der Remediation-Commit
`b09588c63b21be2e62fe374b15f63980e6d6293d` wurde anschließend auf
`agent/sonar-1125-20260727` veröffentlicht, und die lokalen, `origin`- sowie
GitHub-PR-#128-Heads wurden zu diesem Zeitpunkt als gleich beobachtet. Die
GitHub-PR-Checks und das SonarQube-Cloud-Ergebnis bestanden anschließend wie
oben festgehalten. Dieser Record behauptet keinen späteren
Dokumentations-only-Kandidaten-Head, keinen Master-Merge und keine
Parent-`master`-Checks; jeder dieser Zustände benötigt separat beobachtete
Exact-Head-Evidence.
