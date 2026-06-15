> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:39:49Z`
> Generator: `framework:ci/generate-case-matrix.py`
> Make target: `generate-test-matrix`
> Owner: `runtime`
> Severity: `informational`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `complete`

# Generated Phase Coverage

| phase | case_count | top_variables | status_distribution |
|---|---:|---|---|
| 1 | 36 | REQUEST_URI(7), REQUEST_HEADERS_NAMES(5), ARGS:a(4), REQUEST_COOKIES_NAMES(4), ARGS:param1(2) | active:2, imported:34 |
| 2 | 74 | ARGS:q(18), REQUEST_BODY(9), ARGS_NAMES(7), ARGS:test(6), XML(4) | active:5, imported:69 |
| 3 | 12 | RESPONSE_HEADERS:Set-Cookie(4), RESPONSE_HEADERS:Location(2), RESPONSE_HEADERS:Last-Modified(1), RESPONSE_HEADERS:Content-Type(1), RESPONSE_HEADERS:X-Missing(1) | active:1, imported:11 |
| 4 | 20 | RESPONSE_BODY(20) | imported:20 |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `config/testing/import-status.json` | present | input file available |
| `reports/testing/runtime-validation-snapshot.json` | present | input file available |
