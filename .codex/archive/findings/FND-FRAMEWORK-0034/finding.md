# Finding: ModSecurity v3 validator can accept mutable tracked source bytes hidden by Git index flags

**Language:** English | [Deutsch](finding.de.md)

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0034 |
| Category | security_validated |
| Repository / ownership | framework / framework |
| Priority / severity / confidence | P0 / high / validated |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | yes / yes |
| Affected revision | 784977615acfc55567e37b863309abc4a38ac877 |
| Source runs | 20260720T173133Z-pr55-runtime-remediation-7e38e876; 20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607 |

## Summary and security invariant

An existing `MODSECURITY_V3_SOURCE_DIR` must provide only the reviewed pinned
source bytes when a Framework build later copies and executes its inputs. A
clean-status result must not hide a changed tracked file, and the validated
pathname must not be copied as mutable build input after validation.

## Observed and expected behavior

Before remediation, `ci_modsecurity_v3_require_clean_checkout` accepted an
empty `git status --porcelain` result as evidence that the source matched the
pinned Git identity. A task-owned real-Git fixture committed `build.sh` with
`approved-source`, marked it with `git update-index --assume-unchanged`, and
changed it to `unapproved-source`. Status was empty, `git ls-files -v` emitted
lower-case `h build.sh`, and the helper still returned `0`. The direct,
Apache, and NGINX consumers subsequently copy and execute the mutable
`MODSECURITY_V3_SOURCE_DIR`.

The control must reject `assume-unchanged` and `skip-worktree` index state
before any build action. It must materialize root and static approved child
trees from their exact pinned Git objects into the task-owned destination,
rather than copy the supplied working tree. That also eliminates the related
validation-to-copy replacement interval.

## Impact and preconditions

An actor able to provide or modify an existing source checkout and its local
index can cause arbitrary build input such as `build.sh`, `configure`, or a
`Makefile` to be copied and executed with the Framework build or CI identity,
despite pinned root/child commits. This is a high-impact supply-chain
provenance bypass.

The path requires an existing accepted `MODSECURITY_V3_SOURCE_DIR`, a pinned
origin/HEAD/topology appearance, and either a changed tracked file with an
unsafe index bit or a replacement of the supplied source path after validation.

## Affected files and symbols

- `ci/lib/common.sh`: `ci_modsecurity_v3_require_clean_checkout`,
  `ci_require_approved_modsecurity_v3_checkout`,
  `ci_modsecurity_v3_materialize_git_tree`, and
  `ci_materialize_approved_modsecurity_v3_source`.
- `ci/provisioning/build-v3-under-src.sh`,
  `ci/provisioning/prepare-apache-build.sh`, and
  `ci/provisioning/prepare-nginx-build.sh`: existing-checkout build consumers.
- `tests/security_regression/git_provenance_test_support.py` and
  `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py`.
- `docs/connector-integration.md` and `docs/connector-integration.de.md`.

## Reproduction and evidence

1. Create a task-owned disposable Git repository with a committed `build.sh`
   containing `approved-source`.
2. Run `git update-index --assume-unchanged build.sh`, then change it to
   `unapproved-source`.
3. Observe empty `git status --porcelain=v1 --untracked-files=all
   --ignore-submodules=none` output and `h build.sh` from `git ls-files -v`.
4. Source the isolated candidate `ci/lib/common.sh` and invoke
   `ci_modsecurity_v3_require_clean_checkout`; pre-fix it returns `0` although
   `HEAD` and working-tree bytes differ.

| Run | Artifact | SHA-256 | Result |
| --- | --- | --- | --- |
| 20260720T173133Z-pr55-runtime-remediation-7e38e876 | `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-modsecurity-v3-assume-unchanged-reproduction.md` | `1327e5e8d8e4afc92c160f408acf45db59adc15f6ab66a2706501fb1714602b6` | RTK-wrapped real-Git reproduction exited 0 and proved the pre-fix hidden-byte acceptance. |
| 20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607 | `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md` | `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec` | Post-fix focused suite 24/24, Make contract, full lint, object-snapshot control, and independent review passed; no high/critical cross-UID blocker remained. |

