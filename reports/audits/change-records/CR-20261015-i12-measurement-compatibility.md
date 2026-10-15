# Change Record: CR-20261015-i12-measurement-compatibility

**Language:** English | [Deutsch](CR-20261015-i12-measurement-compatibility.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-measurement-compatibility |
| Date (UTC) | 2026-10-15 |
| Base revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

Owner: Parent PR #410.

## Motivation and problem statement

PR #412 scaffold job116469396655 fails against the distribution SDK: the deterministic constructor fixture declares a const ID where its selected header declares a mutable ID, and the APR probe calls an unavailable intervention cleanup helper. Subsequent compatibility controls also demonstrate that the current Common Runtime requires the approved newer SDK. The lint job must prepare that SDK through the existing shared component producer instead of selecting an unrelated distribution library.

## Acceptance criteria

Preserve strict compiler warnings and all existing negative controls. Select the fixture signature by compiling against the actual header. Free the probe's caller-owned intervention strings through the portable C allocation API. Keep the original host qualifier unchanged except for admitting its existing direct SDK MIME producer. Qualify original configuration parser selections in a separate scope without inventing HTTP/native lifecycle evidence.

## Implementation decision and rationale

The lint workflow uses `prepare-runtime-components` with target `shared` and consumes that producer's exact environment snapshot. Existing Framework pins remain authoritative. The constructor probes retain their input, compiler argv and diagnostics. The MIME observation admits role `native_api`, while transport evidence remains invalid. `reviewed_configuration_packet` only accepts original `actual_configtest` contracts with independently bound parser/image/config/source/cleanup evidence; it always returns `full_lifecycle_qualified: false`.

## Changed files

The lint workflow, native observer test fixture, independent APR probe, shared lifecycle qualifier and its negative controls. Product source, immutable capture objects/manifest and Framework/MRTS gitlinks remain unchanged.

## Commands executed

All local commands used RTK. Explicit selected SDK3.0.14 observer suite: 33 PASS. Shared oracle/ledger/report suite: 34 PASS. Real APR/native probe: 4 PASS. A synthetic older-header envelope reproduces additional current Runtime incompatibilities and is retained as failure evidence; it is not presented as an older SDK runtime PASS. Hosted provisioning and final exact-head checks remain to be observed after publication.

## Security impact

No warning, test, quality gate, isolation or provenance guard is relaxed. The workflow prepares dependencies in its existing runner-owned external cache. Parser qualification cannot promote any HTTP/body obligation. Unit validator fixtures are synthetic controls and never host evidence.

## Runtime evidence

Run `i12-lighttpd-412-completion-20261015`, directory `shared`, retains the original CI log, header probes, compile/runtime receipts and both successful and failed checks. These measurement controls add no connector lifecycle PASS by themselves.

## Known limitations

Final hosted SDK preparation and current-head Sonar/CI results are pending. The caller-owned string cleanup is bounded to test probes. Production compatibility with older SDK releases is not added.

## Remaining risks

Shared SDK provisioning adds work to lint; terminal hosted results must confirm the runner's dependency environment. A parser PASS is a configuration-layer result only.

## Checks not run and rationale

No local package installation, release, deployment, master integration or other-connector host matrix. The new workflow's network-dependent build is verified by its hosted run after publication.

## Final diff and review status

Scoped source review preserves the original physical observation roles and baseline exports. The lighttpd follow-up consumes these shared fixes by normal merge from #410; no history rewrite is authorized.
