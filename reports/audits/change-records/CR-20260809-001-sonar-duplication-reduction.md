# Change Record CR-20260809-001: Sonar duplication reduction

**Language:** English | [Deutsch](CR-20260809-001-sonar-duplication-reduction.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260809-001` |
| Date (UTC) | `2026-08-09` |
| Base revision | `27e8756e212fd9452d99e285743dbadc43c814a6` |
| Scope | Parent repository only; no Framework, MRTS, Gitlink, workflow, lock-file, or quality-gate change |

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

## Changed files

- `ci/tools/update-workflow-tools.py`
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
| `python -m py_compile` for the changed Python modules | Passed |
| `make check-ci-security-contract` | Passed: 22 tests; checksum-locked actionlint, zizmor, and gitleaks validation passed |
| checksum-locked actionlint with ShellCheck | Passed for `.github/workflows/*.yml` |
| checksum-locked `zizmor --offline .github/workflows` | Passed: no findings (87 repository-suppressed findings reported by zizmor) |
| `git diff --check HEAD` | Passed |
| Focused security-diff scan | Passed: complete six-file coverage and zero reportable findings |
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

Hosted GitHub Actions and SonarCloud PR analysis are pending at publication of
this local record and must be recorded from their observed results.

## Checks not run and rationale

- The repository has no targets named `test-ci-security-contract`,
  `test-workflow-action-pins`, `check-github-actions-workflows`, or
  `check-documentation`; their closest existing targets were used where
  applicable.
- `ruff` and `pyright` are not installed locally and the repository contains
  no configured replacement target.  No tool was installed or bypassed.
- actionlint, zizmor, and gitleaks were not preinstalled.  The first two were
  downloaded to the external task directory only through the repository's
  checksum-locked fetcher and then executed; the diff-based gitleaks run is
  deferred until the review commits give the work an exact Git range.
- The first `make lint` run exited 2 when a Parent test hard-coded a Framework
  source path relative to the isolated task worktree.  The pinned Framework
  source exists in the authoritative checkout, but this test ignores the
  documented `FRAMEWORK_ROOT` override.  No Framework content or Gitlink was
  changed to work around it.

## Known limitations

Local checks cannot prove the post-change SonarCloud duplication metrics or
the hosted PR quality gate.  The requested hosted analysis remains the
authoritative measurement.  The full local lint target is currently blocked
only by the task worktree's unmaterialized Framework Gitlink dependency.

## Remaining risks

The principal residual risk is behavioral drift in the security-sensitive
updater.  It is reduced by preservation tests, explicit immutable schema
objects, an independent diff audit, the focused security-diff scan, and the
pending hosted checks; it is not eliminated until those checks and SonarCloud
remeasurement are observed.  The audit noted that an artificial,
non-normalized in-memory action record could cause a derived release URL to be
classified as changed before same-version validation rejects it. Valid lock
normalization deterministically derives that URL, so this is not a reachable
lock-file path.

## Final diff and review status

Local refactor validation is complete except for the documented full-lint and
documentation-link infrastructure blockers caused by the unmaterialized
Framework Gitlink. The Change Record's machine-required headings and identity
fields were accepted before those unrelated link checks. It is pending
reviewable commits, a single Draft PR, a diff-based secret scan, hosted GitHub
Actions, and post-PR SonarCloud metric/block comparison. It does not authorize
a merge.
