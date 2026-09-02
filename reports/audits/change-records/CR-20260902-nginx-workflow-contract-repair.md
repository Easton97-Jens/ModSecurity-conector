# Change Record: NGINX workflow-contract repair and Envoy gRPC security update

**Language:** English | [Deutsch](CR-20260902-nginx-workflow-contract-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260902-nginx-workflow-contract-repair |
| Date (UTC) | 2026-09-02 |
| Base revision | 8743fceeb708c06329c14ac00a1f333945edf1d7 |
| Delivery status | The first repair commit was normally pushed and created Draft PR #351; its exact first head passed all reported hosted checks and SonarCloud’s PR Quality Gate with zero PR issues. A High-severity runtime dependency remediation discovered during that delivery is now being added to the same Draft PR and requires fresh exact-successor evidence. No merge, direct master write, force action, bypass, or auto-merge is authorized. |

## Motivation and problem statement

Five current master workflows—test-common, lint, test-apache,
quick-framework-check, and test-nginx—stopped at the same
make check-nginx-common-adoption source-contract failure. The pre-patch check
exited 2 and reported two stale assertions: the response-mapper guard was no
longer inline in ngx_http_modsecurity_body_filter, and seen-byte accounting no
longer used ctx->response_body_bytes_seen += len.

The live NGINX code remains intentionally correct:
ngx_http_modsecurity_prepare_response_body_filter owns eligibility and mapper
ordering, while ngx_http_modsecurity_plan_limited_response_body uses the Common
body-limit plan to record plan.bytes_seen. This repair aligns the checker with
those live boundaries instead of changing request or response handling.

During normal Draft-PR delivery, GitHub surfaced open Dependabot alert #3:
`GHSA-vp52-pcj8-j9qc` / `CVE-2026-84304`. The directly resolved Envoy ext_proc
runtime dependency `google.golang.org/grpc v1.82.1` is within its affected range
through v1.83.0; v1.83.1 is the first patched version. Independent boundary
review confirmed that productive standalone and composite servers use grpc-go
before application-level body/message limits, so the narrow security update is
required for a safe delivery.

## Acceptance criteria

- make check-nginx-common-adoption passes and verifies the live helper
  boundaries rather than the obsolete inline form.
- The checker still requires once-only, non-fatal mapper validation after the
  context and Phase-4 eligibility guards.
- The checker still requires an in-scope gate before response-body ingestion
  and Common-plan assignment of ctx->response_body_bytes_seen.
- Existing NGINX upstream security contracts and CI-security workflow
  contracts pass without a suppression, permission change, scanner change, or
  control relaxation.
- Envoy ext_proc resolves grpc-go v1.83.1 with its complete tidy module graph;
  the security-floor contract rejects the former v1.82.1 minimum.
- Readonly module verification, tests, build, and vet succeed using task-owned
  caches; existing listener, message-size, stream, and UDS safeguards remain
  unchanged.
- A task branch and Draft PR are delivered only after exact-head review; no
  merge is performed by this task.

## Implementation decision and rationale

The change adds extracted static views of the live preparation, body-limit, and
chain-append helpers to ci/checks/connectors/nginx/check-nginx-common-adoption.py.
It verifies that the top-level body filter delegates to preparation; that
preparation performs the null and intervention/processed guards before the
mapper-once helper; that chain append returns before body ingestion for an
out-of-scope Phase 4 response; and that the Common plan records plan.bytes_seen.

No NGINX C source, workflow YAML, action pin, job permission, trigger,
credential, Framework source, MRTS source, Gitlink, scanner, or Quality Gate
configuration changes. The sole dependency change is the Direct Envoy grpc-go
security remediation and the Go tool's required tidy graph adjustment: grpc-go
v1.83.1, its checksum, the grpc-go-selected genproto RPC requirement/checksum,
the already-selected direct x/sys requirement, and the transitively selected
OpenTelemetry 1.44 checksums.

## Security impact

The affected check describes response-body inspection, an explicitly
security-relevant boundary. The repair preserves the non-fatal mapper warning
behavior, once-only validation, Phase-4 scope gate, and Common reject-plan
accounting. It neither broadens a workflow token nor changes a runtime security
decision.

The Codex Security scan of the Parent .github scope found no validated high- or
critical-severity issue. The reviewed SARIF-upload jobs retain the intentionally
allowlisted contents: read plus security-events: write permissions required for
uploads; no workflow file is changed here.

FND-PARENT-1011 records the High-severity gRPC dependency finding. The patch
raises only the direct requirement, complete resolved checksums, semantic CI
floor, and paired module documentation to v1.83.1. It does not claim that
connector message limits, loopback configuration, or the response observer's
UDS authorization substitute for the upstream transport fix.

## Changed files

- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.md
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- connectors/envoy/ext_proc/go.mod
- connectors/envoy/ext_proc/go.sum
- connectors/envoy/ext_proc/README.md
- connectors/envoy/ext_proc/README.de.md
- tests/test_ci_security_workflows.py

## Commands executed

| Check | Actual result |
| --- | --- |
| Pre-patch rtk proxy make check-nginx-common-adoption | Reproduced failure: exit 2 with exactly the stale mapper and seen-byte assertions. |
| Post-patch rtk proxy make check-nginx-common-adoption | Passed. |
| Combined NGINX upstream security and CI-security workflow tests | Passed: 44 tests. |
| Python compilation of the changed checker | Passed. |
| rtk proxy git diff --check | Passed. |
| Codex Security Standard and post-patch diff scans | Both sealed reports validate with complete coverage and 0 reportable findings. |
| gRPC pre-patch dependency and transport-boundary triage | Confirmed Dependabot #3, direct v1.82.1 resolution, the productive server boundary, and v1.83.1 as the first patched version. |
| go mod tidy -diff | Passed after the complete required grpc-go module graph adjustment. |
| go mod verify | Passed: all modules verified. |
| go test -mod=readonly ./... | Passed: all eight Envoy ext_proc packages. |
| go build -mod=readonly -buildvcs=false ./... | Passed; `-buildvcs=false` is required only because the sandbox denies Go’s VCS stamping metadata read. |
| go vet -mod=readonly ./... | Passed. |
| Independent Codex Security bypass/regression review | Passed: no surviving vulnerable resolution route or legitimate behavior regression was validated; `GOWORK=off` module verification and complete module-list evidence passed. |
| make check-bilingual-docs | Blocked only by 20 pre-existing missing Framework Gitlink targets; no current change-record path was reported. |
| make check-doc-links / repository-path reference check | Blocked only by the same absent Framework checkout and its pre-existing targets. |
| make lint | Reached host-runtime preflight, then stopped at the absent Framework no-CRS baseline catalog; no Framework initialization or change was authorized. |
| First Draft-PR #351 exact head hosted checks and SonarCloud PR analysis | Passed before the gRPC remediation; successor-head evidence remains required. |

## Runtime evidence

The repair is a source-contract alignment. No NGINX runtime was started, no
request or response payload was retained, and no privileged, protected, or
maintenance workflow was dispatched. Fresh exact-head hosted evidence remains
required after PR delivery.

The dependency remediation likewise starts no connector listener and retains no
traffic. It proves module integrity and source-level compatibility through the
module's readonly tests, build, and vet controls rather than attempting an
availability attack against gRPC transport buffering.

## Checks not run and rationale

The full documentation and lint controls cannot complete in this worktree
because `modules/ModSecurity-test-Framework` is not checked out. The observed
documentation errors name only missing Framework targets, and lint stops at the
Framework no-CRS baseline catalog after its available local preflight. No
Framework initialization, dependency installation, or cross-repository change
is inferred from this Parent-only request. Full connector runtime matrices and
make quick-check remain outside the checker repair's scope. The gRPC change has
no suitable safe local exploit replay; it uses the authenticated advisory,
resolved-version proof, and standard module controls instead.

## Known limitations

The local validation proves the static contract and the existing NGINX source
security tests, not a native NGINX build or an end-to-end response flow. The
active Parent ruleset and hosted workflow execution remain external controls
that must be observed on the exact PR head.

SonarQube Cloud currently reports a passing Quality Gate for the base revision,
but seven historical project-wide open issues remain, including one
Framework-owned issue outside this Parent-only authority. Literal project-wide
zero therefore requires a user scope decision; no issue is hidden, suppressed,
or marked false-positive by this change.

The default-branch Dependabot alert will remain open until an authorized merge.
This task can validate the PR successor head but cannot claim default-branch
remediation or perform the merge.

## Remaining risks

The checker will deliberately fail if a future refactor removes the extracted
helper relationships or the required guards and Common-plan assignment. Hosted
CI may expose an independent environment or integration failure after PR
creation. This task does not claim that the seven historical SonarQube Cloud
issues are resolved. The directly remediated gRPC transport risk remains present
on master until the draft PR is reviewed and an authorized actor merges it; no
such merge is within the current delivery authorization.

## Final diff and review status

The original workflow repair is committed, pushed, and opened as Draft PR #351;
its first exact head passed the hosted checks and SonarCloud PR Quality Gate
with zero issues. The combined successor diff has passed focused NGINX controls,
44 Python security-contract tests, readonly Go module validation/tests/build/vet,
and the tidy-diff control. Documentation controls remain blocked only by the
absent Framework checkout. The independent Codex Security bypass/regression
review passed; immutable-commit diff scan, normal push, and exact-successor
hosted/SonarCloud evidence remain required. No merge is authorized.
