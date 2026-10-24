# Change Record: CR-20261008-native-baseline-shell-environment

**Language:** English | [Deutsch](CR-20261008-native-baseline-shell-environment.de.md)

Bounded shell-boundary correction; no native runtime claim.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-native-baseline-shell-environment |
| Date (UTC) | 2026-10-08 |
| Base revision | `461bcd62a3cb2159ec9750db6ad64f0ab6053cc3` |

## Motivation and problem statement

ShellCheck reported eight SC2097/SC2098/SC2034 warnings. Stage and first-byte assignment prefixes intentionally expand caller values, but this intent was ambiguous to static analysis. The final VERIFIED_COMPONENT_CACHE reset had no later consumer.

## Acceptance criteria

Clear warning-level ShellCheck without suppression; preserve child environment, quoted arguments, exit status and parent scope. Preserve canonical cache and authority guards, required selection, and prior routing regression.

## Implementation decision and rationale

Use an explicit env executable for both assignment lists: RHS and executable path expansions remain in the caller shell. Consume the initially resolved VERIFIED_COMPONENT_CACHE in the stage environment with the same canonical value. Remove only its dead final assignment; retain the live CONNECTOR_COMPONENT_CACHE inventory reset. Do not add an otherwise unused export.

## Changed files

ci/runtime/lifecycle/run-no-crs-baseline.sh; new tests/test_no_crs_baseline_shell_environment.py; this generated EN/DE record pair. No Framework, MRTS, catalog, schema or fixture changes.

## Commands executed

All commands used RTK. Parent-owned Python ran unittest -v for tests.test_no_crs_baseline_shell_environment, tests.test_no_crs_native_authority_wiring and tests.test_nginx_selected_configtest_wiring. sh -n and shellcheck -S warning checked the baseline. new-change-record.py created this pair and checked the archive; git diff --check checked whitespace. TMPDIR was the neutral external task root /var/tmp/codex/ModSecurity-conector/runs/dv-Hm965b; bytecode and user-site Python disabled.

## Security impact

No bypass, suppression or selection weakening. Tests exercise real shell subprocess boundaries with recording unit doubles, paths containing spaces, canonical cache values and child exit 23. Parent assignments do not leak from either command boundary.

## Runtime evidence

None. Recording subprocesses are unit evidence only. No NGINX host, native traffic, build or Protected gate executed.

## Known limitations

A broader 24-test attempt had two failing subtests within the Apache fixture-existence test: OwnP's uninitialized Framework submodule lacks both late-phase4 Apache YAML fixtures. These are independent hardcoded file-existence assertions, not baseline shell regressions; no fixture or test was changed to hide them.

## Remaining risks

Coordinator integration and full native/canonical runtime remain separate checks. This delivery proves shell wiring only.

## Checks not run and rationale

Native runtime/build, dependency installation, remote CI and Sonar were outside this bounded task. ShellCheck regression skips only when that executable is absent; it was installed and actually ran here.

## Final diff and review status

Focused RED reproduced all eight warnings while both command-boundary characterizations already passed. Final focused suite: 30 tests PASS in 15.585 seconds, no skips. Syntax and warning-level ShellCheck pass. Diff preserves initial cache assignment and actual live inventory reset, changes only approved files, and introduces no suppression or native PASS claim.
