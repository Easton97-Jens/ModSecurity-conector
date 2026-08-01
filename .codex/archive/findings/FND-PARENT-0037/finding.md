# Finding: Aggregate receipt traversal has an intermediate-symlink TOCTOU race

**Language:** English | [Deutsch](finding.de.md)

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0037` |
| Status | `closed` (archived) |
| Priority / severity | `P1 / high` |
| Owner | Parent |
| Root-control boundary | path confinement; producer authenticity; result-file authenticity |
| Release blocker | no |

## Summary

The `FND-PARENT-0031` aggregate-receipt helper performs a lexical `lstat` path
walk and later opens the complete pathname. `O_NOFOLLOW` protects only the
final component, so a concurrent same-UID matrix child can replace a previously
checked intermediate directory with a symlink before the later open.

## Evidence and reproduction

The retained source-to-sink review identifies the affected functions and the
exact lstat-to-open flow. The fixture-first regression uses a one-shot
`os.open` seam: after lexical inspection, it swaps `BUILD_ROOT/inside` for a
symlink to an external directory. Before the descriptor-relative correction,
the helper can read the external regular leaf while retaining an in-root
lexical path. A parallel writer seam swaps `verified-runs` before receipt
publication and proves that no external receipt is created after the fix.

## Root cause

The helper checks a mutable pathname hierarchy and later resolves it again.
Leaf-only `O_NOFOLLOW` cannot make the previously checked intermediate
components part of the later operation's trust boundary.

## Delivered remediation and current PR evidence

PR #59 exact head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` replaces pathname
re-resolution for aggregate-receipt reads and publication with descriptor-
relative traversal rooted at a pinned `BUILD_ROOT` descriptor. Intermediate
components use `O_DIRECTORY|O_NOFOLLOW`; receipt creation is exclusive and
descriptor-relative, with `fchmod` and `fsync`. The runner consumes the
descriptor-derived receipt record rather than re-hashing a mutable pathname.
The final follow-up seals receipts with owner-read-only `0400` mode. The
deterministic intermediate-read and verified-runs publication swaps fail
closed. Current non-skipped CI, CodeQL, Sonar Quality Gate, and zero
review/thread gates passed before a protected squash merge to Parent master
`5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. The exact resulting-master
reproduction passed 57/57 evidence-integrity controls, 11/11 bilingual
controls, shell syntax, and diff hygiene. This finding is verified, not
closed.

## Acceptance criteria

- A deterministic intermediate-directory read swap fails closed and never
  hashes external bytes.
- A deterministic `verified-runs` publication swap fails closed and creates no
  receipt outside `BUILD_ROOT`.
- The valid in-root read and complete twelve-cell aggregate-receipt controls
  remain accepted.
- The user-authorized combined Parent Draft PR retains distinct finding
  traceability; no Framework/MRTS change or merge occurs.

## Scope and dependency

This is Parent-owned and distinct from `FND-PARENT-0026` and
`FND-PARENT-0032`: those findings control caller roots and runtime-root/run-ID
authority, whereas this one protects individual receipt-helper operations after
the root/path check. It depends on `FND-PARENT-0031` as its implementation
base. The current user permits their combined/stacked #59 candidate, but the
findings remain independently tracked, verified, and not closed.

## Residual risk

The receipt chain is not a signature, ACL, process-identity, UID-isolation, or
external-attestation boundary. Mode `0400` limits group/other access only; an
actor with arbitrary same-UID write access to the Parent evidence namespace is
outside this local filesystem trust model. No risk is accepted. The exact
source-head gate and resulting-master original reproduction are verified.
`FND-CROSS-0001` separately blocks real current runtime evidence.
`FND-SONAR-0001` separately fails the global master Quality Gate; it is neither
accepted nor attributed to this finding.

## Current retained post-merge evidence

`pr59-5a22cbf-postmerge-validation.json` in run
`20260720T141403Z-pr55-pr59-master-integration-8a0b8640`, SHA-256
`7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51`, records
the exact source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`, protected
squash master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`, current gates, and
the post-merge original-reproduction and legitimate-control results.

## History

- `2026-07-18T15:45:00Z` — validated from retained Parent source-to-sink
  review; separate root cause and delivery branch allocated.
- `2026-07-20T09:57:03Z` — fixed_on_current_pr_head: #59 head
  `d4f88b886dac6fd5f483940015d6310bc239f814` delivers descriptor-relative
  traversal/publication and the `0400` sealing follow-up. It remains a Draft
  behind current master, so exact-head revalidation, authorized merge, and
  post-merge original reproduction are still required.
- `2026-07-20T15:13:08+00:00` — verified_on_resulting_parent_master: current
  source-head gates passed and #59 was protected-squash-merged from
  `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` to
  `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. The retained 57/57
  original-reproduction/legitimate-control suite includes the intermediate
  read and publication swaps; 11/11 bilingual, shell-syntax, and diff controls
  also passed. `FND-SONAR-0001` remains independent and unaccepted; this
  finding is closed by the current user after current-master validation.

- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_unchanged_path_validation` — affected paths are unchanged from verified master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` through `6ca7e1536ce7e93da68099db9c586b88852ff13e`; `tests.test_generated_report_evidence_integrity` passed in the 144-test control suite.
