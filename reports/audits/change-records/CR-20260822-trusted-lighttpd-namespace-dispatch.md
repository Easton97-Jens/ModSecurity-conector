# Change Record

**Language:** English | [Deutsch](CR-20260822-trusted-lighttpd-namespace-dispatch.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260822-trusted-lighttpd-namespace-dispatch |
| Date (UTC) | 2026-08-22 |
| Base revision | `423abcc130cf5d29ccf15dd7d82e4e7d89d495d3` |
| Delivery status | Separate protected-master bootstrap pull request; no merge or trusted runtime success is asserted. |

## Motivation and problem statement

The Lighttpd same-UID TOCTOU remediation needs a real unprivileged
user/mount/PID-namespace runtime test. GitHub-hosted pull-request runners
correctly fail closed when Ubuntu's AppArmor user-namespace restriction blocks
that test. Putting `sudo` or an AppArmor setup step in the pull-request
workflow would be unsafe because the workflow YAML is supplied by the PR.

This separate, manually dispatched workflow must first be reviewed and merged
to protected `master`. It supplies the short-lived Ubuntu-24.04 setup without
giving a PR-controlled workflow a privileged step.

## Acceptance criteria

- The dispatcher has only `workflow_dispatch`, one `target` input, a
  protected-`master`/canonical-repository gate, and an exact owner-maintainer
  actor gate.
- It has only `contents: read`, no secrets, caches, artifacts,
  `pull_request_target`, status write, or local action checkout.
- Fixed pre-checkout system steps install only fixed packages, load the fixed
  AppArmor user-namespace profile, make `ns-test`, and verify binary, group,
  Docker-socket, and capability preconditions.
- API resolution accepts an open canonical PR number or that PR's exact
  40-character lowercase head SHA; source checkout uses only the resolved SHA.
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

Before checkout, fixed absolute root-owned binaries install only
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

The trusted source path is:

~~~text
manual target -> strict format validation -> fixed public GitHub API request
-> one open canonical PR/head SHA -> exact SHA checkout -> remove .git
-> aa-exec -> setpriv -> env -i -> ns-test namespace test
~~~

No PR-derived text enters a privileged shell command, and the raw input is
never a checkout ref. The PR source is copied only after the identity drop.
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

## Changed files

- `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` — protected
  manual Ubuntu-24.04 dispatcher, API-bound exact checkout, and restricted
  `ns-test` execution.
- `tests/test_trusted_lighttpd_namespace_dispatch_workflow.py` — positive and
  mutation contracts for the trust boundary.
- This English/German Change Record pair and archive entries — authorization,
  invocation, validation, and explicit pending-runtime status.

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
before checkout. Its successful manual run is the required runtime evidence;
it does not make the ordinary pull-request workflow claim success.

## Known limitations

The exact actor/triggering-actor gate is deliberately narrower than a general maintainer role.
A protected environment with required reviewers would add governance, but
repository-settings changes are outside this pull request. The dispatcher
rejects fork PRs and non-head SHA values by design; it is authorized only for
an open same-repository PR whose head is API-bound before checkout.

PR #309 remains Draft until this workflow is merged and an exact-head manual
run succeeds.

## Security impact

The repair removes the model in which a PR could edit privileged steps in the
same pull-request workflow that executes its source. Privileged work now comes
from reviewed protected-master YAML and ends before checkout. The only
post-checkout root operations are fixed Git-state removal and the static
`aa-exec` to `setpriv` launcher; neither reads, copies, parses, or executes PR
source. All source handling happens after the non-root drop.

The dispatcher adds no root path cleanup, privileged-container fallback,
global AppArmor relaxation, or successful skip.

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

## Checks not run and rationale

The manual Ubuntu-24.04 runtime run cannot occur until this separate workflow
is merged to protected `master`; dispatching the copy in this branch would
destroy the trust boundary. No PR #309 code was run locally under this design.
No merge, hosted PR check, SonarQube analysis, or Required Check is claimed.

## Final diff and review status

This Parent-only bootstrap change is intended for its own Draft pull request.
It leaves PR #309's pull-request workflow unprivileged. After the bootstrap PR
is reviewed and merged, the owner must dispatch from `master`, verify the
resulting PR #309 SHA, and leave #309 Draft unless the full namespace evidence
succeeds.
