# Change Record: Parent NGINX event metadata and JSONL writer deduplication corrective batch

**Language:** English | [Deutsch](CR-20260727-sonar-nginx-event-metadata-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260727-sonar-nginx-event-metadata-duplication` |
| Date (UTC) | `2026-07-27` |
| Base revision | `1b0f8825f3510b99b603bb6cd6f0777e1710358e` |
| Corrective base revision | `30bd39faf4214dd27f5fd095def71b07d97ccd3b` |
| Second corrective head | `116a50d0abd7c36471868e7b77d533d1a78ebda5` |
| Tracking | The earlier corrective-base Quality Gate failed with `8.6%` new-code duplication, two S1192 literal candidates (`AZ-l0E9Sjq1bd7qgEUwj` and `AZ-l0E9Sjq1bd7qgEUwk`), and a remaining 22-line JSONL serializer/write-tail clone. The exact second corrective head has observed Quality Gate `OK`, `0` new duplicated lines, and `0.0%` new-code duplication, but one new task-owned `python:S1192` issue (`AZ-l_JOYhdUH4Iu4ldmS`) at `ci/checks/connectors/nginx/check-nginx-common-adoption.py:68` for the three occurrences of `"msconnector/event_jsonl.h"`. |
| Boundary | Parent NGINX request-event metadata and JSONL writer source, its Parent source-contract checker, and this English/German Change Record pair and indexes. Framework and MRTS source and gitlinks, scanner configuration, Quality Gates, remote analysis, and delivery remain unchanged. |
| Delivery status | The exact second corrective head has the observed remote Quality Gate `OK` result above. At authoring of this third-follow-up record, the minimal checker-only correction was locally validated and staged for the authorized normal commit/Draft-PR cycle. No third corrective head had then been created or pushed, so this record claims no third-head remote success, duplication metric, SonarQube issue closure, push, or merge. |

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
head; they do not evaluate the then-local third correction.

The exact second corrective head
`116a50d0abd7c36471868e7b77d533d1a78ebda5` then received the observed
SonarQube Cloud Quality Gate `OK`, `0` new duplicated lines, and `0.0%`
new-code duplication. That same analysis opened one new task-owned
`python:S1192` issue, `AZ-l_JOYhdUH4Iu4ldmS`, at
`ci/checks/connectors/nginx/check-nginx-common-adoption.py:68`: the literal
`"msconnector/event_jsonl.h"` occurred three times. The minimal third
correction is local only; it has no third-head remote result or issue closure.

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
- Record the exact second-head Quality Gate `OK`, `0` new duplicated lines,
  `0.0%` new-code duplication, and task-owned `python:S1192`
  `AZ-l_JOYhdUH4Iu4ldmS` truthfully.
- Correct only the newly reported checker literal locally with
  `EVENT_JSONL_HEADER` in its one header-ownership assertion, without a
  suppression, exclusion, or Quality-Gate change.
- Do not claim a third-head remote success, duplication metric, SonarQube
  issue closure, push, pull request, or merge before exact-head evidence
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
caller tails. The exact second-head remote observation then reported the
separate `python:S1192` issue `AZ-l_JOYhdUH4Iu4ldmS` at line `68` for the
three `"msconnector/event_jsonl.h"` occurrences. The current minimal third
local correction defines `EVENT_JSONL_HEADER = '"msconnector/event_jsonl.h"'`
and uses that constant in the one header-ownership assertion. It removes the
three reported assertion occurrences from current local source, but does not
claim a remote third-head analysis or issue closure.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

The second corrective head changes no additional product path: the same three
NGINX files contain the header-local writer and its two caller delegations,
while the existing source-contract checker covers the writer boundary and the
two earlier S1192 constants. The current third local correction changes only
`ci/checks/connectors/nginx/check-nginx-common-adoption.py`; it adds
`EVENT_JSONL_HEADER` and uses it in the one header-ownership assertion. It
does not alter C source, the C17 source-only evidence boundary, or the NGINX
runtime scope.

## Commands executed

| Command | Result |
| --- | --- |
| `rtk proxy make check-nginx-common-adoption` | passed after the minimal third local `EVENT_JSONL_HEADER` checker correction; it covers header ownership, one serialization/write tail, the no-body boundary, direct-tail removal, and source-specific guards/messages/rule semantics. |
| `rtk proxy make check-nginx-c-standard-wiring` | passed after the local correction. |
| `rtk proxy make check-common-helpers` | passed: `common_helper_smoke`. |
| `rtk proxy make --no-print-directory check-nginx-c17` | passed (exit `0`): `PASS: nginx_c_standards c17 compile completed` against the isolated, digest-verified NGINX `release-1.31.2` header source. All source, build, and include roots were explicit, including the trusted existing ModSecurity include root. The run used only header-only `./configure --with-compat`; it did not build, install, or start NGINX. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | passed: 14 tests in 0.036s for this correction-only update. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` | passed after this English/German second-head/third-local evidence update: bilingual documentation, repository path references, and documentation links all passed. |
| `rtk git diff --check` | passed after the third local checker correction and this English/German second-head/third-local record and index update. |

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

The third correction changes only a source-contract checker literal into the
named `EVENT_JSONL_HEADER` constant. It neither reads request data nor changes
the JSONL sink, parser, serializer, allocation, event, guard, or logging
security boundary.

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

The `22+22` figure is static candidate evidence for the earlier correction,
not a prediction of a future analysis. The exact second corrective head
`116a50d0abd7c36471868e7b77d533d1a78ebda5` has observed Quality Gate `OK`,
`0` new duplicated lines, and `0.0%` new-code duplication. That evidence is
bounded to that exact remote head and does not establish a result for the
current local third correction.

The second-head analysis opened the task-owned `python:S1192`
`AZ-l_JOYhdUH4Iu4ldmS` at
`ci/checks/connectors/nginx/check-nginx-common-adoption.py:68` for three
`"msconnector/event_jsonl.h"` literals. `EVENT_JSONL_HEADER` addresses those
assertion occurrences locally, but the issue remains unclosed remotely until a
new exact third head is delivered and read back. Draft PR #144's earlier
`8.6%` failure and `AZ-l0E9Sjq1bd7qgEUwj`/`AZ-l0E9Sjq1bd7qgEUwk` remain
historical evidence for their previous exact head.

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
- Fresh third-head SonarQube Cloud and GitHub CI evidence was not run. The
  second-head Quality Gate `OK`, `0` new duplicated lines, and `0.0%` facts
  are recorded only for `116a50d0abd7c36471868e7b77d533d1a78ebda5`; at
  record authoring the third checker-only correction had not yet been
  committed or pushed and had to be read back for its own exact head. No issue
  closure is inferred from the local
  constant substitution.
## Final diff and review status

The second corrective head retains the request-event metadata helper and empty
fallbacks, then factors only the identical JSONL serializer/write tail into a
header-local helper. Caller-specific guards, messages, returns, short-write
warnings, intervention/rule-match semantics, and metadata-only output remain
as recorded. Its exact remote analysis has Quality Gate `OK`, `0` new
duplicated lines, and `0.0%` new-code duplication, while identifying the one
new checker-only `python:S1192` issue. The current third local correction only
names `EVENT_JSONL_HEADER` and uses it in the one header-ownership assertion.
The focused source checks and isolated C17 compilation passed at their stated
scope; module-build and native-runtime evidence remain limited as recorded.

This record, its German companion, and their index entries are updated for
local review. At record authoring, the third checker correction and
documentation changes were staged but uncommitted. No third corrective head,
third-head remote success or metric, SonarQube Cloud issue closure, push, or
merge is claimed by this record.
