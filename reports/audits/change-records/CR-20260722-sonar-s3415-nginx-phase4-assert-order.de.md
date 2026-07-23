# Change Record: Parent-NGINX-Phase-4-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260722-sonar-s3415-nginx-phase4-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260722-sonar-s3415-nginx-phase4-assert-order |
| Datum (UTC) | 2026-07-22 |
| Basis-Revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Tracking | Fünf Parent-only-`python:S3415`-Code-Smells: AZ-KYVUffYmbqbBXVNGX, AZ-KYVUffYmbqbBXVNGY, AZ-KYVUffYmbqbBXVNGZ, AZ-KYVUffYmbqbBXVNGa und AZ-KYVUffYmbqbBXVNGb; vorgehaltene Finding-ID FND-SONAR-0017. |
| Grenze | Nur der Parent-NGINX-Phase-4-Wiring-Test sowie dieses Parent-Traceability-Paar/der Index; Framework, MRTS, Gitlinks, Fixtures, Production-Connector-/Runtime-Code, Scanner-Konfiguration und Quality Gates bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Inventur meldet 2.005 offene Projektbefunde.
Fünf aktive Parent-`python:S3415`-Beobachtungen befinden sich in
`tests/test_nginx_phase4_runner_wiring.py`. Jede Assertion übergibt einen
literalen erwarteten Wert als erstes `unittest.TestCase.assertEqual`-Argument
und einen aus dem Fixture abgeleiteten beobachteten Wert als zweites. Equality
ist symmetrisch, aber Actual-First-Reihenfolge lässt Fehlerdiagnosen beobachtete
und erwartete Werte korrekt benennen. Die Korrektur bleibt eine kleine
test-only-Änderung für fünf Keys, ohne Suppressions oder projektweiten
mechanischen Sweep.

## Akzeptanzkriterien

- Exakt die fünf Live-`python:S3415`-Aufrufe in den Zeilen 28, 30, 31, 32 und
  47 so umordnen, dass der beobachtete Wert zuerst und der literale erwartete
  Wert danach steht.
- Jeden Fixture-Namen, jeden erwarteten Mode, Status und Transport sowie das
  Testverhalten erhalten.
- Weder Framework/MRTS-Inhalt, Gitlink, Fixture-Daten, Runtime-Verhalten,
  Dependency-Metadaten, SonarQube-Cloud-Einstellungen noch eine Suppression
  ändern.
- Vor der Delivery Syntax der ausgewählten Datei, direkte Controls der
  geänderten Tests, strukturelle Reihenfolge, Bilingual-/Change-Record-Checks
  und finale Diff-Validierung ausführen.
- Bevor die fünf Keys als behoben bezeichnet werden, frische SonarQube-Cloud-
  Evidence für den exakten Draft-PR-Head einholen; der PR muss ungemergt
  bleiben.

## Implementierungsentscheidung und Begründung

Nur die Argumentreihenfolge ändert sich: `assertEqual(actual, expected)`
erhält dasselbe Prädikat wie die alten Aufrufe und verbessert die Fehlerausgabe.
Die beiden betroffenen Testmethoden bleiben die fokussierten Behavior-Controls
für alle fünf Beobachtungen. Weder Source-Abstraktion, Assertion-Helper,
Regel-Suppression noch eine breite Formatierungsänderung sind gerechtfertigt.

## Security-Auswirkung

Die Änderung beschränkt sich auf Parent-Testdiagnosen. Sie verändert weder
Untrusted-Input-Handling noch Parser-/Protocol-Verhalten, File-/Path-Operation,
Subprocess, Dependency, Credential, Privilege, Logging, Validation, Scanner,
Quality-Gate, Suppression, `NOSONAR` oder False-Positive-Control. Die
fokussierte Bewertung ist für einen separaten Security-Finding-Workflow nicht
anwendbar.

## Geänderte Dateien

