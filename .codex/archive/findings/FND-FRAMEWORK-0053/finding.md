# FND-FRAMEWORK-0053 — Framework PR #42 evidence documents retained stale exact-head claims

## Identity

| Field | Value |
| --- | --- |
| Category | documentation_drift |
| Repository / ownership | framework / framework |
| Priority / severity / confidence | P2 / not_applicable / confirmed |
| Status / feasibility | closed / feasible_now |
| Release blocker / security relevant | false / true |
| Affected files | reports/audits/change-records/20260722-02-migrate-framework-python-314-ci.md; reports/audits/change-records/20260722-02-migrate-framework-python-314-ci.de.md; GitHub pull request #42 description |
| Historical hosted source head | 2930e04e1558b5b10bdeb87a76abb077a2085566 |
| Corrected current PR head | dc6cf411e78b3f37f1e4be52edef59894560b1ae |
| Resulting Framework master / merge commit | 935cf14c676a24672be5c336e92cd13457cc35c8 |

## Summary

The paired Framework PR #42 Change Record accurately retained the historical
CPython 3.14 migration failures, but still described its security-preserving
source follow-up as locally validated with hosted exact-head evidence pending.
That claim was stale: source head
`2930e04e1558b5b10bdeb87a76abb077a2085566` had already passed hosted
`python-ci-security-quality` run `29962792445` / job `89067507532`, repaired
OSV, all non-skipped PR checks, and the PR SonarQube Cloud Quality Gate.

The focused English/German Change-Record correction is commit
`dc6cf411e78b3f37f1e4be52edef59894560b1ae` (`docs: reconcile CPython 3.14 evidence`).
At PR scope, it correctly recorded source-head facts and did not invent
resulting-master evidence. PR #42 was subsequently merged normally at
`2026-07-23T07:41:13Z` as Framework master / merge commit
`935cf14c676a24672be5c336e92cd13457cc35c8`. The retained post-merge receipt
now proves the exact resulting-master state, while the Change Record merged in
that tree still says that resulting-master evidence is unobserved and that PR
#42 has not merged. This newly reproduced factual documentation drift changes
the finding from `fixed` to `in_progress`; it is neither `verified` nor
`closed`.

The first reconciliation left an independently editable evidence surface stale:
the bilingual GitHub PR #42 description still called `2930e04…` the exact head
that had to pass before a merge, although current head was `dc6cf411…`.  At
`2026-07-23T06:12:04Z`, only that PR description was corrected.  It now
identifies `2930e04` as historical evidence, `dc6cf411` as current, and retains
the queued Cloudflare and current-master Sonar delivery limitations.  This did
not change the branch, commit, source, checks, Parent gitlink, or MRTS.

## Observed and expected behavior

Before correction, the identity, commands/results, documentation/runtime,
checks-not-run, limitations, and final-review sections grouped already-observed
hosted source-head evidence with unobserved resulting-master evidence.

The retained post-merge verification now proves that PR #42 was normally merged
as `935cf14c676a24672be5c336e92cd13457cc35c8`, while the Change Record in that
merged tree still reports the resulting-master state as unobserved and PR #42
as unmerged. The original PR-scope correction remains intact; this exact
post-merge mismatch is the new reproduction.

The paired records and bilingual PR description must bind every hosted assertion
to its exact source/current-head SHA, distinguish it from resulting-master
evidence, preserve direct-master-push and fresh-exact-head requirements, and
never create self-referential evidence for a later documentation-only commit.
Once resulting-master evidence exists, they must accurately state its exact
SHA-bound result instead of continuing to call it unobserved.

## Impact, root cause, and remediation

The stale wording could mislead a master-integration reviewer about the
available PR #42 evidence. It did not prove a product vulnerability, runtime
change, risk acceptance, or permission to merge. The newly reproduced merged
record can also falsely report a completed merge/result as absent.

The record was authored before the final source follow-up reached hosted
validation and was not reconciled after that exact-head result arrived. The
first repair changed only the paired Change Record files; the later description
repair changed only GitHub PR metadata. Both preserve all security, Quality
Gate, test, Parent, and MRTS boundaries. The later normal merge/result was not
reconciled into the already merged Change Record, which is the newly reproduced
drift. The current task is tracking-only: it does not authorize a product-source
change, Framework branch, or Framework pull request.

## Evidence and reproduction

| Field | Value |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-premerge-gates.md |
| Artifact type | framework_pr42_documentation_reconciliation_and_premerge_gate_readback |
| SHA-256 | f62126139a762264f3953d821dc0b07362e19675970df897857afc70a5fd34cb |
| Continuation artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-merge-continuation.md |
| Continuation SHA-256 | 2cf2c0943bb7b4d7fa61101cbabdb3646d2c908ebf19b479c5bab38c6b0aaed1 |
| Post-merge artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md |
| Post-merge artifact type | framework_pr42_resulting_master_verification |
| Post-merge SHA-256 | 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1 |
| Post-merge observed at | 2026-07-23T07:51:09Z |
| Producer command | RTK-wrapped Change Record diff review, make check-documentation, git diff --check, exact branch/PR head readback, and current GitHub/Sonar check readback |
| Working directory | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/tmp/framework-worktree-v4 |
| Exit code / observed at | 0 / 2026-07-23T04:13:04Z |
| Retention status | retained_task_evidence |

Reproduce by comparing the original pending claim with hosted run
`29962792445` / job `89067507532`, then inspect the paired correction at
`dc6cf411e78b3f37f1e4be52edef59894560b1ae`. Also compare the pre-correction
PR-description `2930e04` merge-head claim with the current `dc6cf411` PR
metadata and corrected bilingual description.

