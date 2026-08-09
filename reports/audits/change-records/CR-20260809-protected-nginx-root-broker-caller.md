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

The repository's workflow-Python inventory gains a narrowly enumerated
exception only for the two known immutable reusable calls. This retains the
fail-closed rule for every other reusable workflow invocation instead of
misclassifying a remote root-broker call as a third-party action lock entry.

## Changed files

- `.github/workflows/run-protected-nginx-root-broker.yml`
- `ci/runtime/broker/protected_nginx_broker_caller.py`
- `ci/checks/common/check-python-version-contract.py`
- `tests/test_protected_nginx_broker_caller.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_python_version_contract.py`
- `docs/security/trusted-nginx-root-broker.md` and `.de.md`
- this Change Record and its German companion

## Commands executed

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

The still-unobserved hosted environment may reject the read-only API request,
reusable-workflow context, artifact transfer, NGINX/ModSecurity/CRS runtime, or
cleanup. A pre-merge caller quality or protection-gate failure blocks the
caller merge. A resulting-`master` runtime-dispatch failure instead blocks
resumption of PR #240 after that caller merge; neither outcome authorizes a
branch ref, target-code execution, synthetic PASS, or PR #240 merge.

## Checks not run and rationale

The final exact Python 3.14.6 test gate, hosted checks, CodeQL, SonarQube
Cloud, review/branch-protection gates, and protected-master runtime dispatch
have not yet been observed for the final head. All except the separately
post-merge protected-master runtime dispatch remain required before caller
delivery or caller master integration. That runtime dispatch is instead
required before PR #240 can resume.

## Final diff and review status

This is a locally committed, unpublished implementation on the separate branch
`fix/ci-protected-nginx-broker-caller`, synchronized before publication with
current `origin/master` at `83094eb659f0b5df8c2df30b1ae718d524a9adf0`. The
upstream synchronization carries no task-owned Framework or MRTS gitlink
change in the final PR diff. No caller PR, push, PR #240 change, Framework
source change, MRTS source change, force-push, history rewrite, admin bypass,
or auto-merge has occurred. The caller PR must remain Draft and merge-blocked
until its exact-head local, security, hosted, Sonar, review, and branch-
protection evidence is complete.
