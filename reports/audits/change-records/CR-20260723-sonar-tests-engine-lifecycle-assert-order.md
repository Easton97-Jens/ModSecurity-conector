# Change Record: Engine lifecycle assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260723-sonar-tests-engine-lifecycle-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260723-sonar-tests-engine-lifecycle-assert-order` |
| Date (UTC) | `2026-07-23` |
| Base revision | `5b8db00d44ab24f3a9f4216a00f7edee977b6898` |
| Boundary | Parent test source, this English/German Change Record pair and indexes only. Framework, MRTS, gitlinks, production connector source, scanner configuration, Quality Gates, suppressions, and runtime behavior remain unchanged. |
| Finding linkage | `FND-SONAR-0030`; 33 open Parent `python:S3415` Code Smells in `tests/test_engine_lifecycle_artifacts.py`. |

## Motivation and problem statement

The current SonarQube Cloud analysis reports 33 `python:S3415` findings in one
Parent test module. The affected `unittest.TestCase.assertEqual` calls, plus
one `assertNotEqual` call, placed a fixed expected value before the observed
process result, parsed payload, or lifecycle counter. The comparisons already
expressed the intended test predicates; their diagnostic order did not.

The live scoped issue query returned exactly 33 open `MAJOR` Code Smells for
this file. They occupy source lines 115, 117, 128–145, 188, 193–198, 226,
230–232, 241, and 253 under the stable `AZ-KYVW0fYmbqbBXVNJ*`/`...VNK*`
key group. Their issue flows identify the first operand as expected and the
second as actual.

## Acceptance criteria

- Swap only the first two operands of each of the 33 selected assertion calls
  so the observed value is first and the fixed expected value is second.
- Preserve all predicates, optional failure messages, subprocess invocation,
  temporary-artifact inputs, lifecycle fields, expected values, and test
  outcomes.
- Leave the three unselected multi-line hash assertions unchanged because they
  are not in the live Sonar scope for this batch.
- Pass the complete affected Parent test module and an AST/source inventory
  proving all 33 selected calls are actual-first.
- Keep both Change Record languages and both indexes equivalent.
- Obtain fresh exact-head SonarQube Cloud and hosted-check evidence before any
  selected key is called resolved on the Draft PR.

## Implementation decision and rationale

The patch swaps only the first two positional arguments. Process return codes,
the engine version string, transaction/lifecycle values, and the payload-input
rejection return code now appear as the observed value; their existing integer,
string, or list constants remain the expected value. The return-code message
argument stays in third position. No assertion predicate, fixture, event,
temporary path, executable, or writer invocation changed.

This is deliberately a single-file, maintainability-only batch. The 33 live
rows share one test module and the same `actual, expected` correction, while
the untouched hash assertions are excluded to avoid expanding beyond the
scanner's current scope.

## Changed files

- `tests/test_engine_lifecycle_artifacts.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| Official SonarQube Cloud `api/issues/search` for the 33 stable keys | passed: exactly 33 open `python:S3415` Parent Code Smells in the selected file. |
| Focused Parent baseline `tests.test_engine_lifecycle_artifacts` in a clean current-master worktree | passed: 5 tests. |
| Candidate focused Parent test module with explicit `.venv`, isolated `TMPDIR`, and bytecode disabled | passed: 5 tests. |
| In-memory AST inventory of all selected source lines | passed: exactly 33 targeted `assertEqual`/`assertNotEqual` calls are actual-first. |
| `git diff --numstat` scoped to the test file | passed: exactly 33 additions and 33 removals, one operand swap per selected call. |
| `tests.test_bilingual_docs` | passed: 11 tests. |
| Repository bilingual-documentation and link checks | `blocked_environment`: only the 20 pre-existing missing Framework-gitlink targets were reported; no changed Change Record diagnostic appeared. |
| AST syntax parse, `git diff --check`, and bytecode-artifact scan | passed: source parsed, no whitespace diagnostics, and no `*.pyc` artifact exists in the worktree. |
| Exact-head hosted checks | pending: the existing Draft PR #109 must rerun all evidence after its normal branch update; later results must be tied to that exact head. |

## Security impact

The test continues to exercise payload-free lifecycle artifacts, payload-input
rejection, symlinked library hashing, subprocess return codes, and lifecycle
counter behavior. This change alters only failure-message diagnostic order; it
does not change a production parser, untrusted input path, file-access control,
subprocess argument, executable selection, configuration, authentication,
authorization, network operation, artifact writer, or security assertion.
No security finding is claimed fixed.

## Runtime evidence

No connector runtime behavior changed or is claimed. The complete Parent test
module uses temporary fixtures to exercise the artifact writer contract; it is
not a host deployment, Framework run, or MRTS run.

## Known limitations

This batch treats only 33 reviewed Parent test-diagnostic findings. It does not
claim to clear the broader SonarQube Cloud backlog, to fix any Framework or
MRTS finding, or to prove connector runtime behavior beyond the existing
focused test contract.

## Remaining risks

An accidental swap outside a selected assertion could make a failure message
misleading. The live key/source inventory, exact 33-line AST verification,
single-file diff review, and complete affected test module reduce that risk.
Hosted Sonar analysis and CI still need to run against the exact Draft PR head.

## Checks not run and rationale

- No full connector build or host/runtime matrix: only test diagnostic operand
  order changes, and the complete affected Parent test module is the narrow
  regression control.
- No Framework or MRTS test or modification: both are excluded from this
  Parent-only task.
- No exact-post-update-head GitHub Actions, CodeQL, Sonar Quality Gate, PR
  issue query, or review-thread check exists yet; the existing Draft PR must
  be evaluated again after the normal branch update.

## Current normal update and delivery status

The existing Draft PR #109 was refreshed without a rebase by normal merge
commit `62eae66`, which merged Parent `master`
`700e62e5c2287e10f8774757ffff7432753900c0` into its branch. Only the two
shared Change Record indexes conflicted; their resolution retains all current
`master` entries and this record.

Under the current Parent-only authorization, that normal merge may inherit the
Framework gitlink already present in `master` history. The final PR diff must
not, and does not, modify a gitlink. No Framework or MRTS checkout,
modification, test, delivery, or merge occurred.

Fresh validation of the documentation-bearing post-update head, followed by
exact-head hosted checks, SonarQube Cloud evidence, issue/hotspot review, and
PR review/conversation checks remains pending. No readiness transition or
merge is claimed by this record.

## Final diff and review status

The reviewed local batch originated at
`a315a79ab485b1834939c4b9f90b53981151ff67` and is now represented by the
existing updated Draft PR #109. The final diff still has only the selected
Parent test module, this English/German Change Record pair, and their two
indexes. Its delivery evidence remains incomplete until the exact updated head
has passed the required local and hosted controls. No merge, default-branch
update, Framework/MRTS change, suppression, or alert closure is claimed or
authorized.
