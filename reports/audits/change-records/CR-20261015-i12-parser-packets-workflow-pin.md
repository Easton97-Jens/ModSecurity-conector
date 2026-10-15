# Change Record: CR-20261015-i12-parser-packets-workflow-pin

**Language:** English | [Deutsch](CR-20261015-i12-parser-packets-workflow-pin.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-parser-packets-workflow-pin |
| Date (UTC) | 2026-10-15 |
| Base revision | `850879e82ea729f274cb383507b05938df06027a` |

## Motivation and problem statement

Original configuration-test contracts need their existing parser packet path in the current ledger; HTTP-only lifecycle rules cannot describe parser controls. Two HAProxy workflow assertions additionally expect a superseded upload-artifact pin.

## Acceptance criteria

Qualify configuration controls separately, require independently reviewed physical parser evidence, preserve original IDs/contracts/history, and correct only stale test expectations to the already deployed upstream pin. Do not award host lifecycle PASS from validator tests.

## Implementation decision and rationale

The current I12 acceptance ledger now dispatches original `actual_configtest`
contracts to the existing `configuration_parser` packet qualifier. The published
packet API and its `configuration_control` / `full_case_qualified` result remain
in use. Host HTTP packets still require their original 35 observations.

Parser qualification requires Root review of the exact original ID and route,
revision-bound source/configuration/rules inputs, actual invoked host and native
module bytes, a separate physical parser-process receipt, physical stdout and
stderr, cleanup and isolation receipts, and a distinct versioned independent
expectation source. The process receipt must agree with the packet's exact argv,
cwd, waited exit, signal, image digest and run/input identities. Controller exits
and self-referencing receipts cannot stand in for parser measurements.

The three original mandatory observations are exposed without changing the
selected contract: parser execution maps to `parser_process`; source/host/module/
effective-config identity maps to `invocation_identity` and
`source_config_binding`; expected acceptance/rejection maps to the independently
reviewed effective oracle and its digest. A parser PASS has
`full_lifecycle_qualified=false`, occupies `current_configuration_packet`, and
contributes only to the separate current configuration count. Historical rows,
original IDs and original expectations remain unchanged.

Expected acceptance requires normal exit 0; expected rejection requires the
original exact exit 1. Exit 77 does not become a successful rejection. A measured
mismatch can be retained as FAIL, whereas a contradictory PASS claim is rejected.
For the original missing-rules contract, no file digest is invented: `rules_sha256`
is null and `rules_absence_sha256` binds a physical `lstat`/ENOENT receipt with the
exact attempted absolute path, no observed symlink components, and the matching
process/run identity. Existing-rules cases retain physical rules-file binding.

Verification: use the exact receipts under `qualifier-config/` for the recorded
Python 3.14.7 pytest run, baseline regression failures, immutable 1,484-ID/source
selection checks, file digests and whitespace check. These validator controls
are synthetic and award no HAProxy parser or lifecycle PASS by themselves.

## Changed files

`ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py`, `tests/test_i12_lifecycle_ledger.py`, `tests/test_haproxy_evidence_workflow_contract.py`, and this EN/DE Change Record pair. No workflow, security lock, product or shared packet API change.

## Commands executed

Actual CPython 3.14.7 parser/ledger pytest: 33 tests and 57 subtests passed, exit 0. Exact command: `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m pytest -q tests/test_i12_lifecycle_ledger.py tests/test_i12_oracle_reconciliation.py`. Receipt: `qualifier-config/integrated-after.json`; source invariants, baseline failures and output hashes are retained alongside it. Workflow tests: 12 passed; exact command/exit and upstream tag bytes are in `workflow-pin/after-receipts.json`. The canonical scaffold was created with `rtk proxy python3 ci/tools/new-change-record.py create --name i12-parser-packets-workflow-pin --base-revision 850879e82ea729f274cb383507b05938df06027a --date 2026-10-15`.

## Security impact

Corrected the stale expected `actions/upload-artifact` pin in the HAProxy evidence
workflow contract tests from v7.0.1 to v7.0.2, commit
`cf430e030ddbb5b0abf93d22962f4752f3646cd9`. The official GitHub API endpoint
`https://api.github.com/repos/actions/upload-artifact/git/ref/tags/v7.0.2`
independently confirms that the upstream tag points directly to this commit.
The checked-in security-tools lock and existing workflow already agree on this
exact version and SHA. No workflow, lock, upload boundary or assertion was relaxed.

The two stale-pin tests failed before the correction. The focused Python 3.14.7
pytest run then passed all 12 tests. Exact commands, process exits, upstream
response bytes and source/output hashes are retained under `workflow-pin/`.

## Runtime evidence

Validator regression controls are synthetic. No fresh HAProxy parser host PASS or full lifecycle PASS is awarded here. Current configuration packets count only in the configuration column with `full_lifecycle_qualified=false`; HTTP packets retain their original 35-observation gate.

## Known limitations

Parser inputs require a separate physical process receipt and independent expectation source. Controller-only exits, self-references and exit 77 cannot establish successful rejection. Missing-rule evidence records physical absence rather than an invented file digest.

## Remaining risks

Integrated runtime qualification still depends on actual rebuilt host/module images and independently measured parser or transport behavior. Historical rows and immutable 1,484-ID/source selections remain preserved; the focused tests do not establish all connector runtime readiness.

## Checks not run and rationale

No fresh private host acceptance, final-head hosted CI or server Sonar result is claimed by these parser/pin tests. Those require their own observed execution and qualification.

## Final diff and review status

Only the three listed source/test files and this record pair are in scope. Source-bound parser checks, original-selection invariants and workflow-pin regressions pass at their reported layers; final runtime acceptance and Git delivery remain separate. No gate, assertion or original requirement is weakened.
