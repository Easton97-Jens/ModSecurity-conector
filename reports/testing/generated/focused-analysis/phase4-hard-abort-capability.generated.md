> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T15:47:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-phase4-hard-abort-capability.py`
> Make target: `generate-phase4-hard-abort-capability`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
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
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `c747640b424f6aa6fbbf98f07407ce1dfc47c8ae2295220454554acdd5e70aa8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `b73e9279de250d71c12b771bc4c24bb4b712dac0fed0008c60f6075116916797` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `90ff4ac6d2ba5a41121be9c56fd637f52b9b7ac5c9854524ea13cd1a94266df9` | `2026-06-16T19-12-00Z-614c8049` | skipped_stale_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `ebc4b664b9e7a9e5b8d69e1f22a719a1e725426085240726172c08c00fb66c33` | `2026-06-16T19-12-00Z-614c8049` | skipped_stale_input |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