No changed fixture file was executed. No Parent checkout, authoritative
Framework checkout, remote service, or MRTS path was modified or accessed.

## Root cause and remediation

Normal status and index/Gitlink identity were treated as a proxy for all
consumed working-tree bytes. Git index flags weaken that proxy; the consumers
then copied the validated pathname. The local candidate now rejects non-normal
index flags and replaces every executable `cp -a` source copy with object-based
materialization through the hardened Git wrapper and `tar`. It archives the
approved root and each static approved child commit into a private task-owned
destination, rejects embedded `.git` metadata, and checks the destination
parent before any destination mutation.

## Acceptance criteria and validation

1. A lower-case `assume-unchanged` or `skip-worktree` index state returns `77`
   before a build action.
2. Direct, Apache, and NGINX consumers do not use `cp -a` on
   `MODSECURITY_V3_SOURCE_DIR` for executable build input.
3. Root and static approved children are materialized through
   `ci_modsecurity_v3_git` from exact pinned objects and contain no `.git`
   metadata.
4. A real Git fixture with `unapproved-source` in its working tree produces an
   `approved-source` object snapshot.
5. The clean exact eight-child control, focused security regressions, syntax,
   documentation, Change Record, Make, lint, and independent bypass review
   pass.

The planned checks are the two real-Git regressions, the full hermetic
provenance suite, `make test-modsecurity-v3-provenance-contract`, syntax,
documentation/Change-Record validation, lint, and a change-aware review of
index flags, archive coverage, extraction, source replacement, and the
existing local-Git controls.

All listed local controls passed: the focused suite passed 24/24, the Make
contract passed 24/24, the CI-root bootstrap suite passed 6/6, the object
snapshot had 5,532 files with no `.git` and no group/other permissions, and
the full Framework lint passed. The independent review found no remaining high
or critical blocker for the documented cross-UID local-attacker model.

## Dependencies, related findings, and residual risk

This finding depends on the same isolated Framework environment as
`FND-FRAMEWORK-0030` and `FND-FRAMEWORK-0032`; it is not a duplicate of either.
`FND-FRAMEWORK-0030` owns the recursive-topology availability defect, and
`FND-FRAMEWORK-0032` owns local-Git configuration execution/read-only metadata
mutation. `FND-CROSS-0001` remains the separate Parent runtime-evidence
blocker.

The direct race is source-to-sink validated but not dynamically raced. The
object-snapshot design removes reliance on post-validation working-tree bytes.
Portable path-based shell controls cannot isolate a concurrent same-UID writer;
that residual limitation is documented. This finding is `fixed`, not
`verified`: a separate Framework PR, exact-head checks/review/Sonar evidence,
Framework-master verification, and a separately authorized Parent gitlink
update remain required before Parent PR #55 runtime evidence can proceed. No
Framework master, Parent gitlink, or MRTS action has occurred.

## History

| UTC | Event | Detail |
| --- | --- | --- |
| 2026-07-20T19:12:35Z | validated_task_owned_real_git_assume_unchanged_reproduction | Empty status plus `h build.sh` permitted changed bytes through the pre-fix clean-check helper; source-to-sink review confirmed later copy-and-execute consumers. |
| 2026-07-20T19:12:35Z | deduplicated_and_started_framework_remediation | Classified P0/high/validated, in_progress, feasible_now; distinct from FND-FRAMEWORK-0030 and FND-FRAMEWORK-0032. |
| 2026-07-20T21:20:47Z | local_remediation_fixed_pending_framework_delivery | Index flags are rejected and direct/Apache/NGINX consumers materialize pinned objects. Focused/Make/lint/documentation/snapshot controls and independent review passed; status is fixed, not verified, because no Framework PR or master verification exists. |
