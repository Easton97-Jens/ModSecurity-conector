# Change Record: Parent PR #128 residual SonarQube Cloud and workflow remediation

**Language:** English | [Deutsch](CR-20260727-sonar-pr128-residual-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-pr128-residual-remediation |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent PR #128 follow-up for SonarQube Cloud `python:S5843` AZ-jvTOkjjNxyah3ylvp, `python:S1192` AZ-jvTBTjjNxyah3ylvn, `python:S1172` AZ-jvTPajjNxyah3ylvq, and `python:S1481` AZ-jvTJijjNxyah3ylvo; plus the Parent Change Record contract that caused the PR and push lint workflows to fail. |
| Boundary | Parent Python source, Parent tests, Parent Change Records, and PR #128 only. Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, connector/runtime behavior, and external Sonar issue state remain unchanged. |

## Motivation and problem statement

The exact PR #128 SonarQube Cloud query reported four new code-smell rows. The
same candidate also failed the Parent lint workflow because seven newly added
Change Record pairs lacked the repository's required headings. The repair must
remove the local code/documentation causes without weakening a scanner, test,
workflow, or repository boundary.

## Acceptance criteria

- Preserve repository-organization variable matching while replacing the
  high-complexity regular expression with bounded component patterns.
- Give the English/German Markdown suffixes one static owner and preserve
  counterpart construction and link validation behavior.
- Remove only the unused compiler-guide dispatcher argument and the unused
  native-comparison local while retaining the supported `--build-root` CLI
  option.
- Bring all seven affected Change Record pairs into the required bilingual
  heading contract with truthful delivery and validation boundaries.
- Pass focused Parent tests and whitespace review where the uninitialized
  Framework Gitlink does not prevent the check; do not claim hosted Sonar or
  GitHub workflow success before it is observed for the delivered head.

## Implementation decision and rationale

`variable_matches()` merges two simple compiled patterns in source order and
preserves the former scanner's leftmost non-overlapping match behavior. The
documentation checker now owns both suffix constants rather than repeating the
German suffix. `validation_section()` receives only the values it reads, and
the native-comparison runner removes only its dead local assignment; its parser
continues to accept `--build-root` because existing Make targets pass it.

The existing Change Records keep their factual original evidence and gain the
canonical section headings plus explicit status boundaries. This record covers
the four new PR rows and their workflow repair; no Framework or MRTS change is
needed.

## Changed files

- scripts/generate_repository_organization_inventory.py
- tests/test_repository_organization_inventory.py
- ci/checks/documentation/check-bilingual-docs.py
- scripts/generate_compiler_guides.py
- ci/runtime/lifecycle/run-native-case-comparison.py
- seven existing English/German `CR-20260727-sonar-*` Change Record pairs that
  required canonical headings
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

Focused commands use the Parent `.venv` Python with
`PYTHONDONTWRITEBYTECODE=1` and `PYTHONNOUSERSITE=1`:

- rtk proxy env ... `<Parent .venv python>` -B -m unittest -v tests.test_repository_organization_inventory tests.test_bilingual_docs tests.test_compiler_guides tests.test_runtime_env_snapshot_contract
- rtk proxy env ... `<Parent .venv python>` -B ci/checks/documentation/check-bilingual-docs.py
- rtk proxy git diff --check

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused inventory, bilingual-documentation, and compiler-guide modules | passed: 38 tests. |
| Focused native-comparison reduced-context test | passed: `test_native_summary_and_mismatch_helpers_keep_outputs_with_reduced_context_parameters`. |
| Combined runtime-environment module | blocked_environment: one otherwise unrelated test could not find the deliberately uninitialized `modules/ModSecurity-test-Framework/ci/lib/common.sh`; the direct native-comparison test passed. |
| Full bilingual documentation checker | blocked_environment: 20 existing missing Framework-gitlink link targets; it emitted no missing Change Record section for any repaired pair. |
| `git diff --check` | passed: no whitespace error. |
| Published remediation commit `b09588c63b21be2e62fe374b15f63980e6d6293d` | passed: its local branch, `origin` branch, and PR #128 head were observed equal; all visible GitHub PR checks passed. |
| SonarQube Cloud analysis for published remediation commit `b09588c63b21be2e62fe374b15f63980e6d6293d` | passed: Quality Gate passed with 0 New issues, 0 Security Hotspots, and 0.0% Duplication on New Code; the PR issue query returned 0 unresolved rows. |

## Security impact

The focused assessment found no validated security finding. The regular
expression scanner processes repository text, so preserving bounded matching
and the existing regression corpus matters; the replacement neither expands a
trust boundary nor changes a sink. The remaining edits remove dead or unused
code and repair documentation structure only. No security control, scanner,
Quality Gate, suppression, authentication, path guard, connector, or runtime
behavior is weakened.

## Runtime evidence

No connector, host, protocol, or production runtime behavior changed or is
claimed. The tests exercise source and documentation contracts only; they are
not runtime evidence.

## Known limitations

The Parent task worktree deliberately has no initialized Framework Gitlink, so
the complete documentation checker and one unrelated runtime-environment test
cannot complete locally. The published remediation commit listed above has
hosted PR evidence; that historical evidence does not replace fresh checks for
any later candidate head or for Parent `master`.

## Remaining risks

Splitting the variable matcher could accidentally omit an edge form. The
focused inventory regression suite, including an assignment-overlap case,
reduces that risk, and the published remediation commit received the hosted PR
checks and Sonar analysis listed above. Any later candidate head remains
subject to its own exact-head verification.

## Checks not run and rationale

- The full `make quick-check` and Framework-dependent aggregate checks are not
  run locally because the uninitialized Framework Gitlink already blocks their
  shared documentation prerequisite.
- Connector builds, runtime smokes, protocol matrices, Framework checks, and
  MRTS checks are not applicable: no connector/runtime implementation or
  cross-repository content changed.
- No connector/runtime workflow, later-head PR result, or Parent-`master`
  result is claimed here. The observed hosted results apply only to the
  published remediation commit identified above.

## Final diff and review status

The pre-commit local diff review found only the listed Parent source, test, and
traceability changes, with no whitespace error. Its "uncommitted" state is a
historical snapshot: the remediation commit
`b09588c63b21be2e62fe374b15f63980e6d6293d` was subsequently published on
`agent/sonar-1125-20260727`, and the local, `origin`, and GitHub PR #128 heads
were observed equal at that point. The GitHub PR checks and SonarQube Cloud
result then passed as recorded above. This record does not claim a later
documentation-only candidate head, a master merge, or Parent-`master` checks;
each requires separately observed exact-head evidence.
