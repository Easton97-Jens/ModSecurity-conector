# FND-FRAMEWORK-0003 — Framework workflow actions use mutable major tags

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0003` |
| Title / Titel | `Framework workflow actions use mutable major tags` |
| Category / Kategorie | `security_hardening` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `validated` |
| Status | `fixed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The Framework action-pin control is locally remediated: every observed external
action reference is pinned to a reviewed immutable full commit SHA, and a
native regression-tested validator enforces the boundary.

## Observed behavior / Beobachtetes Verhalten

At Framework base `cdc91a398d6c156eaff927d742b23018a3817fb6`, the prior inline
validator accepted seven mutable major tags. The changed Framework workflow
tree now validates only external full-SHA references.

## Expected behavior / Erwartetes Verhalten

Every external executable workflow action must resolve to a reviewed full
40-character Git commit SHA before a Framework job executes it; local `./`
references remain a distinct legitimate control.

## Impact / Auswirkung

The mutable-action supply-chain path is locally removed. Delivery assurance
remains bounded because mandatory static tools and independent Framework
delivery gates are unresolved.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `modules/ModSecurity-test-Framework/.github/workflows/check-action-versions.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/check-common-versions.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/cleanup-artifacts.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/lint.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/test-common.yml`
- `modules/ModSecurity-test-Framework/ci/checks/security/check-workflow-action-pins.py`
- `modules/ModSecurity-test-Framework/tests/security_regression/test_workflow_action_pins.py`
- `modules/ModSecurity-test-Framework/Makefile`

### Symbols / Symbole

- `check-workflow-action-pins.py`
- `external uses: full 40-character Git commit SHA`
- `test-workflow-action-pins`

## Preconditions / Voraussetzungen

- Framework base `cdc91a398d6c156eaff927d742b23018a3817fb6` and retained
  validation evidence remain available.
- The seven action commit SHAs were reviewed from their upstream action
  repositories without changing the intended major versions.

## Reproduction / Reproduktion

- The pre-fix extracted current-master control accepted `actions/checkout@v7`,
  `actions/setup-python@v6`, `actions/github-script@v9`, and
  `peter-evans/create-pull-request@v8`.
