# Change Record: GitHub workflow host-runtime consolidation

**Language:** English | [Deutsch](CR-20260821-github-workflow-hostruntime-consolidation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260821-github-workflow-hostruntime-consolidation |
| Date (UTC) | 2026-08-21 |
| Base revision | `aaeb7c550d8943a584d21f0f5ca5a11cc3706cbf` |
| Delivery status | A Parent-only task branch, one task-owned commit, and one pull request to `master` are authorized. Commit, push, PR creation, hosted checks, and merge evidence are pending at record preparation time; merge is not authorized. |

## Motivation and problem statement

Four connector workflows duplicated the same host-runtime preflight invocation,
sanitized evidence projection, and summary rendering. This made security
controls harder to maintain consistently. Separately, the `Update pinned
workflow tools` run on `master` reproducibly failed because its bounded
candidate tree omitted static transitive inputs required by the existing
CI-security contract.

## Acceptance criteria

- Retain all 29 repository workflow files, workflow names, triggers, jobs,
  permissions, action SHAs, connector profiles, artifacts, and independent
  security scanners.
- Centralize only the four equivalent evidence-collection implementations.
- Preserve fail-closed evidence semantics and prevent shell/path injection.
- Repair the updater's bounded candidate-tree validation without widening its
  source allowlist or bypassing its contract.
- Provide focused tests, YAML/actionlint/ShellCheck/zizmor validation, a
  security-diff review, paired English/German traceability, and one unmerged
  PR after final delivery preflight.

## Implementation decision and rationale

- Added `ci/runtime/common/collect_hostruntime_preflight_evidence.py` and
  changed Envoy, HAProxy, NGINX, and Traefik only to call it with their original
  connector/profile/configuration/fixture values. NGINX retains its Markdown
  code formatting; all four workflows retain their exact artifact paths and
  `if: always()` uploads.
- The collector validates simple components and repository-relative paths,
  invokes the existing preflight through an argument vector, and publishes
  only bounded, allowlisted fields. Malformed status, nonzero `PASS`, absent
  lock data, and binary failures become `BLOCKED`; runtime status remains
  `NOT_RUN`.
- The updater's proposed-tree baseline now includes only exact static inputs
  discovered during the failed contract reproduction. A regression test runs
  the real copied-tree CI-security contract. Workflow pin assertions resolve
  immutable SHAs from the reviewed lock and normalize only those pin/comment
  fragments before digesting the publisher, leaving action identity and all
  other publisher content covered.

## Security impact

The change touches GitHub Actions execution, CI evidence, and updater
provenance. It retains immutable action pins, least-privilege permissions,
read-only checkout credentials, artifact contracts, and restrictive updater
allowlists. The shared collector adds no shell execution or external download;
its output is fail-closed and payload-safe. A later focused review reproduced
the same-user artifact-symlink boundary failure recorded below and the
successor fixes it before delivery.

The initial diff review did not report this boundary failure. A later focused
review reproduced a same-user `RUNNER_TEMP` symlink overwrite in the
collector's fallback path. The successor validates the private artifact root
and uses the existing descriptor-based, no-follow atomic readers/writers for
every collector output; two regressions reject preseeded root and final-status
symlinks without changing their sentinel target.

## Changed files

- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-haproxy.yml`
- `.github/workflows/test-nginx.yml`
- `.github/workflows/test-traefik.yml`
- `ci/runtime/common/collect_hostruntime_preflight_evidence.py`
- `ci/tools/update-workflow-tools.py`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_collect_hostruntime_preflight_evidence.py`
- `tests/test_hostruntime_workflow_evidence_contract.py`
- this paired Change Record and paired archive indexes

## Commands executed

| Check | Actual result |
| --- | --- |
| Collector and workflow-evidence contracts | passed: 6 tests |
| `tests.test_ci_security_workflows` | passed: 28 tests |
| `tests.ci_security.test_update_workflow_tools` | passed: 35 tests, including real copied-tree validation |
| `make check-ci-security-contract` | passed: 122 tests; 5 capability-dependent skips; locked actionlint/zizmor/gitleaks validation passed |
| APR provenance/static contracts | exit 0: 7 static passes; 15 skips because the external Framework checkout HEAD differs from the Parent gitlink |
| Parse all workflow YAML | passed: 29 files |
| actionlint with ShellCheck | passed |
| offline strict-collection zizmor | passed: no unsuppressed findings; 94 existing suppressions honored |
| Direct safe collector execution | passed: produced sanitized `BLOCKED`/`NOT_RUN` evidence for missing local runtime prerequisites |
| `git diff --check` before traceability | passed |
| Full `make lint` | blocked/fails in the Framework-dependent No-CRS group because the task worktree has an empty Framework Gitlink and lacks its catalog; 27 preceding hostruntime tests passed |
| `make check-bilingual-docs` | blocked only by pre-existing missing Framework-Gitlink targets; no new Change Record error remains |
| `make check-doc-links` | blocked only by the same missing Framework-Gitlink targets before it can inspect Framework documentation links |

| Collector symlink-boundary and runtime-artifact contracts | passed: 44 tests; root and final-status symlink targets remained unchanged |

## Runtime evidence

The reproducible `Update pinned workflow tools` failure was recreated in its
candidate-only tree, where required contract inputs were absent. After the
closure repair, the same real copied-tree contract passes without modifying the
source checkout. The host-runtime helper was executed only against safe local
missing-runtime conditions; it does not claim a connector runtime result.

The complete security-diff report is retained outside the source tree at
`/var/tmp/codex/ModSecurity-conector/runs/workflow-consolidation-20260821/security-diff-scan/report.md`.

## Checks not run and rationale

`make setup-dev` was not run because it bootstraps the separate Framework
repository, which the user did not select as writable. No live maintenance
workflow dispatch, token mint, artifact cleanup, root broker, runtime matrix,
or GitHub Actions rerun was performed before delivery. Those actions are not
needed to prove the local consolidation and would expand the task boundary.

## Known limitations

The task worktree's Framework Gitlink is uninitialized. Therefore full
`make lint` cannot run its Framework-dependent No-CRS tests even though its
workflow-specific, security-contract, and static checks pass. Hosted checks
on the eventual exact PR head remain necessary to validate GitHub execution.

## Remaining risks

The shared collector now requires a private non-symlink artifact root rather
than treating the runner-provided temporary directory as sufficient confinement
proof. Future workflow changes must continue to preserve per-connector wrapper
behavior and must add input mappings explicitly. The updater repair's closure
is necessarily
bounded to the current `check-ci-security-contract` static inputs; future
contract dependencies require the same constrained review.

## Final diff and review status

Local final review is ready for delivery: only proven duplicated collection
logic was centralized; the workflow count remains 29 before and after; no
workflow was removed; no security scanner or required wrapper was consolidated.
The source diff, final bilingual/documentation checks, Git preflight, commit,
PR, exact-head hosted checks, and non-merge delivery status must be read back
before this task can be reported as complete.
