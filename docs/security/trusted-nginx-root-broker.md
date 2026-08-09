# Trusted NGINX root broker

**Language:** English | [Deutsch](trusted-nginx-root-broker.de.md)

The trusted NGINX root broker is a deliberately narrow reusable GitHub Actions
workflow. It is the only privileged boundary planned for the NGINX
master/worker proof in the F-GS-003 delivery chain. It is not a general root
command runner: PR #240 code, Framework scripts from a PR checkout, caller
shell fragments, configuration/rule files, CRS paths, binaries, modules, and
generated environment files never run as host root.

## Immutable invocation boundary

The caller uses the reusable workflow at the exact 40-character merge SHA
already reachable from protected Parent `master`:

```yaml
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@e06254ea9622d214a9030b9ba786756560ace417
```

The broker accepts only same-repository `workflow_dispatch` or scheduled
contexts, has read-only `contents` permission, checks the called workflow ref,
checks out the exact broker SHA without persisted credentials, and verifies
that SHA is an ancestor of current `master`. Immediately before every
privileged action it compares the helper's Git blob with the blob at that
protected SHA and invokes Python in isolated mode.

No `@master`, PR-branch reference, local `uses: ./`, `pull_request_target`,
fork context, broad `sudo`, `sudo -E`, `sudo sh -c`, `sudo bash -c`, shell
callback, command string, or caller-provided executable path is part of this
contract.

## Protected resulting-master caller

The reusable-only broker cannot itself create resulting-`master` runtime
evidence. The separate `Protected NGINX Root Broker Lifecycle` workflow at
`.github/workflows/run-protected-nginx-root-broker.yml` supplies that narrow
entry point. It has only `workflow_dispatch`, accepts only required
`parent_head_sha`, grants only `contents: read`, and has a non-cancelling
workflow-wide concurrency group. Every caller job requires the canonical
non-fork repository, a `workflow_dispatch` event, and `refs/heads/master` as
the protected default branch.

`parent_head_sha` is a declarative evidence identity, not a source selector.
The unprivileged preparation job accepts only lowercase SHA-40, confirms that
commit through a fixed read-only GitHub API endpoint, and records it in the two
caller manifests. It never checks out, imports, sources, builds, starts,
loads, or root-executes that commit. The caller checks out only its protected
current-master source to run its reviewed data-only helper. The only root
actions remain inside this immutable call and the Framework gitlink is fixed
to the broker revision rather than to a later Parent state:

```yaml
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@e06254ea9622d214a9030b9ba786756560ace417
```

```text
protected_broker_sha = e06254ea9622d214a9030b9ba786756560ace417
framework_sha        = c71e15db7b7517b237add9fa09b3493e7bc93627
```

The caller makes two explicit immutable calls, never a user-selected matrix:
`no-crs` with profile `no-crs`, and `with-crs` with profile `owasp-crs`. It
creates one private, deterministic, parsed-before-upload manifest artifact for
each fixed run ID. Each artifact contains only `caller-manifest.json`, has one
day retention, and is supplied to the matching immutable reusable call.

## Versioned declarative caller contract

The reusable-workflow interface has exactly six inputs:

- `caller_manifest_artifact`
- `parent_head_sha`
- `framework_sha`
- `protected_broker_sha`
- `matrix_variant`
- `run_id`

Those call inputs are distinct from the schema-v2 JSON manifest. Schema v2 has
exactly seven fields; the additional field is the closed `policy_profile`:

Schema v1 remains the reproducible no-CRS control contract. Schema v2 accepts
exactly the v1 identity fields plus `policy_profile`:

- `schema_version`
- `run_id`
- `matrix_variant`
- `policy_profile` (schema v2 only)
- `parent_head_sha`
- `framework_sha`
- `protected_broker_sha`

The profile is closed and variant-bound: `no-crs` selects the protected
`no-crs` profile, while `with-crs` selects `owasp-crs`. Unknown schema
versions, profiles, fields, and profile/variant combinations fail closed. The
caller cannot select a CRS source/configuration path, rule include, ref,
commit, bundle digest, ModSecurity directive, command, or environment value.
A runtime environment snapshot is parsed as declarative text only; it is never
sourced as shell code.

## Protected artifacts and CRS bundle

The workflow rebuilds the reviewed NGINX binary, ModSecurity NGINX module, and
ModSecurity shared library from the checked-out protected source without root.
For schema-v2 `owasp-crs`, it also creates a fresh private CRS source root and
uses the exact Framework gitlink's canonical fresh-source path. The broker
revision independently cross-checks this reviewed tuple:

