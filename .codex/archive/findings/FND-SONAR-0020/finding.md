# Finding FND-SONAR-0020: Event JSON serializer Cognitive Complexity finding remediated and verified on master

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `sonarqube_finding` |
| Repository / ownership | `parent` / `parent` |
| Priority | `P2` |
| Security severity / relevance | `not_applicable` / `false` |
| Confidence / status | `confirmed` / `closed` |
| Feasibility | `already_fixed` |
| Release blocker | `false` |
| Profile | Historical master `a5901a3c…`; PR #197 was squashed as master `caddd86…`, verified by analysis `43a50e20…` |

## Summary and observed behavior

Historical current-master analysis `f179066b-a8ed-4471-895e-342cebd8dc52`
reported one OPEN `c:S3776` `CODE_SMELL`, key `AZ9cRy9OHhV2CayPTP4Y`, in
`common/src/event.c:502`, symbol `msconnector_event_write_json_ex`: Cognitive
Complexity `26` where `25` was allowed.

PR #197 extracted the shared bounded optional event-JSON-field formatting path
without changing a Sonar rule, Quality Gate, exclusion, `NOSONAR`, suppression,
or risk disposition. Its exact delivery head
`8a9036a7663f4170a02a0e3b7a677e306ddc6012` passed focused local, security,
hosted, and PR-Sonar evidence and was SHA-bound-squashed as master
`caddd86d1eede95de53aa1bc971dd26d875df21c`.

Current-master analysis `43a50e20-8bdd-453a-bc44-549a7e3d7588` records that
exact revision and marks `AZ9cRy9OHhV2CayPTP4Y` `CLOSED` / `FIXED`. The
original reproduction therefore no longer occurs on master.

## Expected behavior and impact

The completed repair keeps `msconnector_event_write_json_ex` at or below the
configured threshold without changing a Sonar rule, Quality Gate, exclusion,
`NOSONAR`, suppression, or risk disposition. It preserves JSON serialization
compatibility, truncation/failure behavior, bounded transport-token validation,
and raw QUIC connection-ID redaction.

This was a confirmed non-security maintainability finding
(`severity: not_applicable`) despite Sonar's historical `CRITICAL` / `HIGH`
maintainability classification. The current master Quality Gate remains
`ERROR` only for the separate accepted `FND-SONAR-0001`
`new_security_rating=5` and `new_security_hotspots_reviewed=0.0` baseline;
`new_maintainability_rating=1` remains passing. This closed finding neither
changes nor extends that risk acceptance.

## Affected scope, historical preconditions, and closure state

- Affected file: `common/src/event.c`
- Affected symbol: `msconnector_event_write_json_ex`
- Protocol / boundary: event JSON serialization
- Historical preconditions: SonarQube Cloud analyzed Parent master
  `a5901a3c89528ec9a43ab9755da5755fdb01420d`; issue
  `AZ9cRy9OHhV2CayPTP4Y` was OPEN at the listed location.
- Closure state: PR #197 delivery head `8a9036a…` was SHA-bound-squashed as
  master `caddd86…`; current analysis `43a50e20…` marks that issue
  `CLOSED` / `FIXED`.

## Reproduction and evidence

The historical run ID is
`20260729T195549Z-fnd-sonar-0020-event-cognitive-complexity`. Its observations
were made from `/root/git/ModSecurity-conector` at `2026-07-29T19:55:49Z`.
The closure run ID is `20260730T135511Z-fnd-sonar-0020-postmerge-verification`;
its retained, secret-free post-merge summary is bound to master `caddd86…`.

