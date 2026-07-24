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

## Runtime evidence

The target is a static CI documentation-layout checker. It validates committed
profile files and rule contents; no live connector, Framework, MRTS, or
production runtime execution is claimed.

## Validation status

The focused checker and profile mapping pass on the current integration head.
The mapping proves that all six required-file tuples and the three direct path
checks retain their exact values after constant substitution. Targeted
bilingual documentation, final scoped diff, and exact-head hosted delivery
evidence remain required before protected integration.

## Known limitations and follow-up

This record covers only three current Parent S1192 findings in one CI checker.
It does not claim that the project-wide 1,474-item inventory or other CI,
Common, Scripts, Tests, or connector findings are resolved.

## Remaining risks

The values are intentionally unchanged. The remaining delivery risk is
external: a fresh exact-head SonarQube Cloud analysis and hosted checks must
verify the updated PR before the findings are marked verified.

## Checks not run and rationale

- No Framework or MRTS test or modification: both are out of scope.
- No live connector runtime: static checker behavior is directly exercised by
  its focused target.
- Exact-head hosted checks and SonarQube Cloud analysis: required after the
  normal Parent branch update is pushed and before protected integration.

## Delivery status

The candidate has been normally updated on an isolated Parent task branch from
the recorded current integration base. It may be pushed to its existing Draft
PR for fresh exact-head validation. A protected squash integration is
authorized only after the applicable exact-head checks, SonarQube Cloud result,
review state, and current-base verification pass. Direct default-branch
updates, rebase, force-push, and Framework/MRTS changes remain prohibited.

## Final diff and review status

The final current-base diff introduces three immutable constants and replaces
their matching uses; it does not change profile values or validation flow. The
focused checker, static profile mapping, and local diff review passed. Fresh
exact-head hosted delivery evidence is still required; this record makes no
premature Quality Gate or PR-status claim.