| Field | Fixed value |
| --- | --- |
| Repository | `https://github.com/coreruleset/coreruleset.git` |
| Release tag | `v4.28.0` |
| Commit | `55b09f5acfd16413e7b31041100711ceb7adc89c` |
| Expected CRS block rule | `949110` |

The bundle manifest binds the tuple, Framework gitlink, broker commit,
creation time, sorted allowed-file records, file count, and aggregate digest.
Only `crs-setup.conf.example`, `rules/*.conf`, and the closed plugin-config
forms are eligible. A record gives a portable relative path, SHA-256, size,
mode, type, broker commit, and CRS commit. Symlinks, extra files, hardlinks,
special files, executable rule files, traversal, absolute paths, duplicate
records, and mutable refs are rejected.

At admission, root reads only the manifested bundle from the fixed protected
build layout using descriptor-relative opens and `O_NOFOLLOW`. It checks owner,
mode, device, link count, inode/size stability, and digest before and after
copying. The only materialized CRS configuration is root-owned and read-only
below the current broker root; no caller path is loaded by NGINX or ModSecurity.

## Fixed profiles and actions

Only these root actions exist:

- `validate-manifest`
- `config-test`
- `start`
- `verify-runtime-profile`
- `verify-master-worker-identity`
- `project-evidence`
- `stop`
- `cleanup-status`

The broker writes the NGINX configuration, rule file, and document itself. It
starts one root master only on loopback and a non-privileged port, requires one
distinct non-root worker with the admitted binary inode, and verifies that the
process group and listener are gone before cleanup.

The `no-crs` profile retains only the broker-owned `/blocked` control rule and
carries no pretend CRS tuple. The `owasp-crs` profile writes the portable serial
audit configuration and fixed includes for the root-owned CRS bundle. It uses
the Framework's canonical CRS smoke request
`/?id=1%20UNION%20SELECT%20password%20FROM%20users`, requires a 200 allow and a
403 block, and rejects the run unless the private audit record binds the run,
request, transaction, status, bundle digest, and CRS rule `949110`.

Candidate and final manifests carry the selected profile. An `owasp-crs` final
manifest additionally carries the repository/tag/commit, bundle-manifest and
aggregate digests, file count, root-local bundle/audit paths, expected rule
evidence, and protected producer bindings. A no-CRS manifest must not carry
those CRS fields.

## Evidence and cleanup boundary

The root-to-runner projection has an exact profile-specific allowlist. Schema
v2 projects `identity.json`, `runtime.json`, `policy.json`, access/error logs,
and, for `owasp-crs`, `nginx-audit.log`. Projection uses no-follow opens,
owner/mode/device/size checks, temporary output, and atomic publication. A
protected non-root workflow step copies only that fixed list outside the
run-specific root before descriptor-relative cleanup. It adds a fixed
`cleanup.json` only after `cleanup-status` returns, recording the bound broker
SHA, run ID, variant, and PASS/FAIL cleanup result.

`runtime.json` reports `root_broker_status: PASS` only after the selected
profile's own root/master/worker/artifact lifecycle has passed. For `owasp-crs`
that result also contains the fixed CRS tuple and bundle identity; it is not an
Apache result and a bare HTTP 403 is insufficient.

The caller then downloads only the two run-bound broker artifacts in an
unprivileged evidence-readback job. It requires the exact profile-specific
file set, rejects unknown JSON fields and symlinks, binds both run IDs, the
declarative Parent SHA, the immutable broker/Framework SHAs, root master and
non-root worker identities, `PASS` cleanup, and the CRS bundle/audit digest
for `owasp-crs`. The no-CRS artifact must not contain an audit file. Its final
always-run result job fails if manifest preparation, either broker profile, or
evidence readback did not succeed; it cannot turn a failed broker job green.

## Validation boundary

Local focused tests cover schema/profile rejection, provenance, bundle path and
file safety, fixed root-generated configuration, stale/missing audit evidence,
IPv6 loopback handling, workflow pins/context, bounded evidence staging, and
descriptor-relative cleanup. A protected-master hosted invocation remains
required to prove GitHub reusable-workflow context semantics, a real root
master/non-root worker, real CRS execution, audit output, listener release,
and final uploaded cleanup evidence. This document is a security contract, not
that runtime evidence.

PR #240 remains blocked until this caller has been normally merged, dispatched
from resulting protected `master`, and observed to pass both `no-crs` and
`owasp-crs` profiles with successful evidence readback and cleanup. A later
dispatch may bind PR #240's final head only as declarative evidence; it never
executes PR #240 code at the root boundary.
