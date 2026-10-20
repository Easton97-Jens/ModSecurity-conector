# Change Record: CR-20261020-request-body-retained-telemetry

**Language:** English | [Deutsch](CR-20261020-request-body-retained-telemetry.de.md)

Request telemetry separates offered bytes from the SDK-retained prefix and unproven inspection.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261020-request-body-retained-telemetry |
| Date (UTC) | 2026-10-20 |
| Base revision | `12cc380c3749fd76c246c05ce479f51446127880` |

## Motivation and problem statement

Traefik forwardAuth Request-v20 offered chunks of 8 and 9 bytes. ProcessPartial retained 16 bytes, allowed the request, and emitted no body-limit event. Reject retained 8 bytes but reported 17 inspected bytes and no truncation. Common counted offered append bytes as inspected and never updated request limit metadata.

## Acceptance criteria

Record offered and SDK-retained bytes separately, never infer inspection from retention, preserve native statuses and decisions, emit non-disruptive ProcessPartial evidence only from native append `0`, and propagate technical/accessor/sink errors. Genuine SDK boundary and negative tests must pass.

## Implementation decision and rationale

Read `msc_get_request_body_length` under the existing native operation lock. Append `bytes_retained` to the progress structure, preserving existing member offsets; consumers must rebuild with the updated C header. Keep request `bytes_inspected=0` as unknown/unproven, including after successful P2/EOS: the disabled-access control retains all 17 bytes too. Reject and ProcessPartial retain native behavior; partial telemetry does not request denial. Reject telemetry records truncation and the native outcome. An impossible accessor length fails the transaction. Response semantics and wire/event field schemas remain unchanged.

## Changed files

`common/runtime/msconnector_runtime.c`, `common/runtime/msconnector_runtime.h`, `tests/request_body_telemetry_test.c`, `tests/engine_response_limit_test.c`, `tests/engine_http_request_stream_test.c`, `tests/test_engine_response_limits.py`, `tests/test_native_api_fail_closed_contract.py`, `tests/test_i09_body_phase.py`, `docs/body-inspection-review-matrix.md`, its German companion, and this Change Record pair.

## Commands executed

All commands used `rtk proxy`. Genuine engine/native API/snapshot/Traefik P2/adapter regression suite: 41 tests passed. The focused telemetry test covers Reject, ProcessPartial, full body, disabled access, impossible accessor length, failed P2, and sink failure; all seven scenarios also passed ASan/UBSan. The original accounting assertion failed before repair. `make check-common-sdk-contract check-common-security-contract check-common-flow-integrity check-i10-common-callers PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` passed (11 I10 tests); `make check-common-memory-safety` and `make check-i09-native-routes` (33 tests) passed. Change Record structure and bilingual pairs/changed links passed. Full documentation checks encountered only missing baseline Framework targets in this uninitialized worktree; final integrated checks remain required.

## Security impact

Prevents false inspection claims and keeps native policy rejection distinct from technical failure. No limits, authentication, isolation, or validation controls are weakened. New partial-event write failures propagate instead of becoming successful authorization.

## Runtime evidence

Original evidence remains in run `i12-traefik-acceptance-20261015`, Request-v20 attempt `attempt-1792515659749428431`. This patch ran genuine libModSecurity/C runtime tests, including existing MRC1 and HTTP authorization streaming tests. It did not execute a new Traefik host run and does not qualify an I12 ID by itself.

## Known limitations

The public SDK C API does not reveal whether retained request bytes were semantically inspected. Zero inspected bytes means unknown, not disabled inspection. Full inspection claims still require independently bound native rule/source/runtime evidence. BodyAccess mismatch alone is not a body-limit signal. Response accounting is unchanged.

## Remaining risks

Fresh Traefik host evidence must use rebuilt binaries and newly sealed producer inputs. Existing C binary consumers must rebuild; no stable binary ABI compatibility is claimed for the enlarged progress/snapshot structures.

## Checks not run and rationale

Fresh Traefik hosts, Go race/vet, current-head remote CI, and Sonar readback belong to the integrating Traefik acceptance task. This focused patch contains no Go changes and introduces no SDK/C++ bridge.

## Final diff and review status

Focused runtime, tests, and bilingual documentation only. No Framework/MRTS, central matrix/generator, host producer, dependency, or master change. Delivery through #382 is authorized; integration through #410/#413 and final host validation remain separate.
