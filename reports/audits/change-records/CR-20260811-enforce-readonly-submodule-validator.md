# Change Record: enforce readonly submodule validator

**Language:** English | [Deutsch](CR-20260811-enforce-readonly-submodule-validator.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260811-enforce-readonly-submodule-validator |
| Date (UTC) | 2026-08-11 |
| Base revision | `4749c02c6dd5e285c4309b4e69b0bb28ae459e48` |
| Delivery status | Implemented and locally validated Parent repair; current-head security scan, hosted validation, PR verification, and delivery remain pending. |

## Motivation and problem statement

The Framework-submodule updater must validate an untrusted Framework candidate
without granting it host-level write access to Parent, Framework, or their Git
metadata. The earlier host-path ACL approach did not provide a reliable
least-privilege execution boundary for the hosted runner's private path layout.
The repair therefore moved candidate execution into a root-created private
mount and PID namespace rather than broadening host-ancestor ACLs.

Hosted run [31488072111](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31488072111)
is failure-only historical evidence at exact head
`5d7d7bbbbb968aa9755d3c0c67a09d8acd651c77`: resolver and sandbox preparation
succeeded, but the validator failed during `make quick-check` with five no-CRS
normalization errors at a runtime-directory traversal denial. The publisher was
skipped, so that run evidences no branch, commit, or pull-request mutation.
`FND-PARENT-0122` is exactly recorded as P1, confirmed, `in_progress`,
security-relevant, and release/candidate-integration-blocking; it is neither
fixed nor verified.

The functional release-blocker repair models only the contained-relative shape
associated with `checks/common.pem` in hosted run `31496603345`. That run ID
identifies the affected hosted context only; a fresh exact-head hosted run must
prove the actual link target conforms. This record does not claim the run
passed or that any later hosted validation has succeeded.

## Acceptance criteria

- Trusted root-side setup creates a private mount and PID namespace, makes
  mount propagation `rprivate`, and keeps its lifecycle outside candidate
  control.
- The candidate receives Parent and Framework sources, including `.git`, only
  through non-recursive read-only `nosuid,nodev` namespace views.
- The workflow must create a fresh `mktemp -d`
  `/tmp/modsecurity-readonly-namespace.XXXXXX` direct child under sticky `/tmp`,
  set it to exactly `root:modsecurity-validator` mode `0750`, and pass it via
  the required `--namespace-parent` argument. The launcher accepts only an
  empty non-symlink direct child of root-owned sticky `/tmp` with that exact
  ownership and mode.
- The candidate receives a writable `nosuid,nodev` namespace view only for the
  exact `external` child of the physical `--write-root`. The fixed logical
  `mount-root`, `source`, and `external` placeholders are each
  `root:modsecurity-validator` mode `0750`, while the physical write root is
  `root:root` mode `0711` and its exact physical `external` child remains
  validator-owned mode `0700`; root-side verification checks the physical
  paths.
- The candidate is PID 1 in the private namespace; the trusted launcher handles
  candidate completion before ending that namespace, guarantees no candidate
  stragglers, and then performs root-side host verification. Teardown uses
  neither lazy unmount nor `rmtree`: it removes only exact empty placeholders
  with non-recursive `rmdir`, and the workflow `EXIT` trap uses non-recursive
  `rmdir` for the trusted namespace parent.
- The locally implemented narrow repair mounts a fresh private `proc` filesystem at `/proc`
  inside PID 1 after `rprivate` is established, with
  `readonly,nosuid,nodev,noexec`. Root mounts it before `PR_SET_NO_NEW_PRIVS`
  and the validator identity drop, then unmounts it and restores the prior
  `/proc` arrangement before namespace exit. It exists solely for
  LeakSanitizer (LSan)'s PID-local `/proc` lookup and is neither full host or
  kernel isolation; hosted validation and finding closure remain pending.
- The root workflow invokes a trusted root `sudo -n python3` launcher. The
  launcher fail-closed sets `PR_SET_NO_NEW_PRIVS`, clears supplementary groups,
  drops to the non-login, non-sudo `modsecurity-validator` GID and UID, and
  `execve`s the fixed candidate program through an explicit fixed environment,
  not an inherited runner environment. That program runs unchanged
  `make quick-check` and receives no publisher or production write authority.
- Source inventory and physical output verification remain fail-closed after
  candidate exit.
- An external output symbolic link is accepted only when validator-owned and
  its link text is nonempty, NUL-free, relative, and lexically normalizes
  within the physical `external` root. Verification must not resolve, stat, or
  dereference its target; absolute targets, including in-root absolute targets,
  lexical escapes to source, guard, or other paths, special objects, and
  source-tree hard links remain rejected.
- `validate_only: true` remains the existing non-publishing exact-ref path; it
  must not become a facility for arbitrary untrusted Parent refs.
- English and German documents and Change Records carry the same material
  facts, evidence status, and limitations.

## Implementation decision and rationale

The repair uses root-side namespace construction because x-only host ACLs are
not an adequate interface for the existing runtime-path validation: opening a
directory can require read permission even when traversal alone is sufficient.
The root-side launcher makes propagation `rprivate` before creating the
candidate mount view, bind-mounts Parent and Framework source/Git state
read-only, non-recursively, with `nosuid,nodev`, and bind-mounts only the
physical `--write-root`/`external` child writable with `nosuid,nodev`. Before
launching, the workflow root-side creates the trusted direct `/tmp` child with
`mktemp -d`, changes it to `root:modsecurity-validator` mode `0750`, and passes
it through the required `--namespace-parent` argument. The launcher validates
that exact empty non-symlink topology, then creates its fixed logical
`mount-root`, `source`, and `external` placeholders as
`root:modsecurity-validator` mode `0750`. The physical write root remains
`root:root` mode `0711`, and its exact physical `external` child remains
validator-owned mode `0700`. The launcher fail-closed sets `PR_SET_NO_NEW_PRIVS`,
clears supplementary groups, drops the candidate GID and UID, and calls
`execve` with an explicit fixed environment. The candidate executes as PID 1 in
that private PID namespace. The launcher waits for and handles its termination,
tears down only the exact empty placeholders with non-recursive `rmdir`, and
verifies physical host source and output state as root; the workflow `EXIT`
trap likewise removes only the trusted namespace parent with non-recursive
`rmdir`.

The locally implemented narrow repair mounts a fresh private `proc` filesystem at `/proc`
inside PID 1 only after the mount namespace is `rprivate`, with
`readonly,nosuid,nodev,noexec`. Root performs this mount before setting
`PR_SET_NO_NEW_PRIVS` and dropping the validator identity, then unmounts it and
restores the prior `/proc` arrangement before namespace exit. This supports
only LeakSanitizer (LSan)'s PID-local `/proc` lookup; it neither expands the
namespace claim to full host or kernel isolation. Hosted validation and
finding closure remain pending.

This maintains the intended output contract without granting the candidate a
host-level traversal or listing right for runner-owned ancestors. Parent,
Framework, and supported output are presented only through namespace views;
ambient unrelated host paths remain outside this scoped contract. It preserves
the separate publisher boundary and leaves Framework and MRTS source, the
Parent Gitlink, and Make target semantics out of scope.

The physical external-output verifier now permits only the narrow
validator-owned relative-link case described in the acceptance criteria. Its
check is lexical containment of nonempty, NUL-free link text inside the
physical `external` root, not target resolution or filesystem inspection. This
models only a contained-relative `checks/common.pem` shape; a fresh exact-head
hosted run must prove the actual target conforms. It retains fail-closed
rejection of absolute links (even in-root ones), lexical escapes, special
objects, and source-tree hard links.

The existing `workflow_dispatch` input `validate_only: true` stays limited to
the trusted task repair ref before merge and protected Parent `master` after
merge with `github.ref_protected == true`. Each allowed path uses its
dispatched `github.sha`, forces candidate validation even when candidate and
gitlink match, and makes the publisher ineligible. This is not an untrusted
Parent pull-request/ref sandbox: Parent workflow and helper code are trusted
before root-side namespace setup; the Framework candidate is the untrusted
payload.

## Security impact

The relevant security boundary is untrusted Framework-candidate execution
against Parent and Framework source/Git state and the updater publisher. The
private mount/PID namespace prevents the candidate from receiving a writable
source view and confines supported candidate output to the physical external
root that root-side verification examines. `rprivate` prevents propagation of
candidate mount changes back through shared mount propagation. `nosuid,nodev`
reduces the mount-view attack surface. `PR_SET_NO_NEW_PRIVS` is set fail-closed
before the candidate identity drop, and the candidate verifies `NoNewPrivs: 1`.
The locally implemented private `/proc` mount is restricted to PID 1 and uses
`readonly,nosuid,nodev,noexec`; it is mounted and removed by root during the
namespace lifecycle solely to support LSan's PID-local lookup.

This is not full host or kernel security isolation. Parent, Framework, and
supported output are the only presented namespace views; unrelated ambient host
paths remain outside the contract. It does not prove that malicious candidate
code cannot use every unrelated globally writable host facility, exploit a
kernel flaw, or escape a process boundary. The repair does not weaken source/Git
locks, output verification, validation-only publication guardrails, branch
protection, or publisher permissions.

The permitted symbolic-link case does not widen that boundary: target text is
checked lexically without resolving, calling `stat` on, or dereferencing an object, and
all nonconforming links remain rejected. It is not evidence of full host
isolation.

## Changed files

The implemented repair changes the Parent validator workflow, the root-side
preparer and namespace launcher, focused contract tests, and this English/German
build documentation and Change Record pair. It does not authorize a Framework
or MRTS change, a Parent Gitlink change, or a delivery action. The final exact
changed-file list must be reconciled with the reviewed repair head before
delivery.

## Commands executed

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_ci_security_workflows
  tests.test_prepare_readonly_submodule_validation_sandbox
  tests.test_run_readonly_submodule_validation_namespace` passed: 55 tests
  with three expected capability skips.
- `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` passed with the
  same 55-test/three-skip suite result and its `validate_only` actionlint,
  zizmor, and gitleaks-lock checks.
- `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` passed (`bilingual
  docs ok`); no-bytecode `py_compile` and `git diff --check` also passed.

This is limited local test and contract evidence. The three expected capability
skips mean it is not privileged mount or validator-identity runtime proof. It
does not substitute for a current-head security scan, hosted validation, PR
checks, SonarQube Cloud, review, merge, resulting-master validation, or
delivery.

## Runtime evidence

Run `31488072111` is the only newly recorded hosted fact in this repair round:
it failed at exact head `5d7d7bbbbb968aa9755d3c0c67a09d8acd651c77` after
resolver and sandbox preparation, during the isolated quick check. Its
root-side post-run source/output verification did not execute, its publisher
was skipped, and its outcome failed because validation failed. It is not a
successful namespace run, security scan, PR check, merge, or delivery result.

Hosted run `31496603345` supplies the `checks/common.pem` context for the
functional verifier repair. It is not recorded here as a successful hosted run
or as validation of the repaired current head; a fresh exact-head hosted run
must prove the actual target conforms.

## Checks not run and rationale

- A current-head security scan — pending the final namespace repair head.
- A fresh hosted `validate_only` run — pending the final namespace repair head.
- PR checks, review disposition, SonarQube Cloud result, squash merge, and
  resulting-master verification — pending the current-head scan and hosted
  validation gates.
- A post-merge updater dispatch and Draft Gitlink PR — outside this repair
  record until the Parent repair is merged and the trusted default-branch
  validation succeeds.

## Known limitations

This record describes an implemented design with bounded local validation. It
does not independently prove GitHub-hosted runner behavior, hosted mount/PID
namespace availability, current-head source integrity, or a successful hosted
execution. The repair head still requires an exact-head security scan and
hosted validation.

## Remaining risks

Correct behavior depends on GitHub-hosted Linux support for the required
root-side namespace and mount operations, and on the launcher failing closed
when setup, lifecycle cleanup, or physical host verification fails. A private
mount/PID namespace is deliberately narrower than a general host sandbox.
`FND-PARENT-0122` remains open until the failure is remediated and the required
fresh local, security, and hosted evidence is observed.

## Final diff and review status

This is not a final delivery record. The observed bilingual and scoped
whitespace checks are recorded above; final current-head scan, hosted, PR,
SonarQube, merge, and resulting-master evidence remain pending.
