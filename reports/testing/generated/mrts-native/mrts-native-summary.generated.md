> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:39:12Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `58b2135bb8adf12a4cad8afb448d1156e801cc00`
> Framework SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
> Input status: `complete`

# MRTS Native Summary

Generated at: `2026-06-19T16:39:12Z`

| Native target | Report | Status | Classification | Critical blocker | Attempted | Pass | Fail | Blocked |
|---|---|---|---|---:|---:|---:|---:|---:|
| Apache2 Ubuntu | mrts-native-apache.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |
| NGINX PR24 | mrts-native-nginx.generated.md | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 |

Combined report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Note: Native MRTS evidence is separate from connector runtime matrix evidence.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `6c266638bedb64d6eef5e4019166250a91bbe6fdd891c6305983989d78a3ffbd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `3a383219cecd9ef88202f413c5b3c01a814f1f5b5995d652f2beafaacb02287a` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
