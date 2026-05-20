# NGINX Runtime Failure Classification

Date: 2026-05-20

This note classifies the 11 remaining NGINX runtime smoke failures from the
latest local source-build run. It does not change connector code, YAML
expectations, XFAIL status, or RESPONSE_BODY verification.

## Summary

Apache completed the corresponding local source-build smoke with 48 PASS,
0 FAIL, and 0 BLOCKED. NGINX completed its source-build smoke with 43 PASS,
11 FAIL, and 0 BLOCKED. Every NGINX FAIL expected HTTP 200 and observed HTTP
403.

The NGINX error logs for all 11 failures report the same non-ModSecurity
origin-serving problem:

```text
htdocs/index.html is forbidden (13: Permission denied)
```

The generated `htdocs/index.html` files themselves are readable, but the
current local build root is under a parent path that the NGINX worker cannot
traverse. The phase-4 cases also have missing or empty `phase4.log` output,
which is consistent with NGINX failing to serve the static origin before the
phase-4 log-only behavior could be classified.

Therefore these 11 failures are classified as **NGINX harness filesystem
permission blocked**. They are not PASS evidence, not XFAIL promotion, not
connector-gap proof, not runtime-difference proof, and not likely-bug proof.
Rerun with an NGINX-readable `BUILD_ROOT` or a harness permission fix before
classifying connector behavior.

## Case Classification

| Case | Area | Expected | Actual | Runtime evidence | Classification |
| --- | --- | ---: | ---: | --- | --- |
| `phase2_args_pass` | Phase 2 `ARGS` pass-through | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission |
| `action_allow_phase1_pass` | Phase 1 `allow` pass-through | 200 | 403 | Rule 2103 logged, then NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission |
| `response_body_pass` | RESPONSE_BODY pass-through | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission; RESPONSE_BODY remains non-promoted |
| `v2_transformation_url_decode_pass_no_match` | `t:urlDecode` no-match pass-through | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission |
| `v3_args_names_get_pass_no_match` | `ARGS_NAMES` no-match pass-through | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission |
| `v3_request_cookies_names_pass_no_match` | `REQUEST_COOKIES_NAMES` no-match pass-through | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission |
| `v3_request_cookies_pass_no_match` | `REQUEST_COOKIES` no-match pass-through | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission |
| `v3_request_headers_names_pass_no_match` | `REQUEST_HEADERS_NAMES` no-match pass-through | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied | BLOCKED: NGINX harness filesystem permission |
| `nginx_phase4_content_type_out_of_scope` | NGINX phase-4 content-type log-only probe | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied; `phase4.log` missing/empty | BLOCKED: NGINX harness filesystem permission; not RESPONSE_BODY promotion |
| `nginx_phase4_minimal_log_only` | NGINX phase-4 minimal log-only probe | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied; `phase4.log` missing/empty | BLOCKED: NGINX harness filesystem permission; not RESPONSE_BODY promotion |
| `nginx_phase4_safe_log_only` | NGINX phase-4 safe log-only probe | 200 | 403 | NGINX `error.log` reports generated `htdocs/index.html` forbidden / permission denied; `phase4.log` missing/empty | BLOCKED: NGINX harness filesystem permission; not RESPONSE_BODY promotion |

## Follow-up

- Use an NGINX-readable `BUILD_ROOT` or fix the NGINX harness staging
  permissions before rerunning `REFRESH=1 make smoke-nginx`.
- Keep the current YAML expectations unchanged until a clean NGINX runtime
  rerun provides connector-level evidence.
- Keep `RESPONSE_BODY` non-verified/non-promoted.
- Do not claim `make smoke-all` PASS from this snapshot; it was not run after
  the NGINX smoke failure.
