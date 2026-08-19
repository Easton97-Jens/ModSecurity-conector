# Change Record: read-only submodule sandbox source preservation

**Language:** English | [Deutsch](CR-20260819-readonly-submodule-sandbox-preservation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260819-readonly-submodule-sandbox-preservation |
| Date (UTC) | 2026-08-19 |
| Base revision | `35c435483dcd637c7b9df0277bed34d6f94dc44d` |
| Historical Framework Gitlink | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| Delivery status | Draft PR [#302](https://github.com/Easton97-Jens/ModSecurity-conector/pull/302) was created from `agent/readonly-submodule-sandbox-preservation` at `c1b07a572321c31de1a0a9ae1fd554e2f9811b9f`; local, remote, and PR-head SHA matched at creation. It remains Draft with hosted checks pending. The current user accepted/deferred the missing mapped non-root namespace/hosted evidence and the five independent HAProxy cache-fixture failures for this Draft PR only; no ready-for-review state or merge is authorized. |

## Motivation and problem statement

The root-side read-only-submodule preparer previously recursively called
`_lock_tree(source)` and `_lock_tree(framework)`. Those calls changed the true
Parent checkout, Parent `.git` and `.git/modules`, and the Framework subtree
in place through `os.chown(..., 0, 0)` and `os.chmod(... & ~0o022)`. The
historical context is [PR #301](https://github.com/Easton97-Jens/ModSecurity-conector/pull/301)
and merge commit `35c435483dcd637c7b9df0277bed34d6f94dc44d`; the Gitlink is
historical context, not the root cause. A restore-based approach is unsafe
because original ownership, groups, modes, ACLs, and local workspace policy
cannot be reconstructed reliably.

## Acceptance criteria

- Parent, Framework, `.git`, and `.git/modules` remain byte-, type-, owner-,
  group-, mode-, link-, and link-target-identical across prepare, candidate,
  verify, failure, and cleanup paths.
- The candidate continues to receive only non-recursive read-only source views
  and only the exact private `external` output root is writable.
- The candidate remains a dedicated unprivileged identity with empty
  supplementary groups, no effective capabilities, and `no_new_privs`.
- The full source inventory is collected before and compared after candidate
  execution; output, link, hardlink, Gitfile, mount, and descriptor controls
  remain fail-closed.
- Nested source mounts are rejected before source binding or candidate code.
- Workflow root use is limited to private guard/identity/inventory/namespace/
  cleanup operations; candidate-state checks and `git diff --check` are not
  run through `sudo`.
- Cleanup accepts only a checked direct private child of `RUNNER_TEMP` and
  cannot follow symlinks, traverse source, or delete an active mount.

## Implementation decision and rationale

`_lock_tree` and both calls on the true source and Framework roots are removed.
The preparer validates topology, source links and Gitfiles, rejects strict
source submounts, validates the identity, inventories the unchanged source,
writes a root-owned mode-`0600` inventory inside the private guard, and creates
the validator-owned mode-`0700` `external` root. The namespace runner remains
the actual write barrier: private mount propagation, a non-recursive source
bind remounted read-only with `nosuid,nodev`, private jail/chroot/PID namespace,
closed inherited descriptors, explicit environment, identity drop,
`PR_SET_NO_NEW_PRIVS`, and candidate probes are retained. It independently
rejects nested source mounts.

The workflow creates and outputs the fixed-prefix
`$RUNNER_TEMP/modsecurity-readonly-validation.XXXXXX` guard before prepare can
fail. The helper cleanup mode requires canonical non-symlink paths, an exact
direct `RUNNER_TEMP` child with that prefix, disjoint Parent/Framework/Git
paths, root-owned mode `0711`, and no active mount. It opens path components by
descriptor with `O_NOFOLLOW` and removes only descriptor-relative entries.

## Security impact

This removes a high-impact trusted-root mutation of source and Git metadata
while retaining the untrusted Framework-candidate containment boundary. It
does not weaken candidate no-write probes, root-side inventory verification,
external-output validation, no-new-privileges, capability checks, publisher
separation, action pins, repository/default-branch guards, or read-only job
permissions. It does not add network-egress or kernel-exploit isolation.

## Changed files

- `ci/tools/prepare-readonly-submodule-validation-sandbox.py`
- `ci/tools/run-readonly-submodule-validation-namespace.py`
- `.github/workflows/update-submodules.yml`
- `tests/test_prepare_readonly_submodule_validation_sandbox.py`
- `tests/test_run_readonly_submodule_validation_namespace.py`
- `tests/test_ci_security_workflows.py`
- `docs/build/README.md` and `docs/build/README.de.md`
- this Change Record pair and the paired archive index
- Parent local finding `FND-PARENT-0184` and task-local evidence/plan records

No Framework or MRTS source, Gitlink, product source, commit, push, pull
request, or merge is authorized by this record.

## Commands executed

- Pre-fix fixture-only reproduction recorded one mode mutation from `0664` to
  `0644` by the old `_lock_tree` path; no real checkout was touched.
- `python3 -m py_compile` for the changed helpers and focused tests passed.
- `python3 -m unittest tests.test_prepare_readonly_submodule_validation_sandbox`
  passed: 25 tests, 2 expected capability/identity skips. It includes complete
  metadata snapshots after prepare, injected namespace-setup and
  candidate-result failures, verify, and cleanup.
- `python3 -m unittest tests.test_run_readonly_submodule_validation_namespace`
  passed: 34 tests, 3 expected namespace-capability skips, including cleanup
  after a partial mount-layout creation failure.
- A dedicated virtual environment below the registered external task root
  installed hash-locked `PyYAML==6.0.3`; its
  `python -m unittest tests.test_ci_security_workflows` run passed: 28 tests.
- `make check-ci-security-contract` passed: 121 tests, 5 expected skips, then
  hash-locked actionlint/zizmor/gitleaks validation.
- Exact pinned `actionlint .github/workflows/update-submodules.yml`,
  `make check-doc-links`, targeted paired-document structural/link checks, and
  `git diff --check` each passed.
- `python3 -m unittest discover -q` exited `5` after `Ran 0 tests`; this
  repository's default invocation does not discover the `tests` package.
- `make lint` and `make quick-check` each exited `2` at the same unrelated
  five HAProxy cache tests, all blocked by `CRS_REPO_URL override is not
  permitted`, before this sandbox's candidate execution path.

## Runtime evidence

The fixture-only pre-fix reproduction is retained at
`/var/tmp/codex/ModSecurity-conector/runs/readonly-submodule-sandbox-preservation-20260819/evidence/pre-fix-lock-tree-reproduction.json`
with SHA-256
`8b83a574f71d29300d627fb2d2a8c672e1c9b3501d6f4f4afeaf3100fca7ec49`.
The current environment maps only UID/GID 0, so that reproduction directly
observed the old mode mutation but cannot demonstrate a non-root UID becoming
UID 0. The new privileged prepare/candidate/verify integration test exists and
skips fail-closed where the kernel or user namespace cannot map the dedicated
identity or create the required namespace.

No successful hosted run is claimed for this change. A direct mapped
user/mount/PID-namespace probe exited `1` with `Operation not permitted`.

## Checks not run and rationale

- The real mapped non-root prepare/candidate/verify integration is blocked in
  this container: both the `nobody` identity mapping and user/mount/PID
  namespace creation are unavailable. The tests skip rather than weaken the
  boundary.
- The broad `make check-bilingual-docs` target was stopped after more than
  seven minutes without a result because its recursive walk enters ignored
  virtual-environment content before applying ignore filtering. The changed
  pairs passed targeted structural, identity, and local-link checks; checker
  behavior is outside this remediation scope.
- A correctly scoped full discovery (`-s tests`) was not run in the shared
  checkout because `FND-PARENT-0182` records a separate checkout-preservation
  risk. The requested default discovery was nevertheless run and recorded
  above.
- Hosted `validate_only`, security scan, pull-request checks, SonarQube, and
  review are pending for Draft PR #302. The local mapped non-root namespace
  integration remains unavailable. No ready-for-review transition or merge is
  authorized.

## Known limitations

The local container may not permit a complete mount/PID namespace or map the
dedicated `nobody` identity; affected integration tests skip rather than weaken
the boundary. This repair does not automatically modify an already root-owned
checkout. Users must inspect a specific path and apply a deliberate manual
repair outside the workflow if appropriate.

## Remaining risks

The namespace is a scoped filesystem/process boundary, not complete host,
kernel, or network isolation. Cleanup performs initial and final active-mount
checks and descriptor-relative deletion; it assumes the trusted runner does
not concurrently mount attacker-controlled content into the root-only guard.
Future changes must retain the source-preservation, nested-mount, private-path,
and no-restore static contracts.

## Final diff and review status

Final local review is complete: source locking is removed, the private guard
cleanup handles partial namespace setup, focused regression/security contracts
and documentation checks pass, and the final diff has no whitespace errors.
The finding remains locally `fixed`, not `verified` or closed, because mapped
non-root namespace and hosted exact-head evidence remain unavailable/not yet
observed; the unrelated HAProxy test blocker also prevents a green broad
lint/quick-check claim. The current user accepted/deferred those exact gaps
only to permit Draft PR #302 from the current checkout. It deliberately makes
no hosted-CI success, ready-for-review, verified-PR, or merge claim.
