# FND-SONAR-0016 — Parent Draft PRs have SonarQube Cloud new-code findings or duplication

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-SONAR-0016` |
| Category | `maintainability` |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / validated |
| Status / feasibility | in_progress / feasible_now |
| Release blocker / security relevance | yes / no |

## Summary

This aggregate retains exact-head SonarQube Cloud evidence for independently
remediable Parent Draft PR Quality-Gate failures. Its historical #74 and #138
evidence remains independently active. Draft PR #151, Draft PR #152, Draft PR
#153, Draft PR #154, Draft PR #155, Draft PR #157, Draft PR #158, and Draft
PR #159 have
clean task-owned exact-head remediation observations. Draft PR #160 instead has
a terminal exact-head blocker: three task-owned OPEN python:S1481 findings in
its Traefik start-wiring checker despite a green Quality Gate and zero new-code
duplication. Initial Draft PR #156 exact-head evidence
had seven task-owned OPEN `python:S3415` findings; its retained successor exact
head `59ff4d5bbb6e278d93c0b965096e842b77f446bb` has a bounded zero-issue
Draft-PR result. Draft PR #157's retained exact head
`3055790e88e6b962bdffdabadccee1de2ce59355` similarly has a bounded zero-issue
result for the original Parent `python:S1192` receipt
`AZ9cRyW7HhV2CayPTPuq`. None of these observations closes this aggregate or makes a
master or global-`652/zero`-backlog claim.

## Observed and expected behavior

Twenty-one task-owned `python:S3415` findings concern assertion diagnostic
argument order; one task-owned `python:S1192` finding concerns the repeated
immutable-commit expression. The single duplicate block is transaction-ID
boundary coverage present in both a helper-local test and the dedicated Parent
regression test. Historical PR #152 head `ba8d` had `S1192`; its exact
follow-up head `c9c011117bd4d9c910aa4d1a767916d50c9bd26a` is clean in the
retained PR receipt. Draft PR #153 remediates `S1066` receipt
`AZ9cRy9OHhV2CayPTP4Z` at exact head
`c5a45dff07ceb11eb84bc7854e6d7ca034dc9bc4`. Draft PR #154 has three clean
task-owned `S1192` receipts `AZ9cRyqOHhV2CayPTPzr`,
`AZ9cRyqOHhV2CayPTPzq`, and `AZ9cRyZWHhV2CayPTPwQ` at exact head
`60a13292c9173a760f94672c6855a97099d1fcc2`. Draft PR #155 has four clean
task-owned receipts `AZ98JczJLJyjbmyNA5LW`, `AZ98JczJLJyjbmyNA5LO`,
`AZ98JczJLJyjbmyNA5LS`, and `AZ98JczJLJyjbmyNA5LU` at exact head
`0e980f6c2a46ef92f14a007bc8d0c6d538885192`. Initial Draft PR #156 exact
head `e2b1370caa32e621ada4ce96ad03f603904cee49` has seven task-owned OPEN
`python:S3415` MAJOR/CODE_SMELL keys
`AZ-pRyPD--pWpbX22nGu` through `AZ-pRyPD--pWpbX22nG0` in
`tests/test_apache_phase4_response_regression_wiring.py`. Its Quality Gate was
`OK` and new duplicated lines/density were `0`/`0.0`, but that did not meet
the exact-head no-open-finding criterion. Its successor exact head
`59ff4d5bbb6e278d93c0b965096e842b77f446bb` has zero direct Sonar PR issues,
Quality Gate `OK`, new duplicated lines `0`, new-duplication density `0.0`,
and 39 terminal GitHub checks. This is a bounded Draft-PR result; a later head
requires a new exact-head readback without changing SonarQube Cloud policy.

## Impact and affected scope

The green Quality Gate alone does not satisfy the user-required delivery
criterion. The independently remediable #151, #152, #153, #154, and #155
portions are clean at their exact Draft heads only. Affected Parent paths include the
runtime component provisioner, report generators/checkers, test modules, the
helper-local HAProxy HTX test, and `common/runtime/http_authorization_service.c`
(`parse_cli` and `parse_cli_value_option`). The retained #153 receipt and the
three clean #154 receipt IDs plus four clean #155 receipt IDs prove their
remediated rule/key observations but
do not state prior source locations, so this record does not infer any.
The initial #156 receipt locates its seven task-owned `python:S3415` findings
only in the named Apache Phase-4 source-wiring test. Its retained successor
receipt records zero direct PR issues at exact head
`59ff4d5bbb6e278d93c0b965096e842b77f446bb`, but is limited to the unmerged
Draft PR and does not establish a default-branch or global result. Framework,
MRTS, and the Parent/Framework gitlink are unaffected.
Framework, MRTS, and the Parent/Framework gitlink are unaffected.

## Evidence and reproduction

Retained evidence is
`.codex/runs/20260726T095800Z-pr74-sonar-zero-findings/evidence/sonar-pr74-pre-fix.md`
with SHA-256
`4905ae4e2a027f37255261756dfea0cf2db66513460ecbe8a6d7d9a88a6c1b55`.
The observed SonarQube Cloud PR endpoints were the OPEN/CONFIRMED issues
search, the new-duplication measures, the file-level component tree, and the
duplication-block endpoint. They returned exit code 0 at 2026-07-26T09:58:00Z.

## Root cause and remediation

The test assertions presented expected values before actual values, a compiled
pattern's literal was repeated, and equivalent HAProxy transaction-ID coverage
was duplicated. Commit `6809e348ad043bf3fcfd9b90d963882cc2fb2cb2` puts actual
values first, reuses `FULL_GIT_COMMIT_ID`, and retains that boundary coverage
only in `tests/test_haproxy_htx_transaction_id.py`. No rule, Quality Gate,
exclusion, suppression, coverage threshold, scanner configuration, Framework,
MRTS, or gitlink changed.

For initial PR #156, the seven newly added unittest source-wiring assertions
put expected values before actual values. The retained successor receipt shows
that those task-owned `python:S3415` issues are absent at exact head
`59ff4d5bbb6e278d93c0b965096e842b77f446bb`; its scope remains a bounded Draft
PR result. Any later head must repeat focused controls and exact-head
SonarQube Cloud/GitHub readback without changing a Sonar rule, Quality Gate,
exclusion, suppression, coverage threshold, scanner configuration, Framework,
MRTS, or a gitlink.

## Validation and controls

Local controls passed: focused Python suite (66 tests), HAProxy helper suite
(8 tests), `make check-ci-security-contract`, `make check-bilingual-docs`, and
`git diff --check`. The dedicated Parent transaction-ID regression remains the
legitimate control: it accepts the maximum native length and rejects one byte
more. The immutable-Git-commit suite preserves the 40-to-64 hexadecimal
boundary.

## Dependencies, residual risk, and history

The exact-head SonarQube Cloud readback for
`6809e348ad043bf3fcfd9b90d963882cc2fb2cb2` reports zero OPEN/CONFIRMED
findings, zero new duplicated lines, and 0.0% new-code duplication. The
retained post-fix receipt is
`.codex/runs/20260726T095800Z-pr74-sonar-zero-findings/evidence/sonar-pr74-post-fix.md`,
SHA-256 `63312dd2153c76f4a306854c5cedc13d264ee5729f192d197a7ebffa1c8f59bb`.
That historic head was `verified`, not closed. The current successor is now
`in_progress`: the strict runtime-evidence producer, the new exact-head
SonarQube Cloud readback, and the remaining protected-integration checks are
separate prerequisites. Related records are `FND-PARENT-0053`,
`FND-PARENT-0054`, `FND-PARENT-0057`, and `FND-PARENT-0058`.

### Current exact-head revalidation — 2026-07-26

The normal Parent-master update produced #74 head
`193fb56c3613b1e14292a1a7fc05371b489fbd3d`. Its new SonarQube Cloud analysis
still had 0.0% new-code duplication but exposed one OPEN `python:S3415` issue
at `tests/test_runtime_env_snapshot_contract.py:72`: the unready-NGINX control
used expected-first assertion arguments. The one-line behavior-preserving
actual-first correction was committed normally as
`77bd39e64194cf5e6d221d874d9c6924549711eb`.

The direct test passed 8 cases and the relevant focused Parent suite passed
158 cases. The completed exact-head SonarQube Cloud analysis for `77bd39e`
reports zero OPEN/CONFIRMED issues, zero new-code violations, and 0.0% new-code
duplication. Retained bounded receipt:
`.codex/runs/20260726T163833Z-pr74-s3415-assertion-order/evidence/pr74-s3415-assertion-order.md`
(SHA-256 `69c55c5bfd7574e57eed8e2289ccb42d64988543181a621b221d7b3874777b7e`).
This re-verifies the finding without a scanner, gate, suppression, Framework,
MRTS, or Gitlink change. The still-running report-governance producer and
protected integration remain independent PR #74 controls.

### Current Draft-PR #74 hosted follow-up — 2026-07-26T18:56:07Z

Read-only hosted observation for exact Draft PR #74 head
`9046c69cc49145e70b18b5fc86a7c3fe67926d5a` now reports Quality Gate `ERROR`:
`new_security_rating` is `3` against error threshold `1`. The SonarQube Cloud
issues endpoint returned 19 OPEN task-owned findings: two `python:S1192`, one
`python:S1172`, two `python:S3776`, thirteen `python:S3415`, and one
`pythonsecurity:S8707` VULNERABILITY key `AZ-fw-Tf7_zRPd2N8_S2` at
`ci/evidence/reports/stage-verified-full-matrix-evidence.py:65`.
New-code duplication remains `0.0%`.

The retained external receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260726T185607Z-pr74-fast-validation-hosted-followup/evidence/hosted-observation.md`,
2978 bytes, SHA-256
`5c64b4fe03ed670b0d2c25c58c2f770b59ae53bab10851ced35bd9012117d956`.
`FND-PARENT-0057` separately tracks the plausible workflow-template-injection
and S8707 correction; `FND-PARENT-0058` separately tracks full-matrix
port-range evidence reliability. PR #74 remains Draft; no rule, Quality Gate,
exclusion, suppression, false-positive disposition, Framework, MRTS, Gitlink,
close, merge, or delivery action occurred.

