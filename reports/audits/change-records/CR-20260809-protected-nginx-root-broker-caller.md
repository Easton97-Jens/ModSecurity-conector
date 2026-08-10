# Change Record

**Language:** English | [Deutsch](CR-20260809-protected-nginx-root-broker-caller.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260809-protected-nginx-root-broker-caller |
| Date (UTC) | 2026-08-09 |
| Base revision | 83094eb659f0b5df8c2df30b1ae718d524a9adf0 |

## Motivation and problem statement

The trusted NGINX root broker v2 was merged as reusable `workflow_call` code,
but protected Parent `master` had no dispatch-only caller. Consequently, no
resulting-master run could prove both fixed `no-crs` and `owasp-crs` broker
profiles, their uploaded evidence, and descriptor-relative cleanup before
PR #240 relied on that boundary.

## Follow-up reusable broker binding repair

After the caller was merged, resulting-master dispatch
[`31310183097`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31310183097)
failed closed before broker checkout, build, CRS creation, `sudo`, root
admission, NGINX start, evidence projection, or cleanup. The former check
expected the broker identity
`Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@e06254ea9622d214a9030b9ba786756560ace417`,
but GitHub supplied the caller identity
`Easton97-Jens/ModSecurity-conector/.github/workflows/run-protected-nginx-root-broker.yml@refs/heads/master`.
The former comparison was correctly fail-closed but conceptually wrong:
GitHub assigns the `github` context in a called reusable workflow to its
caller. Therefore, this run provides no root, NGINX, CRS, worker, artifact, or
cleanup PASS evidence.

The repair keeps a binding stage but separates caller context, caller commit,
caller YAML, immutable reusable-workflow input SHA, checked-out broker HEAD,
both broker source blobs, and Framework gitlink. It accepts only the exact
dispatch-only protected-master caller context, reads the fixed caller path only
as a bounded regular Git blob at the actual caller commit, and validates a
restricted declarative YAML schema. Exactly the two fixed broker jobs must use
one literal SHA-40 equal to their `protected_broker_sha` input, the fixed
variants and inputs, read-only permissions, and no secrets. The broker commit
must be a protected-master ancestor, and both its workflow and Python blobs
must match before candidate creation and immediately before root actions.

No `id-token: write` permission or OIDC alternative is added. The caller stays
on the old `e06254ea9622d214a9030b9ba786756560ace417` pin during this repair.
Because the repository uses squash merge, a separate caller-repin PR must use
the resulting broker-repair merge SHA before a new protected-master dispatch
can provide lifecycle evidence.

## Acceptance criteria

The new caller is available only through `workflow_dispatch` on the canonical
non-fork protected `master` and accepts only required `parent_head_sha`. That
value is lowercase SHA-40 commit evidence only: it is checked through a fixed
read-only GitHub API endpoint and is never checked out, imported, sourced,
built, started, loaded, or root-executed. The caller creates exactly two
private schema-v2 manifests and makes exactly two explicit immutable calls to
broker SHA `e06254ea9622d214a9030b9ba786756560ace417`, bound to Framework SHA
`c71e15db7b7517b237add9fa09b3493e7bc93627`.

The two closed profiles are `no-crs`/`no-crs` and `with-crs`/`owasp-crs`.
An unprivileged readback validates exact evidence files, schemas, identities,
root-master/non-root-worker records, cleanup PASS, and the CRS audit/bundle
binding. A final always-run result job must fail closed when preparation,
either broker, or readback fails.

## Implementation decision and rationale

The implementation adds one Parent-owned workflow rather than widening the
broker's reusable interface or adding another root runner. A small
repository-owned Python helper has only manifest-generation and evidence-
validation subcommands. It serializes deterministic JSON with private paths
and modes, rejects unknown/duplicate fields and symlinks, and treats artifact
contents only as bounded data. The caller uses only full SHA action pins and
the existing full-SHA reusable broker reference; it has no secrets, write
permissions, `sudo`, local reusable reference, profile/path/command input, or
target-commit checkout.

The helper accepts no caller-selected manifest or evidence filesystem path. It
derives its two fixed roots only from an absolute, non-symlink runner-provided
`RUNNER_TEMP` directory and the validated paired fixed run IDs. Invalid or
mismatched path identity therefore fails before API access, artifact creation,
or evidence readback; each derived root is independently required to be a
non-symlink directory.

The repository's workflow-Python inventory gains a narrowly enumerated
exception only for the two known immutable reusable calls. This retains the
fail-closed rule for every other reusable workflow invocation instead of
misclassifying a remote root-broker call as a third-party action lock entry.

## Changed files

This record spans the already merged protected caller (PR #259) and this
follow-up reusable-binding repair. The caller paths below belong to the merged
caller change, not to the current repair diff.

- **Merged caller PR #259:** `.github/workflows/run-protected-nginx-root-broker.yml`,
  `ci/runtime/broker/protected_nginx_broker_caller.py`, and
  `tests/test_protected_nginx_broker_caller.py`.
- **Reusable-binding repair:** `.github/workflows/nginx-root-broker.yml`,
  `ci/runtime/broker/nginx_root_broker.py`,
  `ci/checks/common/check-python-version-contract.py`,
  `tests/test_ci_security_workflows.py`, `tests/test_python_version_contract.py`,
  `tests/test_nginx_root_broker.py`, and `tests/test_nginx_root_broker_workflow.py`.
- **Paired documentation:** `docs/security/trusted-nginx-root-broker.md` and
  `.de.md`, plus this Change Record and its German companion.

## Commands executed

### Historical caller PR validation

The exact-head local validation passed with the available local Python 3.14.4
as a non-canonical static fallback: the focused caller/broker/CI-security/
Python-version suites (82 tests), `make check-ci-security-contract`, source
`py_compile`, `make lint`, bilingual documentation and link checks, actionlint
with ShellCheck, zizmor offline, and `git diff --check` all passed. The focused
security-diff scan was sealed with complete 10/10 file-worklist receipts and no
reportable finding. The project requires Python 3.14.6, so this does not claim
the required exact local interpreter gate. `make check-python-version-contract`
has the same pre-existing inventory failure on unchanged `master` and is not
treated as a caller regression.

On Draft PR #259, SonarQube Cloud initially reported seven task-owned open
findings and failed the new-code security-rating condition. The follow-up
remediation removes arbitrary helper filesystem-path arguments, derives and
checks only fixed runner-temp roots, extracts the reported validation branches,
and adds pre-I/O path regression coverage. Focused caller/CI-security tests,
Python compilation, CI-security contract checks, full `make lint`, bilingual
and link checks, actionlint with ShellCheck, zizmor offline, and diff checks
passed locally on the available Python 3.14.4 fallback. Every current PR head
independently requires fresh hosted and SonarQube Cloud evidence; no historical
head result is a substitute.

### Current reusable-binding repair validation

At the current local candidate stage, the focused Python-contract, broker,
broker-workflow, and CI-security suites passed 80 tests using the available
Python 3.14.4 fallback. `make check-ci-security-contract`, source
`py_compile`, actionlint with ShellCheck, zizmor offline, the bilingual
documentation unit suite, and `git diff --check` passed. The exact Python
3.14.6 gate and all current-head hosted, SonarQube Cloud, review, and
branch-protection evidence remain pending.

`make check-python-version-contract` remains nonzero only for pre-existing
`master` inventory defects outside this repair; the repaired
`nginx-root-broker.yml:trusted-root-smoke` job is not among its diagnostics.
Repository-wide bilingual and link targets are blocked by the intentionally
uninitialized Framework submodule's pre-existing link targets; they report no
repair-specific paired-document mismatch.

## Security impact

The caller preserves the existing root boundary: only the immutable broker
commit checks out and executes protected broker source under root, while the
caller does not run target Parent code or any root action. Its target SHA is
validated before it can enter a manifest, and no shell command, artifact path,
variant, profile, Framework SHA, broker SHA, CRS tuple, rule, binary, module,
or configuration is selected by dispatch input. The explicit evidence validator
also prevents a stale, foreign-run, incomplete, unknown-schema, or failed-
cleanup artifact from being reported as a successful caller lifecycle.

## Runtime evidence

No protected-master caller run has been observed at this local change-record
stage. A successful post-merge manual dispatch must prove the real GitHub
context, the immutable reusable call, root master/non-root worker lifecycle,
both profiles, CRS audit, artifact upload/download, and cleanup. Local tests
cannot substitute for that resulting-master evidence.

## Known limitations

The caller deliberately validates an immutable broker's bounded evidence; it
does not turn that evidence into a generic privileged execution system. GitHub
artifact transport remains the platform boundary between the broker and
unprivileged readback. The readback therefore validates strict structure and
cross-field identity rather than inventing a separate artifact signing scheme.

## Remaining risks

The distinct protected-`master` runtime environment may reject the read-only
API request, reusable-workflow context, artifact transfer,
NGINX/ModSecurity/CRS runtime, or cleanup. A failure of a current-head
pre-merge caller quality or protection gate blocks the caller merge. A
resulting-`master` runtime-dispatch failure instead blocks resumption of PR
#240 after that caller merge; neither outcome authorizes a branch ref,
target-code execution, synthetic PASS, or PR #240 merge.

## Checks not run and rationale

The exact Python 3.14.6 local test gate is unavailable in this environment.
For every current PR head, hosted checks, CodeQL, SonarQube Cloud, review, and
branch-protection evidence must be read afresh at the merge decision; a record
or older head cannot provide that evidence. The protected-`master` runtime
dispatch is necessarily post-merge and is required before PR #240 can resume.

## Final diff and review status

The normal initial push created Draft PR #259 on the separate branch
`fix/ci-protected-nginx-broker-caller`, synchronized with current
`origin/master` at `83094eb659f0b5df8c2df30b1ae718d524a9adf0`. Its initial
head was `b50849263b88a1e9aae5e2c596d05a9af1e88832`: visible GitHub Actions
and CodeQL checks passed, while SonarQube Cloud found the task-owned issues
recorded above. The upstream synchronization carries no task-owned Framework
or MRTS gitlink change in the final PR diff. No PR #240 change, Framework
source change, MRTS source change, force-push, history rewrite, admin bypass,
or auto-merge has occurred. This Change Record intentionally makes no mutable
Draft, check, review, or merge-state assertion: GitHub and SonarQube Cloud are
the authority for the current PR head. A normal protected merge may be
considered only when current exact-head local, security, hosted, Sonar, review,
and branch-protection evidence is complete and the current user authorization
remains valid.
