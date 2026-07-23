# Change Record: Scripts workflow and report path confinement for SonarQube Cloud security findings

**Language:** English | [Deutsch](CR-20260722-sonar-scripts-path-confinement.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260722-sonar-scripts-path-confinement |
| Date (UTC) | 2026-07-22 |
| Original base revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Current master base | 95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3, merged non-rewriting into this task branch on 2026-07-23 |
| Tracking | Two Parent-only security findings in scripts/update-github-actions-versions.py: AZ70CAr3IpeCryPNS2zi (pythonsecurity:S2083) and AZ70CAr3IpeCryPNS2zj (pythonsecurity:S8707); follow-up SonarQube Cloud maintainability findings AZ-LiaSLimiHoxpRJ2G8 (python:S3776) and AZ-LiaLHimiHoxpRJ2G4 through AZ-LiaLHimiHoxpRJ2G7 (python:S5778). |
| Boundary | Parent updater source and regression tests plus this English/German traceability pair and indexes. Framework, MRTS, gitlinks, workflow configuration, action-update policy, scanner configuration, Quality Gates, and suppressions remain unchanged. |

## Motivation and problem statement

The workflow updater enumerated candidates and read their contents before
proving that their resolved paths remained inside the selected repository.
An attacker able to place a symlink in a scanned workflow location could cause
the updater to read and, in write mode, modify an external target. Separately,
the command-line `--report` value was used as an unconstrained output path,
allowing a caller to direct report output outside the repository.

The selected findings are limited to the updater. The Critical temporary-audit
directory finding in `generate_repository_organization_inventory.py` is
already owned by open Draft PR #74, whose matching SonarCloud key is absent
from that PR analysis; it is intentionally not duplicated here.

## Acceptance criteria

- Only regular workflow files whose resolved locations remain below the
  selected repository root are read or modified.
- A report path outside the selected repository root, including a symlink that
  resolves outside it, is rejected before any report write.
- The existing root-relative `actions-update-report.md` workflow usage remains
  supported.
- A malicious workflow-symlink control and an external-report-path control
  fail safely; a legitimate workflow update and root-relative report control
  continue to pass.
- Workflow discovery remains below SonarQube Cloud's cognitive-complexity
  threshold without bypassing any confinement check.
- The negative exception controls retain their inputs and expected failures
  without nested calls inside their assertions.
- Both Change Record languages and both indexes remain equivalent.
- Obtain fresh SonarQube Cloud and hosted-check evidence for the exact Draft
  PR head before calling either selected key resolved.

## Implementation decision and rationale

Workflow discovery now resolves every candidate before opening it and skips a
candidate that is a symlink, is not a regular file, or resolves outside the
repository root. The existing root and Framework-submodule discovery routes
remain available, but each candidate still has to satisfy the Parent-root
confinement check.

The report path is resolved through one helper before `write_report` is
called. It accepts a normal relative path below the current repository root
and rejects absolute, traversal, or symlink targets outside it with the
existing argparse error mechanism. This is the narrowest repository-native
boundary because it protects both the direct CLI sink and the existing CI
default without changing action-version selection semantics.

The current-master follow-up extracts the existing workflow-candidate decision
into `confined_workflow_path`. It retains the same strict resolution,
direct-symlink rejection, regular-file check, and Parent-root confinement
before a candidate reaches workflow reading or write-mode replacement.
The four negative exception controls prepare their path or argument values
before entering `assertRaises`; their rejected inputs and expected failures
are unchanged.

## Changed files

- scripts/update-github-actions-versions.py
- tests/test_update_github_actions_versions.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- In-memory Python syntax compilation of the changed updater: passed.
- `tests.test_update_github_actions_versions`: passed (19 tests).
- Focused exploit and legitimate controls: passed. An external workflow
  symlink produced no scan row and its target stayed unchanged; external and
  symlinked report paths caused a CLI rejection; a root-relative report was
  written successfully.
- `git diff --check`: passed.

## Security impact

The affected source-to-sink paths are workflow-discovery candidates to
`read_text`/write-mode replacement, and CLI `--report` input to
`write_report`. The new invariant is enforced before either path is used:
resolved workflow candidates and report destinations must remain below the
repository root, and direct workflow symlinks are ignored. This blocks the
selected escape paths without changing trusted root-relative workflows,
report format, GitHub API resolution, or submodule write authorization.

The regression controls are designed to fail on the pre-change behavior: the
former scanner would read and update the external symlink target, and the
former CLI would write an external report. No security control is weakened and
no suppression, NOSONAR marker, or scanner configuration change is used.

The maintainability refactor does not turn the earlier checks into a
best-effort filter: `None` is returned only after the same failed resolution,
symlink, regular-file, or root-containment condition that previously skipped
the candidate. The explicit security controls continue to exercise those
decisions.

## Runtime evidence

The regression suite exercises the real updater functions and CLI path
validation using temporary isolated repository roots. It intentionally uses
an empty legitimate workflow root for CLI report tests so no network GitHub
API lookup is required. Existing workflow parsing/update behavior is covered
by the major-ref update test; no production GitHub workflow was executed.

## Current-master refresh and maintainability follow-up

Current remote `master` revision
`95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3` was incorporated with a normal
merge commit, not a rebase or history rewrite. Its only resolution was a
union of this Change Record index entry with the current-master entry. The
subsequent source/test follow-up addresses the five exact PR findings without
changing scanner configuration, Quality Gates, suppressions, workflow
configuration, Framework, MRTS, or the Parent gitlink. Fresh exact-head
hosted and SonarQube Cloud evidence remains required after the follow-up
commit.

## Known limitations

This batch addresses only S2083 and S8707 in the updater. It does not merge
or replace Draft PR #74, does not claim the default branch is already free of
the separate Critical temporary-directory finding, and does not clear the
broader SonarQube Cloud backlog.

## Remaining risks

The updater still intentionally reads regular workflow files inside the
repository and writes a caller-selected report inside it. That is required
behavior. The new confinement checks do not protect a caller who intentionally
selects an unsafe repository root; the caller controls that trust boundary.
Fresh exact-head hosted and SonarQube Cloud validation remains required before
the selected findings are declared resolved.

## Checks not run and rationale

- No live GitHub Actions version update: the security boundary is proven with
  deterministic unit/CLI controls, and a live update would require networked
  version selection unrelated to path confinement.
- No Framework or MRTS test or modification: both are excluded from this
  Parent-only task.
- The complete repository-wide bilingual documentation CLI check is not run
  locally because its known failures are missing links in the deliberately
  uninitialized Framework gitlink; the targeted Change Record rule and hosted
  `scaffold-lint` evidence are used instead.
- Full hosted checks and SonarQube Cloud PR analysis remain pending for the
  current exact Draft PR head.

## Final diff and review status

Local implementation, source-to-sink review, focused exploit controls, and
legitimate controls are complete on the Parent-only task branch. Draft PR
[#91](https://github.com/Easton97-Jens/ModSecurity-conector/pull/91) remains
open and marked Draft. Fresh exact-head hosted checks, Sonar analysis, and the
Quality Gate remain required before the selected findings can be resolved. No
review approval, merge, or default-branch change is claimed or authorized.
