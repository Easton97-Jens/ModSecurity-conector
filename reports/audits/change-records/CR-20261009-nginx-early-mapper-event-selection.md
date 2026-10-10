# Change Record: CR-20261009-nginx-early-mapper-event-selection

**Language:** English | [Deutsch](CR-20261009-nginx-early-mapper-event-selection.de.md)

Preserve truthful pre-mapping event metadata while selecting the exact native
protocol failure.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-early-mapper-event-selection |
| Date (UTC) | 2026-10-09 |
| Base revision | `407b647ce007daae5340cb87d2ead57f7ab4a730` |

## Motivation and problem statement

The genuine R7 NGINX lifecycle executed both Common input-fault operations but
their drivers exited 1. The real `protocol_error` records had the correct
transaction, producer, phase and classification, while `method` and `uri` were
empty because Common mapper validation failed before canonical request
metadata was recorded. The Parent selector incorrectly required `POST` and the
case path and therefore projected no protocol event.

## Acceptance criteria

Select exactly one source event with the closed producer/classification,
transaction and explicitly empty pre-mapping method/URI. Reject nonempty,
foreign, duplicate or otherwise mismatched events. Preserve the complete raw
JSONL bytes and retain the independent access, fault-ledger, configuration and
cleanup bindings. Pin the separately published compatible Framework reader at
`567d36acc010a68882462b5ffe23b9e94bff5d73`, keep MRTS at
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`, and do not change product event
emission or Required scope.

## Implementation decision and rationale

Remove the unused case-path parameter from `select_protocol_events` and match
the product's explicit early-error shape, `method == ""` and `uri == ""`.
The sealed access row, exact configured transaction, own-worker fault ledger
and cleanup event remain responsible for request/case correlation. The
Framework reader was changed and published independently in its own repository;
this Parent change records that exact compatible Gitlink.

## Changed files

`ci/runtime/lifecycle/run-nginx-common-input-fault.py`,
`tests/test_nginx_common_input_fault_driver.py`, and this English/German Change
Record pair, plus the Framework Gitlink only. MRTS is unchanged.

## Commands executed

Focused RED: one Parent selection test failed because the authentic empty event
was projected as `[]` (log SHA-256
`461c1b8193183251ed41e95b0f9137c1bef5299bfc1f663a4be8452fd60754f9`).
Focused GREEN: all 9 input-fault driver tests passed (log SHA-256
`4fc5dc5e0134547ada5ff1d3b174710981eb12804e0d87bf10178de687ee5088`).
The expanded authority, collection, dispatch, request-result, projection and
wiring set passed all 81 tests in 49.519 seconds (log SHA-256
`9bf62d552ae05062da7bde89b92b22879f4e3e37375e27b7863c6403dd8fd7f4`).
A read-only reproducer selected exactly one event for each retained R7 JSONL
without changing either raw digest (log SHA-256
`742bc003f771892d75dc9424ab7f0028f8b44407c47b08f94dc212f6ddd7ee9b`).
The native Change-Record, bilingual-documentation and link checks passed.
After the published Framework pin was installed, a deliberately long temp root
made three unrelated Unix-socket fixtures fail before their assertions (log
SHA-256 `f5aca42afed70e7e972036ebee5c9f417cc91a9bbf611e60bcd57fa6214220c7`);
this is not a source failure or pass. The unchanged retry under a short approved
external root passed all 92 tests in 31.976 seconds (log SHA-256
`abfb3ca8b01569172a21bc185a05168e4c2df884fd6e24c8d6f0d0a787381f97`).
Pre-commit `make lint` exited 0 through its final whitespace check, but nine
tests correctly skipped because committed Parent HEAD still named the old
Framework Gitlink while the worktree named the new one (log SHA-256
`4b48d52e6c1364096cc1a313612a76201c11d88891ea4e9dc2e817fac7b725dc`).
It is not the final clean-head lint proof and will be repeated after commit.

## Security impact

The change does not synthesize request metadata or weaken receipt, path,
ownership, seal, transaction, worker or cleanup checks. It narrows the accepted
event shape to the product's exact pre-mapping empty strings; nonempty or
foreign method/URI values are negative controls. Independent security review
found an evidence-contract defect, not a validated vulnerability.

## Runtime evidence

Retained R7 evidence proves HTTP 400, Root master/nobody worker, Common return
0, exact mapper diagnostic, access/fault transaction binding and cleanup for
both cases. R7 remains FAIL with supervisor/native exit 2 and no final
`result.json`; it is not relabeled or reused. No post-fix native runtime has run.

## Known limitations

Pure and sealed-fixture tests do not establish hosted runtime PASS. A new
Parent/Framework exact tuple, newly built artifacts and a fresh isolated
Root/nobody lifecycle remain required.

## Remaining risks

Any missing, altered or ambiguous access/fault/config/cleanup evidence must
continue to fail instead of borrowing the early protocol event. The fresh
clean-head build and lifecycle must also rebind every source/artifact identity.

## Checks not run and rationale

Final clean-head Parent lint, fresh build, full 97-record lifecycle, remote
CI/Sonar for the future head and protected Exact-Head were not yet run at this
checkpoint. Ruff remains unavailable and separately not run.

## Final diff and review status

Focused implementation diff and independent code/security review found no
actionable issue. The 92-test post-pin Parent focus, documentation checks and
whitespace check are green. Framework delivery was normally pushed and read
back at exact `567d36acc010a68882462b5ffe23b9e94bff5d73`, PR #137 remains
OPEN/DRAFT; Parent commit, clean-head lint and remote readback remain pending.
No amend, force-push, merge, retarget or protected dispatch occurred.
