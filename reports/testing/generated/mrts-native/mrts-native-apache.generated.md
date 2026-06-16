> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:56:38Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `complete`

# MRTS Native Apache Report

Generated at: `2026-06-16T05:56:38Z`

## Target
- Target: `apache2_ubuntu`
- Source: `$MRTS_ROOT/config_infra/apache2_ubuntu`
- Infrastructure: MRTS upstream Apache2 Ubuntu native infra
- Native MRTS evidence is separate from connector full-matrix evidence.

## Status
- Status: **FAIL**

## Counts
- attempted: **13**
- pass: **12**
- fail: **1**
- blocked: **0**
- not_executable: **0**

## Known Limitations
- `phase4_native_limitation`
- `RESPONSE_BODY non-promoted`

## First Failing Cases
- Case: `100003-1`
  Rule ID: `100003`
  Phase: `4`
  Variable/target: `ARGS` / `ARGS`
  Expected: HTTP 200 backend response plus ModSecurity log id 100003
  Actual: HTTP 200 backend response observed; expected phase 4 log id 100003 missing
  Classification: `native_modsecurity_semantics` / `phase4_native_limitation`
  Evidence summary: Native ModSecurity reaches the request and earlier request-collection phases, but the phase 4 ARGS rule does not log in native Apache or NGINX evidence.
  Rule: `SecRule ARGS "@contains attack" "id:100003, phase:4, deny, t:none, log"`
  Request: `POST /?foo=attack`

## Runtime Components
- APACHECTL_BIN: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/apachectl-mrts`
- httpd_binary: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/httpd`
- mod_security3_so: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/build/output/apache/mod_security3.so`
- connector_build_id: `70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22`
- modsecurity_build_id: `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- go_ftw_binary: `$CONNECTOR_COMPONENT_CACHE/bin/go-ftw`
- albedo_binary: `$CONNECTOR_COMPONENT_CACHE/bin/albedo`

## Paths
- staged_infra_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/stage/infra`
- run_log_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log`
- job_json_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json`

## Guardrails
- tools/MRTS read-only
- system paths read-only
- no generated MRTS artifacts committed
- native MRTS evidence is separate from connector full-matrix evidence

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/root/.local/state/ModSecurity-conector-build/mrts-native/apache2_ubuntu/job.json` | `8b350ba5c18a3b09fe0e4bea9b2ac83cab48e9c0d4e88a384577784a7c26e99e` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/mrts-native/apache2_ubuntu/job.json` | present | input file available |
