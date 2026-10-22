# Change Record: NGINX empty terminal request buffer

**Language:** English | [Deutsch](CR-20261022-nginx-empty-terminal-request-buffer.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261022-nginx-empty-terminal-request-buffer` |
| Date (UTC) | `2026-10-22` |
| Base revision | `c03352ba160675a94bf63125cceaa25367f52c27` |
| Pull request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation and problem statement

NGINX represents a valid empty request body with a zeroed `ngx_buf_t` whose
`last_buf` flag is set. The request-body adapter rejected its NULL `pos` and
`last` members as an invalid data range before calling
`msc_process_request_body`. The host therefore returned technical HTTP 500
instead of performing native Phase 2. The former compiled `empty` fixture used
an absent chain and did not exercise this real host buffer shape.

A separate Common mapper fixture also described a nonzero body with NULL data
as `oversized`, although the mapper has no connector-owned body-size policy.
That input is the existing `missing body data` P1 technical error and must not
be reclassified as a P2 result.

## Acceptance criteria

- A real empty terminal control buffer reaches native request-body finalization
  once without a zero-byte append.
- Data followed by a terminal control buffer is appended once and finalized
  once; nonterminal flush and sync controls do not hide following data.
- NULL chain buffers, malformed non-special memory ranges and a nonempty NULL
  append remain technical HTTP 500 paths before native body processing.
- A nonzero Common body with NULL data remains a P1 `missing body data` mapper
  failure; unsupported-body policy still takes precedence.
- Focused C fixtures compile with warnings as errors, documentation remains
  equivalent in English and German, and the integrated I12 host campaign
  supplies the separate real-host/client/native/cleanup evidence.

## Implementation decision and rationale

The adapter now recognizes `ngx_buf_special` after validating the `ngx_buf_t`
pointer. A terminal special buffer ends chain traversal; flush and sync controls
advance to later buffers. All non-special buffers retain the existing pointer
and range validation, so a data-bearing or in-file buffer cannot use a control
flag to bypass validation. EOS remains the later
`msc_process_request_body` invocation.

The regression fixture uses the pinned NGINX flag layout and macro semantics.
It adds the actual empty terminal shape, data/control ordering, flush/sync
controls and negative memory ranges. The stale `oversized` alias is removed;
the explicit NULL-data and unsupported-policy cases retain the actual Common
mapper contract.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `tests/test_nginx_request_native_results.py`
- `tests/fixtures/nginx_common_input_validation.c`
- `tests/test_nginx_common_input_validation.py`
- `connectors/nginx/README.md` and `connectors/nginx/README.de.md`
- this English/German Change Record pair

## Commands executed

All commands were RTK-wrapped. Raw local evidence is retained under
`/var/tmp/codex/ModSecurity-conector/runs/pr416-nginx-complete-20261022`.

| Check | Observed result |
| --- | --- |
| Pre-fix `tests.test_nginx_request_native_results` against base source | Exit 1: 14 tests, six failures. The actual empty terminal, control-buffer ordering and native-finalization assertions fail while invalid ranges remain rejected. `baseline/request-native/pre-fix.log`, SHA-256 `4d33322e77a693dc604ed6a62f3383d7e6c053e6f4760d63b4b646cc0ae97597`. |
| Post-fix `python3 -m unittest -v tests.test_nginx_request_native_results tests.test_nginx_common_input_validation` | Exit 0: 18 tests pass, including actual terminal empty, exactly-once finalization, memory/file paths, flush/sync, invalid ranges and Common P1 NULL-data classification. |
| Clean-base replay of the previously observed Common/cleanup failures | Reproduces the same stale `body too large` expectation and cleanup-fixture compile gap on unmodified `c03352ba...`; `baseline/c033-clean/baseline-failures.log`, SHA-256 `a0a02676ce7c4dfa3e093cb8d67b78a2c06aac0b99cdad8da73541cc3b1c4f45`. This change corrects the Common expectation and carries the controlled cleanup-fixture intervention seam; both now pass the focused #382 validation. |
| Final NGINX product regression sets | Exit 0: two disjoint final runs pass 165 and 82 tests, respectively (247 total), covering Common adoption, exact event writers, request mapping, P1/P2/P3/P4 results, body buffers, native EOS/error paths, mutation guards and once-only close cleanup. |
| Final `make build-nginx` | Exit 0 against pinned NGINX 1.31.6 and the prepared libModSecurity runtime cache; the build stage recompiles the connector from the final product source under `product-382/runtime-final`. No host claim is inferred from this build result. |
| `make check-nginx-c-standard-wiring`; repository-path, bilingual-document and Change Record checks | Exit 0. The Change Record check is structural and is not presented as evidence validation. |
| `git diff --check`; `python3 ci/tools/new-change-record.py check` | Exit 0; archive check reports structural PASS only. |

Integrated Root/Nobody host and exact-revision #410/#416 results remain owned by
the downstream I12 campaign; no unexecuted check is claimed here.

## Security impact

The change accepts only NGINX special control buffers, which by definition are
neither in memory nor in a file. Non-special NULL/reversed ranges still fail
closed before native processing. This prevents valid empty requests from being
misreported as technical failures without weakening malformed-buffer handling,
native return validation, terminal event ownership or cleanup. The work remains
within the user-approved TAC1 focused-review boundary.

## Runtime evidence

This product-stage record contains compiled adapter evidence, not a live-host
claim. The pinned NGINX source independently establishes the empty terminal
buffer shape and `ngx_buf_special` semantics. Root-master/Nobody-worker host,
client bytes, physical events, native EOS and follow-up cleanup are produced
and revision-bound by the downstream #416 I12 campaign after normal integration
through #410.

## Known limitations

The product fixture does not itself start NGINX or libModSecurity. It proves the
adapter branch and native call boundary with compiled controlled dependencies.
Historical I12 results remain bound to their original revisions and are not
promoted to this change.

## Remaining risks

The integrated host run must still prove both empty framing variants, exact
native EOS, Finish/Free, client-visible status/framing and healthy neighboring
requests. Any failure there blocks NGINX acceptance rather than being inferred
from this unit regression.

## Checks not run and rationale

Exact-head #410/#416 host, report, Sonar and GitHub checks are not run at this
product-stage checkpoint because the product fix has not yet been committed and
integrated. Deployment and master merge are outside the authorized task.

## Final diff and review status

The current product diff is limited to NGINX source, NGINX/Common fixtures,
paired NGINX documentation and this record. An independent source review found
no blocking correctness or security issue and requested the now-covered sync
control case. Final commit, remote SHA and complete validation are recorded only
after normal delivery. This record does not authorize merge.
