> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:22:40Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-runtime-matrix.py`
> Make target: `generate-full-runtime-matrix`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `missing`

# Complete connector full-runtime matrix summary.

Status: `skipped_missing_input`

Reason: required input missing or empty

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `/root/git/ModSecurity-conector/.venv/bin/python ci/generate-full-runtime-matrix.py --connector-root /root/git/ModSecurity-conector --framework-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework --build-root /var/tmp/ModSecurity-conector-verified/build/full-matrix --log-root /var/tmp/ModSecurity-conector-verified/build/full-matrix --manifest /var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl --output-dir /root/git/ModSecurity-conector/reports/testing/generated` | skipped_missing_input | - | required input missing or empty |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `unknown` | `2026-06-15T21-01-39Z-9391a8d0` | missing |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | missing | input file missing |
