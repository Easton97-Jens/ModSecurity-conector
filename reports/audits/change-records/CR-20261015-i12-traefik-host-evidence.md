# Change Record: CR-20261015-i12-traefik-host-evidence

**Language:** English | [Deutsch](CR-20261015-i12-traefik-host-evidence.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-traefik-host-evidence |
| Date (UTC) | 2026-10-15 |
| Base revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation and problem statement

Extend separate Native/UDS, forwardAuth request and response-companion I12 evidence from PR410 head f27eb59b. Preserve original280 required IDs and124 original open expectations, rather than treating functional smoke as complete qualification.

## Acceptance criteria

Retain isolated source/config/run identities, real host/client/backend/native/EOS/finish/free/cleanup evidence and original oracles. Execute requested Go/Race/Vet, UDS/observer/security-contract checks. Publish paired evidence reports with explicit unresolved IDs and a Draft PR against work/pr382-i12-host-evidence-20261011. Full I12 acceptance remains partial:6PASS/1FAIL/273unqualified; original124 expectations now4resolved/120unresolved.

## Implementation decision and rationale

Use the existing central traefik-native and traefik-forwardauth capture variants unchanged. Add only Traefik-specific sealed source-copy producers, strict client framing review, explicit synthetic fault fixtures and a standalone ledger importing existing validators. Pin the complete original inventory to prevent injected baseline PASS or oracle resolutions. Reject nonphysical, symlinked, checkout and outside-storage native output paths before writes; validate fresh followup targets. Reject empty host callback captures and TCP-EOF substitution. Retain Commonfinish2 idempotent calls separately from once native finalization/free. Preserve maxResponseBodySize=32768 as authorization-response capacity.

## Changed files

connectors/traefik/harness/i12/native/ and i12_auth/: host producers, clients/backends, fault peers, reviewers, packet proposals and paired READMEs. connectors/traefik/harness/i12_ledger.py plus fixtures/i12_original_inventory.json: independent Traefik ledger/input. Three tests/test_traefik_i12_* modules: evidence-integrity controls. connectors/traefik/build/test-engine-service-runtime.sh: handle immediate BrokenPipe/reset during intentionally saturated worker admission. docs/i12-traefik-evidence-20261015.md and .de.md plus this Change Record pair. Product source, Common, central I12 matrix/shared generators, dependency files and Framework/MRTS/gitlinks are unchanged.

## Commands executed

All shell commands used RTK. Fresh per-module rtk proxy /usr/local/go/bin/go test -count=1 ./..., test -count=1 -race ./... and vet ./... passed for three Traefik modules. rtk proxy make -C connectors/traefik test-engine-service passed after the scoped rejection-test correction; native protocol/self-test,64nonreading peers/deadline/follow-up/socket replacement actually executed. RTK-wrapped Parent unittest checks and make check-common-security-contract passed, with retained initial path/setup failures. Central capture verification and15guards plus31ledger/oracle/report regressions passed. Exact argv, CWD, exit statuses and output SHA256 are under external run i12-traefik-20261015/verification. Final focused I12 tests:23PASS. Paired documentation/local links pass with the unchanged Framework temporarily mounted read-only in a private namespace; Change Record check passes. Separate terminal receipts are i12-final-unit-tests-v3, final-docs-publication and change-record-publication.

## Security impact

No enforcement control, host limit, warning, authentication, peer check or gate is weakened. Candidate code runs nonroot with zero capabilities in independently reviewed namespaces and sealed bindings. Synthetic MSE1/MRC1 faults and same-UID peer fixtures remain explicit test inputs. Complete sample/host rejection, native decision and technical error are distinct. Native Strict is rejected by the current profile; unsupported positive behavior is not fabricated.

## Runtime evidence

External root /var/tmp/codex/ModSecurity-conector/runs/i12-traefik-20261015 retains physical logs, raw synthetic client/backend bytes, loaded image maps, source/config hashes, process/FD/UDS observations and cleanup. Three corrected native matrices21exchanges, independent request14 and companion14exchanges, and focused authorization-capacity3exchanges give52current measured exchanges; older failed/partial attempts remain separate. Root reviewed35-field packets qualify native NEED-request-streaming, request allow_without_marker and companion phase4_rule_observed. The same companion P4 transaction FAILS phase4_deny_after_commit_log_only_safe because late_intervention=false and required mode is absent. The connector-free direct SDK streaming oracle establishes the one new original expectation independently.

## Known limitations

I12 is not fully closed:6qualifiedPASS,1qualifiedFAIL,273unqualified required IDs and120unresolved original oracles remain explicit per route. Native Strict is unsupported by source/profile and actual startup rejection. Original successful-allow/client-cancel/EOS evidence is preserved. Charset fixtures use ASCII and do not establish non-ASCII recoding. Native authorization events report GET while the original client sends POST. Unknown valid64hex correlation handles, H2/H3, original file-backed cases and unexercised sink-fault obligations remain unqualified.

## Remaining risks

Independently confirmed companion telemetry defect: complete physical Late-Intervention event has false late flag and missing mode despite committed deny-to-log_only action. Two independent host runs reproduce it; source review excludes capture interference. No enforcement failure is demonstrated. The producer/receipt/source chain is [handed off to product PR382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382#issuecomment-6194758198); no production fix in this evidence branch. Initial Strict/v4 namespace cleanup failures remain failures even though subsequent exact-PID checks show absence. Latest successful controllers have no survivors/mount leaks and final native mappings0.

## Checks not run and rationale

No broad all-connector matrix, Framework/MRTS execution, H2/H3 run, additional deep security scan, production repair, merge or deployment: outside this Traefik evidence scope. Two optional legacy direct-host loader tests lack TRAEFIK_BIN in the portable contract invocation; separate realhost namespace tests load the actual private plugins. Hosted checks/reviews/Quality Gate apply only after publication and are not inherited from PR410.

## Final diff and review status

Scoped local review includes an independent ledger tamper audit and an independent source/physical-log validation of the companion defect. Root preserves original status/history while independently checking fresh packets against all35measurement roles. Only explicit task-owned files are eligible for staging. Draft #413 is published against the requested base; initial-head Sonar gate fails security rating E/A with15signals, independently triaged without a validated reachable vulnerability under the sealed controller; no remote dispositions/gate changes. Subsequent exact-head checks are retained in external delivery receipts; no force push, merge or master change is authorized.
