# Change Record: read-only submodule sandbox source preservation

**Language:** English | [Deutsch](CR-20260819-readonly-submodule-sandbox-preservation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260819-readonly-submodule-sandbox-preservation |
| Date (UTC) | 2026-08-19 |
| Base revision | `35c435483dcd637c7b9df0277bed34d6f94dc44d` |
| Historical Framework Gitlink | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| Delivery status | Task-owned Draft PR [#302](https://github.com/Easton97-Jens/ModSecurity-conector/pull/302) was created from `agent/readonly-submodule-sandbox-preservation` at `c1b07a572321c31de1a0a9ae1fd554e2f9811b9f`; follow-ups made `35244aae8b3c8676e52d85e3869f9d9b4279f70e` the pre-record current head. On that exact head, all required GitHub Actions passed, SonarQube Cloud check `96135044055` passed with `new_duplicated_lines=0`, `new_duplicated_lines_density=0.0`, zero new violations, and zero annotations, and the one bounded `traefik-go` rerun passed. At `2026-08-19T17:32:07Z`, the current user authorized protected integration of PR #302 and explicitly accepted the two documented residual risks for that one merge. This record correction must receive its own fresh exact-head checks before Ready-for-review and the protected squash merge; no merge is claimed. |

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

The exact Draft PR #302 head `a0f46d4e22830f081b20096734caf7e4a059b5cd`
then failed the unchanged SonarCloud Quality Gate on `6.4% Duplication on New
Code`. Its task-owned annotations identify a duplicate source literal,
cognitive complexity `16` where `15` is allowed, and a test assertion with
multiple potentially throwing calls. The follow-up must reduce duplication to
zero through source-native changes, not scanner, Quality-Gate, exclusion,
suppression, `NOSONAR`, or issue-dismissal changes.

The source-native successor
`35244aae8b3c8676e52d85e3869f9d9b4279f70e` did so without changing a scanner,
Quality Gate, exclusion, suppression, `NOSONAR`, dismissal, or sandbox
control. It passed SonarQube Cloud with zero New-Code duplication and the
required GitHub Actions bundle after the bounded `traefik-go` rerun.

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
- A successor exact PR #302 head reports `new_duplicated_lines=0` and
  `new_duplicated_lines_density=0.0` with the unchanged SonarCloud Quality
  Gate and no task-owned new annotation.
- The Sonar remediation preserves the same source-isolation, mount-topology,
  fail-closed decoder, cleanup, and legitimate external-output controls.
- Required GitHub Actions and SonarCloud results are observed on the same
  successor head before any ready-for-review or protected merge action.

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

The Sonar follow-up deduplicates the preparer's `source root` literal, rewrites
the mountinfo decoder into an equivalent split-and-validate form, extracts the
existing exact placeholder cleanup from `run()`, and adds malformed-octal
decoder coverage. Its test refactor shares only fixture construction and keeps
the existing source-preservation, exception, and external-output assertions.
No scanner setting, quality gate, exclusion, suppression, or sandbox control
changes.

## Security impact

This removes a high-impact trusted-root mutation of source and Git metadata
while retaining the untrusted Framework-candidate containment boundary. It
does not weaken candidate no-write probes, root-side inventory verification,
external-output validation, no-new-privileges, capability checks, publisher
separation, action pins, repository/default-branch guards, or read-only job
permissions. It does not add network-egress or kernel-exploit isolation.

The narrow refactor was security-diff reviewed against sealed patch SHA-256
`79074648aa1f204bcaeddd98a2c50cb62f92d2b2d01e22b98d1cb6b0ce2d9378`.
It produced zero reportable findings. The one cleanup-path candidate,
`NSR-001`, was rejected because `_create_mount_layout()` is already inside
`run()`'s `try/finally` and the injected partial-layout regression proves exact
cleanup.

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

The Sonar follow-up changes only the two Python helpers, the two focused test
modules, and this paired Change Record. Reader-facing build documentation is
unchanged because the sandbox's documented behavior and security contract do
not change.

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
  passed: 35 tests, 3 expected namespace-capability skips, including cleanup
  after a partial mount-layout creation failure.
- A dedicated virtual environment below the registered external task root
  installed hash-locked `PyYAML==6.0.3`; its
  `python -m unittest tests.test_ci_security_workflows` run passed: 28 tests.
- `make check-ci-security-contract` passed: 122 tests, 5 expected skips, then
  hash-locked actionlint/zizmor/gitleaks validation.
- Exact pinned `actionlint .github/workflows/update-submodules.yml`,
  `make check-doc-links`, targeted paired-document structural/link checks, and
  `git diff --check` each passed.
- `python3 -m unittest discover -q` exited `5` after `Ran 0 tests`; this
  repository's default invocation does not discover the `tests` package.
- `make lint` and `make quick-check` each exited `2` at the same unrelated
  five HAProxy cache tests, all blocked by `CRS_REPO_URL override is not
  permitted`, before this sandbox's candidate execution path.
- After byte-identical recovery of the Sonar patch, `PYTHONDONTWRITEBYTECODE=1
  /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v
  tests.test_prepare_readonly_submodule_validation_sandbox` passed: 25 tests,
  2 expected skips; the equivalent namespace command passed: 35 tests, 3
  expected skips. `make check-ci-security-contract` then passed: 122 tests, 5
  expected skips. `git diff --check` passed.
- Exact pre-record PR #302 head `35244aae8b3c8676e52d85e3869f9d9b4279f70e`
  passed SonarQube Cloud check `96135044055` with zero new-code duplication,
  violations, code smells, and annotations; `gh pr checks 302` exited `0`.
  The one initial bounded `traefik-go` fuzz timeout was investigated and its
  unchanged rerun `96141428932` passed. This documentation-only correction
  requires a fresh successor-head run before protected integration.

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

The pre-record exact PR #302 head succeeded in hosted GitHub Actions and
SonarQube Cloud as described above. No hosted `validate_only`
source-preservation run is claimed. A direct mapped user/mount/PID-namespace
probe exited `1` with `Operation not permitted`.

The sealed working-tree security-diff report is
`/var/tmp/codex/ModSecurity-conector/20260819T145000Z-sonar-duplication-security-diff/report.md`
(SHA-256 `761396a57c0182b0b2c4778fdcf4ba08f6514b9039d73d38f31d404f261445c4`).
It covers all four changed paths and has zero reportable findings. The reviewed
and restored patches have the identical SHA-256
`79074648aa1f204bcaeddd98a2c50cb62f92d2b2d01e22b98d1cb6b0ce2d9378`.

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
- The prior exact PR #302 head's SonarCloud failure was remediated: pre-record
  successor `35244aae8b3c8676e52d85e3869f9d9b4279f70e` has successful required
  GitHub Actions and SonarQube Cloud evidence. This record correction is a new
  successor and must repeat all exact-head checks, review, Ready-for-review,
  merge, and resulting-master evidence. The local mapped non-root namespace
  integration remains unavailable.

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

At `2026-08-19T17:32:07Z`, the current user explicitly accepted, for this
protected PR #302 `master` integration only, the absence of mapped non-root
namespace/hosted `validate_only` source-preservation evidence and the five
unrelated HAProxy cache-fixture failures that block broad `make lint` and
`make quick-check`. The wording was: “Ich akzeptiere beide Risiken für den
Master-Merge von PR #302 und autorisiere Ready-for-review und den geschützten
Merge nach maste”. The final word is interpreted as `master` from the
unambiguous selected PR and “Master-Merge” wording. This is neither a finding
closure nor a waiver for later work.

The shared checkout unexpectedly switched to `master` while the follow-up patch
was uncommitted, then returned to the task branch. The patch was recovered
byte-identically and no actor is attributed; `FND-PARENT-0182` retains this
separate lifecycle defect. Branch, reflog, source scope, and patch identity
must be rechecked before staging or pushing. During the current
master-integration preflight, the checkout again moved through a foreign branch
to `master`; the main agent returned cleanly without tracked task loss, and
`FND-PARENT-0182` records the new evidence.

## Final diff and review status

The pre-record Sonar remediation is complete and reviewed: it has no
whitespace errors, the focused security review found zero reportable findings,
the focused modules passed after recovery, `make check-ci-security-contract`
passed, and exact head `35244aae8b3c8676e52d85e3869f9d9b4279f70e` passed the
required hosted checks and SonarQube Cloud. The two independent limitations
are accepted for this one protected PR #302 integration only. This record
correction now requires a focused documentation/diff review, a normal follow-up
commit and push, then a fresh exact-head check, review, ruleset, Ready-for-
review, protected squash-merge, and resulting-master verification cycle. No
ready-for-review or merge result is claimed here.
