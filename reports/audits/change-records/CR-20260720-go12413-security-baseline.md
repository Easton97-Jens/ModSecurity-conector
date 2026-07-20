# Change Record: Go 1.24.13 security baseline

**Language:** English | [Deutsch](CR-20260720-go12413-security-baseline.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260720-go12413-security-baseline` |
| Date (UTC) | `2026-07-20` |
| Base revision | `f2376bb3e39ffbe9d36faca8bcd7397477eadd10` |
| Boundary | Parent Go module declarations, Parent CodeQL workflow, Parent generator/tests/docs, and this Change Record pair only; Framework, MRTS, and both gitlinks remain unchanged. |
| Finding linkage | Exact-master OSV run `29780297716`, job `88479684583`; `FND-PARENT-0001` and `FND-GITHUB-0001`. |

## Motivation and problem statement

The exact-master OSV advisory workflow reported 33 fixable Go standard-library
occurrences from the two Parent module declarations at `go 1.24.0`. Eighteen
of those occurrences have published fixes at or below Go `1.24.13`. The
remaining fifteen require Go `1.25.8` or later, and Dependabot alert #1's safe
`golang.org/x/net v0.55.0` likewise requires Go `1.25`; those are deliberately
outside this narrow patch.

## Acceptance criteria

- Both Parent Go modules declare the patched minimum `go 1.24.13`.
- Both CodeQL Go jobs select `go-version: '1.24.13'`.
- Generated EN/DE compiler guides, CI-security documentation, and focused
  tests describe the same baseline.
- The locked module graph and both `go.sum` files remain unchanged.
- Each module passes `go mod verify`, `go mod tidy -diff`, `go test`, and
  `go vet` with Go `1.24.13`; the CodeQL-equivalent builds are checked as far
  as the isolated worktree permits.
- The change does not claim to resolve the Go-1.25-only OSV rows, Dependabot
  #1, the 83 historical Gitleaks candidates, or any Framework/MRTS work.

## Implementation decision and rationale

The smallest complete Parent change raises only the two `go` directives and
the two CodeQL `actions/setup-go` inputs. It changes the generator source,
regenerates its English/German compiler-guide outputs, and updates the focused
tests that protect the exact pins. It intentionally adds no `toolchain`
directive, runs no `go get`, and makes no dependency, `go.sum`, `x/net`, or
Traefik host-source change.

The security invariant is that supported Parent Go-1.24 builds and the
corresponding CodeQL jobs do not select an unpatched Go `1.24.0` standard
library baseline. Existing module APIs, imports, selected dependency versions,
and legitimate Go build/test behavior remain unchanged.

## Security impact

This is a supply-chain/toolchain-baseline remediation, not a claim that each
underlying standard-library advisory is reachable from a connector request.
The pre-change scanner signal flows from each module's `go 1.24.0` declaration
to OSV's Go-standard-library evaluation; CodeQL separately selected the same
old toolchain. Raising both declaration and CI selectors closes the
Go-1.24-patch-line portion without hiding scanner output. A direct
`go list -buildvcs=false -deps` check still found no
`golang.org/x/net/html` import in the Envoy module, which is counterevidence
for the specific Dependabot parser path but is not an alert dismissal.

## Changed files

- `.github/workflows/ci-security-codeql.yml`
- `connectors/envoy/ext_proc/go.mod`
- `connectors/traefik/native_middleware/go.mod`
- `scripts/generate_compiler_guides.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_compiler_guides.py`
- `docs/build/compilers/envoy.md` and `docs/build/compilers/envoy.de.md`
- `docs/build/compilers/traefik.md` and `docs/build/compilers/traefik.de.md`
- `docs/security/ci-security-tooling.md` and
  `docs/security/ci-security-tooling.de.md`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| `rtk make check-ci-security-contract` | passed: 13 focused workflow/security-contract tests, including both exact CodeQL Go pins. |
| `rtk make check-compiler-guides` | passed: 19 generator, EN/DE parity, link, shell-syntax, and current-output tests. |
| Go `1.24.13` with `go mod verify` and `go mod tidy -diff` in each actual module | passed: both module graphs verify and neither tidy check emits a diff. |
| Go `1.24.13` with `go test -mod=readonly ./...` and `go vet ./...` in each actual module | passed: Envoy processor tests and Traefik middleware tests pass; vet reports no diagnostics. |
| Go `1.24.13` with `go build -mod=readonly ./...` | passed for Traefik. Envoy's unflagged local build is blocked by isolated-worktree VCS stamping; `go build -buildvcs=false -mod=readonly ./...` passed as the documented local equivalent. |
| `go mod graph` for Envoy | passed: the graph still selects `golang.org/x/net@v0.48.0`, `golang.org/x/sys@v0.39.0`, and `golang.org/x/text@v0.32.0`; only the root `go@1.24.13` line changed. |
| `go list -buildvcs=false -deps` exact check for `golang.org/x/net/html` | passed with no matching import path. |
| `rtk git diff --no-ext-diff --exit-code -- connectors/envoy/ext_proc/go.sum connectors/traefik/native_middleware/go.sum` and `rtk git diff --no-ext-diff --check` | passed: no checksum or whitespace drift. |

## Runtime evidence

Not applicable. The change is a minimum-toolchain and CI-selector update; it
does not alter a connector protocol path, host configuration, HTTP behavior,
CRS, MRTS, or native runtime. The module unit/build results above establish
only the stated Go-module behavior.

## Checks not run and rationale

- A new exact PR-head CodeQL run, OSV comparison, Gitleaks pull-request range,
  Scorecard, and SonarQube Cloud result do not yet exist; they are required for
  the eventual exact PR head and are not inferred from local checks.
- `rtk make check-bilingual-docs` ran but is blocked by the isolated
  worktree's uninitialized Framework gitlink: it returned `2` only for existing
  missing Framework link targets, not for either changed EN/DE pair.
- Native Envoy and Traefik host builds/runtimes require libmodsecurity and
  prepared host prerequisites not present in this isolated Parent worktree.
- No Go `1.25` migration, `golang.org/x/net` update, Dependabot closure, or
  individual historical Gitleaks triage was attempted because each requires a
  separate decision or safe occurrence evidence.

## Known limitations

The OSV result retains fifteen Go-1.25-only occurrences after this narrow
patch. A future coordinated Go-1.25 baseline decision must update the module,
CI, documentation, and dependency graph together, then rerun all exact-head
and resulting-master controls. The full bilingual checker cannot complete in
this worktree until its foreign Framework content is initialized without
altering it.

## Remaining risks

Dependabot alert #1 remains open because the compatible safe `x/net` version
requires Go `1.25`. The 83 Gitleaks historical signals remain untriaged
candidates because the advisory workflow provides no payload-safe,
occurrence-level manifest. Neither risk is accepted, dismissed, or hidden by
this change.

## Final diff and review status

Focused local validation, generated-document review, dependency-drift review,
and whitespace review passed. This record is written before staging, commit,
push, pull-request creation, or external check/review evidence; no delivery or
alert closure is claimed.
