# Change Record: Parent-CI-Markersektion- und Script-Literal-Deduplizierung für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-ci-marker-script-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-ci-marker-script-deduplication |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | `8a3872e5e63f93e202bed24e0dcbad7bdf110ede` |
| Umfang und Grenze | Ausschließlich Parent `ci/`, `scripts/`, direkt fokussierte Parent-Tests sowie dieses englisch/deutsche Change-Record-Paar mit seinen Indizes. `.github/`, Framework, MRTS, Gitlinks, generierte Reports und SonarQube-Konfiguration bleiben unverändert. |
| Finding-Verknüpfung | Die SonarQube-Cloud-Master-Analyse vor dem PR meldete 631 offene Issues, 0,2 % Projektduplikation (1.260 Zeilen) und die `python:S1192`-Issues `AZ9cRzA4HhV2CayPTP47` sowie `AZ9cRzA4HhV2CayPTP46` im Repository-Organisationsinventar. Die CI-Clone-Evidence enthält das 113-Zeilen-Paar Nolog/Response-Header. Dieser Record behauptet weder die Schließung historischer Issues noch eine Master-Integration. |

## Motivation und Problemstellung

Sechs Parent-Report-Generatoren führten unabhängig dieselbe begrenzte
Markdown-Marker-Ersetzung, Insertion vor einem Anchor und Append-Fallback aus.
Zwei dieser Generatoren enthielten außerdem dieselbe Framework-Case-Suche, die
bereits die Safe-File-Grenze verwendete. Dieser duplizierte Code erhöhte den
Wartungsaufwand und trug zum gemessenen Parent-CI-Duplikatcluster bei.

Das Repository-Organisationsinventar wiederholte separat zwei stabile
Literale: das deutsche Markdown-Suffix und den Parent-relativen Framework-
Pfadpräfix. Die aktuellen Sonar-Issues weisen diese Literalwiederholungen
direkt aus.

## Akzeptanzkriterien

- `find_framework_case_path()` behält die vorhandene Case-Namens-Prüfung,
  durchsucht nur die vorhandenen Framework-Case-/Upstream-Roots und liefert
  ausschließlich ein `safe_existing_file`-Ergebnis.
- `upsert_marked_section()` hat keine Dateisystemeffekte und erhält die
  vorhandene Markerersetzung, Insertion am gewählten Anchor, Fallback-Append,
  Leerzeilen- und Schlusszeilenumbruch-Semantik.
- Alle sechs Report-Generatoren behalten ihre vorhandenen Report-Pfade sowie
  Safe-Reader-/Writer-Aufrufe; es wird kein Output-Ziel neu abgeleitet oder
  verbreitert.
- Das Inventar behält die englische/deutsche Klassifikation und das
  Parent/Framework-Routing mit benannten Entsprechungen der bisherigen
  Literale.
- Fokussierte Utility- und Inventory-Tests, Conditional-Remediation-Tests,
  Syntaxkompilierung und Whitespace-Validierung bestehen.

## Implementierungsentscheidung und Begründung

Die geteilten Helfer liegen im bereits vorhandenen Parent-only-Modul
`ci/lib/focused_analysis_utils.py`. `find_framework_case_path()` ist eine
unveränderte Verlagerung der zwei geklonten Implementierungen. Der Marker-
Helfer ist eine reine String-Operation mit literalen `split()`-Grenzen statt
einer breiten Regular Expression. Die Caller behalten ihre gegenwärtigen
`read_text()`- und `write_text_file()`-Operationen, daher bleibt
`report_path_safety` die schreibende Enforcement-Grenze.

`FRAMEWORK_PATH_PREFIX` und `GERMAN_MARKDOWN_SUFFIX` benennen die zwei
invarianten Script-Werte. Sie ändern weder die Ermittlung getrackter Dateien,
die Zielauswahl, die temporäre Ausgabe noch die Framework-Ownership.

## Geänderte Dateien

- `ci/lib/focused_analysis_utils.py`
- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/evidence/reports/generate-phase4-hard-abort-capability.py`
- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py`
- `scripts/generate_repository_organization_inventory.py`
- `tests/test_focused_analysis_utils.py`
- `tests/test_repository_organization_inventory.py`
- dieses englisch/deutsche Change-Record-Paar und beide Indizes

## Ausgeführte Befehle

