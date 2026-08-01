# FND-FRAMEWORK-0030 — Framework ModSecurity v3 provenance guard rejects the approved recursive source topology

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0030 |
| Category | ci_failure |
| Repository / ownership | framework / framework |
| Priority / severity | P1 / not_applicable |
| Confidence / status | validated / fixed |
| Feasibility | feasible_now |
| Release blocker | yes |
| Security relevant | yes |

## Observation and impact

At Framework master `784977615acfc55567e37b863309abc4a38ac877`, both
isolated Apache and NGINX consumers stop before source consumption with:

```text
BLOCKED: ModSecurity v3 checkout declares submodules without an approved provenance rule
```

The retained component inventory records the checked-out root origin
`https://github.com/owasp-modsecurity/ModSecurity.git`, exact root commit
`0fb4aff98b4980cf6426697d5605c424e3d5bb60`, `git fsck: PASS`, recursively
initialized submodules, eight pinned children, and clean submodule status.
The blanket Framework guard rejects this known approved topology simply because
the upstream root contains `.gitmodules` and Gitlinks.

The current outcome is fail-closed: no unapproved source reached a build.
However, it also blocks the legitimate source and therefore prevents Apache and
NGINX component preparation, current evidence for `FND-CROSS-0001`, and the
protected integration path for Parent PR #55.

## Evidence and cause

| Consumer / evidence | SHA-256 |
| --- | --- |
| Apache provenance blocker log | `62685d6097be5af3e933c735ac2c04bb0f08a51050485d2e36661b1793fe11b5` |
| NGINX provenance blocker log | `d2b6288dec1b94a6e59d55040fa9355de4949519ae922cefd1ceb7ded9693fd2` |
| Retained component inventory | `d7e6517fe8be3a610dd51478cbb45c2fe9b4af3b1720562076129e24822efac3` |

All artifacts are retained under run
`20260720T163253Z-pr55-runtime-evidence-refresh-698b1734` in its `evidence/`
directory. The first two are the Apache/NGINX consumer logs; the third is
`runtime-component-manifest-initial-failure.json`, whose recursive source
inventory reports the approved root and clean eight-child topology.

`ci_require_approved_modsecurity_v3_checkout` categorically rejects every
`.gitmodules` manifest or mode-`160000` Gitlink before a topology-specific
rule could validate it. That rule is incompatible with this exact approved
upstream commit, which legitimately uses a recursive pinned submodule graph.

Post-fix retained evidence:

| Field | Value |
| --- | --- |
| Run ID | `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607` |
| Artifact | `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md` |
| Type | `framework_postfix_security_validation_report` |
| SHA-256 | `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec` |
| Command | RTK-wrapped focused topology/provenance suite, Framework Make provenance contract, documentation checks, full Framework lint, and independent focused security re-review |
| Working directory | `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree` |
| Exit code / observed | `0` / `2026-07-20T21:07:10Z` |
| Retention | `retained_task_evidence` |

## Required remediation and validation

The local candidate retains root origin/commit/ref and hardened Git controls,
replaces categorical `.gitmodules`/Gitlink rejection with a static exact
eight-child `(path, origin, commit)` topology, and validates clean root/child
worktrees, canonical paths, child-gitdir containment, exactly one `origin`,
and detached HEADs. Missing, uninitialized, extra, dirty, path-mismatched,
origin-mismatched, commit-mismatched, symlinked, escaping, or unparseable
topology fails closed. It never generically accepts recursive submodules.

Fresh acquisition establishes a private source root before Git, pins the root,
scrubs local recursive-update configuration, explicitly initializes/checks out
the approved children, and re-validates the same topology. The focused suite
covers the exact clean topology plus dirty, missing/uninitialized, extra,
wrong origin/commit, path escape/symlink, external gitdir, worktree, remote,
and symbolic-HEAD variants. The suite (24 tests), Framework Make provenance
contract (24 tests), CI bootstrap contract (6 tests), documentation and Change
Record checks, and full Framework lint passed. The independent focused review
found no remaining high or critical blocker for the documented cross-UID local-
attacker model.

The documentation now describes this exact recursive initialization and
validation; it does not claim categorical rejection of all `.gitmodules` or
Gitlinks. A fresh Parent component/runtime exercise still requires the
independent Parent cache repair `FND-PARENT-0042` and an independently
delivered Framework revision.

## Boundaries and disposition

This record is `fixed`, not `verified`, closed, or risk accepted. The evidence
still describes an availability false rejection rather than a successful
supply-chain bypass; dirty-worktree checking is a required fail-closed repair
control. The companion P0/high `FND-FRAMEWORK-0032` is also locally `fixed` in
the same candidate.

No Framework branch, pull request, merge, Parent gitlink update, or MRTS action
has occurred. A separate Framework PR, exact-head checks/review/Sonar evidence,
Framework-master verification, a separately authorized Parent gitlink update,
the independent `FND-PARENT-0042` repair, and fresh `FND-CROSS-0001` runtime
evidence remain required before Parent PR #55 can progress.

## History

- 2026-07-20T16:53:52Z — Apache and NGINX consumer paths both reproduced the
  categorical Framework guard failure; retained inventory showed the approved
  root and clean recursive topology.
- 2026-07-20T17:14:09Z — the finding was deduplicated from prior ModSecurity
  v3 parser/updater records and allocated for a Framework-only fail-closed
  provenance repair; no Framework or MRTS delivery action occurred.
- 2026-07-20T18:36:32Z — FND-FRAMEWORK-0032 was allocated as a distinct
  validated P0/high local-Git security blocker in the candidate. The topology
  repair remains in_progress but is not deliverable until that finding passes
  its focused regression, legitimate-control, and no-mutation proof.
- 2026-07-20T21:20:47Z — the local candidate installed the static exact
  eight-child topology guard, hardened and contained fresh recursive
  initialization, and passed focused topology/configuration negatives,
  legitimate controls, Make, lint, documentation, Change Record, and
  independent review. Status is `fixed`, not `verified`, pending separate
  Framework PR and master verification.
