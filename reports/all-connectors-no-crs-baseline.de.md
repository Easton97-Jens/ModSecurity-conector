> Generierter Capability-Snapshot — Runtime-Status nicht manuell bearbeiten.

# No-CRS-Baseline für alle Connectoren

**Sprache:** [English](all-connectors-no-crs-baseline.md) | Deutsch

Am `2026-07-10` aus den eingecheckten Manifesten `connectors/<name>/capabilities.json` erzeugt. Es wurde kein kanonisches No-CRS-`result.json` verwendet, weil noch kein kanonischer Lauf ausgeführt wurde.

Kanonischer Gesamtstatus: `NOT EXECUTED`

| Connector | Build | Config | Start | Minimale Runtime | No-CRS-Baseline | P1 | P2 | P3 | P4 | Events | Lifecycle | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Apache | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| NGINX | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| HAProxy | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| Envoy | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | UNSUPPORTED | UNSUPPORTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| Traefik | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | UNSUPPORTED | UNSUPPORTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| lighttpd | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |

## Interpretation

`IMPLEMENTED, NOT ASSERTED` ist eine Source-/Capability-Aussage und kein
Runtime-PASS. `UNSUPPORTED` ist eine ehrliche Host-Modell-Grenze und wird
weder als PASS noch als FAIL gezählt. `NOT IMPLEMENTED` ist eine
Connector-Lücke. `NOT EXECUTED` bedeutet, dass kein kanonisches Ergebnis
vorliegt.

- Envoy-Phase 2 ist konfiguriert, aber nicht ausgeübt.
- Envoy und Traefik können im gewählten Autorisierungsmodell die spätere Upstream-Antwort nicht beobachten.
- Traefik-Phase 2 ist in der gewählten nativen Konfiguration nicht implementiert.
- lighttpd-Phase 3 ist implementiert, aber nicht verhaltensseitig belegt.
- lighttpd-Request- und -Response-Bodies sind nicht implementiert.
- Ältere Smoke-, Body-, CRS-, Bridge-, Sidecar- und Self-Test-Ergebnisse sind ausgeschlossen.

## Erwartete kanonische Evidence

Jeder Connector-Lauf schreibt nach
`$EVIDENCE_ROOT/<connector>/<run-id>/`. Das Aggregat darf ausschließlich die
sechs kanonischen `result.json`-Dateien lesen. Fehlende oder mehrdeutige Dateien
bleiben `NOT EXECUTED` oder führen zu einem Fehler; sie können nicht zu PASS
werden.

## Bewusst nicht erhobene Claims

- Production Readiness oder Production Hardening
- Runtime Security oder Security Verification
- CRS-Verifikation oder CRS-Vollständigkeit
- Extended-/Full-Matrix-Verifikation
- über alle Connectoren verifizierter Response Body
- alle Connectoren vollständig verifiziert
