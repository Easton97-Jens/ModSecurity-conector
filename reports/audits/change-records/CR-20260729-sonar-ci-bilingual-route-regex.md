# Change Record: Parent CI bounded bilingual design-route matcher for SonarQube Cloud S8786

**Language:** English | [Deutsch](CR-20260729-sonar-ci-bilingual-route-regex.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-bilingual-route-regex` |
| Date (UTC) | `2026-07-29` |
| Base revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` |
| Boundary | Parent `ci/checks/documentation/check-bilingual-docs.py`, its focused Parent test, this English/German Change Record pair, and paired indexes only. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Current `python:S8786` issue `AZ9gR-Icl6PyoRTCCRIu` at `ci/checks/documentation/check-bilingual-docs.py:143`. |

## Motivation and problem statement

The route-table matcher for the Common design notes combined adjacent whitespace
wildcards with a lazy non-delimiter capture. A malformed contributor-supplied
Markdown row beginning with a cell delimiter and a long run of spaces caused
heavy regex backtracking before the checker could reject the row. SonarQube
Cloud reports that expression as `python:S8786`.

## Acceptance criteria

- A malformed route row without its closing cell delimiter is rejected in a
  bounded time without a backtracking-heavy expression.
- Padded and unpadded connector cells still produce the same normalized route
  keys through the existing `connector.strip()` operation.
- The current English and German Common design notes retain their valid-route
  result and existing diagnostics.
- A future exact PR head reports zero new SonarQube Cloud issues, zero new
  duplicated lines, and `0.0%` New-Code duplication without weakening a rule,
  Quality Gate, exclusion, suppression, or validation control.

## Implementation decision and rationale

The matcher now consumes the first table cell with a delimiter-disjoint
`[^|]+` capture. Whitespace is intentionally retained in that capture because
the immediately existing `connector.strip()` already owns normalization. This
removes the overlapping whitespace/capture choices while preserving route
keys, route values, row ordering, and error messages. The focused regression
checks both valid padding forms and a 1,024-space malformed row.

## Changed files

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-bilingual-route-regex.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-bilingual-route-regex.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Isolated pre-fix Python regex probe on `|` + 1,000 spaces + `x` | reproduced: the previous matcher took `0.96952` seconds while the delimiter-disjoint candidate took `0.000033` seconds. |
| `python -B -m unittest tests.test_bilingual_docs.BilingualDocumentationCheckerTests.test_common_design_note_current_contract_passes_for_both_languages tests.test_bilingual_docs.BilingualDocumentationCheckerTests.test_common_design_route_matcher_keeps_routes_and_rejects_malformed_spacing_quickly tests.test_bilingual_docs.BilingualDocumentationCheckerTests.test_common_design_note_rejects_scaffolded_status_and_current_sidecar_route` | passed: valid English/German notes, padded/unpadded route keys, malformed-row rejection, and existing negative diagnostics. |
| `python -B -m unittest tests.test_bilingual_docs` | passed: 22 tests. |
| Counterfactual matcher probe on the 1,024-space regression input | reproduced: the previous expression took `1.064121` seconds and exceeds the regression budget of `0.25` seconds. |
| Post-fix matcher probe on the same 1,000-space malformed row | passed: no match in `0.000039` seconds. |
| `make check-bilingual-docs` | blocked_external_dependency: the isolated worktree has no Framework checkout, so the checker reports only pre-existing missing Framework-link targets outside this task's boundary. |
| `make check-doc-links` | blocked_external_dependency: it reports the same pre-existing absent Framework-link targets only. |
| `make lint` | blocked_external_dependency after its CI shell-syntax and Python-compilation portions: its next no-CRS test imports the absent Framework checker. |
| Direct `check_change_record_pair(...)` control for this record | passed: no heading, identity, or language-pair errors. |
| `git diff --check` | passed: no whitespace errors in the final scoped diff. |
| Focused security source/diff review | passed: the base resource-exhaustion path is closed by the delimiter-disjoint matcher; no reportable current-diff candidate. |

## Security impact

The relevant input is a documentation line supplied in a Parent change; the
affected sink is CI CPU time while validating that line. The invariant is that
an invalid row must be rejected without an ambiguity that permits excessive
backtracking, while valid selected-route rows retain their normalized keys.
The new delimiter-disjoint expression closes that performance path and adds a
same-boundary malformed-input regression plus a valid padded/unpadded control.
No file path, network, subprocess, authentication, secret, or report-output
behavior changes.

## Runtime evidence

No connector runtime, networked component preparation, package installation,
or host matrix is claimed. The changed boundary is the in-process bilingual
documentation checker and is exercised directly by its focused unit module.

## Known limitations

The regression uses a deterministic 1,024-space malformed row rather than an
unbounded corpus. It proves the reported overlapping-quantifier shape is not
used by the route matcher, but it is not a general performance certification
for every regular expression in the checker.

During the broad Make checks, a readable external `FRAMEWORK_ROOT` satisfied
the Make prerequisite, but the isolated worktree itself intentionally has no
Framework Gitlink checkout. The parent link checker therefore reports missing
worktree-relative Framework targets, and a no-CRS test later imports the
missing worktree-relative Framework checker. Those failures are outside this
matcher change.

## Remaining risks

The exact hosted PR head must still receive a fresh SonarQube Cloud analysis
showing the selected issue absent and zero New-Code issues/duplication. The
isolated worktree cannot execute the repository-wide documentation checker
until the read-only Framework checkout is available at its expected Gitlink.

## Checks not run and rationale

- No connector build, runtime matrix, package download, or networked component
  preparation was run: none is reached by this documentation-regex change.
- No Framework, MRTS, Gitlink, `.github/`, `scripts/`, or unrelated Parent
  source was changed or tested because it is outside the selected remediation
  boundary.
- Hosted SonarQube Cloud, GitHub Actions, review, and merge evidence require
  the eventual exact PR head and are not inferred locally.

## Final diff and review status

The scoped local diff consists only of the matcher, its focused regression,
and this bilingual traceability pair/indexes. Whitespace, Change-Record
structure, and focused security/diff reviews passed. No commit, push, pull
request, hosted check, review, or merge is claimed. Exact-head delivery
evidence remains required before this task can reach `verified_pr`.
