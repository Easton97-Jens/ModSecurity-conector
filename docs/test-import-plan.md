# Test Import Plan

Status: implemented

This document records the current import policy for local connector tests. The
source repositories under `/root/conecter/*` are read-only references. No
upstream Apache or NGINX test file is copied verbatim into this repository.

## Inventory

Observed local source inventory on 2026-05-15:

| Source | Relevant files analyzed | Notes |
| --- | ---: | --- |
| `/root/conecter/ModSecurity-apache/tests/` | 29 | Apache regression `.t`, `.t.in`, and harness files |
| `/root/conecter/ModSecurity-nginx/tests/` | 17 | NGINX `.t`, README, and converter files |

Every relevant source file is mapped in:

- `tests/apache/apache-regression-map.md`
- `tests/nginx/nginx-regression-map.md`
- `tests/common/shared-case-origin-map.md`

## Import Rules

- Common cases are allowed only when the rule, request, and expectation are
  connector-neutral and can run through both Apache and NGINX PoC harnesses.
- Apache-only cases belong under `tests/apache/cases/imported/`.
- NGINX-only cases belong under `tests/nginx/cases/imported/`.
- Cases that need HTTP/2, proxy topology, multipart parsing, streaming,
  response-body filters, config inheritance, debug log text, remote rules, or
  external data files remain mapped until the harness has explicit support.
- Simple multipart text-field bodies are supported; multipart parser errors,
  file-storage collections, and part-header edge cases remain mapped.
- Response-body pass-through may be imported when both connectors return the
  expected HTTP status. Response-body blocking is not counted as common PASS
  unless both connectors return stable HTTP 403.
- Imported YAML must include `origin`, `category`, `capabilities`, `portable`,
  `status`, and `known_limitations`; connector-specific YAML must include
  `connector`.

## Imported Common Cases

The following source-derived common cases were added under
`tests/common/cases/imported/`:

| Case | Source basis | Category | Expected behavior |
| --- | --- | --- | --- |
| `action_deny_phase1.yaml` | Apache disruptive actions; NGINX phase action tests | actions | HTTP 403 |
| `action_deny_phase2.yaml` | Apache disruptive actions; NGINX phase action tests | actions | HTTP 403 |
| `action_allow_phase1_pass.yaml` | Apache allow-before-deny action test | actions | HTTP 200 origin body |
| `collection_args_names_block.yaml` | Apache `ARGS_NAMES` target test | collections | HTTP 403 |
| `collection_args_get_block.yaml` | Apache `ARGS_GET` target test; NGINX ARGS tests | collections | HTTP 403 |
| `collection_args_combined_size_block.yaml` | Apache `ARGS_COMBINED_SIZE` target test | collections | HTTP 403 |
| `request_body_args_post_names_block.yaml` | Apache `ARGS_POST_NAMES`; NGINX request-body tests | request-body | HTTP 403 |
| `request_body_raw_text_block.yaml` | NGINX raw `REQUEST_BODY`; Apache raw body pattern | request-body | HTTP 403 |
| `json_request_body_block.yaml` | Apache JSON parser coverage; NGINX request-body tests | body-processors | HTTP 403 |
| `multipart_basic_block.yaml` | Apache normal multipart parser coverage; NGINX request-body tests | multipart | HTTP 403 |
| `response_body_pass.yaml` | Apache response directives; NGINX response-body access tests | response-body | HTTP 200 |

These cases are imported as portable candidates. They count as proven only in an
environment where both connector smokes observe the expected HTTP behavior.

Observed locally on 2026-05-15 with
`BUILD_ROOT=/src/ModSecurity-conector-build`, `make smoke-all` reported all
eleven common imported cases as `PASS` on Apache and NGINX.

## Body And Filter Import Notes

The response-body block candidate is deliberately not active common coverage.
`ModSecurity-nginx/tests/modsecurity-response-body.t` marks the blocking branch
as TODO, and a local probe recognized the `RESPONSE_BODY` rule but did not
produce stable HTTP 403. The source rows are therefore documented as
`xfail`/`mapped-only` in the maps, while `response_body_pass.yaml` remains a
pass-through smoke only.

`multipart_basic_block.yaml` covers only a simple multipart text field that is
visible through `ARGS:name`. File-name variables, upload temp files,
`MULTIPART_*` parser flags, and malformed multipart bodies remain mapped until
they can be proven without connector-specific setup.

`json_request_body_block.yaml` matches raw `REQUEST_BODY` content. Parsed JSON
collection extraction from Apache `rule/15-json.t` remains mapped because the
current shared smoke path does not prove `ARGS:foo` parity.

## Imported Connector-Specific Cases

The following NGINX-specific cases were added under
`tests/nginx/cases/imported/`:

| Case | Source basis | Category | Expected behavior | Why connector-specific now |
| --- | --- | --- | --- | --- |
| `nginx_redirect_phase1_302.yaml` | `tests/modsecurity.t` redirect302 | actions | HTTP 302 | Imported from NGINX tests and not yet proven against Apache |
| `nginx_tx_scoring_absolute_block.yaml` | `tests/modsecurity-scoring.t` absolute score | actions | HTTP 403 | Imported from NGINX tests and not yet proven against Apache |
| `nginx_tx_scoring_iterative_block.yaml` | `tests/modsecurity-scoring.t` iterative score | actions | HTTP 403 | Imported from NGINX tests and not yet proven against Apache |

Apache-specific candidates reviewed in this pass mostly require Apache::Test
context, httpd config inheritance, or Apache-specific runtime setup, so they
are mapped rather than ported.

Observed locally on 2026-05-15 with
`BUILD_ROOT=/src/ModSecurity-conector-build`, `make smoke-all` reported all
three NGINX-specific imported cases as `PASS` on NGINX.

## Smoke Scopes

The smoke targets use explicit scopes:

```sh
make smoke-common  # common minimal + common imported cases on Apache and NGINX
make smoke-apache  # common cases + Apache-specific imported cases on Apache
make smoke-nginx   # common cases + NGINX-specific imported cases on NGINX
make smoke-all     # all applicable cases on the matching connector
```

`SMOKE_CASES` can still name individual cases or paths. The Python case CLI now
resolves names within the selected scope, validates portability metadata, and
writes detailed result summaries under `$BUILD_ROOT/results/`.

## Deferred Categories

| Category | Status | Reason |
| --- | --- | --- |
| multipart | todo | Runner does not model multipart bodies |
| http2 | blocked | Current harnesses are HTTP/1.1 local smokes |
| proxy | todo | No upstream topology support yet |
| streaming-buffering | todo | No streaming assertions or chunk control yet |
| response-body | todo | Connector filter ordering needs explicit support |
| response-body blocking | xfail | NGINX upstream marks block behavior TODO and local probing did not yield stable HTTP 403 |
| response-body pass-through | imported | `response_body_pass.yaml` verifies no regression when response-body access is enabled |
| multipart basic text field | imported | `multipart_basic_block.yaml` covers simple portable multipart parsing |
| multipart file collections | mapped | FILES/FILES_NAMES/FILES_TMPNAMES need cross-connector proof |
| XML | todo | Parser capability and body setup must be documented |
| external file operators | todo | Needs fixture-file materialization |
| debug logs | mapped | Text is volatile and connector-specific |
