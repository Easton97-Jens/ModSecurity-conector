# FND-SONAR-0006 — Exakter Parent-PR-#59-Head hat acht aufgabeneigene SonarQube-Cloud-Maintainability-CODE_SMELLs

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-SONAR-0006 |
| Kategorie | sonarqube_finding |
| SonarQube-Cloud-Klassifikation | maintainability |
| Repository / Ownership | parent / parent |
| Priorität | P2 |
| Security-Schwere | not_applicable |
| Konfidenz | validated |
| Status | verified (nicht closed) |
| Feasibility | already_fixed |
| Release-Blocker | false |
| Security-relevant | false |
| Connector / Protokoll / Profil | null / null / null |
| Finale Disposition | verified_on_parent_master_5a22cbf5206dbc2b7f53a9f961d72e37d567e188_not_closed |

Die SonarQube-Cloud-Scanner-Labels sind sechs CRITICAL- und zwei MAJOR-Beobachtungen. Sie sind ausschließlich Scanner-Labels und keine Security-Schweren: Dies ist ein nicht-sicherheitsrelevantes Maintainability-Finding mit severity not_applicable, security_relevant false und release_blocker false.

## Zusammenfassung

Die zurückgehaltene SonarQube-Cloud-Issue-Abfrage für Parent-PR #59, Head 841d5d66ba6db852cbc3c0a906e56d74583beb89 gegen Basis 6f80c90592fdd1f2eb990fe1514fdfc4efbf01e8, meldet acht aufgabeneigene CODE_SMELL-Beobachtungen auf geänderten Parent-Zeilen. Das Quality Gate ist OK; alle Beobachtungen sind nicht-sicherheitsrelevante Maintainability-Findings. Der exakte Source b9b22cc36958ba506278f3aa3fbc1d383ea6a151 lieferte eine verhaltenserhaltende, nicht-suppressive Remediation und wurde geschützt squash als Parent-Master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 gemergt. Der zurückgehaltene Post-Merge-Receipt erfasst die erforderlichen Controls und null verbleibende ursprüngliche Keys auf master; dieses Finding ist verified, nicht closed.

## Beobachtetes und erwartetes Verhalten

Die Exact-Head-Issue-Abfrage meldet total=8, open_security_hotspots=0 und open_vulnerabilities=0. Der zurückgehaltene Receipt klassifiziert jedes Resultat als SonarQube-Cloud-CODE_SMELL-Maintainability-Finding, und seine Ownership-Bewertung besagt, dass alle Komponenten geänderte Parent-Pfade und alle gemeldeten Zeilen im aktuellen PR-Diff liegen. Er erfasst Quality Gate OK, neue Reliability-, Security- und Maintainability-Ratings von 1, duplicated-lines density 0.0 und security-hotspots reviewed 100.0.

Die fokussierte PR-#59-Remediation auf b9b22cc36958ba506278f3aa3fbc1d383ea6a151 bewahrt beobachtbares Verhalten und reduziert zugleich die regelbezogenen Complexity-, Nesting-, Exception-Test- und Duplicate-Literal-Smells. Ihr frisches PR-Quality-Gate war OK, und die Resulting-Master-Abfrage auf 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 weist alle acht Beobachtungen als null verbleibend aus, ohne NOSONAR, Regel-Deaktivierung, Exclusions, Quality-Gate-Änderung oder False-Positive-Disposition.

## Auswirkung

Das Quality Gate bleibt bestanden, und diese Beobachtungen sind weder eine Security-Bedingung noch ein Release-Blocker. Ungelöst erhöhen sie Komplexität und Wartungsaufwand in Report-Layout-, Lifecycle-, Receipt- und Evidence-Test-Code. CRITICAL und MAJOR dürfen nicht als Security-Schwere oder Release-Blocker-Status umgedeutet werden.

## Betroffene Dateien, Regeln und exaktes Issue-Inventar

