# HAProxy SPOE/SPOA-Kompatibilitätsartefakte

**Sprache:** [English](spoe-minimal-artifacts.md) | Deutsch

Status: für den aktuellen Laufzeitbereich implementiert

Die minimalen Artefakte aus der Planungszeit wurden durch eingecheckte ersetzt
Beispiele für Kompatibilitätspfade, Build-Ziele und ein Live-Harness. Die
Der Kompatibilitätspfad unterscheidet sich vom ausgewählten nativen HTX-Gesamtlebenszyklus
Profil und fördert keine Phase 4 / RESPONSE_BODY-Funktionen.

## Aktuelle Artefakte

| Artefakt | Status | Zweck |
| --- | --- | --- |
| `examples/haproxy/compatibility-spoe/haproxy-request-only.cfg` | implementiertes Kompatibilitätsartefakt | Anforderungsbeispiel für die Durchsetzung der Phasen 1/2 für den SPOE/SPOA-Kompatibilitätspfad. |
| `examples/haproxy/compatibility-spoe/haproxy-response-headers.cfg` | implementiertes Kompatibilitätsartefakt | Beispiel für einen Antwortheader der Phase 3 für den SPOE/SPOA-Kompatibilitätspfad. |
| `examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg` | Legacy_disabled | Ausgemustertes `wait-for-body`-Beispiel; kein aktueller Laufzeitbeweis. |
| `examples/haproxy/compatibility-spoe/spoe-modsecurity.conf` | implementiertes Kompatibilitätsartefakt | SPOE-Gruppen und Nachrichtenargumentzuordnung. |
| `examples/haproxy/compatibility-spoe/modsecurity-agent.conf` | implementiertes Kompatibilitätsartefakt | SPOA-Laufzeitkonfiguration. |
| `haproxy-modsecurity-spoa` | implementiert | Produktions-SPOA/SPOP-Laufzeitbinärdatei. |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | implementiert | Live-Laufzeit-Harness. |
| `reports/testing/haproxy-poc.md` | implementiert | Aktueller PoC-Beweisbericht. |

## Aktuelle Beweise

- Standard-HAProxy-Smoke-Test: `55/55 PASS`.
- HAProxy Force-All: `133 Versuche / 104 PASS / 23 FAIL / 0 BLOCKIERT /
  6 NOT_EXECUTABLE`.

Phase 4 / RESPONSE_BODY ist `not_implemented` im ausgewählten SPOE/SPOP-Pfad.
Das ehemalige `wait-for-body`-Strict-Abort-Beispiel ist deaktiviert, veraltet und
nichtkanonisch; Es handelt sich nicht um aktuelle Laufzeitbeweise.
