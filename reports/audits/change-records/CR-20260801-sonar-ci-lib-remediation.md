# Change Record: Parent CI library SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-ci-lib-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-ci-lib-remediation` |
| Date (UTC) | `2026-08-01` |
| Base revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Boundary | Parent `ci/lib/generated_report_utils.py`, `ci/lib/runtime_path_utils.py`, one direct Parent regression test, this English/German Change Record pair, and their paired indexes only. Framework and MRTS source, Gitlinks, `.github/`, SonarQube Cloud rules, exclusions, suppressions, Quality Gates, and `master` are unchanged. |
| SonarQube Cloud linkage | The current `ci/lib` inventory contained 19 open items: `python:S5443` at `generated_report_utils.py` lines 61–73 and `runtime_path_utils.py` lines 26, 31–32; `python:S3776` at `generated_report_utils.py` lines 49, 1098, 1538 and `runtime_path_utils.py` line 235; and `python:S1192` at `generated_report_utils.py` lines 1051, 1071, 1136, and 1420. |

## Motivation and problem statement

The Parent CI library contained repeated path, suffix, and reference-prefix
literals, as well as two large decision paths for report provenance and
runtime-root selection. SonarQube Cloud reported 19 open maintainability and
security-rule items in this narrow directory. The runtime policy deliberately
uses a fixed temporary fallback only to derive a private, checked child; it
must not be weakened merely to change a static-analysis result.

## Implementation decision and rationale

The report helper now owns portable path, suffix, and source-reference
constants centrally. Small helpers preserve the prior path-redaction order and
separate report metadata, provenance, stale-state, regular-file, and
directory-input decisions. The runtime helper uses one environment-or-default
path resolver and one fixed policy parent representation, while retaining its
existing allowlist, private-leaf, owner, sticky-parent, and no-follow checks.

The added regression test covers both verified-run and generic temporary path
rendering. It performs presentation-only checks; runtime writes continue to
go through the existing descriptor-based protections.

## Acceptance criteria

- Existing report input status and Framework-provenance outcomes remain
  unchanged, including stale, blocked, missing, and failed-closed states.
- Verified runtime paths continue to reject broad, system-writable, unsafe,
  and symlinked roots while accepting the narrow verified external child.
- Temporary paths are rendered portably without performing filesystem access
  in the report-presentation helper.
- A future exact PR head must show zero new SonarQube Cloud issues and zero
  new duplicated lines without a rule change, exclusion, suppression, or
  downgrade of a security control.

## Changed files

- `ci/lib/generated_report_utils.py`
- `ci/lib/runtime_path_utils.py`
- `tests/test_generated_report_evidence_integrity.py`
- `reports/audits/change-records/CR-20260801-sonar-ci-lib-remediation.md`
- `reports/audits/change-records/CR-20260801-sonar-ci-lib-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Python `py_compile` for both changed Parent CI library modules | passed. |
| Focused Parent `unittest` selection | passed: 98 tests in 14.445 seconds. It includes all generated-report evidence-integrity tests, all runtime-path-security tests, and the selected runtime-path-policy controls. |
| `check-generated-report-layout` invoked by the focused generated-report test suite | passed. |
| `tests.test_bilingual_docs` | passed: 22 tests in 0.280 seconds. |
| `make check-bilingual-docs` | blocked by the intentionally unmaterialized Framework checkout only; after the task-owned heading correction, its remaining diagnostics are all missing Framework link targets. |
| Final `git diff --check` before documentation updates | passed. It will be rerun for the full task diff before delivery. |
| Focused Codex Security scan of all eight `ci/lib` modules | passed with no newly discovered reportable finding. It reviewed filesystem writes, descriptor-relative artifact access, report output paths, subprocess construction, and temporary-root handling. |

## Security impact

The runtime path code is security-relevant because CI paths and temporary
roots may be influenced by environment values or attacker-controlled
filesystem state. The refactor does not change the fixed fallback selection,
the rejection of broad/system paths, or the descriptor-based `O_NOFOLLOW`,
owner, mode, and sticky-parent protections. It adds no command construction,
network access, credential handling, permission change, or new writable
location.

No security finding is suppressed, accepted, or closed by this Change Record.

## Runtime evidence

The focused tests exercise the policy and artifact safety controls without
provisioning a connector or modifying Framework/MRTS content. They are not a
claim that a complete connector runtime matrix was executed.

## Checks not run and rationale

- The complete `tests.test_runtime_path_policy` module cannot complete in the
  isolated task worktree because its subprocess-based Framework control needs
  an intentionally unmaterialized Framework checkout. The selected Parent
  policy controls and the full runtime-path-security suite passed; no
  Framework source was initialized or changed as a workaround.
- `make check-bilingual-docs` was run, but its repository-wide local-link
  scan cannot complete in this task worktree because the Framework checkout is
  deliberately not materialized. The direct bilingual test suite passed, and
  the checker reports no remaining task-owned record error.
- No local SonarQube Cloud analysis was run because this task environment has
  no configured scanner credential. The exact hosted PR head must provide the
  authoritative SonarQube Cloud result.
- During the original remediation phase, no connector matrix, download,
  package installation, Framework/MRTS action, Gitlink change, `.github/`
  action, or `master` integration was run because its scope was the Parent
  `ci/lib` remediation only. A later, separate current-user authorization for
  the already-created Parent PR is recorded below; it does not expand product
  scope.

## Known limitations

The current SonarQube Cloud inventory is a point-in-time server result. Its
closure and the absence of newly introduced findings remain pending until the
hosted analysis runs on the exact published PR head.

## Remaining risks

The remaining risk is a regression in report status ordering or runtime-root
selection. The focused regression suite covers the existing security controls
and presentation order; hosted SonarQube Cloud analysis remains the final
static-analysis evidence.

## Final diff and review status

The original remediation is published as task-owned Draft PR #217. The
source-change validation and the sealed security review bind to the preceding
exact PR head; the current delivery head must be verified again after the
documented base synchronization and this record update.

### Current master-integration authorization

On 2026-08-01 the current user explicitly authorized only Parent PR #217 for
integration into `master` (`bringe das pr 217 in den master`). The
authorization excludes direct pushes, force operations, administrative
bypasses, other PRs, Framework/MRTS actions, Gitlink changes, and releases.

The active `master` ruleset permits a normal merge commit and requires no
approving review, but requires all review threads resolved and the named
status checks for the exact head. The authorized delivery will use that normal
merge method only after the refreshed exact-head checks, SonarQube Cloud
result, review/conversation state, and mergeability are all observed to pass.
The eventual merge evidence is recorded in the task lifecycle record; this
pre-merge Change Record does not claim a result before GitHub has produced
one.
