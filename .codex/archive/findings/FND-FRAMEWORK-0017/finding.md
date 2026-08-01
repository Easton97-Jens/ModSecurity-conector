# FND-FRAMEWORK-0017 — CI security evidence contract accepts required command text after an assignment-only pseudo-call or terminal exec

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0017` |
| Category | `security_hardening` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P1` / `medium` |
| Confidence / status | `validated` / `fixed` |
| Feasibility | `feasible_now` |
| Release blocker | `true` |
| Security relevant | `true` |

## Summary, observed behavior, and impact

At Framework PR #27 head
`82a091a3b6c3e5005126966bf3c6900208c8632b`, retained in-memory workflow
mutations proved two fail-open reachability regressions at that pre-fix head:

1. `unused_scorecard_scan=disabled`, `unused_scorecard_scan[0]=disabled`, and
   `unused_scorecard_scan["mode"]=disabled` are parsed as function invocations
   when the required command appears only in `unused_scorecard_scan() { ... }`.
2. `exec /usr/bin/true` does not terminate direct reachability, so a later
   required scanner command is accepted even though Bash cannot execute it.

Both mutated Scorecard workflows returned no contract errors. A pull request
could therefore retain textual scanner evidence while skipping the scanner and
misleading the CI evidence gate. The local semantic bypass is validated;
external review or branch-protection configuration is not present in the
checkout and did not negate the required fail-closed repair. The current exact
PR head now contains the regression-backed repair.

## Expected behavior and security boundary

Only commands Bash can execute on a direct reachable path may satisfy
`require_commands()`. Assignment-only statements must not invoke helpers, and
an `exec` form with a real command must terminate later reachability. Scalar
and array assignment-only statements are both non-invoking.
Assignment-prefixed legitimate helper calls, bare/redirection-only `exec`, and
commands that precede a terminal `exec` retain their supported behavior.

The affected Framework-owned files are:

- `ci/checks/security/check-ci-security-evidence-contract.py`
- `tests/ci_security/test_ci_security_evidence_contract.py`
- the in-memory `.github/workflows/ci-security-scorecard.yml` test input

The affected symbols are `FUNCTION_CALL`, `shell_function_call_name()`,
`direct_context_lines`,
`shell_function_blocks`, `control_flow_line_indexes`, and
`reachable_shell_lines`.

## Preconditions and reproduction

The exact #27 head contains the semantic checker and a covered,
pull-request-controlled workflow `run:` script contains the required Scorecard
command. The retained pre-fix reproduction replaces that command in an
in-memory workflow with each bypass variant and calls `workflow_errors()`.
The scalar and `exec` variants returned `[]` at the exact head; a simulation of
the immediately prior leading-identifier matcher returned `[]` for the
indexed-array variant too.

The source-unchanged evidence is a regular retained file:

