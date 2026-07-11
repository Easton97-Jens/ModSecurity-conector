> Generierter Capability-Snapshot — Runtime-Status nicht manuell bearbeiten.

# Apache No-CRS-Baseline

**Sprache:** [English](apache-no-crs-baseline.md) | Deutsch

Am `2026-07-10` aus den eingecheckten Manifesten `connectors/<name>/capabilities.json` erzeugt. Es wurde kein kanonisches No-CRS-`result.json` verwendet, weil noch kein kanonischer Lauf ausgeführt wurde.

Kanonischer Gesamtstatus: `NOT EXECUTED`

Hostmodell: `natives Apache-httpd-Modul`

| Dimension | Kanonischer Status | Manifest-Grenze |
|---|---|---|
| Source Contract | IMPLEMENTED, NOT ASSERTED | Source, Metadaten und Host-Wiring sind vorhanden |
| Build / Link | IMPLEMENTED, NOT ASSERTED | Ein aktuelles kanonisches Build-Ergebnis fehlt |
| Config Load | IMPLEMENTED, NOT ASSERTED | Ein aktuelles kanonisches Config-Ergebnis fehlt |
| Request-freier Start | IMPLEMENTED, NOT ASSERTED | Ein aktuelles kanonisches Start-Ergebnis fehlt |
| Minimale Runtime | IMPLEMENTED, NOT ASSERTED | Frühere gezielte Evidence wird nicht in diese Baseline übernommen |
| No-CRS-Baseline | NOT EXECUTED | Kein kanonisches `result.json` vorhanden |
| Phase 1 | IMPLEMENTED, NOT ASSERTED | Capability-Manifest |
| Phase 2 | IMPLEMENTED, NOT ASSERTED | Capability-Manifest |
| Phase 3 | IMPLEMENTED, NOT ASSERTED | Capability-Manifest |
| Phase 4 | IMPLEMENTED, NOT ASSERTED | Capability-Manifest |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only-JSONL muss durch einen kanonischen Lauf belegt werden |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup- und Fehlerfälle benötigen kanonische Case-Ergebnisse |
| Status | NOT EXECUTED | Fehlende Evidence wird niemals als PASS abgeleitet |

## Architekturgrenze

Gepufferte Request- und Response-Pfade sind implementiert; Streaming-Pfade und Drop sind nicht implementiert.

Das Phase-4-Interventionstiming hängt davon ab, ob Apache die Antwort bereits committed hat.

Erwarteter Evidence-Root:

```text
$EVIDENCE_ROOT/apache/<run-id>/
```

## Bewusst nicht erhobene Claims

- Production Readiness oder Production Hardening
- Runtime Security oder Security Verification
- CRS-Verifikation oder CRS-Vollständigkeit
- Extended-/Full-Matrix-Verifikation
- über alle Connectoren verifizierter Response Body
- ein kanonischer No-CRS-PASS
