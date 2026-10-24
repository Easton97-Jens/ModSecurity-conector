# Change Record

**Language:** English | [Deutsch](CR-20260919-update-submodule-sha-projection.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260919-update-submodule-sha-projection |
| Date (UTC) | 2026-09-19 |
| Base revision | e475baabf0787cbc804f176ae998b62156892825 |

## Motivation and problem statement

GitHub Actions Update submodules run 35441775719 failed at Validate Framework
component-pin data contract. Its candidate was
cc36b37d0f6a0fbc3512f3878a691751e91c5fbb while the current Parent gitlink was
d4f7b69dc264852eac74e1439c0887fcb9fbe372. The validator required the static
Parent consumers to equal the candidate before the only authorized publisher
could create that projection. The generic synchronizer did not own those
consumers and the publisher allowlist excluded them.

The requested Parent-only repair removes that deterministic ordering deadlock.
It changes neither Framework nor MRTS source, the Parent gitlink, NGINX
ownership, protected-broker pins, permissions, or delivery state.

After PR #371 was delivered, SonarQube Cloud reported one task-owned `MAJOR`
reliability `CODE_SMELL`, `AaC54ukhy0vepUx4k5_k` / `python:S8786`, at
ci/tools/sync-framework-component-versions.py:381. The Quality Gate was `OK`,
but `new_violations=1` and `new_code_smells=1`. The user requested a zero-issue
result, so this record also covers the narrow no-suppression remediation.

## Acceptance criteria

- A candidate distinct from the current gitlink passes read-only validation
  against the current static Parent projection.
- The publisher proves that current state, projects the candidate into exactly
  five reviewed static slots, then verifies the resulting candidate state.
- Invalid, missing, duplicate, quoted, misplaced, malformed, or dynamically
  aliased static slots fail before a target write; dynamic workflow consumers
  remain unchanged.
- The generic FRAMEWORK_SHA counter accepts the same normal LF assignments,
  rejects CRLF/bare-CR assignments as before, and rejects a long
  whitespace-plus-CRLF malformed slot without a target write.
- A successor exact-head SonarQube Cloud `OPEN,CONFIRMED` query returns zero
  issues and zero new violations without a suppression, exclusion, issue
  acceptance, scanner, workflow, rule, or Quality-Gate change.
- The explicit publisher allowlist and staging cover only the two newly owned
  projection files, and generic NGINX non-consumption remains enforced.
- Focused regression tests and the CI-security contract pass locally. Hosted
  exact-head proof remains a separate delivery condition.

## Implementation decision and rationale

The synchronizer now accepts a separately validated lowercase resolver SHA;
it does not read that value from candidate common.sh. A closed projection
registry owns one CRS/no-MRTS workflow and one test fixture. It requires one
EXPECTED_FRAMEWORK_SHA, three literal FRAMEWORK_SHA assignments, one fixture
constant, and preserves two exact dynamic workflow assignments byte-for-byte.

Read-only validation compares the five static consumers with the current
gitlink. The privileged publisher repeats that comparison, atomically projects
the resolver candidate SHA, and then verifies the candidate state. The
candidate verifier accepts a distinct expected Parent SHA for the pre-write
comparison. This preserves the existing candidate-origin, structure, NGINX,
and protected-broker controls without widening the generic source registry.

The generic FRAMEWORK_SHA counting expression no longer divides whitespace
between two variable-length classes. It captures the whole non-CR/non-LF value
after the colon and requires a following LF or end-of-file. Its sole consumer
already trims the capture, so normal LF value semantics remain unchanged while
the previous CRLF backtracking case fails closed without a super-linear retry.
No SonarQube Cloud configuration or legitimate control changed.

## Changed files

- .github/workflows/update-submodules.yml
- ci/tools/sync-framework-component-versions.py
- ci/tools/verify-framework-candidate-contract.py
- tests/test_update_framework_versions.py
- tests/test_verify_framework_candidate_contract.py
- tests/test_ci_security_workflows.py
- reports/audits/change-records/CR-20260919-update-submodule-sha-projection.md
- reports/audits/change-records/CR-20260919-update-submodule-sha-projection.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

No Framework/MRTS source, Gitlink, .gitmodules file, dependency, credential,
workflow permission, generated report, or production runtime source changed.

## Commands executed

- python -m unittest -v tests.test_update_framework_versions
  tests.test_verify_framework_candidate_contract
  tests.test_ci_security_workflows — passed 76 tests.
- make check-ci-security-contract — passed 153 tests with five expected
  unavailable namespace/identity integration skips.
- python -m py_compile for changed Python paths and tests — passed.
- python -m unittest -v tests.test_update_framework_versions — passed 21
  tests after the SonarQube Cloud remediation.
- python -m py_compile ci/tools/sync-framework-component-versions.py
  tests/test_update_framework_versions.py — passed after the remediation.

The commands ran in the isolated task worktree with dedicated temporary and
bytecode-cache paths. Expected negative-test diagnostics in the test output
are assertions of fail-closed behavior, not test failures.

## Security impact

This change touches a GitHub Actions publication boundary. The resolver SHA is
validated separately from candidate common.sh, the target set is closed and
strictly cardinality-checked, the publisher proves current state before
writing and candidate state afterward, and the new paths are explicitly
allowlisted and staged. NGINX remains excluded from generic synchronization;
protected-broker pins and existing workflow permissions are unchanged.

An independent static post-patch review found no reportable security finding.
It did not execute a hosted workflow and does not replace exact-head delivery
evidence.

The `python:S8786` observation is a validated reliability/maintainability
finding, not a confirmed externally exploitable vulnerability: the expression
matches a fixed Parent workflow target, and malformed target structure still
fails before a registered write. A fresh post-patch bypass review is required
before delivery.

## Runtime evidence

The authoritative failure is [GitHub Actions run 35441775719](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35441775719).
Secret-free retained local evidence is recorded at
.codex/runs/20260919-fix-actions-run-35441775719/evidence.md; the current
artifact hash is retained in that run's hash inventory.

At predecessor head `4affad9cc97383df54a05ec5d35e2c66e7e804b7`, authenticated
SonarQube Cloud evidence recorded exactly `AaC54ukhy0vepUx4k5_k` /
`python:S8786`; its Quality Gate was `OK` but it had one new violation and one
new code smell. Payload-safe task evidence retains the observation, local
regression result, and the required exact-successor query. No successor-head
SonarQube Cloud result is claimed here before it is observed.

At Change Record preparation time, there was no hosted workflow result for the
prospective task head. The authorized delivery lifecycle retains its actual
commit, branch, and pull-request facts in task evidence. This Change Record
makes no merge, GitHub rerun, Framework change, or MRTS change claim.

## Known limitations

Local tests cannot execute GitHub-hosted token permissions, scheduler
expressions, branch protection, concurrent remote races, or a real later
Framework candidate transition. The test environment has no available
namespace/identity integration setup for the five documented skips.

## Remaining risks

An unrelated future privileged caller must continue to bind the new
--framework-sha argument to an official resolver result. The current workflow
does so through its resolver output. A moved remote state, malformed candidate,
invalid projection, allowlist mismatch, or hosted failure remains fail closed;
there is no fallback, auto-merge, or permission expansion.

## Checks not run and rationale

At Change Record preparation time, no authorized hosted workflow rerun or merge
had been performed. Consequently, exact task-head Update-submodules, CI
security, actionlint execution in GitHub, branch-protection, review, and
resulting-master evidence were not available. A separate local actionlint
execution was not needed to establish the source contract because the
CI-security target validates the pinned tool availability and the focused
workflow-contract tests passed; exact-head hosted actionlint remains required
for delivery.

make check-bilingual-docs was attempted but exited 2 because the isolated task
worktree has no initialized Framework submodule. It reported only pre-existing
missing links beneath modules/ModSecurity-test-Framework and no error for this
Change Record pair. Initializing or altering that separate repository boundary
was out of scope.

## Final diff and review status

The Parent-only change is limited to the updater workflow, the bounded projector
and verifier, their focused tests, and this paired Change Record index. It has
passed the recorded local checks and an independent static security review. The
finding stays in_progress until exact-head hosted evidence is observed; no merge
is claimed.
