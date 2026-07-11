> Generierter Capability-Snapshot — Runtime-Status nicht manuell bearbeiten.

# lighttpd No-CRS-Baseline

**Sprache:** [English](lighttpd-no-crs-baseline.md) | Deutsch

Am `2026-07-10` aus den eingecheckten Manifesten `connectors/<name>/capabilities.json` erzeugt. Es wurde kein kanonisches No-CRS-`result.json` verwendet, weil noch kein kanonischer Lauf ausgeführt wurde.

Kanonischer Gesamtstatus: `NOT EXECUTED`

Hostmodell: `natives lighttpd-Plugin`

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
| Phase 3 | IMPLEMENTED, NOT ASSERTED | Capability-Manifest |
| Phase 4 | NOT IMPLEMENTED | Capability-Manifest |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only-JSONL muss durch einen kanonischen Lauf belegt werden |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup- und Fehlerfälle benötigen kanonische Case-Ergebnisse |
| Status | NOT EXECUTED | Fehlende Evidence wird niemals als PASS abgeleitet |

## Architekturgrenze

Request- und Response-Bodies sind bewusst nicht implementiert.

Der Response-Header-Hook existiert, wurde aber noch nicht mit einer echten Phase-3-Regel verhaltensseitig belegt.

## Kanonische Phase-4-Facetten

Jede Antwortkörper- und Antwortphasen-Facette unten ist im aktuellen nativen
Modul `not_implemented`. Das Fehlen eines nativen Antwortkörper-Hooks ist eine
Implementierungslücke, keine belegte Unmöglichkeit des lighttpd-Hostmodells.

| Facette | Capability-Zustand | Folge für den kanonischen Katalog |
|---|---|---|
| Antwortkörper-Verfügbarkeit (`response_body_buffered`) | `not_implemented` | Das native Modul liefert ModSecurity keinen Antwortkörper. |
| Phase-4-Aufruf (`phase4`) | `not_implemented` | Es gibt keinen echten Antwortkörper-Phase-4-Aufruf. |
| Regelauswertung (`phase4_rule_evaluation`) | `not_implemented` | Regel `1100301` kann nicht gegen einen nativen Antwortkörper laufen. |
| Deny vor dem Commit (`phase4_pre_commit_deny`) | `not_implemented` | Vor dem Commit ist kein Antwortkörper-Entscheidungspunkt implementiert. |
| Späte Intervention (`late_intervention`) | `not_implemented` | Es ist kein Antwortkörper-Richtlinienpunkt nach dem Commit implementiert. |
| Sichere späte Intervention (`late_intervention_log_only`) | `not_implemented` | Kein Deny eines bereits festgeschriebenen Antwortkörpers kann als reine Protokollierung erfasst werden. |
| Strikte späte Intervention (`late_intervention_abort`) | `not_implemented` | Keine Abbruchaktion für einen bereits festgeschriebenen Antwortkörper ist implementiert. |
| Statusmetadaten (`late_intervention_status_metadata`) | `not_implemented` | Keine Phase-4-Ereignisquelle trennt WAF-, ursprünglichen und sichtbaren Antwortstatus. |

Phase-4-Fälle bleiben `NOT EXECUTED` (oder sind nicht auswählbar), bis eine
echte native Antwortkörper-Implementierung existiert. Sie dürfen nicht als
`UNSUPPORTED` bezeichnet werden, solange nicht belegt ist, dass lighttpds
Hostmodell keinen geeigneten Hook bereitstellen kann. Ereignisse und Berichte
bleiben metadatenbasiert; sie enthalten weder Body-Inhalte noch Trefferwerte.

Erwarteter Evidence-Root:

```text
$EVIDENCE_ROOT/lighttpd/<run-id>/
```

## Bewusst nicht erhobene Claims

- Production Readiness oder Production Hardening
- Runtime Security oder Security Verification
- CRS-Verifikation oder CRS-Vollständigkeit
- Extended-/Full-Matrix-Verifikation
- über alle Connectoren verifizierter Response Body
- ein kanonischer No-CRS-PASS
