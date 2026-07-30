# Change Record: Parent-CI-Runtime-Cache-Vier-Spalten-Markdown-Separator für SonarQube Cloud S1192

**Sprache:** [English](CR-20260730-sonar-ci-runtime-cache-separator.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-ci-runtime-cache-separator` |
| Datum (UTC) | `2026-07-30` |
| Basis-Revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` |
| Grenze | Ausschließlich Parent `ci/evidence/reports/update-runtime-reports.py`, sein direkter Parent-Präsentationstest, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine `scripts/`, kein Framework, kein MRTS, kein Gitlink, keine Product-Source, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Aktueller OPEN-`python:S1192`-Befund `AZ7b3darcO69wzd-_jHY` für vier identische `"|---|---|---|---|"`-Literale an den Zeilen 183, 207, 211 und 214. |

## Motivation und Problemstellung

Der Runtime-Cache-Report-Renderer gibt denselben Vier-Spalten-Markdown-Tabellenseparator für die Component-Cache-Tabelle und jede der drei Cache-Index-Tabellen aus. SonarQube Cloud meldet dieses wiederholte unveränderliche Literal als `python:S1192`.

## Akzeptanzkriterien

- Die vier semantisch identischen Vier-Spalten-Tabellenseparatoren verwenden eine gemeinsame private Modulkonstante.
- Der Component-Cache-Report behält seinen bestehenden Header, eine strukturelle Separatorzeile, Zeilen-Layout und Payload-Rendering.
- Der Cache-Index-Report behält seine Manifest-, Component- und Important-File-Header, drei strukturelle Separatorzeilen, Zeilen-Layouts und Feldreihenfolge.
- Der exakte PR-Head muss später null neue SonarQube-Cloud-Issues, null neue duplizierte Zeilen und `0.0%` New-Code-Duplizierung erhalten, ohne eine Kontrolle zu schwächen.

## Implementierungsentscheidung und Begründung

`FOUR_COLUMN_TABLE_SEPARATOR = "|---|---|---|---|"` liefert jetzt die vier unveränderten Renderer-Positionen. Die direkte Presentation-Regression lädt das Modul ohne Cache-Lesevorgänge oder Report-Schreibvorgänge, übt befüllte Component-/Cache-Index-Payloads aus und prüft die literalen strukturellen Zeilen sowie repräsentative gerenderte Zeilen. Bestehende Cache-Auswahl, JSON-Lesen, Provenance-Metadaten, Report-Root-Prüfungen, Ausgabe-Pfade und Rendering-Reihenfolge bleiben unverändert.

## Geänderte Dateien

- `ci/evidence/reports/update-runtime-reports.py`
- `tests/test_report_presentation_literals.py`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-cache-separator.md`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-cache-separator.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Direkter SonarQube-Cloud-`api/issues/search`-Readback für `AZ7b3darcO69wzd-_jHY` | bestanden: ein OPEN-`python:S1192`-Befund identifiziert die vier Literal-Positionen. |
| `python -B -m unittest tests.test_report_presentation_literals` | bestanden: 4 Tests, einschließlich der befüllten Component-Cache- und Cache-Index-Layout-Regression. |
| Python-AST-Parse des geänderten Renderers und Tests | bestanden. |
| `git diff --check` | bestanden. |
| Fokussierte Source-/Control-/Sink-Security-Preflight | bestanden: vollständiger Codex-Security-Workflow ist `not_applicable`; kein plausibler diff-induzierter Befund. |
| `make check-bilingual-docs` und `make check-doc-links` | `blocked_external_dependency`: ihre einzigen Diagnosen sind bereits bestehende Links zum fehlenden Worktree-Framework-Gitlink; direkter Change-Record-Validator und 21 Bilingual-Checker-Unittests bestanden. |
| `env VERIFIED_RUN_ROOT=<task-owned external root> make lint` | `blocked_external_dependency`: CI-Shell-Syntax und die Kompilierung aller `ci/*.py` bestanden, bevor ein breiter Test den fehlenden Worktree-Framework-Checker importiert. |

## Security-Auswirkung

Der bestehende Renderer verarbeitet Cache-abgeleitete Werte und erreicht einen Safe-Root-begrenzten Generated-Report-Write-Pfad. Diese Änderung führt nur einen privaten statischen Separator außerhalb des Payload-abgeleiteten Flows ein; sie ändert weder Cache-Root, Environment-Input, Path-Control, JSON-Parsing, Ausgabeziel, Subprozess, Privileg noch Provenance-Verhalten. Die Presentation-Regression prüft strukturelle Separatorzeilen, sodass ein Payload-Substring die Tabellen-Grenz-Kontrolle nicht erfüllen kann. Es wird kein Security-Befund beansprucht, unterdrückt oder geschlossen.

## Runtime-Evidence

Es werden keine Component-Vorbereitung, keine Connector-Runtime, keine netzwerkgestützte Matrix, kein Cache-Lesen und kein Report-Schreiben beansprucht. Die direkte In-Process-Renderer-Regression ist die legitime Behavior-Control für diese byte-erhaltende Presentation-Refaktorierung.

## Bekannte Einschränkungen

Der fokussierte Test verwendet repräsentative befüllte In-Memory-Payloads; er übt nicht jedes Cache-Artefakt oder den bestehenden Report-Write-Workflow aus. Das ist für eine statische Literaländerung beabsichtigt und stellt keine Authentizität der bereits bestehenden Cache-JSON-Inputs fest. Die breiten Make-Dokumentations- und Lint-Targets können in diesem isolierten Worktree nicht enden, weil sein Framework-Gitlink absichtlich fehlt; keines meldet einen geänderten Task-Datei-Defekt.

## Verbleibende Risiken

Der exakte Hosted-PR-Head muss noch das Entfernen des ausgewählten S1192-Receipts mit bestandenem SonarQube-Cloud-Quality-Gate, null neuen Issues, null neuen duplizierten Zeilen und `0.0%` New-Code-Duplizierung belegen. Lokale Prüfungen können diese Hosted-Evidence nicht ersetzen.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Component-Build, Package-Download, keine Connector-Runtime und keine Netzwerk-Matrix wurden ausgeführt: Die Änderung ist eine byte-erhaltende Pure-Renderer-Literalextraktion.
- Kein Framework, MRTS, Gitlink, `.github/`, keine `scripts/` und keine unverbundene Parent-Source wurden geändert. Breite Checks, die Framework-Source benötigen, sind als blockiert statt als umgangen erfasst, weil der Nutzer diese Kampagne auf den Parent-CI-Scope eingeschränkt hat.
- Hosted-GitHub-Actions-, SonarQube-Cloud-PR-Analyse-, Review- und Merge-Evidence werden nicht lokal hergeleitet und benötigen den späteren exakten PR-Head.

## Finaler Diff- und Review-Status

Der lokale Scoped-Diff enthält eine private Konstante, vier Referenz-Ersetzungen, eine direkte Presentation-Regression und dieses Traceability-Paar. Der fokussierte finale Source-/Test-Diff-Review ist `already_safe`: Kein Payload-, Path-, Command-, Parser-, Privileg- oder Report-Write-Control änderte sich. Dieses Record beansprucht keinen Commit, Push, Pull Request, Hosted-Check, Review oder Merge; diese Fakten werden erst nach Beobachtung erfasst.
