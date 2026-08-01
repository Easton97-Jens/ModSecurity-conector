# FND-MRTS-0001 — MRTS-bezogene Assurance bleibt auf kontrollierte External-Copy-Evidence begrenzt

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-MRTS-0001` |
| Title / Titel | `MRTS-bezogene Assurance bleibt auf kontrollierte External-Copy-Evidence begrenzt` |
| Category / Kategorie | `mrts_gap` |
| Repository / Repository | `mrts` |
| Ownership / Ownership | `mrts_external_read_only` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Der originale MRTS-Checkout blieb read-only; aktuelle Schlussfolgerungen beruhen auf task-owned External-Copy-Controls und belegen keine uneingeschränkte Original-Checkout-Runtime-Assurance.

## Observed behavior / Beobachtetes Verhalten

Der originale MRTS-Checkout blieb read-only; aktuelle Schlussfolgerungen beruhen auf task-owned External-Copy-Controls und belegen keine uneingeschränkte Original-Checkout-Runtime-Assurance.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über blocked hinaus fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence begrenzt.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- None / Keine

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '496,517p;620,629p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:496-517,620-629`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '496,517p;620,629p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Ein autorisiertes read-only Assurance-Protokoll definieren, das die Integrität des originalen MRTS bewahrt und exakte Vor-/Nach-Boundary-Controls protokolliert.

## Acceptance criteria / Akzeptanzkriterien

- MRTS-related runtime claims identify external-copy versus original-checkout evidence precisely.
- The original MRTS SHA, status, and Gitlink controls pass before and after authorized work.

## Validation plan / Validierungsplan

- Run only an authorized external-copy harness.
- Retain Parent/Framework/MRTS boundary checks and distinguish assurance limitations from product defects.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-CROSS-0004`
- `FND-FRAMEWORK-0010`

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## Current task update / Aktueller Task-Stand

Read-only-Strukturinspektion fand `DetectionOnly`-Deklarationen, aber keine
aktuelle Runtime-Evidence beweist externe Overlay-Reihenfolge oder trennt das
angeforderte DetectionOnly-Detection-/Audit-Verhalten vom Blocking-Allow-/
Block-Verhalten. Der originale MRTS-Checkout, seine generierte Ausgabe,
Dependencies, sein Git-State und Gitlink wurden nicht geändert.

- Feasibility: `blocked_missing_evidence`
- Next action: ein Framework-owned External-Overlay muss DetectionOnly-
  Allow-/Detection- und Blocking-Allow-/Block-Controls samt Original-MRTS-
  Integrity-Evidence aufbewahren.
- Evidence: Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/039-phase-b-blocker-source-preflight.log`, SHA-256
  `bd04a04698986fd23669aef44c81eff94d1e7c1da2df367858c72257e1d17329`, Exit `0`.

## Test-only MRTS relevance assessment / MRTS-Relevanzbewertung nur für Tests

Der statische Source-Trace wurde am `2026-07-24T04:20:19Z` gegen Framework
`f98a8739cb13b583f23d646784b144e596b61441` und read-only MRTS
`13aa91291adea12d5c607fdd165d010fcfb1da78` erfasst. Ein finaler
Delta-Refresh am `2026-07-24T04:28:24Z` ergab das aktuelle Framework
`4c9753291d26d92f2d7e51ae425dedb79666fd5e`; dessen Delta zur statischen
Source-Revision ändert weder MRTS-Generation/-Import/-Runner-Pfade noch den
Framework-Gitlink, der weiterhin
`160000 13aa91291adea12d5c607fdd165d010fcfb1da78` ist.

- **Klassifikation:** nur bedingt relevant, wenn der opt-in-Framework-Pfad
  `with-mrts` ausgeführt wird. MRTS nur als Testkorpus vorzuhalten oder zu
  lesen ist kein Nachweis einer produktiven MRTS-Schwachstelle oder eines
  Connector-Runtime-Defekts; es begrenzt nur Provenance- und
  Assurance-Aussagen zu Test-Evidence.
- **Test-only-Pfad:** Das Framework ruft den MRTS-Generator in einem externen
  Build-Root auf, importiert generierte Regeln/Cases in einen privaten
  Framework-Runtime-Root und kann nur dann eine lokale Connector-Smoke-Runtime
  erreichen, wenn ein importierter Case aktiv und ausgewählt ist. Das normale
  `test`-Target verwendet kein MRTS; `test-with-mrts` ist opt-in.
- **Aktuelle Grenze:** Die statische Coverage-Zusammenfassung enthält `399`
  importierte Cases, `0` aktive/runtime-ausführbare Cases und `399`
  pending/unclassified Cases. Damit belegt die vorliegende Evidence nicht,
  dass dieser Korpus derzeit eine laufende Connector-Runtime ausführt.
- **Boundary-Ergebnis:** Kein Kommando dieses Tasks hat Parent, Framework
  oder originales MRTS geändert. Auf einen aufgezeichneten externen
  Framework-Fast-Forward folgte der obige Delta-Check; aktuelles Framework und
  MRTS sind sauber und ihr Gitlink stimmt weiterhin überein. Kein Generator,
  Importer, Test, Build oder write-capable MRTS-Kommando wurde ausgeführt. Das
  Finding bleibt `blocked` / `blocked_missing_evidence`, weil keine neue
  autorisierte External-Copy-Runtime-Evidence erzeugt wurde.
- **Aufbewahrte Evidence:** Run
  `20260724T042019Z-open-pr-triage-mrts-test-only-relevance-9786d0b7`,
  `evidence/mrts-test-only-relevance-assessment.md`, SHA-256
  `f06f7a8fb6bf8aa9ed18916f7dcc964b83f6b94ae74f0fda6683a27ad75ed75f`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — Structural Evidence allein autorisierte keine Profile-Assertion und keine MRTS-Mutation.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Das aufbewahrte aktive Source-Preflight-Log wurde in die kanonische Evidence aufgenommen; `blocked_missing_evidence` und die MRTS-read-only-Grenze bleiben unverändert.
- `2026-07-24T04:21:50Z`: test_only_relevance_assessed — Das Finding wurde nur für die opt-in-MRTS-Testausführung als bedingt relevant klassifiziert, nicht als nachgewiesene produktive Exposition. Der blocked-Status und die original-MRTS-read-only-Grenze bleiben unverändert.
- `2026-07-24T04:28:24Z`: framework_delta_refreshed — Ein aufgezeichneter externer Framework-Fast-Forward von `f98a8739cb13b583f23d646784b144e596b61441` nach `4c9753291d26d92f2d7e51ae425dedb79666fd5e` wurde geprüft; kein MRTS-Generation/-Import/-Runner-Pfad und kein Gitlink änderten sich, daher bleibt die Test-only-Klassifikation gültig.
