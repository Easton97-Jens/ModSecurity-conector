# FND-GITHUB-0001 — GitHub Scorecard governance baseline has incomplete controls and follow-up evidence

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-GITHUB-0001` |
| Title / Titel | `GitHub Scorecard governance baseline has incomplete controls and follow-up evidence` |
| Category / Kategorie | `github_governance` |
| Repository / Repository | `github` |
| Ownership / Ownership | `github_configuration` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `closed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Live GitHub evidence covers all requested Scorecard/governance areas. Actions now defaults to `read`, `master` has no-bypass ruleset `19138299`, and repository vulnerability alerts are enabled. Draft PR [#120](https://github.com/Easton97-Jens/ModSecurity-conector/pull/120) exact head `57c411eeca7be024e5718d560e26e4bc051b92ae` supplies source remediation for FuzzingID #11 and VulnerabilitiesID #12; all 33 applicable terminal hosted checks passed at its then-current base. Master has since advanced non-overlappingly to `9e788057d2b551ba51ad7c4e6e1d8c5198b77834`, so GitHub reports the Draft PR as `BEHIND` and it must be normally updated and revalidated before review/merge. Current master alerts remain open; the other governance, review, age, and CII requirements retain their actual external blockers and evidence.

## Observed behavior / Beobachtetes Verhalten

Before remediation, `master` had no visible/effective ruleset or classic protection, Actions defaulted to `write`, and vulnerability alerts were endpoint-confirmed disabled. The currently visible Scorecard alerts are from `2026-07-16`, before this remediation; no score change is claimed until GitHub publishes a later analysis.

## Expected behavior / Erwartetes Verhalten

`master` accepts changes only through no-bypass pull requests with resolved conversations, strict current-head checks, no force push, and no deletion. A merged policy gives a confidential reporting route, and a human approval is configured only after an independent reviewer exists.

## Impact / Auswirkung

Unprotected branches and broad workflow defaults can bypass governance boundaries. Missing disclosure, dependency, SAST, and fuzzing decisions limit assurance. Scanner/advisory leads are not represented as confirmed runtime vulnerabilities without repository proof.

## Governance-point disposition / Disposition der Governance-Punkte

| Finding | Initial state | Action | Final state | Evidence | Remaining risk |
| --- | --- | --- | --- | --- | --- |
| Branch-Protection | `nicht konfiguriert` | Created ruleset `19138299`: deletion, non-fast-forward, pull request, resolved conversations, strict checks, no bypass. | `bereits korrekt` / `verified` | `current_user_can_bypass: never`; `master.protected: true`; PR #53 `d5781bd` is `CLEAN` with all six exact checks successful and zero review threads. | Independent human review is separately unresolved; check stability needs monitoring. |
| Code-Review | `nicht konfiguriert` | Recorded lockout analysis; no approval count and no bypass. | `muss geändert werden` / `blocked` | Sole direct collaborator is owner/admin; no team; PR #51 had no review. | No independent approval until reviewer exists. |
| Security-Policy | `nicht konfiguriert` | Created bilingual policy and Change Record; PR #53 was authorized, squash-merged, and verified on master. | `bereits korrekt` / `verified` | PR #53 `d5781bd` passed all six exact checks without bypass and was merged as `a589cb6`; its master tree matches the reviewed head and all 14 observed master workflows passed. GitHub returns `securityPolicyUrl` `https://github.com/Easton97-Jens/ModSecurity-conector/security/policy`; private reporting is `enabled=true`. | This verified point does not remove the separate independent-review, CII, dependency, SAST, or fuzzing gaps; recheck the URL after later repository changes. |
| Maintained | `nicht anwendbar` | No artificial activity or setting change. | `nicht anwendbar` / `not_applicable` | Scorecard reason is repository age below 90 days. | Recheck after `2026-08-12`. |
| CI-Best-Practices | `muss geändert werden` | Changed Actions default `write` to `read`; retained explicit scheduled-writer permissions pending separate proof. | `muss geändert werden` / `in_progress` | API post-readback is `read`; CII alert is missing external badge. | CII and Token-Permissions work remain scoped decisions. |
| SAST | `muss geändert werden` | Established real partial CodeQL and actionlint/zizmor coverage; added no placeholder. | `muss geändert werden` / `triaged` | Four CodeQL and two workflow-lint checks are stable; the visible Scorecard alert reports score 8 and 5/12 historical commits. | Full connector C/C++ scope needs separate feasibility. |
| Fuzzing | `nicht konfiguriert` | Delivered Draft PR #120's genuine C/libFuzzer Common HTTP-header parser target, bounded runner, Make target, and existing-CodeQL-job invocation; no detector marker or suppression. | `verified_draft_pr_behind_current_master_requires_update_and_revalidation` / `in_progress` | Exact head `57c411eeca7be024e5718d560e26e4bc051b92ae` passed 33 applicable terminal hosted checks; CodeQL bounded-c-cpp job `89542295414` executed the fuzzer successfully. Current master subsequently advanced non-overlappingly and GitHub reports the PR `BEHIND`. | A separately authorized normal branch update, fresh exact-head checks, independent review, merge, and a resulting-default-branch Scorecard analysis are required before alert #11 can be reassessed. |
| Vulnerabilities | `muss geändert werden` | Delivered Draft PR #120's exact safe development pin `PyYAML==6.0.3`, aligned to the existing CI hash lock; no OSV ignore or suppression. | `verified_draft_pr_behind_current_master_requires_update_and_revalidation` / `in_progress` | Exact head passed OSV and SonarCloud along with all other applicable checks; the pin prevents parser treatment of `>=6,<7` as literal version `6,<7`. Current master subsequently advanced non-overlappingly and GitHub reports the PR `BEHIND`. | A separately authorized normal branch update, fresh exact-head checks, independent review, merge, and a resulting-default-branch Scorecard analysis are required before alert #12 can be reassessed. |

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `SECURITY.md`, `SECURITY.de.md`
- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/dependabot.yml`
- `connectors/envoy/ext_proc/go.mod`
- `fuzz/common_http_headers_fuzz.c`
- `ci/checks/common/check-common-http-header-fuzz.sh`
- `Makefile`, `requirements-dev.txt`, `tests/test_ci_security_workflows.py`

### Symbols / Symbole

- `GitHub ruleset 19138299 Protect master`
- `GitHub Actions default workflow permissions`
- `GitHub vulnerability alerts`
- `GitHub Dependency Graph SBOM`
- `Scorecard alerts #1, #7-#13`
- `Dependabot alert #1`
- `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, `zizmor`
- `LLVMFuzzerTestOneInput`, `msconnector_headers_parse_content_length`, `PyYAML==6.0.3`

## Preconditions / Voraussetzungen

- GitHub administration access and stable six check contexts remain available.
- An independent reviewer is added before an approval count is enforced.
- This finding does not authorize a product, Framework, or MRTS change.

## Reproduction / Reproduktion

- `gh api repos/Easton97-Jens/ModSecurity-conector/rulesets/19138299`
- `gh api repos/Easton97-Jens/ModSecurity-conector/rules/branches/master`
- `gh api repos/Easton97-Jens/ModSecurity-conector/actions/permissions/workflow`
- `gh api repos/Easton97-Jens/ModSecurity-conector/vulnerability-alerts --include`
- `gh api repos/Easton97-Jens/ModSecurity-conector/code-scanning/alerts?tool_name=Scorecard&state=open`

## Evidence / Evidence

- Run ID: `20260718T081034Z-github-scorecard-governance`
  - Artifact: `.codex/runs/20260718T081034Z-github-scorecard-governance.json`
  - Type: `sanitized_github_governance_receipt_and_static_triage`; SHA-256: `3822662f25f4517cbb4ebe668ffd55941edcf827dbc7b4b0ee46f0531b8805ce`
  - Command: `gh api governance and security endpoints; static Dependabot-alert triage`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-18T09:21:20Z`; retention: `retained_local_receipt`

## Root-cause analysis / Grundursachenanalyse

The repository lacked complete branch/governance configuration, a discoverable policy, and evidence-backed decisions for every Scorecard heuristic. Solo ownership makes a mandatory approval unsafe without a reviewer or bypass.

## Proposed remediation / Vorgeschlagene Remediation

Retain verified ruleset `19138299` and the GitHub-recognized Security Policy; add an independent reviewer before setting `required_approving_review_count` to one; and treat CII, dependency remediation, expanded SAST, and fuzzing as separate evidence-backed work.

## Acceptance criteria / Akzeptanzkriterien

- Ruleset `19138299` readback proves intended controls on `master`.
- PR #53 at `d5781bd15cd286608168b952dfeb7f2d7ab29772` demonstrated six exact required checks without bypass and its authorized squash merge produced master `a589cb662fb03deb764f78eefbb1056bc64d63e2`.
- A reviewer exists before required human approval is configured.
- `SECURITY.md` and `SECURITY.de.md` are merged via reviewed PR #53; GitHub GraphQL returns `https://github.com/Easton97-Jens/ModSecurity-conector/security/policy` as `securityPolicyUrl`, and private vulnerability reporting is enabled.
- Every table row retains evidence, validation, and residual risk.

## Validation plan / Validierungsplan

- Re-read ruleset, effective rules, Actions permission, alerts, master, and GitHub `securityPolicyUrl` after relevant changes.
- Observe exact check contexts and mergeability without merging or bypassing.
- Run scoped bilingual/link and diff checks for the policy documents; record the Framework-gitlink limitation and verify resulting master content.
- Re-run Scorecard only after GitHub publishes a later analysis.
- Require separate feasibility evidence before SAST expansion or fuzzing.

## Regression tests / Regressionstests

- Ruleset and effective-rules API readback for `master`.
- Required-check observation on a real same-repository PR.
- Targeted bilingual/link control for policy and Change Record pairs.

## Legitimate control tests / Legitime Kontrolltests

- A clean PR head satisfies the six required checks without bypass.
- GitHub accepts a private vulnerability report without public disclosure.
- Dependabot alert inventory remains accessible after enabling alerts.

## Dependencies / Abhängigkeiten

- Independent reviewer, stable SonarCloud result, and the external CII Best Practices registration/attestation decision.
- Independent review and merge of Draft PR #120, followed by a fresh default-branch Scorecard analysis for #11 and #12.

## Blockers / Blocker

- Mandatory approval would lock out the sole owner/admin without forbidden automatic bypass.
- CII registration requires external owner attestation.
- Full-tree documentation checks cannot resolve the unpopulated Framework gitlink in the temporary clone.
- Scorecard #11 and #12 are still open on master `9e788057d2b551ba51ad7c4e6e1d8c5198b77834`; Draft PR #120 is now `BEHIND` and must be normally updated and revalidated before it can update default-branch alerts through a later merge.

## Related findings / Verwandte Findings

- `FND-PARENT-0001`, `FND-PARENT-0003`, `FND-PARENT-0018`, `FND-SONAR-0001`

## Residual risk / Restrisiko

The active configuration improves `master` protection but does not replace independent review, stable SonarCloud evidence, external CII attestation, a normal PR #120 branch update and revalidation, or the resulting-default-branch scan required for its source remediation. No risk is accepted by the current user.

## Current authoritative reconciliation / Aktueller maßgeblicher Abgleich

This section supersedes the historical Scorecard-currentness statement above.
Current Scorecard alerts are bound to resulting Parent master
`cbd8385ce1b34318c84cf8f4a5a92ef98c83f82a`: `BranchProtectionID #1`,
`CodeReviewID #7`, `MaintainedID #8`, `CIIBestPracticesID #10`,
`FuzzingID #11`, and `VulnerabilitiesID #12`. Alert #1 reports missing
approvers, CODEOWNERS review, and last-push approval; #7 reports `0/27`
approved changesets; #8 is the under-90-day condition; #10 needs external
OpenSSF Best Practices enrollment; #11 has no fuzzer integration; and #12
reports ten OSV advisory identifiers.

Dependabot #1 remains open for runtime/transitive `golang.org/x/net v0.48.0`
in `connectors/envoy/ext_proc/go.mod`; its safe floor `v0.55.0` requires
Go `1.25` while the declared module and CI baseline are Go `1.24.0`. It is
not dismissed and requires a user-compatible Go-baseline decision. CodeQL and
secret-scanning inventories are each `0` open; they are independent controls,
not closure of the Dependabot, Scorecard, or Sonar conditions. Evidence:
`post-merge-master-reconciliation-20260720T202018Z.json`
(`sha256:797efffded6d99d9d5cedb2c092547f7fb812e8a09b18f0cbd11c3cf0c6e514c`)
under
`/var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/`.

## Final Parent master reconciliation / Finaler Parent-Master-Abgleich

This section supersedes the preceding current-state section. The exact current
Parent master is `f2376bb3e39ffbe9d36faca8bcd7397477eadd10`. It retains one
open runtime/transitive Dependabot alert for `golang.org/x/net v0.48.0` and
the same six Scorecard rule IDs: `BranchProtectionID`, `CodeReviewID`,
`MaintainedID`, `CIIBestPracticesID`, `FuzzingID`, and `VulnerabilitiesID`.
CodeQL and secret-scanning inventories are each `0` open. The safe dependency
versions still require Go `1.25` while module and CI declare Go `1.24.0`; no
alert was dismissed and no governance bypass was introduced. Evidence:
`post-pr70-master-reconciliation-20260720T204648Z.json`
(`sha256:ac9753d9ba2bb2326ce53c1d9d9e160bb89ca429a18abfd9e0729a0c53366dd5`).

## Resulting Parent master reconciliation after PR #71 / Abgleich des resultierenden Parent-Masters nach PR #71

This section supersedes the preceding current-master statement. PR #71 head
`b1eef0a087432aa9bf9bc1243a34b0b0d8f6080e` was normally squash-merged at
`2026-07-20T22:16:36Z` as Parent master
`929fe60dfca30787947027e5bd49003581a5b080`; the resulting tree
`fae388da52f5d660c8e18f06b058ec67b38adfd7` equals the reviewed PR-head tree.

- Resulting-master CodeQL run `29783353825` succeeded and the GitHub API
  reports zero open CodeQL alerts.
- Resulting-master Scorecard run `29783353831` succeeded, but the same six
  Scorecard alerts remain open: `BranchProtectionID #1`, `CodeReviewID #7`,
  `MaintainedID #8`, `CIIBestPracticesID #10`, `FuzzingID #11`, and
  `VulnerabilitiesID #12`.
- Dynamic Dependabot runs `29783426906` and `29783429481` succeeded, but
  runtime/transitive `golang.org/x/net v0.48.0` Dependabot alert #1 remains
  open. Its supported floor requires Go 1.25, so it is not dismissed or
  risk-accepted while the supported-baseline decision is pending.
- GitHub Secret Scanning has zero active alerts. Separate secret workflow
  `29783388295` establishes advisory-wrapper success only; no raw Gitleaks
  result or count is retained, so the raw scanner disposition remains unknown.
- Sonar analysis `ee3e3400-36fb-452f-b396-775b6c4c2040` remains Quality Gate
  `ERROR` for `new_security_rating=5` and zero reviewed new-security hotspots,
  with 220 unresolved `VULNERABILITY` issues and three `TO_REVIEW` hotspots.

Evidence artifact:
`/var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/resulting-master-go12413-delivery-and-scan-reconciliation-20260720T221900Z.json`
(SHA-256 `f8e8fa49a9aa8639b61946b49fca49bc0fc06623a80554f4145f78ade6ad71b2`).
`FND-GITHUB-0001` remains `in_progress`; no open external alert was closed.

## History / Historie

- `2026-07-17T10:43:59Z`: `bootstrap_created` — retained-evidence bootstrap; no remediation, verification, closure, or risk acceptance.
- `2026-07-18T08:49:52Z`: `governance_inventory_and_bounded_remediation` — updated to the live eight-point aggregate. The existing `.codex` mount denies creation of additional canonical finding directories; point records remain in this canonical aggregate without falsely claiming separate directory allocation.
- `2026-07-18T09:21:20Z`: `post_write_readback_and_pr_control_validation` — ruleset, effective rules, Actions permissions, vulnerability alerts, Dependabot inventory, and the Dependency Graph SBOM were reread. The SBOM endpoint returned `200` and recorded `golang.org/x/net v0.48.0`. PR #53 at `d5781bd15cd286608168b952dfeb7f2d7ab29772` was `CLEAN`/mergeable with six exact required checks successful, no reviews, and zero review threads. The visible Scorecard alerts still report the pre-remediation analysis from `2026-07-16`; no score result was inferred.
- `2026-07-19T10:48:14Z`: `security_policy_master_merge_and_recognition_verified` — authorized PR #53 was squash-merged at `2026-07-19T10:42:53Z` as master `a589cb662fb03deb764f78eefbb1056bc64d63e2`. Remote master content matched reviewed head `d5781bd15cd286608168b952dfeb7f2d7ab29772`; all 14 observed master push workflows succeeded. Private vulnerability reporting read `enabled=true`, and GitHub GraphQL returned `securityPolicyUrl` `https://github.com/Easton97-Jens/ModSecurity-conector/security/policy`. This verifies only the Security-Policy point; the aggregate finding remains `in_progress`.
- `2026-07-20T22:19:00Z`: `post_pr71_resulting_master_github_sonar_reconciled` — PR #71 was protected-squash merged as `929fe60dfca30787947027e5bd49003581a5b080`; resulting-master CodeQL is clear, while Dependabot #1, six Scorecard alerts, the raw secret-scan evidence gap, and the Sonar Quality Gate remain open or blocked. No alert was closed or risk accepted.

## Current reconciliation — 2026-07-23

Authenticated GitHub inventory on current master
`a308d7b414f0859490fe7253e0683a4bde80b563` confirms exactly two open
Dependabot alerts (#1 `golang.org/x/net`, #2 `google.golang.org/grpc`) and six
open Scorecard alerts (#1 BranchProtectionID, #7 CodeReviewID, #8 MaintainedID,
#10 CIIBestPracticesID, #11 FuzzingID, and #12 VulnerabilitiesID). No alert was
closed, dismissed, or treated as fixed.

The effective ruleset still protects against deletion, non-fast-forward updates,
and direct changes outside pull requests, but it requires zero approvals and no
code-owner or last-push approval. An immediate settings change remains unsafe:
only one direct administrator/reviewer is evidenced, so a required approval
would create a merge lockout. CII remains an external OpenSSF registration and
attestation decision; Maintained remains an age-gated Scorecard metric.

Fuzzing is no longer a target-definition blocker. The Traefik native middleware
has a bounded custom UDS result-frame parser suitable for a real Go fuzz target
with valid allow/deny/redirect seeds and a 10-second bounded invocation in the
existing `traefik-go` CI job. It must be delivered in a separate Parent Draft
PR and cannot close alert #11 until it reaches master and a default-branch
Scorecard refresh is observed.

VulnerabilitiesID remains open: only the two current Go dependency roots are
individually mapped; the aggregate alert contains additional IDs that require
raw scanner/package evidence. The required Go dependency and fuzz validation is
blocked by the host's absent Go `1.26.5` toolchain; explicit current-user
authorization is required for isolated official toolchain acquisition/use.

Retained current inventory:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/github/09-current-github-alert-inventory.json`
(SHA-256 `50921ba77734f5a5e219ee65c4e1813daf96f18956f41876298f43eb599e3a5c`).

## Draft-PR delivery update — 2026-07-23

The current task evidence supersedes the above task-local toolchain and
target-definition blockers only. The current user authorized a side-by-side
official Go `1.26.5` in the registered private task cache; its archive
SHA-256 matched `5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053`.

- Draft PR [#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99)
  head `2f0d8a234f984b731229aca01d43caf2749a7d61` remediates the Envoy
  gRPC/x-net/x-sys/x-text floors. Its exact-head CodeQL, OSV, SonarCloud,
  secret-scan, Scorecard-PR, lint, and project checks passed.
- Draft PR [#100](https://github.com/Easton97-Jens/ModSecurity-conector/pull/100)
  head `4602c573b86b397712a2528bbce67fd3af891396` adds the bounded Traefik
  UDS parser fuzz target and its existing-CodeQL-job invocation. Its identical
  exact-head check set passed.

Fresh authenticated post-delivery reads still show Dependabot #1/#2 and all
six Scorecard alerts on master
`a308d7b414f0859490fe7253e0683a4bde80b563`. All 13 VulnerabilitiesID rows are
now mapped: Draft PR #99 addresses the Go roots; the two PyYAML rows are
already safe under the current declaration/CI lock/use. FuzzingID is remediated
only on Draft PR #100. Neither Draft PR reaches master, so no alert is eligible
for closure, dismissal, or fixed status. The separate governance/age/CII
external requirements remain unchanged.

Retained delivery evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T165434Z-github-alert-remediation-go1265-4fc93743/evidence/delivery/20260723-draft-pr-delivery-alert-state.md`
(SHA-256 `7508110eef978259f0b9757df675844535b44bd5e6a4dc30c92d265da05110de`).

## PR #111 exact-head Traefik fuzz timing observation — 2026-07-24

Eligible Parent-only PR #111 head
`2549d15f3181d236eeb83829818a6b03b273edcd`, based on
`5f831257949f4b2655347e2f8bcb2dd5e094a260`, does not change either
`.github/workflows/ci-security-codeql.yml` or
`connectors/traefik/native_middleware`. Its first exact-head CodeQL attempt
(run `30102616292`, job `89512179584`) reached the bounded command
`GOTOOLCHAIN=local go test -mod=readonly -run='^$' -fuzz='^FuzzUDSFrameAndResult$' -fuzztime=15s -parallel=1 .`
and ended after `15.06s` with `context deadline exceeded`.

The immediately preceding resulting master
`5f831257949f4b2655347e2f8bcb2dd5e094a260` passed the same Traefik fuzz job
(`89507225557`) in CodeQL run `30101153404`. One repository-policy-permitted
diagnostic retry of the failing job, with no source change, passed on the same
PR head as job `89513231832`; the fuzz step ran from `14:54:00Z` to
`14:54:36Z`, and CodeQL run `30102616292` attempt 2 completed successfully at
`14:55:06Z`.

The current disposition is a transient CI timing incident, not a PR #111
source or workflow defect. No security control was weakened, no code change or
risk acceptance is needed, and `FND-GITHUB-0001` remains `in_progress`.
Investigate CI stability only if this bounded fuzz job recurs. Local Go
confirmation is `blocked_environment`: the host attempted to obtain Go 1.26.5
under read-only `/root/go`, so it is not treated as product evidence.

Evidence artifact:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b/evidence/pr111-traefik-go-timing-retry.json`
(SHA-256 `1cf369ee311f012a9a584bd30cc535b0061ec9eb2e072e431307aa3b6cd4f8fe`).

## Current-master alert closure reconciliation — 2026-07-24

The authoritative Parent master is
`8e36b86ac17bce06003b0505fe26f6bb60c3cec7`. PR
[#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99) was
merged from `2f0d8a234f984b731229aca01d43caf2749a7d61` as
`5b8db00d44ab24f3a9f4216a00f7edee977b6898`; PR
[#100](https://github.com/Easton97-Jens/ModSecurity-conector/pull/100) was
merged from `dace5ca118a89a91c33fde952a6282f9c391ee10` as
`6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d`. Both exact heads have 33
successful and six scope-appropriate skipped checks. All 14 observed current-
master push workflows are successful, including CodeQL security analysis and
OpenSSF Scorecard; a successful Scorecard workflow does not itself clear an
individual active Scorecard alert.

GitHub now reports Dependabot #1 (`golang.org/x/net`) and #2
(`google.golang.org/grpc`) as `fixed`, with `dismissed_at = null`; the current
open-Dependabot query returns `[]`. That verified Go scope is closed in
`FND-PARENT-0001`, not manually dismissed here.

All six Scorecard alerts remain `open` on the same current master SHA and are
therefore retained:

| Alert | Rule | Current disposition |
| ---: | --- | --- |
| #1 | `BranchProtectionID` | Missing approvers, CODEOWNERS review, and last-push approval require a governance decision. |
| #7 | `CodeReviewID` | Scorecard observes 0/26 approved changesets; real independent review history is required. |
| #8 | `MaintainedID` | Repository age is below 90 days; this is time-based. |
| #10 | `CIIBestPracticesID` | External OpenSSF Best Practices registration/attestation is required. |
| #11 | `FuzzingID` | Still reports no fuzzer integration. The merged bounded `FuzzUDSFrameAndResult` control passed for 15 seconds with 99,749 executions, but an active current scanner result is not manually dismissed. |
| #12 | `VulnerabilitiesID` | Still reports the two PyYAML advisory identifiers; an active current scanner result is not manually dismissed. |

No Scorecard alert was closed, dismissed, suppressed, or risk-accepted. The
finding remains `in_progress` until each active external condition is either
actually remediated and rescanned or receives a separate, explicit,
evidence-backed disposition.

Retained evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/github-alert-closure-verification.md`
(SHA-256 `20ea82fbd04cc7ea672a644c4c5c5621b38b6fc29ce76ed9c54f028ca458afdf`).

## History update — 2026-07-24

- `2026-07-24T15:43:59Z`: `current_master_alert_closure_reconciled` —
  Dependabot closure and active current-master Scorecard retention were
  revalidated. The closed Go dependency scope moved to `FND-PARENT-0001`; this
  aggregate finding remains `in_progress` without any unsafe external closure.

## Post-master advance recheck — 2026-07-24

Authoritative Parent `master` subsequently advanced one commit to
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0`. The comparison from
`8e36b86ac17bce06003b0505fe26f6bb60c3cec7` changes only the bilingual Change
Record/index and `tests/test_full_lifecycle_evidence.py`; it does not change
the Envoy Go modules or the Traefik fuzz target. Dependabot #1/#2 remain
`fixed` without dismissal and the open inventory remains empty; all 14
observed current-master push workflows are successful.

The same six current Scorecard alerts remain open on this newer master:
`BranchProtectionID #1`, `CodeReviewID #7`, `MaintainedID #8`,
`CIIBestPracticesID #10`, `FuzzingID #11`, and `VulnerabilitiesID #12`.
Accordingly, `FND-PARENT-0001` remains closed and this aggregate finding
remains `in_progress`; no Scorecard alert was dismissed, suppressed, closed,
or risk-accepted.

Retained recheck evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-advance-recheck.md`
(SHA-256 `c099c32564c1a78e60f98a61ba350904669d9c7231459c4109587088e31f915f`).

- `2026-07-24T16:00:01Z`: `post_master_advance_alert_rechecked` — the
  current authoritative state was re-read after a scope-irrelevant master
  advance; closure and retention dispositions remain unchanged.

## Second post-master advance recheck — 2026-07-24

Authoritative Parent `master` advanced again to
`185fd358bcfabe63464ab0e135eecedf24c9a699`. The one-commit comparison from
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` changes only a bilingual Change
Record/index and `tests/test_full_lifecycle_profiles.py`; it does not change
the Envoy Go modules or Traefik fuzz target. Dependabot #1/#2 remain `fixed`
without dismissal and the open inventory remains empty.

The six open Scorecard alerts remain open, with their latest alert instances
still bound to `a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0`; GitHub has not
published a newer Scorecard alert instance for the current master. The current
master has 14 completed push-workflow runs: 13 successes and a failed OpenSSF
Scorecard `default-branch` run (`30107490735`); its check inventory also shows
a failed SonarCloud Code Analysis check. None of these conditions was
dismissed, suppressed, closed, or risk-accepted. `FND-PARENT-0001` remains
closed; this aggregate remains `in_progress`.

Retained second-recheck evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-second-advance-recheck.md`
(SHA-256 `17f4abdf4be2939aca498746e9e345d0e33566580adbee0b6e92427bf73b1c8b`).

- `2026-07-24T16:07:44Z`: `post_master_second_advance_alert_rechecked` —
  latest-master scope, alert-instance currentness, Dependabot state, and the
  Scorecard/Sonar workflow failures were retained with no unsafe closure.

## Final current-master recheck after Scorecard retry — 2026-07-24

The authoritative Parent `master` remains
`185fd358bcfabe63464ab0e135eecedf24c9a699`. Dependabot #1/#2 remain `fixed`
without dismissal and no Dependabot alerts are open. OpenSSF Scorecard run
`30107490735`, attempt 3, succeeded, so all 14 observed GitHub Actions push
workflows now have conclusion `success`.

GitHub has refreshed all six still-open Scorecard alerts to this same current
master SHA: `BranchProtectionID #1`, `CodeReviewID #7`, `MaintainedID #8`,
`CIIBestPracticesID #10`, `FuzzingID #11`, and `VulnerabilitiesID #12`.
SonarCloud Code Analysis remains failed. The successful workflow retry does
not clear any active Scorecard alert; no alert was dismissed, suppressed,
closed, or risk-accepted. `FND-PARENT-0001` remains closed and this aggregate
finding remains `in_progress`.

Retained final recheck evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-scorecard-retry-final-recheck.md`
(SHA-256 `2a788454ba88bcd90add62b5eae3545d83a53180f7aefe8c72ffc864a2959746`).

- `2026-07-24T16:14:53Z`: `post_master_final_current_alert_rechecked` — the
  Scorecard retry and all Actions workflows are successful; refreshed active
  Scorecard alerts and the failed SonarCloud check remain retained follow-up.

## Draft PR #120 exact-head validation — 2026-07-24

Fresh authenticated GitHub readback reports the same six Scorecard alerts
`open` on authoritative Parent master
`30ee953b57f4aafebaa0e6ed565a80f6500db1de`: `BranchProtectionID #1`,
`CodeReviewID #7`, `MaintainedID #8`, `CIIBestPracticesID #10`,
`FuzzingID #11`, and `VulnerabilitiesID #12`.

Draft PR [#120](https://github.com/Easton97-Jens/ModSecurity-conector/pull/120)
is `OPEN`, `CLEAN`, and mergeable against that master. Its exact head
`57c411eeca7be024e5718d560e26e4bc051b92ae` passed all 33 applicable terminal
hosted checks, with six scope-appropriate skips; OSV and SonarCloud passed.
CodeQL run `30111632630`, bounded-c-cpp job `89542295414`, executed **Fuzz
Common HTTP header parser** successfully from `2026-07-24T17:06:15Z` through
`2026-07-24T17:06:42Z`.

The PR adds a real C/libFuzzer harness at
`fuzz/common_http_headers_fuzz.c` for the Common HTTP-header parser, bounded
by an external-build runner and invoked in the existing CodeQL job. It also
pins development PyYAML to `PyYAML==6.0.3`, matching the CI hash lock and
giving the OSV parser an unambiguous safe version. This is the narrowest
source-owned remediation for #11 and #12; no scanner suppression, fake marker,
or quality-gate weakening is used.

The PR-event Scorecard run `30111632360`, job `89542294656`, passed, but its
`default-branch` step is correctly skipped on a `pull_request` event. It
cannot update SARIF or clear default-branch alerts. Therefore #11 and #12 are
`verified_draft_pr_pending_resulting_master_scorecard_refresh`, not closed.
The other four alerts remain outside this PR: #1 needs a ruleset/independent-
review configuration decision, #7 needs genuine independent-review history,
and #8 is age-gated until `2026-08-12`, while #10 needs owner-led OpenSSF Best
Practices registration and attestation.

No Scorecard alert was closed, dismissed, suppressed, or risk-accepted. The
next legitimate step is independent review and merge of the Draft PR, followed
by a fresh default-branch Scorecard analysis of the resulting master.

Retained exact-head evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T164102Z-scorecard-alert-remediation-pr-7c78e095/evidence/pr120-exact-head-validation.md`
(SHA-256 `24225b5a3c44a960dcaf3e0dc595a8560546058b019da63d99ce898dcfe9e453`).

- `2026-07-24T17:13:44Z`: `draft_pr120_exact_head_verified` — #11 and #12
  are exact-head-verified Draft-PR source remediations pending independent
  review, merge, and resulting-master Scorecard refresh. #1/#7/#8/#10 remain
  external requirements; all six alerts remain open.

## Draft PR #120 base-advance recheck — 2026-07-24

After the exact-head validation, remote master advanced one non-overlapping
commit from `30ee953b57f4aafebaa0e6ed565a80f6500db1de` to
`9e788057d2b551ba51ad7c4e6e1d8c5198b77834`. The comparison changes only
`ci/checks/common/check-adapter-helpers.sh` and its paired bilingual Change
Record/index; it does not overlap the C header fuzzer, bounded runner, CodeQL
integration, PyYAML pin, focused test, or Change Record in PR #120.

PR #120 remains `OPEN`/Draft at exact head
`57c411eeca7be024e5718d560e26e4bc051b92ae`. GitHub reports it
`mergeable=MERGEABLE` but `mergeStateStatus=BEHIND`. The earlier 33-success
hosted result remains valid evidence for that exact source revision, not an
exact current-merge-candidate result. A fresh authenticated Scorecard readback
binds all six open alerts #1/#7/#8/#10/#11/#12 to current master
`9e788057d2b551ba51ad7c4e6e1d8c5198b77834`.

No PR-branch update, rebase, force push, merge commit, master merge, alert
dismissal, suppression, closure, or risk acceptance was performed. The task
prohibits merge and force push. A separately authorized normal branch update
and fresh exact-head validation are required before the Draft PR can be
reviewed as current and later merged. #11 and #12 therefore remain source-
remediated but `behind_current_master`; all six alerts remain open.

Retained recheck evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T164102Z-scorecard-alert-remediation-pr-7c78e095/evidence/pr120-base-advance-recheck.md`
(SHA-256 `c47ae53a06ddf584a0edac3ddacbfea168a7cc8edb9029a082ef4a0535b57e6f`).

- `2026-07-24T17:25:15Z`: `draft_pr120_base_advance_rechecked` — current
  master moved ahead without source overlap. The PR remains a valid source
  patch but needs an authorized normal update and fresh exact-head checks;
  no prohibited merge or force operation occurred.

## Current GitHub reconciliation and closure — 2026-07-26

This section supersedes the prior current-state narrative. Read-only GitHub
reconciliation at 2026-07-26T13:29:40Z against Parent master
`6ca7e1536ce7e93da68099db9c586b88852ff13e` returned no open Scorecard
alerts. The six tracked source alerts are terminal:

- `BranchProtectionID #1`, `CodeReviewID #7`, and
  `MaintainedID #8`: dismissed as false positive.
- `CIIBestPracticesID #10`: dismissed as used in tests.
- `FuzzingID #11` and `VulnerabilitiesID #12`: fixed.

Parent PRs #99, #100, and #120 are merged. The current Protect-master ruleset
is active, has no bypass actors, and retains strict required checks plus
deletion/non-fast-forward controls. Actions default permission is read, private
vulnerability reporting is enabled, and the repository security policy URL is
present.

The aggregate GitHub source condition is therefore `closed` and the
complete EN/DE/JSON triplet is archived with its historical evidence. This is
not a production-governance certification: before production, publication, or
release, restore this record and revalidate approval, CODEOWNERS, attestation,
and then-current Scorecard requirements.
