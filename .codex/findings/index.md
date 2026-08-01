# Finding index

This is the canonical index of the active local finding stock. `finding.json` is
the structured source; the EN and DE files are equivalent reader records. A
record is closed only after the original root-cause or closure PR, reachable
merge, current source/scanner or control evidence, and applicable checks have
been reviewed; the current reconciliation moved only seven such records.

- Generated / Erzeugt: `2026-08-01T18:28:20Z`
- Active canonical Finding-directory count / Aktive kanonische Finding-Verzeichnisanzahl: `73`; one separately inventoried historical ID remains a reserved directory without a canonical triplet.
- Reconciliation / Abgleich: [2026-08-01 audit matrix](reconciliation-2026-08-01.md) records one action for every original active canonical finding and the seven strict archive decisions.
- Bootstrap status / Bootstrap-Status: `complete; reconciliation recorded`
- Current PR #225 CI-evidence Sonar remediation: [`FND-SONAR-0031`](FND-SONAR-0031/finding.md)
  is Parent P2 `verified` / `feasible_now`, non-release-blocking, not a
  candidate integration blocker, and security-relevant. Protected exact head
  `74bcb950f8a75835b4fb59175a783e9aedcfd1c3` normally merged as master
  `6dc912643133e5c7d3c305979d4052da9cb45153`; all 14 exact-master workflows
  passed. The resulting-master readback closes all 15 retained `python:S3776`
  keys and records zero `ci/evidence` duplicate lines. The separate global
  master Quality-Gate `new_security_rating` E baseline remains `FND-SONAR-0001`.
- Current final Common Sonar remediation: [`FND-SONAR-0028`](FND-SONAR-0028/finding.md)
  and [`FND-SONAR-0029`](FND-SONAR-0029/finding.md) are Parent `verified` /
  `feasible_now`, non-release-blocking, not candidate integration blockers, and
  security-relevant. GitHub normal-merged exact PR #221 head
  `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d` as Parent master
  `3270ab5bdcc86ddab50e9be00db7611aae7fd937`; all 14 exact-master workflows
  passed. The direct resulting-master SonarQube Cloud query reports retained
  original `c:S3776` and `pythonsecurity:S8705` issues `FIXED/CLOSED`.
  The global master Quality-Gate security-rating baseline remains separately
  tracked by `FND-SONAR-0001`.
- Current PR #183 resulting-master reconciliation: Parent master
  `154ee724eba4653fa6378fc3c8729ae433e65697` is tree-identical to final PR
  #183 head `4e4dfb36e1b05f7eda38450fd3710e3a04905118` (tree
  `c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0`), and all 14 master-SHA workflows
  succeeded. `FND-PARENT-0064` is `verified`, not closed, after detached-master
  `make check-apache-ruleset-cleanup` passed five Python contracts and the
  native GCC APR harness; its broader live Apache sequence remains open.
  `FND-PARENT-0070` and `FND-PARENT-0071` are `fixed`, not verified, pending
  respectively fresh master APXS/DSO/HTTP and live start/readiness/403/`SIGUSR1`
  evidence. `FND-PARENT-0072` is `fixed`, not verified, pending direct Sonar
  master analysis and issue-query evidence.
- Current Apache lifecycle remediation / Aktuelle Apache-Lifecycle-Remediation:
  `FND-PARENT-0064` is Parent P1 `verified` / `feasible_now`, non-blocking,
  and security-relevant. PR #183 merged as master
  `154ee724eba4653fa6378fc3c8729ae433e65697` with a tree identical to final
  head `4e4dfb36e1b05f7eda38450fd3710e3a04905118`; all 14 exact-master
  workflows passed. Detached-master `make check-apache-ruleset-cleanup` passed
  five Python contracts and the native GCC APR harness. A broad fresh live
  Apache configuration/readiness/phase-2-`403`/`SIGUSR1` sequence remains
  required before closure.
- Current Apache debug-name lifecycle leak / Aktueller Apache-Debug-Name-
  Lifecycle-Leak: `FND-PARENT-0067` is Parent P2 `validated` /
  `feasible_now`, non-blocking, and not security-relevant. The retained
  private graceful Memcheck receipt
  `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/graceful-memcheck/memcheck.8.log`
  (SHA-256 `a49ca3a72f06aef4f4e67bab0b57056fe785c95a1dfba2361a892fbbf497b931`)
  records `66` definitely lost bytes in `3` `strdup`-backed blocks and no
  Invalid free/read/write or UAF diagnostic. It is separate from `FND-PARENT-0064`;
  no source repair is in the current task.
- Current Parent CI body-processor read boundary:
  FND-PARENT-0065 is Parent P2 `validated` / `feasible_now`, non-blocking
  and security-relevant. Retained pre-fix evidence proves a traversal-bearing
  artifact case_id can make request_body_bytes() disclose the preview and
  SHA-256 of only the fixed suffix conf/request-body.bin outside the safe root.
  An in-root symlink-resolving-outside control is retained for remediation
  validation. Local candidate evidence does not change the status to fixed or
  verified.
- Current Parent CI full-matrix control-evidence boundary:
  `FND-PARENT-0066` is Parent P2 `fixed` / `feasible_now`, non-blocking and
  security-relevant. The local helper now fails closed when a producer declares
  `pass` but lacks live `403` control evidence; retained pre-/post-fix receipts
  and a complete two-path security diff scan exist. Draft PR #178's exact head
  passed all 33 hosted checks, and SonarQube Cloud reports Quality Gate `OK`
  with zero open PR issues and zero new violations/duplicate lines. A
  resulting-master original reproduction remains required before `verified`.
- Current Apache cleanup-runner output-confinement boundary:
  `FND-PARENT-0068` is Parent P3 `in_progress` / `feasible_now`, not a global
  or PR-#183 candidate-integration blocker, and security-relevant. The PR #183
  RulesSet runner uses a validated private temporary leaf; the retained
  pre-remediation report (SHA-256
  `05bcf8565c7de8f6fcadf2f607e8266ff762fd5e7296d9434066c78a4eada6f7`)
  records the former local/shared-host predictable `/var/tmp` output-tree
  race before compiler-output execution. GitHub external-PR/token escalation
  is counterevidenced; only the pre-existing request-transaction sibling
  remains in progress. No closure claim is made.
- Current Apache GCC C17 baseline compiler-hardening group:
  FND-PARENT-0069 is Parent P2 validated / feasible_now and
  security-relevant, but neither a release blocker nor a candidate-integration
  blocker for selective #94A. Retained master and candidate runs both exit 1;
  their mod_security3.c source hash is
  8b21b64c95a1f1cb98ac05437e60e5d5ab8124e363cd2784b7c800e65449f8d7 and
  the 114-line diagnostics normalize to
  34b8bbdfcda5e8420a33ac99eaf57a1283388ec7f87d104b1ee36093744eacc6.
  It is a pre-existing compiler-hardening gap, deliberately separate from
  FND-PARENT-0008 and FND-PARENT-0043; no source repair or delivery claim is
  made.
- Current Apache APXS DSO materialization boundary:
  FND-PARENT-0070 is Parent P1 `fixed` / `feasible_now`, security-relevant,
  and a release blocker for normal Apache builds until a fresh resulting-master
  APXS materialization, DSO make, module-load, and HTTP control passes. The
  merged wrapper stages the expected private header, the master tree equals the
  validated PR tree, and the Apache/Common structural control passes. It is
  not a candidate-integration blocker and is neither verified nor closed.
- Current Apache smoke MIME runtime boundary:
  FND-PARENT-0071 is Parent P1 `fixed` / `feasible_now`, security-relevant,
  and a release blocker for Apache smoke/runtime acceptance until a fresh
  resulting-master live start/readiness/HTTP `403`/`SIGUSR1` sequence passes.
  The merged harness materializes both MIME paths and six focused
  resulting-master Apache/MIME unit tests pass. It is separate from
  FND-PARENT-0070 and does not itself prove the FND-PARENT-0064 APR lifecycle
  repair.
- Finding archive / Finding-Archiv:
  [`.codex/archive/findings/`](../archive/findings/README.md) contains
  one hundred non-active, losslessly retained records after this archival move; their current lifecycle
  statuses and release-blocker flags remain documented there.
- Current-user FND-HOST archive / Aktuelles FND-HOST-Nutzerarchiv:
  `FND-HOST-0001` and `FND-HOST-0005` are archived as `verified`;
  `FND-HOST-0002` and `FND-HOST-0004` are archived as user-scoped
  `not_applicable`, not technically closed. The exact unavailable local
  Python/native/optional-tool and HTTP/3 client/harness conditions remain in
  their retained triplets; `FND-HOST-0003` and `FND-HOST-0006` remain active.
- Framework archive reconciliation / Framework-Archivabgleich:
  `FND-CROSS-0006`, `FND-FRAMEWORK-0004`, `0021`, `0022`, `0026`, `0027`,
  `0028`, `0045`, `0049`, `FND-SONAR-0002`, and `FND-SONAR-0005` are now
  non-active archive records. `FND-FRAMEWORK-0031` is also in the current
  user’s test-only archive: its P1 release-blocker flag and pending Cloud
  revalidation remain effective and it is not technically closed.
- Framework PR #50/#51 resulting-master archive / Framework-PR-#50/#51-
  Resulting-Master-Archiv: `FND-FRAMEWORK-0002`, `0011`, `0053`, and `0056`
  are closed after exact Framework master
  `de705a5efb872f95f010346fe2e6143c88876ad4` and are non-active archive
  records. Receipt SHA-256: `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`.
  `FND-FRAMEWORK-0057` remains active: Parent has adopted the Framework
  Gitlink, but the fresh Parent #74 producer and strict terminal gate are not
  evidenced.
