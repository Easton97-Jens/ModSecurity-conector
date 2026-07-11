> Generierter Capability-Snapshot — Runtime-Status nicht manuell bearbeiten.

# HAProxy No-CRS-Baseline

**Sprache:** [English](haproxy-no-crs-baseline.md) | Deutsch

Am `2026-07-10` aus den eingecheckten Manifesten `connectors/<name>/capabilities.json` erzeugt. Es wurde kein kanonisches No-CRS-`result.json` verwendet, weil noch kein kanonischer Lauf ausgeführt wurde.

Kanonischer Gesamtstatus: `NOT EXECUTED`

Hostmodell: `HAProxy-SPOE/SPOP-Agent`

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

Begrenzte Request- und experimentelle Response-Body-Pfade existieren; Streaming-, Drop- und Abort-Entscheidungen sind nicht implementiert.

Host und Agent sind getrennte Prozesse und benötigen getrennte Logs in einem gemeinsamen Manifest.

## Kanonische Phase-4-Facetten

Der begrenzte, experimentelle Antwortkörperpfad, `phase4` und
`phase4_rule_evaluation` sind Quellpfade mit `implemented_not_asserted`. Ein
Agent- oder Mapperpfad ist kein Phase-4-Laufzeitbeleg: Kein aktueller
kanonischer HAProxy-Lauf auf einem realen Host hat Regel `1100301` beobachtet.
Die semantischen Facetten für Vor-Commit-Deny, späte Aktionen und
Statusmetadaten sind `not_implemented`, weil der Runner kein beim Client
sichtbares Antwortergebnis, keinen tatsächlichen Commit-Zeitpunkt und keinen
Hostpunkt nach dem Commit beobachtet.

| Facette | Capability-Zustand | Erforderlicher Laufzeitbeleg vor einer Bestätigung |
|---|---|---|
| Antwortkörper-Verfügbarkeit (`response_body_buffered`) | `implemented_not_asserted` | Ein begrenzter experimenteller HAProxy-/SPOP-Antwortkörperpfad ist vorhanden; kein aktueller kanonischer Laufzeitbeleg auf einem realen Host belegt die Inspektion eines Antwortausschnitts. |
| Phase-4-Aufruf (`phase4`) | `implemented_not_asserted` | Der experimentelle HAProxy-/SPOA-Antwortkörperaufruf ist verdrahtet; kein aktueller kanonischer Hostlaufzeitbeleg belegt seinen Aufruf. |
| Regelauswertung (`phase4_rule_evaluation`) | `implemented_not_asserted` | Der begrenzte SPOA-/SPOP-Phase-4-Pfad ist vorhanden; kein aktueller kanonischer HAProxy-Hostlaufzeitbeleg belegt die Auswertung von Regel `1100301`. |
| Deny vor dem Commit (`phase4_pre_commit_deny`) | `not_implemented` | Der Agent schreibt policy-abgeleitete Felder, doch kein Host-Runner beobachtet sichtbaren Client-Status und tatsächlichen Commit-Zeitpunkt. |
| Späte Intervention (`late_intervention`) | `not_implemented` | Der aktuelle Pfad für Antwortentscheidungen ist vor dem Commit modelliert und besitzt keinen Hostpunkt nach dem Commit. |
| Sichere späte Intervention (`late_intervention_log_only`) | `not_implemented` | Es gibt keine sichere Aktion `log_only` nach dem Commit und kein hostbeobachtetes Ergebnis mit unverändert sichtbarem Status. |
| Strikte späte Intervention (`late_intervention_abort`) | `not_implemented` | Es gibt keine kontrollierte Aktion `abort_connection` nach dem Commit und kein hostbeobachtetes Abbruchergebnis. |
| Statusmetadaten (`late_intervention_status_metadata`) | `not_implemented` | Policy-abgeleitete Diagnosen liefern keinen hostbeobachteten ursprünglichen/sichtbaren Status und keinen Zeitpunkt. |

Der gemeinsame Katalog trennt Regelauswertung von Transportverhalten:
`phase4_rule_observed` benötigt keinen sichtbaren `403`. HAProxy implementiert
die semantischen Fälle für Vor-Commit-Deny, `log_only` nach dem Commit,
Abbruch nach dem Commit und Statusmetadaten noch nicht; sie bleiben
`NOT_EXECUTED`. Ereignisse und dieser Bericht enthalten weder Body-Inhalte noch
Trefferwerte.

Erwarteter Evidence-Root:

```text
$EVIDENCE_ROOT/haproxy/<run-id>/
```

## Bewusst nicht erhobene Claims

- Production Readiness oder Production Hardening
- Runtime Security oder Security Verification
- CRS-Verifikation oder CRS-Vollständigkeit
- Extended-/Full-Matrix-Verifikation
- über alle Connectoren verifizierter Response Body
- ein kanonischer No-CRS-PASS
