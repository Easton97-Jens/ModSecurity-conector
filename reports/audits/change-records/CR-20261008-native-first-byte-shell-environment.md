# Change Record: CR-20261008-native-first-byte-shell-environment

**Language:** English | [Deutsch](CR-20261008-native-first-byte-shell-environment.de.md)

Bounded first-byte shell follow-up; no native runtime claim.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-native-first-byte-shell-environment |
| Date (UTC) | 2026-10-08 |
| Base revision | `8c19e31a21f0388b7b1417f0d25bb6530f496fae` |

## Motivation and problem statement

Aggregate lifecycle ShellCheck still reported seven SC1007/SC2097/SC2098 warnings in the first-byte helper after the baseline correction. Empty CDPATH and caller-expanded child assignment semantics were implicit.

## Acceptance criteria

Remove these warnings without suppression; retain actual helper/harness paths, caller environment, quoted argv, nonzero exit, Safe mode, fresh projection and missing-evidence rejection. Preserve existing baseline and routing tests.

## Implementation decision and rationale

Spell the empty CDPATH as CDPATH=''. Add only an explicit env executable before the outer assignment list; all RHS and wrapper/harness path expansions remain in the caller shell. No defaults, guards, evidence requirements or native selection change.

## Changed files

ci/runtime/lifecycle/run-native-first-byte.sh (two-line correction); new tests/test_native_first_byte_shell_environment.py; this generated EN/DE pair. No baseline, Framework, MRTS, catalog or schema edits.

## Commands executed

RTK-wrapped Parent Python unittest -v ran tests.test_native_first_byte_shell_environment, tests.test_no_crs_baseline_shell_environment, tests.test_no_crs_native_authority_wiring and tests.test_nginx_selected_configtest_wiring. RTK shellcheck -S warning checked run-no-crs-baseline.sh, run-connector-stage.sh and run-native-first-byte.sh together; RTK sh -n checked each separately. Generator archive and git whitespace checks followed. Neutral external TMPDIR: /var/tmp/codex/ModSecurity-conector/runs/dv-Hm965b; bytecode/user-site disabled.

## Security impact

No suppression or gate relaxation. Recording doubles prove concrete quoted wrapper argv and environment for Apache/NGINX, exit 23, Safe mode and a fresh non-precreated NGINX projection name. Negative controls preserve missing helper BLOCKED, unknown connector rejection, validator failure and missing log/barrier failure.

## Runtime evidence

None. Unit doubles do not run native hosts. The recording validator does not establish real path authority; separate existing path-security coverage remains required. Dummy log bytes are explicitly not native events and cannot produce a result receipt.

## Known limitations

These checks prove shell orchestration and static/syntax validity only, not native streaming, Engine behavior or Protected/canonical proof.

## Remaining risks

Coordinator must cherry-pick and run actual final runtime checks against the clean pinned source/build/authority tuple.

## Checks not run and rationale

Build, native runtime, package installation, remote CI and Sonar were outside scope. ShellCheck was installed and executed, with no skips.

## Final diff and review status

RED reproduced all seven warnings while four behavior controls passed before the change. Final suite: 37 PASS in 21.182 seconds, no skips. Aggregate warning-level ShellCheck and all three syntax checks exit 0. Diff contains only the authorized script, new test and record pair; no dependency replay or status promotion.
