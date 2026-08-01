# FND-PARENT-0074 — Case runners accepted symlinked verified runtime roots before artifact writes and native oracle execution

## Classification

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0074 |
| Category | security_validated |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P3 / low / validated (0.78) |
| Status / feasibility | closed / already_fixed |
| Release blocker / candidate-integration blocker / security relevant | false / false / true |
| Protocol / profile | local/shared-host CI and test-runner verified-artifact-root filesystem boundary / verified clean-history Parent replacement PR #213 was merged to `master` at `f335965fd5f7b9640fc39a1dd7873d46d7c989c5` |

## Summary

Before the local candidate, both lifecycle case runners applied
`Path(...).resolve()` to the selected CLI/environment/default
`VERIFIED_RUN_ROOT` before artifact-directory creation. A lower-privileged
actor sharing a sticky temporary parent could pre-create a final or parent
symlink that redirected runner-owned writes; the native runner then compiled
or reused and executed a fixed-name oracle below that redirected tree.

The local candidate selects `CLI > VERIFIED_RUN_ROOT > historical fallback`
through `prepare_verified_runtime_artifact_root()`. It normalizes lexically,
delegates to the existing descriptor-based no-follow owner/mode validator,
fails closed with exit `77`, and validates runner-created case/log/oracle
directories. Focused negative and legitimate controls pass on the tree proven
identical to current `master`; fresh exact-head hosted verification and
post-merge master checks have completed successfully.

## Observed and expected behavior

The pre-remediation root selection in both case runners followed a
caller-controlled existing symlink with `Path(...).resolve()` before `mkdir`,
artifact writes, compiler output, native-oracle reuse/execution, or a child
harness. The predictable historical fallback is
`/var/tmp/ModSecurity-conector-verified`. This is a local/shared-host
filesystem-integrity boundary, not a GitHub pull-request token, secret,
network, or connector-request boundary.

Before either case runner writes artifacts, compiles, reuses, executes, or
launches a child harness below `VERIFIED_RUN_ROOT`, the selected root and every
created runner-owned descendant must be private, current-user-owned,
non-symlinked, and traversed without following links. The runners preserve
`CLI > VERIFIED_RUN_ROOT > historical fallback` precedence while rejecting
unsafe, broad, foreign-owned, group/world-writable, final-symlinked, or
parent-symlinked roots. Explain-only behavior must not materialize a runtime
root.

## Impact, source-to-sink path, and preconditions

```text
lower-privileged local/shared-host actor -> final or parent symlink below sticky /var/tmp -> Path(...).resolve() follows it -> runner-owned artifact/compiler/oracle/harness path below redirected tree -> potential victim-identity artifact redirection or fixed-name oracle execution
```

A successful pre-seed could redirect evidence artifacts and, on the native
path, cause a trusted developer or runner to reuse or execute a substituted
fixed-name oracle. The effect requires a local/shared-host timing and
filesystem precondition, so this is low/P3. There is no evidence of remote
reachability, public endpoint exposure, GitHub external-PR/token escalation,
secret access, connector request-processing impact, or a normal hosted-CI
attacker path.

Preconditions are a lower-privileged actor sharing a host or self-hosted runner
with the invoking identity, selection of the historical fallback or a
caller-supplied final/parent-symlinked root, and runner-owned artifact creation.
Native impact additionally requires the compiler/oracle prerequisites and
native execution path.

## Affected scope and evidence

- `ci/lib/runtime_path_utils.py`: `prepare_verified_runtime_artifact_root`,
  `verified_runtime_artifact_root`, and `ensure_safe_runtime_directory`.
- `ci/runtime/lifecycle/run-native-case-comparison.py`:
  `run-native-case-comparison.main`, `run_native_case`, and `compile_oracle`.
- `ci/runtime/lifecycle/run-verified-case.py`: `run-verified-case.main`.
- `tests/test_runtime_artifact_utils.py` and
  `tests/test_runtime_path_security.py`.

| Evidence | SHA-256 | Result |
| --- | --- | --- |
| Local case-runner hardening receipt | `ee818da377f476f02852ea5286dcf20b508d14dc85d4b91d0fb51e72357c32e1` | External-root syntax, focused runtime artifact/path/report tests, terminal-status compatibility, and diff hygiene passed; final-/parent-symlink cases return `77` before observed victim/output mutation. |
| Sealed Codex Security diff scan | `f25310a5fd1b2c074d8be405895549c6c3c30f0acd242ace818b16dc1eef463a` | All eight changed source/test rows were fully reviewed; no reportable diff-introduced security finding survived discovery. |
| Draft PR #202 initial delivery receipt | `624874cf47b387a05e3572085ba7e775e55a7bf57b186f9cdab11d47c6b69d03` | Draft PR #202 is open; local, origin, and GitHub head equal `c846c2c6716c5e321b8743c1d191bfc8193163ca`, base is `caddd86d1eede95de53aa1bc971dd26d875df21c`, and terminal hosted checks/Sonar remain pending. |

The retained artifacts are:

- `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/case-runner-root-hardening-local.md`
- `/var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-conector/caddd86d1eede95de53aa1bc971dd26d875df21c_20260730T142059Z/scan-manifest.json`
- `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/pr-202-initial-delivery.md`

