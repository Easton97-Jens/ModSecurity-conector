# Finding-Index

Dies ist der kanonische Index des aktiven lokalen Finding-Bestands. `finding.json`
ist die strukturierte Quelle; die EN- und DE-Dateien sind äquivalente
Leserfassungen. Ein Eintrag wird nur nach Prüfung des ursprünglichen Root-
Cause- oder Closure-PRs, des erreichbaren Merges, aktueller Source-/Scanner-
oder Control-Evidence und anwendbarer Checks geschlossen; der aktuelle Abgleich
verschob nur sieben solche Records.

- Generated / Erzeugt: `2026-08-01T18:28:20Z`
- Active canonical Finding-directory count / Aktive kanonische Finding-Verzeichnisanzahl: `73`; eine getrennt inventarisierte historische ID bleibt ein reserviertes Verzeichnis ohne kanonisches Tripel.
- Reconciliation / Abgleich: [Audit-Matrix 2026-08-01](reconciliation-2026-08-01.de.md) dokumentiert eine Aktion für jedes ursprünglich aktive kanonische Finding und die sieben strengen Archiventscheidungen.
- Bootstrap status / Bootstrap-Status: `complete; reconciliation recorded`
- Aktuelle PR-#225-CI-Evidence-Sonar-Remediation: [`FND-SONAR-0031`](FND-SONAR-0031/finding.de.md)
  ist Parent P2 `verified` / `feasible_now`, nicht release-blocking, kein
  Candidate-Integration-Blocker und sicherheitsrelevant. Der geschützte exakte
  Head `74bcb950f8a75835b4fb59175a783e9aedcfd1c3` mergte normal als Master
  `6dc912643133e5c7d3c305979d4052da9cb45153`; alle 14 Exact-Master-Workflows
  bestanden. Der Resulting-Master-Readback schließt alle 15 aufbewahrten
  `python:S3776`-Keys und dokumentiert null `ci/evidence`-Duplikatzeilen. Die
  getrennte globale Master-Quality-Gate-`new_security_rating`-E-Baseline bleibt
  `FND-SONAR-0001`.
- Aktuelle finale Common-Sonar-Remediation: [`FND-SONAR-0028`](FND-SONAR-0028/finding.de.md)
  und [`FND-SONAR-0029`](FND-SONAR-0029/finding.de.md) sind Parent-`verified` /
  `feasible_now`, nicht release-blocking, keine Candidate-Integration-Blocker
  und sicherheitsrelevant. GitHub mergte exakten PR-#221-Head
  `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d` normal als Parent-master
  `3270ab5bdcc86ddab50e9be00db7611aae7fd937`; alle 14 Exact-Master-Workflows
  bestanden. Die direkte Resulting-Master-SonarQube-Cloud-Abfrage meldet die
  zurückbehaltenen Original-`c:S3776`- und `pythonsecurity:S8705`-Befunde als
  `FIXED/CLOSED`. Die globale Master-Quality-Gate-Security-Rating-Baseline wird
  getrennt unter `FND-SONAR-0001` verfolgt.
- Aktueller PR-#183-Resulting-Master-Abgleich: Parent-master
  `154ee724eba4653fa6378fc3c8729ae433e65697` ist tree-identisch zu finalem
  PR-#183-Head `4e4dfb36e1b05f7eda38450fd3710e3a04905118` (Tree
  `c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0`), und alle 14 Master-SHA-Workflows
  waren erfolgreich. `FND-PARENT-0064` ist `verified`, nicht closed, nachdem
  detached-master `make check-apache-ruleset-cleanup` fünf Python-Contracts und
  den nativen GCC-APR-Harness bestand; seine breitere Live-Apache-Sequenz bleibt
  offen. `FND-PARENT-0070` und `FND-PARENT-0071` sind `fixed`, nicht verified,
  und warten jeweils auf frische Master-APXS-/DSO-/HTTP- bzw.
  Live-Start-/Readiness-/403-/`SIGUSR1`-Evidence. `FND-PARENT-0072` ist
  `fixed`, nicht verified, und wartet auf direkte Sonar-Master-Analyse- und
  Issue-Abfrage-Evidence.
- Aktuelle Apache-Lifecycle-Remediation / Current Apache lifecycle remediation:
  `FND-PARENT-0064` ist Parent P1 `verified` / `feasible_now`, nicht
  blockierend und sicherheitsrelevant. PR #183 mergte als Master
  `154ee724eba4653fa6378fc3c8729ae433e65697` mit einem Tree, der dem finalen
  Head `4e4dfb36e1b05f7eda38450fd3710e3a04905118` entspricht; alle 14 exakten
  Master-Workflows bestanden. Detached-Master `make check-apache-ruleset-cleanup`
  bestand fünf Python-Contracts und den nativen GCC-APR-Harness. Eine breite
  frische Live-Apache-Konfigurations-/Readiness-/Phase-2-`403`-/`SIGUSR1`-
  Sequenz bleibt vor Closure erforderlich.
- Aktueller Apache-Debug-Name-Lifecycle-Leak / Current Apache debug-name
  lifecycle leak: `FND-PARENT-0067` ist Parent P2 `validated` /
  `feasible_now`, nicht blockierend und nicht sicherheitsrelevant. Der
  aufbewahrte private Graceful-Memcheck-Receipt
  `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/graceful-memcheck/memcheck.8.log`
  (SHA-256 `a49ca3a72f06aef4f4e67bab0b57056fe785c95a1dfba2361a892fbbf497b931`)
  dokumentiert `66` definitiv verlorene Bytes in `3` `strdup`-basierten
  Blöcken und keine Invalid-free/read/write- oder UAF-Diagnose. Er ist von
  `FND-PARENT-0064` getrennt; in der aktuellen Aufgabe ist keine Source-
  Reparatur enthalten.
- Aktuelle Parent-CI-Body-Processor-Read-Grenze:
  FND-PARENT-0065 ist Parent P2 `validated` / `feasible_now`, nicht
  blockierend und sicherheitsrelevant. Aufbewahrte Pre-Fix-Evidence beweist,
  dass eine traversalhaltige Artefakt-case_id request_body_bytes() dazu bringen
  kann, Vorschau und SHA-256 nur des festen Suffix conf/request-body.bin
  außerhalb der Safe Root offenzulegen. Eine In-Root-Symlink-der-nach-außen-
  auflöst-Kontrolle ist für die Remediation-Validierung aufbewahrt. Lokale
  Candidate-Evidence ändert den Status nicht zu fixed oder verified.
- Aktuelle Parent-CI-Full-Matrix-Control-Evidence-Grenze:
  `FND-PARENT-0066` ist Parent P2 `fixed` / `feasible_now`, nicht blockierend
  und sicherheitsrelevant. Der lokale Helper failt jetzt closed, wenn ein
  Producer `pass` erklärt, aber keine Live-`403`-Control-Evidence vorliegt;
  aufbewahrte Pre-/Post-Fix-Receipts und ein vollständiger Security-Diff-Scan
  über zwei Pfade liegen vor. Der exakte Head von Draft-PR #178 hat alle 33
  Hosted-Checks bestanden, und SonarQube Cloud meldet Quality Gate `OK` mit
  null offenen PR-Issues und null neuen Violations/Duplicate Lines. Eine
  Original-Reproduktion auf dem resultierenden Master bleibt vor `verified`
  erforderlich.
- Aktuelle Apache-Cleanup-Runner-Output-Confinement-Grenze:
  `FND-PARENT-0068` ist Parent P3 `in_progress` / `feasible_now`, kein
  globaler oder PR-#183-Candidate-Integration-Blocker und sicherheitsrelevant.
  Der PR-#183-RulesSet-Runner verwendet ein validiertes privates temporäres
  Leaf; der zurückgehaltene Pre-Remediation-Bericht (SHA-256
  `05bcf8565c7de8f6fcadf2f607e8266ff762fd5e7296d9434066c78a4eada6f7`)
  dokumentiert den früheren lokalen/shared-host-Race eines vorhersagbaren
  `/var/tmp`-Output-Baums vor Compiler-Output-Execution. GitHub-External-PR-/
  Token-Eskalation ist widerlegt; nur der bereits bestehende Request-
  Transaction-Sibling bleibt in progress. Es wird kein Closure-Claim erhoben.
- Aktuelle Apache-GCC-C17-Baseline-Compiler-Hardening-Gruppe:
  FND-PARENT-0069 ist Parent P2 validated / feasible_now und
  sicherheitsrelevant, aber weder ein Release-Blocker noch ein
  Candidate-Integration-Blocker für selektives #94A. Zurückgehaltene Master-
  und Kandidatenläufe enden beide mit Exit 1; ihr mod_security3.c-Source-Hash
  ist 8b21b64c95a1f1cb98ac05437e60e5d5ab8124e363cd2784b7c800e65449f8d7 und
  die 114-zeiligen Diagnosen normalisieren zu
  34b8bbdfcda5e8420a33ac99eaf57a1283388ec7f87d104b1ee36093744eacc6.
  Dies ist eine bereits bestehende Compiler-Hardening-Luecke, absichtlich von
  FND-PARENT-0008 und FND-PARENT-0043 getrennt; es wird kein Source-Fix- oder
  Delivery-Claim erhoben.
- Aktuelle Apache-APXS-DSO-Materialisierungsgrenze:
  FND-PARENT-0070 ist Parent P1 `fixed` / `feasible_now`, sicherheitsrelevant
  und ein Release-Blocker für normale Apache-Builds, bis frische Resulting-
  Master-APXS-Materialisierung, DSO-make, Modul-Load und HTTP-Control bestehen.
  Der gemergte Wrapper staged den erwarteten privaten Header, der Master-Tree
  entspricht dem validierten PR-Tree, und der Apache/Common-Struktur-Control
  besteht. Er ist kein Candidate-Integration-Blocker und weder verified noch
  closed.
- Aktuelle Apache-Smoke-MIME-Runtime-Grenze:
  FND-PARENT-0071 ist Parent P1 `fixed` / `feasible_now`, sicherheitsrelevant
  und ein Release-Blocker für Apache-Smoke-/Runtime-Akzeptanz, bis eine frische
  Resulting-Master-Live-Start-/Readiness-/HTTP-`403`-/`SIGUSR1`-Sequenz besteht.
  Der gemergte Harness materialisiert beide MIME-Pfade, und sechs fokussierte
  Resulting-Master-Apache/MIME-Unit-Tests bestehen. Sie ist von
  FND-PARENT-0070 getrennt und beweist nicht allein die FND-PARENT-0064-APR-
  Lifecycle-Reparatur.
- Finding-Archiv / Finding archive:
  [`.codex/archive/findings/`](../archive/findings/README.md) enthält
  einhundert nicht aktive, verlustfrei aufbewahrte Records nach diesem Archiv-Move; ihre aktuellen
  Lifecycle-Status und Release-Blocker-Flags sind dort weiterhin dokumentiert.
- Aktuelles FND-HOST-Nutzerarchiv / Current-user FND-HOST archive:
  `FND-HOST-0001` und `FND-HOST-0005` sind als `verified` archiviert;
  `FND-HOST-0002` und `FND-HOST-0004` als nutzerbezogenes
  `not_applicable`, nicht technisch geschlossen. Die exakten nicht verfügbaren
  lokalen Python-/Native-/Optional-Tool- und HTTP/3-Client-/Harness-Zustände
  bleiben in ihren aufbewahrten Tripeln; `FND-HOST-0003` und
  `FND-HOST-0006` bleiben aktiv.
- Framework-Archivabgleich / Framework archive reconciliation:
  `FND-CROSS-0006`, `FND-FRAMEWORK-0004`, `0021`, `0022`, `0026`, `0027`,
  `0028`, `0045`, `0049`, `FND-SONAR-0002` und `FND-SONAR-0005` sind nun
  nicht aktive Archiv-Records. `FND-FRAMEWORK-0031` liegt ebenfalls im
  test-only Archiv des aktuellen Nutzers: Sein P1-Release-Blocker-Flag und die
  ausstehende Cloud-Neubewertung bleiben wirksam; technisch geschlossen ist es
  nicht.
- Framework-PR-#50/#51-Resulting-Master-Archiv / Framework PR #50/#51
  resulting-master archive: `FND-FRAMEWORK-0002`, `0011`, `0053` und `0056`
  sind nach exaktem Framework-Master
  `de705a5efb872f95f010346fe2e6143c88876ad4` geschlossen und nicht aktive
  Archiv-Records. Receipt-SHA-256: `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`.
  `FND-FRAMEWORK-0057` bleibt aktiv: Parent hat den Framework-Gitlink
  übernommen, aber der frische Parent-#74-Producer und das strikte Terminal-
  Gate sind nicht belegt.
