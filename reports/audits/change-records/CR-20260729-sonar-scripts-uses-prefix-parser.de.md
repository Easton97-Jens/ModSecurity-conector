# Change Record: Deterministischer Parent-GitHub-Actions-`uses:`-Prefix-Parser für SonarQube Cloud S8786

**Sprache:** [English](CR-20260729-sonar-scripts-uses-prefix-parser.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-scripts-uses-prefix-parser` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Grenze | Parent `scripts/update-github-actions-versions.py`, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `ci/`-Source, kein `.github/`-Workflow, keine Test-Source, kein Framework, kein MRTS, kein Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Aktueller `python:S8786`-Befund `AZ8hz9F2Ua5zTy8Lzy9S`; das getrennte Content-Taint-Signal `AZ70CAr3IpeCryPNS2zi` bleibt ohne Suppression und wird nicht als Behebung dieses Patches beansprucht. |

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

`parse_uses_line()` bewahrt den bisherigen Dynamic-Reference-Fallback-Prefix. Der Patch ändert weder Action-Eligibility, Semantic-Version-Lookup, Workflow-Path-Containment, Submodule-Handling, Report-Paths, Netzwerk-Requests noch die Anwendung von Writes. Es wird keine versionierte Test-Source geändert, weil der aktuelle Nutzer die Produkt-Remediation auf `ci/` und `scripts/` eingeschränkt hat; die bestehende direkte Suite und ein task-eigener nicht schreibender Vergleichsharness liefern Regression-Evidence.

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
| Vollständiger Current-Diff-Codex-Security-Contract | bestanden: Full-File-Review ergab null reportable Candidates; versiegelter Snapshot-Digest `codex-security-snapshot/v1:sha256:3cd05aa14c03ed2ab1ab7cdf1c15cf2d80327b370762c050f2e53fd98477203a`. |
| Bilinguale Change-Record- und Link-Validierung | bestanden: eingeschränkte Heading-/Table-/Identity-/Language-Switch-/Index-Checks. Root-Checks sind blocked_external_dependency: der direkte bilinguale Checker endete mit `1`, `make check-bilingual-docs` mit `2` und `make check-doc-links` mit `2`, ausschließlich weil 20 vorhandene Framework-Gitlink-Targets in diesem Task-Worktree fehlen; keines meldete dieses Paar oder seine Indizes. |
| Draft-PR-Erstellung und erste Exact-Head-Beobachtung | bestanden: Draft-PR [#165](https://github.com/Easton97-Jens/ModSecurity-conector/pull/165) zielt auf `master`; lokaler, Remote- und PR-Head waren `f5f74f203efb834edb68ff1a13fb9c46a86f1352`. CodeQL-, OSV-, Apache- und Lighttpd-Checks waren in progress; der installierte `gh`-Client unterstützt `pr checks --json` nicht, daher wurde der Status über `gh pr view` `statusCheckRollup` beobachtet. |

## Security-Auswirkung

Workflow-Text ist repository-kontrollierter Input, der letztlich einen maintainer-ausgelösten Workflow-Datei-Write erreichen kann. Der vollständige Current-Diff-Review las den Updater, direkte Tests und Repository-Security-Guidance. Er fand keinen neuen Source-to-Sink-Pfad, keine geschwächte Kontrolle und keinen neuen Filesystem-, Network- oder Process-Sink: fehlgeformte Values schlagen weiterhin fail closed fehl, nicht berechtigte References werden weiter übersprungen, und nur begrenzte Non-Symlink-Workflow-Dateien können bei explizit aktivem Write-Mode geschrieben werden.

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

Der initiale Implementierungs- und Traceability-Commit ist `f5f74f203efb834edb68ff1a13fb9c46a86f1352` auf `agent/parent-scripts-uses-parser-20260729`. Er erzeugte Draft-PR #165 gegen `master`; bei der ersten Beobachtung stimmten local HEAD, der Remote-Branch und der PR-Head exakt überein. Der Source-Diff bleibt auf den deterministischen Parser-Ersatz begrenzt; das erforderliche Record-Paar und die Indizes sind nur Delivery-Traceability. Ein vollständiger Current-Diff-Security-Scan ist mit keiner reportable Finding gültig.

Dieses Follow-up ändert ausschließlich die zwei Change-Record-Dateien, um den beobachteten initialen PR-Zustand aufzubewahren. Es erzeugt absichtlich einen neuen PR-Head; daher müssen alle Hosted-Checks, SonarQube-Cloud-Analyse, Review- und Merge-Evidence für diesen neuen SHA erneut eingeholt werden. Es werden kein aktueller Hosted-Pass, kein Approval, kein Ready-for-Review-Status und kein Merge beansprucht.
