# Envoy I12 host evidence

**Language:** English | [Deutsch](README.de.md)

This Envoy-only test extension reuses the existing `envoy` capture variant and
common native observer. The [task report](../../../../../reports/testing/i12-envoy-host-evidence-20261015.md)
is **PARTIAL**: 284 original IDs are preserved. Three newly approved packets
raise the current lifecycle PASS to six; 119 original oracles remain open.
The central baseline stays unchanged. Synthetic host scenarios do not
automatically qualify original IDs.

All 125 original oracles have individual source reviews. The 33 new fixture-bound
source proposals remain separate from canonical resolution and host acceptance.

## Producers

| Producer | Evidence boundary |
| --- | --- |
| `reconcile.py` | Revalidates original oracle sources and physical ledger; preserves all 284 exact Envoy IDs |
| `prepare_native.py` | Git-free current source copy, unchanged capture overlays, native/CGo build, Go/race/vet and observer controls |
| `source_inventory.py` | Reconstructs every build input from the hash-bound Git archive and explicit capture additions |
| `validate_oracles.py` | Verifies all 125 original-ID reviews and physical references; preserves canonical results |
| `host_scenarios.py` | Sealed independent fixtures, TLS inputs, binary/source binding and private controller; does not start hosts |
| `bind_originals.py` | Seals fresh exact-original-ID retakes of reviewed fixtures with all inputs inside the current private run |
| `run_host.py` | Bounded launches using the existing nonroot controller; exit codes remain observations |
| `review_runs.py` | Physical hashes, loaded images, client/backend bytes, native/host callbacks, cleanup and transport facts |
| `transport.py` | Distinguishes actual local HTTP/2 reset from explicit remote gRPC success |
| `qualify_originals.py` | Stages four selected original cases; individual approval requires exact fixture equality, fresh reproduction of all 35 proof fields and the shared validator |
| `write_report.py` | Generates only this task's EN/DE report and exact-ID JSON; does not update shared generators or ledger |

## Validation

Run from the Parent worktree, with the repository-owned Python interpreter:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -s ci/runtime/lifecycle/i12/envoy -p 'test_*.py' -v
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/runtime/lifecycle/i12/capture_sources.py verify
```

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
