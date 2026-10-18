# Change Record: CR-20261018-haproxy-current-capture-builds

**Language:** English | [Deutsch](CR-20261018-haproxy-current-capture-builds.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-current-capture-builds |
| Date (UTC) | 2026-10-18 |
| Base revision | `ea62ca995557e7c71dd268e1359fb7b62cc8fe32` |

## Motivation and problem statement

Historical capture objects describe an older product tree. Reapplying their complete old files would discard current Common, mapper, SDK-accessor and request-authorization changes. Prepare current HAProxy instrumentation from a complete selected Git archive while preserving historical capture identities and results.

## Acceptance criteria

Reuse the existing Registry, observer collector and v2 disposable-source inventory. Admit only exact, unique historical delta contexts or the explicitly reviewed current allocation/SPOP ports. Preserve current product bytes outside those deltas. Record source/archive/SDK/command/binary identities, build three fresh variants, and keep compilation separate from runtime qualification.

## Implementation decision and rationale

`i12_current_capture.py` exports full 40-character-revision Git archives, records file modes/hashes and gitlink metadata, and creates fresh external source copies. Gitlinks are not materialized. Registry repository objects are reconstructed only from exact hash-matching members of the current or historical archives; that resolution directory is never a product build tree. The original shared manifest and capture objects remain unchanged.

The ordinary instrumentation port requires unique complete context and accepts no fuzzy match. Two reviewed adaptations preserve current semantics: observe the private `begin_request_with_scope` allocation seam shared by direct, companion and request-only authorization calls, forwarding `request_authorization_only`, actual return, native/Common handles and saved errno; bracket the current SPOP companion/request-authorization branch with the existing sample observations. A changed private signature or SPOP branch fails closed.

`i12_request_scope_observer.c` includes the existing observer implementation once and adds its existing `COMMON_TIME_WRAPPER(finish_request_authorization, "common_finish_request_authorization", 0)`. Link this translation unit instead of the ordinary observer C object. It observes actual Common entry/return state, preserves a request-only phase mask of `3`, and retains identity mapping until ordinary cleanup. It does not synthesize P3/P4, EOS, completion or a mask of `15`.

The current version contract pins HAProxy `3.2.25`, archive SHA-256 `d59a68d0daef7b5c596b019b742089788ff1748513ef96e71fe7b3943577866e`. After hash verification, eleven release-fixture symlinks are materialized as ordinary files from regular members of that same archive. No filesystem symlink is created or followed. Absolute/escaping links, missing or chained targets, hardlinks, special files and duplicate members are rejected. The normalization receipt records every original link, resolved member, content hash and mode. Existing native staging refreshes current Common headers/TUs, mapper, profile registry and runtime client inputs. Agent feature flags retain TU-owned `_GNU_SOURCE` definitions and all compiler warnings. The selected capture-tool Python module and build inputs must be trusted operator-selected files.

## Changed files

`connectors/haproxy/harness/i12_current_capture.py`, `connectors/haproxy/harness/i12_request_scope_observer.c`, `tests/test_haproxy_i12_current_capture.py`; this EN/DE Change Record pair. No product, shared capture, central matrix, Framework/MRTS, other connector or historical R1 artifact change.

## Commands executed

The prior focused command `rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -s tests -p test_haproxy_i12_current_capture.py -v` passed nine tests, exit `0`; receipt: `i12-haproxy-415-acceptance-20261015/builds/verification-current-capture-final-20261018/receipt.json`. Review added three source-port tests for allocation scope/identities, changed private signatures and SPOP branch placement/changed anchors. Only those three new methods were rerun, all passed, exit `0`; the unchanged nine were not repeated. The scaffold command was `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/tools/new-change-record.py create --name haproxy-current-capture-builds --base-revision ea62ca995557e7c71dd268e1359fb7b62cc8fe32 --date 2026-10-18`. Exact build argv, exits and output hashes are in external `builds/current-ea62-v4/build-commands/commands.json` and `retry-build-commands/commands.json` under the same run. The completion driver exited `0` after all three fresh builds; `completion-receipt.json` binds 15,761 raw artifacts. Separate `materialized-input-audit.json` checks every original current file against its original or declared capture hash and records three source inventories, 1,391 pristine upstream files, generated host files and additional Common runtime/header copy bindings.

Documentation checks passed, exit `0`: `rtk proxy env PYTHONNOUSERSITE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs`, the same command with `check-doc-links`, and `rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/tools/new-change-record.py check`. These validate documentation structure/links, not runtime evidence.

## Security impact

No production security control changes. Archive/path admission and exact source bindings protect the evidence boundary. Failed attempts remain explicit; no error is converted into success, no compiler warning or gate is disabled, and no credential is recorded. This trusted local build consumer does not sandbox an arbitrary supplied Python capture tool.

## Runtime evidence

Build-only result from `ea62ca995557e7c71dd268e1359fb7b62cc8fe32`: direct binary SHA-256 `beee0738953f07810b0de7a1b9b30ed6d32717b4cf37753011cbf2bd5b330237`; companion `e55d5ae4de28c9d04ee7ada6a52f5ecc7e752d5418787626c61a9df3c4938a0e`; SPOP agent `56a81b2ea8119144511c9a72ab2daaacb81c9ec0dcdb71fff1ee32e2a4e4818d`. `nm` confirms the request-authorization-finish wrapper in all three, and `readelf` receipts bind dynamic-link metadata. The SDK inventory binds the actual compatible `3.0.14` library and headers. These are three build artifacts and zero host runs by this producer, with `runtime_qualified: false`. Independent host evidence and original-oracle qualification remain separate; an SPOP ACK does not qualify the response companion.

## Known limitations

Initial attempts failed on exact repository-object resolution, unsupported archive links, a missing observer include path and redundant `_GNU_SOURCE` definitions. Their raw logs and consumer snapshots remain retained. The last initial agent attempt exited `1` under unchanged `-Werror`; the successful independent retry rebuilt every agent/observer object in new directories while retaining the already successful fresh companion build. Direct was then built fresh. The complete post-build inventory audit is a separate run-scoped receipt, not an automatic output guaranteed by every future producer invocation. Host compile logs retain mixed-declaration warnings, an unused precommit helper and upstream unsupported-warning-option notes.

## Remaining risks

A later Common-sink product integration requires a new complete source export, instrumentation port and fresh builds; these binaries cannot prove that later revision. The observer does not establish physical Common sink success, native deadline support, native file API use, actual client commit/reset or exactly-once cleanup without independent runtime observations. Local tests do not establish a Sonar server Quality Gate result.

## Checks not run and rationale

No host runs, product regression builds, server Sonar analysis, Git delivery or lifecycle qualification were performed during this documentation/source-port review. The build and nine-test results above are retained prior evidence; the three newly added tests were executed separately. Broader unchanged test suites were not repeated.

## Final diff and review status

The producer and observer bytes remain identical to the frozen successful retry consumer. This review adds tests and the paired Change Record only. Documentation validation and exact review receipts are retained externally; no commit, push, merge or final I12 acceptance is claimed.
