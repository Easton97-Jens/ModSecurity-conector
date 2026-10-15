# Change Record: CR-20261015-i12-apache-native-evidence

**Language:** English | [Deutsch](CR-20261015-i12-apache-native-evidence.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-apache-native-evidence |
| Date (UTC) | 2026-10-15 |
| Evidence branch | `codex/i12-apache-410-20261015` |
| Base revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |
| Draft PR target | `work/pr382-i12-host-evidence-20261011` |
| Actual sealed product source base | `02754040bced960cfc1857416cd7101bb3116ef4` |

## Motivation and problem statement

The Apache I12 baseline contains 155 mandatory cases, 25 historical executions, nine configuration PASS and one full lifecycle PASS. Configuration/client success alone cannot close missing native, physical event, EOS/commit, or resource-release observations.

## Acceptance criteria

Record all 155 original IDs separately, retain missing values as `null`, independently reconcile oracles, and preserve original failures. Extend existing Apache lifecycle packages; deliver Apache-only evidence on an isolated branch targeting #410's branch. No `I12_COMPLETE` or release approval is granted.

## Implementation decision and rationale

Reuse sealed source-v5/artifacts-v3 and existing capture/native/host observers. New fixture preparation, waited client capture, candidate review, ledger and packaging remain Apache-specific. Duplicate-header normalization is bound to confirmed Apache Core/APR semantics and native SDK evidence. Response-rule deduplication requires scoped real SDK equivalence for exact fixture payloads. Physical descriptor faults forward actual APR results unchanged.

## Changed files

Apache harness additions: `ci/runtime/lifecycle/apache-i12/`; focused Apache tests: `tests/test_apache_i12_*.py`; bounded evidence: `reports/audits/apache-i12-20261015/`; [English report](../../../docs/i12-apache-native-evidence-20261015.md), [German report](../../../docs/i12-apache-native-evidence-20261015.de.md), and this Change Record pair. The final Git diff is authoritative for exact filenames.

## Commands executed

RTK-wrapped native/focused checks, private-controller host runs, independent SDK probes, capture validation, mutation checks and `git diff --check` are recorded in the [evidence receipts](../apache-i12-20261015/). Focused launcher validation used `rtk proxy python3 -m unittest discover -s tests -p test_apache_i12_launch.py` and passed three tests. Fresh task suites recorded 122 focused tests plus five packaging qualification tests, 76 native regressions, and capture verification plus 15 capture tests. Mapper/sink mutations were detected: five tests with 14 assertion failures, and eight tests with two failures respectively. These are expected negative results.

Documentation/Change Record/path checks passed with exit0 after using a private read-only Framework mount for the isolated worktree. The initial missing-Framework/link failure remains recorded; no native checker was bypassed.

## Security impact

No production fix or weakened control is introduced. Hosts retain private namespaces, UID/GID `65534`, zero capabilities, `NoNewPrivs`, bounded resources and read-only sealed inputs. The APR interposer is opt-in and restricted to the private marker/target; real EBADF/ENOSPC returns are retained. Framework, MRTS, central manifests/observers, other connectors and workflows remain unchanged.

## Runtime evidence

The [case ledger](../apache-i12-20261015/case-ledger.json) carries individual qualification. At report preparation there are eight new full host PASS (seven request cases plus scoped duplicate-header reconciliation), nine unique full cases including the baseline; the original 54 oracles have eight resolved and 46 open. Five physical faults return 500/571 bytes with client exit 0, backend counts 0/1/1, and successful 200/200 follow-up/neighbor requests. Closed descriptor gives real APR 9/zero bytes; physical ENOSPC gives 28/zero bytes. Three earlier rejections precede APR, whose open remains `null`. The no-fault control returns 403/239 bytes and physical Common rules `120001`, `120016`. All 18 observed sink/control transactions clean up once; six controllers terminate cleanly. Fault packets still lack full qualification.

## Known limitations

The instrumented runtime's source base differs from the evidence branch base and is disclosed with component hashes. Native audit/default error-renderer commit binding remains incomplete for sink faults. Response MIME/limit and phase-3 packets do not become PASS from status alone. `phase2_truncated` is a fully framed ProcessPartial request, not HTTP truncation. A literal comma field remains ambiguous after Apache merging. The deduplicated Reject host attempt exits driver 78/controller 77 without HTTP because the original NGINX `runtime_materializable:false` fixture is not materialized; only the native SDK Reject probe is established. Missing observations remain `null`.

## Remaining risks

Forty-six original oracles remain open at the recorded snapshot. Initial missing-preamble exit 78, duplicate-rule configuration failures, impossible fixture-marker expectations, and one transient controller cleanup failure remain retained. Native disruptive 403 in fault cases does not independently attribute an audit rule. Product findings require separately authorized remediation on #382.

## Checks not run and rationale

This Apache-only change does not run unrelated connector/Framework/MRTS delivery or claim a whole-repository runtime sweep. Unexecuted mandatory cases are explicitly listed in the ledger. PR CI, review and merge outcomes are not inferred from local tests.

## Final diff and review status

Local validation receipts and the final diff define the reviewed scope. Normal commit/push and Draft PR delivery are authorized only on the isolated branch against #410's branch; no force-push or automatic merge is authorized. This record contains no fabricated delivery SHA, PR number, CI result or completion approval. Overall I12 status remains partial.
