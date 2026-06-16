> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:57:55Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-intervention-blocking-analysis.py`
> Make target: `generate-intervention-blocking-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `stale`

# Intervention blocking classification and no-match separation.

Status: `skipped_stale_input`

Reason: required generated input is stale

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `/root/git/ModSecurity-conector/.venv/bin/python ci/generate-intervention-blocking-analysis.py --connector-root /root/git/ModSecurity-conector --framework-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework --output-dir /root/git/ModSecurity-conector/reports/testing/generated` | skipped_stale_input | - | required generated input is stale |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `8b6bfa1ccfca933d937939b21678b9543df4b9a125b9802c4b4ace67429daa24` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `6ad06c76b68ec65d7a60b26b5409cfa84c7277e45c1c48488bc3c081dec5e49f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `d54beb4d40ea472648b5615ad1c493533ae642434a4cd62026a055fca9bda479` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0c993999eb0da54fd0b131b1170d183a7d38c68529d7bd8e63f9d5c45f2a96c7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `6a543b34e8941ce08cc523fbb3492eeeeaed4f16ac4b925105f87bdb71c1247d` | `2026-06-15T21-01-39Z-9391a8d0` | stale |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
