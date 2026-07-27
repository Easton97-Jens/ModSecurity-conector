# Change Record: Parent report-generator conditionals and access-log regex for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260727-sonar-report-conditionals-regex.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-report-conditionals-regex |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud `python:S3358` Code Smells AZ9cRyi6HhV2CayPTPyU, AZ9cRyi6HhV2CayPTPyV, AZ9cRyiqHhV2CayPTPyD, AZ9cRyiqHhV2CayPTPyE, AZ9cRyiqHhV2CayPTPyF, AZ9cRyiqHhV2CayPTPyG, AZ9cRyiqHhV2CayPTPyH, AZ9cRyiqHhV2CayPTPyI, AZ9cRyiqHhV2CayPTPyJ, AZ9cRyiqHhV2CayPTPyK, AZ9cRyiqHhV2CayPTPyL, AZ9cRyiqHhV2CayPTPyM, AZ9cRyiqHhV2CayPTPyO, AZ7POyVcBW70q7L2nMJZ, AZ7POyVcBW70q7L2nMJb, AZ7POyVcBW70q7L2nMJc, AZ7POyVcBW70q7L2nMJd, AZ7POyVcBW70q7L2nMJe, AZ7POyVcBW70q7L2nMJf, AZ7HxAmX_i61V0DF6_GO, AZ7HxAmX_i61V0DF6_GR, AZ7HxAmF_i61V0DF6_GH, AZ7HxAne_i61V0DF6_Gk, AZ7HxAlw_i61V0DF6_GD, AZ7HxAoH_i61V0DF6_G0, and AZ7HxAoH_i61V0DF6_G2; and `python:S8786` AZ8hz86oUa5zTy8Lzy9R. |
| Boundary | Nine Parent report-generator modules, one Parent in-memory regression suite, this English/German Change Record pair, and their indexes. Generated reports, report-generator mains, workflows, Makefiles, scanner configuration, Quality Gates, suppressions, external Sonar/GitHub state, Framework/MRTS content, Gitlinks, and delivery remain unchanged. |

## Motivation and problem statement

Twenty-six current `python:S3358` findings use nested conditional expressions
inside report-generation and rendering logic. Their priorities and lazy
fallbacks must stay exact when made readable. Separately, `access_status()`
used a backtracking regular expression over NGINX access-log request text.
The receipt `AZ8hz86oUa5zTy8Lzy9R` identifies super-linear worst-case work on
malformed repeated `HTTP/` fragments.

## Acceptance criteria

- Replace exactly the 26 receipt-mapped nested conditional expressions with
  equivalent ordered branches.
- Preserve fallback order, lazy f-string construction, report status strings,
  quoted action parsing, and existing report/evidence semantics.
- Replace only the `access_status()` request/status regex with bounded linear
  parsing while retaining valid combined-log status extraction and malformed
  record rejection.
- Add focused regression coverage and retain existing evidence-integrity and
  presentation contracts.
- Maintain this English/German Change Record pair and indexes without adding
  generated reports, workflow, Framework, MRTS, Gitlink, or delivery changes.

## Implementation decision and rationale

The `python:S3358` expressions now use local `if`/`elif` decision trees in
the original priority order. The missing-job fallback still reads the
secondary record only when the primary value is not a list, and the
incomplete-matrix message is still formatted only in its selected branch.
Quote-state handling preserves its previous close/open/retain transition.

`access_log_status()` scans quote-delimited request fields once, validates the
same request and three-digit status shape, and returns the first valid status
from each line without invoking `re.search()`. `access_status()` retains its
date filter and last-status selection. The separate `re.match()` used for
evidence-path recognition is unchanged.

## Changed files

- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-connector-roadmap.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `ci/evidence/reports/refresh-connector-reports.py`
- `tests/test_report_conditional_remediation.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_report_conditional_remediation` passed: 5 tests.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_generated_report_evidence_integrity` passed: 74 tests, including `check-generated-report-layout: PASS`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_report_presentation_literals` passed: 3 tests.
- The three suites passed 82 tests in total. An AST review found zero nested `IfExp` nodes in each of the eight S3358-mapped source files.
- The source/test candidate `git diff --check` passed before this Change Record pair was added.
- After a read-only checkout of the Parent-pinned Framework revision
  `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`, `rtk proxy env
  PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` passed:
  `bilingual docs ok`, `repository path references: PASS`, and `doc links ok`.

