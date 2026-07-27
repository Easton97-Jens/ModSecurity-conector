# Change Record: Parent-Bilingual-Markdown-Suffix-Ownership für SonarQube Cloud S1192

**Sprache:** [English](CR-20260727-sonar-bilingual-markdown-suffix.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-bilingual-markdown-suffix |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1192`-Code-Smell AZ9cRyW7HhV2CayPTPup (Zeile 223). |
| Grenze | Parent-Bilingual-Dokumentationschecker und sein Parent-Unit-Test, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Dokumentationspolicy, Companion-Naming-Verhalten, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Status, GitHub-Status, Framework/MRTS-Inhalt und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Der Bilingual-Dokumentationschecker wiederholte das Markdown-Suffix-Literal in
den zwei gegenläufigen Companion-Konstruktoren. Sonar-Regel `python:S1192`
meldet die Duplizierung. Ein moduleigener Name macht den gemeinsamen
Formatvertrag explizit, ohne ihn auf andere Suffix-/Pfadbehandlung auszuweiten.

## Akzeptanzkriterien

- Eine moduleigene Markdown-Suffix-Konstante ergänzen.
- Sie nur in den English/German-Companion-Konstruktoren verwenden.
- Die Abbildung `foo.md` zu `foo.de.md` und zurück bewahren.
- Direkte Unit- und schreibfreie AST-Validierung bestehen lassen.
- Englisches/deutsches Change-Record-Paar und Indizes pflegen, danach
  Dokumentationspaar- und Diff-Hygiene-Validierung ausführen.

## Implementierungsentscheidung und Begründung

`MARKDOWN_SUFFIX` ersetzt nur die zwei doppelten Literale. Der deutsche
Konstruktor hängt weiter `.de` vor dem Suffix an, während der englische
Konstruktor weiter `.de` plus Suffix entfernt. Ein fokussierter bidirektionaler
Test hält beide Pfade fest. Kein Dokumentationsinhalt, Discovery,
Local-Link-Resolution oder Policy-Entscheidung änderte sich.

## Geänderte Dateien

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env TMPDIR=<task-owned evidence root> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v
  tests.test_bilingual_docs` bestand nach der Änderung: 14 Tests in 0.034s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <Suffix-Ownership-, Companion- und Testsyntax-AST-Prädikat>`
  bestand.
- Der Dokumentationspaar-Validator und `rtk proxy git diff --check` werden
  ausgeführt, nachdem dieses Paar angelegt ist; dieses Record behauptet kein
  unbeobachtetes CI-, Runtime-, Review- oder Delivery-Ergebnis.

## Security-Auswirkung

`not_applicable` für den Produkt-Diff: Dies refaktoriert nur ein statisches
Dokumentationssuffix-Literal. Es ändert keine Path-Containment-, Link-Escape-,
Authorization-, Subprocess-, Netzwerk- oder Publication-Logik.

## Runtime-Evidence

Es wurde keine Connector-, Report-Generator-, Framework-, MRTS- oder Host-
Runtime ausgeführt. Der fokussierte Unit-Test prüft nur In-Memory-`Path`-
Companion-Konstruktion.

## Bekannte Einschränkungen

Der lokale Interpreter ist Python 3.14.4, während der CI-Version-File-Vertrag
Python 3.14.6 verlangt; das Ergebnis ist daher same-minor lokale Evidence.
Dieser Batch behandelt einen aktuellen Code-Smell; der öffentliche Projekt-
Endpunkt meldet weiter 1.125 `OPEN`-Issues und dieser uncommittete Kandidat
ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Ein unerwarteter Aufrufer könnte ein anderes Suffix-Verhalten erwarten. Die
zwei Konstruktoren behalten ihre exakten früheren Transformationen und der
bidirektionale Test führt beide aus. Eine Sonar-Analyse auf einem exakten
ausgelieferten Head bleibt erforderlich, bevor der aufgeführte Key extern als
behoben behandelt werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Dokumentations-/Link-Checks liegen außerhalb dieses kleinen
  Suffix-only-Batches; frühere vollständige Läufe sind wegen des absichtlich
  nicht initialisierten Framework-Gitlinks blockiert, nicht wegen dieses Codes.
- Es gab keine GitHub-CI, keine SonarQube-Cloud-PR-Analyse, kein Review,
  keinen Pull Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der B17-Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Delivery-,
Framework- oder MRTS-Action.
