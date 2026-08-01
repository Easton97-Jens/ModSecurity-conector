# FND-PARENT-0023 — Die Submodule-Update-Validierung teilt einen Workspace mit einem späteren GitHub-Token-Publishing

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0023 |
| Titel / Title | Die Submodule-Update-Validierung teilt einen Workspace mit einem späteren GitHub-Token-Publishing |
| Kategorie / Category | security_hardening |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P1 |
| Schweregrad / Severity | medium |
| Konfidenz / Confidence | probable |
| Status | closed (archiviert) |
| Machbarkeitsstatus / Feasibility status | feasible_now |
| Release-Blocker / Release blocker | false |
| Security-Relevanz / Security relevance | true |

## Zusammenfassung / Summary

Fünf GitHub-Code-Scanning-Scorecard-TokenPermissionsID-Alerts identifizierten auf Workflow-Ebene deklarierte Schreibrechte. Insbesondere checkte update-submodules.yml Framework-Submodule-Inhalte rekursiv aus und aktualisierte sie, führte make quick-check aus und veröffentlichte danach in demselben Job mit GH_TOKEN einen Branch und Pull Request. Die Behebung behält restriktive Workflow-Defaults bei und trennt schreibgeschützte Validierung von tokentragendem Publishing. Der finale Pull-Request-Tree und der aktuelle Master-Tree stimmen überein; die ursprüngliche Permission-Boundary-Reproduktion und exakte Master-Controls verifizieren die Behebung.

## Beobachtetes Verhalten / Observed behavior

Bei c8ca0d92b630c18232b881855c4f5d1482568ea6 deklarierte update-submodules.yml auf Top-Level contents: write und pull-requests: write, checkte das Framework-Submodule rekursiv aus und aktualisierte es, führte make quick-check aus und nutzte danach GH_TOKEN, um einen Parent-Pull-Request per Force-Push zu veröffentlichen. cleanup-artifacts.yml und test-full-smoke-sequential.yml deklarierten auf Top-Level actions: write; update-actions-versions.yml deklarierte auf Top-Level contents: write, pull-requests: write und actions: write. Die GitHub-Code-Scanning-API meldete fünf entsprechende Scorecard-Alerts.

## Erwartetes Verhalten / Expected behavior

Jeder betroffene Parent-Workflow deklariert den restriktiven Top-Level-Default contents: read, und jeder Job erhält nur die zusätzlich benötigte Fähigkeit. Remote-Submodule-Inhalte werden nur in einem schreibgeschützten Validierungsjob aufgelöst und ausgeführt. Ein separater Publisher validiert den ausgewählten offiziellen Commit, aktualisiert nur den Gitlink ohne das Submodule auszuchecken oder auszuführen und erhält contents: write und pull-requests: write nur beim Publishing.

## Auswirkung / Impact

Ein kompromittiertes oder unerwartetes Submodule-Update könnte einen Workspace vor einer privilegierten Workflow-Operation beeinflussen. Workflow-weite Schreibrechte vergrößern außerdem die Token-Exposition unbeteiligter Jobs und lösen Scorecard-Sicherheitsbefunde aus. Die ursprüngliche Untersuchung etablierte eine plausible Vertrauensgrenzenverletzung, keine nachgewiesene Token-Exfiltration oder unautorisierte Repository-Schreiboperation.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- .github/workflows/cleanup-artifacts.yml
- .github/workflows/test-full-smoke-sequential.yml
- .github/workflows/update-actions-versions.yml
- .github/workflows/update-submodules.yml
- tests/test_ci_security_workflows.py

### Symbole / Symbols

- cleanup-artifacts
- test-full-smoke-sequential
- update-actions-versions
- update-submodules

## Voraussetzungen / Preconditions

1. Der geplante oder manuell gestartete update-submodules-Workflow läuft auf dem geschützten Default-Branch.
2. Das Framework-Submodule-Remote rückt zu einem Commit vor, der mit git submodule update --remote --recursive ausgewählt wird.
3. Der Workflow-Job führt später GitHub-token-authentifiziertes Branch- und Pull-Request-Publishing aus.

