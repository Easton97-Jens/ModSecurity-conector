# FND-FRAMEWORK-0032 — ModSecurity v3 provenance validator executes local Git fsmonitor configuration and writes during claimed read-only validation

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0032 |
| Category | security_validated |
| Repository / ownership | framework / framework |
| Priority / severity | P0 / high |
| Confidence / status | validated / fixed |
| Feasibility | feasible_now |
| Release blocker | yes |
| Security relevant | yes |

## Summary and behavior

The Framework candidate accepts a caller-supplied existing
MODSECURITY_V3_SOURCE_DIR and invokes git status through ci_modsecurity_v3_git
for the root and every approved child. Before this remediation, the wrapper
cleared inherited/global configuration but did not override local
core.fsmonitor or disable optional Git locks. A private real-Git control with a
benign marker-writing local core.fsmonitor executed the probe during plain git
status; with git --no-optional-locks -c core.fsmonitor=false, it did not
execute the probe.

A second private real-Git control set local core.worktree on an untrusted
checkout. git -C <untrusted> rev-parse --show-toplevel then resolved to a
different physical directory. Before the candidate correction, the focused
Framework test required fail-closed exit 77 but received 0.

Validation must neither execute repository-controlled Git configuration nor
write Git metadata, and it must bind each resolved root/child worktree to the
physical checked directory. Extra remotes, attached symbolic heads, external
child Git directories, topology deviations, or path escapes must fail before a
build action.

## Affected path, preconditions, and impact

Affected symbols are ci_modsecurity_v3_git,
ci_modsecurity_v3_require_clean_checkout,
ci_require_approved_modsecurity_v3_root_checkout, and
ci_require_approved_modsecurity_v3_checkout in ci/lib/common.sh. Apache,
NGINX, and direct v3 build paths invoke this guard on an existing source
checkout before source consumption.

An attacker needs to seed the accepted source checkout's .git/config or an
external child Git directory. The git status sink can then invoke an
attacker-chosen fsmonitor command with the Framework build/CI identity before
the provenance decision. Worktree/config indirection can make the checked
origin, HEAD, and status refer to a different tree. This is a P0/high
supply-chain boundary failure. The controlled proof did not use Parent,
authoritative Framework, or MRTS checkouts.

## Evidence and reproduction

Retained pre-fix evidence:

- Run ID: 20260720T173133Z-pr55-runtime-remediation-7e38e876
- Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-modsecurity-v3-git-validator-pre-fix-security-reproduction.md
- SHA-256: 805dcc95732c9f029194240fcab79b397ec21af1cbc1da0bd5bd768dbc23d716
- Command: RTK-wrapped private Git core.worktree and core.fsmonitor probes plus focused Framework pre-fix regression
- Working directory: /root/git/ModSecurity-conector
- Exit code: 0
- Observed at: 2026-07-20T18:36:32Z
- Retention: retained_task_evidence

Post-fix retained evidence:

- Run ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md`
- Type: `framework_postfix_security_validation_report`
- SHA-256: `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec`
- Command: RTK-wrapped focused provenance suite, real-Git
  fsmonitor/worktree/custom-submodule-update controls, Framework Make
  provenance contract, documentation checks, and full Framework lint
- Working directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit code / observed: `0` / `2026-07-20T21:07:10Z`
- Retention: `retained_task_evidence`

Safe reproduction uses only a task-owned benign marker probe:

1. Configure local core.fsmonitor in a disposable repository and run plain
   git status --porcelain=v1; observe the marker.
2. Repeat with git --no-optional-locks -c core.fsmonitor=false; the marker must
   not exist.
3. Configure core.worktree to another disposable directory and observe
   rev-parse --show-toplevel redirect.
4. Run the focused pre-fix worktree-redirection regression; it fails because
   the guard returns 0 instead of 77.

## Root cause and remediation

The hardened wrapper had trusted local Git configuration for status, did not
disable fsmonitor or optional locks, and did not bind Git's resolved worktree
or child gitdir to the physical source boundary. The local candidate now uses
`--no-optional-locks`, `core.fsmonitor=false`, `core.hooksPath=/dev/null`,
disables built-in fsmonitor, denies file transport, binds every root/child
worktree and child gitdir, requires exactly one `origin` and detached HEADs,
and rejects unsafe source parents before Git. Immediately before recursive Git
commands it clears local `core.worktree`, `core.attributesfile`,
`core.sparseCheckout`, and every local `submodule.*.update` key.

It preserves file-transport denial, TLS verification, hook-path hardening,
exact root/child commits and origins, static eight-child topology, and
deliberate recursive initialization only after root validation. Real-Git
fsmonitor/worktree/custom-update, public-parent, clean-control, topology, Make,
documentation, Change Record, and full-lint controls passed. The independent
review found no remaining high or critical blocker for the documented cross-
UID local-attacker model.

## Acceptance criteria and validation

1. Every provenance Git call disables core.fsmonitor and optional locks.
2. Root/child canonical worktree and child gitdir containment are enforced.
3. Extra remote, attached head, external gitdir, worktree redirect, dirty,
   uninitialized, symlinked, missing/extra, origin, and commit variants fail
   before source consumption.
4. The clean approved eight-child control and fresh pinned provisioner pass.
5. A real retained approved-source guard invocation has unchanged selected Git
   metadata hashes before/after; focused tests, Make contract, syntax,
   documentation, Change Record, lint, and final security review pass.

Regression files: tests/security_regression/test_modsecurity_v3_git_ref_provenance.py
and tests/security_regression/git_provenance_test_support.py. Owning target:
make test-modsecurity-v3-provenance-contract.

## Dependencies, residual risk, and history

This finding depends on the same Framework-only topology remediation as
FND-FRAMEWORK-0030 and is related to FND-CROSS-0001. It is not a duplicate of
FND-FRAMEWORK-0030's availability false rejection or FND-FRAMEWORK-0031's YAML
action-pin bypass. Parent gitlink and MRTS remain unchanged.

This finding is `fixed`, not `verified`: a separate Framework PR, exact-head
checks/review/Sonar evidence, Framework-master verification, and a separately
authorized Parent gitlink update remain required before it can unblock Parent
PR #55 runtime evidence. Portable path-based shell controls cannot isolate a
concurrent same-UID writer, and worktree-scoped or included local configuration
remains a same-UID hardening candidate. No Framework master, Parent gitlink,
or MRTS action has occurred.

- 2026-07-20T18:36:32Z — task-owned real-Git controls validated local
  fsmonitor execution, safe command-line suppression, core.worktree
  redirection, and the candidate's initial fail-open regression.
- 2026-07-20T18:36:32Z — the distinct P0/high Framework finding was allocated
  and remediation began without delivery action.
- 2026-07-20T21:20:47Z — hardened Git calls, root/child worktree and gitdir
  containment, private-parent validation, and recursive local-config scrubbing
  passed fsmonitor, worktree, custom-update, clean-control, Make, lint,
  documentation, and independent-review controls. Status is `fixed`, not
  `verified`, pending separate Framework PR and master verification.
