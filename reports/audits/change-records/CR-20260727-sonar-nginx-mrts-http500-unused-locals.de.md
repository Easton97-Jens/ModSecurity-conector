# Change Record: Parent-NGINX-MRTS-HTTP-500-Report-Bereinigung unbenutzter Lokale für SonarQube Cloud S1481

**Sprache:** [English](CR-20260727-sonar-nginx-mrts-http500-unused-locals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-nginx-mrts-http500-unused-locals |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1481`-Code-Smells AZ7PU4lam6NRVhQ0A9r8 (332), AZ7PU4lam6NRVhQ0A9r9 (334) und AZ7PU4lam6NRVhQ0A9sA (428). |
| Grenze | Parent-Report-Generator-Quelltext, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Framework/MRTS-Repository-Inhalt, Gitlinks, Report-Semantik, Path-Validation, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Issue-Status, GitHub-Status und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Drei lokale Variablen im Parent-NGINX-MRTS-HTTP-500-Clusterreport werden
konstruiert, aber nie konsumiert. SonarQube-Cloud-Regel `python:S1481` meldet
die unbenutzten Bindungen `env_path`, `runtime_conf` und `example`. Ihr
Verbleib verschleiert, welche abgeleiteten Pfade und Report-Felder den Payload
tatsächlich beeinflussen.

## Akzeptanzkriterien

- Nur die drei getrackten unbenutzten lokalen Zuweisungen entfernen.
- Alle genutzten Evidence-Pfade, Harness-Root-Ableitung, Payload-Felder,
  Report-Inputs und Validierung der Verified-Run-ID bewahren.
- Das fokussierte Invalid-Run-ID-Control vor und nach der Änderung bestehen
  lassen.
- Einen schreibfreien In-Memory-Syntax-Compile und einen AST-Check bestehen
  lassen, der beweist, dass keine ausgewählte lokale Zuweisung verbleibt.
- Dieses vollständige englisch/deutsche Change-Record-Paar und die Indizes
  pflegen, danach anwendbare Dokumentations- und Diff-Hygiene-Prüfungen
  ausführen.

## Implementierungsentscheidung und Begründung

`env_path` und `runtime_conf` in `representative_cases(...)` sowie `example`
in `build_payload(...)` hatten nach ihren Zuweisungen keine Lesezugriffe. Die
Änderung löscht nur diese Zuweisungen. Der genutzte `evidence_path`,
`harness_root`, die Case-Configuration-Pfade, `reps`, Input-Metadaten, der
Report-Payload und Aufrufe von `validate_verified_run_id(...)` bleiben
unverändert. Die Datei gehört zum Parent, obwohl sie MRTS-Evidence beschreibt;
kein Framework- oder MRTS-Quelltext wird verändert.

## Geänderte Dateien

- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_runtime_path_security.RuntimePathSecurityTest.test_run_id_is_checked_before_lifecycle_and_report_path_joins` vor der Änderung.
- Derselbe fokussierte Run-ID-Control-Test nach der Änderung.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <in-memory compile(source_text, filename, "exec")>` vor und nach der Änderung.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST no-selected-local-store predicate>` nach der Änderung.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` und `rtk proxy rg --files -g '*.pyc' .`.

## Security-Auswirkung

`not_applicable` für den Produkt-Diff: Die entfernten Variablen vermittelten
weder eine Datei-, Subprocess-, Netzwerk- noch eine Report-Publication-
Operation. Dasselbe fokussierte Security-Control weist weiter Traversal- und
absolute Verified-Run-IDs ab, bevor `build_payload(...)` einen Report-/
Runtime-Pfad zusammenfügt. Kein Path-Validation-, Ownership-, Symlink- oder
Publication-Control änderte sich.

## Runtime-Evidence

Es wurde keine NGINX-, CRS-, MRTS-, Connector-, Report-Generation- oder Host-
Runtime ausgeführt. Der fokussierte Test nutzt eine ungültige Run-ID und
scheitert absichtlich, bevor er einen Framework-Pfad oder Report-Input
konsumiert; er ist ausschließlich Parent-Test-Contract-Evidence.

## Bekannte Einschränkungen

`python -B -m py_compile` ist in diesem gemounteten Worktree
`blocked_environment`: Das Standard-Library-Kommando versucht, das
quelltextnahe `ci/evidence/reports/__pycache__` anzulegen, das schreibgeschützt
ist. Es wurde kein Cache erzeugt. Der dokumentierte In-Memory-`compile(...)`-
Check validiert Syntax, ohne außerhalb des task-eigenen temporären Roots zu
schreiben. Dieser Batch behandelt nur drei aktuelle Sonar-Code-Smells; der
öffentliche Projekt-Endpunkt meldet weiter 1.125 `OPEN`-Issues und dieser
uncommittete Kandidat ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Ein nicht erkannter Lesezugriff auf ein gelöschtes Lokale könnte die
Report-Konstruktion verändern. Der direkte Referenz-Review, der No-Store-AST-
Check, das Vorher-/Nachher-Run-ID-Control und der In-Memory-Syntax-Check
mindern dieses Risiko. Eine Sonar-Analyse auf einem exakten ausgelieferten Head
bleibt erforderlich, bevor die aufgeführten Keys extern als behoben behandelt
werden können.

## Nicht ausgeführte Prüfungen mit Begründung

- `tests.test_bilingual_docs` bestand: 13 Tests in 0.035s. Der direkte
  Change-Record-Paar-Validator bestand, und `git diff --check` bestand. Der
  begrenzte Bytecode-Scan fand keine `*.pyc`-Dateien (der No-Match-`rg`-Status
  ist erwartet).
- Der vollständige Report-Generator, die NGINX/CRS/MRTS-Matrix,
  Connector-Builds und Framework/MRTS-Prüfungen wurden nicht ausgeführt, weil
  die Änderung nur tote Parent-Lokale löscht; ihre Ausführung würde nicht
  verwandte Runtime-Inputs konsumieren.

## Finaler Diff- und Review-Status

Der B12-Kandidat ist lokal, uncommittet und ungepusht. Es gab keine GitHub-CI,
keine SonarQube-Cloud-PR-Analyse, kein Review, keinen Pull Request, keinen
Merge, kein Default-Branch-Update, keine Framework-Action und keine MRTS-
Action.
