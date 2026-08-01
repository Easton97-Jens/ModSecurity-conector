# FND-FRAMEWORK-0023 — Framework-PR #30 fügt SonarQube-Cloud-Duplikation in gemeinsamen Sicherheitskontrollen hinzu

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0023 |
| Kategorie | sonarqube_finding |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P2 / not_applicable |
| Confidence / Status | confirmed / fixed |
| Feasibility | feasible_now |
| Release-Blocker | false |
| Security-relevant | true |

## Zusammenfassung, Beobachtung, erwartetes Verhalten und Auswirkung

Framework-PR #30 hatte zunächst ein SonarQube-Cloud-Quality-Gate mit dem Ergebnis OK, aber seine New-Code-Metriken meldeten new_lines=15461, new_duplicated_lines=182 und new_duplicated_lines_density=1.1771554233232002 (angezeigt als 1.2%). Der aktuelle Nutzer verlangt die Beseitigung dieser Duplikation vor der Integration des PR in master; der grüne Grenzwert <3% ist kein Ersatz für das verlangte Ergebnis.

Die erste verhaltensbewahrende Refaktorierung wurde normal als `ce6c1570d3dfbe4b4da5f9560068c37a807899d3` gepusht. Ihr historischer Exact-Head-Sonar-Readback hatte Quality Gate `OK`, meldete aber noch `new_duplicated_lines=32` und `new_duplicated_lines_density=0.2059732234809475`.

Der aktualisierte PR-Head ist jetzt der normale Merge-Commit `a448d056ef98e745d8551c198b2e56d33fe38194` mit dem früheren PR-Head und dem aktuellen Framework-master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` als Parents. Sein exaktes SonarQube-Cloud-Ergebnis ist Quality Gate `OK`, `new_duplicated_lines=0` und `new_duplicated_lines_density=0.0`. Die lokalen Legitimate Controls und jeder terminale nicht übersprungene Hosted Check bestanden ohne Änderung einer Sonar-Einstellung, eines Grenzwerts, einer Exclusion, Baseline, Suppression oder eines Gates. Der Befund ist daher auf dem verifizierten PR-Head `fixed`. Er ist nicht auf Master `verified`, weil die aktuelle Aufgabe keinen Framework-master-Merge autorisiert.

Die anfänglichen sieben Dateibeiträge ergeben genau 182 neue duplizierte Zeilen:

| Pfad | Neue duplizierte Zeilen |
| --- | ---: |
| ci/reporting/generate-phase-work-queue.py | 37 |
| ci/reporting/generate-connector-work-queue.py | 36 |
| ci/reporting/generate-mrts-native-report.py | 36 |
| ci/provisioning/import-mrts-cases.py | 36 |
| tests/security_regression/test_modsecurity_v3_git_ref_provenance.py | 18 |
| ci/reporting/generate-case-matrix.py | 14 |
| tests/protocol_client/test_check_protocol_evidence.py | 5 |

Der exakte Rest des Heads `ce6c157…` ist auf zwei Blöcke begrenzt:

| Pfad | Neue duplizierte Zeilen | Sonar-Paarung |
| --- | ---: | --- |
| ci/reporting/generate-case-matrix.py | 14 | Zeilen 2947–3021 und 3146–3220 in derselben Datei (je 75 Zeilen) |
| tests/security_regression/test_modsecurity_v3_git_ref_provenance.py | 18 | Zeilen 162–179 gepaart mit test_crs_git_ref_provenance.py Zeilen 221–237 |

Die gepaarten Blöcke enthalten Helfer für sicheres atomares Report-Schreiben und private Runtime-Root-/Pfadvalidierung sowie eng abgegrenzte duplizierte Test-Assertions. Der Sonar-Duplikationsendpunkt stellt innerhalb überlappender Gruppen keine individuelle New-Line-Teilmenge bereit; er identifiziert aber die gemeinsamen Blöcke. Der exakte finale PR-Head muss null neue duplizierte Zeilen und 0.0% Density melden und dabei alle Controls für Traversal, Symlinks, Deskriptoren, sichere temporäre Dateien, atomares Ersetzen, Provenance und Protokoll bewahren.

Duplizierte sicherheitssensitive Helfer können später bei Ablehnungsreihenfolge, Fehlerverhalten, Deskriptor-Lebensdauer oder Confinement-Semantik auseinanderdriften. Dies ist keine validierte ausnutzbare Schwachstelle, sondern eine bestätigte, vom Nutzer blockierte Quality- und Maintainability-Beobachtung, die eine verhaltensbewahrende Refaktorierung und legitime Negative Controls erfordert.

## Scope, Voraussetzungen, Reproduktion und Evidence

Der relevante PR ist Easton97-Jens/ModSecurity-test-Framework#30 (fix/sonarcloud-quality-gate → master). Sein beobachteter Pre-Update-Head ist b6af3ec83011b2070f6bbe4b3f471478b373f055; der beobachtete aktuelle Framework-master ist 9a729226d2e040d07d7e7a4acebf201faf06ab37. Der erste remediierte, normal gepushte Head ist `ce6c1570d3dfbe4b4da5f9560068c37a807899d3`; ein späterer exakter Head muss null Duplikation erreichen. Die SonarQube-Cloud-Analyse muss für das Projekt Easton97-Jens_ModSecurity-test-Framework und Pull Request 30 verfügbar sein.

~~~
rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/measures/component?component=Easton97-Jens_ModSecurity-test-Framework&pullRequest=30&metricKeys=new_lines,new_duplicated_lines,new_duplicated_lines_density'
rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/measures/component_tree?component=Easton97-Jens_ModSecurity-test-Framework&pullRequest=30&metricKeys=duplicated_lines,new_duplicated_lines,new_duplicated_lines_density&qualifiers=FIL&ps=500'
rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/duplications/show?key=Easton97-Jens_ModSecurity-test-Framework&pullRequest=30&file=ci%2Freporting%2Fgenerate-phase-work-queue.py'
~~~

Die aufbewahrte Initial-Evidence ist /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-initial-sonar-duplication.md mit SHA-256 27dc350cc104bd804cadaf479bf2b347cee20738fab375b105637280f4575fd3. Sie wurde in /root/git/ModSecurity-conector durch einen bereinigten SonarQube-Cloud-Measures-und-Duplications-API-Readback mit Exit-Code 0 am 2026-07-19T23:05:08Z erzeugt. Die aufbewahrte historische Rest-Evidence ist /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-current-head-residual-duplication.md mit SHA-256 bc2d2626510bc6f295f33cf6f8e104a1145af82db75423e577a993396b62bd0e, beobachtet am 2026-07-20T00:34:04Z. Die aufbewahrte Exact-Head-Verifikation ist /var/tmp/codex/ModSecurity-conector/runs/20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef/evidence/pr30-refresh-summary.md mit SHA-256 04a0b6891f92b0485c298bb939e57fb464cea2bd5872eb74c65d97f6450f4255, Command `GitHub exact-head check-run/review readback and SonarQube Cloud PR #30 Quality Gate and measure queries`, Working Directory /root/git/ModSecurity-conector, Exit-Code 0, beobachtet am 2026-07-20T06:43:42Z, Retention retained. Sie dokumentiert den Exact-Head mit null Duplikation, Quality Gate `OK` und aktuelle Hosted-Check-Erfolge.

