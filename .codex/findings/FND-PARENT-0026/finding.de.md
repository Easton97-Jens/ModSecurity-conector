# FND-PARENT-0026 — Runtime-Pfad-Policy vertraut caller-kontrollierten Projekt-Roots als Confinement-Ankern

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0026 |
| Titel / Title | Runtime-Pfad-Policy vertraut caller-kontrollierten Projekt-Roots als Confinement-Ankern |
| Kategorie / Category | security_hardening |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P2 |
| Schweregrad / Severity | medium |
| Konfidenz / Confidence | reproduced |
| Status | fixed |
| Machbarkeitsstatus / Feasibility status | feasible_now |
| Release-Blocker / Release blocker | false |
| Security-Relevanz / Security relevance | true |

## Zusammenfassung / Summary

Runtime-Pfad-Helper akzeptierten veränderliche Projekt-Root-Werte als
vertrauenswürdige Containment-Anker. Setzen auf `/` machte Nachfahren von `/etc`
und `/root` Runtime-erlaubt; der Lifecycle-Resolver akzeptierte außerdem breite
`/root/poc-*`-Basen.

## Beobachtetes Verhalten / Observed behavior

`ci/lib/runtime_path_utils.py:50-98` leitet vertrauenswürdige Roots aus
veränderlichen Environment-Inputs ab. Ein nebenwirkungsfreier Probe
klassifizierte `/etc/evidence-escape` und `/root/evidence-escape` als erlaubt,
wenn Projekt-Roots `/` waren. Der Lifecycle-Resolver akzeptierte fünf
`/root/poc-*`-Basen ohne Schreibvorgang.

## Erwartetes Verhalten / Expected behavior

Projekt-Roots können beliebige Systempfad-Nachfahren nicht deklassifizieren.
Invocation-eigene Runtime-Basen müssen kanonische sichere Nachfahren eines
validierten externen Task-Roots sein, während Source-Roots getrennte read-only
Inputs bleiben.

## Auswirkung / Impact

Ein lokaler oder zukünftiger Caller mit Kontrolle über Pfad-Inputs kann das
beabsichtigte Containment umgehen und Lifecycle-Artefakte in breite
System-User-Locations lenken. Aktuelle Workflows binden Roots an Runner-
Temporary-Locations; untrusted Pull-Request-Expression-Reachability wurde nicht
bewiesen.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/common/resolve-runtime-paths.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/checks/evidence/check-runtime-producer-readiness.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_runtime_path_policy.py`
- `tests/test_resolve_runtime_paths.py`
- `tests/test_runtime_producer_readiness_path_policy.py`

### Symbole / Symbols

- `runtime_path_allowed`
- `resolve_runtime_paths`
- `REPO_ROOT`
- `CONNECTOR_ROOT`
- `FRAMEWORK_ROOT`

### Herkunft / Provenance

- Source-Commits: `46f35ad40822081e5b4c8d5c120dd41e2a74344f`,
  `614c80493b6ebd25a17e1d27979071e5e30584d4`
- Flow: caller-kontrollierte Projekt-Roots → positive Helper-Containment-
  Entscheidung → Lifecycle-Resolver → spätere Runtime-Artefakt-Writes.

## Voraussetzungen / Preconditions

- Ein Caller kann Projekt- oder Lifecycle-Root-Inputs liefern.
- Helper/Resolver wird vor einem Runtime-Artefakt-Write verwendet.

## Reproduktion / Reproduction

1. Den nebenwirkungsfreien Helper mit `REPO_ROOT=/`, `CONNECTOR_ROOT=/` und
   `FRAMEWORK_ROOT=/` aufrufen; `/etc/evidence-escape` und
   `/root/evidence-escape` untersuchen.
2. Den Lifecycle-Resolver mit `/root/poc-*`-Basen ausführen und erfolgreiche
   Auflösung ohne Writes beobachten.
3. Einen eigenen externen Task-Root als legitimen Kontrollfall verwenden.

## Evidence / Evidence

- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-003-path-confinement/validation_report.md`
  - Typ: `codex_security_validation_report`; SHA-256:
    `f4468abc4b55ead3129e62093cbe85e3022800f5a99e903b6f0ad1e1c1a457f3`
  - Kommando: `rtk env PYTHONPATH=/root/git/ModSecurity-conector/ci/lib
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python <side-effect-free path probe>`;
    Resolver-Probes sind mit dem Bericht aufbewahrt.
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`;
    beobachtet am `2026-07-18T09:22:02Z`; Aufbewahrung:
    `retained_task_evidence`.

- Delivery-Evidence:
  - Draft-PR: `58` (`agent/harden-evidence-path-confinement`); exakter Head:
    `4f028f911807def8b771faaa3b16c58a513e0385`.
  - Aufbewahrtes Delivery-Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
    (`draft_pr_delivery_status`, SHA-256
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`).
  - `rtk gh pr checks 58 --repo Easton97-Jens/ModSecurity-conector` endete
    mit `0` am `2026-07-18T11:13:55Z`: `33` Checks bestanden; CodeQL-Check-Run
    `88072083077` und SonarCloud-Check-Run `88072115412` bestanden.
- Fokussierte Security-Review-Evidence:
  `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/security_diff_review.md`
  prüfte denselben exakten Head und verzeichnete keinen neuen
  diff-spezifischen actionable Finding.