## Root cause and remediation

The runners treated resolution of an absolute-looking pathname as sufficient
authority. `Path.resolve()` follows an attacker-planted link before the
existing no-follow, ownership, and mode controls can inspect it. The resulting
redirected tree becomes the parent of predictable artifact and native-oracle
paths.

The repair centralizes selection in `prepare_verified_runtime_artifact_root()`:
it preserves `CLI > VERIFIED_RUN_ROOT > historical fallback`, lexically
absolutizes without link resolution, delegates to the existing no-follow
private-root validator, returns `77` before runner-owned writes or children on
`ValueError`, and creates runner-owned case/log/oracle directories with
`ensure_safe_runtime_directory()`. Do not weaken workflow permissions, Sonar
rules, Quality Gates, test controls, or separate root contracts.

## Acceptance criteria and validation plan

1. Both runners preserve `CLI > VERIFIED_RUN_ROOT > historical fallback` and
   return `77` before writes or child-process launch when the root is unsafe.
2. Final-root and parent-component symlinks cannot mutate the target or native
   summary output through either runner interface.
3. A legitimate private root is created with safe modes; relative input is
   lexically normalized and `--explain` does not materialize a runtime root.
4. Focused source/test/security-diff controls pass on the committed candidate
   without a Framework/MRTS action, suppression, or Quality-Gate change.
5. After push, the exact PR head has fresh hosted GitHub/Sonar evidence before
   any `verified` or `closed` disposition.

Retain the two receipts above, rerun `py_compile`, the focused runtime
artifact/path/report tests, terminal-status compatibility, and `git diff
--check` after final documentation/commit changes. Keep the Framework-dependent
`tests.test_collect_no_crs_source` and runtime-environment suite as
`blocked_missing_local_checkout`; do not initialize or change Framework/MRTS
to make them pass. After push, compare local, remote, and PR SHA and inspect
exact-head GitHub and SonarQube Cloud status.

## Dependencies, residual risk, and history

The historical PR #202 entry had task-owned commit and normal push at exact
head `c846c2c6716c5e321b8743c1d191bfc8193163ca`; its then-pending checks are
preserved below as history only. It is related to `FND-PARENT-0068`, but is not a
duplicate: the local/shared-host weakness family has distinct lifecycle
case-runner root selection, sinks, tests, and remediation. `FND-SONAR-0016`
remains the task's aggregate Sonar observation.

The repair covers only verified-run-root selection and runner-created
descendants. It does not claim safety for separate caller-owned `--build-root`,
`--tmp-root`, native `--output-dir`, connector/framework roots, or a same-UID
actor that can mutate an already-private root. No live cross-user race,
connector host, or Framework checkout was introduced. The focused security
controls, exact-head hosted checks, protected merge, and post-merge master
checks have been observed.

- `2026-07-30T14:33:26Z`: Allocated after deduplication against
  `FND-PARENT-0068`. Local source-to-sink, negative symlink,
  legitimate-control, and sealed security-diff evidence support `fixed`;
  commit/push/PR/hosted evidence remains pending.
- `2026-07-30T15:10:00Z`: Normal push created Draft PR #202 against `master`.
  Its local, origin, and GitHub head equal
  `c846c2c6716c5e321b8743c1d191bfc8193163ca`; base equals
  `caddd86d1eede95de53aa1bc971dd26d875df21c`. Initial checks are incomplete,
  so no Quality Gate, zero-new-issue/duplication, `verified`, `closed`, or
  merge claim is made.

### Final verification and closure

The dated PR #202 entries above remain historical evidence only. The current
user-authorized clean-history replacement PR #213 passed its own exact
`pull-request-range` Secret Scanning, required GitHub contexts, and SonarQube
Cloud Quality Gate with zero OPEN/CONFIRMED issues and `0.0%` New-Code
duplication. It was merged by the protected SHA-bound squash flow to
`master` commit `f335965fd5f7b9640fc39a1dd7873d46d7c989c5`; the branch tree
is byte-identical to that master tree, the focused root-security modules pass
26 tests, and the post-merge master checks passed.

This closes the finding: the original symlink-root regression controls now
pass on the resulting master tree. The separate historical PR #202 scanner
observation is retained in `FND-PARENT-0075` as `not_applicable`; it was not
suppressed, rewritten, or treated as a passing scan.

## Current reconciliation confirmation — 2026-08-01

[PR #213](https://github.com/Easton97-Jens/ModSecurity-conector/pull/213) merged
normally as `f335965fd5f7b9640fc39a1dd7873d46d7c989c5`, reachable from current
`origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`. After later runner
changes, the current root/symlink control suite was rerun with `python3 -B -m
unittest tests.test_runtime_artifact_utils tests.test_runtime_path_security
tests.test_generated_report_evidence_integrity`: 107 tests passed. This
confirmation supplements, rather than replaces, the retained 26-test and
exact-range Secret Scanning evidence. The suite was rerun after the test-only
PR #229 update on `59aba762f2d852fd917079ca8519e4ea7f49169c` and again passed
107 tests.
