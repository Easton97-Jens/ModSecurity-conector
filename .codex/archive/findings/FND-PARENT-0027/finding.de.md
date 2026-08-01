# FND-PARENT-0027 — Phase-4-Evidence-Matching lässt ausgewählte Run- und Workload-Identität aus

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0027 |
| Titel / Title | Phase-4-Evidence-Matching lässt ausgewählte Run- und Workload-Identität aus |
| Kategorie / Category | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P1 |
| Schweregrad / Severity | high |
| Konfidenz / Confidence | confirmed |
| Status | closed (archiviert) |
| Machbarkeitsstatus / Feasibility status | feasible_now |
| Release-Blocker / Release blocker | false |
| Security-Relevanz / Security relevance | true |

## Zusammenfassung / Summary

Der Phase-4-Lifecycle-Checker akzeptierte Event-Records nur anhand von Rule-ID
und Phase. Kopierte Events mit fremder Run-ID, fremdem Connector oder fremdem
Profil bestanden dieselben First-Byte- und No-Full-Buffer-Checks wie ein
legitimes Apache-Event.

## Beobachtetes Verhalten / Observed behavior

`ci/checks/evidence/check-full-lifecycle-evidence.py:154-155` verwendet ein
Event-Prädikat, das weder Run-ID, Connector, Host-Profil, Integrationsmodus noch
Transaktionsidentität bindet. Drei temporäre Varianten mit fremder Identität und
ein legitimer Kontrollfall lieferten alle PASS für First-Byte- und
No-Full-Buffer-Checks.

## Erwartetes Verhalten / Expected behavior

Jedes promotete Phase-4-Event muss mit dem kanonischen Event-/Result-Schema die
ausgewählte Run-ID, den Connector, das Host-Profil, den Integrationsmodus und
die Transaktionsidentität binden. Fehlende oder nicht passende Identität
scheitert geschlossen.

## Auswirkung / Impact

Evidence aus einem anderen Run, Connector oder Profil kann als Nachweis für
einen ausgewählten Workload promoted werden und verletzt Run-Identity- und
Integrationsmodus-Integrität.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `ci/checks/evidence/check-six-connector-core-completion.py`
- `Makefile`
- `tests/test_full_lifecycle_evidence.py`
- `tests/test_full_lifecycle_gate_wiring.py`

### Symbole / Symbols

- `matching_events`
- `check_first_byte`
- `check_no_full_buffer`
- identity matcher
- `RUN_PARENT_FULL_LIFECYCLE_EVIDENCE_CHECK`
- `RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK`

### Herkunft / Provenance

- Source-Commit: `6bfdc66329fc68531b3f358cab25ef91b3d9a2a9`
- Parent-Remediation-Commits: `8b7b13b294fe4043fb4002c1cb96ba3de72986f8` und
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e`
- Exakter PR-#57-Head: `5f8949b1d98a98127b933e9f1d626b30e3291b59`
- Resultierender Parent-Master: `fde2e02a1cf2226f8e9106e663e05e9b2941357e`
- Flow: ausgewähltes Result → nur Phase/Rule-Event-Prädikat → First-Byte- oder
  No-Full-Buffer-PASS → promotete Phase-4-Evidence.

## Voraussetzungen / Preconditions

- Ein ausgewähltes Evidence-Verzeichnis enthält ein syntaktisch valides
  Phase-4-Event mit erwarteter Rule und Phase.
- Das Event stammt aus einem fremden Run, Connector, Profil oder
  Integrationsmodus.

## Reproduktion / Reproduction

1. Temporäre Evidence-Roots mit einem Apache-Selected-Run-Result und einem
   Event mit fremdem Run, fremdem Connector oder fremdem Profil bauen.
2. `check-full-lifecycle-evidence.py` mit `--run-id selected-run` und
   `--connectors apache` für `first-byte` und `no-full-buffer` ausführen.
3. PASS für jede fremde Variante und für den legitimen Kontrollfall beobachten.

## Evidence / Evidence

- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-004-phase4-identity/validation_report.md`
  - Typ: `codex_security_validation_report`; SHA-256:
    `70d07710bb9cab22be7cc64657e030302905ec99a4cfdfd1702a5ab8b930a645`
  - Kommando:
    `rtk env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python ci/checks/evidence/check-full-lifecycle-evidence.py --connector-root /root/git/ModSecurity-conector --evidence-root <temporary-root> --run-id selected-run --check <first-byte|no-full-buffer> --connectors apache`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`;
    beobachtet am `2026-07-18T09:22:02Z`; Aufbewahrung:
    `retained_task_evidence`.
- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
  - Typ: `draft_pr_delivery_status`; SHA-256:
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`
  - Kommando:
    `rtk gh pr checks 57 --repo Easton97-Jens/ModSecurity-conector`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`;
    beobachtet am `2026-07-18T11:13:55Z`; Aufbewahrung:
    `retained_task_evidence`.
- Run-ID: `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/pr57-5f8949b-current-head-verification.md`
  - Typ: `parent_pr_current_head_delivery_verification`; SHA-256:
    `cb6ae640643dec166ab77cb364ab61f01d79ce44cfaba99c97477d4d92820178`
  - Kommando: exakte PR-#57-Head-Check-Runs, CodeQL/Code-Scanning,
    SonarCloud-, Review-Thread- und Scoped-Diff-Inspektion.
  - Arbeitsverzeichnis:
    `/var/tmp/codex/worktrees/parent-evidence-phase4-binding`; Exit-Code `0`;
    beobachtet `2026-07-20T10:41:05Z`; Aufbewahrung
    `retained_task_evidence`.
- Run-ID: `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/pr57-master-fde2-phase4-identity-verification.md`
  - Typ:
    `exact_parent_master_phase4_identity_original_reproduction_and_legitimate_control`;
    SHA-256: `8c638de640cd2fd6b49c1c26ac026ac569aa119642fd51e31dec558667d11f0f`
  - Kommando: RTK-proxierte abgetrennte Exact-Master-Inspektion,
    Diff/Gitlink-Vergleich und fokussierte Parent-Lifecycle-/Wiring-/
    Six-Connector-Tests.
  - Arbeitsverzeichnis:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/tmp/parent-pr57-master-fde2`;
    Exit-Code `0`; beobachtet `2026-07-20T11:05:00Z`; Aufbewahrung
    `retained_task_evidence`.

