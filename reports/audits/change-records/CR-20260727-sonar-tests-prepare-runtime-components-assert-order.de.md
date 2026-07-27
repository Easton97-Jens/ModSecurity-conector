# Change Record: Parent-Prepare-Runtime-Components-Provenance-Guard-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-prepare-runtime-components-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-prepare-runtime-components-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`-Code-Smell AZ-KYVRDfYmbqbBXVNDp (324). |
| Grenze | Parent-Testquelltext, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Runtime-Component-Provisioning-Verhalten, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Issue-Status, GitHub-Status und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Der ausgewählte Provenance-Guard-Test prüft bereits das korrekte blockierte
Ergebnis, wenn die Framework-autorisierte ModSecurity-v3-Provenance scheitert.
Seine Assertion übergibt das erwartete Literal vor dem beobachteten Record-
Feld, entgegen der von SonarQube-Cloud-Regel `python:S3415` verlangten
diagnostischen Reihenfolge `Istwert, Erwartungswert`.

## Akzeptanzkriterien

- Nur `AZ-KYVRDfYmbqbBXVNDp` auf die Reihenfolge `Istwert, Erwartungswert`
  korrigieren.
- Das blockierte Provenance-Fixture und jede Assertion bewahren, die Copy-,
  Subprocess-, Output-Copy- oder Publish-Verhalten verhindert.
- Den fokussierten Parent-only-Test vor und nach der Änderung bestehen lassen.
- Eine exakte AST-Zuordnung für den erhaltenen Sonar-Zeilenanker bestehen
  lassen.
- Dieses vollständige englisch/deutsche Change-Record-Paar und die Indizes
  pflegen, danach anwendbare Dokumentations- und Diff-Hygiene-Prüfungen
  ausführen.

## Implementierungsentscheidung und Begründung

Der Test übergibt nun den bereits materialisierten Wert `record["status"]`
vor dem unveränderten inerten Literal `"blocked"`. `prepare_shared_modsecurity(...)`
endet vor der Auswertung der Assertion, daher ändert der Tausch weder den
Guard-Aufruf noch verschiebt er einen Datei-, Subprocess-, Copy- oder Publish-
Sink. Die exakte Equality-Domäne bleibt `str`; kein Fixture, Mock,
Erwartungswert oder keine Assertion des blockierten Build-Verhaltens änderte
sich.

## Geänderte Dateien

- `tests/test_prepare_runtime_components.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_prepare_runtime_components.PrepareRuntimeComponentsTest.test_shared_modsecurity_blocks_before_build_sinks_when_framework_guard_rejects` vor der Änderung.
- Derselbe fokussierte Unittest-Befehl nach der Änderung.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST exact-map predicate>` nach der Änderung.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` und `rtk proxy rg --files -g '*.pyc' .`.

## Security-Auswirkung

`not_applicable` für Produktionsverhalten: Es änderte sich nur die
Testdiagnostik-Reihenfolge. Das erneut ausgeführte Control fordert weiter, dass
abgelehnte Framework-Provenance `"blocked"` ergibt, die Build- und Prefix-
Verzeichnisse fehlen und `copytree`, `run_env`, `copy_modsecurity_outputs`
und `atomic_publish_dir` verboten bleiben. Kein Implementierungs-Provenance-,
Host-Executable-, Path-, Subprocess- oder Publication-Control änderte sich.

## Runtime-Evidence

Es wurde keine Runtime-Component-Preparation, kein Framework-Checkout, kein
Connector-Build und keine Veröffentlichung ausgeführt. Die fokussierte Methode
nutzt einen temporären Fake-Framework-Pfad und mockt jeden Build-/Output-Sink;
sie ist ausschließlich Test-Contract-Evidence.

## Bekannte Einschränkungen

Dieser lokale Batch behandelt einen aktuellen Sonar-Code-Smell. Drei weitere
S3415-Inventarzeilen desselben Moduls bleiben unverändert: Zwei besitzen nicht
inert konstruierte erwartete Command-Listen, und eine ist im aktuellen
Quelltext bereits Istwert-zuerst. Der öffentliche Projekt-Endpunkt meldet
weiter 1.125 `OPEN`-Issues; dieser uncommittete Kandidat ändert keinen
externen Sonar-Status.

## Verbleibende Risiken

Eine unbeabsichtigte Änderung eines Assertion-Werts könnte den Provenance-
Failure-Contract schwächen. Der Ein-Aufruf-Diff, der fokussierte Vorher-/
Nachher-Test, die exakte AST-Zuordnung und die bewahrten Mock-Sink-Verbote
mindern dieses Risiko. Eine Sonar-Analyse auf einem exakten ausgelieferten Head
bleibt erforderlich, bevor der aufgeführte Key extern als behoben behandelt
werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- `tests.test_bilingual_docs` bestand: 13 Tests in 0.035s. Der direkte
  Change-Record-Paar-Validator bestand, und `git diff --check` bestand. Der
  begrenzte Bytecode-Scan fand keine `*.pyc`-Dateien (der No-Match-`rg`-Status
  ist erwartet).
- Das breitere Testmodul, der Runtime-Component-Build, Connector-Builds,
  Host-Runtime-Smoke-Tests, Framework- und MRTS-Prüfungen wurden nicht
  ausgeführt, weil der abgegrenzte Test seine Sinks mockt und kein
  Implementierungsverhalten geändert wurde.

## Finaler Diff- und Review-Status

Der B11-Kandidat ist lokal, uncommittet und ungepusht. Es gab keine GitHub-CI,
keine SonarQube-Cloud-PR-Analyse, kein Review, keinen Pull Request, keinen
Merge, kein Default-Branch-Update, keine Framework-Action und keine MRTS-
Action.
