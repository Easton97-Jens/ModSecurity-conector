# Change Record: CR-20261018-traefik-current-source-export

**Language:** English | [Deutsch](CR-20261018-traefik-current-source-export.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-traefik-current-source-export |
| Date (UTC) | 2026-10-18 |
| Base revision | `95691eb24d53c1d9b4b7a089b96e5776be8b2fcd` |

## Motivation and problem statement

Replace incomplete/historical source staging with complete authenticated current Parent source exports for existing Traefik capture variants.

## Acceptance criteria

Export every committed Parent regular file with exact mode and SHA256; bind HEAD commit, tree and gitlink revisions; exclude foreign gitlink contents, links, Git metadata and uncommitted producers. Require fresh private configured external destinations and keep fixture changes separately bound.

## Implementation decision and rationale

Use git ls-tree and cat-file against the immutable resolved commit, verify each Git blob identity, and freeze the complete v2 inventory before central capture application. Native and forwardAuth preparers reuse the existing central variants and preserve original guards. Native build-manifest source revision now comes from the actual exported inventory.

## Changed files

`connectors/traefik/harness/i12/source_export.py`; `connectors/traefik/harness/i12/native/prepare.py`; `connectors/traefik/harness/i12_auth/prepare.py`; the corresponding native/auth README EN/DE pairs; `tests/test_traefik_i12_source_export.py`; this Change Record pair.

## Commands executed

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_traefik_i12_source_export tests.test_traefik_i12_auth tests.test_traefik_i12_native_measurements tests.test_traefik_i12_quality_controls tests.test_traefik_i12_ledger`: passed, 45 tests, exit 0. Root receipt: `checks/root-traefik-export-integrated-20261018.json` in run `i12-traefik-acceptance-20261015`; stderr SHA256 `235363f05352d02bf9faddb52e8f10e3b5b9312065bbd1d397d80037890cf588`. Focused exporter controls: 5 passed. Earlier combined test retained one stale-manifest rejection before regular shared-capture integration; the integrated retest passed.

## Security impact

Fail closed for invalid storage, links, existing destinations, unsupported Git entries and corrupted blob responses. SHA1 is used solely to verify Git object identity, with usedforsecurity=False; SHA256 binds the evidence inventory. No admission, peer, namespace, UID, capability, read-only or resource controls are relaxed.

## Runtime evidence

No host was launched by this change. Source-only probes successfully exported 2138 regular files from commit `0f174e0e4eb0316abb3e8662eba04eaf2c820e8c`, tree `21519c3215a70b202b29b27f9cb77c63851d769f`, and applied both existing central variants. Temporary copies were removed. This proves source application only.

## Known limitations

Uncommitted acceptance producers are excluded from committed source identity and must be separately exported and hashed as fixtures/instrumentation. Current source application does not establish a build or loaded artifact identity.

## Remaining risks

Fresh integrated builds, actual host observations and original-ID qualification remain required by the parent task.

## Checks not run and rationale

Host tests and final hosted CI/Sonar were not run in this source-export subtask. Their owning acceptance work follows committed integration.

## Final diff and review status

Root reviewed the exporter/preparer diff and reran the 45 integrated tests successfully. Source work is ready for normal commit; no Git delivery or host execution was performed by this worker.
