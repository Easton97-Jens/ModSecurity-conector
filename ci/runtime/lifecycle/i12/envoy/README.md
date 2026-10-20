# Envoy I12 host evidence

**Language:** English | [Deutsch](README.de.md)

This Envoy-only test extension reuses the existing `envoy` capture variant and
common native observer. The [task report](../../../../../reports/testing/i12-envoy-host-evidence-20261015.md)
is **PARTIAL**: 284 original IDs are preserved. Eight newly approved packets
raise the current lifecycle PASS to eleven; 114 original oracles remain open.
The central baseline stays unchanged. Synthetic host scenarios do not
automatically qualify original IDs.

All 125 original oracles have individual source reviews. The 33 new fixture-bound
source proposals remain separate from canonical resolution and host acceptance.

## Current acceptance state

| Route | Lifecycle PASS / original IDs | Open original oracles |
| --- | ---: | ---: |
| `envoy-ext-proc` | 5 / 117 | 46 |
| `envoy-ext-authz-request` | 4 / 94 | 36 |
| `envoy-ext-authz-response-companion` | 2 / 73 | 32 |

Of 273 IDs without full lifecycle acceptance, 8 are configuration-only PASS
and 265 are unqualified. The 86 real host measurements include 37 retakes under
33 exact original IDs. The eight new individual approvals are:

- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-proc::NEED-client-response-bytes`
- `I12::envoy-ext-proc::NEED-client-exit-signal`
- `I12::envoy-ext-authz-request::NEED-complete-sample`
- `I12::envoy-ext-authz-request::NEED-request-multiple-chunks`
- `I12::envoy-ext-authz-request::NEED-client-response-bytes`
- `I12::envoy-ext-authz-response-companion::NEED-allow`

The two additional request-authorization qualifications independently bind the host and client contracts. The physical Envoy trace identifies worker 285 / CID1 / SID6459190741822168578 and host fragments 64+31=95 followed by EOS, then the Authorization Check at line 275. The engine receives one complete 95-byte native sample and one EOS; multiple client writes do not imply multiple native callbacks. The response-byte qualification independently checks raw HTTP framing and client entity bytes. Process remote gRPC status remains unknown and is not counted as success.

## Producers

| Producer | Evidence boundary |
| --- | --- |
| `reconcile.py` | Revalidates original oracle sources and physical ledger; preserves all 284 exact Envoy IDs |
| `prepare_native.py` | Git-free current source copy, unchanged capture overlays, native/CGo build, Go/race/vet and observer controls |
| `source_inventory.py` | Reconstructs every build input from the hash-bound Git archive and explicit capture additions |
| `evidence_io.py` | Bounds physical reads to approved owned paths; rejects symlinks, private configuration and changes during reads |
| `validate_oracles.py` | Verifies all 125 original-ID reviews and physical references; preserves canonical results |
| `host_scenarios.py` | Sealed independent fixtures, TLS inputs, binary/source binding and private controller; does not start hosts |
| `fault_scenarios.py` | Sealed Response-EOS fault fixture with a separate test proxy; real run `fault-host-v1` remains runner77/controller1/client1, unqualified and without new PASS |
| `bind_originals.py` | Seals fresh exact-original-ID retakes of reviewed fixtures with all inputs inside the current private run |
| `run_host.py` | Bounded launches using the existing nonroot controller; exit codes remain observations |
| `review_runs.py` | Physical hashes, loaded images, client/backend bytes, native/host callbacks, cleanup and transport facts |
| `transport.py` | Distinguishes actual local HTTP/2 reset from explicit remote gRPC success |
| `qualify_originals.py` | Stages selected original cases; individual approval requires exact fixture equality, fresh reproduction of all 35 proof fields and the shared validator |
| `write_report.py` | Generates only this task's EN/DE report and exact-ID JSON; does not update shared generators or ledger |

A fresh companion NEED-allow retake binds a separate supplemental source review before execution. Its early backend request-line capture proves exactly one target and one neighbor request; old lower-bound receipts remain unchanged.

## Validation

Run from the Parent worktree, with the repository-owned Python interpreter:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -s ci/runtime/lifecycle/i12/envoy -p 'test_*.py' -v
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/runtime/lifecycle/i12/capture_sources.py verify
```

The current complete Envoy suite has 188 PASS and 0 skips. Receipt: `ci/final-envoy-controls-188-base-a622-v2.json`. Focused fault controls have 16 PASS; separate Go test-proxy controls have 10 PASS. These controls do not automatically qualify the host run.

Each producer exposes `--help`. Native preparation requires a fresh registered
external run root, the current checkout, the existing offline module cache,
the selected real SDK and patched Go toolchain. `--validate-existing` retains
failed setup evidence and reruns checks without silently rebuilding binaries.
Use a short, private, physical temporary path for UDS tests.

Host preparation additionally requires the explicitly hash-bound retained v5
controller/template inputs and the matching native build receipt. These are
external prerequisites, not bundled binaries or permission to install tools.
The controller removes capabilities, enters private namespaces and admits
UID/GID 65534 with NoNewPrivs before running capture programs. The Envoy copy
pins its positively identified PID namespace until after cleanup to prevent
inode reuse from misattributing another run's processes. All original gates
remain active; failed ownership checks remain errors.


The native and host evidence source remains exclusively
`f27eb59b53beff6f65384fc2e5037881a3052c01`. The exact Base head
`a62296fb57263f9be18c6ac879e36e0ab2a9935c` was merged into this branch in
`dfb1a07a863530a53c0006ee204319453d66a2ad`. The retained baseline and physical sources were revalidated with
the current central validators; this Envoy task modified no shared validator.
The retained runtime receipts do not qualify the merged Base product state;
a fresh current-Base capture remains required. Scoped documentation evidence:
`ci/docs-postmerge-a622-v2.json`.

The real ext_proc fault probe `fault-host-v1` drops only the empty Response-EOS callback and performs an actual half-close. The engine API and Envoy trace unambiguously correlated to the target stream report gRPC status14. The client receives an HTTP200 prefix with 96 body bytes in 64+32, but no zero chunk. Runner77/controller1/client1 remain unqualified; new PASS: 0. The target records P1–P3 and P4=0, a `runtime_finish` attempt with result0 and one logging/free/cleanup each. The healthy neighbor has P1–P4/Finish once each; no survivors or mount leaks remain. Proxy wire status remains unobserved. Missing status is not interpreted as successful completion.

## Claim limits

`max_request_bytes` is Envoy's host buffer limit. Authorization samples,
native limits and technical gRPC errors require separate observations.
Started/aborted backend requests are counted independently of completed receipts.
Multiple client writes alone do not prove multiple native body callbacks.
Complete HTTP framing, TCP reset, gRPC status, EOS, Finish and Free are separate
facts. Missing remote gRPC status is never successful completion.

Read the task report and exact-ID JSON for remaining gaps. Do not change the
shared manifest, original catalog, other connectors or product sources through
this extension. Retain raw artifacts externally; version only reviewed metadata.
