# FND-FRAMEWORK-0001 — Framework-test-common- und common-structure-Checks schlagen fehl

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0001` |
| Title / Titel | `Framework-test-common- und common-structure-Checks schlagen fehl` |
| Category / Kategorie | `ci_failure` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `fixed` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Der aktuelle Framework-Default-SHA schlug reproduzierbar bei `test-common / common-structure` fehl; die fokussierte Reparatur besteht nun am exakten Head des Draft-PR #23 `f869d77070dc1fe05f7ff8377d8723b8e3185849`, ist aber absichtlich nicht gemergt. Die unabhängigen Workflow-Hardening- und CI/Security-Draft-PRs #29 und #27 reproduzierten denselben Current-Head-Baseline-Fehler.

## Observed behavior / Beobachtetes Verhalten

Der Default-Workflow schlug mit `expected 141 YAML cases, found 179` fehl. Nach lokalem Entfernen dieses veralteten Guards legte die Runtime-Discovery einen reinen `security-data-flow`-Katalogfall offen, der vor seiner `former_xfail`-/`connector-gap`-Ausschlussmetadaten validiert wurde. Der exakte Head von PR #23 hat nun zwei erfolgreiche `common-structure`-Runs. Die exakten Heads von PR #29 `191b7e3d1999c7ffb39ad16bfaff7821bfc09825` und PR #27 `5b2a26a41e7621e7b246aa1a060149252cfe3062` haben fehlgeschlagene `common-structure`-Runs mit dem unveränderten Guard.

## Expected behavior / Erwartetes Verhalten

Der exakte Task-Branch-Head hat aktuelle GitHub Actions bestanden. Für Verifikation/Schließung sind ein zukünftiger Master-Merge und Rerun erforderlich; beides ist in diesem Task nicht autorisiert.

## Impact / Auswirkung

Die Task-Reparatur ist fixed und ihr Draft PR ist am exakten Head verifiziert. Sie bleibt auf Benutzeranweisung ungemergt; bis diese unabhängige Reparatur oder eine gleichwertige Änderung integriert ist, können unabhängige Draft-PRs wie #29 und #27 nicht `verified_pr` erreichen. Der unabhängige Default-Branch-Sonar-Backlog bleibt ein Release-Thema, schlug aber nicht beim New-Code-Quality-Gate von PR #23 fehl.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `.github/workflows/test-common.yml`
- `tests/runners/runner_core.py`
- `tests/workflow_contract/test_common_structure_workflow.py`

### Symbols / Symbole

- `test-common`
- `common-structure`
- `discover_case_files`
- `is_case_applicable`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.
- Framework `master` steht auf `cdc91a398d6c156eaff927d742b23018a3817fb6` und der Task-Worktree verwendet dessen saubere Branch-Basis.

## Reproduction / Reproduktion

- `sed -n '181,196p;212,215p' .codex/reports/repository-full-assessment.md`
- GitHub-Actions-Run `29527830684` protokolliert `expected 141 YAML cases, found 179`.
- Den wörtlichen common-structure-Materialisierungs-/Assertion-Block mit task-eigenem externen `RUNNER_TEMP` ausführen.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:181-196,212-215`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '181,196p;212,215p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run-ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/common-structure-current.md`
  - Typ: `current_ci_root_cause_and_local_regression`; SHA-256: `03a39f33a6b7e3eac71e3c4d5a32cc102de8e1a6f2d41556a64945d0c5427a1f`
  - Befehl: `rtk make BUILD_ROOT=<task-owned> test-workflow-contract; rtk env RUNNER_TEMP=<task-owned> ... bash -eu -c '<literal common-structure block>'`
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-common-structure`; Exit-Code: `0`
  - Beobachtet am: `2026-07-18T09:20:00Z`; Retention: `retained_task_evidence`
- Run-ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/pr-23-current.md`
  - Typ: `exact_draft_pr_head_ci_sonar_review_verification`; SHA-256: `c28444cfdd989b9884e367f17e0540ccda9858a3bc10b24b26dd8293b500855d`
  - Befehl: Gleichheit von lokalem/Remote-/PR-Head plus schreibgeschützte PR-Checks und Thread-Inspektion über RTK
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-common-structure`; Exit-Code: `0`
  - Beobachtet am: `2026-07-18T09:58:40Z`; Retention: `retained_task_evidence`
- Run-ID: `20260718T081429Z-framework-workflow-hardening-320e9322`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081429Z-framework-workflow-hardening-320e9322/evidence/common-structure-baseline-recheck.md`
  - Typ: `baseline_ci_recheck`; SHA-256: `290001674e3974e268f1a7f63469f1c5e1dc743eeb31f440ed1297a1433d75b9`
  - Befehl: wörtlicher `test-common / common-structure`-Count-Guard, Count im autoritativen Checkout und schreibgeschützte aktuelle-`master`-Workflow-Metadaten über RTK
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-workflow-hardening`; Exit-Code: `1`
  - Beobachtet am: `2026-07-18T10:39:59Z`; Retention: `retained_task_evidence`
- Run-ID: `20260718T081429Z-framework-workflow-hardening-320e9322`
  - Artefakt: `evidence/pr-29-common-structure-status.md`
  - Typ: `current_draft_pr_ci_baseline_confirmation`; SHA-256: `9ae5cd9cb6d4b314a69d4849d880465a79f6927ba2bd8d8b5b322f6ac36b3951`
  - Befehl: aktuelle Draft-PR-Metadaten plus Inspektion des fehlgeschlagenen GitHub-Actions-Runs über RTK
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-workflow-hardening`; Exit-Code: `1`
  - Beobachtet am: `2026-07-18T11:33:16Z`; Retention: `retained_task_evidence`
