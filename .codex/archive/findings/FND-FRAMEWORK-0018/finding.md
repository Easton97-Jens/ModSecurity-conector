# FND-FRAMEWORK-0018 — CRS testing guidance contradicts fail-closed existing-checkout provenance control

## Classification

| Field | Value |
| --- | --- |
| Category | documentation_drift |
| Repository / ownership | Framework / framework |
| Priority / severity | P2 / low |
| Confidence / status | validated / verified |
| Release blocker | no |
| Security relevant | yes |
| Feasibility | feasible_now |

## Summary

## 2026-07-26 current-master verification

Framework master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` passed
`make test-crs-provenance-contract` and `make check-documentation`. The guides
and variables now express the same fail-closed contract: `CRS_SOURCE_DIR` must
be fresh and absent; existing directories and symlinks are rejected before Git.
PR #26 exact-head and resulting-master hosted checks were observed successful.
The later historical wording is superseded by this verified disposition.

The English and German CRS testing guides say that the reviewed full commit
works for existing checkouts. The exact Framework provenance implementation
instead requires an absent CRS_SOURCE_DIR and rejects a pre-existing directory
or symlink before any Git invocation. This is validated reader-facing
documentation drift with security relevance, not a demonstrated runtime
provenance bypass.

## Observed and expected behavior

Both docs/testing-and-evidence.md:99-108 and
docs/testing-and-evidence.de.md:103-114 describe existing-checkout support.
The variable references at docs/reference/variables.md:167-173 and
docs/reference/variables.de.md:171-179 require an absent source path and
fail-closed rejection of existing directories or links. The exact regression
test at tests/security_regression/test_crs_git_ref_provenance.py:247-251
creates an existing checkout containing an untrusted sentinel and asserts exit
77, no Git invocation, and sentinel preservation.

All reader-facing guidance must state that only a fresh, absent source
directory is accepted; existing directories and symlinks are rejected and must
not be reused.

## Impact, preconditions, and reproduction

An operator or automation that follows the testing guide can supply an
existing CRS_SOURCE_DIR containing stale or attacker-controlled content. The
result is failed provisioning and may encourage an unsafe manual workaround.
The static evidence does not show a code-level provenance bypass because the
implementation rejects the path.

Reproduce by inspecting PR #26 exact head
63c42e97b86acbae1374efa9f1c4209ce2ce673b against Framework master
9954b99a31fab0006cdf903ab477c8158c50fea8 and comparing the cited test,
variable-reference, and testing-guide lines.

## Evidence

| Run ID | Artifact | SHA-256 | Command / result |
| --- | --- | --- | --- |
| 20260719T081017Z-framework-pr-resolution-20260719-840082e0 | /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/analysis/security-diff-pr26/artifacts/05_findings/FND-FRAMEWORK-0018-evidence.md | 2b363eb35e8ada3bd9302bbc356159fe9d15ff3b17269e2baafda0a4a14403e8 | rtk git diff --check origin/master...HEAD and RTK-prefixed targeted reads exited 0 and reproduced the contradictory contract. |

The review was static and read-only. No tests, build, network operation,
Git/GitHub write, Parent change, or MRTS operation was performed.

## Root cause and remediation

The revised testing guides retained an inaccurate existing-checkout statement
while the provenance implementation was intentionally changed to reject
pre-existing source paths. Replace that statement in both guides with the
exact fresh-directory, fail-closed contract; retain English/German technical
parity; then re-run the focused provenance regression and relevant
documentation checks on the reconciled exact head.

## Acceptance and validation

- Both testing guides state that CRS_SOURCE_DIR must be absent/fresh and that
  existing directories or symlinks are rejected.
- The English and German statements are technically equivalent.
- tests/security_regression/test_crs_git_ref_provenance.py retains the
  existing-checkout fail-closed case and a fresh-checkout legitimate control.
- The focused provenance target and relevant documentation/bilingual checks
  pass on the reconciled exact PR head.

## Dependencies, related findings, and residual risk

The correction belongs to PR #26 exact-head reconciliation. It has no current
technical blocker. Related finding: FND-FRAMEWORK-0004.

The implementation currently fails closed, but the misleading guidance can
still cause operational failure or unsafe manual reuse attempts until the
documentation is corrected.

## History

- 2026-07-19T10:29:22Z — A read-only exact-diff security review validated the
  conflict between both testing guides and the tested implementation contract.
