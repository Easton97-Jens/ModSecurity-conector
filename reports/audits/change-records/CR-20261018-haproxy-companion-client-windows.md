# Change Record: CR-20261018-haproxy-companion-client-windows

**Language:** English | [Deutsch](CR-20261018-haproxy-companion-client-windows.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-companion-client-windows |
| Date (UTC) | 2026-10-18 |
| Base revision | `f8a1bfa272dfd3ca0953ad8e7ca2dffe5864140d` |

## Motivation and problem statement

Stored companion clients previously recorded only completion `time_ns`; a missing start prevented an unambiguous request window. Connection or send exceptions could leave no client report. Add physical measurements to new captures without manufacturing historical timestamps, associating parallel TLS writes by global order, or awarding lifecycle credit.

## Acceptance criteria

First reproduce the missing start field. Capture child start/completion wall and monotonic clocks, real PID and observed endpoints, plus actual request-send boundaries. Preserve error/cancel bytes and unknown fields. Independently retain exact launched argv, waited exit/signal and parent launch/wait clocks. Keep all 71 original definitions and 82 predictions unchanged in a new sealed v7 snapshot and validate harmless real client components.

## Implementation decision and rationale

New `client-N.json` schema `i12-companion-client-capture-v2` records `started_wall_ns`, `started_monotonic_ns`, `completed_wall_ns`, `completed_monotonic_ns`, `pid`, `connection_local`, `connection_peer`, and request-send start/completion clocks. `time_ns` aliases the newly measured completion wall clock. Endpoint and send fields remain null when not actually reached. Partial response/request bytes and reports are saved on capture exceptions before the same exception propagates; cancellation remains distinct from TLS EOF and native EOS. Existing response/framing comparisons retain their inputs and behavior.

Independent `client-N.process.json` schema `i12-companion-client-process-v1` records exact `argv`, actual `pid`, waited `exit`, `signal`, `reaped`, `timed_out`, `launch_error` and parent launch/wait wall/monotonic clocks. A timed-out child is killed and reaped, with raw stdout/stderr retained. A missing child report stays missing; parent timestamps do not invent a child window. The same process receipt is appended to aggregate commands when returned normally. The independent observer owner received the exact schemas and field names.

Root follow-up review confirmed an ownership regression relative to Python 3.14.7 `subprocess.run`: arbitrary communication exceptions could leave the new explicit `Popen` child running. A real-child control reproduced this for injected parent `KeyboardInterrupt`, `SystemExit` and `RuntimeError`; the negative control itself killed/reaped each survivor afterward. The correction kills, drains, waits and closes owned output pipes before propagating the same original exception. The process receipt records actual waited exit/signal and optional `communication_error`; no missing child timestamps are manufactured. Real `os.waitpid` checks prove the corrected owner already reaped each child. Existing timeout behavior remains covered. This necessary correction creates v7 and preserves v6 unchanged.

## Changed files

- `connectors/haproxy/harness/i12_companion_host.py`
- `tests/test_haproxy_i12_companion_host.py`
- `reports/audits/change-records/CR-20261018-haproxy-companion-client-windows.md`
- `reports/audits/change-records/CR-20261018-haproxy-companion-client-windows.de.md`

## Commands executed

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m pytest -q tests/test_haproxy_i12_companion_host.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion/client-windows-v1/run-component-controls.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion/client-windows-v1/interrupt-cleanup-v1/verify-fixture-parity-v7.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion/prepare-fixtures-v7.py
```

Python 3.14.7: 40 tests and 22 subtests passed, including the prior 39 tests/19 subtests. Before the change the new regression failed with missing `started_wall_ns`; its raw failure is retained. The harmless component procedure measured verified local TLS success (client exit 0), an actual refused connection (exit 1, unknown endpoints/send completion), and an actual SIGTERM wait (signal 15, no invented child report). Mocked controls cover cancel, broken send and timeout/kill/reap. All 1147 parity checks passed: 71 original definitions and all 82 predictions are byte-identical, per-fixture body/MIME/native/source expectations match v5, legacy client fields/raw bytes/transport comparisons match, and untouched producers/guards match the task-start AST. Canonical P3 redirect remains 302.

## Security impact

TLS certificate and hostname verification remain enabled, with explicit fixture OpenSSL configuration. Path/symlink/private-root guards and response/framing predicates are preserved. Endpoints come from the actual socket and are not reconstructed from configured addresses. No product, shared capture, matrix, Framework or MRTS changes and no security scan/gate changes. Local component TLS certificates and private keys are isolated; key files are excluded from the component hash inventory.

## Runtime evidence

External root: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion`. `client-windows-v1/verification.json` retains exact commands, exits, source/diff hashes and frozen identities; `actual-component-controls.json` retains raw component results and per-process receipts; `fixture-parity.json` retains the original 1060 checks; `interrupt-cleanup-v1/fixture-parity-v7.json` retains the final 1147 checks. The follow-up `client-windows-v1/interrupt-cleanup-v1/verification.json` retains the final 40-test result, new source/diff hashes and v7 identities; `real-child-cleanup.json` retains six before/after real-child probes, including explicit control cleanup for the three before-fix survivors. These are client/component measurements: zero HAProxy host or native-engine executions and no lifecycle PASS.

New sealed snapshot: `source-fixtures-v7`; all 88 files have mode `0444` and both directories mode `0555`. Runner SHA-256: `6a30f2e23126ee91483114819b52389ac58906c5c04cecb28c872b8fcfe09c99`; ledger SHA-256: `014ffdb17e3bb3868371ea6a10640af1aab5335408958216511febb1d5cef303`. The v5/v6/v7 ledgers were rehashed. Prior raw captures, v5 and v6 stay unchanged. The first parity script rejected AST differences from pre-existing Sonar refactors of the cases module; it is retained. The second verifies the actual per-fixture function outputs and immutable definition bytes instead. This task did not edit that module.

## Known limitations

A measured interval alone does not prove native ownership, response commit, EOS, rule execution or once-only cleanup. Parallel associations still need independent transaction/handle/socket evidence. A killed child may have no completion report. Historical completion-only data remain incomplete. Of 71 transaction definitions, 49 are capture-ready and 22 retain source/injection gaps; the separate configuration original remains Root-owned.

## Remaining risks

Root must review and admit the new source snapshot before any HAProxy run. Actual independent host write/context correlation, native events, transport and full lifecycle qualification remain separate work. No canonical P3 redirect expectation was retargeted to a product failure status.

## Checks not run and rationale

No HAProxy host, native-engine host, product build, controller `read_spec`, broad/deep security scan, Sonar submission or complete CI execution was performed by this measurement worker. Root owns host scheduling, qualification and Git delivery.

## Final diff and review status

Only the assigned companion runner/tests and this EN/DE pair changed. Focused tests, fixture parity and source-bound controls passed; original source predictions remain unchanged. Root review, admission, real host results and delivery are pending. No Git write was performed.
