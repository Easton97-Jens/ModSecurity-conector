# Change Record: Parent HAProxy SPOE header-parser deduplication and SonarQube Cloud reliability remediation

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-spop-header-parser-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-spop-header-parser-duplication |
| Date (UTC) | 2026-07-29 |
| Base revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Tracking | Four current SonarQube Cloud `c:S1854` findings in `handle_connection(...)`, two current duplication blocks (82 lines) in `parse_notify_payload(...)`, and four `c:S134` nesting findings reported on this Draft PR's first delivery head. |
| Boundary | Parent HAProxy diagnostic-runtime source, one Parent reliability-contract test, and this English/German Change Record pair with its paired indexes. Framework, MRTS, Gitlinks, workflows, Sonar configuration, Quality Gates, suppressions, and `master` are unchanged. |
| Delivery status | A Draft Parent PR is the intended delivery. This record claims only observed local checks and does not claim hosted CI, a hosted Quality Gate, an external issue closure, or a merge. |

## Motivation and problem statement

`parse_notify_payload(...)` contained four structurally duplicated branches for
binary and textual request/response header arguments. The branches had to keep
their typed-value bounds, parse-failure behavior, header ownership, and
response-role semantics in lockstep. SonarQube Cloud also reports four `c:S1854`
dead assignments in the same runtime: an unused initial diagnostic pointer and
three values that were set but never read after body truncation or a transaction
cache failure.

The current master duplication service reports two source duplication blocks in
this file, totalling 82 lines. They are exactly the repeated header branches;
the follow-up intentionally reduces that shared production code instead of
changing Sonar configuration or introducing exclusions. The first Draft-PR
analysis confirmed the duplicate-line reduction but reported four new
`c:S134` nesting findings around the retained header dispatch. This follow-up
removes that nesting without changing parser semantics.

## Acceptance criteria

- The four header argument branches delegate to two bounded helpers without
  changing accepted typed values, parser position, response role, or failure
  propagation.
- Temporary textual-header ownership is freed on every non-transfer path and
  only transferred after a successful replacement decision.
- The four reported unread diagnostic assignments are removed without
  weakening body limits, transaction cleanup, fail-open/fail-closed selection,
  or ACK construction.
- A persistent C17 harness covers binary and text header helpers for both
  request and response roles, including a response-key non-byte value.
- Local checks pass; a fresh exact-head SonarQube Cloud analysis must still
  prove zero new issues, zero new-code duplication, and a lower total duplicate
  count before this candidate can be called hosted-verified.

## Implementation decision and rationale

`parse_notify_headers_bin(...)` centralizes the bounded typed-byte read and the
binary header parser. `parse_notify_headers_text(...)` uses the same bounded
reader, preserves the existing temporary `notify_request` parse, and transfers
its allocated header array only when it is non-empty and not smaller than the
already parsed header list. Both helpers set `is_response` after the typed value
has been consumed, which deliberately preserves the previous response-key
behavior for a syntactically valid but non-byte typed value.

`parse_notify_header_argument(...)` is the flat dispatcher for exactly the four
header keys. It returns the selected helper's result, returns `1` for an
unrelated key so that the existing payload parser handles it, and propagates
`-1` for malformed header data. This replaces the four nested call-site
branches that produced the new `c:S134` findings.

The former `reason` strings that were only assigned for body truncation or a
transaction-cache failure had no observer. The refactor removes only those
unread assignments. Error-specific reasons remain scoped to the two
ModSecurity-failure branches where `runtime_init_decision(...)` consumes them.

## Changed files

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — two bounded
  header parser helpers, a flat four-key dispatcher, four call-site
  replacements, and removal of four unread assignments.
- `tests/test_sonar_reliability_contract.py` — persistent C17 source harness
  for binary/text header handling and response-role preservation.
- `reports/audits/change-records/CR-20260729-sonar-haproxy-spop-header-parser-duplication.md`
  and `.de.md` — this bilingual Change Record pair.
- `reports/audits/change-records/README.md` and `README.de.md` — paired index
  entries.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| Focused `unittest` method `test_haproxy_append_string_runtime_boundaries` | passed; the C17 harness compiles and executes the actual HAProxy diagnostic runtime, including all four binary/text dispatcher keys and the non-byte response-key control. |
| `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | passed. |
| `ci/checks/connectors/haproxy/check-haproxy-c-standard-wiring.py` | passed. |
| `make check-haproxy-c17-lint` | passed; the mandatory C17 compile completed. |
| `git diff --check` | passed. |
| `make check-bilingual-docs` | blocked_external_dependency after validating this Change Record pair: the isolated worktree has no initialized Parent-pinned Framework checkout, so 20 pre-existing cross-repository documentation links are absent. |
| Focused Codex Security diff scan | passed with zero reportable findings; the full parser source and supporting test were reviewed, and the C17 harness supplied direct regression evidence. |
| Follow-up Codex Security diff scan for the flat dispatcher | passed with zero reportable findings; the scan is sealed at `/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/dbbc9c6-local-patch-20260729T045029Z/report.md`. |

## Security impact

The modified code consumes HTTP-derived, untrusted SPOE payload values. The
helpers retain `read_typed_bytes_ref(...)` as the sole typed-value boundary,
preserve `-1` parse failures, and avoid replacing headers until a fully parsed
temporary list qualifies. The response marker remains true for response header
keys even when the typed argument is not a string or binary value, matching the
pre-refactor behavior. No authentication, authorization, process privilege,
network listener, scanner, or Quality Gate control is relaxed.

## Runtime evidence

The focused C17 harness compiles and executes the actual HAProxy diagnostic
runtime translation unit. It routes all four binary/text request/response keys
through the production dispatcher, asserts the consumed parser position and
header flags, and retains the old response-key behavior for a non-byte
argument. This is direct source execution evidence, not an end-to-end HAProxy
deployment.

The canonical focused scan reports are retained outside the Git worktree at
`/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/dbbc9c6-local-patch-20260729T042755Z/report.md`
and the dispatcher follow-up report at
`/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/dbbc9c6-local-patch-20260729T045029Z/report.md`.

## Known limitations

- The C17 harness is direct source execution, not a live HAProxy plus
  libmodsecurity integration run.
- The full `tests/test_sonar_reliability_contract.py` module has a separately
  reproducible current-master failure in the unchanged Traefik optional-text
  harness; it is not attributed to this HAProxy patch.
- `make check-bilingual-docs` recognizes this English/German pair but is
  blocked by 20 cross-repository links because this isolated Parent worktree
  intentionally has no initialized Framework checkout.

## Remaining risks

- Hosted GitHub checks and a fresh exact-head SonarQube Cloud analysis remain
  required for any claim that the four external findings and 82 source duplicate
  lines are closed on the delivery head.

## Checks not run and rationale

No live HAProxy plus libmodsecurity integration run or full connector matrix
was run because this focused Sonar remediation has a bounded native harness and
the required external runtime fixtures are not present in this worktree. The
complete reliability-contract module was run and failed only in the unchanged
Traefik optional-text harness; the same individual test fails on current
`master`, so it is recorded as a baseline failure rather than suppressed or
attributed to this patch. Hosted CI and SonarQube Cloud have not yet run on a
delivery head.

## Final diff and review status

The candidate is confined to the Parent HAProxy connector and its focused test
plus bilingual traceability. It reduces confirmed existing duplication and
confirmed existing Sonar findings together. The final diff has no whitespace
errors, and the local C17, HAProxy adoption, and HAProxy standards checks pass.
No merge is authorized or claimed.
