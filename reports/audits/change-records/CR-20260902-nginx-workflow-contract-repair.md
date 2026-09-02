# Change Record: NGINX workflow-contract repair

**Language:** English | [Deutsch](CR-20260902-nginx-workflow-contract-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260902-nginx-workflow-contract-repair |
| Date (UTC) | 2026-09-02 |
| Base revision | 8743fceeb708c06329c14ac00a1f333945edf1d7 |
| Delivery status | The user authorized a Parent-only repair in a dedicated worktree and one Draft PR. Commit, push, PR creation, exact-head hosted checks, and SonarQube Cloud evidence remain pending. No merge, direct master write, force action, bypass, or auto-merge is authorized. |

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
credential, dependency, Framework source, MRTS source, Gitlink, scanner, or
Quality Gate configuration changes.

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

## Changed files

- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.md
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

| Check | Actual result |
| --- | --- |
| Pre-patch rtk proxy make check-nginx-common-adoption | Reproduced failure: exit 2 with exactly the stale mapper and seen-byte assertions. |
| Post-patch rtk proxy make check-nginx-common-adoption | Passed. |
| Combined NGINX upstream security and CI-security workflow tests | Passed: 44 tests. |
| Python compilation of the changed checker | Passed. |
| rtk proxy git diff --check | Passed. |
| Codex Security Standard and post-patch diff scans | Both sealed reports validate with complete coverage and 0 reportable findings. |
| make check-bilingual-docs | Blocked only by 20 pre-existing missing Framework Gitlink targets; no current change-record path was reported. |
| make check-doc-links / repository-path reference check | Blocked only by the same absent Framework checkout and its pre-existing targets. |
| make lint | Reached host-runtime preflight, then stopped at the absent Framework no-CRS baseline catalog; no Framework initialization or change was authorized. |
| Exact-head hosted and SonarQube Cloud checks | Pending normal Draft-PR delivery. |

## Runtime evidence

The repair is a source-contract alignment. No NGINX runtime was started, no
request or response payload was retained, and no privileged, protected, or
maintenance workflow was dispatched. Fresh exact-head hosted evidence remains
required after PR delivery.

## Checks not run and rationale

The full documentation and lint controls cannot complete in this worktree
because `modules/ModSecurity-test-Framework` is not checked out. The observed
documentation errors name only missing Framework targets, and lint stops at the
Framework no-CRS baseline catalog after its available local preflight. No
Framework initialization, dependency installation, or cross-repository change
is inferred from this Parent-only request. Full connector runtime matrices and
make quick-check remain outside the checker repair's scope.

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

## Remaining risks

The checker will deliberately fail if a future refactor removes the extracted
helper relationships or the required guards and Common-plan assignment. Hosted
CI may expose an independent environment or integration failure after PR
creation. This task does not claim that the seven historical SonarQube Cloud
issues are resolved.

## Final diff and review status

The final local diff check, focused source-contract controls, combined security
contracts, Python compilation, and sealed Codex Security Standard/diff scans
have passed; both scans have 0 reportable findings. Documentation controls are
blocked only by the absent Framework checkout. Commit, push, Draft PR creation,
exact-head GitHub Actions checks, and exact-head SonarQube Cloud analysis remain
required. No merge is authorized.
