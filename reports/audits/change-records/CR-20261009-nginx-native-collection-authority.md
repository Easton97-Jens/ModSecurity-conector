# Change Record: CR-20261009-nginx-native-collection-authority

**Language:** English | [Deutsch](CR-20261009-nginx-native-collection-authority.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-native-collection-authority |
| Date (UTC) | 2026-10-09 |
| Base revision | `cf95e1e2519909d498a4a6fdb0e21db16b2ae3c4` |

## Motivation and problem statement

The genuine Root-master/nobody-worker run `nginx_all_required_20261009_r6`
reached real YAML, configuration, and native invocations, then stopped during
collection with `native bundle raw events cannot enter generic collection or
scrubbing`. The Parent passed the whole `nginx-host-work` stage as native
authority even though ordinary harness logs are siblings of the protected
native-operation bundles inside that stage.

## Acceptance criteria

Pass the exact invocation-local native-operation directory to the collector.
Ordinary sibling logs must remain collectable, while native receipt and raw
event bytes remain outside generic collection and unchanged. Existing
symlink, ownership, permission, identity, duplicate, seal, and raw-event
negative controls must continue to fail closed.

## Implementation decision and rationale

Only the Parent lifecycle argument is narrowed from `$STAGE_BUILD_ROOT` to
`$STAGE_BUILD_ROOT/host-runtime/native-operations-$NO_CRS_RUN_ID`. The Parent
collector guard is unchanged. A wiring regression fixes the exact
argument, and a mixed-topology regression proves that a generic sibling log
is consumed while the native receipt and raw event remain byte-identical.

## Changed files

`ci/runtime/lifecycle/run-no-crs-baseline.sh`;
`tests/test_no_crs_native_authority_wiring.py`;
`tests/test_nginx_native_operation_collection.py`; this English/German Change
Record pair.

## Commands executed

All commands used `rtk proxy`. The test-first wiring regression ran 9 tests
and failed exactly 1 assertion against the old broad argument (exit 1,
SHA-256 `0c8617d82e8e2d7449293cbc9b28ceb8473bf7b1cf23a50bed75097566ef6b3c`).
The focused wiring/collection run passed 25 tests (exit 0, SHA-256
`0bc77456d0ef4950b8314c21b407c5ce918ec13158dc21788219a98b88c71cb4`).
The expanded collector, dispatcher, projection, and First-Byte matrix passed
117 tests (exit 0, SHA-256
`7cbd353497bffd4515198d396876536483e8a16fb85f9255dd18828d8dcf4f4a`).
`sh -n` and ShellCheck passed for the changed lifecycle script; `bash -n` and
ShellCheck passed for both external test helpers.

## Security impact

The correction reduces the protected native authority from a whole build
stage to the exact sealed-bundle parent. The guard preventing immutable native
raw events from entering generic scrubbing remains intact, including rejection
of a generic row that references a path inside the native subtree. No
validator, selection rule, source provenance, Framework file, or MRTS file is
changed.

## Runtime evidence

The retained R6 run exited 2 at the original collector boundary after genuine
Root-master/nobody-worker requests; it is failure evidence, not PASS evidence.
No lifecycle rerun for this correction has yet been executed.

## Known limitations

Unit and contract tests do not prove the hosted lifecycle or Canonical PASS.
A fresh revision-bound build and isolated Root-master/nobody-worker run remain
required.

## Remaining risks

R6 also recorded nonzero driver exits for
`body_size_nonzero_with_null_data` and
`header_count_nonzero_with_null_headers`. They are not conflated with this
authority defect and require fresh post-fix classification if they recur.

## Checks not run and rationale

At this focused pre-commit stage, the full Parent focus suite, full lint, fresh
build, fresh E2E, Canonical finalization, current-head CI/Sonar, and protected
Exact-Head workflow have not yet run. They remain separate required gates.
Ruff remains unavailable in the existing environment; no dependency was
installed.

## Final diff and review status

Independent code and security reviews found no blocking issue. The task diff
contains the one Parent argument change, two regression test files, and this
bilingual record pair. At record finalization, commit, push, remote readback,
and hosted verification remain pending.
