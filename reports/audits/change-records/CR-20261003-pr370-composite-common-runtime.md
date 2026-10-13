# Change Record: CR-20261003-pr370-composite-common-runtime

**Language:** English | [Deutsch](CR-20261003-pr370-composite-common-runtime.de.md)

Parent successor with NGINX excluded from readiness-B qualification: Common/connector repairs, qualification contracts and scoped observed lifecycle evidence.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261003-pr370-composite-common-runtime |
| Date (UTC) | 2026-10-03 |
| Base revision | `c58de8e534463f56875e6f038380d342fcb1fea4` |
| Integrated master revision | `820b6975495bdf0f90aca67eee86e27a3b7d329b` via merge `490437afa0189ac371742c219e6b9b2ab80383b8` |

## Motivation and problem statement

PR #370's Go composite service selected the direct Envoy ext_proc identity and streaming request mode for buffered authorization requests. Startup or premature P2 completion could fail. The correction also resolves native claim, expiry and cleanup ownership defects and replaces surrogate follow-up receipts with independent request/response observations. The current successor additionally repairs and verifies selected Apache, Envoy, HAProxy and Traefik behaviors and develops fail-closed qualification contracts for both lighttpd profiles. NGINX changes from current master are integrated, but NGINX is excluded from readiness-B qualification and runtime credit.

## Acceptance criteria

Closed composite modes select canonical identities and buffered-request/streaming-response modes. Header-only start defers P2 until explicit EOS while ordinary begin remains compatible. Invalid claims cannot acquire native state. Real body limits return 413 with host-action metadata and allow a same-engine follow-up. Consumed cleanup cannot retry freed state; unresolved cleanup faults admission. Qualification runners preserve host-specific phase, limit, recovery, identity and cleanup observations and report missing independent evidence explicitly. These criteria cover the implemented repairs and contracts; complete G1–G9 acceptance of all nine non-NGINX profiles remains open.

## Implementation decision and rationale

Add `msconnector_runtime_transaction_begin_request_headers()`, accepting only BUFFERED with `body.data == NULL` and `body.size == 0`; require explicit append and finish at EOS. Ordinary begin still processes the complete buffered entity, including an empty entity. Host-413 terminal cleanup logs without inventing EOS or P2.

Classify the pinned engine's rule-ID-free response-body-limit rejection only when the intervention is disruptive in P4, has status 403, has no URL and carries the exact native limit log. Apache records that decision as a terminal body-limit denial before rule-ID extraction instead of converting it to `invalid_engine_response`; every ordinary uncorrelated rule intervention remains invalid and fail-closed.

Select `envoy / ext_authz / envoy-ext-authz` or `traefik / forwardAuth / traefik-forwardauth`. The direct `envoy / ext_proc / envoy-ext-proc` Common engine retains streaming request/response callbacks; the host renderer additionally supports `PROFILE=buffered-admission` with BUFFERED request transport. Validate Go claim/context/deadline before native claim and couple lease lifetime. Distinguish successful close, consumed error and unresolved cleanup; quiesce once, retain entry ownership until terminal cleanup, and propagate cleanup failure to a permanent coordinator fault and failed terminal event. The Envoy harness captures separate bounded owner-only request and response receipts.

## Changed files

The current successor spans these changed-file groups; this record is no longer limited to the earlier Composite subdiff:

- Common runtime API/implementation, phase-contract EN/DE documentation and C companion tests.
- Apache intervention mapping and the shared exact classifier for rule-ID-free native response-limit rejection, plus host qualification harness and tests including response-limit framing, controlled restart, resource and cleanup evidence.
- Envoy Composite/ext_proc product code, Common bridge, coordinator/claim/cleanup tests, receipt observers, real-host qualification harnesses and tests, and EN/DE documentation.
- HAProxy HTX/SPOP product integration, qualification harnesses and tests, including origin-dispatch accounting and bounded receipt reconciliation.
- lighttpd Stock sidecar product/tests and Stock/patched qualification contracts/tests. The current Stock contract passes 27 tests and distinguishes prerequisite blocking (77), runtime or cleanup failure (1), and usage errors (2); no host qualification run is claimed.
- Traefik native middleware and forwardAuth integration, qualification harnesses/tests and EN/DE documentation.
- Connector/Common workflows, regression tests, reader-facing EN/DE documentation, this Change Record pair and the archive EN/DE index.

