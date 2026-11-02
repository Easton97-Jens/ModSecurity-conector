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

`.github/workflows/ci-findings-regressions.yml`, `.github/workflows/ci-security-codeql.yml`, `.github/workflows/ci-security-secrets.yml`, `.github/workflows/ci-security-workflow-lint.yml`, `.github/workflows/lint.yml`, `.github/workflows/nginx-root-broker.yml`, `.github/workflows/open-connectors-smoke.yml`, `.github/workflows/protocol-contract.yml`, `.github/workflows/quick-framework-check.yml`, `.github/workflows/reusable-five-connectors-profile.yml`, `.github/workflows/run-protected-nginx-exact-head.yml`, `.github/workflows/run-protected-nginx-root-broker.yml`, `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml`, `.github/workflows/sonar-native-security.yml`, `.github/workflows/sonarqube.yml`, `.github/workflows/test-apache.yml`, `.github/workflows/test-common.yml`, `.github/workflows/test-connectors-with-crs-no-mrts.yml`, `.github/workflows/test-envoy.yml`, `.github/workflows/test-full-smoke-sequential.yml`, `.github/workflows/test-haproxy.yml`, `.github/workflows/test-lighttpd.yml`, `.github/workflows/test-nginx-exact-head.yml`, `.github/workflows/test-nginx.yml`, `.github/workflows/test-traefik.yml`, `.github/workflows/update-go-version.yml`, `.github/workflows/update-python-version.yml`, `.github/workflows/update-submodules.yml`, `.github/workflows/update-workflow-tools.yml`, `.github/workflows/validate-go-candidate.yml`, `.github/workflows/verified-report-governance.yml`, `ci/tooling/project-versions.lock.json`, `ci/tools/sync-framework-component-versions.py`, `docs/security/ci-security-tooling.de.md`, `docs/security/ci-security-tooling.md`, `modules/ModSecurity-test-Framework`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.de.md`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.md`.

## Commands executed

RTK-wrapped focused Python probes using the existing Parent virtual environment: PASS for eight verifier steps and eight bare-command negative controls. The YAML projection seam fails with `ModuleNotFoundError: No module named 'yaml'` with site dependencies disabled, and reads 17981 bytes with the existing dependency available. The native Change Record generator ran with explicit connector/Framework context. Initial generator invocations without package/context paths failed before file creation.

Composed static validation using the separately edited Framework source detected 53 Python jobs with zero violations. Moving scaffold context before setup was rejected in a negative control; the actual added shell gate accepted matching and rejected mismatching initialized Framework identities. The initial unchanged Framework pin reported 45 violations in composite ordering, protected mapping and closed job inventories. Following explicit user authorization, the coordinator integrated joint Framework revision `0ca218773b11bbd401478808b4e8a11af123df57`, including Python 3.15 and the Framework contract repairs; the native Python contract now passes for 53 jobs. For immutable-action jobs, the provenance gate checks both the committed gitlink and initialized checkout against the selected immutable action SHA before checked-out Python runs. The closed synchronizer registry now owns all six early gate pins alongside action/input pins. No-op and pin-change roundtrips pass for all 22 registered workflow projections; stale, missing, extra and symbolic gate pins fail closed. The actual shell gate rejects even a matching changed gitlink/checkout when it differs from the selected immutable action SHA. All 27 native context jobs retain workflow/job permissions and enforce provenance gate before verifier and context after verifier; all gate scripts passed `bash -n`. The Parent working tree now contains the authorized joint Framework gitlink and 23 generated views (project lock plus 22 workflows). No hosted result is claimed.

The coordinator ran `rtk bypass env PYTHONNOUSERSITE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/framework-python315-20261102/parent /root/git/ModSecurity-conector/.venv/bin/python ci/tools/sync-framework-component-versions.py --sync --framework-common /var/tmp/codex/ModSecurity-conector/runs/framework-python315-20261102/parent/framework-common-0ca2187.sh --framework-sha 0ca218773b11bbd401478808b4e8a11af123df57`; replacing `--sync` with `--check` passed without further changes. The input is the exact `0ca218773b11bbd401478808b4e8a11af123df57:ci/lib/common.sh` Git blob. Native `make check-python-version-contract` with explicit task-child `FRAMEWORK_ROOT` and `/var/tmp/codex/ModSecurity-conector/runs/framework-python315-20261102/venv/bin/python` passed for 53 jobs. `verify-framework-candidate-contract.py` with full explicit context and the Parent virtual environment passed for the same revision and NGINX `release-1.31.6`.

## Security impact

Preparation executes pinned installer code and reads the pinned Framework lock before candidate checkout. Candidate permissions, sandbox, hash checks, dependency allowlists and publisher authority are unchanged. `-P` removes the implicit script-directory import path.

## Runtime evidence

The local checks do not execute a hosted workflow or connector runtime. Local evidence proves the joint Python workflow contract, exact Framework candidate contract and YAML-import prerequisite; it does not prove hosted updater or connector runtime behavior.

## Known limitations

The jointly checked revision `0ca218773b11bbd401478808b4e8a11af123df57` is the reviewed integration pin at this record. A subsequent Framework change requires fresh synchronization and native checks. This change does not establish that the complete hosted Python updater succeeds.

## Remaining risks

An authorized hosted rerun is still needed to establish full updater behavior; later independent contract failures may remain.

## Checks not run and rationale

No package installation, full suite, hosted CI, publisher, Sonar or runtime execution: outside this focused local repair. The coordinator committed native Parent fixes as `df858e0b04d851b392accc95f70118489c2d02f2`; joint Framework revision `0ca218773b11bbd401478808b4e8a11af123df57` is on Framework PR #158. Parent pin delivery and hosted success are not yet claimed. No MRTS source or child `tools/MRTS` gitlink change; it and the Parent MRTS lock remain `8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Final diff and review status

Focused diff reviewed; `git diff --check` passed. `rtk make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/parent-updater-contracts-20261102/modules/ModSecurity-test-Framework` passed, including repository path references. Delivery remains with the coordinating agent.

Coordinator evidence: the joint Framework pin is updated to `0ca218773b11bbd401478808b4e8a11af123df57`; fresh native synchronization and no-op checking passed. 78 focused Parent projection/Python/installer tests previously passed on actual Python 3.15.2 at the joint intermediate revision; its Product bootstrap is unchanged. The package-source repair affects Framework Sonar CI. Fresh hosted Parent checks remain required.

The first hosted Parent follow-up at `73984fd57c9b2c4030a72e41aa489c66196a5b6e` passed source admission and Python 3.15.1 interpreter verification, then correctly rejected stale Framework source digests in the active inventory. The new joint Framework pin uses the existing generator to renew exactly ten digest values; every other inventory field and all 100 automatic default cases remain unchanged. Native inventory admission passes locally. Fresh hosted checks of the updated Parent commit remain required. MRTS was not initialized locally; CI must provide the complete materialization check.

The follow-up check at Parent `5aafe1be10f4893dc73c24d33f37988f0f697f30` reached the downstream declarative specialist archive. Its stale generated view was renewed natively in Framework; complete `make check-active-inventory` then passed with both inventory and archive on Python 3.15.2. The updated gitlink and all managed action references jointly consume that archive follow-up commit. Automatic test scope and validation rules remain intact.

The final joint Framework pin also prevents recurrence on the next ordinary Python/component update: inventory and specialist archive are regenerated natively in order; closed publisher paths, base-derived Git-blob proof before checkout and common-maintenance transaction rollback remain enforced. 105 focused Framework tests and a real synthetic offline pin projection passed. The Parent receives no additional write or merge authority.
