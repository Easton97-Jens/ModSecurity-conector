> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:48:20Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Make target: `generate-remaining-failure-analysis`
> Owner: `connector`
> Severity: `important`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Evidence rollup shared by focused analysis and consistency checks.

Status: `blocked`

Reason: required generated input is blocked

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `/root/git/ModSecurity-conector/.venv/bin/python ci/generate-remaining-failure-analysis.py --connector-root /root/git/ModSecurity-conector --output-dir /root/git/ModSecurity-conector/reports/testing/generated` | blocked | - | required generated input is blocked |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `890da243b91305746a7f8658e29fd2e9f814b10a001885be834c69bed542dba2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `c1f815e949464f1ba593aaee1b2c5651739506c91f657fd9bc60ce817c76c73d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `a563b592cfaa69eba42d56c8653fdf35dabd612afed049e7a44125eed2ee2975` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