- Framework-PR-#52-Resulting-Master-Archiv / Framework PR #52 resulting-
  master archive: `FND-FRAMEWORK-0010` ist nach dem normalen Merge von PR #52
  als Framework-Master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` geschlossen.
  Der geprüfte Head-Tree entspricht resultierendem Master; seine fokussierten
  negativen/legitimen Controls, das Dokumentationsaggregat und die anwendbaren
  Master-Checks bestehen. Receipt-SHA-256:
  `cbf90db531a6e4eab99ae84de6ba1008a07d6644b9805dcae2745fc54ad2aee9`.
- Framework-Current-Master-Finding-Batch / Framework current-master finding
  batch: `FND-FRAMEWORK-0013`, `0018`, `0019`, `0036` und `0054` sind auf
  exaktem Framework-master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`
  `verified`. Der aufbewahrte Receipt
  `.codex/runs/20260726-framework-findings-batch/evidence/current-master-revalidation.md`
  (SHA-256 `6912df100503c87123b72e4fac4cc76d6c8bf9f40f884786eeedfcebe0614f3c`)
  dokumentiert fokussierte negative und legitime Controls, historische
  PR-/Readback- sowie Current-Master-Checks. `FND-FRAMEWORK-0057` ist allein
  durch Parent-#74-Terminal-Evidence `blocked`; Parent-Gitlink und MRTS-Status
  blieben unverändert. Die fünf verifizierten Records sind nun verlustfrei
  archiviert. `FND-FRAMEWORK-0025` und `0029` sind als lokales test-only
  `accepted_risk` archiviert, nicht technisch geschlossen; ihre externen
  Helper-/Cloud-Voraussetzungen bleiben ungelöst.
- Aktuelles Nutzerarchiv fester nicht blockierender Framework-Findings /
  Current-user fixed non-blocking Framework archive: `FND-FRAMEWORK-0003`,
  `0005`, `0006`, `0012`, `0014`, `0015`, `0016`, `0023`, `0024`, `0033`
  und `0055` sind nach der Auswahl des aktuellen Nutzers für das exakte
  Prädikat `fixed` / `release_blocker: false` verlustfrei als nicht aktive
  Archiv-Records aufbewahrt. Ihre Lifecycle-Werte, Release-Blocker-Flags und
  Evidence bleiben unverändert; dies ist weder ein Abschluss noch eine neue
  Release-Readiness-Aussage.
- Test-only-Archiv fester Release-Blocker / Test-only fixed release-blocker
  archive: Der aktuelle Nutzer archivierte zusätzlich neunundzwanzig exakt
  als `fixed` markierte Records mit weiterhin `release_blocker: true`, einschließlich
  sicherheitsrelevanter P0/P1-Records, weil dieses Repository nur zum Testen
  verwendet wird und kein Release geplant ist. Dies markiert sie nicht als
  verified, akzeptiert, produktionssicher oder nicht blockierend; ihre
  aufbewahrten Records und die erforderliche spätere Reaktivierung vor jedem
  Release sind im Archiv-README dokumentiert.
- Hinweis zum historischen Status / Historical-status note: Datierte PR- und
  Master-Notizen weiter unten behalten ihre damalige Formulierung. Für eine im
  obigen Archivabgleichen genannte ID sind Archivmitgliedschaft und
  aufbewahrter kanonischer Record maßgeblich für ihren aktuellen aktiven oder
  nicht aktiven Zustand.
- Aktive Erweiterungs-Runs / Active extension source runs: `20260722T145132Z-framework-pr-39-41-master-integration-9a3c7dc7`, `20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`, `20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37`, `20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09`, `20260723T092456Z-framework-sonarqube-test-issues-507-10387697`, `20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a`, `20260724T170026Z-worktree-cleanup-governance`, `20260726T000000Z-mrts-codex-config-reconciliation-current`, `20260726T050327Z-framework-pr45-master-integration`, `20260726T051835Z-framework-pr45-boundary-snapshot`, `20260726T000000Z-pr55-pr74-python314-import`, `20260726T083705Z-apache-upstream-pr-91-94-integration`, `20260726T103539Z-pr74-cache-owner-root`, `merge-prs-129-149-master-20260728`, `sonar-652-duplication-zero-20260728-W8wqjk`, `pr151-verified-16c3-20260728`, `pr152-verified-c9c-20260728`, `pr153-verified-c5a-20260728`, `pr154-verified-60a-20260728`, `pr156-initial-e2b-20260728`, `pr156-verified-59ff-20260728`, `pr157-verified-3055-20260728`, `pr158-verified-552f-20260728`, `pr159-verified-cf32-20260728`
- Zusätzlicher aktiver Erweiterungs-Run / Additional active extension source run:
  pr160-terminal-open-s1481-e456-20260728 ist als terminale,
  remediation-required-Draft-PR-Evidence aufbewahrt.
- Neuester aktiver Erweiterungs-Run / Latest active extension source run:
  pr160-terminal-open-s1481-e456-20260728 bewahrt einen terminalen Draft-PR-
  Blocker auf; er ändert den aktiven Aggregat-Lifecycle nicht.
- Aktueller Exact-Head-SonarQube-Cloud-Blocker von Draft-Parent-PR #160 /
  Current Draft Parent PR #160 exact-head SonarQube Cloud blocker: Der
  versiegelte Run pr160-terminal-open-s1481-e456-20260728 für exakten Head
  e456b9fc909116656294fc744526cf8c81b0c962 gegen Basis master
  8e8acb8dab1cd03723de269cab7da7dd62e5e010 meldet drei OPEN task-eigene
  MINOR-CODE_SMELL-python:S1481-Findings in
  ci/checks/connectors/all/check-remaining-connectors-start-wiring.py:
  AZ-p4PPg1eeMvlV2M02- Zeile 66 (rc_default),
  AZ-p4PPg1eeMvlV2M03A Zeile 68 (kill_zero) und
  AZ-p4PPg1eeMvlV2M02_ Zeile 69 (wait_command). Das Quality Gate ist OK, und
  neue Duplikatzeilen/-dichte sind 0/0.0; die direkte Issue-Anzahl macht
  diesen Head jedoch remediation_required. Alle 39 exakten-SHA-GitHub-Checks
  sind terminal (33 success, sechs scope-skipped), einschließlich
  erfolgreicher SonarCloud Code Analysis; projektweite Duplikatzeilen/-dichte
  bleiben 1260/0.2. PR #160 bleibt Draft, offen, mergeable und ungemergt.
  FND-SONAR-0016 bleibt P1 in_progress; keine Policy-, Suppression-,
  Exclusion-, Framework-/MRTS-Quelltext-, Gitlink-, Ready-for-review-, Merge-,
  master-/Default-Branch- oder globale Abschluss-Aktion wird behauptet.
- Aktuelles Draft-Parent-PR-#74-Hosted-Follow-up / Current Draft Parent PR #74 hosted follow-up:
  Der retained Receipt 20260726T185607Z-pr74-fast-validation-hosted-followup
  (SHA-256 5c64b4fe03ed670b0d2c25c58c2f770b59ae53bab10851ced35bd9012117d956)
  eröffnet FND-SONAR-0016 erneut als P1 / in_progress: Quality Gate ERROR
  hat 19 OPEN task-eigene Findings und 0,0 % New-Code-Duplizierung. Das neue
  FND-PARENT-0057 verfolgt getrennt die plausible Template-zu-Shell-/S8707-
  Korrektur, die den Legacy-Output-File-Pfad durch einen Private-Stage-Parent-
  Environment-Handoff entfernt; FND-PARENT-0058 verfolgt getrennt den
  validierten Full-Matrix-Port-Range-Reliability-Defekt mit seinem
  fail-closed-Plan 1024..65000. Das neue FND-PARENT-0059 verfolgt getrennt
  den validierten Stale-Full-Matrix-Lock-Denial-of-Service und die
  Shell-gehaltene, geerbte-FD-9-Kernel-Lock-Grenze: SIGKILL nur des
  Scheduler-Parents lässt den Lock aktiv, bis der letzte Job-/Make-Nachfahr
  endet. FND-PARENT-0060 verfolgt nun den lokal fixed Non-Work-Conserving-
  Batch-Scheduler: Seine benannte Refill-Regression und ein kombinierter
  107-Test-Scheduler-Run bestanden, während Hosted-Successor-Verifikation
  aussteht. Das neue FND-PARENT-0061 verfolgt getrennt den lokal fixed
  Worker-Wrapper-FIFO-Completion-Watchdog: Die fokussierte Wrapper-Death-
  Regression endet mit 77 und verwendet FD 9 später wieder, während Hosted-
  Successor-Verifikation aussteht. PR #74 bleibt Draft und es wird keine
  Delivery-Aktion behauptet.
- Aktueller Draft-Parent-PR-#138-SonarQube-Cloud-Follow-up / Current Draft
  Parent PR #138 SonarQube Cloud follow-up: Das bestehende Aggregat
  `FND-SONAR-0016` dokumentiert auch den exakten Head
  `e522e43f0957368853772d747a0ffaa38ba76615`: Quality Gate `ERROR` allein
  durch 20 neue duplizierte Zeilen (5.649717514124294% gegenüber 3%) und ein
  neues `python:S3776`-Issue. Der begrenzte Receipt
  `sonar-open-1022-20260727/evidence/pr138-quality-gate-observation.json`
  hat SHA-256
  `96299299690bf6d83a9348e6bea5d42e2f13c795c57bf8cedbfa37c48fedca24`.
  Der korrigierende Source-Batch ist `feasible_now`; der PR bleibt Draft und
  es erfolgten keine Scanner-Policy-, Suppression-, Framework-, MRTS-,
  Gitlink-, Ready-for-review-, Merge- oder externe Disposition-Aktion.
- Aktueller Draft-Parent-PR-#151-SonarQube-Cloud-Follow-up / Current Draft
  Parent PR #151 SonarQube Cloud follow-up: `FND-SONAR-0016` bewahrt den
  Zwischen-`c:S3776`-Receipt `AZ-ovroGM5o_ow3fPM0Z` vom exakten Head
  `ea52192f30ca091f9389eb10c87e9a99e2bbab4c` und den sauberen finalen
  exakten Head `16c3aa5d87e603de718d4a94a6d57afae159fc53`. Der retained
  All-Check-Run `pr151-verified-16c3-20260728` hat null Sonar-PR-Issues,
  Quality Gate `OK`, null neue Duplikatzeilen bei Dichte `0.0` sowie alle 39
  GitHub-Checks abgeschlossen (33 `success`, sechs scope-justified `skipped`,
  null unvollendete). PR #151 bleibt Draft und ungemergt; dies ist nur ein
  task-eigenes Draft-PR-Remediation-Ergebnis, keine Master- oder globale
  Backlog-Aussage.
- Aktueller Draft-Parent-PR-#152-SonarQube-Cloud-Follow-up / Current Draft
  Parent PR #152 SonarQube Cloud follow-up: Der historische Head `ba8d` hatte
  `S1192`; der exakte Follow-up-Head
  `c9c011117bd4d9c910aa4d1a767916d50c9bd26a` ist durch
  `pr152-verified-c9c-20260728` unter
  `/var/tmp/codex/ModSecurity-conector/pr152-verified-c9c.5uh08S` aufbewahrt.
  Seine `SHA256SUMS` validieren den Receipt: null OPEN/CONFIRMED-Sonar-PR-
  Issues, Quality Gate `OK`, neue Duplikatzeilen `0`, New-Duplication-Density
  `0.0` und alle 39 GitHub-Checks abgeschlossen (33 `success`, null `neutral`,
  sechs scope-justified `skipped`). PR #152 bleibt Draft, `OPEN` und
  ungemergt; `FND-SONAR-0016` bleibt P1 `in_progress`, weil die globalen
  `652/zero`-Ziele, historische #74, #138 und der breitere Backlog fortbestehen.
  Es erfolgten keine Sonar-Policy-, Suppression-, Exclusion-, Framework-/MRTS-
  Quelltext-, Gitlink-, Ready-for-review-, Merge- oder Master-Aktion.
- Aktueller Draft-Parent-PR-#153-SonarQube-Cloud-Follow-up / Current Draft
  Parent PR #153 SonarQube Cloud follow-up: Der task-eigene `S1066`-Receipt
  `AZ9cRy9OHhV2CayPTP4Z` ist am exakten Head
  `c5a45dff07ceb11eb84bc7854e6d7ca034dc9bc4` behoben und durch
  `pr153-verified-c5a-20260728` unter
  `/var/tmp/codex/ModSecurity-conector/pr153-verified-c5a.ivXh4u` aufbewahrt.
  Seine `SHA256SUMS` validieren den Receipt: null OPEN/CONFIRMED-Sonar-PR-
  Issues, Quality Gate `OK`, neue Duplikatzeilen `0`, New-Duplication-Density
  `0.0` und alle 39 GitHub-Checks abgeschlossen (33 `success`, null `neutral`,
  sechs scope-justified `skipped`). PR #153 bleibt Draft, `OPEN` und
  ungemergt; `FND-SONAR-0016` bleibt P1 `in_progress`, weil die globalen
  `652/zero`-Ziele, Default-Branch, historischen #74, #138 und der breitere
  Backlog fortbestehen. Es erfolgten keine Sonar-Policy-, Suppression-,
  Exclusion-, Framework-/MRTS-Quelltext-, Gitlink-, Ready-for-review-, Merge-
  oder Master-Aktion.
