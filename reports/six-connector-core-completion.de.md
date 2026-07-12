# Sechs-Connector-HTTP/1.1-Kernabschluss

**Sprache:** [English](six-connector-core-completion.md) | Deutsch

## Evidenzgrenze

Dies ist die kompakte Arbeitsmatrix für die ausgewählten echten HTTP/1.1-
Hosts. Sie dokumentiert nur bestehende Kern-Katalogfälle und deren Evidenz aus
dem finalen kanonischen Lauf. Strict-Transportbehandlung, HTTP/2, HTTP/3 und
der übrige Katalog liegen außerhalb dieses Meilensteins.

| Connector | P1 | P2 | P3 | P4-Regel | P4 Safe | Erstes Byte | Kein Full Buffer | Cleanup | Aktueller Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finale Native-Barriere ausstehend | Finale Native-Barriere ausstehend | Finales Lifecycle-Inventar ausstehend | Frischer Aggregat-Lauf |
| NGINX | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finaler nativer Hostlauf ausstehend | Finale Native-Barriere ausstehend | Finale Native-Barriere ausstehend | Finales Lifecycle-Inventar ausstehend | Frischer Aggregat-Lauf |
| HAProxy | Finaler HTX-Lauf ausstehend | Finaler HTX-P2-Lauf ausstehend | Finaler HTX-Lauf ausstehend | Finaler HTX-P4-Lauf ausstehend | Finaler HTX-P4-Lauf ausstehend | Finale HTX-Barriere ausstehend | Finale HTX-Barriere ausstehend | Finales Lifecycle-Inventar ausstehend | Frischer Aggregat-Lauf |
| Envoy | Finaler ext_proc-Lauf ausstehend | Finaler ext_proc-Lauf ausstehend | Finaler ext_proc-Lauf ausstehend | Finaler ext_proc-Lauf ausstehend | Finaler ext_proc-Lauf ausstehend | Finale ext_proc-Barriere ausstehend | Finale ext_proc-Barriere ausstehend | Finales Lifecycle-Inventar ausstehend | Frischer Aggregat-Lauf |
| Traefik | Finaler Native-Middleware-Lauf ausstehend | Finaler Native-Middleware-Lauf ausstehend | Finaler Native-Middleware-Lauf ausstehend | Finaler Native-Middleware-Lauf ausstehend | Finaler Native-Middleware-Lauf ausstehend | Finale Native-Barriere ausstehend | Finale Native-Barriere ausstehend | Finales Lifecycle-Inventar ausstehend | Frischer Aggregat-Lauf |
| lighttpd | Finaler gepatchter Hostlauf ausstehend | Finaler gepatchter Hostlauf ausstehend | Finaler gepatchter Hostlauf ausstehend | Finaler Entity-Body-P4-Lauf ausstehend | Finaler Entity-Body-P4-Lauf ausstehend | Finale gepatchte Hostbarriere ausstehend | Finale gepatchte Hostbarriere ausstehend | Finales Lifecycle-Inventar ausstehend | Frischer Aggregat-Lauf |

Die zugehörigen IDs der aktuellen Läufe und PASS/FAIL/NOT-EXECUTED-Ergebnisse
werden erst nach Abschluss der einzelnen und des gemeinsamen kanonischen
Laufs hier festgehalten.