### Current Draft PR #138 exact-head Quality-Gate failure — 2026-07-27

Exact Draft PR #138 head
`e522e43f0957368853772d747a0ffaa38ba76615` has all observed GitHub checks
successful, but its SonarQube Cloud Quality Gate is `ERROR`. The concrete
failure is 20 new duplicated lines and `5.649717514124294%` new-code
duplication against the `3%` threshold. The same exact-head analysis reports
one OPEN `python:S3776` key `AZ-lYOLSGYV1PN-Q1gW4` at
`ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py:2261`:
`command_summary` has cognitive complexity 16 where 15 is allowed.

The 20 duplicated lines are five equivalent four-line quote-state conversions
in the report generators. The contained remediation is to use one
behavior-preserving non-nested quote-state expression per location and to move
the new runtime-status decision into a small pure helper. The quote invariant
is exact: a matching quote closes, no current quote opens, a different quote
remains active, and non-quote characters retain state. No security control,
Sonar rule, Quality Gate, exclusion, suppression, Framework, MRTS, Gitlink,
Ready-for-review, merge, or external disposition has changed.

Retained bounded observation:
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/evidence/pr138-quality-gate-observation.json`,
SHA-256
`96299299690bf6d83a9348e6bea5d42e2f13c795c57bf8cedbfa37c48fedca24`.
The successor must rerun focused parser/report controls, documentation and
diff checks, then receive a new exact-head SonarQube Cloud readback before
this active portion can become fixed or verified.

### Corrected exact-head verification for Draft PR #138 — 2026-07-27

The corrective Draft PR #138 head
`3e4a8602e0b989cea24534e5f9ac09ed651a5b51` has a public exact-head
SonarQube Cloud Quality Gate `OK`, zero OPEN/CONFIRMED issues, five new
duplicated lines, and 1.2987012987012987% new-code duplication against the
three-percent threshold. The predecessor `python:S3776` receipt
`AZ-lYOLSGYV1PN-Q1gW4` is absent from that issue readback.

The retained bounded receipt is
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/evidence/pr138-corrected-head-observation.json`,
SHA-256
`b66821c44728165c93bcb539e347eea9ab8bd4be2c4251ddc747968565391bb2`.
This verifies the #138 corrective portion at Draft-PR level only. The
aggregate remains `in_progress` because its historical #74 and protected
integration dependencies are independent; no policy, suppression, exclusion,
Framework, MRTS, Gitlink, Ready-for-review, merge, or external disposition
changed.

### Corrected exact-head verification for Draft PR #141 — 2026-07-27

The first Draft PR #141 head introduced one OPEN `c:S5955` receipt
`AZ-lnrThdnI7fSwu83t-` in the private Common error-map lookup loop despite a
Quality Gate `OK` and zero new duplicated lines. A normal one-file C17 follow-
up moved the loop-index declaration into the `for` initializer. Its corrected
exact head `89bb198bb3a94e2a7d77a78fba8436cf01985b18` now has all completed
hosted checks successful, SonarQube Cloud Quality Gate `OK`, zero
OPEN/CONFIRMED issues, zero new duplicated lines, and 0.0% new-code
duplication. The predecessor receipt is absent from the exact-head issue
readback.

The retained bounded receipt is
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/evidence/pr141-corrected-exact-head-observation.json`,
SHA-256 `f505b3b01c20e2b16d50b5a4e6a204b5a954eb15fd9a834538032d49cf7d9865`.
This verifies only the #141 corrective portion at Draft-PR level. The
aggregate remains `in_progress` because its historical #74 and protected
integration dependencies are independent; no policy, suppression, exclusion,
Framework, MRTS, Gitlink, Ready-for-review, merge, master, or external issue
disposition changed.

### Exact-head Quality-Gate failure for Draft PR #144 — 2026-07-27

Exact Draft PR #144 head `30bd39faf4214dd27f5fd095def71b07d97ccd3b` has all
observed non-Sonar completed checks successful, but SonarQube Cloud Quality
Gate `ERROR`: new-code duplication density is 8.6% against the 3% threshold.
The same readback reports two OPEN `python:S1192` receipts
`AZ-l0E9Sjq1bd7qgEUwj` and `AZ-l0E9Sjq1bd7qgEUwk` in the newly extended NGINX
source-contract checker. The component/duplication endpoints identify three
new duplicated lines in each NGINX event-emitter file and a remaining 22-line
serialization/write clone between `access.c:99` and `log.c:75`.

The retained bounded observation is
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/evidence/pr144-quality-gate-observation.json`,
SHA-256 `3848cfb5ff41491a7fd0b212f00ea72328f813bc68f7d07ce4716571ff1dcd88`.
A normal task-owned corrective commit is required. No Sonar policy, Quality
Gate, suppression, exclusion, Framework, MRTS, Gitlink, Ready-for-review,
merge, master, or external issue-disposition action occurred.

