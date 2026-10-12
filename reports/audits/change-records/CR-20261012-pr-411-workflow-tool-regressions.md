# Change Record: CR-20261012-pr-411-workflow-tool-regressions

**Language:** English | [Deutsch](CR-20261012-pr-411-workflow-tool-regressions.de.md)

Parent-only repair of the evidenced PR #411 workflow-tool regressions.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261012-pr-411-workflow-tool-regressions |
| Date (UTC) | 2026-10-12 |
| Base revision | `159624d7976f881862cfa1d20f27543090a1727d` |

## Motivation and problem statement

PR #411 updated immutable Action pins and zizmor. Its original head failed Security workflow lint (run `38253812611`) and hosted NGINX (run `38253812702`). CodeQL fixtures depended on the live lock; zizmor introduced a self-repository audit; the isolated NGINX step lost the prepared runtime snapshot and prepared again.

## Acceptance criteria

Repair the observed failures, retain checksum/permission/isolation controls, verify legitimate and negative behavior, run the checks before future tool publication, and push a normal follow-up into PR #411 without merging.

## Implementation decision and rationale

Use explicit synthetic release baselines and isolate checkout fixtures from live pin changes. Run the complete nonrecursive updater unit class in the native contract; keep real copied-tree integration separate. Execute checksum-verified proposed actionlint/zizmor, including positive and negative fixtures, before publication. Use GitHub `$/` references and normalize only safe YAML `uses` scalar positions in memory for actionlint 1.7.12; zizmor reads originals. Preserve the exact NGINX producer snapshot across `env -i` and retain target/cache checks.

## Changed files

- `.github/workflows/all-connectors-no-crs.yml`
- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/test-nginx-exact-head.yml`
- `.github/workflows/test-nginx.yml`
- `Makefile`
- `ci/tools/lint_workflows.py`
- `ci/tools/update-workflow-tools.py`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_lint_workflows.py`
- `tests/test_nginx_exact_head_gate_contract.py`
- `tests/test_nginx_exact_head_runtime_handoff.py`
- `docs/security/ci-security-tooling.md`
- `docs/security/ci-security-tooling.de.md`
- This Change Record and its German companion.

## Commands executed

All local commands used RTK. From the external Parent worktree:

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr-411-repair make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract`: 274 tests passed, 6 skipped for unavailable namespace/ownership capabilities; locked tool-record validation passed.
- Updater unit class: 45 tests passed; original suite reproduced 3 failures and 1 error. Copied-tree validation also exposed fixture dependence and missing copied NGINX inputs; both were corrected.
- `tests.ci_security.test_update_workflow_tools.WorkflowToolUpdaterIntegrationTests`: final copied-tree integration passed (1 test, 138.941 seconds), including the real native contract under a synthetic future checkout pin.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/pr-411-repair TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr-411-repair /root/git/ModSecurity-conector/.venv/bin/python ci/tools/update-workflow-tools.py validate --root . --candidate /var/tmp/codex/ModSecurity-conector/runs/pr-411-repair/current-lock-candidate.json --validate-proposed-tree`: passed the real private-tree contract and downloaded-tool lint/fixture checks without changing the checkout.
- `tests.test_lint_workflows`: 4 tests passed, including block-scalar preservation, path rejection, and propagated failures.
- `tests.test_nginx_exact_head_gate_contract`, `tests.test_nginx_exact_head_runtime_handoff`, and `tests.test_runtime_env_snapshot_contract`: 31 tests passed using the clean exact-gitlink Framework.
- Locked actionlint through `ci/tools/lint_workflows.py`: all workflows and permission fixtures passed. Locked zizmor offline: original tree reproduced exit `12`; corrected tree passed. Both unsafe fixtures returned `14`; both safe fixtures returned `0`.
- `make check-bilingual-docs` and `make check-doc-links`, RTK-wrapped with explicit Parent Python/Framework paths: passed after local exact-gitlink Framework materialization. Initial absent-submodule link errors were environment setup failures, not changed-document errors.
- `rtk proxy git diff --check`: passed. Independent read-only review found an initial regex/script-normalization issue; token-based correction and regression passed.

## Security impact

SHA pins, official upstream identities, checksum verification, permission allowlists, and untrusted-PR isolation remain enforced. Candidate lint now rejects checksum, launch, timeout, finding, and unexpected negative-fixture exits. No suppression or severity threshold was added. Scripts/comments are preserved during actionlint normalization; zizmor audits original source. No secrets, dependencies, global services, or Framework/MRTS sources were changed.

## Runtime evidence

The executable handoff regression reproduced an unexpected second preparation (exit `93`) before the fix and passed afterward. It executes the actual workflow shell and cache wrapper with only the expensive build boundary replaced. It verifies prepared paths, removed ambient environment, failed provisioning, and rejected target/cache metadata. This is handoff evidence; real hosted NGINX execution belongs to post-push CI.

## Known limitations

The existing local Parent interpreter is Python `3.14.4`; CI pins `3.14.7`. Local checks establish compatibility within the same minor version, not execution on the exact CI patch. Actionlint requires the documented syntax adapter until upstream supports `$/`.

## Remaining risks

Future tool releases may introduce new rules or failures; the proposed-tree lint now rejects such candidates before publication instead of assuming checksum validity implies compatibility. Actual host runtime and exact CI toolchain results require the current PR-head workflows.

## Checks not run and rationale

Full hosted NGINX and current-head GitHub/SonarQube checks were not run locally; GitHub runs them after the authorized push. No unrelated connector rebuilds, broad security scans, package installations, or merge were performed. Ruff is unavailable in the existing environment and was not installed.

## Final diff and review status

Scoped source, tests, EN/DE guide and this pair reviewed. Original Parent master and nested repositories preserved. Delivery target is existing PR #411 branch `automation/update-modsecurity-conector-workflow-tools`; push and current-head CI readback follow local verification. No merge or master update is authorized.
