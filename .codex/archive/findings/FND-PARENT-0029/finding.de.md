# FND-PARENT-0029 — SonarQube Cloud meldet inkonsistente Rückgabeformen der Apache-Kandidaten

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0029 |
| Titel / Title | SonarQube Cloud meldet inkonsistente Rückgabeformen der Apache-Kandidaten |
| Kategorie / Category | sonarqube_finding |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P1 |
| Schweregrad / Severity | not_applicable |
| Konfidenz / Confidence | confirmed |
| Status | closed |
| Machbarkeitsstatus / Feasibility status | feasible_now |
| Release-Blocker / Release blocker | true |
| Security-Relevanz / Security relevance | false |

## Zusammenfassung / Summary

Die SonarQube-Cloud-PR-Analyse für Draft-PR #56 meldet einen offenen
task-eigenen `python:S8495`-Code-Smell in `apache_development_candidates()`.
Das Quality Gate ist OK, aber Rückgabepfade mit null, einem und zwei oder mehr
Tuple-Elementen blockieren `verified_pr` nach der lokalen Sonar-Delivery-Policy.

## Beobachtetes Verhalten / Observed behavior

Am PR-56-Head `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92` gibt
`ci/tools/run-check-status.py:222-234` abhängig von einer parent-kontrollierten
Environment-Auswahl `(value,)`, `tuple(shlex.split(...))`, `()` oder
`("apxs", "apxs2")` zurück. SonarQube-Cloud-Issue
`AZ90uTmr7VSiD7VvMb8Y` ist an Zeile 222 mit Rule `python:S8495`, Schweregrad
`MAJOR` und `HIGH`-Auswirkungen auf Reliability und Maintainability `OPEN`.

## Erwartetes Verhalten / Expected behavior

Die Parent-eigene Kandidatenauswahl bewahrt die dokumentierte Priorität
`APXS_BIN` → `APXS` → `CI_APXS_BIN_CANDIDATES` → Default, weist aber genau eine
Kandidatensequenz zu und gibt sie über einen kanonischen Pfad zurück. Der
aktuelle exakte PR-Head darf kein offenes task-eigenes Sonar-Issue haben.

## Auswirkung / Impact

Die fokussierten Verhaltenskontrollen bestehen aktuell, aber das task-eigene
externe Reliability-/Maintainability-Issue blockiert die verlangte
`verified_pr`-Disposition. Dies ist keine Wiederkehr des in
`FND-PARENT-0025` erfassten Security-Bypasses durch nicht vertrauenswürdige
Child-Ausgabe.

## Betroffene Dateien und Symbole / Affected files and symbols

- `ci/tools/run-check-status.py` — `apache_development_candidates`,
  `apache_development_available` und `main`.
- `tests/test_optional_prerequisite_status.py` — fokussierte Regression und
  Legitimate-Control-Coverage.
- Source-Commit: `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92`.
- Flow: `Makefile:1134` → `run-check-status.py` →
  `apache_development_available()` → `apache_development_candidates()` →
  Parent-Optional-Prerequisite-Status-Disposition.

## Evidence / Evidence

- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/FND-PARENT-0029-sonar-return-shape/sonar-open-issue.json`
  - Typ: `sonarqube_cloud_pr_issue_query`; SHA-256:
    `e0f0bbcb9f9895461c07a4453471ed016acc9208e8fc974e9c5209f0596d7a71`
  - Kommando:
    `rtk curl -fsS 'https://sonarcloud.io/api/issues/search?projectKeys=Easton97-Jens_ModSecurity-conector&pullRequest=56&resolved=false&ps=100'`
  - Exit-Code: `0`; beobachtet `2026-07-18T12:40:03Z`; Aufbewahrung:
    `retained_task_evidence`.

## Grundursachenanalyse / Root-cause analysis

Die Statuskanal-Remediation führte mehrere semantisch valide, aber strukturell
divergierende Tuple-Rückgaben ein. SonarQube Cloud markiert die unterschiedliche
Tuple-Arity konservativ als Reliability- und Maintainability-Fallstrick.
Child-Ausgabe wird nicht als Kontrolldatum verwendet, und es wurde keine
Wiederkehr eines Security-Bypasses beobachtet.

## Vorgeschlagene Remediation / Proposed remediation

Eine explizit typisierte lokale Kandidatensequenz und genau eine Rückgabe
verwenden, Auswahlpriorität und Verhalten bei fehlerhafter Konfiguration
bewahren sowie eine AST-Single-Return-Regression und eine reale konfigurierte
APXS-Parent-Preflight-Kontrolle ergänzen. Sonar nicht unterdrücken, die Rule
nicht deaktivieren und die Statuskanal-Trust-Boundary nicht verändern.

## Akzeptanzkriterien / Acceptance criteria

- `apache_development_candidates()` gibt seine Sequenz genau einmal zurück.
- Bestehende Kandidatenpriorität und Semantik bei fehlerhafter Konfiguration
  bleiben erhalten.
- Die fokussierte Suite deckt die kanonische Rückgabe und eine valide
  konfigurierte-APXS-Kontrolle ab.
- Der exakte #56-PR-Head hat kein offenes task-eigenes SonarCloud-Issue, und es
  gab keine Scanner-Suppression, Rule-Deaktivierung oder Risikoakzeptanz.
- Child-stdout und -stderr können weiterhin keinen erlaubten Blocked-Status
  autorisieren.

## Validierungsplan / Validation plan

1. `tests.test_optional_prerequisite_status` einschließlich AST- und
   konfigurierte-APXS-Kontrollen ausführen.
2. Den Diff auf Verhaltensänderung oder Statuskanal-Trust-Regression prüfen.
3. Nur den isolierten #56-Follow-up pushen; Gleichheit von lokalem, Remote- und
   PR-Head, Exact-Head-CI, Sonar-Issues und Quality Gate prüfen.

## Verwandte Findings / Related findings

- `FND-PARENT-0025` — andere Grundursache: Nicht vertrauenswürdige Child-Ausgabe
  konnte einen erlaubten Blocked-Status autorisieren.

## Restrisiko / Residual risk

Die Statuskanal-Remediation ist lokal behoben, aber der Draft-PR darf nicht
`verified_pr` heißen, bis der isolierte Return-Shape-Follow-up einen sauberen
Exact-Head-SonarCloud- und CI-Zyklus erhält. Es wird kein Risiko akzeptiert.

## Historie / History

- `2026-07-18T12:40:03Z`: `sonarcloud_task_owned_issue_triaged` — direkte
  SonarQube-Cloud-PR-API-Evidence bestätigte das offene Issue
  `AZ90uTmr7VSiD7VvMb8Y` am #56-Source-Commit. Keine Suppression oder
  Risikoakzeptanz ist autorisiert.

## Geschlossene Disposition — 2026-08-01

[PR #56](https://github.com/Easton97-Jens/ModSecurity-conector/pull/56) wurde
normal als `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f` nach `master` gemergt;
dieser Merge ist vom aktuellen `origin/master`
`59aba762f2d852fd917079ca8519e4ea7f49169c` erreichbar. Der aktuelle Source
hat einen kanonischen Candidate-Return, die zwei spezifizierten Optional-
Prerequisite-Regressions- und legitimen Control-Tests bestehen, und aktuelle
SonarCloud-Abfragen liefern sowohl für den Original-Key als auch für die
ungelöste `python:S8495`-Menge ein leeres Ergebnis. Es wurde keine Suppression,
Rule-Deaktivierung oder Risikoakzeptanz verwendet.
