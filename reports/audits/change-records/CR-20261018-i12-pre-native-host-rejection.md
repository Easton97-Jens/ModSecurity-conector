# Change Record: CR-20261018-i12-pre-native-host-rejection

**Language:** English | [Deutsch](CR-20261018-i12-pre-native-host-rejection.de.md)

Dedicated host rejection evidence scope.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-pre-native-host-rejection |
| Date (UTC) | 2026-10-18 |
| Base revision | `2c38d0ff2960a9ff2a76291955e808683febf06e` |

## Motivation and problem statement

The four original Apache malformed-header contracts permit host rejection before connector allocation, with visible400 and logical phase1. A normal35-field native lifecycle packet cannot truthfully describe no native allocation. This change adds a narrowly scoped validator, without altering the original oracle or inventing a native transaction.

## Acceptance criteria

Only invalid_content_length, conflicting_content_length, duplicate_transfer_encoding and content_length_overflow with their exact original mappings/oracles may enter the dedicated scope. Separate Root source approval and physical process/wire/Core/backend/image/config/isolation/native/event-window/cleanup/control evidence are required. full_case_qualified is true only in host_pre_native_rejection; full_lifecycle_qualified remains false. Existing normal35 and configuration checks remain unchanged.

## Implementation decision and rationale

The new reviewed_pre_native_packet reads existing Apache client/process/native-lifecycle-v1/host/backend capture row shapes. It requires a complete native observer sequence, zero main native calls, positive constructor/API controls before and after, an independent zero-event sink window with actual Common JSONL control records joined to observed native allocations, actual400 headers, backend0, a matching Core diagnostic inside the client UTC window, and source/config/rules/image/UID/PID/cleanup bindings. build_ledger dispatches only the explicit execution_kind and keeps full-case and full-lifecycle counts separate. The adjacent typed-absence validator now accepts the actual native identity and exact finish/free counter dictionaries. A physical zero-event claim reads the immutable sink bytes, checks bounded equal main offsets and complete client-window coverage, and joins nonempty before/after Common JSONL control ranges to successful native allocations; flag-only observer receipts are rejected.

## Changed files

ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py; tests/test_i12_lifecycle_ledger.py; ci/evidence/reports/generate-pr382-i12-oracle-reconciliation.py; tests/test_i12_oracle_reconciliation.py. This Change Record pair documents the dedicated pre-native scope. The integrated capture/absence Change Record belongs to the coordinator.

## Commands executed

rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/resume-20261018 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_i12_lifecycle_ledger tests.test_i12_oracle_reconciliation —54 tests passed, exit0. AST comparison against the base confirms normal35/configuration constants and existing validator functions are unchanged. rtk proxy git diff --check passed; the coordinator owns the final integrated diff review. rtk proxy python3 ci/tools/new-change-record.py check passed (structure only). The coordinator mounted the exact Framework99a7985c1be92a2297b1b59208f64df6768f2cbf Gitlink into a private read-only namespace and reran make check-bilingual-docs and make check-doc-links; both passed, exit0. The namespace receipt confirms the Gitlink remained unchanged and no mount escaped. The EN/DE pair was manually reviewed for factual parity.

## Security impact

The boundary protects evidence integrity: missing native allocation, observer data, cleanup or Core diagnostics cannot become a passing native lifecycle. Root review, immutable selected contracts and independent revisioned source proofs remain mandatory. No product parser, authentication, isolation, compiler or CI control is weakened.

## Runtime evidence

No host was launched and no runtime PASS or Root approval was created. Read-only baseline verification rejects all four dedicated-scope candidates: invalid_content_length, conflicting_content_length and content_length_overflow returned400 but lack a positive pre-main constructor/API control. duplicate_transfer_encoding returned500 and has main native activity. These are not qualified pre-native passes. Evidence is retained under /var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/resume-20261018/.

## Known limitations

The new scope only qualifies an independently established host-before-native rejection; other behavior retains its original contract and requires the applicable native lifecycle or defect assessment. Core diagnostics currently require the actual Apache timestamp format in UTC. Baseline captures lack the required pre-main positive controls and independent event-window/Core evidence. Physical retests and Root approvals remain integration work.

## Remaining risks

Synthetic positive and negative tests establish validator behavior, not live host semantics. Root must review physical observation provenance and source approval before qualification. No existing500 result is normalized into400.

## Checks not run and rationale

Hosted retests were not run: this worker has no host-launch authorization. Ruff was attempted with the Parent virtual environment but is unavailable (No module named ruff); no package was installed. No Git delivery or Framework/MRTS writes were performed; documentation checks used private read-only bindings only.

## Final diff and review status

Scoped code and tests were reviewed against the original contracts; unrelated pending capture files were preserved. Normal35/configuration validator ASTs are unchanged. All new results remain separate from full host lifecycle credit. No commit, push, PR update or merge was performed by this worker.
