# Change Record: CR-20261009-nginx-phase4-path-input-adapter-20261009

**Language:** English | [Deutsch](CR-20261009-nginx-phase4-path-input-adapter-20261009.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-phase4-path-input-adapter-20261009 |
| Date (UTC) | 2026-10-09 |
| Base revision | f63996290925f4b0c04d286506171825de9dc2ff |

## Motivation and problem statement

Actual thin-driver Path arguments raised TypeError before projection preparation.

## Acceptance criteria

Case/run identity and strict path validation remain intact.

## Implementation decision and rationale

Only os.fspath before both existing absolute_path guards; no generic object coercion.

## Changed files

ci/runtime/lifecycle/run-nginx-phase4-cases.py and tests/test_nginx_phase4_path_inputs.py; paired record.

## Commands executed

Focused unittest:17 tests, exit0. Original RED: TypeError or existing projection child. Diff check:0.

## Security impact

No guard, authority, status or seal relaxation.

## Runtime evidence

None. Controlled configtest stops before native start; NOT_EXECUTED retained.

## Known limitations

Adapter test stops at a controlled projection boundary; existing absolute_path guards remain real. Symlinks and arbitrary objects remain rejected.

## Remaining risks

Integrated native proof and publication remain Root-owned.

## Checks not run and rationale

Native build/runtime unauthorized; archive checker0 and scoped record paths0; full Parent docs blocked by unpopulated Framework gitlink (18 path/22 bilingual targets).

## Final diff and review status

Focused unstaged diff reviewed; no Git writes.
