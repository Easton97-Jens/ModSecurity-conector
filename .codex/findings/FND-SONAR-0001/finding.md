# FND-SONAR-0001 — Parent SonarQube quality gate remains failed pending authorized review of three validated-safe hotspots

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-SONAR-0001` |
| Title / Titel | `Parent SonarQube quality gate remains failed pending authorized review of three validated-safe hotspots` |
| Category / Kategorie | `sonarqube_finding` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `sonarqube_configuration` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `blocked` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Current Parent master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` is the
protected squash result of PR #72. Its SHA-bound SonarCloud analysis
`b314d0b2-ea5a-49f4-be74-65eec30469d1` has Quality Gate `ERROR`: new
reliability and maintainability ratings are `1` and new-code duplication is
`0.4%`, but new security rating is `5` and hotspot review is `0.0%`. There are
zero open Bugs, 220 open Vulnerabilities, and three `TO_REVIEW`
`python:S5332` hotspots. The aggregate remains a P1 blocked release gate
because the three residual hotspots still need an authorized external
reviewed/safe disposition.

Ten separate current regular Vulnerability rows were also reviewed against
their exact-master sources. Four `python:S5332` rows are technically
`not_actionable` local loopback-harness or local-classifier uses, five
`pythonsecurity:S2083` rows write input-derived report text only as content,
never as a destination path, and one `python:S5443` row is a secure test-only
TemporaryDirectory use. They remain `OPEN`: no external false-positive
disposition was authorized. Two further `pythonsecurity:S8707` rows have
locally validated source repairs: the response-header fixture-read path now
uses the established safe-root containment before `Path.read_text`, and the
Lighttpd HTTP/1.1 entity fixture helper validates ready/result output files
under `--safe-root` while publishing JSON through exclusive randomized staging.
Both remain externally `OPEN` on master until a delivered head is analyzed.
This bounded result covers twelve rows and does not reconcile the remaining
194 exact-inventory Parent Vulnerability rows.

### Superseding current-master revalidation — 2026-07-23

Protected PR #92 exact head `40a419d5b0f599566469060112b7e55dbab05744`
passed its SonarQube Cloud PR Quality Gate with zero new issues and zero new
security hotspots, then was squash-merged as Parent master
`95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3`. All 14 resulting-master GitHub
Actions workflow runs passed. Its 21 terminal checks have 18 successes, two
expected skips, and only Sonar check `89147577049` failed.

The public exact-master gate still fails only on Security Rating `5` and
hotspot review `0.0%`; reliability and maintainability are `1` and duplication
is `0.4%`. It names the same three `TO_REVIEW` `python:S5332` hotspots at
`check-generated-report-layout.py:42`, `:49`, and
`generate-system-environment-proof.py:98` as predecessor master `ad953cd`.
The current blobs remain
`890e39421f36495da2b87c242e72bd13f122d69f` and
`37ea2ec2fb9f81e843e4d506bcc6c2055266ecbe`, preserving the existing
`already_safe` source/control/sink assessment. This is an independent
pre-existing release blocker, not evidence of a #92 regression. No external
hotspot disposition, suppression, gate change, false-positive action, or risk
acceptance was made. Retained receipt:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09/evidence/pr-92-protected-merge-and-master-validation-20260723T0742Z.md`,
SHA-256 `669dc61a094aa058382f8afc0ff2a7bdf511bc3b54d072beeae2d8ced9b43c0e`.

### Post-PR #100 current-master revalidation — 2026-07-24

Protected PR #100 exact head `dace5ca118a89a91c33fde952a6282f9c391ee10`
passed its SonarCloud PR Quality Gate with zero new issues and zero new
security hotspots, then was squash-merged as Parent master
`6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d`. All 14 resulting-master GitHub
Actions workflows succeeded. Of its 21 terminal commit checks, only
SonarCloud `89440531005` failed.

The public project Quality Gate remains `ERROR` only because Security Rating
is `5` and hotspot review is `0.0%`; reliability and maintainability are `1`
and duplication is `0.4%`. Direct current readback confirms the same three
low-probability `TO_REVIEW` `python:S5332` hotspots (`AZ7K5CRYixFPtcnbna1R`,
`AZ7K5CRYixFPtcnbna1S`, and `AZ7K5CQgixFPtcnbna1J`) and 177 open
Vulnerability rows across mixed Parent, Framework, and original-MRTS-indexed
components. The prior bounded static triage remains `needs_review`: individual
caller provenance and supported security boundaries are not yet established.
No source, external Sonar disposition, suppression, scanner/Gate, Framework,
MRTS, or risk-acceptance state changed. This is a pre-existing mixed-backlog
release blocker, not evidence of a #100 regression; status remains `blocked`.

### Post-PR #101 current-master revalidation — 2026-07-24

Protected PR #101 exact head `f988d627e76c98b7c34f91cb3d82be268750d464`
passed all 39 terminal PR checks and its SonarQube Cloud PR Quality Gate `OK`
with zero new issues and zero new hotspots. It was then squash-merged as Parent
master `215b503a8d68ee85d93e18888f3710d1974c3169` at
`2026-07-24T09:28:31Z`. All 14 resulting-master GitHub Actions workflows
passed. Of 21 terminal commit checks, only SonarCloud `89447965729` failed.

The public master Quality Gate remains `ERROR` only because Security Rating is
`5` and hotspot review is `0.0%`; reliability and maintainability are `1` and
duplication is `0.4%`. PR #101's final diff contains only Parent assertion
diagnostics and its bilingual Change Record/index files, not either
hotspot-bearing source file. This is therefore a revalidation of the existing
mixed-backlog release blocker, not evidence of a #101 regression. No source,
external hotspot review/disposition, suppression, scanner/Gate,
Framework/MRTS, or risk-acceptance state changed; status remains `blocked`.

### Post-PR #102 current-master revalidation — 2026-07-24

Protected PR #102 exact head `193fefd120e69807b40d21ffe376b45f50f10208`
passed all 39 terminal PR checks, its SonarQube Cloud PR Quality Gate `OK`,
and zero open PR issues and security hotspots. It was then squash-merged as
Parent master `ec57576814a3f75c5e153d51c945bd1dd341a916` at
`2026-07-24T10:08:36Z`. All 14 resulting-master GitHub Actions workflows
passed, and all 20 terminal commit check runs are `success` or expected
`skipped`; no SonarCloud master check run was published for this SHA.

The direct public master Quality Gate read after those workflows remains
`ERROR` only because Security Rating is `5` and hotspot review is `0.0%`;
reliability and maintainability are `1` and duplication is `0.4%`. PR #102's
final diff contains only a Parent test's symmetric assertion diagnostics and
its bilingual Change Record/index files, not either hotspot-bearing source
file. This is therefore a current readback of the existing mixed-backlog
release blocker, not evidence of a #102 regression. No source, external
hotspot review/disposition, suppression, scanner/Gate, Framework/MRTS, or
risk-acceptance state changed; status remains `blocked`.

### Post-PR #103 current-master revalidation — 2026-07-24

Protected PR #103 exact head `ad1aef95ed62fd906cee1e9b1d507ce07cbc7d54`
passed all 39 terminal PR check runs with only `success` or expected `skipped`
conclusions, all six protected required checks, and its SonarQube Cloud PR
Quality Gate `OK` with zero new issues and zero security hotspots. It was
then squash-merged as Parent master `90e3d8d9603375f9a33e2a51836ba284221fdd0f`
at `2026-07-24T10:54:20Z`. All 14 resulting-master GitHub Actions workflows
passed. Of 21 terminal master check runs, 18 succeeded, two were expected
skips, and only SonarCloud `89464137047` failed.

That failed master check has the same three `TO_REVIEW` `python:S5332`
hotspots and Security Rating `5` / hotspot review `0.0%` signature as the
immediate predecessor master `ec57576814a3f75c5e153d51c945bd1dd341a916` /
SonarCloud `89456327990`. Direct public readback for current master remains
`ERROR` only on those two conditions; reliability and maintainability are `1`
and duplication is `0.4%`. PR #103's final master diff changes neither
hotspot-bearing source file. This is therefore a revalidation of the existing
mixed-backlog release blocker, not evidence of a #103 regression. No source,
external hotspot review/disposition, suppression, scanner/Gate,
Framework/MRTS, gitlink, or risk-acceptance state changed; status remains
`blocked`.

### Post-PR #104 current-master revalidation — 2026-07-24

Protected PR #104 exact head `53564d896492945b681d20474d33e2a19a1bc4b5`
passed all 39 terminal PR check runs with only `success` or expected `skipped`
conclusions, all six protected required checks, and its SonarQube Cloud PR
Quality Gate `OK` with zero new issues and zero security hotspots. It was
then squash-merged as Parent master `053a9ca5b0f9351319c96d359107c53ba8f9d3a1`
at `2026-07-24T11:34:32Z`. All 14 resulting-master GitHub Actions workflows
passed. Of 21 terminal master check runs, 18 succeeded, two were expected
skips, and only SonarCloud `89471250793` failed.

That failed master check has the same three `TO_REVIEW` `python:S5332`
hotspots and Security Rating `5` / hotspot review `0.0%` signature as the
immediate predecessor master `90e3d8d9603375f9a33e2a51836ba284221fdd0f` /
SonarCloud `89464137047`. Direct public readback for current master remains
`ERROR` only on those two conditions; reliability and maintainability are `1`
and duplication is `0.4%`. PR #104's final master diff changes neither
hotspot-bearing source file. This is therefore a revalidation of the existing
mixed-backlog release blocker, not evidence of a #104 regression. No source,
external hotspot review/disposition, suppression, scanner/Gate,
Framework/MRTS, gitlink, or risk-acceptance state changed; status remains
`blocked`.

### Post-PR #105 current-master revalidation — 2026-07-24

Protected PR #105 exact head `831a6c7a3f8d179b1735ea6e6a0b9ff4d1868bdc`
passed all 39 terminal PR check runs with only `success` or expected `skipped`
conclusions, all six protected required checks, and its SonarQube Cloud PR
Quality Gate `OK` with zero new issues and zero security hotspots. It was then
squash-merged as Parent master `26f0eb9cff2f1c69ba7be9cfc5fd609659e3041f`
at `2026-07-24T11:58:35Z`. All 14 resulting-master GitHub Actions workflows
passed. Of 21 terminal master check runs, 18 succeeded, two were expected
skips, and only SonarCloud `89475577491` failed.

That failed master check has the same three `TO_REVIEW` `python:S5332`
hotspots and Security Rating `5` / hotspot review `0.0%` signature as the
immediate predecessor master `053a9ca5b0f9351319c96d359107c53ba8f9d3a1` /
SonarCloud `89471250793`. Direct public readback for current master remains
`ERROR` only on those two conditions; reliability and maintainability are `1`
and duplication is `0.4%`. PR #105's final master diff changes neither
hotspot-bearing source file. This is therefore a revalidation of the existing
mixed-backlog release blocker, not evidence of a #105 regression. No source,
external hotspot review/disposition, suppression, scanner/Gate,
Framework/MRTS, gitlink, or risk-acceptance state changed; status remains
`blocked`.

### Post-PR #106 current-master revalidation — 2026-07-24

Protected PR #106 exact head `43e55c2e54f738ee6d9e969cc8e57ce2831e0874`
passed all 39 terminal PR check runs with only `success` or expected `skipped`
conclusions, all six protected required checks, and its SonarQube Cloud PR
Quality Gate `OK` with zero new issues and zero security hotspots. It was then
squash-merged as Parent master `a60dd0380332a24cf231a36775256d21a812c027`
at `2026-07-24T12:18:37Z`. All 14 resulting-master GitHub Actions workflows
passed. Of 21 terminal master check runs, 18 succeeded, two were expected
skips, and only SonarCloud `89479343187` failed.

That failed master check has the same three `TO_REVIEW` `python:S5332`
hotspots and Security Rating `5` / hotspot review `0.0%` signature as the
immediate predecessor master `26f0eb9cff2f1c69ba7be9cfc5fd609659e3041f` /
SonarCloud `89475577491`. Direct public readback for current master remains
`ERROR` only on those two conditions; reliability and maintainability are `1`
and duplication is `0.4%`. PR #106's final master diff changes neither
hotspot-bearing source file. This is therefore a revalidation of the existing
mixed-backlog release blocker, not evidence of a #106 regression. No source,
external hotspot review/disposition, suppression, scanner/Gate,
Framework/MRTS, gitlink, or risk-acceptance state changed; status remains
`blocked`.

### Post-PR #107 current-master revalidation — 2026-07-24

Protected PR #107 exact head `c1168e7a715280d50c4a263285b7d0c09245bc6d`
passed all 39 terminal PR check runs with 34 `success` and five expected
`skipped` conclusions, all six protected required checks, and its SonarQube
Cloud PR Quality Gate `OK` with zero new issues and zero security hotspots. It
was then squash-merged as Parent master
`00dfe5f2ae0908228a6242b15e09f70d6742d102` at `2026-07-24T12:43:24Z`. All
14 resulting-master GitHub Actions workflows passed. Of 21 terminal master
check runs, 18 succeeded, two were expected skips, and only SonarCloud
`89484279475` failed.

That failed master check has the same three `TO_REVIEW` `python:S5332`
hotspots and Security Rating `5` / hotspot review `0.0%` signature as the
immediate predecessor master `a60dd0380332a24cf231a36775256d21a812c027` /
SonarCloud `89479343187`. Direct public readback for current master remains
`ERROR` only on those two conditions; reliability and maintainability are `1`
and duplication is `0.4%`. PR #107's final master diff changes neither
hotspot-bearing source file. This is therefore a revalidation of the existing
mixed-backlog release blocker, not evidence of a #107 regression. No source,
external hotspot review/disposition, suppression, scanner/Gate,
Framework/MRTS, gitlink, or risk-acceptance state changed; status remains
`blocked`.

### Post-PR #109 current-master revalidation — 2026-07-24

Protected PR #109 exact head `7cb8c4e294b2b93fe4c0b68c0a64ef1328dcfed1`
passed all 39 terminal PR check runs (33 `success`, six expected `skipped`),
all six protected required checks, and its SonarQube Cloud PR Quality Gate
`OK` with zero PR issues and zero security hotspots. It was then
protected-squash-merged as Parent master
`475c2709f4ae0853f360a8b5dbcd754532c9b52d`. All 14 resulting-master GitHub
Actions workflows passed. Of 21 terminal master check runs, 18 succeeded, two
were expected skips, and only SonarCloud `89500782366` failed.

That failure's exact SHA-bound analysis
`baed7ff9-ca24-47a6-9cc1-5ba6744193f7` has the established global signature:
new reliability rating `5`, security rating `5`, and hotspot review `0.0%`
fail; maintainability is `1` and duplication is `0.4%`. The final #109/master
diff changes exactly five Parent test/documentation paths, leaves the HAProxy
runtime and both hotspot-bearing source files unchanged, and has no gitlink,
Framework, or MRTS path. The normal branch-update merge inherited only
already-present master history from PR #117 under the user's narrow approval;
Framework and MRTS were not checked out, changed, tested, merged, or
delivered. This is a revalidation of the separately tracked global
`FND-SONAR-0001` baseline, not a #109 regression. No source, external Sonar
disposition, suppression, scanner/Gate, or risk-acceptance state changed;
status remains `blocked`.

### Post-PR #110 current-master revalidation — 2026-07-24

Protected PR #110 exact head `e13b86f15d69dc2758c197c3e7faeac07bfebff3`
passed all 39 terminal PR check runs (33 `success`, six expected `skipped`),
all six protected required checks, and its SonarQube Cloud PR Quality Gate
`OK` with zero PR issues and zero security hotspots. It was then
protected-squash-merged as Parent master
`5f831257949f4b2655347e2f8bcb2dd5e094a260`. All 14 resulting-master GitHub
Actions workflows passed. Of 21 terminal master check runs, 18 succeeded, two
were expected skips, and only SonarCloud `89507709322` failed.

That failure's exact SHA-bound analysis
`57e1639e-b414-4179-8609-eb4e0598bc4d` has the unchanged global signature:
new reliability rating `5`, security rating `5`, and hotspot review `0.0%`
fail; maintainability is `1` and duplication is `0.4%`. The same three
`TO_REVIEW` `python:S5332` hotspots remain at the two report-layout locations
and the system-environment-proof location. The final #110/master diff changes
exactly seven Parent test/documentation paths, leaves all three hotspot-bearing
sources and the HAProxy runtime unchanged, and has no gitlink, Framework, or
MRTS path. The normal branch-update merge inherited only already-present master
history under the user's narrow approval; Framework and MRTS were not checked
out, changed, tested, merged, or delivered. This is a revalidation of the
separately tracked global `FND-SONAR-0001` baseline, not a #110 regression. No
source, external Sonar disposition, suppression, scanner/Gate, or
risk-acceptance state changed; status remains `blocked`.

### Post-PR #111 current-master revalidation — 2026-07-24

Protected PR #111 exact head `2549d15f3181d236eeb83829818a6b03b273edcd`
passed all 39 terminal PR check runs (33 `success`, six expected `skipped`),
all six protected required checks, and its SonarQube Cloud PR Quality Gate
`OK` with zero PR issues and zero security hotspots. It was then
protected-squash-merged as Parent master
`8e36b86ac17bce06003b0505fe26f6bb60c3cec7`; its tree equals the reviewed PR
head. All 14 resulting-master GitHub Actions workflows passed. Of 21 terminal
master check runs, 18 succeeded, two were expected skips, and only SonarCloud
`89516958783` failed.

The SHA-bound analysis `cbb65f1a-1990-40d0-80ea-8a000cd0c970` has the same
global signature as immediate predecessor analysis
`57e1639e-b414-4179-8609-eb4e0598bc4d`: new reliability rating `5`, security
rating `5`, and hotspot review `0.0%` fail; maintainability is `1` and
duplication is `0.4%`. The same three `TO_REVIEW` `python:S5332` hotspots
remain at the two report-layout locations and the system-environment-proof
location. The final #111/master diff changes exactly nine Parent
CI-checker/documentation paths and contains no hotspot-bearing source,
HAProxy-runtime, gitlink, Framework, or MRTS path. This is a revalidation of
the separately tracked global `FND-SONAR-0001` baseline, not a #111
regression. No source, external Sonar disposition, suppression, scanner/Gate,
or risk-acceptance state changed; status remains `blocked`.

Evidence: `sonar-pr111-master-8e36b86-triage.json`
(`sha256:4c5155e4fbf335e0348036da7179b03c76e76d536c08c94aeeecd0f997f58bb9`).

### Post-PR #112 current-master revalidation — 2026-07-24

Protected PR #112 exact head `9687e5b295f7bbe1c183ba5d46097e7c84eb151c`
passed all 39 terminal PR check runs (33 `success`, six expected `skipped`),
all six protected required checks, and its SonarQube Cloud PR Quality Gate
`OK` with zero PR issues and zero security hotspots. It was then
protected-squash-merged as Parent master
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0`; its tree equals the reviewed PR
head. All 14 resulting-master GitHub Actions workflows passed. Of 21 terminal
master check runs, 18 succeeded, two were expected skips, and only SonarCloud
`89523003340` failed.

