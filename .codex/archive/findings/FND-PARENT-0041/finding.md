# FND-PARENT-0041 — Apache Phase-4 harness passed an unsupported synchronized-upstream option

## Classification

| Field | Value |
| --- | --- |
| Category | test_failure |
| Repository / ownership | Parent / parent |
| Priority / severity | P1 / not_applicable |
| Confidence / status | validated / fixed |
| Release blocker | yes |
| Security relevant | yes |
| Feasibility | feasible_now |

## Summary and impact

The Parent #60 harness previously passed `--control-root` to the generic
Framework `synchronized_upstream.py` helper. The Parent-gitlink Framework
revision `cdc91a398d6c156eaff927d742b23018a3817fb6` does not implement that
option, so the upstream exited before publishing its address and required
synchronized Phase-4 controls could not start. This is a Parent test-contract
failure, not a Framework/MRTS change authorization or a runtime-gate bypass.

No production byte leak was shown because the failure occurred in the test
upstream. It nevertheless prevented current native proof for the P0
response-body enforcement finding `FND-PARENT-0038`.

## Observed behavior, preconditions, and reproduction

With the exact read-only Framework revision and a synchronized Phase-4 mode,
the initial deny control exited `77`; its stderr recorded an unrecognized
`--control-root` argument. The Parent harness now sends that option only to
the explicit Parent-owned custom MIME helper that supports it. The generic
pinned Framework helper receives only its supported ready, paused, release,
and server-evidence file arguments.

Reproduce the old failure by running the initial exact deny control with the
unconditional option. Reproduce the repair by selecting the supported generic
helper and the explicit custom helper separately, then running the focused
wiring test and exact native matrix.

## Evidence

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| Initial deny synchronized-upstream stderr | `ce80d9e44a44a3d018435ba418db0498a5cd9f4048627d27c0f21a6b81bbdd0b` | exit `77`, argparse rejects `--control-root` |
| Initial deny status | `5f7ce3ab6d8be2a2946edf6669446aec8bb611e755468c11bafc8108304dd354` | upstream did not publish its address |
| Post-fix exact native matrix | `2218e7d5545f6b09dcb43d1b0779889fc778a16d3f3f65e2246598c3b54e4627` | 30 controls exit `0` |
| Post-fix manifest | `1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548` | sealed current inventory |

The complete paths, command lines, working directories, and retention data are
in `finding.json` under run
`20260719T162259Z-pr60-exact-head-revalidation-dfba422e`.

## Root cause and remediation

PR #60 treated the custom MIME helper and the pinned Framework helper as having
the same CLI. They do not. The focused Parent patch makes
`APACHE_PHASE4_SYNCHRONIZED_UPSTREAM_CONTROL_ROOT=1` select
`--control-root` only for the explicit Parent-owned custom helper; the generic
Framework invocation omits it and preserves all supported control-file
arguments. The static wiring regression preserves both contracts.

## Acceptance, validation, and legitimate controls

- The generic pinned Framework helper receives ready, paused, release, and
  server-evidence arguments without `--control-root`.
- The explicit custom MIME helper receives `--control-root` only when selected.
- The focused wiring suite and shell syntax pass.
- The serial exact native 30-control Phase-4 matrix passed after the repair.
- Framework, MRTS, and both gitlinks remain unchanged.

## Dependencies, blockers, and residual risk

Dependencies are the exact read-only Framework revision above and task-owned
Apache/libModSecurity components. This finding is **fixed**, not verified:
the final local Codex Security diff scan, exact pushed-head CI, CodeQL,
SonarCloud, review/thread evidence, protected merge, and resulting-master
validation remain required for PR #60. No runtime gate was bypassed and no risk
is accepted.

Related finding: `FND-PARENT-0038`; this is not a duplicate because it covers
the Parent test contract rather than the response enforcement boundary.

## History

- `2026-07-19T17:06:28Z` — exact native deny control exposed the unsupported
  Framework CLI argument.
- `2026-07-19T18:20:42Z` — focused Parent invocation selection, wiring tests,
  and the sealed exact native matrix passed; finding set to `fixed` locally.
