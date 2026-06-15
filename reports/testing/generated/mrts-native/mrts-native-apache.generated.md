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

# MRTS Native Apache Report

Generated at: `2026-06-15T10:39:57Z`

## Target
- Target: `apache2_ubuntu`
- Source: `$MRTS_ROOT/config_infra/apache2_ubuntu`
- Infrastructure: MRTS upstream Apache2 Ubuntu native infra
- Native MRTS evidence is separate from connector full-matrix evidence.

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
- APACHECTL_BIN: `-`
- httpd_binary: `-`
- mod_security3_so: `-`
- connector_build_id: `-`
- modsecurity_build_id: `-`
- go_ftw_binary: `-`
- albedo_binary: `-`

## Paths
- staged_infra_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/stage/infra`
- run_log_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log`
- job_json_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json`

## Guardrails
- tools/MRTS read-only
- system paths read-only
- no generated MRTS artifacts committed
- native MRTS evidence is separate from connector full-matrix evidence

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/mrts-native/apache2_ubuntu/job.json` | missing | input file missing |
