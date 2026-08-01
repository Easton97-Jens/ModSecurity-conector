# Change Record: Parent CI evidence SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-ci-evidence-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-ci-evidence-remediation` |
| Date (UTC) | 2026-08-01 |
| Base revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | SonarQube Cloud `ci/evidence` baseline: 15 security findings, 1 security hotspot, 96 maintainability findings, 327 duplicated lines, and 1.6% duplicated-lines density. |
| Boundary | Parent `ci/evidence`, one focused Parent regression test, and this English/German Change Record/index pair. Framework, MRTS, Gitlinks, workflows, scanner settings, suppressions, exclusions, Quality Gates, and `master` remain unchanged. |

## Motivation and problem statement

The current `ci/evidence` inventory contains filesystem-boundary and URL-policy
findings, one security hotspot, complex report generators, repeated literals,
redundant list handling, and duplicate report logic. The remediation must
preserve fail-closed evidence inputs, status classification, report schemas,
and source-root containment without changing a SonarQube Cloud rule,
exclusion, suppression, or Quality Gate.

## Acceptance criteria

- Each baseline `ci/evidence` source anchor has a source-level remediation or
  explicit hosted-analysis disposition; no scanner setting or suppression changes.
- Output paths remain below their selected safe roots, reject traversal and
  symlink escapes, and preserve a legitimate in-root output path.
- Repository references remain HTTPS-only where existing policy requires it.
- The capability catalog preserves all 60 names and canonical ordering.
- The final Draft PR head receives fresh Actions and SonarQube Cloud evidence
  before any merge decision.

## Implementation decision and rationale

Narrow parsing, classification, rendering, and data-construction helpers now
own the formerly repeated report logic. Existing root-bound writers retain
output containment, default cache material stays under a user-private root,
and HTTPS validation remains explicit. The capability catalog is grouped by
responsibility and assembled in its prior canonical order, avoiding a second
large tuple without changing its public result. A focused test executes valid
in-root output and rejects traversal, symlink escape, unsafe schemes, and
permissive output permissions.

## Changed files

- `ci/evidence/collectors/connector_capabilities.py`
- nineteen Parent `ci/evidence/reports/*.py` files from the task diff,
  including report refresh, runtime mismatch, system environment, remaining
  critical/failure, and NGINX HTTP-500 generators
- `tests/test_evidence_output_security.py`
- the two Change Record indexes and this English/German record pair

## Commands executed

| Command or check | Result |
| --- | --- |
| `python -m py_compile` for all 20 changed Python source/test files | passed. |
| `python -m unittest tests.test_generated_report_evidence_integrity tests.test_report_conditional_remediation tests.test_evidence_output_security` | passed: 93 tests; embedded generated-report layout check passed. |
| `python ci/evidence/collectors/connector_capabilities.py check` | passed: 6 connectors and 60 capabilities. |
| `git diff --check origin/master...HEAD` | passed before Change Record additions; rerun after documentation updates and before delivery. |
| Focused Parent security diff review | passed: explicit receipts cover all 20 rebased diff files; no reportable security-regression candidate was found. |

## Security impact

Evidence paths continue to reject output traversal and symlink escapes before
publication, use the existing safe root-bound writer, and produce owner-only
capability output. HTTPS-only repository validation and fail-closed runtime
evidence predicates remain active. The focused review inspected changed path,
cache, writer, URL, and evidence-classification code and found no reportable
diff regression; it is not a repository-wide security assessment.

## Runtime evidence

Focused Python controls execute the changed report helpers with temporary
task-owned roots. They demonstrate valid output and reject traversal,
symlink escape, unsafe repository schemes, and permissive permissions. The
capability command executes its public catalog check. These are not claims of
a full connector matrix or external runtime.

## Known limitations

Neither `radon` nor Python `ruff` is available in the selected environment, so
local complexity/duplication numbers do not substitute for SonarQube Cloud.
The packaged security-diff worklist filter excludes `ci`; the review therefore
bound the exact 20 changed paths explicitly and retained one receipt per file.
Exact-head hosted analysis remains the source of truth for Sonar status.

## Remaining risks

An unexercised connector integration path or live artifact shape outside the
fixtures could still reveal a presentation difference. The intentionally
uninitialized, out-of-scope Framework submodule prevents the full Parent suite
from running Framework-dependent controls. Exact-head hosted Actions and
SonarQube Cloud analysis remain necessary before a merge decision.

## Checks not run and rationale

- Full connector builds, runtime matrices, and report generation were not run:
  this task changes Parent evidence tooling and has no task-owned verified
  connector-runtime evidence.
- Framework and MRTS checks were not run. The task is Parent-only; no source
  or Gitlink in either repository changed.
- The broader Parent unittest suite cannot complete Framework-dependent
  controls because the intentionally uninitialized submodule lacks
  `modules/ModSecurity-test-Framework/ci/lib/common.sh`. This is an
  environment limitation, not a passing full-suite claim.
- Hosted Actions, review state, and exact-head SonarQube Cloud require the
  authorized Draft PR and remain pending at record authoring.

## Final diff and review status

At record authoring, the rebased source/test checkpoint is local at
`f9d48a12ba444efb294ae28aa7944cc5eedea87e` on top of the listed base. It is
limited to Parent `ci/evidence`, one focused Parent test, and traceability
documentation. No Framework/MRTS/Gitlink, workflow, dependency, scanner
configuration, suppression, Quality Gate, or `master` change is present.
Local controls and the bounded review passed. Commit, push, Draft PR, hosted
verification, and integration are not claimed by this record; it authorizes no
merge.

### Delivery authorization and intended integration

After the PR reached `verified_pr`, the current user explicitly authorized only
this Parent integration with “bringe das pr 215 in den master”. The authorized
inventory is therefore `Easton97-Jens/ModSecurity-conector` PR #215 only; it
does not include Framework, MRTS, Gitlinks, or another PR. The protected
`master` ruleset requires a pull request, resolved review threads, and its six
listed status checks, but zero approving reviews. It permits merge, squash, and
rebase methods. The two most recent matching Parent integrations (#214 and
#212) are merge commits, so the intended method is a SHA-bound merge commit.
The final head, merge result, and resulting-master evidence must be observed
and retained by the integration task rather than asserted in this pre-merge
record.
