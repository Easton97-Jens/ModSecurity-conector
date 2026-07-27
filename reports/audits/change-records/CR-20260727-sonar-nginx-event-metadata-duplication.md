# Change Record: Parent NGINX event metadata deduplication candidate remediation

**Language:** English | [Deutsch](CR-20260727-sonar-nginx-event-metadata-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260727-sonar-nginx-event-metadata-duplication` |
| Date (UTC) | `2026-07-27` |
| Base revision | `1b0f8825f3510b99b603bb6cd6f0777e1710358e` |
| Tracking | Static `22+22` duplicated-lines candidate in Parent NGINX request-event metadata conversion; no exact-head SonarQube Cloud result has been observed. |
| Boundary | Parent NGINX request-event metadata source and its Parent source-contract checker, plus this English/German Change Record pair and indexes. Framework and MRTS source and gitlinks, scanner configuration, Quality Gates, remote analysis, and delivery remain unchanged. |
| Delivery status | This record itself claims no staging, commit, push, pull request, merge, SonarQube issue closure, or remote analysis. Draft delivery and exact-head verification are separate pending lifecycle steps. |

## Motivation and problem statement

The intervention-request emitter and the native rule-match emitter each
converted the same three request values: `r->method_name`, the raw URI
`r->unparsed_uri`, and `r->headers_in.content_type->value`. Source review
identified a static `22+22` duplicated-lines candidate: 22 lines in each
emitter's conversion block. This is candidate evidence, not a fresh SonarQube
Cloud duplicate count, issue disposition, or Quality-Gate result.

The bounded remediation removes only that repeated conversion while retaining
the existing event-specific decisions and JSONL write paths.

## Acceptance criteria

- Share only method, raw-URI, and content-type conversion through a
  header-local helper.
- Retain the established empty-string fallbacks for absent, empty, `NULL`, and
  `(char *)-1` conversion results.
- Keep event output metadata-only; do not add request-body data to either JSONL
  event.
- Preserve intervention and rule-match identifiers, statuses, decisions,
  guards, rule-ID treatment, and existing JSONL writes.
- Record actual focused source-check results, the blocked C17 host compilation,
  and the absence of native host-runtime evidence truthfully.
- Do not claim a SonarQube Cloud duplicate reduction, issue resolution, Quality
  Gate, remote analysis, pull request, or merge before exact-head evidence
  exists.

## Implementation decision and rationale

`connectors/nginx/src/ngx_http_modsecurity_common.h` now contains the
header-local `ngx_http_modsecurity_event_request_metadata_t` and the private
`static ngx_inline ngx_http_modsecurity_event_request_metadata(...)` helper.
It initializes all three fields to `""`, returns those fallbacks for `r ==
NULL`, converts nonempty NGINX strings with `ngx_str_to_char`, and accepts a
converted value only when it is neither `NULL` nor `(char *)-1`. The content
type remains conditional on a present, nonempty
`r->headers_in.content_type->value`.

The access/intervention emitter and native rule-match emitter call the helper
only for `event.request.method`, `event.request.uri`, and
`event.body.content_type`. The shared output is therefore metadata-only:
neither emitter adds `event.body.bytes_seen`, `event.body.bytes_inspected`, or
`r->request_body` handling. Both retain their existing
`msconnector_event_write_jsonl_line` and `ngx_write_fd` JSONL write paths.

Event construction remains source-specific. The intervention emitter continues
to use `MSCONN_EVENT_REQUEST_BLOCKED`, `MSCONNECTOR_STATUS_BLOCKED`, and its
existing `wanted` action. The rule-match emitter continues to use
`MSCONN_EVENT_RULE_MATCHED`, `MSCONNECTOR_STATUS_OK`, the `"pass"` action, and
its validated `rule_id`. Their distinct guards remain intact. This is a
header-local implementation detail, not a public API or event-schema change.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| `rtk proxy make check-nginx-common-adoption` | passed, including the fallback/adoption, metadata-only request-body exclusion, source-specific semantics, and JSONL-write contracts. |
| `rtk proxy make check-nginx-c-standard-wiring` | passed. |
| `rtk proxy make check-common-helpers` | passed: `common_helper_smoke`. |
| `rtk proxy env BUILD_ROOT=<task-owned external build root> make check-nginx-c17` | blocked: NGINX headers/source are unavailable; the inner check exited 77 and `make` exited 2, so this is not a C17 compilation pass. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | passed: 14 tests in 0.033s. |
| `rtk proxy make check-bilingual-docs check-doc-links` | passed after read-only initialization of the Parent-pinned Framework Gitlink; Framework status remained clean. |
| `rtk git diff --check` | passed after the English/German Change Record pair and index entries were added. |

## Security impact

Request method, raw URI, and content type are request-derived metadata, so the
existing logging boundary was assessed. The helper retains the old missing,
empty, `NULL`, and `(char *)-1` fallbacks and adds no parser, allocation
policy, request-body capture, event field, or sink. The source-contract
controls preserve the metadata-only boundary and source-specific event
semantics. No security control was weakened, and this record does not create,
close, or resolve a security or SonarQube Cloud issue.

An independent focused security review found no candidate regression caused by
this metadata-only refactor. A pre-existing, unvalidated non-UTF8 assurance
lead remains outside the changed scope and is not presented as a finding or
remediation result.

## Runtime evidence

No native NGINX/libModSecurity host request was run. The passing focused checks
are source-contract and helper evidence only; they do not demonstrate deployed
host behavior, a rule decision, client-visible output, or transport
compatibility.

## Known limitations

The C17 host compilation is blocked because this environment does not provide
the required NGINX headers/source. The inner checker exited 77 and the Make
target exited 2; neither result is treated as a compilation pass. The exact
empty task-owned temporary build directories used for that attempt were
removed, so no external build artifact is retained.

The static source-contract checks exercise the intended helper adoption and
preserved source semantics, but do not compile or run the NGINX module against
a native host integration.

## Remaining risks

The `22+22` figure is static candidate evidence, not proof of how a future
SonarQube Cloud analysis will classify the current diff. No new-duplicate
reduction or zero-duplication result is claimed until a remote analysis for an
exact delivery head is observed.

Native integration could expose a NGINX allocation or lifecycle difference not
represented by the source contracts. The retained fallback semantics and the
metadata-only scope limit that risk, but they do not replace a native
NGINX/libModSecurity runtime control.

## Checks not run and rationale

- A native NGINX/libModSecurity host-runtime request was not run because this
  task environment lacks the NGINX headers/source and a compatible host
  integration. It is not inferred from the source-contract checks.
- Fresh exact-head SonarQube Cloud and GitHub CI evidence was not run. It
  requires a delivered remote head and must be read back for that exact head;
  no remote result is asserted here.

## Final diff and review status

The scoped source change shares only request-event metadata conversion and
retains empty fallbacks, metadata-only JSONL output, and source-specific
intervention and rule-match semantics. The focused source checks recorded
above passed at their stated scope; C17 host compilation and native runtime
remain limited as recorded.

This record and its German companion were validated locally with their index
entries before any delivery step. No merge, SonarQube Cloud issue closure,
new-duplicate reduction, Quality-Gate result, or exact-head remote analysis is
claimed.
