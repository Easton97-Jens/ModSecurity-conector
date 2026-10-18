# Change Record: CR-20261018-i12-traefik-expected-absence

**Language:** English | [Deutsch](CR-20261018-i12-traefik-expected-absence.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-traefik-expected-absence |
| Date (UTC) | 2026-10-18 |
| Base revision | `08ed2bd4a37223ba58dc0a46c9aa9787c6f42839` |

## Motivation and problem statement

Some Traefik parser and abnormal transport cases have a source-defined absence of a native decision, native phase or complete HTTP status. The existing reconciliation rejected every null, preventing an independently reviewed absence contract from being expressed without inventing a value.

## Acceptance criteria

Accept only separately Root-reviewed typed absence for the exact original Traefik ID and contract hashes. Preserve literal nulls, original expectations and physical evidence requirements. Reject omitted values, stale/cross-route approvals, unsupported absence types, missing primary sources and altered source bytes. Source resolution must never qualify a host execution.

## Implementation decision and rationale

An optional expected_absence review binds the selected requirement and original oracle canonical hashes. Its field set must equal the literal null expectation fields. Each field needs a reason plus independently bound official host and protocol sources; measurements alone cannot define the expected result. Existing complete expectations use the existing path unchanged.

## Changed files

The central oracle reconciliation script, tests/test_i12_traefik_absence_oracles.py, and this EN/DE Change Record pair. No central matrix, original inventory, product, Framework or MRTS file changes.

## Commands executed

RTK-wrapped Parent-venv unittest execution of the five new absence controls passed. The new tests reproduced the prior rejection before the change; combined existing oracle/ledger regressions passed after it. Receipts remain under the task run checks directory as absence-before/absence-after. Independent read-only review repeated the five controls successfully.

## Security impact

Missing evidence remains missing. Approvals are scoped to the three Traefik routes and immutable original identity; a worker assertion, unrelated proof or observed status cannot authorize a new expectation. No runtime admission or security boundary changes.

## Runtime evidence

No host was started for this source-contract change. full_lifecycle_qualified remains false and no original ID is promoted by these tests or source reviews.

## Known limitations

Hashes authenticate the reviewed sources, not their interpretation. Root must still inspect each actual primary source before issuing an approval; a synthetic regression fixture is not a production oracle.

## Remaining risks

Applicable host lifecycle, client, backend, native observer and cleanup evidence remain separately mandatory under the execution's qualifier contract.

## Checks not run and rationale

Hosted CI and Sonar are pending the integrated published head. Actual Traefik host executions are owned by the acceptance producers and are not claimed here.

## Final diff and review status

Root and independent read-only review found no remaining actionable defect in the bounded change. Targeted tests passed; final integrated checks and published-head gates remain required.
