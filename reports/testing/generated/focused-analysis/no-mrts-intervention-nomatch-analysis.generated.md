> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:58:45Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-no-mrts-intervention-nomatch-analysis.py`
> Make target: `generate-no-mrts-intervention-nomatch-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
> Input status: `blocked`

# Framework-owned no-MRTS no-match semantics.

Status: `blocked`

Reason: required generated input is blocked

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `/root/git/ModSecurity-conector/.venv/bin/python ci/generate-no-mrts-intervention-nomatch-analysis.py --connector-root /root/git/ModSecurity-conector --framework-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework --output-dir /root/git/ModSecurity-conector/reports/testing/generated` | blocked | - | required generated input is blocked |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `a20c5dd83c2a4ab1b072d6f61a472e55a675a8be48212b1bf108621e052f6e69` | `2026-06-16T16-57-44Z-b53340a8` | skipped_stale_input |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `f2c570c502a53acd154797e1b2b9bc6d6b2b49f76de90402a9a13b3d47d5077d` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `7bbf04c71c0bf6a56e892371205db4618f97e091458c0073ac41952a956eb205` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f6134d5f7cc94e181c222e627cd7b4f3bb0a95a9ef85e0b63fb5b55b85268560` | `2026-06-16T16-57-44Z-b53340a8` | stale |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