### Exact second-head follow-up for Draft PR #144 — 2026-07-27

The normal corrective #144 head
`116a50d0abd7c36471868e7b77d533d1a78ebda5` has all completed hosted checks
successful, SonarQube Cloud Quality Gate `OK`, zero new duplicated lines, and
0.0% new-code duplication. Its candidate total is 1,969 duplicated lines,
not a claim about unmerged `master`. It is nevertheless not a clean verified
head: the exact issue readback reports one new task-owned `python:S1192`
receipt `AZ-l_JOYhdUH4Iu4ldmS` at
`ci/checks/connectors/nginx/check-nginx-common-adoption.py:68`, where the
literal `"msconnector/event_jsonl.h"` is used three times.

The retained bounded observation is
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/evidence/pr144-second-head-observation.json`,
SHA-256 `8f95776f74a267078fbec9a3bff27db0d247b89437195daf07c113c4bde258c3`.
The smallest normal third correction introduces one local checker constant and
preserves every contract assertion. Its focused adoption check and diff check
passed locally; it still requires its own commit, exact head, hosted checks,
and Sonar readback. No Sonar policy, Quality Gate, suppression, exclusion,
Framework, MRTS, Gitlink, Ready-for-review, merge, master, or external
disposition action occurred.

### Exact third-head verification for Draft PR #144 — 2026-07-28

The normal third #144 head
`650c08a30254072883fc78379a2873f1b57342e1` has local, origin, and Draft-PR
head equality. All completed hosted checks passed (configured skips remained
skipped). Its direct exact-head SonarQube Cloud readback reports Quality Gate
`OK`, zero OPEN/CONFIRMED issues, zero new duplicated lines, and 0.0% new-code
duplication. Its candidate total is 1,969 duplicated lines, not a claim about
unmerged `master`.

The retained bounded observation is
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/evidence/pr144-third-head-observation.json`,
SHA-256 `4d17ec656467198ae5d5a9b360ce91cdd8c08cfb3dbb16a2faab899b0af7bca3`.
This verifies the #144 portion at Draft-PR level; it removes the active #144
checker follow-up from this aggregate. The aggregate remains `in_progress`
because its historical #74 and #138 / broader-backlog dependencies are
independent. No Ready-for-review, merge, master update, Sonar policy,
suppression, exclusion, Framework/MRTS source, Gitlink, or external issue
disposition action occurred.

### Exact-head verification for Draft PR #151 — 2026-07-28

An intermediate exact Draft PR #151 head
`ea52192f30ca091f9389eb10c87e9a99e2bbab4c` had one OPEN `c:S3776` receipt
`AZ-ovroGM5o_ow3fPM0Z` at
`common/runtime/http_authorization_service.c`: `parse_cli` measured cognitive
complexity `29` where `25` is allowed, despite Quality Gate `OK`. The normal
task-owned correction extracted the value-option handling into the private
`parse_cli_value_option` helper without a Sonar rule, Quality Gate,
suppression, exclusion, or scanner-configuration change.

The final all-check retained external run is
`pr151-verified-16c3-20260728` at
`/var/tmp/codex/ModSecurity-conector/pr151-verified-16c3.W45TRL`; its
`manifest.json` and `SHA256SUMS` are present. It binds exact Draft PR #151
head `16c3aa5d87e603de718d4a94a6d57afae159fc53` to these receipts:

- `issues.json` — SHA-256
  `bd5ffd42633f61ec96f7c97607987808dc670616f3adee47ea593cce85eb5660` —
  zero PR issues.
- `quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `measures.json` — SHA-256
  `1857134d543bbbde04ad8ec14d8a1ed108d5140dd14d2466f2b1091bfb60d4eb` —
  zero bugs, vulnerabilities, code smells, new duplicated lines, and
  new-duplication density `0.0`.
- `pr.json` — SHA-256
  `b8bf4c5c1d26faae3b49afd060e1e8c1c69cf6410cff178d17a5e9c63a11b517` —
  PR #151 remains Draft and unmerged.
- `check-runs.json` — SHA-256
  `70a80c0f452d91c8ddcbe20160b2aa0dcb0deaa2e812286da6ceec66156925ba` —
  successful `SonarCloud Code Analysis` is bound to that SHA; all 39 check
  runs are complete (33 `success`, six scope-justified `skipped`, and zero
  unfinished).

This verifies only the task-owned #151 correction at Draft-PR level. The
aggregate remains `in_progress` because historical #74, #138, and the broader
backlog are independent. No Ready-for-review, merge, master update,
Framework/MRTS source, Gitlink, or external issue-disposition action occurred.

### Exact-head verification for Draft PR #152 — 2026-07-28

Historical Draft PR #152 head `ba8d` had `S1192`. Its exact task-owned
follow-up head `c9c011117bd4d9c910aa4d1a767916d50c9bd26a` is retained as
`pr152-verified-c9c-20260728` at
`/var/tmp/codex/ModSecurity-conector/pr152-verified-c9c.5uh08S`. The receipt's
`SHA256SUMS` validates every listed payload and binds the final head to these
observations:

- `issues.json` — SHA-256
  `55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e` —
  zero OPEN/CONFIRMED PR issues.
- `quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `measures.json` — SHA-256
  `251b5f4d3f6cf6e9c121901f237fbe97767f07107346fe9bbab9871ce2166147` —
  new duplicated lines `0` and new-duplication density `0.0`.
- `pr.json` — SHA-256
  `aa1d32b45d8ab369d0b3f759603826e3ef9af32df1f0f2a1402c8511a3da639b` —
  PR #152 is Draft and `OPEN`.
- `check-runs.json` — SHA-256
  `ad06ccea830f88a90b1355ad603a3437567a659af88482604d044f69c8e27214` —
  successful `SonarCloud Code Analysis` is bound to that SHA; all 39 checks
  are completed: 33 `success`, zero `neutral`, and six scope-justified
  `skipped`.

This verifies only the task-owned #152 correction at Draft-PR level. The
aggregate remains `in_progress` because PR #152 is unmerged and the global
`652/zero` goals, historical #74, #138, and broader-backlog dependencies
remain ongoing. No Ready-for-review, merge, master update, Sonar policy,
suppression, exclusion, Framework/MRTS source, Gitlink, or external
issue-disposition action occurred.

### Exact-head verification for Draft PR #153 — 2026-07-28

Draft PR #153 remediates `S1066` receipt `AZ9cRy9OHhV2CayPTP4Z`. Its exact
task-owned head `c5a45dff07ceb11eb84bc7854e6d7ca034dc9bc4` is retained as
`pr153-verified-c5a-20260728` at
`/var/tmp/codex/ModSecurity-conector/pr153-verified-c5a.ivXh4u`. The receipt's
`SHA256SUMS` validates every listed payload and binds the final head to these
observations:

