# Change Record: Scripts-Workflow- und Report-Pfadbegrenzung für SonarQube-Cloud-Sicherheitsbefunde

**Sprache:** [English](CR-20260722-sonar-scripts-path-confinement.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260722-sonar-scripts-path-confinement |
| Datum (UTC) | 2026-07-22 |
| Ursprüngliche Basis-Revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Aktuelle Master-Basis | 95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3, am 2026-07-23 ohne History-Rewrite in diesen Task-Branch gemergt |
| Tracking | Zwei Parent-only-Sicherheitsbefunde in scripts/update-github-actions-versions.py: AZ70CAr3IpeCryPNS2zi (pythonsecurity:S2083) und AZ70CAr3IpeCryPNS2zj (pythonsecurity:S8707); Follow-up-SonarQube-Cloud-Maintainability-Befunde AZ-LiaSLimiHoxpRJ2G8 (python:S3776) sowie AZ-LiaLHimiHoxpRJ2G4 bis AZ-LiaLHimiHoxpRJ2G7 (python:S5778). |
| Grenze | Parent-Updater-Source und Regressionstests sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Framework, MRTS, Gitlinks, Workflow-Konfiguration, Action-Update-Policy, Scanner-Konfiguration, Quality Gates und Suppressions bleiben unverändert. |

## Motivation und Problemstellung

Der Workflow-Updater ermittelte Kandidaten und las deren Inhalt, bevor er
bewiesen hatte, dass ihre aufgelösten Pfade innerhalb des ausgewählten
Repositorys bleiben. Ein Angreifer, der einen Symlink an einer gescannten
Workflow-Stelle platzieren kann, konnte den Updater veranlassen, ein externes
Ziel zu lesen und im Write-Modus zu verändern. Zusätzlich wurde der CLI-Wert
`--report` als unbeschränkter Ausgabepfad verwendet, sodass ein Aufrufer den
Report außerhalb des Repositorys ablegen konnte.

Die ausgewählten Befunde sind auf den Updater begrenzt. Der Critical-Befund
zum temporären Audit-Verzeichnis in `generate_repository_organization_inventory.py`
gehört bereits zum offenen Draft-PR #74; sein passender SonarCloud-Key fehlt
in dessen PR-Analyse und wird hier absichtlich nicht dupliziert.

## Akzeptanzkriterien

- Nur reguläre Workflow-Dateien, deren aufgelöste Lage unterhalb des
  ausgewählten Repository-Roots bleibt, werden gelesen oder verändert.
- Ein Reportpfad außerhalb des ausgewählten Repository-Roots einschließlich
  eines dorthin aufgelösten Symlinks wird vor jedem Report-Write abgelehnt.
- Die bestehende root-relative Workflow-Verwendung von `actions-update-report.md`
  bleibt unterstützt.
- Ein bösartiger Workflow-Symlink-Control und ein externer Reportpfad-Control
  scheitern sicher; ein legitimer Workflow-Update- und root-relativer
  Report-Control bestehen weiterhin.
- Die Workflow-Discovery bleibt unter dem SonarQube-Cloud-Grenzwert für
  kognitive Komplexität, ohne eine Containment-Prüfung zu umgehen.
- Die negativen Exception-Controls behalten ihre Eingaben und erwarteten
  Fehlschläge ohne verschachtelte Aufrufe in ihren Assertions bei.
- Beide Change-Record-Sprachen und beide Indizes bleiben gleichwertig.
- Frische SonarQube-Cloud- und Hosted-Check-Evidence für den exakten Draft-
  PR-Head einholen, bevor einer der ausgewählten Keys als behoben gilt.

## Implementierungsentscheidung und Begründung

Die Workflow-Discovery löst jetzt jeden Kandidaten auf, bevor sie ihn öffnet,
und überspringt einen Kandidaten, der ein Symlink ist, keine reguläre Datei
ist oder außerhalb des Repository-Roots aufgelöst wird. Die vorhandenen
Discovery-Routen für Root und Framework-Submodule bleiben verfügbar, aber
jeder Kandidat muss weiterhin die Parent-Root-Containment-Prüfung erfüllen.

Der Reportpfad wird über eine Hilfsfunktion aufgelöst, bevor `write_report`
aufgerufen wird. Sie akzeptiert normale relative Pfade unterhalb des aktuellen
Repository-Roots und weist absolute, Traversal- oder Symlink-Ziele außerhalb
davon mit dem vorhandenen argparse-Fehlermechanismus ab. Dies ist die engste
repository-native Grenze, weil sie sowohl den direkten CLI-Sink als auch den
bestehenden CI-Default schützt, ohne die Semantik der Action-Version-Selection
zu ändern.

Das Current-Master-Follow-up extrahiert die vorhandene
Workflow-Kandidatenentscheidung in `confined_workflow_path`. Sie bewahrt
dieselbe strikte Auflösung, Ablehnung direkter Symlinks, Regulärdatei-Prüfung
und Parent-Root-Containment, bevor ein Kandidat Workflow-Lesen oder die
Write-Mode-Replacement erreicht. Die vier negativen Exception-Controls
bereiten ihre Pfad- oder Argumentwerte vor dem Eintritt in `assertRaises` vor;
ihre abgelehnten Eingaben und erwarteten Fehlschläge bleiben unverändert.

## Geänderte Dateien

- scripts/update-github-actions-versions.py
- tests/test_update_github_actions_versions.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

- In-Memory-Python-Syntaxkompilierung des geänderten Updaters: bestanden.
- `tests.test_update_github_actions_versions`: bestanden (19 Tests).
- Fokussierte Exploit- und legitime Controls: bestanden. Ein externer
  Workflow-Symlink erzeugte keine Scan-Zeile und sein Ziel blieb unverändert;
  externe und verlinkte Reportpfade lösten eine CLI-Ablehnung aus; ein
  root-relativer Report wurde erfolgreich geschrieben.
- `git diff --check`: bestanden.

## Security-Auswirkung

Die betroffenen Source-to-Sink-Pfade sind Workflow-Discovery-Kandidaten zu
`read_text`/Write-Mode-Replacement sowie CLI-Eingabe `--report` zu
`write_report`. Die neue Invariante wird erzwungen, bevor einer der Pfade
verwendet wird: Aufgelöste Workflow-Kandidaten und Report-Destinations müssen
unterhalb des Repository-Roots bleiben, und direkte Workflow-Symlinks werden
ignoriert. Das blockiert die ausgewählten Escape-Pfade, ohne vertrauenswürdige
root-relative Workflows, Report-Format, GitHub-API-Resolution oder
Submodule-Write-Autorisierung zu ändern.

Die Regression-Controls sind so gestaltet, dass sie beim Verhalten vor der
Änderung fehlschlagen: Der frühere Scanner hätte das externe Symlink-Ziel
gelesen und verändert, und die frühere CLI hätte einen externen Report
geschrieben. Kein Security-Control wird geschwächt und es werden weder
Suppression, NOSONAR-Marker noch Scanner-Konfigurationsänderung verwendet.

Das Maintainability-Refactoring verwandelt die früheren Prüfungen nicht in
einen Best-Effort-Filter: `None` wird nur nach derselben fehlgeschlagenen
Auflösung, Symlink-, Regulärdatei- oder Root-Containment-Bedingung
zurückgegeben, die den Kandidaten zuvor übersprungen hat. Die expliziten
Security-Controls üben diese Entscheidungen weiterhin aus.

## Runtime-Evidence

Die Regression-Suite übt die echten Updater-Funktionen und die CLI-
Path-Validation mit temporären isolierten Repository-Roots aus. Für CLI-
Reporttests verwendet sie absichtlich einen leeren legitimen Workflow-Root,
sodass kein Network-GitHub-API-Lookup erforderlich ist. Das bestehende
Workflow-Parsing/-Update wird durch den Major-Ref-Update-Test abgedeckt; kein
Production-GitHub-Workflow wurde ausgeführt.

## Current-Master-Refresh und Maintainability-Follow-up

Die aktuelle Remote-`master`-Revision
`95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3` wurde mit einem normalen
Merge-Commit übernommen, nicht durch Rebase oder History-Rewrite. Ihre einzige
Auflösung war die Vereinigung dieses Change-Record-Indexeintrags mit dem
Current-Master-Eintrag. Das anschließende Source/Test-Follow-up behandelt die
fünf exakten PR-Befunde, ohne Scanner-Konfiguration, Quality Gates,
Suppressions, Workflow-Konfiguration, Framework, MRTS oder den Parent-Gitlink
zu verändern. Frische Hosted- und SonarQube-Cloud-Evidence für den exakten
Head bleibt nach dem Follow-up-Commit erforderlich.

## Bekannte Einschränkungen

Dieser Batch behandelt nur S2083 und S8707 im Updater. Er mergt oder ersetzt
Draft-PR #74 nicht, beansprucht nicht, dass der Default-Branch bereits frei
vom getrennten Critical-Befund zum Temp-Verzeichnis ist, und leert nicht den
größeren SonarQube-Cloud-Backlog.

## Verbleibende Risiken

Der Updater liest weiterhin absichtlich reguläre Workflow-Dateien innerhalb
des Repositorys und schreibt einen vom Aufrufer gewählten Report innerhalb
desselben. Das ist erforderliches Verhalten. Die neuen Containment-Checks
schützen keinen Aufrufer, der absichtlich einen unsicheren Repository-Root
auswählt; dieser Trust-Boundary liegt beim Aufrufer. Frische Hosted- und
SonarQube-Cloud-Exact-Head-Validierung bleibt erforderlich, bevor die
ausgewählten Befunde als behoben gelten.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Live-GitHub-Actions-Version-Update: Die Sicherheitsgrenze ist durch
  deterministische Unit-/CLI-Controls bewiesen, und ein Live-Update würde
  netzwerkgebundene Version-Selection erfordern, die nichts mit
  Path-Containment zu tun hat.
- Kein Framework- oder MRTS-Test und keine -Änderung: Sie sind aus diesem
  Parent-only-Task ausgeschlossen.
- Der vollständige repository-weite bilinguale Documentation-CLI-Check läuft
  lokal nicht, weil seine bekannten Fehler fehlende Links im absichtlich nicht
  initialisierten Framework-Gitlink sind; stattdessen werden die gezielte
  Change-Record-Regel und Hosted-`scaffold-lint`-Evidence verwendet.
- Vollständige Hosted-Checks und SonarQube-Cloud-PR-Analyse stehen für den
  aktuellen exakten Draft-PR-Head noch aus.

## Finaler Diff- und Review-Status

Lokale Implementierung, Source-to-Sink-Review, fokussierte Exploit-Controls
und legitime Controls sind auf dem Parent-only-Task-Branch abgeschlossen.
Draft-PR [#91](https://github.com/Easton97-Jens/ModSecurity-conector/pull/91)
bleibt offen und als Draft markiert. Frische Hosted-Checks, Sonar-Analyse und
Quality Gate für den exakten Head sind erforderlich, bevor die ausgewählten
Befunde als behoben gelten. Es werden weder Review-Freigabe noch Merge oder
Default-Branch-Änderung beansprucht oder autorisiert.
