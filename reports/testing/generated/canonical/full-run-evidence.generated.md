> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:40:01Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Make target: `generate-remaining-failure-analysis`
> Owner: `connector`
> Severity: `important`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
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
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `676cc8d9b51b9294387e0b73fe8a7ff1f78a4fe5ff268f5996cb1967b906c576` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `7d7a581758867799859f481971e56c0e7da57ca399f5a7e016b2ce839ac83063` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `b21bba0ae1115efd9761ed2317324b8e142f221801b35359b024704fb2e4c657` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |

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
