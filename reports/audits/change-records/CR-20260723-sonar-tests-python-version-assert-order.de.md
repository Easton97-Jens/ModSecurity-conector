# Change Record: Parent-Python-Version-Assert-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260723-sonar-tests-python-version-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-tests-python-version-assert-order |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | Current integration base `6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d`; original source base `a308d7b414f0859490fe7253e0683a4bde80b563`. |
| Tracking | FND-SONAR-0019; 34 Parent-only SonarQube-Cloud-`python:S3415`-Code-Smells, Keys `AZ-KYVOzfYmbqbBXVNDC` bis `AZ-KYVOzfYmbqbBXVNDj`, in `tests/test_python_version_contract.py`. |
| Grenze | Ein Parent-Testmodul sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, Gitlinks, Produkt-Source, Dependency-Manifeste, Scanner-Konfiguration, Quality Gates, Suppressions und der Default-Branch bleiben unverändert. |

## Motivation und Problemstellung

Die Live-SonarQube-Cloud-Projektinventur meldet weiterhin 1.474 offene
Befunde. Vierunddreißig aktuelle Parent-`python:S3415`-Observations markieren
`unittest.TestCase.assertEqual`-Aufrufe in der Python-Version-Contract-Suite,
deren Expected- und Actual-Operanden gegenüber der Projektkonvention in
umgekehrter Reihenfolge dargestellt waren.

Die vorhandenen Prädikate und Testeingaben sind korrekt. Dieser Batch ändert
nur die Reihenfolge für die Fehlerdiagnostik: Der beobachtete Wert steht
zuerst und der feste Expected-Wert an zweiter Stelle. Er bleibt absichtlich
von allen anderen Sonar-Remediation-Branches unabhängig.

## Akzeptanzkriterien

- Exakt die ersten zwei Operanden der 34 ausgewählten `assertEqual`-Aufrufe
  ändern, die durch die aktuelle Sonar-Key-/Path-/Line-Inventur identifiziert
  sind.
- Jedes Gleichheitsprädikat, optionales drittes `msg`-Argument, Fixture,
  Helper-Invocation, Return-Code-Check und Workflow-Contract-Verhalten
  bewahren.
- Nicht ausgewählte `assertEqual`-Aufrufe in den Zeilen 167, 323 und 334
  unverändert lassen.
- Das vollständige betroffene Parent-Testmodul, den ausgewählten In-Memory-
  Syntax-Check, den Source-to-Key-Occurrence-Review, bilinguale
  Dokumentationsprüfungen und `git diff --check` bestehen lassen.
- Frische Exact-Head-Hosted-Check- und SonarQube-Cloud-Evidence nach jedem
  Branch-Update und vor der geschützten Delivery einholen; nur beobachtete
  Resultate im PR- und Task-Delivery-Record festhalten.

## Implementierungsentscheidung und Begründung

Die ausgewählten Aufrufe liefern jetzt einen geparsten Wert, eine Collection,
einen Return-Code oder ein anderes beobachtetes Result zuerst, gefolgt vom
literal oder konstruierten Expected-Wert. Das optionale Diagnose-Message bleibt
an den Stellen, an denen es existiert, unverändert das dritte Argument.

`assertEqual` vergleicht dieselben Operanden in beiden Reihenfolgen. Jedes
ausgewählte Operandenpaar ist ein Literal, lokaler Wert oder deterministisches
Contract-Helper-Result; die Umordnung ändert daher die Fehlerdarstellung, nicht
das getestete Prädikat oder External-Verhalten. Keine Implementierung, kein
Fixture, Workflow oder Dependency-Change begleitet dieses Diagnose-Cleanup.

## Geänderte Dateien

- `tests/test_python_version_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Security-Auswirkung

Dies ist ein reiner Maintainability-Testdiagnostik-Change. Er verändert keinen
Runtime-Parser, keine Path-Regel, Permission, Command-Invocation, Dependency,
Workflow-Ausführung, Request-Grenze oder Security-Control. Es wird kein
Security-Finding als behoben beansprucht, keine Suppression hinzugefügt und
kein Quality Gate oder Scanner-Setting geändert.

## Ausgeführte Befehle

- Der ausgewählte lokale Parent-Interpreter wurde als
  `/root/git/ModSecurity-conector/.venv/bin/python`, Python `3.14.4`, mit
  einem von `/usr` verschiedenen Virtual-Environment-Prefix verifiziert. Das
  Modul validiert weiterhin den kanonischen `.python-version`-Contract für
  `3.14.6`; die Hosted-Validierung ist separat an den exakten PR-Head gebunden.
- Die fokussierten `tests.test_python_version_contract`-Läufe vor und nach der
  Änderung bestanden beide mit allen 24 Tests.
- Die In-Memory-Syntaxkompilierung des geänderten Testmoduls bestand.
- Der Source-to-Key-Review ordnete nach der Änderung alle 34 ausgewählten
  aktuellen S3415-Zeilen Actual-first/Expected-second-Operanden zu.
- `tests.test_bilingual_docs` bestand alle 11 Tests und `git diff --check`
  bestand. Die zwei vollständigen Repository-Dokumentationsbefehle wurden
  ausgeführt, sind aber nur durch bereits vorhandene fehlende Links unterhalb
  des absichtlich nicht initialisierten Framework-Gitlinks blockiert; keiner
  meldet einen Fehler für dieses Record-Paar.

## Tests und tatsächliche Ergebnisse

| Befehl oder Check | Ergebnis |
| --- | --- |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_python_version_contract` | bestanden: 24 Tests vor und nach dem Assert-Reihenfolge-Change. |
| In-Memory-`compile()` von `tests/test_python_version_contract.py` mit dem ausgewählten Parent-Interpreter | bestanden. |
| AST-/Source-Vergleich gegen das retained `python:S3415`-Ledger | bestanden: 34/34 ausgewählte Zeilen ordnen Actual-first/Expected-second-Operanden zu; die drei nicht ausgewählten Aufrufe bleiben außerhalb des Patches. |
| `tests.test_bilingual_docs` | bestanden: 11 Tests. |
| `make check-bilingual-docs` | nur durch bereits vorhandene fehlende Links unterhalb des absichtlich nicht initialisierten Framework-Gitlinks blockiert; kein Fehler benennt dieses Record-Paar. |
| `make check-doc-links` | nur durch dieselben bereits vorhandenen fehlenden Framework-Gitlink-Targets blockiert. |
| Finales `git diff --check` | bestanden. |

