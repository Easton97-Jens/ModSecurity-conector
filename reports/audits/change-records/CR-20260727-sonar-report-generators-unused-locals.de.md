# Change Record: Parent-Report-Generator-Bereinigung unbenutzter Lokale für SonarQube Cloud S1481

**Sprache:** [English](CR-20260727-sonar-report-generators-unused-locals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-report-generators-unused-locals |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1481`-Code-Smells AZ7K5CQgixFPtcnbna1K (443) und AZ7K5CR4ixFPtcnbna1Z (376). |
| Grenze | Parent-Report-Generator-Quelltext, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Framework/MRTS-Repository-Inhalt, Gitlinks, Report-Inputs/-Outputs, Command-Ausführung, Path-Validation, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Issue-Status, GitHub-Status und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Zwei Parent-Report-Generatoren behalten tote lokale Bindungen: den
Missing-Command-Fehler aus `command_exists(...)` in einem Pfad, der nur
Resolution und Return-Code nutzt, sowie einen Report-Directory-Pfad, der vor
der Auswahl des tatsächlichen Queue-/Report-Pfads konstruiert wird.
SonarQube-Cloud-Regel `python:S1481` meldet beide als unbenutzt, wodurch die
tatsächlich verhaltensbestimmenden Werte verdeckt werden.

## Akzeptanzkriterien

- Nur das eine ignorierte Tuple-Element zu `_` ändern und nur die eine
  unbenutzte `report_dir`-Zuweisung entfernen.
- Command-Resolution-Result-Handling, Missing-Tool-Records, Queue-Auswahl,
  Evidence-Reads und Intervention-Record-Konstruktion bewahren.
- Kontrollierte No-Command-Resolution- und Empty-Queue-Checks vor und nach
  der Änderung bestehen lassen.
- Schreibfreie In-Memory-Syntax-Compiles und eine exakte AST-Zuordnung
  bestehen lassen.
- Dieses vollständige englisch/deutsche Change-Record-Paar und die Indizes
  pflegen, danach anwendbare Dokumentations- und Diff-Hygiene-Prüfungen
  ausführen.

## Implementierungsentscheidung und Begründung

`resolve_candidate_list(...)` verwirft nun das unbenutzte zweite Tuple-Element
als `_`; es liest weiterhin denselben `resolved`-Wert und das Ergebnis `rc`,
bevor ein Missing-Tool-Record erstellt oder ein Tool aufgelöst wird.
`build_records(...)` konstruiert nicht länger das unbenutzte `report_dir`; der
bestehende Aufruf `report_path(...)` bleibt die Quelle des Queue-Pfads. Kein
Command, keine Report-Datei, kein Framework-Pfad und kein MRTS-Inhalt wird neu
ausgewählt oder ausgelassen.

## Geänderte Dateien

- `ci/evidence/reports/generate-system-environment-proof.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <in-memory compile of both sources>` vor und nach der Änderung.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <registered-import mocked missing-command resolution>` vor und nach der Änderung.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <mocked empty intervention-queue check>` vor und nach der Änderung.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST exact no-dead-local predicate>` nach der Änderung.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` und `rtk proxy rg --files -g '*.pyc' .`.

## Security-Auswirkung

`not_applicable` für den Produkt-Diff: Das Tuple-Verwerfen ändert nicht,
welche Command-Candidates ausgewertet werden, und die entfernte
Report-Directory-Konstruktion vermittelte nie einen Read/Write. Der fokussierte
Resolution-Check mockt einen fehlenden Command und bestätigt denselben
`missing`-Record ohne einen Prozess aufzurufen. Der fokussierte
Intervention-Check mockt eine leere Queue und bestätigt, dass kein Evidence-
Pfad gelesen wird. Kein Command-, Path-, Ownership- oder Publication-Control
änderte sich.

## Runtime-Evidence

Es wurde kein System-Environment-Discovery-Command, kein Report-Generator,
kein Connector, kein NGINX, kein Framework, kein MRTS und keine Host-Runtime
ausgeführt. Alle Controls verwenden nur In-Memory-Source-Compile oder gemockte
Parent-Funktionsinputs.

## Bekannte Einschränkungen

Der erste direkte dynamische Import von `generate-system-environment-proof.py`
scheiterte vor der Zielfunktion, weil der Test-Harness das Dataclass-haltige
Modul nicht in `sys.modules` registrierte. Die Registrierung vor der Ausführung
ist das Standard-Importlib-Setup; der korrigierte Vorher-/Nachher-Check bestand.
Dies ist eine Harness-Setup-Beobachtung, kein Produktfehler. Dieser Batch
behandelt nur zwei aktuelle Sonar-Code-Smells; der öffentliche Projekt-Endpunkt
meldet weiter 1.125 `OPEN`-Issues und dieser uncommittete Kandidat ändert
keinen externen Sonar-Status.

## Verbleibende Risiken

Ein nicht erkannter Consumer einer entfernten Bindung könnte ein Generator-
Ergebnis ändern. Der direkte Referenz-Review, die kontrollierten
Vorher-/Nachher-Behavior-Checks und die exakte AST-Zuordnung mindern dieses
Risiko. Eine Sonar-Analyse auf einem exakten ausgelieferten Head bleibt
erforderlich, bevor die aufgeführten Keys extern als behoben behandelt werden
können.

## Nicht ausgeführte Prüfungen mit Begründung

- `tests.test_bilingual_docs` bestand: 13 Tests in 0.036s. Der direkte
  Change-Record-Paar-Validator bestand, und `git diff --check` bestand. Der
  begrenzte Bytecode-Scan fand keine `*.pyc`-Dateien (der No-Match-`rg`-Status
  ist erwartet).
- Vollständige Report-Generation, Command-Discovery, Evidence-Reads,
  Connector-Builds, Matrizen, Framework- und MRTS-Prüfungen wurden nicht
  ausgeführt, weil sie nicht verwandte externe Runtime-Inputs konsumieren
  würden und kein Implementierungsvertrag geändert wurde.

## Finaler Diff- und Review-Status

Der B13-Kandidat ist lokal, uncommittet und ungepusht. Es gab keine GitHub-CI,
keine SonarQube-Cloud-PR-Analyse, kein Review, keinen Pull Request, keinen
Merge, kein Default-Branch-Update, keine Framework-Action und keine MRTS-
Action.