## Reproduktion / Reproduction

1. .github/workflows/update-submodules.yml bei c8ca0d92b630c18232b881855c4f5d1482568ea6 prüfen.
2. Top-Level contents: write und pull-requests: write, rekursiven Submodule-Checkout/-Update, make quick-check und spätere GH_TOKEN-gestützte Push- und Pull-Request-Schritte in einem Job beobachten.
3. Die GitHub-Code-Scanning-API nach offenen Scorecard-Alerts abfragen und die in der retained Evidence dokumentierten TokenPermissionsID-Alerts 2 bis 6 beobachten.

## Evidence / Evidence

1. Ursprüngliche Source- und Scorecard-Untersuchung
   - Run-ID: 20260718T080138Z-harden-workflow-permissions-e804be63
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260718T080138Z-harden-workflow-permissions-e804be63/evidence/workflow-permission-trust-boundary.md
   - Artifact type: workflow_permission_and_trust_boundary_assessment
   - SHA-256: b7a702366ee7c9c7b470f5d7ef950dd4c51cb1ba504f62e1a956bc1f7f7bc6a3
   - Command: rtk gh api 'repos/Easton97-Jens/ModSecurity-conector/code-scanning/alerts?tool_name=Scorecard&state=open&per_page=100' and rtk cat .github/workflows/update-submodules.yml
   - Working directory: /root/git/ModSecurity-conector
   - Exit code: 0; observed at: 2026-07-18T08:01:38Z; retention: retained_task_evidence
2. Historische Exact-Head-Verifikation
   - Run-ID: 20260718T080138Z-harden-workflow-permissions-e804be63
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260718T080138Z-harden-workflow-permissions-e804be63/evidence/pr-54-a9719b8-exact-head-verification.md
   - Artifact type: pull_request_exact_head_verification
   - SHA-256: fd516aa371cf5bb13a8de6d402a97aa088703a2488fb4a406e150dddfb9a2aae
   - Command: rtk gh pr view 54 --repo Easton97-Jens/ModSecurity-conector and rtk gh run view for exact head a9719b89f5a37f6added5b10920eccbd0e405217
   - Working directory: /var/tmp/codex/worktrees/parent-workflow-permissions
   - Exit code: 0; observed at: 2026-07-18T09:32:05Z; retention: retained_task_evidence
3. Finale Exact-Head-Verifikation und Sonar-Behebung
   - Run-ID: 20260719T103749Z-parent-pr-53-60-integration-a7b98a59
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260719T103749Z-parent-pr-53-60-integration-a7b98a59/evidence/pr54-d4318ce-exact-head-verification.md
   - Artifact type: pull_request_exact_head_verification_and_sonar_remediation
   - SHA-256: f0f757e73a26c0ead915e399b755a200e51ded593fd9308dad0978609d88ffb6
   - Command: rtk make check-ci-security-contract; rtk git diff --check origin/master..HEAD; rtk gh pr checks 54 --required; GitHub Checks API; SonarCloud Quality Gate and open-issue API
   - Working directory: /var/tmp/codex/worktrees/parent-workflow-permissions
   - Exit code: 0; observed at: 2026-07-19T11:02:11Z; retention: retained_task_evidence
4. Post-Merge-Master-Verifikation
   - Run-ID: 20260719T103749Z-parent-pr-53-60-integration-a7b98a59
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260719T103749Z-parent-pr-53-60-integration-a7b98a59/evidence/pr54-master-verification-63819e4.md
   - Artifact type: post_merge_master_reproduction_and_workflow_verification
   - SHA-256: e0db6fba0aee9629dd11b71e154c7c2f3daa9d15549c94e3fdf7ee0fb7990b71
   - Command: rtk git rev-parse/diff/grep; rtk make check-ci-security-contract; rtk gh pr view/run list/api Scorecard alerts for PR #54 and master 63819e416984294792bbbe68aa5d84503791baab
   - Working directory: /root/git/ModSecurity-conector
   - Exit code: 0; observed at: 2026-07-19T11:18:33Z; retention: retained_task_evidence

