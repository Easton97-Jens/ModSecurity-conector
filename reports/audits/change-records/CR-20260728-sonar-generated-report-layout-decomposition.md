# Change Record: Parent generated-report layout decomposition for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260728-sonar-generated-report-layout-decomposition.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-generated-report-layout-decomposition |
| Date (UTC) | 2026-07-28 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud `python:S1192` receipts `AZ7K5CRYixFPtcnbna1Q`, `AZ7POyU1BW70q7L2nMJQ`, and `AZ7POyU1BW70q7L2nMJR`; plus `python:S3776` receipts `AZ7K5CRYixFPtcnbna1U`, `AZ7K5CRYixFPtcnbna1V`, `AZ7K5CRYixFPtcnbna1X`, `AZ7K5CRYixFPtcnbna1Y`, and `AZ7Tenm9HrNUCHtbhYSD`. |
| Boundary | Parent report-layout checker and its existing integrity tests only. Framework was inspected read-only at Parent-pinned `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; MRTS, Gitlinks, generated reports, runtime evidence, workflows, scanner policy, suppressions, and external SonarQube Cloud issue state are unchanged. |

## Motivation and problem statement

The selected checker contains repeated immutable literals and five large
orchestrators that SonarQube Cloud reports as maintainability debt. It is also
a fail-closed consumer of generated-report and runtime evidence, so the
refactor must remove only structural duplication and complexity without
relaxing any trust, hash, receipt, revision, symlink, or strict-evidence
control.

## Acceptance criteria

- Replace only the three repeated `python:S1192` literals with immutable
  module constants while preserving their exact values and gates.
- Split the five selected `python:S3776` orchestration paths into narrow
  private helpers without changing their errors, ordering, early returns, or
  control predicates.
- Preserve critical-input validation, aggregate-receipt and revision binding,
  descriptor-bound reads, stability revalidation, strict-evidence semantics,
  and the `--governance-only` distinction.
- Pass the focused evidence-integrity suite and governance check; do not
  regenerate runtime evidence merely to make the strict gate pass.
- Keep the candidate Parent-only and defer any hosted Sonar conclusion until
  an exact Draft-PR head has been observed.

## Implementation decision and rationale

The change introduces immutable constants for the in-progress system-proof
environment key, its exact value, and the generated-report filename prefix.
It extracts pure helpers for system-proof Markdown/JSON content,
legacy-reference candidate collection, HTTPS repository URL policy scanning,
registry-output checks, and completed/incomplete runtime diagnostics.

The sensitive primitives remain in their original control paths:
`is_within`, `has_symlink_component`, `is_regular_file`,
`validate_critical_input_record`, aggregate-receipt/command-receipt checks,
revision binding, and aggregate-receipt stability validation. The refactor
does not add a bypass, report refresh, scanner suppression, or change to a
connector or runtime contract.

## Changed files

- ci/checks/documentation/check-generated-report-layout.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_generated_report_evidence_integrity`
- `make report-governance`
- `make check-generated-report-layout`
- `make check-bilingual-docs check-doc-links`
- `make lint`
- `PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/build/report-layout-pycache /root/git/ModSecurity-conector/.venv/bin/python -P -m py_compile ci/checks/documentation/check-generated-report-layout.py`
- `git diff --check`

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused generated-report evidence-integrity suite | passed: 74 tests in 19.734 seconds. |
| `make report-governance` | passed: the runtime path-policy self-test correctly rejected its intentional unsafe/read-only cases, and governance-only report-layout validation passed. |
| Strict `make check-generated-report-layout` | blocked_environment: the checker failed closed because the task environment lacks current sealed build receipts and report inputs; no runtime evidence was refreshed or rewritten. |
| `make check-bilingual-docs check-doc-links` | passed: bilingual documentation, repository path references, and Framework-provided documentation links passed. |
| Broad `make lint` | blocked_environment: shell/Python syntax, 85 runtime/cache-contract tests, and Apache structure checks passed, but the unrelated native `check-apache-c17-lint` stage produced no output for more than five minutes and the task-owned process was interrupted; no overall pass is claimed. |
| Changed-checker `py_compile` | passed. |
| `git diff --check` | passed: no whitespace error. |
| Focused post-diff security review | passed: no security-relevant behavior drift or plausible finding was identified. |

## Security impact

The change touches a Python evidence-consumer boundary and received a focused
security review. It preserves trusted-root, regular-file, symlink, hash,
receipt, canonical-path, revision, and stability controls, as well as the
strict fail-closed result path. No security control, Quality Gate, scanner
rule, suppression, access boundary, connector, or runtime behavior is
weakened. The review observed a separate low-confidence generated-report
symlink-alias idea but did not reproduce it; it is not silently folded into
this maintainability refactor.

## Runtime evidence

No connector, host, protocol, or production runtime evidence was generated or
changed. The focused suite and governance check are source/documentation
contract evidence only. The unavailable strict evidence state is intentionally
reported as blocked rather than replaced with regenerated artifacts.

## Known limitations

The strict layout gate cannot complete locally without current sealed runtime
receipts and their bound report inputs. The broad `make lint` command reached
an unrelated native Apache C17 stage that produced no output for more than
five minutes, so the task-owned process was safely interrupted and is not
claimed as passed. Hosted GitHub and SonarQube Cloud evidence does not yet
exist for this unpublished candidate head.

The interrupted lint process had one clearly task-owned
`check-apache-c17-lint` child still running. It was identified by its exact
candidate-worktree command, terminated with `SIGTERM`, and a subsequent
read-only process check found no remaining task-owned lint process. The lint
run's generated cache-report edits and temporary snapshot scripts were
restored or removed before final diff review and are not part of this change.

## Remaining risks

Helper extraction can accidentally alter an exception, error-order, or early
return edge case. The existing 74-case integrity suite, governance check,
static diff review, and focused security review reduce that risk, but an
exact-head hosted analysis remains necessary before any receipt is declared
resolved. The separate symlink-alias idea needs a distinct reproducibility
task before it can become a finding or hardening change.

## Checks not run and rationale

- No report refresh, runtime matrix, connector build, protocol matrix, or
  MRTS check was run: the selected change is a Parent checker refactor and
  does not alter connector/runtime behavior; regenerating evidence would
  violate the task boundary.
- The strict gate was attempted but is blocked by absent/stale sealed evidence,
  as recorded above; governance-only success is not presented as strict proof.
- The broad lint target did not finish because the unrelated native Apache C17
  stage stalled without output; the completed partial checks are recorded, and
  focused checker validation remains the delivery-relevant local evidence.
- No hosted GitHub Actions or SonarQube Cloud analysis has yet run because the
  candidate has not been committed, pushed, or opened as a Draft PR.

## Final diff and review status

Before delivery, the scoped diff contains only the Parent checker and this
traceability/documentation pair/index update. `git diff --check`, the focused
integrity suite, governance check, syntax compilation, and independent
security review have the actual dispositions recorded above. This record does
not claim a commit, push, pull request, hosted check, SonarQube Cloud result,
or master integration; each requires separate exact-head evidence.
