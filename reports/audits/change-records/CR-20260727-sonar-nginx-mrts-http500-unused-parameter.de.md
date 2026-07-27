# Change Record: Parent-NGINX-MRTS-HTTP-500-Report-Bereinigung ungenutzter Parameter für SonarQube Cloud S1172

**Sprache:** [English](CR-20260727-sonar-nginx-mrts-http500-unused-parameter.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-nginx-mrts-http500-unused-parameter |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1172`-Code-Smell AZ7PU4lam6NRVhQ0A9r_ (Inventory-Zeile 408). |
| Grenze | Parent-Report-Generator- und Parent-Test-Quelltext, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Framework/MRTS-Repository-Inhalt und Gitlinks, Report-Semantik, Validierungs-Controls, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Issue-Status, GitHub-Status und Delivery bleiben unverändert. |

## Motivation und Problemstellung

`build_payload(...)` akzeptiert `framework_root`, liest ihn aber nie.
SonarQube-Cloud-Regel `python:S1172` meldet diesen toten Hilfsparameter. Sein
Verbleib kann einem Aufrufer fälschlich nahelegen, dass der Payload selbst
Framework-Inhalt konsumiert, obwohl der Kommandozeilenwert erst später für
Report-Metadaten benötigt wird.

## Akzeptanzkriterien

- Nur den ungenutzten Hilfsparameter `framework_root` entfernen.
- Jeden Parent-Aufrufer des Helpers anpassen.
- Den Kommandozeilenpfad `--framework-root` und seine Nutzung für
  Report-Metadaten bewahren.
- Die Ablehnung ungültiger Verified-Run-IDs vor jedem Report-/Runtime-Pfad-Join
  bewahren.
- Das fokussierte Control vor und nach der Änderung sowie schreibfreie Syntax-,
  Signatur-/Aufrufer-, Dokumentationspaar- und Diff-Hygiene-Validierung
  bestehen lassen.

## Implementierungsentscheidung und Begründung

Der `build_payload(...)`-Body liest `framework_root` nicht; `main()` des
Generators löst ihn weiterhin auf und übergibt ihn an `build_metadata(...)`.
Die Änderung entfernt ihn deshalb nur aus der Helper-Signatur und ihren zwei
Parent-Aufrufern: dem lokalen Generator-Aufruf und dem fokussierten
Invalid-Run-ID-Test. CLI-Option, Metadatenidentität, Input-Auswahl,
Run-ID-Validierung und Report-Felder bleiben unverändert. Die Datei gehört zum
Parent, obwohl sie MRTS-Evidence beschreibt; kein Framework- oder MRTS-
Quelltext wird verändert.

## Geänderte Dateien

- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `tests/test_runtime_path_security.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Vor der Änderung bestand das fokussierte Invalid-Run-ID-Control: 1 Test in
  0.281s.
- Vor der Änderung bestätigten schreibfreier In-Memory-Compile und AST-Check
  die Vierparameter-Signatur sowie keinen Body-Lesezugriff auf
  `framework_root`.
- Nach der Änderung bestand dasselbe fokussierte Invalid-Run-ID-Control: 1
  Test in 0.292s.
- Nach der Änderung bestätigten schreibfreier In-Memory-Compile und AST-Check
  die Dreiparameter-Signatur sowie keinen Body-Referenzzugriff auf
  `framework_root`.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v
  tests.test_bilingual_docs`, der direkte Change-Record-Paar-Validator und
  `rtk proxy git diff --check` werden ausgeführt, nachdem dieses Paar angelegt
  ist. Dieses Record behauptet kein CI-, Runtime-, Review- oder
  Delivery-Ergebnis.

## Security-Auswirkung

`not_applicable` für den Produkt-Diff: Der entfernte Hilfsparameter vermittelte
weder eine Datei-, Subprocess-, Netzwerk- noch eine Publication-Operation.
Dasselbe fokussierte Security-Control weist weiter Traversal- und absolute
Verified-Run-IDs ab, bevor `build_payload(...)` einen Report-/Runtime-Pfad
zusammenfügen kann. Kein Path-Validation-, Ownership-, Symlink- oder
Publication-Control änderte sich.

## Runtime-Evidence

Es wurde keine NGINX-, CRS-, MRTS-, Connector-, Report-Generation- oder Host-
Runtime ausgeführt. Der fokussierte Test nutzt eine ungültige Run-ID und
scheitert absichtlich, bevor er einen Framework-Pfad oder Report-Input
konsumiert; er ist ausschließlich Parent-Test-Contract-Evidence.

## Bekannte Einschränkungen

Kein quelltextnaher `py_compile`-Check wird in diesem gemounteten Worktree
verwendet, weil der vorherige Batch desselben Moduls beobachtete, dass er ein
schreibgeschütztes `__pycache__` anlegen will; der dokumentierte In-Memory-
`compile(...)` validiert Syntax, ohne außerhalb des task-eigenen temporären
Roots zu schreiben. Dieser Batch behandelt einen aktuellen Sonar-Code-Smell.
Der öffentliche Projekt-Endpunkt meldet weiter 1.125 `OPEN`-Issues und dieser
uncommittete Kandidat ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Ein unbeobachteter externer Aufrufer könnte noch die alte Helper-Signatur
verwenden. Die repositoryweite Source-Referenzprüfung fand nur die zwei
aktualisierten Parent-Aufrufer, während das fokussierte Invalid-Run-ID-Control
die erhaltene Sicherheitsgrenze ausführt. Eine Sonar-Analyse auf einem
exakten ausgelieferten Head bleibt erforderlich, bevor der aufgeführte Key
extern als behoben behandelt werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Report-Generation, NGINX/CRS/MRTS-Matrizen, Connector-Builds
  und Framework/MRTS-Prüfungen werden nicht ausgeführt, da dies eine reine
  Parent-Signaturbereinigung ist und sie nicht verwandte Runtime-Inputs
  konsumieren würden.
- Es gab keine GitHub-CI, keine SonarQube-Cloud-PR-Analyse, kein Review,
  keinen Pull Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der B14-Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Delivery-,
Framework- oder MRTS-Action.
