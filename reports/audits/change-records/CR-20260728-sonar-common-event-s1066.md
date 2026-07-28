# Change Record: Parent Common event provenance short-circuit refactor for SonarQube Cloud c:S1066

**Language:** English | [Deutsch](CR-20260728-sonar-common-event-s1066.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-common-event-s1066 |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Tracking | SonarQube Cloud issue `AZ9cRy9OHhV2CayPTP4Z`, rule `c:S1066`, at `common/src/event.c:547`. The task context identifies PR #153 as the candidate; no hosted issue, Quality Gate, workflow, review, or exact-head result is claimed here. |
| Boundary | Parent `common` event-JSON provenance serialization and its focused Common-helper smoke assertions, plus this English/German Change Record pair and the two Change Record indexes. This documentation task does not access or modify Framework, MRTS, Gitlinks, workflows, scanner policy, generated artifacts, or hosted PR state. |

## Motivation and problem statement

The reported `c:S1066` issue identifies a nested conditional at
`common/src/event.c:547`. The outer `protocol_present` guard previously
surrounded the existing protocol-append failure chain. The candidate removes
only that redundant nesting; the event JSON provenance fragment must still
avoid emitting a partial result when one of its append helpers fails.

This is a maintainability refactor at an audit/provenance boundary. It must
preserve the established omission behavior when protocol data is absent and
the established fail-closed cleanup when a protocol append cannot complete.

## Acceptance criteria

- The `protocol_present` guard and the complete existing append-failure chain
  remain semantically equivalent through C short-circuit evaluation.
- When no protocol provenance is present, no protocol append helper is
  evaluated and no protocol provenance field is emitted.
- When protocol provenance is present, the append calls retain their ordering;
  any failed append still sets `was_truncated` and clears `provenance_json`.
- The focused smoke retains a no-protocol negative control and a populated
  protocol-provenance control, including `requested_protocol` and
  `connection_reused` assertions.
- The English/German Change Record pair and both indexes accurately retain the
  local evidence while treating hosted SonarQube Cloud and PR evidence as
  pending.

## Implementation decision and rationale

The candidate changes the nested form to one condition:

```c
if (protocol_present && (/* unchanged append-failure OR chain */)) {
    was_truncated = 1;
    provenance_json[0] = '\0';
}
```

In C, `&&` does not evaluate the right-hand side when `protocol_present` is
false. This is the same no-append behavior as the former outer `if`. When it
is true, the unchanged parenthesized `||` chain invokes the same
`append_protocol_string` and `append_protocol_bool` calls in the same order
and retains their existing short-circuit-on-failure behavior. A failure still
executes the unchanged fail-closed cleanup rather than publishing a partial
protocol provenance fragment.

The refactor does not change `protocol_present`, either append helper, field
ordering, existing empty-string omission, or the surrounding event JSON
writer. The smoke adds direct assertions for absent protocol fields in the
negative control and expected fields in the populated control.

## Security impact

Protocol provenance is serialized into an event/audit JSON fragment. The
existing safeguards remain intact: the `protocol_present` gate suppresses the
protocol fragment when it is absent, the append helpers retain their existing
validation and capacity-failure behavior, and a failed append marks the event
as truncated while clearing the whole protocol provenance fragment. No new
input, sink, trust boundary, suppression, or security control is introduced
or weakened by this control-flow-only refactor.

This record does not claim a newly validated security finding or a hosted
security result. It records the candidate's preserved fail-closed behavior and
the available focused source-level evidence only.

## Changed files

- `common/src/event.c`
- `ci/checks/common/check-common-helpers.sh`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260728-sonar-common-event-s1066.md`
- `reports/audits/change-records/CR-20260728-sonar-common-event-s1066.de.md`

## Commands executed

| Command | Actual result |
| --- | --- |
| `make check-common-sdk-contract check-common-security-contract check-common-flow-integrity` using `/root/git/ModSecurity-conector/.venv/bin/python` | passed, as observed by the main agent. |
| `make CC=gcc check-common-helpers-c17` | passed, as observed by the main agent; it matches the supplied GCC C17 Common-helper worker result. |
| `make CC=clang check-common-helpers-c17` | passed, as observed by the main agent; it matches the supplied Clang C17 Common-helper worker result. |
| `git diff --check` | passed, as observed by the main agent and re-run through `rtk proxy -- git diff --check` for this documentation update. |

## Tests and actual results

| Command or control | Result |
| --- | --- |
| Main-agent Common SDK/security/flow contracts and GCC/Clang C17 Common-helper smokes | passed; their individual commands and outcomes are recorded above. This documentation-only scope did not re-run the source-validation commands. |
| Narrow English/German record-parity and index-link review | passed: both companions contain the same Change ID, base revision, Sonar issue ID, rule, source location, validation boundary, and hosted-evidence limitation; both indexes link to their matching companion. |
| `rtk proxy -- git diff --no-index --check` for each new record against `/dev/null` | no whitespace error was reported. Exit `1` is expected because each command compares a new file with `/dev/null`. |

## Runtime evidence

No connector, host, Framework, or MRTS runtime was started. The Common-helper
smokes are focused source/build evidence; they do not establish deployment or
host-runtime compatibility.

## Checks not run and rationale

- The GCC and Clang Common-helper smokes were not re-run by this
  documentation-only task; their passed status is recorded as supplied
  observed candidate evidence.
- Repository-wide bilingual-documentation and documentation-link checks were
  not run because the current task permits only narrow documentation/diff
  validation that does not access or modify Framework or MRTS.
- Hosted SonarQube Cloud issue/Quality-Gate readback, PR workflows, review
  state, and exact-head verification remain pending external evidence for PR
  #153 and were not queried by this task.
- Full connector builds, runtime matrices, Framework checks, MRTS checks, and
  a broad security scan are outside this focused control-flow and
  documentation scope.

## Known limitations

This record has no hosted exact-head SHA, SonarQube Cloud Quality Gate, PR
workflow, or review evidence. It also does not claim a full connector or
deployment runtime result. The local evidence is limited to the main-agent
Common SDK/security/flow contracts and GCC/Clang C17 Common-helper smokes,
scoped source review, record parity, and the whitespace check.

## Remaining risks

The source change is deliberately small, but a later modification to the
append chain could alter its error ordering or short-circuit behavior. The
negative and populated-protocol smoke controls, scoped diff review, and
preserved cleanup reduce that risk. A fresh hosted analysis for the exact PR
head is still required before `AZ9cRy9OHhV2CayPTP4Z` is treated as resolved or
PR #153 is presented as verified.

## Final diff and review status

The scoped source diff merges only the nested condition and preserves the
existing failure body. The helper-smoke changes document both absence and
presence controls for protocol provenance. This English/German record pair,
its two indexes, and `git diff --check` received the narrow local review
recorded above. Hosted SonarQube Cloud and PR evidence remains pending; no
staging, commit, push, PR update, merge, or `master` action was performed by
this documentation task.
