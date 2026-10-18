# Change Record: CR-20261018-i12-traefik-preallocation

**Language:** English | [Deutsch](CR-20261018-i12-traefik-preallocation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-traefik-preallocation |
| Date (UTC) | 2026-10-18 |
| Base revision | `a311c725c44a7a4da95acb1a4818f66bd56c462a` |

## Motivation and problem statement

An original HTTP-parser rejection can occur before a native transaction exists. Applying the normal lifecycle's mandatory transaction ID, phase and Free observations to that path would require fabricated calls. Separately, parser exit 1 alone could incorrectly accept an unrelated loader failure as a named configuration rejection.

## Acceptance criteria

Preserve every original ID and all 35 normal lifecycle observation fields. Add a separate scope only for exact original Traefik parser, NULL-input, early mapping/begin cleanup and sink-open requirements with independently approved nonallocation contracts. Never count this scope as a full native lifecycle. Require physical client bytes, independent early-header backend exclusion, active native instrumentation, zero allocation and healthy controls, source/image/config/run/UID identity, and actual cleanup. Rejected configuration cases require the expected source-bound diagnostic and first cause in addition to the exact exit and signal contract.

## Implementation decision and rationale

The existing ledger is the sole qualifier. Its ordinary `host_http` measurement rules and ALWAYS_APPLICABLE set are unchanged. `host_preallocation_control` is restricted to the eight parser IDs, four NULL-input IDs, six early-mapping/begin cleanup IDs and three sink-open IDs across their original applicable Traefik routes. Eligibility alone never qualifies an execution.

Root approval binds the exact original contract digest and effective independent oracle. Native phase stays null in that effective oracle; original expectations remain unchanged. Unallocated transaction, phase, EOS, Finish and Free observations stay null with reasons. Actual native/runtime API returns are retained and must match the target observer stream exactly, including an empty list when no API call occurred. Separately derived native SDK constructor attempts and successful allocations remain distinct counters. Every prescribed observation field remains present.

Selectors bind existing physical JSON fields or exact JSONL lines; they do not create producer measurements. Native observer records must show activation, uninterrupted per-process sequence, valid identity and terminal coverage. Before/after controls require actual native allocation and cleanup, successful client responses and independently logged backend headers. HTTP/parser/mapping controls share the live native process. A constructor failing before its listener starts uses an admitted fault process and separately healthy processes with identical loaded image/observer hashes.

Raw malformed requests must exercise their exact original header case. Raw responses bind status, entity bytes/hash and framing; a second response cannot pass. Independent backend header-arrival records are examined before body completion. NULL-pointer paths require actual pointer/count measurements and real API returns. Native setup result 1 is not a failure result; the independently observed runtime-begin return is required. API errno stays explicitly absent. Sink-open controls require an actual failing open syscall/errno and the failed process exit/diagnostic. Run cleanup records must account for descriptors, sockets, processes and one cleanup operation; native Finish/Free are never invented.

Configuration rejection now binds a separately reviewed diagnostic and first-cause source to the exact original contract/oracle. A genuine exit 1 with a different cause cannot PASS. Accepted configuration behavior remains unchanged.

## Changed files

- `ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py`: the additional bounded scope, physical bindings, scope accounting and strict configuration rejection.
- `tests/test_i12_traefik_preallocation.py`: producer-shaped positive and tamper controls, all eight parser identities, startup/control-process distinction and ledger counting.
- `tests/test_i12_lifecycle_ledger.py`: rejected-parser controls now carry the independently bound diagnostic/first cause.
- This EN/DE Change Record pair.

## Commands executed

All shell commands used RTK and the Parent virtual environment. The combined command was `rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_i12_traefik_preallocation tests.test_i12_lifecycle_ledger tests.test_i12_traefik_absence_oracles tests.test_i12_oracle_reconciliation`. With `tests.test_bilingual_docs tests.test_change_record` added, 101 tests passed in 3.187 seconds. The external task receipt `preallocation/unit-final-v2-20261018.json` retains the exact command, source hashes and zero host/ID-promotion counters. Change Record structure, AST syntax for three Python files, `git diff --check` and RTK verification passed separately.

## Security impact

Normal lifecycle requirements, UID 65534, physical-reference verification and original catalog integrity remain enforced. This patch grants no runtime admission, does not change product code and does not modify isolation or Sonar state. Missing or contradictory source/observer/client/backend/cleanup evidence fails qualification.

## Runtime evidence

The unit fixtures model existing physical producer formats and are explicitly synthetic. They validate qualifier decisions; they are not new host exchanges or qualified original cases. Actual new host receipts, independent oracle reconciliation and Root review are required before an original ID can enter the new scope.

## Known limitations

The preallocation response decoder accepts complete Content-Length or close-delimited entity bytes. Transfer-Encoding responses require an independently supported entity decoder and currently fail qualification. An empty observer file cannot prove nonallocation. A startup failure without admitted instrumentation cannot use this scope. Only fully established matching preallocation controls receive PASS; incomplete or mismatched controls remain unqualified rather than gaining a lifecycle claim.

## Remaining risks

Fresh real host executions may expose missing producer observations. They must be added physically and reviewed; packet metadata cannot substitute for them. Final hosted checks still need the published integrated head.

## Checks not run and rationale

No host process, scanner upload, Git publication or original-ID promotion is performed by this qualifier change. Integrated host producers and final hosted acceptance belong to the parent task.

## Final diff and review status

The ordinary lifecycle path remains intact. Separate-scope dispatch and summary tests verify that preallocation PASS contributes to applicable original-case qualification while full lifecycle counts stay unchanged. Independent final review passed after correcting the latest native pointer-result binding and rejecting malformed response Content-Length values; its separate 26 focused controls passed. Integration and real-host acceptance remain owned by the parent task.

Integration with the published exact-parser-exit repair preserves independently reviewed POSIX rejection exits from 1 through 255. The incoming exit-255 regression now supplies the same mandatory diagnostic/first-cause binding as the exit-1 control. The initial integrated test failure is retained separately; no exit is normalized and no source requirement removed.
