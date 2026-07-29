# Change Record: Parent Common smoke-writer output-path containment for SonarQube Cloud security findings

**Language:** English | [Deutsch](CR-20260729-sonar-common-smoke-writer-path-security.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-smoke-writer-path-security |
| Date (UTC) | 2026-07-29 |
| Base revision | Original change base `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`; synchronized candidate base `964630d34d0b87e9066d03131e445eeb3677956d` |
| Tracking | SonarQube Cloud `python:S5443` at `common/scripts/write_smoke_result.py:67` and `pythonsecurity:S8707` at lines 83, 90, 97, 347, and 348. The separate `python:S3776` complexity item remains outside this security-only batch. PR #176's prior head reported no new Security findings or duplication but four test-only `python:S5778` Code Smells; the synchronized test-structure follow-up requires a new exact-head analysis. |
| Boundary | Parent `common` runtime-smoke evidence writer, its focused Python security regression test, and paired Change Record/index documents. Framework, MRTS, Gitlinks, workflows, SonarQube policy, and `master` are not modified. |

## Motivation and problem statement

The direct writer accepted output roots that only had to be absolute and outside the checkout. A pre-fix direct invocation set `VERIFIED_RUN_ROOT` to one task root while supplying `--evidence-root` below a sibling root; it created out-of-root `result.json`. Generic writes also followed a pre-existing output-file symlink, and `connector` was interpolated into result filenames without a component check.

## Acceptance criteria

- Every writable CLI root is an absolute, private, symlink-free descendant of `VERIFIED_RUN_ROOT` before output is created.
- Out-of-root values, output-directory symlinks, output-file symlinks, and connector path traversal are rejected without an outside artifact.
- A legitimate private in-root invocation retains JSON, JSONL, and status-log artifacts.
- Existing runtime-smoke path-policy behavior and Python syntax remain valid.

## Implementation decision and rationale

The writer now uses `verified_runtime_paths`, `is_safe_runtime_root`, and `ensure_safe_runtime_directory` before it derives an output filename. All five write-capable CLI roots are checked against the verified runtime root; `connector` is one lower-case filename component. Output files use `os.open` with `O_NOFOLLOW`, are forced to mode `0600`, and are written only after their parent roots are verified. This protects both direct invocation and the existing `run_local_runtime_smoke.py` caller without changing supported in-root layout.

## Security impact

Controlled inputs are `--evidence-root`, `--results-dir`, `--tmp-root`, `--log-root`, `--log-dir`, and `--connector`; protected assets are runtime evidence and host files outside the selected run; the sink is file creation/truncation through JSON/text writers. Validation now precedes every sink: roots are beneath the verified runtime root and pass private no-symlink checks, connector cannot introduce a path component, and descriptors refuse symlink following. The original trigger now exits `BLOCKED`; the legitimate control writes only under the verified root. No control is weakened.

## Changed files

- `common/scripts/write_smoke_result.py`
- `tests/test_write_smoke_result_security.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260729-sonar-common-smoke-writer-path-security.md`
- `reports/audits/change-records/CR-20260729-sonar-common-smoke-writer-path-security.de.md`

## Commands executed

| Command or control | Actual result |
| --- | --- |
| Direct pre-fix writer invocation with `evidence_root` outside `VERIFIED_RUN_ROOT` | reproduced: created out-of-root `result.json`. |
| Identical post-fix invocation | passed closure control: exited `BLOCKED` and did not create a new outside artifact. |
| Direct in-root writer invocation | passed legitimate control: created expected `result.json`, `common-results.jsonl`, and `status.log` only below the verified root. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_write_smoke_result_security tests.test_common_runtime_smoke_crs_source_security tests.test_runtime_path_security` | passed, 50 tests. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_bilingual_docs` | passed, 21 tests. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m py_compile common/scripts/write_smoke_result.py tests/test_write_smoke_result_security.py` | passed. |
| `git diff --check` | passed. |
| Initial SonarQube Cloud PR #176 analysis | 0 new Security findings and 0 New-Code duplicate lines; 4 `python:S5778` test smells found and remediated by the current follow-up. |

## Tests and actual results

| Control | Result |
| --- | --- |
| Legitimate output | passed: private verified-root evidence, results, and log files are written. |
| Original path-escape trigger | passed: out-of-root evidence path is rejected before an outside directory exists. |
| Directory-symlink bypass | passed: symlinked output directory is rejected. |
| Output-file-symlink bypass | passed: `O_NOFOLLOW` rejects `result.json` replacement. |
| Connector traversal bypass | passed: `../outside` is rejected before any runtime root is created. |

## Runtime evidence

The direct writer controls use the real CLI, parser, path validation, and file-write boundary. No connector server, Framework, or MRTS runtime was started.

## Checks not run and rationale

- Full connector runtime matrices were not run because the patch is confined to the evidence writer; direct CLI and existing runtime path-policy tests exercise the altered boundary.
- A full repository security scan was not run; the concrete findings were revalidated, reproduced, and tested through the affected sink.
- `make check-bilingual-docs` is blocked_environment: its only failures are pre-existing links into the deliberately uninitialized Framework submodule, while the focused bilingual suite passed 21 tests. The submodule, its Gitlink, and Framework checks remain out of scope.
- A new exact-head GitHub Actions, SonarQube Cloud PR analysis, and review round is pending after the test-structure follow-up.

## Known limitations

The separate `python:S3776` complexity finding in `main` is not refactored by this security-only batch. There is no connector-host integration or hosted evidence yet.

## Remaining risks

The writer intentionally depends on the caller's verified-runtime environment. If it is absent, broad, or unsafe, the writer now fails closed rather than selecting another root. Exact-head hosted analysis remains required before the listed Sonar findings are treated as resolved.

## Final diff and review status

The scoped diff contains only writer containment, its security regression test, and bilingual traceability. Local security closure, bypass, legitimate-control, syntax, runtime-path regression, and whitespace checks passed. PR #176 is open and non-draft; no merge occurred. Fresh exact-head hosted verification is pending after the normal `master` synchronization and test-structure follow-up.
