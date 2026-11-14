# Change Record: CR-20261108-preparation-publisher-mode

**Language:** English | [Deutsch](CR-20261108-preparation-publisher-mode.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261108-preparation-publisher-mode |
| Date (UTC) | 2026-11-08 |
| Base revision | `6ceeb7a729faa541a5048d7018c2f70e5c72fcea` |

## Motivation and problem statement

The Framework publisher admitted a registered companion changing from regular mode `100644` to `100755`, although this boundary permits content updates with the existing mode. The actual lock-file transition reproduced the defect; unchanged regular mode succeeded and a symlink transition failed.

## Acceptance criteria

Accept status `M` for registered regular companions only when old and new modes match. Reject both executable-mode flips, symlink/type/addition transitions, unknown paths and retired paths. Preserve the existing Gitlink, validation/publisher, App-token, permissions and exact staged-scope controls. Retain the unchanged 100 standard cases.

## Implementation decision and rationale

Add old/new mode equality to the existing raw Git-diff AWK guard in `.github/workflows/update-submodules.yml`. The old-mode field includes its leading colon; compare it to the colon-prefixed new mode. Keep the existing regular-mode and status checks. Framework owns the corresponding positive and negative tests; no connector product source changes.

## Changed files

`.github/workflows/update-submodules.yml` and this English/German Change Record pair. The separately committed Parent governance updater, catalog/templates and reference corrections are dependencies, not additional files in this focused mode-guard change. Framework source/tests/records remain in their own repository.

## Commands executed

The native `ci/tools/new-change-record.py create --name preparation-publisher-mode --base-revision 6ceeb7a729faa541a5048d7018c2f70e5c72fcea --date 2026-11-08` completed with exit 0 under the Parent interpreter and explicit `TEST_ROOT`, `FRAMEWORK_ROOT`, `FRAMEWORK_REVISION`, `CONNECTOR_ROOT`, `CONNECTOR_REVISION` and Framework root/`connector_suite` Python search paths. Earlier missing-context/import attempts executed no scaffold and are retained as diagnostics. `rtk bypass git diff --check` passed before the source review. The Framework-owned full class ran all 48 original methods twice with zero failures/errors/skips; the structured run records 222 subtest executions within those methods. Independent review ran six material methods successfully, including 26 native workflow mutations and eight Sonar context mutations. These are executions, not additional default cases. Evidence: `$EVIDENCE_ROOT/workflow-tests/publisher-mode-repro.json`, `full-class-result.json`, `final-default100-scope.json` and `reviews/workflow-qualified-review.json`.

## Security impact

Closes the registered-companion mode-change gap. Both mode-flip directions and alternative symlink/status/path transitions remain rejected; legitimate unchanged-mode modifications remain accepted. Existing credentials, triggers, write permissions, immutable actions, trusted validation and publisher separation are preserved.

## Runtime evidence

This validation covers workflow contracts and local Git-diff controls. No new connector-host runtime result is claimed.

## Known limitations

The broader preparation remains incomplete. The regular central pre-commit handler still requires operator-owned Gitlink admission. Parent/Framework/MRTS final published pins are not frozen. The separate MRTS governance Draft PR #7 publishes `9a855b092645733ea8ff73a512aff7bfe916407e`; its Framework handoff is still pending. This is an external governance dependency, not an MRTS product change delivered by this record.

## Remaining risks

A tested uninstalled operator proposal does not prove successful live handoff. Final separate Secrets receipts and native pin verification must bind the actual staged commits. FIFO/JSON analyzer coverage gaps remain separate preparation blockers. No hook, trust, gate, baseline or exclusion weakening is used.

## Checks not run and rationale

Current final-pair hosted CI/Sonar and the requested 92 host executions, 195 Go scenarios/vet, reader/registry and complete consistency replay require a regular committed, published, frozen chain. They are not claimed here. `READY_FOR_FULL_ACCEPTANCE=false`; the comprehensive acceptance campaign is `NOT_RUN`. No merge or direct master push is authorized.

## Final diff and review status

The focused guard was reviewed against the reproduced defect and independently checked with the actual current workflow contracts. This pair follows the native scaffold headings. Changed-file Secrets, bilingual/archive checks and the regular commit are recorded separately when actually completed; no final published-pair approval is asserted.