- Aktueller Draft-Parent-PR-#154-SonarQube-Cloud-Follow-up / Current Draft
  Parent PR #154 SonarQube Cloud follow-up: Drei task-eigene `S1192`-Receipts
  `AZ9cRyqOHhV2CayPTPzr`, `AZ9cRyqOHhV2CayPTPzq` und
  `AZ9cRyZWHhV2CayPTPwQ` sind am exakten Head
  `60a13292c9173a760f94672c6855a97099d1fcc2` sauber. Der aufbewahrte
  All-Check-Run `pr154-verified-60a-20260728` unter
  `/var/tmp/codex/ModSecurity-conector/pr154-verified-60a.Hr5Ki8` hat
  validierte `SHA256SUMS`, null OPEN/CONFIRMED-Sonar-PR-Issues, Quality Gate
  `OK`, neue Duplikatzeilen `0`, New-Duplication-Density `0.0` und alle 39
  exakten-SHA-GitHub-Checks terminal, einschließlich erfolgreicher
  `SonarCloud Code Analysis`. PR #154 bleibt Draft, `OPEN` und ungemergt;
  `FND-SONAR-0016` bleibt P1 `in_progress`, weil die globalen `652/zero`-
  Ziele, Default-Branch, historischen #74, #138 und der breitere Backlog aktiv
  bleiben. Es erfolgten keine Sonar-Policy-, Suppression-, Exclusion-,
  Framework-/MRTS-Quelltext-, Gitlink-, Ready-for-review-, Merge- oder Master-
  Aktion.
- Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #159 / Current Draft Parent PR #159 bounded exact-head SonarQube Cloud
  result: Der versiegelte Run `pr159-verified-cf32-20260728` unter
  `/var/tmp/codex/ModSecurity-conector/runs/pr159-exact-head-cf32-20260728.B9kyWO`
  hat validierte `SHA256SUMS` für den exakten Head
  `cf323de85b4411b2c1f56055a430d43f65a8ed97` gegen Basis `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`. Die PR-Beschreibung identifiziert
  zwei Parent-`shelldre:S1192`-Literal-Duplikatbefunde in
  `connectors/lighttpd/harness/run_patched_full_lifecycle.sh` für
  `%{http_code}` an acht Status-Probes und `1,200p` an sechs Diagnosepfaden;
  kein ursprünglicher Sonar-Key wird abgeleitet. Direkte Sonar-Issues sind `0`,
  das Quality Gate ist `OK`, neue Duplikatzeilen/-dichte sind `0`/`0.0`,
  projektweite Duplikatzeilen/-dichte bleiben `1260`/`0.2`, und alle 39
  exakten-SHA-GitHub-Checks sind terminal (33 `success`, sechs scope-skipped),
  einschließlich erfolgreicher `SonarCloud Code Analysis` mit null
  Annotations; Reviews und Review-Kommentare sind beide `0`. PR #159 bleibt
  Draft, offen, mergeable und ungemergt. Dies ist nur begrenzte Draft-PR-
  Evidence: `FND-SONAR-0016` bleibt P1 `in_progress`; keine Policy-,
  Suppression-, Exclusion-, Framework-/MRTS-Quelltext-, Gitlink-, Ready-for-
  review-, Merge-, Master- oder globale Abschluss-Aktion wird behauptet.
- Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #158 / Current Draft Parent PR #158 bounded exact-head SonarQube Cloud
  result: Der versiegelte Run `pr158-verified-552f-20260728` unter
  `/var/tmp/codex/ModSecurity-conector/pr158-verified-552f.umSut7` hat
  validierte `SHA256SUMS` für den exakten Head
  `552fd67ee1212c0a71cec1726f6a079e33671c87` gegen Basis `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`. Sein Manifest benennt nur eine
  Parent-HAProxy-HTX-Diagnostic-Range-`shelldre:S1192`-Remediation, ohne einen
  ursprünglichen Sonar-Key oder Source-Ort abzuleiten. Direkte Sonar-Issues
  sind `0`, das Quality Gate ist `OK`, neue Duplikatzeilen/-dichte sind
  `0`/`0.0`, und alle 39 exakten-SHA-GitHub-Checks sind terminal (33
  `success`, sechs scope-justified `skipped`), einschließlich erfolgreicher
  `SonarCloud Code Analysis`; Reviews und Review-Kommentare sind beide `0`.
  PR #158 bleibt Draft, offen, mergeable und ungemergt. Dies ist nur begrenzte
  Draft-PR-Evidence: `FND-SONAR-0016` bleibt P1 `in_progress`, weil globales
  `652/zero`-Ziel, Default-Branch, historische #74/#138 und breiterer Backlog
  aktiv bleiben. Keine Policy-, Suppression-, Exclusion-, Framework-/MRTS-
  Quelltext-, Gitlink-, Ready-for-review-, Merge-, Master- oder globale
  Abschluss-Aktion wird behauptet.
- Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #156 / Current Draft Parent PR #156 bounded exact-head SonarQube Cloud
  result: `FND-SONAR-0016` bewahrt den initialen exakten Head
  `e2b1370caa32e621ada4ce96ad03f603904cee49` / Run
  `pr156-initial-e2b-20260728` als historische Sieben-OPEN-`python:S3415`-
  Beobachtung. Sein versiegelter Successor-Run `pr156-verified-59ff-20260728`
  unter `/var/tmp/codex/ModSecurity-conector/pr156-verified-59ff.Ce1cD4` hat
  validierte `SHA256SUMS` für exakten Head
  `59ff4d5bbb6e278d93c0b965096e842b77f446bb` gegen Base `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`: direkte Sonar-Issues `0`,
  Quality Gate `OK`, neue Duplikatzeilen/-dichte `0`/`0.0` und alle 39
  exakten-SHA-GitHub-Checks terminal (33 `success`, sechs scope-justified
  `skipped`), einschließlich erfolgreicher `SonarCloud Code Analysis` mit null
  Annotations. PR #156 bleibt Draft, `OPEN` und ungemergt; dies ist nur
  begrenzte Draft-PR-Evidence. `FND-SONAR-0016` bleibt P1 `in_progress`, weil
  globale `652/zero`-Ziele, Default-Branch, historische #74/#138 und breitere
  Backlog-Arbeit aktiv bleiben. Es erfolgten keine Sonar-Policy-, Suppression-,
  Exclusion-, Framework-/MRTS-Quelltext-, Gitlink-, Ready-for-review-, Merge-
  oder Master-Aktion.
- Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #157 / Current Draft Parent PR #157 bounded exact-head SonarQube Cloud
  result: Der ursprüngliche Parent-`python:S1192`-Receipt
  `AZ9cRyW7HhV2CayPTPuq` lag bei
  `ci/checks/documentation/check-bilingual-docs.py:728` in
  `check_tools_mrts_clean(repo)`. Der versiegelte Run
  `pr157-verified-3055-20260728` unter
  `/var/tmp/codex/ModSecurity-conector/pr157-verified-3055.dvn7gp` hat
  validierte `SHA256SUMS` für den exakten Head
  `3055790e88e6b962bdffdabadccee1de2ce59355` gegen Basis `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`: direkte Sonar-Issues `0`,
  Quality Gate `OK`, neue Duplikatzeilen/-dichte `0`/`0.0` und alle 39
  exakten-SHA-GitHub-Checks terminal (33 `success`, sechs scope-justified
  `skipped`), einschließlich erfolgreicher `SonarCloud Code Analysis` mit null
  Annotations. PR #157 bleibt Draft, `OPEN` und ungemergt. Dies ist nur
  begrenzte Draft-PR-Evidence: `FND-SONAR-0016` bleibt P1 `in_progress`, weil
  globales `652/zero`-Ziel, Default-Branch, historische #74/#138 und breiterer
  Backlog aktiv bleiben. Keine Sonar-Policy-, Suppression-, Exclusion-,
  Framework-/MRTS-Quelltext-, Gitlink-, Ready-for-review-, Merge-, Master- oder
  globale Abschluss-Aktion wird behauptet.
- Aktueller Draft-Parent-PR-#155-SonarQube-Cloud-Follow-up / Current Draft
  Parent PR #155 SonarQube Cloud follow-up: Vier saubere task-eigene Receipts
  `AZ98JczJLJyjbmyNA5LW`, `AZ98JczJLJyjbmyNA5LO`,
  `AZ98JczJLJyjbmyNA5LS` und `AZ98JczJLJyjbmyNA5LU` sind am exakten Head
  `0e980f6c2a46ef92f14a007bc8d0c6d538885192` durch
  `pr155-verified-0e9-20260728` unter
  `/var/tmp/codex/ModSecurity-conector/pr155-verified-0e9.NkGL9s` aufbewahrt.
  Seine `SHA256SUMS` validieren null OPEN/CONFIRMED-Sonar-PR-Issues, Quality
  Gate `OK`, neue Duplikatzeilen `0`, New-Duplication-Density `0.0` und alle
  39 exakten-SHA-GitHub-Checks terminal (33 `success`, sechs
  scope-justified `skipped`), einschließlich erfolgreicher `SonarCloud Code
  Analysis`. PR #155 bleibt Draft, `OPEN` und ungemergt; `FND-SONAR-0016`
  bleibt P1 `in_progress`, weil globale `652/zero`-Ziele, Default-Branch,
  historische #74/#138 und breitere Backlog-Arbeit aktiv bleiben. Es
  erfolgten keine Sonar-Policy-, Suppression-, Exclusion-, Framework-/MRTS-
  Quelltext-, Gitlink-, Ready-for-review-, Merge- oder Master-Aktion.
- Aktueller Draft-Parent-PR-#150-SonarQube-Cloud-Follow-up / Current Draft
  Parent PR #150 SonarQube Cloud follow-up: `FND-SONAR-0019` ist am exakten
  Head `4dae04f2d584da855139d6f42ab36c1bdf8c8d63` `fixed`. GitHub bindet einen
  erfolgreichen SonarCloud-Check an diese SHA, und der aufbewahrte PR-Readback
  hat Quality Gate `OK` sowie null OPEN/CONFIRMED-Issues. Der Befund bleibt
  fixed, nicht verified oder closed, bis separat autorisierte Integration und
  eine Current-Master-Nachprüfung erfolgen; keine Scanner-Policy, Suppression,
  Framework, MRTS, Gitlink-, Ready-for-review- oder Merge-Aktion erfolgte.
- Aktuelle Normal-Provisioner-Provenance-Validierung / Current normal-
  provisioner provenance validation: `FND-PARENT-0063` ist P3 `validated` /
  `requires_user_decision`, security-relevant aber nicht release-blocking. Die
  zurückgehaltene Offline-Production-Module-Fixture führte einen synthetischen
  geänderten `releases/latest`-Tag mit `strict=True` durch
  `prepare_release_git_component` bis zum realen Go-Build-Sink, ohne
  Netzwerk-Kontakt oder Upstream-Ausführung. Geplante/manuelle Provisioner-
  Workflows verwenden `contents: read` und `persist-credentials: false`; es
  wurden kein `pull_request_target`, keine Secret-Referenz und kein
  schreibbares Repository-Token gefunden. Der im Scope liegende Supply-Chain-
  Pfad ist low/P3, weil ein Upstream-Kompromiss erforderlich ist. Vor der
  Remediation sind eine aktuelle Immutable-Provenance-Auswahl und eine
  getrennte Framework-Write-Autorisierung erforderlich, falls Defaults
  Framework-owned sind.
- Aktueller Parent-master-Python-Workflow-Inventarvertragsfehler / Current
  Parent master Python workflow inventory contract failure: `FND-PARENT-0062`
  ist P1 `validated` / `feasible_now` und release-blocking. Auf aktuellem
  Parent-master `dd175053b3d7f509286af87646d6eb093a49d578` verlangt das exakte
  Inventar weiterhin
  `verified-report-governance.yml:verified-report-contract-preflight`, aber
  dieser Job fehlt im Workflow. Der Current-Master-Equivalent-Scope-Control
  endet mit `0`, während `rtk proxy make check-python-version-contract` mit
  `2` endet; die aufbewahrte Receipt-SHA-256 ist
  `17ae8b2b76e65e4f9db7625122b56f5d74c171bed69912f6ba2a68198b3b283e`.
  Der getrennte fokussierte Parent-Alignment-PR muss kanonisches Python-Setup
  und Workflow-Trust-Controls bewahren, eine Regression ergänzen und Hosted-
  Proof einholen; er darf nicht stillschweigend in PR #138 gefaltet werden.
  Für diesen Record änderten sich weder Workflow, Scanner, Suppression,
  Framework, MRTS, Gitlink noch Delivery-Status.
- Hinweis zur historischen Kennzeichnung / Historical-label note: Spätere
  Legacy-Bullets mit der Überschrift „Aktuelle Framework-PR #39 …“ sind nur
  aufbewahrte PR-#39-Evidence, nicht der aktuelle `FND-FRAMEWORK-0044`-Status.
  Ihre Verweise auf 25 Keys, CPython 3.13.14, `requires_user_decision` und
  `FND-SONAR-0009` sind für PR #42 durch den maßgeblichen Abgleich weiter unten
  abgelöst.
