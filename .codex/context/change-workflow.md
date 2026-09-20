# Change Workflow

Use this for features, bug fixes, behavior changes, refactors, configuration changes, and non-trivial product work.

## Common preflight

1. Establish expected/current behavior from repository evidence.
2. Determine Parent/Common/connector/Framework ownership.
3. Identify public API/configuration/compatibility/security effects.
4. Define observable acceptance criteria and validation before implementation.
5. Identify affected EN/DE documentation and Change Record applicability.

## Feature-specific

For new capability, define valid/invalid/omitted inputs, defaults, precedence, errors, compatibility/migration, resource limits, and negative security behavior. Implement the smallest complete observable capability; avoid hidden stubs, silent fallback, or always-success branches.

## Bugfix-specific

Do not accept a report as proven. Reproduce the defect where practical, separate expected from observed behavior, establish root cause/ownership, and identify a legitimate control case. Prefer a regression test that fails before and passes after the fix. When runtime reproduction is impossible, use the strongest repository-native proof and state its limitation.

## Implementation

- make the smallest complete root-cause/capability change;
- avoid unrelated refactoring;
- preserve legitimate behavior and compatibility unless the task explicitly changes it;
- surface invalid/error states explicitly;
- do not weaken validation, tests, warnings, security controls, or evidence gates.

## Verification

Run the narrowest applicable real checks first, then broader checks only as required by scope/risk. For bugfixes rerun the original reproducer and legitimate control. For security-relevant changes also apply `security-policy.md`.

Use `definition-of-done.md` for completion.