- Run-ID: `20260718T083435Z-expand-framework-ci-security-32892be1`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T083435Z-expand-framework-ci-security-32892be1/evidence/ci-security/framework-pr27-final-blockers.txt`
  - Typ: `exact_framework_pr_head_common_structure_duplicate_evidence`; SHA-256: `1686ed164f9a892c08c6749ed5d9922269a7a026a442ddd477d62bd240848b5f`
  - Befehl: `rtk proxy gh run view 29645450445 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed`
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-ci-security`; Exit-Code: `0` (Abruf; der beobachtete Job schlug fehl)
  - Beobachtet am: `2026-07-18T13:13:38Z`; Retention: `retained_task_evidence`

## Root-cause analysis / Grundursachenanalyse

Die ursprüngliche feste Zahl wurde in `b7f9bdc9831f9a8d14294cfb8fcb129a183d5d18` eingeführt, als der Bestand 141 YAML-Dateien enthielt; spätere gültige Ergänzungen erhöhten ihn auf 179. Die vorherige `discover_case_files()`-Implementierung rief volle `load_case()`-Validierung vor der Eignungsfilterung auf, sodass ein reiner `former_xfail`-Katalogfall ohne Runtime-`rules` vor dem beabsichtigten Nicht-Runtime-Ausschluss fehlschlug.

## Proposed remediation / Vorgeschlagene Remediation

Dynamische nichtleere Discovery verwenden, Nicht-Runtime-Katalogmetadaten vor Runtime-spezifischer Schemavalidierung filtern, Validierung/Materialisierung ausgewählter Runtime-Fälle erhalten und den exakten Task-Branch-Head in GitHub Actions verifizieren, ohne Sonar-Controls zu ändern.

## Acceptance criteria / Akzeptanzkriterien

- Current Framework test-common and common-structure checks succeed at the target SHA.
- A regression distinguishes the repaired behavior from the failing baseline.
- Leerer Bestand und leere Apache-Common-Auswahl schlagen weiterhin explizit fehl.
- Reine Security-Data-Flow-Katalogfälle bleiben durch ihren dedizierten statischen Check abgedeckt und erreichen keine Materialisierung.

## Validation plan / Validierungsplan

- `make test-workflow-contract` und die wörtliche lokale common-structure-Kontrolle ausführen.
- Den exakten Task-Branch-GitHub-Actions-Workflow erneut ausführen und Current-Head-Evidence aufbewahren.
- Den legitimen dedizierten Security-Data-Flow-Katalogcheck als Control ausführen.

## Regression tests / Regressionstests

- `tests/workflow_contract/test_common_structure_workflow.py` deckt dynamische Guards und reine Katalogausschlüsse ab.

## Legitimate control tests / Legitime Kontrolltests

- Ausgewählte Apache-Common-Fälle materialisieren weiterhin und prüfen ihre erwarteten Status.

## Dependencies / Abhängigkeiten

- `FND-SONAR-0002` bleibt unabhängig und darf nicht in diesen Framework-Patch gemischt werden.

## Blockers / Blocker

- Es gibt keine Merge-Autorisierung; die Richtlinie verlangt Reproduktion nach dem Merge vor der Schließung. Der unabhängige Default-Branch-Sonar-Backlog bleibt trotz bestandenem PR-New-Code-Quality-Gate ein Release-Blocker.

## Related findings / Verwandte Findings

- `FND-SONAR-0002`
- `FND-CROSS-0005`

