# Change Record: Parent Traefik complete SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-traefik-complete-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | \`CR-20260801-sonar-traefik-complete-remediation\` |
| Date (UTC) | 2026-08-01 |
| Base revision | \`c3319575ae86d9810da8b5428590336d60cd3daf\` |
| Tracking | \`FND-SONAR-0016\` — current \`connectors/traefik/\` inventory. |
| Boundary | Parent \`connectors/traefik/\` and direct Parent tests only. |

## Motivation and problem statement

The current Traefik directory inventory contains eight security findings and
two maintainability findings. The Python smoke runners process environment-
derived paths and executable names before creating runtime artefacts or starting
local processes. The native runner also concentrated setup, host execution,
observations, outcome validation and cleanup in one complex function. The Go
middleware exposed a single-method interface under a generic name.

## Implementation decision and rationale

The forwardAuth runner now carries a validated, immutable local executable
value through command construction. It rejects control characters before
process invocation, keeps generated runtime artefacts below fixed names in
validated directories, and never accepts a shell command string. The native
runtime root retains its owner and ancestor checks; shared temporary roots are
rejected through those real permission checks rather than through a brittle
literal deny-list.

The native lifecycle is separated into input collection, staging, private UDS
and loopback setup, request execution, live observations, outcome
finalization, result writing, and cleanup. This preserves the existing protocol
and non-promotion contract while keeping individual responsibilities within
maintainable complexity. The single-method Go interface is named
\`TransactionOpener\`, with \`Engine\` retained as a source-compatible alias.

No SonarQube Cloud rule, exclusion, suppression, \`NOSONAR\`, Quality Gate,
workflow, Framework, MRTS, Gitlink, or \`master\` state changes.

## Acceptance criteria

All ten retained issue keys have a concrete source disposition; malformed,
escaping, symlinked, cross-user-replaceable, or control-character command input
fails before a filesystem or process sink; legitimate private roots and regular
local executables remain valid; native host lifecycle output and safe cleanup
contracts remain intact; and the exact PR head must have zero new issues and
zero New-Code duplication without scanner-control changes.

## Changed files

The change is limited to Traefik Python smoke runners, native middleware Go
sources, their direct Parent Python tests, and this English/German Change
Record pair and indexes. No other repository boundary changes.

## Commands executed

| Command | Result |
| --- | --- |
| Selected Parent Python 3.14: \`python -m py_compile connectors/traefik/scripts/runtime_native_smoke.py connectors/traefik/scripts/runtime_smoke.py\` | passed. |
| Selected Parent Python 3.14: \`python -m unittest -v tests.test_traefik_runtime_smoke_security tests.test_traefik_native_local_plugin\` | passed: 26 tests. |
| Task-owned Go 1.26.5 cache: \`go test -mod=readonly ./...\` in \`connectors/traefik/native_middleware\` | passed. |
| \`gofmt -d\` on changed Go files | passed: no output. |
| \`git diff --check\` | passed before final review; rerun is required before delivery. |
| Full native host lifecycle and linked C17 engine build | not run: this isolated sandbox has no task-provisioned Traefik binary and libmodsecurity development-header/library inputs. It is not substituted by a global installation. |

## Security impact

The executable and artefact changes narrow existing path and process trust
boundaries: command arguments cannot contain control characters, fixed output
names stay below validated roots, and shared temporary directories remain
rejected based on actual ownership and permissions. Regression controls cover
legitimate private roots and executables plus symlink, public-root,
cross-user-replacement and control-character negatives. The lifecycle
refactoring retains socket identity checks, process cleanup, loopback-only
binding, host outcome causality and capability non-promotion. It does not claim
hosted security analysis or a full native runtime result.

## Remaining risks and verification state

The source and focused controls are complete locally. Full native host runtime
evidence is unavailable for the stated prerequisite reason. The requested Draft
PR still needs exact-head hosted Actions, CodeQL and SonarQube Cloud
verification; no PR creation, review, merge, or master change is claimed by
this record.

## Runtime evidence

The focused source controls demonstrate the executable, artefact, root, socket,
and lifecycle-helper contracts, but do not claim a full native host runtime.

## Known limitations

The isolated task environment lacks task-provisioned Traefik and libmodsecurity
inputs required for the complete native host lifecycle and linked C17 build.

## Checks not run and rationale

The complete native host lifecycle and linked C17 engine build require a
task-provisioned Traefik binary plus libmodsecurity development headers and
library, which are unavailable in the isolated task environment. Hosted
exact-head verification remains pending until the Draft PR exists.

## Final diff and review status

The final security-sensitive diff review and delivery status are recorded only
after their respective commands complete. This record intentionally makes no
claim about a commit, push, PR number, hosted check, SonarQube Cloud analysis,
or \`master\` integration.
