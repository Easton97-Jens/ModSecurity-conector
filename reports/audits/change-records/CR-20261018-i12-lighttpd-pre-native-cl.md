# Change Record: CR-20261018-i12-lighttpd-pre-native-cl

**Language:** English | [Deutsch](CR-20261018-i12-lighttpd-pre-native-cl.de.md)

Exact diagnostic lighttpd Content-Length rejection scope.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-lighttpd-pre-native-cl |
| Date (UTC) | 2026-10-18 |
| Base revision | `047d426b` |

## Motivation and problem statement

The original `lighttpd-stock-native-control` contracts for `invalid_content_length`, `conflicting_content_length` and `content_length_overflow` allow HTTP400 rejection before connector allocation. The existing dedicated validator selects only Apache contracts and log formats. Inventing a native transaction, or relabelling lighttpd output as Apache output, cannot establish these diagnostic cases.

## Acceptance criteria

Admit exactly these three unchanged diagnostic mappings/oracles. Require separate Root source/request approval, actual HTTP400, backend0, a complete live native observer with zero main calls, healthy constructor/P1/P2/backend controls and actual positive Common sink controls before and after, private physical event/log windows, loaded images, all four nonroot UIDs, process identity and cleanup. Keep full lifecycle credit false and all mandatory body-route credit unchanged.

## Implementation decision and rationale

Explicit profile selection preserves the four existing Apache contracts and introduces three diagnostic lighttpd mappings. Common source, image, isolation, native sequence, event, client and cleanup checks remain required. Lighttpd selects its actual host-observer and independent backend row shapes. Its native Core log has no Apache PID/client prefix: the new separate producer binds the private0600 log's device/inode to the actual host's open descriptor, brackets the exact main interval with direct file observations, and verifies the parser diagnostic plus unique raw request path/header at nanosecond UTC precision. Apache format is never a fallback. No native allocation, phase call, EOS, finish or free is manufactured for the rejected request.

## Changed files

`ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py`, `tests/test_i12_lifecycle_ledger.py` and this EN/DE Change Record pair. No original inventory, oracle, product, Framework/MRTS or other connector file changes belong to this change.

## Commands executed

`rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/i12-lighttpd-412-completion-20261015/verification /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_i12_lifecycle_ledger tests.test_i12_oracle_reconciliation` —69 tests passed, exit0. Five new lighttpd tests include negative mutations for sibling/TE contracts, changed mappings, Apache schema substitution, stale/low-precision timestamps, other requests, wrong FD inode/PID/UID/mode, incomplete windows and uncorrelated backends/events. The unchanged existing Apache, normal35 and parser regressions also passed.

## Security impact

This is a bounded functional evidence-contract repair. It changes no production parser, UID, namespace, filesystem guard, compiler, CI or Quality Gate. It performs no exploit development, attack-path analysis or additional security scan. Root source approval and exact physical producer hashes remain required.

## Runtime evidence

External evidence root: `/var/tmp/codex/ModSecurity-conector/runs/i12-lighttpd-412-completion-20261015`. Actual sealed nonroot attempt `isolation/attempt-1792320135321593996` completed with controller0. All three cases returned400, had zero main native calls and unchanged nonzero physical event offsets, used before/after HTTP200 healthy controls plus separate real403 sink controls, and exited their actual hosts0 with cleanup. The native log FD device/inode matched the directly measured log file; UIDs were65534. Official lighttpd1.4.85 `request.c`, `log.c` and `configfile.c` and the independent RFC9112 bytes are bound in the source proposals. RFC9112 SHA256: `e4f426bac6206b67fdf9e0da826154f70588db2133a0a86b15cde4ff725d8937`.

`diagnostic/proposals-pre-native-01` retains normalized receipts and their direct producer references. Actual shared native-window, lighttpd Core-window and producer-binding helper validation passed for all three. These are worker proposals: no Root approval, full-case PASS or full-lifecycle PASS was created by this worker. The captures retain their actual `2463b5d8` source identity and `6895649c` product-module identity; they do not claim a later P3 fix build.

## Known limitations

Only three original diagnostic lighttpd CL contracts are added. `duplicate_transfer_encoding`, other profiles, mapping errors, startup-only failures and body-streaming claims remain outside this scope. Source/request approval, final shared qualification and current product P3 retakes remain coordinator work.

## Remaining risks

The new synthetic tests establish validator behavior; the separate physical captures establish host observations. Neither substitutes for independent Root review. Missing or conflicting evidence remains unqualified.

## Checks not run and rationale

No Git delivery or CI/Sonar result is claimed. Integrated documentation checks and final diff review belong to the coordinator. No dependency installation was performed.

## Final diff and review status

Worker implementation, focused regressions and physical helper checks are complete. Root owns review, source approval, commit, push and integration. No original diagnostic ledger status was changed.
