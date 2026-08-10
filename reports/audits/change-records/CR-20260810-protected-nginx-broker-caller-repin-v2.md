# Change Record

**Language:** English | [Deutsch](CR-20260810-protected-nginx-broker-caller-repin-v2.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260810-protected-nginx-broker-caller-repin-v2 |
| Date (UTC) | 2026-08-10 |
| Base revision | 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2 |
| Protected broker SHA | 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2 |
| Broker Framework gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation and problem statement

The protected caller still selected the predecessor immutable broker/Framework tuple. That tuple cannot exercise the later broker runtime-snapshot repair already merged as 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2. The caller must bind both reusable jobs, their input tuple, its manifest/evidence helper, and static contracts to the exact broker commit and the exact mode-160000 Framework gitlink recorded by that broker tree.

## Acceptance criteria

Both fixed caller jobs use the same full immutable broker SHA, pass it as protected_broker_sha, and pass Framework SHA 03880bf66b3905940466ff10b3a431a27ecc6b26. The caller retains its dispatch-only, canonical-repository, non-fork, refs/heads/master, contents: read contract. It must not add a mutable reference, third profile, secret inheritance, write permission, target checkout/execution, root command, Framework/MRTS source change, or Parent gitlink update.

The immutable broker must accept the committed Phase-C caller blob for this tuple and reject a deliberately wrong tuple before artifact, build, candidate, or root activity. The paired security documentation and this Change Record must preserve the same active literals in English and German; older records retain their historical tuple.

## Technical decisions

The repin is a data-only Parent caller change. The new broker SHA is not a branch or tag and cannot be selected by caller input. Framework SHA comes from the broker tree's own gitlink rather than a later Parent state. The two profile calls remain explicit and symmetric, so no matrix, profile, path, or command becomes caller-selectable.

## Implementation decision and rationale

The two uses values, both protected_broker_sha inputs, both framework_sha inputs, and lifecycle result labels now name the new tuple. protected_nginx_broker_caller.py, the Python workflow-version contract, and caller/blob contract tests use that identical pair. No parser, schema, root action, permission, trigger, artifact-path, or cleanup behavior changes.

The trusted-broker English/German guide now describes the protected snapshot contract as active through this broker revision. The Phase-B record and older caller-repin records are historical evidence and are intentionally not rewritten.

## Changed files

- .github/workflows/run-protected-nginx-root-broker.yml
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py
- tests/test_nginx_root_broker.py
- docs/security/trusted-nginx-root-broker.md and docs/security/trusted-nginx-root-broker.de.md
- this Change Record and CR-20260810-protected-nginx-broker-caller-repin-v2.de.md

## Tests and actual results

The focused Parent caller/broker/security/snapshot/Python-contract suite passed 120 tests after the exact pinned Framework gitlink was materialized non-recursively in the task-owned validation worktree. The initial run had one environment-only failure because that worktree intentionally lacked modules/ModSecurity-test-Framework/ci/lib/common.sh; the targeted test and full rerun passed after checkout of exactly 03880bf66b3905940466ff10b3a431a27ecc6b26. Nested MRTS remained uninitialized and unchanged.

## Commands executed

- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> <Parent .venv>/bin/python -m unittest -v tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_nginx_root_broker_crs_profile tests.test_ci_security_workflows tests.test_runtime_env_snapshot_contract tests.test_python_version_contract — PASS, 120 tests after exact Framework materialization; the prior attempt is recorded above as environment-only.
- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> <Parent .venv>/bin/python -m py_compile ci/runtime/broker/protected_nginx_broker_caller.py ci/checks/common/check-python-version-contract.py tests/test_ci_security_workflows.py tests/test_nginx_root_broker.py — PASS.
- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> make PYTHON=<Parent .venv>/bin/python check-ci-security-contract — PASS, 26 workflow-security tests plus read-only tool-lock validation.
- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> make PYTHON=<Parent .venv>/bin/python check-python-version-contract — BLOCKED, exit 2 on existing unmodified workflow-inventory failures. Its output names no violation for run-protected-nginx-root-broker.yml; this repin does not mask or repair that separate baseline.
- actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml — PASS with actionlint 1.7.12 and ShellCheck 0.11.0.
- zizmor --offline .github/workflows — PASS, no findings; 94 existing suppressions reported.
- make PYTHON=<Parent .venv>/bin/python check-bilingual-docs — PASS.
- make PYTHON=<Parent .venv>/bin/python check-doc-links — PASS.
- git diff --check — PASS.

## Security impact

The affected boundary is declaration of the immutable privileged reusable workflow. Caller-controlled dispatch data remains declarative and the caller does not gain authority to select broker source, Framework source, root action, manifest path, executable, profile, permission, or secret. Existing negative contracts continue to reject mutable/local references, wrong or mixed tuple values, duplicate YAML/input values, weakened master gates, PR/fork contexts, write permissions, secrets, sudo, target execution, unsafe artifacts, and failed-result masking.

## Runtime evidence

No resulting-master protected lifecycle has run for this candidate. The prior Phase-C attempt 31328046595 remains a fail-closed pre-root failure and is not evidence for the repaired broker. A new master-only dispatch must separately prove both no-CRS and OWASP-CRS profiles, identity bindings, root-master and non-root-worker behavior, CRS/audit evidence, evidence readback, stop, and cleanup after this caller-repin PR is normally merged.

## Known limitations

The local Parent virtual environment provides CPython 3.14.4 while .python-version requires CPython 3.14.6. Local results are therefore source/static evidence, not CI-equivalent interpreter evidence. The exact Framework submodule was materialized only to run a Parent contract test; no Framework or MRTS source, branch, Gitlink, commit, push, or PR was changed.

## Remaining risks

Any PR-specific review, branch-protection, CodeQL, SonarQube Cloud, or resulting-master lifecycle failure blocks delivery. This record does not authorize a mutable ref, direct master push, history rewrite, check bypass, automatic merge, Framework/MRTS modification, Phase-D dispatch, FND-PARENT-0113 closure, or PR #240 continuation.

## Checks not run and rationale

The resulting-master lifecycle, root admission, NGINX start, worker proof, CRS network fetch, audit evidence, artifact transport, evidence readback, and cleanup are not local checks. They require the later protected GitHub-hosted workflow after exact-head PR verification and master integration. Hosted GitHub Actions, CodeQL, SonarQube Cloud, review, and branch-protection evidence remain unverified for the final PR head.

## Final review status

This record captures pre-commit local validation and the initial normal publication. Draft Parent PR [#270](https://github.com/Easton97-Jens/ModSecurity-conector/pull/270) was opened from `fix/ci-repin-nginx-broker-runtime-snapshot` to `master` at initial head `5e290bb228a47331a53038da258970b6d792ed2f`; it is not ready for review and has no auto-merge request. Committed-blob validation passed; hosted exact-head, review, branch-protection, merge, and lifecycle evidence remain delivery gates. No success claim is made for them.

## Final diff and review status

This record's diff is limited to the nine Parent paths above. It preserves the existing Parent Framework gitlink at 03880bf66b3905940466ff10b3a431a27ecc6b26 and makes no MRTS change. Historical predecessor-tuple references remain only in older Change Records as historical evidence.
