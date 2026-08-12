# F-GS-003 — Pinned NGINX release provenance for full smoke

**Language:** English | [Deutsch](CR-20260802-f-gs-003-pinned-nginx-release-asset.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | F-GS-003 |
| Date (UTC) | 2026-08-02 |
| Base revision | a308e52508a46a62b2f948245ebfa8e153f73bce |

## Motivation and problem statement

The full-smoke NGINX source selection used a mutable release selector. That
cannot provide a reproducible or reviewable source provenance record for a
security-sensitive runtime build. This change records the intended fixed
release tuple and the related evidence boundary.

## Acceptance criteria

- The full-smoke workflow supplies the reviewed NGINX 1.31.3 release tuple:
  GitHub release mode, the nginx/nginx repository, release-1.31.3 tag and
  ref, nginx-1.31.3.tar.gz asset, and SHA-256
  a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525.
- Mutable latest selectors are not accepted as full-smoke provenance, and the
  resolver validates the fixed tuple before cache, network, download, or
  extraction work.
- Cache identity binds the complete tuple; the strict full-smoke flag rejects
  inherited system or MRTS NGINX overrides as evidence.
- The manual cleanup input is boolean and default-off. Cleanup runs only after
  an explicit opt-in, while the smoke job keeps its dependency and uses an
  always condition so a skipped cleanup does not skip smoke execution.
- English and German NGINX and variable documentation describe the same
  release provenance boundary.
- Parent runtime, CI, pull-request, and merge evidence remain pending and are
  not acceptance evidence in this record.

## Implementation decision and rationale

The workflow and wrapper pass the complete fixed tuple to the Parent resolver.
The design rejects mutable selectors early, binds cache reuse to every reviewed
tuple member, verifies the archive digest, and makes the strict full-smoke
path refuse inherited native NGINX binary or module overrides. Direct release
asset provenance replaces any latest-release discovery.

Artifact cleanup can delete prior evidence, so it is deliberately not a normal
manual-run side effect. The cleanup-artifacts job is gated by the
workflow-dispatch cleanup_artifacts input, whose default is false. The smoke
job retains its needs relationship and explicitly tolerates the skipped
cleanup job.

The Parent master synchronization adopts the Framework gitlink
`209389022c942d83113f6be88bf31d25637352f0` from its already-merged Parent
base. It is not a change created by F-GS-003, and this Change Record neither
asserts a Framework change nor investigates Framework PR #74.

## Changed files

The following is the reconciled Parent inventory for the PR range after the
2026-08-12 merge of the current Parent base. The Framework gitlink is not in
this list because it is base-derived, not an F-GS-003 change.

- .github/workflows/test-full-smoke-sequential.yml
- Makefile
- ci/checks/evidence/check-runtime-producer-readiness.py
- ci/evidence/reports/generate-system-environment-proof.py
- ci/evidence/reports/update-runtime-reports.py
- ci/provisioning/components/prepare-runtime-components.py
- ci/provisioning/components/prepare-runtime-components.sh
- ci/runtime/lifecycle/prepare-fresh-crs-source.sh
- connectors/nginx/README.md and connectors/nginx/README.de.md
- connectors/nginx/harness/README.md and connectors/nginx/harness/README.de.md
- docs/reference/variables.md and docs/reference/variables.de.md
- tests/test_prepare_runtime_components.py
- tests/test_report_presentation_literals.py
- tests/test_runtime_component_cache_contract.py
- tests/test_runtime_component_cache_identity.py
- tests/test_runtime_env_snapshot_contract.py
- tests/test_evidence_output_security.py

`prepare-fresh-crs-source.sh` is retained in this Parent range as a distinct
CRS-source separation helper. It does not remediate or validate the separate
broker/CRS findings. APR-util/provider work, broker repairs, and CRS failure
disposition remain outside F-GS-003 and are not merge blockers for this
provenance-only acceptance path.

## Commands executed

- On 2026-08-12, the current local static validation completed successfully
  with the existing non-CI-equivalent Parent Python 3.14.4 virtual environment:
  the six focused runtime-component/evidence unittest modules exited zero; the
  two F-GS-003 workflow-contract test methods passed; changed Python files
  compiled; changed shell files passed `sh -n`; and the repository workflow
  YAML checker accepted all 29 workflow YAML files.
- `make check-ci-security-contract` passed locally: 26 tests, actionlint,
  zizmor, and gitleaks validation all succeeded. These are static/local checks,
  not a runtime provision or hosted-gate result.
- Two independent `make --no-print-directory prepare-runtime-components` runs
  with `RUNTIME_COMPONENT_TARGET=nginx`, fixed NGINX 1.31.3 tuple, and isolated
  external build/cache/report roots exited zero before the final traceability
  commit. This pre-final-commit local evidence is tied to Parent `1aa5f6f7` and
  is a useful consistency check, not final PR-head evidence. Their report SHA-256 values
  are `0927d2e4f912038c47d681bd401ba8f88f28322986af85f3833b2be68282999c`
  (run A) and `be456afbd3021f669bdf5fa13e818774332b2ec6ff9119357d32bbd9acc4ba42`
  (run B). Each report records the expected NGINX archive checksum
  `a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525` as
  `PASS` and a valid runtime contract. Only `modsecurity-v3` and `expat` were
  selected Git components; Apache, HAProxy, go-ftw, and albedo were
  `not_selected`. The observed binary/module SHA-256 identifiers were
  `f19f8b9a…afc7e` / `40a5c734…9b38` (run A) and
  `087c5e5e…5b1e` / `03b49502…f4fd` (run B), at Parent `1aa5f6f7` and
  Framework `209389`. No MRTS workload was invoked; an inert configured root
  is not an MRTS workload or evidence claim.
- A scoped `git diff --check` passed after synchronization. Bilingual and
  variable-documentation checks remain part of the final documentation
  validation and are not claimed here until rerun against this reconciliation.

## Security impact

The intended control is fail-closed release provenance: a reviewed tuple must
be complete and valid before cache or acquisition work, and the archive must
match its reviewed digest before use. The full-smoke strict mode prevents
inherited system or MRTS NGINX artifacts from being presented as the required
managed-build evidence.

The integrated Core, evidence, and test slices additionally bind the managed
module path to the producer record and reject MRTS or system-path mismatches.
This record still does not claim that Parent runtime enforcement has been
fully proven: hosted runtime and CI evidence remain pending.

Final local diff review found that the system-environment proof reporter could
formerly execute an environment-selected `NGINX_BIN -v` before the new managed
runtime-contract validation. The reporter now obtains the contract first,
fails closed when it is not `PASS`, ignores `NGINX_BIN` and framework candidate
fallbacks, and invokes only the contract `binary_path` after a fresh SHA-256
readback. Regression tests prove both no lookup/execution for an invalid
contract and no execution after a binary-digest mismatch.

## Runtime evidence

Two fresh Parent NGINX-only provisions have been accepted as local runtime
evidence before the final traceability commit. They used independent task-owned
external roots retained in a non-versioned, hash-bound receipt and did not run
a host smoke, a hosted workflow, or an MRTS workload. They do not replace the
pending runtime-environment snapshot, producer-readiness output, or
system-environment proof required by the full delivery lifecycle. Two fresh
isolated provisions must be rerun after the final versioned commit and push;
they are not yet claimed as final PR-head provisions.

When produced, the required managed full-smoke runtime-evidence record must
identify the release, ref, and asset; expected and actual archive SHA-256
values; source version and directory; binary path, SHA-256, and version
readback; configure arguments; build, Framework, and Parent identifiers; and
generated time. This field list is a required schema, not a claim that a
current Parent runtime record exists.

The base-derived Framework gitlink is a dependency identity only; it is not
Framework runtime, CI, PR, or merge evidence for this Parent change.

## Known limitations

The repository-required Python 3.14.6 virtual environment is unavailable
locally; the available system interpreter is Python 3.14.4 and is not
CI-equivalent evidence.

The current local Python is 3.14.4 rather than the repository-required 3.14.6,
so all locally observed Python results remain non-CI-equivalent.

## Remaining risks

- The current local suite has not run under the repository-required Python
  3.14.6 environment.
- No host smoke, hosted workflow, Parent CI, Parent PR, or Parent merge
  evidence has been observed.
- The two recorded isolated provisions predate the final traceability commit;
  final PR-head provisions remain required.

## Checks not run and rationale

- The current focused local Python checks are not CI-equivalent because Python
  3.14.6 is unavailable locally.
- Host smoke, remaining runtime evidence generation, hosted checks, exact-head
  PR gates, final PR-head isolated provisions, and merge verification remain
  pending delivery evidence.

## Final diff and review status

Status remains in progress, not complete. The final Parent diff, host-smoke and
hosted runtime validation, final PR-head isolated provisions, Parent CI,
exact-head PR gates, and merge
disposition must be reviewed before completion is declared. No Parent delivery
action is claimed by this record.
