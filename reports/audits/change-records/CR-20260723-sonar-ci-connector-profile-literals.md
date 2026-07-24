# Change Record: CI connector-profile literal deduplication for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260723-sonar-ci-connector-profile-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-ci-connector-profile-literals |
| Date (UTC) | 2026-07-23 |
| Base revision | Current integration base ec57576814a3f75c5e153d51c945bd1dd341a916; original source base a308d7b414f0859490fe7253e0683a4bde80b563. |
| Tracking | FND-SONAR-0021; three current SonarQube Cloud python:S1192 findings AZ9cRyWgHhV2CayPTPuj, AZ9cRyWgHhV2CayPTPuk, and AZ9cRyWgHhV2CayPTPul. |
| Boundary | Parent CI documentation-layout checker, this English/German Change Record pair, and their indexes. Framework, MRTS, gitlinks, profile membership, runtime code, scanner configuration, Quality Gates, suppressions, exclusions, issue state, and default branch remain unchanged. |

## Motivation and problem statement

The connector-profile layout checker repeated the same README, detection-only
rule, and engine-off rule paths for all six connector tuples. The resulting
S1192 findings are maintainability issues, while the profile sets themselves
are intentional connector-specific validation contracts.

## Acceptance criteria

- The three repeated path literals are bound to narrowly named immutable module
  constants and no longer repeated across connector tuples.
- Every required-file tuple for Apache, NGINX, HAProxy, Envoy, Traefik, and
  lighttpd resolves to exactly the same values as at the base revision.
- Direct detection-only, engine-off, and strict-reference checks use the same
  constant values.
- The connector configuration generator and checker continue to pass.
- No profile membership, validation message, rule, Quality Gate, exclusion,
  suppression, NOSONAR, or issue state is changed.
- Fresh exact-head SonarQube Cloud and hosted evidence is required before the
  three findings are declared verified for protected integration.

## Implementation decision and rationale

The module now binds PROFILE_README, DETECTION_ONLY_RULES, and ENGINE_OFF_RULES
once and uses them in all six profile tuples plus the direct checks. The values
remain README.md, rules/detection-only.conf, and rules/engine-off.conf.

A base-to-candidate AST mapping compares the complete required-file dictionary
rather than only counting text occurrences. It proves that all six connector
tuples have the same resolved path values before and after the refactor.

## Changed files

- ci/checks/documentation/check-connector-config-reference.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Security impact

This is not applicable as a runtime security modification. The static checker
still resolves the same repository-relative profile paths and performs the same
file/content validations. No parser, runtime path sink, command, permission,
authentication, isolation, or scanner control changes.

## Commands executed

- Focused make check-connector-config-reference: passed before and after the
  constants-only change; generator reports 21 generated files current and the
  checker reports all seven contract areas passing.
- In-memory base-to-candidate profile mapping: passed for all six connector
  tuples and the three constant values.
- git diff --check: passed for the source-only candidate before this record
  pair was added.
- Targeted `tests.test_bilingual_docs`: passed (11 tests); the paired record
  identity values also match exactly.
- Exact-head hosted evidence for `d19f923cac105501366a90d76c2849265e687874`:
  all 39 check runs completed with only `success` or `skipped` conclusions,
  including the six protected required checks; SonarQube Cloud Quality Gate is
  `OK` with zero new issues and zero security hotspots.

## Runtime evidence

The target is a static CI documentation-layout checker. It validates committed
profile files and rule contents; no live connector, Framework, MRTS, or
production runtime execution is claimed.

## Validation status

The focused checker, profile mapping, targeted bilingual documentation, and
current-base diff review pass. The mapping proves that all six required-file
tuples and the three direct path checks retain their exact values after
constant substitution. The exact-head hosted evidence for
`d19f923cac105501366a90d76c2849265e687874` passed as recorded above. This
record-only follow-up requires a fresh exact-head validation cycle after its
normal publication; it does not alter checker behavior or profile values.

## Known limitations and follow-up

This record covers only three current Parent S1192 findings in one CI checker.
It does not claim that the project-wide 1,474-item inventory or other CI,
Common, Scripts, Tests, or connector findings are resolved.

## Remaining risks

The values are intentionally unchanged. No task-owned Quality-Gate issue or
security hotspot was observed for `d19f923cac105501366a90d76c2849265e687874`.
The remaining delivery risk is limited to a fresh exact-head revalidation of
this record-only follow-up before protected integration.

## Checks not run and rationale

- No Framework or MRTS test or modification: both are out of scope.
- No live connector runtime: static checker behavior is directly exercised by
  its focused target.
- Final exact-head hosted checks and SonarQube Cloud analysis for this
  record-only follow-up: not yet run at the time this record is committed and
  required before protected integration.

## Delivery status

The normal current-base update was pushed at
`d19f923cac105501366a90d76c2849265e687874`, and PR #103 was marked ready for
review after its observed local, hosted, SonarQube Cloud, and review evidence.
This record-only follow-up is published normally and requires a new exact-head
verification cycle before a protected squash integration. Direct
default-branch updates, rebase, force-push, and Framework/MRTS changes remain
prohibited.

## Final diff and review status

The final current-base diff introduces three immutable constants and replaces
their matching uses; it does not change profile values or validation flow. This
record-only follow-up changes no source, test, Framework, MRTS, or gitlink
path. The focused checker, static profile mapping, targeted documentation, and
local diff review passed; the prior exact-head hosted evidence is recorded
above. A new exact-head cycle remains required solely because this record is a
new commit; this record makes no premature final merge claim.
