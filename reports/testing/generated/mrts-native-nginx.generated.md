# MRTS Native NGINX PR24 Report

Generated at: `2026-06-13T11:32:41Z`

## Target
- Target: `nginx-pr24`
- Source: `Framework PR24 overlay`
- PR source: https://github.com/owasp-modsecurity/MRTS/pull/24
- Infrastructure: MRTS PR24 NGINX + libmodsecurity3 native infra
- Native MRTS evidence is separate from connector full-matrix evidence.

## PR Metadata
- PR number: `24`
- PR head SHA: `134ea7e35d72e7d72294b66d80dafa07daa5fc92`
- captured_at_utc: `2026-06-09T15:18:21Z`
- upstream_status: `open-pr`
- stability: `experimental`
- replacement note: replace with $MRTS_ROOT/config_infra/nginx_linux once merged upstream

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
- MRTS_NATIVE_NGINX_BIN: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules`
- ngx_http_modsecurity_module_so: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules/ngx_http_modsecurity_module.so`
- connector_build_id: `24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71`
- modsecurity_build_id: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- go_ftw_binary: `$CONNECTOR_COMPONENT_CACHE/bin/go-ftw`
- albedo_binary: `$CONNECTOR_COMPONENT_CACHE/bin/albedo`

## Paths
- staged_infra_path: `$MRTS_NATIVE_ROOT/nginx-pr24/stage/infra`
- run_log_path: `$MRTS_NATIVE_ROOT/nginx-pr24/run.log`
- job_json_path: `$MRTS_NATIVE_ROOT/nginx-pr24/job.json`

## Guardrails
- tools/MRTS read-only
- system paths read-only
- no generated MRTS artifacts committed
- native MRTS evidence is separate from connector full-matrix evidence
