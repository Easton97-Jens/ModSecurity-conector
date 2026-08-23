# Change Record

**Language:** English | [Deutsch](CR-20260822-trusted-lighttpd-namespace-dispatch.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260822-trusted-lighttpd-namespace-dispatch |
| Date (UTC) | 2026-08-22 |
| Base revision | `423abcc130cf5d29ccf15dd7d82e4e7d89d495d3` |
| Delivery status | Separate protected-master dispatcher repair pull request; normal master refresh and manual integration are authorized, while exact-head validation, integration, and trusted runtime success remain pending at this record update. |

## Motivation and problem statement

The Lighttpd same-UID TOCTOU remediation needs a real unprivileged
user/mount/PID-namespace runtime test. GitHub-hosted pull-request runners
correctly fail closed when Ubuntu's AppArmor user-namespace restriction blocks
that test. Putting `sudo` or an AppArmor setup step in the pull-request
workflow would be unsafe because the workflow YAML is supplied by the PR.

This separate, manually dispatched workflow must first be reviewed and merged
to protected `master`. It supplies the short-lived Ubuntu-24.04 setup without
giving a PR-controlled workflow a privileged step.

## 2026-08-22 master-integration authorization

The current user expressly authorized PR #320 only to be brought to current
`master` and integrated. The branch refresh uses a normal merge of current
`origin/master`; it does not authorize a rebase, force-push, direct push to
`master`, auto-merge, protection bypass, PR #309 merge, Framework/MRTS change,
or Gitlink update. A manual repository-conventional merge remains conditional
on fresh exact-head checks, SonarQube Cloud, and the protected ruleset.

## Acceptance criteria

- The dispatcher has only `workflow_dispatch`, one `target` input, a
  protected-`master`/canonical-repository gate, and an exact owner-maintainer
  actor gate.
- The PR-code test job has only `contents: read`; a separate no-checkout
  reporter has only `statuses: write`, receives no PR source or artifact, and
  can write only the fixed `trusted-lighttpd-namespace` status for the
  API-bound target SHA.
- Fixed pre-checkout system steps install only fixed packages, load the fixed
  AppArmor user-namespace profile, make `ns-test`, and verify binary, group,
  Docker-socket, and capability preconditions.
- API resolution accepts an open canonical PR number or that PR's exact
  40-character lowercase head SHA; the constrained process materializes only
  that resolved SHA from the fixed public HTTPS origin.
- Git credentials and `.git` are removed before source execution. Source runs
  only as `ns-test`, with `NoNewPrivs`, empty groups/capabilities, `env -i`, a
  private `0700` temporary root, and fail-closed namespace probes.

## Implementation decision and rationale

`run-trusted-lighttpd-namespace-dispatch.yml` is a protected-default-branch
control-plane workflow, not a pull-request trigger. It requires both
`github.actor == 'Easton97-Jens'` and
`github.triggering_actor == 'Easton97-Jens'`, so only the canonical repository
owner can manually invoke or re-run this first version. Adding another maintainer requires a
separately reviewed protected-master allowlist change.

Before source materialization, fixed absolute root-owned binaries install only
`apparmor-utils`, `bubblewrap`, and `jq`, confirm Bubblewrap's required flags,
keep `kernel.apparmor_restrict_unprivileged_userns` at `1`, and load this fixed
root-owned profile:

~~~text
profile trusted-lighttpd-ci-userns flags=(unconfined) {
  userns,
}
~~~

It adds no AppArmor capability, mount, ptrace, network, wildcard-file, or
profile-transition rule and makes no global sysctl change. It is not presented
as the sandbox; the actual boundary is the fresh `ns-test` identity,
`NoNewPrivs`, zero capability sets, cleared environment, inaccessible Docker
socket, and the nested private namespace/Bubblewrap probes.

The previous `aa-status --profiled | grep <profile>` assertion was removed:
on Ubuntu 24.04, `--profiled` reports a count of loaded profiles rather than
their names. Immediately after `apparmor_parser --replace`, fixed root-owned
`aa-exec` enters `trusted-lighttpd-ci-userns` and checks
`/proc/self/attr/current`. A different or absent profile exits `77` before
source materialization. The static contract forbids the old count-based form and mutates the
active-profile proof, the reporter isolation, and the privilege inventory.

## 2026-08-23 constrained preflight diagnostic repair

The first protected-master dispatch after the initial correction bound the
exact PR #309 SHA and completed bootstrap, checkout, and Git-state removal,
but exited after 42 ms in an unlabeled predicate inside the post-drop
`aa-exec -> setpriv -> env -i` process. That observation does not establish a
Lighttpd runtime failure and does not justify a fallback.

The repaired protected workflow runs the same fully constrained launcher before
checkout, without consuming a checkout or PR-derived path. It verifies real
and effective UID/GID, empty supplemental groups, `NoNewPrivs`, all five
capability sets, the active AppArmor profile, Docker-socket inaccessibility,
and the user/mount/PID plus Bubblewrap namespace probes. Every prerequisite
failure is converted to a fixed `BLOCKED: preflight.<reason>` label with no
helper stderr or PR data. The post-checkout launcher preserves the same
controls and emits matching `BLOCKED: runtime.<reason>` labels for its setup
and namespace predicates; the actual Python unittest remains unmasked so a
real fixture failure stays observable. Both namespace probes are still
fail-closed, and neither has a root, container, or out-of-namespace fallback.

This record update documents a diagnostic/control-equivalence repair only. It
does not claim a successful trusted runtime run; that evidence must come from
a fresh `master` dispatch against the then-current exact PR #309 head.

The trusted source path is:

~~~text
manual target -> strict format validation -> fixed public GitHub API request
-> one open canonical PR/head SHA -> aa-exec -> setpriv -> env -i
-> fixed HTTPS exact-SHA materialization -> verify -> remove .git
-> ns-test namespace test
~~~

No raw or unvalidated PR-derived text, path, ref, URL, or shell syntax enters a
privileged command; the already API-bound exact SHA is passed only as validated
data. The raw input is never a checkout ref. The PR source is materialized
directly only after the identity drop.
The disposable GitHub-hosted VM owns the final account/profile/temp teardown;
there is deliberately no root-side recursive deletion of an `ns-test`-writable
tree after PR code has run.

The pre-checkout bootstrap creates its per-run state only beneath the
prevalidated root-owned, non-writable `/var/lib` parent. It deliberately does
not use `/var/tmp`, whose standard `1777` mode is both incompatible with the
trusted-directory invariant and unsuitable as the parent of a privileged
runtime root. The dispatcher verifies the exact root-owned `0755` state root
and the exact non-root `source`/private `0700` temporary children before
checkout or PR-code execution.

The test job exposes only its API-validated `target_sha` output. A fresh
GitHub-hosted reporter VM runs after it with no checkout, no local action, no
cache, no artifact, no `sudo`, and no PR-code execution. It revalidates the
lowercase 40-character SHA, maps only the trusted test result to a fixed
`success`/`failure`/`error` value, and posts the fixed status context
`trusted-lighttpd-namespace`. The status token exists only in that reporter;
the test job never receives it.

## 2026-08-23 direct constrained source-materialization and mount-lifecycle repair

Run `32614114266` proved the complete privileged bootstrap, API binding, exact
target validation, `aa-exec -> setpriv -> env -i` identity boundary, and both
namespace probes. It then failed closed with `BLOCKED: runtime.source_root`
before a Lighttpd unittest began: the constrained `ns-test` process could not
traverse the prior runner-workspace checkout. The run does not prove which
workspace ancestor caused the visibility failure, and it is not a Lighttpd
test failure.

The repair removes the runner-workspace handoff entirely. The protected
bootstrap creates a root-owned `0755` parent, an empty root-owned Git template,
and two root-owned fixed helpers under
`/var/lib/trusted-lighttpd-namespace`; it gives only the fixed `source` and
`tmp` children, both `0700`, to `ns-test`. The source-namespace helper receives
only the already API-bound SHA and the fixed `ns-test` numeric identity through
a cleaned environment; its source path, Git template, and public HTTPS origin
are literals in trusted master-controlled text.

A follow-up security review rejected the earlier plan to mount the tmpfs after
`--map-current-user`: after that non-root `exec`, Linux recalculates capability
sets and the mount cannot safely proceed. The trusted helper now validates the
empty fixed source and temporary underlays before any source exists, records
the host namespace IDs, then creates a private mount/PID namespace as root and
explicitly makes mount propagation private. It mounts a bounded `256m` source
tmpfs and a separate bounded `128m` temporary tmpfs, both
`nosuid,nodev,noexec`. It has not fetched, read, copied, parsed, or executed PR
source at this point.

Only after that blank private mount exists, `setpriv --reuid/--regid` clears
supplementary groups, sets `NoNewPrivs`, and removes inheritable, ambient, and
bounding capabilities. A clean `env -i` then enters a same-identity nested
user/mount/PID namespace. The inner `unshare --keep-caps` is permitted only as
the short, fixed transition to the root-owned system `/usr/bin/setpriv` binary:
that finalizer repeats the non-root identity, group, `NoNewPrivs`, inheritable,
ambient, and bounding-set drops before it executes the root-owned source-runner
script as `ns-test`. It never executes PR code while those namespace-local
capabilities exist. The source runner proves its real non-root UID/GID, all
five empty capability sets, `NoNewPrivs`, AppArmor label, Docker-socket
isolation, distinct user/mount/PID namespaces, PID 1, and both private tmpfs
mounts before it materializes Git. It then uses only absolute root-verified
binaries and a bounded Git launcher to initialize the private mount with the empty template, fetch only
the exact SHA (`--no-tags --depth=1 --no-recurse-submodules`), verify the
commit/object and `HEAD`, delete `.git`, reject checkout symlinks, and run the
namespace unittest.

The materialization environment is created by `env -i`: HTTPS is the only
allowed Git protocol; prompts, LFS smudging, global/system configuration,
hooks, credential helpers, file protocol, and filesystem monitoring are
disabled. No token, workspace path, branch/ref, URL, or Git configuration is
accepted from the PR. The private source and test-temporary mounts are released
with their `--kill-child`-bound namespace on normal completion or controlled
parent termination. After Python returns, the constrained runner also verifies
that the private temporary root is empty. The host performs only a
non-destructive absence check for both mounts; it never resolves a
same-UID-writable path for cleanup. This replaces the reviewed unsafe
`find ... -delete` pattern; root never reads, copies, parses, or recursively
deletes PR source or test-temporary data.

This change does not weaken a namespace, AppArmor, capability, token, or
failure gate. It changes neither Framework nor MRTS source, a Gitlink,
dependency, toolchain, action pin, repository setting, ordinary PR workflow,
or PR #309's Draft state. Hosted exact-head runtime and Sonar evidence remain
pending until this separately reviewed master repair is merged and dispatched.

## 2026-08-23 bounded public API binding retry

Run `32619161990` completed the constrained bootstrap and failed before source
materialization when the fixed anonymous GitHub API request for the exact
commit returned HTTP `504`. That result remains fail-closed, but the former
`--retry 0` policy made a transient control-plane outage indistinguishable from
a durable binding failure.

Only the idempotent, fixed-HTTPS GET helper now uses bounded curl retry
settings: three retries, a one-second retry delay, and a 30-second retry
window. Curl's normal transient-error policy covers HTTP `504`; it does not
use `--retry-all-errors`. The resolver still has no token, accepts only the
strictly formatted target, validates the API response, and fails before any PR
source exists if its retries are exhausted. The separate status-writing POST
retains `--retry 0` so a side-effecting status request is not replayed.

## 2026-08-23 user-namespace CapBnd finalizer repair

Protected-master dispatch `32620696697` passed the trusted bootstrap and exact
anonymous PR binding for PR #309 head
`316a5de1ac5e663fce3cce58428f1e1dd306e573`, then failed closed before any PR
source materialization with `BLOCKED: runtime.capability_CapBnd`. The earlier
outer `--bounding-set=-all` correctly cleared host-namespace capability
bounding state, but entry into the nested same-identity user namespace creates
a new namespace-local bounding set. The direct `unshare -> dash` transition
therefore could not make the source runner's all-five-mask precondition true.

The repair confirms `unshare` supports `--keep-caps` during trusted bootstrap
and uses that option exactly once on the inner same-identity `unshare`. It
immediately invokes the fixed, root-owned `/usr/bin/setpriv` system binary,
which repeats `--reuid`, `--regid`, `--no-new-privs`, `--inh-caps=-all`,
`--ambient-caps=-all`, and `--bounding-set=-all` before the final non-root
`dash` exec. The outer trusted drop clears supplementary groups before this
mapping; the inner finalizer deliberately preserves only that already-checked
single primary group without issuing a later `setgroups(2)`. The source runner retains its independent
`CapInh`, `CapPrm`, `CapEff`, `CapBnd`, and `CapAmb` zero checks before it may
perform any Git, filesystem, or Python operation. Thus `--keep-caps` is not a
capability grant to PR code; it is only the minimal trusted transition required
to discard the user-namespace-local bounding set. Missing support or any
failed finalizer or source-runner check remains fail-closed.

The static contract allows no second or relocated `--keep-caps`, requires the
complete immediate finalizer sequence, and mutates removal of every finalizer
drop, the finalizer itself, and the inner capability retention. Hosted
Ubuntu-24.04 execution against the then-current exact PR #309 head remains the
authoritative confirmation of this repair.

### CapBnd repair local validation

- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v tests.test_trusted_lighttpd_namespace_dispatch_workflow` — passed (`2` tests, including the new finalizer weakening mutations).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v tests.test_ci_security_workflows` — passed (`28` tests).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace` in the exact local PR #309 head worktree `316a5de1ac5e663fce3cce58428f1e1dd306e573` — passed (`18` tests; `10` expected skips outside the trusted integration gate).
- Python `compileall`, `actionlint` with ShellCheck, offline `zizmor`, and `git diff --check` — passed.

## 2026-08-23 user-namespace setgroups finalizer repair

Protected-master dispatch `32622549590` reached the trusted bootstrap and the
exact anonymous binding of PR #309 head
`a599ccb2fe3256500e59aef3d0f7d578a079cd7a`, then failed closed before source
materialization with `setpriv: setgroups failed: Operation not permitted`.
`unshare --map-current-user` necessarily implies `--setgroups=deny`, so the
inner CapBnd finalizer cannot safely use `--clear-groups` after that mapping.

The outer trusted finalizer already performs `--clear-groups` while it may do
so, and the freshly created `ns-test` account is independently required to have
only its primary group. The inner finalizer now uses `--keep-groups` solely to
retain that already-cleared state while it repeats identity, `NoNewPrivs`, and
the inheritable, ambient, and bounding capability drops. The final source
runner independently requires its real/effective UID and GID and its complete
group list to equal the `ns-test` IDs before any Git, filesystem, or Python
operation. This avoids a denied `setgroups(2)` call without adding a group,
capability, source path, or fallback.

The static contract permits exactly two outer `--clear-groups` drops and exactly
one inner `--keep-groups` occurrence inside the fixed finalizer sequence. Its
mutations reject a restored inner clear operation or any attempt to set another
group. The next protected Ubuntu-24.04 exact-head dispatch remains the
authoritative runtime proof.

### Local validation

- `rtk test python3 -m unittest -v tests.test_trusted_lighttpd_namespace_dispatch_workflow` — passed (`2` tests, including the weakening mutations).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v tests.test_ci_security_workflows` — passed (`28` tests).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace` in the clean PR #309 worktree — passed (`18` tests; `10` expected skips without the trusted integration gate).
- `actionlint` with ShellCheck, offline `zizmor`, Python `compileall`, the bilingual-documentation suite, and `git diff --check` — passed.

## 2026-08-23 dual UID/GID map repair

Protected-master dispatch `32626930531` used master
`6501aea5070a99636ba3b56d9f7e77e1c55a641a`, bound the then-current exact
Draft PR #309 head `bdc054c74fd8dfd01a6b7bf3ccfe89af9a60fe76`, and completed
the trusted bootstrap and canonical target binding. It failed closed before
the namespace helper forked: the bounded phases contained
`caller-identity-validated` but not `trusted-binaries-validated`, followed by
`trusted namespace binary validation failed`.

The failure is not a missing runner capability and is not permission to relax
the strict ownership guard. The previous source namespace mapped only the
non-root `ns-test` identity via `--map-current-user` and `--map-group`. Linux
reports file ownership through the caller's user namespace, so host UID/GID
`0` appeared as an unmapped overflow owner in that process. The existing
helper correctly rejected the fixed root-owned `/usr` binaries before it could
fork the real fixture lifecycle.

The protected-master helper now creates exactly two explicit map entries for
each identity class before any PR source exists: inner UID/GID `0` maps to host
UID/GID `0`, and inner UID/GID `NS_TEST_UID`/`NS_TEST_GID` maps to the same
host identity. It verifies both exact entries and an exact count of two lines
from the trusted setup process and again from the final constrained source
runner. The workflow checks that its installed `unshare` supports
`--map-users`, `--map-groups`, `--setgroups`, and `--keep-caps`; it then uses
only `--setgroups allow` while trusted root code creates the private mounts.

The namespace still becomes private before the source and temporary `tmpfs`
mounts are created. The fixed root-controlled `setpriv` transition then
clears supplementary groups, sets `NoNewPrivs`, and clears inheritable,
ambient, and bounding capability sets before `env -i` directly starts the
root-owned source runner as `ns-test`. PR code does not run while capabilities
exist. The old same-identity mapper and its `--keep-groups` finalizer are no
longer present; accepting overflow ownership, a container/sudo fallback, or a
skip-to-success path remains prohibited.

The static contract now requires the exact four map arguments, the six
runtime map attestations, map-count guards, the mapping-to-privilege-drop
order, and the absence of every legacy mapper. Its representative mutations
cover altered root/non-root UID and GID maps, map-count weakening,
`--setgroups deny`, restored `--map-current-user`, capability retention, group
retention, and removed privilege drops.

### Current local validation

- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v tests.test_trusted_lighttpd_namespace_dispatch_workflow tests.test_ci_security_workflows` — passed (`30` tests).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace` in the exact local PR #309 worktree — passed (`20` tests; `10` expected capability-gated skips outside the trusted runner).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m compileall -q tests/test_trusted_lighttpd_namespace_dispatch_workflow.py tests/test_ci_security_workflows.py` — passed.
- YAML parsing, ShellCheck of both fixed generated `dash` helpers, `actionlint` with ShellCheck, offline `zizmor`, and `git diff --check` were run; all passed. Offline `zizmor` reported no findings and retained three existing suppressions.

The local container rejects writing a user-namespace map with `Operation not
permitted`, so it cannot prove the hosted kernel behavior. This is not a
fallback condition. The authoritative next step remains a separate reviewed
and normally integrated protected-master workflow PR, followed by a manual
`master` dispatch using the freshly re-resolved full PR #309 head SHA. PR #309
remains open and Draft; no merge or Ready-for-review transition is asserted.

## Changed files

- `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` — protected
  manual Ubuntu-24.04 dispatcher, API-bound direct constrained source
  materialization in a private mount lifecycle, and restricted `ns-test`
  execution.
- `tests/test_trusted_lighttpd_namespace_dispatch_workflow.py` — positive and
  mutation contracts for the trust boundary, active-profile proof, direct Git
  materialization, private mount teardown, and isolated status reporter.
- This English/German Change Record pair — authorization, invocation,
  validation, and explicit pending-runtime status.

The existing pull-request workflow receives no `sudo` or AppArmor setup.
Framework, MRTS, Gitlinks, dependencies, action pins, and settings are not
changed.

## Commands executed

### PASS

~~~text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_trusted_lighttpd_namespace_dispatch_workflow
rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_ci_security_workflows
rtk proxy /var/tmp/codex/ModSecurity-conector/trusted-dispatch-security-tools/actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/run-trusted-lighttpd-namespace-dispatch.yml
rtk proxy /var/tmp/codex/ModSecurity-conector/trusted-dispatch-security-tools/zizmor --offline .github/workflows/run-trusted-lighttpd-namespace-dispatch.yml
~~~

The dispatcher contract, weakening mutations, and repository CI-security
workflow contract passed. `actionlint` passed and locked offline `zizmor`
reported no findings.

## Runtime evidence

No trusted runtime success exists yet. After this workflow is merged to
protected `master`, the canonical owner may dispatch PR #309 with:

~~~text
gh workflow run run-trusted-lighttpd-namespace-dispatch.yml --repo Easton97-Jens/ModSecurity-conector --ref master -f target=309
~~~

For SHA mode, replace `309` with PR #309's current full lowercase
40-character head SHA. The dispatcher prints the API-validated PR and SHA
before source materialization. Its successful manual run is the required runtime evidence.
The reporter publishes its fixed exact-SHA status only after the target is
bound; bootstrap or target-resolution failure has no trustworthy SHA and thus
fails the dispatcher without writing an unbound status.

## Known limitations

The exact actor/triggering-actor gate is deliberately narrower than a general maintainer role.
A protected environment with required reviewers would add governance, but
repository-settings changes are outside this pull request. The dispatcher
rejects fork PRs and non-head SHA values by design; it is authorized only for
an open same-repository PR whose head is API-bound before source materialization.

PR #309 remains Draft until this workflow is merged and an exact-head manual
run succeeds.

The active protected-master ruleset must additionally require
`trusted-lighttpd-namespace` before a green ordinary PR check can be treated
as an automatic merge condition. Repository-settings changes are deliberately
out of scope here; until that explicit rule exists, PR #309's retained Draft
state is the documented mandatory manual merge barrier.

## Security impact

The repair removes the model in which a PR could edit privileged steps in the
same pull-request workflow that executes its source. Privileged work now comes
from reviewed protected-master YAML and ends before source materialization.
There is no runner-workspace checkout; the root helper creates only blank
private mounts and never reads, copies, parses, executes, or cleans up a
PR-derived path. All source handling happens after the non-root drop.

The dispatcher adds no root path cleanup, privileged-container fallback,
global AppArmor relaxation, or successful skip.

The reporting job is deliberately separate from the PR-code job. Its ephemeral
`statuses: write` token cannot be read by PR code because the reporter has no
checkout or transferred data other than a strict SHA output and the test-job
conclusion. It cannot select a context, target, or outcome from PR input.

## Remaining risks

The AppArmor profile uses `flags=(unconfined)` to permit this non-root
user-namespace path on Ubuntu 24.04 and is therefore not a restrictive
AppArmor sandbox. Its scope is bounded by a fresh account with no capabilities,
credentials, inherited environment, or Docker socket, plus the namespace
probes. Kernel or Bubblewrap defects remain external platform risk.

The public API is unauthenticated by design to avoid a secret. Rate limiting or
API failure fails closed. The disposable VM's final teardown removes the
profile, account, and temporary data without root cleanup of an
`ns-test`-writable path.

The reporter context is evidence rather than a repository-rule guarantee until
the repository owner adds it to the protected-master required contexts. This
pull request does not change branch rules; PR #309 must remain Draft until
that governance action and an exact-head successful dispatch are both
independently evidenced.

## Checks not run and rationale

The manual Ubuntu-24.04 runtime run cannot occur until this separate workflow
is merged to protected `master`; dispatching the copy in this branch would
destroy the trust boundary. The exact PR #309 namespace unit module was run
locally, but the container rejects user-map writes with `Operation not
permitted`; that local environment cannot substitute for the required hosted
kernel/AppArmor integration. `make check-bilingual-docs` and `make
check-doc-links` also remain blocked by pre-existing missing Framework
submodule files referenced throughout the repository, not by either updated
Change Record. No merge, hosted PR check, SonarQube analysis, or Required Check
is claimed for this new repair head.

## Final diff and review status

This Parent-only bootstrap change is intended for its own Draft pull request.
It leaves PR #309's pull-request workflow unprivileged. After the bootstrap PR
is reviewed and merged, the owner must dispatch from `master`, verify the
resulting PR #309 SHA, and leave #309 Draft unless the full namespace evidence
succeeds.
