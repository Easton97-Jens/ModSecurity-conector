> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:22:44Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-final-consistency-audit.py`
> Make target: `generate-final-consistency-audit`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
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
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `74dff241151f409d4a958eff005fd65b7e0dc5e03a886ad44bcfc2084e52585f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `3f570cdeada65c05b87f63069c1ed107b78dc1bd2159566a8dfa718b8d8bbfe7` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `cc2e3e94ad36ce80f8675c014493a35a11238ec6e4b008cafedf021486ce8010` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `b2226fe0c3e25f3ae3650ce97c77f43f7c2dee694fad2403544b1279942286b3` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `c27eb0b4dfb6334be9af6aa87597368c2107b924b11689250583fba45df4b7f2` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `99c88712991be652654f3fb3818eec7bc1a0635b1c43fcd0c548a40a00a16133` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `fa93fe73005003fce1a16fc8d3fb9c1f3288c15b21b8b9d47b9d5d83f354b776` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `c04d82c7d4ee21f85bee1ab24642054bf72d53e2053bad7a9df62a148ecc4bad` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `af894d4043bf85d6b941b2c9a5b76b8060bbbb484ed37908547139b5f3fed198` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `c12403d7b77b18bfe9928c9277475659867790c26f2419cd6c18361a9dc89f7e` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `41b01c37817133fd26edbb881422128c0c58a3c957a22f3bfd5a63756d58b766` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `fbbc2c097a08c4b99471215a7fde4ad77b5536577aa6783479f264540a31fc14` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `15b3149cfa94cab5a1f62cb6f424104eaf740569ba26844b370e7604d9c46aeb` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `a5c6dbf0e44c0f3a069ea9d8277619a6f8045e7ccf0802dade28b710ec91404b` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
