# Change Record CR-20261122-manual-common-header-fuzz

**Language:** English | [Deutsch](CR-20261122-manual-common-header-fuzz.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261122-manual-common-header-fuzz |
| Date (UTC) | 2026-11-22 |
| Base revision | `d21e34eb42b7e12793f670e318954798293bb897` |

## Motivation and problem statement

Make the existing Common HTTP header fuzz test available to maintainers through GitHub Actions.

## Acceptance criteria

The workflow starts with `workflow_dispatch`, runs the existing bounded Make target on a GitHub-hosted runner, and fails the job when the test fails.

## Implementation decision and rationale

The selected Connector revision supplies product sources and its recorded Framework Gitlink supplies the harness. The initial Gitlink is `b4d619127a3fbd2a4074998e874c592d693413b9`.

On the default branch, use **Actions → Common HTTP header fuzzing → Run workflow**.

## Changed files

- `.github/workflows/fuzz-common.yml`
- This English and German Change Record pair.

## Commands executed

Repository-pinned `actionlint` with the repository's configuration and `bash -n` both exited `0`. The exact workflow shell step, exercised locally with Clang 19.1.7, exited `0`.

With Clang available and `BUILD_ROOT` set to a writable absolute path outside the worktrees, run:

```sh
rtk make ON_DEMAND_TESTS=1 BUILD_ROOT="$BUILD_ROOT" check-common-http-header-fuzz
```

## Security impact

The job uses a five-minute limit, read-only repository permissions and checkout without persisted credentials. The build, compiler temporary files and full fuzz output stay in a per-run temporary directory. The job publishes only the test status.

## Runtime evidence

The existing in-process fuzz harness completed in the local check. The test does not start a Connector service.

## Known limitations

The checks cover the shared HTTP header helper. The available test harness follows the selected Connector revision's Framework Gitlink.

## Remaining risks

The bounded run samples generated inputs for 15 seconds. Retain the fixed regression suite for continuous coverage.

## Checks not run and rationale

A hosted manual dispatch is pending until the workflow is available on the default branch. The local validation disabled LeakSanitizer because the scratch sandbox restricts its process inspection.

## Final diff and review status

The diff adds the manual workflow and the paired Change Record. The current pull-request test inventory stays in effect.
