> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:39:29Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
> Input status: `complete`

# MRTS Native Summary

Generated at: `2026-06-17T02:39:29Z`

| Native target | Report | Status | Classification | Critical blocker | Attempted | Pass | Fail | Blocked |
|---|---|---|---|---:|---:|---:|---:|---:|
| Apache2 Ubuntu | mrts-native-apache.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |
| NGINX PR24 | mrts-native-nginx.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |

Combined report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Note: Native MRTS evidence is separate from connector runtime matrix evidence.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `9aa3ecd89fbfce7a5c4eba7fdee9b0ba04eda8ec365a1b347aa7c1bba546c900` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `03ea2803bcd564284e704492dee86dcb19afa74b281581aae987bb099ace7a8f` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