For the newly reproduced drift, read the Change Record as merged at
`935cf14c676a24672be5c336e92cd13457cc35c8` and compare its still-unobserved
resulting-master / unmerged-PR statements with the retained post-merge receipt:
PR #42 is `MERGED`, the resulting tree is the reviewed PR-head tree, and eight
exact-SHA GitHub workflow runs completed successfully. The receipt also records
the distinct, still-unresolved SonarQube Cloud and Cloudflare dispositions; it
does not treat either as passing or resolved.

## Acceptance criteria and validation plan

1. The English/German records have equivalent SHA values, run/job IDs, facts,
   risks, and limitations.
2. They identify source-head hosted evidence as observed and bind the actual
   resulting-master result to `935cf14c676a24672be5c336e92cd13457cc35c8`,
   rather than calling it unobserved.
3. They make no claim beyond the exact documentation-reconciliation or
   resulting-master evidence that is actually retained.
4. `make check-documentation` and `git diff --check` pass.
5. A separately authorized correction is normally committed and pushed in its
   own Framework PR; no direct master push, Parent gitlink update, or MRTS
   change occurs.
6. The PR description names `2930e04` as historical evidence and `dc6cf411` as
   the current head in equivalent English and German without changing the PR
   head.
7. A separately authorized Framework documentation follow-up is normally
   reviewed, validated, merged, and rechecked on its resulting master before
   this finding can become `verified` or `closed`.

Validation was paired-diff review, `git diff --check`, native
`make check-documentation` under selected `python3` (CPython 3.14.4), exact
remote/PR head confirmation, fresh PR check readback, and GitHub App current
PR metadata/body readback after the description correction.

The current reproduction validation is the hash-addressed post-merge receipt
at `2026-07-23T07:51:09Z`. No product documentation was changed and therefore
`make check-documentation` and `git diff --check` were not rerun for a
nonexistent follow-up in this tracking-only task.

## Regression and legitimate-control tests

- Regression: `make check-documentation`; `git diff --check`; GitHub Actions
  and SonarQube Cloud exact-head readback for PR #42.
- Legitimate control: both records retain the direct-master-push prohibition,
  require fresh evidence for every later PR head, and distinguish observed
  resulting-master evidence from the still-unresolved SonarQube Cloud and
  Cloudflare limits; the PR description retains the queued Cloudflare and
  failed current-master Sonar limitations.

## Dependencies, blockers, related findings, and residual risk

- Dependencies: a separately authorized Framework documentation-only
  follow-up branch/PR and its resulting-master verification.
- Blockers: the current tracking task authorizes neither a product-source
  change nor a Framework branch or PR. `FND-GITHUB-0007` and
  `FND-SONAR-0002` remain globally unresolved; their bounded PR #42 delivery
  acceptance does not correct this finding.
- Related findings: `FND-FRAMEWORK-0045`, `FND-GITHUB-0007`, and
  `FND-SONAR-0002`.

The original stale Change-Record and PR-description claims no longer reproduce
on exact PR head `dc6cf411e78b3f37f1e4be52edef59894560b1ae`. However, the
merged Change Record at exact master
`935cf14c676a24672be5c336e92cd13457cc35c8` now falsely retains the
unobserved-result / unmerged-PR state, so this factual drift reproduces again.
The bounded PR #42 delivery acceptance for SonarQube Cloud and Cloudflare does
not waive documentation accuracy, does not close either global finding, and
does not authorize this task to modify product source, create a branch, or
open/update a PR.

## History

- `2026-07-23T04:07:43Z` —
  `pr42_change_record_source_head_evidence_reconciled`: only the paired records
  were committed as `dc6cf411e78b3f37f1e4be52edef59894560b1ae` and normally
  pushed. `make check-documentation` and `git diff --check` passed.
- `2026-07-23T04:13:04Z` —
  `documentation_drift_tracked_after_deduplication`: this is distinct from
  `FND-FRAMEWORK-0045`, which owns the independently remediable PR #37 record.
  No source, Parent, gitlink, MRTS, merge, or risk-acceptance change occurred.
- `2026-07-23T06:12:04Z` —
  `pr42_description_current_head_reconciled_and_deduplicated`: corrected the
  existing bilingual GitHub PR #42 description without changing branch or head.
  The independently editable metadata surface shares the incomplete PR #42
  evidence-reconciliation root cause and therefore extends this canonical
  finding instead of receiving a duplicate ID.
- `2026-07-23T07:51:09Z` —
  `resulting_master_documentation_drift_reproduced`: retained post-merge
  evidence hash `0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`
  proves normal PR #42 merge and exact Framework master
  `935cf14c676a24672be5c336e92cd13457cc35c8`. The merged Change Record still
  says resulting-master evidence is unobserved and PR #42 has not merged.
  Reclassified `fixed` to `in_progress`; no product source, Framework branch,
  or PR was changed or authorized by this tracking task.
- `2026-07-26T16:13:56Z` — `remediation_fixed` and
  `resulting_master_verified_and_closed`: Framework PR #50 corrected the paired
  PR #42 Change Record facts. Exact Framework master
  `de705a5efb872f95f010346fe2e6143c88876ad4` retains those paths unchanged
  through PR #51 and passes `make check-documentation`. Global SonarQube Cloud
  and Cloudflare records remain separate. Receipt:
  `.codex/runs/20260726T160903Z-framework-pr50-pr51-master-verification/finding-closure-evidence.md`
  (SHA-256 `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`).
