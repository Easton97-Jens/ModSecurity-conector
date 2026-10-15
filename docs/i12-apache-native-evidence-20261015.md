# Apache I12 native host evidence — 2026-10-15

**Language:** English | [Deutsch](i12-apache-native-evidence-20261015.de.md)

The Apache assessment remains **partial**. This report does not grant approval or claim `I12_COMPLETE`. The [155-case machine ledger](../reports/audits/apache-i12-20261015/case-ledger.json) is authoritative for each original ID, qualification, missing observation, and evidence reference. Missing observations remain `null`; one execution does not qualify unrelated aliases.

## Scope and identity

The isolated evidence branch is `codex/i12-apache-410-20261015`, based on PR #410 at `f27eb59b53beff6f65384fc2e5037881a3052c01`. Its delivery target is `work/pr382-i12-host-evidence-20261011`, not `master`. PR #410 is not changed directly.

The reused sealed, instrumented runtime identifies product source base `02754040bced960cfc1857416cd7101bb3116ef4`. This identity is distinct from the evidence branch base. Comparisons retained in the evidence packets bind the selected Apache/Common files to the current base; they do not establish whole-repository runtime identity. Framework is `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS metadata is `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. MRTS was not exercised or modified.

Apache `2.4.66`, APR `1.7.6`, and libModSecurity `3.0.14` are qualified only with the binary, module, SDK, effective configuration, run, UID, process, and source hashes in each approved packet. No result transfers automatically to another build. Native hosts run in the existing private controller with UID/GID `65534`, zero capabilities, `NoNewPrivs`, read-only input bindings, bounded resources, and separate network/mount/PID namespaces.

Only Apache I12 fixtures, harness extensions, tests, and Apache evidence were added. The central matrix, report generators, capture manifest, shared observers, other connectors, workflows, Framework/MRTS Gitlinks, and production code remain outside this change.

## Qualification snapshot

| Item | Observed result |
| --- | --- |
| Apache mandatory cases | 155 |
| Historical executed cases | 25 |
| Historical configuration PASS | 9 |
| Historical full lifecycle PASS | 1 |
| Fresh actual host executions, distinct required IDs | 28: 8 newly qualified and 20 partial packets, including the unsigned baseline replay |
| Required IDs without a fresh host execution | 127 |
| Total retained private attempts | 46, including setup failures and the separate no-fault control |
| Unique full lifecycle PASS, old and new | 9; 146 IDs still lack a complete lifecycle PASS |
| Newly qualified host cases | 8: seven requests and the independently reconciled duplicate-header case |
| Original 54 oracle expectations resolved | 8, including the historical lifecycle case |
| Original oracle expectations still open | 46 |

Counts come from the machine ledger; individual qualification remains authoritative. The baseline replay confirms behavior but is retained as an unsigned candidate, so it adds no newly qualified ID. The seven request cases are `NEED-request-empty`, `NEED-request-single-chunk`, `NEED-request-content-type-present`, `NEED-request-content-type-missing`, `NEED-request-charset-present`, `NEED-request-charset-missing`, and `NEED-request-csv`. Their distinct executions retain client results, backend counts, native phase calls, physical events, EOS/commit ordering where required, finish, cleanup, and follow-up observations. A fresh baseline retake also preserves the existing lifecycle proof.

`phase2_truncated` sends a completely framed 65-byte request under native `ProcessPartial`. It does **not** prove truncated HTTP transport. MIME, response-limit, denial, and redirect executions remain separate host facts when their original event metadata or lifecycle requirements are missing. Phase-3 fixtures return 403/302 for their neighbor too because fixture response headers apply globally; those packets remain partial.

## Duplicate-header oracle

The original fixture and original failure are retained. The four independently checked boundaries are:

1. Wire capture contains two `X-No-Crs-Duplicate` fields with values `one` and `two`.
2. The pinned Apache Core/APR path merges them to one field with value `one, two`.
3. The connector mapper forwards the resulting field without inventing a split.
4. Native SDK probes distinguish the original two-value/count-two oracle from the merged single-value/count-one oracle.

