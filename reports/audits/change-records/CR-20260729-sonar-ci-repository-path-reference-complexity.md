# Change Record: Parent CI repository-path-reference complexity remediation

**Language:** English | [Deutsch](CR-20260729-sonar-ci-repository-path-reference-complexity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-repository-path-reference-complexity` |
| Date (UTC) | `2026-07-29` |
| Base revision | `5a345e3ff90cf5405caea5ff7ae4536b52f826c9` |
| Tracking | Open SonarQube Cloud `python:S3776` issue `AZ9cRyWvHhV2CayPTPuo` at `main()` in `ci/checks/documentation/check-repository-path-references.py`, requesting cognitive complexity reduction from 17 to 15. |
| Boundary | Parent `ci/` checker, its direct Parent test, this English/German Change Record pair, and paired indexes only. No `.github`, `scripts`, Framework, MRTS, Gitlink, product source, Sonar rule/profile/gate/exclusion/suppression, or `master` change. |

## Motivation and problem statement

The portable documentation checker had one `main()` function responsible for
both per-document parsing and repository-wide traversal, filtering,
aggregation, presentation, and exit behavior. SonarQube Cloud reports the
resulting cognitive complexity as 17 where 15 is allowed. The remediation must
remove only that structural complexity while keeping every documentation-path
diagnostic and all compatibility behavior unchanged.

## Acceptance criteria

- A private per-document helper preserves UTF-8 reads, local developer-path
  detection, obsolete `COMPILE_*` detection, link extraction, the two legacy
  placeholder exemptions, raw missing-target text, and propagated read errors.
- `main()` retains the same document inventory, ignored generated-document
  handling, deterministic `sorted(set(errors))` aggregation, stderr failure
  output, stdout success output, and return codes.
- Direct tests cover local/encoded/angled/parent-relative/fragment links,
  scheme/netloc links, raw missing targets, literal query behavior, errors,
  ignored documents, deduplication, ordering, streams, and exit statuses.
- The exact Draft-PR head must later have a SonarQube Cloud Quality Gate `OK`,
  zero new issues, zero new duplicated lines, and `0.0%` new-code duplication
  without a rule, profile, gate, exclusion, suppression, or false-positive
  change.

## Implementation decision and rationale

`document_diagnostics(path)` now owns exactly the existing per-document
read/scan/diagnostic loop. `main()` continues to select current documents,
skip ignored paths, aggregate diagnostics, and control output and exit status.
`local_target()` is not changed: it continues to trim/unwrap, percent-decode,
skip fragment-only and scheme/netloc targets, strip fragments, and resolve
remaining paths relative to the source document. This is a narrow extraction,
not a change to path containment or link policy.

## Changed files

- `ci/checks/documentation/check-repository-path-references.py`
- `tests/test_repository_path_references.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-repository-path-reference-complexity.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-repository-path-reference-complexity.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_repository_path_references` | passed: 6 direct tests. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m py_compile ci/checks/documentation/check-repository-path-references.py tests/test_repository_path_references.py` | passed. |
| `git diff --check` for the source/test implementation before this traceability update | passed. |
| Direct Parent checker with bytecode disabled | `blocked_external_dependency`: it reports only pre-existing links to absent Parent-pinned Framework README/rule files in this isolated worktree; no task-owned document is named. |
| Direct `check-bilingual-docs.py` | `blocked_external_dependency`: 20 diagnostics name only established absent Framework-Gitlink targets; this Change Record pair and indexes are not named. |
| `make check-doc-links` with bytecode disabled | `blocked_external_dependency`: the direct Parent checker emits the same 16 pre-existing absent Framework README/rule targets and exits before the Framework checker. |
| Focused security preflight | passed / `already_safe`: the extraction adds no source type, privilege, sink, or control bypass; focused post-diff review remains required. |
| Focused final security-diff review | passed / `already_safe`: full changed checker/test flow review confirmed that `local_target()`, document roots, ignored-path boundary, raw diagnostics, existing read/resolve/exists calls, streams, and exit behavior are unchanged; no new filesystem, process, network, privilege, cache, or logging path exists. |

## Security impact

Repository-controlled Markdown remains the relevant input. Its links continue
through the unchanged `local_target()` parser into the existing local
`Path.resolve()` and `Path.exists()` checks; `document_diagnostics()` only
moves the already-present UTF-8 read and diagnostic loop into a private helper.
There is no new traversal root, file write, process, network request, cache,
log, or output channel. The test suite retains both negative and legitimate
path/link controls. A pre-existing POSIX-absolute link can still produce an
existence probe outside the repository; no confidentiality, integrity, or
execution impact was established, and changing that semantic is out of scope.

## Runtime evidence

No connector, host, network, or protocol runtime applies. The direct unit
suite is in-process documentation-checker evidence only. The direct whole-tree
checker was attempted but is blocked by missing Framework Gitlink content, so
it is not represented as a successful runtime or documentation-tree result.

## Known limitations

This task does not restore or materialize the missing Framework Gitlink files.
Consequently, the isolated worktree cannot currently produce a successful
whole-tree `check-repository-path-references.py`, `check-bilingual-docs.py`,
or `make check-doc-links` result even though the new checker-specific unit
tests and direct Change-Record validation pass.

## Remaining risks

A future change to document enumeration, `local_target()`, or output handling
must retain the tests' URL/path and aggregation contract. Hosted analysis is
still required to prove that SonarQube Cloud attributes no new issue or
duplication to the exact delivered head.

## Checks not run and rationale

- Broad `make lint` is not run because the already-executed direct checker and
  `make check-doc-links` establish the same absent-Framework blocker before
  unrelated validation layers can add task-irrelevant failures.
- No Framework, MRTS, Gitlink, `.github`, `scripts`, product-source, connector
  runtime, or matrix command is in this Parent-`ci/` scope.
- Exact-head GitHub Actions, review, and SonarQube Cloud evidence require a
  pushed Draft PR and are not inferred locally.

## Final diff and review status

The working candidate contains the private helper, six direct regression
tests, and this bilingual traceability update. Final local source/test and
security-diff review passed, while whole-tree documentation checks remain
truthfully blocked by absent Framework-Gitlink targets. This record claims no
remote push, pull request, hosted result, or merge. Exact-head hosted
verification is required after the task commit is delivered through a Draft PR.