The SHA-bound analysis `2236aa46-8e7d-4f98-8c21-679f5de23a50` has the same
global signature as immediate predecessor analysis
`cbb65f1a-1990-40d0-80ea-8a000cd0c970`: new reliability rating `5`, security
rating `5`, and hotspot review `0.0%` fail; maintainability is `1` and
duplication is `0.4%`. The same three `TO_REVIEW` `python:S5332` hotspots
remain at the two report-layout locations and the system-environment-proof
location. The final #112/master diff changes exactly five Parent
test/documentation paths and contains no hotspot-bearing source,
HAProxy-runtime, gitlink, Framework, or MRTS path. This is a revalidation of
the separately tracked global `FND-SONAR-0001` baseline, not a #112
regression. No source, external Sonar disposition, suppression, scanner/Gate,
or risk-acceptance state changed; status remains `blocked`.

Evidence: `sonar-pr112-master-a99bd0b-triage.json`
(`sha256:27e26724404b7b212bb7080a90292723f0a671fa22f1c3becbc986dddd118db2`).

## Observed behavior / Beobachtetes Verhalten

Latest master `a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` has 21 observed
check runs: 18 succeeded, two were expected skips, and only SonarCloud failed.
All 14 triggered GitHub Actions workflows passed, including CodeQL run
`30105722349` and OpenSSF Scorecard run `30105722194`. The latest Sonar
quality gate is `ERROR` only for new security rating `5` and hotspot-review
`0.0%`; reliability is `5`. The three
unreviewed hotspots remain at
`ci/checks/documentation/check-generated-report-layout.py:42`, `:49`, and
`ci/evidence/reports/generate-system-environment-proof.py:98`. No hotspot
review, scanner suppression, gate change, or risk acceptance was made.

The separate four regular `python:S5332` Vulnerability keys remain externally
open after exact-master source-to-sink review. The HAProxy and Envoy helpers
are loopback-only harnesses, the bilingual-document checker only classifies
remote links locally, and the response-header backend is loopback-only test
fixture infrastructure. No source patch or scanner-control change was made.

Separately, three adjacent pythonsecurity:S2083 rows in the local runtime-root
audit renderer carry their JSON payload only to report text, never to an output
path. Two further S2083 rows in refresh-connector-reports.py carry retained
report or command text only to write_text content while the report catalog
chooses the independent destination path. A further S5443 row is a test-only
TemporaryDirectory constructor that securely creates its private parent before
test child paths are derived. All six exact-master local results are
not_actionable; no source patch or scanner-control change was made.

The distinct current `pythonsecurity:S8707` issue
`AZ9cRyfJHhV2CayPTPxt` at
`ci/runtime/common/response-header-test-backend.py:101` exposed a real local
containment gap: `--fixture-file` reached `Path.read_text` without the
`--safe-root` control already used for `--body-file`. The local Parent repair
now resolves fixture paths through the same canonical regular-file and
safe-root check before JSON loading. Direct external-fixture and in-root
symlink escapes reproduce before the repair and are rejected after it; the
valid in-root declarative fixture control remains covered. No delivery or
external Sonar action has occurred.

The separate current `pythonsecurity:S8707` issue
`AZ9cRynaHhV2CayPTPzR` at
`connectors/lighttpd/harness/lighttpd_http1_entity_fixture_upstream.py:47`
exposed a real local output-containment gap: CLI `--ready-file` and
`--result-file` reached JSON publication without a declared safe root, and the
helper used a predictable `.{path.name}.tmp` sibling before replacing the final
path. The local Parent repair requires `--safe-root`, rejects direct outside
paths, symlinked-directory escapes, and final symlink control files before
listening, and writes through `mkstemp` plus `os.replace`. The pre-fix test
reproduced `result.json` becoming a symlink after a pre-placed
`.result.json.tmp` symlink; the post-fix tests reject that bypass and preserve
the valid JSON publication contract. No delivery or external Sonar action has
occurred.

