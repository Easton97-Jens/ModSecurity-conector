# Change Record: CR-20261009-nginx-upstream-header-reader

**Language:** English | [Deutsch](CR-20261009-nginx-upstream-header-reader.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-upstream-header-reader |
| Date (UTC) | 2026-10-09 |
| Base revision | `c57e6b0a930161e83cb59bf5905a6db00311dc91` |

## Motivation and problem statement

The current Sonar finding `AaEhok3w0iUkTaK5Ajv2` reports `_Handler.handle` cognitive complexity 19 against the unchanged limit 15. The Parent fixture requires a behavior-preserving extraction, not a weakened gate.

## Acceptance criteria

Reduce per-function cognitive complexity without changing publication ordering, initial write/flush failure, suffix failure, timeout or malformed/truncated request behavior. Preserve the Required scope, Framework and MRTS.

## Implementation decision and rationale

Extract only the existing bounded-per-line request-head loop into `read_request_head()`. An absent or rejected head returns `None`; the response method returns before parsing or writing. The 4096-byte per-line limit, EOF behavior and request parsing are unchanged. Publication stays before the unbuffered write; initial failures still clear it. No new total-header limit or parsing policy is introduced.

## Changed files

- `ci/runtime/lifecycle/nginx_sequence_upstream.py`
- `tests/test_nginx_sequence_upstream_barrier.py`
- `reports/audits/change-records/CR-20261009-nginx-upstream-header-reader.md`
- `reports/audits/change-records/CR-20261009-nginx-upstream-header-reader.de.md`

## Commands executed

```sh
rtk run -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_sequence_upstream_barrier
rtk run -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_nginx_sequence_*py' -v
rtk run -- /usr/local/bin/sonar-with-env api get '/api/rules/show?key=python:S3776'
```

The new genuine-handler controls passed before the extraction: 12/12 tests, exit 0. This behavior-preserving refactor therefore has baseline GREEN, not a claimed RED. After extraction the sequence neighbor suite passed 53/53, exit 0. The canonical-wrapper Sonar rule lookup returned API 400, exit 1; rule guidance uses the known cognitive-complexity contract, not a claimed successful server query.

Additional commands ran through RTK: `ci/tools/new-change-record.py check`, in-memory Python compilation and `git diff --check` passed, exit 0. `make check-bilingual-docs` and `make check-doc-links` with the Parent interpreter returned exit 2 because this isolated worktree has an uninitialized Framework submodule and existing repository links cannot resolve; no links were weakened. Integrated-worktree documentation verification remains required. RTK version, gain and executable-path verification passed. The full sequence log is retained under `/var/tmp/codex/ModSecurity-conector/analysis/nginx-r12-race-followup-20261009T172437Z/complexity-tests/sequence-tests.log`.

## Security impact

No guardrail, validation, authorization, timeout, error classification or evidence expectation is weakened. EOF and oversize request lines cannot arm publication. A complete malformed request retains the existing `IndexError` before output; this change does not add a parser capability.

## Runtime evidence

No NGINX runtime is performed by this isolated refactor. Unit results are not runtime or Canonical evidence and do not alter the original R12 status.

## Known limitations

The request reader preserves its existing per-line bound and does not introduce a total byte count or socket deadline. The malformed-complete-request exception is unchanged.

## Remaining risks

Fresh server-side Sonar analysis must confirm the metric on the integrated commit. Any runtime claim requires genuine separately retained Root/nobody observations.

## Checks not run and rationale

No Full97 or protected workflow, native build or fresh server-side Sonar scan is performed in this writer worktree. The coordinator retains ownership of integrated verification and publication.

## Final diff and review status

The diff is restricted to the Parent request-head extraction, two genuine-handler regression controls and this bilingual Change Record. No Git commit, push or integration-worktree write is performed by this worker.
