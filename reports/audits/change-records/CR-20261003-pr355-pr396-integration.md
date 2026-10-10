# Change Record: PR #355 integration into the PR #396 successor

**Language:** English | [Deutsch](CR-20261003-pr355-pr396-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261003-pr355-pr396-integration` |
| Date (UTC) | `2026-10-03` |
| Base revision | `ac4c746f6a4c07006f25b078f660e31b16341479` |
| Original PR #355 base | `b779167ff979aa73cdd9321a829f9c693d943760` |
| Original PR #355 head | `b42ebda511cb9b6dca1de5c23b1b7b55ee400fd8` |
| Local ordered-port checkpoint | `0cfb8f900cbc3839c1590ba6f90683ab144ac7ef` |
| Starting Framework head | `2e721082d2d2bdead188995aeb7c9151a6dd518b` |
| Current Framework documentation successor | `b9b9534b7e0b15edad31393699ebd0617748148d` |
| Parent callback correction | `28ecd53d61f9b9065ba687ead373dcae53969368` |
| Parent strict-artifact correction | `3dcd9980cece2afec29dad61ec824b3f63cc84f7` |
| Parent dependency-binding checkpoint | `2c880b9319abb381daa29a073669d1668eba1a82` |
| Starting Collector revision, Parent ancestor | `8fe56043968fa4989f5dcf4f5b48f24dbeb3fe6f` |
| MRTS, read-only | `615b13bacbd008562c17408246c41ab27dca3104` |
| Last observed PR #396 remote head | `2634d821acd80ad208a8e1cd3e4f49fd7e80c628` |
| Delivery status | Framework published to Draft PR #135; Parent remote delivery pending; PR #355 and PR #396 OPEN/DRAFT/UNMERGED |

## Motivation and problem statement

PR #355 contains the protected exact-head NGINX workflow and privileged
execution boundary. PR #396 is the successor carrying newer lifecycle,
configuration and Canonical work. Their histories diverged; integrating the
complete older security contract requires preserving the newer behavior and
proving every original commit and file. Closing PR #355 depends on verified
remote supersession by PR #396, not merely a local port.

## Acceptance criteria

Account for all 19 original commits and 25 original changed files. Preserve
the dispatcher, trusted-base identity, exact candidate-head validation,
artifact digests, private runner/root boundary, retained-descriptor launcher,
worker separation, root-owned evidence, bounded cleanup and fail-closed checks.
Revalidate protected tests and current Parent/Framework/Collector regressions;
retain the closed `empty_header_value`, `invalid_boolean` and `invalid_size`
records. Keep protocol wiring separate and MRTS unchanged. Only after passing
gates, correct dependency references, a verified PR #396 push/read-back and
relevant remote CI may PR #355 be closed without merge. Neither a Full E2E
run nor Exact-Head E2E PASS is part of this integration stage.

## Implementation decision and rationale

Use an isolated authoritative Parent worktree based on the committed local
successor, leaving uncommitted protocol wiring in its original checkout.
Seventeen non-merge PR #355 commits were cherry-picked in order with `-x`
provenance. The two upstream merge commits refer to ancestors already
satisfied by the newer base; they are accounted for separately rather than
replayed as a competing branch merge. The local port checkpoint is
`0cfb8f900cbc3839c1590ba6f90683ab144ac7ef`; this is not a final verified or
remote successor identity. Ancestry, original blobs and the index union
account for all 19 commits and 25 net paths in the finalized machine proof:
17 ordered `-x` ports, the two upstream merge commits
(`5368569351e968e8ea641fc485590654df6a4336` and
`acc0ca1d22fd8a452453e66f51115ce026517b52`) proved as ancestors,
23 byte-equal net paths, and two archive indexes
resolved by an addition-only union. Coverage is 19/19 commits and 25/25 files;
this does not certify all semantic or delivery gates.

Resolve the EN/DE archive-index conflict as a union: retain current records,
the protected-base entry and the correct English link. The historical
23-path checklist is clarified to include the two review-package paths in
the final 25-path scope, without changing historical evidence.

Fresh compatibility inspection found an `&&`/`||` callback guard that rejected
the valid `on` plus callback `1` combination in a real shell reproduction
(exit 19). Its test-first correction passed nine callback controls. Builder
adaptation preserves strict source/artifact admission while reconciling the
current native source and library-input layout. Builder and launcher checks
passed 23 and 46 tests. A cross-producer collector regression also failed
before its correction and passed afterwards: only two collector constants
were aligned to NGINX `1.31.5` and source digest
`e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279`;
19 collector tests passed. The Collector revision above is a Parent ancestor,
not a separate repository or independent delivery boundary.

The historical reference audit found Framework
`2e721082d2d2bdead188995aeb7c9151a6dd518b` unpublished and the then-current gitlink
`cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` could not consume the Boolean/size
receipts. The documentation-only successor
`b9b9534b7e0b15edad31393699ebd0617748148d` has now been published separately
without force push to [Framework Draft PR #135](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/135),
observed OPEN/DRAFT/UNMERGED. Its six remote CI jobs are queued, not PASS.
The dedicated Parent gitlink commit
`2c880b9319abb381daa29a073669d1668eba1a82` binds this Framework successor and
unchanged MRTS `615b13bacbd008562c17408246c41ab27dca3104`.
The protected workflow's master-base and base-equal-gitlink requirements
remain enforced. Stacked PR #396 is ineligible for manual protected execution
under that unchanged contract.
The Framework documentation-only successor is now
`b9b9534b7e0b15edad31393699ebd0617748148d`; code, tests and catalog remain
identical to `2e721082d2d2bdead188995aeb7c9151a6dd518b`.

## Security impact

No control may be relaxed to make the integration pass. Candidate callback
or JSONL values remain untrusted observations, not root attestation. Preserve
protected workflow permissions, actor/repository/base checks, runner preflight,
exact artifact admission and evidence read-back, and the FND-PARENT-1038
private root-parent cleanup contract. FND-PARENT-1038 remains `in_progress`;
FND-PARENT-1036 remains `blocked_external_dependency`. Ported source and local
tests do not resolve external protected-host or security-archive requirements.

## Changed files

The original PR #355 net inventory contains these 25 paths; local porting is
present and covered by the finalized machine proof; remaining validation and
delivery gates are separate:

- `.github/actionlint.yaml`
- `.github/workflows/run-protected-nginx-exact-head.yml`
- `ci/runtime/broker/nginx_exact_head_result_collector.py`
- `ci/runtime/broker/nginx_exact_head_root_launcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_builder.py`
- `ci/runtime/broker/protected_nginx_exact_head_dispatcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_runner_preflight.py`
- `ci/runtime/broker/run_nginx_exact_head_cells.sh`
- `docs/security/protected-exact-head-host-gate.md`
- `docs/security/protected-exact-head-host-gate.de.md`
- `docs/security/protected-exact-head-nginx.md`
- `docs/security/protected-exact-head-nginx.de.md`
- `docs/security/protected-exact-head-review-package.md`
- `docs/security/protected-exact-head-review-package.de.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `tests/test_nginx_exact_head_base_helper.py`
- `tests/test_nginx_exact_head_result_collector.py`
- `tests/test_nginx_exact_head_root_launcher.py`
- `tests/test_protected_nginx_exact_head_builder.py`
- `tests/test_protected_nginx_exact_head_dispatcher.py`
- `tests/test_protected_nginx_exact_head_runner_preflight.py`
- `tests/test_protected_nginx_exact_head_workflow.py`

This paired integration record is additional traceability material. External
proof artifacts are `pr355-full-integration.csv`,
`pr355-integration-summary.md`, `pr355-file-coverage.csv` and
`pr355-commit-coverage.csv` under
`/var/tmp/codex/ModSecurity-conector/analysis/`. The required proof accounts
for 19/19 commits and 25/25 files without `UNKNOWN`, `IGNORED` or `DROPPED`.
The finalized proof satisfies both totals; this is not a claim that all
verification gates passed.

## Commands executed

### Tests and actual results

The original-range `rtk proxy git diff --name-only` inventory confirmed
25 changed paths. The coordinator observed fresh RTK-wrapped results:

- Combined protected suite: 139 tests passed; independent focused suite: 75 tests passed.
- Callback controls: test-first failure then nine passes; builder: 23 passes; launcher: 46 passes; cross-producer collector: test-first failure then 19 passes.
- Parent security suite: 164 tests, exit 0, with five skips. Two require the unavailable `nobody` identity in this user namespace; one requires an unavailable dedicated unprivileged identity capability; two require unavailable mount/PID namespace capability. Exact skip evidence is retained in `analysis/pr355-parent-gates-20261003.log` under external task storage.
- actionlint, error-level ShellCheck on the discovered actual paths, syntax and diff checks: exit 0. The first ShellCheck command with erroneous paths is retained as a diagnostic, not passing evidence.
- Native bilingual and documentation-link checks passed after materializing Framework `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` in the worktree. This resolves the earlier missing-relative-link failures; it does not verify compatibility of that old reference with newer receipts.
- Fresh final-head Framework No-CRS: 166 passes; API: 23 passes, at `b9b9534b7e0b15edad31393699ebd0617748148d`.
- Framework lint initially failed at an existing FIFO/spawn measurement (attempt 3 missing readiness). Three isolated repetitions of the unchanged test passed all nine strict attempts. A second whole-lint run passed the heavy provenance/archive cases, then failed because of an incorrectly inherited `FRAMEWORK_ROOT`/tool-repository identity. This invocation error is not a demonstrated new source defect. The final whole-lint run with explicit `FRAMEWORK_ROOT` and environment roots (session `60548`) completed with exit 0: PASS.
- Broader Parent suite: terminal FAIL, 816 tests. In the requested 810-test scope, 809 were green and one sandbox-UID test failed. An exact root-to-`nobody` materializer-unit host rerun passed its one test; it made no NGINX requests. The six extra multi-connector tests produced 14 subtest failures and one error, reproduced at base `ac4c746f6a4c07006f25b078f660e31b16341479` with unchanged sources. No PR-#355-scope regression was demonstrated; the complete failed log remains retained, and the broad run is not relabeled PASS.
- Additional Parent native lint first failed on a legacy Apache `OUT` condition; its second run failed at a CLI/Make root-override fixture. The isolated 20-test environment-root-binding check passed. The final native-lint run (session `20449`) was deliberately terminated with exit 143 under the job resource contract: actual host execution encountered missing HAProxy headers and entered a large libmodsecurity build despite runtime allowance being disabled. No real HAProxy headers were found in the selected cache for a bounded repeat. Extra Parent full lint remains UNVERIFIED; no additional source fix is claimed.
- Independent native CI-consumed targets `check-common-sdk-contract`, `check-adapter-contracts` and `check-directive-parity` each passed with exit 0. These targets do not invoke the six baseline multi-connector modules. The user-required 810-test scope is satisfied by the 809 green tests plus the exact host-ownership rerun; protected 139, statics, security, documentation and full Framework gates passed. The separate broad 816-test run remains FAIL.
- The original size-configtest bundle's 47 checksums passed again. This revalidates the original source/artifact/run identities, not current-head runtime.
- The historical Parent 99-test dependency focus before gitlink binding completed with three correct provenance guard skips. The final post-binding rerun (session `21082`) passed all 99 tests with no skips in 19.276 seconds, exit 0; all identity controls executed with Framework gitlink `b9b9534b7e0b15edad31393699ebd0617748148d`.
- Current-head Framework PR #135 Sonar readback reports Quality Gate `OK`, zero bugs and vulnerabilities, and 28 open maintainability findings. This is not a zero-finding or runtime claim; Parent current-head analysis and remote CI remain separate delivery gates.

After this record update,
`rtk proxy make check-bilingual-docs check-doc-links PYTHON=python3 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/pr355-integration-docs`
passed with exit 0, including repository path references; the repeated
`rtk proxy git diff --check` also exited 0.

Historical 98/99/129-test and Sonar checkpoints in the older Change Record
remain historical and do not prove the integrated successor.

## Runtime evidence

No fresh protected-host runtime or independent host attestation is claimed.
The prior selected configtest evidence and its checksum receipts retain their
own source/artifact/run identity; they do not prove this integration's runtime.
Exact-Head E2E PASS: NO.

## Checks not run and rationale

Full Exact-Head E2E is expressly deferred. Framework publication and the local
Parent gitlink binding are complete, but this checkpoint has no Parent push,
PR #396 successor read-back, passing remote CI confirmation or PR #355 closure.
These are conditional later delivery steps. Protected host
bootstrap, Environment, dedicated runner and independent attestation remain
external prerequisites; unavailable host evidence cannot be replaced by a
source test, build, configuration load or client-only observation.

## Known limitations

Commit provenance and file presence are distinct from complete equivalence.
Remaining remote gates must finish before remote
supersession. Full Framework lint passed; optional extra Parent full lint
remains UNVERIFIED after resource-contract termination. The broader Parent
run remains FAIL with the scoped rerun and baseline reproduction above.
Starting coverage was 97 selected, 51 open required and 8 open configuration
records; these are historical starting values, not a new measurement.
Canonical/MIME work resumes only after PR #355 is verified closed.

## Remaining risks

Incorrect adaptation could regress current source materialization, lifecycle
containment, projection freshness, ownership ordering, first-byte handling,
native events, redirect Location, port cleanup or configuration receipts.
The unprivileged lexical artifact handoff still requires root-side descriptor
and digest re-admission and later protected-host evidence. No Sonar result or
security finding disposition is forecast for a future head.

## Final diff and review status

INCOMPLETE: ordered local porting and finalized 19/19-commit and 25/25-file
machine proof exist; Framework publication and local Parent dependency binding
are complete; the final post-binding 99-test identity focus also passed
without skips. Remote CI verification and Parent remote delivery gates remain
pending. The requested local
gates passed as qualified above; the optional extra Parent full lint remains
UNVERIFIED, and the broad 816-test run remains FAIL. Framework PR #135 remains
OPEN/DRAFT/UNMERGED with six CI jobs queued. PR #396's last observed remote
head remains `2634d821acd80ad208a8e1cd3e4f49fd7e80c628`; no Parent push has
occurred at this checkpoint.
PR #396 remains OPEN/DRAFT/UNMERGED;
PR #355 remains OPEN/DRAFT/UNMERGED and is not yet eligible for closure.
No master merge, protocol commit, MRTS write or Full E2E is asserted.
