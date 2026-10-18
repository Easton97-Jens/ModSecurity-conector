# Change Record: CR-20261018-haproxy-native-sequence-fixtures

**Language:** English | [Deutsch](CR-20261018-haproxy-native-sequence-fixtures.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-native-sequence-fixtures |
| Date (UTC) | 2026-10-18 |
| Base revision | `8582074ce1efc0df330277c1c2514d762f17afab` |

## Motivation and problem statement

Existing single-response fixtures cannot demonstrate three independent transaction lifecycles or reuse of one TLS connection. Prepare original `multiple_sequential_requests` and `keep_alive_requests_if_supported` inputs without changing either selected requirement.

## Acceptance criteria

Preserve original IDs and contract hashes. Prepare separate Allow/Deny/Allow fixtures, record every HTTP response and actual socket identity, reject incomplete or ambiguous framing, and retain independent native allocation/finish/free records. Preparation and component checks must award no host or lifecycle PASS.

## Implementation decision and rationale

Reuse the sealed v7 `allow` capture launcher and its existing observer. A fixture-owned HAProxy `errorfile 403` independently defines denial payload bytes. The sequential variant uses three connections; the keepalive variant sends all three requests through one actual SSLSocket and never reconnects on close/error. The backend uses persistent Content-Length framing and ThreadingHTTPServer. Native association accepts only one actual allocation in each measured request interval; missing calls stay missing and extra cleanup calls remain visible.

## Changed files

New `connectors/haproxy/harness/i12_native_sequences.py`, `tests/test_haproxy_i12_native_sequences.py`, and this EN/DE Change Record pair. No product, shared capture, central matrix, Framework or MRTS changes.

## Commands executed

`rtk proxy <run>/test-env/bin/python -m pytest -q tests/test_haproxy_i12_native_sequences.py`: 10 passed under CPython 3.14.7, exit 0. Exact wrapped argv, cwd, times and output hashes: `<run>/commands/native-sequences-components-v4-20261018.json`. Fixture generation with `--base <run>/native/original-fixtures-v7/allow --plans <run>/native/original-fixtures-v7/original-case-plans.json --output <run>/native/sequence-fixtures-v4` exited 0; exact argv: `<run>/commands/native-sequences-prepare-v4-20261018.json`. Here `<run>` is `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015`. Both fixtures contain six SHA-256-bound regular files, mode 0444, with case directories 0555. Earlier v1 preparation remains historical.

## Security impact

No production behavior changes. The bounded client requires one decimal Content-Length and rejects Transfer-Encoding, duplicate lengths, oversized or incomplete messages. Preparation uses the existing admitted external-output helper. Socket close is not asserted as native EOS or transport reset.

## Runtime evidence

No HAProxy host was started. Two prepared fixtures and 10 component tests provide zero independent host runs and zero lifecycle PASS. `join_native` exposes actual native rows and return counts; it does not replace the existing qualifier or infer missing Finish/Free.

## Known limitations

Actual HAProxy keepalive behavior after a local deny must be measured. A closed connection is retained as a failed execution, not automatically classified as host unsupported or N/A. The existing single-request extractor cannot directly consume the sequence JSON; review each joined request and the original physical sink/host records.

## Remaining risks

Fresh integrated native binaries, private-host execution, physical sink observations, commit/EOS order, descriptor cleanup and independent original-oracle qualification remain required. The deliberate errorfile makes denial bytes deterministic but does not prove the native deny by itself.

## Checks not run and rationale

Private host execution and final CI/Sonar were not run by this bounded fixture task; Root owns host execution and delivery. No new native or transport outcome is claimed.

## Final diff and review status

Only the owned new files were changed. Component validation and sealed fixture hash/mode verification passed; independent Root review, host execution and Git delivery remain pending.