## Current 2026-07-21 update / Aktuelles Update vom 2026-07-21

PR #72 final head `486aef56424f5bf33bcd7396f6dc2f881f7f3bdd` was
squash-merged as current master
`0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`; both trees are
`f5decb679205a57b2b7b1d901003f908815d4f90`. Its task-owned Sonar PR result
passed with zero new issues/hotspots and `0.0%` duplication. The master result
remains independently `ERROR` only for the same three `python:S5332` hotspots
and security rating `5`; reliability and maintainability are `1`, and
duplication `0.4%` passes its `3%` threshold.

The current hotspot source blobs are
`890e39421f36495da2b87c242e72bd13f122d69f` for
`check-generated-report-layout.py` and
`37ea2ec2fb9f81e843e4d506bcc6c2055266ecbe` for
`generate-system-environment-proof.py`. They preserve the source/control/sink
assessment: forbidden-protocol detector literals and the HTTP negative vector
never reach an HTTP client, download, socket, credential, or subprocess sink.
Removing or concealing them would weaken or evade the HTTPS-only control.

Retained evidence is
`/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-pr72-master-validation-20260721T000550Z-final.json`,
SHA-256 `667e2642b90988cf25096ab96c176f6af66f22bb873b3eb6e937d8dc72a1b9f3`.
No external Sonar disposition, source suppression, Quality-Gate change, or
risk acceptance was made.

### Independent public recheck — 2026-07-21T00:34:45Z

An independent public readback confirmed Parent master
`0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` unchanged. The Quality Gate is
`ERROR` because security rating `5` and hotspot review `0.0%` fail;
reliability/maintainability remain `1` and duplication `0.4%` passes. Exactly
three `TO_REVIEW` `python:S5332` hotspots remain:
`AZ7K5CRYixFPtcnbna1R` at
`ci/checks/documentation/check-generated-report-layout.py:42`,
`AZ7K5CRYixFPtcnbna1S` at
`ci/checks/documentation/check-generated-report-layout.py:49`, and
`AZ7K5CQgixFPtcnbna1J` at
`ci/evidence/reports/generate-system-environment-proof.py:98`. The retained
receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/sonar-current-master-recheck-20260721T003445Z-final.json`,
SHA-256 `59bc405a7b822a62c0d134321b497d0f2e0931f8c3ef2be685f3eb3adff3a060`.
It confirms the prior `already_safe` source/control/sink assessment; no source,
hotspot-review, suppression, scanner/gate, false-positive, risk-acceptance,
Framework, MRTS, or gitlink action occurred. Status remains `blocked`.

## Current regular S5332 Vulnerability triage — 2026-07-21T02:02:13Z

Exact-master review of four regular `python:S5332` `VULNERABILITY` rows found
no reachable product network boundary and requires no source change:

- `AZ9cRysWHhV2CayPTP0c` —
  `connectors/haproxy/harness/haproxy_htx_smoke_helper.py:174`, blob
  `efc406f490f1a76cd151b31911e5c2e8196c4e90`: the supported runtime runner
  constructs every probe URL on `127.0.0.1`; a manually supplied CLI URL is a
  same-privilege local operator action, not remote SSRF.
- `AZ9MwivX-bUaKQ_zSGAh` —
  `connectors/envoy/harness/envoy_smoke_helper.py:197`, blob
  `4a999c53f1c246ec431d5e1f3d0f0d910c3b6c71`: the adjacent test server binds
  to `127.0.0.1`, and both supported Envoy runners build loopback-only probes.
- `AZ9cRyW7HhV2CayPTPur` —
  `ci/checks/documentation/check-bilingual-docs.py:15`, blob
  `6c6be14680dd9f9e50c08367d0038de5053f7a9b`: `REMOTE_PREFIXES` rejects
  remote links before filesystem resolution; the module has no HTTP client or
  other network sink.
- `AZ9cRyfJHhV2CayPTPxs` —
  `ci/runtime/common/response-header-test-backend.py:191`, blob
  `fed58d05fbf3897d8e0d19299048c2310773c092`: the fixture binds only to
  `127.0.0.1` and retains its safe-root, regular-file, size, header, and
  framing controls.

All four have the technical disposition `not_actionable` with high confidence.
They were unchanged from exact inventory master
`f2376bb3e39ffbe9d36faca8bcd7397477eadd10`; no code, suppression, rule,
Quality-Gate, hotspot-review, false-positive, Framework, MRTS, gitlink, or
risk-acceptance state changed. The retained receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260720T213808Z-sonar-external-evidence-76c763a2/evidence/sonar-s5332-regular-vulnerability-current-master-triage-20260721T020213Z.json`,
SHA-256 `710339515e3f89b89b560209c39788db5b008cc2e03dc742dc357cfbd4ffd6d5`.
Changing an external issue to false positive still requires a current explicit
user decision and a fresh exact-master readback. The result covers only these
four keys; its then-untriaged exact-inventory Parent scope was 202 rows. The
following audit-renderer S2083 triage reduced the then-current scope to 199
rows; the later refresh-report S2083 triage reduced it to 197, and the current
secure-TemporaryDirectory S5443 triage reduces it to 196.

## Earlier audit-renderer S2083 Vulnerability triage — 2026-07-21T02:37:33Z

Exact-master review of the three adjacent pythonsecurity:S2083 VULNERABILITY
rows at ci/evidence/reports/audit-full-lifecycle-runtime-roots.py:339-341,
blob edc6ff23aa3e3527e370edf0e0a4ffbecab0ecb6, found no payload-to-path flow:

- AZ9cRygDHhV2CayPTPxy at line 339 writes serialized payload as the content
  argument of args.output_json.write_text(...).
- AZ9cRygDHhV2CayPTPxx and AZ9cRygDHhV2CayPTPxz at lines 340 and 341 write
  markdown(payload, "en") and markdown(payload, "de") as content.
- Sonar traces the parsed JSON object from read_object line 79 through payload
  line 303. The three required output Path values are independent argparse
  arguments; no payload value is assigned to, concatenated into, or otherwise
  propagated to an output path.

The local CLI can re-render a caller-selected retained JSON file, but exact-name
searches in ci, tests, Makefile, and .github found no automatic Parent caller.
The source itself has no HTTP server/client entry point despite the scanner's
generic HTTP-source label. Thus the scanner flow reaches text being written,
not the filesystem target required for a path-injection claim.

All three have the technical disposition not_actionable with high confidence;
no source change is required. The retained receipt is
/var/tmp/codex/ModSecurity-conector/runs/20260721T022325Z-sonar-s2083-current-triage-fcf66308/evidence/sonar-s2083-runtime-root-audit-triage-20260721T023733Z.json,
SHA-256 9a361f2ed67a4a0fa1dae11f6107ca2cd8fe7c88dd2557c84c2473dee3318d9c.
No source, suppression, rule, Quality-Gate, hotspot-review, false-positive,
Framework, MRTS, gitlink, or risk-acceptance state changed. An external
false-positive disposition remains subject to a current explicit user decision
and fresh exact-master readback. At the end of this audit-renderer cluster, the
local cumulative work covered seven regular keys and 199 exact-inventory Parent
Vulnerability rows remained untriaged. The later refresh-report cluster below
reduces the current bounded backlog to 197 rows.

### Refresh-report S2083 cluster / Refresh-Report-S2083-Cluster — 2026-07-21T02:56:57Z

Exact-master review of `refresh-connector-reports.py`, blob
`696aa3d1e447090f483369243c7d1b15ab9ac1c8`, found no payload-to-path flow for
the two further current `pythonsecurity:S2083` rows:

- `AZ9cRyiqHhV2CayPTPyS` at line 281 writes `"".join(retained)` as the
  content of `path.write_text`; the source flow from `path.read_text` never
  reaches the independent `path` receiver.
- `AZ9cRyiqHhV2CayPTPyR` at line 1063 writes retained report or command text
  as content; `mark_retained_markdown` receives its path only from
  `primary_output_paths` built from the static `GENERATED_REPORTS` catalog.
- The supported Make callers supply explicit checkout/runtime roots. Those
  operator roots, not report content or `blocked_reason`, select the output
  location. The inspected file imports only standard-library modules and no
  project HTTP request handler reaches these functions.

Both are technically `not_actionable` with high confidence, require no source
change, and remain externally `OPEN`. Retained evidence is
`/var/tmp/codex/ModSecurity-conector/runs/20260721T022325Z-sonar-s2083-current-triage-fcf66308/evidence/sonar-s2083-refresh-connector-reports-triage-20260721T025657Z.json`,
SHA-256 `3f73655e0a861a0b39d8987eafea08e33ef3b66e3625c3925fb0777cc315ae4f`.
No source, suppression, rule, Quality-Gate, hotspot-review, false-positive,
Framework, MRTS, gitlink, or risk-acceptance state changed. At the end of this
cluster the local scope was nine regular keys with 197 exact-inventory Parent
Vulnerability rows untriaged; the current S5443 triage below reduces it to
196. Any external disposition still needs a current explicit user decision and
a fresh exact-master readback.

### Clang temporary-directory S5443 cluster / Clang-Temporary-Directory-S5443-Cluster — 2026-07-21T03:12:22Z

Exact-master review of `tests/test_clang_analysis_baseline.py`, blob
`0b8a34b44453faed5de129a13ec186de2e12c5eb`, found the current
`python:S5443` key `AZ9gJKOrg304P0Qlak6y` at line 41 technically
`not_actionable`:

- The affected statement is `tempfile.TemporaryDirectory` with a constant
  prefix and optional `TMPDIR` parent. All seven local callers use it as a
  context manager before they derive test child paths.
- `TemporaryDirectory` uses the standard-library `mkdtemp` security rules.
  Python documents race-safe creation and a newly created directory accessible
  only by its creating user, including when the parent is a shared temporary
  directory: <https://docs.python.org/3/library/tempfile.html>.
- `TMPDIR` is a same-privilege test-launcher environment setting, not remote
  request data. The focused eight-test contract suite passed, including
  relative and symlink-escaping path rejection before runner writes.

No source change is required. Retained evidence is
`/var/tmp/codex/ModSecurity-conector/runs/20260721T022325Z-sonar-s2083-current-triage-fcf66308/evidence/sonar-s5443-clang-tempdir-triage-20260721T031222Z.json`,
SHA-256 `87d162bf24ab136cbc00e841b3cb9f2a8637aea81d34f8301ebaae5a1f176b98`.
No source, suppression, rule, Quality-Gate, hotspot-review, false-positive,
Framework, MRTS, gitlink, or risk-acceptance state changed. The current local
cumulative scope is ten regular keys with 196 exact-inventory Parent
Vulnerability rows untriaged at this historical point. The response-header
S8707 repair below raises the covered scope to eleven rows and the Lighttpd
S8707 repair raises it to twelve, reducing the bounded backlog to 194; the ten
not_actionable external dispositions still need a current explicit user
decision and fresh exact-master readback.

### Response-header fixture S8707 source fix / Response-Header-Fixture-S8707-Source-Fix — 2026-07-21T03:37:23Z

