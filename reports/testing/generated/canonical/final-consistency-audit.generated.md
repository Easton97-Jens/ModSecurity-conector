> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:58:47Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-final-consistency-audit.py`
> Make target: `generate-final-consistency-audit`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
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
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `f2c570c502a53acd154797e1b2b9bc6d6b2b49f76de90402a9a13b3d47d5077d` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `ec37c9971529b06b80763ce9c360dd9164c46f80f63e8d69526854253daf7e7c` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `36f90db93c8a3a554305350d2a745835c1a9d8773742ef5359192beb364299ea` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `7bbf04c71c0bf6a56e892371205db4618f97e091458c0073ac41952a956eb205` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f6134d5f7cc94e181c222e627cd7b4f3bb0a95a9ef85e0b63fb5b55b85268560` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `dd74444ee2dda65ac29c6c32ad15aa9592fbb95ad095f607e1b02e03b309e6d4` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `56f68e0495da29c03f847d077d74a6f79b2608c9624f3217a2f725e28d953644` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `5bc32041708470287a9581441360673a6d1ecbfffa00cdc32eb25fed93aa3cb9` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `88c93af067aff9d0039f0fdb70588e0b760ba950e249375081b65ef346d318b2` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `29a64da4865de4f551ffd230b36ce8c8ff8261e43c1d88ecfac1ca8249b9bd43` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `bca39fdc9484e13668b49c73a89db6f0e90ac73d976d8c125d5e49a80591d447` | `2026-06-16T16-57-44Z-b53340a8` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `a20c5dd83c2a4ab1b072d6f61a472e55a675a8be48212b1bf108621e052f6e69` | `2026-06-16T16-57-44Z-b53340a8` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `b3e54024c30f3b3a31a5800714e6b65658ec01f5610a39560b5d925e5fccf07b` | `2026-06-16T16-57-44Z-b53340a8` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `34c111cc26bc25e09ed6d820ef127bdd830bd55a76e896ebf7fc6f8cd39cd06e` | `2026-06-16T16-57-44Z-b53340a8` | skipped_stale_input |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