A supplemental Apache-specific fixture uses `one, two` only for that confirmed version-bound Core behavior. Independent reconciliation qualifies this scoped case; its actual host success does not erase the original FAIL. A single literal `one, two` field is ambiguous with a merged pair after that boundary; downstream SDK evidence cannot reconstruct the original wire cardinality.

## Physical sink retakes

The [bounded evidence directory](../reports/audits/apache-i12-20261015/) retains the five original fault definitions and readback. These are five physical scenarios, not proof of all operation-specific `NEED-physical-event-sink-*` obligations.

| Fault | Actual main client | Follow-up / neighbor | Backend main / follow-up / neighbor | Physical boundary |
| --- | --- | --- | --- | --- |
| Missing parent path | 500, 571 bytes, exit 0 | 200 / 200 | 0 / 1 / 1 | Common/POSIX rejection before APR; APR open `null` |
| `/dev/full` path | 500, 571 bytes, exit 0 | 200 / 200 | 0 / 1 / 1 | Common/POSIX rejection before APR; APR open `null` |
| Parent mode `0500` | 500, 571 bytes, exit 0 | 200 / 200 | 0 / 1 / 1 | Common/POSIX rejection before APR; APR open `null` |
| Closed descriptor | 500, 571 bytes, exit 0 | 200 / 200 | 0 / 1 / 1 | Real APR `EBADF` 9; zero bytes written |
| Physical ENOSPC | 500, 571 bytes, exit 0 | 200 / 200 | 0 / 1 / 1 | Real APR `ENOSPC` 28; zero bytes written |

ENOSPC is produced by rebinding the admitted task-owned descriptor to `/dev/full` with `dup2`, followed by the real APR write. Filesystem-capacity exhaustion was not tested.

The latter two faults perform a real descriptor operation before forwarding to APR; they do not substitute an APR return value. Later native sink writes succeed on reopened descriptors. Persistent invalid path/device/permissions are not repaired: successful follow-ups show request-scoped host recovery. Follow-up and neighbor clients each receive 3 bytes and exit 0. Native/API and host transcripts, physical JSONL, process maps, FD samples, and host/backend/controller cleanup remain separate evidence.

A same-boundary no-fault control uses `/sink-disruptive` and rule `120016` to distinguish the ordinary denial path from sink-failure behavior. Configuration of that rule alone does not prove its execution: the failing paths also log the earlier nonterminal rule `120001`. The no-fault control returns 403 with 239 bytes and physical Common events for `120001` then `120016`. Fault cases also contain a native disruptive 403: absence of physical Common rule `120016` does not prove that the engine did not evaluate it. Independent native audit attribution to `120016` remains `null`. The control records successful APR writes of 1052/1087/1049/1049 bytes. All 18 observed transactions have exactly one native/Common cleanup, and all six relevant controllers report clean terminal cleanup.

All five fault packets remain incompletely qualified: native audit, default Apache error-renderer commit binding, and other original lifecycle observations are missing. Their `full_lifecycle_qualified` values remain false and missing outcomes remain `null`.

## Fixture failures and independent repair

Initial canonical runs exited 78 because their required `tests/rules/no-crs-baseline.conf` preamble was omitted. Apache-only launch settings now forward `MODSECURITY_RULE_PREAMBLE_FILE`; Framework validation was retained. Those failed attempts remain setup failures.

Response-limit fixtures then exposed duplicate rule `1100301` between the original local rule and the canonical preamble. Local actions omit explicit `t:none`; the canonical form includes it. Real SDK probes compared both forms with identical directives, no `SecDefaultAction`, and the exact 64/65-byte ASCII fixture payloads. Append/P4 results, intervention, status, and logged rule IDs matched. New fixtures remove only the local duplicate and retain the canonical rule, original YAML/hash, expectations, proof, and original load failure. This is a scoped semantic proof, not universal textual equivalence.