## Corrective follow-up after hosted analysis

The original Draft PR [#138](https://github.com/Easton97-Jens/ModSecurity-conector/pull/138)
head `e522e43f0957368853772d747a0ffaa38ba76615` received a SonarQube Cloud
Quality Gate error: `new_duplicated_lines_density` was `5.649717514124294%`
against a maximum of `3%`, with 20 new duplicated lines. The five repeated
four-line quote-state blocks caused those duplicates. Sonar also reported
`python:S3776` receipt `AZ-lYOLSGYV1PN-Q1gW4` in
`generate-verified-runtime-mismatch-analysis.py` because `command_summary()`
had cognitive complexity 16 against the maximum 15.

The local corrective candidate keeps this PR independent of other branches:
each quote transition is now one non-nested statement, and the pure
runtime-status choice moved to `full_runtime_status()`. Its local focused
tests pass 6 report-conditional, 74 evidence-integrity, and 3 presentation
tests (83 total); `git diff --check`, bilingual documentation, and document
link checks also pass. The added tests cover both quote directions within an
active value, unterminated input, all status outcomes, `{0, None}` as
non-mismatches, and both lazy short-circuits. A fresh exact-head hosted scan
is still required before claiming that the Quality Gate or receipt is clear.

## Security impact

`AZ8hz86oUa5zTy8Lzy9R` is a localized availability/performance candidate in a
Parent report generator: client-derived request text can be recorded by NGINX,
then later read from test evidence by `read_lines()` and passed to
`access_status()`. The correction removes the unbounded backtracking search
from that source-to-sink path without changing input paths, safe-root/output
controls, report provenance, status semantics, subprocesses, network access,
or publication. The 26 readability-only branch changes do not relax a
security control.

## Runtime evidence

The pre-change malformed input took 0.000653 s, 0.002457 s, and 0.009628 s
for 200, 400, and 800 repeated `HTTP/` segments. The candidate parser returned
`None` in 0.000003 s, 0.000002 s, and 0.000002 s for the same inputs. It
matched the prior regex output for seven targeted compatibility cases and
10,000 deterministic generated cases. The focused suite also verifies valid
combined-log extraction, malformed-line rejection without `re.search()`, and
last-status selection. No connector, report-generator main, output writer,
Framework, MRTS, or host runtime was run.

## Known limitations

The local Parent interpreter is Python 3.14.4 while the CI version-file
contract is Python 3.14.6, so this is same-minor local evidence. The current
worktree is an uncommitted candidate based on
`1b0f8825f3510b99b603bb6cd6f0777e1710358e`; it changes no external
SonarQube Cloud state.

## Remaining risks

The parser replacement could differ on unusual malformed quote sequences.
The direct valid/malformed controls and 10,007 comparison cases reduce that
risk, but a fresh exact delivered-head SonarQube Cloud analysis is still
required before the listed receipts can be treated as externally resolved.

## Checks not run and rationale

- Full report generation and the full runtime matrix were intentionally not
  run because they can read or write evidence and require runtime/Framework
  inputs outside this focused source/test batch.
- No GitHub CI, SonarQube Cloud PR analysis, review, pull request, merge, or
  default-branch update has occurred.

## Final diff and review status

The candidate is local, uncommitted, and unpushed. It has no staging, commit,
push, pull request, MRTS, or Gitlink action. The Parent-pinned Framework was
initialized read-only only for documentation checks; its source, Gitlink, and
nested MRTS state remain unchanged. Parent delivery and the exact-head hosted
SonarQube Cloud analysis remain separate steps.

At the time of this corrective note, the initial candidate remains Draft PR
#138 while the follow-up is locally uncommitted and unpushed. The failed
initial analysis is negative evidence only; it does not establish the status
of the corrected head.
