# FND-FRAMEWORK-0028 — Framework automatic ModSecurity v3 updater can plan an incomplete provenance identity change

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0028 |
| Category | security_hardening |
| Repository / ownership | framework / framework |
| Priority / severity | P2 / medium |
| Confidence / status | validated / verified |
| Feasibility | feasible_now |
| Release blocker | false |
| Security relevant | true |

## Summary, observation, expected behavior, and impact

After the parser repair makes ModSecurity v3 approved literals visible, a live
check reports v3.0.15 outdated and plans to change only
MODSECURITY_V3_GIT_REF at line 184 to v3.0.16. The scheduled privileged
workflow writes common.sh and creates a pull request, but it cannot
simultaneously establish the reviewed release-tag-to-immutable-commit identity.

The automated updater must not write a partial ModSecurity v3 identity. A new
release must remain an explicit review item unless the updater can atomically
verify and update the release tag, repository identity, and approved immutable
commit.

Runtime provenance validation rejects the inconsistent alias fail-closed, so
this is not a confirmed supply-chain bypass. However, the privileged scheduled
workflow could create unusable update pull requests and pressure an operator to
weaken a provenance control. Preventing partial automation preserves the
approved tag-to-commit boundary.

## Scope, preconditions, reproduction, and evidence

Affected Framework paths are ci/tools/check-common-versions.py,
.github/workflows/check-common-versions.yml, and ci/lib/common.sh. The
relevant symbols are check_github_release_ref, check_all,
MODSECURITY_V3_GIT_REF, MODSECURITY_V3_RELEASE_TAG,
MODSECURITY_V3_APPROVED_COMMIT, and ci_require_approved_modsecurity_v3_provenance.

The issue requires resolved approved literals, a newer GitHub ModSecurity v3
release, and the scheduled workflow running --update with contents and
pull-requests write permissions.

1. Run python3 ci/tools/check-common-versions.py --check --json --timeout 20.
2. Observe an outdated ModSecurity v3 component and an update plan for only
   MODSECURITY_V3_GIT_REF.
3. Inspect the scheduled workflow write mode and the runtime provenance
   invariant.
4. Confirm the plan does not update MODSECURITY_V3_RELEASE_TAG or
   MODSECURITY_V3_APPROVED_COMMIT atomically.

Retained evidence:

- Run: 20260720T080314Z-parent-pr55-57-59-framework-update-3443af13
- Artifact:
  /var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/framework-common-version-parser/modsecurity-v3-auto-update-plan.json
- Type: framework_modsecurity_v3_partial_auto_update_plan
- SHA-256: 93f14b78781506a54f7d04f36067b50f47d95c1f94eb9147e309eb7435597368
- Command: python3 ci/tools/check-common-versions.py --check --json --timeout 20;
  source and scheduled-workflow review
- Working directory: /var/tmp/codex/worktrees/framework-common-version-parser
- Exit code: 1
- Observed: 2026-07-20T09:01:13Z
- Retention: retained
- Result: only MODSECURITY_V3_GIT_REF is planned to change from its release-tag
  alias to v3.0.16.

## Root cause and proposed remediation

check_all invokes the generic check_github_release_ref with the compatibility
alias MODSECURITY_V3_GIT_REF as ref_var. The generic updater cannot
authenticate a release tag to its immutable commit or update the coupled
approved identity atomically.

Model ModSecurity v3 after the existing CRS provenance path: check the
approved repository/release tag, report a newer release as unknown/manual
review, and clear automatic updates. Add a focused regression proving an
outdated ModSecurity v3 release cannot change the compatibility alias alone.

## Acceptance criteria and validation plan

- [x] An outdated ModSecurity v3 release produces no automatic update for
  MODSECURITY_V3_GIT_REF.
- [x] The component reports a review-required unknown/manual-review state rather than a
  partial update.
- [x] The candidate component result yields exit code zero when only
  review-required unknown states remain.
- [x] Runtime exact-commit and alias-equality provenance checks remain
  unchanged.
- [x] No Parent, Sonar control, or MRTS file changes.

Add focused in-memory release-client coverage, run the focused common-version
provenance suite and ModSecurity v3 provenance contract, and review the
candidate's empty update list. Update mode must never run against canonical
common.sh; no fixture write is needed when the candidate has no ModSecurity v3
update to apply. Review the exact diff and collect exact-head Framework PR
checks.

## Local remediation and observed validation

The same isolated Framework task branch adds
`check_modsecurity_v3_release_provenance`. It checks the approved repository
and reviewed release-tag anchor, reports a newer release as `unknown` / manual
review, and clears all update instructions. The compatibility aliases therefore
cannot be changed alone by the scheduled writer.

The in-memory newer-release regression asserts `STATUS_UNKNOWN`, an empty
update list, the exact review reason, and `exit_code([result]) == 0`. The
focused suite passed 15 tests; the existing 10-test ModSecurity v3 provenance
contract, documentation checks, and Framework lint all passed. Independent
source-security review and follow-up found no bypass, permission expansion, or
MRTS change.

The canonical writing update command was deliberately not run. Static review
and the empty update list establish that its update applicator has no
ModSecurity v3 write to perform.

