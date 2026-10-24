# Change Record: CR-20261018-traefik-source-export-quality

**Language:** English | [Deutsch](CR-20261018-traefik-source-export-quality.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-traefik-source-export-quality |
| Date (UTC) | 2026-10-18 |
| Base revision | `a29019558678222b88913be0e202db3c9d14323a` |

## Motivation and problem statement

The exact published PR #413 head `a29019558678222b88913be0e202db3c9d14323a` received Sonar python:S3776 for `validate_destination` (complexity 17, limit 15) and python:S1172 for the unused `refresh_capture_source` parameter `profile`.

## Acceptance criteria

Retain every external-root, physical-path, ancestor, symlink, Git-marker, ownership and private-mode guard with the same validation order and storage boundary. Remove the unused private parameter and update its sole internal caller. Preserve committed source bytes, file modes, gitlinks and source manifests.

## Implementation decision and rationale

Extract the existing per-ancestor checks into `validate_private_ancestor`. The caller still walks the destination and all ancestors through the configured storage root, checks each ancestor before stopping, and does not inspect above that root. The helper retains the same symlink, UID/mode and below-root Git-marker conditions. The native preparer only loses an unused argument; profile-dependent fixture staging is unchanged.

## Changed files

- `connectors/traefik/harness/i12/source_export.py`.
- `connectors/traefik/harness/i12/native/prepare.py`.
- `tests/test_traefik_i12_source_export.py`.
- This EN/DE Change Record pair.

## Commands executed

All commands used RTK and the Parent virtual environment. Nine source-export characterization tests passed before the refactor. Afterward, `python -m unittest tests.test_traefik_i12_source_export tests.test_traefik_i12_native_measurements tests.test_traefik_i12_auth tests.test_traefik_i12_ledger` passed 34 tests. Adding the bilingual-documentation and Change Record modules produced 76 passing tests in 5.706 seconds. AST syntax for three Python files, Change Record structure and `git diff --check` passed. Exact wrapped commands and source hashes are retained in `source-export-quality/after.json` in the external task evidence directory.

## Security impact

No admission or path guard is removed or weakened. Added controls cover a permitted private nested destination, group-writable ancestry, foreign UID, ordinary and dangling-symlink Git markers, symlink ancestry and attempts to use the storage root itself. Existing committed-object, inventory and no-overwrite controls remain intact.

## Runtime evidence

These tests exercise physical filesystem fixtures and committed-source export behavior without starting hosts or mutating a repository. They do not qualify host transactions or alter historical I12 evidence.

## Known limitations

Local tests verify behavior preservation and call compatibility. A fresh hosted Sonar analysis is required to establish that these two findings are absent at the next published head.

## Remaining risks

The separate S5332 finding and HAProxy fixture compilation failure are assigned to the parent task. This scoped change does not claim overall CI or Sonar success.

## Checks not run and rationale

No host runtime, scanner upload, Git publication or Sonar issue-state change is performed. The parent task owns final integrated checks and publication.

## Final diff and review status

The final diff is limited to helper extraction, removal of the unused parameter/caller argument, meaningful boundary controls and this record. Unrelated acceptance producers and authorization relay changes remain with their owners.