The corrected `ProcessPartial` fixture checks a native 64-byte inspection buffer with non-disruptive rule `91041504`, independently motivated by SDK `src/transaction.cc:1195-1206`. Earlier marker expectations that could not match their payload are preserved as fixture errors. Reject expectations were not changed to manufacture PASS. The deduplicated at-limit and over-limit retakes reach real host execution with driver/controller exits 0. The Reject retake `attempt-1792074553855617952` exits driver 78/controller 77 without HTTP: the original NGINX-only `runtime_materializable:false` case yields an empty selection and `IsADirectoryError`. This retained setup failure leaves a real Apache Reject driver missing; Reject currently has independent SDK evidence only. No shared validation flag is changed. Host rejection and event/lifecycle metadata still require individual qualification.

One controller attempt reported three transient namespace survivors. A later readback found them gone; the original failed cleanup receipt remains retained. It is not silently converted to a clean initial result.

## Verification and reproduction

Fresh checks recorded by the task include 122 focused tests plus five packaging qualification tests, 76 native regression tests, capture verification plus 15 capture tests, and the focused launcher checks. The mapper mutation was detected by five tests with 14 failed assertions; the sink mutation was detected by eight tests with two failures. Mutation failures are expected negative evidence, not passing unmodified test executions. Exact commands, exits, hashes, and scope belong to the [packaged receipts](../reports/audits/apache-i12-20261015/). [Identity](../reports/audits/apache-i12-20261015/identity.json) records full binary/SDK/module hashes; [readback](../reports/audits/apache-i12-20261015/readback.json) exposes all attempt exits and bounded observed facts. These summaries do not replace physical SHA-bound captures retained under the external run root.

Documentation checks passed (exit 0): `check-bilingual-docs`, `check-doc-links`, and repository path references, using an existing Framework read-only inside a private mount namespace. Original Gitfiles/Gitlinks and host mounts were preserved. The initial direct worktree run failed because its Framework was not populated; the corrected German link and namespace rerun are both recorded. `new-change-record.py check` and `git diff --check` passed (exit 0). The bounded `root-review-*.py` artifacts preserve the exact task-specific review assertions; they require the retained run inputs and are not a generic auto-approval mechanism.

Reusable entry points are `ci/runtime/lifecycle/apache-i12/prepare.py`, `prepare_sinks.py`, `review.py`, `ledger.py`, and `package.py`. All shell invocations use RTK. Preparation seals new inputs and never launches a host. Root executes the existing approved private controller; `launch.py` / `sink_launch.py` retain actual waited exits. Review extracts candidates; explicit independent review precedes ledger acceptance.

```sh
rtk proxy python3 ci/runtime/lifecycle/apache-i12/prepare.py --list
rtk proxy python3 ci/runtime/lifecycle/apache-i12/review.py --help
rtk proxy python3 ci/runtime/lifecycle/apache-i12/ledger.py --help
rtk proxy python3 ci/runtime/lifecycle/apache-i12/package.py --help
rtk git diff --check
```

Preparation requires the existing PyYAML environment, for example the already sealed `python-site` binding; no dependency installation is implied. Output paths are new directories below the approved external run root. `--deduplicate-response-rule` additionally requires the exact native semantic proof and rejects changed inputs.

## Remaining work and delivery boundary

The machine ledger lists every missing case and incomplete field. Streaming/chunk split, transport truncation, keep-alive, unexercised failures, and missing physical/lifecycle metadata cannot be inferred from the completed request cases or sink probes. Confirmed product defects require a separately authorized fix on #382; this branch contains no product fix.

Normal commits and a Draft PR are authorized for the isolated branch and #410's branch target. This report records evidence rather than a CI, merge, or approval outcome. No force-push, automatic merge, release, or I12 completion is authorized or claimed.