- Framework PR #52 resulting-master archive / Framework-PR-#52-Resulting-
  Master-Archiv: `FND-FRAMEWORK-0010` is closed after normal PR #52 merge as
  Framework master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`. The reviewed
  head tree equals resulting master; its focused negative/legitimate controls,
  documentation aggregate, and applicable master checks pass. Receipt
  SHA-256: `cbf90db531a6e4eab99ae84de6ba1008a07d6644b9805dcae2745fc54ad2aee9`.
- Framework current-master finding batch / Framework-Current-Master-Finding-
  Batch: `FND-FRAMEWORK-0013`, `0018`, `0019`, `0036`, and `0054` are
  `verified` on exact Framework master
  `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`. The retained receipt
  `.codex/runs/20260726-framework-findings-batch/evidence/current-master-revalidation.md`
  (SHA-256 `6912df100503c87123b72e4fac4cc76d6c8bf9f40f884786eeedfcebe0614f3c`)
  records focused negative and legitimate controls, historic PR/readback, and
  current-master checks. `FND-FRAMEWORK-0057` is `blocked` solely on Parent
  #74 terminal evidence; no Parent Gitlink or MRTS state changed. The five
  verified records are now losslessly archived. `FND-FRAMEWORK-0025` and
  `0029` are archived as local test-only `accepted_risk`, not technically
  closed; their external helper/Cloud prerequisites remain unresolved.
- Current-user fixed non-blocking Framework archive / Aktuelles Nutzerarchiv
  fester nicht blockierender Framework-Findings: `FND-FRAMEWORK-0003`, `0005`,
  `0006`, `0012`, `0014`, `0015`, `0016`, `0023`, `0024`, `0033`, and `0055`
  are losslessly retained as non-active archive records after the current user
  selected the exact `fixed` / `release_blocker: false` predicate. Their
  lifecycle values, release-blocker flags, and evidence remain unchanged; this
  is neither a closure nor a new release-readiness claim.
- Test-only fixed release-blocker archive / Test-only-Archiv fester
  Release-Blocker: the current user additionally archived twenty-nine exact
  `fixed` records retaining `release_blocker: true`, including security-relevant
  P0/P1 records, because this repository is used only for testing and no release
  is planned. This does not mark them verified, accepted, safe for production,
  or non-blocking; their retained records and the required future reactivation
  before any release are documented in the archive README.
- Historical-status note / Hinweis zum historischen Status: dated PR and
  master notes below retain their contemporaneous wording. For an ID listed in
  the archive reconciliations above, the archive membership and its retained
  canonical record are authoritative for its present active/non-active state.
- Active extension source runs / Aktive Erweiterungs-Runs: `20260722T145132Z-framework-pr-39-41-master-integration-9a3c7dc7`, `20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`, `20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37`, `20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09`, `20260723T092456Z-framework-sonarqube-test-issues-507-10387697`, `20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a`, `20260724T170026Z-worktree-cleanup-governance`, `20260726T000000Z-mrts-codex-config-reconciliation-current`, `20260726T050327Z-framework-pr45-master-integration`, `20260726T051835Z-framework-pr45-boundary-snapshot`, `20260726T000000Z-pr55-pr74-python314-import`, `20260726T083705Z-apache-upstream-pr-91-94-integration`, `20260726T103539Z-pr74-cache-owner-root`, `merge-prs-129-149-master-20260728`, `sonar-652-duplication-zero-20260728-W8wqjk`, `pr151-verified-16c3-20260728`, `pr152-verified-c9c-20260728`, `pr153-verified-c5a-20260728`, `pr154-verified-60a-20260728`, `pr156-initial-e2b-20260728`, `pr156-verified-59ff-20260728`, `pr157-verified-3055-20260728`, `pr158-verified-552f-20260728`, `pr159-verified-cf32-20260728`
- Additional active extension source run / Zusätzlicher aktiver Erweiterungs-Run:
  pr160-terminal-open-s1481-e456-20260728 is retained as terminal,
  remediation-required Draft-PR evidence.
- Latest active extension source run / Neuester aktiver Erweiterungs-Run:
  pr160-terminal-open-s1481-e456-20260728 retains a terminal Draft-PR blocker;
  it does not change the active aggregate lifecycle.
- Current Draft Parent PR #160 exact-head SonarQube Cloud blocker / Aktueller
  Exact-Head-SonarQube-Cloud-Blocker von Draft-Parent-PR #160: sealed run
  pr160-terminal-open-s1481-e456-20260728 for exact head
  e456b9fc909116656294fc744526cf8c81b0c962 against base master
  8e8acb8dab1cd03723de269cab7da7dd62e5e010 reports three OPEN task-owned
  MINOR CODE_SMELL python:S1481 findings in
  ci/checks/connectors/all/check-remaining-connectors-start-wiring.py:
  AZ-p4PPg1eeMvlV2M02- line 66 (rc_default),
  AZ-p4PPg1eeMvlV2M03A line 68 (kill_zero), and
  AZ-p4PPg1eeMvlV2M02_ line 69 (wait_command). Quality Gate is OK and new
  duplicated lines/density are 0/0.0, but the direct issue count makes this
  head remediation_required. All 39 exact-SHA GitHub checks are terminal
  (33 success, six scope-skipped), including successful SonarCloud Code
  Analysis; project-wide duplicated lines/density remain 1260/0.2. PR #160
  stays Draft, open, mergeable, and unmerged. FND-SONAR-0016 remains P1
  in_progress; no policy, suppression, exclusion, Framework/MRTS source,
  Gitlink, Ready-for-review, merge, master/default-branch, or global closure
  is claimed.
- Current Draft Parent PR #74 hosted follow-up / Aktuelles Draft-Parent-PR-#74-Hosted-Follow-up:
  retained receipt 20260726T185607Z-pr74-fast-validation-hosted-followup
  (SHA-256 5c64b4fe03ed670b0d2c25c58c2f770b59ae53bab10851ced35bd9012117d956)
  reopens FND-SONAR-0016 as P1 / in_progress: Quality Gate ERROR has
  19 OPEN task-owned findings and 0.0% new-code duplication. New
  FND-PARENT-0057 separately tracks the plausible template-to-shell/S8707
  correction, which removes the legacy output-file path through a private
  stage-parent environment hand-off; FND-PARENT-0058 separately tracks the
  validated full-matrix port-range reliability defect with its fail-closed
  1024..65000 plan. New FND-PARENT-0059 separately tracks the validated
  stale-full-matrix-lock denial of service and shell-held, inherited-FD-9
  kernel-lock boundary: SIGKILL of only the scheduler parent leaves the lock
  active until the final job/Make descendant exits. FND-PARENT-0060 now tracks
  the locally fixed non-work-conserving batch scheduler: its named refill
  regression and a 107-test combined scheduler run passed, while hosted-
  successor verification remains pending. New FND-PARENT-0061 separately
  tracks the locally fixed worker-wrapper FIFO-completion watchdog: the focused
  wrapper-death regression exits 77 and later reuses FD 9, while hosted-
  successor verification remains pending. PR #74 remains Draft and no delivery
  action is claimed.
- Current Draft Parent PR #138 SonarQube Cloud follow-up / Aktueller Draft-
  Parent-PR-#138-SonarQube-Cloud-Follow-up: the existing aggregate
  `FND-SONAR-0016` also records exact head
  `e522e43f0957368853772d747a0ffaa38ba76615`: Quality Gate `ERROR` solely
  on 20 new duplicated lines (5.649717514124294% against 3%) and one new
  `python:S3776` issue. The bounded receipt
  `sonar-open-1022-20260727/evidence/pr138-quality-gate-observation.json`
  has SHA-256
  `96299299690bf6d83a9348e6bea5d42e2f13c795c57bf8cedbfa37c48fedca24`.
  The corrective source batch is `feasible_now`; the PR remains Draft and no
  scanner-policy, suppression, Framework, MRTS, Gitlink, Ready-for-review,
  merge, or external disposition action occurred.
- Current Draft Parent PR #151 SonarQube Cloud follow-up / Aktueller Draft-
  Parent-PR-#151-SonarQube-Cloud-Follow-up: `FND-SONAR-0016` retains the
  intermediate `c:S3776` receipt `AZ-ovroGM5o_ow3fPM0Z` from exact head
  `ea52192f30ca091f9389eb10c87e9a99e2bbab4c` and the clean final exact head
  `16c3aa5d87e603de718d4a94a6d57afae159fc53`. The retained all-check run
  `pr151-verified-16c3-20260728` has zero Sonar PR issues, Quality Gate `OK`,
  zero new duplicated lines at density `0.0`, and all 39 GitHub checks
  complete (33 `success`, six scope-justified `skipped`, zero unfinished).
  PR #151 remains Draft and unmerged; this is only a task-owned Draft-PR
  remediation result, not a master or global-backlog claim.
- Current Draft Parent PR #152 SonarQube Cloud follow-up / Aktueller Draft-
  Parent-PR-#152-SonarQube-Cloud-Follow-up: historical head `ba8d` had
  `S1192`; exact follow-up head `c9c011117bd4d9c910aa4d1a767916d50c9bd26a`
  is retained by `pr152-verified-c9c-20260728` at
  `/var/tmp/codex/ModSecurity-conector/pr152-verified-c9c.5uh08S`. Its
  `SHA256SUMS` validates the receipt: zero OPEN/CONFIRMED Sonar PR issues,
  Quality Gate `OK`, new duplicated lines `0`, new-duplication density `0.0`,
  and all 39 GitHub checks completed (33 `success`, zero `neutral`, six
  scope-justified `skipped`). PR #152 remains Draft, `OPEN`, and unmerged;
  `FND-SONAR-0016` remains P1 `in_progress` because the global `652/zero`
  goals, historical #74, #138, and broader backlog remain ongoing. No Sonar
  policy, suppression, exclusion, Framework/MRTS source, Gitlink,
  Ready-for-review, merge, or master action occurred.
- Current Draft Parent PR #153 SonarQube Cloud follow-up / Aktueller Draft-
  Parent-PR-#153-SonarQube-Cloud-Follow-up: task-owned `S1066` receipt
  `AZ9cRy9OHhV2CayPTP4Z` is remediated at exact head
  `c5a45dff07ceb11eb84bc7854e6d7ca034dc9bc4`, retained by
  `pr153-verified-c5a-20260728` at
  `/var/tmp/codex/ModSecurity-conector/pr153-verified-c5a.ivXh4u`. Its
  `SHA256SUMS` validates the receipt: zero OPEN/CONFIRMED Sonar PR issues,
  Quality Gate `OK`, new duplicated lines `0`, new-duplication density `0.0`,
  and all 39 GitHub checks completed (33 `success`, zero `neutral`, six
  scope-justified `skipped`). PR #153 remains Draft, `OPEN`, and unmerged;
  `FND-SONAR-0016` remains P1 `in_progress` because the global `652/zero`
  goals, default branch, historical #74, #138, and broader backlog remain
  ongoing. No Sonar policy, suppression, exclusion, Framework/MRTS source,
  Gitlink, Ready-for-review, merge, or master action occurred.
- Current Draft Parent PR #154 SonarQube Cloud follow-up / Aktueller Draft-
  Parent-PR-#154-SonarQube-Cloud-Follow-up: three task-owned `S1192` receipts
  `AZ9cRyqOHhV2CayPTPzr`, `AZ9cRyqOHhV2CayPTPzq`, and
  `AZ9cRyZWHhV2CayPTPwQ` are clean at exact head
  `60a13292c9173a760f94672c6855a97099d1fcc2`. The retained all-check run
  `pr154-verified-60a-20260728` at
  `/var/tmp/codex/ModSecurity-conector/pr154-verified-60a.Hr5Ki8` has
  validated `SHA256SUMS`, zero OPEN/CONFIRMED Sonar PR issues, Quality Gate
  `OK`, new duplicated lines `0`, new-duplication density `0.0`, and all 39
  exact-SHA GitHub checks terminal, including successful `SonarCloud Code
  Analysis`. PR #154 remains Draft, `OPEN`, and unmerged; `FND-SONAR-0016`
  remains P1 `in_progress` because the global `652/zero` goals, default branch,
  historical #74, #138, and broader backlog remain active. No Sonar policy,
  suppression, exclusion, Framework/MRTS source, Gitlink, Ready-for-review,
  merge, or master action occurred.
- Current Draft Parent PR #156 bounded exact-head SonarQube Cloud result /
  Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #156: `FND-SONAR-0016` retains initial exact head
  `e2b1370caa32e621ada4ce96ad03f603904cee49` / run
  `pr156-initial-e2b-20260728` as the seven-OPEN-`python:S3415` historical
  observation. Its sealed successor run `pr156-verified-59ff-20260728` at
  `/var/tmp/codex/ModSecurity-conector/pr156-verified-59ff.Ce1cD4` has
  validated `SHA256SUMS` for exact head
  `59ff4d5bbb6e278d93c0b965096e842b77f446bb` against base `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`: direct Sonar issues `0`,
  Quality Gate `OK`, new duplicated lines/density `0`/`0.0`, and all 39
  exact-SHA GitHub checks terminal (33 `success`, six scope-justified
  `skipped`), including successful `SonarCloud Code Analysis` with zero
  annotations. PR #156 remains Draft, `OPEN`, and unmerged; this is bounded
  Draft-PR evidence only. `FND-SONAR-0016` remains P1 `in_progress` because
  global `652/zero` goals, the default branch, historical #74/#138, and
  broader backlog work remain active. No Sonar policy, suppression, exclusion,
  Framework/MRTS source, Gitlink, Ready-for-review, merge, or master action
  occurred.
- Current Draft Parent PR #159 bounded exact-head SonarQube Cloud result /
  Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #159: sealed run `pr159-verified-cf32-20260728` at
  `/var/tmp/codex/ModSecurity-conector/runs/pr159-exact-head-cf32-20260728.B9kyWO`
  has validated `SHA256SUMS` for exact head
  `cf323de85b4411b2c1f56055a430d43f65a8ed97` against base `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`. The PR description identifies
  two Parent `shelldre:S1192` literal-duplication findings in
  `connectors/lighttpd/harness/run_patched_full_lifecycle.sh` for
  `%{http_code}` at eight status probes and `1,200p` at six diagnostic paths;
  no original Sonar key is inferred. Direct Sonar issues are `0`, Quality Gate
  is `OK`, new duplicated lines/density are `0`/`0.0`, project-wide duplicated
  lines/density remain `1260`/`0.2`, and all 39 exact-SHA GitHub checks are
  terminal (33 `success`, six scope-skipped), including successful
  `SonarCloud Code Analysis` with zero annotations; reviews and review
  comments are both `0`. PR #159 remains Draft, open, mergeable, and unmerged.
  This is bounded Draft-PR evidence only: `FND-SONAR-0016` remains P1
  `in_progress`; no policy, suppression, exclusion, Framework/MRTS source,
  Gitlink, Ready-for-review, merge, master, or global closure is claimed.
- Current Draft Parent PR #158 bounded exact-head SonarQube Cloud result /
  Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #158: sealed run `pr158-verified-552f-20260728` at
  `/var/tmp/codex/ModSecurity-conector/pr158-verified-552f.umSut7` has
  validated `SHA256SUMS` for exact head
  `552fd67ee1212c0a71cec1726f6a079e33671c87` against base `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`. Its manifest identifies only
  Parent HAProxy HTX diagnostic-range `shelldre:S1192` remediation, with no
  original Sonar key or source location to infer. Direct Sonar issues are `0`,
  Quality Gate is `OK`, new duplicated lines/density are `0`/`0.0`, and all 39
  exact-SHA GitHub checks are terminal (33 `success`, six scope-justified
  `skipped`), including successful `SonarCloud Code Analysis`; reviews and
  review comments are both `0`. PR #158 remains Draft, open, mergeable, and
  unmerged. This is bounded Draft-PR evidence only: `FND-SONAR-0016` remains
  P1 `in_progress` because the global `652/zero` target, default branch,
  historical #74/#138, and broader backlog remain active. No policy,
  suppression, exclusion, Framework/MRTS source, Gitlink, Ready-for-review,
  merge, master, or global closure is claimed.
- Current Draft Parent PR #157 bounded exact-head SonarQube Cloud result /
  Aktuelles begrenztes Exact-Head-SonarQube-Cloud-Ergebnis für Draft-Parent-
  PR #157: the original Parent `python:S1192` receipt
  `AZ9cRyW7HhV2CayPTPuq` was at
  `ci/checks/documentation/check-bilingual-docs.py:728` in
  `check_tools_mrts_clean(repo)`. Sealed run `pr157-verified-3055-20260728`
  at `/var/tmp/codex/ModSecurity-conector/pr157-verified-3055.dvn7gp` has
  validated `SHA256SUMS` for exact head
  `3055790e88e6b962bdffdabadccee1de2ce59355` against base `master`
  `8e8acb8dab1cd03723de269cab7da7dd62e5e010`: direct Sonar issues `0`,
  Quality Gate `OK`, new duplicated lines/density `0`/`0.0`, and all 39
  exact-SHA GitHub checks terminal (33 `success`, six scope-justified
  `skipped`), including successful `SonarCloud Code Analysis` with zero
  annotations. PR #157 remains Draft, `OPEN`, and unmerged. This is bounded
  Draft-PR evidence only: `FND-SONAR-0016` remains P1 `in_progress` because
  the global `652/zero` goal, default branch, historical #74/#138, and broader
  backlog remain active. No Sonar policy, suppression, exclusion,
  Framework/MRTS source, Gitlink, Ready-for-review, merge, master, or global
  closure is claimed.
- Current Draft Parent PR #155 SonarQube Cloud follow-up / Aktueller Draft-
  Parent-PR-#155-SonarQube-Cloud-Follow-up: four clean task-owned receipts
  `AZ98JczJLJyjbmyNA5LW`, `AZ98JczJLJyjbmyNA5LO`,
  `AZ98JczJLJyjbmyNA5LS`, and `AZ98JczJLJyjbmyNA5LU` are retained at exact
  head `0e980f6c2a46ef92f14a007bc8d0c6d538885192` by
  `pr155-verified-0e9-20260728` at
  `/var/tmp/codex/ModSecurity-conector/pr155-verified-0e9.NkGL9s`. Its
  `SHA256SUMS` validates zero OPEN/CONFIRMED Sonar PR issues, Quality Gate
  `OK`, new duplicated lines `0`, new-duplication density `0.0`, and all 39
  exact-SHA GitHub checks terminal (33 `success`, six scope-justified
  `skipped`), including successful `SonarCloud Code Analysis`. PR #155
  remains Draft, `OPEN`, and unmerged; `FND-SONAR-0016` remains P1
  `in_progress` because global `652/zero` goals, the default branch,
  historical #74/#138, and broader backlog work remain active. No Sonar
  policy, suppression, exclusion, Framework/MRTS source, Gitlink,
  Ready-for-review, merge, or master action occurred.
- Current Draft Parent PR #150 SonarQube Cloud follow-up / Aktueller Draft-
  Parent-PR-#150-SonarQube-Cloud-Follow-up: `FND-SONAR-0019` is `fixed` at
  exact head `4dae04f2d584da855139d6f42ab36c1bdf8c8d63`. GitHub binds a
  successful SonarCloud check to that SHA, and the retained PR readback has
  Quality Gate `OK` plus zero OPEN/CONFIRMED issues. The finding remains fixed,
  not verified or closed, until separately authorized integration and a
  current-master recheck; no scanner policy, suppression, Framework, MRTS,
  Gitlink, Ready-for-review, or merge action occurred.
- Current normal-provisioner provenance validation / Aktuelle Validierung der
  Normal-Provisioner-Provenance: `FND-PARENT-0063` is P3 `validated` /
  `requires_user_decision`, security-relevant but not release-blocking. The
  retained offline production-module fixture passed a synthetic changed
  `releases/latest` tag through `prepare_release_git_component` with
  `strict=True` to the real Go build sink, without network contact or upstream
  execution. Scheduled/manual provisioner workflows use `contents: read` and
  `persist-credentials: false`; no `pull_request_target`, secret reference, or
  writable repository token was found. The in-scope supply-chain path is low/P3
  because an upstream compromise is required. A current immutable-provenance
  choice and separate Framework write authorization, if defaults are
  Framework-owned, are required before remediation.
- Current Parent master Python workflow inventory contract failure / Aktueller
  Parent-master-Python-Workflow-Inventarvertragsfehler: `FND-PARENT-0062` is
  P1 `validated` / `feasible_now` and release-blocking. On current Parent
  master `dd175053b3d7f509286af87646d6eb093a49d578`, the exact inventory still
  requires `verified-report-governance.yml:verified-report-contract-preflight`,
  but that job is absent from the workflow. The current-master-equivalent
  scope control exits `0`, while `rtk proxy make check-python-version-contract`
  exits `2`; retained receipt SHA-256 is
  `17ae8b2b76e65e4f9db7625122b56f5d74c171bed69912f6ba2a68198b3b283e`.
  The separate focused Parent alignment PR must preserve canonical Python setup
  and workflow trust controls, add a regression, and obtain hosted proof; it
  must not be silently folded into PR #138. No workflow, scanner, suppression,
  Framework, MRTS, Gitlink, or delivery state changed for this record.
- Historical-label note / Hinweis zur historischen Kennzeichnung: later legacy
  bullets headed “Current Framework PR #39 …” are retained PR-#39 evidence
  only, not current `FND-FRAMEWORK-0044` state. Their references to 25 keys,
  CPython 3.13.14, `requires_user_decision`, and `FND-SONAR-0009` are
  superseded for PR #42 by the authoritative reconciliation below.
- Current Framework PR #45 resulting-master Sonar reassessment / Aktuelle
  Framework-PR-#45-Resulting-Master-Sonar-Neubewertung: exact head
  `dd7e221d903a7e2e0a59af203ba312dfca55d69c` normally merged with exact-head
  protection as Framework master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb`;
  its tree equals the reviewed head. Applicable resulting-master GitHub checks
  passed, but SonarCloud Check Run `89757305894` failed solely on Security C
  (actual `3`, threshold `1`). The current leak-period inventory has 19
  open/confirmed records: nine read-only MRTS VULNERABILITY signals and ten
  CODE_SMELL records. `FND-SONAR-0002` remains P1 `blocked`; no PR-#45 risk
  acceptance, Parent/gitlink/MRTS action, control change, or closure occurred.
  A later read-only boundary snapshot preserved three unattributed dirty MRTS
  working-tree paths while confirming unchanged task-owned gitlink/commit
  references. Receipts SHA-256: `21a8bb0c5cf83ac6ca0156d3285e5829ca1d871754dc9019516844ef9c94695d`,
  `07da9852d035d0be72a3260258d0d05b350d7a1b1e49c5acd7e6f229f39b13d9`.
