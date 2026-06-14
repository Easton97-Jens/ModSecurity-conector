# HAProxy SPOE/SPOA Minimal Artifacts

Status: implemented for current runtime scope

The planning-era minimal artifacts have been superseded by checked-in examples,
build targets, and a live harness.

## Current Artifacts

| Artifact | Status | Purpose |
| --- | --- | --- |
| `examples/haproxy/haproxy-request-only.cfg` | implemented | Request phases 1/2 enforcement example. |
| `examples/haproxy/haproxy-response-headers.cfg` | implemented | Phase 3 response-header example. |
| `examples/haproxy/haproxy-phase4-strict-abort.cfg` | implemented | Bounded Phase 4 strict-abort example. |
| `examples/haproxy/spoe-modsecurity.conf` | implemented | SPOE groups and message argument mapping. |
| `examples/haproxy/modsecurity-agent.conf` | implemented | SPOA runtime configuration. |
| `haproxy-modsecurity-spoa` | implemented | Production SPOA/SPOP runtime binary. |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | implemented | Live runtime harness. |
| `reports/testing/haproxy-poc.md` | implemented | Current PoC evidence report. |

## Current Evidence

- Default HAProxy smoke: `55/55 PASS`.
- HAProxy force-all: `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED /
  6 NOT_EXECUTABLE`.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