## Grundursache und vorgeschlagene Remediation

Der historische PR führte gleichwertige gehärtete Pfad-/Runtime-Root- und sichere Report-Schreibroutinen unabhängig in mehreren Producer-Skripten ein, statt ihre gemeinsame Semantik in einem geprüften Shared Utility abzulegen. Zwei Testmodule wiederholten zudem eng verwandte Assertion-Sequenzen. Der normale Master-Merge und die erste Extraktion beseitigten den Großteil der Duplikation. Der bestätigte Rest besteht aus zwei semantisch identischen Case-Matrix-Runtime-Snapshot-Abschnitten und einer Assertion-Sequenz für unveränderliche Commit-Provenance, die V3- und CRS-Tests gemeinsam haben; die Extraktion muss Rendering-Reihenfolge, Evidence-Zeilen, No-Clone-/No-Submodule-Assertions und jeden Negativfall bewahren.

Die erste fokussierte Reparatur erstellte Shared Framework Utilities für das duplizierte Runtime-Pfad- und sichere Report-Schreibverhalten und bewahrte direkte Test-Call-Points. Die verbleibende Reparatur ist absichtlich enger: ein reiner Case-Matrix-Runtime-Snapshot-Section-Appender plus Ordnungs-Regression und ein Assertion-Helper für unveränderliche Commit-Fetch-Controls, der von getrennten V3- und CRS-Legitimate-Control-Tests genutzt wird. Sie darf weder die V3/CRS-Fake-Git-Fixtures oder ihre einzigartigen Negativ-Controls noch eine SonarQube-Cloud-Regel, ein Gate, einen Grenzwert, eine Baseline, Exclusion, Coverage-Einstellung, Suppression oder NOSONAR-Markierung ändern.

## Akzeptanzkriterien und Validierungsplan

- [complete] Der aktuelle Framework-master wird normal in die PR-#30-Lineage gemergt, ohne Force-Push oder History-Rewrite.
- [complete] Nur die erwarteten vier Current-Master-Dateien wurden durch die Synchronisierung ergänzt oder geändert; die Konfliktauflösung bewahrt beide Hardening-Pfade.
- [complete] Negative Controls für Traversal, Symlinks, unsichere Runtime-Roots, unsichere temporäre Dateien, atomares Ersetzen, Provenance und Protokoll bestehen.
- [complete] Der exakte PR-#30-Head `a448d056ef98e745d8551c198b2e56d33fe38194` meldet new_duplicated_lines=0, new_duplicated_lines_density=0.0 und Quality Gate OK.
- [complete] Kein analytisches Control wird abgeschwächt oder umgangen.
- [complete] Exact-Head-Hosted-Checks sowie Review-/Thread-Readback bestanden.
- [pending authorization] Normale Framework-master-Integration und Resulting-Master-Revalidation sind von der aktuellen Aufgabe nicht autorisiert.

