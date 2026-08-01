# Change Record: Parent Envoy transaction-opener interface naming

**Language:** English | [Deutsch](CR-20260801-sonar-envoy-transaction-opener.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-envoy-transaction-opener` |
| Date (UTC) | 2026-08-01 |
| Base revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | Current Envoy SonarQube Cloud row `godre:S8196` `AZ9cRyqvHhV2CayPTP0H` at `connectors/envoy/ext_proc/internal/processor/processor.go:128`. |
| Boundary | Parent Envoy ext_proc internal Go API and this paired Change Record/index documentation only. Framework, MRTS, gitlinks, C sources, protocol configuration, dependencies, and workflows remain unchanged. |

## Motivation and problem statement

The current Envoy SonarQube Cloud inventory contains one maintainability row.
It flags `Engine`, a one-method internal interface whose sole operation opens a
transaction, because its name does not use Go's standard `-er` convention.

## Acceptance criteria

- The tracked `godre:S8196` row has a source-native correction without a
  suppression, `NOSONAR`, rule exclusion, Quality Gate change, or false-
  positive disposition.
- The interface's method signature and all callers retain their existing
  transaction-opening behavior.
- Focused Go formatting, compilation, and static checks pass with the pinned
  module toolchain.
- A Draft PR obtains fresh exact-head GitHub and SonarQube Cloud evidence
  before any merge decision.

## Implementation decision and rationale

`processor.Engine` is renamed to `processor.TransactionOpener`. The new name
describes the existing `Open(context.Context, StreamMetadata)` operation,
satisfies the Go one-method-interface convention, and retains the exact method
set. The five internal typed use sites and the extension-process main package
are updated together, so neither the `CommonRuntimeEngine` implementation nor
the `PassthroughEngine` test seam needs an adapter or behavior change.

## Changed files

- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`
- `reports/audits/change-records/README.md`, `README.de.md`, and this
  English/German Change Record pair.

## Commands executed

| Command or procedure | Result |
| --- | --- |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go test -mod=readonly ./...` in `connectors/envoy/ext_proc` with task-owned Go caches | passed: the main package compiled and the processor package passed. |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go vet -mod=readonly ./...` in `connectors/envoy/ext_proc` with the same task-owned Go caches | passed. |
| `gofmt -d` for the two changed Go files | passed with no output. |
| Scoped search for the retired `processor.Engine` type | passed: no remaining Envoy ext_proc use; all six expected `TransactionOpener` declarations and use sites are present. |

## Security impact

This is a compile-time internal type-name correction. It preserves the method
set, CGo bridge implementation, transaction lifecycle, Envoy gRPC stream
handling, request metadata, response-commit boundary, configuration, and all
network-facing behavior. It adds no parser, file, process, authentication,
TLS, logging, dependency, scanner, or CI control change.

## Runtime evidence

No runtime claim is made. The package-wide Go test compiles both the service
and extension-process main package and exercises the existing processor
lifecycle tests; it is focused source/behavior evidence, not a replacement for
a native Envoy runtime matrix.

## Known limitations

No native Envoy process, full CRS/MRTS matrix, HTTP/1.1, HTTP/2, or HTTP/3
runtime probe was run. Those dimensions are not affected by this internal Go
identifier rename, and no transport-compatibility claim is made.

## Checks not run and rationale

The C17 connector build is not applicable because no C source, CGo bridge, or
compiler configuration changed. Native Envoy runtime checks require a pinned
Envoy binary and component inputs, and are not necessary to establish the
unchanged Go method set. Hosted GitHub Actions, review state, and SonarQube
Cloud analysis require the exact remote Draft-PR head and remain pending. The
repository-wide bilingual checker is blocked only by 20 pre-existing links to
the unpopulated Framework gitlink; it did not report a pair or structure error
for this Change Record.

## Remaining risks

The external SonarQube Cloud row is closed only after the exact Draft-PR head
is analysed with no task-owned new issue or new-code duplication. The local
package checks do not substitute for hosted analysis.

## Final diff and review status

The candidate is Parent-only and contains no Framework/MRTS/Gitlink,
dependency, workflow, scanner-configuration, suppression, or `master` change.
Focused source validation passed. Final diff/security review, commit, push,
Draft PR, and exact-head hosted verification remain pending at record
authoring.
