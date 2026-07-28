# Change Record: Parent runtime-mismatch control-path deduplication for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260728-sonar-runtime-mismatch-control-path-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-runtime-mismatch-control-path-deduplication |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Scope and boundary | Parent `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py` and its focused `tests/test_report_conditional_remediation.py`, plus this English/German Change Record pair and its indexes only. Framework, MRTS, both gitlinks, workflows, and generated reports remain unchanged. |
| Finding linkage | Parent SonarQube Cloud runtime-mismatch duplicate-control-path remediation, followed by exact-PR-head code smell `AZ-o2G_i1eeMvlV2C-0t`, rule `python:S1192`, for the repeated `nginx-summary.json` literal. The follow-up candidate does not claim alert closure or delivery completion. |

## Motivation and problem statement

The runtime-mismatch report had repeated composition of the same no-MRTS
control root from `build_root`, the first CRS component of a slash-bearing
variant, and the connector. Keeping those compositions in separate report
paths made maintenance harder and contributed to duplicate control-path code.

The requested remediation centralizes only that existing root composition in
the private `_no_mrts_control_identity` helper. It is deliberately not a
change to what evidence is accepted or how a report is generated.

The first exact Draft PR head then exposed three repeated uses of the NGINX
force-all summary filename in the newly concentrated source region. The
follow-up uses one private named constant for that unchanged filename; it does
not alter any summary location or reader behavior.

## Acceptance criteria

- `_no_mrts_control_identity` preserves the existing slash and first-CRS
  behavior and returns the existing fixed no-MRTS control root only for
  Apache, HAProxy, and NGINX.
- Apache and HAProxy retain their existing result layouts; NGINX retains its
  existing summary traversal.
- The existing pass/`403` gates and NGINX phase-4 marker semantics remain
  unchanged.
- One private NGINX force-all summary filename constant preserves the exact
  existing filename at all three existing reader sites.
- The focused conditional-remediation test control passes all 9 tests.
- The runtime-environment snapshot-contract test control passes all 9 tests
  only in its disposable external overlay using the read-only Parent-pinned
  Framework archive `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`.
- No report generation, `runtime-all`, matrix, Framework/MRTS, hosted, or
  delivery result is claimed.

## Implementation decision and rationale

`_no_mrts_control_identity` receives `build_root`, `connector`, and
`variant`; it rejects a variant without `/` and a connector outside the fixed
Apache/HAProxy/NGINX set. For an accepted variant, it retains the first
component from `variant.split("/", 1)` and returns the pre-existing
`build_root / "full-matrix" / crs / "no-mrts" / connector` root.

`no_mrts_control_evidence`, `no_mrts_case_control_evidence`, and
`nginx_no_mrts_phase4_log_control` consume that identity while retaining their
own result selection and predicates. Apache and HAProxy keep their existing
runtime-result layouts. NGINX keeps its existing summary-file traversal,
including its phase-4 marker handling. The refactor introduces no new
connector route or path broadening.

`NGINX_FORCE_ALL_SUMMARY_FILE` supplies the same `nginx-summary.json` leaf to
each of those three unchanged NGINX summary paths. The focused test asserts
that constant's value while its existing temporary-tree controls exercise all
three consumers.

## Changed files

- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `tests/test_report_conditional_remediation.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Actual result |
| --- | --- |
| Focused conditional-remediation test control (9 tests) | passed. |
| Runtime-environment snapshot-contract test control (9 tests) | passed only in a disposable external overlay using the read-only Parent-pinned Framework archive `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`. |
| `git diff --check` | passed; no whitespace error was reported. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | blocked_environment: it reported 20 missing local targets under the unpopulated Framework gitlink; no diagnostic named this Change Record pair or its indexes. |
| Disposable exact-candidate overlay with the read-only Parent-pinned Framework archive: `check-bilingual-docs.py`, `check-repository-path-references.py`, and Framework `check-doc-links.py` | passed: `bilingual docs ok`, `repository path references: PASS`, and `doc links ok`. |

## Security impact

The report's no-MRTS control-identity selection is an evidence-reclassification
boundary. The focused security review found no validated issue. The change
centralizes the existing fixed root composition and identifies only the
existing Apache, HAProxy, and NGINX routes; it does not broaden a path or add
a new evidence source.

No Framework or MRTS source, gitlink, runtime path, access control, or
generated report is changed by this batch.

## Runtime evidence

The two 9-test controls are local source and snapshot-contract evidence only.
The snapshot-contract result is bounded to its disposable external overlay and
the read-only Parent-pinned Framework archive. It is not evidence of report
generation, `runtime-all`, a connector matrix, a Framework/MRTS runtime, or a
hosted result.

## Known limitations

No report generation, `runtime-all`, connector/CRS matrix, or Framework/MRTS
check was run for this candidate. The preceding exact PR head had an `OK`
Quality Gate and zero new duplication but exposed `AZ-o2G_i1eeMvlV2C-0t`;
fresh hosted proof for the filename-constant follow-up remains required. No
generated report or runtime matrix artifact was created or refreshed.

## Remaining risks

Future changes to the fixed connector set, first-CRS handling, or no-MRTS
control-root composition could reclassify evidence. The focused tests bound
the reviewed behavior, but an unrun report-generation or runtime-matrix path
could expose an integration difference outside this batch.

## Checks not run and rationale

- Report generation was not run; it is outside this duplication-only source
  remediation and no generated report was updated.
- `runtime-all` and matrix checks were not run; their runtime and artifact
  prerequisites are outside the reviewed local source-test scope.
- Framework and MRTS checks were not run. The only Framework material used by
  the snapshot-contract control was the read-only Parent-pinned archive named
  above; no Framework or MRTS worktree, source, branch, or gitlink changed.
- The native `make check-doc-links` target was not run because it would use
  the unpopulated Framework gitlink; the Framework-owned `check-doc-links.py`
  equivalent passed only in the disposable read-only-archive overlay above.
- Hosted checks were not run because this candidate has no delivered
  exact-head review or analysis cycle.

## Final diff and review status

Initial commit `ba8d2b2b9048ccc0d1716cc2d5b689bbe24c64c8` is on Draft PR #152.
Its exact hosted analysis passed the Quality Gate and had zero new duplication,
but reported `AZ-o2G_i1eeMvlV2C-0t`. This candidate adds only the private
filename constant and its focused assertion. The supplied focused test evidence
and `git diff --check` passed before this normal follow-up push; the direct
repository-wide bilingual target was blocked by absent Framework targets, but
the exact-candidate external overlay passed bilingual, repository-path, and
Framework document-link checking. The focused security review found no
validated issue while recording the evidence-reclassification boundary. No
merge, master update, report generation, or final hosted-analysis result is
claimed.
