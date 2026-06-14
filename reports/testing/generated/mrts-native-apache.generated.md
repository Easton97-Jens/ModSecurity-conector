# MRTS Native Apache Report

Generated at: `2026-06-13T11:32:41Z`

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
- APACHECTL_BIN: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/httpd/bin/apachectl-mrts`
- httpd_binary: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/httpd/bin/httpd`
- mod_security3_so: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/build/output/apache/mod_security3.so`
- connector_build_id: `030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72`
- modsecurity_build_id: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
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
