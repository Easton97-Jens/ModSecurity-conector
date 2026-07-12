> Generierter Capability-Snapshot — Runtime-Status nicht manuell bearbeiten.

# NGINX No-CRS-Baseline

**Sprache:** [English](nginx-no-crs-baseline.md) | Deutsch

Am `2026-07-10` aus den eingecheckten Manifesten `connectors/<name>/capabilities.json` erzeugt. Es wurde kein kanonisches No-CRS-`result.json` verwendet, weil noch kein kanonischer Lauf ausgeführt wurde.

Kanonischer Gesamtstatus: `NOT EXECUTED`

Hostmodell: `natives NGINX-HTTP-Modul`

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

Begrenzte Request- und Response-Body-Filter sind implementiert; Streaming-Phasensemantik und Drop sind nicht implementiert.

Späte Phase-4-Ergebnisse hängen davon ab, ob NGINX die Response-Header bereits gesendet hat.

## Kanonische Phase-4-Facetten

Der Antwortkörperpfad und alle untenstehenden Antwortphasen-Facetten sind
`implemented_not_asserted`. Das ist eine Quelltext- und Verdrahtungs-Aussage,
kein Phase-4-`PASS`: Kein aktueller kanonischer Lauf auf einem realen Host hat
Regel `1100301`, einen Deny vor dem Commit oder eine der späten Interventionen
beobachtet.

| Facette | Capability-Zustand | Erforderlicher Laufzeitbeleg vor einer Bestätigung |
|---|---|---|
| Antwortkörper-Verfügbarkeit (`response_body_buffered`) | `implemented_not_asserted` | Ein begrenzter NGINX-Body-Filterpfad ist verdrahtet; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt die Verarbeitung eines Antwortkörpers. |
| Phase-4-Aufruf (`phase4`) | `implemented_not_asserted` | Der Antwortkörper-Phase-4-Aufruf ist verdrahtet; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt seinen Aufruf. |
| Regelauswertung (`phase4_rule_evaluation`) | `implemented_not_asserted` | Der Body-Filter-Phase-4-Pfad ist vorhanden; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt die Auswertung von Regel `1100301`. |
| Deny vor dem Commit (`phase4_pre_commit_deny`) | `implemented_not_asserted` | Ein Deny-Zweig vor den Headern ist vorhanden; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt `requested_action=deny`, `actual_action=deny`, ungesendete Header und sichtbaren `403`. |
| Späte Intervention (`late_intervention`) | `implemented_not_asserted` | Richtlinienzweige für späte Interventionen sind verdrahtet; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt eine disruptive Entscheidung nach dem Commit. |
| Sichere späte Intervention (`late_intervention_log_only`) | `implemented_not_asserted` | Ein sicherer Nur-Protokollierungszweig ist verdrahtet; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt `actual_action=log_only` bei unverändert sichtbarem Status. |
| Strikte späte Intervention (`late_intervention_abort`) | `implemented_not_asserted` | Ein strikter Abbruchzweig ist verdrahtet; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt `actual_action=abort_connection` und `connection_aborted=true`. |
| Statusmetadaten (`late_intervention_status_metadata`) | `implemented_not_asserted` | Die Phase-4-Metadaten sind verdrahtet; kein aktuelles kanonisches Ereignis belegt getrennten WAF-Anforderungsstatus, ursprünglichen Hoststatus, sichtbaren Clientstatus sowie angeforderte und tatsächliche Aktion. |

Der gemeinsame Katalog trennt Regelauswertung von Transportverhalten:
`phase4_rule_observed` benötigt keinen sichtbaren `403`; ein Deny vor dem
Commit dagegen schon. Nach dem Commit kann ein `log_only`-Ergebnis korrekt einen
sichtbaren `200` belassen, und ein Abbruch bedeutet nicht, dass ein Client
`403` sehen kann. Ereignisse und dieser Bericht enthalten weder Body-Inhalte
noch Trefferwerte.

Erwarteter Evidence-Root:

```text
$EVIDENCE_ROOT/nginx/<run-id>/
```

## Bewusst nicht erhobene Claims

- Production Readiness oder Production Hardening
- Runtime Security oder Security Verification
- CRS-Verifikation oder CRS-Vollständigkeit
- Extended-/Full-Matrix-Verifikation
- über alle Connectoren verifizierter Response Body
- ein kanonischer No-CRS-PASS
