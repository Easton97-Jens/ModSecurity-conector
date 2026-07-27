# Change Record: Parent-Full-Runtime-Matrix-UTC-Offset für SonarQube Cloud S1192

**Sprache:** [English](CR-20260727-sonar-full-runtime-matrix-utc-offset.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-full-runtime-matrix-utc-offset |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1192`-Code-Smell AZ7POyMJBW70q7L2nMI1 (Zeile 164). |
| Grenze | Parent-Full-Runtime-Matrix-Report-Zeitstempelformatierung und ihr Parent-In-Memory-Parsing-Test, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Manifest-Parsing, UTC-`Z`-Repräsentation, Report-Generierung, Runtime-Matrix-Ausführung, Evidence, Output-Pfade, Status-Semantik, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Status, GitHub-Status, Framework/MRTS-Inhalt und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Der Full-Runtime-Matrix-Report verwendete das gleiche ISO-8601-UTC-Offset-
Literal dreimal: einmal beim Akzeptieren eines `Z`-Manifestzeitstempels und
zweimal beim Ausgeben eines `Z`-Zeitstempels. Sonar-Regel `python:S1192`
meldet diese Duplizierung. Eine private Konstante macht die
numerische-Offset-Repräsentation explizit, während der sichtbare `Z`-Vertrag
unverändert bleibt.

## Akzeptanzkriterien

- Eine moduleigene private numerische UTC-Offset-Konstante definieren.
- Nur die drei `"+00:00"`-Literale ersetzen.
- Parsing von `Z`-Eingaben, UTC-aware Dauerarithmetik und die ausgegebene
  `Z`-Designator-Semantik bewahren.
- Das Modul nur über das etablierte Dynamic-Import-Pattern importieren; weder
  `main()`, noch eine Runtime-Matrix oder Report-Ausgabe ausführen.
- Englisches/deutsches Change-Record-Paar und Indizes pflegen, danach
  Dokumentationspaar- und Diff-Hygiene-Validierung ausführen.

## Implementierungsentscheidung und Begründung

`_UTC_OFFSET = "+00:00"` ersetzt genau den Parser-Normalisierungsoperanden
und die zwei Generated-at-Normalisierungsoperanden. Die drei `"Z"`-Literale
bleiben inline, weil sie die einzeichenlange serialisierte Repräsentation und
nicht der Sonar-Befund sind. Der fokussierte Test importiert das Modul mit der
für sein `@dataclass` nötigen `sys.modules`-Registrierung, prüft
`Z`-Parsing in ein UTC-aware Datetime und eine Dauer von 60 Sekunden.

## Geänderte Dateien

- `ci/evidence/reports/generate-full-runtime-matrix.py`
- `tests/test_report_presentation_literals.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env TMPDIR=<task-owned evidence root> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest
  tests.test_report_presentation_literals` bestand nach der Änderung: 3 Tests
  in 0.001s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <AST-Offset-Ownership-Prädikat>` bestand und bestätigte ein
  `"+00:00"`-Literal sowie drei `_UTC_OFFSET`-Loads.
- Der Dokumentationspaar-Validator und `rtk proxy git diff --check` werden
  ausgeführt, nachdem dieses Paar angelegt ist; dieses Record behauptet kein
  unbeobachtetes CI-, Runtime-, Review- oder Delivery-Ergebnis.

## Security-Auswirkung

`not_applicable` für den Produkt-Diff: Dies ist eine statische
Zeitstempelformat-Literalextraktion. Sie ändert keine Path-/Root-Validierung,
Manifestquelle, Evidence-Authentizität, Subprocess-, Netzwerk-,
Request-/Rule-/Status-Behandlung oder Output-Write-Verhalten.

## Runtime-Evidence

Es wurde keine Runtime-Matrix-Producer-, Report-Generator-`main()`-,
Output-Writer-, Connector-, Framework-, MRTS- oder Host-Runtime ausgeführt.
Der Test importierte das Modul und rief nur die reinen Zeitstempel-Parsing- und
Dauer-Helper auf.

## Bekannte Einschränkungen

Der lokale Interpreter ist Python 3.14.4, während der CI-Version-File-Vertrag
Python 3.14.6 verlangt; das Ergebnis ist daher same-minor lokale Evidence.
Dieser Batch behandelt einen aktuellen Code-Smell; der öffentliche Projekt-
Endpunkt meldet weiter 1.125 `OPEN`-Issues und dieser uncommittete Kandidat
ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Generierte Reports sind Audit-Artefakte, deren UTC-Schreibweise extern
konsumiert wird. Das `Z`-Token bleibt byte-genau unverändert, das Input-
Parsing ist direkt abgedeckt, und eine Sonar-Analyse auf einem exakten
ausgelieferten Head bleibt erforderlich, bevor der aufgeführte Key extern als
behoben behandelt werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Runtime-Matrix-Generierung ist absichtlich ausgeschlossen: Sie
  liest Manifest-Evidence und schreibt Reports, außerhalb dieses reinen
  Literal-Batches.
- Vollständige Dokumentations-/Link-Checks liegen außerhalb dieses kleinen
  Batches; frühere vollständige Läufe sind wegen des absichtlich nicht
  initialisierten Framework-Gitlinks blockiert, nicht wegen dieser
  Zeitstempelformatierung.
- Es gab keine GitHub-CI, keine SonarQube-Cloud-PR-Analyse, kein Review,
  keinen Pull Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der B19-Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Delivery-,
Framework- oder MRTS-Action.
