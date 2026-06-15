> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:39:57Z`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `missing`

# MRTS Native NGINX PR24 Report

Generated at: `2026-06-15T10:39:57Z`

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
- Status: **NOT_RUN**

## Counts
- attempted: **0**
- pass: **0**
- fail: **0**
- blocked: **0**
- not_executable: **0**

## Known Limitations
- `phase4_native_limitation`
- `RESPONSE_BODY non-promoted`

## First Failing Cases
- None recorded.

## Runtime Components
- MRTS_NATIVE_NGINX_BIN: `-`
- MRTS_NATIVE_NGINX_MODULE_DIR: `-`
- ngx_http_modsecurity_module_so: `-`
- connector_build_id: `-`
- modsecurity_build_id: `-`
- go_ftw_binary: `-`
- albedo_binary: `-`

## Paths
- staged_infra_path: `$MRTS_NATIVE_ROOT/nginx-pr24/stage/infra`
- run_log_path: `$MRTS_NATIVE_ROOT/nginx-pr24/run.log`
- job_json_path: `$MRTS_NATIVE_ROOT/nginx-pr24/job.json`

## Guardrails
- tools/MRTS read-only
- system paths read-only
- no generated MRTS artifacts committed
- native MRTS evidence is separate from connector full-matrix evidence

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/mrts-native/nginx-pr24/job.json` | missing | input file missing |
