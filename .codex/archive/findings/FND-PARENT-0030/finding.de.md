# FND-PARENT-0030 — Striktes Report-Evidence-Gate akzeptiert fehlende und hash-inkonsistente Runtime-Resultate

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0030 |
| Titel / Title | Striktes Report-Evidence-Gate akzeptiert fehlende und hash-inkonsistente Runtime-Resultate |
| Kategorie / Category | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P1 |
| Schweregrad / Severity | high |
| Konfidenz / Confidence | reproduced |
| Status | closed (archiviert) — Abschluss durch aktuellen Nutzer nach Unchanged-Path-Neuvalidierung |
| Final disposition / Enddisposition | `closed_by_current_user_after_current_master_unchanged_evidence_integrity_validation` |
| Machbarkeitsstatus / Feasibility status | feasible_now |
| Release-Blocker / Release blocker | false |
| Security-Relevanz / Security relevance | true |

## Zusammenfassung / Summary

Das strikte Verified-Report-Evidence-Gate akzeptierte früher kritischen `missing`-Input-Status und berechnete deklarierte Output-Hashes oder Byte-Zahlen nicht neu. Die isolierte Parent-Remediation weist nicht verifizierte und malformatierte Status-Schemata zurück, leitet die kanonische Zwölf-Zellen-Artefaktkette ab und prüft sie und bewahrt die geprüften Source-Felder. Der exakte PR-#59-Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` bestand vor dem Merge alle nicht übersprungenen erforderlichen CI-, CodeQL- und SonarQube-Cloud-Quality-Gate-Checks bei 0 eingereichten Reviews, Review Requests und Review Threads. Der protected-squash Parent-`master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` hat einen Source-Tree, der dem Source-Head entspricht. Die aufbewahrte Detached-Master-Post-Merge-Validierung bestand die 57/57-Evidence-Integrity-Suite, bilingual 11/11, Shell-Syntax und `git diff --check`. Dieses Finding ist `verified`, niemals `closed` oder risikakzeptiert. Ein getrenntes Detached-Producer-Receipt-Finding wird als `FND-PARENT-0031` geführt.

## Beobachtetes Verhalten / Observed behavior

Auf `verified-report-governance.yml:49` → `Makefile:392` → `check-generated-report-layout.py` haben die kritischen Refresh-Records `full_runtime_matrix`, `full_matrix_job_completeness` und `verified_runtime_mismatch_analysis` `input_status=missing`, aber die strikte Ausgabe benennt sie nicht. Das Verified-Run-Manifest deklariert `full-runtime-matrix.generated.json` mit SHA-256 `e3510bad867fdcf97ee0892378b608c484c081b568334b85f55784354d103711` und 12419 Bytes; die tatsächliche Datei hat SHA-256 `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` und 12418 Bytes, ohne strikten Mismatch-Fehler. Das aktuelle PR-#59-Fixture zeigte außerdem, dass `BUILD_ROOT:../outside-runtime.json`, `framework:../outside-runtime.json` und `../outside-runtime.json` jeweils einen passenden Hash einer externen regulären Datei akzeptierten. Governance-only besteht; strict scheitert nur wegen unabhängiger veralteter Reports.

## Erwartetes Verhalten / Expected behavior

Strikte Akzeptanz verlangt eine valide Run-ID, einen abgekoppelten Command-Receipt, eine vollständige Raw-Runtime-Matrix mit zwölf Zellen, job-lokale reguläre Artefaktpfade, passende Connector-/Profil-/Run-Identität und neu berechnete Hashes und Byte-Zahlen. Beanspruchte kritische Input-Pfade und vertrauenswürdige Roots werden vor dem Containment-Vergleich normalisiert, während Leaf- und Zwischen-Symlink-Ablehnung explizit bleibt. Alle nicht verifizierten kritischen Zustände scheitern geschlossen; ein Dashboard oder Report-Name kann keine Runtime-Authentizität erzeugen.

## Auswirkung / Impact

Ein gefälschter oder kopierter Report bzw. ein Manifest kann abgeleitete Diagnostik vollständig aussehen lassen, ohne passenden Raw-Runtime-Run, Artefaktkette, Prüfsumme, Connector oder Profil nachzuweisen. Ein gefälschtes Critical-Input-Receipt konnte zusätzlich eine externe reguläre Datei durch lexikalische Traversal und einen bekannten Digest vertrauenswürdig erscheinen lassen. Die FND-PARENT-0024-Workflow-Verdrahtung ist korrekt, aber ihr striktes Gate muss diese Result-File-Grenze erzwingen.

