> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T07:59:01Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-case-matrix.py`
> Make target: `generate-test-matrix`
> Owner: `runtime`
> Severity: `informational`
> Connector SHA: `32249c908820cfcc21432656b0a0442740584e60`
> Framework SHA: `ec4562aae1f5463d2ce2527d33e7c697f7bb2023`
> Input status: `complete`

# Generated Coverage Summary

**Language:** English | [Deutsch](coverage-summary.generated.de.md)

- Total cases: 160
- RESPONSE_BODY cases: 29
- Verified runtime cases: 0
- Non-verified runtime cases: 160

## By scope
- common: 149
- apache: 2
- nginx: 9
- unknown: 0

## By source
- ModSecurity-apache PR: 4
- owasp-modsecurity/ModSecurity-apache#78: 3
- unknown: 153

## By status
- active: 8
- connector-gap: 15
- imported: 133
- pending: 4

## By variable/collection
- `RESPONSE_BODY`: 20
- `ARGS:q`: 18
- `REQUEST_BODY`: 10
- `REQUEST_URI`: 7
- `ARGS_NAMES`: 6
- `ARGS:test`: 6
- `REQUEST_HEADERS_NAMES`: 5
- `ARGS:a`: 4
- `REQUEST_COOKIES_NAMES`: 4
- `ARGS:param1`: 4
- `MULTIPART_FILENAME`: 4
- `ARGS`: 4
- `RESPONSE_HEADERS:Set-Cookie`: 4
- `ARGS:probe`: 4
- `XML`: 3
- `ARGS:chain_a`: 3
- `ARGS:chain_b`: 3
- `FILES_NAMES`: 2
- `REQUEST_HEADERS:Content-Type`: 2
- `XML:/*`: 2
- `TX:SCORE`: 2
- `REQUEST_COOKIES:USER_TOKEN`: 2
- `RESPONSE_HEADERS:Location`: 2
- `ARGS:audit`: 1
- `REQUEST_HEADERS:X-PR70-Phase`: 1
- `ARGS_POST:arg1`: 1
- `RESPONSE_HEADERS:Last-Modified`: 1
- `ARGS:foo`: 1
- `FILES`: 1
- `ARGS:name`: 1
- `FILES_COMBINED_SIZE`: 1
- `FILES:filedata1`: 1
- `REQUEST_HEADERS:X-Missing`: 1
- `REQUEST_HEADERS:X-Phase`: 1
- `ARGS_COMBINED_SIZE`: 1
- `ARGS_GET`: 1
- `ARGS_POST_NAMES`: 1
- `ARGS_POST:test`: 1
- `REQUEST_HEADERS:User-Agent`: 1
- `REQUEST_HEADERS:X-Entity-Probe`: 1
- `RESPONSE_HEADERS:Content-Type`: 1
- `RESPONSE_HEADERS:X-Missing`: 1
- `RESPONSE_HEADERS:content-type`: 1
- `RESPONSE_HEADERS:Server`: 1

## By phase
- phase 1: 38
- phase 2: 75
- phase 3: 12
- phase 4: 20

## Verification note
- Generated summaries are reporting only and do not replace full runtime evidence from `make smoke-all`.
- RESPONSE_BODY remains non-verified/non-promoted until stable full-smoke runtime evidence exists.
- RESPONSE_BODY remains non-verified/non-promoted; legacy bounded samples and pass-through rows do not prove selected-host support.

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
