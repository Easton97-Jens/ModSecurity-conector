# Change Record: NGINX lifecycle materialization root

**Language:** English | [Deutsch](CR-20260927-nginx-lifecycle-output-root.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260927-nginx-lifecycle-output-root` |
| Date (UTC) | `2026-09-27` |
| Base revision | `57b0ed6a72ff7c7235037a59f008164be673e7a5` |

Framework: `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`.
MRTS: `615b13bacbd008562c17408246c41ab27dca3104`.

## Motivation and problem statement

The fresh NGINX lifecycle failed before its first request. Parent passed a
runtime path under `runs/nginx/<run-id>/host-runtime` while the Framework
materializer selected `build/nginx/<run-id>` as its output root. Framework
correctly rejected the sibling write with `write path escapes output root`.
NGINX source materialization, module build and provisioning had already passed.

## Acceptance criteria

Both baseline and First-Byte child invocations must materialize within a
narrow common output root. The old sibling path must still be rejected.
Canonical evidence, the raw event collector, connector build inventory,
Cache-v2, pinned source identities and external static docroot projection
must retain their boundaries. A runtime PASS requires fresh real root-master
and nobody-worker requests plus validated canonical evidence.

## Implementation decision and rationale

Follow the existing HAProxy child host-work pattern: NGINX children use
`<connector-run-root>/nginx-host-work` for their Framework `BUILD_ROOT` and
nested runtime, result, temporary and harness paths. The Parent's global
connector build root is unchanged. Raw Phase-4 sources remain inside the
collector's raw run. First-Byte receives these stage aliases and an explicit
`SYNCHRONIZED_UPSTREAM_CONTROL_ROOT=<connector-run-root>` so its evidence
destination remains contained. Its explicit report root keeps the reserved
runtime environment snapshot under the unchanged connector build root.
Other helper callers retain the previous
control-root default. No Framework or MRTS change is required.

## Security impact

Framework containment, audit checks, symlink/path authority, separate root
master/nobody worker identities, private-network runtime and root-owned
external static projection remain enforced. No global temporary write
authority, source-map change or provenance override is introduced.

## Changed files

- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/runtime/lifecycle/run-native-first-byte.sh`
- `tests/test_nginx_functional_materialization_layout.py`
- `tests/test_collect_no_crs_source.py`
- This English/German Change Record pair.

## Commands executed

RTK wrapped all shell commands. The two new Parent-path reproductions failed
against the base for the observed containment error; after correction all
four materialization tests passed. The combined runtime resolver/path,
collector, runner-wiring, projection, master/worker and full-lifecycle
profile/evidence selection passed 156 tests. Shell syntax checks passed.
ShellCheck reported 15 pre-existing warnings; normalized base/current
diagnostics are identical. No warnings were suppressed. `git diff --check`
passed. Documentation checks are recorded in the external execution plan.

## Runtime evidence

The small tests invoke the real Framework materializer and actual Parent
assignment/call fragments. The controlled host seam stops before requests;
these tests are not runtime PASS evidence. A fresh exact-commit lifecycle
rerun follows the separate source commit and records its result externally.

## Checks not run and rationale

At record preparation, the post-commit real E2E rerun has not executed.
Remote CI, SonarQube, push, PR and merge are outside this local task.

## Known limitations

Path acceptance alone does not prove root/nobody audit compatibility or
response-phase behavior. Independent later runtime failures remain failures.
The old `aff1ba13` and base `57b0ed6` lifecycle results are not PASS.

## Remaining risks

Moving only child paths preserves the raw collector and component cache,
but actual host execution is required to validate ownership and lifecycle
interactions. Cache reuse must pass the repository's normal provenance checks.

## Final diff and review status

The focused Parent-only diff was independently reviewed. Framework/MRTS
gitlinks and the validated SOURCE_MAP repair remain unchanged. Delivery is a
separate local commit; no history rewrite or remote delivery is authorized.
