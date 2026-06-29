# HAProxy SPOE/SPOA Externe Nachweise

**Sprache:** [English](spoe-external-evidence.md) | Deutsch

Status: Externer Mechanismus dokumentiert, Repository-Laufzeit implementiert

HAProxy SPOE/SPOP ist der externe Mechanismus, der vom aktuellen HAProxy verwendet wird
Verbindungspfad. Externe Dokumentation legt den Mechanismus fest; Repository
Runtime-Nachweise legen das Connector-Verhalten fest.

## Mechanismuszuordnung

| Mechanism | Repository use |
| --- | --- |
| `filter spoe engine modsecurity config <file>` | Attaches the ModSecurity SPOE engine. |
| Dedicated SPOP backend | Connects HAProxy to `haproxy-modsecurity-spoa`. |
| SPOE request messages | Send request phases 1/2 data. |
| SPOE response messages | Send response headers and bounded response-body bytes. |
| Set-var ACK values | Return `txn.modsec.*` variables for HAProxy enforcement. |

## Repository-Nachweise

- Beispiele: `examples/haproxy/`.
- Harness: `connectors/haproxy/harness/run_haproxy_smoke.sh`.
- Laufzeitbericht:
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- PoC-Bericht: `reports/testing/haproxy-poc.md`.

Phase 4 / RESPONSE_BODY bleibt nicht promoted; begrenzte strikte Abbruchbeweise sind
documented/reported nur als Laufzeitbeweis.
