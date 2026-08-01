# FND-FRAMEWORK-0036 — Fresh ModSecurity v3 provisioning honors local Git worktree and attribute configuration before provenance validation

## Identity

- Category: `security_validated`
- Repository / ownership: `framework` / `framework`
- Priority / severity / confidence: `P0` / `high` / `validated`
- Status / feasibility: `verified` / `feasible_now`
- Release blocker / security relevant: `true` / `true`
- Affected revision: `f98a8739cb13b583f23d646784b144e596b61441` (historically validated on `784977615acfc55567e37b863309abc4a38ac877`)
- Parent impact: blocks the legitimate runtime-evidence prerequisite for Parent PR #55; no Parent gitlink change is authorized.
- MRTS impact: none; MRTS remains strictly read-only.

## Summary, invariant, and impact

## 2026-07-26 current-master verification

The f98-based reopening evidence is historical. Framework PR #44 introduced
the reviewed fresh-root containment and local-config scrubbing hardening; it
is present on current master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`.
The current-master suite passed real-Git worktree redirect, attributes/filter,
recursive-update, fake-PATH, and clean legitimate controls, together with
`make test-modsecurity-v3-provenance-contract` and `make lint`. No Parent
Gitlink or MRTS state was changed by this verification.

After `git init` creates `MODSECURITY_V3_SOURCE_DIR/.git`, a competing actor
can alter its local configuration before the fresh pinned checkout. The
candidate invokes `ci_modsecurity_v3_git -C <source> checkout --detach
<approved commit>` before its first physical-worktree/provenance guard. The
generic wrapper removes inherited, global, and system configuration but honors
the newly written local configuration.

The invariant is that no fresh checkout may write outside its intended source
directory or execute an attribute filter before provenance validation. A
task-owned actual-wrapper fixture proved that `core.worktree=<external>` made
the checkout return `0` and write `payload.txt` only externally; only the later
guard returned `77`. A second fixture proved that `core.attributesfile` plus
`filter.evil.smudge` created a benign marker before validation. A clean control
wrote the payload only under the intended source directory.

An actor racing a shared fresh source root can redirect checkout output or
execute a local filter with the Framework/CI identity. This is a high-impact
supply-chain provisioner compromise; the proof used only temporary local Git
objects, benign payloads, and a marker, and did not access Parent, authoritative
Framework, or MRTS sources.

The earlier local remediation is historical only. On `2026-07-23`, an
independent static review of the isolated candidate based on Framework master
`f98a8739cb13b583f23d646784b144e596b61441` found that its fresh route again
uses the generic wrapper for remote add, fetch, checkout, and recursive
initialization. It does not include the required dedicated fresh-root helper,
explicit `--git-dir`/`--work-tree` binding, `core.attributesfile=/dev/null`,
`core.sparseCheckout=false`, or immediate local recursive-update scrubbing.
The validated high-impact class is therefore reopened as `in_progress`; the
reopening is static evidence, not a substitute for a fresh dynamic rerun.

## Affected path, source-to-sink, and reproduction

- `ci/provisioning/fetch-smoke-sources.sh` —
  `provision_fresh_modsecurity_v3` initializes Git and checks out before its
  root guard.
- `ci/lib/common.sh` — `ci_modsecurity_v3_git`.
- `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py` —
  required real-Git regressions.

Set local `core.worktree=<external>` after `git init`, then run the actual
candidate checkout: the pinned checkout succeeds but writes only externally.
Alternatively set `core.attributesfile=<attacker attributes>` and
`filter.evil.smudge=<benign marker script>`: checkout succeeds and creates the
marker before a guard runs. A clean same-boundary control succeeds safely.

## Retained evidence

- Run ID: `20260720T173133Z-pr55-runtime-remediation-7e38e876`
- Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-fresh-checkout-config-race-validation.md`
- Type: `task_owned_real_git_fresh_checkout_config_race_validation`
- SHA-256: `af927b36a6221b831c47446f15aa0ce25258dff1bad5325f933f686aa896eb81`
- Command: RTK-wrapped task-owned `invoke-wrapper.sh` worktree,
  attributes/filter, clean-control, and contained-checkout experiments
- Working directory: `/root/git/ModSecurity-conector`
- Exit code / observed: `0` / `2026-07-20T19:59:28Z`
- Retention: `retained_task_evidence`

Post-fix retained evidence:

