# HAProxy SPOE/SPOA PoC Plan

Status: implemented for current production SPOA runtime scope

The earlier plan has moved from planned-only documentation to a live
production-style SPOA path. The remaining plan is now about promotion evidence
and production hardening.

## Implemented

- HAProxy starts with SPOE config.
- `haproxy-modsecurity-spoa` starts as the external SPOA/SPOP component.
- Benign requests can pass.
- Disruptive decisions can block through HAProxy enforcement rules.
- `decision.jsonl` records runtime decisions.
- Audit-log plumbing is available.
- Generated reports are produced by the framework report flow.

## Remaining Plan

- Expand force-all FAIL investigation.
- Add production service-manager examples.
- Prove long-running multi-worker behavior.
- Define promotion criteria for full RESPONSE_BODY support.
- Keep generated root summaries connector-neutral and row-level HAProxy detail
  in generated HAProxy detail reports.

Phase 4 / RESPONSE_BODY is `not_implemented` in the selected SPOE/SPOP path.
The former `wait-for-body` strict-abort sample is disabled, legacy, and
noncanonical; it is not current runtime evidence.
