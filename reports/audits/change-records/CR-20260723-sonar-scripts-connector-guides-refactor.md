# Change Record: Parent connector-guide renderer decomposition for SonarQube Cloud S3776 and S1481

**Language:** English | [Deutsch](CR-20260723-sonar-scripts-connector-guides-refactor.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-scripts-connector-guides-refactor |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Parent `python:S3776` `AZ9cRzBCHhV2CayPTP5L` and `python:S1481` `AZ9cRzBCHhV2CayPTP5K` in `scripts/generate_connector_guides.py`. |
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

## Scope and non-goals

The source change reorganizes only `scripts/generate_connector_guides.py` and
adds `tests/test_connector_guides.py`. It does not change a rendered string,
path layout, document kind, language pairing, file encoding, connector input,
checked-in documentation, subprocess, network action, security control,
Sonar rule/profile, Quality Gate, Framework, MRTS, or gitlink.

The Change Record and its German companion are the only versioned documentation
changes. The shared indexes are updated for traceability. No merge or
default-branch write is part of this change.

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

The focused renderer test, in-memory syntax compilation, output digest
comparison, AST dispatch inspection, and diff check passed locally. Targeted
bilingual-documentation tests passed. The full documentation/link commands are
blocked only by pre-existing missing Framework-gitlink targets and emitted no
task Change Record error. Full hosted and SonarCloud exact-head results remain
pending until a separate unmerged Draft PR exists.

## Acceptance criteria

- Remove the unused `suffix` local and decompose the flagged `content()`
  ladder without a suppression or scanner configuration change.
- Preserve all 96 keyed rendered outputs exactly and write exactly those files
  only in a controlled temporary test root.
- Keep both Change Record languages and both indexes equivalent.
- Obtain exact Draft-PR-head SonarQube Cloud and hosted-check evidence before
  calling either selected key resolved.

## Implementation decision and rationale

The public `content()` seam now computes its partner name and delegates to a
small renderer dispatch. Each document kind has a focused helper with only the
inputs it uses; `_finish_content()` retains the existing German structural
parity conversion. A global document-kind tuple is shared by the dispatch,
writer, and test to keep the 96-output contract explicit.

## Changed files

- scripts/generate_connector_guides.py
- tests/test_connector_guides.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- Focused `tests.test_connector_guides`: passed (2 tests).
- In-memory syntax compilation: passed (2 Python files).
- Renderer output parity: passed (96 renders, recorded SHA-256).
- AST dispatch inspection: passed; `content()` has no branch node, all eight
  renderer helpers exist, and no `suffix` assignment remains.
- `tests.test_bilingual_docs`: passed (11 tests; 13 combined focused tests).
- `git diff --check`: passed.
- Full documentation/link checks: blocked only by known missing
  Framework-gitlink targets; no task Change Record error was emitted.
- Full Draft-PR-hosted/SonarCloud analysis: pending because no Draft PR exists
  yet.

## Security impact

No security behavior changes. The temporary output test constrains writes to a
test-owned `TemporaryDirectory`, and the generator is not run against the
checkout during validation. No security finding is claimed fixed.

## Runtime evidence

No connector runtime behavior changed or was claimed. This is an offline
documentation-generator and unit-test change, not a host/runtime deployment or
a Framework/MRTS run.

## Known limitations

This batch addresses only the two selected SonarQube Cloud observations. It
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
- Full hosted checks and SonarQube Cloud PR analysis: no Draft PR exists yet.

## Final diff and review status

The local generator refactor, output-compatibility validation, and targeted
documentation validation are complete on the Parent-only task branch. Hosted
checks, Sonar analysis, and the Quality Gate remain pending until the separate
unmerged Draft PR is pushed. No review approval, merge, or default-branch
change is claimed or authorized.
