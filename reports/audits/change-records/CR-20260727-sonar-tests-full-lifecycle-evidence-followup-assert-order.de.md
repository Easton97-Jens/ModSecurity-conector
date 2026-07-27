# Change Record: Parent-Full-Lifecycle-Evidence-Folge-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-full-lifecycle-evidence-followup-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-full-lifecycle-evidence-followup-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`-Code-Smells AZ-KYVT1fYmbqbBXVNGD (168), AZ-KYVT1fYmbqbBXVNGE (197), AZ-KYVT1fYmbqbBXVNGF (239) und AZ-KYVT1fYmbqbBXVNGG (251). |
| Grenze | Parent-Testquelltext, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Full-Lifecycle-Checker-/Runtime-Verhalten, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Issue-Status, GitHub-Status und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Die vier ausgewählten `unittest.assertEqual`-Aufrufe prüfen bereits die
beabsichtigten Werte, übergeben aber den erwarteten Wert vor dem beobachteten
Ergebnis. SonarQube-Cloud-Regel `python:S3415` verlangt die diagnostische
Reihenfolge `Istwert, Erwartungswert`. Die Korrektur ausschließlich dieser
Reihenfolge verbessert die Fehlerausgabe, ohne Akzeptanzkriterien oder die
getesteten Full-Lifecycle-Controls zu ändern.

## Akzeptanzkriterien

- Nur die vier getrackten Assertion-Aufrufe auf die Reihenfolge `Istwert,
  Erwartungswert` korrigieren.
- Jedes Fixture, jeden Input, jeden Erwartungswert, jeden Checker-Aufruf,
  Testzweig und jede Produktionsquelldatei bewahren.
- Die vier fokussierten Parent-only-Methoden vor und nach der Änderung
  bestehen lassen.
- Eine exakte AST-Zuordnung für die vier erhaltenen Sonar-Zeilenanker
  bestehen lassen.
- Dieses vollständige englisch/deutsche Change-Record-Paar und die Indizes
  pflegen, danach die anwendbaren Dokumentations- und Diff-Hygiene-Prüfungen
  ausführen.

## Implementierungsentscheidung und Begründung

Die geänderten Aufrufe stellen jetzt jeweils das bestehende beobachtete
Ergebnis voran: den Integer von `sanitizer.main(...)` vor `0`, die bereits
gebundene `errors`-Liste vor ihre erwartete Liste,
`checker.profile_errors(...)` vor `[]` und `checker.main(...)` vor `1`.
Jeder frühere Erwartungsoperand ist ein inertes eingebautes Literal oder eine
Listenkonstruktion. Das Vorziehen des beobachteten Ergebnisses fügt weder
einen Input, Zweig, Dateisink, Prozess noch einen Vergleichstyp hinzu; die
Equality-Domänen bleiben eingebaute `int`- oder Listenwerte. Es wurden kein
Helper, keine Abstraktion, kein Fixture, kein erwarteter String und keine
Runtime-Bedingung geändert.

## Geänderte Dateien

- `tests/test_full_lifecycle_evidence.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v <four selected FullLifecycleEvidenceTest methods>` vor der Änderung.
- Derselbe fokussierte Unittest-Befehl nach der Änderung.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST exact-map predicate>` nach der Änderung.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` und `rtk proxy rg --files -g '*.pyc' .`.

## Security-Auswirkung

`not_applicable` für Produktionsverhalten: Es handelt sich ausschließlich um
diagnostische Argumentreihenfolge in Parent-Testcode. Der ausgewählte
Log-Sanitizer-Test bleibt ein Same-Boundary-Control für Credential-/Body-
Redaction und bestand vor sowie nach der Änderung. Es änderten sich kein
Parser, keine Path-Policy, kein Subprocess-Vertrag, keine Credential-
Verarbeitung, kein Transport-Control und kein Connector-Enforcement-Verhalten.

## Runtime-Evidence

Es wurde kein Connector-Runtime-Verhalten geändert oder behauptet. Die vier
fokussierten Methoden nutzen temporäre lokale Fixtures und validieren nur
Parent-Test-/Checker-Verträge.

## Bekannte Einschränkungen

Dieser lokale Batch behandelt nur vier aktuelle Sonar-Code-Smells. Der
öffentlich erneut geprüfte Projekt-Endpunkt meldet weiter 1.125 `OPEN`-Issues;
aus diesem uncommitteten Kandidaten wird kein externer Sonar-Status abgeleitet.

## Verbleibende Risiken

Eine unbeabsichtigte Änderung eines Erwartungswerts oder Fixtures könnte die
Evidence-Controls schwächen. Der minimale Vier-Aufruf-Diff, die fokussierten
Vorher-/Nachher-Tests, die exakte AST-Zuordnung und das bewahrte
Redaction-Control mindern dieses Risiko. Eine Sonar-Analyse auf einem exakten
ausgelieferten Head bleibt erforderlich, bevor ein aufgeführter Key extern als
behoben behandelt werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- `tests.test_bilingual_docs` bestand: 13 Tests in 0.034s. Der direkte
  Change-Record-Paar-Validator bestand, und `git diff --check` bestand. Der
  begrenzte Bytecode-Scan fand keine `*.pyc`-Dateien (der No-Match-`rg`-Status
  ist erwartet).
- Das weitere Full-Lifecycle-Modul, Connector-Builds, Host-Runtime-Smoke-
  Tests, Protokollmatrizen, Framework- und MRTS-Prüfungen wurden nicht
  ausgeführt: Die Änderung bleibt auf vier Parent-only-Assertion-Diagnostiken
  beschränkt und ändert diese Implementierungsgrenzen nicht.

## Finaler Diff- und Review-Status

Der B10-Kandidat ist lokal, uncommittet und ungepusht. Es gab keine GitHub-CI,
keine SonarQube-Cloud-PR-Analyse, kein Review, keinen Pull Request, keinen
Merge, kein Default-Branch-Update, keine Framework-Action und keine MRTS-
Action.