## Grundursachenanalyse / Root-cause analysis

Schreibrechte wurden auf Workflow-Ebene vergeben, obwohl nur einzelne Jobs sie benötigten. update-submodules kombinierte Remote-Submodule-Auswahl, Ausführung von Submodule-Code und tokentragendes Publishing in einem Workspace/Job. Der repositoryweite Actions-Default war write, sodass Workflows ohne expliziten restriktiven Default ebenfalls übermäßige Autorität erbten.

## Vorgeschlagene Remediation / Proposed remediation

Auf Top-Level jedes betroffenen Workflows contents: read setzen. actions: write in isolierte Artefakt-Cleanup-Jobs verschieben. Schreibrechte von update-actions-versions auf seinen einzelnen Publisher-Job begrenzen und persist-credentials: false beibehalten. update-submodules in schreibgeschützte Auflösung/Validierung und einen separaten Publisher mit Minimalrechten teilen, der den offiziellen Remote-Commit validiert und nur den Gitlink aktualisiert, ohne das Submodule auszuchecken oder auszuführen. security-events: write für SARIF-Upload-Jobs erhalten und die Permission-Contract-Fixtures sowie Regressionstests ergänzen.

## Akzeptanzkriterien / Acceptance criteria

- Alle Parent-Workflow-Dateien deklarieren exakt den restriktiven Top-Level-Default contents: read.
- Kein Job mit Checkout, Produktausführung, rekursivem Submodule-Zugriff oder nicht vertrauenswürdiger Pull-Request-Ausführung hat einen write-scoped GitHub-Token, ein benanntes Secret oder persistierte Checkout-Credentials, sofern dies nicht separat begründet und als sicher nachgewiesen ist.
- update-submodules validiert Remote-Inhalt in einem contents: read-Job und veröffentlicht nur aus einem getrennten Job, der Submodule-Inhalt weder auscheckt noch ausführt.
- CodeQL und andere legitime SARIF-Uploads behalten nur die erforderliche Berechtigung security-events: write neben contents: read.
- Workflow-Permission-Contract-Tests, Safe/Unsafe-Fixtures, actionlint, ShellCheck, zizmor, Secret Scanning, OSV, Scorecard, CodeQL/SARIF und git diff --check liefern die stärkste anwendbare Evidence.

## Validierungsplan / Validation plan

1. Alle Workflow-YAMLs durch actionlint mit ShellCheck-Integration parsen.
2. Den fokussierten CI-Security-Workflow-Contract einschließlich Safe- und Unsafe-Fixtures, Fork-/nicht vertrauenswürdiger Pull-Request-Modellierung, Submodule-Trust-Boundaries und SARIF-Upload-Berechtigungen ausführen.
3. zizmor über Produktionsworkflows ausführen und prüfen, dass seine unsichere Fixture weiter fehlschlägt, während die sichere Fixture besteht.
4. Gitleaks-, OSV- und Scorecard/CodeQL-Workflow-Checks durch den fokussierten Pull Request ausführen und den exakten Head-SHA in GitHub Actions und Code Scanning verifizieren.
5. git diff --check ausführen und den finalen Parent-only-Diff prüfen.

## Regressionstests / Regression tests

- tests/test_ci_security_workflows.py
- ci/fixtures/workflow-permission-contract/safe.yml
- ci/fixtures/workflow-permission-contract/unsafe.yml

## Legitime Kontrolltests / Legitimate control tests

- CodeQL, OSV und Scorecard behalten security-events: write nur in SARIF-Upload-Jobs und behalten contents: read.
- Artefakt-Cleanup-Jobs behalten actions: write ohne Checkout oder Produktausführung.
- Der update-submodules-Publisher-Job kann den erwarteten Parent-Pull-Request erstellen, nachdem schreibgeschützte Validierung einen verifizierten offiziellen Remote-Commit ausgewählt hat.

