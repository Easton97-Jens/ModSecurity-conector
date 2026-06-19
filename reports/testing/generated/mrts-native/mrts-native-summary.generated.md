> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:52:03Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

# MRTS Native Summary

Generated at: `2026-06-19T16:52:03Z`

| Native target | Report | Status | Classification | Critical blocker | Attempted | Pass | Fail | Blocked |
|---|---|---|---|---:|---:|---:|---:|---:|
| Apache2 Ubuntu | mrts-native-apache.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |
| NGINX PR24 | mrts-native-nginx.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |

Combined report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Note: Native MRTS evidence is separate from connector runtime matrix evidence.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `69b359db6b8f622d3c56c149b90807db442dca4742eba51272dbe88d16111ed3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `d168d51d79ae446b3230f92e65e8bd65828db400208075a79a95dc86066b56f4` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