- `issues.json` — SHA-256
  `55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e` —
  zero OPEN/CONFIRMED PR issues.
- `quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `measures.json` — SHA-256
  `d6dae5e41266c5b92887eb2700e4bb7a10ee3983ffa13bd138b043e28727a10c` —
  new duplicated lines `0` and new-duplication density `0.0`.
- `pr.json` — SHA-256
  `25ce8a7d818385c9901ad6bb2b3e07425c6b4ce20ad747f506f811dd5784b4fe` —
  PR #153 is Draft and `OPEN`.
- `check-runs.json` — SHA-256
  `05e2102286a6ccc4a16ed67c644a814985280f317e4b1eb2fb2907d49c0af713` —
  successful `SonarCloud Code Analysis` is bound to that SHA; all 39 checks
  are completed: 33 `success`, zero `neutral`, and six scope-justified
  `skipped`.

The retained final receipt establishes the remediated rule/key and exact-head
result but not an unrecorded prior source location, so no source path is
claimed. This verifies only the task-owned #153 correction at Draft-PR level.
The aggregate remains P1 `in_progress` because PR #153 is Draft, `OPEN`, and
unmerged, while the global `652/zero` goals, default branch, historical #74,
#138, and broader-backlog dependencies remain ongoing. No Ready-for-review,
merge, master update, Sonar policy, suppression, exclusion, Framework/MRTS
source, Gitlink, or external issue-disposition action occurred.

### Exact-head verification for Draft PR #154 — 2026-07-28

Draft PR #154 has exact head
`60a13292c9173a760f94672c6855a97099d1fcc2` and remains Draft and `OPEN`.
The retained all-check run `pr154-verified-60a-20260728` is at
`/var/tmp/codex/ModSecurity-conector/pr154-verified-60a.Hr5Ki8`. Its
`SHA256SUMS` validates every listed payload and binds the exact head to three
clean task-owned `S1192` receipts `AZ9cRyqOHhV2CayPTPzr`,
`AZ9cRyqOHhV2CayPTPzq`, and `AZ9cRyZWHhV2CayPTPwQ`:

- `issues.json` — SHA-256
  `55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e` —
  zero OPEN/CONFIRMED Sonar PR issues.
- `quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `measures.json` — SHA-256
  `a2681deb88fa4c94405b4dfd6502dbea3f2b5d73e53db76d4fb4022793f85e46` —
  new duplicated lines `0` and new-duplication density `0.0`.
- `pr.json` — SHA-256
  `264c0e2044414806bafcf18d0f5101663c366a2b399a8bcc5ea0efb7ff9b9b4b` —
  PR #154 is Draft and `OPEN`.
- `check-runs.json` — SHA-256
  `c950290fceb249aefbc3abf43c3cfa9f2cd3cb4745ee9fb59c1c7299b0e3415f` —
  all 39 exact-SHA GitHub checks are terminal, including successful
  `SonarCloud Code Analysis`.

This verifies only the task-owned #154 corrective portion at Draft-PR level.
The aggregate remains P1 `in_progress` because PR #154 is Draft, `OPEN`, and
unmerged, while the global `652/zero` goals, default branch, historical #74,
#138, and broader-backlog dependencies remain active. If the #154 head
changes, repeat exact-head Sonar issue, Quality Gate, measure, and GitHub-check
readback before reliance. No Ready-for-review, merge, master update, Sonar
policy, suppression, exclusion, Framework/MRTS source, Gitlink, or external
issue-disposition action occurred.

### Exact-head verification for Draft PR #155 — 2026-07-28

Draft PR #155 has exact head
`0e980f6c2a46ef92f14a007bc8d0c6d538885192` and remains Draft, `OPEN`, and
unmerged. The retained all-check run `pr155-verified-0e9-20260728` is at
`/var/tmp/codex/ModSecurity-conector/pr155-verified-0e9.NkGL9s`. Its
`SHA256SUMS` validates every listed payload and binds the exact head to four
clean task-owned receipts `AZ98JczJLJyjbmyNA5LW`, `AZ98JczJLJyjbmyNA5LO`,
`AZ98JczJLJyjbmyNA5LS`, and `AZ98JczJLJyjbmyNA5LU`:

- `issues.json` — SHA-256
  `55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e` —
  zero OPEN/CONFIRMED Sonar PR issues.
- `quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `measures.json` — SHA-256
  `c9cce6fe993a71e63bda0bdd86fdae4a7ab9214956f0ca6c67282b3ecc9d1135` —
  new duplicated lines `0` and new-duplication density `0.0`.
- `pr.json` — SHA-256
  `ff575f3731af7268d426413e3067011da2a0889a6820ce6ef6fc46db742e3c9a` —
  PR #155 is Draft and `OPEN`.
- `check-runs.json` — SHA-256
  `5377882d35f0abd7f68458891b0603b744633947cae0a8ea948e08ed106e0929` —
  all 39 exact-SHA GitHub checks are terminal: 33 `success` and six
  scope-justified `skipped`, including successful `SonarCloud Code Analysis`.

This verifies only the task-owned #155 corrective portion at Draft-PR level.
The aggregate remains P1 `in_progress` because PR #155 is Draft, `OPEN`, and
unmerged, while the global `652/zero` goals, default branch, historical #74,
#138, and broader-backlog dependencies remain active. If the #155 head
changes, repeat exact-head Sonar issue, Quality Gate, measure, and GitHub-check
readback before reliance. No Ready-for-review, merge, master update, Sonar
policy, suppression, exclusion, Framework/MRTS source, Gitlink, or external
issue-disposition action occurred.

### Initial exact-head remediation-required receipt for Draft PR #156 — 2026-07-28

Draft PR #156 is Draft, `OPEN`, and unmerged at exact head
`e2b1370caa32e621ada4ce96ad03f603904cee49`. Retained all-check run
`pr156-initial-e2b-20260728` is at
`/var/tmp/codex/ModSecurity-conector/pr156-initial-e2b.Dou6Iz`. Its manifest
states that the receipt contains public metadata/analysis only, and its
`SHA256SUMS` validates all five payloads:

- `sonar-issues.json` — SHA-256
  `759bcbe82af395403ce9868a86436d8adea1adb7623faedebf963abbccc0e9b9` —
  seven OPEN task-owned `python:S3415` MAJOR/CODE_SMELL keys
  `AZ-pRyPD--pWpbX22nGu`, `AZ-pRyPD--pWpbX22nGv`,
  `AZ-pRyPD--pWpbX22nGw`, `AZ-pRyPD--pWpbX22nGx`,
  `AZ-pRyPD--pWpbX22nGy`, `AZ-pRyPD--pWpbX22nGz`, and
  `AZ-pRyPD--pWpbX22nG0` in
  `tests/test_apache_phase4_response_regression_wiring.py`.
- `sonar-quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `sonar-measures.json` — SHA-256
  `16aaecb3c146bbce90b099e3a5090d70154b60f4e5fb7db5630851b046518e55` —
  seven code smells, new duplicated lines `0`, and new-duplication density
  `0.0`.
- `github-pr.json` — SHA-256
  `40f26c40cd677c8bd68e50a3107489eb18c06872db4524cb9fc4240358b2c94a` —
  PR #156 is Draft, `OPEN`, and unmerged at the exact head.
