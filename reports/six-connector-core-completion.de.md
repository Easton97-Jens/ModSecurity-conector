# Sechs-Connector-HTTP/1.1-Kernabschluss

**Sprache:** [English](six-connector-core-completion.md) | Deutsch

## Evidenzgrenze

Diese kompakte Matrix umfasst nur die ausgewählten echten HTTP/1.1-Hostpfade
und vorhandenen Kern-Katalogfälle. Sie dokumentiert kanonische Lauf-Evidence;
sie behauptet weder einen vollständigen Katalog noch eine Capability-Promotion
oder ein Production-Ergebnis. Strict-Transportbehandlung, HTTP/2, HTTP/3 und
erweiterte Katalogfälle bleiben getrennte Arbeit.

| Connector | P1 | P2 | P3 | P4-Regel | P4 Safe | Erstes Byte | Kein Full Buffer | Cleanup | Aktueller Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| NGINX | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| HAProxy | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| Envoy | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| Traefik | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| lighttpd | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |

## Kanonische gemeinsame Evidence

- Gemeinsame Run-ID: `six-connectors-core-final-20260712T164725Z-e16e7f1`
- Aggregat-Target `full-lifecycle-all-connectors`: Exit `0`; jeder
  ausgewählte Connector-Runner endete mit `0`.
- `make check-six-connector-core-completion`: `PASS`.
- Jeder Aggregat-Connector-Status bleibt ausschließlich wegen der nicht zum
  Kern gehörenden erweiterten Katalogfälle `NOT_EXECUTED`; die obigen
  Kernzeilen sind `PASS`, und kein Lauf meldete `FAIL` oder `BLOCKED`.

## Ausgewählte echte Hostpfade

| Connector | Ausgewählter HTTP/1.1-Hostpfad | Integrationsmodus | Finale Run-ID | Kern-Evidence |
| --- | --- | --- | --- | --- |
| Apache | natives httpd-Modul | `native-httpd-module` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/Alternative, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| NGINX | natives HTTP-Modul | `native-nginx-http-module` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/Alternative, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| HAProxy | nativer HTX-Filter | `native-htx-filter` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/429, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| Envoy | ext_proc-Listener und -Service | `ext_proc` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403, P2 403, P3 403/302-Redirect, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| Traefik | native Local-Plugin-Middleware | `native-traefik-middleware` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/429, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| lighttpd | gepatchter nativer Entity-Body-Host | `patched-native-lighttpd` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/Alternative, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |

Für jeden ausgewählten Pfad ist das P4-Safe-Event nach Commit ein angefordertes
`deny` mit tatsächlichem `log_only`, sichtbarem HTTP 200, gesendeten
Headern/Body und ohne Connection-Abort. Das synchronisierte First-Byte-
Artefakt ist ein payloadfreier Real-Host-PASS: Der Client erhielt ein Body-
Byte bei pausiertem Upstream, vor dessen EOS und ohne connector-eigenes
vollständiges Response-Buffering. Lifecycle-Zähler sind ausgeglichen, und die
ausgewählten P2-/P4-EOS-Pfade werden einmal pro Transaktion aufgezeichnet. Die
Evidence enthält begrenzte Transaction- und Rule-IDs, aber keine Body-Payloads.

Das Ergebnis behauptet keine per-Chunk-Phase-4-Entscheidung: Response-Body-
Chunks werden inkrementell ingestiert, und die ausgewählte P4-Regel wird dort
bei End-of-Stream ausgewertet, wo Host/Runtime dies melden.
