# Change Record: Parent bilingual-documentation checker PR-template literal extraction and diagnostic-order preservation for SonarQube Cloud S1192 and S3776

**Language:** English | [Deutsch](CR-20260727-sonar-bilingual-doc-checker.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-bilingual-doc-checker |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud `python:S1192` AZ9dAfch4Zz5JRbUl4id (repeated PR-template literal) and `python:S3776` AZ9dAfch4Zz5JRbUl4ie (cognitive complexity 18 > 15). |
| Boundary | Parent `ci/checks/documentation/check-bilingual-docs.py`, its Parent unit test, this English/German Change Record pair, and their indexes. Framework/MRTS content and Gitlinks, scanner configuration, Quality Gates, suppressions, external Sonar state, GitHub state, connector/runtime behavior, and delivery are unchanged. |

## Motivation and problem statement

The bilingual-documentation checker repeated the PR-template path literal in
five locations: three operational path uses and two diagnostic prefixes. Sonar
rule `python:S1192` reports that duplicate. The same
`check_change_record_pair()` routine combined Change Record heading checks with
filename and identity checks, which Sonar rule `python:S3776` measured at
cognitive complexity 18 where the threshold is 15. The batch must make those
responsibilities explicit without changing PR-template inclusion/exemption
semantics or the established diagnostic order.

## Acceptance criteria

- Introduce `PR_TEMPLATE_PATH` and use it at all five existing PR-template
  path references.
- Keep `.github/pull_request_template.md` exempt from English/German companion
  pairing while retaining its required-template validation and path-qualified
  diagnostics.
- Extract the Change Record heading and filename/identity checks into focused
  helpers without changing the wrapper's early-return rules or its diagnostic
  order.
- Add focused regressions for the retained PR-template behavior and the exact
  Change Record diagnostic sequence.
- Maintain this English/German Change Record pair and both indexes, recording
  this documentation subtask's `tests.test_bilingual_docs` and
  `git diff --check` validations.

## Implementation decision and rationale

`PR_TEMPLATE_PATH = Path(".github/pull_request_template.md")` is the single
owner of the PR-template path. `pair_required()`, `checked_markdown_files()`,
and `check_pr_template()` retain their former behavior by comparing or joining
that same relative `Path`; emitted diagnostics continue to name the same path.

`check_change_record_headings()` performs the existing English-then-German
heading checks. `check_change_record_filename_and_identity()` then performs the
existing filename and identity checks. `check_change_record_pair()` retains its
non-record/README early return, heading-only template behavior, and ordered
extension of the second helper's diagnostics. The extraction is therefore
behavior-preserving rather than a change to Change Record policy or validation
semantics.

## Changed files

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- The initial relative-worktree `.venv/bin/python` selection was
  `blocked_environment` (exit 127): this isolated worktree contains no such
  virtual-environment executable, so no test ran from that invocation.
- Environment selection with the existing Parent virtual environment passed:
  its `sys.prefix` was the Parent `.venv` and differed from `sys.base_prefix`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`
  passed: 18 tests in 0.043s.
- `rtk proxy git diff --check` passed with no whitespace diagnostics.

## Security impact

`not_applicable` to the product security boundary: this is a maintainability
refactor of repository-owned documentation validation. It changes no input
trust boundary, path-containment rule, link-resolution rule, subprocess,
authorization, network behavior, scanner control, or suppression. No Codex
Security workflow is triggered by this documentation-checker maintenance batch.

## Runtime evidence

No connector, protocol, host, Framework, MRTS, report-generator, or production
runtime was run or changed. The focused unit suite exercises only checker
logic with in-memory temporary repository layouts; it is not runtime evidence.

## Known limitations

This documentation subtask records only `tests.test_bilingual_docs` and
`git diff --check`. Repository-wide documentation/link checks, builds,
linters, CI, review, PR state, and hosted SonarQube Cloud analysis remain
pending primary-candidate validation and are not claimed here.

## Remaining risks

A caller not covered by the focused suite could depend on a subtle diagnostic
ordering or PR-template-path representation. The added regressions assert the
PR-template exemption/inclusion contract and the complete ordered Change
Record diagnostic list. The two Sonar receipt IDs cannot be treated as resolved
externally until SonarQube Cloud analyzes the exact delivered head.

## Checks not run and rationale

- Full documentation/link checks, builds, linting, and unrelated unit suites
  are pending primary-candidate validation; they are outside this documentation
  subtask's scoped checks.
- No GitHub CI, remote SonarQube Cloud PR analysis, review, pull request,
  commit, push, merge, default-branch update, or Framework/MRTS action has
  occurred as part of this documentation contribution.

## Final diff and review status

This is an uncommitted local candidate on
`agent/sonar-bilingual-doc-checker-20260727`, based on
`1b0f8825f3510b99b603bb6cd6f0777e1710358e`. Delivery is only planned: if
later authorized, it is limited to a Draft pull request. Before either receipt
is described as resolved externally, the local HEAD, remote task-branch SHA,
and Draft-PR head SHA must be observed equal and SonarQube Cloud must report
its result for that exact head. No merge, Parent-`master` change, or external
Sonar resolution is asserted.