## Abhängigkeiten, Blocker und verwandte Findings / Dependencies, blockers, and related findings

### Abhängigkeiten / Dependencies

- GitHub-Actions-Runner und GitHub Code Scanning führen die fokussierten Pull-Request-Checks aus.
- FND-GITHUB-0001 bleibt separat verfolgt, weil repositoryweite Default-Workflow-Permission-Konfiguration außerhalb dieses Parent-Pull-Requests liegt.

### Blocker / Blockers

- None / Keine.

### Verwandte Findings / Related findings

- FND-GITHUB-0001

## Aktuelle Behebungsdisposition und Restrisiko / Current remediation disposition and residual risk

PR #54 mit finalem Head d4318cef184a1cdeb70858cc18861d7e5649037b wurde als 63819e416984294792bbbe68aa5d84503791baab squash-gemergt. Der Master-Tree entspricht dem finalen PR-Tree; die ursprüngliche Source-/Permission-Boundary-Reproduktion meldet keinen TokenPermissionsID-Alert mehr; und alle 14 beobachteten exakten Master-Workflows einschließlich OpenSSF Scorecard waren erfolgreich. default_workflow_permissions auf Repository-Ebene liest nun read; separate verbleibende Governance-Alerts bleiben in FND-GITHUB-0001. Es gibt keine Risikoakzeptanz. Dieser Befund ist verified, nicht closed; ein Abschluss erfordert eine separate Lifecycle-Entscheidung.

## Historie / History

- 2026-07-18T08:01:38Z — finding_created_from_scorecard_and_source_assessment: fünf offene Scorecard-TokenPermissionsID-Alerts und die plausible update-submodules-Validierungs-zu-Publishing-Trust-Boundary vor der Behebung festgehalten.
- 2026-07-18T09:32:05Z — fixed_on_exact_pull_request_head: PR-#54-Head a9719b89f5a37f6added5b10920eccbd0e405217 bestand CodeQL, OSV-SARIF-Upload, Scorecard, Secret Scanning, Workflow-Lint und SonarQube-Quality-Gate; er blieb fixed bis Merge und Default-Branch-Reproduktion.
- 2026-07-19T11:05:11Z — post_master_sync_sonar_delivery_blocker_remediated: nach normalem Merge von a589cb662fb03deb764f78eefbb1056bc64d63e2 ersetzte PR #54 das äquivalente Zwei-Leerzeichen-JOB_HEADER-Präfix durch {2}. Finaler Head d4318cef184a1cdeb70858cc18861d7e5649037b bestand Required Checks, CodeQL, OSV, report-governance und SonarCloud mit null offenen PR-Issues und null Security Hotspots.
- 2026-07-19T11:18:33Z — current_master_reproduction_verified: PR #54 wurde als 63819e416984294792bbbe68aa5d84503791baab gemergt; der Tree entspricht dem finalen Head d4318cef184a1cdeb70858cc18861d7e5649037b; die ursprüngliche Reproduktion meldet keinen TokenPermissionsID-Alert mehr; und alle 14 beobachteten exakten Master-Workflows bestanden. Der Befund ist verified, nicht closed.
- 2026-07-19T11:58:56Z — canonical_category_and_bilingual_record_normalized: die kanonische Kategorie auf security_hardening normalisiert und die retained historische Exact-Head-Evidence mit SHA-256 fd516aa371cf5bb13a8de6d402a97aa088703a2488fb4a406e150dddfb9a2aae in die vollständigen englischen und deutschen Records zurückgeführt. Status, Severity, Confidence, Release-Blocker-Disposition und Master-Verifikationsevidence sind unverändert.
- 2026-07-26T14:09:02Z — closed_by_current_user_after_current_master_validation: der aktuelle Nutzer autorisierte Abschluss und Archivierung; `tests.test_ci_security_workflows` bestand auf Parent-Master `6ca7e1536ce7e93da68099db9c586b88852ff13e` als Teil der 144-Test-Control-Suite. Das getrennte Repository-Default-Governance-Finding bleibt aktiv.
