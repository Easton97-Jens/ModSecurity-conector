# Change Record: CR-20261009-native-input-ledger-fd

**Language:** English | [Deutsch](CR-20261009-native-input-ledger-fd.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-native-input-ledger-fd |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

Independent review identified a conditional fixture-ledger identity gap: reopening a path did not itself pin the writer to the admitted private inode. Reachability through the ordinary closed CLI or an unprivileged attacker was not established.

## Acceptance criteria

Pass only the preopened fresh root-owned0600 regular empty single-link writable descriptor into the actual owned native master. Never arm configuration testing; fsync and close on every exit.

## Implementation decision and rationale

Replace MSCONNECTOR_OWNED_INPUT_LEDGER with MSCONNECTOR_OWNED_INPUT_FD. Open the unchanged raw leaf exclusively with NOFOLLOW through the existing private-root authority, retain the FD>=3, and pass exactly that descriptor to native Popen. Keep configtest without pass_fds; strip all INPUT_ variables and preload from curl. Nested finally closes even if cleanup or fsync raises.

## Changed files

ci/runtime/lifecycle/run-nginx-common-input-fault.py and tests/test_nginx_common_input_fault_driver.py. The C fixture counterpart is a separately owned coordinated slice; no C fixture was edited here.

## Commands executed

Controlled FD tests failed before migration (exit1), then the existing pointer-driver module passed7 tests (exit0). Final current-source six-module focus58 tests/48.211s/exit0 without skips includes configtest-exception cleanup. Evidence: python-sonar-ledger-red.log, python-sonar-ledger-green.log and python-sonar-slice-final-focus-r2.log. Tests use actual file descriptors with mocked process launch, not a native process.

Independent candidate review identified a narrow acquisition-cleanup gap when the private-root context exits with an exception after ledger creation. A controlled root-context-exit test first failed (1 test, exit1: descriptor remained open). Extending the existing descriptor cleanup try around context entry/acquisition/exit closes that descriptor. RTK-wrapped Parent Python -m unittest tests.test_nginx_common_input_fault_driver -v with external TMPDIR and explicit FRAMEWORK_ROOT then passed9 tests/0.804s/exit0 without skips. This follow-up changes no pass_fds or receipt behavior and is not a demonstrated exploit.

## Security impact

Restore fixture resource integrity without expanding admitted faults, changing Common mapping or manufacturing native events. The fixture-only conditional risk is not presented as a demonstrated ordinary-CLI exploit.

## Runtime evidence

No native runtime or loaded interposer was executed for this slice. Actual inode/FD observations in unit tests prove only local producer behavior.

## Known limitations

Driver and separately owned C fixture must integrate together with the same FD environment name and constructor validation. Existing raw ledger basename, original bytes and SHA retention remain unchanged.

## Remaining risks

Fresh integrated native execution and independent source/security review are still required; unit FD tests do not prove native fault delivery.

## Checks not run and rationale

No build, native E2E, new scan, authentication/configuration mutation, Git writes or publication. Coordinator owns integration and runtime.

## Final diff and review status

Isolated uncommitted candidate reviewed for exact pass_fds, unarmed configtest and finally cleanup. Separate security record from behavior-preserving quality changes.
