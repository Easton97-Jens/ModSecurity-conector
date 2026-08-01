# Change Record: Parent Envoy maintainability remediation

**Language:** English | [Deutsch](CR-20260730-sonar-envoy-maintainability-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-envoy-maintainability-remediation` |
| Date (UTC) | 2026-07-30 |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | 16 current SonarQube Cloud maintainability rows below `connectors/envoy/`: `shelldre:S1192` ×2, `go:S3776` ×5, `c:S107` ×1, `godre:S8193` ×3, `godre:S8196` ×1, `go:S1186` ×1, and `godre:S8242` ×1. |
| Boundary | Parent Envoy ext_proc service, C bridge, test code, runtime harness, and this paired Change Record/index documentation only. |

## Motivation and problem statement

The current Envoy component reports sixteen maintainability issues. They are
repeated fixed harness literals, high-complexity lifecycle methods, a C bridge
body call with too many independent arguments, and small Go API/test-code
hygiene concerns. The public component display also includes one
`python:S5332` security row for the standard-library fixture server.

## Acceptance criteria

- The sixteen listed maintainability rows have focused source-level
  remediations without scanner suppression or Quality Gate changes.
- gRPC receive, cancellation, EOF, send-failure, response-commit, and host
  action semantics remain covered by the processor tests.
- The changed native bridge builds as C17 with `-Wall -Wextra -Werror` against
  the installed libmodsecurity headers and library.
- The existing fixed-loopback TLS and private-runtime-root security controls
  continue to pass their legitimate and negative transport contracts.
- The delivered PR receives fresh exact-head GitHub and SonarQube Cloud
  evidence before any merge decision.

## Implementation decision and rationale

The service now delegates stream receive/send lifecycle, headers, body limits,
and header decoding to purpose-specific helpers. This keeps each state
transition in one small unit while preserving the existing `streamState`
owner, timeout, close-reason, and response-commit boundaries. A failed send on
a cancelled stream still ends processing without writing host-action evidence.

The Common Runtime bridge receives a typed C body descriptor rather than four
separate body-direction arguments. The descriptor retains the same bounded
pointer, length, direction, and end-of-stream validation and is compiled as
C17. Common lifecycle test cases are named helpers, and the test gRPC stream
exposes its mandated `Context()` through a provider rather than storing a
`context.Context` field.

The two fixed shell literals have one readonly owner. The optional response
commit interface has a verb-aligned name, and the source-only transaction's
empty `Close` implementation records why it owns no resources.

The `python:S5332` row is revalidated but intentionally not changed. Its
`ThreadingHTTPServer` is a same-process upstream fixture bound at a fixed
`127.0.0.1` address; it is not the downstream client sink. The existing
downstream probes accept only credential-free `https://127.0.0.1`, use a
certificate-verifying TLS context, and enforce TLS 1.2 or later. The canonical
`FND-SONAR-0001` forbids an external false-positive disposition without a
current explicit user decision. No suppression or topology rewrite is used.

## Changed files

- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.h`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go`
- `connectors/envoy/ext_proc/internal/processor/config.go`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- `reports/audits/change-records/README.md`, its German companion, and this
  English/German Change Record pair.

## Commands executed

| Command | Result |
| --- | --- |
| `GOWORK=off go test -mod=readonly ./...` in `connectors/envoy/ext_proc` | passed. |
| `ENVOY_EXT_PROC_COMMON_TEST=1 sh connectors/envoy/build/build_ext_proc.sh` with task-owned caches/build root, `/usr/include`, and the installed libmodsecurity `.so` | passed; module verification, C17 compile, Go Common tests, and binary build passed. |
| Built binary `--config connectors/envoy/config/envoy-ext-proc-service.json --check-config` | passed. |
| `shellcheck -S error -x connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` | passed. |
| `python3 -m unittest tests.test_envoy_transport_hardening_contract` | passed: 16 tests. |
| `git diff --check` | passed before record creation; rerun before delivery. |

## Security impact

The refactor retains the established request isolation, context cancellation,
bounded header/body checks, native transaction lifetime, response-commit, and
loopback-TLS controls. No path acceptance, network exposure, TLS policy,
artifact-root confinement, event payload policy, scanner rule, suppression, or
Quality Gate configuration changes. A focused source/diff review found no
new source-to-sink security candidate.

## Runtime evidence

The native build used the real installed libmodsecurity headers and shared
library, compiled the bridge with strict C17 diagnostics, and executed the
libmodsecurity-tagged Common Runtime Go tests. The transport contract started
only temporary loopback test servers and verified normal TLS behavior together
with private-root and unsafe-endpoint negative controls.

## Known limitations

No complete Envoy binary/runtime matrix, production deployment, HTTP/2 or
HTTP/3 downstream exercise, or Framework/MRTS test was run. These are outside
this focused Parent Envoy maintenance change.

## Checks not run and rationale

The full connector matrix and real Envoy process smoke were not run because
the local environment does not provide the pinned Envoy binary. Hosted Actions,
review state, and SonarQube Cloud analysis are necessarily pending until this
Draft PR exists at an exact remote head. The first sandbox run of the Python
transport contract could not bind its intentional `127.0.0.1` test sockets;
the same unmodified test passed outside the sandbox.

## Remaining risks

The sixteen applicable source rows are only externally closed when current-head
SonarQube Cloud confirms their absence with zero new issues and zero new-code
duplication. The revalidated `python:S5332` fixture-server row remains open in
SonarQube Cloud pending a separately authorized external disposition; it is not
a source defect in this change.

## Final diff and review status

The candidate remains within the Parent Envoy boundary and contains no
Framework/MRTS/Gitlink, workflow, dependency, scanner-configuration,
suppression, or `master` modification. At record authoring, local validation
passed; delivery and exact-head hosted verification remain pending, and no
merge is claimed.