- `github-check-runs.json` — SHA-256
  `0eacac4743e9482ebfcd2a5380c40a101ed1a600906f3d34edaa8fedf4cb39a8` —
  all 39 exact-SHA GitHub checks are terminal: 33 `success` and six
  scope-justified `skipped`, including successful `SonarCloud Code Analysis`
  with seven annotations.

This is an intermediate exact-head receipt with `remediation_required`, not an
end-state record. The Quality Gate and duplication metrics do not resolve the
seven task-owned OPEN findings. `FND-SONAR-0016` therefore remains P1
`in_progress`; the global `652/zero` goals, default branch, historical #74,
#138, and broader backlog remain independently active. If the #156 head
changes, correct the seven assertion argument orders and repeat exact-head
Sonar issue, Quality Gate, measure, and GitHub-check readback before reliance.
No Ready-for-review, merge, master update, Sonar policy, suppression,
exclusion, Framework/MRTS source, Gitlink, or external issue-disposition
action occurred.

### Bounded zero-issue exact-head receipt for Draft PR #156 — 2026-07-28

The initial `e2b1370caa32e621ada4ce96ad03f603904cee49` receipt above remains
the historical seven-issue observation. Its sealed successor run
`pr156-verified-59ff-20260728` is retained at
`/var/tmp/codex/ModSecurity-conector/pr156-verified-59ff.Ce1cD4` for exact
head `59ff4d5bbb6e278d93c0b965096e842b77f446bb` against base `master`
`8e8acb8dab1cd03723de269cab7da7dd62e5e010`. The public-metadata-only
manifest and `SHA256SUMS` validate all five payloads:

- `sonar-issues.json` — SHA-256
  `55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e` —
  direct Sonar PR issue total `0`; the seven preceding `python:S3415` keys
  are absent from this exact-head readback.
- `sonar-quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `sonar-measures.json` — SHA-256
  `039e30f3c3ae59b80583cfbcbab92c43b78071330a3dd1c1cc022c11e79b376b` —
  zero bugs, vulnerabilities, and code smells; new duplicated lines `0` and
  new-duplication density `0.0`. Project-wide duplicated-lines density/lines
  remain `0.2`/`1260` and are not a global completion result.
- `github-pr.json` — SHA-256
  `00ceee8fa66b7ec93cecc51924d65cec4b133a51ac201db2633c59e199c01135` —
  PR #156 is Draft, `OPEN`, and unmerged at the exact head/base.
- `github-check-runs.json` — SHA-256
  `6e119ce37717ab7132fb0cedf1aa76d14eeec92100d1bb60335b1feff5632459` —
  all 39 exact-SHA GitHub checks are terminal: 33 `success` and six
  scope-justified `skipped`, including successful `SonarCloud Code Analysis`
  with zero annotations.

This is the current bounded Draft-PR #156 result, not a master/default-branch
or global-backlog result. PR #156 remains Draft and unmerged, and
`FND-SONAR-0016` remains P1 `in_progress` because the global `652/zero` goals,
historical #74/#138, and broader backlog remain independently active. If the
PR head changes, repeat exact-head Sonar issue, Quality Gate, measure,
PR-head/base, and GitHub-check readback before reliance. No Ready-for-review,
merge, master update, Sonar policy, suppression, exclusion, Framework/MRTS
source, Gitlink, or external issue-disposition action occurred.

### Bounded zero-issue exact-head receipt for Draft PR #157 — 2026-07-28

The original live Parent `python:S1192` receipt `AZ9cRyW7HhV2CayPTPuq` was at
`ci/checks/documentation/check-bilingual-docs.py:728` in
`check_tools_mrts_clean(repo)`, where the fixed `tools/MRTS` literal had three
equivalent roles. Sealed retained run `pr157-verified-3055-20260728` is at
`/var/tmp/codex/ModSecurity-conector/pr157-verified-3055.dvn7gp` for exact
head `3055790e88e6b962bdffdabadccee1de2ce59355` against `master` base
`8e8acb8dab1cd03723de269cab7da7dd62e5e010`. Its public-metadata-only manifest
and `SHA256SUMS` validate all five payloads:

- `sonar-issues.json` — SHA-256
  `55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e` —
  direct Sonar PR issue total `0`; the original `AZ9cRyW7HhV2CayPTPuq` receipt
  is absent from this exact-head readback.
- `sonar-quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `sonar-measures.json` — SHA-256
  `42d562f2ed09cdbf1f28dc97b2f48df090bef9349c7a74d4626ba1c216915a5f` —
  new duplicated lines `0` and new-duplication density `0.0`; project-wide
  duplicated-lines density/lines remain `0.2`/`1260`.
- `github-pr.json` — SHA-256
  `4307c13605039d72596c27e5028a5163a304fe7d1eca2beb8d1c5d52b007d75a` —
  PR #157 is Draft, `OPEN`, and unmerged at the exact head/base.
- `github-check-runs.json` — SHA-256
  `f982a6a08c64023cad59b1a843205877ba546389994f13c8700577e77c114805` —
  all 39 exact-SHA GitHub checks are terminal: 33 `success` and six
  scope-justified `skipped`, including successful `SonarCloud Code Analysis`
  with zero annotations.

This is a bounded clean Draft-PR result only. `FND-SONAR-0016` remains P1
`in_progress`: PR #157 is unmerged, and the global `652/zero` goal,
default-branch work, historical #74/#138, and broader backlog remain
independently active. If the PR head changes, repeat exact-head Sonar issue,
Quality Gate, measure, PR-head/base, and GitHub-check readback before reliance.
No master/default-branch/global completion, Ready-for-review, merge, Sonar
policy, suppression, exclusion, Framework/MRTS source, Gitlink, or external
issue-disposition action is implied.

### Bounded zero-issue exact-head receipt for Draft PR #158 — 2026-07-28

The sealed retained run `pr158-verified-552f-20260728` is at
`/var/tmp/codex/ModSecurity-conector/pr158-verified-552f.umSut7` for exact
Draft PR #158 head `552fd67ee1212c0a71cec1726f6a079e33671c87` against
`master` base `8e8acb8dab1cd03723de269cab7da7dd62e5e010`. Its manifest scopes
the work to a Parent-only HAProxy HTX diagnostic-range Sonar
`shelldre:S1192` remediation; it does not provide an original Sonar key or
source location, so none is inferred. Its public-metadata-only manifest and
`SHA256SUMS` validate all seven payloads:

- `sonar-issues.json` — SHA-256
  `55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e` —
  direct Sonar issue total `0`.
- `sonar-quality-gate.json` — SHA-256
  `c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77` —
  Quality Gate `OK`.
- `sonar-measures.json` — SHA-256
  `833ee10944af9a1aa7812fa8d52f35823bcb59fc0f66027f2feacfabd408862a` —
  new duplicated lines `0` and new-duplication density `0.0`; project-wide
  duplicated lines/density remain `1260` / `0.2`.
- `github-pr.json` — SHA-256
  `399137dbf3448d5e4d8d9117f61cea38b7ee48f897b4c6966c662553d89b535d` —
  PR #158 is Draft, open, mergeable, and unmerged at the exact head/base.
- `github-check-runs.json` — SHA-256
  `10047899318efb4968e6777e665b42959b8070495f157e72b3edbbdc9f96568d` —
  all 39 exact-SHA GitHub checks are terminal: 33 `success`, six
  scope-justified `skipped`, and none pending or failing; `SonarCloud Code
  Analysis` is successful for the same SHA.