- Aktuelle Framework-PR-#45-Resulting-Master-Sonar-Neubewertung / Current
  Framework PR #45 resulting-master Sonar reassessment: Exakter Head
  `dd7e221d903a7e2e0a59af203ba312dfca55d69c` mergte normal mit Exact-Head-
  Schutz als Framework-master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb`;
  sein Tree entspricht dem geprüften Head. Anwendbare Resulting-Master-GitHub-
  Checks bestanden, aber SonarCloud Check Run `89757305894` scheiterte
  ausschließlich an Security C (Actual `3`, Threshold `1`). Das aktuelle
  Leak-Period-Inventar hat 19 offene/bestätigte Records: neun read-only-MRTS-
  VULNERABILITY-Signale und zehn CODE_SMELL-Records. `FND-SONAR-0002` bleibt
  P1 `blocked`; es erfolgten keine PR-#45-Risikoakzeptanz, Parent-/Gitlink-/
  MRTS-Aktion, Control-Änderung oder Closure. Ein späterer schreibgeschützter
  Boundary-Snapshot bewahrt drei nicht zugeordnete dirty MRTS-Working-Tree-
  Pfade und bestätigt zugleich unveränderte task-eigene Gitlink-/Commit-
  Referenzen. Receipt-SHA-256:
  `21a8bb0c5cf83ac6ca0156d3285e5829ca1d871754dc9019516844ef9c94695d`,
  `07da9852d035d0be72a3260258d0d05b350d7a1b1e49c5acd7e6f229f39b13d9`.
- Framework PR #44 unter eng begrenzter Master-Sonar-Akzeptanz gemergt / Framework PR #44 merged under bounded master-Sonar acceptance: Exakter Head `3b67efb8534fb56a93f085897417ada449ff1a39` mergte normal mit Exact-Head-Schutz als Framework-master `4c9753291d26d92f2d7e51ae425dedb79666fd5e`; sein Tree entspricht dem geprüften Head. Resulting-Master-CodeQL-, Advisory-, common-structure- und Lint-Controls bestanden. SonarCloud scheitert nur am akzeptierten Security-C-Restrisiko (Actual `3`, Threshold `1`) mit neun `needs_review`-read-only-MRTS-Signalen. Das globale P1-`FND-SONAR-0002` bleibt `blocked`; kein Control-, Parent- oder MRTS-Scope wurde waived oder geändert. Post-Merge-Receipt-SHA-256: `71228129d8b0a24706a35219fb568679ef7be0e7a47a615cb7f5abcc167c1f3f`.
- Maßgeblicher aktueller Framework-PR-#42-Sonar-/Python-Abgleich / Authoritative current Framework PR #42 Sonar/Python reconciliation: `FND-FRAMEWORK-0044` ist lokal `fixed` für seine 27 besessenen nicht sicherheitsrelevanten Code-Smell-Keys, und die historische 15-Key-PR-#42-Teilmenge von `FND-FRAMEWORK-0050` ist lokal `fixed`. Der kombinierte task-eigene Framework-Patch konfiguriert exaktes CPython `3.14.6`; ausgewählte lokale CPython-`3.14.4`-Controls bestanden 61 Migrationstests, 49 direkte Remediation-Tests, Contracts, CP314-Hash-Lock-Controls, Dokumentationsprüfungen, `git diff --check` und vollständiges natives `make lint`. Der vollständige 22-Pfad-Security-Scan hat null reportable Findings (`report.md` SHA-256 `1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36`). Dies belegt weder Hosted Sonar noch einen Ziel-3.14.6-Hosted-Job oder Delivery; normale Exact-Head-Einreichung und frischer No-Suppression-Sonar-Nachweis bleiben erforderlich. Der ältere PR-#39-/CPython-3.13.14-Text weiter unten ist nur historisch, und `FND-SONAR-0002` bleibt der unabhängige Master-Blocker.
- Aktuelle Framework-master-S3415-Verifikation / Current Framework-master S3415 verification: Der exakte Head `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` von PR [#43](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/43) mergte normal als Framework-master `f98a8739cb13b583f23d646784b144e596b61441`. Die 507 Framework-eigenen `python:S3415`-MAJOR-Test-Keys des Pre-Remediation-Masters `935cf14c676a24672be5c336e92cd13457cc35c8` / der Analyse `dda3ea04-2721-4ee6-a9c1-74bd2925f139` fehlen verifiziert in der exakten Resulting-Master-Analyse `77e255d6-17a2-4e8a-bb29-6438e91e6fa8`. Das resultierende Gate ist ausschließlich wegen des unabhängigen `FND-SONAR-0002` Security C aus neun read-only-MRTS-Signalen ERROR; die nur-PR-#42-Risikoakzeptanz deckt #43 nicht ab. Post-Merge-Receipt-SHA-256: `d8a63662d10def3118b5795c90474a0c63ab9a96a82d5e93debb8436c79bd79c`.
- Aktuelle Framework-PR-#42-Resulting-Master-Disposition / Current Framework PR #42 resulting-master disposition: Exakter PR-#42-Head `dc6cf411e78b3f37f1e4be52edef59894560b1ae` wurde normal mit Exact-Head-Schutz als Framework-master `935cf14c676a24672be5c336e92cd13457cc35c8` gemergt; sein Tree entspricht dem geprüften PR-Head und acht exakte Master-GitHub-Actions-Workflows endeten erfolgreich. `FND-FRAMEWORK-0046`, `0049`, `0051` und `0052` sind nach bestandenen ursprünglichen OSV-, Pyright- beziehungsweise Ruff-Controls sowie Resulting-Master-Evidence `verified`, nicht closed. `FND-FRAMEWORK-0053` ist `in_progress`: Der gemergte Change Record behauptet weiter, PR-#42-/Resulting-Master-Evidence sei unbeobachtet, daher ist ein separat autorisierter bilingualer Dokumentations-Follow-up nötig. Die abgeschlossene Delivery bewahrt zwei begrenzte historische Risiken: Exakte Sonar-Analyse `dda3ea04-2721-4ee6-a9c1-74bd2925f139` ist ERROR ausschließlich auf Security C, und die Resulting-Master-Cloudflare-Suite `81246317347` ist ohne Check-Runs queued. `FND-SONAR-0002` bleibt ein aktives globales P1-blocked-Finding; `FND-GITHUB-0007` liegt separat als aktuelles Nutzer-`accepted_risk` im lokalen Archiv, nicht als bestanden oder technisch geschlossen. Aufbewahrte Post-Merge-Receipt-SHA-256: `0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`. Parent-Gitlink und MRTS bleiben unverändert.
- Ablösende Model-1-PR-#39-Coverage-Aktualisierung / Superseding Model-1 PR #39 coverage update: Der Nutzer hat Model 1 ausgewählt. Die lokale Model-1-Workflow-Implementierung ist fixed, aber FND-SONAR-0009 hat den Lifecycle `blocked` / `blocked_external_dependency`: Die finale lokale Suite bestand 23 Tests, und der generische Workflow-, CI-security-contract-, CI-security-evidence-contract- sowie ausgewählte Syntax-Check bestanden. Der Projekt-Owner muss weiterhin einen dedizierten least-privilege SONAR_TOKEN konfigurieren und das bestehende SonarQube-Cloud-Projekt von automatischer auf CI-basierte Analyse umstellen; keine externe Aktion, kein Hosted-Scan, keine importierte Coverage und kein Quality Gate wurden beobachtet. Die exakte Restrisiko-Annahme lautet: same-repository PR initiators are authorized for the project analysis token. FND-HOST-0006 ist der getrennte P2-blocked_environment-lokale-CPython-3.13.14-_sqlite3/Coverage.py-Blocker; er ist nicht der Hosted-Projekt/Token-Blocker.
- Aktuelle Framework-PR-#37-Delivery-Record-Reconciliation / Current Framework PR #37 delivery-record reconciliation: `FND-FRAMEWORK-0045` ist auf Framework-master `f73f8842f45318e2df8aff1d31855eeb7c20a22f` `verified`, nicht closed. Exakter Source `1e9fa0d22639517193d450b05eb7b07193e41257` mergte nach frischen PR-Head-Controls normal; die ursprüngliche veraltete No-Merge-Formulierung tritt nicht mehr auf und direkte `master`-Pushes bleiben verboten. Der unabhängige Default-Branch-SonarCloud-Blocker ist `FND-SONAR-0002`; er eröffnet dieses Dokumentationsfinding nicht erneut. Es erfolgte keine Parent-Gitlink- oder MRTS-Aktion.
- Historische Framework-PR-#39–#41-Konsolidierung (ersetzt durch exakten
  PR-#42-Head `2930e04e1558b5b10bdeb87a76abb077a2085566`) / Historical
  Framework PR #39–#41 consolidation: `FND-FRAMEWORK-0047` und
  `FND-FRAMEWORK-0048` bleiben P1-`fixed`-Local-Remediations mit ihrer
  aufbewahrten Exact-Head-Evidence. `FND-FRAMEWORK-0046` war damals
  `in_progress`: Der exakte PR-#42-Head
  `e0564d219980d62bc37162ac6c11641f289f1b71` scheiterte in OSV-Run
  `29956021487` / Job `89045175516`, weil CPython `3.14.6` aus begrenzten
  Head-Daten den CP313-only-Lock der Trusted Base
  `f73f8842f45318e2df8aff1d31855eeb7c20a22f` installierte. Die
  exact-SHA-bound Trusted-Base-CPython-`3.13.14`-Bridge gilt nur für diese
  exakte Base mit fehlendem Selector; jede andere Base oder jeder andere
  Selector-Zustand scheitert fail closed. Zu diesem historischen Zeitpunkt
  war keine aktuelle lokale oder Hosted-Verifikation aufgezeichnet.
- Historischer Framework-PR-#42-Quality-Follow-up (ersetzt durch exakten Head
  `2930e04e1558b5b10bdeb87a76abb077a2085566`) / Historical Framework PR #42
  quality follow-up: Der exakte Follow-up-Head
  `f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c` bestand den korrigierten
  OSV-Control, SonarQube Cloud und die Ruff-Stufen, aber sein Python-Quality-
  Job `29961019802` / `89061788219` erreichte gehostetes CPython-`3.14.6`-
  Pyright und meldete zwei getrennte Fixture-Annotationen. Diese Diagnosen
  waren P1-`in_progress` `FND-FRAMEWORK-0052`; ihre Ein-Datei-Test-only-
  Korrektur war lokal validiert und wartete auf ein neues Exact-Head-Hosted-
  Ergebnis. `FND-FRAMEWORK-0049` bleibt unabhängig `fixed`, nicht verified:
  Sein exakter grüner Head `1fd3b362e0fed9766c6920e3c7bd1939535850f2` bestand
  Run `29943112344` / Job `89001693819`, doch normale Framework-Master-
  Integration und Resulting-Master-Evidence fehlen weiter. Es erfolgte keine
  Parent-Gitlink- oder MRTS-Änderung.
- Aktuelle Framework-PR-#37-Master-Sonar-Neubewertung / Current Framework PR #37 master Sonar reassessment: `FND-SONAR-0002` bleibt P1-`blocked`. Resultierender Master `f73f8842f45318e2df8aff1d31855eeb7c20a22f` hat nur einen fehlgeschlagenen SonarCloud-Check (New Security Rating C, Actual `3`, Threshold `1`); anwendbare Actions und CodeQL bestanden. Die neun aktuellen Gate-treibenden Signale sind unveränderte, vor PR #37 vorhandene, read-only-MRTS-Inputs und nach statischer Source-/Control-/Sink-Triage `needs_review`. Keine aktuelle Risikoakzeptanz, MRTS-Aktion, Scanner-/Gate-Änderung oder PR-#37-Kausalität ist festgehalten.
- Aktuelle Framework-PR-#39-Sonar-Remediation und Coverage-Ingestion-Blocker / Current Framework PR #39 Sonar remediation and coverage-ingestion blockers: FND-FRAMEWORK-0044 bleibt für 25 lokal behobene nicht sicherheitsrelevante CODE_SMELL-Keys `fixed`. Seine Framework-spezifische CPython-`3.13.14`-Qualifikation bestand hash-locked `PyYAML-6.0.3`, `pip check`, 30 direkte betroffene Tests, 89 `make test-ci-security-contract` Tests, Workflow- und Dokumentations-Checks, `python -m compileall -q ci tests`, den Response-Body-Guard und `make lint`; Receipt-SHA-256: `2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30`. Diese lokale Evidence belegt keine Hosted-SonarQube-Cloud- oder GitHub-Bestätigung, und es änderten sich keine Coverage-, Scanner-, Quality-Gate-, Regel-, Exclusion-, Suppression- oder Hosted-Service-Konfiguration. FND-FRAMEWORK-0044 hat Feasibility `requires_user_decision`, weil FND-SONAR-0009 die getrennte P1-`blocked`-Coverage-Ingestion-Bedingung bleibt: Eine aktuelle Nutzerentscheidung muss Scope und Owner der externen CI- und SonarQube-Cloud-Coverage-Authentifizierung auswählen und autorisieren, bevor Delivery, Exact-Head-Report-Ingestion und aussagekräftige Coverage verifiziert werden können. Die frische Exact-Head-SonarQube-Cloud-Bestätigung aller 25 ursprünglichen Keys steht weiter aus; es wurde kein Risiko akzeptiert.
- Aktuelle S8707-Lighttpd-Entity-Fixture-Output-Containment-Reparatur / Current S8707 Lighttpd entity-fixture output containment repair: Der aktuelle Parent-`pythonsecurity:S8707`-VULNERABILITY-Key `AZ9cRynaHhV2CayPTPzR` bei `connectors/lighttpd/harness/lighttpd_http1_entity_fixture_upstream.py:47`, Master-Blob `e64d11434ccff675a0470ed1d3d1a053c3c7978d`, nahm CLI-`--ready-file`- und `--result-file`-Ausgabepfade ohne deklarierte Safe Root an und schrieb JSON über einen vorhersehbaren `.{path.name}.tmp`-Sibling, bevor der finale Pfad ersetzt wurde. Die lokale Parent-Reparatur verlangt `--safe-root`, weist direkte Outside-Root-, Symlink-Directory- und finale Symlink-Control-File-Escapes vor dem Lauschen ab, aktualisiert den Runner auf `--safe-root "$FIXTURE_DIR"` und publiziert JSON über `mkstemp` plus `os.replace`. Die Pre-Fix-Regression bewies, dass ein vorab platzierter `.result.json.tmp`-Symlink `result.json` als Symlink zurücklassen konnte; nach der Reparatur bestand die Helper-Suite sieben Tests, Python-Compilation bestand, und die vollständige Lighttpd-Patched-Host-Contract-Suite bestand 16 Tests. Aufbewahrter Receipt: `sonar-s8707-lighttpd-fixture-output-fix-20260721T043051Z.json`, SHA-256 `94f14a450f447fcea4095914309b4e1a8290ef41376520863a8981b319a3adfb`. Das lokale Ergebnis lautet `fixed`, aber das externe Issue bleibt auf Master `OPEN`, bis ein getrennt autorisierter ausgelieferter Head eine Sonar-Analyse erhält; es ist kein False-Positive-Kandidat. Zusammen mit den zehn not_actionable-Records und der lokalen Response-Header-S8707-Reparatur deckt der aktuelle abgegrenzte Scope zwölf reguläre Keys ab und lässt 194 exakte Parent-Vulnerability-Inventory-Zeilen; `FND-SONAR-0001` bleibt durch drei getrennt unreviewte Hotspots blockiert. Es erfolgten keine Delivery, externe Sonar-Aktion, Suppression, Regel-/Gate-Änderung, Framework-/MRTS-/Gitlink-Aktion oder Risikoakzeptanz.
- Aktuelle S8707-Response-Header-Fixture-Containment-Reparatur / Current S8707 response-header fixture containment repair: Der aktuelle Parent-`pythonsecurity:S8707`-VULNERABILITY-Key `AZ9cRyfJHhV2CayPTPxt` bei `ci/runtime/common/response-header-test-backend.py:101`, Master-Blob `fed58d05fbf3897d8e0d19299048c2310773c092`, erreichte `Path.read_text` über `--fixture-file` ohne den bereits auf `--body-file` angewendeten `--safe-root`-Check. Die lokale Parent-Reparatur teilt den kanonischen Regular-File- und Safe-Root-Resolver mit Fixture-Pfaden. Die Real-CLI-Regression bewies direkte Outside-Root- und In-Root-Symlink-Bypässe vor der Reparatur; nach der Reparatur bestand die Backend-Suite sechs Tests und weist beide vor dem Lauschen ab, während die gültige In-Root-Fixture-Kontrolle erhalten bleibt. Python-Compilation, angrenzende Apache-/Full-Lifecycle-Contract-Suites und eine unabhängige Security-Diff-Review bestanden. Aufbewahrter Receipt: `sonar-s8707-response-header-fixture-fix-20260721T033723Z.json`, SHA-256 `80922e5534416cbfc66145e2707b6bcbff0a1633ab3e24db09f8a54b7205fbf8`. Das lokale Ergebnis lautet `fixed`, aber das externe Issue bleibt auf Master `OPEN`, bis ein getrennt autorisierter ausgelieferter Head eine Sonar-Analyse erhält; es ist kein False-Positive-Kandidat. Bei diesem Meilenstein deckte der abgegrenzte Scope zusammen mit den zehn not_actionable-Records elf reguläre Keys ab und ließ 195 exakte Parent-Vulnerability-Inventory-Zeilen; die Lighttpd-S8707-Reparatur oben erhöht den aktuellen lokalen Scope auf zwölf und lässt 194. `FND-SONAR-0001` bleibt durch drei getrennt unreviewte Hotspots blockiert. Es erfolgten keine Delivery, externe Sonar-Aktion, Suppression, Regel-/Gate-Änderung, Framework-/MRTS-/Gitlink-Aktion oder Risikoakzeptanz.
- Hinweis zum historischen Zähler / Historical-count note: Der unmittelbar folgende S5443-Eintrag dokumentiert den früheren Zehn-Key-/196-Zeilen-Stand. Die zwei S8707-Reparaturen oben sind der aktuelle Stand und reduzieren den abgegrenzten Backlog auf 194.
- Aktuelle Clang-Temporary-Directory-S5443-Vulnerability-Triage / Current Clang temporary-directory S5443 Vulnerability triage: Der aktuelle Parent-`python:S5443`-VULNERABILITY-Key `AZ9gJKOrg304P0Qlak6y` bei `tests/test_clang_analysis_baseline.py:41`, Exact-Master-Blob `0b8a34b44453faed5de129a13ec186de2e12c5eb`, ist technisch `not_actionable`. Das test-only-`tempfile.TemporaryDirectory` hat ein konstantes Prefix und einen optionalen gleichberechtigten `TMPDIR`-Parent; alle sieben Caller nutzen es als Context Manager, bevor sie Child-Pfade ableiten. Python dokumentiert race-sichere `mkdtemp`-Erzeugung und ein nur für den erzeugenden Benutzer zugängliches Verzeichnis: <https://docs.python.org/3/library/tempfile.html>. Die fokussierte Acht-Test-Contract-Suite bestand. Es erfolgten kein Source-Patch, keine externe False-Positive-Disposition, kein Hotspot-Review, keine Suppression, Regel- oder Quality-Gate-Änderung, Framework-/MRTS- oder Gitlink-Aktion und keine Risikoakzeptanz. Der aufbewahrte Receipt ist `sonar-s5443-clang-tempdir-triage-20260721T031222Z.json`, SHA-256 `87d162bf24ab136cbc00e841b3cb9f2a8637aea81d34f8301ebaae5a1f176b98`. Bei diesem Meilenstein umfasste der kumulierte lokale Scope zehn reguläre Keys und 196 exakte Parent-Vulnerability-Inventory-Zeilen; die zwei S8707-Reparaturen oben reduzieren den aktuellen lokalen Backlog auf 194. `FND-SONAR-0001` bleibt durch die drei getrennten unreviewten Hotspots blocked, und jede externe Disposition benötigt weiterhin eine aktuelle ausdrückliche Nutzerentscheidung.
- Frühere Refresh-Report-S2083-Vulnerability-Triage / Earlier refresh-report S2083 Vulnerability triage: Zwei Parent-`pythonsecurity:S2083`-VULNERABILITY-Keys, `AZ9cRyiqHhV2CayPTPyS` und `AZ9cRyiqHhV2CayPTPyR`, sind auf exaktem Master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` technisch `not_actionable`. Zurückgehaltener Report- oder Command-Text erreicht in `ci/evidence/reports/refresh-connector-reports.py:281` und `:1063` nur `Path.write_text`-Inhalt; statische `GENERATED_REPORTS`-Katalog-Outputs und explizite Operator-Roots wählen unabhängig den Ziel-Path. Es erfolgten kein Source-Patch, keine externe False-Positive-Disposition, kein Hotspot-Review, keine Suppression, Regel- oder Quality-Gate-Änderung, Framework-/MRTS- oder Gitlink-Aktion und keine Risikoakzeptanz. Der aufbewahrte Receipt ist `sonar-s2083-refresh-connector-reports-triage-20260721T025657Z.json`, SHA-256 `3f73655e0a861a0b39d8987eafea08e33ef3b66e3625c3925fb0777cc315ae4f`. Beim Abschluss dieses Clusters umfasste der kumulierte lokale Scope neun reguläre Keys und 197 exakte Parent-Vulnerability-Inventory-Zeilen; die aktuelle S5443-Triage oben reduziert ihn auf 196. `FND-SONAR-0001` bleibt durch die drei getrennten unreviewten Hotspots blocked, und jede externe Disposition benötigt weiterhin eine aktuelle ausdrückliche Nutzerentscheidung.
- Frühere Audit-Renderer-S2083-Vulnerability-Triage / Earlier audit-renderer S2083 Vulnerability triage: Drei Parent-`pythonsecurity:S2083`-VULNERABILITY-Keys, `AZ9cRygDHhV2CayPTPxy`, `AZ9cRygDHhV2CayPTPxx` und `AZ9cRygDHhV2CayPTPxz`, waren auf exaktem Master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` technisch `not_actionable`. Der lokale JSON-Payload erreicht in `ci/evidence/reports/audit-full-lifecycle-runtime-roots.py:339-341` nur `Path.write_text`-Inhalt, niemals dessen unabhängige Output-Paths; es erfolgten kein Source-Patch, keine externe False-Positive-Disposition, kein Hotspot-Review, keine Suppression, Regel- oder Quality-Gate-Änderung, Framework-/MRTS- oder Gitlink-Aktion und keine Risikoakzeptanz. Der aufbewahrte Receipt ist `sonar-s2083-runtime-root-audit-triage-20260721T023733Z.json`, SHA-256 `9a361f2ed67a4a0fa1dae11f6107ca2cd8fe7c88dd2557c84c2473dee3318d9c`. Beim Abschluss dieses Clusters umfasste der Scope sieben reguläre Keys und 199 exakte Parent-Vulnerability-Inventory-Zeilen; die spätere Refresh-Report-Triage reduzierte ihn auf 197, und die aktuelle S5443-Triage oben reduziert ihn auf 196. Die getrennte S5332-only-Zahl von 202 weiter unten ist historisch vor beiden S2083-Triagen.
- Aktuelle Apache-Intervention-Ownership-Remediation / Current Apache intervention ownership remediation: `FND-PARENT-0043` ist ein getrenntes Parent-`P2`/`medium`-`security_validated`-Finding in `blocked`, nicht fixed, verified oder closed, weil native Validierung unbekannt bleibt. Der finale PR-#72-Head `486aef56424f5bf33bcd7396f6dc2f881f7f3bdd` wurde als aktueller Master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` squash-gemergt und hat einen identischen Tree; 14 beobachtete Master-Actions-Workflows bestanden. Das aufgabeneigene PR-SonarQube-Cloud-Ergebnis bestand mit null neuen Issues/Hotspots und `0,0 %` Duplikation. Master-Duplikation ist `0,4 %` und besteht; sein getrenntes Quality-Gate-Fehlerbild bleibt in `FND-SONAR-0001`. Native Apache/APR/libModSecurity- und ASan/LSan-Validierung bleiben blockiert.
- Aktueller PR-#55-Current-master-Gate / Current PR #55 current-master gate: Der geprüfte Framework-Provenance-Candidate wurde ohne Pfadüberlappung auf den privaten Framework-`master` `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b` übertragen; Byte-Vergleiche, `git diff --check` und Shell-Syntax der geänderten Dateien bestanden. Die ausgewählte Framework-`.venv/bin/python` fehlt, daher sind die Provenance-Suite, Dokumentationsprüfung und der vollständige Lint auf dem exakten Candidate `blocked_environment` und wurden nicht durch System-/Parent-Python ersetzt. Es erfolgten kein Framework-Branch, Commit, Push, PR, Parent-Runtime-Run, Gitlink-Update, Merge oder MRTS-Aktion. Retained Evidence: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`, SHA-256 `067db2ef9c429fa405737d193aa7a7fa5751c158b4d0ffdddbc6667918ce3ed6`.
- Aktuelles Framework-Python-Wartungs-Hardening / Current Framework Python-maintenance hardening: `FND-FRAMEWORK-0033`, `FND-FRAMEWORK-0037`, `FND-FRAMEWORK-0038` und `FND-FRAMEWORK-0039` sind nach expression-aware Secret-Kontext-Contract, Runner-Kontext-/ShellCheck-, Fallback-YAML- und festem Kandidatenpfad-Fix lokal `fixed`. Die 36 fokussierten Tests, 85 CI-Security-Tests, nativen Workflow-/Dokumentations-/vollständigen-Lint-Gates und der versiegelte vollständige 11-Dateien-Security-Diff-Scan bestanden mit null reportable Findings. Exact-Current-Head-GitHub-Actions-, Review- und SonarQube-Evidenz steht auf dem autorisierten Draft-PR noch aus; es erfolgten kein Framework-Merge, kein Parent-Gitlink-Update und keine MRTS-Aktion. Source Run: `20260720T180337Z-framework-python-313-updater-f3349a7e`.
- Aktuelle PR-#55-Runtime-Evidence-Remediation / Current PR #55 runtime-evidence remediation: `FND-PARENT-0042` ist der unabhängige P1-Parent-Cache-Release-Asset-Blocker in `blocked` / `blocked_environment`, nicht fixed, verified oder closed. Seine lokale Parent-Source-Korrektur bindet das exakte GitHub-Release-Tupel, besitzt keinen Tag-Archiv-/Latest-Fallback und bestand 31 fokussierte Cache-/Provenance-Tests sowie die fokussierten Shell-, Dokumentations- und Review-Controls. Das korrigierte Manifest mit SHA-256 `3adf2284d3318cc35e690d319a84fe27200fe33047f43db22a328bf3c986253a` dokumentiert die exakte Release-Download-URL und passende Release-Asset-SHA-256; der ursprüngliche `sha256_mismatch` reproduziert nicht mehr. Die legitime Vorbereitung stoppt anschließend unabhängig bei `missing_nginx_modsecurity_module` (NGINX-Build-Exit `77`), während breite Dokumentations-Make-Checks ausschließlich wegen bestehender Links in den bewusst uninitialisierten Framework-Gitlink `blocked_environment` bleiben. `FND-FRAMEWORK-0036` ist wieder `in_progress`: Dem f98-basierten Fresh-Fetch-Candidate fehlt der zuvor validierte explizite Fresh-Root-Containment-/Scrubbing-Helper. Das getrennte `FND-FRAMEWORK-0054` ist ein `triaged` P2/medium plausibler Host-Git-PATH-Binding-Kandidat; er belegt keinen produktiven hostile-PATH-Akteur. `FND-PARENT-0050` bewahrt seinen historischen Build-Order-Nachweis und verfolgt nun die unbestätigte generische-Git-Acquisition-Übergabe nach Configuration-Admission; sie benötigt eine Framework-owned Safe-Acquisition-Bridge oder überprüfte Entsprechung. In diesem Registry-Update erfolgten kein Staging, Commit, Push, PR, Merge, Parent-Gitlink-, Framework- oder MRTS-Aktion. `FND-CROSS-0001` bleibt bis zur vollständigen legitimen Runtime-Evidence-Kette separat blockiert.
- Aktuelle reguläre S5332-Vulnerability-Triage / Current regular S5332 Vulnerability triage: Vier aktuelle Parent-`python:S5332`-`VULNERABILITY`-Keys (`AZ9cRysWHhV2CayPTP0c`, `AZ9MwivX-bUaKQ_zSGAh`, `AZ9cRyW7HhV2CayPTPur` und `AZ9cRyfJHhV2CayPTPxs`) sind auf exaktem Master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` technisch `not_actionable`: zwei Loopback-only-Connector-Harnesses, ein lokaler Documentation-Link-Klassifizierer und ein Loopback-Response-Header-Testfixture. Es erfolgten kein Source-Patch, keine False-Positive-Disposition, kein Hotspot-Review, keine Suppression, Regel- oder Quality-Gate-Änderung, Framework-/MRTS- oder Gitlink-Aktion und keine Risikoakzeptanz. Der aufbewahrte Per-Key-Receipt ist `sonar-s5332-regular-vulnerability-current-master-triage-20260721T020213Z.json`, SHA-256 `710339515e3f89b89b560209c39788db5b008cc2e03dc742dc357cfbd4ffd6d5`; das Ergebnis betrifft nur vier Keys und lässt 202 exakte Parent-Vulnerability-Inventory-Zeilen untriagiert. `FND-SONAR-0001` bleibt wegen der drei getrennt unreviewten Hotspots `blocked`, und externe Dispositionen benötigen weiterhin eine aktuelle ausdrückliche Nutzerentscheidung.
- Aktuelle Codex-Cloud-Security-Reconciliation / Current Codex Cloud Security reconciliation: `FND-FRAMEWORK-0029` ist `blocked_permissions`, keine Source-Vulnerability-Disposition. Framework-`master` ist exakt `784977615acfc55567e37b863309abc4a38ac877`; GitHub CodeQL ist aktuell und unabhängig clear, aber nicht Codex Cloud. Nach der Nutzerfreigabe leiteten die dokumentierten Codex-Cloud-Findings- und Scans-URLs diesen Transport um `2026-07-20T17:03:40Z` auf die ChatGPT-Anmeldung um. Das aktive Ziel bleibt blockiert, bis eine authentifizierte Workspace-Session oder ein autoritativer Export verfügbar ist; kein Cloud-Finding wurde geschlossen. Source Run: `20260720T162741Z-framework-codex-cloud-security-reconciliation-08539bb5`.
- Aktuelle Parser-Blocker-Erweiterung / Current parser-blocker extension: FND-FRAMEWORK-0027 und FND-FRAMEWORK-0028 sind auf Framework-Master `784977615acfc55567e37b863309abc4a38ac877` `verified`, nicht closed oder risikoakzeptiert. Der aktualisierte #36-Head `1608352912a755f0f8639eddfa2350436446067e` ist ein Vorfahr mit identischem Tree; die Original-Exact-Master-Reproduktion bestand mit aufgelösten freigegebenen Literalen/Aliasen und einem Manual-Review-Leer-Update für v3.0.16. Es erfolgte keine Parent-Gitlink- oder MRTS-Änderung.
- Aktuelle Framework-PR-#35-/#36-Integration / Current Framework PR #35 / #36 integration: #36 wurde nach bestandenen frischen Exact-Head-Actions, CodeQL, PR-Sonar-Quality-Gate, Dokumentations-, Review-, Konflikt- und Security-Controls normal als Framework-Master `784977615acfc55567e37b863309abc4a38ac877` gemergt. Resultierende Master-CodeQL-Actions/Python/C++, Lint, test-common und OpenSSF bestanden. Master-SonarQube Cloud bleibt unabhängig Security E (`new_security_rating=5`, Threshold `1`), während Reliability, Maintainability, Duplikation und Hotspot-Review bestehen; sein Vorgänger hatte dieselbe Bedingung. Die eng begrenzte Nutzerakzeptanz wurde nur für diese geschützte Delivery verwendet. `FND-SONAR-0002` bleibt blocked, und keine Parent-Gitlink- oder MRTS-Änderung ist autorisiert. Source Run: `20260720T113905Z-framework-pr35-36-integration-de98515c`.
- Aktuelle PR-#59-Integration / Current PR #59 integration: Der geschützte Squash-Merge des exakten Source-Heads `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` erzeugte Parent-master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. `FND-PARENT-0030`, `FND-PARENT-0031` und `FND-PARENT-0037` sind nun `verified`, nicht `closed`, und keine eigenen Release-Blocker mehr: Frische nicht übersprungene CI-, CodeQL-, Sonar-Quality-Gate- sowie Null-Review/Thread-Controls bestanden vor dem Merge; die exakte Resulting-Master-Suite bestand 57/57 Evidence-Integrity-, 11/11 Bilingual-, Shell-Syntax- und Diff-Controls. Es erfolgte keine Parent-Gitlink-, Framework- oder MRTS-Aktion. Der unabhängig bereits bestehende `FND-SONAR-0001`-Master-Fehler bleibt nicht akzeptiert und lässt die aggregierte Delivery partial; er eröffnet diese verifizierten Findings nicht erneut. Source Run: `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`.
- Aktuelle PR-#57-Erweiterung / Current PR #57 extension: Parent-PR #57 mit exaktem Head `5f8949b1d98a98127b933e9f1d626b30e3291b59` wurde squash als aktueller Parent-master `fde2e02a1cf2226f8e9106e663e05e9b2941357e` gemergt. In einem sauberen abgetrennten Exact-Master-Worktree bestanden 20 fokussierte Lifecycle-/Wiring-/Six-Connector-Tests: fremde oder fehlende Run-, Connector-, Profil-, Integrationsmodus- und Transaktionsidentitäten scheitern auf First-Byte- und No-Full-Buffer-Pfaden fail closed, während die legitime ausgewählte Apache-Kontrolle besteht. `FND-PARENT-0027` ist `verified`, nicht closed, und kein Release-Blocker mehr; FND-CROSS-0006 ist separat auf Framework-master verified. Alle 14 Master-Actions-Workflows bestanden. Der unabhängige bereits bestehende Parent-Sonar-Fehler `FND-SONAR-0001` lässt die aggregierte Delivery partial, eröffnet dieses verifizierte Finding aber nicht erneut. Der Framework-Gitlink bleibt `efdbcbd98afeed0f39f8912ce1140aaa5742f507`; es erfolgte keine Framework- oder MRTS-Git-Aktion. Source Run: `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`.
- Aktuelle PR-#61-Integration / Current PR #61 integration: Geschützter Parent-PR #61 mit Head `c9b505a7a0f697318a57f42fe30493038ef03527` wurde squash als aktueller Master `6bba8206de1bb598b40f76677943e86770b6992c` gemergt; der resultierende Tree entspricht dem geprüften Head, und kein Framework-/MRTS-Gitlink änderte sich. Alle 14 resultierenden Master-GitHub-Actions-Workflows bestehen, während exakter SonarCloud-Check `88361885739` scheitert. Das exakte PR-Quality-Gate von PR #61 bestand mit null neuen Issues/Hotspots und `0,0 %` Duplikation; Master hat nun 229 offene Bug/Vulnerability-Records (220 Vulnerabilities und 9 Bugs), weniger als die zurückgehaltenen 230. `FND-SONAR-0001` bleibt blockiert P1, weil die drei unreviewten Hotspots und E/E-Ratings verbleiben; diese Integration ist daher `master_integration_partial`, ohne Hotspot-Review, Sonar-Control-Änderung, Framework-/MRTS-Aktion oder Risikoakzeptanz. Source Run: `20260720T131144Z-pr61-master-integration-6bba820`.
- Aktuelle PR-#59-Sonar-Maintainability-Erweiterung / Current PR #59 Sonar maintainability extension: `FND-SONAR-0006` ist auf Parent-master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` `verified`, nicht `closed`. Seine acht aufgabeneigenen historischen `CODE_SMELL`-Keys für Source `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` sind sowohl in frischer PR-Evidence als auch in der Resulting-Master-Key-Abfrage null, ohne NOSONAR, Suppression, Exclusion, Scanner-/Gate-Änderung, False-Positive-Disposition oder Risikoakzeptanz. Der zurückgehaltene Post-Merge-Receipt erfasst die fokussierten Controls; `FND-SONAR-0001` bleibt der getrennte nicht akzeptierte Master-Quality-Gate-Fehler. Source Run: `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`.
- Ersetzter Erweiterungs-Run / Superseded extension run: `20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b`
- Aktueller Parent-Sicherheitsabgleich / Current Parent security reconciliation: Der geschützte PR #66 wurde als `cbd8385...` gemergt; Follow-up-PR #70 mit exaktem Head `8d7f8b7283319528cf2c14479fc02399dd215825` bestand 33 terminale PR-Checks, Sonar-Quality-Gate `OK` und null Reviews/Threads und wurde danach normal squash als finaler Parent-Master `f2376bb3e39ffbe9d36faca8bcd7397477eadd10` gemergt. Tree-Gleichheit und alle resultierenden GitHub-Actions-Workflows bestanden. Seine SHA-gebundene Sonar-Analyse `e04ce5bc-a9f7-44ce-bb13-8fe25c872d55` schloss `AZ7b3dgOcO69wzd-_jHv` / `c:S3519`; es bleiben null offene Bugs, 220 Vulnerabilities und drei `TO_REVIEW`-Hotspots. Exakte Master-Source/Control/Sink-Evidence klassifiziert diese Hotspots als `already_safe` mit `no_change`; eine externe reviewed/safe-Disposition bleibt bis zu einer aktuellen ausdrücklichen Nutzerentscheidung blockiert. `FND-SONAR-0001` bleibt blockiert P1; ausstehende kanonische Importe `FND-SONAR-0007`/`0008` sind auf Parent-Master fixed, können aber keine Verzeichnisse erhalten. Es erfolgte keine Framework-/MRTS- oder Gitlink-Änderung. Source Run: `20260720T164715Z-parent-security-reconciliation-5a22cbf5`.
- Aktuelle Task-Erweiterung / Current task extension: Framework-PR #33 wurde vom exakten Head `e94029f5b893ef6a8efa118d21698426a43c82dd` normal als Master `9a729226d2e040d07d7e7a4acebf201faf06ab37` gemergt. `FND-FRAMEWORK-0021` und `FND-FRAMEWORK-0022` sind nach erfolgreichen ursprünglichen fail-closed-Controls, allen anwendbaren Master-Actions und CodeQL `verified`. Master-SonarCloud scheitert unabhängig weiter mit Security E und Reliability D; die historische `FND-SONAR-0002`-Akzeptanz nennt nur PRs #24, #26, #27 und #29 und deckt PR #33 daher nicht automatisch ab. Source Runs: `20260719T211529Z-framework-python-313-master-migration-939e61b5`, `framework-pr-33-master-9a729226-20260719T221845Z` und `framework-pr-33-master-sonar-20260719T221823Z`.
- Aktuelle PR-#34-Erweiterung / Current PR #34 extension: Framework-PR #34 wurde vom exakten Head `4fc22651ab2da652cbcaa7026258506d79b9af9c` normal als Master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` gemergt. `FND-CROSS-0006` ist `verified`, nachdem seine ursprünglichen Foreign/Missing-Identity-Controls erneut auf master bestanden. PR-Head-SonarQube Cloud bestand; Master-SonarQube Cloud scheiterte unabhängig mit Security E und Reliability D. Die historische `FND-SONAR-0002`-Akzeptanz nennt nur PRs #24, #26, #27 und #29, daher ist das Finding für die aktuelle Master-Integrationsverifikation `blocked`. Source Run: `20260720T042405Z-framework-pr-34-master-integration-31a1528d`.
- Aktuelle PR-#30-Erweiterung / Current PR #30 extension: Der normale Merge-Commit `a448d056ef98e745d8551c198b2e56d33fe38194` aktualisierte `fix/sonarcloud-quality-gate` mit aktuellem Framework-master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. `FND-FRAMEWORK-0023` ist auf dem verifizierten PR-Head `fixed`: SonarQube Cloud hat Quality Gate `OK` mit `new_duplicated_lines=0` und `new_duplicated_lines_density=0.0`; lokale Legitimate Controls und alle terminalen nicht übersprungenen Hosted Checks bestanden ohne Änderungen analytischer Controls. Der historische `FND-SONAR-0002`-Master-Backlog bleibt getrennt und wird nicht waived.
- Aktuelle PR-#30-CI-Erweiterung / Current PR #30 CI extension: `FND-FRAMEWORK-0024` ist auf demselben exakten Head `fixed`. Die unveränderte CI-Security-Suite bestand alle 69 Tests, Dokumentationsprüfungen bestanden und alle terminalen nicht übersprungenen Hosted Checks waren erfolgreich. Der ursprüngliche Überschriftenvertragsfehler wurde ohne Änderung von Checker, Template, Traceability-Control oder Exception repariert.
- Aktuelle PR-#30-CodeQL-Erweiterung / Current PR #30 CodeQL extension: `FND-FRAMEWORK-0026` ist `verified`. Das historische C/C++-CodeQL-Initialisierungs-HTTP-503 war ein von GitHub gehosteter Ausfall vor der Analyse, kein Framework-Source-Defekt. Auf exaktem Head `a448d056ef98e745d8551c198b2e56d33fe38194` bestanden CodeQL-Actions-Job `88287878237`, Python-Job `88287878246` und C/C++-Job `88287878247`. Kein CodeQL-, Workflow-, Quality-Gate- oder Source-Workaround wurde genutzt. Der PR bleibt offen; kein Framework-master-Merge ist von dieser Aufgabe autorisiert. Source Run: `20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef`.
- Aktuelle PR-#30-Security-Scan-Tooling-Erweiterung / Current PR #30 security-scan tooling extension: `FND-FRAMEWORK-0025` ist `validated`, nachdem der Codex-Security-Local-Patch-Rank-Input-Helper bei Exit-Code 0 für vierzehn gestagte PR-#30-Dateien null Zeilen zurückgab, weil seine statische EXCLUDED_DIRS ci und tests ausschließt. Die exakte Staged-Git-Inventur führte alle vierzehn Dateien wieder in die Worklist über, sodass der aktuelle Scan keinen ungeprüften PR-#30-Code hat; die External-Tool-Regression bleibt getrennt bearbeitbar und ist kein Release-Blocker für diesen PR.
- Aktuelle externe Erweiterungsbeobachtung / Current external extension observation: PR-#27-Merge-Commit `6de40c1714410241e917e9083ee890a82fb2fdbb` bewahrt seine historische Advanced-CodeQL-Upload-Ablehnung. Der spätere externe Master `4dee26fcff988fd408bc7df577de772373c4b765` änderte zwölf geprüfte Python-`3.12.13`-Workflow-Werte in acht Workflows ohne passendes Lock-Update auf `3.13`; vier hash-gesperrte CI-Controls scheitern nun fail closed. Das historische `FND-GITHUB-0006` liegt als aktuelles Nutzer-`accepted_risk` im lokalen Archiv, nicht als verifizierte Konfigurationsauflösung; `FND-FRAMEWORK-0021` besitzt die spätere CI-Regression.
- Source runs / Source-Runs: `20260716T193351Z-repository-full-assessment-0cb855ad`, `20260717T054830Z-native-runtime-evidence-6c0853fe`, `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`, `20260717T114213Z-feasibility-runtime-remediation-838d9adc`, `20260717T181659Z-codeql-action-4-37-1-batch-36346991`, `20260718T053406Z-pr-51-master-integration-546d9dc2`, `20260718T074759Z-codeql-xss-alerts-14-15-87ada941`, `20260718T080138Z-harden-workflow-permissions-e804be63`, `20260718T080726Z-fnd-parent-0018-4dd4e268`, `20260718T081034Z-github-scorecard-governance`, `20260718T082206Z-github-scorecard-governance-45b01572`, `20260718T075200Z-parent-evidence-integrity-ade378cf`, `20260718T081746Z-framework-common-structure-d6ee7cec`, `20260718T092308Z-fnd-framework-0005-pcre2-digest-e064e1d8`, `20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058`, `20260718T110742Z-fnd-parent-0028-mutable-action-images`, `20260718T083435Z-expand-framework-ci-security-32892be1`, `20260718T084030Z-expand-framework-ci-security-be8fb24d`, `20260718T075146Z-harden-temp-paths-97486abe`, `20260718T192214Z-framework-pr-resolution-20260718-b30403da`, `20260719T081017Z-framework-pr-resolution-20260719-840082e0`, `20260719T211529Z-framework-python-313-master-migration-939e61b5`, `framework-pr-33-master-9a729226-20260719T221845Z`, `framework-pr-33-master-sonar-20260719T221823Z`, `20260720T113905Z-framework-pr35-36-integration-de98515c`, `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`

