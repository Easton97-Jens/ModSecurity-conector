# Change Record: complete Framework handoff

**Language:** English | [Deutsch](CR-20260930-complete-framework-handoff.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-complete-framework-handoff |
| Date (UTC) | 2026-09-30 |
| Base revision | `bbd74521ee9b1c7544b11c225e399a1c7f8d49da` |

## Motivation and problem statement

The owner requested actual delivery of the original Framework repair into PR #393, including NGINX and ModSecurity-v3 upgrade safeguards. Earlier local runs applied the changes but stopped at two privileged sandbox tests, so no repair commit reached the PR.

## Acceptance criteria

Apply the reviewed Framework update and all associated projections; retain security boundaries; pass affected unit, contract and documentation checks; publish a normal follow-up commit to the existing PR branch. Confirm final-head CI and Sonar separately before declaring readiness. No merge is authorized.

## Implementation decision and rationale

Review the exact twelve literal changes from Framework f9e48b0774b5bdf7aaa8e38ce98eb6c50bf293c8 to 0290a979ba4bc63a7abed175a53471367b385553. Recompute structure digest 2c3a5774da760981804907a357dc5dafb62f9ba3de1db17a2807ff53fd83c291 and align the Parent NGINX tuple to release-1.31.6, archive nginx-1.31.6.tar.gz, SHA-256 974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1. Include the missed evidence-writer pin and exact single-line version readback. Check empty global and read-only job-local permissions rather than restoring global rights. Add an offline source/projection checker and ModSecurity cache/layout regressions. ModSecurity stays v3.0.16 at 7ea9fefbe0ba409d8733b4d682c8c4c059cd028d.

The two privileged test callbacks now receive the resolved interpreter rather than an external virtualenv alias. Their child error handlers retain failure and print a bounded diagnostic. A regression verifies that the external alias remains rejected while its already allowed resolved target is accepted; the production jail allowlist is unchanged.

## Changed files

The generator's nineteen Parent text targets and Framework gitlink; the missed NGINX writer; its regression tests; namespace and sandbox tests; early quick-check; the new reviewed-version checker and tests; paired upgrade documentation and this record. The temporary validation-branch helper is excluded from the repair tree.

## Commands executed

The owner-supplied previous run completed the real verifier, synchronizer and affected regression commands, then failed two of 167 CI-security tests. Those are baseline observations, not success claims. Direct delivery reproduces and tests the scoped patch on a GitHub-hosted checkout; the linked validation job and final PR checks carry the actual terminal results. A commit object is prepared only after the configured validation gates pass. The exact tested Git tree is checked again during publication.

## Security impact

No broader mutable registry, candidate-shell approval, permission expansion, scanner suppression or protected-broker edit. The source tuples and path restrictions remain fail-closed. Resolved Python selection fixes test-harness inputs without mounting external host directories. The validation job has read-only repository access; a separate bounded publisher creates Git objects and cannot merge or update master.

## Runtime evidence

Unit and synthetic library-layout tests are not native ABI or WAF compatibility evidence. The actual NGINX exact-head runtime job and any required privileged namespace results must be inspected separately. No new ModSecurity release is selected or certified.

## Known limitations

ChatGPT's local environment lacks GitHub DNS and RTK. Hosted execution supplies repository-native results; local fixture results are not substituted. A green preparation-only commit was insufficient and is superseded only when the actual repair commit is on the PR branch.

## Remaining risks

Future versions may change public APIs, SONAME, output layout or WAF behavior. Early drift checks do not guarantee every future release. The independently protected NGINX broker remains a separate review boundary.

## Checks not run and rationale

No new ModSecurity release build or complete multi-connector runtime matrix is initiated solely for these guard changes. Pending final-head CI and Sonar are not counted as passed. Environmental skips must be reported rather than hidden.

## Final diff and review status

Deliver only the bounded repair tree after validation and unchanged-branch checks. Read back the final PR SHA and its checks. Preserve all existing Sonar fixes and documentation safeguards. No force push, master push or merge.
