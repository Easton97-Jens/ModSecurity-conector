> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T19:07:56Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/reporting/generate-case-matrix.py`
> Make target: `generate-test-matrix`
> Owner: `runtime`
> Severity: `informational`
> Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
> Framework SHA: `06d09c6173d929911bbf75e79e9ee0bf7ea3f734`
> Input status: `complete`

# Generated Phase Coverage

**Language:** English | [Deutsch](phase-coverage.generated.de.md)

| phase | case_count | top_variables | status_distribution |
|---|---:|---|---|
| 1 | 38 | REQUEST_URI(7), REQUEST_HEADERS_NAMES(5), ARGS:a(4), REQUEST_COOKIES_NAMES(4), ARGS:param1(2) | active:2, imported:36 |
| 2 | 75 | ARGS:q(18), REQUEST_BODY(10), ARGS_NAMES(6), ARGS:test(6), MULTIPART_FILENAME(4) | active:5, imported:70 |
| 3 | 12 | RESPONSE_HEADERS:Set-Cookie(4), RESPONSE_HEADERS:Location(2), RESPONSE_HEADERS:Last-Modified(1), RESPONSE_HEADERS:Content-Type(1), RESPONSE_HEADERS:X-Missing(1) | active:1, imported:11 |
| 4 | 20 | RESPONSE_BODY(20) | imported:20 |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `config/testing/import-status.json` | `5eea82df1ded18c34bbc8cf6fc5992572edaa6723a33b6dd4a0b49ee00ab5a4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/runtime-validation-snapshot.json` | `d3017f038a44a5f5596e36e3482f92cd93ce6f2173bb958da98cddc05884cd8f` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `config/testing/import-status.json` | present | input file available |
| `reports/testing/runtime-validation-snapshot.json` | present | input file available |