- Aktuelle PR-#59-S2083-Erweiterung / Current PR #59 S2083 extension: FND-PARENT-0040 ist nach der Current-Path- und Retained-Evidence-Revalidierung vom 2026-07-26 closed. Seine In-Memory-only-Remediation f00eb11a25172959d50aa3e213fd1d7ace209599 ist ein Vorfahr des exakten Source-Heads b9b22cc36958ba506278f3aa3fbc1d383ea6a151, dessen Tree dem Master entspricht; PR-weite null Issues deckten das ursprüngliche pythonsecurity:S2083 ab, die exakte Resulting-Master-Suite bestand, beide aufbewahrten Hashes stimmen, und die einzige betroffene Testdatei blieb bis zum aktuellen Parent-HEAD unverändert. FND-SONAR-0001 bleibt der getrennte nicht akzeptierte Master-Blocker. Source Run: 20260720T141403Z-pr55-pr59-master-integration-8a0b8640.

- Aktuelles Parent-PR-#66-Sonar-Follow-up: Exakter Draft-Head
  91fea6d05850cc5aeef8ce7fb66a4123ac14e190 bestand 30 terminale Checks,
  SonarCloud-Check 88453362314, Quality Gate OK und null
  offene/confirmed/reopened Bugs. Zwei Traefik-c:S5489-Keys und ein
  HAProxy-c:S3519-Key sind CLOSED/FIXED. Angeforderte Child-Records
  FND-SONAR-0007 und FND-SONAR-0008 liegen als vollständige EN/DE/JSON-
  Import-Triplets vor, weil der kanonische .codex/findings-Mount read-only ist;
  FND-SONAR-0001 trägt die aggregierte Querverbindung und bleibt durch
  unabhängige Parent-Master-Bedingungen blockiert.