Exact current Parent master has `pythonsecurity:S8707` key
`AZ9cRyfJHhV2CayPTPxt` at
`ci/runtime/common/response-header-test-backend.py:101`, source blob
`fed58d05fbf3897d8e0d19299048c2310773c092`. The optional `--fixture-file`
was handed to `load_fixture_file` and then `Path.read_text` without the
existing `--safe-root` containment enforced for `--body-file`. Supported
Apache and NGINX harnesses already generate the fixture under `RUNTIME_ROOT`
and pass that root, so this was a broken same-identity CLI file-read boundary,
not a remote exploit claim.

The Parent-only repair generalizes the established resolver. It preserves
`--body-file`'s error label and `MAX_BODY_BYTES` bound, and validates an
optional fixture as a canonical regular file inside a declared root before it
is loaded. It deliberately preserves the fixture's previous unbounded-size
behavior. The real-CLI regression first failed as intended because both a
direct outside-root fixture and an in-root symlink to one left the loopback
server running. After the repair, both fail before listening; the backend
module passed all six tests, Python compilation, adjacent Apache and
full-lifecycle contract suites, and an independent security diff review.

Retained evidence is
`/var/tmp/codex/ModSecurity-conector/runs/20260721T033717Z-sonar-s8707-response-header-fix-5d88e02f/evidence/sonar-s8707-response-header-fixture-fix-20260721T033723Z.json`,
SHA-256 `80922e5534416cbfc66145e2707b6bcbff0a1633ab3e24db09f8a54b7205fbf8`.
The local result is `fixed`; no staging, commit, push, PR, Sonar disposition,
suppression, rule/gate change, Framework/MRTS/gitlink action, or risk
acceptance occurred. It is not a false-positive candidate: external `OPEN`
state requires a separately authorized delivered head and fresh Sonar analysis.
The cumulative local scope at this point covered eleven regular rows with 195
exact-inventory Parent Vulnerability rows still untriaged; the following
Lighttpd S8707 repair raises the local scope to twelve rows and 194 remaining.
The three unrelated hotspots still keep this aggregate `blocked`.

### Lighttpd entity-fixture S8707 source fix / Lighttpd-Entity-Fixture-S8707-Source-Fix — 2026-07-21T04:31:04Z

Exact current Parent master has `pythonsecurity:S8707` key
`AZ9cRynaHhV2CayPTPzR` at
`connectors/lighttpd/harness/lighttpd_http1_entity_fixture_upstream.py:47`,
source blob `e64d11434ccff675a0470ed1d3d1a053c3c7978d`. The helper accepted
CLI `--ready-file` and `--result-file` output paths and passed them to
`write_json`. `write_json` used a predictable sibling `.{path.name}.tmp`,
wrote JSON through that path, and then replaced the requested target. The sole
supported caller creates `$FIXTURE_DIR` below the Lighttpd smoke directory and
passes fixed `upstream-ready.json` and `result.json` children.

The Parent-only repair adds required `--safe-root` handling to the helper and
updates the runner to pass `--safe-root "$FIXTURE_DIR"`. Both output paths are
resolved before the listener starts and must be fresh absolute descendants of
that root. Direct outside-root paths, symlinked-directory escapes, and final
symlink control files are rejected. JSON publication now uses
`tempfile.mkstemp`, `os.fdopen`, `os.fsync`, `os.replace`, and cleanup, which
preserves sorted, indented, newline-terminated JSON and same-directory atomic
replacement without using a predictable temporary filename.

The focused pre-fix regression failed as intended: a pre-placed
`.result.json.tmp` symlink caused the old implementation to leave
`result.json` as a symlink. After the repair,
`tests.test_lighttpd_http1_entity_fixture_upstream` passed seven tests, Python
compilation passed for the helper and test, and the full Lighttpd patched-host
contract suite passed 16 tests. Retained evidence is
`/var/tmp/codex/ModSecurity-conector/runs/20260721T043051Z-sonar-s8707-lighttpd-fixture-output-fix-1725c7b1/evidence/sonar-s8707-lighttpd-fixture-output-fix-20260721T043051Z.json`,
SHA-256 `94f14a450f447fcea4095914309b4e1a8290ef41376520863a8981b319a3adfb`.
The local result is `fixed`; no staging, commit, push, PR, Sonar disposition,
suppression, rule/gate change, Framework/MRTS/gitlink action, or risk
acceptance occurred. It is not a false-positive candidate: external `OPEN`
state requires a separately authorized delivered head and fresh Sonar analysis.
The cumulative local scope now covers twelve regular rows with 194 exact-
inventory Parent Vulnerability rows still untriaged; the three unrelated
hotspots still keep this aggregate `blocked`.

## Current 2026-07-19 update / Aktuelles Update vom 2026-07-19

The superseding retained public baseline for current remote master
`aabde81a9a315bf3e494e595ab0399357c596f9c` again reports Quality Gate
`ERROR`: new reliability rating `5`, new security rating `5`, and new-hotspot
review `0.0%` fail; new maintainability rating `1` and duplication `0.5%`
pass. It contains 1,451 open issues and three unreviewed hotspots. There are
209 Parent-only OPEN vulnerabilities: five exact static/loopback records are
locally already safe for their stated concern, while 204 remain candidates.
Nested Framework/MRTS scope contamination is independently tracked in
`FND-SONAR-0004`; no source, gate, suppression, hotspot-review, or
risk-acceptance change was made.

## Current 2026-07-20 update / Aktuelles Update vom 2026-07-20

Resulting Parent master
`fde2e02a1cf2226f8e9106e663e05e9b2941357e` again has Quality Gate ERROR:
three Security Hotspots plus New Security and Reliability Rating E. Immediate
predecessor `9ef0619b9c00729c16b7056943d7843785223095` has the identical
signature, while exact PR #57 head
`5f8949b1d98a98127b933e9f1d626b30e3291b59` passed with zero new issues and
zero hotspots. The exact master has 18 successful and two expected-skipped
check runs, one SonarCloud failure, and all 14 GitHub Actions workflows pass.
The current 230 open Bug/Vulnerability records (219 vulnerabilities and 11
bugs) are an untriaged multi-file backlog; no #57 attribution is supported.

The three `TO_REVIEW` `python:S5332` hotspots were created on 2026-06-15 and
are outside #57's eight-file diff:

- `AZ7K5CRYixFPtcnbna1R` —
  `ci/checks/documentation/check-generated-report-layout.py:31`
- `AZ7K5CRYixFPtcnbna1S` —
  `ci/checks/documentation/check-generated-report-layout.py:38`
- `AZ7K5CQgixFPtcnbna1J` —
  `ci/evidence/reports/generate-system-environment-proof.py:98`

They are deliberate insecure-repository-URL rejection inputs, but this is not
a safe-hotspot disposition. No Sonar review state, scanner suppression,
quality gate, source, Framework, MRTS, or risk-acceptance state changed.

## Current 2026-07-20 post-PR #61 update / Aktuelles Post-PR-#61-Update vom 2026-07-20

Protected PR #61 was marked ready only after its current exact head
`c9b505a7a0f697318a57f42fe30493038ef03527` had passing required checks,
CodeQL, zero review threads, and SonarQube Cloud Quality Gate `OK` with zero
new issues/hotspots and `0.0%` new-code duplication. It was squash-merged as
Parent master `6bba8206de1bb598b40f76677943e86770b6992c`; its tree exactly
equals the reviewed head, whitespace validation passes, and no Framework/MRTS
gitlink changed.

All 14 resulting-master GitHub Actions workflows pass. The exact SHA-bound
SonarCloud check `88361885739` fails because reliability/security remain E and
the three `python:S5332` hotspots remain unreviewed. Sonar analysis history
names `6bba820...` as the latest master revision. The public current inventory
is 220 open vulnerabilities, 9 open bugs, 845 code smells, 3 hotspots, and
2,035 duplicated lines; this is a small real reduction from the retained
post-#57 inventory (230 Bug/Vulnerability records, 915 code smells, and 2,069
duplicated lines), not a complete quality-gate remediation.

The resulting status is `master_integration_partial`. No hotspot review,
source or scanner suppression, gate change, Framework/MRTS action, or risk
acceptance occurred. The retained exact-master receipt is
`.codex/runs/20260720T131144Z-pr61-master-integration-6bba820/evidence/pr61-master-6bba820-sonar-postmerge.md`
with SHA-256
`8016ace97659e99be38c8eb57d2e8216b8f8fa16bbc89b9ef69744000fadf2ac`.

## Current Draft PR #66 follow-up update

Exact Draft PR #66 successor head 91fea6d05850cc5aeef8ce7fb66a4123ac14e190
passes SonarCloud check 88453362314, Quality Gate OK, and zero
open/confirmed/reopened Bugs. The two task-owned Traefik c:S5489 keys
AZ-A5siIrAfWDxf7qa7r and AZ-A5siIrAfWDxf7qa7s plus surfaced HAProxy c:S3519
key AZ-A5sdsrAfWDxf7qa7q are CLOSED/FIXED by analysis
3263335b-3f73-4bdd-bdbe-e5e525760547. The retained successor receipt is
sonar-pr-66-91fea6d-success-analysis.json, SHA-256
e29d39badd5263d2a27844281e95d8e251172e003d2c4556beaeecddf8381847.

Those are two independent child root causes: requested FND-SONAR-0007 contains
the Traefik lock-identity pair and requested FND-SONAR-0008 contains HAProxy
source-extent validation. The canonical .codex/findings mount is read-only, so
their directories cannot be allocated. Complete pending EN/DE/JSON import
triplets are retained in the task evidence with JSON SHA-256
c722a69da3f5d72f767a42adeab5c1c07cd484f5c878aebd6d5fa26da47e4992 and
0fc6a52f9845c58b18d02e5bf468cd5095e98bc9da0e4f836133254b31e204ea. This
storage limitation does not turn the two repairs into a master verification
and does not resolve this independent aggregate blocker.

## Expected behavior / Erwartetes Verhalten

Current evidence must be rerun against a known revision before this finding can advance beyond blocked.

## Impact / Auswirkung

Release and assurance claims remain bounded by the recorded evidence.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `ci/checks/documentation/check-generated-report-layout.py`
- `ci/evidence/reports/generate-system-environment-proof.py`

### Symbols / Symbole

