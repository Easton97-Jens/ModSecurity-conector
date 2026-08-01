# FND-PARENT-0055 — Apache upstream-integration adapters rejected their own task-local runtime contract

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0055 |
| Category | test_failure |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / validated |
| Status / feasibility | blocked / feasible_now |
| Release blocker / security relevant | false / true |
| Scope | Parent Apache request-body regression and Valgrind soak adapters |
| Framework / MRTS impact | read-only / unchanged |

## Observation and impact

The initial Parent request-body adapter passed a generated external YAML through
`TEST_CASE` without registering its configuration directory through the
Framework-supported `EXTRA_CASE_ROOTS` boundary. Framework therefore rejected
the case as outside the selected scope before Apache startup.

The initial Parent soak adapter reused the POSIX-shell global variable name
`candidate` in nested validators. The ancestor walker changed the caller's
validated external root to `/`, causing an attempted run directory under
`//apache-soak-*` before any Valgrind or Apache process could begin.

These were test-adapter defects, not production Apache behavior or a security
exploit. They prevented required evidence from reaching the real environment
prerequisites and are now verified repaired at that preflight boundary.

## Scope and constraints

The correction is Parent-only. It adds the generated configuration directory
as the sole extra case root, enables the fixture's no-CRS baseline, and keeps
all Framework source, MRTS, Gitlinks, Docker/Compose assets, production
handlers, path controls, and artifact budgets unchanged.

## Remediation and validation

The request-body adapter now sets `EXTRA_CASE_ROOTS` to exactly its
task-local configuration directory and `NO_CRS_BASELINE=1`. The soak adapter
uses distinct variables for its outer directory, path check, and ancestor
walk, preserving its absolute-path, symlink, and outside-checkout checks.

- `make check-apache-request-body-regression-wiring` passed: 8 tests and shell syntax.
- `make check-apache-soak-wiring` passed: 12 tests and shell syntax.
- The request-body rerun resolved its external case and then blocked only on
  the missing prepared Apache `httpd`; the former scope failure was absent.
- Memcheck and Helgrind reruns each wrote bounded task-local reports and then
  blocked only because Valgrind is unavailable; the former `//apache-soak-*`
  path failure was absent.

## Acceptance criteria

1. The external request-body YAML resolves through `CASE_SCOPE=all`, a
   restricted `EXTRA_CASE_ROOTS`, and the no-CRS baseline.
2. A valid external soak root remains unchanged through nested shell helpers
   and is never reduced to `/`.
3. Both focused Parent contract suites pass.
4. Reruns reach only legitimate Apache/Valgrind prerequisite blockers.
5. A future prepared environment runs native request-body, Memcheck, and
   Helgrind evidence without treating a blocker as success.

## Evidence and limitation

Retained artifact:
`.codex/runs/20260726T083705Z-apache-upstream-pr-91-94-integration/evidence/apache-adapter-preflight-repair.md`
(SHA-256 `a7ddb2d028d70914dd98178a8913b3c91d74af9f84d27b5d4ada72b8f3609ce5`).

The strongest available proof reran both original adapter entry points to the
next legitimate fail-closed prerequisite. The environment lacks a prepared
Apache runtime and Valgrind, so no native HTTP result, memory-leak result, or
race result is claimed.

## Residual risk

The repaired contracts are verified locally, but native request-body,
Memcheck, and Helgrind assurance remains blocked by the separate local tooling
condition (`FND-HOST-0002`). No gate was bypassed and no risk is accepted.

## History

- 2026-07-26 — Recorded the external-case-scope and shell-variable-collision
  failures observed during the Parent upstream PR #91–#94 adapter preflight.
- 2026-07-26 — Applied the narrow Parent-only corrections, passed both static
  suites, and reran to the legitimate missing-`httpd`/missing-Valgrind
  blockers. The finding is verified, not a claim of native runtime success.
