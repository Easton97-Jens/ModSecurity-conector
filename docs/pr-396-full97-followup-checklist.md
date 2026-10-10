# PR #396 — Full97 follow-up

**Language:** English | [Deutsch](pr-396-full97-followup-checklist.de.md)

Updated: 2026-10-10. [Draft PR #396](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396).
Only the authorized NGINX R13 follow-up; the [overarching PR-382 checklist](pr-382-checklist.md) is unchanged. No I09–I12/cross-connector/secret-scan acceptance.

## Revision and evidence contract

- Tested baseline Parent: `dca17fd5690c2ec2b8806024d1061744db8c3ad8`.
- Tested baseline Framework: `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9`.
- MRTS: `8a6bb546c4c81d8ffc7be801dceac60c6925685f`.
- Current Parent: `dca17fd5690c2ec2b8806024d1061744db8c3ad8`.
- Current Framework: `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9`.

R13 is unchanged: 97 Required = 80 original Case-PASS / 9 FAIL / 8 NOT_EXECUTED; four additional aggregate-schema errors affect two of those MIME Case-PASS. Make/supervisor 2, Canonical FAIL, validator 1. No new Full97; authorization **NEIN**. Protected **BLOCKED / NOT RUN**.

Code implemented, focus verified and Full97 confirmed are separate milestones. Documentation commits do not inherit runtime proof. Each completed item references revision-bound evidence; local files are not public GitHub downloads.

Local task evidence: `/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-followup-20261010T084822Z/`. `baseline-reconciliation.json` and `issue-record-matrix.csv` only read historical inputs; **NOT A NEW RUNTIME RUN**. B0–B3, D1, E1–E2: Parent/Framework baseline SHAs above; readback and original comparison passed, no fix commit, no new runtime. Original report: `/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-dca17fd5-20261009T225409Z/report.md`.

## B — Baseline

- [x] B0: Verify actual revisions, branches, Gitlinks and preserved R13. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] B1: Map all nine original FAIL records. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] B2: Map all eight original NOT_EXECUTED to their first missing boundary. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] B3: Map four nested errors to the two MIME-Allow Case-PASS. (`baseline-reconciliation.json`; baseline SHA binding above).

## A — Intervention outcomes

- [ ] A1: Reproduce the invalid event sequence.
- [ ] A2: Identify producer, overwritten fields and governing observation time.
- [ ] A3: Demonstrate RED regressions.
- [ ] A4: Implement the minimal identity-bound correction.
- [ ] A5: Pass positive, technical-fault, cross-transaction and priority controls.
- [ ] A6: Verify a genuine bounded host focus.
- [ ] A7: Integrate and bind the tested SHA.
- [ ] A8: Confirm original record status in a new Full97 (approval required).

## B — First-Byte snapshot

- [ ] B4: Determine invocation/time/counter contract.
- [ ] B5: Reproduce bad snapshot binding and RED controls.
- [ ] B6: Fix and reject stale, wrong-time/TX/invocation snapshots.
- [ ] B7: Run a genuine causal First-Byte focus with complete Safe response.
- [ ] B8: Integrate and bind the tested SHA.
- [ ] B9: Confirm in new Full97 (approval required).

## C — Native H1 binding

- [ ] C1: Trace observed protocol through operation/receipt/event to Canonical.
- [ ] C2: Reproduce the first missing identity binding.
- [ ] C3: Fix strictly; retain protocol/identity/artifact negative controls.
- [ ] C4: Verify a genuine native H1 focus.
- [ ] C5: Integrate Framework and Parent consistently.
- [ ] C6: Confirm in new Full97 (approval required).

## D — MIME aggregate schema

- [x] D1: Identify four errors separately from two Case-PASS. (`baseline-reconciliation.json`; baseline SHA binding above).
- [ ] D2: Trace case result, producer, nested aggregate and validator.
- [ ] D3: Demonstrate RED through actual dynamic aggregation.
- [ ] D4: Implement the narrowly justified schema-conforming contract.
- [ ] D5: Verify both real MIME-Allow cases and mismatch controls.
- [ ] D6: Integrate and bind the tested SHA.
- [ ] D7: Validate the new Full97 aggregate (approval required).

