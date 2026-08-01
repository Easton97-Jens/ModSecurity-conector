# FND-PARENT-0024 — Verified-Report-Workflow akzeptiert Governance-only-Validierung ohne striktes Runtime-Evidence-Gate

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0024 |
| Titel / Title | Verified-Report-Workflow akzeptiert Governance-only-Validierung ohne striktes Runtime-Evidence-Gate |
| Kategorie / Category | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P1 |
| Schweregrad / Severity | high |
| Konfidenz / Confidence | reproduced |
| Status | fixed |
| Machbarkeitsstatus / Feasibility status | feasible_now |
| Release-Blocker / Release blocker | true |
| Security-Relevanz / Security relevance | true |

## Zusammenfassung / Summary

Der Verified-Report-Workflow rief nur ein Governance-only-Report-Layout-Target
auf. Er konnte deshalb erfolgreich sein, während das strikte
Runtime-Evidence-Gate fehlschlug; dadurch konnte Governance mit verifizierter
Runtime-Evidence verwechselt werden.

## Beobachtetes Verhalten / Observed behavior

Auf Parent-Revision `c8ca0d92b630c18232b881855c4f5d1482568ea6` rief
`.github/workflows/verified-report-governance.yml:41-44`
`make report-governance` auf. `Makefile:388-390` delegiert dieses Target an
`check-generated-report-layout.py --governance-only`; es ruft nicht das strikte
`verified-report-evidence-gate` aus `Makefile:392-393` auf. Das Governance-Target
war erfolgreich, während der strikte Checker veraltete oder fehlende
Runtime-Evidence-Inputs ablehnte.

## Erwartetes Verhalten / Expected behavior

Ein Workflow, der verifizierte Report-Evidence repräsentiert, muss nach
Governance das vorhandene strikte Runtime-Evidence-Gate ausführen.
Governance-only-Validierung darf verfügbar bleiben, kann aber keinen
Runtime-Evidence-Claim erzeugen.

## Auswirkung / Impact

Ein veralteter, unvollständiger oder fehlender Runtime-Manifest-Satz konnte
hinter einem erfolgreichen Governance-only-Ergebnis verborgen werden und damit
Release-Evidence und Report-Integrität untergraben.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `.github/workflows/verified-report-governance.yml`
- `Makefile`
- `ci/checks/documentation/check-generated-report-layout.py`

### Symbole / Symbols

- `report-governance`
- `verified-report-evidence-gate`
- `check_generated_report_layout`

### Herkunft / Provenance

- Source-Commit: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
- Flow: Workflow → `make report-governance` → `--governance-only`-Checker;
  striktes Gate existierte, war aber nicht verdrahtet.

## Voraussetzungen / Preconditions

- Der Workflow läuft gegen Reports mit gültigem Governance-Layout.
- Strikte Runtime-Evidence ist veraltet, unvollständig oder wird aus einem
  anderen Evidence-Integritätsgrund abgelehnt.

## Reproduktion / Reproduction

1. `make report-governance` mit den dokumentierten externen Task-Roots ausführen
   und Erfolg beobachten.
2. Den strikten Report-Evidence-Checker gegen denselben Checkout ausführen und
   seine Ablehnung veralteter oder fehlender Runtime-Evidence beobachten.
3. Vor der Remediation den fokussierten Workflow-Contract-Test ausführen, der
   `make verified-report-evidence-gate` verlangt, und einen Fehler beobachten.

## Evidence / Evidence

- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-001-governance-gate/validation_report.md`
  - Typ: `codex_security_validation_report`; SHA-256:
    `b8f6e7b7ba71fccef38a2119938491748475498b62560ceb7b883b303eaebfba`
  - Kommando: `rtk make report-governance`; das strikte Checker-Kommando und
    Ergebnis sind im Validierungsbericht aufbewahrt.
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; beobachtet am
    `2026-07-18T09:22:02Z`; Aufbewahrung: `retained_task_evidence`.

## Grundursachenanalyse / Root-cause analysis

Der Workflow verdrahtete ein Governance-only-Target, ließ aber das vorhandene
strikte Runtime-Evidence-Target aus. Diese Targets erzwingen unterschiedliche
Trust Boundaries.

## Vorgeschlagene Remediation / Proposed remediation

Das vorhandene strikte Target zum Verified-Workflow hinzufügen, Governance als
Begleitcheck beibehalten und Reihenfolge sowie beide Target-Namen mit einem
fokussierten Test abdecken. Keine Reports regenerieren und den strikten Checker
nicht abschwächen.

## Akzeptanzkriterien / Acceptance criteria

- Der Workflow ruft `make verified-report-evidence-gate` nach
  `make report-governance` auf.
- Ein Report ohne akzeptierte Runtime-Manifeste kann kein erfolgreiches
  Verified-Evidence-Workflow-Ergebnis erzeugen.
- Ein vollständiger Runtime-Evidence-Run mit konsistenten Prüfsummen bleibt für
  Verifikation berechtigt.
- Kein Report wird von Hand editiert, damit das strikte Gate besteht.

## Validierungsplan / Validation plan

- Den Pre-Fix-Workflow-Contract-Fehler aufbewahren und denselben Test nach der
  Source-Änderung erneut ausführen.
- Workflow-/YAML-Validierung ausführen, wenn verfügbar.
- Separate Ergebnisse für Report-Governance und das strikte Evidence-Gate
  beibehalten.
- PR-CI-, CodeQL-, SonarQube-Cloud- und Exact-Head-Evidence einholen, bevor der
  Status zu `verified` fortschreiten kann.

## Regressionstests / Regression tests

- `tests/test_ci_security_workflows.py`
- Fokussierte Strict-Gate-Tests für fehlende Runtime-Manifeste und inkonsistente
  Prüfsummen.

## Legitime Kontrolltests / Legitimate control tests

- Ein vollständiger aktueller Run mit konsistenten Manifesten und Prüfsummen
  besteht das strikte Gate.
- Governance-only-Layout-Checks bleiben verfügbar, repräsentieren aber keine
  Runtime-Verifikation.

## Abhängigkeiten / Dependencies

- `FND-CROSS-0001` muss abgeglichen werden, bevor das aktuell veraltete
  Repository release-verifiziert werden kann.

## Blocker / Blockers

- FND-CROSS-0001 bleibt ungelöst. PR 55 schlägt am neu verdrahteten strikten
  Runtime-Evidence-Gate für veraltete kritische Inputs korrekt fehl und ist
  daher kein verifizierter PR.

## Verwandte Findings / Related findings

- `FND-CROSS-0001`
- `FND-CROSS-0005`

## Restrisiko / Residual risk

PR-55-Head 42b31f1c84c0c915a5cb65119714613fbf3e0c40 enthält das strikte Gate
und bestand CodeQL sowie SonarCloud. Sein erwartetes report-governance-
Fehlschlagen belegt, dass FND-CROSS-0001 ungelöst ist. Dieses Finding ist
fixed, nicht verified oder closed, weil kein grüner aktueller Runtime-Evidence-
Run und kein Master-Rerun existieren. Es wurde kein Risiko akzeptiert.

## Remediation-Update / Remediation update

- Draft-PR 55 verdrahtet make verified-report-evidence-gate nach
  make report-governance.
- Der fokussierte Workflow-Test bestand (6 Tests), YAML-Parse und Diff-Check
  bestanden, und die fokussierte Security-Review fand keinen Bypass.
- Delivery-Evidence SHA-256:
  70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366.
- Es erfolgte kein Merge.

## Historie / History

- `2026-07-18T09:22:02Z`: `validated_and_root_cause_remediation_started` —
  Governance-only-Erfolg und strikte Runtime-Evidence-Ablehnung wurden
  reproduziert; die isolierte Parent-Workflow-Remediation startete nach einem
  Pre-Fix-Workflow-Contract-Fehler.
- 2026-07-18T11:13:55Z: fixed_strict_gate_wired_cross_evidence_blocked —
  PR 55 verdrahtete das strikte Gate und bestand die fokussierte Review, aber
  seine erwartete CI-Ablehnung bewahrt FND-CROSS-0001 als Release-Blocker.