- Framework PR #44 merged under bounded master-Sonar acceptance / Framework PR #44 unter eng begrenzter Master-Sonar-Akzeptanz gemergt: exact head `3b67efb8534fb56a93f085897417ada449ff1a39` was normally merged with exact-head protection as Framework master `4c9753291d26d92f2d7e51ae425dedb79666fd5e`; its tree equals the reviewed head. Resulting-master CodeQL, advisory, common-structure, and lint controls passed. SonarCloud fails only on the accepted Security-C residual (actual `3`, threshold `1`) with nine `needs_review` read-only MRTS signals. The global P1 `FND-SONAR-0002` remains `blocked`; no control, Parent, or MRTS scope was waived or changed. Post-merge receipt SHA-256: `71228129d8b0a24706a35219fb568679ef7be0e7a47a615cb7f5abcc167c1f3f`.
- Authoritative current Framework PR #42 Sonar/Python reconciliation / Maßgeblicher aktueller Framework-PR-#42-Sonar-/Python-Abgleich: `FND-FRAMEWORK-0044` is `fixed` locally for its 27 owned non-security code-smell keys, and the historical 15-key PR #42 subset of `FND-FRAMEWORK-0050` is `fixed` locally. The combined task-owned Framework patch configures exact CPython `3.14.6`; selected local CPython `3.14.4` controls passed 61 migration tests, 49 direct remediation tests, contracts, CP314 hash-lock controls, documentation checks, `git diff --check`, and full native `make lint`. The complete 22-path security scan has zero reportable findings (`report.md` SHA-256 `1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36`). This does not prove hosted Sonar, a target-3.14.6 hosted job, or delivery; normal exact-head submission and fresh no-suppression Sonar proof remain required. The older PR #39/CPython-3.13.14 text below is historical only, and `FND-SONAR-0002` remains the independent master blocker.
- Current Framework-master S3415 verification / Aktuelle Framework-master-S3415-Verifikation: PR [#43](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/43) exact head `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` merged normally as Framework master `f98a8739cb13b583f23d646784b144e596b61441`. The 507 Framework-owned `python:S3415` MAJOR test keys from pre-remediation master `935cf14c676a24672be5c336e92cd13457cc35c8` / analysis `dda3ea04-2721-4ee6-a9c1-74bd2925f139` are verified absent from exact resulting-master analysis `77e255d6-17a2-4e8a-bb29-6438e91e6fa8`. The resulting gate is ERROR solely on independent `FND-SONAR-0002` Security C from nine read-only MRTS signals; the PR #42-only risk acceptance does not cover #43. Post-merge receipt SHA-256: `d8a63662d10def3118b5795c90474a0c63ab9a96a82d5e93debb8436c79bd79c`.
- Current Framework PR #42 resulting-master disposition / Maßgebliche aktuelle Framework-PR-#42-Resulting-Master-Disposition: PR #42 exact head `dc6cf411e78b3f37f1e4be52edef59894560b1ae` was normally merged with exact-head protection as Framework master `935cf14c676a24672be5c336e92cd13457cc35c8`; its tree equals the reviewed PR head and eight exact-master GitHub Actions workflows completed successfully. `FND-FRAMEWORK-0046`, `0049`, `0051`, and `0052` are `verified`, not closed, after their original OSV, Pyright, or Ruff controls and resulting-master evidence passed. `FND-FRAMEWORK-0053` is `in_progress`: the merged Change Record still claims that PR #42/resulting-master evidence is unobserved, so a separately authorized bilingual documentation follow-up is needed. The completed delivery retains two bounded historical risks: exact Sonar analysis `dda3ea04-2721-4ee6-a9c1-74bd2925f139` is ERROR solely on Security C, and resulting-master Cloudflare suite `81246317347` is queued with no check runs. `FND-SONAR-0002` remains an active global P1 blocked finding; `FND-GITHUB-0007` is retained separately in the local archive as current-user `accepted_risk`, not as passing or technically closed. Retained post-merge receipt SHA-256: `0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`. Parent gitlink and MRTS remain unchanged.
- Superseding Model-1 PR #39 coverage update / Ablösende Model-1-PR-#39-Coverage-Aktualisierung: The user selected Model 1. The local Model-1 workflow implementation is fixed, but FND-SONAR-0009 is lifecycle `blocked` / `blocked_external_dependency`: the final local suite passed 23 tests, and the generic workflow, CI-security contract, CI-security evidence-contract, and selected syntax checks passed. The project owner must still configure a dedicated least-privilege SONAR_TOKEN and switch the existing SonarQube Cloud project from automatic to CI-based analysis; neither external action, a hosted scan, imported coverage, or a Quality Gate was observed. The exact residual trust assumption is: same-repository PR initiators are authorized for the project analysis token. FND-HOST-0006 is the distinct P2 blocked_environment local CPython 3.13.14 _sqlite3/Coverage.py blocker; it is not the hosted project/token blocker.
- Current Framework PR #37 delivery-record reconciliation / Aktuelle Framework-PR-#37-Delivery-Record-Reconciliation: `FND-FRAMEWORK-0045` is `verified`, not closed, on Framework master `f73f8842f45318e2df8aff1d31855eeb7c20a22f`. Exact source `1e9fa0d22639517193d450b05eb7b07193e41257` was normally merged after fresh PR-head controls; the original stale no-merge wording no longer occurs and direct `master` pushes remain prohibited. The independent default-branch SonarCloud blocker is `FND-SONAR-0002`; it does not reopen this documentation finding. No Parent gitlink or MRTS action occurred.
- Historical Framework PR #39–#41 consolidation (superseded by exact PR #42
  head `2930e04e1558b5b10bdeb87a76abb077a2085566`) / Historische
  Framework-PR-#39–#41-Konsolidierung: `FND-FRAMEWORK-0047` and
  `FND-FRAMEWORK-0048` remain P1 `fixed` local remediations with their retained
  exact-head evidence. `FND-FRAMEWORK-0046` was then `in_progress`: exact PR
  #42 head `e0564d219980d62bc37162ac6c11641f289f1b71` failed OSV run
  `29956021487` / job `89045175516` because CPython `3.14.6` from bounded head
  data installed trusted base `f73f8842f45318e2df8aff1d31855eeb7c20a22f`'s
  CP313-only lock. The exact-SHA-bound trusted-base CPython `3.13.14` bridge
  applies only to that exact base with its missing selector; every other base
  or selector state fails closed. At that historical stage, no current local
  or hosted verification was recorded.
