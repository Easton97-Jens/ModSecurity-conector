# Change Record

**Language:** English | [Deutsch](CR-20260808-trusted-nginx-root-broker.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260808-trusted-nginx-root-broker |
| Date (UTC) | 2026-08-08 |
| Base revision | cd1328e25bb2d9e6769461c61c6e7012a2c49d07 |

## Motivation and problem statement

The existing NGINX smoke harness requires a root master and a distinct
non-root worker. Elevating Parent or Framework code from PR #240 would execute
branch-owned shell, generated data, binaries, modules, or libraries as root.
The user therefore authorized a separate protected-master broker PR before PR
#240 may consume an exact merge SHA.

## Acceptance criteria

The broker must run only protected-master code as root; accept only a bounded
declarative manifest and fixed actions; build or attest the NGINX/module
artifacts from the protected source; verify SHA, paths, owner, modes,
master/worker identity, loopback listener, evidence, and cleanup; and carry
paired EN/DE documentation and tests. It must not include PR #240 pinning,
CRS separation, Framework, or MRTS changes.

## Implementation decision and rationale

A SHA-bound reusable workflow checks out the exact protected broker revision,
verifies protected-master ancestry and a matching Framework gitlink, builds
artifacts without root, and passes only a six-field caller manifest to the
broker. The Python helper copies/re-hashes artifacts into a root-owned exact
layout and implements the closed action list. Root-generated configuration and
rules prevent caller configuration execution. The root-to-runner projection is
allowlisted and descriptor-relative. The broker records a root-broker-only
result, deliberately not a CRS result. Its privileged parent is the fixed
root-owned `/var/lib/msconnector-nginx-root-broker` state location; no caller
or broker CLI input can select the parent, staging root, or runtime snapshot
path used across the privilege boundary.

## Changed files

- `.github/workflows/nginx-root-broker.yml`
- `ci/runtime/broker/nginx_root_broker.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_ci_security_workflows.py`
- `docs/security/trusted-nginx-root-broker.md` and `.de.md`
- `docs/README.md` and `docs/README.de.md`
- this Change Record and its German companion

## Commands executed

Python compilation, the focused broker/workflow/CI-security suite (`39` tests),
`make check-ci-security-contract`, `make check-bilingual-docs`,
`make check-doc-links`, `git diff --check`, actionlint with ShellCheck, and
zizmor offline completed successfully. `make lint` completed successfully; its
optional NGINX C17 compile check was explicitly blocked/skipped because this
local environment has no NGINX headers/source. The final security-diff scan
completed with no reportable finding and a valid sealed artifact. Hosted checks,
SonarQube Cloud, review/branch-protection gates, and the protected-master root
invocation remain pending delivery evidence.

## Security impact

The change creates a narrow privileged boundary rather than elevating PR code.
The caller cannot provide a root command, shell fragment, configuration path,
or executable path. Root execution is limited to the exact protected helper,
the exact root-copied NGINX binary, and fixed actions. Cleanup is
descriptor-relative and cannot recursively follow caller-controlled paths. A
fault-injected failed `chown` also removes a newly created fixed root parent or
run root, rather than leaving privileged stale state behind.

## Runtime evidence

No protected-master hosted root invocation has been observed yet. Local static
tests do not prove GitHub reusable-workflow context semantics, a real NGINX
root master, worker identity, listener release, or artifact upload. Those are
required post-push evidence, not present results.

## Known limitations

The broker performs a fixed static ModSecurity allow/block smoke. Its
`matrix_variant` is an attribution binding only; it does not claim CRS
materialization or CRS behavior. Fresh CRS source validation remains a
separate PR #240 responsibility.

## Remaining risks

The exact SHA/blob and protected-master checks require hosted confirmation on
GitHub Actions. A pending environment-specific dependency, workflow-context,
or NGINX runtime failure blocks broker delivery rather than authorizing a
fallback to PR-branch root execution.

## Checks not run and rationale

Hosted CI, SonarQube Cloud, review/branch-protection gates, and the
protected-master root invocation remain pending the first normal publication
of the broker branch. They remain required before any merge. The local
security-diff scan is complete; its report is local evidence and does not
replace the required hosted root-lifecycle validation.

## Final diff and review status

Status at the local-validation capture: local validation is complete. At that
capture, no Parent PR #240 change, Framework change, MRTS change, push, Draft
PR, or merge had occurred for this broker record. Subsequent delivery facts
must be recorded only after they are observed.
