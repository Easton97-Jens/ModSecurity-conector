# Change Record: lighttpd stock-sidecar endpoint metadata

**Language:** English | [Deutsch](CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260916-lighttpd-stock-sidecar-endpoint-metadata |
| Date (UTC) | 2026-09-16 |
| Base revision | `e475baabf0787cbc804f176ae998b62156892825` |
| User authorization | “erstelle ein eigenen worktree und ein pr dann” |
| Delivery status | One task-owned Parent worktree and Draft PR are authorized. No merge, auto-merge, direct `master` write, Framework/MRTS/Gitlink change, or branch deletion is authorized. |

## Motivation and problem statement

The retained general-state run `20260913T142629Z-e475baa` reported 14/33
lighttpd stock-sidecar loopback failures and a failed first real-host allow
case. On the current base, the unchanged focused allow control returned `502`
where `200` was expected. `sidecar_exchange_request` constructed
`msconnector_request` without `request.client` or `request.server`, while
Common `validate_request_input` requires bounded nonempty endpoint addresses.

## Acceptance criteria

- A valid accepted loopback TCP request passes actual client/server endpoint
  metadata to Common and can reach the normal allow path.
- A phase-1 block still returns `451`, does not release the upstream, and its
  event reports `client_ip` `127.0.0.1`.
- Invalid endpoint lookup, address conversion, family, or zero-port data fails
  closed before transaction begin and upstream contact.
- The socket-free `runtime_begin_smoke` has valid explicit test metadata.
- C17/Werror builds succeed with `cc` and `clang`.

## Implementation decision and security impact

`sidecar_capture_request_endpoints` obtains both endpoints exclusively with
`getpeername()` and `getsockname()` from the accepted client socket. It rejects
syscall errors, unexpected sockaddr sizes/families, conversion errors, and
zero ports. Converted values live in `sidecar_exchange_state` through
transaction cleanup, avoiding borrowed stack pointers. No `Host` header or
fabricated production fallback is used.

The listener remains literal IPv4 loopback-only. A failed capture cannot start
a Common transaction or contact the upstream; the existing connector error
path fails closed. `runtime_begin_smoke` is not socket-backed, so its explicit
loopback values are confined to synthetic test input.

## Changed files

- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/lighttpd/stock_sidecar/runtime_begin_smoke.c`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.md`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or check | Result | Observed result |
| --- | --- | --- |
| Stock-sidecar C17/Werror build with `CC=cc` | passed | Build completed using the external task root and verified ModSecurity library copy. |
| Stock-sidecar C17/Werror build with `CC=clang` | passed | Independent Clang build completed. |
| Focused allow, endpoint-metadata, and runtime-identity tests | passed | 3 named tests passed in the final task worktree. |
| Complete `connectors/lighttpd/tests/test_stock_sidecar_contract.py` module | failed | 33 of 34 tests passed; the immediate client-reset event case remained empty. |
| `git diff --check` before delivery setup | passed | No whitespace errors in the product diff. |

## Runtime evidence

The focused TCP sidecar tests exercised a real accepted loopback connection.
The new phase-1 block test observes `client_ip` `127.0.0.1`, status `451`, and
no upstream release. The original focused allow changed from the reproduced
`502` failure to `200` after the repair.

## Checks not run and rationale

No real stock-lighttpd backend, full connector matrix, hosted PR check,
SonarQube Cloud analysis, review readback, or resulting-master workflow can be
claimed yet. The repository-wide `make check-bilingual-docs` invocation was
interrupted after 80 seconds without a result, so it is not recorded as passed.
The immediate-reset test is left intact because changing it without a proven
synchronization contract could mask a delivery-lifecycle defect.

## Known limitations and follow-up

The complete module has one failing immediate-reset test with no event record
after the client reset. The real stock-lighttpd backend and full matrix were
not rerun. `FND-PARENT-1091` is locally `fixed`, not `verified`; its release
and candidate-integration blocker status remains until the complete contract,
real backend, and original reproduction/control evidence pass at the exact PR
head.

## Final diff and delivery status

This record is part of the task-owned branch. It records only local evidence
available before the Draft PR. After the push, local HEAD, remote branch SHA,
and PR head SHA must be compared exactly. Required GitHub checks, SonarQube,
review/conversation status, and any later merge are pending and are not
asserted by this record.
