# Change Record: CR-20261018-i12-haproxy-owned-decision-values

**Language:** English | [Deutsch](CR-20261018-i12-haproxy-owned-decision-values.de.md)

Internal ownership correction; source/native-layer evidence is separate from host acceptance.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-haproxy-owned-decision-values |
| Date (UTC) | 2026-10-18 |
| Base revision | `630be0bcc7158c5c642e47bc1d6956c5b137acb7` |

## Motivation and problem statement

A real Companion P4 Safe host observation reached native Deny403/rule1100301 but failed OUTCOME and closed the client response. Common retains decision reason/intervention-log and redirect/intervention-redirect in separate owned buffers. The HA SPOP bridge incorrectly required pointer identity, so equal valid copied values were rejected before the physical Common event. Strict and redirect decisions cross the same boundary.

## Acceptance criteria

Accept equal bounded text values after actual Common ownership transfer; retain rejection of missing, inconsistent, oversized or unsupported metadata. Copy queued owner data before its source lifetime ends. Preserve native phase/status/rule authority, first error, checked sink failure, OUTCOME-before-RELEASE and once-only cleanup; do not claim host delivery from a source/native seam.

## Implementation decision and rationale

Only copy_spop_bridge_decision changes: keep NULL/shape/status checks, copy the native reason/redirect into bounded task-owned storage, and compare each duplicate field by bounded value rather than pointer identity. No Common source, public layout, wire protocol, configuration, phase policy or original oracle changes. Reader-facing configuration is unchanged, so the Change Record pair documents this internal correction without a README edit.

## Changed files

Product: `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`. Focused tests: `tests/test_haproxy_spop_owned_decision.py` and `tests/haproxy_i10_spop_caller_test.c`. Documentation: this English/German Change Record pair. The new seam extracts unchanged actual Common decision-copy functions and the actual HA bridge helper; it does not replace either with a model.

## Commands executed

All commands used RTK. `rtk proxy python3 -m unittest -v tests.test_haproxy_spop_owned_decision` passed3tests, including6mutants,13malformed controls,128parallel owned copies and ASan/UBSan. `rtk proxy python3 -m unittest -v tests.test_haproxy_native_companion_events tests.test_haproxy_redirect_contract.HAProxyNativeRedirect tests.test_haproxy_spop_event_sink_failures` passed21tests. Owner physical-event and phase/first-cause/reentry tests passed2tests under HAPROXY_I10_BINDING_SANITIZERS=1. Three unchanged transaction-contract functions passed through unittest.FunctionTestCase, including delayed owner lifetime ASan/UBSan and terminal timeout finalizer controls. `rtk proxy make check-haproxy-c17 check-haproxy-htx-overlay` passed. Exact argv/cwd/exits/log hashes and generated C/compiler/binary receipts are under `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/product-spop/owner-deepcopy` and sibling `owner-*.json` receipts. Fresh HAProxy3.2.25 full build, binding selftest and production SPOA build passed (owner-host-build.json). `rtk proxy make check-bilingual-docs check-doc-links` passed. Existing direct backend concurrency/blocked-neighbor, timeout/finalizer and exactly-once cleanup checks compiled and passed under ASan/UBSan (owner-backend-asan.json). The final4test run repeated actual Common ownership/error/mutation checks and physical P3/P4 Safe/Strict owner events with native403, visible403/200 and actual abort flag assertions; all passed.

## Security impact

Bounded defensive correctness repair: equal owned data no longer causes an erroneous failclosed abort. Missing or conflicting duplicate metadata still fails closed; no validation, sink checks, redaction or isolation is weakened. Native input remains owned before queued use. No deep security scan was performed.

## Runtime evidence

The source-bound failing-before test compiles the unchanged product and actual Common copy path, then fails the expected successful HA copy assertion (owner-boundary-before-v2). After the correction the same contract passes. Real SDK3.0.14 native P3/P4 events and canonical P3 redirect1100202 pass at their engine/API layer. Root-owned actual Safe host failure is preserved as a failure, not promoted; post-fix real host retakes remain required.

## Known limitations

Controlled concurrency proves independent local copies and lifetime behavior, not private host parallel transport. Owner P3/P4 tests observe physical sink data and supplied host OUTCOMEs; they do not prove actual frontend delivery. The owner still omits unknown host phase4 mode rather than inventing Safe. No EOS, abort or HTTP success is inferred from an ACK.

## Remaining risks

Actual Safe complete-client delivery, Strict transport abort, companion302 Location and neighboring requests require independent post-fix host acceptance by the coordinator. Full I12 lifecycle eligibility remains separately assessed against every original requirement.

## Checks not run and rationale

No host runtime, package installation, Common modification, Git commit/push/merge, broad/deep security scan or external publication was performed by this worker; coordinator owns delivery and real host retakes. Existing independent sink/phase tests remain the authority for their covered behavior.

## Final diff and review status

Scoped five-file diff reviewed against630be0bcc7158c5c642e47bc1d6956c5b137acb7; independent bounded review requested and remains open at freeze. C17/overlay/build/doc checks passed; exact source and raw artifact hashes are retained externally under owner-deepcopy. No Git action, delivery or full host qualification is claimed.