- Historical Framework PR #42 quality follow-up (superseded by exact head
  `2930e04e1558b5b10bdeb87a76abb077a2085566`) / Historischer
  Framework-PR-#42-Quality-Follow-up: the exact follow-up head
  `f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c` passed the repaired OSV control,
  SonarQube Cloud, and the Ruff stages, but its Python-quality job
  `29961019802` / `89061788219` reached hosted CPython `3.14.6` Pyright and
  reported two distinct fixture annotations. Those diagnostics were P1
  `in_progress` `FND-FRAMEWORK-0052`; its one-file, test-only correction was
  locally validated and awaited a new exact-head hosted result.
  `FND-FRAMEWORK-0049` remains independently `fixed`, not verified: its exact
  green head `1fd3b362e0fed9766c6920e3c7bd1939535850f2` passed run
  `29943112344` / job `89001693819`, but normal Framework-master integration
  and resulting-master evidence remain absent. No Parent gitlink or MRTS
  change occurred.
- Current Framework PR #37 master Sonar reassessment / Aktuelle Framework-PR-#37-Master-Sonar-Neubewertung: `FND-SONAR-0002` remains P1 `blocked`. Resulting master `f73f8842f45318e2df8aff1d31855eeb7c20a22f` has only a failed SonarCloud check (New Security Rating C, actual `3`, threshold `1`); applicable Actions and CodeQL passed. The nine current gate-driving signals are unchanged, pre-PR-#37, read-only MRTS inputs and are `needs_review` after static source/control/sink triage. No current risk acceptance, MRTS action, scanner/gate change, or PR #37 causality is recorded.
- Current Framework PR #39 Sonar remediation and coverage-ingestion blockers / Aktuelle Framework-PR-#39-Sonar-Remediation und Coverage-Ingestion-Blocker: FND-FRAMEWORK-0044 remains `fixed` for 25 locally remediated non-security CODE_SMELL keys. Its Framework-specific CPython `3.13.14` qualification passed hash-locked `PyYAML-6.0.3`, `pip check`, 30 direct affected tests, 89 `make test-ci-security-contract` tests, workflow and documentation checks, `python -m compileall -q ci tests`, the response-body guard, and `make lint`; receipt SHA-256: `2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30`. This local evidence does not establish hosted SonarQube Cloud or GitHub confirmation, and no coverage, scanner, Quality Gate, rule, exclusion, suppression, or hosted-service configuration changed. FND-FRAMEWORK-0044 has feasibility `requires_user_decision` because FND-SONAR-0009 remains the distinct P1 `blocked` coverage-ingestion condition: a current user decision must select and authorize the external CI and SonarQube Cloud coverage-authentication scope and owner before delivery, exact-head report ingestion, and meaningful coverage can be verified. The fresh exact-head SonarQube Cloud confirmation of all 25 original keys remains pending; no risk is accepted.
- Current S8707 Lighttpd entity-fixture output containment repair / Aktuelle S8707-Lighttpd-Entity-Fixture-Output-Containment-Reparatur: current Parent `pythonsecurity:S8707` VULNERABILITY key `AZ9cRynaHhV2CayPTPzR` at `connectors/lighttpd/harness/lighttpd_http1_entity_fixture_upstream.py:47`, master blob `e64d11434ccff675a0470ed1d3d1a053c3c7978d`, accepted CLI `--ready-file` and `--result-file` output paths without a declared safe root and wrote JSON through a predictable `.{path.name}.tmp` sibling before replacing the final path. The local Parent repair requires `--safe-root`, rejects direct outside-root, symlinked-directory, and final-symlink control-file escapes before listening, updates the runner to pass `--safe-root "$FIXTURE_DIR"`, and publishes JSON through `mkstemp` plus `os.replace`. The pre-fix regression proved a pre-placed `.result.json.tmp` symlink could leave `result.json` as a symlink; post-fix the helper suite passed seven tests, Python compilation passed, and the full Lighttpd patched-host contract suite passed 16 tests. Retained receipt: `sonar-s8707-lighttpd-fixture-output-fix-20260721T043051Z.json`, SHA-256 `94f14a450f447fcea4095914309b4e1a8290ef41376520863a8981b319a3adfb`. The local result is `fixed`, but the external issue is still `OPEN` on master until a separately authorized delivered head receives Sonar analysis; it is not a false-positive candidate. Together with the ten not_actionable rows and the response-header S8707 local repair, the current bounded scope covers twelve regular keys and leaves 194 exact-inventory Parent Vulnerability rows; `FND-SONAR-0001` remains blocked by its three separately unreviewed hotspots. No delivery, external Sonar action, suppression, rule/gate change, Framework/MRTS/gitlink action, or risk acceptance occurred.
- Current S8707 response-header fixture containment repair / Aktuelle S8707-Response-Header-Fixture-Containment-Reparatur: current Parent `pythonsecurity:S8707` VULNERABILITY key `AZ9cRyfJHhV2CayPTPxt` at `ci/runtime/common/response-header-test-backend.py:101`, master blob `fed58d05fbf3897d8e0d19299048c2310773c092`, reached `Path.read_text` through `--fixture-file` without the existing `--safe-root` check applied to `--body-file`. The local Parent repair shares the canonical regular-file and safe-root resolver with fixture paths. The real-CLI regression proved direct outside-root and in-root-symlink bypasses before the repair; post-fix the backend suite passed six tests and rejects both before listening while retaining the valid in-root fixture control. Python compilation, adjacent Apache/full-lifecycle contract suites, and an independent security diff review passed. Retained receipt: `sonar-s8707-response-header-fixture-fix-20260721T033723Z.json`, SHA-256 `80922e5534416cbfc66145e2707b6bcbff0a1633ab3e24db09f8a54b7205fbf8`. The local result is `fixed`, but the external issue is still `OPEN` on master until a separately authorized delivered head receives a Sonar analysis; it is not a false-positive candidate. At this milestone, together with the ten not_actionable rows, the bounded scope covered eleven regular keys and left 195 exact-inventory Parent Vulnerability rows; the Lighttpd S8707 repair above raises the current local scope to twelve and leaves 194. `FND-SONAR-0001` remains blocked by its three separately unreviewed hotspots. No delivery, external Sonar action, suppression, rule/gate change, Framework/MRTS/gitlink action, or risk acceptance occurred.
- Historical-count note / Hinweis zum historischen Zähler: the S5443 entry immediately below records the prior ten-key/196-row state. The two S8707 repairs above are the current state and reduce the bounded backlog to 194.
- Current Clang temporary-directory S5443 Vulnerability triage / Aktuelle Clang-Temporary-Directory-S5443-Vulnerability-Triage: current Parent `python:S5443` VULNERABILITY key `AZ9gJKOrg304P0Qlak6y` at `tests/test_clang_analysis_baseline.py:41`, exact-master blob `0b8a34b44453faed5de129a13ec186de2e12c5eb`, is technically `not_actionable`. The test-only `tempfile.TemporaryDirectory` has a constant prefix and optional same-privilege `TMPDIR` parent; all seven callers use it as a context manager before deriving child paths. Python documents race-safe `mkdtemp` creation and a directory accessible only by its creating user: <https://docs.python.org/3/library/tempfile.html>. The focused eight-test contract suite passed. No source patch, external false-positive disposition, hotspot review, suppression, rule or Quality-Gate change, Framework/MRTS or gitlink action, or risk acceptance occurred. The retained receipt is `sonar-s5443-clang-tempdir-triage-20260721T031222Z.json`, SHA-256 `87d162bf24ab136cbc00e841b3cb9f2a8637aea81d34f8301ebaae5a1f176b98`. At that milestone the cumulative local scope was ten regular keys and 196 exact-inventory Parent Vulnerability rows; the two S8707 repairs above reduce the current local backlog to 194. `FND-SONAR-0001` remains blocked by the three separately unreviewed hotspots, and any external disposition still requires a current explicit user decision.
- Earlier refresh-report S2083 Vulnerability triage / Frühere Refresh-Report-S2083-Vulnerability-Triage: two Parent `pythonsecurity:S2083` VULNERABILITY keys, `AZ9cRyiqHhV2CayPTPyS` and `AZ9cRyiqHhV2CayPTPyR`, are technically `not_actionable` on exact master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`. Retained report or command text reaches only `Path.write_text` content in `ci/evidence/reports/refresh-connector-reports.py:281` and `:1063`; static `GENERATED_REPORTS` catalog outputs and explicit operator roots independently select the destination Path. No source patch, external false-positive disposition, hotspot review, suppression, rule or Quality-Gate change, Framework/MRTS or gitlink action, or risk acceptance occurred. The retained receipt is `sonar-s2083-refresh-connector-reports-triage-20260721T025657Z.json`, SHA-256 `3f73655e0a861a0b39d8987eafea08e33ef3b66e3625c3925fb0777cc315ae4f`. At the end of this cluster the cumulative local scope was nine regular keys and 197 exact-inventory Parent Vulnerability rows; the current S5443 triage above reduces it to 196. `FND-SONAR-0001` remains blocked by the three separately unreviewed hotspots, and any external disposition still requires a current explicit user decision.
- Earlier audit-renderer S2083 Vulnerability triage / Frühere Audit-Renderer-S2083-Vulnerability-Triage: three Parent `pythonsecurity:S2083` VULNERABILITY keys, `AZ9cRygDHhV2CayPTPxy`, `AZ9cRygDHhV2CayPTPxx`, and `AZ9cRygDHhV2CayPTPxz`, were technically `not_actionable` on exact master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`. The local JSON payload reaches only `Path.write_text` content in `ci/evidence/reports/audit-full-lifecycle-runtime-roots.py:339-341`, never its independent output Paths; no source patch, external false-positive disposition, hotspot review, suppression, rule or Quality-Gate change, Framework/MRTS or gitlink action, or risk acceptance occurred. The retained receipt is `sonar-s2083-runtime-root-audit-triage-20260721T023733Z.json`, SHA-256 `9a361f2ed67a4a0fa1dae11f6107ca2cd8fe7c88dd2557c84c2473dee3318d9c`. At the end of that cluster the cumulative scope was seven regular keys and 199 exact-inventory Parent Vulnerability rows; the later refresh-report triage reduced it to 197, and the current S5443 triage above reduces it to 196. The separate S5332-only count of 202 below is historical before both S2083 triages.
- Current Apache intervention ownership remediation / Aktuelle Apache-Intervention-Ownership-Remediation: `FND-PARENT-0043` is a distinct Parent `P2`/`medium` `security_validated` finding in `blocked`, not fixed, verified, or closed because native validation remains unknown. Final PR #72 head `486aef56424f5bf33bcd7396f6dc2f881f7f3bdd` was squash-merged as current master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` with an identical tree; 14 observed master Actions workflows passed. The task-owned PR SonarQube Cloud result passed with zero new issues/hotspots and `0.0%` duplication. Master duplication is `0.4%` and passes; its separate Quality-Gate failure remains in `FND-SONAR-0001`. Native Apache/APR/libModSecurity and ASan/LSan validation remain blocked.
- Current PR #55 current-master gate / Aktueller PR-#55-Current-master-Gate: the reviewed Framework provenance candidate was transferred without path overlap to private Framework `master` `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b`; byte comparisons, `git diff --check`, and changed-shell syntax passed. The selected Framework `.venv/bin/python` is absent, so the exact-candidate provenance suite, documentation check, and complete lint are `blocked_environment`, not substituted with system/Parent Python. No Framework branch, commit, push, PR, Parent runtime run, gitlink update, merge, or MRTS action occurred. Retained evidence: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`, SHA-256 `067db2ef9c429fa405737d193aa7a7fa5751c158b4d0ffdddbc6667918ce3ed6`.
- Current Framework Python-maintenance hardening / Aktuelles Framework-Python-Wartungs-Hardening: `FND-FRAMEWORK-0033`, `FND-FRAMEWORK-0037`, `FND-FRAMEWORK-0038`, and `FND-FRAMEWORK-0039` are locally `fixed` after the expression-aware secret-context contract, runner-context/ShellCheck, fallback-YAML, and fixed candidate-path repairs. The 36 focused tests, 85 CI-security tests, native workflow/documentation/full-lint gates, and sealed complete 11-file security-diff scan passed with zero reportable findings. Exact-current-head GitHub Actions, review, and SonarQube evidence remains pending on the authorized Draft PR; no Framework merge, Parent gitlink update, or MRTS action occurred. Source run: `20260720T180337Z-framework-python-313-updater-f3349a7e`.
- Current PR #55 runtime-evidence remediation / Aktuelle PR-#55-Runtime-Evidence-Remediation: `FND-PARENT-0042` is the independent P1 Parent cache-release-asset blocker in `blocked` / `blocked_environment`, not fixed, verified, or closed. Its local Parent source repair binds the exact GitHub release tuple, has no tag-archive/latest fallback, and passed 31 focused cache/provenance tests plus the focused shell, documentation, and review controls. The corrected manifest SHA-256 `3adf2284d3318cc35e690d319a84fe27200fe33047f43db22a328bf3c986253a` records the exact release-download URL and matching release-asset SHA-256; the original `sha256_mismatch` no longer reproduces. The legitimate preparation then stops independently at `missing_nginx_modsecurity_module` (NGINX build exit `77`), while broad documentation make checks remain `blocked_environment` only by pre-existing links into the intentionally uninitialized Framework gitlink. `FND-FRAMEWORK-0036` is reopened as `in_progress`: the f98-based fresh-fetch candidate lacks the previously validated explicit fresh-root containment/scrubbing helper. The distinct `FND-FRAMEWORK-0054` is a `triaged` P2/medium plausible host-Git PATH-binding candidate; it does not demonstrate a productive hostile PATH actor. `FND-PARENT-0050` preserves its historical build-order proof and now tracks the unverified generic-Git acquisition hand-off after configuration admission; it requires a Framework-owned safe acquisition bridge or reviewed equivalent. No staging, commit, push, PR, merge, Parent gitlink, Framework, or MRTS action occurred in this registry update. `FND-CROSS-0001` remains separately blocked pending the complete legitimate runtime evidence chain.
- Current regular S5332 Vulnerability triage / Aktuelle reguläre S5332-Vulnerability-Triage: four current Parent `python:S5332` `VULNERABILITY` keys (`AZ9cRysWHhV2CayPTP0c`, `AZ9MwivX-bUaKQ_zSGAh`, `AZ9cRyW7HhV2CayPTPur`, and `AZ9cRyfJHhV2CayPTPxs`) are technically `not_actionable` on exact master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`: two loopback-only connector harnesses, a local documentation-link classifier, and a loopback response-header test fixture. No source patch, false-positive disposition, hotspot review, suppression, rule change, Quality-Gate change, Framework/MRTS or gitlink action, or risk acceptance occurred. The retained per-key receipt is `sonar-s5332-regular-vulnerability-current-master-triage-20260721T020213Z.json`, SHA-256 `710339515e3f89b89b560209c39788db5b008cc2e03dc742dc357cfbd4ffd6d5`; the result covers only four keys and leaves 202 exact-inventory Parent Vulnerability rows untriaged. `FND-SONAR-0001` remains `blocked` for the three separately unreviewed hotspots and external dispositions still require a current explicit user decision.
- Current Codex Cloud Security reconciliation / Aktuelle Codex-Cloud-Security-Reconciliation: `FND-FRAMEWORK-0029` is `blocked_permissions`, not a source-vulnerability disposition. Framework `master` is exactly `784977615acfc55567e37b863309abc4a38ac877`; GitHub CodeQL is current and independently clear, but it is not Codex Cloud. After user authorization, documented Codex Cloud Findings and Scans URLs redirected this transport to ChatGPT login at `2026-07-20T17:03:40Z`. The active goal remains blocked until an authenticated workspace session or authoritative export is available; no Cloud finding was closed. Source run: `20260720T162741Z-framework-codex-cloud-security-reconciliation-08539bb5`.
- Current parser-blocker extension / Aktuelle Parser-Blocker-Erweiterung: FND-FRAMEWORK-0027 and FND-FRAMEWORK-0028 are `verified`, not closed or risk-accepted, on Framework master `784977615acfc55567e37b863309abc4a38ac877`. The refreshed #36 head `1608352912a755f0f8639eddfa2350436446067e` is an ancestor with an equal tree; the original exact-master reproducer passed with resolved approved literals/aliases and a manual-review empty update for v3.0.16. No Parent gitlink or MRTS change occurred.
- Current Framework PR #35 / #36 integration / Aktuelle Framework-PR-#35-/#36-Integration: #36 was normally merged as Framework master `784977615acfc55567e37b863309abc4a38ac877` after fresh exact-head Actions, CodeQL, Sonar PR Quality Gate, documentation, review, conflict, and security controls passed. Resulting-master CodeQL Actions/Python/C++, lint, test-common, and OpenSSF passed. Master SonarQube Cloud independently remains Security E (`new_security_rating=5`, threshold `1`), while reliability, maintainability, duplication, and hotspot review pass; its predecessor had the same condition. The current user’s bounded acceptance was used only for this protected delivery. `FND-SONAR-0002` remains blocked, and no Parent gitlink or MRTS change is authorized. Source run: `20260720T113905Z-framework-pr35-36-integration-de98515c`.
- Current PR #59 integration / Aktuelle PR-#59-Integration: Protected squash merge of exact source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` produced Parent master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. `FND-PARENT-0030`, `FND-PARENT-0031`, and `FND-PARENT-0037` are now `verified`, not `closed`, and no longer their own release blockers: fresh non-skipped CI, CodeQL, Sonar Quality Gate, and zero-review/thread controls passed before merge; the exact resulting-master suite passed 57/57 evidence-integrity, 11/11 bilingual, shell-syntax, and diff controls. No Parent gitlink, Framework, or MRTS action occurred. The independently pre-existing `FND-SONAR-0001` master failure remains unaccepted and leaves aggregate delivery partial; it does not reopen these verified findings. Source run: `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`.
- Current PR #59 Sonar maintainability extension / Aktuelle PR-#59-Sonar-Maintainability-Erweiterung: `FND-SONAR-0006` is `verified`, not `closed`, on Parent master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. Its eight task-owned historical `CODE_SMELL` keys for source `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` are zero on both fresh PR evidence and the resulting-master key query, without NOSONAR, suppression, exclusion, scanner/gate change, false-positive disposition, or risk acceptance. The retained post-merge receipt records the focused controls; `FND-SONAR-0001` remains the separate unaccepted master Quality-Gate failure. Source run: `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`.
- Current PR #57 extension / Aktuelle PR-#57-Erweiterung: Parent PR #57 exact head `5f8949b1d98a98127b933e9f1d626b30e3291b59` was squash-merged as current Parent master `fde2e02a1cf2226f8e9106e663e05e9b2941357e`. In a clean detached exact-master worktree, 20 focused lifecycle/wiring/six-connector tests passed: foreign or missing run, connector, profile, integration-mode, and transaction identities fail closed on both first-byte and no-full-buffer paths, while the selected Apache legitimate control passes. `FND-PARENT-0027` is `verified`, not closed, and no longer a release blocker; FND-CROSS-0006 is separately verified on Framework master. All 14 master Actions workflows passed. The independent pre-existing Parent Sonar failure `FND-SONAR-0001` leaves aggregate delivery partial but does not reopen this verified finding. The Framework gitlink remains `efdbcbd98afeed0f39f8912ce1140aaa5742f507`; no Framework or MRTS Git action occurred. Source run: `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`.
- Current PR #61 integration / Aktuelle PR-#61-Integration: Protected Parent PR #61 head `c9b505a7a0f697318a57f42fe30493038ef03527` was squash-merged as current master `6bba8206de1bb598b40f76677943e86770b6992c`; the resulting tree equals the reviewed head and no Framework/MRTS gitlink changed. All 14 resulting-master GitHub Actions workflows pass, while exact SonarCloud check `88361885739` fails. PR #61's exact PR Quality Gate passed with zero new issues/hotspots and `0.0%` duplication; master now has 229 open Bug/Vulnerability records (220 vulnerabilities and 9 bugs), down from the retained 230. `FND-SONAR-0001` remains blocked P1 because the three unreviewed hotspots and E/E ratings remain; this integration is therefore `master_integration_partial`, with no hotspot review, Sonar-control change, Framework/MRTS action, or risk acceptance. Source run: `20260720T131144Z-pr61-master-integration-6bba820`.
- Superseded extension run / Ersetzter Erweiterungs-Run: `20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b`
- Current Parent security reconciliation / Aktueller Parent-Sicherheitsabgleich: protected PR #66 was merged as `cbd8385...`; follow-up PR #70 exact head `8d7f8b7283319528cf2c14479fc02399dd215825` passed 33 terminal PR checks, Sonar Quality Gate `OK`, and zero reviews/threads, then was normally squash-merged as final Parent master `f2376bb3e39ffbe9d36faca8bcd7397477eadd10`. Tree equality and all resulting GitHub Actions workflows passed. Its SHA-bound Sonar analysis `e04ce5bc-a9f7-44ce-bb13-8fe25c872d55` fixed/closed `AZ7b3dgOcO69wzd-_jHv` / `c:S3519`, leaving zero open Bugs, 220 Vulnerabilities, and three `TO_REVIEW` hotspots. Exact-master source/control/sink evidence classifies those hotspots `already_safe` with `no_change`; an external reviewed/safe disposition remains blocked pending a current explicit user decision. `FND-SONAR-0001` remains blocked P1; pending canonical imports `FND-SONAR-0007`/`0008` are fixed on Parent master but cannot receive directories. No Framework/MRTS or gitlink change occurred. Source run: `20260720T164715Z-parent-security-reconciliation-5a22cbf5`.
- Current task extension / Aktuelle Task-Erweiterung: Framework PR #33 was normally merged from exact head `e94029f5b893ef6a8efa118d21698426a43c82dd` as master `9a729226d2e040d07d7e7a4acebf201faf06ab37`. `FND-FRAMEWORK-0021` and `FND-FRAMEWORK-0022` are `verified` after their original fail-closed controls, all applicable master Actions, and CodeQL passed. Master SonarCloud independently remains failed with Security E and Reliability D; the historical `FND-SONAR-0002` acceptance names only PRs #24, #26, #27, and #29, so it does not automatically cover PR #33. Source runs: `20260719T211529Z-framework-python-313-master-migration-939e61b5`, `framework-pr-33-master-9a729226-20260719T221845Z`, and `framework-pr-33-master-sonar-20260719T221823Z`.
- Current PR #34 extension / Aktuelle PR-#34-Erweiterung: Framework PR #34 was normally merged from exact head `4fc22651ab2da652cbcaa7026258506d79b9af9c` as master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. `FND-CROSS-0006` is `verified` after its original foreign/missing-identity controls passed again on master. PR-head SonarQube Cloud passed; master SonarQube Cloud independently failed with Security E and Reliability D. The historical `FND-SONAR-0002` acceptance names only PRs #24, #26, #27, and #29, so the finding is `blocked` for current master-integration verification. Source run: `20260720T042405Z-framework-pr-34-master-integration-31a1528d`.
- Current PR #30 extension / Aktuelle PR-#30-Erweiterung: normal merge commit `a448d056ef98e745d8551c198b2e56d33fe38194` refreshed `fix/sonarcloud-quality-gate` with current Framework master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. `FND-FRAMEWORK-0023` is `fixed` on the verified PR head: SonarQube Cloud is Quality Gate `OK` with `new_duplicated_lines=0` and `new_duplicated_lines_density=0.0`; local legitimate controls and all terminal non-skipped hosted checks passed without analytical-control changes. The historical `FND-SONAR-0002` master backlog remains distinct and is not waived.
- Current PR #30 CI extension / Aktuelle PR-#30-CI-Erweiterung: `FND-FRAMEWORK-0024` is `fixed` on the same exact head. The unchanged CI-security suite passed all 69 tests, documentation checks passed, and all terminal non-skipped hosted checks succeeded. The original heading-contract failure was repaired without changing the checker, template, traceability control, or exception.
- Current PR #30 CodeQL extension / Aktuelle PR-#30-CodeQL-Erweiterung: `FND-FRAMEWORK-0026` is `verified`. The historical C/C++ CodeQL initialization HTTP 503 was a GitHub-hosted outage before analysis, not a Framework source defect. On exact head `a448d056ef98e745d8551c198b2e56d33fe38194`, CodeQL Actions job `88287878237`, Python job `88287878246`, and C/C++ job `88287878247` all succeeded. No CodeQL, workflow, quality-gate, or source workaround was used. The PR remains open; no Framework-master merge is authorized by this task. Source run: `20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef`.
- Current PR #30 security-scan tooling extension / Aktuelle PR-#30-Security-Scan-Tooling-Erweiterung: `FND-FRAMEWORK-0025` is `validated` after the Codex Security local-patch rank-input helper returned zero rows at exit code 0 for fourteen staged PR #30 files because its static EXCLUDED_DIRS excludes ci and tests. The exact staged Git inventory restored all fourteen files to the worklist, so the current scan has no unreviewed PR #30 code; the external-tool regression remains separately actionable and is not a release blocker for this PR.
- Current external extension observation / Aktuelle externe Erweiterungsbeobachtung: PR #27 merge commit `6de40c1714410241e917e9083ee890a82fb2fdbb` retained its historical Advanced-CodeQL upload rejection. Later external master `4dee26fcff988fd408bc7df577de772373c4b765` changed twelve reviewed Python `3.12.13` workflow values across eight workflows to `3.13` without a matching lock update; four hash-locked CI controls now fail closed. Historical `FND-GITHUB-0006` is retained in the local archive as current-user `accepted_risk`, not as a verified configuration resolution; `FND-FRAMEWORK-0021` owns the later CI regression.
- Source runs / Source-Runs: `20260716T193351Z-repository-full-assessment-0cb855ad`, `20260717T054830Z-native-runtime-evidence-6c0853fe`, `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`, `20260717T114213Z-feasibility-runtime-remediation-838d9adc`, `20260717T181659Z-codeql-action-4-37-1-batch-36346991`, `20260718T053406Z-pr-51-master-integration-546d9dc2`, `20260718T074759Z-codeql-xss-alerts-14-15-87ada941`, `20260718T080138Z-harden-workflow-permissions-e804be63`, `20260718T080726Z-fnd-parent-0018-4dd4e268`, `20260718T081034Z-github-scorecard-governance`, `20260718T082206Z-github-scorecard-governance-45b01572`, `20260718T075200Z-parent-evidence-integrity-ade378cf`, `20260718T081746Z-framework-common-structure-d6ee7cec`, `20260718T092308Z-fnd-framework-0005-pcre2-digest-e064e1d8`, `20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058`, `20260718T110742Z-fnd-parent-0028-mutable-action-images`, `20260718T083435Z-expand-framework-ci-security-32892be1`, `20260718T084030Z-expand-framework-ci-security-be8fb24d`, `20260718T075146Z-harden-temp-paths-97486abe`, `20260718T192214Z-framework-pr-resolution-20260718-b30403da`, `20260719T081017Z-framework-pr-resolution-20260719-840082e0`, `20260719T211529Z-framework-python-313-master-migration-939e61b5`, `framework-pr-33-master-9a729226-20260719T221845Z`, `framework-pr-33-master-sonar-20260719T221823Z`, `20260720T113905Z-framework-pr35-36-integration-de98515c`, `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`

