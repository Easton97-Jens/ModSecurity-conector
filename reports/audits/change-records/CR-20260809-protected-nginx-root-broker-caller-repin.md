# Change Record

**Language:** English | [Deutsch](CR-20260809-protected-nginx-root-broker-caller-repin.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260809-protected-nginx-root-broker-caller-repin |
| Date (UTC) | 2026-08-09 |
| Base revision | c2836f74510b9f72bae466d8b7d92a3f9f38c007 |

## Motivation and problem statement

The protected caller must select the repaired reusable NGINX root broker through
the immutable resulting protected-master merge commit, rather than the former
broker commit. The separate repin is necessary because a squash merge makes
the Phase-A result unavailable while the broker repair is reviewed.

The resulting broker revision is
c2836f74510b9f72bae466d8b7d92a3f9f38c007. Its exact Parent tree records
Framework gitlink 4c9af1cee72caa0107fa011e59eef9e853338cf5 with mode 160000.
The former e06254ea9622d214a9030b9ba786756560ace417 and
c71e15db7b7517b237add9fa09b3493e7bc93627 values remain historical evidence
for failed run 31310183097 and are not executable caller policy pins.

## Acceptance criteria

Both protected caller jobs use the same literal immutable broker SHA in their
reusable-workflow reference and protected_broker_sha input. Both use the
Framework gitlink recorded by that broker commit. The manifest helper,
evidence readback, Python workflow contract, workflow-security tests, broker
tests, and paired security documentation carry the same canonical tuple.

The caller remains master-only, dispatch-only, read-only, unprivileged, and
data-only. This repin changes neither broker logic, permissions, root actions,
manifest schema, profile rules, Framework source, MRTS source, nor a Gitlink.

## Implementation decision and rationale

The revision is a separate Parent-only caller PR. The reusable broker revision
is protected-master reachable, and its Framework revision is derived from its
exact Git tree instead of copied from the old pin. Constants and regression
fixtures are updated together so a mixed broker, manifest, evidence, or
Framework tuple fails the existing contract rather than selecting a moving ref.
The constrained workflow-tool publisher receives the caller as one exact
reviewed path in both its source allowlist and matching staging list; this
restores complete centrally locked Action-pin coverage without a broad prefix.

No branch, tag, master reference, local reusable path, caller-selected broker
source, OIDC permission, write permission, secret, or root execution path is
introduced.

## Changed files

- .github/workflows/run-protected-nginx-root-broker.yml
- .github/workflows/update-workflow-tools.yml
- ci/tools/update-workflow-tools.py
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py and tests/test_nginx_root_broker.py
- docs/security/trusted-nginx-root-broker.md and its German companion
- this Change Record and its German companion

## Commands executed

The exact Phase-B base, broker SHA, and Framework gitlink were checked from
the resulting protected-master tree. Before the later `origin/master` sync,
the following source/static validations were observed with the available
Parent virtual-environment Python `3.14.4`:

- `PYTHONDONTWRITEBYTECODE=1 <Parent .venv>/bin/python -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_protected_nginx_broker_caller tests.test_ci_security_workflows tests.test_python_version_contract tests.ci_security.test_update_workflow_tools tests.security_regression.test_workflow_security_contract` — PASS, 133 tests.
- `make PYTHON=<Parent .venv>/bin/python check-ci-security-contract` — PASS,
  26 tests plus read-only actionlint, zizmor, and gitleaks lock validation.
- `actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml` — PASS.
- `zizmor --offline .github/workflows` — PASS, no findings.
- `git diff --check c2836f74510b9f72bae466d8b7d92a3f9f38c007` — PASS.

The original finite-allowlist reproduction failed before the two-path repair,
then the focused updater/security-contract suite passed with the legitimate
unallowlisted-workflow negative control. The final Phase-B range, validation,
and security-diff review must be rerun after the normal `origin/master` sync.
No runtime lifecycle result is claimed here.

## Security impact

The immutable caller-to-broker binding remains fail closed. Declarative caller
inputs and manifests must agree with the pinned broker and Framework tuple
before the reusable broker can admit artifacts or reach existing privileged
actions. The update does not broaden the trusted source set or allow caller or
PR code to execute as root.

## Runtime evidence

No post-repin protected-master lifecycle has been observed. Once this separate
caller PR is normally merged, a manual protected-master dispatch must prove
both no-crs and with-crs profiles, broker binding, root and worker identity,
CRS and audit evidence where applicable, evidence readback, stop, and cleanup.
That resulting-master evidence is required before PR #240 resumes.

## Known limitations

This record is not a substitute for GitHub-hosted checks, SonarQube Cloud, or
the privileged runtime. Local source and contract validation cannot prove
GitHub reusable-workflow context, artifact transport, runner sudo behavior, or
the full NGINX and CRS lifecycle. The available Python `3.14.4` is a
repository-permitted source/static fallback rather than the configured
CPython `3.14.6` CI baseline.

## Remaining risks

A Phase-B quality, security, review, or branch-protection failure blocks the
caller PR. A resulting-master lifecycle or evidence-readback failure blocks
FND-PARENT-0113 verification and PR #240 continuation. Neither outcome
authorizes a mutable reference, direct master edit, bypass, or synthetic PASS.

## Checks not run and rationale

`make check-python-version-contract` is blocked by unchanged current-master
workflow inventory/shape violations in `verified-report-governance.yml`,
`test-apache.yml`, `test-haproxy.yml`, and `update-workflow-tools.yml`; it
reports no caller-repin-specific violation. The repository-wide bilingual
checker and broad 897-test unit discovery are blocked by the intentionally
uninitialized Framework submodule in this task worktree; the Framework policy
prohibits automatic initialization. The post-merge lifecycle is intentionally
unavailable until the separate caller repin passes current-head gates and is
normally merged. Hosted checks, CodeQL, SonarQube Cloud, review, and
branch-protection results must be freshly observed for the eventual PR head.

## Final diff and review status

This is an uncommitted local Phase-B candidate based on protected-master
revision c2836f74510b9f72bae466d8b7d92a3f9f38c007. A newer `origin/master`
was discovered during review and must be integrated normally before delivery;
the record's final base, range, and validation results will then be
reconciled. It makes no claim that a push, pull request, merge, hosted check,
or lifecycle has completed. The final range must contain only Parent-owned
caller, contract, test, documentation, and record changes; it must contain no
Framework or MRTS source or Gitlink change.