- `github-reviews.json` — SHA-256
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` —
  zero reviews at collection time.
- `github-review-comments.json` — SHA-256
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` —
  zero review comments at collection time.

This is a bounded clean Draft-PR result only. `FND-SONAR-0016` remains P1
`in_progress`: PR #158 is unmerged, and the global `652/zero` target,
default-branch work, historical #74/#138, and broader backlog remain
independently active. If the PR head changes, repeat exact-head Sonar issue,
Quality Gate, measure, PR-head/base, GitHub check-run, review, and review-
comment readback before reliance. No master/default-branch/global completion,
Ready-for-review, merge, Sonar policy, suppression, exclusion, Framework/MRTS
source, Gitlink, or external issue-disposition action is implied.

### PR #182 exact-head S5778 corrective successor — 2026-07-29

At exact PR #182 head `c15092f2bf05d5281f0976e87450bb79e6ea9e65`, the
Quality Gate was `OK` and New-Code duplication was `0` / `0.0`, but direct
Sonar readback found one OPEN task-owned `python:S5778` key
`AZ-vW5dtuVkXWHIWkGg3` at
`tests/test_runtime_artifact_utils.py:57`. The minimal normal successor
`948168ca3fdeaaa9c77eaa972e9994b40fb99c4c` derives the path before the
exception assertion, leaving only the intended invocation inside it. The
focused common/HAProxy/Envoy/runtime-path suite passed all 42 tests and the
successor was pushed without force. Retained receipt:
`evidence/pr182-c150-sonar-s5778-followup.md`, SHA-256
`1c973877463101254a35c2fd3a2a1d86ed4204b33a8f3f42fb077786ba7480e9`.

This is a remediation-in-progress observation only. Fresh exact-head GitHub,
Sonar, review/thread, and mergeability evidence is required before any merge;
no Sonar policy, suppression, exclusion, Framework/MRTS source, Gitlink,
master, or global-backlog conclusion is implied.

### Current exact-head terminal blocker for Draft Parent PR #160 — 2026-07-28

Sealed run pr160-terminal-open-s1481-e456-20260728 is retained at
/var/tmp/codex/ModSecurity-conector/runs/pr160-exact-head-e456-20260728.YLtDu6
for exact Draft PR #160 head e456b9fc909116656294fc744526cf8c81b0c962
against master base 8e8acb8dab1cd03723de269cab7da7dd62e5e010. The PR is
open, Draft, mergeable, clean, and unmerged. SHA256SUMS validates the five
bounded sanitized receipt payloads:

- sonar-issues.json — SHA-256
  77306d8fd8e760d9a7654f874a082afdea9f4db779a60ceee218e17bbf9f9f68:
  direct SonarQube Cloud issue total 3.
- sonar-quality-gate.json — SHA-256
  39b3817ab81505f0dead51643a6cfb43580adeb86c626026723a4f915dc76523:
  Quality Gate OK.
- sonar-measures.json — SHA-256
  b62a5d6e327701cc52beaaa64b9f04a065accbbd1ceae62cb8d1ec969116caf8:
  new duplicated lines/density 0/0.0; project-wide duplicated lines/density
  remain 1260/0.2.
- github-pr.json — SHA-256
  bc65042063ce96dddbb43dfc67a2a2919943803dacd6fc89664819e997cad708:
  exact PR/head/base state.
- github-check-summary.json — SHA-256
  cb57f9d4e9af7cca395bca349057d705c29f595703b62bd667f47ec0046db469:
  all 39 exact-SHA GitHub checks terminal (33 success, six scope-skipped,
  none pending or unacceptable); SonarCloud Code Analysis succeeded for the
  same SHA.

The three exact-head task-owned OPEN findings are all MINOR CODE_SMELL
python:S1481 in ci/checks/connectors/all/check-remaining-connectors-start-wiring.py:
AZ-p4PPg1eeMvlV2M02- at line 66 (rc_default), AZ-p4PPg1eeMvlV2M03A at line
68 (kill_zero), and AZ-p4PPg1eeMvlV2M02_ at line 69 (wait_command). SonarQube
Cloud describes each as an unused local variable. This tracking-only task did
not inspect the checker semantics or claim that removal is behavior-safe.

Therefore the exact head is remediation_required despite its Quality Gate and
zero new-code duplication. A normal Parent-owned correction must establish
the variables' intended contract, retain legitimate static-wiring behavior,
and obtain fresh exact-head issue, Quality-Gate, measure, PR-head/base, and
GitHub-check evidence. FND-SONAR-0016 remains P1 in_progress; this record
does not authorize or claim Ready-for-review, merge, master/default-branch or
global closure, Sonar policy/suppression/exclusion, Framework/MRTS source,
Gitlink, or external issue disposition.

### Bounded zero-issue exact-head receipt for Draft PR #159 — 2026-07-28

The sealed retained run `pr159-verified-cf32-20260728` is at
`/var/tmp/codex/ModSecurity-conector/runs/pr159-exact-head-cf32-20260728.B9kyWO`
for exact Draft PR #159 head `cf323de85b4411b2c1f56055a430d43f65a8ed97`
against `master` base `8e8acb8dab1cd03723de269cab7da7dd62e5e010`. The PR
description identifies two Parent-owned `shelldre:S1192` literal-duplication
findings in `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`: fixed
`%{http_code}` at eight status probes and fixed `1,200p` at six bounded
diagnostic paths. The fixed file-local owners are `HTTP_STATUS_FORMAT` and
`DIAGNOSTIC_LINES`. It provides no original Sonar key, so none is inferred. Its
public-metadata-only manifest and `SHA256SUMS` validate all seven payloads:

- `sonar-issues.json` — SHA-256
  `3afea43ab59b9b77b506b956538dd4e09ae0c56d564f1c7991bdf1eaf8a224e5` —
  direct Sonar issue total `0`.
- `sonar-quality-gate.json` — SHA-256
  `8cfb48611758ee377cd6c00ebee6ae6470fa1ffba0a0e53797d780bbc275955f` —
  Quality Gate `OK`.
- `sonar-measures.json` — SHA-256
  `09685d4b0ac08bf5a56725720e03d842a4e9cfa99b77665f103559ff6408644f` —
  new duplicated lines `0` and new-duplication density `0.0`; project-wide
  duplicated lines/density remain `1260` / `0.2`.
- `github-pr.json` — SHA-256
  `05b361fdbb574ac44d7b0d89ceedcf2a96287ae249945acd019e3b83cdb3e4b8` —
  PR #159 is Draft, open, mergeable, and unmerged at the exact head/base.
- `github-check-summary.json` — SHA-256
  `419300eb0e452ea0eafdcd5d5ba14875d48109537645aadc4e54f895b0896c95` —
  all 39 exact-SHA GitHub checks are terminal: 33 `success`, six
  scope-skipped, and none pending or failing; `SonarCloud Code Analysis` is
  successful for the same SHA with zero annotations.
- `github-reviews.json` — SHA-256
  `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` —
  zero reviews at collection time.
- `github-review-comments.json` — SHA-256
  `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` —
  zero review comments at collection time.