- Current PR #59 S2083 extension / Aktuelle PR-#59-S2083-Erweiterung: FND-PARENT-0040 is closed after the 2026-07-26 current-path and retained-evidence revalidation. Its in-memory-only remediation f00eb11a25172959d50aa3e213fd1d7ace209599 is an ancestor of exact source b9b22cc36958ba506278f3aa3fbc1d383ea6a151, whose tree equals master; PR-wide zero issues covered the original pythonsecurity:S2083, the exact resulting-master suite passed, both retained hashes match, and the sole affected test file remains unchanged through current Parent HEAD. FND-SONAR-0001 remains the separate unaccepted master blocker. Source run: 20260720T141403Z-pr55-pr59-master-integration-8a0b8640.

- Current Parent PR #66 Sonar follow-up: exact Draft head
  91fea6d05850cc5aeef8ce7fb66a4123ac14e190 passed 30 terminal checks,
  SonarCloud check 88453362314, Quality Gate OK, and zero
  open/confirmed/reopened Bugs. Two Traefik c:S5489 keys and one HAProxy
  c:S3519 key are CLOSED/FIXED. Requested child records FND-SONAR-0007 and
  FND-SONAR-0008 are retained as complete EN/DE/JSON pending-import triplets
  because the canonical .codex/findings mount is read-only; FND-SONAR-0001
  carries their aggregate cross-reference and remains blocked by independent
  Parent-master conditions.

