# FND-MRTS-0002 — MRTS upstream-policy safety marker was absent from an enforced governance control

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-MRTS-0002` |
| Category | `test_failure` |
| Repository | `mrts` |
| Ownership | `mrts_explicit_user_task` |
| Priority | `P1` |
| Severity | `not_applicable` |
| Confidence | `confirmed` |
| Status | `fixed` |
| Feasibility | `requires_user_decision` |
| Release blocker | `false` |
| Security relevance | `true` |

## Summary, observed behavior, and impact

The MRTS governance validator failed because the active fork-and-upstream
policy lacked its required explicit instruction not to guess an upstream URL.
Before the repair, `tools/validate-governance.py` exited `1` and identified the
missing marker `Do not guess an upstream URL`. No remote, source, network, or
delivery action was attempted.

The failed mandatory local check prevented a verified configuration-
reconciliation result and omitted an explicit defense-in-depth instruction at
an upstream trust boundary. No actual remote misuse or runtime exploit was
demonstrated.

## Expected behavior and affected boundary

The active MRTS upstream policy must explicitly prohibit guessing an upstream
URL, require observation of the configured remote before inspection, and keep
upstream inspection-only without inferring delivery authority. The current
native validator must explicitly assert that exact marker, and its focused
tests must preserve both the missing-marker negative control and the legitimate
policy control.

Affected files are `.codex/context/fork-and-upstream-policy.md`,
`tools/validate-governance.py`, and `tools/test_validate_governance.py`.
Affected controls are the explicit non-guessing marker, the MRTS governance
validator, and the MRTS fork-and-upstream policy.

## Preconditions and safe reproduction

The existing embedded MRTS checkout and its native governance validator must be
available. The retained pre-repair evidence records the exact validator command
and its exit code without mutating a remote. After the repair, run:

```text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-governance.py
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/test_validate_governance.py
```

The validator must exit `0`; the focused suite must pass all three tests. A
passing current validator is not sufficient when it no longer asserts the exact
marker that failed originally. Do not alter remote configuration or attempt an
outbound action to demonstrate the control.

## Evidence

- Run ID: `20260726T000000Z-mrts-codex-config-reconciliation-current`
  - Pre-repair artifact: `evidence/governance-validator-before.txt`
  - SHA-256: `99fac1ae7620a2b32e321603fe51153cdf10f3187b28046c9651bc36de2dfa0a`
  - Command: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-governance.py`
  - Exit code: `1`; observed `2026-07-26T04:19:42Z`
  - Retention: `retained_task_evidence`
- Run ID: `20260726T000000Z-mrts-codex-config-reconciliation-current`
  - Post-repair artifact: `evidence/governance-validator-after.txt`
  - SHA-256: `f67f95dec10d1042cd42915734114d0a12884b920502df8290cbf406104d6354`
  - Commands: the validator above and
    `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/test_validate_governance.py`
  - Exit code: `0`; observed `2026-07-26T04:24:52Z`
  - Retention: `retained_task_evidence`

## Root cause and remediation

The policy and validator had drifted: the policy already preserved upstream
inspection-only restrictions, but it lacked the validator's exact explicit
non-guessing marker. The minimal repair adds that marker, requires observation
of the configured remote before inspection, and forbids inferring an upstream
destination from a repository name, previous task, or nested Gitlink. Existing
delivery prohibitions remain unchanged.

The current closure audit found a later validator/test change: the policy still
contains `Do not guess an upstream URL`, but the active marker list no longer
asserts that exact text. The historical repair therefore remains a code/policy
change (`fixed`), not a current verification of the enforced control.

## Acceptance criteria and validation

- The policy contains `Do not guess an upstream URL`.
- Upstream remains inspection-only; the repair grants no upstream push, merge,
  synchronization, tag, rebase, or Gitlink-update authority.
- The current native validator explicitly asserts the exact non-guessing marker.
- The original validator exits `0`.
- The focused governance regression suite passes all three tests.
- No MRTS product source, remote, branch, Gitlink, commit, push, PR, or merge
  changes.

The original validator and the three-test regression suite passed after the
repair. They are retained historical evidence, but no longer sufficient for
`verified` because the current validator does not enforce that same exact
marker. A separately authorized MRTS source/test correction must restore the
assertion and rerun the missing-marker negative and legitimate positive controls.

## Dependencies, residual risk, and history

The current validation-coverage regression blocks closure: restoring the exact
validator assertion and rerunning its controls requires separately authorized
MRTS source/test work. The policy and validator are governance evidence rather
than a host-side interceptor. A future authorized delivery must still perform
its independent remote/identity preflight, and no upstream delivery authority
is inferred.

- `2026-07-26T04:19:42Z` — `original_validator_failure_reproduced`: the native
  validator exited `1` for the missing marker; no remote, source, network, or
  delivery action occurred.
- `2026-07-26T04:24:52Z` — `minimal_policy_repair_verified`: the explicit
  marker was added without widening authority; the original validator and all
  three focused regression tests passed.
- `2026-07-26T11:35:17Z` — `verification_reassessed_after_current_validator_coverage_regression`:
  current read-only inspection found that the active validator/test no longer
  asserts `Do not guess an upstream URL`; the policy text remains, but the
  historical legitimate control is no longer current. Status is `fixed`; no
  MRTS source, test, remote, Gitlink, branch, commit, or delivery action occurred.

Final disposition:
`fixed_policy_marker_present_but_current_validator_no_longer_asserts_exact_marker`.
