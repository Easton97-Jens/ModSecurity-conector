# Change Record: Parent CI NGINX HTTP-500 literal deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-ci-nginx-http500-literal-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-nginx-http500-literal-deduplication` |
| Date (UTC) | `2026-07-29` |
| Base revision | `fda62539b6f0a710865707e3003b73ed4469f20e` |
| Source revision assessed | Local task patch against the stated base revision. |
| Boundary | Parent `ci` source listed below, one direct Parent test, this EN/DE pair, and paired indexes only. No `.github`, `scripts`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch action. |
| SonarQube Cloud linkage | Targets the current `python:S1192` literal findings `AZ7PU4lam6NRVhQ0A9r2` and `AZ7PU4lam6NRVhQ0A9r3` for `"htdocs/index.html"` and `"Permission denied"`; no scanner control or issue status is changed. |

## Motivation and problem statement

The NGINX MRTS HTTP-500 cluster report used the same two fixed error-log
literals in error classification, representative-excerpt selection, a
permission-probe path, and report evidence text. SonarQube Cloud reports the
repeated source literals as `python:S1192`; those usages sit beside
classification and evidence-path behavior that must remain unchanged.

## Implementation decision and rationale

`DOCROOT_INDEX_PATH` owns the fixed relative `htdocs/index.html` path and
`PERMISSION_DENIED_TEXT` owns the exact case-sensitive NGINX log token. All
selected consumers use those constants without changing conditions, ordering,
or output text.

`ERROR_PERMISSION_DENIED` intentionally remains separate: it is a lower-case
diagnostic phrase with distinct semantics from the case-sensitive log marker.
The refactor does not change verified-run-ID validation, evidence input
selection, safe-root setup, output writes, or the existing permission-probe
stat behavior.

## Acceptance criteria

- Index-file, directory, critical, and generic-failure classifications retain
  their previous precedence and exact literals.
- Representative excerpts retain final-run date filtering, selection order,
  and 600-character truncation.
- `Path / DOCROOT_INDEX_PATH` remains the same relative
  `htdocs`/`index.html` target in the permission probe.
- The exact future PR head must show zero new SonarQube Cloud issues and
  `0.0%` New-Code duplication without changing scanner policy or controls.

## Changed files

- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `tests/test_nginx_mrts_http500_cluster_analysis.py`
- this English/German Change Record pair and its indexes

## Commands executed

| Command or control | Result |
| --- | --- |
| Focused NGINX HTTP-500 cluster-analysis test suite | passed: 3 tests covering classification precedence, ordinary-file negative control, final-run date filtering, excerpt truncation, and permission-probe path components. |
| Selected-file `py_compile` with task-owned bytecode cache | passed. |
| `git diff --check` | passed. |
| Independent final source and test security-diff reviews | passed: no plausible diff-induced security candidate. |
| `make check-bilingual-docs` | `blocked_external_dependency`: the checker reported only pre-existing missing Framework-submodule link targets and did not report a changed Change Record or index error. |

## Security impact

The generator receives CI evidence rows and error-log paths, then writes
generated evidence reports through existing safe-root controls. The constants
are source-authored fixed data, not external inputs. The existing
`validate_verified_run_id()` check, `add_safe_roots()` setup, and
`write_text_file()` output path control are untouched. No new filesystem,
network, subprocess, deserialization, or authorization path is introduced.

## Runtime evidence

No connector runtime, NGINX/MRTS execution, networked preparation, or report
generator `main()` execution ran. The focused test uses a private temporary
filesystem and does not write repository reports. Hosted GitHub Actions,
SonarQube Cloud, review, approval, merge, and master verification are not yet
observed or claimed.

## Known limitations

The isolated worktree lacks Framework-submodule targets referenced by existing
repository documentation, so the repository-wide documentation check may be
externally blocked. This record does not claim that the wider Parent `ci/`
backlog is exhausted.

## Remaining risks

The report generator retains its pre-existing assumptions about evidence-row
and case metadata provenance. This literal-only change does not validate a
full connector runtime, a hosted Quality Gate result, or resulting-master
state.

## Checks not run and rationale

- No connector runtime, report-generator `main()`, or networked preparation
  ran because the refactor owns fixed source literals and the focused test
  exercises the affected behavior without generated runtime evidence.
- Hosted GitHub Actions, SonarQube Cloud, review, approval, merge, and master
  checks have not yet run for a PR head because no PR has been created.

## Delivery status

Before verification, the exact PR head must be reconciled with master and
receive fresh hosted checks and SonarQube Cloud results. No direct master
change or merge is authorized or implied.

## Final diff and review status

The local source/test diff passed focused tests, selected compilation,
whitespace validation, and independent source/test security-diff review with
no plausible diff-induced candidate. The final exact PR-head hosted
verification remains pending.