| ID | Priorität | Repository | Kategorie | Status | Release-Blocker | Titel |
| -- | -------- | ---------- | -------- | ------ | --------------- | ----- |
| [FND-CROSS-0001](./FND-CROSS-0001/finding.de.md) | P0 | parent_and_framework | evidence_gap | validated | ja | Evidence-Freshness-Manifest enthält veraltete Einträge und SHA-Abweichungen |
| [FND-CROSS-0002](./FND-CROSS-0002/finding.de.md) | P0 | parent_and_framework | evidence_gap | validated | ja | Historische GitHub-JSON-Receipts sind kein parsebares kanonisches JSON |
| [FND-CROSS-0003](./FND-CROSS-0003/finding.de.md) | P1 | parent_and_framework | test_gap | blocked | ja | Aktuelle Connector-Restart-Coverage ist nicht zurückgehalten |
| [FND-CROSS-0004](./FND-CROSS-0004/finding.de.md) | P1 | parent_and_framework | crs_gap | blocked | ja | Ausgewählte CRS-Profilrouten bleiben für mehrere Connectoren nicht verfügbar |
| [FND-CROSS-0005](./FND-CROSS-0005/finding.de.md) | P1 | parent_and_framework | release_blocker | blocked | ja | Release-Readiness bleibt durch ungelöste Evidence- und Quality-Gates blockiert |
| [FND-CROSS-0007](./FND-CROSS-0007/finding.de.md) | P2 | parent_and_framework | security_hardening | fixed | nein | Parent- und Framework-Task-Delivery band das effektive Origin-Push-Ziel nicht an das erwartete Benutzer-Repository |
| [FND-CROSS-0008](./FND-CROSS-0008/finding.de.md) | P1 | parent_and_framework | ci_failure | fixed | ja | #74-Root-Fix vorhanden; aufbewahrter Runtime-/Terminal-Artefaktbeleg bleibt erforderlich |
| [FND-FRAMEWORK-0007](./FND-FRAMEWORK-0007/finding.de.md) | P1 | framework | lifecycle_defect | blocked | ja | Apache-kanonischer Full-Lifecycle-Finalizer beendet sich nach Live-Traffic mit 77 |
| [FND-FRAMEWORK-0009](./FND-FRAMEWORK-0009/finding.de.md) | P1 | framework | protocol_gap | blocked | ja | NGINX-HTTP/2-Route hat keine protokollkorrelierte Case-Execution |
| [FND-FRAMEWORK-0057](./FND-FRAMEWORK-0057/finding.de.md) | P1 | framework | ci_failure | fixed | ja | Framework #51 und Parent #126/#74 fixten die Ursache; Parent-Runtime-Beleg bleibt erforderlich |
| [FND-HOST-0003](./FND-HOST-0003/finding.de.md) | P1 | host_environment | lifecycle_defect | blocked | ja | NGINX-Non-Root-Worker-Isolation kann im aktuellen Sandbox nicht bewiesen werden |
| [FND-HOST-0006](./FND-HOST-0006/finding.de.md) | P2 | host_environment | tooling | blocked | nein | Task-CPython 3.13.14 fehlt _sqlite3 und blockiert die lokale Coverage.py-Cobertura-XML-Validierung |
| [FND-MRTS-0001](./FND-MRTS-0001/finding.de.md) | P1 | mrts | mrts_gap | blocked | ja | MRTS-bezogene Assurance bleibt auf kontrollierte External-Copy-Evidence begrenzt |
| [FND-MRTS-0002](./FND-MRTS-0002/finding.de.md) | P1 | mrts | test_failure | fixed | nein | MRTS-Upstream-Policy-Sicherheitsmarker fehlte in einer erzwungenen Governance-Kontrolle |
| [FND-PARENT-0002](./FND-PARENT-0002/finding.de.md) | P2 | parent | maintainability | triaged | nein | Parent-ShellCheck-Diagnosen erfordern eine abgegrenzte Triage |
| [FND-PARENT-0003](./FND-PARENT-0003/finding.de.md) | P2 | parent | static_analysis_finding | triaged | nein | Envoy- und Traefik-staticcheck-Diagnosen erfordern eine Disposition |
| [FND-PARENT-0005](./FND-PARENT-0005/finding.de.md) | P3 | parent | security_validated | fixed | nein | #74-Deadline-Fix gemergt; aktueller Timeout-Control-Replay bleibt erforderlich |
| [FND-PARENT-0006](./FND-PARENT-0006/finding.de.md) | P3 | parent | security_validated | validated | nein | NGINX-Response-Handling kann einen Over-Limit-Suffix aus der Inspektion auslassen |
| [FND-PARENT-0007](./FND-PARENT-0007/finding.de.md) | P3 | parent | security_validated | validated | nein | Traefik-Connector-Worker-Admission ist unbegrenzt |
| [FND-PARENT-0008](./FND-PARENT-0008/finding.de.md) | P2 | parent | compiler_warning | fixed | nein | Draft PR #183 fixt Apache-module_directives-designated-initializer; Hosted-/resulting-master-Evidence steht aus |
| [FND-PARENT-0009](./FND-PARENT-0009/finding.de.md) | P2 | parent | binary_hardening_gap | triaged | nein | Apache-Binary-Hardening-Profil hat stale RUNPATH und unvollständigen Full-RELRO-Nachweis |
| [FND-PARENT-0010](./FND-PARENT-0010/finding.de.md) | P1 | parent | connector_gap | blocked | ja | HAProxy-native Capability bleibt nicht promotet |
| [FND-PARENT-0011](./FND-PARENT-0011/finding.de.md) | P1 | parent | connector_gap | blocked | ja | Envoy-native Capability bleibt nicht promotet |
| [FND-PARENT-0013](./FND-PARENT-0013/finding.de.md) | P1 | parent | security_candidate | blocked | ja | Traefik-Pfad-UDS-Cleanup behält ein finales Same-UID-Unlink-Rennen |
| [FND-PARENT-0014](./FND-PARENT-0014/finding.de.md) | P1 | parent | security_candidate | blocked | ja | Manifest-Cleanup behält ein Same-UID-Leaf-Replacement-Löschrennen |
| [FND-PARENT-0015](./FND-PARENT-0015/finding.de.md) | P1 | parent | security_candidate | blocked | ja | Traefik-Pfad-UDS erlaubt Same-UID-Endpoint-Umleitung nach Bereitschaft |
| [FND-PARENT-0020](./FND-PARENT-0020/finding.de.md) | P1 | parent | test_failure | fixed | nein | #51 erreichbar; aktueller Native-Middleware-Control bleibt erforderlich |
| [FND-PARENT-0021](./FND-PARENT-0021/finding.de.md) | P2 | parent | storage_cleanup | blocked | nein | Storage-Budget-Finalisierung kann task-eigene Validierungs- und Build-Artefakte nicht bereinigen |
| [FND-PARENT-0026](./FND-PARENT-0026/finding.de.md) | P2 | parent | security_hardening | fixed | nein | Runtime-Pfad-Policy vertraut caller-kontrollierten Projekt-Roots als Confinement-Ankern |
| [FND-PARENT-0028](./FND-PARENT-0028/finding.de.md) | P2 | parent | security_hardening | triaged | nein | SHA-gepinnte Parent-Scanner-Actions behalten mutable Docker-Image-Abhängigkeiten |
| [FND-PARENT-0042](./FND-PARENT-0042/finding.de.md) | P1 | parent | ci_failure | blocked | ja | Parent-Runtime-Komponenten-Cache bindet den NGINX-Release-Digest an ein anderes Tag-Archiv |
| [FND-PARENT-0043](./FND-PARENT-0043/finding.de.md) | P2 | parent | security_validated | blocked | nein | Apache-Interventionspuffer benötigen request-eigene Kopien vor dem nativen Cleanup |
| [FND-PARENT-0050](./FND-PARENT-0050/finding.de.md) | P1 | parent | security_hardening | fixed | ja | #74-Immutable-Source-Grenze vorhanden; volle Producer-/Cross-Repo-Validierung bleibt |
| [FND-PARENT-0052](./FND-PARENT-0052/finding.de.md) | P1 | parent | dependency_risk | fixed | ja | #74-Immutable-EXPAT-Pfad vorhanden; volle Producer-Validierung bleibt |
| [FND-PARENT-0053](./FND-PARENT-0053/finding.de.md) | P1 | parent | ci_failure | fixed | ja | #74-PCRE2-Literal-Hash-Pfad vorhanden; terminales Producer-Gate bleibt |
| [FND-PARENT-0054](./FND-PARENT-0054/finding.de.md) | P1 | parent | evidence_gap | in_progress | nein | Historische begrenzte Runtime-Log-Diagnose ist vom aktuellen Master nicht erreichbar; kein gleichwertiges aktuelles Control belegt |
| [FND-PARENT-0055](./FND-PARENT-0055/finding.de.md) | P1 | parent | test_failure | blocked | nein | Referenzierte Pfade ohne autorisierte Entfernungs-/Replacement-Provenance |
| [FND-PARENT-0056](./FND-PARENT-0056/finding.de.md) | P1 | parent | ci_failure | fixed | ja | #74/#126-Source-/Gitlink-Evidence vorhanden; Strict-Producer-Replay bleibt |
| [FND-PARENT-0057](./FND-PARENT-0057/finding.de.md) | P1 | parent | security_candidate | in_progress | ja | Draft-Parent-PR #74 expandiert PR-kontrollierte Workflow-Ausgabe an einer Template-zu-Shell-Grenze |
| [FND-PARENT-0058](./FND-PARENT-0058/finding.de.md) | P1 | parent | test_failure | fixed | ja | #74-Port-Plan-Change bleibt; Full-Matrix-/Hosted-Replay bleibt |
| [FND-PARENT-0059](./FND-PARENT-0059/finding.de.md) | P1 | parent | security_validated | fixed | ja | #74-Locking-Fix bleibt; Target-Receipt und Hosted-Run bleiben |
| [FND-PARENT-0060](./FND-PARENT-0060/finding.de.md) | P1 | parent | lifecycle_defect | fixed | ja | Full-Matrix-Batch-Scheduler schöpft seine Parallelitätsgrenze nicht work-conserving aus |
| [FND-PARENT-0061](./FND-PARENT-0061/finding.de.md) | P1 | parent | lifecycle_defect | fixed | ja | Worker-Wrapper-Abbruch vor FIFO-Completion kann den Full-Matrix-Scheduler blockieren |
| [FND-PARENT-0062](./FND-PARENT-0062/finding.de.md) | P1 | parent | ci_failure | validated | ja | Python-Workflow-Inventarvertrag referenziert einen entfernten Verified-Report-Governance-Job |
| [FND-PARENT-0063](./FND-PARENT-0063/finding.de.md) | P3 | parent | security_validated | validated | nein | Normale Runtime-Provisionierung führt release-ausgewählten veränderlichen Upstream-Source aus |
| [FND-PARENT-0064](./FND-PARENT-0064/finding.de.md) | P1 | parent | lifecycle_defect | verified | nein | Resulting-Master-APR-Harness besteht; breitere Live-Apache-Sequenz bleibt vor Abschluss |
| [FND-PARENT-0065](./FND-PARENT-0065/finding.de.md) | P2 | parent | security_validated | fixed | nein | #175-Safe-File-Containment/Regressionen vorhanden; Resulting-Master-Control bleibt |
| [FND-PARENT-0066](./FND-PARENT-0066/finding.de.md) | P2 | parent | evidence_gap | fixed | nein | Ungültige Full-Matrix-Control-Evidence konnte den Status pass behalten und eine reine Evidence-Reklassifizierung erlauben |
| [FND-PARENT-0067](./FND-PARENT-0067/finding.de.md) | P2 | parent | lifecycle_defect | validated | nein | Apache name_for_debug verwendet über den Konfigurations-Lifecycle hinweg eine nicht besessene strdup-Allocation |
| [FND-PARENT-0068](./FND-PARENT-0068/finding.de.md) | P3 | parent | security_validated | in_progress | nein | Apache-Cleanup-Runner führen Compiler-Ausgabe aus vorhersagbaren gemeinsam genutzten temporären Bäumen aus |
| [FND-PARENT-0069](./FND-PARENT-0069/finding.de.md) | P2 | parent | compiler_hardening_gap | validated | nein | Apache mod_security3.c hat eine baseline-identische GCC-C17-Werror-Fehlergruppe |
| [FND-PARENT-0070](./FND-PARENT-0070/finding.de.md) | P1 | parent | build_defect | fixed | ja | Gemergte Reparatur wartet auf frische Resulting-Master-APXS-/DSO-/HTTP-Validierung |
| [FND-PARENT-0071](./FND-PARENT-0071/finding.de.md) | P1 | parent | runtime_defect | fixed | ja | Gemergte Reparatur wartet auf frische Resulting-Master-Live-Start-/Readiness-/403-/SIGUSR1-Validierung |
| [FND-PARENT-0072](./FND-PARENT-0072/finding.de.md) | P3 | parent | sonarqube_finding | fixed | nein | PR-Sonar-Reparatur ist gemergt; direkte Resulting-Master-Sonar-Analyse/Issues bleiben nötig |
| [FND-PARENT-0073](./FND-PARENT-0073/finding.de.md) | P1 | parent | test_failure | verified | nein | #182-fokussierte Controls und resultierende PR-Evidence vorhanden; volle Framework-Suite bleibt blockiert |
| [FND-PARENT-0075](./FND-PARENT-0075/finding.de.md) | P1 | parent | ci_failure | not_applicable | nein | Historische PR-#202-Secret-Scanning-Heuristik ist nach dem gemergten verifizierten Ersatz-PR #213 überholt |
| [FND-PARENT-0046](./FND-PARENT-0046/finding.de.md) | P2 | parent | ci_failure | triaged | nein | Python-Versions-Updater-Workflow weist gültige Python-3.14-Patch-Versionen zurück |
| [FND-PARENT-0036](./FND-PARENT-0036/finding.de.md) | P2 | parent | sanitizer_finding | fixed | nein | Native-Oracle-Append-Error-Pfad gibt einen Request-Body doppelt frei |
| [FND-SONAR-0001](./FND-SONAR-0001/finding.de.md) | P1 | parent | sonarqube_finding | blocked | ja | Parent-SonarQube-Quality-Gate bleibt wegen Security-Rating und unreviewter Hotspots fehlgeschlagen |
| [FND-SONAR-0004](./FND-SONAR-0004/finding.de.md) | P1 | parent | sonarqube_finding | blocked | ja | SonarQube-Cloud-Projekt analysiert schreibgeschützte Framework- und MRTS-Bäume |
| [FND-SONAR-0009](./FND-SONAR-0009/finding.de.md) | P1 | framework | sonarqube_finding | blocked | ja | Der Model-1-Same-Repository-Coverage-Workflow für Framework-PR #39 ist lokal fixed und wartet auf die SonarQube-Cloud-Projektkonfiguration |
| [FND-SONAR-0016](./FND-SONAR-0016/finding.de.md) | P1 | parent | maintainability | in_progress | ja | Parent-Draft-PRs bewahren SonarQube-Cloud-New-Code-Finding- oder Duplizierungs-Follow-ups |
| [FND-SONAR-0019](./FND-SONAR-0019/finding.de.md) | P1 | parent | sonarqube_finding | fixed | nein | Sonar-Blocker der Traefik-Resultatserialisierung von PR #150 sind auf ihrem exakten Draft-Head behoben |
| [FND-SONAR-0022](./FND-SONAR-0022/finding.de.md) | P1 | parent | security_validated | fixed | ja | Block-Status-Generator erlaubt, dass CLI-ausgewählte Ausgabe ihre gewählte Root verlässt |
| [FND-SONAR-0023](./FND-SONAR-0023/finding.de.md) | P2 | parent | maintainability | verified | nein | Native-ModSecurity-Oracle-Result-Writer überschreitet Sonars Parameteranzahlgrenze |
| [FND-SONAR-0024](./FND-SONAR-0024/finding.de.md) | P2 | parent | maintainability | verified | nein | Native-ModSecurity-Oracle-main überschreitet Sonars Grenze für kognitive Komplexität |
| [FND-SONAR-0025](./FND-SONAR-0025/finding.de.md) | P2 | parent | security_candidate | verified | nein | Lighttpd-Lifecycle-Fixture-Input besitzt keine verifizierte Runtime-Root-Begrenzung |
| [FND-SONAR-0026](./FND-SONAR-0026/finding.de.md) | P2 | parent | maintainability | verified | nein | PR-#198-Test-Bootstrap verwendet eine optimierungssensitive zusammengesetzte Assert-Anweisung |
| [FND-SONAR-0027](./FND-SONAR-0027/finding.de.md) | P2 | parent | maintainability | verified | nein | NGINX-Connector enthält sechzehn aktuelle SonarQube-Cloud-Maintainability-Befunde |
| [FND-SONAR-0028](./FND-SONAR-0028/finding.de.md) | P2 | parent | maintainability | verified | nein | Historisches Common-Runtime-`c:S3776` ist nach PR #221 auf Resulting Master `FIXED/CLOSED` |
| [FND-SONAR-0029](./FND-SONAR-0029/finding.de.md) | P1 | parent | sonarqube_finding | verified | nein | Historisches Common-Scripts-`pythonsecurity:S8705` ist nach PR #221 auf Resulting Master `FIXED/CLOSED` |
| [FND-SONAR-0030](./FND-SONAR-0030/finding.de.md) | P2 | parent | maintainability | fixed | nein | #226 als d7dfbc5 gemergt mit 33 Checks; direkte aktuelle Sonar-Key-Readbacks bleiben |
| [FND-SONAR-0031](./FND-SONAR-0031/finding.de.md) | P2 | parent | maintainability | verified | nein | Die fünfzehn ursprünglichen `python:S3776`-CI-Evidence-Zeilen und der Duplikatblock sind nach PR #225 auf Resulting Master `FIXED/CLOSED` |

## Deduplication und Grenzen

- Historische RFA-IDs sind als Source-Mapping in `backlog.json` erhalten; sie sind keine zweiten lokalen Findings.
- Das historische generische RFA-06 wurde nicht dupliziert, weil aktuelle Runtime-Evidence seine Aussage „keine Native-Evidence“ ersetzt. Seine verbleibenden unabhängigen Lücken sind als spezifische Canonical Findings erfasst.
- `P-DISC-09-02` und reine TODO/FIXME-Zählungen wurden nicht promotet, weil die retained Evidence keine reportable Finding-Disposition stützt.
- MRTS-bezogene Einträge bleiben `mrts_external_read_only`; keine Finding-Datei autorisiert eine MRTS-Änderung.
