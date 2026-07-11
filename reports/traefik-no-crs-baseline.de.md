> Generierter Capability-Snapshot — Runtime-Status nicht manuell bearbeiten.

# Traefik No-CRS-Baseline

**Sprache:** [English](traefik-no-crs-baseline.md) | Deutsch

Am `2026-07-10` aus den eingecheckten Manifesten `connectors/<name>/capabilities.json` erzeugt. Es wurde kein kanonisches No-CRS-`result.json` verwendet, weil noch kein kanonischer Lauf ausgeführt wurde.

Kanonischer Gesamtstatus: `NOT EXECUTED`

Hostmodell: `HTTP-forwardAuth-Service`

| Dimension | Kanonischer Status | Manifest-Grenze |
|---|---|---|
| Source Contract | IMPLEMENTED, NOT ASSERTED | Source, Metadaten und Host-Wiring sind vorhanden |
| Build / Link | IMPLEMENTED, NOT ASSERTED | Ein aktuelles kanonisches Build-Ergebnis fehlt |
| Config Load | IMPLEMENTED, NOT ASSERTED | Ein aktuelles kanonisches Config-Ergebnis fehlt |
| Request-freier Start | IMPLEMENTED, NOT ASSERTED | Ein aktuelles kanonisches Start-Ergebnis fehlt |
| Minimale Runtime | IMPLEMENTED, NOT ASSERTED | Frühere gezielte Evidence wird nicht in diese Baseline übernommen |
| No-CRS-Baseline | NOT EXECUTED | Kein kanonisches `result.json` vorhanden |
| Phase 1 | IMPLEMENTED, NOT ASSERTED | Capability-Manifest |
| Phase 2 | NOT IMPLEMENTED | Capability-Manifest |
| Phase 3 | UNSUPPORTED | Capability-Manifest |
| Phase 4 | UNSUPPORTED | Capability-Manifest |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only-JSONL muss durch einen kanonischen Lauf belegt werden |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup- und Fehlerfälle benötigen kanonische Case-Ergebnisse |
| Status | NOT EXECUTED | Fehlende Evidence wird niemals als PASS abgeleitet |

## Architekturgrenze

Traefik kann forwardAuth-Bodies puffern; die gewählte native Konfiguration aktiviert forwardBody jedoch nicht und nutzt request_body_mode=none.

Das vorgelagerte forwardAuth-Modell kann die spätere Upstream-Antwort nicht beobachten.

Erwarteter Evidence-Root:

```text
$EVIDENCE_ROOT/traefik/<run-id>/
```

## Bewusst nicht erhobene Claims

- Production Readiness oder Production Hardening
- Runtime Security oder Security Verification
- CRS-Verifikation oder CRS-Vollständigkeit
- Extended-/Full-Matrix-Verifikation
- über alle Connectoren verifizierter Response Body
- ein kanonischer No-CRS-PASS
