# Change Record: CR-20261022-pr410-ci-fixture-drift

**Language:** English | [Deutsch](CR-20261022-pr410-ci-fixture-drift.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261022-pr410-ci-fixture-drift |
| Date (UTC) | 2026-10-22 |
| Base revision | `afaf6305bd55646073c3b40632b52fc4e5edf714` |

## Motivation and problem statement

The current #410 head failed `scaffold-lint` because its extracted native
callback fixture did not model `request_partial_observed`. Both HAProxy
structure jobs also failed because the fake libModSecurity API used by the I10
caller tests did not declare or implement `msc_get_request_body_length` after
the Common runtime began reading retained request-body length. These were test
fixture drifts at base revision
`afaf6305bd55646073c3b40632b52fc4e5edf714`, not product-runtime failures.

## Acceptance criteria

- The native-result fixture compiles the current callback and proves that a
  partial request append remains sticky across later successful and empty
  appends.
- The HAProxy I10 fake API models transaction-local retained request-body
  length, bounded partial retention, append failure, and reset for a new
  transaction.
- Focused tests and the complete `check-i10-haproxy-callers` mutation matrix
  pass without changing product source or weakening a check.

## Implementation decision and rationale

The callback preamble now contains the same partial marker used by the product
transaction. Assertions cover the marker's initial, partial, sticky and empty-
append states. The fake libModSecurity transaction stores retained bytes and
exposes them through the current C API. Each direct/SPOP caller fixture runs a
self-check before its existing caller/mutation assertions. This tests the
meaning of the API instead of adding a compile-only constant stub.

## Changed files

- `tests/test_native_result_event_protocol.py`
- `tests/test_haproxy_i10_binding_callers.py`
- `reports/audits/change-records/CR-20261022-pr410-ci-fixture-drift.md`
- `reports/audits/change-records/CR-20261022-pr410-ci-fixture-drift.de.md`

## Commands executed

- `rtk /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m unittest -v tests.test_native_result_event_protocol tests.test_haproxy_i10_binding_callers` — exit `0`; 26 tests passed in 187.792 seconds.
- `rtk make PYTHON=/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python check-i10-haproxy-callers` — exit `0`; 20 tests passed in 251.011 seconds.
- `rtk git diff --check` — exit `0`.
- `rtk make check-bilingual-docs` — exit `2`; the isolated Git worktree has
  no populated Framework submodule, so the repository-wide checker reported
  only pre-existing missing `modules/ModSecurity-test-Framework/...` targets.
- `rtk make check-doc-links` — exit `2` for the same absent Framework
  submodule; no failure referenced either new Change Record.
- `rtk --version`, `rtk which rtk`, and `rtk gain` — RTK `1.0.1` at `/root/.local/bin/rtk`; all commands and validation used the required proxy.

## Security impact

No production trust boundary changes. The tests strengthen fail-closed body
accounting by rejecting constant retained-length behavior, retained bytes after
a failed append, loss of a partial limit, and failure to reset a new
transaction. No validation, isolation, logging or Quality Gate control is
disabled.

## Runtime evidence

No new host runtime claim. These checks compile and execute extracted current C
callbacks and HAProxy direct/SPOP caller fixtures with a semantically accurate
fake native API. Existing host evidence remains revision-bound to its recorded
executions.

## Known limitations

The change repairs only the two confirmed CI fixture drifts. It does not alter
Common or connector product behavior and cannot by itself qualify a hosted
runtime lifecycle.

## Remaining risks

Current-head GitHub and Sonar results must be read after normal delivery to the
#410 branch. Any independent #410 Quality Gate findings remain separate from
these two compilation failures.

## Checks not run and rationale

No full connector matrix or private host run was repeated because the change is
limited to compile/execution fixtures and changes no shipped runtime source.
Repository-wide tests were not substituted for the two focused suites and the
complete affected I10 caller target. The repository-wide bilingual and link
checks could not complete in this isolated worktree because its Framework
submodule is not populated; their diagnostics did not identify either changed
test or Change Record.

## Final diff and review status

The scoped diff contains two test files plus this bilingual Change Record. Both
focused validations and `git diff --check` pass. Review found no product,
generator, matrix, connector implementation or unrelated file change. Normal
commit/push and exact-head CI readback are pending; no merge or master change is
claimed.
