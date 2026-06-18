> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:47:53Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# MRTS Native Summary

Generated at: `2026-06-18T17:47:53Z`

| Native target | Report | Status | Classification | Critical blocker | Attempted | Pass | Fail | Blocked |
|---|---|---|---|---:|---:|---:|---:|---:|
| Apache2 Ubuntu | mrts-native-apache.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |
| NGINX PR24 | mrts-native-nginx.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |

Combined report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Note: Native MRTS evidence is separate from connector runtime matrix evidence.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `03bb0aefae70d11b6fdf0c7bdbf372bdfce9285c160a675deadc08ff526a01d3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `425f99fe2b96bf291a2c688f8dd34a4eb756f8c496aecb909b8ce996f616f5a8` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