## Runtime-Evidence

Es änderte sich kein Connector- oder Produkt-Runtime-Verhalten und es wird
keines beansprucht. Das betroffene Modul verwendet begrenzte temporäre Test-
Fixtures und prüft einen Parent-CI-Workflow-Contract; es ist weder ein Host-
Runtime-Deployment noch ein Framework-/MRTS-Lauf.

## Validierungsstatus

Die fokussierte verhaltensbewahrende Test-, Syntax-, gezielte bilinguale und
finale Diff-Evidence für die Test-Source-Änderung ist vollständig. Die zwei
vollständigen Repository-Dokumentationsbefehle sind wahrheitsgemäß nur durch
vorhandene Framework-Gitlink-Targets außerhalb des ausgewählten Parent-Batches
`blocked`. Exact-Head-GitHub- und SonarQube-Cloud-Resultate sind nach jedem
Branch-Update vor der geschützten Delivery erforderlich; das beobachtete
per-Head-Resultat bleibt im PR- und Task-Delivery-Record erhalten und wird
nicht aus einem älteren Head abgeleitet oder fortgeschrieben.

## Bekannte Einschränkungen und Follow-up

Dieser Batch behebt nur die ausgewählten 34 `python:S3415`-Testdiagnostiken.
Er beansprucht weder, den verbleibenden Parent-SonarQube-Cloud-Backlog zu
leeren, noch nicht verfügbare Connector-, CRS-, Framework- oder MRTS-
Umgebungen zu validieren.

## Verbleibende Risiken

Eine unbeabsichtigte Operandenänderung außerhalb der ausgewählten Inventur
könnte eine künftige Testfehlermeldung weniger klar machen. Das exakte
34-Key-/Line-Mapping, der Unchanged-Call-Review und das vollständige
fokussierte Testmodul reduzieren dieses Risiko. Frische Hosted- und Sonar-
Exact-Head-Evidence bleibt vor verifizierter Delivery erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Connector-Build, keine Host-Konfiguration, kein Runtime-Smoke-, CRS-,
  Protocol- oder Matrix-Check: Dieser reine Testdiagnostik-Change verändert
  diese Grenzen nicht, und das vollständige betroffene Unit-Modul ist die
  engste gültige Regressionsebene.
- Kein Framework- oder MRTS-Test und keine -Änderung: Beide Repositories sind
  ausdrücklich außerhalb dieses Parent-only-Batches.
- Kein vollständiger repositoryweiter Unittest-Lauf: Das ausgewählte Modul
  besitzt die geänderten Assertions vollständig; breitere Targets fügen
  ausgeschlossene Framework-Voraussetzungen hinzu und üben kein anderes
  geändertes Verhalten aus.
- Hosted-Checks und SonarQube-Cloud-PR-Analyse: nur für den exakten aktuellen
  PR-Head vor der geschützten Delivery bewerten; kein älteres Head-Resultat
  wiederverwenden.

## Delivery-Status

Der Kandidat ist Parent-PR #101 auf dem isolierten Branch
`codex/sonar-tests-python-version-20260723-master-a308d7b`, abgeglichen auf
die Integrationsbasis `6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d` aus der
ursprünglichen Source-Basis `a308d7b414f0859490fe7253e0683a4bde80b563`. Er
darf unter der aktuellen Task-Autorisation nur durch den repository-geschützten
Squash-Merge nach einem frischen Exact-Head-Review geliefert werden. Es gibt
keinen direkten Default-Branch-Update, Framework-/MRTS-Change, Rebase,
Force-Push oder Control-Bypass.

## Finaler Diff- und Review-Status

Der aktuelle Kandidat bleibt auf das exakte S3415-Assert-Reihenfolge-Cleanup,
dieses bilinguale Change-Record-Paar und seine zwei Indizes begrenzt. Der
finale lokale Review ist vollständig: fokussierte Tests, Syntax, Source-to-Key-
Review, gezielte bilinguale Tests und `git diff --check` bestanden; die zwei
breiteren Dokumentationsbefehle sind nur durch die dokumentierte Framework-
Gitlink-Bedingung blockiert. Exact-Head-Hosted-Checks, SonarQube-Cloud-
Quality-Gate, PR-Status und Merge-Evidence werden bei der Delivery bewertet und
nur als beobachtete Fakten im PR- und Task-Delivery-Record erhalten.
