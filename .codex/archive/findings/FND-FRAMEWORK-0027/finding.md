# FND-FRAMEWORK-0027 — Framework common-version checker omits approved ModSecurity v3 provenance literals

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0027 |
| Category | ci_failure |
| Repository / ownership | framework / framework |
| Priority / severity | P1 / not_applicable |
| Confidence / status | validated / verified |
| Feasibility | feasible_now |
| Release blocker | false |
| Security relevant | true |

## Summary, observation, expected behavior, and impact

The current Framework master common-version workflow fails closed because its
parser accepts literal approved provenance values only for CRS variables. It
therefore omits the reviewed ModSecurity v3 approved repository, commit, and
release-tag literals before resolving the alias defaults that the checker
validates.

Scheduled Framework workflow run 29728340118 at master
efdbcbd98afeed0f39f8912ce1140aaa5742f507 exits 2 in
check-common-versions with MODSECURITY_REPO_URL, MODSECURITY_GIT_REF,
MODSECURITY_V3_GIT_URL, and MODSECURITY_V3_GIT_REF empty. The same failure
reproduces locally:

~~~
python3 ci/tools/check-common-versions.py --check --json --timeout 20
~~~

The checker must resolve the existing reviewed ModSecurity v3 approved literal
identity before resolving aliases and must keep missing tracked provenance
variables fail-closed. The scheduled check should pass when the approved
common.sh identity is present and current.

The mandatory Framework master version-provenance check is red although the
pinned identity is present. This blocks current-master readiness and obscures a
real missing-provenance condition behind a parser defect. The defect is
security relevant because the checker is a supply-chain provenance control, but
it fails closed and does not evidence an active provenance bypass.

## Scope, preconditions, reproduction, and evidence

Affected Framework files and symbols:

- ci/tools/check-common-versions.py: parse_common_assignment and parse_common.
- ci/lib/common.sh: MODSECURITY_V3_APPROVED_REPO_URL,
  MODSECURITY_V3_APPROVED_COMMIT, MODSECURITY_V3_RELEASE_TAG, and the four
  dependent repository/ref aliases.

The reproduction requires Framework source at
efdbcbd98afeed0f39f8912ce1140aaa5742f507, where common.sh defines the three
approved literal identity values and the checker resolves the four aliases
through them.

1. Read failed GitHub Actions run 29728340118, check check-common-versions,
   for that master SHA.
2. In an isolated worktree at that SHA, run the command above with task-owned
   external BUILD_ROOT and state paths.
3. Observe exit code 2 and the four empty ModSecurity repository/ref variables.
4. Inspect parse_common_assignment: its literal branch accepts CRS_APPROVED_*
   and CRS_RELEASE_TAG, but not MODSECURITY_V3_APPROVED_*.

Retained evidence:

- Run: 20260720T080314Z-parent-pr55-57-59-framework-update-3443af13
- Artifact:
  /var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/framework-common-version-parser/reproduction.json
- Type: framework_common_version_parser_reproduction
- SHA-256: 5b5bfe2c6ecff48658b948e3bcfaac9f1a80c7ac3d91cfb56f1a73c342ca8174
- Command: python3 ci/tools/check-common-versions.py --check --json --timeout 20;
  GitHub Actions failed-log readback for run 29728340118
- Working directory: /var/tmp/codex/worktrees/framework-common-version-parser
- Exit code: 2
- Observed: 2026-07-20T09:01:13Z
- Retention: retained
- Result: four aliases are empty although common.sh contains the three approved
  literal provenance anchors.

## Root cause and proposed remediation

parse_common_assignment restricts literal assignments to CRS_APPROVED_* and
CRS_RELEASE_TAG. MODSECURITY_V3_APPROVED_REPO_URL,
MODSECURITY_V3_APPROVED_COMMIT, and MODSECURITY_V3_RELEASE_TAG are therefore
absent from the resolver map; the alias defaults resolve against absent anchors
and become empty.

Extend only the explicit approved-literal allowlist with the three
MODSECURITY_V3_APPROVED_* identity names. Add a focused literal-and-alias
regression. Do not mark aliases optional, relax tracked-variable validation,
change common.sh provenance pins, or alter MRTS.

