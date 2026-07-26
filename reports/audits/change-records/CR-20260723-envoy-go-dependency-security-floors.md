# Change Record: Envoy Go dependency security floors

**Language:** English | [Deutsch](CR-20260723-envoy-go-dependency-security-floors.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260723-envoy-go-dependency-security-floors` |
| Date (UTC) | `2026-07-23` |
| Base revision | `a308d7b414f0859490fe7253e0683a4bde80b563` |
| Boundary | Parent Envoy `ext_proc` module, its Parent test and reader documentation, and this Change Record pair/index only; Framework, MRTS, and both gitlinks remain unchanged. |
| Finding linkage | Dependabot alerts #1/#2; Scorecard `VulnerabilitiesID` #12; `FND-GITHUB-0001` and `FND-PARENT-0001`. |

## Motivation and problem statement

Current master selected gRPC `v1.79.3`, x/net `v0.48.0`, x/sys `v0.39.0`, and
x/text `v0.32.0` in the Envoy `ext_proc` module. Fresh Dependabot, OSV, and
govulncheck evidence identified open gRPC/x/net alerts and additional
Scorecard dependency rows. The existing Go 1.26.5 module baseline supports the
published fixed module versions.

## Acceptance criteria

- The Envoy `ext_proc` module selects gRPC `>=v1.82.1`, x/net `>=v0.56.0`,
  x/sys `>=v0.46.0`, and x/text `>=v0.39.0` without changing its Go baseline.
- Resolver-required indirect upgrades and `go.sum` changes are tidy and verify.
- A focused static contract prevents a downgrade below each floor while
  permitting later stable security versions.
- English/German reader documentation and this Change Record pair describe the
  same floors and limitations.
- Go module tests, vet, build, and current vulnerability scanning pass with the
  task-local Go 1.26.5 toolchain.
- No alert closure, merge, direct `master` push, Framework change, MRTS change,
  or PyYAML suppression is claimed.

## Implementation decision and rationale

The fix updates the single affected Parent module through Go's resolver. It
pins the two Dependabot fixes and the minimum versions that remove the current
x/sys and x/text Scorecard findings. x/net `v0.56.0` requires x/sys `v0.46.0`,
so the resolver-selected x/sys version is intentionally higher than the
advisory's minimum fixed version. The resulting xDS, protoc-gen-validate, and
genproto increments are resolver-required closure, not unrelated upgrades.

The regression test parses stable `go.mod` requirements and compares numeric
semantic-version tuples. It fails closed for a missing, malformed, or
pre-release target requirement, while allowing future stable patch/minor
security upgrades.

## Changed files

- `connectors/envoy/ext_proc/go.mod` and `go.sum`
- `tests/test_ci_security_workflows.py`
- `connectors/envoy/ext_proc/README.md` and `README.de.md`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| Official Go 1.26.5 release-index/hash verification in the registered private task run | passed; archive SHA-256 matched `5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053`. |
| Baseline `go mod graph`, `go mod verify`, test, vet, and build with isolated Go 1.26.5 | passed before remediation; current selections were below the required floors. |
| `go get google.golang.org/grpc@v1.82.1 golang.org/x/net@v0.56.0 golang.org/x/sys@v0.46.0 golang.org/x/text@v0.39.0` | passed; the first `x/sys@v0.44.0` candidate was rejected because x/net `v0.56.0` requires `v0.46.0`. |
| Candidate `go mod tidy`, `go mod tidy -diff`, and `go mod verify` | passed. |
| Candidate `go test -mod=readonly ./...` and `go vet ./...` | passed. |
| Candidate `go build -buildvcs=false -mod=readonly ./...` | passed; the unflagged isolated-worktree build is recorded below. |
| Candidate `govulncheck -show verbose ./...` with the task-local Go first in `PATH` | passed: no vulnerabilities found. |
| Focused dependency-floor contract | passed; 17 unit tests and the actionlint, zizmor, and gitleaks validate-only controls passed. |
| Repository bilingual-documentation check | blocked_environment only by 20 pre-existing missing Framework-gitlink link targets in this isolated worktree; no diagnostic named a changed English/German pair. |

## Security impact

This is a supply-chain dependency remediation for the Parent's network-serving
gRPC `ext_proc` module. It removes the current module/package results reported
by govulncheck and selects Dependabot's published fixed gRPC version plus the
complete x/net floor. The current scan did not find a directly called vulnerable
symbol before the update; that reachability counterevidence is not an alert
dismissal and does not weaken the version remediation.

The two historical PyYAML IDs in the aggregate Scorecard message remain
already safe under declared `PyYAML>=6,<7` and the exact CI `6.0.3` lock. No
unnecessary Python change or suppression is included.

## Runtime evidence

The update changes no connector protocol, configuration, or application source
path. Parent Go unit, vet, build, module-integrity, and vulnerability-scanner
controls establish module compatibility only. The optional Common/libmodsecurity
bridge tests remain skipped because explicit native include/library paths were
not supplied.

## Known limitations

The isolated worktree does not materialize the Parent-relative Framework rules
fixture used by the runtime-config portion of `make test-envoy-ext-proc`; that
portion is `blocked_environment`. The direct Envoy module tests passed, and the
unchanged Parent baseline completed the config segment. This does not replace a
future real Envoy/Common runtime-smoke run with its explicit prerequisites.

## Remaining risks

Dependabot and Scorecard remain open until their hosted scans refresh on the
resulting default-branch revision. This change does not resolve Scorecard's
separate BranchProtectionID, CodeReviewID, MaintainedID, CIIBestPracticesID, or
FuzzingID root causes. No external governance setting, reviewer evidence,
OpenSSF registration, or alert dismissal is attempted.

## Checks not run and rationale

- Exact-PR-head CodeQL, OSV, Scorecard, Dependabot refresh, Gitleaks range,
  SonarQube Cloud, and GitHub review evidence do not exist before the Draft PR
  and cannot be inferred locally.
- The unflagged `go build -mod=readonly ./...` in this isolated worktree is
  blocked by VCS stamping; `-buildvcs=false` is the documented local equivalent
  and passed.
- Full native Envoy/Common runtime smoke requires explicit libmodsecurity,
  Envoy, and prepared host prerequisites not selected for this dependency-only
  change.

## Final diff and review status

The record is written before staging, commit, push, pull-request creation, and
external check/review evidence. Local validation is complete. An independent
scoped security review found no reportable new security finding; it recorded a
future optional guard against repository-controlled Go replace/workspace
resolution as not applicable in the reviewed state. Final delivery evidence
remains pending; no alert closure is claimed.
