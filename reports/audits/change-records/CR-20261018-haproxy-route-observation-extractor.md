# Change Record: CR-20261018-haproxy-route-observation-extractor

**Language:** English | [Deutsch](CR-20261018-haproxy-route-observation-extractor.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-route-observation-extractor |
| Date (UTC) | 2026-10-18 |
| Base revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation and problem statement

The retained SPOP and response-companion captures need a source-bound observation envelope for independent Root review. A request ACK cannot qualify response processing, and source predictions cannot replace physical client/native measurements.

## Acceptance criteria

Preserve all 35 fields of the existing `reviewed_packet` API. Require explicit attempt, case data root, spec, build receipt, fixture, route and original case identity. Missing or ambiguous observations remain null with reasons. Every outcome and approval field remains pending. Historical raw artifacts and fixtures remain unchanged.

## Implementation decision and rationale

The extractor reuses current capture descriptor admission, the native transition helper, the bounded SPOP decoder, MRC1 framing and the existing measurement role schema. Controller/spec/admission hashes bind the execution. Sealed Root binding ledgers resolve namespace images to physical external storage; no namespace path is opened locally. Build provenance and physical image hashes must agree. Batch queue hashes and actual member receipts bind each case to its own data directory.

## Changed files

The v4 correction decodes physical SPOP backend `header_hex` and `body_hex` rows, retaining their original `neighbor`, `wall_ns` and raw record. The recorded header excludes the CRLFCRLF delimiter; embedded delimiters, invalid request/header syntax, ambiguous lengths, transfer coding, body-length mismatch and oversized hex are rejected. Unknown or corrupt rows leave the exact backend count and correlation unknown. A measured zero additionally requires backend readiness, a joined producer and one independently captured healthy neighbor. Existing companion backend shapes remain supported. Path counts alone do not establish per-client correlation.

Current host-input provenance can bind the reviewed three-binary completion seal directly. The observer requires the exact Direct, Agent and Companion inventory, the exact source revision, all four immutable image hashes including the separately pinned native engine, and the controller-verified artifact ledger. The earlier build-receipt format remains supported for retained runs.

The native Direct observer additionally requires the controller-hashed spec and admission receipt. It resolves the namespace-only Direct binary, SDK, source provenance, fixture contract and launch entry point through the exact artifact and fixture ledgers, then checks all provenance images against their source, sealed copy and completion seal. Namespace paths remain separate from physical paths; a substituted spec, fixture, binary, SDK, ledger or provenance file is rejected.

- `connectors/haproxy/harness/i12_native_cases.py`
- `connectors/haproxy/harness/i12_native_observe.py`
- `connectors/haproxy/harness/i12_route_observe.py`
- `tests/test_haproxy_i12_native_cases.py`
- `tests/test_haproxy_i12_route_observe.py`
- `reports/audits/change-records/CR-20261018-haproxy-route-observation-extractor.md`
- `reports/audits/change-records/CR-20261018-haproxy-route-observation-extractor.de.md`

## Commands executed

```sh
rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_route_observe
```

Nineteen focused tests cover stored schemas, incomplete/corrupt evidence, sibling cases, client payload/UUID/endpoint/time conflicts, sealed images, batch roots, actual process receipts and request-authorization finish. Stored extraction receipts preserve exact arguments, exits and raw hashes under `R2/route-observer-20261018`.

For v4, the declared Python 3.14.7 environment ran:

```sh
rtk proxy env PYTHONNOUSERSITE=1 /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m pytest -q tests/test_haproxy_i12_route_observe.py
```

All 24 tests and 20 subtests passed, including literal retained pilot backend rows, valid bodies, malformed boundaries/headers/lengths/metadata, unknown rows, missing positive controls and incomplete JSONL. The v4 stored extraction and validation receipts are retained under `R2/route-observer-20261018/v4`; this correction adds no host run or qualification.

The current follow-up ran the two affected modules together and then the full HAProxy-I12 harness group. The focused result was 48 tests and 29 subtests passed; the broader result was 194 tests and 106 subtests passed. The added controls reject a same-content Direct binary at another path, a changed SDK, wrong namespace, changed seal/provenance image and incomplete image inventory. Redirect header comparison accepts HTTP optional whitespace while continuing to reject missing, wrong or duplicate `Location` fields.

## Security impact

This is a bounded defensive acceptance tool. It reads admitted physical files and writes a fresh exclusive output. It adds no host traffic, broad scan, authorization change, exception or suppression. A changed source seal or conflicting namespace binding is rejected.

## Runtime evidence

Seven packets were extracted from retained case executions in six isolation attempts: Safe, Strict, three earlier SPOP cases and two fresh SPOP pilot members sharing one controller. Extraction starts no host. Every packet retains all 35 fields, pending Root review, null oracle evaluation and null outcome. Existing Safe/Strict captures lack client start times; original SPOP client rows lack both interval endpoints. Those missing timestamps remain unknown.

## Known limitations

UUID/PID/scope/path/payload joins retain only partial association when client intervals are missing. MRC1 capability hashes connect actual claims, handoffs and host callbacks separately. Global unmatched native rows, host callbacks and physical sink rows remain visible. Actual finite P2 completion and request finalization remain known raw facts; their streaming EOS argument stays explicitly null. SPOP sample completion does not synthesize streaming EOS or response phases. Common cleanup does not count as a second native free.

## Remaining risks

First-cause classification, terminal event semantics, exact transport/write attribution and original-oracle evaluation remain independent Root work. Native audit never substitutes for physical Common events. Unknown framework/MRTS identities remain null. Future timestamp fields are supported only when newly captured; older packets are not repaired by inference.

## Checks not run and rationale

This harness follow-up started no new host, product build or scanner run. It was applied to a separately retained current host attempt; that attempt and its independent Root qualification are recorded in the current acceptance evidence rather than treated as a property of the extractor.

## Final diff and review status

Only HAProxy fixture/observation harnesses, their tests and this paired change record are changed. The previous six frozen Sonar files are untouched. Delivery and publication remain separate steps.