Betroffene Dateien:

- ci/checks/documentation/check-generated-report-layout.py
- ci/evidence/reports/generate-full-matrix-job-completeness.py
- ci/runtime/lifecycle/run-verified-report-run.py
- tests/test_generated_report_evidence_integrity.py
- ci/lib/verified_full_matrix_receipt.py

Betroffene Rule-/Symbol-Identifiers sind python:S3776, python:S1066, python:S5778, python:S1192 und die SonarQube-Cloud-PR-#59-Exact-Head-Issue-Abfrage.

| Key | Rule | Scanner-Label | Datei | Zeile | Meldung |
| --- | --- | --- | --- | ---: | --- |
| AZ98bS-YZDHgEby5GFdC | python:S3776 | CRITICAL | ci/checks/documentation/check-generated-report-layout.py | 1128 | Reduce cognitive complexity from 36 to 15 |
| AZ98bS_lZDHgEby5GFdG | python:S3776 | CRITICAL | ci/evidence/reports/generate-full-matrix-job-completeness.py | 496 | Reduce cognitive complexity from 20 to 15 |
| AZ98bS_GZDHgEby5GFdE | python:S3776 | CRITICAL | ci/runtime/lifecycle/run-verified-report-run.py | 636 | Reduce cognitive complexity from 18 to 15 |
| AZ98bS_GZDHgEby5GFdF | python:S3776 | CRITICAL | ci/runtime/lifecycle/run-verified-report-run.py | 798 | Reduce cognitive complexity from 18 to 15 |
| AZ98bS_GZDHgEby5GFdD | python:S1066 | MAJOR | ci/runtime/lifecycle/run-verified-report-run.py | 1751 | Merge the nested if statement with its enclosing condition |
| AZ98bTAcZDHgEby5GFdI | python:S5778 | MAJOR | tests/test_generated_report_evidence_integrity.py | 729 | Keep only one potentially throwing invocation in the exception test |
| AZ98bS59ZDHgEby5GFc_ | python:S1192 | CRITICAL | ci/lib/verified_full_matrix_receipt.py | 57 | Define a constant for the duplicated verified_run_id error literal |
| AZ98bS59ZDHgEby5GFdA | python:S3776 | CRITICAL | ci/lib/verified_full_matrix_receipt.py | 457 | Reduce cognitive complexity from 24 to 15 |

## Vorbedingungen und Reproduktion

Vorbedingungen:

- Der zurückgehaltene Receipt ist an Parent-PR #59, Head 841d5d66ba6db852cbc3c0a906e56d74583beb89 und Basis 6f80c90592fdd1f2eb990fe1514fdfc4efbf01e8 gebunden.
- Der Receipt erfasst Quality Gate OK, null offene Security-Hotspots und null offene Vulnerabilities für diese Exact-Head-Abfrage.
- Die Ownership-Bewertung des Receipts belegt, dass alle acht Komponenten geänderte Parent-Pfade und alle aufgelisteten Zeilen im aktuellen Diff sind.
- Jede Remediation bleibt Parent-owned, verhaltenserhaltend und nicht-suppressiv; Framework und MRTS liegen außerhalb des Scopes.

So wird die aufgezeichnete Beobachtung reproduziert:

1. Das unten genannte zurückgehaltene JSON lesen und pull_request=59, die exakten Head- und Base-SHAs, quality_gate.status=OK und issue_query.total=8 bestätigen.
2. Den aufgezeichneten Integrity-Command ausführen und das SHA-256-Ergebnis vergleichen.
3. Für ein Remediation-Resultat eine frische, an den exakten Remediation-Head gebundene SonarQube-Cloud-PR-Analyse beschaffen und das Quality Gate sowie jeden Key aus der Inventartabelle prüfen.

## Evidence