Framework Draft PR [#36](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/36)
now provides exact-head hosted evidence for
`2bf862e1a5f262251043ec421447f6e4db11e17d` against base
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`: it is open, Draft, and mergeable
`CLEAN`. All 14 terminal checks are current: 11 succeeded (including CodeQL
Actions/Python/C++, SonarCloud Code Analysis, PR-head/range, scaffold-lint, and
common-structure); 3 advisory checks are expected skips; none failed,
cancelled, or remains pending. No review or unresolved review thread was
observed.

Post-merge lifecycle/evidence event at `2026-07-20T13:10:07Z`: PR #36 was
normally merged at `2026-07-20T13:06:39Z` as Framework master
`784977615acfc55567e37b863309abc4a38ac877`. Refreshed PR head
`1608352912a755f0f8639eddfa2350436446067e` is an ancestor and its tree equals
that master. Fresh hosted evidence for that exact head passed: CodeQL Actions,
Python, and C++; OSV; OpenSSF; secret scanning; lint; test-common; and the PR
SonarQube Cloud Quality Gate with 0 new issues, 0 Security Hotspots, and 0.0%
duplication. No human review, review request, or unresolved review thread was
observed. Resulting-master CodeQL Actions/Python/C++, lint, test-common, and
OpenSSF also passed. The separate master Sonar check failed only with inherited
FND-SONAR-0002 Security E, under the current user's bounded master-only
acceptance; no causality is attributed to this finding.

The retained isolated exact-master original-reproduction artifact
`analysis/pr36-master-common-version-original-reproduction.json`
(SHA-256 `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`)
records exit code 0 for `--check --json --timeout 20`: ModSecurity v3.0.15
versus v3.0.16 remains `unknown` / manual review with an empty update list,
while `missing_required` is empty and all approved anchors and aliases resolve.
The command used `--check` only and did not invoke `--update`, `--markdown`,
or `--write-files`. The prior local 15/15 parser, 10/10 provenance-contract,
`py_compile`, bilingual/documentation, and diff checks remain part of the
exact-head evidence. The separate FND-SONAR-0002 acceptance does not waive any
fresh PR-head check, PR Sonar gate, review, permission, or security control.

## Regression and legitimate-control tests

Regression tests:

- tests/security_regression/test_common_versions_sonar_provenance.py
- make test-modsecurity-v3-provenance-contract

Legitimate controls:

- The current approved ModSecurity v3 release remains current with no update.
- A newer release remains visible for manual review without changing common.sh.
- Runtime provenance still rejects mismatched aliases or immutable commits.

## Dependencies, boundaries, related findings, and residual risk

The historical exact-head and current exact-master controls now satisfy this
finding's source-validation dependency; GitHub Releases API availability
remains a legitimate runtime dependency of the checker. This is not a duplicate
of FND-FRAMEWORK-0027: that finding owns missing literal resolution, while this
one owns partial automatic updates made reachable after the literals resolve.

The normal Framework-master delivery occurred without a Parent file or Parent
gitlink update and without an MRTS content or Git action. Update mode was not
run against canonical common.sh to avoid source mutation. The runtime control
continues to reject the inconsistent outcome, so no successful malicious
dependency update was reproduced.

Manual ModSecurity v3 release maintenance remains necessary until a safe
tag-to-immutable-commit resolver is designed and reviewed. This repair
intentionally preserves manual review rather than synthesizing a commit pin
from an unverified release tag.

## Current delivery disposition

This finding is `verified`, not `closed` or risk-accepted. PR #36 was normally
merged as exact Framework master `784977615acfc55567e37b863309abc4a38ac877`;
its tree equals refreshed head `1608352912a755f0f8639eddfa2350436446067e`, and
the original partial-auto-update reproduction plus legitimate controls passed
on that master. FND-SONAR-0002 remains a separate blocked Framework-master
issue with a bounded master-only acceptance; it does not alter this finding's
verified status or waive its PR controls. No Parent gitlink or MRTS action
occurred.

## History

- 2026-07-20T09:01:13Z — confirmed_during_fnd_framework_0027_security_review:
  the live check planned only MODSECURITY_V3_GIT_REF=v3.0.16. Security review
  confirmed runtime remains fail-closed, but the scheduled privileged updater
  could otherwise create an inconsistent pull request.
- 2026-07-20T09:36:58Z — local_remediation_validated: the provenance wrapper
  converts a newer ModSecurity v3 release into an empty-update manual-review
  result and the focused, contract, documentation, lint, and independent
  security checks passed. Exact-head Draft-PR evidence remains pending; no
  Framework master, Parent, or MRTS Git action occurred.
- 2026-07-20T10:14:31Z — fixed_on_framework_pr_36_exact_head_validated: Draft
  PR #36 exact head `2bf862e1a5f262251043ec421447f6e4db11e17d`, based on
  `efdbcbd98afeed0f39f8912ce1140aaa5742f507`, is mergeable CLEAN with 11
  successful and 3 expected-skipped terminal checks and no failed/pending
  check, review, or unresolved review thread. Master merge, current-master
  reproduction, Parent gitlink, and MRTS actions remain out of scope.
- 2026-07-20T13:10:07Z — verified_on_framework_master_after_pr_36_normal_merge:
  PR #36 was normally merged at `2026-07-20T13:06:39Z` as Framework master
  `784977615acfc55567e37b863309abc4a38ac877`; exact head
  `1608352912a755f0f8639eddfa2350436446067e` is an ancestor with a tree equal
  to master. Fresh PR-head controls and resulting-master CodeQL Actions/Python/
  C++, lint, test-common, and OpenSSF passed. The retained exact-master
  artifact `analysis/pr36-master-common-version-original-reproduction.json`
  (SHA-256 `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`)
  records exit 0, v3.0.15 versus v3.0.16 as `unknown` / manual review, and an
  empty update list. The master Sonar Security E is the separate inherited
  FND-SONAR-0002 gate under a bounded acceptance, not a causal disposition of
  this finding; no Parent gitlink or MRTS action occurred.
