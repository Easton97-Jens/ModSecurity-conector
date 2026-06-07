# HAProxy ModSecurity Examples

## Purpose

These examples show the production SPOA path for HAProxy:
`haproxy-modsecurity-spoa`, HAProxy + SPOE/SPOP + libmodsecurity, decision
logging, audit-log plumbing, request phases 1/2, implemented phase 3 response
headers, and bounded Phase 4 strict-abort evidence.

## Files

- `haproxy-request-only.cfg`: HAProxy request-phase enforcement through SPOE.
- `haproxy-response-headers.cfg`: HAProxy request plus response-header checks.
- `haproxy-phase4-strict-abort.cfg`: bounded Phase 4 strict-abort example.
- `spoe-modsecurity.conf`: SPOE message and variable mapping.
- `modsecurity-agent.conf`: `haproxy-modsecurity-spoa` configuration.

## Production Paths

The examples use production-style paths:

- `/usr/local/sbin/haproxy-modsecurity-spoa`
- `/etc/haproxy/haproxy.cfg`
- `/etc/haproxy/spoe-modsecurity.conf`
- `/etc/haproxy/modsecurity-agent.conf`
- `/etc/modsecurity/haproxy-rules.conf`
- `/var/log/haproxy-modsecurity/decision.jsonl`
- `/var/log/haproxy-modsecurity/audit.log`
- `/var/log/haproxy-modsecurity/agent.log`

## Request Phases 1/2

`haproxy-request-only.cfg` sends request metadata, headers, and request body to
the SPOA service through the `request-check` group. HAProxy enforces returned
transaction variables with `http-request deny`, redirect, and silent-drop
rules.

## Phase 3 Response Headers

`haproxy-response-headers.cfg` adds the `response-check` group. It sends
response status and selected response headers to the SPOA service and enforces
returned variables with `http-response` rules.

## Phase 4 / RESPONSE_BODY Strict-Abort

`haproxy-phase4-strict-abort.cfg` adds `http-response wait-for-body` and sends
bounded response bytes to the SPOA service. The runtime can record bounded
strict-abort evidence, including `decision.jsonl` and audit-log output.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented as runtime evidence only.

## Variable And Placeholder Reference

