# Change Record: Parent adapter-helper explicit default case for SonarQube Cloud S131

**Language:** English | [Deutsch](CR-20260724-sonar-ci-adapter-helpers-default-case.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260724-sonar-ci-adapter-helpers-default-case |
| Date (UTC) | 2026-07-24 |
| Base revision | 30ee953b57f4aafebaa0e6ed565a80f6500db1de |
| Original source base | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Parent SonarQube Cloud shelldre:S131 Code Smell AZ422z_PmJyaFL6eWoJF at line 23. |
| Boundary | Parent CI shell source plus this English/German traceability pair and indexes. Build-root policy, Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, generated artifacts, and runtime behavior remain unchanged. |

## Motivation and problem statement

The selected SonarQube Cloud row identifies a canonicalized BUILD_ROOT case
that rejects checkout-contained roots but lacks an explicit default arm. An
unmatched shell case already continues to later validation; representing that
intent with an empty default arm resolves the maintainability observation
without changing any allowed or rejected root.

## Acceptance criteria

- Add only one explicit empty default arm to the selected case.
- Preserve canonicalization, the checkout-root pattern, rejection message,
  exit 77, and every later command byte-for-byte.
- Pass shell syntax and prove the checkout-contained Build-root control still
  rejects with expected exit 77 before Framework metadata access.
- Maintain synchronized English/German Change Records and indexes.
- Obtain exact-head GitHub and SonarQube Cloud Draft-PR evidence before
  describing the selected key as verified.

## Implementation decision and rationale

The selected case now has an explicit empty default arm after the existing
checkout-root reject arm. It is a shell semantic no-op: nonmatching roots
already fell through to later existing validation. No path is newly accepted,
no rejection is removed, and no command, variable, compiler invocation, or
Framework metadata route changes.

## Security impact

This is not a security finding, but the edited case protects a Build-root path
boundary. The focused security assessment therefore requires no-regression
evidence rather than a broad security claim. The direct pre/post negative
control confirms a canonical Build-root inside the Parent checkout still emits
the same rejection and exits 77 before any Framework metadata access. No
security control is weakened and no security finding is claimed fixed.

## Changed files

- ci/checks/common/check-adapter-helpers.sh
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- rtk proxy sh -n ci/checks/common/check-adapter-helpers.sh
- rtk proxy env FRAMEWORK_ROOT="$PWD" BUILD_ROOT="$PWD" sh ci/checks/common/check-adapter-helpers.sh
- rtk proxy rg <exact empty default-arm inventory>
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_bilingual_docs
- rtk proxy make check-bilingual-docs
- rtk proxy make check-doc-links
- rtk proxy git diff --check origin/master...HEAD

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Normal master update | passed: normal update commit `151f409800a685aa41b92e3fc8fdb14e9db09f7b` merged current Parent `master` `30ee953b57f4aafebaa0e6ed565a80f6500db1de`; only the paired Change-Record indexes conflicted and were manually reconciled. |
| Shell syntax after the master update | passed. |
| Checkout-contained Build-root control after the master update | passed: the script prints the established rejection and returns exit 77 before Framework metadata access. |
| Exact source inventory | passed: exactly one empty default arm is present at the selected case. |
| Focused path-control security review | passed: the only source delta is an empty default arm; canonicalization, reject pattern/message, exit 77, and later commands are unchanged. |
| Final Parent diff and gitlink check | passed: five Parent paths differ from current `master`; the Framework gitlink has no final PR delta and is inherited only through the normal master-update parent. |
| git diff --check | passed: no whitespace error. |
| tests.test_bilingual_docs | passed: the English/German pair and both indexes remain structurally valid. |
| make check-bilingual-docs | blocked_environment: existing missing Framework-gitlink link targets prevent the repository-wide local check; no Framework source, gitlink, or generated artifact was changed. |
| make check-doc-links | blocked_environment: existing missing Framework-gitlink link targets prevent the repository-wide local check; no Framework source, gitlink, or generated artifact was changed. |
| Hosted-delivery checks | pending: the update creates a new PR head, so checks, SonarQube Cloud, and reviews must be observed again for that exact head. |

## Runtime evidence

No full successful adapter-helper script run is claimed. It requires excluded
Framework adapter metadata. The changed arm executes only after a non-checkout
root match and is empty; the direct checkout-contained negative control covers
the affected policy branch without initializing, mocking, or modifying
Framework/MRTS.

## Checks not run and rationale

- Full successful script execution is blocked_environment by excluded
  unavailable Framework metadata. No Framework/MRTS workaround is authorized.
- Connector builds, configuration checks, host runtime smoke tests, protocol
  matrices, and MRTS checks are not applicable because no connector/runtime
  implementation or Framework/MRTS content changed.
- Ruff and Pyright are not applicable because this shell-only change has no
  configured Parent route or installed executable; no dependency is installed.
- Exact-head GitHub checks, SonarQube Cloud Quality Gate, PR issue query, bot
  result, and review state must be refreshed after the normal master update
  and documentation-reconciliation push; no stale Draft evidence is used for
  merge eligibility.

## Known limitations

This batch corrects only one selected Parent SonarQube Cloud finding. It does
not claim to remediate the wider SonarQube Cloud backlog.

## Remaining risks

An unintended edit to the existing reject arm could weaken Build-root
containment. The one-line no-op diff, exact exit-77 negative control, syntax
check, and pending exact-head hosted validation reduce that risk. The full
success route remains blocked only by excluded unavailable Framework metadata.

## Final diff and review status

The initial source correction is in Parent commit
41f8ed308bf8acb4d6688dd8639944b5e3482957 from original source base
5b8db00d44ab24f3a9f4216a00f7edee977b6898. The normal master-update commit
151f409800a685aa41b92e3fc8fdb14e9db09f7b brings the branch to current Parent
master `30ee953b57f4aafebaa0e6ed565a80f6500db1de`; it resolves only the paired
index ordering conflict. The historical Draft evidence for old head
`a0c78a5c87b3fc4a9af8e2759fa0fee9c5bd3034` is retained as history but is not
merge evidence after this update. Draft PR
[#115](https://github.com/Easton97-Jens/ModSecurity-conector/pull/115) must be
republished and freshly verified before an authorized protected merge. No
default-branch update, Framework action, MRTS action, scanner-control change,
or suppression has occurred.