## Grundursachenanalyse / Root-cause analysis

Das Event-Prädikat verwendete nur Rule-ID und Phase und wurde anfangs nicht von
den tatsächlichen Parent-Make-Targets für First-Byte, No-Full-Buffer und
Promotion aufgerufen. Ein stärkerer Identity-Matcher existierte im
Six-Connector-Completion-Checker, wurde aber weder wiederverwendet noch in die
Promotion verdrahtet.

## Vorgeschlagene Remediation / Proposed remediation

Das kanonische Identity-Matching-Muster wiederverwenden, vor Promotion alle
ausgewählten Identitätsfelder verlangen und die Parent-Targets für First-Byte,
No-Full-Buffer und Promotion mit ihren passenden Parent-Checks verdrahten. Die
genannten Foreign-Identity-Fixtures, eine legitime Kontrolle und einen
statischen Target-Wiring-Contract ergänzen.

## Akzeptanzkriterien / Acceptance criteria

- Events mit fremder Run-ID, fremdem Connector, fremdem Profil und fremdem
  Integrationsmodus können keine First-Byte- oder No-Full-Buffer-Checks
  erfüllen.
- Fehlende erforderliche Event-Identität scheitert geschlossen.
- Ein legitimes Event des ausgewählten Runs bleibt akzeptiert.
- Result-, Event-, Manifest- und Checksum-Identität werden konsistent geprüft,
  ohne Dateiname-/PASS-only-Entscheidung.
- Die tatsächlichen Parent-Make-Targets für First-Byte, No-Full-Buffer und
  Promotion rufen ihre passenden Parent-Identity-Checks auf.

## Validierungsplan / Validation plan

- Die genannten Fixtures mit fremder Identität und den validen Kontrollfall vor
  der Implementierungsänderung ergänzen.
- Die ursprünglichen Copied-Event-PoCs, einen alternativen Missing-Identity-Fall
  und den validen Kontrollfall nach dem Fix erneut ausführen.
- Fokussierte Lifecycle-Evidence-Tests, einen statischen Makefile-Target-
  Wiring-Contract und anwendbare Runtime-Harness-Contract-Tests ausführen.

## Regressionstests / Regression tests

- Fokussierte `check-full-lifecycle-evidence`-Tests für Run-, Connector-,
  Profil- und Integrationsmodus-Mismatch.
- Bestehende Six-Connector-Identity-Matcher-Kontrolltests.

## Legitime Kontrolltests / Legitimate control tests

- Ein ausgewählter Apache-Run mit identity-konsistentem nativen Event besteht
  First-Byte- und No-Full-Buffer-Checks.
- Eine vollständige Manifestkette mit passender Event-/Result-Identität bleibt
  akzeptiert.

## Abhängigkeiten / Dependencies

- Keine.

## Blocker / Blockers

