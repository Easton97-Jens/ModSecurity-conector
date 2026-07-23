# Change Record: Central Go toolchain and Update-submodules validation repair

**Language:** English | [Deutsch](CR-20260722-central-go-toolchain-submodule-validation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260722-central-go-toolchain-submodule-validation |
| Date (UTC) | 2026-07-22 |
| Base revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Boundary | Parent CI/tooling, Parent tests, paired Parent documentation, and this Change Record pair only. Framework source, MRTS, the Parent gitlink, Go modules, dependencies, and action pins are unchanged. |
| Finding linkage | FND-PARENT-0045: validated Parent CI compatibility blocker for the failing Update submodules candidate validation; FND-SONAR-0011: 23 task-owned, non-gating SonarQube Cloud test maintainability observations. |
| Delivery status | Historical initial Draft PR #90 head `0acba7768848651758610928e89f4481dbb90c81` failed five ordinary push workflows at the obsolete Parent HAProxy expectation. Its later exact head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf` passed the observed ordinary checks and SonarQube Cloud Quality Gate. The current user-authorized Sonar cleanup is locally validated but not yet committed or pushed, so no fresh hosted result, review, or master integration is asserted for this continuation. |

## Motivation and problem statement

The user requested a replacement for stale PR 80 that makes Go centrally
selected like Python, safely checks for a newer Go release, and repairs the
currently failing Update submodules validation. The old Parent HAProxy fixture
contradicted the current Framework BUILD_ROOT containment control and blocked
an otherwise successfully resolved Framework candidate.

## Acceptance criteria

- One exact checked-in Go CI selector controls both ordinary CodeQL Go jobs.
- The updater proposes only a newer stable patch in the existing 1.26 series.
- The updater leaves module declarations and dependency files unchanged.
- The Update submodules regression preserves both legitimate cache reuse and
  the separate-BUILD_ROOT rejection when the selected Framework revision
  supplies that containment control.
- Local static and focused test evidence is recorded truthfully; exact-head
  hosted validation remains a separate requirement.

## Implementation decision and rationale

The root <code>.go-version</code> is the one exact Go CI toolchain authority,
initially <code>1.26.5</code>. The two CodeQL Go jobs consume it through the
immutable setup-go action with <code>go-version-file: .go-version</code> and
<code>check-latest: false</code>. It does not replace module-owned
<code>go.mod</code> language directives, and no module, <code>go.sum</code>,
dependency, or <code>toolchain</code> directive is changed.

The Go updater accepts only the official exact Go release endpoint. It rejects
redirects, non-JSON, malformed, oversized, duplicate-key, prerelease,
cross-minor, leading-zero, downgrade, and unsafe-target conditions. Its only
write operation is an atomic update of the regular root <code>.go-version</code>
after an independently expected higher <code>1.26.N</code> patch is confirmed.

The workflow separates a default-branch read-only resolver, a read-only
candidate validator, and the only narrow writer. Candidate module commands
use <code>GOTOOLCHAIN=local</code> and readonly module flags. The publisher can
create or safely update only a Draft PR whose merge-base diff is
<code>.go-version</code> alone; it has no direct master-write, force-push,
auto-merge, submodule-initialization, or module-update path.

## Changed files

- Root Go selector, Go updater, Go static contract, and focused updater tests.
- CodeQL Go selectors and the new three-stage Go updater workflow.
- Python workflow inventory and contract tests because the Go updater executes
  the bounded checked-in Python parser under the existing interpreter contract.
- Parent HAProxy cache regression tests, paired documentation, Change Record
  indexes, and this bilingual Change Record pair.
- The current three-test Sonar cleanup: assertion diagnostic order only and
  one prerelease fixture moved outside its expected exception assertion.

No Framework source, MRTS content, Parent gitlink, Go module, Go checksum,
dependency, action pin, or security-tools lock file is changed.

## Update-submodules root cause and correction

GitHub Actions run
[29945542984](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29945542984)
resolved Framework candidate f73f8842f45318e2df8aff1d31855eeb7c20a22f and
then failed three Parent HAProxy cache tests during its read-only quick check.
The candidate correctly rejects HAPROXY runtime paths outside BUILD_ROOT; its
own security regression requires that rejection. The failing Parent fixture
instead placed a runtime binary in a shared cache while independently setting
BUILD_ROOT.

The Parent direct test now models the legitimate production layout, where the
effective managed connector entry is also BUILD_ROOT. Its explicit negative
control requires exit 77 from a Framework source that supplies the strict
split-root containment contract. The known current Parent gitlink
`784977615acfc55567e37b863309abc4a38ac877` predates that contract and is
transparently skipped; any other selected revision that lacks the contract
fails. The Update submodules candidate therefore executes the exit-77 control
without making ordinary Parent PR checks misclassify the older pinned Framework
revision as a Parent regression. The test accepts a deliberately supplied
read-only Framework source for local evidence without initializing or
modifying the Parent gitlink. The workflow remains resolve then read-only
validation then narrow publisher; no permission, trigger, workflow, or
Framework-source change bypasses the failure.

## Commands executed

- The focused suite using the reviewed read-only Framework root ran 61 tests
  and exited 0: Go updater/contract, Python workflow contract, CI-security,
  and Parent runtime-component regression coverage all passed.
- `make check-go-version-contract check-python-version-contract
  check-ci-security-contract` exited 0; the Python contract reported Python
  3.14.6 and 28 Python-executing workflow jobs, and 16 CI-security tests
  passed.
- `tests.test_bilingual_docs` ran 11 tests and exited 0. The final focused
  security-diff review is a separate required staging precondition for this
  final three-file follow-up.
- `git diff --check` passed during final local review; it is repeated as a
  staging precondition.
- Initial Draft PR #90 head
  `0acba7768848651758610928e89f4481dbb90c81` triggered the completed push
  runs [29955277020](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277020),
  [29955277057](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277057),
  [29955276989](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955276989),
  [29955277045](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277045),
  and [29955277071](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29955277071).
  Each failed at the same legacy test assertion: expected exit 77, observed
  exit 0 from the old gitlink's managed-cache reuse behavior. This is failure
  evidence for the initial head, not a hosted delivery success.

The historical initial-head failures above remain failure evidence. The later
exact head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf` separately passed its
observed ordinary checks and SonarQube Cloud Quality Gate. The current local
Sonar cleanup has not yet created a new exact PR head, so it has no new hosted
delivery result yet.

## Runtime evidence

Not applicable. The change affects CI toolchain selection and a Parent
provisioning-test contract; it does not start a connector or establish a
connector protocol or runtime claim.

## Known limitations

The local Go executable is older than 1.26.5, so it cannot prove candidate
module execution with the requested patch. Candidate hosted validation is the
required exact-toolchain evidence. The full documentation target also depends
on an intentionally uninitialized Framework gitlink. `Update submodules` is a
default-branch schedule/manual workflow, so the follow-up still requires its
own fresh hosted candidate-validation evidence after normal PR checks.

## Remaining risks

A newer Go patch can expose module or runner compatibility differences that
static local evidence cannot prove. The narrow updater avoids a direct default
branch mutation, but exact-head hosted candidate validation, review, and
normal PR delivery remain required. No risk is accepted.

## Checks not run and rationale

- Exact Go 1.26.5 module validation on GitHub-hosted runners is pending a
  task-owned candidate head. The installed local executable is Go 1.26.0, so
  `GOTOOLCHAIN=local go test ./...` and `go vet ./...` in both actual module
  roots reject the required 1.26.5 before executing or downloading anything.
- A fresh Sonar-cleanup commit and its exact-head ordinary CI, CodeQL, review,
  SonarQube Cloud, and resulting-master evidence do not exist yet. The
  `Update submodules` workflow is not currently branch-protection-required,
  but its recorded task acceptance requirement must be reassessed before merge.
- Full documentation link validation exited 2 solely for targets under the
  intentionally uninitialized Framework gitlink; it must not be made green by
  changing Framework or MRTS from this Parent task.

## Final diff and review status

The follow-up local diff has focused static, regression, bilingual, and
security-diff coverage. The scope contains no Framework source, MRTS, Parent
gitlink, Go module, dependency, or action-pin change. Final staging requires
the documented status/diff review and delivery preflight. No current hosted
success is implied for the uncommitted Sonar cleanup.

## 2026-07-23 continuation: Sonar cleanup and protected-integration preparation

The user explicitly authorized remediation of the 23 current SonarQube Cloud
PR #90 observations and protected Parent-master integration. The local change
reverses only the 22 `unittest.TestCase.assertEqual` operand orders flagged by
`python:S3415` and moves the unchanged `release("go1.26.6rc1")` fixture outside
the `assertRaises(MetadataError)` context flagged by `python:S5778`. It does
not alter production/runtime code, workflow permissions, action pins, Sonar
configuration, exclusions, suppressions, false-positive disposition, or risk
acceptance.

The three affected modules passed as a 24-test focused suite. The preceding
100-test focused PR suite, the Go/Python/CI-security contract targets, selected
Python compilation, and `git diff --check` also passed. A complete local
security diff scan explicitly reviewed all three changed test-control files
(the generic source worklist excludes `tests/`) and produced zero reportable
findings. Its retained completion receipt is outside the repository under the
task run; it is not a substitute for a fresh hosted SonarQube Cloud analysis.

The next delivery step is a normal task-owned commit and push, then exact-head
Sonar issue/Quality Gate, required-check, review-thread, mergeability, and
protected-branch evidence. The user authorization does not permit direct
master writes, bypasses, Framework/MRTS mutation, gitlink changes, or branch
cleanup.

## Security impact

This CI supply-chain and validation-boundary change retains immutable action
pins, read-only defaults, narrow writer permissions, default-branch gates, no
persisted checkout credentials, and separated candidate validation. It does
not weaken Framework runtime-output containment, alter a submodule boundary,
or install or update system Go.
