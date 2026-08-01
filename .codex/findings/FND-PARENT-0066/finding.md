# FND-PARENT-0066 — Invalid full-matrix control evidence can retain pass status and permit evidence-only reclassification

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0066 |
| Category | evidence_gap |
| Repository / ownership | Parent / Parent |
| Priority / severity / confidence | P2 / low / validated |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | false / true |
| Connector / profile | Apache, HAProxy, NGINX full-matrix evidence / verified runtime mismatch analysis |

## Summary

At Parent revision 9f23ae2c5fe908cef38f203be03f93fda75a8dd7,
full_matrix_case_control_evidence() retains a producer-declared pass in its
fallback even after its required pass/403/403/live predicate fails. Both
collection-semantics classifiers use only the emitted status as their all-pass
gate. The retained focused pre-fix unit proves the non-live variant; the
adjacent wrong-actual-status variant takes the same fallback.

This is a bounded CI evidence-integrity defect. It does not establish a
request-path enforcement bypass, an external hosted-CI attacker path, source
execution, filesystem access, or secret disclosure.

## Boundary, behavior, and impact

Full-matrix summary JSON crosses from connector CI producers into an evidence
generator. A control is legitimate only if its producer status is pass, its
expected status is 403, its actual or observed status is 403, and it ran live.
The helper currently emits the producer status unchanged on every failed
predicate. The two downstream classification functions then permit an
evidence-only/documentation-only reclassification when all emitted statuses
are pass.

Thus stale or malformed producer evidence can make a non-live or false-allow
control appear sufficient, lowering a generated mismatch report's criticality
or merge-readiness signal. The evidence demonstrates only that report-control
boundary; it does not claim direct production impact.

## Reproduction and evidence

The focused test
tests.test_report_conditional_remediation.ReportConditionalRemediationTest.test_full_matrix_control_evidence_keeps_fixed_case_and_fallback_contracts
supplies a HAProxy record with status=pass, expected_status=403,
actual_status=403, and live_executed=false. It requires the helper to emit
status=fail; the baseline instead emits status=pass and exits 1.

| Evidence | Result |
| --- | --- |
| /var/tmp/codex/ModSecurity-conector/runs/ci-b-verified-runtime-mismatch-qgBSMu/pre-fix-control-evidence-negative-test.txt | Retained pre-fix regression failure, SHA-256 ef0876d194abe7258f5302263b0efa0a35f40a869cf84d2d00ad5d463427efe9 |
| Command | rtk proxy bash -lc 'PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_report_conditional_remediation.ReportConditionalRemediationTest.test_full_matrix_control_evidence_keeps_fixed_case_and_fallback_contracts' |
| Result | exit 1 before the repair; expected fail, observed pass for the non-live control |

The same test contains the adjacent status=pass, expected 403, actual 200,
live true case. It must also become non-passing after the source repair.

## Remediation and validation

Retain the wrapper and the four-part success predicate. Only normalize a
fallback producer pass to fail when the predicate is not met. Preserve the
producer's non-pass status and evidence fields. Add direct coverage for the
non-live and wrong-actual paths, while retaining legitimate live-403 Apache
and NGINX controls and wrapper/parameterized-helper equivalence.

Acceptance criteria:

- A pass/403/403/non-live record is non-passing.
- A pass/403/200/live record is non-passing.
- Valid pass/403/403/live controls remain pass.
- Neither downstream status-only all-pass gate can receive a false pass from
  the failed predicate.
- Focused tests, syntax/diff checks, final bypass review, and exact-head
  hosted PR checks are recorded without weakening any evidence or scanner
  control.

## Residual risk and history

The record is fixed, not verified or closed. The repair converts an invalid
fallback `pass` to `fail`; the retained post-fix regression passes, the
complete direct test module passes 11 tests, selected Python compilation and
diff hygiene pass, and a complete two-path local security diff scan reports
zero reportable findings. Draft PR #178 is exactly at
`178f0f9b965f75982230ef855fe386474e9a4652` locally, remotely, and on GitHub;
all 33 hosted checks pass. SonarQube Cloud reports Quality Gate `OK`, zero
open PR issues, `new_violations=0`, `new_duplicated_lines=0`, and
`new_duplicated_lines_density=0.0`. A resulting-master original reproduction
remains required before verified or closed. It is not a release blocker and no
risk acceptance, merge, master result, or hosted exploit claim is made.

- 2026-07-29T09:02:14Z — focused pre-fix non-live bypass reproduced and
  retained.
- 2026-07-29T09:02:14Z — narrow Parent CI remediation started.
- 2026-07-29T09:26:36Z — local source repair set to fixed after the retained
  post-fix control regression, 11-test module, syntax/diff checks, and complete
  local security-diff review; exact-head hosted verification remains pending.
- 2026-07-29T09:48:47Z — Draft PR #178 exact-head verification completed:
  local, remote, and GitHub HEAD are
  `178f0f9b965f75982230ef855fe386474e9a4652`; all 33 hosted checks pass, and
  SonarQube Cloud reports Quality Gate OK, zero open PR issues, and zero new
  violations/duplicate lines. The finding remains fixed pending a separately
  authorized master result and original reproduction.
