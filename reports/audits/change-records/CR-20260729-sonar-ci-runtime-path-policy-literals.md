# Change Record: Parent CI runtime-path-policy fixed-fixture literal ownership for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260729-sonar-ci-runtime-path-policy-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-runtime-path-policy-literals` |
| Date (UTC) | `2026-07-29` |
| Base revision | `5a345e3ff90cf5405caea5ff7ae4536b52f826c9` |
| Boundary | Parent `ci/checks/security/check-runtime-path-policy.py`, its direct Parent test `tests/test_runtime_path_policy.py`, this English/German Change Record pair, and paired indexes only. No `.github/`, `scripts/`, Framework or MRTS source, Gitlink, SonarQube Cloud rule, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Current `python:S1192` issues `AZ9cRyb-HhV2CayPTPwj`, `AZ9cRyb-HhV2CayPTPwh`, `AZ9cRyb-HhV2CayPTPwi`, and `AZ9cRyb-HhV2CayPTPwg` for repeated fixed `/var/lib/foo`, `/var/log/foo`, `/etc/foo`, and `/usr/local/foo` self-test fixtures. |

## Motivation and problem statement

The runtime-path-policy checker deliberately probes fixed denied paths through
its Python, Framework-shell, and HAProxy self-test branches. Four exact test
fixture strings appeared three times each, which SonarQube Cloud reports as
four `python:S1192` maintainability issues. These fixtures are security
controls, not interchangeable cosmetic examples.

## Implementation decision and rationale

`VAR_LIB_SELFTEST_PATH`, `VAR_LOG_SELFTEST_PATH`,
`ETC_SELFTEST_PATH`, and `USR_LOCAL_SELFTEST_PATH` now own the four repeated
fixed strings. `PYTHON_BLOCKED_RUNTIME_PATHS` retains the existing ordered
seven-path Python denial set; `SHELL_SYSTEM_PATH_SELFTEST_PATHS` keeps the
existing six-path shell subset; and `HAPROXY_BLOCKED_SOURCE_ROOTS` retains the
existing four-path HAProxy order. No value is derived from the environment,
filesystem, configuration, or tool output.

## Acceptance criteria

- The exact seven Python denied fixtures, six shell denied fixtures, and four
  HAProxy denied source roots retain their prior values and ordering.
- The Python and shell policy self-tests retain their allow/deny, quoting, and
  exit behavior.
- Manipulated project roots, broad runtime parents, `/etc`, `/root`, source
  mounts, and the legitimate verified external runtime root retain their
  current control outcomes.
- A future exact PR head must have zero new SonarQube Cloud issues, zero new
  duplicated lines, and `0.0%` New-Code duplication without weakening rules
  or controls.

## Changed files

- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_runtime_path_policy.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-path-policy-literals.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-path-policy-literals.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Six focused `python -B -m unittest -v` controls from `tests.test_runtime_path_policy` | passed. They cover fixed-fixture grouping, Python self-test behavior, mocked shell-policy calls, broad-parent denial, mutable-project-root denial, and verified-runtime-root controls. |
| Direct changed-checker control with the existing read-only Framework `common.sh` dependency | passed. It reports the expected `/root` denial and all four HAProxy blocked-source-root controls, then `check-runtime-path-policy: PASS`. |
| Default-policy subprocess test on the unchanged main checkout | passed. It confirms that a caller-provided cache override cannot poison the checker’s default probe; it is recorded separately because the isolated task worktree lacks the Framework dependency. |
| Python `-m py_compile` for the changed checker and direct test module with an external bytecode-cache root | passed. |
| Direct Change Record-pair validation and `tests.test_bilingual_docs` | passed. The pair has matching required headings and identity values; the focused documentation test module ran 21 tests successfully. |
| Final `git diff --check` | passed for the full six-file task diff. |
| Focused security preflight | passed with disposition `already_safe`: centralizing source-authored immutable self-test data introduces no new input, filesystem, subprocess, network, credential, or privilege path. |
| Final focused security-diff review | passed with no plausible diff-induced security finding. It independently confirmed that values, grouping, shell quoting, subprocess construction, and fail-closed behavior are unchanged. |
| Initial exact-head SonarQube Cloud PR query for #195 | failed the task criterion: one new `python:S3415` at the added test assertion, while duplication remained `0.0%`. The issue correctly identified reversed `assertEqual` actual/expected arguments; the test now passes the source-authored actual tuple first and local controls were rerun. |

## Security impact

The checker is security-relevant because it verifies that environment values
cannot authorize broad or system-writable runtime paths. Its invariant is that
only the narrow verified external run root is writable; source mounts remain
read-only inputs and system/privileged paths remain denied. The extraction
does not change `policy_environment()`, `is_system_write_path()`,
`is_allowed_runtime_path()`, `verified_runtime_paths()`, shell quoting,
subprocess construction, error handling, or exit behavior.

No security finding is claimed, suppressed, or closed.

## Runtime evidence

No connector runtime, package installation, download, provisioned component,
network service, or host matrix is claimed. The direct checker control invokes
only its established policy self-test path and verifies denial behavior; it is
not evidence of a full HAProxy runtime.

## Checks not run and rationale

- The complete `tests.test_runtime_path_policy` module in the isolated task
  worktree could not complete its subprocess-based default-policy test because
  that worktree intentionally lacks a materialized Framework
  `ci/lib/common.sh`. The same test passes on the unchanged main checkout,
  and the changed checker passed through the existing read-only Framework
  dependency using the focused direct control. No Framework source was
  changed or initialized as a workaround.
- `make check-runtime-path-policy` was not run in the task worktree for the
  same absent Framework-worktree dependency. It is not replaced by a claim
  that the Make target passed.
- The complete `check-bilingual-docs.py` scan was run in the isolated task
  worktree and reports only pre-existing links into the absent Framework
  checkout. The Change Record pair itself passed its direct structural
  validation and the focused bilingual-documentation tests; no Framework
  source was materialized or changed to make the broader scan pass.
- No broad lint, connector runtime, provisioning, download, package install,
  Framework/MRTS action, Gitlink change, `.github/` action, or unrelated
  Parent check was run because this task changes only fixed Parent CI
  self-test data.
- Hosted GitHub Actions, SonarQube Cloud PR analysis, review, and merge
  evidence do not exist yet and are not inferred locally.

## Known limitations

The selected four findings are a small part of the current Parent CI SonarQube
Cloud backlog. The unclaimed Clang SARIF-parser complexity issue remains
separate for a later focused PR.

## Remaining risks

Residual risk is limited to accidentally omitting, reordering, or mis-grouping
a fixed fixture; the new direct grouping test plus the existing Python and
shell policy controls cover that risk. The exact hosted PR head must still
prove the four `S1192` issues are absent and that no new issue or duplication
was added.

## Final diff and review status

The task-owned branch was pushed and [Draft PR #195](https://github.com/Easton97-Jens/ModSecurity-conector/pull/195)
exists against `master`. When `master` advanced, a normal merge of the current
`master` into the task branch preserved the published PR history; only the two
Change Record indexes conflicted and both records were retained. The one new
SonarQube Cloud `python:S3415` issue then found at the initial PR head is
locally corrected. The updated exact head must still be pushed and hosted
analysis, reviews, and exact-head verification remain pending. No merge into
`master` is authorized or claimed.