| Artifact | SHA-256 | Command / result |
| --- | --- | --- |
| `issue.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/issue.json`) | `69d6fa710a3e99b4a18151a13eb6bcf83e600a1c0d3188b0036b4115cb66c4ea` | `rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&issues=AZ9cRy9OHhV2CayPTP4Y&ps=10'`; returns one OPEN `c:S3776` issue at `common/src/event.c:502`, complexity `26` where `25` is allowed. |
| `analysis.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/analysis.json`) | `1c12b6c8e780a1282cdb8fdc154ddc2543bf5ca2901f267994a26c83ef8ba446` | `rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/project_analyses/search?project=Easton97-Jens_ModSecurity-conector&ps=1'`; binds analysis `f179066b-a8ed-4471-895e-342cebd8dc52` to master `a5901a3c89528ec9a43ab9755da5755fdb01420d`. |
| `quality-gate.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/quality-gate.json`) | `a65798fd40f5538e793d1734eb631235eb6809ae9107a2086acdc9a87b6e3689` | `rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-conector'`; shows the separate security-hotspot baseline and `new_maintainability_rating=1`. |
| `receipt.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/receipt.md`) | `5790131a8e4b5b159001af9a60c9b316209d8ceca6fc66e2e1453f52c4b7cd8f` | Bounded command, exit-code, source-revision, and interpretation receipt. |
| `sonar-master-readback.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/evidence/sonar-master-readback.json`) | `1c1c704489e1d8bf4ea09f466b6a132dd9f5f36a0095a069c2cf9b6da93d86c3` | Read-only post-merge Sonar/GitHub monitor readback plus `rtk git rev-parse HEAD origin/master`; analysis `43a50e20…` binds to `caddd86…`, and `AZ9cRy9OHhV2CayPTP4Y` is `CLOSED` / `FIXED`. |
| `post-merge receipt.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/evidence/receipt.md`) | `d0857f57980009e47ba469f143d91055c2e8b75d77ce155e27b6c25b12ad531d` | Hash-bound receipt for the exact replayable read-only master, analysis, issue, and Quality-Gate readbacks. |

The historical secret-free inventory is sealed in
`manifest.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/manifest.md`)
and `SHA256SUMS` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/SHA256SUMS`).
The separate closure-run inventory is sealed in
`manifest.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/manifest.md`)
and `SHA256SUMS` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/SHA256SUMS`).

## Root cause and proposed remediation

Historically, the function combined numerous independent validation, redaction,
metadata-presence, formatting, and truncation branches. PR #174 lowered the
measured complexity from `32` to `26`, but left the finding one point over the
threshold.

Completed without a Sonar configuration change: PR #197 extracted the shared
bounded optional JSON-field formatting path. Its exact head passed C17 and
ASan/UBSan Common-helper smokes, Common SDK/security/flow contracts, 22
bilingual-documentation tests, a sealed zero-finding security-diff scan, all
required hosted gates, and PR Sonar Quality Gate `OK`, then was
SHA-bound-squashed to master.

## Acceptance criteria and validation plan

1. `AZ9cRy9OHhV2CayPTP4Y` is `CLOSED` / `FIXED` in current-master analysis
   `43a50e20…`.
2. No `NOSONAR`, suppression, Sonar rule, Quality-Gate, exclusion, or risk-
   acceptance change was used.
3. Exact-head Common C17, ASan/UBSan, SDK/security/flow, bilingual, and diff
   checks passed.
4. The sealed focused security-diff review reports zero reportable findings and
   confirms preserved serialization, truncation, bounded-token, and
   raw-QUIC-CID redaction controls.
5. The exact PR head passed current hosted checks, reviews/threads, CodeQL,
   dependency/secret controls, and SonarQube Cloud without bypass.
6. The SHA-bound merge created `caddd86…`; its current-master analysis reran
   the original issue readback successfully before this finding was closed.

## Dependencies, related findings, and residual risk

The focused Parent remediation and current SonarQube Cloud exact-head/current-
master access have completed. It has no current technical blocker.

- `FND-SONAR-0001` is related current-master Quality-Gate context, not a
  duplicate: it owns the accepted three-`python:S5332` security-hotspot
  baseline.
- `FND-SONAR-0016` is related scanner-family context, not a duplicate: it is
  an aggregate Draft-PR new-code/duplication record.

No FND-SONAR-0020-specific residual risk remains. The only remaining Master
Quality-Gate error is the separate, unchanged and bounded
`FND-SONAR-0001` baseline; this record neither changes nor extends it.

## History

- `2026-07-29T19:55:49Z` — allocated stable ID `FND-SONAR-0020` after
  current-master evidence confirmed the independently remediable OPEN issue.
- `2026-07-30T13:41:13Z` — exact PR #197 head `8a9036a…` fixed the focused
  source boundary and passed local, security, hosted, and PR-Sonar evidence.
- `2026-07-30T13:49:52Z` — resulting master `caddd86…` was verified by
  analysis `43a50e20…`; the original issue is `CLOSED` / `FIXED`, so the
  finding is closed.

## Current reconciliation confirmation — 2026-08-01

[PR #197](https://github.com/Easton97-Jens/ModSecurity-conector/pull/197)
merged normally as `caddd86d1eede95de53aa1bc971dd26d875df21c`, reachable from
current `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`. Current
SonarCloud API readback for `AZ9cRy9OHhV2CayPTP4Y` remains `CLOSED` / `FIXED`;
the exact PR checks report 33 passed and 0 failed. The global master Quality
Gate error is separately tracked as `FND-SONAR-0001`.