`FND-CROSS-0006` ist unabhängig auf Framework-master verifiziert. Die separate
Runtime-Evidence-Lücke `FND-CROSS-0001` bleibt nachverfolgt und wird durch diese
Parent-only-Remediation weder ersetzt noch risikoakzeptiert. Das unabhängige
Parent-Finding `FND-SONAR-0001` blockiert die aggregierte Master-Delivery; es
eröffnet diese verifizierte Identity-Reparatur weder erneut noch wird es hier
risikoakzeptiert.

## Verwandte Findings / Related findings

- `FND-CROSS-0001`
- `FND-CROSS-0006`

## Remediation-Update / Remediation update

PR #57, exakter Head `5f8949b1d98a98127b933e9f1d626b30e3291b59`, wurde als
Parent-Master `fde2e02a1cf2226f8e9106e663e05e9b2941357e` squash-gemergt. Der
exakte resultierende Master enthält nur die geprüften acht Parent-Dateien und
bewahrt Framework-Gitlink `efdbcbd98afeed0f39f8912ce1140aaa5742f507`. In einem
sauberen abgetrennten Worktree bestanden alle 20 fokussierten Lifecycle-/
Wiring-/Six-Connector-Tests: fremde Run-, Connector-, Profil-,
Integrationsmodus-, Transaktions- und Missing-Identity-Varianten scheitern
über beide First-Byte- und No-Full-Buffer-Pfade geschlossen, während die
ausgewählte legitime Apache-Kontrolle akzeptiert bleibt. Das Finding ist
verified, nicht closed.

## Restrisiko / Residual risk

Der exakte Parent-Master reproduziert die ursprünglichen und alternativen
kopierten/fehlenden Identity-Fälle fail closed und bewahrt die ausgewählte
legitime Apache-Kontrolle. `FND-PARENT-0027` ist verified, nicht closed.
`FND-CROSS-0006` ist separat verifiziert und `FND-CROSS-0001` bleibt eine
eigenständige Runtime-Evidence-Grenze. Der unabhängige Parent-Sonar-Release-
Blocker `FND-SONAR-0001` verhindert aggregate `master_integration_complete`,
eröffnet diese verifizierte Phase-4-Identity-Reparatur aber nicht erneut. Es
wurde kein Risiko akzeptiert.

## Historie / History

- `2026-07-18T09:22:02Z`: `validated_foreign_identity_promotion` — Events mit
  fremdem Run, Connector und Profil bestanden die ausgewählten Apache-Phase-4-
  Checks neben dem legitimen Kontrollfall.
- `2026-07-18T11:13:55Z`: `fixed_parent_gate_wiring_after_security_review` —
  unabhängige Review fand, dass der initiale Identity-Matcher nicht in die
  tatsächlichen Parent-Promotion-Targets verdrahtet war. Follow-up `0124b0d`
  verdrahtete First-Byte-, No-Full-Buffer- und Promotion-Checks, bestand 20
  fokussierte Tests und 33 PR-Checks und erhielt eine saubere Re-Review.
  `FND-CROSS-0006` erfasst die separate Framework-autoritative Grenze.
- `2026-07-20T10:41:05Z`: `fixed_current_pr_57_head_validated` — exakter Head
  `5f8949b1d98a98127b933e9f1d626b30e3291b59` hat aktuelle terminale Checks,
  CodeQL, SonarCloud, null offene Code-Scanning-Alerts, keinen Review-Thread
  und einen geprüften Parent-only-Diff. Das Finding bleibt fixed bis
  autorisiertem Merge und Master-Reproduktion.
- `2026-07-20T11:05:00Z`:
  `verified_on_resulting_parent_master_after_original_reproduction` — Source-
  Head `5f8949b...` ist als exakter Parent-Master `fde2e02...` gemergt. Ein
  sauberer abgetrennter Master-Worktree bestand 20 fokussierte Lifecycle-/
  Wiring-/Six-Connector-Tests: fremde Run-, Connector-, Profil-,
  Integrationsmodus-, Transaktions- und Missing-Identity-Varianten scheitern
  auf beiden First-Byte- und No-Full-Buffer-Pfaden geschlossen, während
  ausgewählte Apache-Evidence akzeptiert bleibt. Der Framework-Gitlink bleibt
  `efdbcbd...`. Der unabhängige Parent-Sonar-Fehler `FND-SONAR-0001` lässt die
  aggregierte Delivery partial, eröffnet dieses verifizierte Finding aber nicht
  erneut.

## Abschluss / Closure

Der aktuelle Nutzer autorisierte Abschluss und Archivierung, nachdem `tests.test_full_lifecycle_evidence` und `tests.test_full_lifecycle_gate_wiring` auf Parent-Master `6ca7e1536ce7e93da68099db9c586b88852ff13e` als Teil der 144-Test-Control-Suite bestanden. `FND-SONAR-0001` bleibt ein unabhängiger aktiver Quality-Gate-Blocker.
