# Build documentation

**Language:** English | [Deutsch](README.de.md)

This section explains how root and connector Make targets prepare and build
selected connector routes. A build, link, or config-load result is not runtime
evidence and does not make a production, CRS, HTTP/2, HTTP/3, complete-matrix,
or strict-for-all-connectors claim.

## Build inputs and safe paths

The root Makefile derives its working tree below
<code>VERIFIED_RUN_ROOT</code>. For a reproducible local build, set
<code>BUILD_ROOT</code> to an absolute writable directory outside the
checkout:

~~~sh
make build-nginx BUILD_ROOT="/srv/modsecurity-work/build"
~~~

<code>BUILD_ROOT</code> is optional because the Makefile derives
<code>VERIFIED_RUN_ROOT/build</code> when it is not provided. The example
value <code>/srv/modsecurity-work/build</code> is an absolute runtime path, not
a repository default. Do not use the repository root, a system directory, or a
path containing secrets. See [configuration variables](../reference/variables.md#runtime-and-repository-paths)
for format, scope, impact, and security details.

The placeholder <code>&lt;connector&gt;</code> means exactly one of
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code>, or <code>lighttpd</code>. For
example, use <code>make build-nginx</code>; do not type
<code>make build-&lt;connector&gt;</code> literally.

## Target families

| Target | Purpose | Prerequisites / important variables | Produced output | Boundary |
|---|---|---|---|---|
| <code>make check-framework</code> | Checks that the Framework is available | <code>FRAMEWORK_ROOT</code> points to an existing Framework checkout | Console result | Does not build a connector |
| <code>make setup-dev</code> | Installs or prepares development Python dependencies through the Framework | <code>PYTHON</code>, <code>FRAMEWORK_ROOT</code> | Development environment changes outside tracked source | Does not prepare every host component |
| <code>make prepare-runtime-components</code> | Obtains/builds reusable pinned host components | Safe build/cache paths, optional source pin variables | Component cache and environment snapshot | Does not execute connector lifecycle traffic |
| <code>make build-<connector></code> | Runs the selected connector build stage | Framework, build root, target-specific host inputs | Connector-specific build output | A successful build is not config or runtime proof |
| <code>make build-all-connectors</code> | Runs the build stage for all six connector names | All relevant host/component prerequisites | Per-connector build output | Aggregate build does not create full-lifecycle evidence |
| <code>make check-config-<connector></code> | Loads/checks selected connector configuration | Prepared selected build and configuration | Config-load diagnostics | Does not send traffic |
| <code>make prepare-open-connector-runtimes</code> | Prepares selected Envoy, Traefik, and lighttpd host inputs | Framework and cache/provisioning prerequisites | Component preparation output | Preparation is not capability promotion |
| <code>make lint</code> | Runs source, contract, and documentation-oriented checks | Python, shell tools, Framework, C toolchain where available | Diagnostics | Not an all-host runtime test |

Process exit code <code>0</code> means only that the invoked target completed
its technical contract. <code>1</code> is a general failure, <code>2</code>
is invalid input/contract validation, and <code>77</code> means a missing
optional or required environment prerequisite. See [Testing](../testing-and-evidence.md)
for the status vocabulary.

## Parent CI Python-version contract

This checked-in Parent GitHub Actions contract records the implemented
interpreter strategy, workflow boundaries, and local static-validation
evidence. It does not represent a GitHub Actions execution, remote CI run,
pull request, review, or delivery result.

### Canonical interpreter and strategy

The committed root [`.python-version`](../../.python-version) is the generated
setup-action view of `python_version` in the canonical
[`ci/tooling/project-versions.lock.json`](../../ci/tooling/project-versions.lock.json).
Its required content is the exact stable release <code>3.15.1</code>. Every normal Python-executing job in the inventory below
must run `actions/setup-python` before its first direct or indirect Python use
with:

~~~yaml
python-version-file: .python-version
check-latest: false
~~~

The version literal must not be duplicated in workflow YAML. The setup action
is separately action-pinned; an action-lock record is not an interpreter
version source. The accepted setup reference is the existing immutable
`actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0`
pin that is also recorded in `ci/tooling/security-tools.lock.yml`; the
contract checker must validate that same v7 reference rather than a stale v6
expectation. After setup, the workflow contract must validate that `python`
and `python3` select equivalent configured Python <code>3.15.1</code>
interpreters before either name, a Python-backed Make target, or an indirect
Framework check is used. No normal job may fall back to an ambient runner,
bootstrap, virtual-environment, or system `python3` interpreter.

| Alternative | Decision | Rationale |
| --- | --- | --- |
| Floating `3.15` | Rejected | A later runner/tool-cache resolution can silently select a different patch release, creating patch drift. |
| Exact `3.15.1` from one committed `.python-version` file | Selected | The exact stable patch is reviewable and reproducible, while `python-version-file` gives every covered job the same source. |
| Exact version plus a permanent canary workflow | Rejected | The independent, read-only candidate-validation stage below validates a proposed patch before publication; an additional canary would duplicate that control without changing the publisher trust boundary. |

For Python 3.15, install the Parent CI dependency from a task-owned virtual
environment with `python ci/tools/install-ci-dependencies.py --build-root "$RUNNER_TEMP"`,
where `RUNNER_TEMP` selects an approved external directory. The reviewed
`requirements-ci.lock` pins the official PyYAML `6.0.3` source; the separate
`requirements-ci-build.lock` pins its builder wheels. This is the sole sourcebuild
exception while official CPython-3.15 wheels are unavailable. The helper checks
wheel metadata and hashes before installing into the selected interpreter;
see the [complete dependency-build contract](../security/ci-security-tooling.md#reviewed-python-315-ci-dependency-build)
for target guards, candidate versions, Framework version alignment and the
network-evidence boundary. Hosted CI uses the explicit guarded `--ci-toolcache`
mode; it does not replace the setup interpreter or change `GITHUB_PATH`.

### Current Parent workflow/job inventory

The closed inventory in [the Python workflow checker](../../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_ci/checks/common/check-python-version-contract.py)
contains 41 normal jobs, one candidate job, two immutable protected calls, one
local reusable caller and one reviewed system-Python namespace job. Normal jobs
select `.python-version` and verify the exact setup interpreter before Python
use. Unlisted jobs, dynamic executable heads, mutable Action references and
selector drift fail the contract.

| Workflow | Jobs | Interpreter contract |
| --- | --- | --- |
| `ci-findings-regressions.yml` | `nginx-b09-regression` | Canonical Python `3.15.1` |
| `ci-security-codeql.yml` | `trusted-go-version` | Canonical Python `3.15.1` |
| `ci-security-secrets.yml` | `advisory-full-history`, `pull-request-range` | Canonical Python `3.15.1` |
| `ci-security-workflow-lint.yml` | `actionlint`, `apr-util-provenance`, `zizmor` | Canonical Python `3.15.1` |
| `lint.yml` | `scaffold-lint` | Canonical Python `3.15.1` |
| `nginx-root-broker.yml` | `trusted-root-smoke` | Canonical Python `3.15.1` |
| `open-connectors-smoke.yml` | `open-connectors-smoke` | Canonical Python `3.15.1` |
| `protocol-contract.yml` | `nginx-profile-and-client-preflight`, `protocol-contract` | Canonical Python `3.15.1` |
| `quick-framework-check.yml` | `quick-check` | Canonical Python `3.15.1` |
| `reusable-five-connectors-profile.yml` | `aggregate`, `no-crs`, `resolve-profile` | Canonical Python `3.15.1` |
| `run-protected-nginx-root-broker.yml` | `prepare-manifests`, `verify-evidence` | Canonical Python `3.15.1` |
| `test-apache.yml` | `apache-autotools-bootstrap`, `apache-structure` | Canonical Python `3.15.1` |
| `test-common.yml` | `common-structure` | Canonical Python `3.15.1` |
| `test-connectors-with-crs-no-mrts.yml` | `aggregate-with-crs-no-mrts`, `connector-mode` | Canonical Python `3.15.1` |
| `test-envoy.yml` | `envoy-contract` | Canonical Python `3.15.1` |
| `test-full-smoke-sequential.yml` | `manual-heavy-runtime-validation` | Canonical Python `3.15.1` |
| `test-haproxy.yml` | `haproxy-structure` | Canonical Python `3.15.1` |
| `test-lighttpd.yml` | `lighttpd-contract` | Canonical Python `3.15.1` |
| `test-nginx-exact-head.yml` | `nginx-exact-head` | Canonical Python `3.15.1` |
| `test-nginx.yml` | `nginx-structure` | Canonical Python `3.15.1` |
| `test-traefik.yml` | `traefik-contract` | Canonical Python `3.15.1` |
| `update-go-version.yml` | `create-go-update-pr`, `resolve-go-release`, `validate-go-release` | Canonical Python `3.15.1` |
| `update-python-version.yml` | `publish-python-update`, `resolve-python-patch` | Canonical Python `3.15.1` |
| `update-submodules.yml` | `create-submodule-update-pr`, `validate-submodule-update` | Canonical Python `3.15.1` |
| `update-workflow-tools.yml` | `publisher`, `resolver`, `validator` | Canonical Python `3.15.1` |
| `verified-report-governance.yml` | `report-governance` | Canonical Python `3.15.1` |
| `update-python-version.yml` | `validate-python-patch` | Independently resolved exact stable `3.15.N` candidate; no downgrade |
| `run-protected-nginx-root-broker.yml` | `run-no-crs-broker`, `run-with-crs-broker` | Existing immutable protected reusable-workflow tuple |
| `all-connectors-no-crs.yml` | `no-crs` | Exact local `$/.github/workflows/reusable-five-connectors-profile.yml` caller; its fixed `./` equivalent is also accepted |
| `run-trusted-lighttpd-namespace-dispatch.yml` | `trusted-lighttpd-namespace` | Reviewed fixed `/usr/bin/python3` inside the cleared, unprivileged AppArmor namespace |

The namespace exception requires both its literal reviewed whole-workflow digest
and the complete dedicated trust validator. Adding setup/checkout before its
privileged bootstrap would cross its trust boundary. It is not a Python 3.15
qualification; any change requires a new profile review. Ordinary Action pins
are read from the central security-tool lock by both language checkers, keeping
SHA and provenance comments aligned when the constrained updater proposes a release.

### Safe stable-patch updater contract

The updater retains its separate candidate boundary. The checked-in
`.github/workflows/update-python-version.yml` has exactly four jobs:

| Job | Interpreter and trust boundary | Required behavior |
| --- | --- | --- |
| `resolve-python-patch` | Exact trusted event SHA and current canonical `.python-version`; `contents: read` | Calls only the fixed official structured Python release API `https://www.python.org/api/v2/downloads/release/?is_published=true` through HTTPS with exact host `www.python.org`, no redirects, `application/json`, bounded response handling, and schema validation. Its tested `--check --json` interface emits `status`, `current_version`, `latest_version`, and `update_available`; it proposes only a higher stable `3.15.N` patch. |
| `validate-python-patch` | Exact trusted event SHA and independently installed candidate; `contents: read` | Re-resolves the candidate with `--expected-version`, verifies the exact candidate interpreter, installs hash-locked CI dependencies, runs `pip check`, compile/contracts/focused tests, and `make check-ci-security-contract`; it performs no source or branch mutation. |
| `publish-python-update` | Canonical non-fork `master` event, current trusted `origin/master`; normal `GITHUB_TOKEN` has `contents: read` | The sole App-secret consumer mints the existing pinned GitHub App token with only `Contents: write` and `Pull requests: write`, rebuilds the maintenance branch from current master, and may create or update only the matching same-repository Draft PR. |
| `report-python-update-outcome` | Always runs; `permissions: {}` | Fails closed on inconsistent resolver/validator/publisher results and writes an English/German summary for either the current or independently validated/published result. |

The only triggers are the scheduled Monday run and a manual
`workflow_dispatch`; there is no push or pull-request trigger. The concurrency
group is `modsecurity-conector-python-version-maintenance-${{ github.repository }}`
with `cancel-in-progress: false`. Resolver, validator, and publisher each
require the exact canonical repository, non-fork event, literal `master`
default branch/ref, and schedule-or-manual event before checking out
`${{ github.sha }}` without submodules or persisted credentials.

`--check` resolves and validates a candidate without changing files. `--update`
is reserved for the publisher after the independent validation and expected-
version re-resolution succeed. Version syntax is owned by the tested updater,
not duplicated as workflow regexes. The publisher is not an updater for
arbitrary Python versions: it accepts only a resolver-validated stable
<code>3.15.N</code> patch, never a lower patch, prerelease, alternate minor
series, or unstructured/HTML release data.

The publisher uses the constant branch
`automation/update-python-315` and the stable title
`chore(ci): propose Python 3.15 patch update`, marker
`<!-- modsecurity-conector-python-315-updater -->`, and only the `python_version`
field in `ci/tooling/project-versions.lock.json` plus its `.python-version` view. It creates a Draft PR only when neither matching branch
nor PR exists. It reuses a branch only with exactly one matching same-
repository Draft PR whose title, marker, head/base, and disabled auto-merge
state all verify. After checking its historical scope, it rebuilds from current
`origin/master`, stages only `ci/tooling/project-versions.lock.json` and `.python-version`, and uses the exact
`--force-with-lease=refs/heads/$UPDATE_BRANCH:$EXPECTED_REMOTE_TIP` form for a
verified replacement branch. It never does an unconditional force push,
default-branch push, merge, or auto-merge.

Only the publisher reads `WORKFLOW_UPDATER_APP_CLIENT_ID` and
`WORKFLOW_UPDATER_APP_PRIVATE_KEY`; its normal job token remains read-only and
the App token never requests `Workflows`, `Actions`, or `Issues` write access.
The English/German PR body records the previous/proposed version, Python.org
metadata URL, validation run URL, Framework source SHA, only the `python_version` lock field and its `.python-version` view, retained Python 3.15 minor version, and manual review/
manual merge requirement.

The independent validation stage is the evidence boundary for a proposed
patch; it is not a claim that a scheduled run, candidate, pull request, or
merge has occurred. Those results require separately observed CI and delivery
evidence.

### Read-only Framework-submodule candidate validation

`update-submodules.yml` separates candidate validation from publication. Its
validator installs the same `build-essential apache2-dev libmodsecurity-dev`
prerequisites as the ordinary quick-check jobs after the Python interpreter
contract and before capturing the immutable source baseline. The selected Apache
lifecycle tests compile against real Apache/APR/ModSecurity headers and APR
libraries; their assertions require those prerequisites. Tools and headers are
then available through the existing read-only runtime mounts. The fixed
`APACHE_C_STANDARDS_OUT` points to `/external/build/apache-c-standards`, so the
Apache C17 check does not attempt its default output below the absent `/var`.
No additional host directory becomes visible or writable.

The publisher synchronizes its fixed component targets together with exactly
two derived companions: `config/testing/active-cases.json` and
`reports/testing/test-selection-archive.generated.json`. It admits the complete
inventory before mutation and includes both companions in the same rollback
transaction as the primary targets. Only existing source SHA fields and the
archive's `inventory_sha256` may change; existing archive `source_sha256` fields
may also follow proven changes to registered test sources. Case IDs, selectors,
profiles, source paths and archived definitions remain fixed. A separate
`--verify-companions --base` reconstruction from trusted master proves exact
primary and companion bytes before staging and again with `--staged` afterwards.
Changed companions must remain regular `100644` files with modification status
`M`. The existing one-updater-commit rule still governs reuse of an open update
branch: a manually repaired PR with an additional commit requires reviewed
integration before that branch can be reused automatically.

Its `validate-submodule-update` job creates a fresh `mktemp -d`
`/tmp/modsecurity-readonly-namespace.XXXXXX` direct child under sticky `/tmp`,
then makes that parent exactly `root:modsecurity-validator` mode `0750` before
passing it through the required `--namespace-parent` argument. The trusted
launcher rejects any other topology: the supplied parent must be an empty,
non-symlink direct child of root-owned sticky `/tmp` with that exact ownership
and mode. Trusted root-side setup then enters a private mount and PID
namespace. It makes mount propagation `rprivate` and creates a fresh private
`tmpfs` jail. It binds the Parent and Framework source tree (including `.git`)
non-recursively and read-only at `/source`, and binds only the exact validator
output child at `/external`; the latter is the only validator-writable
location. `/guard` is a root-owned, non-writable logical guard. The jail root
is remounted read-only after setup. It exposes only the read-only runtime
directories `/usr`, `/bin`, `/sbin`, `/lib`, `/lib64`, and only the exact
`actions/setup-python` runtime below
`/opt/hostedtoolcache/Python/<version>/<architecture>`, plus the minimal
required read-only `/etc` material. The launcher accepts only the resolved
non-symlink `<version>/x64` subtree and bind-mounts that exact subtree
read-only before candidate code starts. The hosted runner may manage the
source directory with permissive host permissions, but neither the host `/opt`
tree nor another host alias is exposed inside the jail. It mounts a
fresh read-only `proc`
filesystem at jailed `/proc` with `nosuid,nodev,noexec` and constructs a
private `/dev` containing only `null` and `urandom`.

Inside the already read-only `/usr` mount, the launcher resolves the fixed
`/usr/bin/gcc` and `/usr/bin/g++` paths and accepts their final targets only as
executable regular files still under that mount. It passes the resolved paths
to the candidate through the explicit `CC` and `CXX` environment variables.
`/etc/alternatives` is intentionally not exposed, so the candidate cannot
select a compiler through the host alternatives mechanism.

The trusted launcher enters that jail with `chroot` before executing candidate
code. It closes inherited descriptors other than standard input, output, and
error before dropping to `modsecurity-validator`, so pre-opened host directory
or file descriptors cannot bypass the path allowlist. Consequently the
candidate has no host-path alias for `/tmp`, `/var`, `/home`, `/root`, `/run`,
`/sys`, or `/dev/shm`; source and output are available only through `/source`
and `/external`. It is PID 1 of that namespace and its completion is handled
before the namespace lifecycle ends, guaranteeing no candidate stragglers.
Teardown uses neither lazy unmount nor `rmtree`: the helper removes only its
exact empty placeholders with non-recursive `rmdir`, and the workflow `EXIT`
trap likewise uses non-recursive `rmdir` for the trusted namespace parent.
Root-side host verification follows outside the candidate namespace.
The root workflow invokes the trusted launcher through `sudo -n python3`; the
launcher fail-closed sets `PR_SET_NO_NEW_PRIVS`, clears supplementary groups,
drops to the `modsecurity-validator` GID and UID, and uses `execve` with an
explicit fixed environment rather than an inherited runner environment. Within
the namespace the candidate applies `umask 077` before output and runs the
unchanged `make quick-check` as that dedicated, non-login, non-sudo identity.

After candidate data validation and before sandbox creation, the ordinary runner
prepares PyYAML with the unchanged trusted Parent dependency installer in guarded
`--ci-toolcache` mode. It passes
`--framework-lock modules/ModSecurity-test-Framework/requirements-ci.lock` to
validate the candidate lock as data and runs `python3 -m pip check`. Every source
and build-tool artifact remains hash-pinned. The selected runtime is then bound
read-only as before. Inside the jail, the original selected Python uses `-I` to
import the prepared pure-Python PyYAML without considering `PYTHONPATH`; a failed
import or unexpected LibYAML extension stops validation before `quick-check`.
No dependency installation or builder virtual environment is created in the
validator output tree. Its strict permission and escaping-link checks remain
unchanged.

The workflow prints captured namespace stdout on failure as well as success;
stderr remains visible directly. It preserves the original nonzero exit code
before examining the completion marker. A printed marker cannot turn a failed
candidate into success. Root-side source/output verification and both cleanup
paths still run according to their existing gates, so a future failure retains
its test/compiler diagnostics before temporary outputs are removed.

This replaces host-ancestor ACL handling: the candidate does not receive a
host-level traversal or read grant merely to reach `RUNNER_TEMP`. Parent,
Framework, and supported output are presented only through those namespace
views; root-side source inventory and root-side output verification constrain
legitimate output to the exact physical `--write-root`/`external` containment.
The validator retains its existing network access; dependency downloads occur
during trusted runner preparation. This change adds no network or egress
isolation. The jail is a filesystem and inherited-descriptor boundary,
not a claim of complete host or kernel isolation.

The host checkout is not a lock target. The historical root-owned checkout
mutation came from the former recursive `_lock_tree` calls in the root-side
preparer, not from the Framework Gitlink itself; its historical context is
[PR #301](https://github.com/Easton97-Jens/ModSecurity-conector/pull/301) and
merge commit `35c435483dcd637c7b9df0277bed34d6f94dc44d`. The preparer now
validates the path topology, source links, and Gitfiles, rejects every active
mount strictly below the host source root, validates the dedicated identity,
and records the original inventory before it creates any candidate output. It
does not call `chown` or `chmod` on Parent, Framework, `.git`, or
`.git/modules`; no ownership, group, mode, content, link, or Git metadata is
restored because none is changed. The namespace runner independently repeats
the nested-source-mount rejection before it creates the non-recursive source
bind, so a writable submount cannot be silently visible below the read-only
bind.

The inventory remains the fail-closed source-preservation proof. Every entry
records relative path, type, size, UID, GID, mode, and link count; regular
files additionally record SHA-256 and symbolic links record their link text.
The post-candidate inventory must match exactly before output validation. This
detects content, ownership, group, permission, link, and link-target changes
without causing any of them. The external-output check continues to reject
source hard links, escaping links, special objects, foreign ownership, and
unsafe modes.

Before any fallible prepare operation, the workflow creates a fresh
`$RUNNER_TEMP/modsecurity-readonly-validation.XXXXXX` guard as a direct,
non-symlink child with the fixed prefix, changes only that new guard to
`root:root` mode `0711`, and stores its exact path in step output. The helper
creates the root-owned mode-`0600` inventory and the validator-owned
mode-`0700` `external` child inside that guard. `sudo` is confined to identity
creation, private guard ownership/mode, root-side inventory prepare/verify,
namespace/chroot setup, and private cleanup; candidate-state validation and
both `git diff --check` operations run as the normal runner user.

An `if: always()` cleanup step invokes the helper's `--cleanup` mode even
after a candidate, inventory, namespace, parser, or contract failure. Before
removal it requires the exact absolute direct child of `RUNNER_TEMP`, the
fixed prefix, no symlink components, no overlap with Parent, Framework, or
Git metadata, and no active mount under the guard. It opens the trusted
temporary path one directory descriptor at a time and removes entries only
relative to checked descriptors without following symlinks. A cleanup failure
is visible and cannot turn a prior security failure into success.

This correction prevents future mutation; it deliberately does not repair an
already root-owned local or self-hosted checkout. Diagnose a concrete path
read-only first, for example:

~~~sh
find /path/to/ModSecurity-conector -xdev \
  \( -uid 0 -o -gid 0 \) -printf '%M %u:%g %p\n'
~~~

Confirm the intended checkout, expected local owner/group, mount topology, and
workspace policy before a user or administrator performs a deliberate,
path-specific manual repair. Do not use a blanket `chown -R`, `chmod -R`, ACL
reset, or `git clean -fdx`; the workflow never executes those operations.

Hosted run `31484727901` is historical failure evidence for the earlier ACL
precheck. Hosted run `31488072111` is also failure-only historical evidence: on
`5d7d7bbbbb968aa9755d3c0c67a09d8acd651c77`, resolver and sandbox preparation
succeeded, but the isolated quick check failed with five no-CRS normalization
errors at a runtime-directory traversal denial. The publisher was skipped. No
successful rerun, current-head scan, or delivery result is claimed for those
historical failures.

Local regression and static-contract evidence for this remediation is recorded
with the delivery work; this guide does not assign it a final count. It is not
a privileged hosted-mount or validator-identity runtime proof. A bounded
GitHub-hosted `workflow_dispatch` `validate_only` proof was observed in run
[`31776302498`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31776302498)
at exact head `c7bbc70bcf729d148a7d87f45ca352ae7247416b`: the validator
`make quick-check`, postverification, and enforcement succeeded. The publisher
was skipped and created no output pull request, commit, or branch. This does
not establish a SonarQube result, PR merge, or closure of `FND-PARENT-0122`,
which was closed by separately recorded exact-head and protected-master
evidence. It is not evidence for this newer source-preservation correction.

The manual `workflow_dispatch` input `validate_only: true` is a
non-publishing exact-ref proof/revalidation path with exactly two trusted
refs in the canonical non-fork Parent repository
`Easton97-Jens/ModSecurity-conector`: the reviewed repair branch
`fix/ci-enforce-readonly-submodule-validation` before merge for its exact-head
proof, and protected Parent `master` after that repair is merged for
resulting-master sandbox revalidation; the latter additionally requires GitHub
`github.ref_protected == true`. It is not a general facility to execute
arbitrary untrusted Parent refs or pull requests. Each allowed path checks out
its dispatch event's `github.sha` for resolution and validation,
forces the validator to run even when the resolved Framework candidate already
equals the dispatched Parent gitlink, and makes the publisher ineligible. It
cannot create or update a gitlink branch or pull request.

This is not an untrusted Parent pull-request/ref sandbox: at both allowed refs,
the Parent workflow and helper SHA are trusted before root-side setup, while
the Framework candidate remains untrusted code governed by the sandbox. Run
`31776302498` is bounded functional evidence only for
`c7bbc70bcf729d148a7d87f45ca352ae7247416b`; it is not evidence of SonarQube,
a PR merge, or finding closure. The two-ref allowlist is a guardrail; the
master path must also satisfy `github.ref_protected == true`. Neither condition
protects against a hostile same-repository writer absent branch protection or
environment approval.

The protected-master validation-only revalidation is not the authorized
post-merge Parent updater dispatch. That separate dispatch runs on `master`
with `validate_only` left false, validates the resolved Framework transition
from the trusted default branch, and may enter the constrained publisher only
after successful validation. Neither validation-only path grants publication
authority or substitutes for that post-merge updater dispatch.

This boundary is deliberately narrower than a general read-only job label: the
trusted root launcher constructs the candidate's fixed environment, with no
inherited runner environment or user site, and puts `HOME`, Git configuration,
pip cache, bytecode cache, build, log, and other cache roots below the writable
namespace view of the physical `external` directory. It sets
`PR_SET_NO_NEW_PRIVS` fail-closed before the identity drop, and the candidate
checks `NoNewPrivs: 1`. Trusted root-side setup verifies mount construction and
lifecycle; root-side host verification checks Parent and Framework source/Git
state and physical external output after the candidate namespace exits. The
validator cannot publish a gitlink or pull request. Production write permission
remains solely with the separate publisher job after successful validation; it
is not granted to the validator or to `make quick-check`.

Before the candidate starts, the root-side helper records a full source
inventory of the Parent and Framework source trees. Each entry captures its
path, type, size, mode, UID, GID, and link count; regular files also carry a
SHA-256 digest and symbolic links carry their link text. After `make quick-check`
the helper requires that inventory to match exactly, failing closed on any
source-tree mutation. It also fail-closed scans the validator's external tree:
validator-owned directories and regular files without group/other write
permissions are permitted. An external output symbolic link is permitted only
when it is validator-owned and its link text is nonempty, NUL-free, relative,
and lexically normalizes within the physical `external` root. The verifier does
not resolve, stat, or dereference that target. It rejects absolute targets,
including in-root absolute targets, lexical escapes to source, guard, or other
paths, special objects, and source-tree hard links.

This narrow output rule models only the contained-relative shape associated
with `checks/common.pem` in hosted run `31496603345`. The exact-head hosted
`validate_only` run `31776302498` completed the validator quick-check,
postverification, and enforcement successfully, but remains limited to that
run and head. It is not a SonarQube result, PR merge, delivery, or proof of
full host isolation. `FND-PARENT-0122` is a closed historical finding and this
documentation does not claim a new hosted result for the source-preservation
correction.

This describes the implemented workflow contract and its bounded local evidence,
not evidence of a hosted run, current-head security scan, published update, or
merge. Those results require separately observed execution evidence.

## Parent CI Go-toolchain contract

The central <code>ci/tooling/project-versions.lock.json</code> is the
version authority; the root <code>.go-version</code> is its generated Go CI
selector. It contains one exact stable numeric <code>MAJOR.MINOR.PATCH</code>
release, currently <code>1.27.3</code>. The trusted-base CodeQL selector
independently resolves the latest official stable release and its two Go jobs
use only the validated output:

~~~yaml
go-version: ${{ needs.trusted-go-version.outputs.version }}
check-latest: false
~~~

Module <code>go</code> directives remain separate compatibility contracts;
all four Go modules require the patched minimum <code>1.26.9</code>.
The component updater permits only the registered Envoy bundle:
<code>google.golang.org/grpc v1.83.2</code>,
<code>golang.org/x/net v0.61.0</code>,
<code>golang.org/x/sys v0.49.0</code>, and
<code>golang.org/x/text v0.43.0</code>. The latter two satisfy the selected
x/net release's requirements. Protobuf remains <code>v1.36.11</code>.
The original and previous registered baselines may advance independently;
x/net can be repaired when gRPC is already safe. Newer safe pins are preserved.
Other older versions, dependencies, paths, file modes, and unverified target
checksums are rejected. <code>--apply-requirements</code> atomically applies
only approved manifest upgrades before <code>go mod tidy</code>; the candidate
validator then checks exact manifest bytes and trusted checksum pairs.

<code>.github/workflows/update-go-version.yml</code> follows the same
three-stage trust boundary as the Python updater:

| Job | Toolchain and trust boundary | Required behavior |
| --- | --- | --- |
| <code>resolve-go-release</code> | Canonical <code>.go-version</code> and checked-in component policy; <code>contents: read</code> | Calls only the exact Go release endpoint <code>https://go.dev/dl/?mode=json</code>, rejects redirects and malformed or oversized metadata, accepts the greatest stable exact numeric <code>MAJOR.MINOR.PATCH</code> release, and resolves only the fixed Envoy component bundle. |
| <code>validate-go-release</code> | Independently resolved candidate checkout; <code>contents: read</code> | Re-resolves the candidate, runs the static contract and focused tests, creates the fixed component candidate only when approved, binds its <code>go.mod</code>/<code>go.sum</code> hashes, then validates every actual module with <code>GOTOOLCHAIN=local</code>, <code>go mod tidy -diff</code>, <code>go mod verify</code>, <code>go test -mod=readonly</code>, <code>go test -race -mod=readonly</code>, <code>go vet -mod=readonly</code>, and <code>go build -mod=readonly</code>. It cannot fall back to a downloaded Go toolchain, publish, or modify a remote branch. |
| <code>create-go-update-pr</code> | Canonical Python for the bounded updater; narrow publisher | Re-resolves with <code>--expected-version</code>, regenerates only the independently validated candidate, and may change only the Go field in <code>ci/tooling/project-versions.lock.json</code>, its generated <code>.go-version</code>, and/or <code>connectors/envoy/ext_proc/go.mod</code> plus <code>go.sum</code>. It rejects all other path, mode, and content hashes before it may create or safely update the repository-owned Draft PR on <code>automation/update-go-release</code>. It has only contents and pull-requests write permissions. |

The updater is Python because the bounded, offline-testable release parser is
checked-in Python. Each Go updater job therefore first uses the existing
<code>.python-version</code> and interpreter contract, preserving the
no-ambient-interpreter rule rather than adding a bootstrap exception.

### Automatic Go dependency updates

`.github/dependabot.yml` checks Go dependencies weekly in the four Parent modules:

| Module directory |
| --- |
| `/connectors/envoy/ext_proc` |
| `/connectors/traefik/response_observer` |
| `/connectors/traefik/native_middleware` |
| `/connectors/traefik/composite_middleware` |

Version proposals have a seven-day cooldown and a configured
`open-pull-requests-limit: 5`; no repository-wide PR cap is claimed.
Security updates do not inherit that cooldown. Existing Python updates
remain configured; Action updates stay with the dedicated workflow-tool updater.
Dependabot proposes changes to the module manifests and checksums for review and
CI validation. These settings take effect on the default branch; this task does
not merge dependency PRs or demonstrate a live bot publication.

The fixed `approved_minimums` in the Go updater are reviewed security floors,
not a latest-release feed. The resolver already preserves newer versions;
regressions cover future and mixed bundles without downgrading them. Updating
the four actual module dependencies above those floors is Dependabot's role.

### Candidate validation

<code>.github/workflows/validate-go-candidate.yml</code> validates the selected
PR head with read-only contents permissions, no credentials, and no publication
path. Its four-module matrix runs tidy, checksum verification, tests, vet,
build, and race tests with <code>GOTOOLCHAIN=local</code>. Native CGo builds
remain a separate connector check. The privileged updater continues to check
out only the trusted default branch and cannot publish after validation fails.
A successful default-branch dispatch requires separately observed evidence.


## Derived maintenance metadata and remaining prerequisites

Maintenance may derive exactly two companion files: `config/testing/active-cases.json` (existing SHA fields only) and `reports/testing/test-selection-archive.generated.json` (`inventory_sha256` only). Selectors, cases, profiles, source paths and subtest metadata cannot change through this mechanism. Trusted-base reconstruction must reproduce exact bytes and regular stage-0 mode `100644` before staging, publication or reuse. The primary Actions publisher allowlist is unchanged. Three focused regressions now pass: a future Go minor 1.28 is eligible, rollback preserves a foreign companion change, and rollback restores its own companion larger than 4 KiB.

Four `go.mod` declarations and `requirements-ci.lock`, `requirements-ci-build.lock`, `requirements-dev.txt` are seven non-executable dependency declarations, not collector source bindings. Go module/sum files and the three requirements remain bound by actual build identity and pre/post source snapshots. This avoids dependency-metadata churn without removing controller or executable-code bindings.

Sonar's job budget is now 120 minutes instead of 45 for the explicitly larger selection; individual 600-second limits and the one-second timing assertion remain unchanged. Observed profiles reduced 429 AST parses to 41 and 6841 source reads to a few hundred. The earlier 15.723 s measurement had nine concurrent workloads, whereas the later 1.788 s measurement was idle: these different conditions do not establish a controlled speedup.

After the user marked configuration complete, observed Dependabot secret metadata lists exactly one name: `SONAR_TOKEN`. The earlier zero-name/pending-secret state is historical and resolved at the metadata layer. No token value was read, and neither live bot authentication nor a successful Dependabot PR is claimed. That execution proof still requires separately authorized default-branch maintenance checks; current PR authentication is a separate result. [GitHub's Dependabot-on-Actions rules](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-on-actions) describe that separate secret context. No secret or provider setting is changed by this documentation.

## Compiler and linker variables

Use standard compiler environment variables only when the local toolchain
requires them. The root defaults are:

| Variable | Required | Root default | Example | Effect / safety |
|---|---:|---|---|---|
| <code>PYTHON</code> | no | <code>.venv/bin/python</code> if present, otherwise <code>python3</code> | <code>PYTHON=python3</code> | Selects the Python interpreter for scripts; use a trusted executable |
| <code>MSCONNECTOR_C_STD</code> | no | <code>c17</code> | <code>MSCONNECTOR_C_STD=c23</code> | Selects the Common helper C profile; unsupported optional profiles may be skipped |
| <code>MSCONNECTOR_CFLAGS</code> | no | <code>-std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror</code> | <code>MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"</code> | Flags passed to Common helper checks; preserve quoting |
| <code>CC</code>, <code>CXX</code> | no | shell/toolchain default | <code>CC=clang</code> | Selects trusted C/C++ compilers |
| <code>CPPFLAGS</code>, <code>CFLAGS</code>, <code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code> | no | no root default | <code>CFLAGS="-O2"</code> | Adds compile/link inputs; untrusted flags can change the build |
| <code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code>, <code>PATH</code> | no | shell default | <code>PKG_CONFIG_PATH="/srv/prefix/lib/pkgconfig"</code> | Changes tool/library discovery; restrict to trusted paths |

The <code>$(MSCONNECTOR_C_STD)</code> notation above is a Make-variable
reference, not a shell command. The Makefile resolves it before running a
recipe. Full formats, defaults, and Framework-forwarded source variables are
listed in [configuration variables](../reference/variables.md).

## Local C/C++ diagnostics

Integration level 1 provides a reproducible local C17/C++17 diagnostic
foundation. It is a source and contract check only: it neither prepares runtime
components nor downloads or installs tools, and it does not claim runtime,
production, CRS, or connector-release evidence.

### Tool prerequisites and blocked status

Run <code>make check-analysis-tools</code> before a diagnostic capture. It
prints the actual selected <code>CC</code>, <code>CXX</code>, <code>clangd</code>,
and Bear paths and versions. Run <code>make check-clang-analysis-tools</code>
before the advisory baseline; it independently reports the selected
<code>clang-tidy</code>, <code>clang</code>, and <code>clang++</code> tools.
Neither target installs, downloads, or prepares a substitute.

The advisory baseline requires a marked, writable <code>CODEX_TEMP_ROOT</code>
with its <code>tmp/</code> child, at least 5 GiB free space, and an external
C17/C++17 compilation database below that root. It refuses a relative,
checkout-internal, symlink-escaping, or otherwise unsafe CDB/output path before
creating output. Missing tools or prerequisites return exit code <code>77</code>;
invalid or unsafe parameters return exit code <code>2</code>; another non-zero
exit code means a technical analysis failure.

The baseline adds neither a <code>.clang-tidy</code> file nor a
<code>.clangd</code> file. It uses an explicit inline Tidy configuration,
does not apply <code>--fix</code>, <code>--fix-errors</code>,
<code>--fix-notes</code>, or <code>--export-fixes</code>, and does not add
<code>NOLINT</code> entries, sanitizer flags, production binary flags, a CI
gate, or a workflow change.

### Capture and C++17 evaluator targets

| Target | Required local input | Result and boundary |
|---|---|---|
| <code>make compile-db-nginx-c17</code> | Absolute external <code>COMPDB_OUTPUT</code>; existing NGINX and libmodsecurity headers | Bear captures the direct <code>check-nginx-c17</code> compiler process. It covers the NGINX and Common sources declared in <code>connectors/nginx/config</code>, including <code>common/src/late_intervention.c</code>. |
| <code>make check-targeted-evaluator-cpp17</code> | Absolute external <code>CPP_BUILD_ROOT</code>, <code>MODSECURITY_INCLUDE_DIR</code>, and <code>MODSECURITY_LIB_DIR</code>; optional absolute <code>MODSECURITY_LIB_FILE</code> | Compiles only <code>common/scripts/modsecurity_targeted_eval.cc</code> with <code>-std=c++17 -Wall -Wextra -Werror</code>. The local binary is not executed and is not a production artifact. |
| <code>make compile-db-cpp17</code> | The same C++17 inputs plus the same external <code>COMPDB_OUTPUT</code> | Bear captures the real evaluator compiler process and atomically merges its C++17 entry with a valid existing database. It never invents a compiler command. |
| <code>make check-clangd-c17</code> | A merged external <code>COMPDB_OUTPUT</code> containing NGINX, Common, and evaluator entries | Validates the database and checks one representative NGINX, Common, and C++17 translation unit with <code>clangd --check</code>. It applies no fixes and disables configuration, background indexing, Clang-Tidy, and clangd tweaks. |

### Advisory Clang analysis baseline

| Target | Required local input | Result and boundary |
|---|---|---|
| <code>make check-clang-analysis-tools</code> | Trusted <code>clang-tidy</code>, <code>clang</code>, and <code>clang++</code> on <code>PATH</code>, or the corresponding executable overrides | Reports the selected versions without creating analysis output. A missing tool returns <code>77</code>. |
| <code>make clang-tidy-baseline</code> | Absolute <code>COMPDB_OUTPUT</code> and absolute <code>ANALYSIS_OUTPUT</code>, both below the marked <code>CODEX_TEMP_ROOT</code> | Runs <code>clang-tidy</code> for every validated C17/C++17 translation unit using the explicit <code>-*,bugprone-*,cert-*</code> profile. Writes raw logs and <code>clang-tidy-baseline.json</code> only below <code>ANALYSIS_OUTPUT</code>. |
| <code>make clang-analyzer-baseline</code> | The same safe CDB/output paths | Replaces CDB compiler drivers with <code>clang</code> or <code>clang++</code>, strips output-writing arguments, and runs direct <code>clang --analyze</code> with the <code>core,unix,security,cplusplus,deadcode</code> profile and owned SARIF output. Writes <code>clang-analyzer-baseline.json</code>. It does not require <code>scan-build</code>. |
| <code>make clang-analysis-baseline</code> | The same safe CDB/output paths | Runs both advisory paths and writes one normalized <code>clang-analysis-baseline.json</code> plus run-scoped raw logs below <code>ANALYSIS_OUTPUT</code>. |

The runner validates that CDB entries name unique, tracked repository C/C++
sources with the required C17/C++17 flag before it writes any result. It stages
a sanitized compilation database and removes only that runner-owned staging
child after the invocation; it never recursively removes a caller-supplied
<code>ANALYSIS_OUTPUT</code>. It snapshots the CDB, analyzed source content, and
working-tree status before and after each run. A changed snapshot is a technical
failure, while pre-existing independent worktree changes are allowed to remain
unchanged.

The normalized JSON always contains the CDB SHA-256, tool paths and versions,
requested and active Tidy checks, the direct static-analyzer route, translation
unit counts, raw-artifact references, findings, technical failures, read-only
verification, and zero-inclusive classification totals. A technically complete
baseline exits <code>0</code> even when findings are present. The only
classification values are:

~~~text
confirmed_bug
needs_validation
possible_security_candidate
false_positive
third_party_header
intentional_pattern
out_of_scope
~~~

Tool diagnostics are triage input, not automatic proof. Repository diagnostics
normally start as <code>needs_validation</code>; CERT/security-oriented checks
may be <code>possible_security_candidate</code>; external headers are
<code>third_party_header</code>; and external non-header locations are
<code>out_of_scope</code>. The baseline never automatically labels a finding a
confirmed bug, false positive, or intentional pattern. A
<code>possible_security_candidate</code> is explicitly unconfirmed and needs
separate Codex Security validation before any security conclusion or source
change.

Every capture filters generated probes and external copied sources, retains only
tracked checkout translation units, validates C17/C++17 and
<code>-Wall -Wextra -Werror</code>, deduplicates by translation unit, and
publishes with an atomic replacement. A failed capture or validation leaves an
existing <code>COMPDB_OUTPUT</code> unchanged. The output path and every
captured compiler output must be absolute and outside the checkout.

Use an external analysis root rather than the checked-out local
<code>compile_commands.json</code>; the root filename and
<code>/.cache/clangd/</code> are intentionally ignored by Git. For a complete
C17/C++17 database, capture NGINX first and then merge C++17 into the same file:

~~~sh
make check-analysis-tools
make compile-db-nginx-c17 COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json"
make check-targeted-evaluator-cpp17 \
  CPP_BUILD_ROOT="/abs/build/cpp-evaluator" \
  MODSECURITY_INCLUDE_DIR="/abs/libmodsecurity/include" \
  MODSECURITY_LIB_DIR="/abs/libmodsecurity/lib"
make compile-db-cpp17 \
  COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json" \
  CPP_BUILD_ROOT="/abs/build/cpp-evaluator-cdb" \
  MODSECURITY_INCLUDE_DIR="/abs/libmodsecurity/include" \
  MODSECURITY_LIB_DIR="/abs/libmodsecurity/lib"
make check-clangd-c17 COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json"
~~~

<code>compile-db-cpp17</code> preserves valid NGINX rows and replaces only a
matching evaluator row, so it can also run before the NGINX capture. A
database containing only one language is still valid for its capture target,
but <code>check-clangd-c17</code> fails clearly until both required coverage
sets are present.

Use a marked external Codex temporary root for the advisory paths. The CDB is
an input from the capture steps above; the baseline does not recapture or edit
it:

~~~sh
export CODEX_TEMP_ROOT="/abs/marked-codex-temp-root"
export TMPDIR="$CODEX_TEMP_ROOT/tmp"
export ANALYSIS_ROOT="$CODEX_TEMP_ROOT/analysis"
export COMPDB_OUTPUT="$ANALYSIS_ROOT/final-cpp-diagnostics/compile_commands.json"

make check-clang-analysis-tools

make clang-tidy-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/tidy"

make clang-analyzer-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/analyzer"

make clang-analysis-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/combined"
~~~

This first level has no Apache, HAProxy, Envoy, Traefik, or lighttpd compilation
database coverage. It does not execute connector traffic, inspect runtime
artifacts, modify product source, alter the Framework or its submodule, or
establish any production or runtime release.

## Cache and source provisioning

<code>CACHE_ROOT</code> defaults to
<code>VERIFIED_RUN_ROOT/cache-v2</code>, and
<code>CONNECTOR_COMPONENT_CACHE</code> defaults to its <code>shared</code>
child. Both are absolute cache paths once derived. The cache is reusable input,
not canonical evidence.

For an isolated invocation, choose a parent before preparation:

~~~sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
~~~

<code>VERIFIED_RUN_PARENT</code> is optional; the root chooses
<code>RUNNER_TEMP</code>, then <code>TMPDIR</code>, then the documented
<code>&lt;system-temporary-root&gt;</code> fallback when it is empty.
<code>&lt;system-temporary-root&gt;</code> denotes the runtime's system
temporary fallback; it is a documentation placeholder and does not change the
checked-in runtime default. The example is a recommended local value, not a
repository default. Set <code>SKIP_RUNTIME_COMPONENT_PREPARE=1</code> only when a valid
invocation-local snapshot and compatible cache already exist. It does not mean
“skip missing dependencies.”

Advanced source/provenance values such as <code>HAPROXY_SOURCE_URL</code>,
<code>HTTPD_SHA256</code>, <code>NGINX_SOURCE_GIT_REF</code>, and
<code>MODSECURITY_V3_GIT_REF</code> are Framework-forwarded. URLs, revisions,
checksums, and source paths change provisioning identity and may cause
rebuilds. They do not change a connector capability or promote an outcome.

### Five-connector No-CRS baseline layout

The visible <code>all-connectors-no-crs.yml</code> caller is limited to its
scheduled or repository-authorized manual dispatch path. It delegates only the
hard-coded <code>no-crs</code> input to
<code>reusable-five-connectors-profile.yml</code>. Both workflows use
read-only repository permissions and have no pull-request trigger.

The reusable profile has one closed, authoritative connector map: Apache,
HAProxy, Envoy, Traefik, and lighttpd. A profile value or connector row that is
not in that map is rejected before it can produce profile evidence. NGINX is
not part of this baseline and this workflow makes no NGINX result claim.
Each invocation uses private sibling <code>build</code>, <code>evidence</code>,
<code>runs</code>, <code>run-logs</code>, and <code>cache-v2</code> roots below
<code>$RUNNER_TEMP/ModSecurity-conector-verified</code>. Mutable build, cache,
and logs are consequently outside the canonical evidence root.

For each selected connector, the finalizer records its existing scoped result
and a profile receipt bound to the profile, connector, run ID, Parent commit,
Framework commit, and cleanup disposition. The aggregate accepts exactly one
valid result and receipt for each of the five names. This is an evidence
contract, not a statement that a hosted runtime run has passed.

#### Capability audit and future-profile extension contract

The <code>no-crs</code> profile selects the existing HTTP/1.1 routes and their
declared integration/Phase-4 boundaries: Apache
<code>native-httpd-module</code>, HAProxy <code>spoe-spop-agent</code>, Envoy
<code>http-ext-authz-service</code>, Traefik
<code>http-forwardauth-service</code>, and lighttpd
<code>native-lighttpd-plugin</code>. These selections do not claim CRS, MRTS,
production readiness, a complete connector matrix, HTTP/2, HTTP/3, or
unobserved response behavior.

A future profile must add an explicit closed map and matching validation for
its connector set, capability fields, receipt schema, aggregation expectations,
tests, and English/German documentation. It must fail closed for unknown
profiles and unsupported rows. It cannot obtain CRS, MRTS, or full-lifecycle
coverage merely by reusing this No-CRS workflow.

## Selected build routes

| Connector | Build target | Selected full-lifecycle profile | Build/integration note |
|---|---|---|---|
| Apache | <code>build-apache</code> | <code>native-httpd-module</code> | Native httpd module route; APXS and host inputs are provisioned/checked separately |
| NGINX | <code>build-nginx</code> | <code>native-nginx-http-module</code> | Native NGINX HTTP module route; module, prefix, and worker paths remain host-specific |
| HAProxy | <code>build-haproxy</code> | <code>native-htx-filter</code> | Native HTX filter route; source/build presence is not a response-body claim |
| Envoy | <code>build-envoy</code> | <code>ext_proc</code> | Streamed external-processing route; an alternate ext_authz helper is not silently the selected route |
| Traefik | <code>build-traefik</code> | <code>native-middleware</code> | Native middleware route with a local UDS service; forwardAuth compatibility helpers remain distinct |
| lighttpd | <code>build-lighttpd</code> | <code>patched-native</code> | Patched native host/module route; patch/build success is not full-lifecycle proof |

The profile values are supplied by full-lifecycle targets. Do not set
<code>FULL_LIFECYCLE_HOST_PROFILE</code> manually to relabel a direct or
compatibility build.

## Troubleshooting

| Symptom | Meaning | Safe next action |
|---|---|---|
| <code>BLOCKED: FRAMEWORK_ROOT is missing</code> / exit <code>77</code> | The submodule/Framework path is unavailable | Initialize the submodule or set <code>FRAMEWORK_ROOT</code> to a trusted existing Framework checkout |
| Build root rejected | Output is inside the checkout or otherwise unsafe | Set <code>BUILD_ROOT</code> or <code>VERIFIED_RUN_PARENT</code> to an absolute external writable path |
| Component preparation missing | Cache/snapshot is absent or preparation was skipped | Run <code>make prepare-runtime-components</code> without the skip flag |
| Compiler profile skipped | Optional C profile is unavailable | Use the documented default C17 check or install a compiler that supports the optional profile |
| Config check fails | Build, host configuration, or input file is invalid | Run the matching build target, review the sanitized log, and verify its documented variables |

Do not paste raw logs containing cookies, authorization headers, TLS private
keys, or other sensitive values into issues or canonical evidence.