## Residual risk / Restrisiko

Die fokussierte Reparatur ist nur am ungemergten Draft-PR-Head verifiziert. Keine Risikoakzeptanz liegt vor; zukünftige Master-Integration und der unabhängige Default-Branch-Sonar-Backlog liegen außerhalb dieses Tasks.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T09:27:57Z`: current_task_root_cause_and_repair_in_progress — Current-SHA-Evidence bewies den veralteten Kardinalitätsguard und den maskierten Discovery-Ordering-Defekt; fokussierte lokale Regression und wörtliche Kontrolle bestanden. Keine PR-Head-Verifikation oder Closure ist erfolgt.
- `2026-07-18T09:58:40Z`: exact_draft_pr_head_verified_fixed — Draft PR #23 ist clean, der exakte Head stimmt lokal/remote/im PR überein, sechs Checks einschließlich zweier `common-structure`- und SonarCloud-Runs bestehen, und es gibt keine Reviews oder Review-Threads. Der PR wird absichtlich nicht gemergt, daher ist das Finding fixed und nicht geschlossen.
- `2026-07-18T10:39:59Z`: workflow_hardening_baseline_recheck_deduplicated — Der separate Workflow-Hardening-Task führte den unveränderten Count-Guard erneut aus: Er endet weiterhin mit `1` und `expected 141 YAML cases, found 179`. Der autoritative Checkout hat denselben Count, und der aktuelle `master`-Run `29527830684` ist bei `cdc91a398d6c156eaff927d742b23018a3817fb6` weiterhin fehlgeschlagen. Dies ist eine Duplikatbestätigung, keine task-eigene Remediation.
- `2026-07-18T11:33:16Z`: workflow_hardening_draft_pr_ci_baseline_confirmation — Draft PR #29 mit Head `191b7e3d1999c7ffb39ad16bfaff7821bfc09825` bestand `check-action-versions` und `scaffold-lint`, aber beide Current-Head-`common-structure`-Runs schlugen mit dem unveränderten Guard `expected 141 YAML cases, found 179` fehl. Dieser Task ändert weder `tests/cases` noch common structure; dies ist daher nur Duplikat-Baseline-Evidenz.
- `2026-07-18T13:13:38Z`: ci_security_draft_pr_baseline_recheck_deduplicated — Der exakte Head `5b2a26a41e7621e7b246aa1a060149252cfe3062` des Draft-PRs #27 hat zwei fehlgeschlagene `common-structure`-Checks mit dem unveränderten Guard `expected 141 YAML cases, found 179`. Die CI/Security-Erweiterung ändert weder `tests/cases` noch common structure; dies ist daher nur Duplikat-Baseline-Evidenz. Der Status bleibt `fixed`, bis die separate ungemergte Reparatur integriert ist.
- `2026-07-18T14:26:12Z`: final_ci_security_draft_pr_baseline_recheck_deduplicated — Der finale exakte Head `66d90872cfc0125536267d574b776d2e88d26b23` des Draft-PRs #27 schlug im `common-structure`-Run `29647958875` erneut mit unverändertem `expected 141 YAML cases, found 179` fehl. Dieser Task ändert weiterhin weder `tests/cases` noch common structure; der Status bleibt `fixed` und die neue Evidence ist nur eine Duplikat-Baseline-Bestätigung.

## Aktuelle Exact-Head-Duplikat-Evidence

`framework-pr27-final-remote-status.md` bewahrt den exakten Final-Head-Run,
SHA-256 `ccedabbe5e020bf43eb91ccf93b1e1484b8d11471e2817b6d078a95eeddb3552`.
Sie bestätigt, dass dieses nicht zusammenhängende Gate die PR-#27-Delivery
blockiert, ohne das separate fixed Finding wieder zu öffnen, abzuschwächen oder
zu ändern.

## Direkte Stale-PR-Rückeinführungsgefahr vom 2026-07-19

Die direkten Zwei-Baum-Vergleiche vom aktuellen Framework-`master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` zeigen, dass die veralteten,
ungemergten PR-Heads #24, #27 und #29 die gemergte dynamische nichtleere
common-structure-Kontrolle entfernen und den behobenen Count-/Ordering-Fehler
wiederherstellen. Dies ist ein Merge-Blocker, keine Wiedereröffnung des
Findings: Der aktuelle Master bleibt `fixed`, und keine Kontrolle wurde
abgeschwächt.

Zurückgehaltene Evidence: Run
`20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
beobachtet am `2026-07-19T12:01:55Z` durch RTK-präfixierte Direct-Diff- und
GitHub-Gate-Readbacks.
