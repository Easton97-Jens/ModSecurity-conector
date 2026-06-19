> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:43:33Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
> Input status: `complete`

# MRTS Native Summary

Generated at: `2026-06-19T06:43:33Z`

| Native target | Report | Status | Classification | Critical blocker | Attempted | Pass | Fail | Blocked |
|---|---|---|---|---:|---:|---:|---:|---:|
| Apache2 Ubuntu | mrts-native-apache.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |
| NGINX PR24 | mrts-native-nginx.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |

Combined report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Note: Native MRTS evidence is separate from connector runtime matrix evidence.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `6f80c01c4e5af53144685e17d1cb95a4416862f6a2a04b2b79cb5d87b08bdc48` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `6da3160351259ac1f864890e3666c2f2f7acd4c8eebd06e1a3df5d0b85f67550` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
