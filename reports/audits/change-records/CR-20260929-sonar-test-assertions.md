# Change Record: precise assertions for the three PR 393 Sonar findings

**Language:** English | [Deutsch](CR-20260929-sonar-test-assertions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260929-sonar-test-assertions |
| Date (UTC) | 2026-09-29 |
| Base revision | `e8dfd50cb604c575dbf6d36b41eef91fee968c88` |

## Motivation and problem statement

The user requested correction of the three Sonar findings on PR #393.
The complete public issue response contained three open MAJOR findings:
`AaDuoPI6WRbu3JJPyreg` and `AaDuclXM-TCTlyo6I0zq` (`python:S9073`),
and `AaDuclXM-TCTlyo6I0zr` (`python:S5778`).
They concern the two module-loader assertions and the missing-source-field
exception test, not product code.

## Acceptance criteria

Resolve all three findings without suppressions, preserve the tested contracts,
run the affected tests, and verify a fresh Sonar result for the successor PR head.

## Implementation decision and rationale

Split each `SPEC`/loader conjunction into two ordered assertions, preserving
short-circuit safety while making the failing precondition unambiguous.
Prepare the missing-field fixture before `assertRaisesRegex`, leaving only
`structure_digest(previous)` in the exception scope. Keep both the expected
`RepairError` class and the `Incomplete` message check unchanged.

## Changed files

`tests/test_change_record.py` and
`tests/test_prepare_reviewed_framework_handoff.py`, plus this EN/DE record.
Remove the temporary readback workflow introduced in commit
`eff6c291de6aa6cb494c12606e3d9c8c83cfca1f` only to obtain public issue
details; it is absent from the final PR diff.

## Commands executed

In-process Python 3.13.5 verification of the modified handoff module:
19 tests passed. AST parsing, whitespace and final-newline checks passed.
The loader guard was checked with an absent spec, an absent loader, and a valid
loader: rejection/rejection/success is unchanged. The selected exception
block has one call after the edit, compared with two before it.

Original test/source bytes were matched to the GitHub Git blob hashes before
editing. No local repository-native or local Sonar execution is claimed.
Hosted verification uses the existing early CI step and
`python3 -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff`.
Its actual result and fresh Sonar readback belong to the successor commit's
PR checks/comments, not a prediction in this record.

## Security impact

No product code, approval hash, dependency pin, submodule, checker, workflow
permission, Sonar rule, exclusion, suppression, or Quality Gate is changed.
The temporary diagnostic used no token, secret, checkout, or repository write.

## Runtime evidence

None required or claimed for this test-only correction. The original Framework
handoff repair remains unapplied and is outside this three-finding correction.

## Known limitations

Local GitHub DNS resolution and local RTK/Sonar tooling were unavailable.
[Diagnostic run 36628373759 / job 109611057786](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36628373759/job/109611057786)
retrieved all three public findings, then failed with HTTP 400 on a separate
rule-description request. It is not reported as a successful complete job.

## Remaining risks

Passing unit tests alone does not establish a clean Sonar analysis.
A green preparation PR would not establish that the original updater is fixed.

## Checks not run and rationale

No native connector build or runtime matrix: neither is exercised by these
test-only edits. No local Sonar scan or full local checkout test: required
tooling/network access was unavailable. Fresh hosted results must be checked
against the final PR head, not an earlier commit.

## Final diff and review status

The source correction is limited to the three identified test sites.
Keep PR #393 in draft for its separate unapplied Framework repair.
No merge, direct master push, or history rewriting is authorized.
