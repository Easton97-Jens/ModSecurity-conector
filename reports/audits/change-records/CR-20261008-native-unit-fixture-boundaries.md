# Change Record: CR-20261008-native-unit-fixture-boundaries

**Language:** English | [Deutsch](CR-20261008-native-unit-fixture-boundaries.de.md)

Bounded fixture corrections; local unit and namespace evidence.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-native-unit-fixture-boundaries |
| Date (UTC) | 2026-10-08 |
| Base revision | `06df37a5fc8963bdc8c9c5577d602b9861e4bb4d` |

## Motivation and problem statement

The legacy route unit replay silently stopped changing its fixture after caller-prefix preservation expanded the route block. A real namespace jail test hardcoded /tmp rather than the required external task TMPDIR.

## Acceptance criteria

Reproduce the stale replay failure, transform exactly one actual route assignment with explicit change assertions, preserve routing expectations, and run the full real jail probe under configured temporary storage without weakening any isolation assertion.

## Implementation decision and rationale

The replay replaces only the exact native host_script assignment with the legacy Framework assignment; it asserts exactly one source match, changed fixture and absence of the original assignment. Product routing and prefix controls are untouched. Namespace TemporaryDirectory honors TMPDIR; the comment now explains physical host-path denial without assuming /tmp.

## Changed files

Only tests/test_nginx_selected_configtest_wiring.py, tests/test_run_readonly_submodule_validation_namespace.py and this paired record. The approved existing integration dependency 9cfae553 was replayed normally to reproduce current source; it is not part of the new delivery diff.

## Commands executed

RTK-wrapped replay test failed before correction (RED). The complete selected configtest wiring module passed 17 tests in 6.998 seconds. Five inspected namespace checks outside the UID0-only sandbox passed in 0.396 seconds with zero skips, after diff inspection. Neutral short external task TMPDIR/cache was used. Record generator rejected an initial short base revision; the full40 invocation created the proper pair.

## Security impact

The fixture transformation cannot silently become a no-op. Namespace jail, UID drop, inherited descriptor closure, forbidden host/source/Git writes, readonly runtime, PID1 and background-process lifetime assertions all remain unchanged. No /tmp exception or gate waiver.

## Runtime evidence

Real local permission and namespace unit probes only. The fifth check exercises the actual private jail and nobody identity. This is not NGINX runtime, compiled artifact authority, Protected workflow or canonical PASS evidence.

## Known limitations

Outside-sandbox UID/GID mappings are needed for the existing nobody identity; restricted sandbox EINVAL does not establish host inability. Namespace kernel support remains an explicit authored prerequisite, not bypassed.

## Remaining risks

Integrated Parent/Framework pin agreement and authorized native build/runtime remain separate coordinator gates. Existing ShellCheck warnings and unrelated dependency skips are not remediated by these fixture changes.

## Checks not run and rationale

No native build/runtime, Protected pipeline, Framework/MRTS mutation, pin update, installation or product-source routing change. Checks outside this bounded fixture slice are not claimed.

## Final diff and review status

Reviewed only the two approved test diffs and generated paired record. Existing source and unrelated commits preserved; a separate normal focused commit contains no replayed dependency.
