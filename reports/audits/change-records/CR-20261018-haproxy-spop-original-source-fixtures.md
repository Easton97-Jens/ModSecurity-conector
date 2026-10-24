# Change Record: CR-20261018-haproxy-spop-original-source-fixtures

**Language:** English | [Deutsch](CR-20261018-haproxy-spop-original-source-fixtures.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-spop-original-source-fixtures |
| Date (UTC) | 2026-10-18 |
| Base revision | `8582074ce1efc0df330277c1c2514d762f17afab` |

## Motivation and problem statement

Prepare source-bound execution definitions for the 94 frozen `haproxy-spop-request` original IDs: 91 transaction cases and three configuration cases. Preserve every original contract and distinguish concrete source expectations from future host observations. Correct the malformed NOTIFY control without transferring a historical harness failure to a new original ID.

## Acceptance criteria

Validate all 94 original memberships and hashes; preserve unresolved native or injection expectations; record actual SPOP tags, body sample length, `req.body_size`, HTTP version and frame identities; separate main traffic from a healthy neighbor. Unit tests must reject truncated frames, inconsistent metadata, unframed HTTP/2 inspection claims and incomplete response framing. Real host acceptance remains a separate requirement.

## Implementation decision and rationale

The source module pins each original contract and preserves its original oracle. Canonical rules and YAML rules remain source-bound. Explicit native request limits use `Reject` or `ProcessPartial`. The driver records an independent waited client, correlated NOTIFY/ACK identities, raw wire bytes, backend requests, process snapshots and shutdown receipts. A diagnostic ID cannot acquire original membership through an incoming legacy `case_id`.

Sample faults apply only to the main request. Held-transaction TTL fixtures use a separate clean frontend in the same host and agent for the neighbor; no response-companion qualification follows from this request profile. Constructed packets are labelled component fixtures and never host observations.

Prehost review found a harness oracle defect in `source-fixtures-v1`: expected intervention phase 1 was incorrectly treated as a phase ceiling. The actual public `begin_atomic_request` caller only skips request-body finalization after an actual disruptive P1 result. Version 2 changes 17 selected definitions, including benign transaction-ID and sequence cases, while preserving all original contract hashes. Version 1 remains immutable and is classified `HARNESS_DEFECT`; no host result transfers. Added controls distinguish P1 Allow from P1 Deny/Redirect and bind this behavior to the primary caller source.

Further independent prehost review found that version 2 accepted plausible orphan ACKs, ignored excess/duplicate ACKs and action types, accepted integer/string IP metadata contrary to native `read_typed_ip_to_buffer`, and sealed files without sealing directories. Version 3 rejects these observations, requires matching connection/stream/frame and valid directions/envelopes/types/scopes, checks finite inspection claims against actual samples, emits real packed IPv4/IPv6 tags `6`/`7`, and seals the entire physical tree. Negative tests exercise the actual evaluator with correct HTTP/backend facts plus an orphan ACK and require failure. All 94 selected original definitions and oracles remain identical to version 2.

Version 4 adds the explicitly enabled native audit/debug observation configuration missing from version 3: `SecAuditEngine On`, `SecAuditLogType Serial`, `SecAuditLogParts ABFHZ`, `/task/native-audit.log`, `/task/native-debug.log` and `SecDebugLogLevel 9`. Canonical rules and native body limits remain intact. Audit parts `C` and `E` are excluded. The regression checks configuration only, fails against version 3 and passes against version 4; it does not fabricate or claim an audit file. Native physical file creation and rule/body/MIME observations still require Root-owned fresh host runs.

## Changed files

- `connectors/haproxy/harness/i12_spop_cases.py`
- `connectors/haproxy/harness/i12_spop_host.py`
- `connectors/haproxy/harness/i12_spop_wire.py`
- `tests/test_haproxy_i12_spop_wire.py`
- `tests/test_haproxy_i12_spop_samples.py`
- `reports/audits/change-records/CR-20261018-haproxy-spop-original-source-fixtures.md`
- `reports/audits/change-records/CR-20261018-haproxy-spop-original-source-fixtures.de.md`

## Commands executed

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m unittest discover -s tests -p test_haproxy_i12_spop_wire.py -v
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/spop/prepare-source-fixtures-v4.py
```

Python 3.14.7: 37 focused tests passed. The new P1 Allow regression fails against the immutable version 1 module (expected exit 1) and passes against version 2. Source preparation produced 729 immutable files; all 728 ledger entries were independently rehashed without error in both versions. All 94 original memberships validated. Version 4 ledger SHA-256: `1cd048e2890d4a1faf9a3079c9149486adb8ece26471c7f2f091190d615858c8`. All 107 directories have mode `0555`; all 729 regular files have mode `0444`. The two new wire regressions fail against the immutable version 2 modules (expected exit 1); the corrected suite passes (exit 0). The audit configuration regression also fails against version 3 (expected exit 1) and passes against version 4. Scoped `git diff --check` passed. The persisted test receipt is `spop/fixture-tests-v4.json` under the external acceptance run root. The Change Record archive check, `make check-bilingual-docs` and `make check-doc-links` passed through RTK using the same Python 3.14.7 environment.

The legacy native admission mutation test was also corrected after the explicit HTTP-version guard changed the old mutant's meaning. Its generated C driver temporarily provides `Content-Length: 0` to isolate missing version presence, then restores unframed input before the HTTP/2 control. Three independent C17 builds now return the asserted values: current source `0`, unframed-HTTP/2 fallback mutant `4`, and missing-version-presence mutant `3`. No existing duplicate-length, Transfer-Encoding, size or typed-value controls were removed. The focused unittest failed before this test correction (exit 1) and passed afterward (exit 0) under Python 3.14.7. Receipts and before/after source copies are under `spop/sample-mutation-review-20261018`. This does not change the frozen version 4 host harness or product code.

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m unittest discover -s tests -p test_haproxy_i12_spop_samples.py -v
```

## Security impact

No product, Common, shared capture, central matrix, Framework or MRTS source changes. Finite authorization samples never imply unbounded streaming inspection. HTTP/2 or unknown/chunked framing does not receive an inspection claim from an ACK. Actual client framing and clean-neighbor observations remain required; faults cannot silently contaminate the neighbor.

## Runtime evidence

External root: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015`. Current source definitions and component packets: `spop/source-fixtures-v4`; versions 1, 2 and 3 remain unchanged. Correction audits: `spop/source-fixtures-v1-harness-defect-eos.json`, `spop/source-fixtures-v2-harness-defects.json` and `spop/source-fixtures-v3-observation-gap.json`. Root reported rejection of the original version 2 binding before host start because its directories were writable, then observed absence of a native audit file in its separately admitted version 2 allow probe. These are not a full lifecycle qualification. This worker launched no private host, claims no successful controller `read_spec`, and produces no lifecycle PASS. Source-preparation receipts and configuration tests remain separate from physical native events.

## Known limitations

68 transaction definitions are capture-ready; 23 retain explicit measured-injection or source gaps. The three configuration originals require the actual agent configuration/native-rules admission driver. Native body-limit Reject ACK/client mapping and finite-frame first-cause fields remain unresolved where an independent oracle is absent. Physical sink failures, actual pointer/allocation/finish faults, ordered first causes, cancel/reset/timeout and postcommit scenarios still require their real mechanisms.

## Remaining risks

Fresh admitted runs must verify the generated HAProxy configuration, typed samples, real response bytes, native request scope, physical sink events and exactly-once cleanup. Source predictions and unit tests cannot replace those measurements. Parent orchestration owns qualification against the 35-field measurement contract.

## Checks not run and rationale

Private HAProxy/agent builds and hosts, controller admission, sanitizer/mutation runs for product code, SonarQube and complete CI were not run by this bounded source-preparation task. Parent owns those separate executions and delivery. No Git write or host launch was performed.

## Final diff and review status

The four owned SPOP files and this EN/DE pair were reviewed for source/evidence separation. Other workers' native and companion changes remain untouched. Delivery, independent runtime review and full original-ID qualification remain outstanding.
