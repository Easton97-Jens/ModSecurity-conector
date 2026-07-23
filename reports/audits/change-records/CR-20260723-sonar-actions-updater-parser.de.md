# Change Record: GitHub-Actions-Updater-Parser- und Komplexitätsbehebung

**Sprache:** [English](CR-20260723-sonar-actions-updater-parser.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260723-sonar-actions-updater-parser` |
| Datum (UTC) | `2026-07-23` |
| Basis-Revision | `5b8db00d44ab24f3a9f4216a00f7edee977b6898` |
| Grenze | Ausschließlich Parent-`scripts/update-github-actions-versions.py`, der zugehörige Parent-Unit-Test, dieses englische/deutsche Change-Record-Paar und die beiden Indizes; Framework, MRTS und beide Gitlinks bleiben unverändert. |
| Finding-Verknüpfung | `FND-SONAR-0029` (aufbewahrt, Import ausstehend); `AZ8hz9F2Ua5zTy8Lzy9S`, `AZ70CAr3IpeCryPNS2zf`, `AZ70CAr3IpeCryPNS2zc` und `AZ70CAr3IpeCryPNS2zg`. |

## Motivation und Problemstellung

Der GitHub-Actions-Updater nutzte einen regulären Ausdruck mit optionalem Quote
und Backreference zum Parsen von Workflow-`uses:`-Werten. SonarQube Cloud
meldet dies wegen möglichem superlinearem Backtracking als `python:S8786`.
Im selben Updater bestehen außerdem zwei `python:S3776`-Befunde zur kognitiven
Komplexität und ein `python:S1192`-Befund zu einem duplizierten Status. Die
Implementierung benötigt eine fokussierte Behebung, die unterstützte
Workflow-Syntax und bestehende Update-/Write-Kontrollen unverändert bewahrt.

## Akzeptanzkriterien

- Die vier aufgeführten SonarQube-Cloud-Befunde werden durch eine frische
  Exact-Draft-PR-Analyse ohne Suppression, Exclusion, Issue-Disposition,
  Regel-/Profil- oder Quality-Gate-Änderung entfernt.
- Ungequotete, einfach quotierte und doppelt quotierte aktualisierbare
  `uses:`-Werte bewahren ihre Kommentare/Suffixe, während ihre Referenz
  aktualisiert wird.
- Fehlgeformte Values mit fehlendem oder nicht passendem Quote werden nicht
  geparst oder umgeschrieben.
- Bestehendes Dynamic-, Local-, Docker-, SHA-pinned-, Symlink-Containment- und
  Report-Path-Containment-Verhalten besteht weiterhin seine fokussierten
  Parent-Tests.
- Der finale Task-Branch ist ein ungemergter Draft PR auf Basis des
  aufgezeichneten aktuellen `master`, mit Exact-Head-Checks und
  SonarQube-Cloud-Evidence, bevor er als verifiziert beschrieben wird.

## Implementierungsentscheidung und Begründung

`_parse_uses_value` scannt jetzt einen einzelnen Workflow-Wert von links nach
rechts und gibt Quote-Marker, Value und Suffix nur zurück, wenn ein passendes
Quote vorhanden ist. Es ersetzt den optionalen Quote-/Backreference-regulären
Ausdruck und bewahrt den bestehenden Dynamic-Expression-Fallback.

Kleine private Helper trennen Report-Row-Erzeugung, Nicht-Update-Skip-
Klassifikation, Semver-Auflösung, Scannen einer einzelnen Datei und Anwendung
von Replacements. Dies reduziert die kognitive Komplexität von `analyze_uses`
und `scan_workflows`, ohne ihre öffentlichen Interfaces oder Update-Reihenfolge
zu ändern. `SKIPPED_DYNAMIC` ist das eine gemeinsame Literal an allen drei
Dynamic-Action-Statusstellen.

## Security-Auswirkung

Die Sicherheitsgrenze wurde bewertet, weil Workflow-Text einen möglichen
Workflow-Datei-Write erreicht. `update-actions-versions.yml` läuft nur
zeitgesteuert oder durch manuellen Dispatch und nur auf dem Default-Branch;
`check-actions-versions.yml` ist ebenfalls zeitgesteuert/manuell und nutzt
read-only Contents-Permission. Es wurde kein untrusted Pull-Request-/Event-Pfad
oder Angreifer-Precondition mit geringeren Rechten gezeigt. Die S8786-
Security-Hypothese hat deshalb das `fix-finding`-Ergebnis `no_change`, nicht
eine behauptete Security-Remediation.

Der deterministische Parser entfernt die vom Scanner gemeldete Backreference,
während bestehende Workflow-Symlink-, Report-Path-, Dynamic/Local/Docker/SHA-
und Protected-Submodule-Kontrollen bewahrt werden. Kein Security-Control,
Token-Handling, Permission, Sonar-Regel, Quality Gate oder CI-Schutz wird
geschwächt.

## Geänderte Dateien

- `scripts/update-github-actions-versions.py`
- `tests/test_update_github_actions_versions.py`
- `reports/audits/change-records/CR-20260723-sonar-actions-updater-parser.md`
- `reports/audits/change-records/CR-20260723-sonar-actions-updater-parser.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Fokussierte Baseline: `rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/20260723T134220Z-sonarqube-parent-backlog-remediation.xZluLr/tmp/scripts-actions-updater.2c1xcV /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_update_github_actions_versions` | bestanden: 19 Tests vor der Änderung. |
| In-Memory-AST-Parse der geänderten Source und des Tests | bestanden: 2 Dateien. |
| Fokussierter Post-Change-Unit-Test mit demselben expliziten Parent-Interpreter und task-eigenem `TMPDIR` | bestanden: 25 Tests, einschließlich Parser-Kompatibilitäts-, Lookup-Fehler-, No-Downgrade-, Protected-Submodule- und Read-only-Write-Kontrollen. |
| Differenzieller Parservergleich gegen Basis `5b8db00` über 132 Kombinationen aus Quotes, ungequoteten, Dynamic-, fehlgeformten, Local-, Docker- und Suffix-Formen | bestanden: 132 Fälle, null Unterschiede. |
| Begrenzte Pre-Change-Kontrolle für fehlgeformte Eingabe | gab für einen 65.547-Zeichen-Value mit fehlendem Quote in 5.655 ms `None` zurück; dies ist eine begrenzte Performance-Beobachtung, keine universelle ReDoS-Behauptung. |
| `git diff --check` | bestanden. |
| Checkout-Artefakt-Scan für `*.pyc` | bestanden: keine Dateien gefunden. |
| `tests.test_bilingual_docs` mit dem expliziten Parent-Interpreter | bestanden: 11 Tests. |
| `make check-bilingual-docs` | ausschließlich durch 20 vorhandene fehlende Framework-Gitlink-Targets blocked_environment; keine task-eigene Change-Record-Diagnose bleibt. |
| `make check-doc-links` | ausschließlich durch dieselben vorhandenen fehlenden Framework-Gitlink-Targets blocked_environment. |

## Runtime-Evidence

Es wurde keine Connector- oder Host-Runtime-Evidence erhoben oder beansprucht.
Die Änderung ist auf einen Repository-Workflow-Updater-Parser und seine
Unit-Level-Temporary-Workflow-Fixtures begrenzt. Die fokussierten Tests üben die
reale Parser-zu-Scan-zu-Write-Grenze mit einem Fake-Resolver und task-eigenen
Temporary-Roots aus.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Live-Updater-Lauf gegen Repository-Workflows: Er nutzt netzwerkgestützte
  GitHub-API-Auflösung und kann einen Report erzeugen oder Workflow-Dateien
  schreiben; die deterministischen Unit-Fixtures sind deshalb die ausgewählte
  sichere Regression-Grenze.
- Kein Framework- oder MRTS-Check und keine -Änderung: Beide liegen außerhalb
  des Parent-only-Scopes.
- Exact-Head-GitHub-Actions-, SonarQube-Cloud-, Review- und PR-Evidence
  existieren erst nach einem Push eines task-eigenen Draft PR und werden nicht
  lokal hergeleitet.

## Bekannte Einschränkungen

Der breite SonarQube-Cloud-Parent-Backlog bleibt offen. Vollständige
Dokumentationskommandos werden voraussichtlich die vorhandenen fehlenden
Framework-Gitlink-Targets melden; dieser Umgebungszustand wird nicht durch die
Parent-only-Änderung umgangen.

## Verbleibende Risiken

Der Parser-Kompatibilitätsvergleich ist ein fokussierter Korpus, kein Beweis für
jede mögliche YAML-Form; der Updater behandelt weiterhin absichtlich die
unterstützte `uses:`-Syntax statt als YAML-Parser zu agieren. SonarQube Cloud
und Hosted-Checks müssen den exakten Draft-PR-Head noch analysieren, bevor die
vier Befunde verifiziert sind. Kein Merge ist autorisiert.

## Finaler Diff- und Review-Status

Der Scoped-Diff wurde vor dem Staging geprüft. Die lokale Source-, fokussierte
Test-, differenzielle Parser- und Bilingual-Validierung ist abgeschlossen und
der private Finding-Record ist aufbewahrt. Commit
`03b487f88a98ec71edf438e8ac347dd76b370f69` wurde auf der genannten Basis
erstellt; normaler Push, Draft-PR-Erstellung und Exact-Head-Hosted-Analyse
bleiben erforderlich und werden hier nicht behauptet.
