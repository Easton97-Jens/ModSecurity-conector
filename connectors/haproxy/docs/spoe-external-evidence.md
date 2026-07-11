# HAProxy SPOE/SPOA External Evidence

**Language:** English | [Deutsch](spoe-external-evidence.de.md)

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
| SPOE response messages | The active repository configuration sends response headers only; a response-body stream requires a separate native callback. |
| Set-var ACK values | Return `txn.modsec.*` variables for HAProxy enforcement. |

## Repository Evidence

- Examples: `examples/haproxy/`.
- Harness: `connectors/haproxy/harness/run_haproxy_smoke.sh`.
- Runtime report:
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- PoC report: `reports/testing/haproxy-poc.md`.

Phase 4 / RESPONSE_BODY is not implemented in the active harness. The former
bounded sample used `http-response wait-for-body` and is disabled; it is not
strict-abort evidence.