- tests/test_nginx_phase4_runner_wiring.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Selected Parent Virtual-Environment Identity Check | bestanden: `/root/git/ModSecurity-conector/.venv/bin/python`, Python `3.14.4` und Venv-Prefix verifiziert. |
| Selected-File-Python-Syntax mit externem Bytecode-Cache | bestanden: `python -B -s -m compileall -q tests/test_nginx_phase4_runner_wiring.py`. |
| Direct Changed-Test Controls | bestanden: Die zwei Methoden mit allen fünf umgeordneten Assertions bestanden (2 Tests) in einem task-owned Parent-Overlay. Das Overlay liest den vorhandenen Framework-Runner nur, weil der isolierte Parent-Worktree sein Framework-Submodule absichtlich nicht initialisiert; weder Framework- noch MRTS-Pfad wurde verändert. |
| AST-Ordering-Control | bestanden: Alle fünf Zielzeilen haben exakt die Actual-First-/Expected-Second-Argumentpaare. |
| `ruff check`- und `ruff format --check`-Applicability | blockiert: Der ausgewählte Parent-Venv hat kein `ruff`-Modul; für diese fokussierte Reparatur ist weder External-Tool-Provisioning noch eine Repository-Dependency-Änderung autorisiert. |
| Pyright-Applicability | blockiert: Der ausgewählte Parent-Venv hat kein `pyright`-Modul; für diese fokussierte Reparatur ist weder External-Tool-Provisioning noch eine Repository-Dependency-Änderung autorisiert. |
| `pip check` | nicht anwendbar: Der Commit ändert weder Dependency-Manifest noch Lock, Package oder Environment. |
| Full Focused Module mit geändertem Source | vor den geänderten Assertions fehlgeschlagen: `test_generic_case_environment_carries_only_the_reviewed_mode` löst `TypeError: write_shell_env() missing 1 required keyword-only argument: 'output_root'` aus; die anderen 5 Tests bestehen. |
| Full Focused Module mit unverändertem `origin/master`-Source | mit identischem `write_shell_env`-TypeError und denselben 5 bestehenden Tests fehlgeschlagen; dies beweist, dass der lokale Fehler dieser Änderung mit fünf Assertions vorausgeht. |
| Fokussierter Change-Record-Pair-Contract | bestanden: erforderliche Headings und übereinstimmende Identity Values. |
| `tests.test_bilingual_docs`-`unittest`-Modul | bestanden: 11 Tests. |
| Repository-Bilingual-Document-Checker | blockiert: Sein Full-Checkout-Run endet nur wegen bereits vorhandener Links in das absichtlich nicht initialisierte Framework-Submodule mit Exit 1; kein neuer Change-Record-Pfad wird gemeldet. |
| `rtk proxy git diff --check` nach Source- und Traceability-Dateien | bestanden. |

Dieser Record behauptet keinen unbeobachteten PR-, CI-, SonarQube-Cloud-,
Review- oder Delivery-Status.

## Runtime-Evidence

Es ändern sich weder Connector-Runtime-Pfad, Phase-4-Verhalten, Fixture-Daten
noch Production-Implementierung. Die zwei direkten Parent-Testmethoden sind
die Behavior-Controls für die umgeordneten Diagnosen; sie beweisen weder einen
Connector-Build noch einen Runtime-Lifecycle.

## Nicht ausgeführte Prüfungen mit Begründung

- Das vollständige lokale Testmodul hat einen bekannten Baseline-Fehler
  außerhalb der fünf geänderten Assertions. Sein aktueller `origin/master`-
  Source schlägt identisch fehl, weil der Parent-Test `write_shell_env` ohne
  das erforderliche `output_root`-Argument des read-only-Framework-Runners
  aufruft. Der aktuelle Parent-Gitlink ist
  `784977615acfc55567e37b863309abc4a38ac877`; der verfügbare read-only-
  Framework-Checkout ist `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b`.
  Framework-Remediation liegt außerhalb dieses Parent-only-Sonar-Batches.
  Exakte Hosted-Checks bleiben für die Validierung des konfigurierten
  Checkout-Paars erforderlich.
