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
| SPOE response messages | Die aktive Repository-Konfiguration sendet nur Response-Header; ein Response-Body-Stream braucht einen separaten nativen Callback. |
| Set-var ACK values | Return `txn.modsec.*` variables for HAProxy enforcement. |

## Repository-Nachweise

- Beispiele: `examples/haproxy/`.
- Harness: `connectors/haproxy/harness/run_haproxy_smoke.sh`.
- Laufzeitbericht:
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- PoC-Bericht: `reports/testing/haproxy-poc.md`.

Phase 4 / RESPONSE_BODY ist im aktiven Harness nicht implementiert. Das frühere
begrenzte Sample verwendete `http-response wait-for-body` und ist deaktiviert;
es ist kein Nachweis für einen strikten Abbruch.
