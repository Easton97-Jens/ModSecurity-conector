# FND-PARENT-0062 — Python workflow inventory contract references a removed verified-report governance job

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0062 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / confirmed |
| Status / feasibility | validated / feasible_now |
| Release blocker / security relevant | yes / no |
| Scope | Parent Python workflow inventory and verified-report governance job identities |

## Observation, expected behavior, and impact

On Parent master `dd175053b3d7f509286af87646d6eb093a49d578`, the command
`rtk proxy make check-python-version-contract` exits `2`. Its explicit normal-
job inventory still requires
`verified-report-governance.yml:verified-report-contract-preflight`, while
`.github/workflows/verified-report-governance.yml` no longer defines that job.

The receipt independently proves that the workflow, checker, and Makefile
scope is identical to `origin/master` and is not changed by PR #138:

```text
git diff --quiet origin/master -- .github/workflows/verified-report-governance.yml ci/checks/common/check-python-version-contract.py Makefile
exit 0
```

The unaltered failing result is:

```text
python-version-contract: expected normal Python job is absent: verified-report-governance.yml:verified-report-contract-preflight
make: *** [Makefile:1276: check-python-version-contract] Error 1
```

The explicit inventory and checked-in workflows must instead describe the same
current contract, so the make target exits `0` on current Parent master while
still failing closed for an actually missing required Python job. The current
failure blocks trustworthy CI validation and can mask meaningful inventory
drift behind a permanently failing baseline. It is a P1 CI release blocker,
not a security finding.

## Evidence and reproduction

Retained evidence belongs to source run `merge-prs-129-149-master-20260728`:

`/var/tmp/codex/ModSecurity-conector/runs/merge-prs-129-149-master-20260728/evidence/fnd-parent-0062-python-workflow-contract-drift.md`

SHA-256:
`17ae8b2b76e65e4f9db7625122b56f5d74c171bed69912f6ba2a68198b3b283e`

The evidence was recorded at `2026-07-28T07:03:58Z`. From
`/var/tmp/codex/ModSecurity-conector/worktrees/parent/sonar-report-conditionals-20260727`,
the scope-equivalence control exited `0`, then `rtk proxy make
check-python-version-contract` exited `2`. No workflow, scanner, suppression,
Framework, MRTS, Gitlink, or delivery state changed while the receipt was
collected.

To reproduce, confirm the same scope-equivalence control, run the make target,
and observe the exact missing identity above.

## Root cause and bounded remediation

`ci/checks/common/check-python-version-contract.py` retains
`JobIdentity("verified-report-governance.yml", "verified-report-contract-preflight")`
in `EXPECTED_NORMAL_PYTHON_JOBS`, but
`.github/workflows/verified-report-governance.yml` no longer defines that job.
`inventory_violations` therefore emits the missing-job failure.

The remediation is a separate focused Parent workflow/checker-alignment PR.
It must preserve canonical Python setup and the existing workflow trust
controls, restore a truthful exact inventory/workflow relationship, add a
regression test, and obtain hosted proof. It must not be silently folded into
PR #138.

## Acceptance and validation

Acceptance requires all of the following:

- the exact inventory and defined verified-report-governance jobs are aligned
  at the corrective PR head without weakening canonical Python setup or trust
  controls;
- `rtk proxy make check-python-version-contract` exits `0` on that aligned
  tree;
- focused coverage in `tests/test_python_version_contract.py` proves the
  selected alignment and an independent missing-job negative control;
- the inventory remains explicit rather than becoming a broad filename or
  job-name pattern;
- relevant workflow syntax and CI-contract checks pass; and
- the exact corrective head has hosted proof, followed by an original-target
  rerun on resulting Parent master before the finding becomes verified or
  closed.

The legitimate controls retain the canonical `.python-version` setup and
verifier contract, keep a deliberately absent different required job
fail-closed through `inventory_violations`, and preserve the existing
least-privilege/trust-control topology of the verified-report-governance
workflow.

## Dependencies, residual risk, and history

Dependencies are a separate focused Parent alignment PR, focused Python
inventory regression coverage, and exact-head hosted plus resulting-master
proof. There are no current blockers to implementing that focused repair.

Until the repair and its resulting-master rerun exist, the mandatory Python
workflow inventory contract cannot serve as a passing current-master control.
No trust-control weakening, scanner change, suppression, Framework/MRTS action,
Gitlink update, or risk acceptance is recorded.

- `2026-07-28T07:03:58Z` — Validated on current-master-equivalent scope with
  the retained receipt hash above. This record is deliberately separate from
  PR #138 because its workflow/checker alignment root cause and remediation
  boundary are independent.
