# Trusted NGINX root broker

**Language:** English | [Deutsch](trusted-nginx-root-broker.de.md)

The trusted NGINX root broker is a deliberately narrow reusable GitHub Actions
workflow. It is the only planned privileged boundary for the NGINX
master/worker proof required by the F-GS-003 delivery chain. It is not a
general root command runner and it does not authorize PR #240 code, binaries,
modules, shell fragments, or generated environment files to run as host root.

## Immutable invocation boundary

The caller must use the reusable workflow at the exact 40-character merge SHA
that is already reachable from protected Parent `master`:

```yaml
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@<broker-merge-sha>
```

The broker accepts only same-repository `workflow_dispatch` or scheduled
contexts, has read-only `contents` permission, checks the called workflow ref,
checks out the exact broker SHA without persisted credentials, and verifies
that the SHA is an ancestor of current `master`. Immediately before every
privileged action it compares the broker helper's current Git blob with the
blob at that protected SHA and invokes Python in isolated mode.

No `@master`, PR-branch reference, local `uses: ./`, `pull_request_target`,
fork context, broad `sudo`, `sudo -E`, shell callback, command string, or
caller-provided executable path is part of this contract.

## Declarative caller contract

The caller artifact contains one bounded JSON object with exactly these fields:

- `schema_version`
- `run_id`
- `matrix_variant`
- `parent_head_sha`
- `framework_sha`
- `protected_broker_sha`

The workflow binds all six fields to its own inputs. The manifest has no
command, shell, argument-list, configuration-path, or environment field. A
runtime environment snapshot is parsed as declarative text only; it is never
sourced as shell code.

## Protected artifacts and fixed actions

The broker rebuilds the reviewed NGINX binary, ModSecurity NGINX module, and
ModSecurity shared library from the checked-out protected source without root.
It hashes the artifacts, copies them into a fresh root-owned private run tree
with no-follow descriptor checks, and rehashes each artifact before NGINX is
executed. The final manifest fixes every artifact, runtime, PID, log, and
evidence path below that one run tree. The privileged parent is the fixed
root-owned `/var/lib/msconnector-nginx-root-broker` location with runner-group
traversal only; neither the caller nor a broker CLI argument can select it.

Only these root actions exist:

- `validate-manifest`
- `config-test`
- `start`
- `verify-master-worker-identity`
- `project-evidence`
- `stop`
- `cleanup-status`

The broker writes the NGINX configuration, rule, and document itself. It
starts one root master only on loopback and a non-privileged port, requires one
non-root worker with the configured UID/GID and admitted binary inode, and
checks that the process group and listener are gone before cleanup.

## Evidence and cleanup boundary

Only four root-side files can cross to the runner: `identity.json`,
`runtime.json`, `nginx-access.log`, and `nginx-error.log`. Projection uses a
fixed allowlist, no-follow opens, owner/mode/device/size checks, temporary
output, and atomic publication. After upload, cleanup removes exactly the
run-specific root tree descriptor-relatively; it never recursively changes a
repository, cache, or system path.

`runtime.json` reports `root_broker_status: PASS` only for the broker's own
root/master/worker/artifact lifecycle. A `matrix_variant` is retained for
run-bound attribution, but the broker intentionally makes no CRS assertion.
Fresh CRS source materialization and CRS behavior remain separate PR #240
controls and must be evidenced independently.

## Validation boundary

Local focused tests cover schema rejection, SHA/run/variant bindings,
artifact-path/digest checks, no-follow special-file rejection, fixed actions,
workflow pins/context, and descriptor-relative cleanup. A protected-master
hosted invocation is still required to validate GitHub's reusable-workflow
context, real root/master/worker identity, listener release, and artifact
projection on an actual hosted runner. This document is a security contract,
not that runtime evidence.
