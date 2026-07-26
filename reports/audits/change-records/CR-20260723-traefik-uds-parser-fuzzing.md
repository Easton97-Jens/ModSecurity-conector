# Change Record: Traefik UDS parser fuzzing

**Language:** English | [Deutsch](CR-20260723-traefik-uds-parser-fuzzing.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-traefik-uds-parser-fuzzing |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Boundary | Parent Traefik native middleware UDS parser, its CodeQL job, focused workflow contract, reader documentation, and this Change Record pair/index only. Framework, MRTS, and both gitlinks remain unchanged. |
| Finding linkage | Scorecard FuzzingID #11; FND-PARENT-0001. |

## Motivation and problem statement

The fresh Scorecard inventory reported no repository-recognized fuzz target for
the custom Traefik UDS frame and result parser. That parser handles bytes from
the middleware's private Unix-domain-socket engine connection and must reject
truncated or malformed protocol data without a panic. The selected host
configures the peer as a same-UID private service; this does not remove the need
for bounded parser regression evidence.

## Acceptance criteria

- A Go-native FuzzUDSFrameAndResult target exercises the bounded UDS frame
  reader and result parser from deterministic malformed and valid seeds plus
  arbitrary bounded input.
- The target does not open a socket, start the engine, invoke CGo/Common, alter
  the protocol, or claim host-runtime behavior.
- The existing traefik-go CodeQL job runs it for 15 seconds with one worker.
- Local formatter, Go test, vet, build, module-integrity, bounded fuzz, and
  focused workflow-contract checks pass with task-local Go 1.26.5.
- English/German reader documentation and this Change Record pair describe the
  same boundary and limitations.
- No hosted-alert closure, merge, direct master push, Framework change, or MRTS
  change is claimed.

## Implementation decision and rationale

The fuzz target calls readUDSFrame over an in-memory bytes.Reader and limits
supplied input to one maximum protocol frame plus its header. Successful reads
are written back with writeUDSFrame and compared to the exact consumed bytes,
deliberately permitting a subsequent frame in the same stream. Result payloads
are parsed only for the result opcode; accepted actions must remain in the
parser's recognized range.

The deterministic corpus includes empty and truncated data, a normal begin
frame, two concatenated frames, and allow/deny/redirect result payloads. This
covers framing and action branches without creating a socket, launching the
private engine service, or relying on host-specific Traefik loading. The
focused CI-security contract asserts the target name and time/worker bounds so
the workflow integration cannot silently disappear.

## Changed files

- connectors/traefik/native_middleware/engine_uds_fuzz_test.go
- .github/workflows/ci-security-codeql.yml
- tests/test_ci_security_workflows.py
- connectors/traefik/native_middleware/README.md and README.de.md
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| Task-local official Go 1.26.5 provenance/hash verification | passed; retained archive SHA-256 matched 5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053. |
| gofmt -d for the new fuzz target | passed; no formatter output. |
| Module Go test and vet | passed. |
| Bounded Go fuzz target, 15 seconds, one worker | passed; 105,190 executions and no crash. |
| go mod verify and go mod tidy -diff | passed. |
| Go build with buildvcs disabled in the isolated worktree | passed. |
| make -C connectors/traefik test-native-middleware with task-local Go and registered output | passed. |
| Focused CI-security contract | passed; 16 tests plus actionlint, zizmor, and gitleaks validate-only checks. |
| Repository bilingual-documentation check | blocked_environment only by 20 pre-existing missing Framework-gitlink link targets in this isolated worktree; it reported no error in the changed English/German pairs. |
| Independent scoped security diff review | passed; no reportable new security finding. It independently confirmed the parser allocation bound, action validation, stream invariant, and untrusted-PR workflow controls. |

## Security impact

This adds regression coverage at the UDS protocol parser boundary and makes
that coverage visible to the repository security workflow. It controls parser
panics and invalid action acceptance; it does not prove the absence of all
parser defects, socket-level attacks, engine defects, host behavior, or a
hosted FuzzingID refresh.

The target is deliberately resource bounded. It rejects inputs larger than one
protocol maximum frame before allocation, preserves stream semantics by checking
only the consumed frame, and treats parser errors as expected fuzz outcomes.

## Runtime evidence

The local fuzz target is only in-memory source-level evidence. It does not open
a Unix socket, start Traefik or the persistent Common/libmodsecurity engine,
load a plugin in a host, or invoke CGo. The native-middleware source test target
passed, but no full-lifecycle host capability is promoted.

## Known limitations

The committed control intentionally runs for 15 seconds with one worker to
bound CodeQL time and resource use. It has no long-running corpus, sanitizer,
socket-peer fault-injection, or Common/libmodsecurity integration coverage.
Transient Go fuzz discoveries remain in the task-local cache; only reviewed
deterministic seeds are versioned.

## Remaining risks

Scorecard must rescan the resulting default-branch revision before it can
recognize the target and refresh FuzzingID. The separate Scorecard governance
causes (BranchProtectionID, CodeReviewID, MaintainedID, and
CIIBestPracticesID) remain external to this Parent-source change. No external
governance setting, reviewer evidence, OpenSSF registration, or alert dismissal
is attempted.

## Checks not run and rationale

- Exact-PR-head CodeQL, Scorecard refresh, Dependabot refresh, OSV, Gitleaks
  range, SonarQube Cloud, and GitHub review evidence require a pushed Draft PR
  or default-branch scan.
- Full Traefik/Common/libmodsecurity runtime smoke needs explicit native host
  and engine prerequisites; it is not required to exercise this focused parser
  boundary.
- Longer fuzz campaigns, sanitizers, and socket-peer fault injection are future
  hardening options, not evidence for this bounded control.

## Final diff and review status

This record is written before staging, commit, push, pull-request creation, and
external check/review evidence. Local validation and independent scoped security
review are complete and found no reportable new finding. Final delivery evidence
remains pending; no alert closure is claimed.
