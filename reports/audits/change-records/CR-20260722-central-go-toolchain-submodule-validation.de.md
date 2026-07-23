# Change Record: Zentralisierte Go-Toolchain und Update-Submodules-Validierungsreparatur

**Sprache:** [English](CR-20260722-central-go-toolchain-submodule-validation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260722-central-go-toolchain-submodule-validation |
| Datum (UTC) | 2026-07-22 |
| Basis-Revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Grenze | Nur Parent-CI/Tooling, Parent-Tests, gepaarte Parent-Dokumentation und dieses Change-Record-Paar. Framework-Source, MRTS, Parent-Gitlink, Go-Module, Abhängigkeiten und Action-Pins bleiben unverändert. |
| Finding-Verknüpfung | FND-PARENT-0045: validierter Parent-CI-Kompatibilitätsblocker für die fehlschlagende Update-submodules-Candidate-Validierung; FND-SONAR-0011: 23 task-owned nicht gate-blockierende SonarQube-Cloud-Test-Maintainability-Beobachtungen. |
| Delivery-Status | Der historische initiale Draft-PR-#90-Head `0acba7768848651758610928e89f4481dbb90c81` scheiterte in fünf gewöhnlichen Push-Workflows an der veralteten Parent-HAProxy-Erwartung. Sein späterer exakter Head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf` bestand die beobachteten gewöhnlichen Checks und das SonarQube-Cloud-Quality-Gate. Die aktuell nutzerautorisierte Sonar-Bereinigung ist lokal validiert, aber noch nicht committed oder gepusht; für diese Fortsetzung wird daher kein frischer Hosted-Erfolg, Review- oder Master-Integrationserfolg behauptet. |

## Motivation und Problemstellung

Der Nutzer bat um einen Ersatz für den veralteten PR 80, der Go wie Python
zentral selektiert, sicher auf ein neueres Go-Release prüft und die aktuell
fehlschlagende Update-submodules-Validierung repariert. Die alte Parent-
HAProxy-Fixture widersprach dem aktuellen Framework-BUILD_ROOT-Containment-
Control und blockierte einen ansonsten erfolgreich aufgelösten Framework-
Candidate.

## Akzeptanzkriterien

- Ein exakter eingecheckter Go-CI-Selector steuert beide gewöhnlichen
  CodeQL-Go-Jobs.
- Der Updater schlägt nur einen neueren stabilen Patch der vorhandenen
  1.26-Serie vor.
- Der Updater lässt Moduldeklarationen und Dependency-Dateien unverändert.
- Die Update-submodules-Regression bewahrt sowohl legitimen Cache-Reuse als
  auch die Rejection für getrenntes BUILD_ROOT, wenn die ausgewählte
  Framework-Revision diesen Containment-Control bereitstellt.
- Lokale statische und fokussierte Test-Evidence wird wahrheitsgemäß erfasst;
  Exact-Head-Hosted-Validierung bleibt eine getrennte Voraussetzung.

## Implementierungsentscheidung und Begründung

Die Root-<code>.go-version</code> ist die eine exakte Go-CI-Toolchain-
Autorität, initial <code>1.26.5</code>. Die zwei CodeQL-Go-Jobs konsumieren
sie über die unveränderliche setup-go-Action mit
<code>go-version-file: .go-version</code> und
<code>check-latest: false</code>. Sie ersetzt keine modul-eigenen
<code>go.mod</code>-Sprachdirektiven; kein Modul, <code>go.sum</code>, keine
Abhängigkeit und keine <code>toolchain</code>-Direktive wird geändert.

Der Go-Updater akzeptiert nur den offiziellen exakten Go-Release-Endpoint. Er
weist Redirects, Nicht-JSON, fehlerhafte, zu große, duplicate-key,
Prerelease-, Cross-Minor-, Leading-zero-, Downgrade- und unsichere-Target-
Bedingungen zurück. Seine einzige Schreiboperation ist ein atomisches Update
der regulären Root-<code>.go-version</code>, nachdem ein unabhängig erwarteter
höherer <code>1.26.N</code>-Patch bestätigt ist.

Der Workflow trennt einen read-only-Resolver auf dem Default-Branch, einen
read-only-Candidate-Validator und den einzigen engen Writer. Candidate-
Modulbefehle verwenden <code>GOTOOLCHAIN=local</code> und readonly-Modulflags.
Der Publisher kann nur einen Draft PR sicher erstellen oder aktualisieren,
dessen Merge-Base-Diff allein <code>.go-version</code> enthält; es gibt keinen
direkten Master-Write-, Force-Push-, Auto-Merge-, Submodule-
Initialisierungs- oder Modulupdate-Pfad.

## Geänderte Dateien

- Root-Go-Selector, Go-Updater, Go-Static-Contract und fokussierte
  Updater-Tests.
- CodeQL-Go-Selectoren und der neue dreistufige Go-Updater-Workflow.
- Python-Workflow-Inventar- und Contract-Tests, weil der Go-Updater den
  begrenzten eingecheckten Python-Parser unter dem vorhandenen Interpreter-
  Vertrag ausführt.
- Parent-HAProxy-Cache-Regressionstests, gepaarte Dokumentation,
  Change-Record-Indizes und dieses bilinguale Change-Record-Paar.
- Die aktuelle Drei-Test-Sonar-Bereinigung: nur Assertion-Diagnosereihenfolge
  und eine Prerelease-Fixture außerhalb ihrer erwarteten Exception-Assertion.

Keine Framework-Source, kein MRTS-Inhalt, Parent-Gitlink, Go-Modul, Go-
Checksum, Dependency, Action-Pin oder Security-Tools-Lock-Datei wird geändert.

## Update-Submodules-Grundursache und Korrektur

GitHub-Actions-Run
[29945542984](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29945542984)
löste Framework-Candidate f73f8842f45318e2df8aff1d31855eeb7c20a22f auf und
scheiterte danach in drei Parent-HAProxy-Cache-Tests während seines read-only
quick check. Der Candidate weist HAPROXY-Runtime-Pfade außerhalb von
BUILD_ROOT korrekt zurück; seine eigene Sicherheitsregression verlangt diese
Sperre. Die fehlschlagende Parent-Fixture legte stattdessen ein Runtime-
Binärprogramm in den Shared Cache und setzte BUILD_ROOT unabhängig.

Der direkte Parent-Test modelliert jetzt das legitime produktive Layout, bei
dem der effektive Managed-Connector-Entry zugleich BUILD_ROOT ist. Sein
expliziter Negativ-Control verlangt Exit 77 von einer Framework-Source, die
den strikten Split-Root-Containment-Vertrag bereitstellt. Der bekannte aktuelle
Parent-Gitlink `784977615acfc55567e37b863309abc4a38ac877` datiert vor diesem
Vertrag und wird transparent übersprungen; jede andere ausgewählte Revision,
der der Vertrag fehlt, schlägt fehl. Der Update-submodules-Candidate führt den
Exit-77-Control somit aus, ohne dass gewöhnliche Parent-PR-Checks die ältere
gepinnte Framework-Revision fälschlich als Parent-Regression klassifizieren.
Der Test akzeptiert für lokale Evidence bewusst eine übergebene read-only-
Framework-Source, ohne den Parent-Gitlink zu initialisieren oder zu verändern.
Der Workflow bleibt Resolve, dann read-only-Validierung, dann enger Publisher;
kein Berechtigungs-, Trigger-, Workflow- oder Framework-Source-Change umgeht
den Fehler.

## Ausgeführte Befehle

- Die fokussierte Suite mit der geprüften read-only-Framework-Root führte 61
  Tests aus und endete mit Exit 0: Go-Updater/-Contract, Python-Workflow-
  Contract, CI-Security und Parent-Runtime-Component-Regressionen bestanden.
- `make check-go-version-contract check-python-version-contract
  check-ci-security-contract` endete mit Exit 0; der Python-Contract meldete
  Python 3.14.6 und 28 Python-ausführende Workflow-Jobs, und 16 CI-Security-
  Tests bestanden.
- `tests.test_bilingual_docs` führte 11 Tests aus und endete mit Exit 0. Der
  finale fokussierte Security-Diff-Review ist eine getrennte erforderliche
  Staging-Voraussetzung für dieses finale Drei-Dateien-Follow-up.
- `git diff --check` bestand im finalen lokalen Review; es wird als
  Staging-Voraussetzung erneut ausgeführt.
- Der initiale Draft-PR-#90-Head
  `0acba7768848651758610928e89f4481dbb90c81` löste die abgeschlossenen
  Push-Runs [29955277020](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277020),
  [29955277057](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277057),
  [29955276989](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955276989),
  [29955277045](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277045)
  und [29955277071](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277071)
  aus. Jeder scheiterte an derselben Legacy-Test-Assertion: erwartet wurde Exit
  77, beobachtet Exit 0 aus dem Managed-Cache-Reuse-Verhalten des alten Gitlinks.
  Dies ist Failure-Evidence für den initialen Head, kein Hosted-Delivery-Erfolg.

Die obigen historischen Initial-Head-Fehlschläge bleiben Failure-Evidence. Der
spätere exakte Head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf` bestand getrennt
seine beobachteten gewöhnlichen Checks und das SonarQube-Cloud-Quality-Gate.
Die aktuelle lokale Sonar-Bereinigung hat noch keinen neuen exakten PR-Head
erzeugt und damit noch kein neues Hosted-Delivery-Ergebnis.

## Runtime-Evidence

Nicht anwendbar. Die Änderung betrifft CI-Toolchain-Selection und einen
Parent-Provisioning-Testvertrag; sie startet keinen Connector und etabliert
keinen Connector-Protokoll- oder Runtime-Claim.

## Bekannte Einschränkungen

Die lokale Go-Executable ist älter als 1.26.5 und kann daher die Candidate-
Modulausführung mit dem angeforderten Patch nicht belegen. Candidate-Hosted-
Validierung ist die erforderliche Exact-Toolchain-Evidence. Das vollständige
Documentation-Target hängt außerdem vom absichtlich nicht initialisierten
Framework-Gitlink ab. `Update submodules` ist ein Default-Branch-Schedule-/
Manual-Workflow; das Follow-up benötigt daher nach den normalen PR-Checks
seine eigene frische Hosted-Candidate-Validierung.

## Verbleibende Risiken

Ein neuerer Go-Patch kann Modul- oder Runner-Kompatibilitätsunterschiede
offenlegen, die lokale statische Evidence nicht beweisen kann. Der enge
Updater vermeidet eine direkte Default-Branch-Mutation, doch Exact-Head-
Hosted-Candidate-Validierung, Review und normale PR-Delivery bleiben nötig.
Kein Risiko wird akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

- Exakte Go-1.26.5-Modulvalidierung auf GitHub-hosted Runners ist bis zu einem
  task-eigenen Candidate-Head ausstehend. Die installierte lokale Executable
  ist Go 1.26.0, daher weisen `GOTOOLCHAIN=local go test ./...` und `go vet
  ./...` in beiden tatsächlichen Modul-Roots die benötigte 1.26.5 vor jeder
  Ausführung oder jedem Download zurück.
- Ein frischer Sonar-Bereinigungs-Commit und seine Exact-Head-gewöhnliche CI,
  CodeQL-, Review-, SonarQube-Cloud- und Resulting-Master-Evidence existieren
  noch nicht. Der `Update submodules`-Workflow ist aktuell nicht durch Branch
  Protection erforderlich, aber seine dokumentierte Task-Akzeptanzanforderung
  muss vor dem Merge erneut bewertet werden.
- Die vollständige Documentation-Link-Validierung endete ausschließlich für
  Ziele unter dem absichtlich nicht initialisierten Framework-Gitlink mit Exit
  2; sie darf nicht durch eine Framework- oder MRTS-Änderung aus diesem
  Parent-Task grün gemacht werden.

## Finaler Diff- und Review-Status

Der lokale Follow-up-Diff hat fokussierte Static-, Regressions-, Bilingual- und
Security-Diff-Coverage. Der Scope enthält keine Framework-Source, kein MRTS,
keinen Parent-Gitlink, kein Go-Modul, keine Dependency- oder Action-Pin-
Änderung. Vor dem Staging sind der dokumentierte Status-/Diff-Review und der
Delivery-Preflight erforderlich. Für die uncommittete Sonar-Bereinigung ist
kein aktueller Hosted-Erfolg impliziert.

## Fortsetzung 2026-07-23: Sonar-Bereinigung und Vorbereitung der geschützten Integration

Der Nutzer autorisierte ausdrücklich die Behebung der 23 aktuellen
SonarQube-Cloud-PR-#90-Beobachtungen und die geschützte Parent-Master-
Integration. Die lokale Änderung dreht nur die 22 durch `python:S3415`
markierten `unittest.TestCase.assertEqual`-Operand-Reihenfolgen um und
verschiebt die unveränderte `release("go1.26.6rc1")`-Fixture aus dem durch
`python:S5778` markierten `assertRaises(MetadataError)`-Kontext. Sie ändert
weder Produkt-/Runtime-Code, Workflow-Berechtigungen, Action-Pins,
Sonar-Konfiguration, Exclusions, Suppressions, False-Positive-Disposition noch
Risikoakzeptanz.

Die drei betroffenen Module bestanden als fokussierte 24-Test-Suite. Die
vorhergehende fokussierte PR-100-Test-Suite, die Go-/Python-/CI-Security-
Contract-Targets, ausgewählte Python-Kompilierung und `git diff --check`
bestanden ebenfalls. Ein vollständiger lokaler Security-Diff-Scan prüfte
explizit alle drei geänderten Test-Control-Dateien (der generische Source-
Worklist schließt `tests/` aus) und erzeugte null reportable Findings. Sein
aufbewahrter Completion-Receipt liegt außerhalb des Repositories im Task-Run;
er ersetzt keine frische gehostete SonarQube-Cloud-Analyse.

Der nächste Delivery-Schritt ist ein normaler task-owned Commit und Push, dann
Exact-Head-Sonar-Issue-/Quality-Gate-, Required-Check-, Review-Thread-,
Mergeability- und Protected-Branch-Evidence. Die Nutzerautorisierung erlaubt
keine direkten Master-Writes, Bypässe, Framework-/MRTS-Mutationen,
Gitlink-Änderungen oder Branch-Cleanup.

## Security-Auswirkung

Diese CI-Supply-Chain- und Validierungsgrenzen-Änderung bewahrt
unveränderliche Action-Pins, read-only-Defaults, enge Writer-Berechtigungen,
Default-Branch-Gates, keine persistenten Checkout-Credentials und getrennte
Candidate-Validierung. Sie schwächt weder Framework-Runtime-Output-Containment
noch verändert sie eine Submodule-Grenze oder installiert beziehungsweise
aktualisiert System-Go.