## Grundursachenanalyse / Root-cause analysis

Die Policy verwendet caller-kontrollierte Projekt-Roots als positive
Autorisierungsanker, statt beschreibbare Runtime-Pfade auf einen einzigen
invocation-eigenen externen Root zu beschränken.

## Vorgeschlagene Remediation / Proposed remediation

Breite/System-Basen und environment-abgeleitete Projekt-Roots für beschreibbare
Runtime-Pfade ablehnen. Jede beschreibbare Lifecycle-Basis gegen einen
validierten Invocation-Root auflösen; explizite read-only Source-Root-Behandlung
getrennt beibehalten.

## Remediation-Update / Remediation update

- PR `58` (`agent/harden-evidence-path-confinement`) am exakten Head
  `4f028f911807def8b771faaa3b16c58a513e0385` folgt auf die Commits
  `1ee0ba3718ef35c210ed959988460d03db21d46c` und
  `4f028f911807def8b771faaa3b16c58a513e0385` und beschränkt beschreibbare
  Runtime-Pfade auf den validierten Invocation-Root.
- Fokussierte Runtime-Path-Tests bestanden `13`; Shell-Syntax- und Diff-Checks
  bestanden. Die vollständige Runtime-Path-Policy-Shell-Hälfte ist nur
  blockiert, weil `modules/ModSecurity-test-Framework/ci/lib/common.sh` im
  isolierten Parent-Worktree fehlt; kein Framework-Inhalt wurde geändert oder
  umgangen.
- Die fokussierte Security-Diff-Review fand keinen neuen diff-spezifischen
  actionable Finding. Dieses Finding ist `fixed`, nicht `verified` oder
  `closed`: Es gab keinen Merge und keinen Master-Rerun.

## Akzeptanzkriterien / Acceptance criteria

- `/`, `/etc`, `/root` und ihre Nachfahren können durch Projekt-Root-Werte nicht
  zu beschreibbaren Runtime-Roots werden.
- Symlink-, Traversal- und Mixed-Root-Escapes scheitern nach Kanonisierung
  geschlossen.
- Ein eigenes sicheres Run-Layout unter dem task-eigenen externen Root bleibt
  akzeptiert.
- Aktuelle workflow-eigene Runner-Temporary-Layouts bleiben unterstützt.

## Validierungsplan / Validation plan

- Broad-Root- und Path-Escape-Fixtures vor dem Source-Fix ergänzen, einschließlich
  einer lexikalischen Traversal-/Symlink-Alternative.
- Helper- und Lifecycle-Resolver-Negativ-/Kontrolltests ohne Writes in
  Systempfade ausführen.
- Fokussierte Runtime-Path- und Lifecycle-Suites sowie einen Security-Diff-Scan
  ausführen.

## Regressionstests / Regression tests

- Fokussierte `runtime_path_utils`-Tests für Broad-Project-Root-Ablehnung.
- Fokussierte `resolve-runtime-paths`-Tests für kanonisches Task-Root-
  Containment.

## Legitime Kontrolltests / Legitimate control tests

- Ein sicheres Connector-Run-Layout unter einem task-eigenen externen Root wird
  erfolgreich aufgelöst.
- Read-only-Projekt-Source-Pfade bleiben dort nutzbar, wo sie explizit benötigt
  werden.

## Abhängigkeiten / Dependencies

- Keine.

## Blocker / Blockers

- Keiner für die isolierte Parent-Hardening-Änderung.

## Verwandte Findings / Related findings

- Keine.

## Restrisiko / Residual risk

PR `58` exakter Head `4f028f911807def8b771faaa3b16c58a513e0385` bestand `33`
Checks, CodeQL, SonarCloud, fokussierte Negativkontrollen und Security-Review.
Die vollständige lokale Shell-Policy-Hälfte bleibt durch fehlendes
`modules/ModSecurity-test-Framework/ci/lib/common.sh` im isolierten
Parent-Worktree blockiert; kein Framework-Inhalt wurde geändert. Es gab keinen
Merge und keinen Master-Rerun. Das Finding bleibt `fixed`, nicht `verified`
oder `closed`, und es wurde kein Risiko akzeptiert.

## Historie / History

- `2026-07-18T09:22:02Z`: `validated_side_effect_free_path_escape` —
  kontrollierte Root-Werte umgingen Helper-Containment für Systempfad-Nachfahren;
  aktuelle PR-Expression-Reachability wurde nicht nachgewiesen.
- `2026-07-18T11:13:55Z`: `fixed_on_verified_pr_head` — PR `58` exakter Head
  `4f028f911807def8b771faaa3b16c58a513e0385` bestand `33` GitHub-Checks,
  CodeQL, SonarCloud, fokussierte Negativ-/Kontrolltests und Security-Review.
  Das Finding bleibt bis Merge und Master-Rerun `fixed` statt `verified` oder
  `closed`.
- `2026-07-18T11:51:43Z`: `corrected_affected_file_provenance` —
  korrigierte den nicht existierenden Pfad
  `ci/runtime/lifecycle/resolve-runtime-paths.py` zu
  `ci/runtime/common/resolve-runtime-paths.py` und erfasste die
  tatsächlichen Parent-Checks und fokussierten Testdateien aus PR `58`.