- Run: `20260719T180448Z-framework-pr27-sonar-remediation-72a73203`
- Path:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T180448Z-framework-pr27-sonar-remediation-72a73203/evidence/fnd-framework-0017-pre-fix-reproduction.md`
- SHA-256:
  `b9c910089001ca9b67a45d2d3021f697c237b426ce221036b86fe52b2a334f67`
- Command:
  `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-run>/tmp/pycache python3 -c <in-memory Scorecard assignment-only and exec reachability mutations>`
- Exit code: `0`; observed at `2026-07-19T18:05:00Z`.

The host Python reproduction establishes the checker logic only. It is not a
substitute for Framework's pinned CPython 3.12 CI environment, which is absent
locally.

The newly added focused regression suite also exited `1` as expected before the
repair: ten existing tests passed and exactly the assignment-only and terminal
`exec` negative controls failed. Its retained result is
`evidence/fnd-framework-0017-pre-fix-regression-suite.md` under the same run,
SHA-256 `8a74a663cad6e1664fb190913c78620cb2c356044e8c661b776235635293951b`.

The post-fix local receipt is
`evidence/fnd-framework-0017-final-local-validation.md` under the same run,
SHA-256 `6afd44552895aeb9e2030f1a7d4acf0663e0ade7f111c4c5735c46dcdfb26039`.
It records the prior-matcher indexed-array simulation and the passing focused
12-test suite, direct checker, Ruff checks, full `make lint`, and final
`git diff --check`. The local Make target uses CPython 3.14.4, so hosted
CPython 3.12 exact-head evidence remains required.

That exact-head evidence now exists for
`c323f9d937b63b97257b1ebc8be75e4fdaa3d697`: all current GitHub checks passed,
SonarCloud reports zero open/confirmed PR new-code issues, and no review threads
or reviews remain. The retained receipt is
`evidence/fnd-framework-0017-exact-pr-head-validation.md`, SHA-256
`04eaa7e9762dd53c6d9847da98aec7e5c624fdf37e44083598b4c06ede805556`.

The current exact PR head is the test-only follow-up
`6a4e057b2cef1f911ba25ab9f95e1b01b390691b`; it leaves the repaired parser
unchanged. Its 20 check successes, three expected advisory skips, empty review
state, SonarCloud `OK` Quality Gate, zero open/confirmed issues, and zero new
duplicated lines are retained in `evidence/pr27-6a4e057-exact-head-validation.md`,
SHA-256 `cca00d78d239b9f2dc21b2ff4f7bf3ed75a0390eeff726254fa8153633b97f58`.

## Root cause and proposed remediation

The reachability parser's leading-identifier matcher treats scalar and array
assignment syntax as a function call, and its terminal-statement model
recognizes `exit` but not `exec` with a command. The narrow repair parses
ordinary leading shell assignment words before resolving a function call,
refuses an identifier immediately followed by `[` as non-call syntax,
recognizes only `exec` forms with a real command as terminal, retains
bare/redirection-only `exec` semantics, and adds negative plus paired
legitimate-control regressions.

## Acceptance criteria and validation plan

- Scalar, indexed-array, and quoted-key array assignment-only statements
  cannot make an uncalled helper reachable.
- A direct `exec` form with a real command prevents later required commands
  from satisfying the contract.
- An assignment-prefixed direct helper call remains reachable.
- Commands preceding terminal `exec` remain accepted.
- Existing comment, branch-hidden command, uncalled helper, and legitimate
  nested-OSV-helper controls remain covered.
- Focused local checks, source-level security review, and the final exact
  PR-head CI/Sonar cycle pass without relaxing workflow, permission, scanner,
  or evidence requirements.

The local implementation now adds deterministic Scorecard mutations for each
bypass and paired legitimate control; the focused semantic suite, direct
checker, relevant quality checks, final diff review, and hosted exact-head
CI/Sonar evidence pass. Resulting-master verification remains separately gated
on the explicit GitHub Code Scanning Default Setup decision.

## Dependencies, related findings, residual risk, and history

Related records are `FND-FRAMEWORK-0012` and `FND-FRAMEWORK-0015`. The
remaining work depends on the separate Default Setup decision before
resulting-master verification.

The exact PR head is fixed, but the separate Default Setup setting gate blocks
trusted-master and resulting-master verification. No risk is accepted.

- `2026-07-18T15:18:00Z`: the historical dead-branch and uncalled-function
  bypass repair was locally fixed.
- `2026-07-19T18:05:00Z`: this finding was reopened from `fixed` to
  `in_progress` after the exact #27-head assignment-only and `exec` variants
  reproduced; it blocks #27 integration pending the regression-backed repair.
- `2026-07-19T18:48:52Z`: scalar, indexed-array, quoted-key-array, and
  terminal-`exec` repairs plus paired legitimate controls passed local focused
  and full native validation. The finding remains `in_progress` only until a
  normal push obtains exact final PR-head CI/Sonar evidence.
- `2026-07-19T18:58:30Z`: the two Framework-only files were committed as
  `f1ad17230072b460c7c85104efac381c19807bb6` and normally pushed to PR #27;
  exact-head GitHub and SonarCloud checks are in progress.
- `2026-07-19T19:07:56Z`: follow-up
  `c323f9d937b63b97257b1ebc8be75e4fdaa3d697` passed all current exact-head
  checks; SonarCloud returned zero open/confirmed PR new-code issues and the
  review-thread/review state is empty. The finding is `fixed` pending only the
  separately gated resulting-master verification.
- `2026-07-19T19:34:25Z`: the test-only duplication follow-up
  `6a4e057b2cef1f911ba25ab9f95e1b01b390691b` passed its full exact-head
  GitHub/Sonar validation. The parser remains unchanged; the finding remains
  `fixed` pending the Default Setup decision and resulting-master verification.

## Resulting-master observation — 2026-07-19T20:00:39Z

PR #27 was squash-merged as `6de40c1714410241e917e9083ee890a82fb2fdbb`.
Its source tree equals exact PR head `6a4e057b2cef1f911ba25ab9f95e1b01b390691b`,
the Framework worktree is clean, and no `tools/MRTS` gitlink diff exists.
`scaffold-lint`, `python-ci-security-quality`, `common-structure`, workflow
lint, and the Default Setup CodeQL analyses passed on that exact master SHA.

The required trusted Advanced CodeQL uploader nevertheless failed for all three
languages after analysis because Default Setup remains enabled. This independent
configuration failure is now `FND-GITHUB-0006`; it prevents this record from
becoming `verified`, but does not reintroduce the fixed parser bypass. The
current user authorized the merge while retaining Default Setup, not a
corrective configuration change. No Parent, MRTS, direct-master, bypass, or
cleanup action occurred.
