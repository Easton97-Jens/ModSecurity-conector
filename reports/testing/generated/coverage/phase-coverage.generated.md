> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:56:26Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-case-matrix.py`
> Make target: `generate-test-matrix`
> Owner: `runtime`
> Severity: `informational`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `complete`

# Generated Phase Coverage

| phase | case_count | top_variables | status_distribution |
|---|---:|---|---|
| 1 | 36 | REQUEST_URI(7), REQUEST_HEADERS_NAMES(5), ARGS:a(4), REQUEST_COOKIES_NAMES(4), ARGS:param1(2) | active:2, imported:34 |
| 2 | 74 | ARGS:q(18), REQUEST_BODY(9), ARGS_NAMES(7), ARGS:test(6), XML(4) | active:5, imported:69 |
| 3 | 12 | RESPONSE_HEADERS:Set-Cookie(4), RESPONSE_HEADERS:Location(2), RESPONSE_HEADERS:Last-Modified(1), RESPONSE_HEADERS:Content-Type(1), RESPONSE_HEADERS:X-Missing(1) | active:1, imported:11 |
| 4 | 20 | RESPONSE_BODY(20) | imported:20 |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `config/testing/import-status.json` | `5eea82df1ded18c34bbc8cf6fc5992572edaa6723a33b6dd4a0b49ee00ab5a4f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/runtime-validation-snapshot.json` | `dfeb2c386052d649210cd1b1acaa5dab644396c933eec71daa33e2bbd5f3b5ed` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `config/testing/import-status.json` | present | input file available |
| `reports/testing/runtime-validation-snapshot.json` | present | input file available |
