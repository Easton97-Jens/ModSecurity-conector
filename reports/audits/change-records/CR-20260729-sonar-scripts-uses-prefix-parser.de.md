# Change Record: Deterministischer Parent-GitHub-Actions-`uses:`-Prefix-Parser für SonarQube Cloud S8786

**Sprache:** [English](CR-20260729-sonar-scripts-uses-prefix-parser.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-scripts-uses-prefix-parser` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Grenze | Parent `scripts/update-github-actions-versions.py`, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `ci/`-Source, kein `.github/`-Workflow, keine Test-Source, kein Framework, kein MRTS, kein Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Aktueller `python:S8786`-Befund `AZ8hz9F2Ua5zTy8Lzy9S`; die erste PR-Analyse meldete außerdem den PR-lokalen `python:S1192`-Befund `AZ-sKgRKKem7UxiInyxV` für den nun wiederholten Mapping-Key `uses:`. Das Follow-up zentralisiert diesen Key. Das getrennte Content-Taint-Signal `AZ70CAr3IpeCryPNS2zi` bleibt ohne Suppression und wird nicht als Behebung dieses Patches beansprucht. |

## Motivation und Problemstellung

Der Parent-GitHub-Actions-Updater verwendete einen verankerten Python-regulären Ausdruck, um Workflow-`uses:`-Prefixes zu erkennen. SonarQube Cloud meldet ihn wegen möglichem superlinearem Backtracking als `python:S8786`. Diese enge Behebung ersetzt ausschließlich diese Prefix-Aufteilung durch einen deterministischen Zeichenscan und bewahrt unterstütztes zeilenbasiertes Verhalten sowie Update-/Write-Kontrollen.

## Akzeptanzkriterien

- Die Prefix-Erkennung ist für lange repository-kontrollierte Workflow-Zeilen deterministisch und linear.
- Das bestehende unterstützte `uses:`-Parsing bleibt für normale, quotierte, Whitespace-, Blank-Value-, fehlgeformte und Dynamic-Reference-Grenzfälle äquivalent.
- Bestehende Local-, Docker-, Dynamic-, SHA-pinned-, Workflow-Path-/Symlink- und Write-enabled-Kontrollen bleiben unverändert und bestehen die direkte Updater-Suite.
- Der exakte Draft-PR-Head muss frische SonarQube-Cloud-Evidence mit null neuen Issues und `0.0%` New-Code-Duplizierung erhalten, ohne Regel-, Profil-, Exclusion-, Suppression-, False-Positive-Disposition- oder Quality-Gate-Änderung.
- Dieser Datensatz beansprucht Delivery-Fakten erst nach ihrer Beobachtung am finalen Head.

## Implementierungsentscheidung und Begründung

`_uses_value_rest()` scannt jetzt eine physische Workflow-Zeile von links nach rechts: führender Whitespace, ein optionaler List-Marker, literales `uses:` und folgender Whitespace werden verarbeitet, bevor der exakte Prefix und der nichtleere Rest zurückgegeben werden. Es ersetzt den verankerten Prefix-regulären Ausdruck, ohne einen YAML-Parser hinzuzufügen, `_parse_uses_value()` zu ändern oder akzeptierte Prefixes zu erweitern.

`parse_uses_line()` bewahrt den bisherigen Dynamic-Reference-Fallback-Prefix.
`USES_MAPPING_KEY` formuliert denselben Mapping-Key nach SonarQube Clouds
Hinweis auf die vier identischen Parser-Literale nur einmal für Scanner und
Fallback. Der Patch ändert weder Action-Eligibility, Semantic-Version-Lookup,
Workflow-Path-Containment, Submodule-Handling, Report-Paths, Netzwerk-Requests
noch die Anwendung von Writes. Es wird keine versionierte Test-Source geändert,
weil der aktuelle Nutzer die Produkt-Remediation auf `ci/` und `scripts/`
eingeschränkt hat; die bestehende direkte Suite und ein task-eigener nicht
schreibender Vergleichsharness liefern Regression-Evidence.

## Geänderte Dateien

- `scripts/update-github-actions-versions.py`
- `reports/audits/change-records/CR-20260729-sonar-scripts-uses-prefix-parser.md`
- `reports/audits/change-records/CR-20260729-sonar-scripts-uses-prefix-parser.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Fokussierte bestehende Updater-Suite: `python -B -m unittest discover -s tests -p test_update_github_actions_versions.py -v` | bestanden: 25 Tests, einschließlich quotierter/ungequoteter Erhaltung, fehlgeformter Values, Dynamic/Local/Docker/SHA-Skips, Workflow-Symlink-Ablehnung und Write-Kontrollen. |
| Task-eigener nicht schreibender Parser-Vergleich gegen `origin/master` | bestanden: normale, Long-Whitespace-, Blank-Value- und Dynamic-Reference-Fälle erzeugten identische Parser-Ergebnisse. |
| `python -P -m py_compile scripts/update-github-actions-versions.py` | bestanden. |
| `git diff --check origin/master -- scripts/update-github-actions-versions.py` | bestanden. |
| Erste Exact-Head-SonarQube-Cloud-Analyse | Quality Gate bestanden und New-Code-Duplizierung bei null Zeilen / `0.0%`, aber der PR blieb korrekt unverifiziert, weil er einen neuen `python:S1192`-Befund für die vier Parser-Kopien von `uses:` meldete. Es wurden weder Regel, Profil, Exclusion, Suppression, False-Positive-Disposition noch Quality Gate geändert. |
| Follow-up-Konstantenextraktion und lokaler Wiederholungslauf | bestanden: `USES_MAPPING_KEY` ersetzte ausschließlich die vier identischen Mapping-Key-Literale des Parsers; die 25-Test-Updater-Suite, der nicht schreibende Parser-Vergleich, `py_compile` und `git diff --check` bestanden erneut. |
| Vollständiger Branch-Diff-Codex-Security-Contract | bestanden: Delegierter Full-File-Review ergab für `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc..99629c1e8fac38caa79e4c7d3cd352052d78feed` null reportable Candidates; versiegelter Snapshot-Digest `codex-security-snapshot/v1:sha256:74e566917334508fc229bfd7002116257ffdc9b32c51c85e3084be6cef28360d`. Der frühere Parser-Scan bleibt nur als abgelöste Evidence erhalten. |
| Bilinguale Change-Record- und Link-Validierung | bestanden: eingeschränkte Heading-/Table-/Identity-/Language-Switch-/Index-Checks. Root-Checks sind blocked_external_dependency: der direkte bilinguale Checker endete mit `1`, `make check-bilingual-docs` mit `2` und `make check-doc-links` mit `2`, ausschließlich weil 20 vorhandene Framework-Gitlink-Targets in diesem Task-Worktree fehlen; keines meldete dieses Paar oder seine Indizes. |
| Draft-PR-Erstellung und erste Exact-Head-Beobachtung | bestanden: Draft-PR [#165](https://github.com/Easton97-Jens/ModSecurity-conector/pull/165) zielt auf `master`; lokaler, Remote- und PR-Head waren `f5f74f203efb834edb68ff1a13fb9c46a86f1352`. CodeQL-, OSV-, Apache- und Lighttpd-Checks waren in progress; der installierte `gh`-Client unterstützt `pr checks --json` nicht, daher wurde der Status über `gh pr view` `statusCheckRollup` beobachtet. |

## Security-Auswirkung

Workflow-Text ist repository-kontrollierter Input, der letztlich einen maintainer-ausgelösten Workflow-Datei-Write erreichen kann. Der vollständige Branch-Diff-Review las den Updater, direkte Tests und Repository-Security-Guidance. Er fand keinen neuen Source-to-Sink-Pfad, keine geschwächte Kontrolle und keinen neuen Filesystem-, Network- oder Process-Sink: fehlgeformte Values schlagen weiterhin fail closed fehl, nicht berechtigte References werden weiter übersprungen, und nur begrenzte Non-Symlink-Workflow-Dateien können bei explizit aktivem Write-Mode geschrieben werden.

Das getrennte Content-Taint-Signal ist kein Path-Injection-Proof: feste Discovery-Globs sowie Resolved-Root-/Non-Symlink-/Regular-File-Checks begrenzen den Writer, und der Updater ist ein Default-Branch-Schedule/Manual-Pfad. Es bleibt ohne Suppression. Dieser Datensatz beansprucht nicht, dass eine Security-Vulnerability behoben wurde.

## Runtime-Evidence

Es wurde keine Connector- oder Host-Runtime-Evidence erhoben oder beansprucht. Die Änderung ist auf einen Maintenance-Script-Parser begrenzt. Die direkte Unit-Suite und der nicht schreibende Vergleichsharness üben den Parser und seine kontrollierte Temporary-Workflow-Write-Grenze ohne netzwerkgestütztes GitHub-Actions-Update aus.

## Bekannte Einschränkungen

Der Updater bleibt ein absichtlich unterstützter zeilenbasierter `uses:`-Parser und kein vollständiger YAML-Parser. Bestehende Flow-Style- oder Block-Scalar-Grenzen gehen diesem Diff voraus und sind kein neu unsicherer Rewrite-Pfad. Der breite Parent-SonarQube-Cloud-Backlog liegt außerhalb dieses isolierten ersten Batches.
Vollständige Dokumentations-/Link-Checks bleiben wegen vorhandener fehlender Framework-Gitlink-Targets in diesem task-eigenen Worktree blockiert; dieser Patch stellt sie nicht wieder her, befüllt sie nicht und ändert sie nicht.

## Verbleibende Risiken

Der lokale Vergleichskorpus ist starke Regression-Evidence, aber kein Beweis für jede YAML-Form. Hosted-Analyse und -Checks müssen den finalen exakten PR-Head bewerten, bevor S8786 als behoben oder Delivery als verifiziert gilt. Die Aufgabe macht keine Permission-, Token-, Workflow-, Scanner- oder Suppression-Änderung, um dieses Ergebnis zu erzwingen.

## Nicht ausgeführte Prüfungen mit Begründung

- Ruff und Pyright sind in der ausgewählten lokalen Umgebung nicht installiert; sie wurden nicht allein für diese enge Remediation installiert.
- Es wurde kein Live-Updater-Lauf gegen Repository-Workflows durchgeführt, weil er netzwerkgestützte Auflösung verwendet und Workflow-Dateien schreiben kann; deterministische Tests und der nicht schreibende Harness sind die sichere lokale Grenze.
- Es wurde kein Framework-, MRTS-, Gitlink-, `.github/`- oder anderer unverbundener Parent-Source-Check ausgeführt oder geändert, weil der Nutzer diese Aufgabe auf `ci/` und `scripts/` begrenzt hat.
- Exact-Head-GitHub-Actions-, SonarQube-Cloud-, Review- und PR-Evidence benötigen den gepushten Draft-PR-Head und werden nicht lokal hergeleitet.

## Finaler Diff- und Review-Status

Der initiale Implementierungs- und Traceability-Commit ist `f5f74f203efb834edb68ff1a13fb9c46a86f1352` auf `agent/parent-scripts-uses-parser-20260729`. Er erzeugte Draft-PR #165 gegen `master`; die erste Hosted-Analyse zeigte anschließend trotz bestandenem Quality Gate und null New-Code-Duplizierung einen task-eigenen S1192-Befund. Source-Follow-up-Commit `99629c1e8fac38caa79e4c7d3cd352052d78feed` führt ausschließlich `USES_MAPPING_KEY` ein und entfernt dieses wiederholte Parser-Literal. Das erforderliche Record-Paar und die Indizes sind nur Delivery-Traceability. Der aktuelle vollständige Branch-Diff-Security-Scan ist ohne reportable Finding gültig.

Dieses Follow-up aktualisiert das Record-Paar, um den beobachteten Sonar-Status und die exakte Source-Security-Evidence festzuhalten. Es erzeugt absichtlich einen neuen PR-Head; daher müssen alle Hosted-Checks, SonarQube-Cloud-Analyse, Review- und Merge-Evidence für diesen neuen SHA erneut eingeholt werden. Es werden kein aktueller Hosted-Pass, kein Approval, kein Ready-for-Review-Status und kein Merge beansprucht.
