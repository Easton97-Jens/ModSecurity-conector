# Change Record: Parent NGINX event metadata and JSONL writer deduplication corrective batch

**Language:** English | [Deutsch](CR-20260727-sonar-nginx-event-metadata-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260727-sonar-nginx-event-metadata-duplication` |
| Date (UTC) | `2026-07-27` |
| Base revision | `1b0f8825f3510b99b603bb6cd6f0777e1710358e` |
| Corrective base revision | `30bd39faf4214dd27f5fd095def71b07d97ccd3b` |
| Tracking | Exact Draft PR #144 Quality Gate failure at the corrective base: `8.6%` new-code duplication, two S1192 literal candidates (`AZ-l0E9Sjq1bd7qgEUwj` and `AZ-l0E9Sjq1bd7qgEUwk`), and a remaining 22-line JSONL serializer/write-tail clone. The local correction has no new exact-head remote result. |
| Boundary | Parent NGINX request-event metadata and JSONL writer source, its Parent source-contract checker, and this English/German Change Record pair and indexes. Framework and MRTS source and gitlinks, scanner configuration, Quality Gates, remote analysis, and delivery remain unchanged. |
| Delivery status | Draft PR #144's observed Quality Gate is failed for its earlier exact head. The local correction is unstaged; this record claims no new remote success, staging, commit, push, pull request, merge, SonarQube issue closure, or remote analysis. |

## Motivation and problem statement

The intervention-request emitter and the native rule-match emitter each
converted the same three request values: `r->method_name`, the raw URI
`r->unparsed_uri`, and `r->headers_in.content_type->value`. Source review
identified a static `22+22` duplicated-lines candidate: 22 lines in each
emitter's conversion block. This is candidate evidence, not a fresh SonarQube
Cloud duplicate count, issue disposition, or Quality-Gate result.

The bounded remediation removes only that repeated conversion while retaining
the existing event-specific decisions and JSONL write paths.

The exact Draft PR #144 Quality Gate for the corrective base
`30bd39faf4214dd27f5fd095def71b07d97ccd3b` subsequently failed with `8.6%`
new-code duplication. Its retained failure evidence is the two S1192 string
candidates `AZ-l0E9Sjq1bd7qgEUwj` and `AZ-l0E9Sjq1bd7qgEUwk` plus the remaining
22-line serializer/write-tail clone. Those facts describe the earlier remote
head; they do not evaluate the currently unstaged local correction.

## Acceptance criteria

- Share only method, raw-URI, and content-type conversion through a
  header-local helper.
- Retain the established empty-string fallbacks for absent, empty, `NULL`, and
  `(char *)-1` conversion results.
- Keep event output metadata-only; do not add request-body data to either JSONL
  event.
- Preserve intervention and rule-match identifiers, statuses, decisions,
  guards, rule-ID treatment, and existing JSONL writes.
- Record actual focused source-check results, the passed isolated C17
  compilation against the digest-bound NGINX release asset, and the absence of
  module-build and native host-runtime evidence truthfully.
- Extract only the shared JSONL serializer/write tail into a header-local
  helper while retaining caller-specific guards, event construction, diagnostic
  messages, return behavior, and warning-only short-write behavior.
- Replace the two S1192 Python literal candidates with named constants without
  suppressions, exclusions, or Quality-Gate changes.
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
`r->request_body` handling. The later writer correction moves only their
identical serialization/write tail; it does not broaden the metadata helper.

Event construction remains source-specific. The intervention emitter continues
to use `MSCONN_EVENT_REQUEST_BLOCKED`, `MSCONNECTOR_STATUS_BLOCKED`, and its
existing `wanted` action. The rule-match emitter continues to use
`MSCONN_EVENT_RULE_MATCHED`, `MSCONNECTOR_STATUS_OK`, the `"pass"` action, and
its validated `rule_id`. Their distinct guards remain intact. This is a
header-local implementation detail, not a public API or event-schema change.

### Corrective JSONL writer batch

`connectors/nginx/src/ngx_http_modsecurity_common.h` now directly includes
`msconnector/event_jsonl.h` and defines the header-local
`static ngx_inline int ngx_http_modsecurity_write_event_jsonl(...)` after the
metadata helper. It owns exactly one `char line[4096]` serialization/write
tail. It calls `msconnector_event_write_jsonl_line` once; on serialization
failure it preserves the `%s%s` warning, including the ` (truncated)` suffix,
and returns `0`. On serialization success it calculates `ngx_strlen(line)`,
calls `ngx_write_fd` once, preserves
`written < 0 || (size_t)written != line_length` and the
`written < 0 ? ngx_errno : 0` error selection, logs the supplied literal
message through `%s`, and returns `1` even for a negative or short write.

The access emitter retains its `r`/`mcf`/log-file/fd guard, context lookup,
redirect-versus-deny selection, blocked event/status, and `wanted` decision.
The native rule-match emitter retains rule-ID validation before context lookup,
its distinct guard, matched event, `"pass"` decision, and validated `rule_id`.
Each passes its existing serialization and write-failure literals to the
helper and retains `if (!ngx_http_modsecurity_write_event_jsonl(...)) return;`.
Consequently only serialization failure returns from the caller; the existing
warning-only negative/short-write behavior remains unchanged. Neither caller
now directly includes `msconnector/event_jsonl.h`, calls the serializer/writer,
or owns the local line, truncation, length, or write variables.

`ci/checks/connectors/nginx/check-nginx-common-adoption.py` replaces the two
S1192 body-counter literal candidates with `EVENT_BODY_BYTES_SEEN` and
`EVENT_BODY_BYTES_INSPECTED`. It also names the existing no-request-body
assertion `REQUEST_BODY_ACCESS` and verifies the new writer's single
serialization/write, preserved warning/return contract, metadata-only scope,
source-specific guards/messages/rule semantics, and removal of both direct
caller tails.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

The corrective batch changes no additional product path: the same three NGINX
files now contain the header-local writer and its two caller delegations, while
the existing source-contract checker covers the writer boundary and the two
S1192 constants.

## Commands executed

| Command | Result |
| --- | --- |
| `rtk proxy make check-nginx-common-adoption` | passed after the local JSONL-writer correction; it covers header ownership, one serialization/write tail, the no-body boundary, direct-tail removal, and source-specific guards/messages/rule semantics. |
| `rtk proxy make check-nginx-c-standard-wiring` | passed after the local correction. |
| `rtk proxy make check-common-helpers` | passed: `common_helper_smoke`. |
| `rtk proxy make --no-print-directory check-nginx-c17` | passed (exit `0`): `PASS: nginx_c_standards c17 compile completed` against the isolated, digest-verified NGINX `release-1.31.2` header source. All source, build, and include roots were explicit, including the trusted existing ModSecurity include root. The run used only header-only `./configure --with-compat`; it did not build, install, or start NGINX. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | passed: 14 tests in 0.036s for this correction-only update. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` | passed after this English/German C17-evidence update: bilingual documentation, repository path references, and documentation links all passed. |
| `rtk git diff --check` | passed after this English/German record and index update. |

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

The writer correction keeps the same bounded JSONL serializer and escaping
boundary: serialization failure returns before a line is written, and it adds
no request body or event field. Warning-only handling of a negative or short
`ngx_write_fd` is intentionally preserved caller behavior, not a new
availability/security claim. The focused correction review found no
refactor-introduced security candidate; the earlier non-UTF8 assurance lead
remains outside this batch.

## Runtime evidence

No native NGINX/libModSecurity host request was run. The passing focused checks
are source-contract and helper evidence only; they do not demonstrate deployed
host behavior, a rule decision, client-visible output, or transport
compatibility.

The local writer-helper checks add no host-runtime evidence. They demonstrate
only source structure and retained contracts.

The isolated C17 pass adds compile evidence only; it does not alter the
host-runtime boundary.

## Known limitations

The isolated C17 check passed against the digest-bound NGINX `release-1.31.2`
release asset retained under
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/nginx-c17`.
The asset SHA-256 `af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`
matched the fixed release digest. Header preparation was limited to
`./configure --with-compat`, with an explicit trusted existing ModSecurity
include root.

This is compilation-only evidence: it compiles the selected C sources under
C17, but does not build or link NGINX or an NGINX module, install NGINX, test
an NGINX configuration, start a service, load the connector, execute a
request or rule, or establish host, transport, or runtime compatibility.

The static source-contract checks exercise the intended helper adoption and
preserved source semantics. They complement the C17 compilation, but do not
build or run the NGINX module against a native host integration.

The passing source-contract, C-standard-wiring, and Common-helper checks do
not replace a module build or native host request.

## Remaining risks

The `22+22` figure is static candidate evidence, not proof of how a future
SonarQube Cloud analysis will classify the current diff. No new-duplicate
reduction or zero-duplication result is claimed until a remote analysis for an
exact delivery head is observed.

Draft PR #144's `8.6%` Quality-Gate failure and
`AZ-l0E9Sjq1bd7qgEUwj`/`AZ-l0E9Sjq1bd7qgEUwk` are evidence for the previous
exact head, not a current failure or success result for the local correction.
The remaining writer-tail clone and two S1192 literals were addressed locally,
but only a newly delivered exact head can establish a changed remote
duplication metric, Quality Gate, or issue disposition.

Native integration could expose a NGINX allocation or lifecycle difference not
represented by the source contracts. The retained fallback semantics and the
metadata-only scope limit that risk, but they do not replace a native
NGINX/libModSecurity runtime control.

## Checks not run and rationale

- A native NGINX/libModSecurity host-runtime request was not run. The isolated
  C17 check deliberately stopped after header-only configuration and source
  compilation; it selected no NGINX/module build or link, installation,
  service start, connector load, or request path. It is not inferred from the
  compile or source-contract checks.
- Fresh exact-head SonarQube Cloud and GitHub CI evidence was not run. It
  requires a newly delivered remote head after the local correction and must
  be read back for that exact head; the failed Draft PR #144 result is not
  reused as current evidence.
## Final diff and review status

The scoped correction retains the request-event metadata helper and empty
fallbacks, then factors only the identical JSONL serializer/write tail into a
header-local helper. Caller-specific guards, messages, returns, short-write
warnings, intervention/rule-match semantics, and metadata-only output remain
as recorded. The focused source checks and isolated C17 compilation passed at
their stated scope; module-build and native-runtime evidence remain limited as
recorded.

This record, its German companion, and their index entries are updated for
local review. The source correction and documentation changes remain unstaged
and uncommitted. No new remote success, merge, SonarQube Cloud issue closure,
new-duplicate reduction, Quality-Gate pass, or exact-head remote analysis is
claimed.
