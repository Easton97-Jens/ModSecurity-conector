# Change Record: CR-20261018-traefik-own-scope-ledger

**Language:** English | [Deutsch](CR-20261018-traefik-own-scope-ledger.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-traefik-own-scope-ledger |
| Date (UTC) | 2026-10-18 |
| Base revision | `782f31ed78353b59a0dcd63978638ae5b107f8cf` |

## Motivation and problem statement

Valid configuration and preallocation packets were accepted by the central validators but rejected by the Traefik consumer because it always selected the HTTP lifecycle validator.

## Acceptance criteria

Accept each original contract through its existing central validator. Preserve immutable inventory, native absence and lifecycle counts; reject missing producers and scope substitution.

## Implementation decision and rationale

Original `actual_configtest` contracts use `reviewed_configuration_packet`; explicit `host_preallocation_control` packets use the exact-ID-restricted `reviewed_preallocation_packet`. Other packets retain the existing 35-field validator. Store `fresh_configuration`, `fresh_preallocation` and `fresh_lifecycle` separately. Add per-scope PASS/FAIL counts and `case_qualified_pass`, `case_qualified_fail`, `case_unqualified_ids`; existing lifecycle counters keep their meaning. Historical configuration results are not promoted into current qualification.

## Changed files

`connectors/traefik/harness/i12_ledger.py`, `tests/test_traefik_i12_ledger.py`, and this English/German Change Record pair. No shared generator, production source or frozen inventory changes.

## Commands executed

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_traefik_i12_ledger tests.test_i12_lifecycle_ledger tests.test_i12_traefik_preallocation`: 70 tests passed. The preceding five-control reproducer failed twice on the valid own-scope controls before the fix.

## Security impact

Functional evidence-consumer repair only. Existing independent parser/source/process proofs and exact preallocation ID restrictions remain mandatory. No security scan, capability exemption or validation weakening.

## Runtime evidence

No host execution in this change. Synthetic producer-shaped controls establish consumer behavior only; they do not qualify actual original IDs.

## Known limitations

Preallocation regression inputs use the real frozen selected contract plus a synthetic reviewed effective oracle passed into the consumer API. They do not approve or resolve a real oracle. Runtime packets still require separate Root review.

## Remaining risks

Actual acceptance and exact-head hosted checks remain separate work. No delivery or runtime PASS is claimed by this Change Record.

## Checks not run and rationale

Go/race/vet and host tests were not rerun for this Python consumer-only change; the task owner retains those integrated validation obligations.

## Final diff and review status

Focused diff reviewed for scope and immutable baseline preservation. No Git commit, push, PR merge or hosted gate result performed by this worker.