Die Validierungsfolge lautet: normalen Master-Merge inspizieren und jeden Konflikt manuell auflösen; die fokussierten Producer-/Security-Regression-Module, bei Änderung seines Moduls Protocol-Client-Tests, Workflow-Contract-Tests, gezielte Python-Kompilierung, git diff --check und anwendbares Linting mit task-eigenen Output-Roots ausführen; einen fokussierten Security-Diff-Review durchführen; danach exakte Local-/Remote-/PR-Head-Gleichheit, frische CI, Review, Issue-/Hotspot-, Quality-Gate- und Zero-Duplication-Evidence verlangen. Nach dem autorisierten Squash-Merge werden der resultierende Framework-master-SHA und anwendbare Master-Checks ausgelesen. Parent und MRTS bleiben durchgehend unverändert.

## Regression- und Legitimate-Control-Tests

Direkter Regressions-Scope:

- tests/security_regression/test_generate_case_matrix_sonar.py
- tests/security_regression/test_generate_phase_work_queue_sonar.py
- tests/security_regression/test_generate_connector_work_queue_sonar.py
- tests/security_regression/test_import_mrts_cases_sonar.py
- tests/security_regression/test_runtime_snapshot_sonar.py
- tests/security_regression/test_modsecurity_v3_git_ref_provenance.py
- tests/security_regression/test_second_remediation.py
- tests/protocol_client/test_check_protocol_evidence.py

Legitime Controls müssen Traversal, Symlink-Komponenten, unsichere Runtime-Roots und unsichere temporäre-Datei-Bedingungen weiterhin ablehnen; gültige von ungültigen Provenance- und Protokoll-Inputs unterscheiden; Deskriptor-relative sichere Erstellung und atomares Ersetzen bewahren; und ohne analytischen Control-Workaround null neue Sonar-Duplikation erreichen.

## Abhängigkeiten, Grenzen, verwandte Findings und Restrisiko

Abhängigkeiten sind ein sauberer task-eigener Framework-Worktree, aktuelles origin/master, Exact-Head-GitHub-Actions- und SonarQube-Cloud-Analysen sowie der autorisierte normale PR-#30-Merge. Es ist keine externe Implementierungsabhängigkeit bekannt; dieser Record hat keine aktuellen blocked_by-Einträge und keine Duplikate.

Dieser Befund ist von FND-SONAR-0002 verschieden, das den bestehenden Framework-master-Multi-File-Quality-Gate-Backlog und dessen abgegrenzte historische Risikoentscheidung besitzt. Dieser Backlog ist weder Ursache dieses reproduzierbaren PR-#30-Ergebnisses noch wird er hier automatisch waived. Dass die Sonar-Block-API keine individuellen New-Line-Ranges bereitstellt, ist eine Evidence-Limitierung; die finale Current-Head-Metrik muss nach der Refaktorierung erneut ausgelesen werden.

Das ursprüngliche PR-spezifische Sonar-Ergebnis reproduziert auf dem exakten PR-Head nicht mehr, daher ist dieser Befund fixed. Die einzige Delivery-Lücke ist die bewusst nicht ausgeführte Framework-master-Integration mit Resulting-Master-Revalidation; sie folgt weder aus diesem Finding noch ist sie vom aktuellen Nutzer autorisiert. Kein Parent-Gitlink-Update und keine MRTS-Änderung ist autorisiert.

## Verlauf

- 2026-07-19T23:05:08Z — confirmed_pr30_new_code_duplication_tracked: Die aufbewahrte SonarQube-Cloud-Evidence verzeichnete 182 neue duplizierte Zeilen und 1.1771554233232002% Density über sieben Dateien. Normaler Branch-Update, fokussierte Shared-Helper-Extraktion, lokale Controls, Exact-Head-Remote-Validierung und Master-Integration stehen noch aus.
- 2026-07-20T00:34:04Z — first_remediation_reduced_but_did_not_clear_duplication: Der normale nicht-rewriteende Push von `ce6c1570d3dfbe4b4da5f9560068c37a807899d3` reduzierte das exakte PR-#30-Sonar-Ergebnis bei Quality Gate OK auf 32 neue duplizierte Zeilen und 0.2059732234809475% Density. Die zwei verbleibenden Blöcke sind bestätigt und blockieren den Merge, bis ein späterer exakter Head null meldet.
- 2026-07-20T06:43:42Z — exact_refreshed_pr_head_clears_duplication: Der normale Merge-Commit `a448d056ef98e745d8551c198b2e56d33fe38194` aktualisierte PR #30 mit Framework-master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. Exakte SonarQube Cloud meldet Quality Gate `OK`, `new_duplicated_lines=0` und `new_duplicated_lines_density=0.0`; lokale Legitimate Controls und alle terminalen nicht übersprungenen Hosted Checks bestanden. Der Befund ist auf dem verifizierten PR-Head fixed; die Master-Integration bleibt nicht autorisiert.
