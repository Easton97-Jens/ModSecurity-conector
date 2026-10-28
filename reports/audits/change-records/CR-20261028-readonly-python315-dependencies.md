# Change Record: CR-20261028-readonly-python315-dependencies

**Language:** English | [Deutsch](CR-20261028-readonly-python315-dependencies.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-readonly-python315-dependencies |
| Date (UTC) | 2026-10-28 |
| Base revision | `d50877a697c8eae3e18f2226d0b6532622ecdcd0` |

## Motivation and problem statement

Updater run `40648924250`, job `122684319837`, passes the previous NGINX handoff repair but fails installing `PyYAML==6.0.3` in the private namespace: no matching CPython-3.15 binary wheel exists. The missed namespace path still used the legacy binary-only lock instead of the already reviewed Parent source installer. The requested outcome is to repair this failure while preserving source protection and candidate privilege separation.

## Acceptance criteria

Prepare only the reviewed PyYAML dependency before runtime protection; validate the candidate Framework lock only as data. Keep the original selected Python and isolated import inside the jail. Stop before Make when dependency preparation/import fails. Preserve all source, namespace, output, permission and publication controls, and the exact automatic selection of 100 cases / 80 executions. New head-bound hosted validation remains required.

## Implementation decision and rationale

The ordinary runner invokes the unchanged trusted Parent `ci/tools/install-ci-dependencies.py --ci-toolcache --framework-lock modules/ModSecurity-test-Framework/requirements-ci.lock` after candidate data checks and before private guard/sandbox creation, then runs `python3 -m pip check`. Only the selected setup-python runtime receives the reviewed pure-Python wheel. It is subsequently mounted read-only. No candidate Framework code executes during preparation.

The namespace replaces its obsolete binary-only pip call with `"$PYTHON" -I -c "import yaml; assert not yaml.__with_libyaml__"`, then retains the original Make invocation and interpreter. `-I` ignores candidate `PYTHONPATH`. No installer API, dependency version, source/build-tool lock, job permission or ref allowlist changes.

A private-venv prototype was rejected: Python 3.15 copies activation-template mode bits, including group-write permissions, which the existing output guard correctly rejects. Preparing the dependency outside the validator output tree avoids adding either target or builder venvs there and preserves that guard.

## Changed files

- `.github/workflows/update-submodules.yml`: reviewed dependency preparation and pip check before protection.
- `ci/tools/run-readonly-submodule-validation-namespace.py`: isolated prepared-dependency preflight, no in-jail install.
- `tests/test_ci_security_workflows.py`, `tests/test_run_readonly_submodule_validation_namespace.py`: ordering, arguments, isolation, failure propagation and unchanged-interpreter regressions. One new method is on demand only.
- `config/testing/active-cases.json`: six explicitly reviewed source SHA256 slots; complete standard/archived execution arrays unchanged (100/80 and 1893/839).
- `reports/testing/test-selection-archive.generated.json`: regenerated through its native generator; one additional retained on-demand method.
- `docs/build/README.md`, `docs/build/README.de.md`, `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`: equivalent current behavior and trust-boundary documentation.
- This English/German Change Record pair.

## Commands executed

Every project shell payload was wrapped with task-local, checksum-verified RTK `v1.0.1`.

| Check | Observed result |
| --- | --- |
| Reviewed installer in a task-owned Python 3.15.1 venv, with `--build-root /workspace/scratch/5e0fa1c15f63/task-state/pyyaml315-host-validation/build --framework-lock modules/ModSecurity-test-Framework/requirements-ci.lock` | Exit 0; actual pinned source build/install, PyYAML 6.0.3, `libyaml_extension: false`. |
| Same interpreter, `-m pip check` | Exit 0, no broken requirements. |
| Seven explicit affected unittest selectors on Python 3.15.1 with `ON_DEMAND_TESTS=1` | Exit 0, 7 passed; candidate-program/preflight/workflow tests plus corrupt-source, corrupt-builder, Framework-version and native-wheel rejection controls. |
| Three final candidate/preflight/workflow regressions on Python 3.12.14 | Exit 0, 3 passed. Original helper loaded in memory fails both new preflight scenarios at the intended boundary. |
| Actual prepared Python 3.15.1/PyYAML 6.0.3 through the candidate shell tail, with Make replaced only at its external boundary | Exit 0; isolated import succeeds, original interpreter reaches Make, no dependency files added to external output. |
| Full source/inventory admission, exact selection comparison, archive generator and `--check`, project-version check | Passed; standard and archived execution arrays unchanged. |
| Local `make quick-check` using Python 3.15.1 and the candidate output-path environment | Blocked at `common.memory-lifetime`: LeakSanitizer cannot inspect `/proc/.../task` in this environment; no sanitizer disabled. Earlier local attempts lacked required output directories; the configured attempt passed those prerequisites. |
| `python3 ci/checks/common/check-python-version-contract.py` | Exit 1: five existing violations; an in-memory comparison using the unmodified master workflow returns exactly the same five violations. This patch adds none. |
| Documentation and final whitespace checks | Passed: bilingual documentation, documentation links, Change Record structure and final whitespace checks. |

Source SHA256: `d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f`; locally built wheel SHA256: `4806af48a4cec5305abb1d0f44a64c0351aa22ed9a941dd3c89979bde5b73dc9`. The separate Python 3.15.1 test runtime came from `astral-sh/python-build-standalone` release `20261021`, verified SHA256 `01d901e09ca673c99a6c9bd9ec2cfbd58dbe8813d07514c36cb73cfd20b18bd8`; it does not replace repository pins or a hosted runtime.

## Security impact

Dependency execution remains limited to the previously reviewed, hash-pinned Parent source/build-tool exception, under the ordinary runner with the installer's credential-stripped backend environment. Candidate Framework input is passive lock data only. Candidate code still runs only after UID/GID drop in the existing private jail. Runtime/source mounts, write probes, output permission/link checks, sanitizer checks, CI permissions, ref gates and publishing separation remain unchanged.

## Runtime evidence

The local build/import proofs establish dependency bootstrap behavior on exact Python 3.15.1. They do not establish full privileged namespace execution, a hosted updater success, connector runtime qualification or I12 acceptance. No such claim is made.

## Known limitations

The local environment cannot complete the sanitizer-backed quick check or the privileged hosted namespace. Updater dispatch is intentionally restricted to master or its existing reviewed validation ref; this patch does not widen the allowlist to run a task branch. Hosted validation must be read back after normal integration. The first fully sanitized local network probe could not resolve the artifact host; the documented host-side installer subsequently completed using the normal host environment.

## Remaining risks

Current master also has five unchanged Python-workflow-contract violations: one trusted lighttpd profile, two protected NGINX reusable references and two unlisted native Sonar jobs. They are recorded as baseline, not silently accepted or repaired in this dependency-only change. Fresh PR CI/Sonar may expose other existing failures. No passing overall gate is claimed.

## Checks not run and rationale

Full updater publication, new hosted read-only namespace validation, connector runtime/matrix and fresh Sonar analysis are not local execution evidence. The complete local quick check is environment-blocked as above; no rule, sanitizer, test or gate was bypassed. Historical I12 work remains outside scope.

## Final diff and review status

An independent read-only review found no material blocker in the final workflow/helper/tests. Final integrated delivery and head-bound hosted checks are pending. This record claims no merge, master change, new updater success or `verified_pr` status.
