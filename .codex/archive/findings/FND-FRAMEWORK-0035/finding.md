# FND-FRAMEWORK-0035 — ModSecurity v3 object materialization uses a predictable archive path outside its private staging boundary

## Identity

- Category: `security_validated`
- Repository / ownership: `framework` / `framework`
- Priority / severity / confidence: `P0` / `high` / `validated`
- Status / feasibility: `fixed` / `feasible_now`
- Release blocker / security relevant: `true` / `true`
- Affected revision: `784977615acfc55567e37b863309abc4a38ac877`
- Parent impact: blocks the legitimate runtime-evidence prerequisite for Parent PR #55; no Parent gitlink change is authorized.
- MRTS impact: none; MRTS remains strictly read-only.

## Summary, invariant, and impact

The isolated Framework candidate materializes approved ModSecurity v3 Git
objects but initially writes its archive at the predictable pathname
`$parent/.modsecurity-v3-archive-$$.tar`. It checks that pathname before the
archive command and later passes it to `git archive --output`. The invariant is
that archive and extraction intermediates may be written only inside the fresh
private materialization boundary, even if a competing actor can create entries
in the configured destination parent.

A task-owned real-Git regression created a symlink for the legacy predictable
archive path after the helper's check. The helper returned `0`, while Git
followed the replacement and created its archive at the controlled outside
target. The proof uses only benign temporary files and never executes a
modified file. An actor sharing the destination parent can redirect a Git
archive write to another filesystem target writable by the Framework/CI
identity; this is a high-impact path-containment defect in a supply-chain
build-input boundary.

## Affected path, source-to-sink, and reproduction

- `ci/lib/common.sh` — `ci_modsecurity_v3_materialize_git_tree` and
  `ci_materialize_approved_modsecurity_v3_source`.
- `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py` —
  real-Git replacement regression.

The controlled destination parent contributes an entry after the helper's
`-e`/`-L` check. The helper invokes `ci_modsecurity_v3_git archive
--output=<predictable path>`, so Git follows the substituted symlink before
`tar` reads the archive. Reproduce using a local benign Git source and the
focused test
`test_git_object_materialization_does_not_use_predictable_parent_archive_path`.
Before remediation it returns `0` from the helper while the controlled outside
archive exists.

## Retained evidence

- Run ID: `20260720T173133Z-pr55-runtime-remediation-7e38e876`
- Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-modsecurity-v3-materialization-archive-race-reproduction.md`
- Type: `task_owned_real_git_path_containment_reproduction`
- SHA-256: `2251b587118c6c1fbb6a291c9ba05eca0efc8c5076fb3cd21432ba881515f0aa`
- Command: RTK-wrapped selected Framework unittest for
  `test_git_object_materialization_does_not_use_predictable_parent_archive_path`
- Working directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit code / observed: `1` / `2026-07-20T19:54:45Z`
- Retention: `retained_task_evidence`

Post-fix retained evidence:

- Run ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
- Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md`
- Type: `framework_postfix_security_validation_report`
- SHA-256: `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec`
- Command: RTK-wrapped focused provenance suite, public-parent/empty-
  placeholder control, Framework Make provenance contract, documentation
  checks, and full Framework lint
- Working directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit code / observed: `0` / `2026-07-20T21:07:10Z`
- Retention: `retained_task_evidence`

## Remediation, validation, and residual risk

The local candidate creates an atomically allocated private staging directory
under a parent it validates before any destination mutation, writes the archive
and extraction tree only inside that directory, and publishes the completed
tree to a previously absent destination without a predictable archive name. It
rejects normal, symlinked, or pre-existing destinations except the explicit
empty Gitlink placeholder, which the public-parent control proves remains
untouched when the parent is rejected.

Acceptance requires: the replacement regression keeps the outside target
absent while the committed snapshot is present; no predictable archive filename
is used in the caller-controlled parent; destination symlink/pre-existence
fails closed; direct, Apache, and NGINX legitimate snapshot controls continue
to succeed without `.git`; and focused security regressions, the complete
provenance suite, syntax, Make, documentation, Change Record, lint,
retained-source checks, and an independent bypass review pass before delivery.

The archive-race, public-parent, normal/symlink destination, empty-Gitlink-
placeholder, immutable snapshot, Make, documentation, and full lint controls
all passed. The independent review found no remaining high or critical blocker
for the documented cross-UID local-attacker model. Portable path-based shell
controls cannot isolate a concurrent same-UID writer; that residual limitation
remains documented. This finding is `fixed`, not `verified`: a separate
Framework PR, exact-head checks/review/Sonar evidence, Framework-master
verification, and a separately authorized Parent gitlink update remain
required before Parent PR #55 runtime evidence can proceed. It is not a
duplicate of `FND-FRAMEWORK-0034`, which owns mutable source bytes; this
finding owns output-path containment after immutable object selection.

## Related findings and history

- Related: `FND-FRAMEWORK-0030`, `FND-FRAMEWORK-0032`,
  `FND-FRAMEWORK-0034`, and `FND-CROSS-0001`.
- `2026-07-20T19:54:45Z`: validated in a task-owned real-Git replacement
  fixture; candidate delivery paused.
- `2026-07-20T21:20:47Z`: private random staging and pre-mutation private-
  parent validation passed all local controls; status is `fixed`, not
  `verified`, pending separate Framework PR and master verification.