NGINX changes from current master are integrated; they are not part of this record's readiness-B qualification or runtime evidence. Framework and MRTS source are outside this successor's write scope.

## Commands executed

The actual wrapped commands and effective inputs are retained in the external run `execution.json` files and runners. Payload summaries below omit external compiler/linker paths and run configuration; they are not implied defaults.

~~~sh
rtk proxy go mod verify
rtk proxy go test -mod=readonly -count=1 ./cmd/msconnector-composite ./internal/processor ./internal/composite ./internal/compositeenvoy ./internal/compositetraefik
rtk proxy make -C connectors/envoy build-envoy-ext-proc
rtk proxy env CGO_ENABLED=1 go test -mod=readonly -tags libmodsecurity -count=1 -timeout=3m -json ./...
rtk proxy make -C connectors/envoy test-envoy-ext-proc
rtk proxy make -C connectors/envoy build-envoy-composite
rtk proxy make -C connectors/envoy runtime-smoke-envoy-ext-proc
rtk proxy sh connectors/envoy/harness/run_envoy_composite_matrix.sh
rtk proxy go test -mod=readonly -count=1 ./...
rtk proxy /usr/local/bin/python3.14 -B connectors/traefik/harness/test_composite_config.py
rtk proxy /usr/local/bin/python3.14 -B connectors/traefik/harness/test_composite_harness_paths.py
rtk proxy /bin/sh connectors/traefik/harness/run_traefik_composite_matrix.sh
~~~

Envoy Go commands ran from `connectors/envoy/ext_proc`; the second `go test ./...` ran from `connectors/traefik/composite_middleware`. Normal stages exited 0. The tagged suite had 344 named passes and zero skips. C17 companion compilation with `-Wall -Wextra -Werror -pedantic` and its executable passed. The Traefik harness ran per case; P4 Strict intentionally exited 1 with `NON_PASS`. The native scaffold generator created this pair with the identity values above. Documentation validation is recorded in the final review section.

Later successor validation passed offline in `p370finalregress.20261003a`: the Envoy ext_proc build compiled Common as strict C17, verified Go modules and passed all eight libmodsecurity-tagged packages; the complete Traefik native middleware `go test -mod=readonly -count=1 ./...` passed. The broad Python run passed 368 tests with two expected real-libmodsecurity Stock skips because the SDK environment was absent. A separate Stock run with the exact SDK environment passed all 52 tests without skips. The patched qualification contract passed 18 tests; no trusted qualification executor was available. A historical Stock qualification run passed 21 tests without a host run. The current 27-test contract, including its exit-code distinctions, passed again on 2026-10-07 within a 463-test qualification suite. After merging current master, 202 focused provisioning, Apache, workflow, revision-pin and toolchain tests passed without skips. These are local checks, not hosted successor CI or Sonar results, and historical results do not establish acceptance of the successor revision integrated with current master.

Fresh post-`#402` validation on 2026-10-07 passed 104 focused Envoy qualification tests and 85 focused Apache/native-limit contract tests. Strict Common-helper C17 and Apache C17 builds passed; the current Apache DSO was rebuilt twice from the copied successor source and then exercised in the fresh host campaign below. The current Envoy ext_proc build compiled Common as strict C17 and all eight libmodsecurity-tagged Go packages passed. These checks and campaigns are local exact-worktree evidence; they do not substitute for hosted CI, Sonar, the still-open profile matrices or final published-SHA readback.

## Security impact

Limits fail closed with host-confirmed status. Invalid/expired claims cannot acquire live native state. Unresolved cleanup prevents further admission; consumed errors never retry freed pointers. Independent receipts prevent false follow-up claims. Linux peer credentials and owner-only UDS/file checks remain required. No authentication, tests, warnings, Quality Gate or capability boundary is weakened.

## Runtime evidence

All roots are below `/var/tmp/codex/ModSecurity-conector/runs/`.

