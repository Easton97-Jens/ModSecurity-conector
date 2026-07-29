# Change Record: Parent Lighttpd runtime-output containment

**Language:** English | [Deutsch](CR-20260729-sonar-lighttpd-runtime-output-containment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-lighttpd-runtime-output-containment |
| Date (UTC) | 2026-07-29 |
| Base revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | Six current SonarQube Cloud `pythonsecurity:S8707` findings: fixture ready/result, first-byte metadata, and lifecycle projection/summary/results outputs. |
| Boundary | Parent Lighttpd harness source and tests, plus paired Change Record indexes. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

## Motivation and problem statement

The three helpers accepted command-line output paths and wrote them after only creating parents. The full-lifecycle shell runner accepted an absolute smoke directory but did not establish a private no-symlink write root before it created, removed, or forwarded artifacts. A caller could choose an unintended filesystem location or redirect a path with a symbolic link.

## Acceptance criteria

- Every generated fixture, first-byte, projection, summary, and lifecycle output is an absolute non-symlink path strictly below a verified private runtime-output root.
- The root is validated with the existing runtime-path policy before shell cleanup, creation, fixture start, or forwarding to downstream helpers.
- Generated files use private `O_NOFOLLOW|O_EXCL` temporary creation and atomic replacement; JSON/JSONL schemas remain unchanged.
- Legitimate nested temporary outputs succeed; escaped and symlink output paths are rejected before they can write an artifact.
- Exact-head hosted checks and SonarQube Cloud must prove zero New Issues and zero New-Code duplication before any merge consideration.

## Implementation decision and rationale

`safe_runtime_output.py` is a local Lighttpd harness adapter over the existing Parent runtime-path policy. It verifies a narrow private root, requires every output and parent to remain below it, and uses a non-following exclusive temporary file before `os.replace`. Each writer receives `--runtime-output-root`; the shell runner validates its smoke root and first-byte evidence path before its first write, then passes that same root to every affected helper. The adapter avoids changing the shared `ci/lib` contract while applying its established controls to Lighttpd-specific outputs.

## Changed files

- `connectors/lighttpd/harness/safe_runtime_output.py` — verified root, containment, and atomic no-follow writer.
- The three affected writer/fixture helpers and their shell caller.
- Focused event-validation and host-contract tests.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| Python bytecode compilation for the four changed harness modules | passed. |
| `sh -n connectors/lighttpd/harness/run_patched_full_lifecycle.sh` | passed. |
| Focused Lighttpd event-validation and host-contract tests | passed: 23 tests, including normal nested output, escaped-output rejection, symlink-escape rejection, and both fixture-control escape cases. |
| `make check-lighttpd-common-adoption` | passed. |
| Lighttpd host-integration and build-wiring checks | passed. |
| `git diff --check` | passed. |

## Security impact

The attacker-controlled source is the CLI/environment-derived output location. Former sinks were `mkdir` plus direct text/stream writes in three helpers and shell cleanup/create operations under the configured smoke root. The new invariant validates the root and each output before those sinks. Negative tests show that outside-root paths and symlink descendants are rejected before an artifact exists; positive tests show valid temporary nested outputs preserve bounded metadata. No request-body, rule, event, authorization, runtime-claim, or Quality Gate control is weakened.

## Runtime evidence

The focused tests execute the real writer CLIs and the same filesystem helpers used by the patched lifecycle runner. They do not require a built Lighttpd host. The shell contract proves the runner passes the verified root to every affected helper.

## Known limitations

- A complete patched-Lighttpd/libmodsecurity host runtime and connector matrix were not run because their version-pinned host build and fixtures are absent from this temporary task worktree.
- The complete Codex Security diff-scan capability is unavailable because its mandatory delegated-worker preflight is incomplete; no full scan report is claimed.
- Hosted checks and fresh exact-head SonarQube Cloud analysis remain pending.

## Remaining risks

- New Lighttpd harness writers must use this adapter and receive a verified root; bypassing it needs a new focused path-security review.

## Checks not run and rationale

No live patched-Lighttpd runtime, full connector matrix, or complete Codex Security diff scan ran. The required host build/fixtures are absent from this temporary worktree and the scanner's mandatory delegated-worker capability is unavailable. The CLI-level malicious and legitimate controls are the strongest available direct proof for these filesystem sinks.

## Final diff and review status

The candidate is confined to Parent Lighttpd harness security and bilingual traceability. It covers all six selected S8707 locations with one shared verified-root boundary. Local review and focused validation are complete; a separate Draft PR and exact-head hosted verification remain required before any delivery or merge claim.
