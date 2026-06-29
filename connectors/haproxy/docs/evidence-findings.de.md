# HAProxy-Nachweisergebnisse

**Sprache:** [English](evidence-findings.md) | Deutsch

Status: aktuelle Runtime-Nachweise

## Zusammenfassung finden

| Finding | Status | Evidence |
| --- | --- | --- |
| SPOE/SPOP integration path | selected and implemented for current scope | HAProxy examples, harness, production SPOA runtime |
| Production SPOA binary | implemented | `haproxy-modsecurity-spoa` |
| libmodsecurity binding | implemented | build and self-test targets |
| Request phases 1/2 | live evidenced | default smoke and matrix summaries |
| Phase 3 response headers | implemented, live evidenced | response SPOE group and decision logs |
| Decision log | implemented | `decision.jsonl` |
| Audit-log plumbing | implemented | `audit.log` paths and live artifacts |
| Phase 4 / RESPONSE_BODY | bounded strict-abort evidence only | phase4 HAProxy example and runtime evidence |
| Synthetic matrix writer | not used | generated reports consume runtime summaries and snapshots |

## Aktuelle Zählungen

- Standard-HAProxy-Smoke: `55/55 PASS`.
- HAProxy force-all: `133 versucht / 104 PASS / 23 FAIL / 0 BLOCKED /
  6 NOT_EXECUTABLE`.

## Externe Basis

HAProxy dokumentiert SPOE/SPOP als den Mechanismus, der für die Kommunikation mit externen Geräten verwendet wird
Stream-Verarbeitungsagenten. Das Repository implementiert diesen Pfad mit einem lokalen SPOA
Laufzeit, die libmodsecurity lädt und HAProxy-Transaktionsvariablen zurückgibt.

## Verbleibende Erkenntnisse

- Ganzkörper-RESPONSE_BODY-Unterstützung ist nicht nachgewiesen.
- Multi-Worker, Langzeit-Cache-Druck und Paketierung bleiben in Produktion
  Härteaufgaben.
- Die dynamische Statuszuordnung für Störungen, die über die aktuellen HAProxy-Regeln hinausgeht, bleibt bestehen
  begrenzt.

Phase 4 / RESPONSE_BODY bleibt nicht promoted; begrenzte strikte Abbruchbeweise sind
documented/reported nur als Laufzeitbeweis.
