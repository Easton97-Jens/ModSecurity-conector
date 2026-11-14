# Change Record: CR-20261114-preparation-master-integration

**Language:** English | [Deutsch](CR-20261114-preparation-master-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261114-preparation-master-integration |
| Date (UTC) | 2026-11-14 |
| Base revision | `34a924ec602826e87f74e8fb986486d5fced7e8b` |

## Motivation and problem statement

Integrate Parent #445 without waiting for another PR. Master already contains the externally merged #448 at `d420a12c4155a4bc2b9ea63ee5cef633085705e7`. The ordinary reconciliation commit is `34a924ec602826e87f74e8fb986486d5fced7e8b`; duplicate private C/Go proposals were not applied. Framework #169 is actually merged as `452f7fc7ca1d9c44c9e768cef565f52882a40e2d`, with the same reviewed candidate tree.

## Acceptance criteria

The final committed chain must select Framework `452f7fc7ca1d9c44c9e768cef565f52882a40e2d` and MRTS `9a855b092645733ea8ff73a512aff7bfe916407e`, with the version lock and all22 workflow projections agreeing. The separate pin requires matching complete-source evidence and regular exact-index admission. Required current-head CI/reviews/Gates,92 host executions,195 Go scenarios plus `go vet`, fresh Apache2.4.71 artifact admission/build/CRS and a genuine five-cell Aggregate must be verified before Parent integration.

## Implementation decision and rationale

Preserve both parents through an ordinary merge. Resolve SHA-only conflicts to the coherent first-parent f13/M9a baseline, then perform the actual Framework-master handoff in a separate native pin change. Preserve upstream response-counter saturation and native-error classification together with this PR's late-action handling. The Common Runtime gate for `strict_post_commit_action=0` remains; the selected Envoy profile declares `strict_post_commit_action=1`. A successful `strict_immediate_response_sent` records a send; it does not establish a downstream reset. Safe optional-event tolerance excludes native Reject, technical and audit errors.

## Changed files

The reconciliation changes61 regular paths against its first parent while leaving the24 pin paths unchanged. Four resolved documentation files are the EN/DE pairs under `connectors/envoy/ext_proc/` and `connectors/traefik/native_middleware/`. Existing upstream Common/connector source and Change Records are preserved. This record pair documents that reconciliation and the separate intended change of `modules/ModSecurity-test-Framework`, `ci/tooling/project-versions.lock.json` and22 workflow projections.

## Commands executed

Normal `git fetch origin master`, `git merge --no-commit --no-ff origin/master`, scoped conflict staging, `git diff --cached --check` and a normal active-hook commit succeeded. The merge parents are `5bab6e9da4ea63a4e53c432d3c433ff9f6d00072` and `d420a12c4155a4bc2b9ea63ee5cef633085705e7`; its tree is `7b83d86c6685ad8e6b5bec02bdb0251d847e4a57`. Native scaffold creation with `python3 ci/tools/new-change-record.py create --name preparation-master-integration --base-revision 34a924ec602826e87f74e8fb986486d5fced7e8b --date 2026-11-14` succeeded. Exact regular-file Secrets checks succeeded; automatic apply-hook incomplete results were separately recovered and are not claimed as automatic passes.

## Security impact

No authorization, isolation, source admission, error handling, test, CI requirement or Quality Gate is weakened. Keep mandatory audit/cleanup and distinguish optional late Safe events from native/technical failures. No blanket False Positive decision is made. The new immutable Framework target needs a separately matching regular admission; an earlier target's receipt is not reused as authority for the new commit.

## Runtime evidence

No new final-pair host or Go execution is claimed at this record's creation. The complete Framework-master source proof preserves2622 paths and57 authentic receipts from the reviewed identical tree; it proves its source/Secrets layer only. Candidate CI or a Secrets pass does not establish host reset/abort behavior or replace the final-pair checks.

## Known limitations

Framework-master Sonar analysis completes but its Gate fails the security rating. The previous master `939d1718b7548a36ff7a550080ed8b811aad8a98` already reported the same E security condition. The115 unresolved master findings are undergoing an individual baseline/scope comparison. This does not claim a green master Gate or classify every finding as false. Fresh Parent results are still required after the final pin commit.

## Remaining risks

Strict host/wire outcomes require independent target, peer and follow-up evidence. Rebuild native ABI consumers against matching Common headers and the required ModSecurity3.0.17 SDK. Old SDK3.0.14 diagnostics and HTTPD2.4.70 preparation failures do not qualify the final pair. Preserve all100 standard cases and80 selectors.

## Checks not run and rationale

The separate final pin/admission, its committed-pair CI/Sonar,92 hosts,195 Go scenarios plus `go vet`, fresh Apache2.4.71 admission/build/CRS and genuine five-cell Aggregate are not yet executed at record creation; their final immutable input is not committed yet. Comprehensive acceptance remains a subsequent step. No not-run check is reported as passed.

## Final diff and review status

An independent bounded static review of the four automatically merged product files found no additional demonstrated merge defect. The EN/DE conflict resolutions follow actual profile and Safe-event semantics. The reconciliation commit is local, clean and unpushed at record creation; Parent #445 is not merged. The pin will remain a separate scoped change so its normal hook can verify the exact publication. Final current-head review and delivery evidence remain required.