## Betroffene Dateien und Symbole / Affected files and symbols

- `ci/checks/documentation/check-generated-report-layout.py` — `check_manifest`, `check_critical_report_run_consistency`, `validate_critical_input_records`, `trusted_input_roots`, `input_root_for_path`, `is_within`, `has_symlink_component`, `check_verified_runtime_diagnostics` und `check_verified_runtime_artifact_chain`.
- `ci/evidence/reports/generate-full-matrix-job-completeness.py` — `rewrite_manifest`; `ci/evidence/reports/refresh-connector-reports.py` — `build_governance_record`.
- `ci/runtime/lifecycle/run-full-matrix-parallel.sh` und `ci/runtime/lifecycle/run-verified-report-run.py` — kanonischer Job-Producer und `generated_output_records`.
- Source-Commits: `1e0c825de82d1325b5e7b070a4916de2f5af2207` und `dd6e0455c4838949ce86cff81ce89dccd4e524f8`; geschützter PR-#59-Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`; protected-squash Parent-`master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`.

## Evidence / Evidence

- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`.
- Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/FND-PARENT-0030-result-file-authenticity/strict-gate-pre-fix-analysis.json`.
- Typ: `strict_gate_result_authenticity_validation`; SHA-256: `9a5def690f41d36ae5fd63a7dd0c95e08803d25f7dd4c1f005a9e84de3bcc0f5`.
- Strikte und Governance-only-Checks wurden am 2026-07-18 UTC beobachtet. Strict meldete veraltete Reports, ließ aber die genannten Missing-/Hash-/Byte-Fälle aus; Governance-only bestand.
- Post-Fix-Artefakt: `.../FND-PARENT-0030-result-file-authenticity/post-fix-validation.json`, SHA-256 `49e9463ca746524cacb82e8355a488a2caec8c32b6b2a22d6d474741582e24ea`; die 25 fokussierten Negativ-/Kontrolltests, Shell-Syntax, In-Memory-Kompilierung und der Diff-Check bestanden. Die strikte Retained-Evidence-Kontrolle scheitert nun fail closed; Governance-only besteht weiterhin, ohne Runtime-Evidence zu behaupten.
- PR-#59-Containment-Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260719T134234Z-pr59-containment-evidence-61aae959/evidence/pr59-critical-input-containment-validation.md`, Run `20260719T134234Z-pr59-containment-evidence-61aae959`, SHA-256 `6f79cc322e568d8943434db95abd98caa5d6ad37dc06f2df7a6b468f8d41f1f3`. Das Pre-Fix-Fixture scheiterte wie erwartet für alle drei Traversal-Formen; nach der Normalisierung bestanden die fokussierte 32-Test-Suite, die 11-Test-Bilingual-Docs-Suite und `git diff --check`.
- Finales PR-#59-Exact-Head-Scan-Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260719T141048Z-pr59-final-security-diff-98aafaa7/evidence/pr59-final-security-diff-report.md`, Run `20260719T141048Z-pr59-final-security-diff-98aafaa7`, SHA-256 `2a37f50ff38fca2613fe2851d54463b41f121fd88d806b80f90cb439676ed369`. Der versiegelte Scan deckt alle zehn finalen `aabde81..fb9becc`-Diff-Zeilen ab und meldet keine neue reportable Security-Feststellung.
- Aktuelles PR-#59-Exact-Head-Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/pr59-d4-current-head-verification.md`, Run `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`, Typ `pr59_d4_current_head_verification`, SHA-256 `38e88188683330e57704bb3d4559c5604dbea303c1f305fb17e695545267107d`. Bei `d4f88b886dac6fd5f483940015d6310bc239f814` beobachteten `gh pr checks`, Exact-Head-Check-Run- und CodeQL-Alert-Abfragen 33 erfolgreiche Runs, 6 erwartete Skips, keine fehlgeschlagenen/pending/abgebrochenen Runs, erfolgreiche aktive Required Contexts, CodeQL mit 0 offenen Alerts und ein bestehendes SonarQube-Cloud-Quality-Gate. Der automatisierte SonarQube-Cloud-Kommentar meldete 9 neue Issues und 0 Security Hotspots; er ist kein Human Review. Dasselbe Artefakt dokumentiert 0 eingereichte Reviews, 0 Review Requests und 0 Review Threads sowie einen bestehenden lokalen Exact-Diff-Check ohne Framework-, MRTS- oder Gitlink-Pfad. Die fokussierten Kontrollen decken gepaarte veränderbare Result/Job/Raw-Fälschung, Raw-only-Rewrite, Receipt-Symlinks, deterministische Intermediate-Read- und Verified-Runs-Publication-Swaps, Post-Validation-Swaps, Foreign-Run-Selection, die vollständige Zwölf-Zellen-Kontrolle und die Owner-read-only-`0400`-Assertion ab.
- Post-Merge-Verifikation: Run-ID `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`; Artefakt `/var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/pr59-5a22cbf-postmerge-validation.json`; Typ `pr59_protected_squash_merge_postmerge_security_finding_verification`; SHA-256 `7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51`; Kommando: `Protected PR #59 squash merge with --match-head-commit from exact source head b9b22cc36958ba506278f3aa3fbc1d383ea6a151 to Parent master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188; retained detached-master validation runs the 57/57 evidence-integrity suite, including valid full-matrix and forged identity/result/path/symlink/hash/seal/swap controls, plus bilingual 11/11, shell syntax, git diff --check, and clean/no-.pyc checks.` Arbeitsverzeichnis `/root/git/ModSecurity-conector`; Exit-Code `0`; beobachtet am `2026-07-20T15:09:01Z`; Retention-Status `retained_task_evidence`. Vor dem Merge bestand Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` alle nicht übersprungenen erforderlichen CI-, CodeQL- und SonarQube-Cloud-Quality-Gate-Checks bei 0 eingereichten Reviews, Review Requests und Review Threads. Der Post-Merge-Parent-`master`-Source-Tree entspricht dem Source-Head.

## Grundursachenanalyse / Root-cause analysis

Der strikte Consumer validierte ausgewählte abgeleitete Report-Status-Claims und Datei-Existenz. Er wies nur `stale`/`blocked` zurück, verlangte keine listen-typisierten aggregierten Statusfelder, berechnete keine abgekoppelten Artefakt-Hashes neu und validierte keine Raw-Full-Matrix-Jobkette. Das Producer-Manifest-Rewrite verlor außerdem Identity- und Hash-Felder, die ein Consumer-Verifier benötigt. Der PR-#59-`present`-Input-Guard verglich zusätzlich `.absolute()`-lexikalische Pfade, nachdem `resolve_input_reference()` `..` bewahrt hatte, wodurch logisches Containment vom physischen Ziel abweichen konnte. Die reparierte veränderbare Kette benötigt gegen synchronisiertes Receipt-Rewriting weiterhin einen separaten Parent-generierten Aggregate-Seal (`FND-PARENT-0031`).

## Vorgeschlagene Remediation / Proposed remediation

Der isolierte Parent-Branch stellt nun einen strikten Verifier bereit, der bei einer validierten Run-ID und einem abgekoppelten Command-Receipt beginnt, erwartete Raw-Job-Pfade für zwölf Zellen ableitet statt Report-Pfaden zu vertrauen, Identity/Status/Schema und reguläre job-lokale Artefakte validiert, Hashes und Größen neu berechnet, Leaf- und Zwischen-Symlinks zurückweist und nur allowlistete listen-typisierte kritische Status-Records akzeptiert. Er normalisiert beanspruchte kritische Input-Pfade und vertrauenswürdige Roots vor dem Containment-Vergleich. Er bewahrt Raw-Evidence-Felder und erzeugt typisierte Refresh-Arrays. Self-generated-Manifest-Records bleiben von abgekoppelten Hash-Prüfungen ausgeschlossen. #55, Framework, MRTS und erzeugte Reports nicht von Hand ändern. Ein abgekoppelter Aggregate-Producer-Receipt wird nur im getrennten `FND-PARENT-0031`-Branch geliefert.

## Akzeptanzkriterien / Acceptance criteria

- Strict weist fehlende Runtime-Manifeste, fremde Run-IDs, kopierte Connector-/Profil-Records, unsichere Pfade, Checksum-/Byte-Mismatches und unvollständige Matrix-Jobs zurück.
- Ein vollständiger kanonischer Parent-Run mit zwölf Zellen, passenden Hashes und passender Identität besteht den fokussierten Verifier.
- Abgeleitete Reports können keine Authentizität erzeugen; alle kritischen nicht verifizierten Zustände scheitern in strict geschlossen.
- `BUILD_ROOT:`, `framework:` und unpräfixierte lexikalische Parent-Traversal scheitern geschlossen, auch wenn eine externe reguläre Datei den deklarierten Digest besitzt; ein passender In-Root-Receipt bleibt akzeptiert.
- Self-generated-Manifeste sind ausgeschlossen oder benutzen einen expliziten abgekoppelten Receipt; keine Selbstreferenz gilt als Proof.
- FND-PARENT-0024-Workflow-Verdrahtung bleibt unverändert, ohne Framework-/MRTS-Änderung, Suppression oder Merge.

## Validierungsplan / Validation plan

1. Temporäre Fixture-Builder vor dem Source-Fix ergänzen.
2. Missing-Manifest, Checksum-/Byte-Tamper, unvollständigen Job, fremden Run, kopierten Connector/Profil, `BUILD_ROOT:`-/`framework:`-/unpräfixierte Parent-Traversal, Pfadescape und eine vollständige valide Kontrolle testen.
3. Abgeschlossen: Der exakte PR-#59-Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` bestand alle nicht übersprungenen erforderlichen CI-, CodeQL- und SonarQube-Cloud-Quality-Gate-Checks bei 0 eingereichten Reviews, Review Requests und Review Threads. Der geschützte Squash-Merge erzeugte Parent-`master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`, dessen Source-Tree dem Source-Head entspricht; die aufbewahrte Detached-Master-Validierung bestand 57/57 Integrity-Kontrollen, bilingual 11/11, Shell-Syntax, `git diff --check` und clean/no-`.pyc`-Checks.
4. `FND-CROSS-0001` als erwarteten End-to-End-Strict-Gate-Blocker bewahren; diesen Verifier niemals lockern. Der globale `master`-Fehler `FND-SONAR-0001` ist von dieser Verifikation unabhängig und wird weder akzeptiert noch unterdrückt.

