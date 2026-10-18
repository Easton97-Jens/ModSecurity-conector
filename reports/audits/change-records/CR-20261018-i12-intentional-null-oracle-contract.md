# Change Record: CR-20261018-i12-intentional-null-oracle-contract

**Language:** English | [Deutsch](CR-20261018-i12-intentional-null-oracle-contract.de.md)

Source-only contract review; no host qualification.
## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-intentional-null-oracle-contract |
| Date (UTC) | 2026-10-18 |
| Base revision | `a2d545ac7ec4abce23595e1c033f094104617201` |

## Motivation and problem statement

The original canonical `phase2_over_limit` has `visible_status: null` and no unresolved reason. The previous review rejected this defined, host/config-dependent contract as missing expected data.

## Acceptance criteria

Accept only unchanged, explicitly present original `visible_status: null` with separate Root interpretation and hash/revision-bound independent primary proof. Reject unknown originals, other missing fields, changed expectations and proof substitution; award no execution or host qualification.

## Implementation decision and rationale

Add `intentional_null_fields.visible_status` to the existing review API. Its primary proof must join the same independent path/hash/kind/revision and remain disjoint from implementation bytes. The complete effective/original canonical digests must match; corrections and replacement expectations cannot use this declaration. `native_result`, `phase` and the status key remain mandatory. Existing original ID/contract hashes stay unchanged.

## Changed files

- `ci/evidence/reports/generate-pr382-i12-oracle-reconciliation.py`
- `tests/test_i12_oracle_reconciliation.py`
- `ci/runtime/lifecycle/i12/README.md`
- `ci/runtime/lifecycle/i12/README.de.md`
- `reports/audits/change-records/CR-20261018-i12-intentional-null-oracle-contract.md`
- `reports/audits/change-records/CR-20261018-i12-intentional-null-oracle-contract.de.md`

## Commands executed

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m pytest -q tests/test_i12_oracle_reconciliation.py tests/test_i12_lifecycle_ledger.py
rtk proxy make check-bilingual-docs PYTHON=/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python
rtk proxy make check-doc-links PYTHON=/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework
rtk proxy git diff --check
```

Python 3.14.7: 41 tests and 76 subtests passed. Bilingual documentation and link checks passed; whitespace check passed. The genuine original-row before probe rejected visible_status as expected. Exact commands, exits, original row/primary YAML hashes and output hashes are retained in the external task evidence.

## Security impact

The change prevents an intentional unspecified value from being confused with missing evidence. It does not permit missing observations, remove any host measurement, accept an unresolved original or treat implementation/probe output as independent primary proof.

## Runtime evidence

No host was launched. The source-only review still returns `full_lifecycle_qualified=false` and no retest. The real original selection hash is `98f5423f9cf2a019997a8c751429c43956d3211488452b1e323b6099d10f847d`; its Framework primary YAML hash is `83e1bc8c6292e90f01acc84617f05113d2dbe625c88d7c4278f5327a6c121cfd`. The eight new test methods include this pinned canonical contract plus negative controls.

## Known limitations

This exception covers only an already defined visible_status null. It does not resolve any of the original 596 unknown-oracle records or choose a client status for a new fixture. No historical ledger, reconciliation or central matrix was regenerated.

## Remaining risks

Root must still assess the primary source interpretation and separately review every fresh actual host packet. The declaration itself cannot establish physical client status, native lifecycle or complete acceptance.

## Checks not run and rationale

Host/build tests, CI and Sonar were not run for this bounded source-contract change. Existing owning lifecycle/oracle tests and full documentation checks were run; Root owns subsequent integration/delivery verification.

## Final diff and review status

Scope reviewed: existing oracle API, regression tests, paired API README and this paired Change Record only. No product, capture-object, Framework/MRTS gitlink or historical evidence edits. No commit, push or host execution by this worker.
