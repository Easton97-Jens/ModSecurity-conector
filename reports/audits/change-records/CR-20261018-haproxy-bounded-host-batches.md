# Change Record: CR-20261018-haproxy-bounded-host-batches

**Language:** English | [Deutsch](CR-20261018-haproxy-bounded-host-batches.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-bounded-host-batches |
| Date (UTC) | 2026-10-18 |
| Base revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation and problem statement

Independent HAProxy cases repeatedly pay the private controller setup cost. Reuse one unchanged private namespace for a bounded sequence of fresh existing capture drivers, while keeping every original ID, process lifetime and measurement separate.

## Acceptance criteria

Prepare at most six cases from one route per queue. Preserve original JSON, oracles and payload bytes. Hash-bind every input, record explicit runtime path/port relocation diffs, and reject mutable or unreviewed input. Wait each real driver, retain its exit unchanged, and stop before another case on process/descriptor/socket leaks, timeout, missing/failed cleanup or an output/runtime budget violation. A completed batch and controller exit 0 must never award lifecycle PASS.

## Implementation decision and rationale

Add `i12_batch.py` as a HAProxy-only coordinator. Native and SPOP fixture copies relocate only the known Python drivers, from `/task` and `/mnt/fixtures` to case subdirectories, with distinct complete port blocks. Companion uses its existing `--root` and dynamic ports without source modification. Every case starts fresh driver/host/agent processes. Process PID/starttime, coordinator descriptors and actual kernel socket tables are compared before/after; TCP TIME_WAIT is retained as the documented non-live-owner exception and unique ports avoid reuse delays. Existing driver cleanup receipts remain separate from HTTP/native qualification. HOME is inherited unchanged; per-case TMPDIR and XDG directories separate transient/cache output. Actual TCP TIME_WAIT rows are retained separately in each before/after snapshot. A failed /proc identity read leaves starttime null and still waits the actual child before stopping. The unchanged controller remains responsible for admission, capability drop, namespace supervision and aggregate memory/process budgets.

## Changed files

New `connectors/haproxy/harness/i12_batch.py`, `tests/test_haproxy_i12_batch.py`, and this EN/DE Change Record pair. No existing driver, controller, product, shared capture, central matrix, Framework or MRTS file is changed by this work.

## Commands executed

`rtk proxy <run>/test-env/bin/python -m pytest -q tests/test_haproxy_i12_batch.py`: 22 tests passed under CPython 3.14.7, exit 0. Tests include real harmless child exits, a bounded sleeping process, an actual loopback listener, actual descriptor changes, timeout/reaping, output-budget failure, and queue/source tampering. These component processes are not HAProxy host runs. Exact wrapped argv/cwd/times/output hashes: `<run>/commands/haproxy-batch-components-v6-20261018.json`. Three preparations exited 0: `<run>/commands/haproxy-batch-pilot-prepare-{native,spop,companion}-v2-20261018.json`. `<run>` is `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015`. The native, SPOP and companion pilot sources are respectively `native/original-fixtures-v7`, `spop/source-fixtures-v4` and `companion/source-fixtures-v5`.

## Security impact

No production security behavior changes. Sealed queues bind the exact coordinator, source fixtures, drivers and relocation receipts; executable argv is derived from the admitted route/member rather than accepted as arbitrary shell text. Physical paths reject traversal, symlinks and foreign owners. The runtime requires the original nonroot controller admission and matching actual namespace identities. A cleanup defect prevents further case execution. The final artifact binding remains a separate Root-reviewed controller input.

## Runtime evidence

Three two-case pilot candidates exist under `<run>/batches/20261018-pilot-v2`. `root-review.json` and the three `*-relocations.diff` files contain the exact proposed argv, hashes, changes and bounds. Root reviewed and sealed only the SPOP candidate, recording `spop-root-approval.json` and the exact `spop-root-spec.json` (SHA-256 `e471578a2db9e3bbfe4f52d9ee6bf1a2038aada7c929f2d0519b6fa60c5b650e`). The coordinator SHA-256 is `2e2f10191bd8729dbc5beed1ee345663d7eafd87557159b7b77a3b06fd220ce9`. Native and companion candidate directories remain unsealed.

Root executed SPOP pilot `attempt-1792320861376221286`: two fresh SPOP cases, each driver exit 0, with main ACK statuses 200 and 403, corresponding backend request counts 1 and 0, and healthy neighbors. The batch completed both cases without cleanup errors; controller exit 0, no timeout, no surviving namespace PIDs and no outside mount leaks. Raw evidence remains under `<run>/isolation/attempt-1792320861376221286`, including `controller-result.json`, `data/batch-result.json` and each case’s client/frame/backend/native files. These two SPOP cases are not separate native or companion runs. Main-client timestamps are missing from this snapshot, preventing independent lifecycle association; measurement repair and fresh execution remain required. No lifecycle PASS is claimed. This worker started no HAProxy host or agent.

## Known limitations

Cases share one actual namespace admission, not one HTTP transaction or engine instance. Qualification must retain this relationship explicitly and use each case’s separate real process identities and raw files. The existing native single-case observer needs an independently reviewed optional data-directory adaptation before consuming nested batch output. A kernel TCP TIME_WAIT entry is not treated as a living listener/process leak.

## Remaining risks

Native/companion private-host pilots, repaired SPOP client timestamps with fresh execution, complete artifact/SDK and loaded-image bindings, all original oracle comparisons, lifecycle review and final CI/Sonar remain required. The SPOP pilot above demonstrates capture execution and cleanup only; no measured batching speedup or host completeness is claimed. Full source review confirms that the existing candidate already writes `/task/isolation-admission.json`; v2 preserves that original receipt and additionally checks immutable `/opt/controller/admission.json`, actual capabilities/NoNewPrivs and separation from outside namespaces. Earlier review uncertainty about a missing receipt is not an actual runtime defect. V1 remains retained and unexecuted.

## Checks not run and rationale

This worker ran no private HAProxy host, CI or server Sonar analysis. Root separately approved, sealed and executed the SPOP pilot described above. Native and companion pilot sealing/execution remain deferred. Root owns Git delivery.

## Final diff and review status

The owned new module, tests and Change Record pair are prepared. Component tests passed; Root reviewed the relocation diffs and approved/sealed/executed only the SPOP pilot. Native and companion candidates remain deferred and unsealed. The coordinator is frozen at the SHA-256 above. Earlier structural documentation checks did not establish German content completeness; the retained German scaffold has now been replaced with a complete companion and all 12 sections were manually checked against the English facts. No merge, push, new PR or lifecycle acceptance result is asserted.
