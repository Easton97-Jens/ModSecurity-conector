# F-GS-003 — Pinned NGINX release provenance for full smoke

**Language:** English | [Deutsch](CR-20260802-f-gs-003-pinned-nginx-release-asset.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | F-GS-003 |
| Date (UTC) | 2026-08-02 |
| Base revision | 97afc25007a20fff0c637d364745a22c2feb7bba |

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

Framework provenance is recorded separately from Parent delivery. Framework
PR #60 had head 9c4ebef13eab8cfb2e8626bbf2738023c2320ad5 before integration. A
requested SHA-bound merge was rejected because merge commits are disabled; the
repository-approved SHA-bound squash merge completed at
2026-08-02T13:29:14Z. Its PR #60 merge/master result is
8362b569406cabc5237a41e4e46f0505fb04c51f, which is intentionally the
Parent gitlink target in this task worktree.

## Changed files

The following is the reconciled task-worktree inventory after Core, evidence,
and test-slice integration.

- .github/workflows/test-full-smoke-sequential.yml
- ci/checks/evidence/check-runtime-producer-readiness.py
- ci/evidence/reports/generate-system-environment-proof.py
- ci/evidence/reports/update-runtime-reports.py
- ci/provisioning/components/prepare-runtime-components.py
- ci/provisioning/components/prepare-runtime-components.sh
- connectors/nginx/README.md and connectors/nginx/README.de.md
- connectors/nginx/harness/README.md and connectors/nginx/harness/README.de.md
- docs/reference/variables.md and docs/reference/variables.de.md
- modules/ModSecurity-test-Framework gitlink
- tests/test_prepare_runtime_components.py
- tests/test_report_presentation_literals.py
- tests/test_runtime_component_cache_contract.py
- tests/test_runtime_component_cache_identity.py
- tests/test_runtime_env_snapshot_contract.py
- tests/test_evidence_output_security.py

## Commands executed

- The repository workflow YAML checker completed successfully for
  .github/workflows/test-full-smoke-sequential.yml.
- Scoped static assertions completed successfully for the exact full-smoke
  NGINX tuple, the absence of latest selectors in that workflow, and the
  wrapper export of the provenance variables.
- The bilingual-documentation checker and variable-documentation checker
  completed successfully after this Change Record was added.
- Shell syntax validation completed successfully. ShellCheck reported only the
  three pre-existing diagnostics already present in the base wrapper.
- Scoped git diff --check completed successfully for the documentation and
  workflow slice at the time it was run.
- On the non-CI-equivalent local Python 3.14.4 interpreter, AST parsing
  passed; the producer-readiness path-policy test passed 4/4, the evidence
  output-security test passed 9/9, and the report-presentation unittest module
  passed 5/5. The evidence-slice diff check passed, and no
  nginx-latest-release.json consumer reference was found.
- The integrated focused diagnostic suite passed 108 tests on the existing
  Parent virtual-environment interpreter (Python 3.14.4), with
  `PYTHONDONTWRITEBYTECODE=1` and an external `PYTHONPYCACHEPREFIX`. This is
  useful local evidence only; the project requires Python 3.14.6 for
  CI-equivalent validation.
- Python compilation of the changed resolver and system-environment proof
  reporter passed. A final scoped `git diff --check` passed before delivery.

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

No Parent build, smoke run, runtime-environment snapshot, producer-readiness
output, or system-environment proof has been accepted for this change.

When produced, the required managed full-smoke runtime-evidence record must
identify the release, ref, and asset; expected and actual archive SHA-256
values; source version and directory; binary path, SHA-256, and version
readback; configure arguments; build, Framework, and Parent identifiers; and
generated time. This field list is a required schema, not a claim that a
current Parent runtime record exists.

The observed Framework integration evidence is limited to the following:
Framework PR #60 exact-head PR checks and Sonar Zero/Quality Gate passed
before integration; post-merge Framework master workflows test-common,
OpenSSF Scorecard, CodeQL analysis, and lint passed. This is Framework
provenance only, not Parent runtime, CI, PR, or merge evidence.

## Known limitations

The repository-required Python 3.14.6 virtual environment is unavailable
locally; the available system interpreter is Python 3.14.4 and is not
CI-equivalent evidence.

Core, evidence, and test slices are integrated, including the diagnostic
archive-side-effect, producer-to-checker contract, and system-proof
no-NGINX-I/O-before-contract coverage. The focused 108-test result was
produced only with Python 3.14.4, so it is not CI-equivalent validation.

## Remaining risks

- The diagnostic suite has not run under the repository-required Python 3.14.6
  environment.
- Hosted workflow, Parent runtime, Parent CI, Parent PR, and Parent merge
  evidence have not yet been observed.

## Checks not run and rationale

- actionlint was not run locally because it is not installed or provisioned by
  this task; hosted actionlint remains pending.
- Parent unit and integration tests were not run under the required Python
  3.14.6 environment because that exact environment is unavailable. The
  focused 108-test diagnostic suite instead ran on the existing Parent virtual
  environment with Python 3.14.4 and is explicitly non-CI-equivalent.
- Parent build, runtime smoke, evidence generation, manual full-smoke matrix,
  CI, PR, and merge checks remain pending as hosted runtime and delivery
  evidence.

## Final diff and review status

Status at record preparation is in progress, not complete. An independent
English/German NGINX documentation parity review passed, and the
Core/evidence/test slices are integrated. The final Parent diff, hosted runtime
validation, Parent CI, PR, and merge disposition must be reviewed before
completion is declared. No Parent delivery action is claimed by this record.