| Feld | Wert |
| --- | --- |
| Run-ID | 20260720T141403Z-pr55-pr59-master-integration-8a0b8640 |
| Artefakt | /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/sonar-pr59-841d5d6-maintainability.json |
| Artefakttyp | exact_pr_head_sonarqube_cloud_maintainability_issue_query |
| SHA-256 | 538bb94b4716979d1b75fb95b4cff97a3d4d47710b2592fc35ce5b285c2e4222 |
| Integrity-Command | rtk sha256sum /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/sonar-pr59-841d5d6-maintainability.json |
| Working Directory | /root/git/ModSecurity-conector |
| Exit-Code | 0 |
| Beobachtet am | 2026-07-20T14:35:23Z |
| Retention | retained_task_evidence |

Das zurückgehaltene JSON ist der Exact-Head-SonarQube-Cloud-PR-#59-Issue-Query-Receipt.

Der zweite zurückgehaltene Receipt erfasst die lokale Remediation auf Source-Commit b9b22cc36958ba506278f3aa3fbc1d383ea6a151 (`refactor: resolve PR 59 Sonar maintainability findings`). Es ist lokale Validation-Evidence und kein frisches Remote-SonarQube-Cloud-Resultat.

| Feld | Wert |
| --- | --- |
| Source-Commit | b9b22cc36958ba506278f3aa3fbc1d383ea6a151 |
| Artefakt | /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/pr59-b9b22cc-local-sonar-remediation-validation.json |
| Artefakttyp | local_sonar_maintainability_remediation_validation |
| SHA-256 | c78e125ceb25956b25cd248bad1d04e83221a1bf2a332360148dc67005ed9e53 |
| Beobachtet am | 2026-07-20T14:48:00Z |
| Retention | retained_task_evidence |
| Lokales Resultat | 57/57 Evidence-Integrity-Tests bestanden; Shell-Syntax bestanden; bilinguale Dokumentation 11/11 bestanden; git diff --check bestanden; unabhängiger fokussierter Five-File-Receipt/Path/TOCTOU-Security-Review bestanden. |

Der dritte zurückgehaltene Receipt ist die geschützte Merge- und Resulting-Master-Verifikation. Er ersetzt die frühere lokale-only-Delivery-Formulierung in diesem Record.

| Feld | Wert |
| --- | --- |
| Exakter Source / Merge-Methode | b9b22cc36958ba506278f3aa3fbc1d383ea6a151 / geschützter Squash-Merge mit `--match-head-commit` |
| Resultierender Parent-Master | 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 |
| Artefakt | /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/pr59-5a22cbf-postmerge-validation.json |
| Artefakttyp | postmerge_pr59_master_verification |
| SHA-256 | 7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51 |
| Beobachtet am | 2026-07-20T15:13:08Z |
| Resultat | 57/57 Evidence-Integrity-, 11/11 Bilingual-Dokumentations-, Shell-Syntax- und Merge-Diff-Whitespace-Controls bestanden; das PR-Quality-Gate war OK und die Abfrage aller acht ursprünglichen Keys meldet null auf master. |
| Unabhängige Grenze | FND-SONAR-0001 bleibt ein nicht akzeptierter Master-Quality-Gate-Fehler; er wird diesem Finding nicht zugeschrieben. |

## Root-Cause-Analyse

Die Exact-Head-Abfrage identifiziert unabhängig abgegrenzte Maintainability-Smells: fünf Cognitive-Complexity-Stellen, eine Nested-Condition-Regel, eine Exception-Test-Regel und eine Duplicate-Literal-Regel. Die Evidence belegt Task-Ownership und Klassifikation, aber keine Security-Vulnerabilität und keinen Hotspot. Das detaillierte Source-Level-Refactoring-Design bleibt Teil der geplanten Remediation.

## Remediation und abgeschlossene Verifikation

Commit b9b22cc36958ba506278f3aa3fbc1d383ea6a151 hat für jede gemeldete Stelle ein kleines verhaltenserhaltendes Parent-only-Refactoring angewendet:

