# Change Record: CR-20261015-i12-capture-current-export-sdk-compat

**Language:** English | [Deutsch](CR-20261015-i12-capture-current-export-sdk-compat.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-capture-current-export-sdk-compat |
| Date (UTC) | 2026-10-15 |
| Base revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation and problem statement

Native evidence tests failed against the public libModSecurity 3.0.12 API; the capture installer accepted only its historical revision.

## Acceptance criteria

Compile against both supported ID argument signatures without casts or disabled warnings. Preserve every historical capture byte. Verify a complete current Git export before any overlay write.

## Implementation decision and rationale

Use C17 generic selection of the selected public declaration and explicit intervention string ownership. Add a strict v2 source inventory; retain v1 validation and all nine historical profiles. The versioned controller relocation changes only its authorized run root.

## Changed files

`ci/runtime/lifecycle/native-lifecycle-observer.[ch]`, its native tests, the Apache header probe/tests, `ci/runtime/lifecycle/i12/{capture_sources.py,test_capture_sources.py,manifest.json,objects/}`, both I12 README companions and this Change Record pair.

## Commands executed

`rtk proxy python3 -B -m unittest discover -s ci/runtime/lifecycle/i12 -p test_capture_sources.py -v`: 48 tests, exit 0. Native observer and Apache header tests: 38 tests, exit 0 with explicit SDK include/library roots. `rtk proxy python3 -B ci/runtime/lifecycle/i12/capture_sources.py verify`: exit 0, 155 objects and nine profiles. `rtk proxy git diff --check`: exit 0.

## Security impact

Reject extra/missing files, duplicate fields, special files, links, changed modes/hashes and Git metadata before writes. No credential, isolation, compiler, scanner or gate control is weakened. A trusted Git export producer remains necessary; a revision string alone is not authenticated.

## Runtime evidence

This change establishes compile/capture integrity only. The native header probe uses the actual APR and SDK libraries; legacy-header compilation does not establish a 3.0.12 runtime. Current Apache host qualification remains a separate PR #414 deliverable.

## Known limitations

No Apache acceptance or I12_COMPLETE claim. Historical source overlays keep their original semantics and before-hash guards. The controller remains a reviewed test-only external execution contract.

## Remaining risks

Exact-head CI and SonarCloud must still run after normal delivery to #410 and integration into #414.

## Checks not run and rationale

Initial bilingual documentation validation failed because this isolated worktree has no populated Framework checkout. The final `make check-bilingual-docs check-doc-links` passed with exit 0 using a read-only Framework binding in a private mount namespace; Gitlinks and outside mounts remained unchanged. No host run is claimed by this repair.

## Final diff and review status

Root reviewed the bounded SDK/capture changes and historical reconstruction invariants. Normal commit/push and final remote readback are tracked separately; no merge is authorized.