| Run | Observed result and boundary |
| --- | --- |
| `p370efix.LLQmPm7g` | Successful native build, 344 tagged passes, C17 companion, direct real-Envoy allow/block/413/P3/Safe traffic and Go composite matrix. `stage_status=0`, `cleanup_ok=true`, no cleanup issues, unchanged source manifest. Earlier attempts remain historical. |
| `p370efu.Ggj72Jct` | Independent bounded request/response receipts: deny403 then allow200 in the same service process; 19 receipt/projection tests passed. Allow-response SHA256 `81f2257e4b0c2040e12b9116ac86279aead533c7a4357fba96dbece040a9288b`, mode `0600`. No full G5/G6 claim. |
| `p370t.T4wJJ8kA` | Real Traefik: ten `LIFECYCLE_ONLY` cases (P1/P2 allow/deny, P2 oversize, P3 deny/redirect, P4 Safe, metadata omitted, P2-to-P3 timeout). P4 Strict returns 200 and expected `NON_PASS`. `stage_status=0`, `cleanup_ok=true`, unchanged source manifest, no cleanup issues and ephemeral test keys removed. |

Both composite matrices retain `catalog_acceptance=false`; Strict is not promoted. Executable/library hashes, actual loaded-libmodsecurity mappings, bounded resource samples, effective configurations and upstream observations remain external. Resource monitoring proves run containment, not concurrency/soak qualification. Evidence applies to Go `msconnector-composite`; retained legacy C `implemented_not_asserted` / `configured_not_exercised` statuses and sibling profiles remain separate.

The following later runs extend selected host evidence. They do not retroactively change the result or scope of the historical runs above.

| Run | Observed result and boundary |
| --- | --- |
| `p370extprocqualbufferedcurrent.20261003a` | Historical Envoy ext_proc PASS: three starts, delayed P2/body-limit checks, the then-current connector-owned response-limit Safe behavior, Common cancellation/recovery, unavailable/restart, four-client overlap and verified cleanup. Current master delegates response inspection limits to libModSecurity, so the response-limit result is not credited to the integrated successor until rerun. `catalog_acceptance=false`; aggregate G1/G7/G8 acceptance remains external. |
| `p370extprocpost402.20261007c` | Fresh integrated Envoy ext_proc PASS: three distinct starts with 31 probes each, controlled stop/restart and verified cleanup. The 33-byte legacy connector-budget control completed HTTP 200 with the full body and EOS, `late_action=none` and no native engine events; it proves removal of the old connector budget, not a native engine-limit rejection. Runner SHA256 `ce6fc41251f91315f2df37f5388ee0e70a00a13dded4621bae1c206b2a59bf01`; source SHA256 `2e1c3f73e4428f0c5783cc9789a80592f45402af2d9a88f27700995e3806d7f4`; `catalog_acceptance=false`. Open gaps are reproducible build provenance, the complete boundary matrix, timeout/abort/failmode coverage, separately pinned native Reject/ProcessPartial response-limit profiles with event correlation, external regression and canonical G1–G9 acceptance. |
| `p370compositefinal.6BOXCIIW` | Envoy ext_authz and Traefik forwardAuth PASS: three starts, timeout/recovery, keepalive, four-client overlap, P1/P2/body-limit origin exclusion and cleanup. Diagnostic evidence only. |
| `p370traefiknativequal4.PribNi` | Traefik native PASS: three starts, P1/P2/keepalive denial and abort origin exclusion, P3/P4 Safe, recovery, four-client overlap, resources and cleanup. Diagnostic evidence only. |
| `p370htxcampaigncurrent5.20261003a` | HAProxy HTX PASS: three distinct starts, host/origin accounting, four-client overlap, resource samples, exact input pins and controlled stop/reap/cleanup. Aggregate G1, fuller G4, G7 and G8 remain open. |
| `p370apachequalfinal3.20261003a/qualification-parent/campaign-06` | Historical Apache PASS: 35 cases, no failed probes, three starts plus controlled restart under the real nonroot identity, four-client overlap, resource and cleanup evidence. Its connector-owned response-limit BEFORE result predates current master's engine-owned contract and is not credited to the integrated successor; the fresh successor result is recorded separately below. |
| `p370apachequalfinal3.20261003a/qualification-parent/campaign-post402-d` | Fresh integrated Apache PASS: 36 cases with no failed probes, four distinct UID/GID 33 starts with zero effective capabilities, controlled restart, four-client peak, RSS/FD samples and complete process/origin cleanup. The 33-byte legacy connector-budget control returned full HTTP 200 with no event. The 1025-byte engine-owned response completed full HTTP 200 in the observed committed Safe branch and emitted the exact native P4 deny as `log_only`, with no fabricated rule ID or connector-limit fields; the follow-up succeeded. Module SHA256 `651e85ed22008fba7591746227589f7c7d9dc7cdd9f529b3c9788fd7b716e140`; result SHA256 `a2599394a825732738115d1f442a40d913204f7b8ef37efa4ae3a8374f46ab71`; `full_b_acceptance=false`. Separate late-commit Safe/Strict qualification, engine-fault injection and the full security/error matrix remain open. |
| `p370spopcampaigncurrent6.20261003a` | HAProxy SPOP intentionally returns exit 77 / `BLOCKED`: three distinct starts; first start passes 44 probes and G2–G7/G9 prerequisites, subsequent starts pass Allow/P1/P2. Phase/limit boundaries, malformed/truncated traffic, abort, agent restart, keepalive, overlap, resources and cleanup are observed. Independent G1/G8 acceptance remains blocked. |