This is a bounded clean Draft-PR result only. `FND-SONAR-0016` remains P1
`in_progress`: PR #159 is unmerged, and the global `652/zero` target,
default-branch work, historical #74/#138, and broader backlog remain
independently active. If the PR head changes, repeat exact-head Sonar issue,
Quality Gate, measure, PR-head/base, GitHub check-run, review, and review-
comment readback before reliance. No master/default-branch/global completion,
Ready-for-review, merge, Sonar policy, suppression, exclusion, Framework/MRTS
source, Gitlink, or external issue-disposition action is implied.

### Resulting-master red gate after protected PR #182 — 2026-07-29

PR #182 merged normally as
`a81456110a6bb6f7cf2f8202f5223fb3f7b3a194`. Its exact PR head
`76644bfe832d1530704ca2ae0f2182338949ead5` was clean: Quality Gate `OK`,
new-security rating `A` / `1`, 100% reviewed new security hotspots, and zero
OPEN/CONFIRMED PR issues.

The resulting master Quality Gate is red, but the retained chronology proves
that it is not a #182 regression. The immediately preceding master analysis
had 121 open vulnerability reports, rating `E` / `5`, and three open hotspots;
the merge analysis has 105, the same rating, and the same three hotspots. All
remaining vulnerability reports predate the merge, and a query for reports
created after the preceding analysis returns zero. The three unreviewed
`python:S5332` clear-text-protocol hotspots were created on 2026-06-15 outside
#182's diff. The configured New-Code period starts on 2026-05-14, so the red
gate includes this older backlog.

The retained bounded receipt is
`/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-master-postmerge-sonar-triage.md`,
SHA-256
`5b3a3625e759082bb48ed9c314326c2c9d435412b5f63a2b72200370d1009f1e`.
This records a default-branch backlog only: it does not claim that any
remaining scanner report is safe, false positive, or irrelevant, and it does
not relax the fresh exact-head Quality-Gate requirement for later PRs.

### Exact-head S134 remediation for Parent PR #181 — 2026-07-29

Exact Parent PR #181 head
`736d9ff8affebd0ccd6ebdef5ef275546b312c41` removes its two task-owned
SonarQube Cloud `c:S134` nesting findings by dispatching only the exact SPOP
`body` and `response_body` keys to the existing typed value parser. The
focused C17 harness preserves String/Binary acceptance, non-byte consumption,
response-role flags, and unknown-key non-consumption.

The exact hosted result is clean against master
`a81456110a6bb6f7cf2f8202f5223fb3f7b3a194`: Quality Gate `OK`, zero
OPEN/CONFIRMED PR issues, zero new duplicated lines, 0.0% new-code duplication,
security rating `A` / `1`, 100% new-hotspot review, zero reviews/comments, and
39 terminal GitHub checks (33 `success`, six scope-justified `skipped`). The
initial push-triggered `quick-check` was externally stalled and was cancelled
only after the time-limit anomaly; one normal rerun on the unchanged SHA then
succeeded. The PR is Ready for review and `CLEAN`/mergeable.

The retained bounded receipt is
`/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr181-736-exact-head-hosted.md`,
SHA-256
`df134334f44a9752957787a5e9fd3f51debbefee3a1b6778f3743898659fce9c`.
This is exact-head readiness evidence only until protected merge and
post-merge verification; it does not change any Sonar policy, suppression,
exclusion, Framework/MRTS source, Gitlink, or default-branch control.

### Protected merge and resulting-master verification for PR #181 — 2026-07-29

PR #181 merged normally at 20:43:09 UTC as
`fda62539b6f0a710865707e3003b73ed4469f20e`, equal to fetched
`origin/master`. GitHub reports 21 terminal master checks: 18 `success`, two
scope-justified `skipped`, and one failed SonarCloud check; every GitHub
Actions workflow itself is successful.

SonarQube Cloud explicitly binds its 20:43:20 UTC master analysis to this
commit. Its red Quality Gate remains the independently tracked New-Code-period
security backlog: rating `E` / `5`, zero-percent reviewed hotspots, 105
vulnerabilities, and the same three low-probability 2026-06-15 hotspots. A
query for reports created after the preceding #182 master analysis returns
zero, so no new #181-attributed scanner report is evidenced. New-Code
duplication decreased from 727 to 697 lines.

The retained bounded receipt is
`/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr181-master-postmerge.md`,
SHA-256
`807b67666aa18b4b05c79f7e862ea28deebf43f1f8d4c9ec5782ff4625831adb`.
This verifies the protected integration without calling any outstanding scanner
report safe or changing a Sonar policy, suppression, exclusion, Framework/MRTS
source, Gitlink, or default-branch control.

### C12 exact-head No-CRS S1192 remediation for Draft PR #199 — 2026-07-30

The current Parent-master SonarQube Cloud receipt `AZ9cRycZHhV2CayPTPw4`
(`shelldre:S1192`) identified five equivalent No-CRS missing-cases diagnostics
at `ci/runtime/lifecycle/run-connector-stage.sh:292`. Draft PR #199 moves
only that static diagnostic into the readonly
`NO_CRS_SELECTED_CASES_MISSING_MESSAGE` owner. Its hermetic Parent control
exercises all six generic missing-case routes and preserves both the selected
Envoy generic target and the full-lifecycle Envoy target. The five existing
non-empty guards, stderr redirects, and `exit 1` outcomes remain unchanged.

The retained exact-head receipt is
`/var/tmp/codex/ModSecurity-conector/runs/ci-c12-no-crs-missing-cases-message/evidence/pr199-exact-head-verification.md`,
SHA-256
`eac8ed28ecc6b93daf0160ac2f4b5d31ee2697890352b16afea494eeb21b0f39`.
At `2026-07-30T07:01:03Z`, it binds open Draft PR #199, unmerged and
mergeable/clean, to exact head
`76ebf6b76043a5bc24667312bd9b8b6dbc9c6a1e` against master base
`fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f`. Local, remote, and GitHub PR
heads are equal. The exact-head readback has Quality Gate `OK`, zero
OPEN/CONFIRMED PR issues with the original key absent, `new_violations=0`,
zero new duplicated lines, `0.0` new-code duplication density, 39 terminal
GitHub checks (33 `success`, six scope-justified `skipped`), and zero reviews
and inline review comments. The observed project-wide duplicated-lines/density
values `589` / `0.1` are only current project observations, not a claim that
C12 resolved the global backlog.

This verifies only the C12 portion at the exact open Draft-PR head. If that
head changes, repeat focused controls and the exact-head Sonar issue,
Quality-Gate, measure, PR-head/base, GitHub check-run, review, and
review-comment readbacks before relying on it. `FND-SONAR-0016` remains P1
`in_progress` / `feasible_now` and release-blocking; no Ready-for-review,
merge, master/default-branch/global closure, Sonar policy, suppression,
exclusion, Framework/MRTS source, Gitlink, or external issue-disposition
action is authorized or claimed.

### PR #202 exact-head bounded Sonar result — 2026-08-01

Draft PR #202 exact head
`ecccaa0adf16b329162167eb1abe8a0003dc0052` against base
`651834ef577095a48b7f54d5bd7ffcc76d9c388a` has SonarQube Cloud Quality
Gate `OK`, zero OPEN/CONFIRMED PR issues, `new_violations=0`, zero new
duplicated lines, and `0.0%` New-Code duplication. The retained receipt is
`/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/pr-202-head-eccc-sonar-clean.md`,
SHA-256
`8cea3f6df1afb3b33b4f84acfbf91373282d7d1b8477d96ec975fd2060e002c3`.

