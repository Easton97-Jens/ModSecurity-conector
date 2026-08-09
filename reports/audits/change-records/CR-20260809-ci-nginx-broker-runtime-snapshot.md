# Change Record

**Language:** English | [Deutsch](CR-20260809-ci-nginx-broker-runtime-snapshot.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260809-ci-nginx-broker-runtime-snapshot |
| Date (UTC) | 2026-08-09 |
| Base revision | ef88a616498e0a2893cd3da54003dd7cdea57015 |
| Framework gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation and problem statement

Protected lifecycle run 31328046595 correctly stopped before candidate creation and
before every root action because its no-CRS job could not find the required
NGINX_BINARY and NGINX_MODULE exports in the invocation-local runtime snapshot.
The broker also requires MODSECURITY_SHARED_PREFIX.

The generic producer could publish effective runtime values influenced by
environment or MRTS compatibility inputs. That is not an acceptable source for
the privileged broker. The repair therefore gives only the protected broker
workflow a narrow, independently validated producer-to-consumer contract.

## Acceptance criteria

The protected workflow selects a fixed snapshot contract before dependency
preparation. Its one invocation-local snapshot contains exactly one non-empty
assignment each for NGINX_BINARY, NGINX_MODULE, and MODSECURITY_SHARED_PREFIX,
with no additional exports.

Those values match a private, canonical provenance record derived from the
completed NGINX plan rather than caller environment, PATH, a system binary,
MRTS compatibility overrides, or an unverified cache entry. The broker fails
closed for missing, empty, duplicate, malformed, mismatched, replaced,
outside-root, symlinked, wrong-owner, writable, or digest-mismatched inputs
before it creates a candidate. No-CRS requires no CRS bundle; with-CRS adds
only the protected bundle while retaining the same NGINX artifact digests in
separate private staging roots.

## Technical decisions

The contract is deliberately restricted to the protected workflow, preserving
the compatibility surface of generic snapshots while making the broker input
independently reproducible and rejectable.

## Implementation decision and rationale

nginx-root-broker.yml selects RUNTIME_COMPONENT_SNAPSHOT_CONTRACT=protected-nginx-broker
before make fetch-deps. In this mode the existing canonical serializer and
atomic-publication path write a mode-0600 fixed record at
build/runtime-component-reports/trusted-nginx-broker-provenance.json before
they write the restricted existing invocation-local snapshot.

The record has a fixed schema and canonical compact-SHA-256 identity. It binds
the Parent broker source revision, Framework gitlink, completed NGINX plan,
release tuple, canonical NGINX binary/module paths, ModSecurity library path,
and artifact metadata and digests. The producer derives the two NGINX paths
from the canonical plan layout, not from effective environment values.

The broker reads both record and snapshot without sourcing either file. It
requires exact record identity, private regular-file metadata, canonical roots,
and equality of the three snapshot values, then derives candidate inputs only
from the revalidated record. Generic runtime snapshots retain their existing
compatibility behavior.

The sole Gitlink update sets modules/ModSecurity-test-Framework to
03880bf66b3905940466ff10b3a431a27ecc6b26 with mode 160000. No Framework
source, MRTS source, MRTS Gitlink, MRTS remote, caller pin, or root action is
changed by this Phase-B candidate.

## Changed files

- .github/workflows/nginx-root-broker.yml
- ci/provisioning/components/prepare-runtime-components.py
- ci/provisioning/components/prepare-runtime-components.sh
- ci/runtime/broker/nginx_root_broker.py
- modules/ModSecurity-test-Framework
- tests/test_runtime_env_snapshot_contract.py
- tests/test_nginx_root_broker.py
- tests/test_nginx_root_broker_crs_profile.py
- tests/test_nginx_root_broker_workflow.py
- tests/test_ci_security_workflows.py
- docs/security/trusted-nginx-root-broker.md and its German companion
- this Change Record and its German companion

## Tests and actual results

Focused producer, consumer, workflow, profile, documentation, and static
checks cover the protected contract; the observed commands and outcomes follow.

## Commands executed

The following replay-safe command forms were observed in the isolated Phase-B
worktree. TMPDIR was an existing task-owned external directory; no test wrote
to the source tree.

- PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned TMPDIR> python3 -m unittest -v tests.test_runtime_env_snapshot_contract tests.test_runtime_producer_readiness_path_policy tests.test_nginx_root_broker tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker_workflow tests.test_nginx_root_broker_crs_profile tests.test_ci_security_workflows — PASS, 100 tests.
- make PYTHON=<Parent .venv>/bin/python check-runtime-producer-readiness — BLOCKED, exit 77: the isolated worktree intentionally has no prepared NGINX binary/module or archive cache. Running make prepare-runtime-components would add an unrelated networked runtime build; the hermetic producer-readiness tests above are the applicable local control.
- make PYTHON=<Parent .venv>/bin/python check-ci-security-contract — PASS, 26 workflow-security tests plus read-only actionlint, zizmor, and gitleaks lock validation.
- python3 -m py_compile ci/provisioning/components/prepare-runtime-components.py ci/runtime/broker/nginx_root_broker.py tests/test_runtime_env_snapshot_contract.py tests/test_nginx_root_broker.py tests/test_nginx_root_broker_crs_profile.py — PASS.
- sh -n ci/provisioning/components/prepare-runtime-components.sh — PASS.
- shellcheck --shell=sh --severity=error ci/provisioning/components/prepare-runtime-components.sh — PASS. A full informational run reports only existing SC1007, SC1091, and SC2034 diagnostics; none is introduced by this diff.
- actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml — PASS.
- zizmor --offline .github/workflows — PASS, no findings.
- make check-bilingual-docs and make check-doc-links — PASS.
- git diff --check HEAD — PASS.

The optional cache/identity/producer suite had one error in
test_nginx_discards_marker_owned_partial_root_before_build: its fixture lacks
common/src/header_validation_internal.h. The identical test fails on clean
Parent master and is already tracked as FND-PARENT-0077; it was neither
suppressed nor changed by this repair.

## Security impact

The repair closes the demonstrated producer/consumer contract gap without
loosening the broker. Snapshot text remains declarative and cannot select a
candidate artifact. A snapshot-only replacement, a caller override, a system
or MRTS path, and a mismatched provenance record fail before candidate staging
or any privileged operation. The existing fixed root-action allowlist remains
unchanged.

## Runtime evidence

No new protected-master lifecycle has run for this local candidate. The prior
run 31328046595 is retained as the failure reproduction: both profile jobs
stopped before candidate admission, sudo, NGINX start, evidence projection, and
cleanup. A fresh hosted lifecycle is required only after this separate Parent
broker PR has passed its exact-head gates and is normally merged.

## Known limitations

The available local Python is CPython 3.14.4; .python-version requires CPython
3.14.6. The local result is therefore source/static validation, not
CI-equivalent interpreter evidence. Local tests do not prove GitHub Actions
context enforcement, actual runner sudo, full NGINX execution, CRS network
fetching, audit evidence, artifact transport, or cleanup behavior.

## Remaining risks

Any Parent broker PR failure, review finding, branch-protection failure,
CodeQL/SonarQube Cloud finding, or resulting-master lifecycle failure blocks
Phase C and PR #240 continuation. This record does not authorize mutable refs,
direct master changes, a bypass, a system fallback, a root shell, or a
synthetic runtime PASS.

## Checks not run and rationale

The protected no-CRS/with-CRS runtime, root admission, worker verification,
CRS/audit proof, evidence readback, and cleanup are deliberately not run
locally: they require the resulting protected Parent master workflow and
GitHub-hosted trusted runner. make test-no-crs, make test-with-crs, and broader
runtime targets are therefore deferred to the later mandatory hosted lifecycle.
The direct check-runtime-producer-readiness target was attempted and blocked as
recorded above; no Framework or MRTS remote operation is required for the
applicable local contract checks.

## Final review status

The candidate remains local until an exact-head PR validation and review round
has completed; no delivery conclusion is inferred from these local checks.

## Final diff and review status

This is an uncommitted Phase-B candidate in the task-owned external worktree
on fix/ci-nginx-broker-runtime-snapshot, based on
ef88a616498e0a2893cd3da54003dd7cdea57015. The final diff contains only the
listed Parent workflow/producer/broker/test/documentation files and the one
Framework Gitlink. An independent focused security review found no reportable
trust-boundary regression. No commit, push, pull request, hosted check, merge,
or Phase-C runtime result is claimed by this record.
