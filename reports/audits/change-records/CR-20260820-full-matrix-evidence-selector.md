# CR-20260820 — Constrain full-matrix evidence summary selection

**Language:** English | [Deutsch](CR-20260820-full-matrix-evidence-selector.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260820-full-matrix-evidence-selector` |
| Date (UTC) | 2026-08-20 |
| Base revision | `ab9cb2c276f159397ec2558b2d58cc260fd66ce2` |
| Finding | `FND-PARENT-0197` |
| Scope | Parent evidence generator and Parent regression tests only |
| Framework boundary | Gitlink and nested `HEAD` remain `bd69ee96e0e7082317d4afe1232bee625665eb9a`; no Framework source or Gitlink change |
| Delivery disposition | A later current user request authorizes one Parent Draft PR. At this record revision, commit, PR, and hosted-check facts are pending observation; the PR lifecycle/task completion record retains them without a self-referential commit loop. |

## Motivation and problem statement

The full-matrix completeness generator accepted a raw job-local `summary.path`
value before its later strict report-evidence gate. That value could select a
process-readable file outside the fixed job root and reach summary parsing plus
`file_record()` metadata/hash handling. The issue is a Parent evidence-
integrity boundary, not a connector host-runtime claim.

## Acceptance criteria

- An external `summary.path` selector cannot change the selected summary path.
- A traversal-form selector cannot change the selected summary path.
- A direct canonical summary remains selectable.
- The owning generated-report evidence-integrity suite passes.
- The repair remains Parent-only, starts no host runtime, changes no
  Framework/MRTS source or Gitlink, and uses only the separately authorized
  normal Parent delivery path.

## Implementation decision and rationale

`summary_path()` no longer reads the legacy `summary.path` indirection. It now
selects only existing fixed candidates beneath the job root, preserving the
direct canonical `results/` fallback and the existing `force-all/` candidate.
Removing the unsafe selector is smaller and more fail-closed than attempting
to retroactively validate an arbitrary path after it was read.

The regression suite adds the original external-selector case, a traversal
variant, and a legitimate direct-canonical-summary control. No generated
artifact was edited directly.

## Security impact

`FND-PARENT-0197` is a Parent P2, medium-severity, confirmed
`security_validated` finding. Primary CWEs are `CWE-73` (external control of
file name or path) and `CWE-22` (traversal-form variant). A job-evidence
producer that can write `job_root/summary.path` could previously cause the
local generator to read and hash a process-readable arbitrary file before the
later gate. The retained reproduction used only an empty benign JSON fixture;
no secret, request, response, cookie, Authorization value, or raw log was
read or retained.

## Changed files

- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `tests/test_generated_report_evidence_integrity.py`
- this English/German Change Record pair
- the paired Change-Record archive indexes

## Commands executed

All commands ran locally with RTK mediation. Private temporary-directory paths
are intentionally represented as `<private-task-root>`.

- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<private-task-root>/test .venv/bin/python -m unittest -v tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_summary_selector_rejects_external_override tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_summary_selector_rejects_traversal_override tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_summary_selector_keeps_canonical_direct_summary` — exit `0`; original external selector rejected, traversal alternate rejected, direct canonical control selected.
- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<private-task-root>/test .venv/bin/python -m unittest -q tests.test_generated_report_evidence_integrity` — exit `0`; `Ran 82 tests in 54.396s`, `OK`, `check-generated-report-layout: PASS`.
- `make check-common-security-contract check-common-flow-integrity check-directive-parity check-bilingual-docs` — exit `0`; the audit's relevant static Parent contracts passed.
- `make check-common-memory-safety check-common-http-header-fuzz` with a registered private `BUILD_ROOT` — exit `0`; bounded memory-safety and 15-second header fuzz checks passed.
- `git diff --check` — exit `0` before final documentation validation; no whitespace error observed.
- Focused `check_change_record_pair` plus `structural_pair_errors` from `ci/checks/documentation/check-bilingual-docs.py` — exit `0`; the new pair has required headings, matching identity fields, language switches, and structural parity.
- `make check-bilingual-docs` was started after the new pair was added, but emitted no diagnostic and was interrupted after approximately five minutes with exit `130`; it is not counted as a pass.
- `make check-bilingual-docs` in the isolated delivery worktree — exit `2`;
  repository-wide pre-existing documentation links require the uninitialized
  Framework submodule. No Framework initialization occurred because
  `SUBMODULE_SCOPE=METADATA_ONLY`; this is a blocked broad documentation
  prerequisite, not a Change-Record pair failure.

## Runtime evidence

There is no host-runtime evidence. `RUNTIME_AUTHORIZED=false` prohibits
starting Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd hosts. The local
proof is limited to source behavior and the owning Python test suite.

Payload-safe receipts are retained in external run
`20260820T000000Z-defensive-security-audit-770d35c` as
`evidence/evidence-selector-baseline.md` (SHA-256
`26e708ad3a51e7b42401fc4f615df40bd3efa2b25eab11c9b2a253c255a11d1c`) and
`evidence/evidence-selector-remediation.md` (SHA-256
`751cf0616d6dc1e4ac9ab78fd16522694b75e9e8add04adb4b7f813ea528b953`).

## Checks not run and rationale

- `make check-doc-links` was not run because it invokes `check-framework` and
  a Framework documentation checker; `SUBMODULE_SCOPE=METADATA_ONLY` excludes
  Framework content from this audit.
- The full post-change `make check-bilingual-docs` validator is not a passing
  result: the original run was interrupted after no progress or diagnostic
  output, and the fresh isolated-worktree run returned `2` because it lacks
  Framework content required by pre-existing links. The focused Change-Record
  contract/parity check above is the strongest completed alternative.
- `make check-ci-security-contract` was not run during the original audit:
  its test set exercises temporary Git-write behavior outside that audit's
  authorization. The later normal delivery authorization does not retroactively
  make it a selector regression, so it remains not run.
- Full connector lifecycle, build, configuration-load, and host smoke checks
  were not run because `RUNTIME_AUTHORIZED=false`.
- Networked scans and downloads were not run under the original
  `NETWORK_AUTHORIZED=false` audit boundary. The later delivery extension
  authorizes only normal GitHub delivery; hosted PR checks are pending actual
  observation and are not asserted here.

## Known limitations

The audit is source-based and does not prove every report consumer, deployment
path, or connector host behavior. The currently initialized Framework checkout
has parallel dirty changes outside this task; only its Gitlink and `HEAD` were
reviewed, and no Framework contents were changed or attributed here.

## Remaining risks

The correction confines this legacy summary selector only. Other report inputs,
host runtime behavior, hosted workflow semantics, and networked scanner results
remain outside the authorized evidence. `FND-PARENT-0197` is locally `fixed`,
not delivery-verified or closed.

## Final diff and review status

The final review at this record revision is limited to the observed local diff,
source-to-sink reproduction, focused regressions, the 82-test owning suite,
static Parent contracts, evidence checksums, and the focused Change-Record
documentation contract. The separately authorized Draft-PR lifecycle retains
actual branch, commit, PR-head, hosted-check, and review facts only after they
are observed. No merge, resulting-master validation, Framework change, MRTS
change, or Gitlink update is claimed.
