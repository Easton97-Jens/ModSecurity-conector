# Change Record: Prevent recurring Change Record contract failures

**Language:** English | [Deutsch](CR-20260929-change-record-prevention.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260929-change-record-prevention |
| Date (UTC) | 2026-09-29 |
| Base revision | `d62e0427a1cdbe4e4f0f95dec8053187046dfc6e` |

## Motivation and problem statement

The user requested prevention of recurring Change Record CI failures and correction
of the SonarQube findings in PR #393. The previous documentation-only correction
fixed 19 heading/identity diagnostics, but the reader-facing traceability policy
still suggested synonyms which the unchanged bilingual checker does not accept.
This follow-up removes that authoring trap rather than weakening the checker.

## Acceptance criteria

The new creator must derive both language skeletons from the existing checker,
validate them before writing, and preserve existing files. The policy must list
the exact checked headings and identity labels. A read-only archive check and
regressions must run before framework setup in quick-framework-check. Existing
full checks, permissions, pins, and repository boundaries must remain unchanged.
The separate request to fix the two Sonar findings remains blocked until their
actual rules and locations can be retrieved; this record does not claim it met.

## Implementation decision and rationale

Add a standard-library-only creator and early checker. The creator loads the
repository-owned bilingual checker from its fixed sibling location, derives
headings and identity labels from its existing constants, and calls its existing
pair/structure checks before opening outputs. Names, dates, and full base SHAs
are validated. Existing archive directories are opened with directory descriptors
and no-follow flags; exclusive creation does not overwrite existing records.
On a handled creation failure, rollback removes only outputs whose recorded
device/inode identity still matches. There is no crash-atomic pair guarantee.

The early read-only check reuses the same checker functions, also rejecting
missing companions and symlink files. It checks structure, not whether prose
contains adequate evidence. Correct the policy in both languages and test its
literal tables against the same canonical definitions. The existing workflow
gains one read-only step running the archive check and both test modules before
make setup-dev. The original full quick-check and documentation checks remain.

## Changed files

- `ci/tools/new-change-record.py`
- `tests/test_change_record.py`
- `docs/change-traceability.md`
- `docs/change-traceability.de.md`
- `.github/workflows/quick-framework-check.yml`
- `reports/audits/change-records/CR-20260929-change-record-prevention.md`
- `reports/audits/change-records/CR-20260929-change-record-prevention.de.md`

## Commands executed

In-process Python 3.13.5 validation in an isolated fixture passed all 39 tests:
20 new Change Record tests and the 19 unchanged handoff-generator tests.
The new tests used the applicable unchanged checker definitions extracted from
the fetched source, not a full repository checkout. Original policy/workflow and
unchanged handoff source/test bytes were verified against their Git blob hashes.

Before the policy/wiring change, the regression found 60 missing canonical
heading/label literals across the two policies, and the early workflow step was
absent. After the change, all 39 tests passed. Negative cases cover every required
heading/identity label, differing identities, language/code parity, invalid input,
existing outputs, symlink paths, rollback, absent/empty archives, and schema drift.
AST parsing, whitespace/final-newline checks, and policy EN/DE structural parity
passed. YAML parsing confirmed that removing the single added step reproduces
the original workflow configuration exactly.

The following are repository-native validation payloads for the real checkout,
not a claim that they were executed locally through the unavailable RTK wrapper:

```sh
python3 ci/tools/new-change-record.py check
python3 -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff
make check-bilingual-docs
make check-doc-links
git diff --check
```

## Security impact

No checker rule, Quality Gate, exclusion, suppression, permission, dependency
pin, Framework/MRTS source, or gitlink is changed. The helper executes no shell or
network command and does not invoke Git. The creator is an explicit local write
operation confined to derived record filenames in an existing trusted checkout;
the CI path invokes only its read-only check. Never use structural success as
security, test-evidence, or runtime approval.

## Runtime evidence

None. This change concerns authoring and CI structure only. No native connector
build, host runtime, or original Framework handoff repair is claimed.

## Known limitations

The creator requires POSIX directory-descriptor/no-follow support and an
existing record directory. Its output is intentionally unfinished prose that
must be replaced with actual facts. The checker cannot prove factual correctness.
The isolated validation is not a repository-native or pinned Python 3.14.7 run.
The original Framework candidate repair in PR #393 is still preparation-only.

## Remaining risks

Future authors can still bypass the creator or change mandatory headings; CI
will reject such records rather than silently normalize them. Process termination
between the two creations can leave a partial pair, which the early check rejects.
Full-checkout, current-head CI and Sonar results require their own fresh evidence.

## Checks not run and rationale

No local full-checkout execution, full bilingual/link suite, pinned Python run,
or Sonar analysis was performed. GitHub DNS from the local environment, RTK,
the canonical sonar-with-env launcher, and a Sonar CLI/MCP were unavailable.

The current-head GitHub Sonar check 109566898629 reported a passed Quality Gate
with two new findings at the base revision above. The connection rejected its
annotations endpoint, and no actionable rule/file/line details were available.
Therefore no speculative Sonar source fix, suppression, or issue disposition was
made. A passed gate does not establish that those two findings were corrected.

## Final diff and review status

The scoped source, tests, policy pair, and single workflow-step diff were
reviewed before publication. Isolated tests and syntax/parity checks passed.
Successor hosted checks were not available when this record was authored.
The Sonar remediation request remains blocked and the original handoff repair
remains unapplied. No merge, master write, or history rewrite is authorized.
