# Change Record

**Language:** English | [Deutsch](CR-20260822-nginx-framework-updater-decoupling.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260822-nginx-framework-updater-decoupling |
| Date (UTC) | 2026-08-22 |
| Base revision | `c8881eaadf7d3ef5d4173d581a62726a2df3fdf2` |
| Delivery status | Prepared on a dedicated Draft pull request; no merge is asserted. |

## Motivation and problem statement

Framework-update run `32557767129` validated and attempted to publish an NGINX
`release-1.31.4` tuple from Framework commit
`52fe6ee334f1381c35d5c3b7140433c626469523`. The push failed because the
generic publisher was trying to modify `.github/workflows/nginx-root-broker.yml`.
A later upstream provenance check established that `1.31.4` was not an official
NGINX release on 2026-08-22; the latest published mainline release remained
`1.31.3`, which the protected Parent broker already used.

## Acceptance criteria

The generic Framework synchronizer must ignore every `NGINX_*` assignment,
must contain no NGINX Parent projection or workflow target, and must leave all
NGINX-owned Parent files byte-identical when only Framework NGINX data changes.
The dedicated protected NGINX root broker must remain present and pinned to
the currently reviewed `1.31.3` release tuple.

## Implementation decision and rationale

Remove NGINX source fields, semantic validation, derived values, and Parent
targets from the general Framework-to-Parent synchronizer. Add import-time
ownership guards and regression tests that prevent an NGINX field or target
from being reintroduced. This eliminates the workflow-write failure without
granting the general submodule publisher permission to alter workflow files.
The root broker is retained because it is the privileged and independently
reviewed execution boundary.

## Changed files

- `ci/tools/sync-framework-component-versions.py`: removes generic NGINX
  ingestion and projection, documents the ownership boundary, and adds static
  registry guards.
- `tests/test_update_framework_versions.py`: proves hostile or future Framework
  NGINX data is unconsumed and cannot change NGINX-owned Parent files.
- This paired Change Record and archive entries record authorization and
  validation evidence.

## Commands executed

- `python3 -m py_compile ci/tools/sync-framework-component-versions.py tests/test_update_framework_versions.py`
- `python3 -m unittest -v tests.test_update_framework_versions tests.test_update_submodules_local_git tests.test_ci_security_workflows`
- `make PYTHON="$(command -v python3)" check-ci-security-contract`
- `make PYTHON="$(command -v python3)" check-bilingual-docs`
- `git diff --check`

## Runtime evidence

The bounded bootstrap runs the focused synchronizer, local-git updater, and
CI-security suites on the exact branch head before constructing the final
single commit. Hosted pull-request checks remain authoritative after the
temporary bootstrap workflow removes itself.

## Known limitations

This change does not invent or publish an unreleased NGINX version and does not
automatically merge future NGINX updates. A future official NGINX release still
requires its own reviewed NGINX change and protected broker validation.

## Security impact

The generic submodule publisher loses all ability to derive or write NGINX
pins, including workflow files. No broader token scope, mutable reusable
workflow reference, auto-merge, or PR-controlled root execution is introduced.
The immutable protected root-broker boundary remains intact.

## Remaining risks

A future NGINX-specific updater must independently verify an official release
tag, exact release asset, and SHA-256 before proposing a broker repin. The
Framework repository can continue to contain NGINX metadata, but it is treated
as unconsumed data by this Parent updater.

## Checks not run and rationale

Merge, protected-master execution, and post-merge NGINX lifecycle evidence
cannot be claimed before reviewed integration. These remain branch-protection
and protected-workflow gates.

## Final diff and review status

The replacement pull request remains Draft. The final branch is rewritten to
one commit directly on the stated base revision, contains no temporary
bootstrap workflow, and does not change the existing NGINX `1.31.3` pins.
