# Change Record: static connector-mode workflow coverage

**Language:** English | [Deutsch](CR-20260812-connector-mode-workflow-coverage.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260812-connector-mode-workflow-coverage |
| Date (UTC) | 2026-08-12 |
| Base revision | `33973d094b3f0aeb47605f08ced16a4043f643a0` |
| Delivery status | Implemented and locally validated in a task-owned Parent worktree; commit, push, Draft PR, hosted checks, and Ready-for-Review disposition remain pending. |

## Motivation and problem statement

The current connector state needs an explicit, truthful workflow surface for
the four CRS/MRTS mode combinations without claiming capabilities that are not
implemented. Apache and HAProxy have native runtime paths for all four modes.
Envoy, Traefik, and lighttpd have a no-CRS/no-MRTS runtime path, a static
Framework contract for with-CRS/no-MRTS, and no supported MRTS full-matrix
route. NGINX is deliberately excluded because its protected broker has a
separate trust boundary.

## Acceptance criteria

- Four named top-level workflows each contain one direct, static five-row
  `strategy.matrix.include` and collectively implement the required twenty
  cells without NGINX or `_template` rows.
- Runtime cells invoke existing native controls and preserve cleanup and exit
  status. Contract cells run the existing static Framework contract and retain
  its `CONTRACT_VALIDATED`/`UNATTESTED` distinction.
- Expected-unsupported cells invoke the real full-matrix runner for the
  selected connector, `unknown`, and `_template`; each must reject with exit
  `2`, the invalid-choice diagnostic, and no build root.
- Workflow security remains read-only and fail-closed, with immutable action
  pins, no secrets or write token, no persisted checkout credentials, no
  `pull_request_target`, no cache, no privilege escalation, and no broad
  artifact publication.
- On a pull request, checkout and the recorded Parent revision use the event's
  immutable head SHA; `github.sha` is only the manual-dispatch fallback.
- Parent and Framework/MRTS Gitlinks stay fixed at
  `209389022c942d83113f6be88bf31d25637352f0` and
  `615b13bacbd008562c17408246c41ab27dca3104` respectively.

## Implementation decision and rationale

The four workflows use exactly the five non-NGINX connectors: `apache`,
`envoy`, `haproxy`, `lighttpd`, and `traefik`. Their static mapping is:

| Connector | no-crs/no-mrts | with-crs/no-mrts | no-crs/with-mrts | with-crs/with-mrts |
| --- | --- | --- | --- | --- |
| apache | runtime | runtime | runtime | runtime |
| haproxy | runtime | runtime | runtime | runtime |
| envoy | runtime | contract | expected_unsupported | expected_unsupported |
| traefik | runtime | contract | expected_unsupported | expected_unsupported |
| lighttpd | runtime | contract | expected_unsupported | expected_unsupported |

The implementation reuses existing Parent entry points only. It does not add a
connector capability, alter the full-matrix allowlist, write Framework or MRTS
source, or modify the existing workflow-tool updater. The latter's unrelated
all-workflow inventory regression already fails for an action-free local
reusable caller on the clean base; this task does not weaken or alter that
test oracle.

Before the static Framework contract is invoked, its required CI dependency is
installed from the Framework's hash-locked `requirements-ci.lock`; the step
uses `--require-hashes` and `pip check` rather than a mutable dependency path.
The checked-out Parent, Framework, and MRTS revisions are verified against the
recorded immutable SHAs before that lockfile is read.

## Changed files

- Four `test-connectors-*.yml` workflows.
- Focused workflow and Python-version contract tests/checker.
- This English/German Change Record pair and its archive indexes.

No connector source, capability manifest, lifecycle runner, Framework/MRTS
source, Gitlink, dependency lock, ruleset, or NGINX workflow changes are part
of this change.

## Commands executed

- The pinned Framework static five-connector CRS contract and CRS-provenance
  regression both passed.
- `tests.test_ci_security_workflows` plus
  `tests.test_python_version_contract` passed: 56 tests.
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract` passed: 69 tests, three expected environment
  capability skips, and validate-only actionlint/zizmor/gitleaks lock checks.
- PyYAML loaded all four workflows, and ShellCheck passed every extracted
  GitHub-hosted Bash `run:` script at warning severity.
- The direct Python workflow-contract checker reports the same 24 pre-existing
  inventory/setup diagnostics in the clean base and task worktrees. It reports
  no diagnostic caused by these four workflows.

## Security impact

The workflows are pull-request-safe by construction: top-level
`permissions: contents: read`, immutable full-SHA action pins, recursive
checkout with `persist-credentials: false`, and no user-controlled ref in a
shell command. The event head SHA is used only as the declarative checkout and
revision-equality input, never interpolated into a shell body. Unsupported routes execute only a parser rejection under the
private runner temporary root; a rejection log is diagnostic-only and no
build/evidence artifact is uploaded. Static contract routes do not pretend to
be host runtime evidence. Their sole dependency installation uses the
Framework's hash-locked CI requirements and fails closed on an invalid
dependency set after the immutable Gitlink revisions have been verified.

## Runtime evidence

Before implementation, all 18 selected/`unknown`/`_template` negative runner
attempts for the six unsupported cells rejected with exit `2` and created no
build root. The Framework contract and provenance tests are static evidence
only. No local connector build or host runtime was run; the four new hosted
workflows must supply their own exact-head runtime evidence.

## Known limitations

Local `actionlint` and `zizmor` binaries are unavailable and were not
downloaded or installed. The installed ShellCheck binary cannot replace
actionlint's workflow/YAML analysis. A local static result does not prove
GitHub-hosted runner behavior, connector runtime success, or exact PR-head
security enforcement.

The pre-existing updater exact-inventory regression remains outside the
authorized path list: correcting it would require an unrelated test-oracle
change and modifying an existing updater workflow/tool.

## Remaining risks

Apache and HAProxy runtime cells still depend on hosted runner prerequisites
and their existing build paths. Envoy, Traefik, and lighttpd MRTS cells remain
explicitly unsupported until an independently authorized capability and
evidence change exists. A failure in a fresh hosted run must be investigated
without weakening the negative, static-contract, cleanup, or security guards.

## Checks not run and rationale

- Local actionlint, actionlint-mediated ShellCheck, and zizmor scans: their
  pinned binaries are absent and fetching tools is outside this task's local
  validation authority. Exact-head hosted checks are required instead.
- Local connector runtime/build matrix: the task is workflow/test-only and
  hosted workflows are the requested runtime evidence path.
- Current-head PR checks, SonarQube Cloud applicability, review, merge, and
  resulting-master validation: no commit or pull request exists yet. Merge is
  explicitly out of scope.

## Final diff and review status

This is a pre-delivery record. Local scoped contracts pass except for the
separately reproduced pre-existing global Python inventory diagnostics. The
final review must verify the exact committed head, remote branch, PR head,
four workflow runs, actionlint/ShellCheck/zizmor, required checks, and Sonar
applicability before the PR is marked Ready for Review.