- Helfer extrahieren oder vereinfachen, während Inputs, Outputs, Fehlerbehandlung, Reihenfolge und fail-closed-Verhalten erhalten bleiben.
- Die verschachtelte Bedingung nur bei logischer Äquivalenz zusammenführen.
- In der Exception-Assertion genau einen potenziell werfenden Aufruf behalten und die beabsichtigte Testabdeckung bewahren.
- Das duplizierte verified_run_id-Fehlerliteral durch eine benannte Konstante ersetzen.
- Fokussierte Regression-Coverage für Report Layout, Full-Matrix-Receipt, Verified-Report-Lifecycle und Evidence Integrity erhalten.

Die zurückgehaltenen Receipts erfassen forbidden_controls_changed=false. Kein NOSONAR, keine Regel-Suppression, Regel-Deaktivierung, Exclusion, Quality-Gate-Änderung oder False-Positive-Disposition wurde verwendet. Frische nicht übersprungene CI-, CodeQL-, PR-Sonar-Quality-Gate-OK- sowie Null-Review/Thread-Controls lagen vor dem geschützten Merge vor; die exakte Resulting-Master-Evidence bestand anschließend. Das Finding ist verified, nicht closed.

## Akzeptanzkriterien

1. Bestanden: Eine frische SonarQube-Cloud-PR-Analyse war an den exakten Source b9b22cc36958ba506278f3aa3fbc1d383ea6a151 gebunden und meldete Quality Gate OK.
2. Bestanden: Die Resulting-Master-Abfrage auf 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 meldet alle acht aufgelisteten Keys als null verbleibend, ohne Suppression, Exclusion, Regel-Deaktivierung, Quality-Gate-Änderung oder False-Positive-Disposition.
3. Bestanden: Der zurückgehaltene Post-Merge-Receipt erfasst 57/57 bestandene fokussierte Evidence-Integrity-Tests, bestandene Shell-Syntax, 11/11 bestandene bilinguale Dokumentationstests und bestandene Merge-Diff-Whitespace-Validierung; der unabhängige fokussierte Five-File-Receipt/Path/TOCTOU-Security-Review bestand ebenfalls.
4. Bestanden: Die Refactorings bewahrten öffentliches und operatives Verhalten einschließlich Validierung, Fehlerbehandlung, Ausgabe, Reihenfolge und fail-closed Controls.
5. Bestanden: Evidence bleibt SHA-adressiert, und die englischen, deutschen, Index-, Backlog- und Roadmap-Records sind synchronisiert.

## Validierungsplan

1. Im zurückgehaltenen lokalen Receipt abgeschlossen: Jedes fokussierte Refactoring wurde gegen das ursprüngliche Bedingungs-, Fehler-, Ausgabe-, Reihenfolge- und Validierungsverhalten geprüft.
2. Im zurückgehaltenen lokalen Receipt abgeschlossen: Die kleinsten relevanten lokalen Regressionstests und Legitimate Controls liefen, und ihre exakten Resultate wurden aufbewahrt.
3. Abgeschlossen: SonarQube Cloud meldete Quality Gate OK für exakten Source b9b22cc36958ba506278f3aa3fbc1d383ea6a151, und die Resulting-Master-Abfrage meldet alle acht ursprünglichen Issue-Keys als null.
4. Abgeschlossen: Die zurückgehaltene Evidence erfasst keine verbotene Control-Änderung; die frischen GitHub-, CodeQL-, PR-Sonar-, Review- und Thread-Controls bestanden vor dem geschützten Merge.

## Regression und Legitimate Controls

Der zurückgehaltene lokale Receipt meldet diese Regression- und Legitimate-Control-Evidence:

