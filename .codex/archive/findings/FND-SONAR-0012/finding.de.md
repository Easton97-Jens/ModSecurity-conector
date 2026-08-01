# FND-SONAR-0012 — Die SonarQube-Cloud-Validator-Signale von MRTS-PR #3 sind durch den gemergten PR #4 behoben

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-SONAR-0012` |
| Kategorie | `sonarqube_finding` |
| Repository / Ownership | `mrts` / `mrts` |
| Priorität / Schwere / Konfidenz | `P1` / `not_applicable` / `confirmed` |
| Status / Machbarkeit | `closed` / `feasible_now` |
| Release-Blocker / Security-Relevanz | `false` / `true` |
| Betroffene Revisionen | historischer PR #3 `e8bb04edf9e0cea03786e834c1f516f367d6136a`; Remediation-PR #4 `9cdfd4136286014b244f8fecfb99701681fecae4`; aktueller main `615b13bacbd008562c17408246c41ab27dca3104` |

## Zusammenfassung, Verhalten und Auswirkung

Der historische Draft-MRTS-PR-#3-Head
`e8bb04edf9e0cea03786e834c1f516f367d6136a` scheiterte an
`new_security_rating`: Actual `4` (D), erforderlich `1` (A), mit sieben
aufgabeneigenen Signalen in `tools/validate-governance.py`.

MRTS-PR #4 mit Head `9cdfd4136286014b244f8fecfb99701681fecae4` remedierte
diese Bedingung, bestand Analyze (python), CodeQL, Python-3.14-Governance und
SonarCloud Code Analysis und wurde als aktueller main
`615b13bacbd008562c17408246c41ab27dca3104` per Squash-Merge integriert.
Hash-valide aufbewahrte Receipts und der aktuelle Live-Recheck von SonarQube
Cloud für PR #3, PR #4 und main melden Quality Gate `OK` und null
Vulnerabilities.

Der frühere CI-/Quality-Gate-Blocker ist geschlossen. Diese Disposition gilt
nur für die sieben historischen Validator-Signale von PR #3 und schließt keine
unabhängigen SonarQube-Cloud-Coverage- oder Framework-Findings.

## Boundary-, Source-/Control-/Sink-Bewertung

Die betroffene Datei bleibt ein lokales, read-only-Governance-CLI. Die
fokussierte PR-#4-Remediation und die aufbewahrten Tests bewahren die
No-Git/No-Shell/No-Network/No-Cleanup-Execution-, Containment-, Symlink-,
UTF-8-JSON- und exakten Cleanup-Invarianten. Es wurden keine Scanner-Regel,
kein Quality Gate, keine Exclusion, False-Positive-Disposition, kein
`NOSONAR`, keine Suppression und keine Security-Control abgeschwächt.

## Voraussetzungen und Reproduktion

- Das aufbewahrte historische PR-#3-Receipt dokumentiert den früheren Fehler.
- PR #4 ist gemergt und `615b13bacbd008562c17408246c41ab27dca3104` ist der
  aktuelle MRTS-`main`.
- Die PR-#4- und Resulting-main-Receipts sind weiter hash-valid; aktuelle
  öffentliche SonarQube-Cloud- und GitHub-Readbacks sind verfügbar.

```text
rtk gh pr checks 4 --repo Easton97-Jens/MRTS
rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_MRTS&pullRequest=4'
rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_MRTS&pullRequest=4&resolved=false&types=VULNERABILITY&ps=100'
```

Die aktuellen Checks bestehen; das historische Receipt bleibt der ursprüngliche
Fehlerbeleg.

## Evidence

- Historischer Fehlerbeleg: `.codex/runs/20260724T170026Z-worktree-cleanup-governance/sonar-pr3-quality-gate.json`, SHA-256 `164f994006807455abe42da8b2b563eeb4a8032e04287d9a9bc3a5f42a6bbcf7`, Exit `1`.
- PR-#4-Issue-/Gate-Receipts: `.codex/runs/20260726T101017Z-mrts-sonarcloud-zero-pr4/sonar-pr-issues.json` und `sonar-quality-gate.json`, SHA-256 `ee8fdf86104a53c760e40f0d42b92b51d2c13f2e289efcb6b562dce9076f6a55` und `1db063f467b49ec05719b0f44b2c703bc402ae52f2515452169ddafbe4343c64`, Exit `0`.
- Resulting-main-Receipts: `.codex/runs/20260726T105800Z-mrts-pr4-squash-merge/github-post-merge.json`, `sonar-main-issues.json` und `sonar-main-quality-gate.json`, SHA-256 `6d77c474bdc6a8b9744dd3ac8e2b6c76195a47e47fb945caa75acb5173a1f936`, `58cf67de638c7b544b279c8365ac3334eb279716faed0996d6fe439a6ac9ad58` und `0f88c3322a2a779ea067fcf61cbf21946c614836989b5f5d360f7c04f078e69b`, Exit `0`.

## Grundursache und Remediation-Grenze

Die ursprüngliche PR-#3-Validator-Form löste Sonar-Taint-Regeln für lokale
Manifest-Pfade aus. PR #4 wandte die fokussierte repository-native Remediation
samt Testabdeckung an. Die exakten Hosted- und Resulting-main-Receipts belegen
jetzt den Abschluss ohne Abschwächung von Scanner-Regeln, Quality Gate,
Containment, Symlink-, Remote-, Gitlink- oder Cleanup-Controls.

## Akzeptanz, Validierung und Restrisiko

- PR #4 bestand Analyze (python), CodeQL, Python-3.14-Governance und
  SonarCloud Code Analysis; er wurde als `615b13bacbd008562c17408246c41ab27dca3104`
  gemergt.
- Die aufbewahrte lokale Validierung bestand 38 fokussierte Tests, Python
  compileall und `git diff --check`; legitime Controls bewahren
  metazeichensichere argv, `shell=False` und Pre-`Popen`-Validierungsfehler.
- PR #4 und der resultierende main melden Quality Gate `OK` und null offene
  Vulnerabilities, ohne verbotenen Sonar- oder Security-Control-Shortcut.

Restrisiko: Künftige Validator-Änderungen brauchen frische Exact-Head-
SonarQube-Cloud-/GitHub-Evidence. Dieser archivierte Record löst
`FND-SONAR-0009` nicht. Verwandte Findings: `FND-CROSS-0007`,
`FND-FRAMEWORK-0055`, `FND-SONAR-0017`.

## Historie und finale Disposition

- `2026-07-24T18:30:00Z` — exakter Draft-PR-#3-Sonar-Gate-Fehler mit sieben
  aufgabeneigenen Scanner-Signalen.
- `2026-07-24T18:30:00Z` — statische Triage fand keinen Beleg für einen
  unterstützten Remote-Angreifer oder Runtime-Sink; keine Source-/Scanner-
  Änderung erfolgte.
- `2026-07-26T10:10:17Z` bis `2026-07-26T10:58:00Z` — PR-#4- und
  Resulting-main-Receipts belegten ein bestehendes Gate und null Vulnerabilities
  nach der fokussierten Remediation und dem Merge.
- `2026-07-26T17:45:32Z` — der aktuelle öffentliche SonarQube-Cloud-/GitHub-
  Recheck bestätigte den geschlossenen Zustand; das vollständige Tripel ist für
  die lokale Archivierung geeignet.

Finale Disposition: `closed_verified_by_merged_mrts_pr4_and_live_sonar_reconciliation_20260726`.