- `Sonar check 87720810615`
- `Sonar check 88053560480`
- `Sonar check 88361885739`
- `3 Security Hotspots`
- `Security Rating E`
- `Reliability Rating E`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '187,196p;212,214p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:187-196,212-214`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '187,196p;212,214p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260717T181659Z-codeql-action-4-37-1-batch-36346991`
  - Artifact:
    `https://sonarcloud.io/api/qualitygates/project_status?analysisId=9c69bb17-16b6-4ad1-85f1-ee68b55fd2ee`
  - Type: `direct_sonarcloud_current_master_quality_gate_api`; checksum:
    not applicable to direct API evidence.
  - Command: `curl SonarCloud quality-gate API by current analysis ID, then compare condition set to preceding analysis ca8887e8-6f8e-40ff-8b26-6db70cfb8d7f`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T19:00:46Z`; retention:
    `direct_external_api_receipt`
- Run ID: `20260718T053406Z-pr-51-master-integration-546d9dc2`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/master-c8ca0d9-sonar-preexisting-comparison.md`
  - Type: `current_master_sonar_preexisting_condition_comparison`; SHA-256:
    `9f86277f2e150d31ca5109e71ef8952766c50414c7284489cd72f58ce870ef7d`
  - Command: `rtk gh api exact check-runs for current master c8ca0d92b630c18232b881855c4f5d1482568ea6, immediate parent 635b8f603f852cff10926cd6f5449e763f6194a4, and PR head 2589c085a1ed7bbb2c2033635f06e71f5f75fb8b`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-18T06:40:39Z`; retention:
    `retained_task_evidence`

- Run ID: `20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b/evidence/sonar-baseline-project.json`
  - Type: `paginated_current_sonarcloud_project_quality_gate_baseline`;
    SHA-256: `35fbcd6c1a05903e07a0caa19990cec5844155bf34f094bae19b5dfaa2a3e6a5`
  - Producer: RTK-proxied public SonarQube Cloud V1 project, branch, measures,
    quality-gate, issue, and hotspot readback with paginated retained baseline;
    working directory `/root/git/ModSecurity-conector`; exit code `0`;
     observed `2026-07-19T13:18:35Z`; retention `retained_task_evidence`.
- Run ID: `20260719T134711Z-sonarcloud-parent-remediation-current-3de21a87`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260719T134711Z-sonarcloud-parent-remediation-current-3de21a87/evidence/sonar-baseline-project.json`
  - Type: `paginated_superseding_current_sonarcloud_project_quality_gate_baseline`;
    SHA-256: `4e4571357660a4a7677529674020340db370c77b065c8e08119e6f079e80f982`
  - Producer: RTK-proxied public SonarQube Cloud V1 exact-current project,
    branch, measures, quality-gate, issue, and hotspot readback with complete
    retained pagination; working directory `/root/git/ModSecurity-conector`;
    exit code `0`; analysis observed `2026-07-19T13:20:27Z`; retention
    `retained_task_evidence`.
- Run ID: `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/pr57-master-fde2-sonar-preexisting-comparison.md`
  - Type: `exact_parent_master_sonar_preexisting_comparison_after_pr57`;
    SHA-256: `c8ddaf7b0de34e0174b573c6d717b989e2a27b0f8e65f264f578c7ab41df9d95`
  - Command: RTK-proxied exact GitHub check-run comparison for Parent
    predecessor `9ef0619...`, PR #57 head `5f8949b...`, and resulting master
    `fde2e02...`, plus public SonarCloud quality-gate, hotspot, and issue
    readback.
  - Working directory: `/root/git/ModSecurity-conector`; exit code `0`;
    observed `2026-07-20T11:01:59Z`; retention `retained_task_evidence`.

- Run ID: `20260720T131144Z-pr61-master-integration-6bba820`
  - Artifact:
    `.codex/runs/20260720T131144Z-pr61-master-integration-6bba820/evidence/pr61-master-6bba820-sonar-postmerge.md`
  - Type: `exact_resulting_parent_master_sonarcloud_and_delivery_receipt`;
    SHA-256: `8016ace97659e99be38c8eb57d2e8216b8f8fa16bbc89b9ef69744000fadf2ac`
  - Command: RTK-proxied exact GitHub merge/check-run/workflow readback plus
    public SonarQube Cloud analysis, quality-gate, measures, issue-facet, and
    hotspot readback for resulting master `6bba820...`.
  - Working directory: `/root/git/ModSecurity-conector`; exit code `0`;
    observed `2026-07-20T13:14:02Z`; retention `retained_task_evidence`.

## Root-cause analysis / Grundursachenanalyse

The current gate failure remains a multi-file Parent-master condition. PR #61
passes its isolated exact-head gate and its resulting master retains the same
three-hotspot/E/E signature while reducing the open Bug/Vulnerability inventory
from 230 to 229. The gate-driving remaining backlog needs individual
source/control/sink triage; no single #61 product-code cause or complete remedy
for the remaining master failure is supported.

## Proposed remediation / Vorgeschlagene Remediation

Obtain an explicitly authorized, individually scoped Sonar remediation
decision, validate source/control/sink and a legitimate control for the
selected record, remediate without scanner evasion or quality-gate weakening,
and rerun the current master gate. A separately explicit user disposition is
required before changing a Sonar hotspot review state.

## Acceptance criteria / Akzeptanzkriterien

- The Parent current-master quality gate passes or every remaining item has a current authorized disposition.
- Directly sourced issue detail is retained without exposing excluded paths.

## Validation plan / Validierungsplan

- Run the authorized Parent Sonar quality gate/check.
- Verify the current SHA and retain the gate result.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- The 220 current open Vulnerabilities need individual technical triage; no
  safe single remediation scope is selected.
- The three current `python:S5332` hotspots lack an evidence-backed technical
  disposition. No risk acceptance, hotspot review, scanner change, or quality
  gate weakening is authorized by this record.

## Related findings / Verwandte Findings

- `FND-CROSS-0005`
- `FND-SONAR-0004`

## Residual risk / Restrisiko

The final Parent master remains blocked by three unreviewed hotspots, security
rating `5`, and a 220-record open-Vulnerability backlog. The HTTP literals are
deliberate insecure-URL rejection controls, but this evidence is not a
safe-hotspot disposition. The untriaged multi-file backlog may contain genuine
defects; no risk has been accepted by the current user.

## Prior authoritative reconciliation / Vorheriger maßgeblicher Abgleich

This section supersedes the historical current-state paragraphs above. PR #66
head `284d0fd858419baf3edc65b48ddb51b589c0505b` was squash-merged as Parent
master `cbd8385ce1b34318c84cf8f4a5a92ef98c83f82a` at
`2026-07-20T20:09:38Z`. All 14 observed resulting-master GitHub Actions
workflow runs passed, but Sonar check `88462334259` / analysis
`6cc3a8ba-3926-4240-b6ec-f2c1f99509ff` failed Quality Gate `ERROR` with new
reliability/security ratings `5`, hotspot review `0.0%`, and three
`TO_REVIEW` `python:S5332` hotspots at
`check-generated-report-layout.py:42`, `:49`, and
`generate-system-environment-proof.py:98`. Maintainability `1` and duplication
`0.4%` pass.

The only externally open Bug is BLOCKER `AZ7b3dgOcO69wzd-_jHv` / `c:S3519` at
`ci/tools/native_modsecurity_oracle.c:131`. Focused source/sink triage is
`already_safe` / `not_actionable` with high static confidence: the static
CI oracle's sole serializer caller supplies literals, bounded local buffers,
or library-defined C strings; no supported attacker-controlled byte span
reaches the traversal. It is not dismissed or treated as a security finding.
No source change, suppression, false-positive disposition, hotspot review,
scanner/Gate change, or risk acceptance was made. Evidence:
`post-merge-master-reconciliation-20260720T202018Z.json`
(`sha256:797efffded6d99d9d5cedb2c092547f7fb812e8a09b18f0cbd11c3cf0c6e514c`)
and `sonar-c-s3519-triage-20260720T202835Z.json`
(`sha256:13095f4fd51b41f0309a370178db863ee22669973a04e58fdd7236fe461a6c52`)
under
`/var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/`.

## Final master reconciliation / Finaler Master-Abgleich

This section supersedes every preceding current-state paragraph. PR #70 exact
head `8d7f8b7283319528cf2c14479fc02399dd215825` passed its 33 terminal PR
checks (six required contexts), Sonar PR Quality Gate `OK`, and zero
reviews/comments/threads before normal protected squash merge at
`2026-07-20T20:38:21Z`. Its resulting Parent master is
`f2376bb3e39ffbe9d36faca8bcd7397477eadd10`; its tree equals the reviewed PR
head tree `d1903f4702d5dcf1de893ba14d5f6ec798368350`.

SonarCloud analysis `e04ce5bc-a9f7-44ce-bb13-8fe25c872d55`, explicitly bound
to that master revision, reports Quality Gate `ERROR`: reliability `1`,
maintainability `1`, and duplication `0.4%` pass; security rating `5` and
hotspot review `0.0%` fail. The only preceding current Bug,
`AZ7b3dgOcO69wzd-_jHv` / `c:S3519`, is now `FIXED`/`CLOSED` at the same
analysis. The final open Bug query returns `0`; the final Bug/Vulnerability
query returns `220`, all Vulnerabilities. Three `python:S5332` hotspots remain
`TO_REVIEW` at the listed paths. The two Traefik `c:S5489` and the HAProxy
`c:S3519` PR-#66 child keys no longer return current issue records; their
separate retained exact-PR evidence remains the source for the blocked
canonical-import state. No evidence supports closing this aggregate finding.

No Framework/MRTS source, gitlink, scanner-control, Quality-Gate, hotspot-review,
suppression, false-positive, or risk-acceptance state changed in this delivery.

## Exact-master S5332 hotspot validation / Exakte S5332-Hotspot-Validierung

This section supersedes the earlier statement that the three remaining hotspots
lacked a technical disposition. Exact-master source/control/sink validation
now classifies `AZ7K5CRYixFPtcnbna1R`, `AZ7K5CRYixFPtcnbna1S`, and
`AZ7K5CQgixFPtcnbna1J` as `already_safe` on
`f2376bb3e39ffbe9d36faca8bcd7397477eadd10`.

- The two checker locations are a forbidden-protocol detector signature and
  a static HTTP negative vector. `urllib.parse.urlsplit` only parses that
  vector locally; it is not supplied to an HTTP client, clone, download,
  credential, socket, or subprocess sink.
- The generator location is the same forbidden-protocol detector signature.
  It performs a text-membership comparison and emits a diagnostic report; it
  does not interpret the string as a URI.