## Verwandte Findings / Related findings

- `FND-PARENT-0024` — Workflow-Auswahl des strict- gegenüber governance-only-Gate.
- `FND-PARENT-0031` — fehlender abgekoppelter Parent-Producer-Receipt für synchronisierte veränderbare Artefaktumschreibungen.
- `FND-CROSS-0001` — stale Cross-Runtime-Evidence bleibt separater Blocker.
- `FND-SONAR-0001` — unabhängiger globaler `master`-Fehler; wird durch diese Verifikation weder akzeptiert noch unterdrückt.

## Restrisiko / Residual risk

Dieses Finding ist auf Parent-`master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` nach geschütztem PR-#59-Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` sowie Post-Merge-Originalreproduktion und Legitimate-Control-Validierung `verified`. Es ist nicht `closed` oder risikakzeptiert. Die Receipt-Kette ist keine Signatur-, ACL-, Prozessidentitäts-, UID-Isolations- oder External-Attestation-Grenze: Modus `0400` begrenzt nur Gruppen-/Other-Zugriff, während ein Akteur mit beliebigem Same-UID-Schreibzugriff auf den Parent-Evidence-Namespace außerhalb dieses lokalen Dateisystem-Trust-Modells bleibt. `FND-PARENT-0031` ist getrennt verifiziert; `FND-CROSS-0001` bleibt eine unabhängige stale-Cross-Evidence-Bedingung und eröffnet dieses verifizierte Finding nicht erneut. Der globale `master`-Fehler `FND-SONAR-0001` ist von dieser Verifikation unabhängig und wird weder akzeptiert noch unterdrückt. Es wird kein Risiko akzeptiert.