| ID | Priority | Repository | Category | Status | Release blocker | Title |
| -- | -------- | ---------- | -------- | ------ | --------------- | ----- |
| [FND-CROSS-0001](./FND-CROSS-0001/finding.md) | P0 | parent_and_framework | evidence_gap | validated | yes | Evidence freshness manifest contains stale entries and SHA mismatches |
| [FND-CROSS-0002](./FND-CROSS-0002/finding.md) | P0 | parent_and_framework | evidence_gap | validated | yes | Historical GitHub JSON receipts are not parseable canonical JSON |
| [FND-CROSS-0003](./FND-CROSS-0003/finding.md) | P1 | parent_and_framework | test_gap | blocked | yes | Current connector restart coverage is not retained |
| [FND-CROSS-0004](./FND-CROSS-0004/finding.md) | P1 | parent_and_framework | crs_gap | blocked | yes | Selected CRS profile routes remain unavailable for multiple connectors |
| [FND-CROSS-0005](./FND-CROSS-0005/finding.md) | P1 | parent_and_framework | release_blocker | blocked | yes | Release readiness remains blocked by unresolved evidence and quality gates |
| [FND-CROSS-0007](./FND-CROSS-0007/finding.md) | P2 | parent_and_framework | security_hardening | fixed | no | Parent and Framework task delivery did not bind origin effective push destination to the expected user repository |
| [FND-CROSS-0008](./FND-CROSS-0008/finding.md) | P1 | parent_and_framework | ci_failure | fixed | yes | #74 root fix is present; retained runtime/terminal artifact proof remains required |
| [FND-FRAMEWORK-0007](./FND-FRAMEWORK-0007/finding.md) | P1 | framework | lifecycle_defect | blocked | yes | Apache canonical full-lifecycle finalizer exits 77 after live traffic |
| [FND-FRAMEWORK-0009](./FND-FRAMEWORK-0009/finding.md) | P1 | framework | protocol_gap | blocked | yes | NGINX HTTP/2 route lacks protocol-correlated case execution |
| [FND-FRAMEWORK-0057](./FND-FRAMEWORK-0057/finding.md) | P1 | framework | ci_failure | fixed | yes | Framework #51 and Parent #126/#74 fixed the root cause; Parent runtime proof remains required |
| [FND-HOST-0003](./FND-HOST-0003/finding.md) | P1 | host_environment | lifecycle_defect | blocked | yes | NGINX non-root worker isolation cannot be proven in the current sandbox |
| [FND-HOST-0006](./FND-HOST-0006/finding.md) | P2 | host_environment | tooling | blocked | no | Task CPython 3.13.14 lacks _sqlite3, blocking local Coverage.py Cobertura XML validation |
| [FND-MRTS-0001](./FND-MRTS-0001/finding.md) | P1 | mrts | mrts_gap | blocked | yes | MRTS-related assurance remains limited to controlled external-copy evidence |
| [FND-MRTS-0002](./FND-MRTS-0002/finding.md) | P1 | mrts | test_failure | fixed | no | MRTS upstream-policy safety marker was absent from an enforced governance control |
| [FND-PARENT-0002](./FND-PARENT-0002/finding.md) | P2 | parent | maintainability | triaged | no | Parent ShellCheck diagnostics require scoped triage |
| [FND-PARENT-0003](./FND-PARENT-0003/finding.md) | P2 | parent | static_analysis_finding | triaged | no | Envoy and Traefik staticcheck diagnostics require disposition |
| [FND-PARENT-0005](./FND-PARENT-0005/finding.md) | P3 | parent | security_validated | fixed | no | #74 deadline fix is merged; current timeout-control replay remains required |
| [FND-PARENT-0006](./FND-PARENT-0006/finding.md) | P3 | parent | security_validated | validated | no | NGINX response handling can omit an over-limit suffix from inspection |
| [FND-PARENT-0007](./FND-PARENT-0007/finding.md) | P3 | parent | security_validated | validated | no | Traefik connector worker admission is unbounded |
| [FND-PARENT-0008](./FND-PARENT-0008/finding.md) | P2 | parent | compiler_warning | fixed | no | Draft PR #183 fixes Apache module_directives designated initializer; hosted/resulting-master evidence pending |
| [FND-PARENT-0009](./FND-PARENT-0009/finding.md) | P2 | parent | binary_hardening_gap | triaged | no | Apache binary hardening profile has stale RUNPATH and incomplete full-RELRO proof |
| [FND-PARENT-0010](./FND-PARENT-0010/finding.md) | P1 | parent | connector_gap | blocked | yes | HAProxy native capability remains non-promoted |
| [FND-PARENT-0011](./FND-PARENT-0011/finding.md) | P1 | parent | connector_gap | blocked | yes | Envoy native capability remains non-promoted |
| [FND-PARENT-0013](./FND-PARENT-0013/finding.md) | P1 | parent | security_candidate | blocked | yes | Traefik pathname UDS cleanup retains a same-UID final unlink race |
| [FND-PARENT-0014](./FND-PARENT-0014/finding.md) | P1 | parent | security_candidate | blocked | yes | Manifest cleanup retains a same-UID leaf-replacement deletion race |
| [FND-PARENT-0015](./FND-PARENT-0015/finding.md) | P1 | parent | security_candidate | blocked | yes | Traefik pathname UDS permits same-UID post-readiness endpoint redirection |
| [FND-PARENT-0020](./FND-PARENT-0020/finding.md) | P1 | parent | test_failure | fixed | no | #51 is reachable; current native middleware control remains required |
| [FND-PARENT-0021](./FND-PARENT-0021/finding.md) | P2 | parent | storage_cleanup | blocked | no | Storage-budget finalization cannot clean task-owned validation and build artifacts |
| [FND-PARENT-0026](./FND-PARENT-0026/finding.md) | P2 | parent | security_hardening | fixed | no | Runtime path policy trusts caller-controlled project roots as confinement anchors |
| [FND-PARENT-0028](./FND-PARENT-0028/finding.md) | P2 | parent | security_hardening | triaged | no | SHA-pinned Parent scanner actions retain mutable Docker image dependencies |
| [FND-PARENT-0042](./FND-PARENT-0042/finding.md) | P1 | parent | ci_failure | blocked | yes | Parent runtime-component cache binds the NGINX release digest to a different tag archive |
| [FND-PARENT-0043](./FND-PARENT-0043/finding.md) | P2 | parent | security_validated | blocked | no | Apache intervention buffers require request-owned copies before native cleanup |
| [FND-PARENT-0050](./FND-PARENT-0050/finding.md) | P1 | parent | security_hardening | fixed | yes | #74 immutable source boundary is present; full producer/cross-repository validation remains |
| [FND-PARENT-0052](./FND-PARENT-0052/finding.md) | P1 | parent | dependency_risk | fixed | yes | #74 immutable EXPAT path is present; full producer validation remains |
| [FND-PARENT-0053](./FND-PARENT-0053/finding.md) | P1 | parent | ci_failure | fixed | yes | #74 literal PCRE2 hash path is present; terminal producer gate remains |
| [FND-PARENT-0054](./FND-PARENT-0054/finding.md) | P1 | parent | evidence_gap | in_progress | no | Historical bounded runtime-log diagnostic is not reachable from current master; no equivalent current control is evidenced |
| [FND-PARENT-0055](./FND-PARENT-0055/finding.md) | P1 | parent | test_failure | blocked | no | Referenced paths lack authorized removal or replacement provenance |
| [FND-PARENT-0056](./FND-PARENT-0056/finding.md) | P1 | parent | ci_failure | fixed | yes | #74/#126 source and gitlink evidence exists; strict producer replay remains |
| [FND-PARENT-0057](./FND-PARENT-0057/finding.md) | P1 | parent | security_candidate | in_progress | yes | Draft Parent PR #74 expands PR-controlled workflow output at a template-to-shell boundary |
| [FND-PARENT-0058](./FND-PARENT-0058/finding.md) | P1 | parent | test_failure | fixed | yes | #74 port-plan change remains; full matrix/hosted replay remains |
| [FND-PARENT-0059](./FND-PARENT-0059/finding.md) | P1 | parent | security_validated | fixed | yes | #74 locking fix remains; retained target receipt and hosted run remain |
| [FND-PARENT-0060](./FND-PARENT-0060/finding.md) | P1 | parent | lifecycle_defect | fixed | yes | Full-matrix batch scheduler is not work-conserving at its concurrency cap |
| [FND-PARENT-0061](./FND-PARENT-0061/finding.md) | P1 | parent | lifecycle_defect | fixed | yes | Worker-wrapper death before FIFO completion can stall the full-matrix scheduler |
| [FND-PARENT-0062](./FND-PARENT-0062/finding.md) | P1 | parent | ci_failure | validated | yes | Python workflow inventory contract references a removed verified-report governance job |
| [FND-PARENT-0063](./FND-PARENT-0063/finding.md) | P3 | parent | security_validated | validated | no | Normal runtime provisioning executes release-selected mutable upstream source |
| [FND-PARENT-0064](./FND-PARENT-0064/finding.md) | P1 | parent | lifecycle_defect | verified | no | Resulting master APR harness passes; broader live Apache sequence remains before closure |
| [FND-PARENT-0065](./FND-PARENT-0065/finding.md) | P2 | parent | security_validated | fixed | no | #175 safe-file containment and regressions exist; current resulting-master control remains |
| [FND-PARENT-0066](./FND-PARENT-0066/finding.md) | P2 | parent | evidence_gap | fixed | no | Invalid full-matrix control evidence could retain pass status and permit evidence-only reclassification |
| [FND-PARENT-0067](./FND-PARENT-0067/finding.md) | P2 | parent | lifecycle_defect | validated | no | Apache name_for_debug uses an unowned strdup allocation across configuration lifecycle |
| [FND-PARENT-0068](./FND-PARENT-0068/finding.md) | P3 | parent | security_validated | in_progress | no | Apache cleanup runners execute compiler output from predictable shared temporary trees |
| [FND-PARENT-0069](./FND-PARENT-0069/finding.md) | P2 | parent | compiler_hardening_gap | validated | no | Apache mod_security3.c has a baseline-identical GCC C17 Werror failure group |
| [FND-PARENT-0070](./FND-PARENT-0070/finding.md) | P1 | parent | build_defect | fixed | yes | Merged repair awaits fresh resulting-master APXS/DSO/HTTP validation |
| [FND-PARENT-0071](./FND-PARENT-0071/finding.md) | P1 | parent | runtime_defect | fixed | yes | Merged repair awaits fresh resulting-master live start/readiness/403/SIGUSR1 validation |
| [FND-PARENT-0072](./FND-PARENT-0072/finding.md) | P3 | parent | sonarqube_finding | fixed | no | PR Sonar repair is merged; direct resulting-master Sonar analysis/issues remain required |
| [FND-PARENT-0073](./FND-PARENT-0073/finding.md) | P1 | parent | test_failure | verified | no | #182 focused controls and resulting PR evidence are retained; full Framework suite remains blocked |
| [FND-PARENT-0075](./FND-PARENT-0075/finding.md) | P1 | parent | ci_failure | not_applicable | no | Historical PR #202 Secret-scanning heuristic is superseded after verified replacement PR #213 merged |
| [FND-PARENT-0046](./FND-PARENT-0046/finding.md) | P2 | parent | ci_failure | triaged | no | Python version updater workflow rejects valid Python 3.14 patch versions |
| [FND-PARENT-0036](./FND-PARENT-0036/finding.md) | P2 | parent | sanitizer_finding | fixed | no | Native Oracle append-error path double-frees a request body |
| [FND-SONAR-0001](./FND-SONAR-0001/finding.md) | P1 | parent | sonarqube_finding | blocked | yes | Parent SonarQube quality gate remains failed on security rating and unreviewed hotspots |
| [FND-SONAR-0004](./FND-SONAR-0004/finding.md) | P1 | parent | sonarqube_finding | blocked | yes | SonarQube Cloud project analyzes read-only Framework and MRTS trees |
| [FND-SONAR-0009](./FND-SONAR-0009/finding.md) | P1 | framework | sonarqube_finding | blocked | yes | Framework PR #39 Model-1 same-repository coverage workflow is locally fixed and awaits SonarQube Cloud project configuration |
| [FND-SONAR-0016](./FND-SONAR-0016/finding.md) | P1 | parent | maintainability | in_progress | yes | Parent Draft PRs retain SonarQube Cloud new-code finding or duplication follow-ups |
| [FND-SONAR-0019](./FND-SONAR-0019/finding.md) | P1 | parent | sonarqube_finding | fixed | no | PR #150 Traefik result serialization Sonar blockers are fixed on its exact Draft head |
| [FND-SONAR-0022](./FND-SONAR-0022/finding.md) | P1 | parent | security_validated | fixed | yes | Block-status generator permits CLI-selected output to escape its selected root |
| [FND-SONAR-0023](./FND-SONAR-0023/finding.md) | P2 | parent | maintainability | verified | no | Native ModSecurity oracle result writer exceeds Sonar parameter-count threshold |
| [FND-SONAR-0024](./FND-SONAR-0024/finding.md) | P2 | parent | maintainability | verified | no | Native ModSecurity oracle main exceeds Sonar Cognitive Complexity threshold |
| [FND-SONAR-0025](./FND-SONAR-0025/finding.md) | P2 | parent | security_candidate | verified | no | Lighttpd lifecycle fixture input lacks verified runtime-root containment |
| [FND-SONAR-0026](./FND-SONAR-0026/finding.md) | P2 | parent | maintainability | verified | no | PR #198 test bootstrap uses an optimization-sensitive composite assert |
| [FND-SONAR-0027](./FND-SONAR-0027/finding.md) | P2 | parent | maintainability | verified | no | NGINX connector contains sixteen current SonarQube Cloud maintainability findings |
| [FND-SONAR-0028](./FND-SONAR-0028/finding.md) | P2 | parent | maintainability | verified | no | Common runtime historical `c:S3776` is `FIXED/CLOSED` on resulting master after PR #221 |
| [FND-SONAR-0029](./FND-SONAR-0029/finding.md) | P1 | parent | sonarqube_finding | verified | no | Common scripts historical `pythonsecurity:S8705` is `FIXED/CLOSED` on resulting master after PR #221 |
| [FND-SONAR-0030](./FND-SONAR-0030/finding.md) | P2 | parent | maintainability | fixed | no | #226 merged as d7dfbc5 with 33 checks; direct current Sonar-key readbacks remain required |
| [FND-SONAR-0031](./FND-SONAR-0031/finding.md) | P2 | parent | maintainability | verified | no | CI evidence's fifteen original `python:S3776` rows and duplicate block are `FIXED/CLOSED` on resulting master after PR #225 |

## Deduplication and boundaries

- Historical RFA IDs are retained as source mapping in `backlog.json`; they are not second local findings.
- Historical generic RFA-06 was not duplicated because current runtime evidence supersedes its “no native evidence” statement. Its remaining independent gaps are represented by specific canonical findings.
- `P-DISC-09-02` and TODO/FIXME counts alone were not promoted because retained evidence does not support a reportable finding disposition.
- MRTS-related records remain `mrts_external_read_only`; no finding file authorizes an MRTS change.
