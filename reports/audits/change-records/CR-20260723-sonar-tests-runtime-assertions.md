# Change Record: Runtime-test assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260723-sonar-tests-runtime-assertions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-tests-runtime-assertions |
| Date (UTC) | 2026-07-23 |
| Base revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Boundary | Parent test source, this English/German Change Record pair, and indexes only. Framework, MRTS, gitlinks, production connector source, scanner configuration, Quality Gates, suppressions, and runtime behavior remain unchanged. |
| Finding linkage | Nine live Parent python:S3415 Code Smells in the three listed test modules. AZ-KYVTnfYmbqbBXVNF9 at tests/test_runtime_path_policy.py:184 is excluded as environment-blocked and tracked as FND-SONAR-0031. |

## Motivation and problem statement

SonarQube Cloud reports nine reviewed python:S3415 findings in three independent
Parent test modules. Each selected unittest assertion placed a fixed expected
value before its observed process result, parsed payload, component identity, or
runtime-path value. The predicates are correct; only diagnostic operand order
is not.

The exact keys are AZ-KYVS5fYmbqbBXVNFm and AZ-KYVS5fYmbqbBXVNFn at lines
50 and 51 in tests/test_make_runtime_defaults.py; AZ-KYVUrfYmbqbBXVNGh,
AZ-KYVUrfYmbqbBXVNGi, and AZ-KYVUrfYmbqbBXVNGj at lines 89, 93, and 126 in
tests/test_runtime_component_cache_identity.py; and AZ-KYVSKfYmbqbBXVNFQ,
AZ-KYVSKfYmbqbBXVNFR, AZ-KYVSKfYmbqbBXVNFS, and AZ-KYVSKfYmbqbBXVNFT at
lines 45, 214, 216, and 228 in tests/test_resolve_runtime_paths.py.

The adjacent runtime-path-policy key is separate because its unchanged baseline
fails when the isolated Parent worktree cannot load
modules/ModSecurity-test-Framework/ci/lib/common.sh. A diagnostic-only change
without a valid baseline could hide a path-policy control failure.

## Acceptance criteria

- Swap only the first two operands of nine selected assertions.
- Preserve predicates, failure messages, subprocess calls, fixtures, expected
  values, and test outcomes.
- Pass the complete three-module subset and an AST/source inventory showing
  exactly nine actual-first calls.
- Preserve the runtime-path resolver negative controls.
- Keep English/German Change Records and indexes equivalent.
- Obtain exact-head SonarQube Cloud and hosted-check evidence before calling a
  selected key resolved on a Draft PR.

## Implementation decision and rationale

Only the first two positional arguments change. Observed return codes, payload
fields, shell values, component values, and status appear first; existing
integer, string, list, and set constants remain expected. Three return-code
messages remain third arguments. RuntimePaths.shell_values() was source-reviewed
as frozen-data construction without a relevant side effect.

This is a three-file maintainability batch. The blocked path-policy test is not
modified, and no production runtime source or security-control implementation
changes.

## Changed files

- tests/test_make_runtime_defaults.py
- tests/test_runtime_component_cache_identity.py
- tests/test_resolve_runtime_paths.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| Official SonarQube Cloud api/issues/search for ten initially selected keys | passed: all ten were open Parent MAJOR python:S3415 Code Smells; nine are feasible here. |
| Four-module Parent pre-change baseline | blocked_environment: 20 tests ran, 19 passed, and only tests.test_runtime_path_policy failed because Framework common.sh is absent. |
| Independent three-module baseline with explicit .venv, isolated TMPDIR, and bytecode disabled | passed: 14 tests. |
| Candidate three-module subset | passed: 14 tests. |
| In-memory AST parse and inventory | passed: exactly nine selected assertEqual/assertNotEqual calls are actual-first; three failure messages remain. |
| Scoped git diff --stat, git diff --check, and pyc scan | passed: three test files, nine additions/nine removals, no whitespace diagnostics, and no bytecode artifacts. |
| make check-bilingual-docs | blocked_environment: the only 20 diagnostics are pre-existing missing Framework-gitlink link targets; no changed Change Record or index diagnostic appeared. |
| tests.test_bilingual_docs | passed: 11 tests. |
| make check-doc-links | blocked_environment: the only 16 diagnostics are pre-existing missing Framework-gitlink link targets. |
| Focused Codex Security staged-diff scan | passed: all seven staged files received closure receipts; canonical report has complete coverage and zero reportable findings. |
| Exact-head hosted checks | pending: the existing Draft PR #110 must rerun all required evidence after its normal branch update and next push. |

