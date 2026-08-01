# FND-SONAR-0010 — Parent PR #90 Go-updater Quality Gate blocker

## Classification

- **Category:** `sonarqube_finding` (`reliability_and_duplication`)
- **Repository / ownership:** `parent` / `parent`
- **Priority / severity / confidence:** `P1` / `not_applicable` / `confirmed`
- **Status / feasibility:** `verified` / `feasible_now`
- **Release blocker:** yes
- **Security relevant:** no; remediation still touches security-sensitive updater mechanics and requires a focused security-diff review.

## Summary

Parent Draft PR #90 at exact head
`d99eafd76d9fdbef5b63a19d084fd2d7caff6c08` fails its applicable
SonarQube Cloud Quality Gate. The gate reports 15.9% duplicated new code
(maximum 3%) and Reliability C (required A). The only new reliability Bug is
`AZ-LhTtmzOcepZz2Zxpc`, rule `python:S5850`, at
`ci/checks/common/check-go-version-contract.py:24`. The duplicated code is
primarily 183 of 451 new lines in `scripts/update-go-version.py` and 55 of
207 new lines in `tests/test_update_go_version.py`. The exact-head evidence
attributes both conditions to the initial Go-centralization implementation,
not to the later three-file Framework-compatibility follow-up.

The repair extracts the common updater and test-support mechanics, keeps the
Go and Python endpoint/schema/version-policy adapters separate, and makes the
CodeQL Go selector mapping exact. It is verified at exact head
`06a4e71408a60e5a72a55065a653b9c4e79a1ecf`: Quality Gate is `OK`, New
Reliability is `A`, and duplicated new-code density is 0.0%.

## Observed and expected behavior

GitHub check run `89053617816` belongs to the current exact PR head and reports
Quality Gate `ERROR`. The retained receipt records 238 duplicated lines out of
1497 new lines (15.898%) and the one `python:S5850` reliability Bug.

The PR must retain the fail-closed central-version contract, official release
authority, bounded no-redirect JSON parser, and symlink-safe atomic version
file updates while its current head reaches a Quality Gate with no new
reliability Bug and at most 3% duplicated new code. No rule, Quality Gate,
exclusion, suppression, false-positive disposition, or risk acceptance may
change to obtain that result.

## Impact

PR #90 cannot be represented as a verified delivery candidate while its
current head fails the required Quality Gate. Leaving parallel implementations
of security-sensitive release transport and safe file-update mechanics also
creates unnecessary divergence risk.

## Affected scope and preconditions

- `ci/checks/common/check-go-version-contract.py` (`SETUP_GO_STEP`)
- `scripts/update-go-version.py` and `scripts/update-python-version.py`
- `tests/test_update_go_version.py` and `tests/test_update_python_version.py`
- Parent Draft PR #90 remains open at
  `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08`.
- GitHub check run `89053617816` and the SonarQube Cloud PR integration apply
  to this exact head.

## Reproduction and evidence

1. Inspect PR #90 and check run `89053617816`; confirm exact head
   `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08`.
2. Run the recorded read-only query:
   `rtk proxy curl -fsSL 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=90&ps=500'`.
3. Compare `python:S5850` and the affected component measures with the PR
   diff.

Retained evidence: `sonar-pr90-d99eafd-quality-gate.json` (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/sonar-pr90-d99eafd-quality-gate.json`), SHA-256
`e4d465b8cc49131866942eecc6f854bf578d5689a0f95131cab33d0fa797427b`.

## Root cause and remediation

The initial Go implementation copied the Python updater's transport, strict
JSON, regular-file, atomic-write, CLI, fixture, and test-harness mechanics
into parallel Go-specific files. It preserved behavior but created the
reported clone. The static CodeQL parser also uses an ambiguous multiline
regex boundary. The later `d99eafd` follow-up only changes Framework cache
compatibility tests and bilingual Change Records.

The remediation replaces the ambiguous boundary with an explicit safe parser
or grouped boundary and extracts shared updater mechanics and test support into
internal Parent modules. Python and Go retain separate endpoint, schema, and
version-policy adapters. No updater security control or Sonar control may be
weakened.

## Acceptance and validation

- `python:S5850` is absent from the exact PR head, while static-contract
  rejection behavior is retained.
- Shared logic retains endpoint equality before open, no redirects, 2 MiB
  bounded strict JSON parsing, safe regular-file checks, and atomic updates.
- Both language adapters retain their CLI, JSON, version schema, and
  fail-closed behavior.
- Exact-head SonarQube Cloud has no task-owned reliability Bug and 0.0%
  duplicated new code, without a forbidden workaround.
- Focused updater, contract, CI-security, bilingual, diff, and security-diff
  validation passed locally; ordinary exact-head hosted checks are terminal
  success or skipped.

The final local validation summary records 100 passing focused tests, Python
syntax compilation, all three static contract targets, safe updater `--help`
smokes, and whitespace validation:
sonar-remediation-final-local-validation.md (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/sonar-remediation-final-local-validation.md`)
(SHA-256 `444a215b5cf98118daf3032e38485b07b3d100ddb8e422cb41ebbeca92d5a624`).
The complete final security-diff scan found no reportable finding:
report.md (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/tmp/codex-security-scans/ModSecurity-conector/d99eafd76d9_20260722T221118Z/report.md`)
(SHA-256 `12df4f3ed8d6f850feaf644a512d7bd1de0c3b41b6fffb5e99e021e21a25e1b4`).
The fresh hosted receipt is
hosted-pr90-06a4e71-validation.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/hosted-pr90-06a4e71-validation.json`)
(SHA-256 `db38c89e5c1646e343ec022466d7fec899998dda05558ccf85789196d273ea20`).

## Dependencies, blockers, and related findings

Fresh exact-head SonarQube Cloud and GitHub Actions validation has passed.
This finding is distinct from `FND-PARENT-0045` (Update-submodules candidate
compatibility) and relates to historical Sonar remediation record
`FND-SONAR-0006` only by classification. The non-gating open test code smells
are separately tracked by `FND-SONAR-0011`.

`Update submodules` is not dispatched, no master integration is authorized,
and no Framework, MRTS, gitlink, rule, Quality Gate, suppression, or risk
acceptance action has occurred.

## History

- `2026-07-22T21:25:24Z`: Allocated from current exact-head PR #90 evidence
  as a confirmed, task-owned P1 Quality Gate blocker; focused remediation is
  in progress.
- `2026-07-22T22:47:54Z`: Local remediation is fixed: shared updater/test
  mechanics, exact selector contract, 100 focused tests, static contracts,
  and a complete zero-finding security-diff scan passed. The task still needs
  a commit, normal push, and fresh exact-head hosted Quality Gate.
- `2026-07-22T23:02:27Z`: exact head `06a4e71` passed its Quality Gate and
  ordinary hosted checks; this finding is verified. No master integration or
  Update-submodules dispatch occurred.