## Acceptance criteria and validation plan

- [x] The parser resolves all three MODSECURITY_V3_APPROVED_* literal anchors
  and all four dependent aliases from a focused fixture.
- [x] validate_entries reports no missing variable for a fixture with approved
  literals and alias defaults.
- [x] A fixture without approved anchors still leaves required aliases empty
  and is rejected by existing fail-closed validation.
- [x] The candidate checker reproduction no longer exits 2 for missing
  ModSecurity provenance variables.
- [x] No optional-variable list, provenance pin, Sonar setting, Parent file,
  or MRTS file is changed.

Run the focused common-version provenance unit test with bytecode writing
disabled, Python syntax compilation for the checker, the Framework ModSecurity
v3 provenance contract with external task-owned paths, and a final scoped
security review. A later Framework Draft PR must collect exact-head CI, CodeQL,
Sonar, review, and conversation evidence.

## Local remediation and observed validation

The isolated Framework task branch, based on
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`, now uses an explicit allowlist for
the existing CRS names and the three ModSecurity v3 approved literal anchors.
It also delegates ModSecurity v3 release checking through a provenance wrapper:
a newer tag is visible as `unknown` / manual review and produces no automatic
update plan unless a reviewed tag-to-immutable-commit change is made.

Observed candidate validation in source run
`20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`:

- the focused common-version provenance suite passed 15 tests;
- Python compilation passed;
- `make test-modsecurity-v3-provenance-contract` passed 10 tests with
  task-owned external paths;
- the non-writing `--check --json --timeout 20` command exited 0 with no
  missing required variables and no ModSecurity v3 update plan;
- `make check-bilingual-docs`, `make check-documentation`, and `make lint`
  passed; and
- independent source-security review and follow-up found no bypass, permission
  expansion, or MRTS change.

The scheduled writing `--update --markdown --write-files` variant was not run
against canonical common.sh. It is not needed to establish the corrected
non-writing control and would unnecessarily mutate canonical source.

Framework Draft PR [#36](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/36)
now provides exact-head hosted evidence for
`2bf862e1a5f262251043ec421447f6e4db11e17d` against base
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`: it is open, Draft, and mergeable
`CLEAN`. All 14 terminal checks are current: 11 succeeded (including CodeQL
Actions/Python/C++, SonarCloud Code Analysis, PR-head/range, scaffold-lint, and
common-structure); 3 advisory checks are expected skips; none failed,
cancelled, or remains pending. No review or unresolved review thread was
observed.

Post-merge lifecycle/evidence event at `2026-07-20T13:10:07Z`: PR #36 was
normally merged at `2026-07-20T13:06:39Z` as Framework master
`784977615acfc55567e37b863309abc4a38ac877`. Refreshed PR head
`1608352912a755f0f8639eddfa2350436446067e` is an ancestor and its tree equals
that master. Fresh hosted evidence for that exact head passed: CodeQL Actions,
Python, and C++; OSV; OpenSSF; secret scanning; lint; test-common; and the PR
SonarQube Cloud Quality Gate with 0 new issues, 0 Security Hotspots, and 0.0%
duplication. No human review, review request, or unresolved review thread was
observed. Resulting-master CodeQL Actions/Python/C++, lint, test-common, and
OpenSSF also passed. The separate master Sonar check failed only with inherited
FND-SONAR-0002 Security E, under the current user's bounded master-only
acceptance; no causality is attributed to this finding.

The retained isolated exact-master original-reproduction artifact
`analysis/pr36-master-common-version-original-reproduction.json`
(SHA-256 `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`)
records exit code 0 for `--check --json --timeout 20`: `missing_required` is
empty and all approved ModSecurity v3 anchors and dependent aliases resolve.
It also records v3.0.15 versus v3.0.16 as `unknown` / manual review with an
empty update list. The command used `--check` only and did not invoke
`--update`, `--markdown`, or `--write-files`. The prior local 15/15 parser,
10/10 provenance-contract, `py_compile`, bilingual/documentation, and diff
checks remain part of the exact-head evidence. The separate FND-SONAR-0002
acceptance does not waive any fresh PR-head check, PR Sonar gate, review,
permission, or security control.

