# Change Record: NGINX configtest path authority

**Language:** English | [Deutsch](CR-20261003-nginx-configtest-path-authority.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261003-nginx-configtest-path-authority` |
| Date (UTC) | `2026-10-03` |
| Base revision | `acefed5c81a56f636610601edcc447a257b9e947` |
| Framework, frozen | `b9b9534b7e0b15edad31393699ebd0617748148d` |
| MRTS, unchanged | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery status | Local CI/Sonar remediation; PR #355 OPEN, PR #396 DRAFT; remote checks pending |

## Motivation and problem statement

The configtest driver and selected-case wiring admitted writable output
parents/ancestors and build/results/configuration parents. Test-first checks
observed six negative subcontrols failing to reject those inputs, while the
owned `0755` positive control passed. The correction applies the established
external-runtime directory authority contract to those exact parents.
Remote Sonar review at the published base is remediation input, not passing
evidence: Quality Gate `ERROR`, 12 reported issues. Two static security leads
remain `needs_review`; neither is published here as a confirmed exploit or
dismissed finding.

## Acceptance criteria

Reject writable parents and unsafe existing result files before execution or
append. Preserve allowed owned `0755` parents, legitimate `0644` results,
external-root containment, checkout exclusion, fresh private `0700` children,
selected Boolean/size diagnostics and receipt identity. Reject stale case
children. Keep mechanical complexity/test/shell changes behavior-preserving.
Verify focused tests, negative controls, static checks and bilingual documents;
remote CI and a fresh exact-head Sonar result remain separate gates.

## Implementation decision and rationale

Reuse non-following `ensure_safe_runtime_directory` for the exact external
parents instead of creating another directory-admission policy. Existing
result files must be effective-UID-owned regular files with one hard link,
no `0022` permission bits and size at most 4 MiB. Reject an existing case
child before append. Preserve `/var/tmp/codex/ModSecurity-conector`
containment and checkout exclusion.
New parents retain mode `0700` rather than inheriting the helper's default
`0755`; explicit positive fixtures also prove that existing owned `0755`
parents and legitimate `0644` results retain those modes.

Separate mechanical S3776 refactors of collector, driver and dispatcher,
split assertions and no-op shell defaults retain semantics. Worker
characterizations passed 954 parity controls and header-baseline parity;
these observations are distinct from final combined regression validation.
Delivery is phased: the authority correction and its paired record precede
the separate mechanical follow-up in the same publication batch. This record
describes the combined validated scope without conflating the commits.

## Changed files

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-selected-nginx-configtests.py`
- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_configtest_driver.py`
- `tests/test_nginx_selected_configtest_wiring.py`
- `tests/test_nginx_configtest_collection.py`
- `tests/test_nginx_h1_request_protocol.py`
- `tests/test_protected_nginx_exact_head_builder.py`
- `docs/testing-and-evidence.md` and `docs/testing-and-evidence.de.md`
- This Change Record pair and `reports/audits/change-records/README.md` / `README.de.md`

## Commands executed

### Tests and actual results

Observed test-first state: six negative path-authority subcontrols RED;
owned `0755` positive control green. An immutable replay at
`ac4c746f6a4c07006f25b078f660e31b16341479` ran nine tests: the safe positive
control passed and nine negative subcontrols failed across two parent modes;
subtests account for the difference between test and failure counts.

Final coordinator verification through
`/var/tmp/codex/ModSecurity-conector/analysis/verify-pr396-ci-remediation.py`
orchestrated RTK-wrapped commands and retained complete logs/exit receipts:

- Protected focus: 139 tests PASS; current NGINX/runtime/collector/config focus: 237 tests PASS. Total: 376 tests, no skips, `pr396-ci-final-focus.exit` = 0.
- Path-authority/mode focus: 33 tests PASS after the guards and again after both main refactor extractions. Independent reviewer: 96 tests PASS.
- Worker characterization: 954 parity controls and header-baseline parity PASS.
- Python compilation, `sh -n`, error-level ShellCheck, all-workflow actionlint, native bilingual/path/link checks and `git diff --check`: PASS; `pr396-ci-static.exit` = 0.

Logs and receipts are under `/var/tmp/codex/ModSecurity-conector/analysis/`.
These tests use fake source/fixture executables and establish contract behavior,
not real NGINX host execution or a new configuration/runtime evidence bundle.
The documentation checkpoint ran
`rtk proxy make check-bilingual-docs check-doc-links PYTHON=python3 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/pr355-integration-docs`
with exit 0, including repository path references. `rtk proxy git diff --check`
also exited 0. These checks do not replace focused source validation.

## Security impact

The correction strengthens existing output/result authority without weakening
artifact, receipt, collector or protected-host admission. The two static
security leads are review inputs requiring validation. FND-PARENT-1038 remains
subject to exact-head verification and FND-PARENT-1036 to its external
dependency; these source/fixture checks do not resolve their host/archive
requirements. No exploit details, secrets or raw evidence are published here.

## Runtime evidence

No HTTP request, daemon startup, protected-host runtime or independent
attestation is claimed. Existing config-only receipts retain their original
identity; no new runtime evidence is invented. Exact-Head E2E PASS: NO.

## Known limitations

Local focused and static validation passed. Remote CI and Sonar results for this
local successor are not yet observed. Framework and MRTS are unchanged.

## Remaining risks

Path admission and file metadata checks establish only their tested layer.
Fresh remote checks and any applicable host verification remain required;
the current published base's failing Quality Gate is not reclassified.

## Checks not run and rationale

Full Exact-Head E2E, MIME work and protected runtime are outside this CI/Sonar
remediation slice. PR #355 remains OPEN pending verified supersession;
PR #396 remains DRAFT. No new local-successor push or closure is asserted.

## Final diff and review status

Local source/fixture remediation and focused/static validation PASS for the
15-file scope listed above, including both documentation pairs and indexes.
Delivery remains INCOMPLETE:
Remote CI/Sonar remain pending; no current remote-green claim is made.
