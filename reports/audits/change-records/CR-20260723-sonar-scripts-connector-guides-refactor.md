# Change Record: Parent connector-guide renderer decomposition for SonarQube Cloud S3776 and S1481

**Language:** English | [Deutsch](CR-20260723-sonar-scripts-connector-guides-refactor.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-scripts-connector-guides-refactor |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Parent `python:S3776` `AZ9cRzBCHhV2CayPTP5L`, `python:S1481` `AZ9cRzBCHhV2CayPTP5K`, and the two PR-created `python:S1172` rows `AZ-Qn4qN18-5KNpatmRP`, `AZ-Qn4qO18-5KNpatmRQ` in `scripts/generate_connector_guides.py`. |
| Boundary | Parent generator/test and this English/German Change Record pair plus indexes. Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, and checked-in connector documentation content remain unchanged. |

## Motivation and problem statement

SonarQube Cloud reports that `content()` has cognitive complexity 38 where 15
is allowed, and that its local `suffix` variable is unused. The function
combines common setup, eight document-kind renderers, bilingual handling, and
final structural-parity conversion, making future edits difficult to review.

## Decision

Keep `content()` as the public rendering seam but dispatch it to small
document-kind helpers. Move the shared title/scope setup and German label
conversion into named helpers and constants. Remove the unused local. Add a
focused regression test that proves all six connectors × eight document kinds
× two languages retain the current deterministic aggregate SHA-256 and that
`main()` writes exactly the same 96 files into a controlled temporary root.
Wire that regression into the existing `lint` contract. After the first exact
Draft-PR analysis surfaced two unused private-helper parameters introduced by
the decomposition, remove only those parameters and their matching dispatch
arguments.

## Scope and non-goals

The source change reorganizes only `scripts/generate_connector_guides.py` and
adds `tests/test_connector_guides.py`. It does not change a rendered string,
path layout, document kind, language pairing, file encoding, connector input,
checked-in documentation, subprocess, network action, security control,
Sonar rule/profile, Quality Gate, Framework, MRTS, or gitlink.

The Change Record and its German companion are the only versioned documentation
changes. The shared indexes are updated for traceability. No merge or
default-branch write is part of this change.

`Makefile` receives only the named test target and its `lint` invocation. The
task branch also contains a normal synchronization merge of current `master`;
the sole conflict combined the two bilingual Change Record index entries. That
merge neither changes `master` nor rewrites published history.

## Output compatibility and test boundary

The pre-edit and post-edit aggregate digest is
`b98dae8bd83ebb0ee3f6694269b29d0ee1f97a26ec7aba8aaa054eac749d4728` for
exactly 96 renders. The permanent test calculates the same keyed digest and
also patches the generator root only inside `TemporaryDirectory`; it compares
every generated file byte-for-byte to `content()` output and asserts exactly
96 Markdown files. It never calls `main()` against the checkout.

## Security and compatibility

This is controlled documentation-rendering refactoring. It does not introduce
or change untrusted input, user-selected paths, subprocesses, credentials,
network access, privileges, memory safety, or host runtime enforcement. The
temporary output root remains test-owned and is removed by the standard
temporary-directory context. No security workflow is triggered by this delta.

## Validation and delivery status

The focused renderer test, `make check-connector-guides`, in-memory syntax
compilation, output digest comparison, AST dispatch inspection, and diff check
passed locally. Targeted bilingual-documentation tests passed. The full
documentation/link commands are blocked only by pre-existing missing
Framework-gitlink targets and emitted no task Change Record error. The first
exact-head Draft-PR analysis passed its Quality Gate and removed the original
two rows, but found two task-introduced unused private-helper parameters. Their
focused follow-up is locally validated; fresh exact-head hosted and SonarCloud
results are pending.

## Acceptance criteria

- Remove the unused `suffix` local, the two task-introduced unused
  private-helper parameters, and decompose the flagged `content()` ladder
  without a suppression or scanner configuration change.
- Preserve all 96 keyed rendered outputs exactly and write exactly those files
  only in a controlled temporary test root.
- Run that output regression through the named repository `lint` target.
- Keep both Change Record languages and both indexes equivalent.
- Obtain exact Draft-PR-head SonarQube Cloud and hosted-check evidence before
  calling either selected key resolved.

## Implementation decision and rationale

The public `content()` seam now computes its partner name and delegates to a
small renderer dispatch. Each document kind has a focused helper with only the
inputs it uses; the two initially redundant helper inputs were removed after
the first PR analysis. `_finish_content()` retains the existing German structural
parity conversion. A global document-kind tuple is shared by the dispatch,
writer, and test to keep the 96-output contract explicit.

## Changed files

- scripts/generate_connector_guides.py
- tests/test_connector_guides.py
- Makefile
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- Focused `tests.test_connector_guides`: passed (2 tests).
- `make check-connector-guides`: passed (2 tests) and is invoked by `lint`.
- In-memory syntax compilation: passed (2 Python files).
- Renderer output parity: passed (96 renders, recorded SHA-256).
- AST dispatch inspection: passed; `content()` has no branch node, all eight
  renderer helpers exist, and no `suffix` assignment remains.
- `tests.test_bilingual_docs`: passed (11 tests; 13 combined focused tests).
- `git diff --check`: passed.
- Full documentation/link checks: blocked only by known missing
  Framework-gitlink targets; no task Change Record error was emitted.
- First Draft-PR SonarCloud analysis: Quality Gate `OK`; the original two rows
  are absent, but it found two task-introduced `python:S1172` rows.
- Fresh full Draft-PR-hosted/SonarCloud analysis: pending for the focused
  S1172 follow-up head.

## Security impact

No security behavior changes. The temporary output test constrains writes to a
test-owned `TemporaryDirectory`, and the generator is not run against the
checkout during validation. No security finding is claimed fixed.

## Runtime evidence

No connector runtime behavior changed or was claimed. This is an offline
documentation-generator and unit-test change, not a host/runtime deployment or
a Framework/MRTS run.

## Known limitations

This batch addresses the two selected SonarQube Cloud observations and the two
directly task-introduced S1172 observations. It
does not claim to clear the broader SonarCloud backlog or validate connector
builds, host configurations, or production documentation deployment.

## Remaining risks

A future renderer edit could unintentionally change generated text or output
layout. The keyed 96-render digest and temporary-tree byte comparison reduce
that risk; fresh hosted exact-head analysis remains required before delivery is
verified.

## Checks not run and rationale

- No connector build or runtime matrix: the delta is pure controlled
  documentation rendering and its complete focused unit test passes.
- No Framework or MRTS test or modification: both are excluded from this
  Parent-only task.
- Full documentation checks: will be run after the bilingual Change Record
  pair is present; known Framework-gitlink blockers will be retained if they
  are the only observed failures.
- Fresh full hosted checks and SonarQube Cloud PR analysis: a Draft PR exists,
  but its S1172 follow-up head still requires a new exact-head analysis.

## Final diff and review status

The local generator refactor, output-compatibility validation, named lint
target, and targeted documentation validation are complete on the Parent-only
task branch. The exact Draft PR exists and remains unmerged. Hosted checks,
Sonar analysis, and the Quality Gate must be restarted for the focused S1172
follow-up head. No review approval, PR merge, or default-branch change is
claimed or authorized.