## Regression and legitimate-control tests

Regression tests:

- tests/security_regression/test_common_versions_sonar_provenance.py
- make test-modsecurity-v3-provenance-contract

Legitimate controls:

- A missing approved anchor remains fail-closed through validate_entries.
- The existing approved ModSecurity v3 repository, commit, and release tag
  remain the resolved source of the aliases.
- No network lookup occurs merely to parse the fixture.

## Dependencies, boundaries, related findings, and residual risk

The historical exact-head and current exact-master controls now satisfy this
finding's source-validation dependency. Upstream availability remains a
legitimate runtime dependency of common-version checks. The separate
Framework-master Sonar blocker FND-SONAR-0002 remains blocked globally; its
current bounded master-only acceptance enabled the protected #36 delivery but
does not weaken, replace, or reopen this finding's controls.

This is not a duplicate of FND-FRAMEWORK-0001, whose test-common and
common-structure failures have a different cause, or FND-SONAR-0002, which owns
the independent current-master Sonar gate. FND-FRAMEWORK-0028 separately owns
the partial automatic-update path made reachable once the approved literals
resolve.

The normal Framework-master delivery occurred without a Parent file or Parent
gitlink update and without an MRTS content or Git action. Passing this
correction and the PR-head SonarCloud check does not clear the separate
Framework-master Sonar gate.

A future common.sh layout or provenance-name change needs explicit parser
review. The correction must remain restricted to the approved ModSecurity v3
identity names so arbitrary literals cannot enter the tracked resolver.

## Current delivery disposition

This finding is `verified`, not `closed` or risk-accepted. PR #36 was normally
merged as exact Framework master `784977615acfc55567e37b863309abc4a38ac877`;
its tree equals refreshed head `1608352912a755f0f8639eddfa2350436446067e`, and
the original missing-approved-literal reproduction plus legitimate controls
passed on that master. FND-SONAR-0002 remains a separate blocked
Framework-master issue with a bounded master-only acceptance; it does not alter
this finding's verified status or waive its PR controls. No Parent gitlink or
MRTS action occurred.

## History

- 2026-07-20T09:01:13Z — confirmed_and_remediation_started: the scheduled
  master check and focused isolated local control both exited 2 because the
  parser omitted MODSECURITY_V3_APPROVED_* literal provenance anchors. A narrow
  parser and regression-test remediation was authorized; no Parent,
  Framework-master, or MRTS Git action was taken.
- 2026-07-20T09:36:58Z — local_remediation_validated: the task branch resolves
  only the intended approved literals, preserves missing-anchor fail-closed
  behavior, and passes the focused, provenance-contract, documentation, and
  Framework lint controls. The separate Draft PR and exact-head hosted evidence
  remain pending; no Framework master, Parent, or MRTS Git action occurred.
- 2026-07-20T10:14:31Z — fixed_on_framework_pr_36_exact_head_validated: Draft
  PR #36 exact head `2bf862e1a5f262251043ec421447f6e4db11e17d`, based on
  `efdbcbd98afeed0f39f8912ce1140aaa5742f507`, is mergeable CLEAN with 11
  successful and 3 expected-skipped terminal checks and no failed/pending
  check, review, or unresolved review thread. Master merge, current-master
  reproduction, Parent gitlink, and MRTS actions remain out of scope.
- 2026-07-20T13:10:07Z — verified_on_framework_master_after_pr_36_normal_merge:
  PR #36 was normally merged at `2026-07-20T13:06:39Z` as Framework master
  `784977615acfc55567e37b863309abc4a38ac877`; exact head
  `1608352912a755f0f8639eddfa2350436446067e` is an ancestor with a tree equal
  to master. Fresh PR-head controls and resulting-master CodeQL Actions/Python/
  C++, lint, test-common, and OpenSSF passed. The retained exact-master
  artifact `analysis/pr36-master-common-version-original-reproduction.json`
  (SHA-256 `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`)
  records exit 0, no missing required variable, and all approved anchors and
  aliases resolved. The master Sonar Security E is the separate inherited
  FND-SONAR-0002 gate under a bounded acceptance, not a causal disposition of
  this finding; no Parent gitlink or MRTS action occurred.
