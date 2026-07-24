# Change Record: Parent adapter-helper explicit default case for SonarQube Cloud S131

**Language:** English | [Deutsch](CR-20260724-sonar-ci-adapter-helpers-default-case.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260724-sonar-ci-adapter-helpers-default-case |
| Date (UTC) | 2026-07-24 |
| Base revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
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

- rtk proxy -- sh -n ci/checks/common/check-adapter-helpers.sh
- rtk proxy -- sh -c <checkout-contained BUILD_ROOT exit-77 control>
- rtk proxy -- rg <exact empty default-arm inventory>
- rtk proxy -- shellcheck ci/checks/common/check-adapter-helpers.sh
- rtk proxy -- git diff --check

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Official current key and all open-PR selected-path overlap queries | passed: the one Parent key is OPEN on the recorded base and none of the 20 open PRs changes the selected file. |
| Shell syntax before and after the edit | passed. |
| Checkout-contained Build-root control before and after the edit | passed: the script prints the existing rejection and returns expected exit 77 before Framework metadata access. |
| Exact source inventory | passed: exactly one empty default arm is present at the selected case. |
| Focused path-control security review | passed: the only source delta is an empty default arm; canonicalization, reject pattern/message, exit 77, and later commands are unchanged. |
| git diff --check | passed: no whitespace error. |
| Current-batch worktree bytecode scan | passed: no Python bytecode file. |
| ShellCheck | baseline-equivalent warning result: SC1007 at existing canonicalization lines 4 and 23 before and after the edit; the new default arm introduces no warning. These pre-existing warnings are outside this one-key batch and are not suppressed. |
| tests.test_bilingual_docs and direct Change Record/index parity | passed: 11 tests; both Change Records have 13 level-two sections and matching Change ID, base revision, key, and affected path. |
| make check-bilingual-docs | blocked_environment: exactly 20 existing missing Framework-gitlink link targets; no new Change Record error. |
| make check-doc-links | blocked_environment: exactly 16 existing missing Framework-gitlink link targets; no Framework source, gitlink, or generated artifact changed. |
| Hosted-delivery checks | pending: no Draft PR exists yet. |

## Runtime evidence

No full successful adapter-helper script run is claimed. It requires excluded
Framework adapter metadata. The changed arm executes only after a non-checkout
root match and is empty; direct pre/post evidence covers the affected
checkout-root policy branch without initializing, mocking, or modifying
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
  result, and review state await a future open Draft PR and are not claimed.

## Known limitations

This batch corrects only one selected Parent SonarQube Cloud finding. It does
not claim to remediate the wider 1,474-item SonarQube Cloud backlog.

## Remaining risks

An unintended edit to the existing reject arm could weaken Build-root
containment. The one-line no-op diff, exact exit-77 negative control, syntax
check, and pending exact-head hosted validation reduce that risk. The full
success route remains blocked only by excluded unavailable Framework metadata.

## Final diff and review status

The source correction and initial English/German traceability material are
locally validated on task branch
codex/sonar-ci-adapter-helpers-default-case-20260724-master-5b8db00 from base
5b8db00d44ab24f3a9f4216a00f7edee977b6898. No commit, push, PR, merge,
default-branch update, Framework action, MRTS action, scanner-control change,
or suppression has occurred. Final delivery facts are added only after they
are observed on an open, unmerged Draft PR.
