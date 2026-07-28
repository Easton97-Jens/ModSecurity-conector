# Change Record: Parent Envoy lifecycle literal ownership for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260728-sonar-s1192-envoy-lifecycle.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-s1192-envoy-lifecycle |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Candidate designation | Parent #154 candidate. This is a local candidate designation only; no hosted pull-request state, remote-head SHA, review result, or delivery outcome is recorded. |
| Tracking | Parent SonarQube Cloud python:S1192 issue keys AZ9cRyqOHhV2CayPTPzr, AZ9cRyqOHhV2CayPTPzq, and AZ9cRyZWHhV2CayPTPwQ. Their post-change hosted states are not yet available. |
| Affected components | Envoy HTTP smoke-helper lifecycle fixture and Parent full-lifecycle evidence checker, with their focused Python contract tests. |
| Boundary | Parent-only candidate: connectors/envoy/harness/envoy_smoke_helper.py, ci/checks/evidence/check-full-lifecycle-evidence.py, their two focused tests, and this English/German Change Record pair plus its two indexes. Framework, MRTS, Gitlinks, workflows, scanner configuration, generated reports, and external issue state are unchanged. |

## Motivation and problem statement

The selected Parent files repeat three immutable literals that SonarQube Cloud
reports as python:S1192 maintainability debt: /phase4-marker, text/plain, and
events.jsonl. The repeated values are part of HTTP lifecycle fixtures and
full-lifecycle evidence loading, so the remediation must remove duplication
without changing request routing, response metadata, artifact selection, or
the existing evidence gates.

## Acceptance criteria

- Give /phase4-marker, text/plain, and events.jsonl one immutable module-level
  owner each and reuse those owners at the selected call sites.
- Preserve the Envoy helper's Phase-4 default path, marker response body, HTTP
  status, and content-type behavior.
- Preserve lifecycle-counter, artifact-profile, event-identity, and
  first-byte/no-buffer evidence validation while loading the same events.jsonl
  artifact.
- Keep the change Parent-only and retain the focused contract tests as local
  behavior evidence.
- Record the three supplied live SonarQube Cloud keys, but do not treat any as
  resolved until a fresh exact-head hosted analysis exists.
- Keep the English/German records and indexes equivalent, including all
  required Change Record headings.

## Previous and new behavior

Before the change, the selected code used repeated string literals directly:
the Envoy helper repeated /phase4-marker in routing and CLI defaults and
text/plain in response headers, while the lifecycle checker repeated
events.jsonl when loading event records for three evidence paths. The new
behavior gives these exact values the static owners PHASE4_MARKER_PATH,
TEXT_PLAIN_CONTENT_TYPE, and EVENTS_FILENAME and substitutes those owners at
the existing uses. The literals, branch predicates, function calls, protocol
values, and validation decisions remain unchanged.

## Implementation decision and rationale

The constant extraction stays within the two affected Python modules. In
connectors/envoy/harness/envoy_smoke_helper.py, PHASE4_MARKER_PATH supplies
both the upstream-handler comparison and the phase4-first-byte default, while
TEXT_PLAIN_CONTENT_TYPE supplies the three existing content-type headers. In
ci/checks/evidence/check-full-lifecycle-evidence.py, EVENTS_FILENAME supplies
the existing event-file reads in lifecycle_errors, first_byte_errors, and
no_buffer_errors.

No helper is introduced and no condition, request input, output payload, JSONL
parser, evidence-record filter, or failure path is changed. This is the
smallest literal-ownership change that can address the selected python:S1192
issues while retaining the established HTTP and evidence contracts.

## Security impact

The scoped change touches an HTTP fixture and evidence-consumer paths, so a
focused security review used this invariant: moving immutable literals must not
change the Phase-4 route, response content type, marker payload, or the strict
selection of the event artifact used by lifecycle evidence checks. The
controlled loopback request path, response headers/body, JSONL loading,
artifact-profile gate, event-identity check, and counter/error handling retain
their existing controls.

The focused review is approved: no security-relevant behavior drift and no
plausible or reportable finding was identified within this literal-extraction
scope. It is not a full Envoy deployment or repository-wide security scan, and
it does not assert a hosted SonarQube Cloud result.

## Changed files

- connectors/envoy/harness/envoy_smoke_helper.py
- ci/checks/evidence/check-full-lifecycle-evidence.py
- tests/test_envoy_transport_hardening_contract.py
- tests/test_full_lifecycle_evidence.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| Managed exact-worktree /root/git/ModSecurity-conector/.venv/bin/python -B tests/test_envoy_transport_hardening_contract.py | passed: 9/9 tests. |
| Managed exact-worktree /root/git/ModSecurity-conector/.venv/bin/python -B tests/test_full_lifecycle_evidence.py | passed: 18/18 tests. |
| git diff --check for the candidate | passed; no whitespace errors. |
| Focused security review of the scoped HTTP/evidence invariant | approved; no finding. |
| Scoped Change Record pair heading/identity/structure parity check and scoped documentation diff check | passed; performed only on this pair and the two Change Record indexes, without Framework or MRTS access. |

## Tests and actual results

| Command or check | Result |
| --- | --- |
| tests/test_envoy_transport_hardening_contract.py | passed: 9/9. The added contract verifies the phase4-first-byte default remains /phase4-marker, the response remains HTTP 200 with text/plain, and the marker body remains unchanged. |
| tests/test_full_lifecycle_evidence.py | passed: 18/18. The added contract verifies lifecycle inventory acceptance using the matching events.jsonl artifact without changing the lifecycle-counter contract. |
| Candidate git diff --check | passed; no whitespace error. |
| Scoped English/German Change Record parity and index-link review | passed; all required headings, language switches, identity fields, technical literals, and index links are present. |

## Runtime evidence

No external Envoy, xDS, ext-proc, Common/libmodsecurity, host-proxy, Framework,
or MRTS runtime evidence was generated or changed. The focused Python modules
provide source and controlled-loopback contract evidence only. In particular,
the preserved HTTP and evidence invariants are not represented as a production
runtime capability claim.

## Known limitations

The supplied local test evidence proves only the selected Parent contracts and
literal reuse. It does not prove a complete Envoy deployment, a full connector
matrix, or the absence of unrelated SonarQube Cloud findings. The three
referenced issue keys have no post-change hosted disposition in this record.

## Remaining risks

A future caller could introduce a new hard-coded equivalent literal or alter a
surrounding HTTP/evidence control outside this focused scope. The static
owners, direct contract tests, local whitespace review, and focused security
review reduce that risk, but a fresh exact-head SonarQube Cloud analysis is
still required before any listed issue is declared resolved.

## Checks not run and rationale

- Hosted pull-request checks, exact-head SonarQube Cloud analysis, Quality Gate
  evaluation, review, merge, and master integration were not available for this
  candidate and are not claimed.
- No full Envoy build, integration run, connector/runtime matrix, Framework, or
  MRTS check was run: these are outside the Parent-only literal-remediation and
  documentation scope.
- Repository-wide make check-bilingual-docs and make check-doc-links were not
  run because their configured checks inspect Framework and/or MRTS state; the
  task explicitly permits only scoped documentation parity and diff checks
  without Framework/MRTS access.

## Final diff and review status

The local Parent #154 candidate contains the scoped literal ownership change,
its focused contracts, and this paired traceability update. The supplied
exact-worktree test results, candidate whitespace review, focused security
review, and scoped documentation review passed as recorded above. No commit,
push, hosted PR check, SonarQube Cloud post-change issue state, Quality Gate,
review approval, merge, or default-branch update is claimed.