| Befehl oder Kontrolle | Tatsächliches Ergebnis |
| --- | --- |
| Aktuelle SonarQube-Cloud-Issue-, Measure-, Component-Tree- und Duplikat-API-Abfrage | bestanden: 631 offene/bestätigte Issues; 0,2 % / 1.260 duplizierte Zeilen; die ausgewählte Parent-only-CI- und Script-Evidence ist oben festgehalten. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_focused_analysis_utils tests.test_repository_organization_inventory` | bestanden: 16 Tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_report_conditional_remediation` | bestanden: 9 Tests. |
| `env PYTHONPYCACHEPREFIX=<task-owned external cache> python3 -P -m py_compile <changed Python files>` | bestanden. |
| `git diff --check` | bestanden; kein Whitespace-Fehler wurde gemeldet. |
| Direktes `python3 -m compileall` | blocked_environment: Es versucht, `__pycache__` unter dem schreibgeschützten Task-Worktree anzulegen. Die äquivalente ausgewählte `py_compile`-Kontrolle bestand mit einem in ein registriertes task-owned externes Verzeichnis umgeleiteten Cache. |
| Direkte Bilingual-Dokumentations- und Repository-Pfad-Prüfungen | blocked_environment: Alle Diagnosen benennen fehlende Ziele unter dem nicht ausgefüllten Framework-Gitlink; keine benennt dieses Change-Record-Paar oder seine Indizes. |

## Security-Auswirkung

Dies ist eine CI-/Reporting- und pfadsensitive Grenzprüfung. Der Framework-
Case-Helfer erhält die vorhandene Slash-/Backslash-Ablehnung und das
`safe_existing_file`-Gate unverändert. Der Marker-Helfer liest oder schreibt
keine Dateien und akzeptiert nur Caller-bereitgestellte statische Marker und
Anchors. Jeder Caller behält seine vorhandene sichere Report-Pfadkonfiguration
und seinen Writer.

Es sind keine Workflow-Berechtigungen, Action-Pins, Scanner-Kontrollen,
Suppressions, Runtime-Path-Policy, Framework-/MRTS-Quellen, Gitlinks oder
generierten Report-Änderungen enthalten. Aktuelle sicherheitsklassifizierte
Sonar-Zeilen wurden gegen die kanonische Triage `FND-SONAR-0001` geprüft und
sind nicht als Fixes dieses Duplikat-Batches dargestellt.

## Runtime-Evidence

Die bestandenen Kontrollen sind ausschließlich lokale Source-, Import- und
fokussierte Unit-Evidence. Sie behaupten weder Report-Generation,
Runtime-Matrix-Ausführung, Connector-Runtime, Framework-/MRTS-Ausführung noch
Hosted-CI-/SonarQube-Cloud-Analyse.

## Bekannte Einschränkungen

Die Änderung bearbeitet bewusst nur einen begrenzten Teil der 1.260
Projektduplikatzeilen. Die aktuelle SonarQube-Cloud-Analyse des aktiven
PR-Heads ist externe Delivery-Evidence und muss für genau diesen Head
verifiziert werden; sie wird nicht in diesem statischen Source-Record
eingefroren. Ein künftiger Report-Generator mit materiell anderem Anchor liegt
außerhalb dieses Batches.

## Verbleibende Risiken

Ein künftiger Report-Generator mit materiell anderem Anchor muss den Helfer
bewusst verwenden und eine Exact-Output-Kontrolle behalten. Eine Hosted-
SonarQube-Cloud-Analyse kann verbleibende Klone in der breiteren
Report-Generator-Familie identifizieren; diese benötigen eine getrennte
evidenzbasierte Auswahl statt eines ungeprüften großen Refactors.

## Nicht ausgeführte Prüfungen mit Begründung

- Report-Generation, Connector-/CRS-Matrizen und Runtime-Checks wurden nicht
  ausgeführt: Die Änderung ist eine Source-only-Deduplizierung und es wurde
  bewusst kein generiertes Artefakt aktualisiert.
- `make lint` wurde nicht ausgeführt: Seine erforderliche Voraussetzung
  `check-framework` kann den nicht ausgefüllten Parent-gebundenen Framework-
  Gitlink in diesem Task-Worktree nicht verwenden. Die ausgewählten Python-
  Dateien bestanden stattdessen direkte Syntax- und fokussierte
  Verhaltenskontrollen.
- Die direkten Dokumentationsprüfungen können nicht vollständig enden, solange
  derselbe Framework-Gitlink nicht ausgefüllt ist; ihre Diagnosen nannten
  weder dieses Record-Paar noch einen seiner Indizes als Fehler.
- Hosted-CI und SonarQube Cloud sind externe Delivery-Controls. Ihr Ergebnis
  muss für den aktiven PR-Head verifiziert werden, statt es in diesen
  statischen Record zu kopieren.

## Finaler Diff- und Review-Status

Die lokale Prüfung fand ausschließlich die erklärten Parent-Source-, Test- und
Traceability-Dateien. Der Task-Worktree basiert auf der oben genannten
frischen Remote-Master-Revision; die unabhängige Framework-Gitlink-Änderung
des ursprünglichen Shared-Checkouts wurde weder kopiert noch gestaged. Es wird
weder Merge noch Master-Update autorisiert oder behauptet.
