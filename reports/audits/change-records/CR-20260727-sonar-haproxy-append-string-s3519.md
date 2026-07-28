# Change Record: Parent HAProxy append-string preflight for SonarQube Cloud c:S3519

**Language:** English | [Deutsch](CR-20260727-sonar-haproxy-append-string-s3519.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-haproxy-append-string-s3519 |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud BLOCKER `c:S3519` receipt `AZ-URJYx1ap3oKwyiaQ7` at `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` in `append_string(...)`. |
| Boundary | Parent HAProxy diagnostic-runtime source, its focused Parent reliability-contract test, and this English/German Change Record pair with its indexes. Framework, MRTS, Gitlinks, workflows, scanner configuration, Quality Gates, suppressions, and the external SonarQube Cloud issue state remain unchanged. |
| Candidate status | Local and uncommitted. No staging, commit, push, pull request, merge, Framework or MRTS change, or Gitlink change has occurred. |

## Motivation and problem statement

The former `append_string(...)` implementation wrote a variable-length header
and then called `append_bytes(buf, value, len, len)`. The call describes the
source extent only as the value being copied, which is the direct pattern
reported by `c:S3519`. The candidate removes that call from the string path
and does not change the existing, separately bounded frame-payload copy.

Before `append_string(...)` mutates its direct target, it now validates the
buffer pointer and length, validates a NUL-terminated C string within
`SPOP_FRAME_MAX`, calculates the variable-length-header size, and proves that
the header plus payload fit in the remaining buffer. It subsequently appends
the header and string bytes directly. The preflight makes direct
`append_string(...)` rejection atomic for NULL, unterminated, and
capacity-overflow inputs.

The boundary cases are intentionally exact: a 239-byte string has a one-byte
header containing `239` and produces a 240-byte encoded result; a 240-byte
string has the two-byte header `240`, `0` and produces a 242-byte result. An
exact fit up to `SPOP_FRAME_MAX` succeeds, while an insufficient combined
header-and-payload capacity returns `-1` without changing the buffer.

`append_typed_string(...)` writes its pre-existing type marker before calling
`append_string(...)`; its marker behavior and any wrapper-level partial state
remain explicitly outside this focused change.

## Acceptance criteria

- `append_string(...)` no longer contains `append_bytes(buf, value, len, len)`.
- Direct `append_string(...)` validates C-string, buffer, and combined
  header/payload capacity before its first mutation.
- The 239/240 variable-length encodings, exact-fit success, overflow failure,
  unterminated-input failure, and NULL failure have focused regression
  coverage.
- The record does not claim wrapper-level atomicity for
  `append_typed_string(...)`, live HAProxy behavior, a hosted Quality Gate, or
  an external issue closure.

## Implementation decision and rationale

Add `varint_encoded_length(...)` so that the header length is calculated using
the same thresholds as `append_varint(...)`: one byte below `240`, then the
existing continuation-byte progression. `append_string(...)` uses that length
only for its preflight. After successful validation, the pre-existing
`append_varint(...)` and `append_byte(...)` primitives serialize the same
header and payload without presenting an artificial `data_len == len` source
extent to `append_bytes(...)`.

This deliberately keeps `append_bytes(...)` for the frame-payload call where
the actual source capacity is `sizeof(payload->data)`, rather than widening
the remediation beyond the Sonar receipt.

## Changed files

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — direct
  `append_string(...)` preflight and bounded byte append, plus
  `varint_encoded_length(...)`.
- `tests/test_sonar_reliability_contract.py` — source-contract assertions and
  the persistent native C harness for direct `append_string(...)` boundary
  behavior.
- `reports/audits/change-records/CR-20260727-sonar-haproxy-append-string-s3519.md`
  and `.de.md` — this bilingual Change Record pair.
- `reports/audits/change-records/README.md` and `README.de.md` — paired index
  entries.

## Commands executed

| Executed control or recorded validation | Observed result |
| --- | --- |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | passed: 8 focused tests, including the persistent native C harness that compiles and runs direct `append_string(...)` boundary cases. |
| `rtk proxy make check-haproxy-common-adoption` | passed. |
| `rtk proxy make check-haproxy-c-standard-wiring` | passed. |
| `rtk proxy make check-haproxy-c17-lint` | passed. |
| `rtk proxy env BUILD_ROOT=<task-owned external build root> CC=gcc make check-haproxy-c17` | passed; the temporary GCC build output was removed after validation. |
| `rtk proxy env BUILD_ROOT=<task-owned external build root> CC=clang make check-haproxy-c17` | passed; the temporary Clang build output was removed after validation. |
| Independent security review of the focused source/test diff | passed: no new reportable security finding; the direct `append_string(...)` preflight invariant and the explicitly excluded `append_typed_string(...)` marker behavior were reviewed. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make check-bilingual-docs` | passed after the Parent-pinned Framework Gitlink was initialized read-only in this isolated candidate worktree. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make check-doc-links` | passed after the Parent-pinned Framework Gitlink was initialized read-only in this isolated candidate worktree. |
| `rtk proxy git diff --check` | passed. |

## Security impact

The Sonar BLOCKER concerns a native buffer-copy boundary. The correction
preserves a fail-closed direct API: NULL buffer or C-string inputs, an
unterminated C string, an invalid buffer length, and insufficient combined
header-and-payload capacity return `-1` before `append_string(...)` modifies
the target buffer. The focused native harness proves the documented direct
cases, including overflow non-mutation. It does not alter authentication,
authorization, configuration trust, or connector process privileges.

The review does not make a claim about `append_typed_string(...)` failure
atomicity: that wrapper's existing marker is intentionally outside scope.

## Runtime evidence

The focused test module contains a persistent native C harness which compiles
and runs the actual diagnostic-runtime translation unit. It checks every
varint length through `SPOP_FRAME_MAX`, the exact 239/240 encodings, exact-fit
success, overflow non-mutation, unterminated input non-mutation, and a NULL
direct buffer. This is bounded native execution evidence for
`append_string(...)`; it is not a live HAProxy/SPOP network-runtime result.

## Known limitations

- The receipt is attached to the stated base revision. A fresh exact-head
  SonarQube Cloud analysis is required before claiming that
  `AZ-URJYx1ap3oKwyiaQ7` is resolved externally.
- No live HAProxy runtime or full connector matrix was run for this candidate.
- `append_typed_string(...)` marker behavior remains pre-existing and outside
  the direct `append_string(...)` atomicity claim.
- Documentation link validation required the Parent-pinned Framework; it was
  initialized read-only at `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` only
  to run the Parent documentation checks. No Framework/MRTS source, branch,
  or Gitlink changed.

## Remaining risks

The focused contract, native harness, and independent GCC/Clang C17 compiles
reduce the risk of a header-length or capacity-preflight regression, but they
do not exercise a live HAProxy process or all SPOP message construction paths.
Hosted CI and a fresh exact-head
SonarQube Cloud analysis can still reveal issues not covered by the local
candidate. The external issue remains open until such an analysis observes a
delivered head.

## Checks not run and rationale

No live HAProxy runtime, full connector matrix, hosted GitHub CI, hosted
SonarQube Cloud analysis, delivery action, Framework source/delivery action,
or MRTS action was run. The candidate is local and this documentation task is
confined to the Parent worktree. The Parent-pinned Framework Gitlink was
initialized read-only at `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` solely to
run `make check-bilingual-docs` and `make check-doc-links`; both passed.

## Final diff and review status

At record creation, the worktree contains the local, uncommitted HAProxy
source/test candidate and this bilingual documentation pair with its indexes.
No Git or delivery action is asserted. The existing focused source/test,
HAProxy adoption/wiring/C17-lint, and independent security-review evidence is
recorded above. The full bilingual-docs and link checks now pass after the
read-only Parent-pinned Framework initialization, while the whitespace-diff
check also passed. A fresh exact-head SonarQube Cloud analysis remains
mandatory before an external issue-resolution claim.
