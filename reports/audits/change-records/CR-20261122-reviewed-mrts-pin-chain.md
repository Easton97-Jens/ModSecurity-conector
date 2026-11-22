# Change Record: CR-20261122-reviewed-mrts-pin-chain

**Language:** English | [Deutsch](CR-20261122-reviewed-mrts-pin-chain.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261122-reviewed-mrts-pin-chain |
| Date (UTC) | 2026-11-22 |
| Base revision | `60a7b74e057769503d6b4cb01b2cc9ba8da875c8` |

## Motivation and problem statement

Integrate the reviewed inheritance correction from [MRTS #7](https://github.com/Easton97-Jens/MRTS/pull/7) through [Framework #187](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/187) into Parent. Two inherited Parent policy bindings had diverged. Source review established the semantic changes before accepting their digests. This record is a PREPUBLICATION snapshot: Parent publication and exact operator admission remain outstanding.

## Acceptance criteria

The Parent gitlink, strict version lock and all registered Framework caller references must agree with the actual reviewed Framework/MRTS commits. Inheritance, candidate contracts, primary verification, documentation, normal Git hooks and fresh applicable CI/Quality Gates must pass before integration. Preserve the 100 core cases, 80 selectors, 1144 offline exceptions, integrity controls and protected broker identities. Do not merge on evidence from an older head.

## Implementation decision and rationale

MRTS reviewed head `9a855b092645733ea8ff73a512aff7bfe916407e` was regularly squash-merged to `488e75388d917615feecab91650c3278b9c78b1e`, with prior main `ee2174431c4edf97e66afe32558ce8454deb2397` as sole parent and the reviewed tree unchanged. Only `PARENT-ARCHITECTURE-AND-BOUNDARIES` and `PARENT-COMMAND-EXECUTION` bindings changed. Historical Parent preimages were recovered: the architecture change removes an illustrative reading-list entry; the command change clarifies the direct starter path for automatic Secrets hooks. Ownership, agent RTK use and authorization boundaries remain intact. No blind checksum repair was used.

Framework reviewed head `0cf20b680bef0ba5dd635f874cea1626de8bdef3` became actual squash `b4d619127a3fbd2a4074998e874c592d693413b9`, with sole parent `e1964415efcd3cda11614ce13b7d34331ee0cf06` and the same tree. Its only changes are `tools/MRTS` and the bilingual integration record. Parent already adopted Framework `e1964415efcd3cda11614ce13b7d34331ee0cf06` through #459. This follow-up therefore changes that Framework pin to `b4d619127a3fbd2a4074998e874c592d693413b9` and MRTS from `ee2174431c4edf97e66afe32558ce8454deb2397` to `488e75388d917615feecab91650c3278b9c78b1e`.

The native synchronizer owns the generated projections. Explicit `--mrts-sha` and `--expected-candidate-mrts-sha` preserve the joint contract; the five-key lock and toolchains are retained. Earlier SDK/output-layout changes were already present in the selected Parent base and are not introduced by this follow-up.

## Changed files

| Paths | Change |
| --- | --- |
| `modules/ModSecurity-test-Framework` | Select actual Framework squash and its nested MRTS commit. |
| `ci/tooling/project-versions.lock.json` | Native update of `framework_sha` and `mrts_sha`. |
| 22 registered files under `.github/workflows/` | Native regeneration of Framework references. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | Current integration snapshot and remaining steps. |
| `reports/audits/change-records/CR-20261122-reviewed-mrts-pin-chain.md`, `reports/audits/change-records/CR-20261122-reviewed-mrts-pin-chain.de.md` | Native-scaffolded record pair. |

No product source, test definition, generated measurement report, repository rule or CI gate is changed.

## Commands executed

Commands ran through RTK with the prescribed interpreters and explicit Framework environment. Exact arguments, prerequisites and receipts are retained under run ID `20261122-readiness-continuation`.

| Native command or procedure | Observed result |
| --- | --- |
| `ci/tools/new-change-record.py create` | Initial missing `TEST_ROOT` rejected; explicit complete Framework context passed. Editable native scaffolds created. |
| `ci/tools/verify-framework-candidate-contract.py` before synchronization | Exit 0 for actual Framework/MRTS candidate. |
| `ci/tools/sync-framework-component-versions.py` with `--validate`, `--sync`, `--check` | All exit 0; two lock fields and 22 registered references synchronized; final `changed=[]`. |
| Candidate verification after exact nested materialization | Exit 0. Initial exit 2, `cannot read pinned Framework Git source`, occurred before the new object existed in the nested object store; retained and corrected by materializing the exact commits. No guard changed. |
| Four existing explicit-MRTS-handoff regression methods | Passed in 27.632s at `94ce9c76eab09420d5a58f2f9b6b412405d70cbb`; relevant native tools are byte-identical at this record's base. Final staged-chain checks remain separate. |
| Original inheritance validator on private candidate composition | Exit 0: 27 Parent / 21 Framework / 12 MRTS entries, no violations or warnings. This validates the composition, not a future Parent commit. |
| Original inheritance validator on actual materialized Parent worktree | Exit 0: 27 Parent / 21 Framework / 12 MRTS entries, no violations or warnings; Parent base and exact physical Framework/MRTS above confirmed, still uncommitted. |
| Independent metadata comparison | All 22 workflow diffs contain only the selected ordinary Framework replacement; exactly two lock fields changed; protected tuples unchanged. |
| Framework lineage/security tests and native security contract | Exit 0. Bindings/archive/active checks passed with `CONNECTOR_TEST_PROFILE=parent`; the earlier missing-profile rejection is retained. |
| MRTS actual main CI and full Sonar readback | Four successful checks, two successful workflows; all five gate conditions OK, none ignored, overall/new Reliability A, Security A, Maintainability A; zero unresolved/new issues or hotspots at the exact revision above. |
| Framework #187 exact-head CI and full Sonar readback | 17 terminal checks: 14 success, three expected advisory skips; all four returned gate conditions OK, none ignored, overall/new Reliability A, Security A, Maintainability A; zero unresolved/new issues or hotspots at the reviewed head above. |

Native compiler-guide regeneration with `scripts/generate_compiler_guides.py` and the full Framework context exited 0; all 18 outputs remained byte-identical. Workflow file modes also remained unchanged.

Native Parent checks before this status-text update passed: full original bilingual checker exit 0 (6.739s), `ci/tools/new-change-record.py check` exit 0 (0.865s), synchronizer `--verify-primary --base 60a7b74e057769503d6b4cb01b2cc9ba8da875c8 --staged` exit 0 (1.571s) for the exact Framework/MRTS selection. Actual worktree inheritance already passed with 27/21/12 entries. Receipts: `parent-final-prechecks/native-final-checks.json`. Final repetition after this text update remains required; these results do not qualify an unpublished Parent commit.

## Security impact

No validation or gate is weakened. Protected broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` and protected Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` remain unchanged. No publisher, rootbroker, protected dispatch, administrative rule change, Sonar installation or authentication repair was performed. Existing CI analysis remains active.

## Runtime evidence

This pin transition changes no H2/H3 reader, executor, collector, schema or product runtime source. No new host/protocol qualification is claimed. Historical 2026-11-03 results retain their old revisions; their raw evidence location was absent on arrival. They cannot qualify this chain or prove reuse of a current SDK/build artifact.

## Known limitations

Actual Framework master `b4d619127a3fbd2a4074998e874c592d693413b9` now has nine terminal checks: eight success, one expected PR-context skip; all five workflows passed. Full stable revision-bound Sonar gate OK, all returned conditions OK, none ignored; overall/new Reliability A, Security A, Maintainability A; zero bugs, vulnerabilities or hotspots. One open MINOR `go:S8209` remains at `compositeenvoy/server_test.go:756`, created `2026-11-01T10:10:38`. Its key, rule, message, positions/flow and complete file blob match baseline `e1964415efcd3cda11614ce13b7d34331ee0cf06`; all regular code is unchanged across the pin transition. The server also counts this issue in the New Code Period. It is independently pre-existing, without a false-positive, acceptance or other disposition; this is not a zero-issue or globally defect-free master claim.

Parent primary/inheritance and full bilingual/archive checks passed as recorded above before this status-text update; final repetition, commit, PR and fresh CI remain outstanding. Exact local MRTS CPython 3.14.6 is unavailable; 3.14.4 was not substituted. Hosted 3.14.6 governance tests use an isolated policy fixture and do not replace the actual Parent composition check.

## Remaining risks

The installed pre-commit guard requires operator-owned V2 admission bound to the exact worktree, HEAD, staged index and selected Framework/MRTS source proofs. That new tuple is not installed. Private proof preparation does not grant installation authority. Reconcile any concurrent Parent movement and repeat the affected checks before normal delivery. At task takeover, the original workspace had unrelated `.gitignore` conflicts and a parallel `Makefile` modification. This task did not modify or restore that workspace; recheck its current state before any cleanup.

## Checks not run and rationale

No comprehensive acceptance campaign, new product build, host runtime or protected broker execution was run for this metadata-only transition. No current Parent PR gate exists yet. Native staged primary and full bilingual/archive checks passed after the new records entered tracked-file discovery; final repetition follows this status-text update. Historical baseline CI is not a substitute for those results.

## Final diff and review status

The semantic MRTS correction and actual Framework merge tree were reviewed; native Parent metadata synchronization and corrected candidate verification passed. This snapshot records preparation only. The exact staged diff, source admission, normal commit/PR and fresh head-bound CI/complete Quality Gate must still be verified before the authorized regular Parent squash merge. No Parent PR number or resulting commit is asserted.
