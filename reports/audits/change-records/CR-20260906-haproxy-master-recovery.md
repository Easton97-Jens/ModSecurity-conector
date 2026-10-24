# Change Record: HAProxy master recovery for Common-adoption and SPOP bounds

**Language:** English | [Deutsch](CR-20260906-haproxy-master-recovery.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260906-haproxy-master-recovery |
| Date (UTC) | 2026-09-06 |
| Base revision | 9925ef647b5fb49d21aebd658a658d4fdb649c58 |
| Delivery status | Local implementation and validation on an isolated branch based on the stated revision. A normal push and separate Draft PR are authorized only after a fresh delivery preflight. No merge, direct `master` push, force push, rebase, or branch deletion is authorized. |

## Motivation and problem statement

Five resulting-master Actions jobs (`quick-framework-check`, `lint`,
`test-apache`, `test-nginx`, and `test-common`) all stopped at the same stale
HAProxy Common-adoption assertion. The old checker required both a Host-derived
hostname and the obsolete `out->request.hostname = src->server_ip` fallback.
The current mapper instead rejects missing or duplicate Host before owned-header
allocation, rejects empty Host after the lookup with cleanup, maps `server_ip`
only to `request.server.address`, and derives `hostname` from the validated Host
header.

The exact master SonarQube Cloud analysis
`1878d424-279f-4452-8b32-b7d9c05e724a` for the stated base also reported
`AaBwK2W4SQwNCdYHcQVm` / `c:S3519` at the direct SPOP NOTIFY argument-count
byte access. This is a confirmed analyzer and delivery blocker, not a
reproduced runtime out-of-bounds defect: bounded frame reception and
`read_string_ref()` already reject the reported truncated message-name shape.

PR #346 head `5432cf5607ac0f105579651bb24eca9f57b99e1d` is read-only reference
only. Its relevant sequence is `139030d2`, `1c32bbac`, and `5432cf56`; no PR
#346 branch, file, Gitlink, or delivery state is changed here.

## Acceptance criteria

- The global checker proves the active request mapper validates exactly one
  Host before owned-header allocation, rejects empty Host with cleanup, derives
  `hostname` from Host, keeps `server_ip` only as server address, and evaluates
  both Common request-validation returns correctly.
- Comment-only and foreign-function decoys cannot satisfy the active Host,
  request/response Common-validation, or engine config-merge/validate
  assertions; removed or ignored Host rejection, a reintroduced hostname
  fallback, and inverted return handling are rejected by focused mutation tests.
- `read_byte()` rejects null input/cursor/output pointers, end-of-input,
  cursor-outside-length, and `SIZE_MAX` cursor values before a byte access;
  failed reads preserve the caller cursor and output value.
- `parse_notify_message_header()` keeps raw one-byte count semantics, rejects
  a missing count byte, accepts a complete zero-count parser control, and does
  not convert parser acceptance into request authorization.
- Empty input, truncated message name, complete name without count, valid
  zero-count control, malformed-then-legitimate sequence, cleanup, C17,
  ASan/UBSan, and the repository runtime self-test have current local evidence.
- No workflow, governance, Quality-Gate, suppression, exclusion, source-lock,
  Gitlink, Framework, MRTS, PR #346, or unrelated connector source change is
  included.

## Implementation decision and rationale

The checker now masks comments and extracts the concrete request mapper,
response mapper, header validator, and engine-creation function bodies before
checking their ordered fail-closed forms. This binds the Host admission guard,
the request and response validation/cleanup returns, and the Common
config-merge/validate guard to their active functions. It is deliberately a
narrow function-boundary contract, rather than a broad rewrite of the global
checker or an attempt to restore a prohibited `server_ip` hostname fallback.

The SPOP transfer is the smallest dependency-complete subset of the three
referenced PR #346 commits: `read_byte()` owns its local cursor; it validates
pointer inputs, uses `cursor > len || len - cursor < sizeof(*value)` before
access, reads one raw byte, and advances the caller cursor only after success.
`parse_notify_message_header()` performs its own pointer/cursor validation,
parses the message name, reads the raw count through that helper, and preserves
the existing valid-message and response-role rules. No wider PR #346 runtime,
worker, cache, socket, or lifecycle change is transferred.

## Changed files

- `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `tests/test_haproxy_common_adoption.py`
- `tests/test_haproxy_header_validation_contract.py`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/CR-20260906-haproxy-master-recovery.md`
- `reports/audits/change-records/CR-20260906-haproxy-master-recovery.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Check | Actual result |
| --- | --- |
| Pre-patch direct checker and `make check-haproxy-common-adoption` | Reproduced the stale Host/`server_ip` fallback assertion on the stated base. |
| Pre-patch `make lint` and `make quick-check` with isolated output roots | Both reached and failed at that same stale HAProxy assertion. |
| Focused checker mutation, mapper/header, native Host, and Sonar contract tests | Passed: 37 tests; negative controls cover removed or ignored pre-allocation Host rejection, empty-Host cleanup removal, `server_ip` hostname fallback, inverted request/response Common returns, and inverted config merge despite comment and foreign-function decoys. |
| `make check-haproxy-common-adoption` | Passed. |
| `make check-haproxy-c17` | Passed. |
| `tests.test_sonar_reliability_contract` with `-fsanitize=address,undefined` | Passed: 15 tests; its HAProxy C harness covers empty/truncated/missing-count/zero-count, cursor boundary, pointer, and cleanup controls. |
| `make -C connectors/haproxy self-test-spoa-runtime` | Passed: the repository SPOP protocol self-test completed. |
| `make -C connectors/haproxy self-test-spoa` | Failed before SPOP parser execution: the pre-existing starter target omits `common/src/block_statuses.c` and cannot link `msconnector_block_status_is_allowed`; no Makefile change is in scope. |
| Valgrind on the built runtime self-test | Passed with zero errors, zero definite/indirect/possible leaks, and no parent-process retained allocations. |
| Direct `clang --analyze` of the changed SPOP translation unit | Passed with no diagnostic output. |
| `make check-analysis-tools` and `make check-clang-analysis-tools` | Passed. |
| Post-patch `make lint` and `make quick-check` | Both passed the repaired global checker and HAProxy C17, then stopped at four pre-existing HTX-overlay assertions outside this scope. |

## Security impact

The mapper source-to-sink path is received HAProxy headers →
`haproxy_validate_source_headers()` → owned Common headers → Host lookup →
Common mapper validation → transaction admission. The repaired checker now
binds its assertions to that active path: missing, empty, and duplicate Host
remain fail-closed; a mapped allocation is cleaned on the empty-Host failure;
and endpoint metadata cannot silently substitute for authority.

The SPOP source-to-sink path is peer frame → `recv_frame()` →
`handle_connection()` → `handle_notify_frame()` → `parse_notify_payload()` →
`parse_notify_message_header()` → typed argument parsers → endpoint admission
and transaction owner handling. The change preserves frame limits, exact
payload consumption, duplicate-argument rejection, bounded header/body paths,
and fail-closed missing endpoint behavior. A parser-valid zero-count message
still encounters the later Host and endpoint admission controls; it is not an
authorization grant.

## Runtime evidence

The direct compiled HAProxy harness executes the parser controls under
AddressSanitizer and UndefinedBehaviorSanitizer. The repository's built
SPOP runtime self-test also passed under Valgrind. This is bounded local
protocol evidence only; it is not a complete HAProxy host-runtime, P1–P4, or
17×10 matrix acceptance claim.

## Known limitations

The checker is a deliberately narrow source contract, not a full C parser or
proof of arbitrary macro/control-flow reachability. The Sonar signal was not
independently reproduced as a runtime overflow; the source-native bounds proof
and regressions address the analyzer-reported byte-access shape without making
that unsupported claim. The bounded comment and foreign-function decoy cases
are covered; this does not claim arbitrary C semantic equivalence.

## Remaining risks

The five other exact-master Sonar issues are independent and unchanged:
`AaBjSjUps3vKd0hpl5pP` is Apache checker duplication; three NGINX shell issues
are independent; and `AaA34UWlbqrRc02noCI3` belongs to the Framework Gitlink
path. There is no additional current HAProxy issue in the six-issue inventory.
The post-patch aggregate chains reveal four HTX-overlay contract failures;
they are a separate HAProxy follow-up and are not hidden or repaired by this
change.

## Checks not run and rationale

`tests/test_haproxy_transaction_contract_binding.py` could not be collected
because the isolated Python environment has no `pytest` module; no dependency
was installed merely to change that result. The repository-wide
`clang-analyzer-baseline` was blocked because no HAProxy compilation database
was available. The starter `self-test-spoa` target has an independent existing
link omission and therefore stops before parser execution. No repository-native
HAProxy ThreadSanitizer target exists. No full native HAProxy runtime, complete
P1–P4 acceptance, or 17×10 matrix is claimed.

## Final diff and review status

The final allowlist is limited to the nine paths listed above. The first
independent review reproduced three checker-integrity false negatives, which
were then closed with bounded copied-source controls; a fresh independent
read-only recheck found no additional validated bypass or parser regression.
The generated analyzer plist was removed and is not part of the diff. A final
exact-delivery preflight remains required before delivery. This record
intentionally does not claim a commit SHA, pushed head, Draft PR number, hosted
checks, Sonar result, Ready state, or merge; those facts must be observed
independently after delivery.