- `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python ci/checks/security/check-workflow-action-pins.py`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:159-177,228-228`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '159,177p;228p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058/evidence/fnd-framework-0003-validation-summary-retained.md`
  - Type: `retained_validation_summary`; SHA-256: `b45fb9acc7a9ed5f12e5b49bce0669b815730b2cde9ee116c77b82f8240a8ba5`
  - Command: `rtk proxy .codex/bin/storage-budget retain-evidence --run 20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058 --source /var/tmp/codex/ModSecurity-conector/runs/20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058/tmp/fnd-framework-0003-validation-summary-source.md --destination evidence/fnd-framework-0003-validation-summary-retained.md --json`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-18T10:27:28Z`; retention: `retained_task_evidence`

## Root-cause analysis / Grundursachenanalyse

The Framework action-pin control explicitly permits mutable major tags, so scheduled or manually dispatched jobs can execute externally resolved action code without an immutable action identity.

## Proposed remediation / Vorgeschlagene Remediation

Implemented locally: require reviewed full commit SHAs for every external
workflow action, expose the pin control as a Framework-native checker, and
retain focused regression and update-review evidence.

## Acceptance criteria / Akzeptanzkriterien

- Every external Framework workflow action is pinned to a reviewed immutable
  full 40-character commit SHA.
- The checker recursively covers `.yml` and `.yaml` workflow locations and
  rejects mutable or unsupported action-reference forms fail-closed.
- Focused mutable-tag and syntax-bypass regression cases fail before the
  control and pass after it; full-SHA legitimate controls remain valid.
- The action update process records source, review, and retained validation
  evidence.

## Validation plan / Validierungsplan

- Run the focused pin suite, broader Framework security-regression suite,
  real-workflow checker, Framework lint, and Framework documentation checks.
- Run actionlint, ShellCheck, zizmor, SonarQube Cloud, and independent Codex
  Security revalidation with factual pass/fail/blocked dispositions.

## Regression tests / Regressionstests

- `tests/security_regression/test_workflow_action_pins.py`: 21 focused cases
  covering mutable tags, syntax bypasses, and legitimate controls.
- `tests/security_regression`: 34 cases passed.

## Legitimate control tests / Legitime Kontrolltests

- A quoted or unquoted external full-SHA reference and an external reusable
  workflow pinned to a full SHA validate.
- Local `./` action and local reusable-workflow references validate as
  non-external controls.

## Root-cause triage / Grundursachen-Triage

- Framework SHA: `cdc91a398d6c156eaff927d742b23018a3817fb6`
- Verdict: `confirmed`; static confidence: `medium`.
- Root-cause group: `RC-FW-001-action-reference-immutability`; singleton; no common patch or regression suite was proven with another finding, so a separate Framework PR is required.
- Entry points: `.github/workflows/check-common-versions.yml:3-10,20-24,106-115` and `.github/workflows/cleanup-artifacts.yml:3-18`.
- Source → broken control / sink: mutable external `uses:` major tags → `.github/workflows/check-action-versions.yml:27` accepts `@vN` → a scheduled or manually dispatched runner executes the action code, including a `contents: write` and `pull-requests: write` job.
- Attacker prerequisites: an action publisher or its tag authority changes a referenced major tag before the affected workflow runs. No tag rewrite or workflow run was reproduced.
- Existing countercontrols: explicit job permissions and a pin checker exist, but that checker deliberately accepts mutable major tags.
- Impact: altered action code can exercise the affected job's GitHub token permissions and alter workflow-controlled repository or artifact state.
- Required regression / legitimate control: reject `@vN` in every supported workflow file; accept a reviewed 40-hex SHA and preserve valid workflow syntax and triggers.
- Bypass review: quoted/commented entries, `.yaml` files, reusable workflows, local/Docker actions, abbreviated hashes, and future workflow locations.
- Parent impact: none in this triage; a later Framework delivery can reach Parent only through a separately authorized gitlink update. MRTS impact: none; no MRTS source or checkout access is required.
- Delivery boundary: Framework-only branch and Draft PR; Parent gitlink unchanged; MRTS untouched. Current Framework CI/Sonar blockers require separate evidence-backed dispositions before verified delivery.
- Proof gaps: no applicable Framework `SECURITY.md` and no dynamic action-tag rewrite were available. The complete follow-up brief is in `.codex/roadmap/framework-security-root-cause-triage.md`.

## Dependencies / Abhängigkeiten

- `FND-FRAMEWORK-0001`
- `FND-SONAR-0002`

## Blockers / Blocker

- `actionlint` and `zizmor` are required by the task but unavailable; no
  repository-approved or user-authorized provisioning route exists.
- `FND-FRAMEWORK-0001` and `FND-SONAR-0002` remain independent
  verified-delivery gates.

## Related findings / Verwandte Findings

- `FND-GITHUB-0001`
- `FND-FRAMEWORK-0004`

## Residual risk / Restrisiko

The local action-pin control is fixed, but no commit, push, Draft PR,
current-head CI, SonarQube Cloud result, or exact SHA equality exists.
`actionlint`/`zizmor` are unavailable, ShellCheck retains independent baseline
diagnostics, and `FND-FRAMEWORK-0001`/`FND-SONAR-0002` remain separate delivery
gates. No risk has been accepted.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T08:09:21Z`: root_cause_triaged — Current static evidence confirmed the mutable-major-tag control gap; it remains an open singleton group without delivery or risk acceptance.
- `2026-07-18T10:27:28Z`: local_remediation_validated_delivery_blocked — The Framework action-pin control was remediated locally with reviewed full-SHA pins, a native checker, a 21-case focused suite, a 34-case broader security-regression suite, Framework lint, documentation checks, and independent Codex Security revalidation with no concrete bypass. Delivery remains blocked: `actionlint`/`zizmor` are unavailable, ShellCheck retains baseline diagnostics, and `FND-FRAMEWORK-0001`/`FND-SONAR-0002` are independent gates; no commit, push, Draft PR, merge, Parent gitlink change, or MRTS change occurred.

## 2026-07-19 direct stale-PR reintroduction hazard

The direct comparison of current Framework `master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` to stale PR #24 confirms that
the unmerged head deletes the full-SHA action parser, regression suite, and
Makefile hook, replacing them with a major-tag-tolerant check. PR #27 has a
separately reviewed parser-regression candidate. These are merge blockers only;
master remains `fixed`. PR #29's replacement checker is not recorded as a
reintroduction.

Retained evidence: run `20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
observed `2026-07-19T12:01:55Z` by RTK-prefixed direct-diff and static
action-control review.
