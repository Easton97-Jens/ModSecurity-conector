> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T15:48:03Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-final-consistency-audit.py`
> Make target: `generate-final-consistency-audit`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
> Input status: `blocked`

# Merge-readiness consistency gate across generated evidence.

Status: `blocked`

Reason: required generated input is blocked

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `/root/git/ModSecurity-conector/.venv/bin/python ci/generate-final-consistency-audit.py --connector-root /root/git/ModSecurity-conector --framework-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework --output-dir /root/git/ModSecurity-conector/reports/testing/generated` | blocked | - | required generated input is blocked |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `b73e9279de250d71c12b771bc4c24bb4b712dac0fed0008c60f6075116916797` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `c747640b424f6aa6fbbf98f07407ce1dfc47c8ae2295220454554acdd5e70aa8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `29210f6193c70c53ff0d6fb934005c9e2f29129f88cb322eabb328198ae25dbf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `781564315ab245d2dd9d89e2ed9445f71d222553697e36daec83189a8d3d998b` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `18f53c9539c3c8d74bd89e6549062846275bbb678857522f3f76ab99af603989` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `df41566492fb236cb03508161261b1eedb8745fc8aa07feff56de02969cb50fb` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `eb9242e77b1ed5456b66e3a9ccb94ffff873edf23b955d35254937cb8b77c040` | `2026-06-16T19-12-00Z-614c8049` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `70b4612471c9b05902042bac06a3fdeb02558aab7b3d3f5fb923dfb34d1ee66c` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `90aeb81722723302cc20ba6994c3868717cb3056ec6a4c0b57b52b6329dbd894` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `883fdce904c304d9ea0b2557badb239635568e14ae49b9d5bb54a4b4357816d1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `0e48530472eb758d223f427075d5c03f65f78fc16e3b2e534aee95aa238293b3` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `68692c6831e04ee96e716010e2d8cfee87fc5351914df21816c508f6346e77e4` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `3f52c0b718d8e8b65705890c1540609646f224f4bac4409f7c3d39e4c177a297` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `9060fe37e06facf05ca49cf4bb37ea42ac07acac63d8b9c721293b426265658b` | `2026-06-16T19-12-00Z-614c8049` | blocked |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