## E — Eight derived records

- [x] E1: Map each record to its first blocked boundary. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] E2: Distinguish A–D dependencies from independent causes. (`baseline-reconciliation.json`; baseline SHA binding above).
- [ ] E3: Complete authorized corrections and bounded focus proofs.
- [ ] E4: Measure fresh original statuses in Full97 (approval required).

## Q — Integration and quality

- [ ] Q1: Preserve successful existing regressions.
- [ ] Q2: Pass required Parent/Framework tests and lint.
- [ ] Q3: Bind Gitlinks and verified remote heads.
- [ ] Q4: Read fresh current-head CI/Sonar.
- [ ] Q5: Reconcile EN/DE checklist and PR description.

## F — Overall acceptance

- [ ] F1: Obtain explicit authorization for one new Full97.
- [ ] F2: Actually execute the new Full97.
- [ ] F3: Validate the whole fresh aggregate schema.
- [ ] F4: Verify valid evidence for every Required record.
- [ ] F5: Check Canonical PASS and actual lifecycle/validator exits.
- [ ] F6: Verify full cleanup and fresh checksums.

## P — Protected, separate

- [ ] P1: Independently approve Trusted Base.
- [ ] P2: Verify permitted base/Gitlink/workflow binding.
- [ ] P3: Administratively approve runner and environment.
- [ ] P4: Verify Exact-Base host gate.
- [ ] P5: Start and evaluate an admissible protected run.

## Record mapping and remaining work

A: `phase3_deny_before_commit`, `phase3_redirect_before_commit`, `phase4_deny_after_commit_log_only`, `phase4_deny_after_commit_abort`, `phase4_deny_after_commit_log_only_safe`. A+B: `phase4_rule_observed`, `phase4_no_full_response_buffering`, `phase4_first_byte_before_response_end`. C: `phase4_strict_http1_client_abort`.

The eight pending records are closed derivations of blocked basis records, not presumed missing drivers:

| Record | Basis / boundary |
| --- | --- |
| phase4_event_contains_original_status | A: phase4_deny_after_commit_log_only / phase4_deny_after_commit_abort |
| phase4_event_contains_late_intervention_action | A: phase4_deny_after_commit_log_only / phase4_deny_after_commit_abort |
| event_has_no_response_body_payload | A+B: phase4_rule_observed |
| phase3_original_and_visible_status | A: phase3_deny_before_commit |
| phase4_deny_after_commit_abort_strict | A: phase4_deny_after_commit_abort |
| phase4_status_metadata | A: phase4_event_contains_original_status |
| phase4_action_metadata | A: phase4_event_contains_late_intervention_action |
| phase4_no_payload_event | A+B: event_has_no_response_body_payload |

D: `phase4_out_of_scope_content_type` and `phase4_missing_content_type` remain Case-PASS. Their `requested_action` and `actual_action` = string `allow` violate the nested enum at `$.phase4_case_results[17]` / `[18]`: four schema errors, not four runtime FAILs.

Open: genuine bounded focus probes, consistent Gitlink integration and current quality gates. Implemented commits: Parent A `b0d75ef6bbc33228423aef65d8ea3409387ab30f`, B `58d07970b755d7435c23030e844a32e2f6b6b583`, scoped positive-fault follow-up `7672340c57b3f7c80f4f5c68fc55fecca2ae4af8`; Framework C `e8a8f98a4c24958616b15b98aadedcc73345a786`, D `0c7f224731cda059decee026c7bd32e58bf9aa21`. These commits alone do not establish runtime acceptance. `issue-record-matrix.csv` contains all 97 records with original status, operation, raw evidence, boundary, owner and dependency; fresh focus/Full97 columns stay separate. No Required reduction or historical status changes.