## Security impact

Only Parent tests changed. The resolver test still passes its existing controls
for broad or system-owned writable roots, symlink escapes, traversal, foreign
connectors, overlapping bases, and an invocation-root escape. No production
parser, untrusted-input path, file-access control, subprocess argument,
executable selection, configuration, authentication, authorization, network
operation, or runtime path-policy implementation changed. The environment-
blocked path-policy assertion remains unmodified. No security finding is
claimed fixed. A focused Codex Security staged-diff review covered all seven
staged files and found no reportable security candidate; its deterministic
report is retained with the task evidence. This review does not replace the
pending exact-head hosted checks or the separately blocked path-policy
baseline.

## Runtime evidence

No connector runtime behavior changed or is claimed. The focused Parent tests
use temporary fixtures and resolver subprocesses; they are not a host
deployment, Framework run, MRTS run, or full connector/runtime matrix.

## Known limitations

This batch treats nine Parent test-diagnostic findings only. It does not clear
the wider SonarQube Cloud backlog, fix Framework or MRTS findings, or prove
connector runtime behavior beyond focused unit tests. The tenth reviewed key
remains open as FND-SONAR-0031 until an authorized clean baseline is available.

## Remaining risks

An out-of-scope swap could make a failure message misleading or change
evaluation order. Live-key/source inventory, purity review, nine-call AST
inventory, three-file diff review, and the complete focused subset reduce that
risk. Hosted Sonar analysis and CI still need exact Draft-PR-head evidence.

## Checks not run and rationale

- No complete tests.test_runtime_path_policy pass: its unchanged baseline is
  blocked_environment by absent Framework common.sh; no Framework/MRTS action is
  authorized.
- No full connector build or host/runtime matrix: only test diagnostics change.
- No Framework or MRTS test or modification: both are outside this Parent task.
- No exact-post-update-head GitHub Actions, CodeQL, Sonar Quality Gate, PR
  issue query, or review-thread check exists yet; the existing Draft PR must
  be evaluated again after the normal branch update and next push.

## Current normal update and delivery status

The existing Draft PR #110 was refreshed without a rebase by normal merge
commit `44611ee60e181b118952cc4ad52f06e633515611`, which merged Parent
`master` `475c2709f4ae0853f360a8b5dbcd754532c9b52d` into its original head
`07aa52fa35d464c30ad45e5c361850b1bc3002e8`. Only the paired Change Record
indexes conflicted; their resolution retains all current `master` entries and
this record.

Under the current Parent-only authorization, that normal merge may inherit the
Framework gitlink already present in `master` history. The final PR diff may
not, and does not, modify a gitlink. No Framework or MRTS checkout,
modification, test, delivery, or merge occurred.

After the update merge, the affected three-module subset completed 14 tests in
1.709 seconds. A fresh AST comparison against current `origin/master` proved
exactly nine selected actual-first `assertEqual`/`assertNotEqual` operand swaps
and no other changed assertion call; `git diff --check origin/master...HEAD`
reported no whitespace diagnostic. The previous hosted results apply only to
superseded head `07aa52fa35d464c30ad45e5c361850b1bc3002e8`; exact-head hosted
checks, SonarQube Cloud evidence, issue/hotspot review, and PR
review/conversation checks must be repeated for the next pushed head. This
record claims neither a ready transition nor a merge.

## Final diff and review status

The reviewed local batch is now represented by the existing updated Draft PR
#110. Its final current-base diff has exactly seven Parent paths: the three
selected test modules, this English/German Change Record pair, and the two
indexes. It contains no Framework, MRTS, or gitlink modification. Source and
focused-test controls plus bilingual validation have passed; exact-head delivery
evidence remains incomplete until the next pushed head has passed the required
controls. No merge, default-branch update, Framework/MRTS change, suppression,
or alert closure is claimed or authorized.
