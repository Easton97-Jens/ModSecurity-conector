# Change Record CR-20260809-001: Sonar duplication reduction

**Language:** English | [Deutsch](CR-20260809-001-sonar-duplication-reduction.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260809-001` |
| Date (UTC) | `2026-08-09` |
| Base revision | `cc58f94e6a0dd17eea651cd46376843472b83f7c` |
| Scope | Parent repository only; no Framework, MRTS, Gitlink, lock-file, or quality-gate change; one user-authorized exact publisher staging entry |

## Motivation and problem statement

SonarCloud reported duplicated-code density above the requested threshold in
the workflow-tool updater and its test module, plus two duplicated C-source
parsing helpers in NGINX contract tests.  The change removes only demonstrated
structural duplication while retaining the security review points of the
updater.

The recorded pre-change SonarCloud metrics were:

| Component | Duplicated-lines density | Duplicated lines | Duplicated blocks |
| --- | ---: | ---: | ---: |
| `tests/ci_security/test_update_workflow_tools.py` | 67.2% | 709 | 13 |
| `ci/tools/update-workflow-tools.py` | 62.1% | 1,305 | 15 |
| `tests/test_nginx_intervention_url_ownership.py` | 18.1% | 25 | 2 |
| `tests/test_nginx_upstream_security_contract.py` | 6.6% | 25 | 2 |

## Acceptance criteria

- Refactor only the approved Parent source and test scope, with small shared
  test support where necessary.
- Preserve update CLI flags, YAML/lock serialization, candidate canonical
  JSON, SHA-256 inputs, exit codes, rejection behavior, and output paths.
- Preserve strict trust boundaries for action/tool identity, immutable pins,
  release commits, URLs, asset paths, hashes, and Runner temporary paths.
- Do not use `NOSONAR`, Sonar exclusions, suppression annotations, test
  deletion, weaker assertions, quality-gate changes, or generic lock-record
  merges.
- Run focused tests, compilation, contract checks, documentation checks, a
  security-diff scan, and hosted PR/SonarCloud validation.

## Implementation decision and rationale

- Added `CandidateGroupSpec` and immutable candidate-payload construction to
  centralize the reviewed action/tool schema while keeping the distinct action
  and tool identity and release-resolution paths explicit.
- Kept all public helper function names at their current call sites; their
  implementations delegate to narrowly scoped immutable boundary objects for
  Runner temporary paths, workflow inventory, and the GitHub API.
- Added `tests/c_source_contract.py` for balanced C-definition extraction and
  its unit tests, then made both NGINX tests consume that helper.
- Replaced repeated test fixture maps with explicit fixtures and table-driven
  cases.  Existing test methods remain present and additional rejection and
  immutability cases were added.
- A follow-up test-only consolidation shares Connector-specific proposed-tree
  and generated-branch fixtures while retaining independent lock, RUNNER_TEMP,
  exact-blob, and malicious-publisher assertions. It also isolates a release
  fixture before the exception context, resolving S5778 without changing the
  negative test.

## Security impact

The modified updater crosses input, filesystem, network, serialization, and
lock-file trust boundaries.  The refactor preserves strict candidate-group
fields; immutable action pin and tool release-commit validation; trusted
GitHub origin and redirect validation; URL, asset, and SHA-256 checks;
canonical candidate JSON; safe relative-path and symlink rejection; and
atomic lock-file replacement.

The focused security-diff scan covered all six changed code files and produced
zero reportable candidates.  It did not identify a new attack path or a
weakened control.

After the rebase onto current `origin/master`, the pre-existing trusted NGINX
root-broker workflow exposed a fail-closed gap: its locked Action pins were not
in the updater's finite publisher path set. The user explicitly authorized the
only complete companion repair: the exact same literal path in the existing
publisher `git add --` list. The source/staging equality control, real coverage
test, and existing fail-closed negative control pass. A second focused
two-file Security diff review also has zero reportable findings.

SonarCloud initially identified one task-owned S5778 test smell. Its
two-invocation exception context was split into explicit setup plus the single
operation under assertion; the original immutable-release rejection remains
covered. The resulting PR code head has Quality Gate OK, zero unresolved
issues, zero Security Hotspots, and no accepted issue. The historical S5778
record is resolved as FIXED, not accepted or open.

## Changed files

- `ci/tools/update-workflow-tools.py`
- `.github/workflows/update-workflow-tools.yml` (one user-authorized matching staging path)
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/c_source_contract.py`
- `tests/test_c_source_contract.py`
- `tests/test_nginx_intervention_url_ownership.py`
- `tests/test_nginx_upstream_security_contract.py`
- `reports/audits/change-records/CR-20260809-001-sonar-duplication-reduction.md`
- `reports/audits/change-records/CR-20260809-001-sonar-duplication-reduction.de.md`

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| Focused unittest suite | Passed: 51 tests in 11.926 s |
| Follow-up updater/NGINX/helper suite | Passed: 51 tests in 12.602 s; the updater module retains 34 test methods |
| Rebased-current-master focused unittest suite before the narrow repair | Historical reproduction: 50 tests passed and one fail-closed publisher-allowlist error named only `.github/workflows/nginx-root-broker.yml` |
| User-authorized one-path publisher repair | Passed: focused suite 51 tests in 11.394 s; real coverage and fail-closed unallowlisted/YAML negative controls pass |
| `python -m py_compile` for the changed Python modules | Passed |
| `make check-ci-security-contract` | Passed: 23 tests; checksum-locked actionlint, zizmor, and gitleaks validation passed |
| checksum-locked actionlint with ShellCheck | Passed for `.github/workflows/*.yml` |
| checksum-locked `zizmor --offline .github/workflows` | Passed: no findings (88 repository-suppressed findings reported by zizmor) |
| checksum-locked diff-range gitleaks | Passed: six task commits scanned, no leaks found |
| `git diff --check HEAD` | Passed |
| Focused security-diff scan | Passed: complete six-file coverage and zero reportable findings |
| Focused authorized-workflow security-diff scan | Passed: complete two-file coverage and zero reportable findings |
| PR 256 code-head hosted checks | Passed: all applicable checks, including SonarCloud Code Analysis, CodeQL, actionlint, zizmor, pull-request diff/range, structure, and connector-contract checks |
| PR 256 SonarCloud code-head readback | Quality Gate OK; 0 unresolved issues; 0 Security Hotspots; the sole intermediate S5778 record is FIXED |
| `make check-bilingual-docs` | Blocked only by 20 missing Framework-link targets in the unmaterialized task-worktree Gitlink; the Change Record emitted no heading/identity error |
| `make check-doc-links` with the authoritative `FRAMEWORK_ROOT` | Blocked only by the same local Gitlink link targets |

The focused suite includes the updater tests, both NGINX contract tests, and
the new C-source helper tests.  It verifies canonical candidate payload bytes
and SHA-256 input stability, CLI parsing, validation rejection paths, output
paths, and lock-file application behavior.

## Runtime evidence

No production connector runtime was required or executed because this is a
Python refactor of static CI-security tooling and contract tests.  The
applicable evidence is the focused unit/contract suite and the sealed
security-diff scan at
`/var/tmp/codex/ModSecurity-conector/tmp/codex-security-scans/ModSecurity-conector/27e8756e212fd9452d99e285743dbadc43c814a6_20260809T053956Z/report.md`.

At code-change head c43df1b01771523a9f8903a252232a9002786cdd, hosted GitHub
Actions and SonarCloud PR analysis passed. The PR remains Draft/open and no
merge authority is implied.

## Checks not run and rationale

- The repository has no targets named `test-ci-security-contract`,
  `test-workflow-action-pins`, `check-github-actions-workflows`, or
  `check-documentation`; their closest existing targets were used where
  applicable.
- `ruff` and `pyright` are not installed locally and the repository contains
  no configured replacement target.  No tool was installed or bypassed.
- actionlint, zizmor, and gitleaks were not preinstalled. They were downloaded
  to the external task directory only through the repository's checksum-locked
  fetcher; all three applicable checks then passed.
- The first `make lint` run exited 2 when a Parent test hard-coded a Framework
  source path relative to the isolated task worktree.  The pinned Framework
  source exists in the authoritative checkout, but this test ignores the
  documented `FRAMEWORK_ROOT` override.  No Framework content or Gitlink was
  changed to work around it.

## Known limitations

The requested hosted analysis is retained as the authoritative measurement.
The full local lint target remains blocked by the task worktree's
unmaterialized Framework Gitlink dependency. The publisher-path gap discovered
after the rebase is repaired under the user's explicit one-path workflow
authorization.

The NGINX files are both at 0.0% duplication. The updater test reaches 21.0%
and 252 duplicated lines, a 64.5% reduction from 709 and below the requested
25% target. The production updater improves from 1,305 to 951 lines at 41.5%
but does not reach the requested 50% or under-20% target. Every remaining block is an
exact Parent versus separately owned Framework counterpart. The blocks cover
path/symlink boundaries, release provenance, candidate schemas, immutable
lock mutation, publisher scope, and reusable-branch verification. Rewriting
them solely for CPD would be a security-sensitive reimplementation; sharing
them requires a coordinated Framework delivery, outside this task. Exact raw
block evidence is retained externally under the task Sonar evidence directory.

## Remaining risks

The principal residual risk is behavioral drift in the security-sensitive
updater.  It is reduced by preservation tests, explicit immutable schema
objects, an independent diff audit, the focused security-diff scan, and the
observed hosted checks and SonarCloud remeasurement. The audit noted that an artificial,
non-normalized in-memory action record could cause a derived release URL to be
classified as changed before same-version validation rejects it. Valid lock
normalization deterministically derives that URL, so this is not a reachable
lock-file path.

## Final diff and review status

The refactor commits are reviewable and based on current master. The
user-authorized two-line publisher repair restores the finite source/staging
contract without changing any Action pin, permission, lock, Framework, MRTS,
or Gitlink. PR 256 is one Draft PR and remains unmerged. The NGINX and updater
test targets are met, while the updater-source target is documented as
partially blocked by the independent Framework ownership boundary. This record
does not authorize a merge.