- `tests/test_generated_report_evidence_integrity.py`: 57/57 Tests bestanden, einschließlich validem Full-Matrix-Control und Receipt/Path/Hash/Symlink/TOCTOU-Negativ-Controls.
- `sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh`: bestanden.
- `tests.test_bilingual_docs`: 11/11 Tests bestanden.
- `git diff --check`: bestanden.
- Unabhängiger fokussierter Five-File-Receipt/Path/TOCTOU-Security-Review: bestanden; finale TOCTOU-Revalidierung und fail-closed Controls blieben erhalten.

Die zurückgehaltenen lokalen und Resulting-Master-Resultate stützen den Status verified. Ein Abschluss ist eine separate Lifecycle-Entscheidung und folgt nicht automatisch aus diesem Merge.

## Dependencies, Blocker und verwandte Findings

- Dependency: keine verbleibend für die Verifikation; FND-SONAR-0001 ist ein getrennter, nicht akzeptierter Parent-Master-Quality-Gate-Blocker.
- Blocked by: none.
- Duplicates: none. Die acht Keys wurden gegen die bestehenden FND-SONAR-Records geprüft und sind eindeutig.
- Verwandte Findings: FND-SONAR-0001 und FND-PARENT-0040; beide sind von diesem nicht-sicherheitsrelevanten P2-Maintainability-Finding getrennt.
- Source Run: 20260720T141403Z-pr55-pr59-master-integration-8a0b8640.

## Restrisiko

Die acht ursprünglichen aufgabeneigenen Keys sind auf Parent-Master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 als nicht vorhanden verifiziert, ohne Risikoakzeptanz, Suppression oder Scanner-Control-Änderung. Dieses Finding bleibt bis zu einer separaten Lifecycle-Entscheidung verified statt closed. FND-SONAR-0001 bleibt ein unabhängiger, nicht akzeptierter Parent-Master-Quality-Gate-Fehler und lässt die aggregierte Delivery partial; er wird diesem Finding nicht zugeschrieben.

## Historie

| Zeitpunkt | Ereignis | Detail |
| --- | --- | --- |
| 2026-07-20T14:39:40Z | exact_pr59_head_maintainability_finding_created | Nach unabhängiger SHA-256-Verifikation des zurückgehaltenen Exact-Head-Receipts erstellt. Acht eindeutige aufgabeneigene Parent-CODE_SMELLs wurden gegen bestehende FND-SONAR-Records dedupliziert; sechs CRITICAL- und zwei MAJOR-Werte sind ausschließlich nicht-sicherheitsrelevante Scanner-Labels. |
| 2026-07-20T15:03:04Z | local_non_suppressive_remediation_fixed | Source-Commit b9b22cc36958ba506278f3aa3fbc1d383ea6a151 ist nach zurückgehaltener lokaler Evidence als fixed erfasst: 57/57 Evidence-Integrity-Tests, Shell-Syntax, bilinguale Dokumentation 11/11, git diff --check und unabhängiger fokussierter Five-File-Receipt/Path/TOCTOU-Security-Review bestanden. Frische Remote-Exact-Head-Validierung bleibt erforderlich; Status ist nicht verified oder closed. |
| 2026-07-20T15:13:08Z | verified_on_protected_pr59_squash_merge_parent_master | Exakter Source b9b22cc36958ba506278f3aa3fbc1d383ea6a151 wurde geschützt squash als Parent-Master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 gemergt. Frische nicht übersprungene CI-, CodeQL-, PR-Sonar-Quality-Gate-OK- sowie Null-Review/Thread-Controls bestanden vor dem Merge; zurückgehaltene Resulting-Master-Evidence erfasst 57/57 Evidence-Integrity-, 11/11 Bilingual-, Shell-Syntax- und Diff-Controls bestanden sowie null der acht ursprünglichen Keys. Es erfolgten keine Suppression, Scanner-/Gate-Änderung, False-Positive-Disposition oder Risikoakzeptanz. FND-SONAR-0001 bleibt unabhängig und nicht akzeptiert. Status ist verified, nicht closed. |