## Abschluss / Closure

Der aktuelle Nutzer autorisierte Abschluss und Archivierung. Die betroffenen Pfade sind bis Parent-Master `6ca7e1536ce7e93da68099db9c586b88852ff13e` unverändert, und `tests.test_generated_report_evidence_integrity` bestand in der 144-Test-Control-Suite.

## Historie / History

- `2026-07-18T12:50:18Z`: `validated_strict_result_file_authenticity_gap` — direkte strict/governance-Ausführungen und der kanonische Manifestvergleich bestätigten ausgelassene Missing-Input- und Hash-/Byte-Mismatch-Fehler. #55 bleibt unverändert; isolierte Parent-Fixture-first-Remediation folgt.
- `2026-07-18T13:53:55Z`: `fixture_first_remediation_locally_validated` — 25 fokussierte Negativ-/Kontrolltests weisen gefälschten Checksum/PASS-Inhalt, Missing/Raw/Foreign/Incomplete/Copy/Path/Schema-Fälle zurück und bewahren eine valide Zwölf-Zellen-Kontrolle. Der strikte Retained-Check scheitert nun fail closed; Governance-only bleibt Non-Runtime-Evidence. Ein unabhängiges Review ordnete synchronisiertes Mutable-Receipt-Rewriting dem getrennten `FND-PARENT-0031` zu.
- `2026-07-19T10:00:00Z`: `pr59_revalidation_found_unverified_present_input_receipts` — ein fokussiertes PR-#59-Diff-Review bestätigte, dass die strikte Status-Allowlist weiterhin einen nicht existierenden oder ersetzten kritischen Input akzeptierte, wenn Metadaten selbst `present` deklarierten. Die lokale Korrektur verlangt jetzt eine vertrauenswürdige reguläre Datei und einen passenden SHA-256; Missing-, Empty-, Symlink- und Digest-Mismatch-Kontrollen sowie eine legitime Kontrolle bestanden in der fokussierten Suite. `FND-PARENT-0031` bleibt getrennt und offen; kein Finding wird geschlossen und kein Risiko akzeptiert.
- `2026-07-19T13:43:18Z`: `pr59_lexical_parent_traversal_reproduced_and_locally_fixed` — `BUILD_ROOT:`-, `framework:`- und unpräfixierte `../...`-Receipts akzeptierten jeweils eine korrekt gehashte externe reguläre Datei, weil `.absolute()` lexikalische Traversal bewahrte. Die schmale `resolve(strict=False)`-Containment-Korrektur behält die Symlink-Ablehnung bei; 32 fokussierte Tests decken Original-/Alternativ-Traversal, Digest-Mismatch, Summary-/JSONL-Fallback und einen legitimen In-Root-Receipt ab. Delivery und Master-Verifikation bleiben ausstehend.
- `2026-07-19T14:19:05Z`: `pr59_final_synchronized_security_diff_scan_completed` — die begrenzte Korrektur ist als `fcdf9b2479486ad25c1e4bd4f28556b9339a1287` committed, mit Master `aabde81a9a315bf3e494e595ab0399357c596f9c` normal synchronisiert und am exakten Head `fb9becc76f903d68fa36c212cc60940a5e6e20c5` gepusht. Der versiegelte finale Scan deckt alle zehn Diff-Zeilen ab und findet keine neue reportable Feststellung. Remote-Checks, Reviews, SonarCloud, Merge und resultierende Master-Verifikation bleiben ausstehend.
- `2026-07-20T09:57:03Z`: `pr59_d4_current_head_fixed_pending_master_sync_and_post_merge_reproduction` — das aufbewahrte Artefakt SHA-256 `38e88188683330e57704bb3d4559c5604dbea303c1f305fb17e695545267107d` verifiziert PR-#59-Exact-Head `d4f88b886dac6fd5f483940015d6310bc239f814`: 33 erfolgreiche Checks, 6 erwartete Skips, erfolgreiche aktive Required Contexts, CodeQL mit 0 offenen Alerts, ein bestehendes SonarQube-Cloud-Quality-Gate, 0 eingereichte Reviews/Requests/Threads und einen bestehenden lokalen Exact-Diff-Check. Der PR ist weiterhin Draft und zwei Commits hinter Parent-`master` `9ef0619b9c00729c16b7056943d7843785223095`; das Finding ist deshalb `fixed`, nicht verified oder closed, bis normale Synchronisierung, frische Exact-Head-Validierung, autorisierter Merge und Post-Merge-Originalreproduktion erfolgen.
- `2026-07-20T15:09:01Z`: `verified_on_protected_pr59_squash_merge_parent_master` — exakter Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` bestand alle nicht übersprungenen PR-#59-Checks, erforderlichen geschützten Contexts, CodeQL, SonarQube Cloud Quality Gate, Issue Query und Zero-Review/Thread-Kontrollen. Passende Remote-Refs wurden mit `--match-head-commit` protected-squash als Parent-`master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` gemergt; dessen Source-Tree entspricht dem Source-Head. Aufbewahrte Detached-Master-Evidence dokumentiert 57/57 Integrity-Kontrollen, einschließlich fehlgeschlossener originaler Fälschungsreproduktionen für Identity/Result/Path/Symlink/Hash/Seal/Swap und einer bestehenden validen Full-Matrix-Kontrolle, plus bilingual 11/11, Shell-Syntax, Diff und clean/no-`.pyc`. Das Finding wechselt von `fixed` zu `verified`, niemals `closed`; sein eigener Release-Blocker ist `false` und kein Risiko wird akzeptiert. Der globale `master`-Fehler `FND-SONAR-0001` ist unabhängig und wird weder akzeptiert noch unterdrückt.
