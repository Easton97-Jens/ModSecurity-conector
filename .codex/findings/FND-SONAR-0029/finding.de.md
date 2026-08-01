# Finding FND-SONAR-0029: Common-Scripts enthalten siebenundzwanzig aktuelle SonarQube-Cloud-Befunde

**Sprache:** [English](finding.md) | Deutsch

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `sonarqube_finding` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Severity / Confidence | `P1` / `medium` / `confirmed` |
| Status / Feasibility | `verified` / `feasible_now` |
| Release-Blocker / Candidate-Integration-Blocker / sicherheitsrelevant | nein / nein / ja |
| Sonar-Inventar | 15 Security- und 12 Maintainability-Zeilen; kein Component-Duplikatblock. |

## Zusammenfassung und Scope

Der aufbewahrte Current-Master-Receipt bindet das `common/scripts/`-Inventar
an Parent-Revision `6b4aca18d390363764b96d85cd31969b9bb114a1`. Er erfasst 27
aktuelle Zeilen in den drei genannten Sources. Die Remediation ist auf lokale
Smoke-Protokoll-/Input-Grenzen, Lifecycle-Zerlegung, C++17-RAII-Cleanup,
direkte Tests und gepaarte Change Records begrenzt. Sonar-Policy, Suppression,
Exclusion, `NOSONAR`, Workflow-, Framework-/MRTS-, Gitlink- und master-
Änderungen sind ausgeschlossen.

## Aktueller Status

Frühere Resulting-Master-Evidence bewahrte den OPEN-`pythonsecurity:S8705`-
Befund `AZ7z-HdL4L5Jot4fEMXc` in
`common/scripts/run_local_runtime_smoke.py:1551`. GitHub mergte
[PR #221](https://github.com/Easton97-Jens/ModSecurity-conector/pull/221)
normal am exakten geprüften Head `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d`
und erzeugte Parent-master `3270ab5bdcc86ddab50e9be00db7611aae7fd937` um
`2026-08-01T13:36:33Z`. Alle 14 Push-Workflows für diese exakte Master-Revision
bestanden. Der direkte Resulting-Master-SonarQube-Cloud-Recheck um
`2026-08-01T13:39:56Z` meldet Originalbefund `AZ7z-HdL4L5Jot4fEMXc` um
`2026-08-01T13:37:19Z` als `FIXED/CLOSED`.

Das Finding ist `verified`. Die getrennte projektweite
`FND-SONAR-0001`-New-Security-Rating-Baseline hält das Master-Quality-Gate auf
`ERROR`; kein Scanner- oder Security-Control wurde abgeschwächt oder geändert.

## Aufbewahrte Evidence

- Eingegrenztes Sonar-Inventar (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/evidence/sonar-inventory.md`)
- Versiegelter Security-Diff-Review (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/security-diff-scan/report.md`)
- Finaler versiegelter Security-Diff-Review (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/security-diff-scan-terminal-amendment/report.md`)
- Resulting-Master-SonarQube-Cloud-Receipt (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/evidence/post-merge-master-sonar-20260801.md`)
- PR-#221-Exact-Head-Verifikation (`/root/git/ModSecurity-conector/.codex/runs/parent-common-sonar-remediation-20260801/evidence/pr221-exact-head-verification.md`)
- PR-#221-Merge-/Master-Verifikation (`/root/git/ModSecurity-conector/.codex/runs/parent-common-sonar-remediation-20260801/evidence/pr221-merge-master-verification.md`)

## Historie

- `2026-08-01T10:40:00Z`: Finding aus dem aktuellen, revisionsgebundenen
  Scope-Receipt allokiert; bei der Allokation existierten kein Commit, PR,
  Merge, Scanner-Control- oder master-Change.
- `2026-08-01T10:54:10Z`: Der initiale Draft-PR-#218-Sonar-Readback hatte 12
  task-eigene Zeilen und 0,0 % New-Code-Duplizierung. Das lokale Amendment
  besitzt 56 bestandene fokussierte Tests, einen C++17-Kompilierungscontrol
  und einen zweiten versiegelten Security-Review; frische Hosted-Evidence für
  den geänderten Head steht aus.
- `2026-08-01T11:16:50Z`: Exact-Head-SonarQube Cloud liefert null offene
  Zeilen, Quality Gate `OK`, null neue Violations und 0,0 % New-Code-
  Duplizierung; alle anwendbaren GitHub-Checks bestanden. Das Finding ist
  `fixed`; ein Merge wurde weder autorisiert noch ausgeführt.
- `2026-08-01T11:36:41Z`: PR #218 wurde als
  `a7e2e70f307c91bc3da702b7240a1c4218cb2b79` gemergt und alle 14
  Resulting-Master-Workflows bestanden. Die direkte Resulting-Master-
  SonarQube-Cloud-Abfrage bewahrt OPEN-`pythonsecurity:S8705`
  `AZ7z-HdL4L5Jot4fEMXc` in Zeile 1551. Der statische Review hat keine
  unterstützte HTTP-zu-CLI-Grenze nachgewiesen, deshalb ist der Kandidat
  `triaged` statt akzeptiert, fixed, verified oder geschlossen.
- `2026-08-01T13:12:18Z`: exakter Draft-PR-#221-Head
  `482ba035ed53b3668009b7158c656214d6924e6f` verifiziert private reguläre
  Evaluator-Inputs, verwirft unsichere Linker-/Ownership-Fälle vor
  Process-Erzeugung und bindet die verifizierte ausgewählte Library-Datei direkt
  ein. Anwendbare Hosted-Checks bestanden; SonarQube Cloud meldet null offene
  PR-Issues, null New-Violations und `0,0 %` New-Code-Duplikation; der
  vollständige Security-Diff-Review besitzt null reportable Befunde. Das
  Finding ist `fixed` und wartet vor `verified` oder `closed` auf autorisierten
  Merge und Resulting-Master-Reproduktion.
- `2026-08-01T13:39:56Z`: GitHub mergte exakten PR-#221-Head
  `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d` normal als Resulting Master
  `3270ab5bdcc86ddab50e9be00db7611aae7fd937`; alle 14 Exact-Master-Workflows
  bestanden. Der direkte SonarQube-Cloud-Recheck meldet Original-
  `AZ7z-HdL4L5Jot4fEMXc` / `pythonsecurity:S8705` um `2026-08-01T13:37:19Z`
  als `FIXED/CLOSED`. Das Finding ist `verified`; `FND-SONAR-0001` bleibt
  getrennt.
