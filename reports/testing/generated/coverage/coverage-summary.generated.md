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

# Generated Coverage Summary

- Total cases: 141
- RESPONSE_BODY cases: 24
- Verified runtime cases: 0
- Non-verified runtime cases: 141

## By scope
- common: 134
- apache: 0
- nginx: 7
- unknown: 0

## By source
- ModSecurity-apache PR: 4
- owasp-modsecurity/ModSecurity-apache#78: 3
- unknown: 134

## By status
- active: 8
- imported: 133

## By variable/collection
- `RESPONSE_BODY`: 20
- `ARGS:q`: 18
- `REQUEST_BODY`: 10
- `ARGS_NAMES`: 7
- `REQUEST_URI`: 7
- `ARGS:test`: 6
- `REQUEST_HEADERS_NAMES`: 5
- `ARGS:a`: 4
- `REQUEST_COOKIES_NAMES`: 4
- `XML`: 4
- `ARGS:param1`: 4
- `ARGS`: 4
- `RESPONSE_HEADERS:Set-Cookie`: 4
- `ARGS:probe`: 4
- `MULTIPART_FILENAME`: 3
- `ARGS:chain_a`: 3
- `ARGS:chain_b`: 3
- `FILES_NAMES`: 2
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
- `XML:/*`: 1
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
- phase 1: 36
- phase 2: 74
- phase 3: 12
- phase 4: 20

## Verification note
- Generated summaries are reporting only and do not replace full runtime evidence from `make smoke-all`.
- RESPONSE_BODY remains non-verified/non-promoted until stable full-smoke runtime evidence exists.
- Bounded Phase 4 / strict-abort evidence remains experimental/non-promoted; pass-through rows do not prove full RESPONSE_BODY support.

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
