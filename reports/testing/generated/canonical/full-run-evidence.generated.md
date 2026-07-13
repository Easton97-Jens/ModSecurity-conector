> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T20:12:28Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/evidence/reports/generate-remaining-failure-analysis.py`
> Make target: `refresh-connector-reports`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
> Framework SHA: `4e9d4ba616235127b6fc0a2ee87107d93d03f40b`
> Input status: `stale`

# Evidence rollup shared by focused analysis and consistency checks.

**Language:** English | [Deutsch](full-run-evidence.generated.de.md)

Status: `skipped_stale_input`

Reason: required generated input is stale

## Verified Command

| Command | Status | Return Code | Notes |
|---|---|---:|---|
| `<local-home-root>/git/ModSecurity-conector/.venv/bin/python ci/evidence/reports/generate-remaining-failure-analysis.py --connector-root <local-home-root>/git/ModSecurity-conector --output-dir <local-home-root>/git/ModSecurity-conector/reports/testing/generated` | skipped_stale_input | - | required generated input is stale |

## Rows

_No rows available. Reason: producer command was not run or verified input is unavailable._

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `8b8298f135b70c6487dcfbae620801fc09fabe03e73c91fe8657a27505216bce` | `2026-06-16T19-12-00Z-614c8049` | stale |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |

## MRTS Native Summary
- Report generated at: `-`
- Native MRTS evidence is separate from connector runtime matrix evidence.

| Target | Status | Exit code | Attempted | PASS | FAIL | BLOCKED | Reason | Run log | Summary |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| apache2_ubuntu | NOT_RUN | - | 0 | 0 | 0 | 0 | - | `-` | `-` |
| nginx-pr24 | NOT_RUN | - | 0 | 0 | 0 | 0 | - | `-` | `-` |

<!-- mrts-native-infrastructure-evidence:start -->
## MRTS Native Infrastructure Evidence

- Apache native: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

These native MRTS reports are separate from connector full-matrix evidence.
<!-- mrts-native-infrastructure-evidence:end -->