- Eine Connector-Build-/Runtime- oder CRS/MRTS-Matrix ist nicht anwendbar: Es
  ändern sich weder Connector-Source noch Production-Lifecycle,
  Transportverhalten, Framework-Dateien oder MRTS-Dateien.
- Der repository-weite Bilingual-Document-Checker ist lokal durch das nicht
  initialisierte Framework-Submodule blockiert; der fokussierte Record-Pair-
  Contract und seine 11 Checker-Tests bestehen. Es wird kein Framework-
  Checkout initialisiert oder verändert, um diese Environment-Prerequisite in
  einen scheinbaren Documentation-Pass umzuwandeln.
- Ruff und Pyright sind im ausgewählten Parent-Venv nicht verfügbar. Sie sind
  optionale Quality-Tools für diesen Scope und werden nicht nebenbei
  installiert; Syntax-, direkte Test-, AST-, Documentation- und Hosted-
  Quality-Gate-Pfad bleiben die ausgewählte Validierungsroute.
- Ein vollständiger Repository-Sonar-Sweep ist keine lokale Evidence. Die
  SonarQube-Cloud-PR-Analyse für den exakten Head ist der erforderliche
  Hosted-Entscheidungspunkt.

## Bekannte Einschränkungen

Diese Änderung behandelt fünf aktuelle Parent-Beobachtungen, nicht alle 2.005
Projektbefunde. Die konfigurierte CI-Lane ist Python `3.13.14` aus
`.python-version`, während der verfügbare lokale Parent-Venv Python `3.14.4`
nutzt; die Ausführung in der exakten Lane bleibt eine Hosted-Anforderung. Der
aktuelle lokale Full-Module-Baseline-Fehler wird dokumentiert und weder
versteckt noch außerhalb des Scopes gepatcht.

## Verbleibende Risiken

Der breite Parent-only-SonarQube-Cloud-Backlog bleibt bestehen. Hosted-
Exact-Head-GitHub-Actions, SonarQube-Cloud-Quality-Gate, Selected-Key-Queries
und Review-Evidence sind erforderlich, bevor ein Draft-PR als verifiziert
bezeichnet werden kann; der PR muss ungemergt bleiben.

## Current-Master-Integrationsnachtrag (2026-07-23)

Das historische Baseline-Ergebnis vom 2026-07-22 bleibt zur
Nachvollziehbarkeit erhalten. Nachdem der Parent auf Master
`b348c7ef78bfbce058dae06794e80b5f77515907` mit Framework-Gitlink
`935cf14c676a24672be5c336e92cd13457cc35c8` aktualisiert wurde, reproduzierte
dasselbe vollständige fokussierte Modul den bereits vorhandenen
`write_shell_env`-`output_root`-API-Mismatch. Der Parent-only-Test übergibt
jetzt sein vorhandenes `TemporaryDirectory` als `output_root`; damit bleibt der
Write-Containment-Control des Frameworks erhalten und weder Framework- noch
MRTS-Inhalt ändert sich. Nach dieser Anpassung bestehen alle 6 Tests des
vollständigen fokussierten Moduls. Dies ist zusätzlich zu den fünf S3415-
Assertion-Reihenfolgen eine für die Current-Master-Integration notwendige
Kompatibilitätsreparatur.

Dieser Nachtrag ersetzt die frühere vorausschauende Draft-/Unmerged-
Delivery-Formulierung. Frische Hosted-Checks für den exakten Head,
SonarQube-Cloud-Evidence und Review-Evidence bleiben vor einem geschützten
Merge erforderlich.

## Finaler Diff- und Review-Status

Der beabsichtigte Source-Diff tauscht nur die Argumentreihenfolge in fünf
`assertEqual`-Aufrufen und fügt bilinguale Traceability hinzu. Vor der Delivery
müssen finaler scoped Diff, Documentation-Checks, die exakte lokale/Remote/PR-
SHA-Beziehung, anwendbare GitHub-Checks, SonarQube-Cloud-Quality-Gate,
All-Five-Key-Query und der Draft-PR-Status für den tatsächlichen Head erneut
geprüft werden.
