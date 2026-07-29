# Change Record: Parent Common header validation and NGINX strict JSONL-tail deduplication

**Language:** English | [Deutsch](CR-20260728-sonar-common-nginx-strict-jsonl-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-common-nginx-strict-jsonl-duplication |
| Date (UTC) | 2026-07-28 |
| Base revision | 8a3872e5e63f93e202bed24e0dcbad7bdf110ede |
| Boundary | Parent Common and NGINX source, their direct source-contract checks, and this English/German Change Record pair and indexes. Framework/MRTS source and Gitlinks, workflows, scanner configuration, suppressions, exclusions, Quality Gates, and default-branch integration are unchanged. |
| Delivery status | Local candidate only at record authoring. No task commit, push, pull request, hosted SonarQube Cloud analysis, hosted-check closure, merge, or master integration exists. |

## Motivation and problem statement

The current `master` assessment identifies 630 unresolved project rows and
0.2% project duplication. Filtering to `common/` and `connectors/` gives 285
open rows. The larger HAProxy duplicate candidates parse protocol input or
enforce request-body lifecycle rules, so they are deliberately not included in
this first, narrow batch.

This candidate removes the identical private header-validator implementation
from Common request and response helpers. It also removes the 18-line Phase 3
and 18-line Phase 4 NGINX JSONL serialization/write tail. The latter paths are
not interchangeable with the existing warning-only request-event writer:
their serialization, write, and short-write failures must remain fatal to the
caller.

To make the overall issue baseline decrease as well as the duplication metric,
the candidate also resolves the existing MAJOR `c:S1854` row in
`common/runtime/http_authorization_service.c`. `decision_name` is assigned on
each path that reaches `send_response`; the only path before those assignments
returns after sending its own invalid-request response. Its initial `"error"`
store is therefore dead and is removed without changing an authorization
decision or response.

## Acceptance criteria

- Both Common validators use one private implementation without changing their
  request-only method/URI or response-only status controls.
- Invalid header names and invalid value/size combinations remain rejected;
  a NULL value with zero size remains valid.
- Phase 3 and Phase 4 share only a strict bounded JSONL tail that preserves
  their `NGX_ERROR` failure propagation and rendered diagnostics.
- The warning-only request-event JSONL helper remains warning-only and is not
  reused by the enforcement-relevant Phase 3/4 paths.
- The existing `c:S1854` initialization issue is removed without changing any
  reachable authorization-service result.
- The exact PR-head analysis must report `0 New issues`, `0.0% Duplication on
  New Code`, fewer total duplicated lines, and a lower total open-issue count
  than the recorded `master` baseline.
- Local checks, security-diff review, and the English/German record report
  observed results and limitations truthfully.

## Implementation decision and rationale

`common/src/header_validation_internal.h` contains a private `static inline`
validator. It retains the exact previous checks for a non-NULL nonempty name,
space/control/DEL/colon rejection using an unsigned-byte comparison, and the
NULL-value-only-when-size-is-zero rule. It exposes no public ABI. Request and
response helpers retain their separate surrounding validation.

`ngx_http_modsecurity_write_phase_event_jsonl` is separate from
`ngx_http_modsecurity_write_event_jsonl`. It serializes the existing metadata
only to a 4096-byte stack buffer, writes to the same configured descriptor,
and returns `NGX_ERROR` after a serialization failure, failed write, or short
write. Its only current callers pass the fixed literals `phase3` and `phase4`;
the `%s` use is a data argument, not a caller-controlled format string.

The authorization-service control flow is intentionally unchanged. All
non-returning branches assign `decision_name` before `send_response`: request
mapping failure selects `mapping_error`, runtime begin/finish failure selects
`runtime_error`, and a successful transaction derives the action name. The
dead declaration initializer is removed rather than replaced with a
suppression or a comment.

## Changed files

- common/src/header_validation_internal.h
- common/src/request_helpers.c
- common/src/response_helpers.c
- common/runtime/http_authorization_service.c
- connectors/nginx/src/ngx_http_modsecurity_common.h
- connectors/nginx/src/ngx_http_modsecurity_header_filter.c
- connectors/nginx/src/ngx_http_modsecurity_body_filter.c
- ci/checks/common/check-common-helpers.sh
- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- this English/German Change Record pair and both indexes

No Framework/MRTS source or Gitlink, workflow, Makefile, scanner setting,
suppression, exclusion, Quality Gate, or `master` branch is changed.

## Commands executed

| Command or procedure | Result |
| --- | --- |
| `make check-nginx-common-adoption` | passed. The source contract verifies the retained warning-only helper, the distinct strict helper, one bounded serialization/write tail, no body data in that helper, fixed phase callers, and propagated Phase 4 failure handling. |
| `make check-common-helpers` | passed with C17, `-Wall -Wextra -Werror`; it covers the retained Common header validation contract. |
| `make check-common-sdk-contract`, `make check-common-security-contract`, and `make check-common-flow-integrity` | passed. |
| `make check-common-memory-safety` | passed when run outside the sandbox. Its initial sandbox attempt stopped before testing because LeakSanitizer cannot operate under that tracing boundary. |
| `make check-http-authorization-service-timeout` | passed outside the sandbox with C17, `-Wall -Wextra -Werror`, configuration-error, timeout, and loopback-service controls. Its initial sandbox attempt could not reserve a loopback port. |
| `make check-nginx-c-standard-wiring` | passed. |
| `make check-nginx-c17` | blocked_external_dependency: NGINX headers/source are absent; the underlying control returns 77. No compilation success is claimed. |
| `make check-bilingual-docs` | blocked_external_dependency in the isolated worktree: the unpopulated Framework submodule makes existing Parent links unresolved. No documentation check was changed or bypassed. The scoped paired-record/link and whitespace validation passed. |

## Security impact

The focused diff review covered an HTTP-header validation boundary and an NGINX
security/audit-event write boundary. The Common helper preserves every prior
rejection condition and adds no public entry point. The strict NGINX helper
does not process header or body payloads, change the output file or descriptor,
allocate memory, or alter request/response lifecycle state. Crucially, it does
not convert a prior failure into a warning: all three failure classes still
return `NGX_ERROR`, while the unrelated warning-only request-event helper keeps
its former semantics.

The authorization-service edit is at a network authorization boundary, so its
control flow was reviewed separately. The only pre-assignment path sends the
invalid-request response and returns; each path that reaches the later response
sink assigns `decision_name`. Removing its dead initial value neither changes a
default allow/deny decision nor introduces an uninitialized reachable value.

No new plausible high- or critical-impact security finding was identified in
the changed diff. This is focused source evidence, not host-runtime evidence.

## Runtime evidence

No native NGINX/libModSecurity host runtime, connector load, request, response,
transport, service start, or allocation-fault scenario was run. The passing
NGINX check is a source-contract control. The attempted C17 control could not
start compilation because the external NGINX source/header prerequisite is
absent.

## Checks not run and rationale

- Native NGINX/libModSecurity runtime testing was not run because its host
  prerequisites are absent; it is not inferred from the source contract.
- A successful NGINX C17 compilation was not run: the exact control is blocked
  by missing external headers/source, not by a source compile diagnostic.
- Hosted SonarQube Cloud and GitHub Actions checks were not run because this
  record precedes the candidate commit, push, and Draft PR.
- Full repository bilingual-link validation cannot pass in this isolated
  checkout until its external Framework submodule content is present. The
  scoped paired-record/link validation is narrower evidence, not a replacement.

## Known limitations

The 36 NGINX duplicate lines and the Common helper clone are source-selection
evidence, not a new hosted SonarQube Cloud metric. Only the exact pushed PR
head can establish new-code duplication, Quality Gate, or issue status.

The static NGINX contract proves the intended source shape and failure
propagation but cannot prove host ABI compatibility or runtime filter ordering.

The required hosted `0 New issues`, `0.0% Duplication on New Code`, and lower
project-wide counts are acceptance gates, not yet observed results. The Draft
PR must remain open until its exact head supplies that evidence.

## Remaining risks

A native NGINX integration could expose a host ABI, descriptor, or filter-chain
interaction that source-contract testing cannot exercise. Retained caller
guards, a bounded metadata-only buffer, fixed current phase literals, and
strict error propagation reduce that risk but do not replace native testing.

No hosted delivery or analysis exists at record authoring, so this record does
not claim global duplication reduction, an issue closure, lower issue count,
or Quality Gate success.

## Final diff and review status

The local diff centralizes only the selected clones. The Common validator keeps
the former byte and size rules; NGINX Phase 3/4 callers retain event creation
and delegate only the strict write tail. The focused security-diff review found
no weakened control. Local checks named above have their observed status; the
external NGINX C17 limitation remains open. No commit, push, Draft PR, hosted
analysis, review, merge, or master integration exists at record authoring.
