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

## Kanonische Phase-4-Facetten

Jede untenstehende Antwortphasen-Facette ist
`unsupported_by_host_model`. Die gewählte Traefik-`forwardAuth`-Integration
läuft vor der Upstream-Verarbeitung und kann den späteren Upstream-Antwortkörper
nicht inspizieren. Das ist eine Architekturgrenze dieser Integration, kein
fehlender Laufzeitbeleg.

| Facette | Capability-Zustand | Folge für den kanonischen Katalog |
|---|---|---|
| Antwortkörper-Verfügbarkeit (`response_body_buffered`) | `unsupported_by_host_model` | Der Autorisierungsaufruf hat keinen späteren Upstream-Antwortkörper zur Inspektion. |
| Phase-4-Aufruf (`phase4`) | `unsupported_by_host_model` | Über diesen Pfad kann kein Antwortkörper-Phase-4-Aufruf erfolgen. |
| Regelauswertung (`phase4_rule_evaluation`) | `unsupported_by_host_model` | Regel `1100301` kann nicht in einer späteren Upstream-Antwort beobachtet werden. |
| Deny vor dem Commit (`phase4_pre_commit_deny`) | `unsupported_by_host_model` | Dieser Pfad hat keinen Antwortphasen-Punkt, an dem eine Upstream-Antwort verändert werden kann. |
| Späte Intervention (`late_intervention`) | `unsupported_by_host_model` | Die Autorisierungsentscheidung endet, bevor die Upstream-Antwort beginnt. |
| Sichere späte Intervention (`late_intervention_log_only`) | `unsupported_by_host_model` | Es steht keine bereits festgeschriebene Upstream-Antwort für eine reine Protokollierung bereit. |
| Strikte späte Intervention (`late_intervention_abort`) | `unsupported_by_host_model` | Der Dienst kann Traefiks spätere clientseitige Antwort nicht als Phase-4-Aktion abbrechen. |
| Statusmetadaten (`late_intervention_status_metadata`) | `unsupported_by_host_model` | Es gibt kein Antwortphasen-Ereignis, das WAF-, ursprünglichen und sichtbaren Antwortstatus trennt. |

Alle Phase-4-Fälle müssen deshalb als `UNSUPPORTED` erscheinen, niemals als
`PASS` oder `NOT EXECUTED`. Ein künftiger anderer Traefik-Integrationspfad
liegt außerhalb dieses Belegumfangs. Ereignisse und Berichte bleiben
metadatenbasiert; sie enthalten weder Body-Inhalte noch Trefferwerte.

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
