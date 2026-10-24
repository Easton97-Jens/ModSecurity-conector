# Change Record: CR-20261018-haproxy-spop-sequences-sonar-refactor

**Language:** English | [Deutsch](CR-20261018-haproxy-spop-sequences-sonar-refactor.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-spop-sequences-sonar-refactor |
| Date (UTC) | 2026-10-18 |
| Base revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation and problem statement

Address the 16 assigned Sonar findings in the SPOP source fixtures/host driver and native sequence driver/test without changing route predicates, original oracles, wire representations or frozen fixture artifacts. The input is the retained PR 415 issue report for revision `7ad1d7b1c6d88c7430213d408f1f184f2442314c`.

## Acceptance criteria

Reduce the reported function complexity and repeated literals, remove the unused client parameter and nested conditional, and isolate the single throwing call in the exception test. Prove selected-definition, packet, configuration and observation parity, retain all frozen artifacts, and pass the focused Python 3.14.7 checks. A fresh Sonar readback remains separately required.

## Implementation decision and rationale

Extract endpoint IP/port checks, per-request/evaluator checks, observation status, host preparation/startup, native sequence item capture and allocation association. Centralize the existing fetch expressions, file names and ledger suffix as constants. Preserve comparison order, failure reasons, guards, control values, client request bytes, socket reuse, native allocation intervals and extra-call retention. The exception test constructs its socket before entering the exception assertion. No suppression or gate change is used.

## Changed files

- `connectors/haproxy/harness/i12_spop_cases.py`
- `connectors/haproxy/harness/i12_spop_host.py`
- `connectors/haproxy/harness/i12_native_sequences.py`
- `tests/test_haproxy_i12_native_sequences.py`
- `reports/audits/change-records/CR-20261018-haproxy-spop-sequences-sonar-refactor.md`
- `reports/audits/change-records/CR-20261018-haproxy-spop-sequences-sonar-refactor.de.md`

## Commands executed

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m pytest -q tests/test_haproxy_i12_spop_wire.py tests/test_haproxy_i12_native_sequences.py tests/test_haproxy_i12_spop_samples.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/sonar-spop-sequences-20261018/verify-parity-v3.py
```

Python 3.14.7: 49 tests and 47 subtests passed. The parity script completed 812 equal comparisons: all 94 original definitions, 96 constructed NOTIFY packets, raw HTTP inputs, 68 original configurations, 16 diagnostic configurations, seven actual-evaluator scenarios, four mocked sequence transports and native joins. All 728 SPOP v4 ledger entries and 50 native sequence fixture entries across retained versions were rehashed without error. Scoped `git diff --check` passed.

## Security impact

Existing type, framing, correlation, ACK-integrity, finite-sample, body-limit, isolation and evidence controls are preserved. Metadata failures, orphan/duplicate ACKs, truncated framing and missing/extra native calls retain their actual outcomes. Mocked transports start no hosts. Product, Common, shared captures, central matrices, Framework and MRTS remain unchanged.

## Runtime evidence

External evidence root: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/sonar-spop-sequences-20261018`. `verification-final.json` retains exact argv, exits, interpreter, before/after source hashes and diff hash; `parity-v3.json` retains the 812 equality checks including actual socket close-call counts; `native-frozen-integrity-final.json` records the fresh native fixture hash recheck; `native-frozen-integrity.json` retains the individual native fixture hashes. Before/after source copies, test output, `source-final.diff` and the executable parity procedure are retained. The initial parity-report serializer could not serialize bytes in a returned tuple; its first script is retained, and version 2 fixes only report serialization and uses fresh output directories. No host ran and no lifecycle credit is awarded.

A final source review found an uncommitted refactor regression: closing a non-reused socket inside `drive_item` before raising on surplus left the caller holding its old reference, so `finally` closed it again. The initial parity check tracked only the closed boolean and missed the duplicate call. The corrected driver receives the captured response, assigns the release result in the caller, then validates surplus separately; ownership and the prior exception order are preserved. The new close-call regression fails against the retained initial refactor (exit 1) and passes against the correction. Normal independent, keepalive EOF and surplus-exception paths assert exactly one close. All 812 parity comparisons were rerun with close-call counts included. No host qualification arose from either result.

## Known limitations

The changed executable source files have new source hashes. Existing sealed source copies and every verified fixture file remain untouched; no fixture regeneration was needed. The parity proof compares generated inputs and component observations, and does not establish a real HAProxy or native lifecycle result.

## Remaining risks

Root must run the fresh Sonar analysis/readback and the normal delivery checks. Later host evidence must bind its actual executable snapshot and product revision; these component results must not be transferred as new host runs.

## Checks not run and rationale

No new host, product build, sanitizer campaign, controller admission, Sonar submission or complete CI run was performed by this bounded remediation worker. Root owns those independent checks and Git delivery.

## Final diff and review status

The four assigned files and this EN/DE pair were reviewed against the captured before sources. Focused tests and byte-parity checks passed. Other workers’ changes were preserved. Fresh remote Sonar status and delivery are pending; no Git write was performed.
