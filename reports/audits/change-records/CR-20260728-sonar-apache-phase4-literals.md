# Change Record: Parent Apache Phase-4 control-literal ownership for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260728-sonar-apache-phase4-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260728-sonar-apache-phase4-literals` |
| Date (UTC) | `2026-07-28` |
| Base revision | `8e8acb8dab1cd03723de269cab7da7dd62e5e010` |
| Candidate designation | Draft Parent PR [#156](https://github.com/Easton97-Jens/ModSecurity-conector/pull/156). Its initial exact head `e2b1370caa32e621ada4ce96ad03f603904cee49` has hosted checks and a Quality Gate result; a task-owned S3415 follow-up is now awaiting a new exact-head cycle. No review or merge outcome is claimed. |
| Tracking | `AZ98JczJLJyjbmyNA5LT` and `AZ98JczJLJyjbmyNA5LN`; both are live Parent `shelldre:S1192` findings before this candidate. |
| Boundary | Parent Apache Phase-4 smoke harness, its direct source-wiring test, this English/German Change Record pair, and its two indexes. Framework, MRTS, Gitlinks, workflows, reports, scanner policy, and hosted state remain unchanged. |

## Motivation and problem statement

The Apache Phase-4 smoke harness repeated the fixed response prefix
`first-byte-prefix` in four body-leak checks and the fixed fail-closed log
message `request transaction cannot be safely rebound to the target URI` in
six redirect/error-document checks. SonarQube Cloud reports both repetitions as
S1192 maintainability findings. These are response and redirect integrity
controls, so literal ownership must not relax an assertion, change a grep
argument, or turn a non-success/refusal path into a successful path.

## Acceptance criteria

- `PHASE4_FIRST_BYTE_PREFIX` owns exactly the four selected fixed grep patterns
  and each use remains a quoted `grep -F` argument against the response body.
- `PHASE4_TRANSACTION_REBIND_REFUSAL` owns exactly the six selected fixed grep
  patterns and each use remains a quoted `grep -F` argument against the Apache
  error log.
- Bypass, precommit-deny, custom-MIME deny, engine-append-failure, internal
  redirect, nested ErrorDocument, and preoutput ErrorDocument controls retain
  their existing failure conditions and diagnostic messages.
- Shell syntax, direct source-wiring tests, whitespace, security review,
  bilingual documentation, and later exact-head hosted evidence are recorded
  truthfully.

## Implementation decision and rationale

The harness declares two POSIX `readonly` values near its file-local runtime
configuration:

- `PHASE4_FIRST_BYTE_PREFIX`
- `PHASE4_TRANSACTION_REBIND_REFUSAL`

Each value is initialized from its exact former single-quoted literal and is
used only through a double-quoted expansion. The refactor preserves fixed-string
matching, one shell argument, the searched file, redirects, `|| fail` control
flow, and all existing failure messages. The two complete expected-response
body literals remain deliberately separate because they assert full allowed
body content rather than the four reported prefix-search calls.

The direct source-wiring test verifies one declaration per constant, absence of
the old raw grep forms, absence of unquoted variable forms, exactly four/six
quoted grep uses, and the retained response-leak and transaction-rebind
diagnostic contracts.

## Changed files

- `connectors/apache/harness/run_apache_smoke.sh`
- `tests/test_apache_phase4_response_regression_wiring.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-phase4-literals.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-phase4-literals.de.md`

## Commands executed

| Command or control | Actual result |
| --- | --- |
| `sh -n connectors/apache/harness/run_apache_smoke.sh` in the exact task worktree | passed. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B tests/test_apache_phase4_response_regression_wiring.py` with `PYTHONNOUSERSITE=1` and `PYTHONDONTWRITEBYTECODE=1` in the exact task worktree | passed: 11/11 tests. |
| `git diff --check` | passed; no whitespace error. |
| Focused shell/protocol security review | approved; no plausible or validated finding. |
| Disposable exact-candidate Parent/Framework documentation overlay | passed: bilingual documentation, repository path references, and Framework document links. |
| Initial exact-head hosted round for PR #156 | GitHub checks terminal success/scope-justified skip and Quality Gate `OK` with `0.0` new duplication; not clean because seven task-owned `python:S3415` issues remained. |
| Follow-up direct source-wiring module | passed: 11/11 tests after only swapping the seven `assertEqual(actual, expected)` argument orders. |

## Security impact

The changed values are fixed grep patterns used at a response-body leak
detection and fail-closed redirect boundary. The review verified that no
request, response, environment, or command-substitution value can influence
either pattern: both are hard-coded `readonly` values and each expansion is
double quoted. `grep -F` still treats response bodies and logs as searched data,
not shell code.

The bypass branch still requires the prefix. Precommit-deny, custom-MIME deny,
and engine-append-failure still fail if it appears. All six redirect/error-
document paths still require the rebind-refusal log entry while retaining their
non-success and body-leak assertions. No broken control or reportable security
finding was identified.

## Runtime evidence

No Apache host runtime, connector matrix, Framework runtime, or MRTS runtime
was started. The shell syntax and direct source-wiring test establish only the
static harness contract; they do not establish deployment compatibility or an
end-to-end Apache runtime result.

## Known limitations

The initial exact hosted round is retained, but it is not final evidence: it
found seven task-owned `python:S3415` test-assertion-order issues. The normal
follow-up changes only argument ordering and requires a new exact-head PR,
SonarQube Cloud, workflow, review, and Quality Gate cycle. The existing Apache
runtime/matrix remains intentionally out of scope for this literal extraction.

## Remaining risks

A future harness edit could add an equivalent unowned grep literal or change a
body/redirect contract outside this scope. The file-local owners, direct test,
shell syntax check, and focused security review reduce that risk. Fresh
exact-head hosted analysis remains required before the cited SonarQube Cloud
receipts can be treated as fixed.

## Checks not run and rationale

- No Apache host build, real smoke runtime, full matrix, report generation,
  workflow execution, Framework source check, or MRTS check was run; each is
  outside this Parent-only static extraction.
- `make check-bilingual-docs` is not run directly in the task worktree because
  its pinned Framework Gitlink is intentionally absent. Instead, the exact
  candidate plus the read-only Parent-pinned Framework archive passed the
  three repository documentation checks in a disposable external overlay.
- The final corrected head has not yet been pushed or analyzed. Its exact-head
  hosted PR/Sonar evidence is required before delivery is considered verified.

## Final diff and review status

Initial commit `e2b1370caa32e621ada4ce96ad03f603904cee49` is pushed as Draft
PR #156. Its initial checks and Quality Gate passed, but seven task-owned
`python:S3415` issues require a normal source-only follow-up. The current
uncommitted follow-up swaps only actual/expected order in those assertions;
all original comparisons and Phase-4 contracts remain unchanged. No
Ready-for-review, merge, master change, Framework/MRTS change, Gitlink update,
workflow change, or scanner-policy action is claimed.
