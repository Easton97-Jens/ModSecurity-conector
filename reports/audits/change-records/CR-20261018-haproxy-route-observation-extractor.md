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

- `connectors/haproxy/harness/i12_route_observe.py`
- `tests/test_haproxy_i12_route_observe.py`
- `reports/audits/change-records/CR-20261018-haproxy-route-observation-extractor.md`
- `reports/audits/change-records/CR-20261018-haproxy-route-observation-extractor.de.md`

## Commands executed

```sh
rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_route_observe
```

Nineteen focused tests cover stored schemas, incomplete/corrupt evidence, sibling cases, client payload/UUID/endpoint/time conflicts, sealed images, batch roots, actual process receipts and request-authorization finish. Stored extraction receipts preserve exact arguments, exits and raw hashes under `R2/route-observer-20261018`.

## Security impact

This is a bounded defensive acceptance tool. It reads admitted physical files and writes a fresh exclusive output. It adds no host traffic, broad scan, authorization change, exception or suppression. A changed source seal or conflicting namespace binding is rejected.

## Runtime evidence

Seven packets were extracted from retained case executions in six isolation attempts: Safe, Strict, three earlier SPOP cases and two fresh SPOP pilot members sharing one controller. Extraction starts no host. Every packet retains all 35 fields, pending Root review, null oracle evaluation and null outcome. Existing Safe/Strict captures lack client start times; original SPOP client rows lack both interval endpoints. Those missing timestamps remain unknown.

## Known limitations

UUID/PID/scope/path/payload joins retain only partial association when client intervals are missing. MRC1 capability hashes connect actual claims, handoffs and host callbacks separately. Global unmatched native rows, host callbacks and physical sink rows remain visible. Actual finite P2 completion and request finalization remain known raw facts; their streaming EOS argument stays explicitly null. SPOP sample completion does not synthesize streaming EOS or response phases. Common cleanup does not count as a second native free.

## Remaining risks

First-cause classification, terminal event semantics, exact transport/write attribution and original-oracle evaluation remain independent Root work. Native audit never substitutes for physical Common events. Unknown framework/MRTS identities remain null. Future timestamp fields are supported only when newly captured; older packets are not repaired by inference.

## Checks not run and rationale

No host run, new product build, scanner run or Root qualification was performed. The assignment covers extraction and regression checks against existing captures. Product failures and acceptance remain with their assigned owners.

## Final diff and review status

Only the new HAProxy extractor, its tests and this paired change record are changed. The previous six frozen Sonar files are untouched by this task. Root review/publication remains pending; no Git mutation is included.
