# Change Record: CR-20261008-nginx-p3-technical-source

**Language:** English | [Deutsch](CR-20261008-nginx-p3-technical-source.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-p3-technical-source |
| Date (UTC) | 2026-10-08 |
| Base revision | `ec632b50d439385859113f9667fcbddb29cde357` |

## Motivation and problem statement

P3 native-return and monotonic-clock failures sealed Common technical errors but emitted no corresponding technical JSONL event. Helper-only tests did not execute the complete header-filter caller.

## Acceptance criteria

Actual full header_filter return 0/negative/undocumented native values and both clock failures must fail closed with no P3 completion or downstream forwarding, emit one exact technical event and remain idempotent on failed reinvocation. Valid over-budget return 1 emits exactly measured timing plus technical timeout. Disabled and exact-budget success complete P3 and forward once.

## Implementation decision and rationale

The new C17 fixture extracts actual full header_filter, its success dispatch and event writer, module budget helpers, technical emitter, Common begin/complete wrappers and inline JSONL writer/disposition. It links real Common transaction state/profile registry/serializer and includes the actual bounded URI helper. Lightweight NGX header enumeration/mapper plumbing, pool hooks, native return/no-pending intervention, downstream/finalize host functions, monotonic clock and fd capture are controlled seams. No Common outcome, budget decision or emitted event is supplied by fixture expectations.

A real Common transaction completes request_headers and request_body before the full P3 call. Actual state, native/host counts and actual serialized JSON are checked. Failed reinvocation executes the same full function, so missing guards cause duplicate effects to fail the assertions. Default ROOT remains the test checkout; the integration test command changes only the imported Python module property to the current coordinator checkout, without source copies or production environment features.

## Changed files

Only new tests/test_nginx_p3_technical_source.py and this EN/DE pair. Root owns caller/technical-mapper source changes; no existing source/tests or integration worktree files were changed.

## Commands executed

RTK-wrapped Framework Python loader with RUNNER_TEMP and PYTHONPYCACHEPREFIX under external roots compiles controlled C17 -Wall -Wextra -Werror and links actual Common source. After fixture declaration/enum/identity corrections, intended RED had five missing-event subcase failures; disabled/exact-budget success and measured timeout already passed. After Root caller changes, all five test methods passed (including native 0/-1/2 and both successful controls). Logs stream-c-p3-technical-red.log and stream-c-p3-technical-green.log are retained in the run analysis directory.

## Security impact

No Rule-ID is invented; technical error taxonomy is explicit. Native failure cannot be hidden by timing or become an allowed response. No failed native/clock/budget path completes Common P3, forwards headers or repeats event/native work.

## Runtime evidence

This is controlled source-bound execution, not native NGINX/Engine runtime, wire/status delivery or PASS evidence.

## Known limitations

The owned standalone checkout lacks coordinator budget/technical/URI helpers. Validation used the actual current Root source via the test-loader property override; normal integrated test invocation uses its default ROOT. Header content mapping and pending intervention classification are outside this fixture's scope.

Change Record structure and the new EN/DE pair pass. Full bilingual documentation validation remains blocked by pre-existing missing Framework-submodule link targets in this standalone worktree; no new-record violation remains. Diff whitespace checks pass.

## Remaining risks

Full native source compilation, runtime event sink behavior and actual HTTP delivery remain coordinator integration checks. The fixture captures real JSONL through a controlled fd, not a filesystem/nginx process.

## Checks not run and rationale

No native connector build, E2E or runtime slot was used. Final native runtime and fresh-head CI/Sonar remain Root-owned.

## Final diff and review status

Focused three-new-file Parent slice; no Root/source mutation, unrelated edits, Gitlink/MRTS changes or publication.
