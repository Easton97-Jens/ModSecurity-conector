# Change Record: CR-20261020-i12-traefik-historical-anchors

**Language:** English | [Deutsch](CR-20261020-i12-traefik-historical-anchors.de.md)

Historical source-storage repair only.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261020-i12-traefik-historical-anchors |
| Date (UTC) | 2026-10-20 |
| Base revision | `81b0f802b8af9acaa18a88f86121c632fb9237ea` |

## Motivation and problem statement

Preserve historical registry verification after product changes advanced three repository files. Their historical hashes previously failed verification.

## Acceptance criteria

All three objects reconstruct exact historical bytes; only three storage mappings change. Profiles, deltas, results and provenance remain identical. Registry and capture controls pass.

## Implementation decision and rationale

Freeze lossless `text_lines` authenticated against `3a1bafecd0c38ccf20427d580c767ed42addf4aa`; retain existing historical identities and current-input acceptance semantics.

## Changed files

`ci/runtime/lifecycle/i12/manifest.json`, `ci/runtime/lifecycle/i12/README.md`, `ci/runtime/lifecycle/i12/README.de.md`; three `objects/text/` files with prefixes `0fa85f5658be96a25204adf489b2e18149a5f826b5ed528e55ec7b2ffe410aa4`, `7f1544f1f36042c68359c7caed7d5dc4ce8cc77d44282debdc3955ea725a5e9c`, `445dcfd6c296c442d8b1593e4bc1106077900b0c745cf1b79beb0d3ead555580`; `reports/audits/change-records/CR-20261020-i12-traefik-historical-anchors.md`, `reports/audits/change-records/CR-20261020-i12-traefik-historical-anchors.de.md`.

## Commands executed

`rtk proxy python3 -B ci/runtime/lifecycle/i12/capture_sources.py verify`: PASS (155 objects/10 profiles). `rtk proxy python3 -B -m unittest discover -s ci/runtime/lifecycle/i12 -p test_capture_sources.py -v`: PASS (57 tests). Independent Git-byte/hash comparison: PASS for all three objects. Structural manifest comparison: PASS; only the three storage mappings changed.

## Security impact

No product, protocol, authentication, authorization or isolation change. Strict hash and source-input checks remain active.

## Runtime evidence

No host launched; source verification awards no lifecycle qualification.

## Known limitations

Current product input bytes remain subject to existing profile pins.

## Remaining risks

Fresh exports, builds and host evidence remain required in the owning route acceptance task.

## Checks not run and rationale

`rtk proxy make check-doc-links` failed at the repository-path prerequisite: 18 existing links into the uninitialized Framework submodule are missing. Go/Race/Vet/host tests are outside this source-storage repair and remain required by the parent task.

## Final diff and review status

Scoped diff reviewed; historical identities, profiles, deltas and provenance unchanged. `rtk proxy python3 -B ci/tools/new-change-record.py check`: PASS. Scoped EN/DE pair and changed-document link checks using the repository checker: PASS. `rtk proxy git diff --check`: PASS. `rtk proxy make check-bilingual-docs` reports only 22 existing missing Framework links; the full link target reports 18 at its prerequisite. Manual EN/DE content parity reviewed. All commands used RTK; `rtk --version`, `rtk gain` and `rtk proxy which rtk` succeeded. No commit/push performed by this worker.
