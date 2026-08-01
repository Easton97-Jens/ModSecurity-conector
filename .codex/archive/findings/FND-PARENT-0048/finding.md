# FND-PARENT-0048 — Update-submodules validation lacks its declared PyYAML prerequisite

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0048 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity | P1 / not_applicable |
| Confidence / status | confirmed / closed |
| Feasibility | feasible_now |
| Release blocker | yes |
| Security relevant | yes |

## Observation and impact

Authorized [run 29981644356](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29981644356)
ran against Parent `master` `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3`.
It resolved candidate `f73f8842f45318e2df8aff1d31855eeb7c20a22f`, completed the
read-only candidate checkout, selected Python `3.14.6`, and passed the
interpreter contract. `make quick-check` then failed at
`check-framework-fixture-syntax` with:

```text
PyYAML is required for fixture syntax lint
```

The publisher was skipped. No candidate branch, PR, Parent gitlink, Framework
source, or MRTS state changed. This blocks valid candidate publication but
remains fail-closed rather than enabling a privileged path.

## Root cause and safe remediation boundary

`requirements-dev.txt` already declares `PyYAML>=6,<7`, and the checker
deliberately fails when it cannot import that dependency. The validation job
sets up the interpreter but does not install a validation dependency before
`make quick-check`.

Install a CI-only PyYAML 6.0.3 lock after `Verify Python interpreter contract`
and before `Run quick check without write permissions`. It uses
`--require-hashes` and `--only-binary=:all:` to admit only the reviewed GitHub-
hosted Linux x86_64 wheel. The cross-platform development declaration remains
unchanged. Static coverage asserts the lock identity, hash, and ordering. Do
not change permissions, candidate execution boundary, publisher, Parent
gitlink, Framework, or MRTS.

## Security assessment

Remote Framework content executes only in the `contents: read` validator; the
separate writer runs only after success, revalidates the full official SHA,
checks out no submodule, and changes only the Parent gitlink. That topology is
`already_safe`. The correction adds neither an explicitly injected secret nor
a write permission or publisher path. The new package-acquisition boundary is
hash-locked and rejects source distributions.

## Acceptance criteria and validation plan

1. The validator installs the CI-only immutable PyYAML lock in the documented
   order.
2. The lock admits only PyYAML 6.0.3's reviewed Linux x86_64 wheel hash and
   rejects source distributions.
3. Static CI-security coverage proves the command, lock identity/hash, order,
   exact job permissions, and resolver → validator → publisher gating.
4. Focused workflow tests, lock-metadata validation, `make
   check-ci-security-contract`, a focused security-diff review, and `git diff
   --check` pass without a local/system package installation.
5. A task-owned Parent PR includes source, regression, full English/German
   Change Record, and actual evidence; it is not merged by this task.
6. Only a later separately authorized master integration followed by a fresh
   successful current-master run can verify this finding.

## Dependencies, blockers, and residual risk

`requirements-dev.txt` remains the cross-platform development declaration;
the CI-only lock is the immutable authority for this hosted Linux x86_64 step.
The lock fails closed on a platform change until it is reviewed. The master-
only workflow cannot prove a new PR head, so the hosted workflow remains
pending until a separate master authorization. Candidate publication stays
blocked meanwhile; no security risk is accepted.

## Evidence

Retained receipt:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09/evidence/update-submodules-run-29981644356.md`

SHA-256:
`ee0f259951d639b96624e9bccc84fd45f5384845eb95b42e84e75535e3baa412`

## History

- `2026-07-23T05:15:37Z` — The single authorized current-master dispatch
  exposed this distinct dependency-preparation failure after the full-SHA
  resolver and read-only candidate checkout succeeded. The publisher skipped
  correctly. This record is separate from `FND-PARENT-0045` because the root
  cause and remediation boundary differ.
- `2026-07-23T06:34:43Z` — The first `FND-PARENT-0048` corrective
  implementation introduced distinct `FND-PARENT-0049`: an unquoted
  `--only-binary=:all:` command made the workflow invalid YAML before validator
  or publisher execution. `FND-PARENT-0048` remains the missing PyYAML
  prerequisite; `FND-PARENT-0049` owns the YAML-scalar quoting regression.

## Closed disposition — 2026-08-01

[PR #92](https://github.com/Easton97-Jens/ModSecurity-conector/pull/92) merged
normally as `95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3`, reachable from current
`origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`. The current workflow
installs the hash-locked validation dependency before the quick check; the
current master quick-check workflow succeeded at both that install and the
read-only quick-check step. Exact PR checks passed.
