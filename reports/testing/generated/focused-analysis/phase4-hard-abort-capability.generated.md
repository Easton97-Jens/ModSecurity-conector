> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:22:42Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-phase4-hard-abort-capability.py`
> Make target: `generate-phase4-hard-abort-capability`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `blocked`

# Phase 4 hard-abort capability evidence.

Status: `blocked`

Reason: required generated input is blocked

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `/root/git/ModSecurity-conector/.venv/bin/python ci/generate-phase4-hard-abort-capability.py --connector-root /root/git/ModSecurity-conector --output-dir /root/git/ModSecurity-conector/reports/testing/generated` | blocked | - | required generated input is blocked |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `3f570cdeada65c05b87f63069c1ed107b78dc1bd2159566a8dfa718b8d8bbfe7` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `74dff241151f409d4a958eff005fd65b7e0dc5e03a886ad44bcfc2084e52585f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `3f29f03f5e41e041a7f4a072fcf20441401b7633f1afc6f62cd9f6ed9c45785f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `17994ec83ca33c03a84eabd97f494c7a706cef28658c68de50699fc6c160b8b4` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
