# Change Record

**Language:** English | [Deutsch](CR-20260810-protected-nginx-broker-caller-repin-v4.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260810-protected-nginx-broker-caller-repin-v4 |
| Date (UTC) | 2026-08-10 |
| Base revision | 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 |
| Previous protected broker SHA | 409caa5b9664bcb8e1919d35684575e00a959f6a |
| Active protected broker SHA | 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 |
| Broker Framework gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |
| Broker availability | [PR #273](https://github.com/Easton97-Jens/ModSecurity-conector/pull/273) merged broker commit `7a9240d35e50475cc1a381fa103b0bb5cca2bee3` at 2026-08-10T14:13:09Z |

## Motivation and problem statement

The trusted-broker guides must name the caller tuple selected by this separate
uncommitted Phase-B patch. PR #273 merged broker commit
`7a9240d35e50475cc1a381fa103b0bb5cca2bee3` to `master`, making that broker
revision available, but its committed caller workflow/helper still pin
`409caa5b9664bcb8e1919d35684575e00a959f6a`. This Phase-B patch repins the
caller to broker `7a9240d35e50475cc1a381fa103b0bb5cca2bee3` with Framework
gitlink `03880bf66b3905940466ff10b3a431a27ecc6b26`. Historical Change Records
are retained unchanged.

## Acceptance criteria

The English and German guides contain the same active broker SHA-40 and
Framework gitlink in both reusable-workflow examples and the caller tuple.
They accurately distinguish PR #273 making the broker revision available from
this uncommitted Phase-B patch selecting the tuple, without treating either
the merge, its master checks, or local validation as protected runtime evidence.
This record and its German companion link reciprocally, disclose only observed
Phase-B local, hosted, and lifecycle status, and contain no private path or
secret.

## Implementation decision and rationale

Technical decision: Phase-B synchronizes the immutable caller tuple across the
caller workflow, caller helper, Python version-contract checker, focused tests,
paired trusted-broker guides, and this paired Change Record. The immutable
`uses` reference and `protected_broker_sha` remain the caller's privileged
selection boundary; no branch or mutable reference is introduced. The
Framework value is the exact mode-`160000` gitlink recorded by the broker
revision. The synchronization changes no behavior, admission gate, permission,
schema, or root command. PR #273 supplies the available broker commit; its
committed caller remains at `409caa5b9664bcb8e1919d35684575e00a959f6a`, and
this uncommitted Phase-B patch performs the caller repin. The record separates
that state, the observed PR #273 master checks, and the separate dispatch-only
protected lifecycle, which is not established by ordinary `push` workflows.

## Security impact

The update does not alter a runtime control. It preserves the documented
fail-closed immutable broker selection and makes no claim that root admission,
NGINX execution, CRS handling, artifact readback, or cleanup succeeded.

## Changed files

- docs/security/trusted-nginx-root-broker.md
- docs/security/trusted-nginx-root-broker.de.md
- .github/workflows/run-protected-nginx-root-broker.yml
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py
- tests/test_nginx_root_broker.py
- reports/audits/change-records/CR-20260810-protected-nginx-broker-caller-repin-v4.md
- reports/audits/change-records/CR-20260810-protected-nginx-broker-caller-repin-v4.de.md

## Tests and actual results

The broker-availability commit's exact-master hosted evidence was observed with
`rtk proxy gh run list --repo Easton97-Jens/ModSecurity-conector --commit 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 --limit 100 --json databaseId,name,status,conclusion,workflowName,event,headSha,url,createdAt,updatedAt`.
All listed runs were `push` runs on that exact head and completed with
`success`:

| Workflow | Run ID |
| --- | ---: |
| protocol-contract | 31396967424 |
| verified-report-governance | 31396967538 |
| Security workflow lint | 31396967572 |
| test-lighttpd | 31396967725 |
| test-envoy | 31396967530 |
| OpenSSF Scorecard | 31396968045 |
| test-haproxy | 31396967380 |
| test-traefik | 31396968058 |
| test-common | 31396967586 |
| test-nginx | 31396967630 |
| lint | 31396967719 |
| test-apache | 31396967342 |
| quick-framework-check | 31396967765 |
| CodeQL security analysis | 31396967460 |

The corrected bilingual check reported no diagnostic for either v4 record or
either trusted-broker guide; its remaining failures are the 20 pre-existing
missing Framework-gitlink targets outside this task worktree. The Change
Record adds no further source or test path beyond the complete nine-file
Phase-B scope listed above.

Actual Phase-B local validation passed 109 tests in 9.253s with the protected
caller, broker, workflow, CI security-workflow, and Python-version-contract
test modules. `check-ci-security-contract` also passed its 26 CI security
tests plus validate-only actionlint/zizmor/gitleaks locks. The standalone
Python-version-contract command exited 2 only for unchanged current-`master`
inventory violations in `verified-report-governance`, `ci-security-codeql`
trusted-go-version, Apache/HAProxy, and `update-workflow-tools`; this is
nonpassing baseline evidence, not a Phase-B pin violation.

## Commands executed

- `rtk proxy gh pr view 273 --repo Easton97-Jens/ModSecurity-conector --json number,url,state,isDraft,mergedAt,mergeCommit,headRefName,headRefOid,baseRefName,statusCheckRollup,reviewDecision` — observed PR #273 as `MERGED` into `master`, with head `bf838c3985e574756870498de176fd3294cba028`, resulting SHA `7a9240d35e50475cc1a381fa103b0bb5cca2bee3`, and merge time `2026-08-10T14:13:09Z`.
- `rtk proxy gh run list --repo Easton97-Jens/ModSecurity-conector --commit 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 --limit 100 --json databaseId,name,status,conclusion,workflowName,event,headSha,url,createdAt,updatedAt` — PASS: the 14 exact-head `push` runs listed above completed with `success`.
- `rtk proxy make check-bilingual-docs` — first run BLOCKED because this new pair lacked required headings; corrected rerun BLOCKED only by 20 pre-existing missing Framework-gitlink targets and reported no diagnostic for either v4 record or either trusted-broker guide.
- `rtk proxy make check-doc-links` — BLOCKED only by 16 pre-existing missing Framework-gitlink targets outside this scope; no scoped-path diagnostic was reported.
- `rtk proxy git diff --check -- docs/security/trusted-nginx-root-broker.md docs/security/trusted-nginx-root-broker.de.md` — PASS.
- `rtk proxy git diff --no-index --check /dev/null <each new v4 record>` — PASS for whitespace; the new-file difference is expected.
- `rtk proxy rg -n <old/new broker SHA, Framework SHA, and PR head> <four scoped files>` — PASS: both guides contain only the active broker SHA and Framework gitlink; the predecessor SHA remains only as the historical identity in this new record pair.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_ci_security_workflows tests.test_python_version_contract` — PASS: 109 tests in 9.253s.
- `rtk proxy make PYTHON=python3 check-ci-security-contract` — PASS: 26 CI security tests plus validate-only actionlint/zizmor/gitleaks locks.
- `rtk proxy make PYTHON=python3 check-python-version-contract` — exit 2 only for unchanged current-`master` inventory violations in `verified-report-governance`, `ci-security-codeql` trusted-go-version, Apache/HAProxy, and `update-workflow-tools`; nonpassing baseline evidence, not a Phase-B pin violation.

## Runtime evidence

No resulting-caller Phase-B protected lifecycle evidence was observed. The
exact-head listing above contains the 14 ordinary `push` workflows for the
broker-availability commit only; it does not show a successful dispatch of
`Protected NGINX Root Broker Lifecycle` for this uncommitted caller repin and
cannot prove its root-master/non-root-worker, CRS, artifact, or cleanup
behavior.

## Checks not run and rationale

No protected lifecycle dispatch, root action, NGINX start, CRS fetch, audit,
artifact readback, stop, or cleanup was run for this Phase-B caller repin.
Those operations require the separate protected GitHub-hosted workflow and
are not implied by PR #273 or its exact-master checks.

## Known limitations

This record documents the complete Phase-B caller-repin scope and the observed
local validation above. PR #273 established broker availability only; this
uncommitted nine-file patch has no new PR, hosted exact-head check, review,
merge, branch-protection, SonarQube Cloud, or resulting-caller lifecycle
result.

## Remaining risks

The uncommitted caller tuple still needs a separate resulting-master protected
lifecycle to establish runtime evidence for both `no-crs` and `owasp-crs`
profiles.

## Final review status

Scoped literal, bilingual-pair, reciprocal-link, and whitespace review is
complete. Global documentation checks remain blocked by the pre-existing
unmaterialized Framework targets. The observed Phase-B local validation is
recorded above; PR, hosted, and protected-lifecycle evidence remain separate
and unclaimed. No staging, commit, push, pull request, or merge is authorized
by this record.

## Final diff and review status

The Phase-B scope is the nine paths listed above; the scoped guide/record
whitespace review is clean. Historical records, Framework content, MRTS
content, and gitlinks are not changed by this caller repin.