- Exact remote blobs for both files and the Makefile equal the locally tested
  `5a22cbf` blobs: `890e39421f36495da2b87c242e72bd13f122d69f`,
  `37ea2ec2fb9f81e843e4d506bcc6c2055266ecbe`, and
  `970f984452c47a3cfa8a55bcf134cc66ab55ca26`, respectively.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v
  tests.test_generated_report_evidence_integrity` passed 57 tests, and
  `PYTHONDONTWRITEBYTECODE=1 make report-governance` passed. The latter ran
  the HTTPS-only policy's negative and legitimate controls.

Changing the literals to HTTPS would weaken or break the rejection control;
dynamically hiding them solely from Sonar would be scanner evasion. Therefore
the `fix-finding` outcome is `no_change`, not a code patch. The Quality Gate
remains `blocked` only because Sonar still records the three external hotspots
as `TO_REVIEW`. Per the Sonar policy, a current explicit user decision is
required before marking them reviewed/safe; no review, suppression,
false-positive disposition, Quality-Gate change, or risk acceptance occurred.
Evidence is retained as
`post-pr70-master-reconciliation-20260720T204648Z.json`
(`sha256:ac9753d9ba2bb2326ce53c1d9d9e160bb89ca429a18abfd9e0729a0c53366dd5`)
and `sonar-s5332-hotspot-source-triage-20260720T205006Z.json`
(`sha256:13b70c17f11eeb8a50e4c24bc8a9dd57760cef810cb3ef3bd26ae49327cff1dd`)
under `/var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/`.

## Post-PR #69 exact-master reconciliation

PR #69's exact head `2b41add0cfeb442149c4516fcbb1b199d83a86c2` passed its
SonarQube Cloud PR Quality Gate with zero new issues and zero new security
hotspots. It then merged normally by protected squash as Parent master
`5fa90474a79eaee2df034bf1c4389572fdcca42f`.

The resulting master has successful terminal GitHub Actions workflows,
including all six strict required contexts. Its SonarQube Cloud check
`88556930734` nevertheless fails the Quality Gate on exactly the same
three `TO_REVIEW` `python:S5332` hotspots, New Security Rating `5`, and
new-hotspot review `0.0%` as immediate predecessor
`0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` / Sonar check `88506822225`.
Reliability and maintainability remain `1`; duplication `0.4%` passes.

This is an `unrelated_baseline` revalidation of the existing release blocker,
not a regression attributed to PR #69. The retained exact comparison is
`sonar-master-baseline-5fa90474-20260721T061703Z.json`
(`sha256:365ed868587a32ef0876b4ba5e06d8155147d2334c6b4af79ba75d92a826dcf2`)
under
`/var/tmp/codex/ModSecurity-conector/runs/20260721T061646Z-pr65-67-68-69-master-integration-2ee109e2/evidence/`.
No source, external hotspot review, suppression, Quality-Gate, false-positive,
Framework, MRTS, gitlink, or risk-acceptance state changed.

## Post-PR #65 exact-master reconciliation

PR #65's exact head `1ddeb7163076e6e552dc161d8813a46bf24903d0` passed its
SonarQube Cloud PR Quality Gate with zero new issues and zero new security
hotspots. It then merged normally by protected squash as Parent master
`1fa024ca6ec97023ea5b6f7dff5215e43f10b74c`.

All 14 observed resulting-master GitHub Actions push workflows and all six
strict required contexts succeeded. SonarQube Cloud check `88560064918`
nevertheless fails the Quality Gate on exactly the same three `TO_REVIEW`
`python:S5332` hotspots, New Security Rating `5`, and new-hotspot review
`0.0%` as immediate predecessor
`5fa90474a79eaee2df034bf1c4389572fdcca42f` / Sonar check `88556930734`.
Reliability and maintainability remain `1`; duplication `0.4%` passes.

This is a second `unrelated_baseline` revalidation of the existing release
blocker, not a regression attributed to PR #65. The retained exact comparison
is `sonar-master-baseline-1fa024ca-20260721T063155Z.json`
(`sha256:464c31f2f8a3e9d517af13198149f031dd557a89ba870e79d4d179ec98b41b79`)
under
`/var/tmp/codex/ModSecurity-conector/runs/20260721T061646Z-pr65-67-68-69-master-integration-2ee109e2/evidence/`.
No source, external hotspot review, suppression, Quality-Gate, false-positive,
Framework, MRTS, gitlink, or risk-acceptance state changed.

## Post-PR #75 and #76 exact-master reconciliation

Task-owned replacement PR #75 (for Dependabot #67) passed its exact-head
SonarQube Cloud Quality Gate with zero new issues and zero new security
hotspots, then protected-squash merged as Parent master
`5c26ffb698a892ffe83b7aa1749a456eae10b956`. Replacement PR #76 (for
Dependabot #68) then passed the same exact-head Sonar gate and all six strict
required contexts before protected-squash merge as current Parent master
`2ade0d40983b7af21a65b8cd2884866b85626393`.

All 15 resulting-master Actions workflow runs for `2ade0d...` succeeded. Its
22 terminal check runs comprise 19 successes, the two expected skips
`nginx-profile-and-client-preflight` and `same-repository-pull-request`, and
one failure: SonarCloud check `88577130249`. The public Sonar Quality Gate is
`ERROR` solely because New Security Rating is `5` and new-hotspot review is
`0.0%`; reliability and maintainability are `1` and duplication `0.4%` passes.
The exact same three `TO_REVIEW` `python:S5332` hotspot keys remain:
`AZ7K5CRYixFPtcnbna1R` and `AZ7K5CRYixFPtcnbna1S` at
`ci/checks/documentation/check-generated-report-layout.py:42` and `:49`, and
`AZ7K5CQgixFPtcnbna1J` at
`ci/evidence/reports/generate-system-environment-proof.py:98`.

This is a fresh `unrelated_baseline` readback of this existing aggregate
release blocker, not a causal attribution to #75 or #76. No source, external
hotspot review, suppression, scanner/Quality-Gate, false-positive, Framework,
MRTS, gitlink, or risk-acceptance state changed. The retained receipt is
`pr67-pr68-protected-delivery-20260721T080505Z.json`
(`sha256:2010d3a79b1d590b1e2fc65dabd928b4850eea0ccae87b2636802cf073018015`)
under
`/var/tmp/codex/ModSecurity-conector/runs/20260721T071522Z-pr67-68-action-lock-replacements-45705602/evidence/`.

## Post-PR #99 exact-master reconciliation

Protected Parent PR #99 exact head
`2f0d8a234f984b731229aca01d43caf2749a7d61` passed its exact-head
SonarQube Cloud Quality Gate with zero new issues and zero new security
hotspots. It was then squash-merged as Parent master
`5b8db00d44ab24f3a9f4216a00f7edee977b6898`. All 15 resulting-master GitHub
Actions workflows succeeded.

The additional exact-master SonarCloud check `89321542088` nevertheless failed
the Quality Gate solely on New Security Rating `5` and new-hotspot review
`0.0%`; reliability and maintainability are `1` and duplication `0.4%` passes.
It reports the same three `TO_REVIEW` `python:S5332` hotspots as the
pre-merge master `a308d7b414f0859490fe7253e0683a4bde80b563` / Sonar check
`89221608146`. Neither hotspot-bearing file changed across the exact compared
commits; both blob identities are identical. A focused source/control/sink
recheck confirms the literals are static HTTPS-only policy detector data and
negative controls, not network sinks.

This is a fresh `unrelated_baseline` revalidation of the existing aggregate
release blocker, not a causal #99 regression. The retained receipt is
`sonar-master-5b8db00-pr99-postmerge-baseline-recheck.md`
(`sha256:14f086d445d7c21a30c0c6dbf5f475f38343d148a8ae39952d4577157b94ea9e`)
under
`/var/tmp/codex/ModSecurity-conector/runs/20260723T200627Z-pr99-pr100-master-integration-075c1b11/evidence/`.
No source, external hotspot review, suppression, scanner/Quality-Gate,
false-positive, Framework, MRTS, gitlink, or risk-acceptance state changed.

## Post-PR #108 resulting-master Sonar re-triage

Protected PR #108 exact head
`4727d9bddd0100bf1f1cf47150db6832f96b6873` passed all 39 terminal hosted
checks, all six protected required checks, the SonarQube Cloud PR Quality Gate,
and zero PR issues or security hotspots. It was squash-merged as Parent master
`700e62e5c2287e10f8774757ffff7432753900c0`; all 14 resulting-master GitHub
Actions workflows passed.

The SHA-bound master analysis
`7308b325-84f3-4df6-a6b4-ff30fc8f9e3d` / Sonar check `89490754566` nevertheless
failed the project Quality Gate. Alongside the existing three `TO_REVIEW`
`python:S5332` hotspots, it created two open HAProxy BUG rows:
`AZ-URJYx1ap3oKwyiaQ7` / `c:S3519` at line 388 and
`AZ-URJYx1ap3oKwyiaQ8` / `c:S2637` at line 2666. PR #108's final master diff
does not modify that source path.

The exact static source/control/sink review is retained at
`/var/tmp/codex/ModSecurity-conector/runs/20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b/evidence/sonar-pr108-master-700e62e-triage.json`
(`sha256:d4bdc2061441727c4afe199ff349681af95f0cec0b2541e3e82aaaad75d1accd`).
`append_bytes` rejects an oversized source length, an out-of-range destination
offset, and a destination overrun before `memcpy`; its current callers provide
matching source extents. Each affected `fprintf(stderr, ...)` is immediately
dominated by `if (stderr != NULL)`. The focused existing Parent reliability
contract passed all six tests, including both guards. The two rows are therefore
locally `already_safe` / false-positive candidates, not a reportable
high-or-critical security finding and not a causal PR #108 regression.

No external Sonar issue disposition, hotspot review, suppression, scanner or
Quality-Gate modification, source patch, Framework/MRTS action, or risk
acceptance was made. The aggregate remains `blocked`: the project Quality Gate
still has security rating `5`, hotspot review `0.0%`, and mixed-scope backlog
work outside this PR-integration task.

## History / Historie

- `2026-07-29T13:14:43Z`: bounded current-user delivery-risk acceptance — The
  user explicitly stated “ich akzeptiere das rest risiko” after the current
  three-hotspot master baseline was disclosed. The acceptance covers only
  SHA-bound Parent PR #173–#182 delivery while resulting-master Sonar remains
  exactly at the documented non-causal `python:S5332` / security-rating-`5` /
  hotspot-review-`0.0%` signature. It waives no PR-specific gate or security
  control and does not change the global `blocked` P1/release-blocker status,
  external Sonar disposition, scanner/Gate, Framework/MRTS, Gitlink, or
  direct-master policy.
- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T19:00:46Z`: current master gate revalidated as pre-existing —
  current revision `635b8f603f852cff10926cd6f5449e763f6194a4` has the same
  failing condition set as the preceding master analysis; no batch-specific
  regression is supported.
- `2026-07-18T06:40:39Z`: post-merge master gate revalidated as pre-existing —
  master `c8ca0d92b630c18232b881855c4f5d1482568ea6` failed check `88053560480`
  with the same signature as immediate pre-merge master check `87968758684`;
  exact PR #51 head check `88053106295` passed with zero PR issues and
  hotspots. No task-owned master fix, gate weakening, or risk acceptance was
  performed.
- `2026-07-19T13:30:00Z`: current master gate revalidated with paginated scope
  baseline — current master `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f`
  retains Quality Gate `ERROR` with new reliability/security ratings `5` and
  new-hotspot review `0.0%`; new maintainability `1` and duplication `0.5%`
  pass. The analysis has 1,456 open issues and three hotspots. Scope
  contamination is separately recorded in `FND-SONAR-0004`; no source, gate,
  suppression, or risk-acceptance change occurred.
- `2026-07-19T14:09:34Z`: superseding current-master gate revalidated with
  complete pagination — remote master `aabde81a9a315bf3e494e595ab0399357c596f9c`
  has analysis `ab643038-c835-490f-ba36-a621da59de1d` and retains Quality Gate
  `ERROR` with new reliability/security ratings `5` and new-hotspot review
  `0.0%`; new maintainability `1` and duplication `0.5%` pass. It has 1,451
  open issues, three unreviewed hotspots, and 209 Parent-only OPEN
  vulnerabilities. Five exact static/loopback records are locally already safe
  for their stated concern; 204 remain candidates. Four `S5443` records are
  closed in this analysis, but their original regression control was not
  rerun. Scope contamination remains separately recorded in `FND-SONAR-0004`;
  no source, gate, suppression, hotspot-review, or risk-acceptance mutation was
  performed.
- `2026-07-20T11:01:59Z`: post-PR-#57 master gate revalidated as pre-existing
  Parent blocker — resulting master `fde2e02...` has 18 successful and two
  expected-skipped terminal check runs plus failed Sonar check `88333445075`.
  It has the same three hotspots and E/E ratings as predecessor `9ef0619...`
  check `88317800622`; exact #57 head `5f8949b...` passed check `88328644200`
  with zero new issues and hotspots. All 14 master Actions workflows passed.
  No causal attribution, source/gate/hotspot-review mutation, or risk
  acceptance was made.
- `2026-07-20T13:14:02Z`: post-PR-#61 master gate revalidated with small
  backlog reduction — protected PR #61 head `c9b505a...` was squash-merged as
  exact Parent master `6bba820...`; the resulting tree equals the reviewed
  head. All 14 master Actions workflows passed, while terminal Sonar check
  `88361885739` failed with the three-hotspot/E/E signature. SonarCloud names
  `6bba820...` as the analysis revision. The public open Bug/Vulnerability
  inventory fell from the retained 230 to 229 (220 vulnerabilities and 9
  bugs); no hotspot review, source/gate/scanner mutation, causal attribution of
  the remaining failure, or risk acceptance was made.
