# Change Record: latest stable Go release contract

**Language:** English | [Deutsch](CR-20260912-go-latest-release-contract.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260912-go-latest-release-contract |
| Date (UTC) | 2026-09-12 |
| Base revision | `3c3908dbb3a87a18d823ab8f1a286ba5b9c00e94` |
| Delivery status | Parent PR #365 contains this paired record. Branch, exact head, hosted checks, reviews, Ready state, and any merge result are delivery-lifecycle facts asserted only after observation; this record itself neither grants nor asserts a merge. |

## Motivation and problem statement

At the base revision, the committed selector `1.27.0` was already an exact
stable Go release but the Go updater, its source contract, and CodeQL's
trusted-base selector still accepted only the `1.26.N` series. The updater
would therefore choose an obsolete series and the CodeQL Go jobs would reject
the committed selector before analysis. This is tracked as
`FND-PARENT-1085`.

PR #363 is reviewed as context only: it updates submodule pointers and does
not contain this Parent-owned Go updater correction. This change does not
modify Framework or MRTS source, Gitlinks, module language baselines,
workflow permissions, action pins, dependency locks, or repository merge
settings; it never directly writes `master`.

## Acceptance criteria

- The updater accepts exact stable numeric `MAJOR.MINOR.PATCH` releases,
  rejects malformed, prerelease, and non-stable metadata, and resolves the
  greatest stable numeric release without a fixed Go minor-series assumption.
- The committed Go contract and trusted-base CodeQL selector accept the same
  exact numeric-release grammar while retaining fail-closed validation and
  pinned trusted-base checkout behavior.
- The scheduled updater separates read-only resolution, read-only validation,
  and narrowly scoped publication under the renamed release-oriented jobs.
- Focused updater, contract, workflow-security, Python-contract, and
  bilingual-documentation checks provide recorded local evidence; unavailable
  hosted and locally incompatible Go-module checks remain explicitly bounded.
- English and German documentation and this paired Change Record describe the
  same current selector and release-oriented workflow structure.

## Implementation decision and rationale

- Resolve the greatest stable numeric release only at the updater's bounded
  scheduled or manually dispatched resolution. Pull-request CodeQL consumes
  the committed trusted-base selector instead of querying live release
  metadata, preserving reproducibility and avoiding a new external trust
  dependency on every analysis run.
- Generalize the Python parser and checker grammar to positive major versions
  with canonical minor and patch components. Tuple ordering supplies explicit
  monotonicity across future Go release series.
- Rename the updater stages to `resolve-go-release`, `validate-go-release`,
  and `create-go-update-pr`; preserve the read-only resolver/validator and the
  constrained publisher boundary. The publisher remains limited to
  `.go-version` and the fixed, independently validated Envoy component bundle.
- Keep module `go` and `toolchain` directives independent: they are module
  compatibility contracts, not the repository CI-toolchain selector.

## Security impact

The correction restores the trusted selector's availability for CodeQL Go
analysis without relaxing its input validation, action pins, permissions,
trusted-base checkout, or `check-latest: false` reproducibility control. The
updater continues to reject redirects, malformed or oversized metadata,
unexpected version changes, unsafe file targets, and unapproved component
changes. A source-only concern about `GOTOOLCHAIN=local` behavior remains
deferred pending hosted execution evidence; this change does not weaken that
control or claim a hosted result.

## Changed files

- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/update-go-version.yml`
- `ci/checks/common/check-go-version-contract.py`
- `ci/checks/common/check-python-version-contract.py`
- `scripts/update-go-version.py`
- `scripts/version_updater_common.py`
- focused updater, Go-contract, and CI-security workflow tests
- paired English/German build and CI-security documentation
- this paired Change Record and the Change-Record indexes

## Commands executed

| Check | Actual result |
| --- | --- |
| Baseline Go contract at `3c3908dbb3a87a18d823ab8f1a286ba5b9c00e94` | failed as expected: the old checker rejected the committed `1.27.0` selector; retained in the task run evidence. |
| Live updater check | passed: the official endpoint returned `current_version=latest_version=1.27.1`, `status=current`, and `update_available=false`. |
| Focused updater, Go-contract, workflow-security, Python-contract, and bilingual unit suite | passed: 91 tests. |
| Bounded component regression suite | passed: 15 tests. |
| `make check-go-version-contract` and `make check-ci-security-contract` | passed; the CI-security contract ran 125 tests with five documented environment capability skips. |
| `actionlint` and offline `zizmor` for the changed workflows | passed; zizmor reported no findings. |
| Workflow-equivalent Go module matrix | passed for Envoy ext_proc and the three Traefik modules with `GOTOOLCHAIN=local`, `GOWORK=off`, and task-owned external caches. |
| `make check-bilingual-docs` | blocked only by pre-existing missing Framework Gitlink link targets in the intentionally uninitialized task worktree; no task-owned paired-document or Change-Record error remained. |
| `make check-python-version-contract` | blocked by pre-existing unlisted/malformed Python-shell workflow inventory violations outside this task; its dedicated unit suite passed. |
| Fresh post-patch security review | passed: no plausible new security finding in the scoped diff. |

## Runtime evidence

This static source record does not assert a specific hosted workflow, CodeQL
analysis, SonarQube Cloud analysis, runtime connector matrix, exact PR head,
review, or merge result. The local Go executable is `1.27.1`, matching the
selected CI selector; the four workflow-equivalent Go module validations passed
with `GOTOOLCHAIN=local` and `GOWORK=off` in task-owned external caches.
That local result does not replace delivery evidence bound to the current exact
PR head.

## Known limitations

The local Python executable is `3.14.4`, below the checked-in
`.python-version` selector `3.14.7`; the Go module matrix nevertheless used
the matching local Go `1.27.1` toolchain. The checked-in documentation link
inventory also includes Framework targets absent from this intentionally
uninitialized task worktree. No Framework/MRTS initialization or modification
is authorized.

## Remaining risks

`FND-PARENT-1085` is not closed by source editing alone. Its original source
failure must no longer reproduce and the current exact PR head needs its
applicable hosted controls before a verified integration claim. Any failed
hosted control must be triaged as new evidence. A merge requires a separate
current-user authorization and exact-head evidence; this static source record
neither supplies that authorization nor asserts a later merge result.

## Checks not run and rationale

The source-validation suite does not substitute for CodeQL Go analysis or
applicable hosted PR controls. Those controls are evaluated against the
current exact PR head during the delivery lifecycle; this static record does
not classify a planned or later delivery result as passed.

## Final diff and review status

The focused local checks and fresh post-patch security review are complete.
The final source-diff readback is complete. Delivery branch, PR, exact-head,
hosted-check, review, and merge facts are retained only after observation in
the delivery lifecycle; this source record does not pre-assert them.
