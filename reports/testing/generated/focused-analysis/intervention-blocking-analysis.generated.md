> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:22:43Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-intervention-blocking-analysis.py`
> Make target: `generate-intervention-blocking-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `blocked`

# Intervention blocking classification and no-match separation.

Status: `blocked`

Reason: required generated input is blocked

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `/root/git/ModSecurity-conector/.venv/bin/python ci/generate-intervention-blocking-analysis.py --connector-root /root/git/ModSecurity-conector --framework-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework --output-dir /root/git/ModSecurity-conector/reports/testing/generated` | blocked | - | required generated input is blocked |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `3f570cdeada65c05b87f63069c1ed107b78dc1bd2159566a8dfa718b8d8bbfe7` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `74dff241151f409d4a958eff005fd65b7e0dc5e03a886ad44bcfc2084e52585f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `b2226fe0c3e25f3ae3650ce97c77f43f7c2dee694fad2403544b1279942286b3` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `cc2e3e94ad36ce80f8675c014493a35a11238ec6e4b008cafedf021486ce8010` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `c27eb0b4dfb6334be9af6aa87597368c2107b924b11689250583fba45df4b7f2` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | blocked | generated report input is not usable: status=blocked |