| Name | Type | Required | Example value | Used in | Meaning | Change requires restart/reload | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `haproxy-modsecurity-spoa` | binary path | Yes | `/usr/local/sbin/haproxy-modsecurity-spoa` | service unit or process supervisor | Production SPOA/SPOP process that loads libmodsecurity. | restart SPOA | Built by `make -C connectors/haproxy build-spoa-runtime`. |
| `filter spoe engine modsecurity` | HAProxy directive | Yes | `config /etc/haproxy/spoe-modsecurity.conf` | `haproxy-*.cfg` | Attaches the ModSecurity SPOE engine. | reload HAProxy | Config path must be readable by HAProxy. |
| `http-request send-spoe-group` | HAProxy directive | Yes | `modsecurity request-check` | request and phase4 HAProxy configs | Sends request data to the SPOA service. | reload HAProxy | Required for phases 1/2. |
| `http-response send-spoe-group` | HAProxy directive | Response modes | `modsecurity response-check` | response-header and phase4 HAProxy configs | Sends response data to the SPOA service. | reload HAProxy | Required for phase 3 and bounded phase 4 evidence. |
| `http-response wait-for-body` | HAProxy directive | Phase 4 only | `time 50ms at-least 1` | `haproxy-phase4-strict-abort.cfg` | Allows bounded response bytes to be available to SPOE. | reload HAProxy | Keep timeout and byte expectations bounded. |
| `be_spoa_modsecurity` | HAProxy backend | Yes | `127.0.0.1:12345` | `haproxy-*.cfg` | SPOP backend for the SPOA process. | reload HAProxy | Address must match agent `listen`. |
| `spoe-agent modsecurity-agent` | SPOE section | Yes | `use-backend be_spoa_modsecurity` | `spoe-modsecurity.conf` | Defines the SPOE agent and backend. | reload HAProxy | Uses HAProxy `mode spop`. |
| `groups` | SPOE option | Yes | `request-check response-check` | `spoe-modsecurity.conf` | Declares available SPOE groups. | reload HAProxy | Request-only deployments can still leave response group defined. |
| `register-var-names` | SPOE option | Yes | `blocked action status redirect_url rule_id phase error` | `spoe-modsecurity.conf` | Registers transaction variables returned by SPOA. | reload HAProxy | HAProxy enforcement rules read these variables. |
| `max-frame-size` | SPOE option | Yes | `65532` | `spoe-modsecurity.conf` | Bounds SPOE frame size. | reload HAProxy | Keep aligned with request/response body limits. |
| `request_id` | SPOE message arg | Yes | `unique-id` | `spoe-modsecurity.conf` | Correlates requests in decision and audit logs. | reload HAProxy | `unique-id-header` exposes the same value upstream. |
| `headers_bin` | SPOE message arg | Request checks | `req.hdrs_bin` | `spoe-modsecurity.conf` | Sends request headers in binary form. | reload HAProxy | Used by request phases. |
| `body` | SPOE message arg | Request checks | `req.body` | `spoe-modsecurity.conf` | Sends bounded request body bytes. | reload HAProxy | Requires `option http-buffer-request`. |
| `response_headers` | SPOE message arg | Response checks | `res.hdrs` | `spoe-modsecurity.conf` | Sends response headers for phase 3. | reload HAProxy | Supported by response-header evidence. |
| `response_body` | SPOE message arg | Phase 4 only | `res.body` | `spoe-modsecurity.conf` | Sends bounded response body bytes. | reload HAProxy | Non-promoted runtime evidence only. |
| `listen` | agent config key | Yes | `127.0.0.1:12345` | `modsecurity-agent.conf` | Address where `haproxy-modsecurity-spoa` listens. | restart SPOA | Must match HAProxy SPOP backend. |
| `rules-file` | agent config key | Yes | `/etc/modsecurity/haproxy-rules.conf` | `modsecurity-agent.conf` | ModSecurity rules loaded by the SPOA process. | restart SPOA | Include CRS from this file when needed. |
| `decision-log` | agent config key | Yes | `/var/log/haproxy-modsecurity/decision.jsonl` | `modsecurity-agent.conf` | JSONL runtime decision log. | restart SPOA | Preserve for evidence and debugging. |
| `audit-log` | agent config key | No | `/var/log/haproxy-modsecurity/audit.log` | `modsecurity-agent.conf` | libmodsecurity audit log output. | restart SPOA | Ensure writable directory permissions. |
| `log-file` | agent config key | No | `/var/log/haproxy-modsecurity/agent.log` | `modsecurity-agent.conf` | Agent diagnostic log. | restart SPOA | Rotate with system logs. |
| `mode` | agent config key | Yes | `block` | `modsecurity-agent.conf` | Enables disruptive enforcement. | restart SPOA | Use detection mode only if implemented in the deployed binary. |
| `fail-mode` | agent config key | Yes | `closed` | `modsecurity-agent.conf` | Behavior when processing fails. | restart SPOA | Choose according to service risk tolerance. |
| `request-body-limit` | agent config key | No | `65532` | `modsecurity-agent.conf` | Bounds request body bytes processed. | restart SPOA | Keep within SPOE frame limits. |
| `response-body-limit` | agent config key | Phase 4 only | `65532` | `modsecurity-agent.conf` | Bounds response body bytes processed. | restart SPOA | `0` disables response-body processing. |
| `response-body-timeout` | agent config key | Phase 4 only | `50` | `modsecurity-agent.conf` | Bounded wait for response body evidence. | restart SPOA | Keep small to avoid response latency. |
| `spoe-timeout` | agent config key | No | `2000` | `modsecurity-agent.conf` | Agent-side SPOE timeout in milliseconds. | restart SPOA | Keep aligned with HAProxy processing timeout. |
| `worker-count` | agent config key | No | `1` | `modsecurity-agent.conf` | SPOA worker count. | restart SPOA | Size for production traffic after testing. |
| `max-transactions` | agent config key | No | `4096` | `modsecurity-agent.conf` | Agent transaction capacity. | restart SPOA | Tune with memory and concurrency. |

## Runtime Evidence

Local generated evidence uses:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime/decision.jsonl`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime/audit.log`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`

Default HAProxy smoke reports `55/55 PASS`. Force-all HAProxy evidence reports
`133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED / 6 NOT_EXECUTABLE`.

## Reload And Restart

Run `haproxy -c -f /etc/haproxy/haproxy.cfg` before reload. Reload HAProxy
after HAProxy or SPOE config changes. Restart the SPOA service after
`modsecurity-agent.conf`, rule file, binary, or library-path changes.

## Limitations

The root summaries are connector-neutral. Row-level HAProxy evidence stays in
`reports/testing/generated/haproxy-runtime-results.generated.md`. There is no
synthetic matrix writer; generated reports consume runtime summaries and
snapshot data.

## Related Docs

- `COMPILE_HAPROXY.md`
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
- `reports/testing/haproxy-poc.md`
