# FND-FRAMEWORK-0020 — Framework PR #27 CI-security Python-quality failure fixed on the exact PR head, pending resulting-master verification

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0020` |
| Category | `ci_failure` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `validated` / `fixed` |
| Feasibility | `requires_user_decision` |
| Release blocker | `true` |
| Security relevant | `true` |

## Summary and distinct boundary

Framework PR #27 originally failed the mandatory CI-security Python-quality
job first on Ruff formatting and then on a deterministic Pyright mapping-key
diagnostic. The current exact PR head
`6a4e057b2cef1f911ba25ab9f95e1b01b390691b` retains repair commit
`82a091a3b6c3e5005126966bf3c6900208c8632b` without weakening a quality or
security control: it types the existing PyYAML Boolean-key fallback as
`dict[Any, Any]`, while preserving its runtime body and fail-closed
workflow-event checks.

Fresh GitHub check-runs for that exact head are terminal and passing, including
`python-ci-security-quality`, all three `CodeQL PR` languages, dependency
review, the PR-range secret scan, actionlint, zizmor, and SonarCloud PR
analysis. The finding is `fixed`, not `verified`: a normal merge and resulting
Framework-master verification remain blocked by a separate explicit user
decision about GitHub Code Scanning Default Setup.

The current exact-head receipt is
`evidence/pr27-6a4e057-exact-head-validation.md`, SHA-256
`cca00d78d239b9f2dc21b2ff4f7bf3ed75a0390eeff726254fa8153633b97f58`.

This finding is distinct from `FND-FRAMEWORK-0012`, which covers semantic
reachability/enforcement of the CI-security evidence contract. This record
covers the independently remediable CI type-quality failure in that checker.

## Affected scope, preconditions, and reproduction

Affected source: `ci/checks/security/check-ci-security-evidence-contract.py`.
Relevant symbols: `workflow_events`, `Mapping.get`, `reportArgumentType`,
`ruff format --check`, and `ruff check`.

The historical Pyright failure occurred at exact head
`55a46ce68b69c8b6ef758ee94e184688aab995a4`, GitHub Actions run `29696794348`,
job `88218830400`. The repair is commit
`82a091a3b6c3e5005126966bf3c6900208c8632b`, a direct child of the Ruff-only
follow-up `55a46ce68b69c8b6ef758ee94e184688aab995a4`.

To reproduce the historical error, inspect
[`29696794348 / 88218830400`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29696794348/job/88218830400).
To validate the repair, inspect exact-head check-runs for `82a091a…` and,
after an authorized normal merge, rerun the equivalent master evidence. Older
heads cannot substitute.

## Evidence and limitations

- Historical failure: exact head `55a46ce68b69c8b6ef758ee94e184688aab995a4`,
  run `29696794348`, job `88218830400`, observed `2026-07-19T17:28Z`.
  Pyright reported: `check-ci-security-evidence-contract.py:424:42 Argument
  of type Literal[True] cannot be assigned to parameter key of type str in
  function get (reportArgumentType)`. Ruff passed.
- Repair evidence: exact head
  `82a091a3b6c3e5005126966bf3c6900208c8632b`; GitHub's commit check-runs API
  was read at `2026-07-19T17:37Z` with exit code `0`. All non-advisory checks
  were terminal `success`; the three deliberately advisory jobs were terminal
  `skipped`. `python-ci-security-quality` passed at
  [run `29697123197`, job `88219679430`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29697123197/job/88219679430).
- Scoped local evidence: exact source diff `55a… -> 82a…` is one annotation
  line; `git diff --check` passed; the Framework MRTS gitlink stayed
  `13aa91291adea12d5c607fdd165d010fcfb1da78`; focused security review found
  no reportable finding.
- Limitation: external GitHub output was inspected live and is not retained as
  a hash-addressed local artifact. No SHA-256 is fabricated. The local runner
  lacks Node.js, so the SHA-locked Pyright bundle could not be executed there;
  an unsupported interpreter was not substituted. The exact hosted Pyright
  result is the authoritative validation.

## Root cause, impact, and implemented remediation

PyYAML may parse an unquoted workflow `on` key as Boolean `True`. The checker
already deliberately supports that compatibility fallback with
`data.get("on", data.get(True))`, but its annotation incorrectly promised
`dict[str, Any]`; Pyright therefore rejected the Boolean key.

Commit `82a091a…` changes only the `workflow_events` parameter annotation to
`dict[Any, Any]`. It neither changes parsing, the Boolean fallback, permission
logic, workflow-event acceptance, error sinks, nor the workflow matrix. PR
CodeQL still requires exactly `pull_request`; trusted CodeQL still rejects
`pull_request` and requires `push`, `schedule`, and `workflow_dispatch`.

The historical mandatory failure is repaired on the PR head. It remains a
release blocker only until the resulting Framework master is normally merged
and verified. Suppressing Pyright, disabling Ruff, or weakening the
CI-security evidence contract was not used and remains prohibited.

## Acceptance criteria and validation plan

- [passed] `python-ci-security-quality` passes on current exact PR head `6a4e057…`.
- [passed] Ruff format and lint pass at that same head.
- [passed] The focused security review confirms unchanged fail-closed event
  behavior, and no Parent or MRTS change exists.
- [pending] The user explicitly authorizes the required Code Scanning Default
  Setup configuration change or another approved security design.
- [pending] PR #27 is normally merged with its exact verified head; the
  resulting master SHA is checked for reachability, content, MRTS integrity,
  and fresh master workflows.
- [pending] The original Pyright reproduction and legitimate controls pass on
  that resulting master before this record becomes `verified`.

## Regression and legitimate-control tests

- `tests/ci_security/test_ci_security_evidence_contract.py`
- Hosted `python-ci-security-quality` Pyright, Ruff format, and Ruff lint
- Exact-head GitHub check-runs for PR #27
- The trusted-CodeQL negative event control: adding `pull_request` remains
  rejected by the evidence-contract checker

## Dependencies, blockers, relationships, residual risk, and history

Dependencies: normal PR #27 integration; exact resulting-master verification;
and an explicit user decision for GitHub Code Scanning Default Setup. Related
findings: `FND-FRAMEWORK-0012`, `FND-GITHUB-0005`. There is no duplicate.

The blocking setting currently reads `state: configured` for Actions, C/C++,
and Python. The trusted advanced CodeQL uploader would conflict with that
Default Setup after a master merge. This finding does not authorize a settings
change, bypass, direct master push, Parent gitlink update, or MRTS change.

- `2026-07-19T17:16Z`: exact head `2f635be…` failed only because Ruff would
  reformat the checker and focused test; Ruff lint passed.
- `2026-07-19T17:28Z`: exact head `55a46ce…` passed Ruff but failed the
  deterministic Pyright `Literal[True]` mapping-key check.
- `2026-07-19T17:35Z`: normal repair commit `82a091a…` was pushed after a
  focused security review found no reportable finding.
- `2026-07-19T17:37Z`: all exact-head hosted PR checks passed; status changed
  to `fixed`, pending resulting-master verification and the settings decision.
- `2026-07-19T19:34:25Z`: current test-only descendant `6a4e057…` passed its
  full exact-head GitHub/Sonar validation, retaining the Pyright repair. The
  record remains `fixed` pending the settings decision and resulting master.

## Resulting-master observation — 2026-07-19T20:00:39Z

PR #27 was squash-merged as `6de40c1714410241e917e9083ee890a82fb2fdbb`; its
tree equals exact PR head `6a4e057b2cef1f911ba25ab9f95e1b01b390691b`, and its
MRTS gitlink did not change. The exact master `python-ci-security-quality`
control passed, along with `scaffold-lint`, `common-structure`, and workflow
lint. This proves the repaired Pyright path remains in the merged source.

The required trusted Advanced CodeQL uploader failed after its analysis for all
three languages because GitHub Default Setup remains enabled, although the
three Default Setup CodeQL analyses on the same SHA succeeded. This external
configuration failure is `FND-GITHUB-0006`, so this finding remains `fixed`,
not `verified`. The user's merge authorization retained Default Setup; it did
not authorize a settings change, direct master repair, control weakening,
Parent change, or MRTS action.