This is a bounded Sonar result, not overall PR readiness or merge evidence.
`FND-PARENT-0075` separately records the unresolved historical
Secret-scanning heuristic failure, and current `master` conflict state blocks
the Draft PR. `FND-SONAR-0016` remains P1 `in_progress` /
`feasible_now` and release-blocking; no policy, suppression, exclusion,
Framework/MRTS source, Gitlink, Ready-for-review, merge, or master/global
closure is implied.

### Traefik ten-key current-master remediation — 2026-08-01

The retained current-master receipt
\`/var/tmp/codex/ModSecurity-conector/runs/traefik-sonar-remediation-20260801/evidence/sonar-traefik-current-master.md\`,
SHA-256 \`61f977ad46fba21fddda2096b337016afae4a5a158256081ada21b2f50ca18d0\`,
records ten current \`connectors/traefik/\` keys at base
\`c3319575ae86d9810da8b5428590336d60cd3daf\`: eight vulnerability reports
(\`python:S5443\`, \`pythonsecurity:S2083\`, \`pythonsecurity:S8707\`, and
\`pythonsecurity:S8701\`) and two maintainability reports
(\`python:S3776\` and \`godre:S8196\`). The isolated Parent remediation
validates immutable local executables and fixed in-root artefact names, keeps
permission-based shared-root rejection, splits the native lifecycle, and names
the Go single-method interface without a compatibility break. Focused Python
and Go controls pass locally; the full native host lifecycle is blocked only by
missing task-provisioned Traefik and libmodsecurity inputs.

This is current remediation evidence, not an exact-PR-head verification. The
requested Draft PR still needs a fresh issue, Quality-Gate, new-issue,
duplication, GitHub-check, review and security-diff readback before this
aggregate can record a bounded verified result. No Sonar policy, suppression,
exclusion, Framework/MRTS source, Gitlink, merge, or master/global closure is
claimed.

### PR #211 exact-head Traefik result — 2026-08-01

Draft PR #211 head 0c9e2f495b2d913d3d79a5bfd66217e56e0f2993 against base
51d70325eac17bfe3fa7ebd187b991fd91291808 is open, Draft, mergeable, and
clean. All 66 completed GitHub checks passed; scope-inapplicable checks were
skipped. SonarQube Cloud reported Quality Gate OK, zero OPEN/CONFIRMED PR
issues, new_violations=0, zero new duplicated lines, and 0.0% New-Code
duplication. The first analyzed head had one new S2083 result-output issue;
the normal follow-up uses fixed whitelisted names with descriptor-relative
O_NOFOLLOW writes and a symlink negative control. The retained bounded receipt
is /var/tmp/codex/ModSecurity-conector/runs/traefik-sonar-remediation-20260801/evidence/pr211-hosted-verification.md,
SHA-256 36f535d595e372a1fd82b3647c86f39d5782568ca34347ca0f5f2d4d41bedef8.

This verifies the Traefik PR #211 portion only. The aggregate stays P1
in_progress / feasible_now and release-blocking because its historical and
independent Parent Draft-PR portions remain active. No master, global-backlog,
Sonar-policy, suppression, exclusion, Framework/MRTS source, Gitlink, or
external issue-disposition claim follows from this bounded result.

### PR #214 exact-head Envoy S8196 result — 2026-08-01

The current Envoy receipt `AZ9cRyqvHhV2CayPTP0H` (`godre:S8196`) named the
one-method `processor.Engine` interface at
`connectors/envoy/ext_proc/internal/processor/processor.go:128`. Draft PR
#214 renames only that internal type to `TransactionOpener` in its definition
and five typed consumers, preserving the sole `Open(context.Context,
StreamMetadata) (Transaction, error)` method and all runtime behavior.
`ResponseCommitter` is a separate valid interface and was intentionally left
unchanged.

At exact open Draft head `326186cd54255d5f4fb77230bf8230f40745b6b3` against
base `6b4aca18d390363764b96d85cd31969b9bb114a1`, local and remote branch heads
match the GitHub PR head. The retained hosted receipt
`/var/tmp/codex/ModSecurity-conector/runs/20260801T093020Z-envoy-sonar-maintainability-followup-20260801-ea028ca6/evidence/pr214-hosted-verification.md`,
SHA-256
`f7b99a825d90f8f951dfb781265cd54ca2cd5084ef5cb549c15a25c9d385349d`,
records an open Draft, CLEAN/mergeable PR with all applicable GitHub checks
terminal (passed or scope-justified skipped), zero reviews and inline review
comments, SonarQube Cloud Quality Gate `OK`, zero OPEN/CONFIRMED PR issues,
`new_violations=0`, zero new duplicated lines, and `0.0%` New-Code
duplication. Focused Go test, vet, gofmt, and diff checks passed. The
bilingual-documentation unit suite passed; its full checker remains blocked
only by 20 pre-existing absent links within the intentionally unpopulated
Framework gitlink. The final sealed security-diff review reports no
reportable security finding.

This verifies only the Envoy S8196 portion at its exact open Draft-PR head.
If the head changes, repeat focused controls and exact-head Sonar, GitHub
check, review, and security-diff readback. `FND-SONAR-0016` remains P1
`in_progress` / `feasible_now` and release-blocking because unrelated Parent
backlog entries remain active. No Ready-for-review, merge, master/default-
branch/global closure, Sonar policy, suppression, exclusion, Framework/MRTS
source, Gitlink, or external issue-disposition action is claimed.

### PR #214 protected merge and resulting-master result — 2026-08-01

PR #214 was merged by the current authorized regular merge method at
`2026-08-01T10:12:58Z`. Its verified head
`326186cd54255d5f4fb77230bf8230f40745b6b3` and base
`6b4aca18d390363764b96d85cd31969b9bb114a1` produced resulting master commit
`b370740dcb16739be7e0b323152f69da31c1a8c1`. The two expected parents and the
six expected changed files are present. All 14 GitHub Actions workflows for
that exact resulting-master commit succeeded.

The external SonarCloud master check is red, but it is demonstrably not an
Envoy-PR #214 regression: the immediately preceding master commit had the same
Quality-Gate failure, and an exact query finds no open issue created after its
analysis. The retained post-merge receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260801T093020Z-envoy-sonar-maintainability-followup-20260801-ea028ca6/evidence/pr214-master-postmerge.md`,
SHA-256
`0fc9bb2e3a941ac985717aff02c0a5bf216263df1947b0ca15419ac15525c81e`.
The remaining failure is the pre-existing `FND-SONAR-0001` New-Code-period
backlog: rating `E` and the unreviewed 2026-06-15 low-probability
`python:S5332` hotspot `AZ7K5CQgixFPtcnbna1J` at
`ci/evidence/reports/generate-system-environment-proof.py:98`.

This records the successful bounded merge and an external post-merge blocker
without classifying the backlog as safe or fixed. `FND-SONAR-0016` remains P1
`in_progress` / `feasible_now` and release-blocking; no Sonar policy,
suppression, exclusion, Framework/MRTS source, Gitlink, or direct-master
follow-up was performed.