The earlier HTX and SPOP failures remain retained as failures; successful later runs do not relabel them. No NGINX runtime credit is taken.

## Known limitations

Complete G1–G9 acceptance for nine non-NGINX profiles remains open. The selected later runs establish repeated starts, particular phase/limit boundaries, recovery, keepalive/concurrency and RSS/FD observations only within their recorded host profiles. Stock lighttpd requires independent operator attestation; G1/G4/G8 remain blocked and no qualification host run has occurred. Patched lighttpd requires the trusted namespace/noexec execution path and independent provenance/qualification executor; local namespace setup failed with `uid_map` EPERM and an ordinary bwrap run does not provide equivalent evidence. The Stock contract's 27 tests and patched contract's 18 tests do not establish host runtime acceptance or B. NGINX readiness-B qualification is excluded by the user. The evidence does not establish full catalog, CRS, HTTP/2/HTTP/3, Strict post-commit reset, production readiness or real-user traffic approval.

## Remaining risks

Native calls already executing cannot be canceled in place; unresolved cleanup requires controlled process restart. A successor delivery commit needs fresh integrated checks and hosted CI/Sonar readback. Baseline Sonar does not establish successor duplication or Quality Gate status. Fresh Envoy and Apache runs now validate the adapted connector-budget controls and the observed Apache engine-owned Safe branch. Separately pinned Envoy native Reject/ProcessPartial profiles, both Apache timing policies as independent gates, engine-fault injection and the broader matrices remain open.

TAC advisory readback is granted at `tac1`; this access does not substitute for host runtime evidence, the missing lighttpd prerequisites or successor Sonar. Successor new-code duplication at exactly 0.0% is still pending; no readiness-B or master-ready claim is made.

## Checks not run and rationale

The full nine-profile G1–G9 campaign is not established by these selected runs. Production traffic, universal protocol/CRS coverage, independent Strict host-reset evidence and NGINX readiness-B runtime were not run within this repair. Current master was merged into the PR branch; no merge into master, direct master push or deployment is performed. Framework/MRTS source remains unchanged.

## Final diff and review status

The earlier focused code and security review found no remaining blocker in its Composite/Common subdiff after cleanup and entry-ownership corrections. That conclusion does not release the whole current successor or close its runtime/delivery prerequisites. At that review, `rtk proxy make check-bilingual-docs check-doc-links`, `rtk proxy python3 ci/tools/new-change-record.py check`, `rtk proxy python3 -m unittest -v tests.test_change_record` (20 tests), and `rtk proxy git diff --check` passed. Manual owned-diff and EN/DE review confirmed matching technical values and evidence boundaries. An initial extra test-module selection failed because that module does not exist; the documented archive suite was then run successfully. The broadened current successor still requires final integrated review, complete requested acceptance and hosted checks for its published revision. Current-master integration is recorded above; no merge into master or successor Sonar result is asserted.
