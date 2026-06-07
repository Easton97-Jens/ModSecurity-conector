# HAProxy SPOE/SPOA External Evidence

Status: external mechanism documented, repository runtime implemented

HAProxy SPOE/SPOP is the external mechanism used by the current HAProxy
connector path. External documentation establishes the mechanism; repository
runtime evidence establishes the connector behavior.

## Mechanism Mapping

| Mechanism | Repository use |
| --- | --- |
| `filter spoe engine modsecurity config <file>` | Attaches the ModSecurity SPOE engine. |
| Dedicated SPOP backend | Connects HAProxy to `haproxy-modsecurity-spoa`. |
| SPOE request messages | Send request phases 1/2 data. |
| SPOE response messages | Send response headers and bounded response-body bytes. |
| Set-var ACK values | Return `txn.modsec.*` variables for HAProxy enforcement. |

## Repository Evidence

- Examples: `examples/haproxy/`.
- Harness: `connectors/haproxy/harness/run_haproxy_smoke.sh`.
- Runtime report:
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- PoC report: `reports/testing/haproxy-poc.md`.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