- `2026-07-21T00:34:45Z`: independent exact-master public Sonar recheck
  confirmed `0e8be81...` unchanged: Quality Gate `ERROR` only on security
  rating `5` and hotspot review `0.0%`; reliability/maintainability `1` and
  duplication `0.4%` pass. The same three `TO_REVIEW` `python:S5332` keys
  remain, preserving the `already_safe` source/control/sink assessment. No
  source, external disposition, suppression, scanner/gate, false-positive,
  risk-acceptance, Framework, MRTS, or gitlink action occurred; status remains
  `blocked`.
- `2026-07-21T06:17:03Z`: post-PR-#69 master gate revalidated as pre-existing
  — PR #69 passed its exact-head Sonar PR Quality Gate, but resulting master
  `5fa90474...` failed Sonar check `88556930734` with the identical
  three-hotspot / Security Rating `5` / hotspot-review `0.0%` signature as
  immediate predecessor `0e8be81...` / check `88506822225`. All resulting
  GitHub Actions workflows and required contexts passed. No Sonar disposition,
  source change, gate change, or risk acceptance occurred.
- `2026-07-21T06:31:55Z`: post-PR-#65 master gate revalidated as pre-existing
  — PR #65 passed its exact-head Sonar PR Quality Gate, but resulting master
  `1fa024ca...` failed Sonar check `88560064918` with the identical
  three-hotspot / Security Rating `5` / hotspot-review `0.0%` signature as
  immediate predecessor `5fa90474...` / check `88556930734`. All 14 resulting
  GitHub Actions workflows and required contexts passed. No Sonar disposition,
  source change, gate change, or risk acceptance occurred.
- `2026-07-21T08:05:05Z`: post-PR-#75/#76 master gate revalidated as
  pre-existing — exact PR heads #75 and #76 passed their Sonar PR Quality
  Gates with zero new issues/hotspots and then protected-squash merged through
  masters `5c26ffb...` and `2ade0d4...`. All 15 observed Actions workflow
  runs for current master `2ade0d4...` passed; its 22 terminal checks have 19
  successes, two expected skips, and only Sonar check `88577130249` failed.
  Public Sonar readback shows the same three `TO_REVIEW` `python:S5332`
  hotspots, Security Rating `5`, and hotspot review `0.0%`; no causal
  attribution, source, gate, scanner, hotspot-review, or risk-acceptance
  change occurred.
- `2026-07-23T04:52:07Z`: protected PR #90 exact head `0a1f603` passed all
  required checks, Quality Gate `OK`, and zero open/confirmed PR leak-period
  issues, then squash-merged as master `ad953cd`. Its exact master analysis
  `93842ace-ff04-4318-ab02-7dd065389f0a` remains Quality Gate `ERROR` only on
  Security Rating `5` and hotspot review `0.0%`; reliability/maintainability
  `1` and duplication `0.4%` pass. The same three `TO_REVIEW`
  `python:S5332` hotspots and validated source blobs remain, while all
  applicable resulting-master GitHub Actions workflows passed. No source,
  hotspot-review, scanner/gate, suppression, false-positive, or risk-acceptance
  action occurred; status remains `blocked`.
- `2026-07-23T07:47:27Z`: protected PR #92 exact head `40a419d` passed its
  Sonar PR Quality Gate with zero new issues/hotspots and squash-merged as
  master `95fb491`. All 14 resulting-master Actions workflows passed. The
  sole failed check was Sonar `89147577049`, with the same three
  `TO_REVIEW` `python:S5332` hotspots, Security Rating `5`, and hotspot review
  `0.0%` as predecessor `ad953cd` / check `89121173685`; reliability,
  maintainability, and duplication pass. Current source blobs equal the prior
  `already_safe` assessment. No causal #92 regression, external disposition,
  suppression, gate change, false-positive action, or risk acceptance is
  evidenced; status remains `blocked`.
- `2026-07-23T20:23:07Z`: protected PR #99 exact head `2f0d8a2` passed its
  Sonar PR Quality Gate with zero new issues/hotspots and squash-merged as
  master `5b8db00`. All 15 resulting-master Actions workflows passed. The
  sole failed check was Sonar `89321542088`, with the same three `TO_REVIEW`
  `python:S5332` hotspots, Security Rating `5`, and hotspot review `0.0%` as
  predecessor `a308d7b` / check `89221608146`; reliability, maintainability,
  and duplication pass. Both hotspot-bearing source blobs are identical across
  the compared commits; focused source/control/sink review confirms static
  policy-detector data rather than a network sink. No causal #99 regression,
  external disposition, suppression, gate change, false-positive action, or
  risk acceptance is evidenced; status remains `blocked`.
- 2026-07-24T08:30:18Z: protected PR #98 exact head a2f2dd1 was
  squash-merged as master 3311f3f. All 14 applicable resulting-master Actions
  workflows passed, and the three targeted PR #98 base Sonar keys are
  CLOSED/FIXED. The public project Quality Gate remains ERROR: Security Rating
  5 and hotspot review 0.0% fail while reliability and maintainability are 1
  and duplication is 0.4%. The same three TO_REVIEW python:S5332 hotspots
  remain. Sonar currently reports 177 open Vulnerability rows across mixed
  Parent, Framework and original-MRTS-indexed components. A bounded static
  triage returns needs_review, because per-entry caller provenance and
  supported security boundaries are not yet established. No external hotspot
  review, suppression, false-positive disposition, scanner/gate change,
  Framework/MRTS action, or risk acceptance occurred; status remains blocked.

- 2026-07-24T08:53:43Z: protected PR #100 exact head `dace5ca` passed its
  SonarCloud PR Quality Gate with zero new issues and zero new hotspots, then
  was squash-merged as master `6c1f571`. All 14 resulting-master GitHub
  Actions workflows passed. Of 21 terminal commit checks, only Sonar
  `89440531005` failed: the global gate keeps Security Rating `5` and hotspot
  review `0.0%`, while reliability/maintainability are `1` and duplication is
  `0.4%`. Direct current API readback confirms the same three low-probability
  `TO_REVIEW` `python:S5332` hotspots and 177 open Vulnerability rows across
  mixed Parent, Framework, and original-MRTS-indexed components. No source,
  external hotspot review/disposition, suppression, scanner/Gate,
  Framework/MRTS, or risk-acceptance action occurred; status remains `blocked`.
- 2026-07-24T09:32:14Z: protected PR #101 exact head
  `f988d627e76c98b7c34f91cb3d82be268750d464` passed all 39 terminal PR
  checks, SonarQube Cloud Quality Gate `OK`, and zero new issues/hotspots,
  then was squash-merged as Parent master
  `215b503a8d68ee85d93e18888f3710d1974c3169`. All 14 resulting-master
  GitHub Actions workflows passed. Of 21 terminal commit checks, only Sonar
  `89447965729` failed with the same Quality-Gate signature: Security Rating
  `5` and hotspot review `0.0%` fail, while reliability/maintainability are
  `1` and duplication is `0.4%`. The final #101 diff contains neither
  hotspot-bearing source file. No external hotspot review/disposition,
  suppression, scanner/Gate, Framework/MRTS, or risk-acceptance action
  occurred; status remains `blocked`.
- 2026-07-24T10:11:50Z: protected PR #102 exact head
  `193fefd120e69807b40d21ffe376b45f50f10208` passed all 39 terminal PR
  checks, SonarQube Cloud Quality Gate `OK`, and zero open PR issues/hotspots,
  then was squash-merged as Parent master
  `ec57576814a3f75c5e153d51c945bd1dd341a916`. All 14 resulting-master GitHub
  Actions workflows passed and its 20 terminal commit checks are only success
  or expected skips; no SonarCloud master check run was published for this
  SHA. The direct public master Quality Gate readback remains `ERROR` with the
  same Security Rating `5` and hotspot review `0.0%` signature, while
  reliability/maintainability are `1` and duplication is `0.4%`. The final
  #102 diff contains neither hotspot-bearing source file. No external hotspot
  review/disposition, suppression, scanner/Gate, Framework/MRTS, or
  risk-acceptance action occurred; status remains `blocked`.
- 2026-07-24T10:57:36Z: protected PR #103 exact head
  `ad1aef95ed62fd906cee1e9b1d507ce07cbc7d54` passed all 39 terminal PR check
  runs, its SonarQube Cloud PR Quality Gate `OK`, and zero new issues/hotspots,
  then was squash-merged as Parent master
  `90e3d8d9603375f9a33e2a51836ba284221fdd0f`. All 14 resulting-master GitHub
  Actions workflows passed. Of 21 terminal master checks, 18 succeeded, two
  were expected skips, and only SonarCloud `89464137047` failed with the same
  three-hotspot / Security Rating `5` / hotspot-review `0.0%` signature as
  predecessor `ec57576814a3f75c5e153d51c945bd1dd341a916` / SonarCloud
  `89456327990`. The final #103 diff contains neither hotspot-bearing source
  file. No external hotspot review/disposition, suppression, scanner/Gate,
  Framework/MRTS/gitlink, or risk-acceptance action occurred; status remains
  `blocked`.
- 2026-07-24T11:37:09Z: protected PR #104 exact head
  `53564d896492945b681d20474d33e2a19a1bc4b5` passed all 39 terminal PR check
  runs, its SonarQube Cloud PR Quality Gate `OK`, and zero new issues/hotspots,
  then was squash-merged as Parent master
  `053a9ca5b0f9351319c96d359107c53ba8f9d3a1`. All 14 resulting-master GitHub
  Actions workflows passed. Of 21 terminal master checks, 18 succeeded, two
  were expected skips, and only SonarCloud `89471250793` failed with the same
  three-hotspot / Security Rating `5` / hotspot-review `0.0%` signature as
  predecessor `90e3d8d9603375f9a33e2a51836ba284221fdd0f` / SonarCloud
  `89464137047`. The final #104 diff contains neither hotspot-bearing source
  file. No external hotspot review/disposition, suppression, scanner/Gate,
  Framework/MRTS/gitlink, or risk-acceptance action occurred; status remains
  `blocked`.
- 2026-07-24T12:01:28Z: protected PR #105 exact head
  `831a6c7a3f8d179b1735ea6e6a0b9ff4d1868bdc` passed all 39 terminal PR check
  runs, its SonarQube Cloud PR Quality Gate `OK`, and zero new issues/hotspots,
  then was squash-merged as Parent master
  `26f0eb9cff2f1c69ba7be9cfc5fd609659e3041f`. All 14 resulting-master GitHub
  Actions workflows passed. Of 21 terminal master checks, 18 succeeded, two
  were expected skips, and only SonarCloud `89475577491` failed with the same
  three-hotspot / Security Rating `5` / hotspot-review `0.0%` signature as
  predecessor `053a9ca5b0f9351319c96d359107c53ba8f9d3a1` / SonarCloud
  `89471250793`. The final #105 diff contains neither hotspot-bearing source
  file. No external hotspot review/disposition, suppression, scanner/Gate,
  Framework/MRTS/gitlink, or risk-acceptance action occurred; status remains
  `blocked`.
