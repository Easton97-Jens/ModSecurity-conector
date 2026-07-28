# Change Record: Parent common error duplicate-mapping refactor

**Language:** English | [Deutsch](CR-20260727-sonar-common-error-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-common-error-duplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent local SonarQube Cloud duplication-reduction candidate for `common/src/error.c`; no Sonar issue key is asserted closed. |
| Boundary | Parent Common error-description implementation, its C helper smoke contract, the focused static contract, and this English/German Change Record pair plus indexes. Public headers, public API/ABI, connector behavior, Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and problem statement

`common/src/error.c` contained two parallel `switch` mappings for each known
`msconnector_error_code`: one for its name and one for its default message.
The candidate removes that duplicated mapping data without treating an enum
value as an array index or changing error classification, event conversion, or
fallback behavior.

## Acceptance criteria

- Keep every current known error-code name and default message byte-for-byte equivalent.
- Replace only the duplicated name/default-message mappings with a translation-unit-private, keyed lookup; do not use `msconnector_error_descriptions[code]` or another enum-indexed access.
- Preserve the public headers, enum values, exported function signatures, and ABI.
- Preserve the known and unknown error contracts, including `MSCONNECTOR_ERROR_NONE`, caller-provided messages, and fail-safe unknown-code fallbacks.
- Maintain focused C17 helper coverage with GCC and Clang, focused/static contracts, and a complete English/German Change Record pair with indexes.
- Do not claim a SonarQube Cloud reduction or closed issue until a fresh analysis evaluates the exact delivered candidate head.

## Implementation decision and rationale

`common/src/error.c` now holds a `static const`
`msconnector_error_descriptions[]` table keyed by its explicit
`msconnector_error_code` field. The translation-unit-private helper
`msconnector_error_description_for_code` performs a bounds-limited linear
search and returns `NULL` on a miss. `msconnector_error_code_name` and
`msconnector_error_default_message` each consume that result and retain their
existing fixed fallbacks.

The approach keeps error-code values decoupled from table positions: negative,
out-of-range, and future unmapped values cannot select memory through an enum
index. It intentionally leaves `msconnector_error_status`,
`msconnector_error_http_status`, `msconnector_error_is_fatal`,
`msconnector_error_set`, and `msconnector_error_to_event` behavior unchanged.

For every current known code, the helper smoke contract covers the name,
default message, status, HTTP status, fatal flag, generated event ID/event
level, event message, and decision reason. It separately covers
`MSCONNECTOR_ERROR_NONE`, a caller-provided message, null error/event inputs,
and three unknown values: `-1`, the next value after
`MSCONNECTOR_ERROR_INTERNAL`, and `INT_MAX`.

## Changed files

- common/src/error.c
- ci/checks/common/check-common-helpers.sh
- tests/test_sonar_reliability_contract.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

The received implementation handoff reports the following commands, using a
task-owned external build directory where `BUILD_ROOT` is shown:

- `env BUILD_ROOT=<task-owned external build directory> CC=gcc make check-common-helpers-c17`
- `env BUILD_ROOT=<task-owned external build directory> CC=clang make check-common-helpers-c17`
- `env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_sonar_reliability_contract`
- `make check-common-security-contract`
- `make check-common-sdk-contract`
- `make check-common-flow-integrity`
- `make check-common-memory-safety`
- `git diff --check`
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_bilingual_docs`
- `rtk proxy make check-bilingual-docs`
- `rtk proxy make check-doc-links`
- `rtk proxy git diff --check`

## Tests and actual results

| Command or check | Result |
| --- | --- |
| C17 Common helper smoke with GCC | passed according to the received implementation handoff. |
| C17 Common helper smoke with Clang | passed according to the received implementation handoff. |
| `tests.test_sonar_reliability_contract` | passed according to the received implementation handoff; it asserts that the description table is private, keyed, and not accessed as `msconnector_error_descriptions[code]`. |
| `make check-common-security-contract` | passed according to the received implementation handoff. |
| `make check-common-sdk-contract` | passed according to the received implementation handoff. |
| `make check-common-flow-integrity` | passed according to the received implementation handoff. |
| `make check-common-memory-safety` | passed according to the received implementation handoff. |
| Source-candidate `git diff --check` | passed according to the received implementation handoff. |
| `tests.test_bilingual_docs` | passed: 14 tests in 0.035s after this Change Record pair and indexes were added. |
| `make check-bilingual-docs` | passed after the Parent-pinned Framework Gitlink was initialized read-only in this isolated candidate worktree. |
| `make check-doc-links` | passed after the Parent-pinned Framework Gitlink was initialized read-only in this isolated candidate worktree. |
| Documentation-inclusive `git diff --check` | passed after this Change Record pair and indexes were added. |

## Security impact

The change touches a public Common error-code boundary: an unexpected value
must not become an out-of-bounds lookup or weaken the existing fail-safe error
path. The keyed linear search uses an actual static-table bound, returns only
static-lifetime strings, and has no public symbol or header change. On a miss,
the pre-existing safe behavior remains: name `"internal"`, default message
`"Internal connector error"`, status `MSCONNECTOR_STATUS_ERROR`, HTTP status
`500`, nonfatal classification, and an `MSCONN_EVENT_INTERNAL_ERROR` event at
level `"error"` when converted.

The received independent security review is `PASS`: it found no validated new
security regression in the candidate. This is not a claim that an unrelated
security finding or the whole SonarQube Cloud inventory is fixed.

## Runtime evidence

The received C17 helper checks exercise the Common error contract with GCC and
Clang. They are narrow component-level smoke evidence, not connector-host,
protocol-matrix, or production-runtime evidence. No Framework or MRTS runtime
was run or changed.

## Known limitations

The description table and the helper-smoke expectation table are manually
maintained. A future public enum addition must be added to both. If it is
omitted, the implementation degrades safely to the existing internal-error/500
fallback, but the new enum's intended semantic mapping would be incomplete.

At this record's creation, the candidate remains local and uncommitted. A
fresh exact-head SonarQube Cloud analysis is still required to measure the
actual duplicate-lines result and any remaining findings.

## Remaining risks

An accidentally omitted current mapping could change a name or default message;
the expanded C helper contract reduces that risk across all 16 current codes.
The local static source-contract test cannot by itself prove hosted analysis,
all compiler/toolchain combinations, or downstream connector behavior.

No conclusion about the reported project-wide `0.4%` duplication density,
unrelated SonarQube Cloud rows, or a delivered PR follows until the exact
candidate head has completed fresh hosted checks and analysis.

## Checks not run and rationale

- No fresh exact-candidate-head SonarQube Cloud analysis, GitHub CI result, commit, push, pull request, review, or merge exists at this local/uncommitted candidate stage; therefore no external issue disposition or duplication reduction is claimed.
- The Parent-pinned Framework Gitlink was initialized read-only at `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` solely to run `make check-bilingual-docs` and `make check-doc-links`; both passed. No Framework or MRTS source, branch, or Gitlink changed.
- Full connector builds, connector-host smokes, protocol matrices, and production runtime tests were not run for this focused Common mapping refactor; they are outside its narrow validation scope.
- Framework and MRTS checks were not run because no Framework, MRTS, or Gitlink content changed.

## Final diff and review status

The local task-worktree candidate consists of the keyed Parent Common
description mapping, the expanded Common helper smoke contract, the focused
static contract, and this required bilingual traceability material. Public
headers, API/ABI, status/HTTP/fatal classification, event conversion, and all
known/unknown fallback semantics remain within the stated preservation
boundary.

The candidate is not a delivered change. Its final source and documentation
diff still require exact-head delivery validation, including a fresh SonarQube
Cloud analysis, before it can be represented as reducing duplicate density or
resolving any external issue.
