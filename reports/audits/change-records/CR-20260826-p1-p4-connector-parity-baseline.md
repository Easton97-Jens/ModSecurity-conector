# Change Record CR-20260826: P1–P4 connector-parity baseline

**Language:** English | [Deutsch](CR-20260826-p1-p4-connector-parity-baseline.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260826-p1-p4-connector-parity-baseline` |
| Date (UTC) | `2026-08-26` |
| Base revision | `6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` |
| Scope | Parent-only code-near baseline report, its German companion, this paired Change Record, and the bilingual Change-Record archive indexes. No connector source, Framework/MRTS source, Gitlink, dependency, CI/workflow, branch-rule, required-check, or hosted-test configuration change. |

## Motivation and problem statement

The user requested a step-by-step P1–P4 parity program for ten named
connector paths from a separate worktree with a regularly updated PR. The
first deliverable is a truthful current-master gap analysis and execution
plan, not a speculative claim of runtime parity.

This documentation milestone provides the required, evidence-bounded Prompt 1
baseline.

## Acceptance criteria

Its specific acceptance criteria are:

- derives P1–P4 from the common source and vectors rather than redefining it;
- records source/harness entry points, current phase state, and concrete gaps
  for all ten paths;
- keeps response-phase gaps for ext_authz and forwardAuth as required
  architecture work rather than `not_applicable` exceptions;
- separates source wiring from real-host evidence and lists the required
  promotion matrix;
- records overlapping Draft-PR ownership without copying, merging, or
  superseding another branch; and
- preserves CI and all security controls unchanged.

## Implementation decision and rationale

- The report is based on current Parent `master`, not on the overlapping,
  unmerged Draft PRs #344, #345, and #346.
- It names an explicit user decision as the next source-execution gate to
  avoid competing implementations or an unauthorized integration of those
  branches.
- It retains `FND-PARENT-0234` as an existing release-blocking finding and
  labels new SPOP observations only as plausible static candidates pending
  runtime validation.
- The report has a German peer and is retained with this paired Change Record
  under the repository's explicit traceability policy and the user's requested
  PR delivery.

## Security impact

This baseline concerns untrusted request/response processing, local sockets,
process lifecycle, and event integrity. It changes documentation only and
does not modify a security boundary. It preserves bounded event metadata,
body-payload exclusion, loopback/TLS/UDS defaults, validation, fail modes, and
cleanup requirements. No candidate is represented as a validated finding or
as a completed fix.

## Changed files

- `reports/audits/p1-p4-connector-parity-baseline.md`
- `reports/audits/p1-p4-connector-parity-baseline.de.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-parity-baseline.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-parity-baseline.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| Code, capability, harness, and documentation inspection for the ten paths | Passed as a read-only baseline review; the detailed sources and gaps are in the paired report. |
| `make check-bilingual-docs` | Blocked by the task worktree's absent Framework Gitlink content (exit `2`) after the record's required headings were corrected. The repeated output named only pre-existing missing Framework targets, not either new baseline file or Change Record. |
| `make check-doc-links` | Blocked by the same absent Framework Gitlink content (exit `2`); repository path-reference validation reported only existing Framework targets outside this change. |
| `git diff --check` | Passed after the final documentation correction. |
| Connector build, config validation, or real-host P1–P4 matrix | Not run: this is the deliberately documentation-only Prompt 1 milestone; source implementation awaits the overlapping-PR ownership decision. |

## Runtime evidence

An isolated task-owned storage preflight passed for later local builds and
runtime evidence. No build, real host, network listener, connector engine, or
runtime matrix was started for this documentation-only change. Therefore this
record supplies no new runtime claim, no connector promotion, and no hosted
check result.

## Checks not run and rationale

- Connector build, configuration validation, and the real-host P1–P4 matrix
  are intentionally not run in this documentation-only Prompt 1 milestone.
  They require source implementation and an ownership decision about the
  overlapping drafts.
- `make check-bilingual-docs` and `make check-doc-links` both reached the
  absent Framework Gitlink content and exited `2`. Their output named existing
  missing Framework targets only after the new Change Record's required
  headings were corrected. Initializing or altering Framework/Gitlink content
  is outside the selected Parent-only scope, so the failure is recorded as an
  environment limitation rather than worked around.

## Known limitations

The isolated storage preflight is a prerequisite check, not runtime evidence.
This change has neither promoted a connector nor created a replacement for the
required per-path real-host results. The record cannot resolve ownership of
the overlapping Draft PRs or claim their code as part of this branch.

## Remaining risks

The known P1–P4 gaps, `FND-PARENT-0234`, and the unvalidated SPOP candidates
remain. A documentation-only PR cannot reduce the source, transport, resource,
or event-integrity risks identified in the baseline; later changes must keep
the stated controls and verify each result at the exact delivery head.

The final task requires a fresh, run-bound evidence bundle for every named
path. The draft PR created for this milestone remains a Draft; no merge,
direct `master` push, Framework/MRTS modification, Gitlink update, CI change,
or manual hosted-check trigger is authorized or asserted.

## Final diff and review status

The baseline report and this record are ready for local documentation
validation and a narrow review of their final diff. The broader parity program
remains in progress and must not be reported complete until all ten paths meet
the stated real-host acceptance matrix.
