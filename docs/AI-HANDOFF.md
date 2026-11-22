# AI handoff

**Language:** English | [Deutsch](AI-HANDOFF.de.md)

## Snapshot and goal

PREPUBLICATION snapshot, **2026-11-22 UTC**. Continue the explicitly authorized reviewed MRTS #7 → Framework pin follow-up → Parent pin follow-up, including regular exact-head squash merges after the applicable checks. Parent branch: `codex/inheritance-pin-chain-20261122`; selected base: `60a7b74e057769503d6b4cb01b2cc9ba8da875c8`. This snapshot does not assert a Parent commit, PR or merge. Reconcile current HEAD, index, remote state and source proofs before continuing.

| Repository boundary | Observed state |
| --- | --- |
| [MRTS #7](https://github.com/Easton97-Jens/MRTS/pull/7) | Merged reviewed head `9a855b092645733ea8ff73a512aff7bfe916407e` as actual main `488e75388d917615feecab91650c3278b9c78b1e`; reviewed tree preserved, sole parent `ee2174431c4edf97e66afe32558ce8454deb2397`. |
| [Framework #187](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/187) | Merged reviewed head `0cf20b680bef0ba5dd635f874cea1626de8bdef3` as actual master `b4d619127a3fbd2a4074998e874c592d693413b9`; reviewed tree preserved, sole parent `e1964415efcd3cda11614ce13b7d34331ee0cf06`, nested MRTS `488e75388d917615feecab91650c3278b9c78b1e`. |
| Parent | #458 preserved `TMPDIR`; #459 already adopted Framework `e1964415efcd3cda11614ce13b7d34331ee0cf06`. This follow-up prepares Framework `b4d619127a3fbd2a4074998e874c592d693413b9` / MRTS `488e75388d917615feecab91650c3278b9c78b1e` from the selected base. Publication and exact operator admission remain outstanding. |

At task takeover, the original user checkout had unrelated `.gitignore` conflicts and a parallel `Makefile` modification. This task did not modify or restore that checkout. Work proceeds in the isolated task worktree; recheck the current original-checkout state before any cleanup.

## Relevant components and completed work

MRTS changes only the inherited `PARENT-ARCHITECTURE-AND-BOUNDARIES` and `PARENT-COMMAND-EXECUTION` digests. Historical source preimages were recovered and reviewed: removal of an illustrative architecture reading-list entry, and clarification of the automatic Secrets-hook starter path. These do not expand write, installation, authentication, merge or MCP authority. This is not a blind checksum update.

Framework changes only `tools/MRTS` and its bilingual integration record between `e1964415efcd3cda11614ce13b7d34331ee0cf06` and `b4d619127a3fbd2a4074998e874c592d693413b9`. Product/test/analysis/SDK helpers are unchanged across that interval. Inventory remains 100 core cases, 80 selectors and 1144 offline exceptions. Earlier SDK layout/PCRE2 changes are already in the Parent base; this follow-up introduces no new runtime or reader path.

The native Parent synchronizer updated two lock fields and 22 registered Framework references. Candidate verification passed before synchronization and after exact nested materialization; native `--validate`, `--sync` and `--check` passed. The initial post-sync object-availability failure is retained as a preparation failure, not hidden by a code or guard change. See the [current Change Record](../reports/audits/change-records/CR-20261122-reviewed-mrts-pin-chain.md).

## Changes selected for the PR

The selection consists of the Framework gitlink, `ci/tooling/project-versions.lock.json`, 22 registered `.github/workflows/` projections, `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` and the current Change Record pair. No product source, test definition, generated measurement report or repository rule is changed. Generated metadata comes from `ci/tools/sync-framework-component-versions.py`; the Change Record pair uses `ci/tools/new-change-record.py` scaffolds.

## Decisions, rejected approaches and open work

Keep the joint Framework/MRTS contract: explicit `--mrts-sha`, `--expected-candidate-mrts-sha`, the strict five-key lock and existing toolchains. Protected broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` and protected Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` remain unchanged. No publisher, rootbroker or protected dispatch was invoked; no gate or administrative protection was weakened.

The installed pre-commit guard requires operator-owned V2 admission for the exact worktree, HEAD, full staged index, selected gitlink and complete Framework/MRTS proofs. The new exact tuple is not installed. Private proof preparation does not authorize protected installation. Prepare the concrete proposal and required evidence before requesting operator approval; normal task-branch delivery and regular merges are already authorized.

## Executed checks and limitations

| Scope | Result and boundary |
| --- | --- |
| MRTS actual main | Four checks and two workflows successful; complete revision-bound Sonar gate OK, five conditions OK, none ignored; overall/new Reliability A, Security A, Maintainability A; zero unresolved/new issues or hotspots. |
| Framework #187 reviewed head | 17 terminal checks: 14 success, three expected advisory skips; full stable Sonar gate OK, four returned conditions OK, none ignored; overall/new Reliability A, Security A, Maintainability A; zero unresolved/new issues or hotspots. |
| Inheritance | Original validator passed on both private candidate composition and actual materialized Parent worktree: 27 Parent / 21 Framework / 12 MRTS entries; no violations or warnings. The actual worktree uses the exact base and physical Framework/MRTS above, still uncommitted; this does not attest a future Parent commit. |
| Parent native preparation | Candidate before/after, synchronizer validation/sync/check all exit 0; independent comparison confirms only ordinary Framework replacements in 22 workflows, two lock fields changed and protected tuples unchanged; four existing handoff regression methods passed in 27.632s at `94ce9c76eab09420d5a58f2f9b6b412405d70cbb`, with relevant tool sources unchanged at the current base. Staged primary verification and full native bilingual/archive checks passed before this status-text update; final repetition follows. |
| Framework targeted checks | Lineage/security regressions and native security contract passed. Bindings/archive/active checks passed with `CONNECTOR_TEST_PROFILE=parent`; missing-profile rejection retained. Framework documentation checks passed before publication. |

Actual Framework master `b4d619127a3fbd2a4074998e874c592d693413b9` now has nine terminal checks: eight success, one expected PR-context skip; all five workflows passed. Full stable revision-bound Sonar gate OK, all returned conditions OK, none ignored; overall/new Reliability A, Security A, Maintainability A; zero bugs, vulnerabilities or hotspots. One open MINOR `go:S8209` remains at `compositeenvoy/server_test.go:756`, created `2026-11-01T10:10:38`. Its key, rule, message, positions/flow and complete file blob match baseline `e1964415efcd3cda11614ce13b7d34331ee0cf06`; all regular code is unchanged across the pin transition. The server also counts this issue in the New Code Period. It is independently pre-existing, without a false-positive, acceptance or other disposition; this is not a zero-issue or globally defect-free master claim.

Native compiler-guide regeneration with `scripts/generate_compiler_guides.py` and the full Framework context exited 0; all 18 outputs remained byte-identical. Workflow file modes also remained unchanged.

Native Parent checks before this status-text update passed: full original bilingual checker exit 0 (6.739s), `ci/tools/new-change-record.py check` exit 0 (0.865s), synchronizer `--verify-primary --base 60a7b74e057769503d6b4cb01b2cc9ba8da875c8 --staged` exit 0 (1.571s) for the exact Framework/MRTS selection. Actual worktree inheritance already passed with 27/21/12 entries. Receipts: `parent-final-prechecks/native-final-checks.json`. Final repetition after this text update remains required; these results do not qualify an unpublished Parent commit.

Exact commands and receipts are retained under run ID `20261122-readiness-continuation`, including `parent-pin-sync/commands.json` and `parent-pin-sync/candidate-after-materialization.json`. No current Parent PR/Quality Gate is asserted. Exact local MRTS CPython 3.14.6 is absent; 3.14.4 was not substituted. Hosted 3.14.6 governance tests use isolated policy fixtures and remain distinct from actual Parent inheritance.

No new product build, host/protocol qualification or comprehensive acceptance campaign ran for this metadata transition. H2/H3 reader/executor/collector/schema paths are unchanged. The [2026-11-03 readiness record](../reports/audits/change-records/CR-20261103-runtime-readiness-prerequisites.md) is historical, with older revisions and raw evidence absent on arrival; do not relabel its results or infer current build reuse.

## Repository-derived start, build and test commands

Use current `AGENTS.md`, routed policies, root `Makefile` and selected Framework-native contracts. Relevant next checks are the native candidate verifier, synchronizer `--check` / `--verify-primary`, inheritance validation and documentation checks: `rtk make check-bilingual-docs`, `rtk make check-doc-links`, `rtk make check-variable-documentation`, and `rtk bypass git diff --cached --check`. Supply their prescribed interpreters, full Framework context and external writable roots. Stage selected new records before checks that discover Git-tracked documents. Observed pre-update passes are recorded above; final repetition follows this status-text update.

Historical delivery details remain in the [2026-11-14 handoff Change Record](../reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.md) and [2026-11-19 security Change Record](../reports/audits/change-records/CR-20261119-composite-cleanup-redirect-haproxy-rule-id.md). Their old Draft, pin, operator and CI states are historical. Parent #454–#456 and Framework #179–#183 have since merged; do not resume them as open drafts.

## Next steps

1. Reconcile current Parent base and exact Framework/MRTS trees, lock, references and staged scope. Repeat the passed staged native primary/inheritance/documentation checks after this final status-text update; retain failures and corrected results.
2. Framework actual-master terminal CI and full revision-bound Quality Gate are read back as recorded above, including the retained MINOR issue. Finish complete source proofs, prepare the exact operator admission proposal and obtain its separately required installation approval; preserve existing guards.
3. Create the normal Parent commit and existing-or-new task PR with truthful EN/DE description. Verify its exact-head checks, reviews, conversations and complete applicable Sonar gate before the authorized regular squash merge; read back the resulting master and actual commit pair.
4. Update the handoff and retained final report with observed publication, merge and check results. Preserve unrelated workspace changes and historical evidence; clean only task-owned processes and disposable runtime artifacts.
