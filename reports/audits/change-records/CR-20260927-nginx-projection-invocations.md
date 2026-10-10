# Change Record: NGINX per-invocation docroot projections

**Language:** English | [Deutsch](CR-20260927-nginx-projection-invocations.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260927-nginx-projection-invocations` |
| Date (UTC) | `2026-09-27` |
| Base revision | `9fbaa70227b17d71c11005bc45984a11b9dd5dce` |
Framework: `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`.
MRTS: `615b13bacbd008562c17408246c41ab27dca3104`.

## Motivation and problem statement

Parent reused one exact projection child across independent NGINX cases and
native First-Byte. The first real request succeeded; later invocations were
correctly refused by the unchanged fresh-child guard.

## Acceptance criteria

Every independent case and First-Byte invocation uses a distinct, nonexistent,
safe direct child of the shared external parent. Reuse remains rejected.
Previous source-map/containment fixes, Framework/MRTS and cache contracts stay
unchanged. Exact-Head PASS requires all intended requests, root master/nobody
workers, canonical PASS, exit 0 and complete checksummed evidence.

## Implementation decision and rationale

Batch dispatch validates the original caller seed before selecting
`nginx-case-<UUID>` siblings. First-Byte separately validates its seed and selects
`nginx-first-byte-<UUID>`. Names remain bounded even with a 128-character seed.
Only the existing projector creates children. Direct single-case calls retain
their exact-root contract. Baseline explicitly forwards its canonical verified
root to First-Byte, which retains the component wrapper's standalone default.

## Security impact

No freshness, containment, no-follow, ownership, worker identity or private
network control is weakened. Malformed/existing seeds are not silently repaired.
No projection is deleted or reused. Private source, rules, logs, evidence and
cache authority remain separate. Canonical validators are unchanged.

## Changed files

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `ci/runtime/lifecycle/run-native-first-byte.sh`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `tests/test_nginx_projection_invocations.py`
- `tests/test_nginx_functional_materialization_layout.py`
- `connectors/nginx/harness/README.md` / `README.de.md`
- This English/German Change Record pair.

## Commands executed

RTK wraps every shell command. Before the fix, the three focused invocation
regressions failed at repeated-child authorization. After the fix, real
validator/projector tests cover repeated batches, separate First-Byte, combined
dispatch, invalid seeds and the default verified root. Neighboring resolver,
collector, runner, master/worker, lifecycle and protocol tests passed 142 tests.
The focused suite passed 34 tests (176 tests in total). Shell syntax passed;
ShellCheck reported 28 inherited diagnostics, identical to normalized base
diagnostics, with no suppressions. Native documentation/path-policy results
are retained in the external execution plan before committing.

## Runtime evidence

Small regressions execute real projection guards at controlled host seams;
they do not start servers or claim request evidence. The fresh committed
Exact-Head E2E outcome and SHA256SUMS will be retained externally after commit.

## Checks not run and rationale

At record preparation the post-commit E2E has not run. Remote CI, SonarQube,
push, PR and merge are outside this local task.

## Known limitations

Projection freshness alone does not prove canonical event completeness.
Missing allow events remain a separate diagnostic only after intended requests
execute; validators and expectations are not changed by this fix.

## Remaining risks

UUID collisions fail closed under existing freshness guards. Native cache
reuse/rebuild remains subject to normal provenance checks. Actual host execution
is necessary to validate all lifecycle and canonical acceptance criteria.

## Final diff and review status

The focused Parent-only diff preserves existing commits and repository pins.
Delivery is a separate local commit followed by fresh Exact-Head validation;
no history rewrite or remote delivery is authorized.
