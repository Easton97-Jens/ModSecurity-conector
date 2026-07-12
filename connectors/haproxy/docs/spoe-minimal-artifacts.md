# HAProxy SPOE/SPOA Compatibility Artifacts

**Language:** English | [Deutsch](spoe-minimal-artifacts.de.md)

Status: implemented for current runtime scope

The planning-era minimal artifacts have been superseded by checked-in
compatibility-path examples, build targets, and a live harness. The
compatibility path is distinct from the selected native HTX full-lifecycle
profile and does not promote Phase 4 / RESPONSE_BODY capabilities.

## Current Artifacts

| Artifact | Status | Purpose |
| --- | --- | --- |
| `examples/haproxy/compatibility-spoe/haproxy-request-only.cfg` | implemented compatibility artifact | Request phases 1/2 enforcement example for the SPOE/SPOA compatibility path. |
| `examples/haproxy/compatibility-spoe/haproxy-response-headers.cfg` | implemented compatibility artifact | Phase 3 response-header example for the SPOE/SPOA compatibility path. |
| `examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg` | legacy_disabled | Retired `wait-for-body` sample; not current runtime evidence. |
| `examples/haproxy/compatibility-spoe/spoe-modsecurity.conf` | implemented compatibility artifact | SPOE groups and message argument mapping. |
| `examples/haproxy/compatibility-spoe/modsecurity-agent.conf` | implemented compatibility artifact | SPOA runtime configuration. |
| `haproxy-modsecurity-spoa` | implemented | Production SPOA/SPOP runtime binary. |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | implemented | Live runtime harness. |
| `reports/testing/haproxy-poc.md` | implemented | Current PoC evidence report. |

## Current Evidence

- Default HAProxy smoke: `55/55 PASS`.
- HAProxy force-all: `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED /
  6 NOT_EXECUTABLE`.

Phase 4 / RESPONSE_BODY is `not_implemented` in the selected SPOE/SPOP path.
The former `wait-for-body` strict-abort sample is disabled, legacy, and
noncanonical; it is not current runtime evidence.