- 2026-07-24T12:21:11Z: protected PR #106 exact head
  `43e55c2e54f738ee6d9e969cc8e57ce2831e0874` passed all 39 terminal PR check
  runs, its SonarQube Cloud PR Quality Gate `OK`, and zero new issues/hotspots,
  then was squash-merged as Parent master
  `a60dd0380332a24cf231a36775256d21a812c027`. All 14 resulting-master GitHub
  Actions workflows passed. Of 21 terminal master checks, 18 succeeded, two
  were expected skips, and only SonarCloud `89479343187` failed with the same
  three-hotspot / Security Rating `5` / hotspot-review `0.0%` signature as
  predecessor `26f0eb9cff2f1c69ba7be9cfc5fd609659e3041f` / SonarCloud
  `89475577491`. The final #106 diff contains neither hotspot-bearing source
  file. No external hotspot review/disposition, suppression, scanner/Gate,
  Framework/MRTS/gitlink, or risk-acceptance action occurred; status remains
  `blocked`.
- 2026-07-24T12:47:01Z: protected PR #107 exact head
  `c1168e7a715280d50c4a263285b7d0c09245bc6d` passed all 39 terminal PR check
  runs, its SonarQube Cloud PR Quality Gate `OK`, and zero new issues/hotspots,
  then was squash-merged as Parent master
  `00dfe5f2ae0908228a6242b15e09f70d6742d102`. All 14 resulting-master GitHub
  Actions workflows passed. Of 21 terminal master checks, 18 succeeded, two
  were expected skips, and only SonarCloud `89484279475` failed with the same
  three-hotspot / Security Rating `5` / hotspot-review `0.0%` signature as
  predecessor `a60dd0380332a24cf231a36775256d21a812c027` / SonarCloud
  `89479343187`. The final #107 diff contains neither hotspot-bearing source
  file. No external hotspot review/disposition, suppression, scanner/Gate,
  Framework/MRTS/gitlink, or risk-acceptance action occurred; status remains
  `blocked`.
- 2026-07-27T17:43:56Z: protected PR #128 exact head
  `e9e97895faa1c45178f49ca2aaf60873e12b7c46` passed its protected required
  contexts, SonarQube Cloud Quality Gate `OK`, zero PR issues, zero security
  hotspots, and `0.0%` duplication on new code, then was squash-merged as
  Parent master `1b0f8825f3510b99b603bb6cd6f0777e1710358e`. All 14
  resulting-master GitHub Actions workflows passed. Of 21 terminal checks, 18
  succeeded, two were expected skips, and only SonarCloud `90056181012` failed.
  Direct analysis `6b27b281-df12-42ae-9976-80ea2620b805` has the same three
  TO_REVIEW `python:S5332` hotspots and E reliability/security signature as
  immediate predecessor `7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d` /
  SonarCloud `89923119911`. `check-generated-report-layout.py` is byte-
  identical; the only #128 edit in `generate-system-environment-proof.py` is
  the unrelated line-440 unused-local removal, while hotspot line 98 is
  identical; the two HAProxy reliability rows predate #128 and their source
  blob is unchanged. Retained static triage classifies the three hotspot
  literals as HTTPS-policy detector or negative-test data, not network
  endpoints. No causal #128 regression, external hotspot review/disposition,
  suppression, scanner/Gate change, Framework/MRTS/gitlink action, or risk
  acceptance occurred; status remains `blocked`.

### Draft PR #142 exact-head serializer remediation — 2026-07-27

Draft Parent PR #142 has exact local, origin, and GitHub PR head
`b8080c93b463fb438dd27e9011ef7f440429cd19`. All completed hosted checks
passed, and the public SonarQube Cloud exact-head readback reports Quality Gate
`OK`, zero `OPEN`/`CONFIRMED` PR issues, zero new duplicated lines, and 0.0%
new-code duplication. Receipt `AZ-URJYx1ap3oKwyiaQ7` / `c:S3519` is absent
from that PR issue readback.

The retained, bounded evidence is
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/evidence/pr142-exact-head-observation.json`,
SHA-256 `0e92b1b386db985f1e9af2fb534ea88683405b0f63f06e89df37ffb8f68591f0`.
It verifies only the serializer-local Parent candidate at Draft-PR level. No
master change, external Sonar disposition, policy/gate change, suppression,
exclusion, Framework/MRTS/Gitlink action, Ready-for-review transition, or
merge occurred; the aggregate finding therefore remains `blocked`.

### Scripts workflow-updater S2083 triage — 2026-07-29

The current scripts-scoped SonarQube Cloud inventory contains one issue:
`AZ70CAr3IpeCryPNS2zi` / `pythonsecurity:S2083` at
`scripts/update-github-actions-versions.py:623` on exact Parent master
`fc6027681cfae342dcef8e1606a38523c450044c`. The reported trace begins with
workflow-file content at line 620 and reaches the *content argument* of
`path.write_text` at line 623 after split/join processing. It does not make
that content select or construct the `Path` receiver.

The receiver is independently produced by fixed workflow globs below the
resolved Parent root. `confined_workflow_path` strictly resolves every result,
rejects direct symlinks and non-files, and requires resolved containment below
that root before it can enter the replacement map. The focused updater suite
passed all 25 tests, including the legitimate in-root update and direct
external-workflow-symlink rejection. A controlled ancestor-`.github` symlink
check likewise returned no candidates and left the external workflow unchanged.

The technical disposition is therefore `not_actionable`: no source change is
required or justified. No suppression, rule/Quality-Gate change, external
false-positive disposition, Framework/MRTS/Gitlink action, PR, or merge was
made. The external Sonar issue remains `OPEN`; removing it requires a separately
authorized external false-positive disposition. Retained evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260729-scripts-last-sonar-finding/evidence/sonar-s2083-workflow-updater-triage-20260729T071145Z.json`,
SHA-256 `59ce099f2f9dd2040256d5b0e0ddc051288e596219b45078a3d08eab8c9983ac`.

### Post-PR #175 resulting-master revalidation — 2026-07-29

PR #175 exact head `16959671eff46937910c4ec854a14fe1651d5b96` passed all six
protected required checks, CodeQL, OSV, Secret scanning, and its SonarQube
Cloud PR Quality Gate with zero new bugs, vulnerabilities, and security
hotspots. It was then merged only through the SHA-bound squash request as
Parent master `5bf35f7f50f2ff9ed8b17f538d8043b3909b945b`.

The resulting-master GitHub Actions checks succeeded except SonarCloud check
`90552680188`, which completed at `2026-07-29T10:45:06Z` with Quality Gate
`ERROR`: new security rating is `5` / E and hotspot review is `0.0%`; new
reliability and maintainability ratings are `1` / A and new duplication is
`0.1%`. Direct master API readback returns exactly the pre-existing
`TO_REVIEW` `python:S5332` keys `AZ7K5CRYixFPtcnbna1R`,
`AZ7K5CRYixFPtcnbna1S`, and `AZ7K5CQgixFPtcnbna1J`, all created on
`2026-06-15`.

The two hotspot-bearing paths are unchanged between pre-merge master
`9f23ae2c5fe908cef38f203be03f93fda75a8dd7` and resulting master
`5bf35f7f50f2ff9ed8b17f538d8043b3909b945b`; no remaining authorized target
PR #176, #177, #174, or #173 changes either path. This is a re-observation of
the existing P1 release blocker, not a causal #175 regression. No external
reviewed/safe or false-positive disposition, suppression, scanner/Gate change,
Framework/MRTS/Gitlink action, or risk acceptance occurred. Therefore
`FND-SONAR-0001` remains `blocked` and PR #175 is
`merged_post_validation_failed`; the controlled integration sequence cannot
continue without a separately authorized, scope-correct disposition.

Retained task evidence:
`/var/tmp/codex/ModSecurity-conector/pr-integration-173-177-20260729T094937Z/master/pr175-master-5bf35f7-sonar-retriage.md`,
SHA-256 `23183fad63183cfead35b431f848157dea055333d05b3da4a48a0a0f9ddd8834`.

### Current bounded delivery acceptance — 2026-07-29

This section supersedes the earlier statement that no risk has been accepted
for the present controlled delivery. At `2026-07-29T13:14:43Z`, after the
pre-existing resulting-master condition was disclosed, the current user stated
“ich akzeptiere das rest risiko”. The decision accepts only the following
residual risk for the sequential, SHA-bound Parent PR #173–#182 integration:
the resulting-master SonarCloud Quality Gate may remain `ERROR` with security
rating `5` and security-hotspot review `0.0%` solely because the same three
`TO_REVIEW` `python:S5332` keys remain:

- `AZ7K5CRYixFPtcnbna1R` at
  `ci/checks/documentation/check-generated-report-layout.py:42`;
- `AZ7K5CRYixFPtcnbna1S` at
  `ci/checks/documentation/check-generated-report-layout.py:49`; and
- `AZ7K5CQgixFPtcnbna1J` at
  `ci/evidence/reports/generate-system-environment-proof.py:98`.

The accepted baseline is master
`154ee724eba4653fa6378fc3c8729ae433e65697` / completed SonarCloud check
`90559417652`, retained in
`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/risk-acceptance.md`
(`sha256:59b9e9ec44e40d7315b8f26ffea607e071cd42720f19459228a1b65fa0816b98`).
Every resulting-master readback must prove the same non-causal signature and
that the selected PR did not modify either hotspot-bearing path.

This bounded acceptance waives no PR-specific required check, PR Quality Gate,
security scan, review or thread; no new/changed master Sonar failure; and no
direct-master action, bypass, external reviewed/safe or false-positive
disposition, suppression, exclusion, scanner/Gate change, Framework/MRTS
action, or Gitlink change. The global finding remains `blocked` and
release-blocking. The acceptance permits this delivery sequence to continue;
it is not a technical verification, external Sonar disposition, or global
release approval.

### Post-PR #219 resulting-master revalidation — 2026-08-01

PR #219 exact head `5765a626433591ec3b758463ad3afbf75c857b10` passed its
strict protected checks, SonarQube Cloud PR Quality Gate, and direct PR issue
readback with zero rows and `0.0%` New-Code duplication. It was then merged by
the current user's SHA-bound protected squash authorization as Parent master
`904a8fca64b35cd287348722b4bdc2260b4f64b3`. All fourteen matching GitHub
Actions push workflows succeeded.

Only SonarCloud check `91368002687` failed on the resulting master. Its
analysis `6774d409-f6fe-46b7-8ee9-20b288d4c67e` has Quality Gate `ERROR`
solely on New Security Rating `5`; reliability and maintainability remain `1`,
New-Code duplication is `0.0%`, and new security-hotspot review is `100.0%`.
The immediately preceding master analysis
`67693a09-e0d9-4810-ac36-9305962957d1` at
`4a9992109ab3ac26526d14f6356b5be7215ab658` already has the same security-
rating failure. PR #219 does not change Sonar configuration, a Quality Gate,
suppression/exclusion, Framework, MRTS, or a Gitlink.

This is therefore another evidence-backed observation of the existing
project-wide baseline, not a causal PR #219 regression or a new independently
remediable finding. No external Sonar disposition, hotspot review,
suppression, policy change, or current risk acceptance occurred. The finding
remains `blocked` and release-blocking; the #219 integration is recorded as
`master_integration_failed` because its post-merge Sonar check was red.
Retained concise evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260801T103430Z-parent-ci-runtime-sonar-complete-remediation-20260801-6a18910f/evidence/pr-219-resulting-master-sonar-baseline-retriage.md`,
SHA-256 `e88afb18d0b0a0e92048a6f8399f8627949a88cb74a1bc353ebcd3c7055c210e`.
