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
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@<broker-merge-sha>
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

## Versioned declarative caller contract

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

## Validation boundary

Local focused tests cover schema/profile rejection, provenance, bundle path and
file safety, fixed root-generated configuration, stale/missing audit evidence,
IPv6 loopback handling, workflow pins/context, bounded evidence staging, and
descriptor-relative cleanup. A protected-master hosted invocation remains
required to prove GitHub reusable-workflow context semantics, a real root
master/non-root worker, real CRS execution, audit output, listener release,
and final uploaded cleanup evidence. This document is a security contract, not
that runtime evidence.
