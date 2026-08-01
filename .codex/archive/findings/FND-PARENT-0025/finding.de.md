# FND-PARENT-0025 — Erlaubter Blocked-Status wird aus nicht vertrauenswürdiger Child-Ausgabe abgeleitet

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0025 |
| Titel / Title | Erlaubter Blocked-Status wird aus nicht vertrauenswürdiger Child-Ausgabe abgeleitet |
| Kategorie / Category | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P1 |
| Schweregrad / Severity | high |
| Konfidenz / Confidence | reproduced |
| Status | closed (archiviert) |
| Machbarkeitsstatus / Feasibility status | feasible_now |
| Release-Blocker / Release blocker | false |
| Security-Relevanz / Security relevance | true |

## Zusammenfassung / Summary

Der Status-Wrapper parste einen allowgelisteten Blocked-Reason-Marker aus
kombinierter Child-stdout- und stderr-Ausgabe. Ein Child mit Exit `77` konnte
diesen Marker ausgeben und einen fehlgeschlagenen Check in ein erfolgreiches
Workflow-Ergebnis verwandeln.

## Beobachtetes Verhalten / Observed behavior

`ci/tools/run-check-status.py:186-210` akzeptierte `CHECK_STATUS_REASON` aus
Child-Ausgabe, und `workflow_exit_code` wandelte einen allowgelisteten Reason
in Exit-Code `0` um. Kontrollierte stdout- und stderr-Fixtures erzeugten beide
`allowed_by_contract=true` und Workflow-Exit-Code `0`. Der betroffene Make-Call
ist `Makefile:1132-1134`.

## Erwartetes Verhalten / Expected behavior

Nur eine vom Parent verifizierte Prerequisite darf eine erlaubte
Blocked-Disposition erzeugen. Child-Ausgabe und Exit-Codes bleiben Diagnostik;
sie dürfen keinen erfolgreichen Workflow-Abschluss autorisieren.

## Auswirkung / Impact

Ein kompromittiertes, fehlerhaftes oder absichtlich permissives Child-Kommando
konnte einen erforderlichen Check-Fehler als erlaubten Environment-Block
maskieren.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `ci/tools/run-check-status.py`
- `Makefile`

### Symbole / Symbols

- `extract_block_reason`
- `workflow_exit_code`
- `test-optional-prerequisite-status`

### Herkunft / Provenance

- Source-Commit: `57d8753bc9db93d42eeb8be806798c7b394a8076`
- Flow: kontrollierte Child-stdout/stderr → `extract_block_reason` → Allowlist
  → `workflow_exit_code` → erfolgreiche Make-/CI-Disposition.

## Voraussetzungen / Preconditions

- Der Wrapper erlaubt `apache_development_prerequisite`.
- Das ausgeführte Child kann stdout oder stderr ausgeben und mit `77` enden.

## Reproduktion / Reproduction

1. Die aufbewahrte stderr-Spoof-Fixture mit dem allowgelisteten Reason durch
   `run-check-status.py` ausführen.
2. Die aufbewahrte stdout-Spoof-Fixture durch denselben Wrapper ausführen.
3. In beiden Fällen einen strukturierten Blocked-Status mit
   `allowed_by_contract=true` und Wrapper-Exit-Code `0` beobachten.

## Evidence / Evidence

- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-002-status-channel/validation_report.md`
  - Typ: `codex_security_validation_report`; SHA-256:
    `024f6956d07e3b787f1f4f1441bc107c4c9c15432a9337946a132262a7173218`
  - Kommando:
    `rtk env BUILD_ROOT=<task-run> PYTHONDONTWRITEBYTECODE=1 .venv/bin/python ci/tools/run-check-status.py --check status_spoof --allow-blocked-reason apache_development_prerequisite -- <controlled-fixture>`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`;
    beobachtet am `2026-07-18T09:22:02Z`; Aufbewahrung:
    `retained_task_evidence`.

