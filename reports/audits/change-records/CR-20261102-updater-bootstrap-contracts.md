# Change Record: CR-20261102-updater-bootstrap-contracts

**Language:** English | [Deutsch](CR-20261102-updater-bootstrap-contracts.de.md)

Scoped updater bootstrap repair.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261102-updater-bootstrap-contracts |
| Date (UTC) | 2026-11-02 |
| Base revision | `430d3194fa04ca4aafcdaef6aeb256d21dc18f0c` |

## Motivation and problem statement

Run `41412832386` reached a YAML-dependent candidate check before preparing PyYAML. Run `41412784227` exposed verifier commands without the required `-P`.

## Acceptance criteria

Prepare the existing hash-locked dependency while Framework still matches the Parent gitlink; preserve candidate isolation. Match updater interpreter-verifier commands to the pinned Framework contract and order all affected native bootstrap jobs as provenance shell gate, Python setup, stdlib interpreter verifier, context binding, then other Python consumers.

## Implementation decision and rationale

Move the unchanged dependency-preparation block before candidate checkout and the YAML-dependent contract. Add `-P` to the Python, Go and submodule verifier calls; preserve version and interpreter-path arguments. Reorder 27 context bindings across 13 native workflows, add canonical setup/verifier to the submodule resolver, and authenticate initialized Framework HEAD against the committed gitlink before checked-out verifier execution. Keep the trusted-base Go resolver compatibility exception unchanged.

## Changed files

`.github/workflows/ci-security-codeql.yml`, `.github/workflows/ci-security-secrets.yml`, `.github/workflows/ci-security-workflow-lint.yml`, `.github/workflows/lint.yml`, `.github/workflows/protocol-contract.yml`, `.github/workflows/sonar-native-security.yml`, `.github/workflows/sonarqube.yml`, `.github/workflows/update-go-version.yml`, `.github/workflows/update-python-version.yml`, `.github/workflows/update-submodules.yml`, `.github/workflows/update-workflow-tools.yml`, `.github/workflows/validate-go-candidate.yml`, `.github/workflows/verified-report-governance.yml`, `ci/tools/sync-framework-component-versions.py`, `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.md`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.de.md`.

## Commands executed

RTK-wrapped focused Python probes using the existing Parent virtual environment: PASS for eight verifier steps and eight bare-command negative controls. The YAML projection seam fails with `ModuleNotFoundError: No module named 'yaml'` with site dependencies disabled, and reads 17981 bytes with the existing dependency available. The native Change Record generator ran with explicit connector/Framework context. Initial generator invocations without package/context paths failed before file creation.

Composed static validation using the separately edited Framework source detected 53 Python jobs with zero violations. Moving scaffold context before setup was rejected in a negative control; the actual added shell gate accepted matching and rejected mismatching initialized Framework identities. The unchanged pinned Framework checker still reports 45 violations in composite ordering, protected mapping and closed job inventories; these are a separate Framework delivery/pin prerequisite. For immutable-action jobs, the provenance gate checks both the committed gitlink and initialized checkout against the selected immutable action SHA before checked-out Python runs. The closed synchronizer registry now owns all six early gate pins alongside action/input pins. No-op and pin-change roundtrips pass for all 22 registered workflow projections; stale, missing, extra and symbolic gate pins fail closed. The actual shell gate rejects even a matching changed gitlink/checkout when it differs from the selected immutable action SHA. All 27 native context jobs retain workflow/job permissions and enforce provenance gate before verifier and context after verifier; all gate scripts passed `bash -n`. No changed gitlink or hosted result is claimed.

## Security impact

Preparation executes pinned installer code and reads the pinned Framework lock before candidate checkout. Candidate permissions, sandbox, hash checks, dependency allowlists and publisher authority are unchanged. `-P` removes the implicit script-directory import path.

## Runtime evidence

No hosted workflow or connector runtime was executed. Local evidence proves verifier shape and the YAML-import prerequisite only.

## Known limitations

Framework-wide closed workflow inventories and bootstrap ordering remain separate prerequisites. This change does not establish that the complete Python updater succeeds.

## Remaining risks

An authorized hosted rerun is still needed to establish full updater behavior; later independent contract failures may remain.

## Checks not run and rationale

No package installation, full suite, hosted CI, publisher, Sonar or runtime execution: outside this focused local repair. No commit, push, PR, gitlink or MRTS change by this worker.

## Final diff and review status

Focused diff reviewed; `git diff --check` passed. `rtk make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/parent-updater-contracts-20261102/modules/ModSecurity-test-Framework` passed, including repository path references. Delivery remains with the coordinating agent.
