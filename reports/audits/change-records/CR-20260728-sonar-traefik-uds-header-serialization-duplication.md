# Change Record: Traefik UDS header-serialization deduplication for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260728-sonar-traefik-uds-header-serialization-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-traefik-uds-header-serialization-duplication |
| Date (UTC) | 2026-07-28 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Boundary | Parent Traefik native-middleware UDS header serializers and focused source tests, plus this English/German Change Record pair and indexes only. Framework, MRTS, both gitlinks, workflow, scanner policy, and generated reports remain unchanged. |
| Finding linkage | Parent SonarQube Cloud duplicate-lines-density remediation. This source refactor does not itself close an individual external issue before an exact-head analysis. |

## Motivation and problem statement

The request- and response-header UDS payload builders each contained the same
header-count plus ordered name/value serialization. Keeping those copies
separate increased the Parent duplicate-code measure and made a future change
to one protocol path easier to miss in the other.

The values are security-relevant at this boundary: HTTP request or upstream
response headers become bytes sent to the private local-engine Unix socket.
The remediation therefore shares only the byte-identical serialization core.
It must not broaden validation, alter the frame format, or move caller-owned
lifecycle and precondition logic.

## Acceptance criteria

- A private helper appends exactly the existing uint16 header count and ordered
  validated name/value pairs for both builders.
- `buildUDSBegin` retains its early header-count check, metadata encoding,
  default HTTP version, and final payload-size check.
- `buildUDSResponseHeaders` retains its status/count checks, default HTTP
  version, and final payload-size check.
- Direct tests prove byte-exact request and response layout with the
  `HTTP/1.1` fallback and fail-closed rejection in both builders for excess
  headers, empty/NUL/oversized fields, and an oversized aggregate payload.
- Isolated Go 1.26.5 tests, race check, bounded fuzzing, module test, vet,
  build, formatting, whitespace, and focused security review pass.
- No hosted alert closure, Ready-for-review transition, merge, master update,
  Framework/MRTS change, or scanner-policy change is claimed.

## Implementation decision and rationale

`appendUDSHeaderPairs` owns only the sequence already common to both callers:

1. append `uint16(len(headers))`;
2. for each input header in order, append the required bounded name;
3. append the optional bounded value.

It delegates all field checks to the unchanged `appendUDSText`. It does not
validate a header-count policy itself, choose an opcode, allocate a frame,
choose a default version, serialize request metadata or response status, write
to the socket, or mutate transaction state. The two callers keep their
existing early checks and post-serialization payload limit, preserving their
established error ordering and fail-closed behavior.

## Changed files

- `connectors/traefik/native_middleware/engine_uds.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| Official task-local Go 1.26.5 provenance, SHA-256, archive-layout, and exact-version verification | passed; the official Linux AMD64 archive matched SHA-256 `5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053`. |
| `go mod verify` with the isolated, no-network, read-only-module toolchain | passed. |
| Focused `TestUDS` and `-race` `TestUDS` | passed. |
| `FuzzUDSFrameAndResult`, 15 seconds, one worker | passed; 93,578 executions and no new interesting input. |
| `go test -mod=readonly ./...`, `go vet ./...`, and `go build -mod=readonly ./...` | passed. |
| `gofmt -d engine_uds.go engine_uds_test.go` and `git diff --check` | passed; no output. |
| Independent focused post-diff security review | passed; no plausible regression or reportable finding. |
| Repository bilingual-documentation, repository-path, and link checks | passed after read-only initialization of the Parent-pinned Framework commit; the Framework remained clean and unchanged. |

## Security impact

The refactor preserves the existing defense-in-depth controls before any UDS
write: caller-owned count limits, required non-empty names, per-field byte
limits, uint16 representability, NUL rejection, final builder payload limits,
and the independent checks in `exchangeLocked` and `writeUDSFrame`. Request
metadata, response status/version handling, opcode choice, socket deadlines,
session state, and lifecycle behavior are outside the shared helper and are
unchanged.

The focused review found no evidence that a malformed header can reach the
socket through the new helper. The direct tests assert the valid byte layout
and both-builder failure behavior; existing lifecycle tests continue to cover
the one-session UDS opcode order.

## Runtime evidence

The new direct serializer tests are source-level byte-contract evidence. The
same focused Go suite also runs the existing local Unix-socket lifecycle tests,
but it does not start Traefik, load a plugin, invoke Common/libmodsecurity or
CGo, or establish a native host-runtime capability.

## Known limitations

The helper intentionally relies on its two private prevalidated callers for
the `udsMaxHeaders` policy. Its current call graph is limited to those callers;
a future caller must retain that explicit count validation before passing a
slice to the helper.

## Remaining risks

The change does not prove the behavior of an external UDS peer or of a full
Traefik/Common deployment.

## Checks not run and rationale

- Exact-PR-head hosted checks and SonarQube Cloud analysis require the normal
  task-owned Draft PR delivery cycle and remain pending at this record stage.
- Full Traefik host/plugin and private-engine runtime testing needs separate
  native prerequisites and is not represented as local source-test evidence.

## Final diff and review status

This record is written before staging, commit, push, pull-request creation,
and external analysis for this candidate. The local source validation and
focused security review passed. No duplicate-code reduction is claimed until a
fresh exact-head SonarQube Cloud analysis observes it.