- Run ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
- Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md`
- Type: `framework_postfix_security_validation_report`
- SHA-256: `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec`
- Command: RTK-wrapped focused provenance suite, real-Git custom submodule
  update control, Framework Make provenance contract, documentation checks,
  and full Framework lint
- Working directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit code / observed: `0` / `2026-07-20T21:07:10Z`
- Retention: `retained_task_evidence`

Current reopening evidence:

- Run ID: `20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d`
- Candidate `ci/lib/common.sh`:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d/tmp/parent/modules/ModSecurity-test-Framework/ci/lib/common.sh`
  - Type: `isolated_f98_based_framework_candidate_static_fresh_root_common_review`
  - SHA-256: `46744e1ad7f1b6dd4817984586985b6841085589d307b86fe963aed12c57ca62`
- Candidate `ci/provisioning/fetch-smoke-sources.sh`:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d/tmp/parent/modules/ModSecurity-test-Framework/ci/provisioning/fetch-smoke-sources.sh`
  - Type: `isolated_f98_based_framework_candidate_static_fresh_root_fetch_review`
  - SHA-256: `97f3026f1958f0af08de69f90458e3236e310f7d140bd825cccae185dd476a19`
- RTK-wrapped diff/context/hash inspection exited `0` at
  `2026-07-23T17:31:41Z`. It found only generic wrapper calls and none of the
  required fresh-root containment/scrubbing controls.

## Remediation, validation, and residual risk

The corrected candidate must establish a private source root before Git and
restore a dedicated fresh-root checkout/acquisition helper for every fresh
remote add, fetch, checkout, and recursive submodule command. It must use
`--git-dir=<source>/.git`, `--work-tree=<source>`,
`-c core.attributesfile=/dev/null`, and `-c core.sparseCheckout=false`, and
clear local `core.worktree`, `core.attributesfile`, `core.sparseCheckout`, and
every local `submodule.*.update` key immediately before the relevant Git
commands. `-c core.worktree=<source>` alone remains insufficient because the
controlled experiment still redirected checkout output.

The retained real-Git regressions cover worktree redirect, attribute/filter
execution, a public source parent rejected before Git, a custom
`submodule.*.update` marker that never executes while the legitimate child
initializes, and the clean control. The historic focused suite (24 tests),
Framework Make provenance contract (24 tests), CI bootstrap contract (6 tests),
documentation/Change Record checks, and full Framework lint passed only for
the earlier local candidate. They do not validate the current f98-based patch;
the same tests plus independent bypass review must be rerun on its corrected
exact head.

This finding is `in_progress`, not `fixed` or `verified`: a corrected Framework
PR, exact-head dynamic checks/review/Sonar evidence, Framework-master
verification, and a separately authorized Parent gitlink update remain required
before Parent PR #55 runtime evidence can proceed. Portable path-based shell
controls cannot isolate a concurrent same-UID writer; worktree-scoped or
included local configuration is therefore a same-UID hardening candidate rather
than a verified isolation claim. The finding remains distinct from
`FND-FRAMEWORK-0032` (inspection configuration), `FND-FRAMEWORK-0034`
(mutable source bytes), `FND-FRAMEWORK-0035` (materialization output
containment), and the separate host-Git PATH candidate
`FND-FRAMEWORK-0054`.

## Related findings and history

- Related: `FND-FRAMEWORK-0030`, `FND-FRAMEWORK-0032`,
  `FND-FRAMEWORK-0034`, `FND-FRAMEWORK-0035`, and `FND-CROSS-0001`.
- `2026-07-20T19:59:28Z`: dynamically validated in a task-owned actual-wrapper
  fixture; candidate delivery paused.
- `2026-07-20T21:20:47Z`: private source-parent validation, explicit fresh
  checkout containment, and recursive local-config scrubbing passed the
  worktree, attributes/filter, custom-update, clean-control, Make, lint,
  documentation, and independent-review controls on the then-reviewed local
  candidate; this is historical local evidence.
- `2026-07-23T17:31:41Z`: independent review and static inspection of the
  isolated f98-based candidate found no dedicated fresh-root helper or required
  containment/scrubbing options before generic Git calls. The validated P0/high
  finding is reopened as `in_progress` pending a corrected candidate and fresh
  dynamic controls; no product source, Framework branch/PR, Parent gitlink, or
  MRTS state changed by this tracking update.
