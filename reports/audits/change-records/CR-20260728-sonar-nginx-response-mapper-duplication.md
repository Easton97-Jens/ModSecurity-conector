# Change Record: Parent NGINX response-mapper validation-tail deduplication

**Language:** English | [Deutsch](CR-20260728-sonar-nginx-response-mapper-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-nginx-response-mapper-duplication |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Boundary | Parent NGINX response-mapper/filter source and source-contract checker, plus this English/German Change Record pair and indexes. Framework and MRTS source and Gitlinks, workflows, scanner configuration, suppressions, exclusions, Quality Gates, and default-branch integration are unchanged. |
| Delivery status | Local candidate only. No task commit, push, pull request, hosted SonarQube Cloud analysis, hosted check closure, Ready-for-review action, merge, or master integration exists at record authoring. |

## Motivation and problem statement

The current Parent duplication assessment identified the common response-mapper
validation tail in two distinct NGINX filter paths: 18 lines in the body path
and 18 lines in the header path, for 36 Parent duplicate lines. The shared
tail initializes a response-mapper contract, calls the existing mapper, and
emits a warning when mapping cannot validate.

The callers are not semantically interchangeable. The body path has a
once-per-response gate, while the header path remains eligible in its existing
header-filter path and must keep its own ordering. This candidate extracts
only the common tail; it does not turn a local warning into a filter failure
and does not claim a new hosted metric or issue closure.

## Acceptance criteria

- One internal NGINX mapper helper owns only the shared contract-init/map/fixed
  warning tail and has a void, nonfatal interface.
- A compile-time header/body enum selects the existing fixed warning context;
  no caller-provided diagnostic string or new error-propagation path is added.
- The body once gate, header eligibility/order, existing caller guards, and
  caller-owned state transitions remain local to their filters.
- No header, body, filter-chain, allocation, or response-mapper behavior is
  intentionally changed by this source-level extraction.
- The focused adoption check and scoped whitespace check record their actual
  passing results. The C17 control is recorded as blocked, not as a compiler
  pass.
- The English/German Change Record pair and indexes state local-only delivery
  and runtime limitations truthfully.

## Implementation decision and rationale

The internal mapper surface declares
ngx_http_modsecurity_validate_response_mapper as a void helper and declares
ngx_http_modsecurity_response_mapper_diagnostic_t with the compile-time values
NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER and
NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY. The helper owns the
existing stack-local response-mapper contract, mapped-response value, and
mapper-error buffer. It calls the existing
ngx_http_modsecurity_map_response_from_ctx exactly once.

On successful mapping, the helper returns normally. On unsuccessful mapping,
the enum chooses one of the two existing fixed header/body warning formats,
emits NGX_LOG_WARN, and returns without an error result. The helper introduces
neither a caller-controlled format string nor a new fatal filter result.

The body caller retains ctx->common_response_validated as its once gate before
the helper, calls the helper after its existing null-context and intervention
guards, sets the flag after the attempt, and returns NGX_OK. The header caller
retains its existing null-context and intervention guards, calls the helper on
its existing eligible path, sets ctx->common_response_validated after the
attempt, and retains its processed-state ordering. It does not receive a once
gate.

The helper does not change mapper inputs or output contracts and does not own
header/body data, filter-chain control, allocation, enforcement, intervention,
processed-state, or caller lifecycle state.

## Changed files

- connectors/nginx/src/ngx_http_modsecurity_mapper.c
- connectors/nginx/src/ngx_http_modsecurity_mapper.h
- connectors/nginx/src/ngx_http_modsecurity_body_filter.c
- connectors/nginx/src/ngx_http_modsecurity_header_filter.c
- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- reports/audits/change-records/CR-20260728-sonar-nginx-response-mapper-duplication.md
- reports/audits/change-records/CR-20260728-sonar-nginx-response-mapper-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

No Framework or MRTS source, Gitlink, workflow, Makefile, scanner setting,
suppression, or exclusion is changed.

## Commands executed

| Command or procedure | Result |
| --- | --- |
| rtk proxy -- make check-nginx-common-adoption | passed. The focused source contract checks the internal void helper, compile-time diagnostic enum, warning-only/nonfatal result, absence of direct caller tails, body once gate/order, header eligibility/order, fixed diagnostics, and retained mapper contracts. |
| Scoped git diff --check over the five NGINX implementation paths | passed. This is whitespace evidence for local implementation paths, not delivery evidence. |
| rtk proxy -- env BUILD_ROOT=<task-owned-exact-parent-framework-overlay>/build make check-nginx-c17 | blocked_external_dependency. The exact Parent/Framework-pinned overlay reached the repository C17 control, but NGINX headers/source are absent. The underlying script stopped with blocked exit 77 and make returned exit 2. No C17 compilation pass is claimed. |
| Scoped Change-Record pair and index whitespace/paired-structure validation | passed. No trailing whitespace was found in the four owned documentation paths; the English/German records each contain the corresponding 12 required sections, reciprocal language links, the same technical literals, and paired index targets. This limited validation does not replace root-owned exact-overlay documentation/link validation. |

## Security impact

The response mapper consumes response metadata at a filter boundary, so the
extraction is constrained to preserve its existing controls. The helper takes
only the existing context, request pointer, and a compile-time enum. It does
not accept a dynamic diagnostic string, create a new sink, process header/body
data, allocate memory, alter mapper validation, reorder enforcement, or make
a mapper warning fatal.

The focused response-filter review found the existing path already safe and
the narrow extraction feasible when the caller lifecycle controls remain local.
The adoption contract encodes those safeguards. This is source-level evidence;
it does not establish a host runtime result or close a security finding.

## Runtime evidence

No NGINX/libModSecurity host runtime, connector load, request, response,
transport, service start, or allocation-fault scenario was run. The available
passing check is source-contract evidence only. The attempted C17 control did
not compile because its external NGINX source/header prerequisite was absent.

## Checks not run and rationale

- A native NGINX/libModSecurity runtime control was not run. It is outside this
  local source-deduplication candidate and is not inferred from source checks.
- A successful C17 compilation was not run: the exact Parent/Framework overlay
  control was attempted but is blocked_external_dependency by absent NGINX
  headers/source, with script exit 77 and make exit 2.
- Hosted SonarQube Cloud, GitHub Actions, review, and pull-request checks were
  not run because no commit, push, or pull request exists yet.
- Repository-wide bilingual/link validation is not claimed here. Root performs
  the later exact-overlay validation; a candidate checkout without the
  Parent-pinned Framework material is not treated as a documentation defect.

## Known limitations

The 36-line figure is a current source/assessment target, not a new hosted
SonarQube Cloud result. Only an exact candidate PR head can establish new-code
duplication, Quality Gate, check, or issue-closure status.

The C17 control currently lacks a host NGINX headers/source prerequisite. Its
blocked result is an external-dependency limitation, not a source compile
failure and not evidence of a successful build. Source-contract validation
does not build or link the NGINX module.

## Remaining risks

Native NGINX integration could reveal a lifecycle, allocation, or host-header
interaction not exercised by the source contract. Retained guards,
caller-local state transitions, fixed warnings, and the nonfatal helper
interface limit that risk; they do not replace native runtime or a successful
C17 compile.

No delivery or hosted analysis exists yet, so the local result does not claim
to reduce global project duplication density, close a SonarQube Cloud issue,
or satisfy a Quality Gate.

## Final diff and review status

Source review confirms that the candidate has one internal void mapper helper
with a compile-time diagnostic discriminator and that the body/header lifecycle
distinctions remain in the callers. This English record, its German companion,
and the paired indexes passed their scoped whitespace/paired-structure review.

At record authoring there is no task commit, push, pull request, hosted
analysis, hosted closure, review outcome, or merge. The exact C17 limitation
and absence of host runtime evidence remain open and are not represented as
passing results.