- Delivery-Evidence:
  - Draft-PR: `56` (`agent/harden-evidence-status-channel`); exakter Head:
    `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92`.
  - Aufbewahrtes Delivery-Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
    (`draft_pr_delivery_status`, SHA-256
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`).
  - `rtk gh pr checks 56 --repo Easton97-Jens/ModSecurity-conector` endete
    mit `0` am `2026-07-18T11:13:55Z`: `33` Checks bestanden; CodeQL-Check-Run
    `88070191900` und SonarCloud-Check-Run `88070221640` bestanden.
- Fokussierte Security-Review-Evidence:
  `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/security_diff_review.md`
  prüfte denselben exakten Head und verzeichnete keinen neuen
  diff-spezifischen actionable Finding.
- Post-Merge-Master-Verifikation:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T103749Z-parent-pr-53-60-integration-a7b98a59/evidence/pr56-master-verification-a73c335.md`
  (`post_merge_master_reproduction_and_workflow_verification`, SHA-256
  `2260f2573467879d7c105dddfb9c64395308b021e1eccec6e53f358fef7c2562`).

## Grundursachenanalyse / Root-cause analysis

Der Statuskanal behandelte frei formatierte Child-Diagnostik als autoritative
Kontrolldaten und verband diese Daten mit der Allowlist-Entscheidung.

## Vorgeschlagene Remediation / Proposed remediation

Die Entscheidung über die erlaubte fehlende Prerequisite in eine explizite
strukturierte Parent-Disposition verschieben und Child-Text-Autorisierung
entfernen. Beliebige Child-Ausgabe nur als escaped Diagnostik behalten;
nicht klassifizierte Exit-`77`-Ergebnisse ablehnen.

## Remediation-Update / Remediation update

- Der finale PR-`56`-Head `cd0211bbefd4baef4ddee300ccf872e4d1ad9a53`
  verlagert die Autorisierung der erlaubten Blocked-Disposition in einen
  strukturierten Parent-Preflight und wurde als Master
  `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f` squash-gemergt.
- `origin/master` ist exakt dieser Commit und sein Tree entspricht dem finalen
  PR-Head. `tests/test_optional_prerequisite_status.py` bestand `20`
  fokussierte ursprüngliche Spoof-, Bypass- und legitime Kontrolltests;
  `allowed_by_contract=false` und ein nonzero Child-Exit `77` bleiben für
  Child-kontrollierte Ausgabe erzwungen.
- Die fokussierte Security-Diff-Review fand keinen neuen diff-spezifischen
  actionable Finding. Alle 14 beobachteten exakten Master-Workflows,
  einschließlich CodeQL, Security workflow lint, OpenSSF Scorecard und
  verified-report-governance, waren erfolgreich. Dieses Finding ist
  `verified`, nicht `closed`.

## Akzeptanzkriterien / Acceptance criteria

- Weder stdout- noch stderr-Marker-Text kann einen Child-Fehler in ein erlaubtes
  Blocked-Workflow-Ergebnis umwandeln.
- Eine echte vom Parent erkannte fehlende Apache-Development-Prerequisite bleibt
  ein explizites schema-valide Blocked-Ergebnis.
- Alle anderen Child-Fehler, einschließlich Exit `77`, bleiben nonzero.
- Der persistierte Status-Record verwendet die Parent-Disposition statt nicht
  vertrauenswürdigem Child-Text als Reason-Feld.

## Validierungsplan / Validation plan

- stdout- und stderr-Spoof-Fixtures vor dem Fix ergänzen und zeigen, dass beide
  danach scheitern.
- Einen Parent-erkannten Missing-Prerequisite-Kontrollfall und einen gewöhnlichen
  Child-Fehler-Kontrollfall ausführen.
- Die fokussierte Optional-Prerequisite-Status-Suite und einen Security-Diff-
  Scan ausführen.

## Regressionstests / Regression tests

- `tests/test_optional_prerequisite_status.py`
- Fokussierte stdout-/stderr-Spoof-Fixtures für `run-check-status.py`.

## Legitime Kontrolltests / Legitimate control tests

- Eine echte fehlende Apache-Development-Prerequisite erzeugt einen vom Parent
  authentifizierten erlaubten Blocked-Status.
- Ein gültiges Child-Kommando ist erfolgreich, ohne sich auf einen Status-Marker
  zu stützen.

## Abhängigkeiten / Dependencies

- Keine.

## Blocker / Blockers

- Keiner für die isolierte Parent-Status-Channel-Remediation.

## Verwandte Findings / Related findings

- `FND-PARENT-0024`

## Restrisiko / Residual risk

Der finale PR-`56`-Head `cd0211bbefd4baef4ddee300ccf872e4d1ad9a53` ist als
Master `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f` gemergt; der Master-Tree
entspricht dem finalen Head, die ursprüngliche 20-Test-Statuskanal-Suite
besteht, und alle beobachteten exakten Master-Workflows bestehen. Die
APXS-Selector-Konfiguration bleibt vertrauenswürdige Job-/Operator-Eingabe;
aktuelle produktive PR-Workflows leiten keine nicht vertrauenswürdige
PR-Eingabe dorthin. Bei Änderung dieser Vertrauensgrenze erneut bewerten. Es
wurde kein Risiko akzeptiert. Das Finding ist `verified`, nicht `closed`.

## Historie / History

- `2026-07-18T09:22:02Z`: `validated_stdout_and_stderr_spoofing` —
  unabhängige kontrollierte stdout- und stderr-Marker-Fixtures erhielten beide
  eine erlaubte Blocked-Workflow-Disposition.
- `2026-07-18T11:13:55Z`: `fixed_on_verified_pr_head` — PR `56` exakter Head
  `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92` bestand lokale Kontrollen, `33`
  GitHub-Checks, CodeQL, SonarCloud und fokussierte Security-Review. Das
  Finding bleibt bis Merge und Master-Rerun `fixed` statt `verified` oder
  `closed`.
- `2026-07-19T11:42:54Z`: `current_master_reproduction_verified` — PR `56`
  wurde als `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f` gemergt; sein
  Master-Tree entspricht dem finalen Head
  `cd0211bbefd4baef4ddee300ccf872e4d1ad9a53`. Die 20-Test-Suite für
  ursprüngliche Spoof-/Bypass-/legitime Kontrollfälle und der 13-Test-
  Workflow-Permission-Contract bestanden; alle 14 beobachteten exakten
  Master-Workflows bestanden. Das Finding war `verified` und ist nach Current-Master-Validierung und Archivierungsautorisierung durch den aktuellen Nutzer nun `closed`.

- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_validation` — `tests.test_optional_prerequisite_status` bestand auf Parent-Master `6ca7e1536ce7e93da68099db9c586b88852ff13e` als Teil der 144-Test-Control-Suite.
