# Change Record: CR-20261018-haproxy-spop-client-window

**Language:** English | [Deutsch](CR-20261018-haproxy-spop-client-window.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-spop-client-window |
| Date (UTC) | 2026-10-18 |
| Base revision | `f8a1bfa272dfd3ca0953ad8e7ca2dffe5864140d` |

## Motivation and problem statement

Original SPOP client rows lacked actual start/completion timestamps, preventing independent allocation/client-window joins. The parent client command also lacked its actual waited child PID. Existing diagnostic stamps and historical runs must remain unchanged.

## Acceptance criteria

Record actual wall/monotonic request-send and completion windows, including errors, actual IP socket endpoints or explicit missing reasons, and actual client PID. Record the parent Popen PID, waited exit/signal, timeout and reaping without inference. Preserve original requests/responses/frames, admission and expected predicates; retain all94original JSON/oracles byte-identically and all729historical v4files.

## Implementation decision and rationale

Only the original client path gains measurements. Completion is sampled in finally; failed send completion remains null with a reason. Endpoint queries use the real socket. A narrow Popen/wait boundary keeps the exact argv and40second timeout; timeout kills and waits before propagation, and other wait exceptions also kill/wait. No product, Common capture, generator, Framework or oracle changes.

## Changed files

`connectors/haproxy/harness/i12_spop_host.py`, new `tests/test_haproxy_i12_spop_client_window.py`, and this EN/DE Change Record pair. Other concurrent work remains outside this change.

## Commands executed

All shell commands used RTK. Failing-before spop-window-before compiled/executed the old client with a harmless real TCP peer and failed at missing started_wall_ns. `rtk proxy python3 -m unittest -v tests.test_haproxy_i12_spop_client_window tests.test_haproxy_i12_spop_wire` passed45tests:8measurement tests and37existing wire/predicate tests. Positive/error TCP controls observe actual intervals/endpoints; independent children exercise0/7/SIGTERM/timeout-kill-wait/launch failure. Exact argv/cwd/exits/log hashes are retained under `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/product-spop/spop-window-*.json`. Final `rtk proxy make check-bilingual-docs check-doc-links` and `rtk proxy git diff --check` passed. Exact source comparison also confirms capture_response, original_rules, original_configuration, evaluate_original, prepare_host_inputs, original_client and response_measurement remain byte-identical against the base.

## Security impact

Bounded defensive evidence correction. No validation, isolation, redaction or expected behavior is weakened. Missing data stays explicitly absent; process cleanup is observed through wait. No deep security scan or actual HAProxy host run was performed.

## Runtime evidence

Harmless real TCP and child-process component controls prove only the measurement boundary. No HAProxy, native allocation, lifecycle PASS, backend delivery or original oracle qualification is claimed. Historical rows receive no invented timestamps or PID/exit backfill.

## Known limitations

The original request window starts immediately before its send on an already connected socket; connection establishment before that point is outside this window. Socket endpoint absence is explicit. Diagnostic capture_response stamps remain as previously implemented.

## Remaining risks

Only a fresh admitted host run can join these independent client windows/PIDs to physical native observations. Root owns review, v5fixture sealing, actual host retakes and qualification.

## Checks not run and rationale

No product rebuild is required for this measurement-only Python change. No HAProxy host, Git write, publication, merge, package install or deep scan was performed by this worker. Fixture v5 remains unsealed pending coordinator review; old v4 stays sealed and immutable.

## Final diff and review status

The external v5preparation comparison retains729files, changes only106host measurement copies plus sourcebinding/index/ledger metadata, and keeps106selected JSON files (including94original effective oracles) byte-identical. Source/diff hashes and final bilingual/link results are retained under spop/client-window; Root controls review, sealing and delivery. No full host claim is made.
