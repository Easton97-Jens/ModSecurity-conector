# Trusted NGINX root broker

**Language:** English | [Deutsch](trusted-nginx-root-broker.de.md)

The trusted NGINX root broker is a deliberately narrow reusable GitHub Actions
workflow. It is the only privileged boundary planned for the NGINX
master/worker proof in the F-GS-003 delivery chain. It is not a general root
command runner: PR #240 code, Framework scripts from a PR checkout, caller
shell fragments, configuration/rule files, CRS paths, binaries, modules, and
generated environment files never run as host root.

## Immutable invocation boundary

This separate caller-repin patch updates the caller to use the
reusable workflow at the exact 40-character broker commit SHA already reachable
from protected Parent `master`:

```yaml
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@49c40779a7b6de9f699391bcd524ea069787df42
```

Both caller `uses` values and both `protected_broker_sha` values in this
caller-repin patch are pinned to the available protected broker-repair commit SHA
`49c40779a7b6de9f699391bcd524ea069787df42`; neither a branch nor `master` is
an acceptable substitute.

GitHub documents that the `github` context in a called reusable workflow is
associated with its caller, including `github.workflow_ref`. The broker
therefore treats that value exclusively as the exact caller identity
`Easton97-Jens/ModSecurity-conector/.github/workflows/run-protected-nginx-root-broker.yml@refs/heads/master`,
not as the identity of `.github/workflows/nginx-root-broker.yml`. The
immutable `uses` SHA selects the called workflow; GitHub recommends a commit
SHA as the safest reference. [Reusable-workflow reference](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
and the [contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
define those semantics.

Before the broker checkout, a fixed shell gate accepts only the exact
same-repository `workflow_dispatch` caller context: canonical repository,
non-fork, `refs/heads/master`, default branch `master`, exact caller workflow
reference, and canonical `github.sha`. If `github.workflow_sha` is available,
it must also be canonical SHA-40 and equal `github.sha`; otherwise the caller
commit is bound through `github.sha` and its Git object without fabricating a
positive check. The broker separately validates canonical
`protected_broker_sha`, then checks out exactly that broker SHA without
persisted credentials and with full history. That checkout is used only to
prove protected-`master` ancestry, interrogate the caller Git object, and bind
the broker source; caller-YAML validation completes before any manifest
download, build, candidate generation, or root action. The broker proves the
caller commit exists, is on protected `master`, and descends from the broker
commit.

The caller workflow file is never checked out, sourced, or executed by the
broker. The broker reads only its fixed path as a bounded regular `100644`
Git blob from the caller commit, using `git cat-file`, then parses a deliberately
restricted declarative YAML subset. It rejects duplicate keys, anchors,
aliases, tags, merge keys, flow syntax, unsafe encodings, malformed nesting,
and unexpected job schemas. Exactly `run-no-crs-broker` and
`run-with-crs-broker` may call the broker; both must use the same literal
SHA-40 equal to `protected_broker_sha`, exact variant, exact inputs, and only
`contents: read`, with no secrets or additional reusable job.

The broker binds the checked-out Framework HEAD and input to the `160000`
Framework gitlink recorded by the broker commit and requires recursive clean
submodules. It verifies both `.github/workflows/nginx-root-broker.yml` and
`ci/runtime/broker/nginx_root_broker.py` as regular non-symlink files whose
Git blobs match the broker commit before caller-YAML validation, after setup
or build activity, before candidate generation, and immediately before every
root action. Python remains isolated for root actions.

Neither workflow grants `id-token: write`; the observed token boundary is
limited to `Contents: read` and `Metadata: read`. This Git-object and
declarative-YAML contract removes any need for an OIDC alternative.

No `@master`, PR-branch reference, local `uses: ./`, `pull_request_target`,
fork context, broad `sudo`, `sudo -E`, `sudo sh -c`, `sudo bash -c`, shell
callback, command string, or caller-provided executable path is part of this
contract.

### Observed fail-closed mismatch

[Run `31310183097`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31310183097)
was a `workflow_dispatch` from `master` at caller SHA
`128a2f63f182758b1c1a1d4746f5e56f609d245d`. Its manifest preparation passed,
but both broker profiles failed at the former binding step and evidence
readback was skipped. The old check expected
`Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@e06254ea9622d214a9030b9ba786756560ace417`,
while GitHub supplied the actual caller reference
`Easton97-Jens/ModSecurity-conector/.github/workflows/run-protected-nginx-root-broker.yml@refs/heads/master`.
The failure was correctly fail-closed but compared identities from different
layers. It occurred before protected broker checkout, build, CRS creation,
`sudo`, root admission, NGINX start, artifact projection, and cleanup. It is
caller-context evidence only; it is not root, NGINX, CRS, worker, artifact, or
cleanup PASS evidence.

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
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@49c40779a7b6de9f699391bcd524ea069787df42
```

```text
protected_broker_sha = 49c40779a7b6de9f699391bcd524ea069787df42
framework_sha        = 03880bf66b3905940466ff10b3a431a27ecc6b26
```

The caller makes two explicit immutable calls, never a user-selected matrix:
`no-crs` with profile `no-crs`, and `with-crs` with profile `owasp-crs`. It
creates one private, deterministic, parsed-before-upload manifest artifact for
each fixed run ID. Each artifact contains only `caller-manifest.json`, has one
day retention, and is supplied to the matching immutable reusable call.

The helper accepts no caller-selected manifest or evidence filesystem path.
It derives the two fixed directory roots only from the runner-provided
absolute, non-symlink `RUNNER_TEMP` directory and the validated paired
`protected-nginx-root-…-no-crs` / `protected-nginx-root-…-with-crs` run IDs.
Both derived roots are independently required to be non-symlink directories.
Any missing, relative, symlinked, malformed, or mismatched path identity fails
before API access, artifact creation, or evidence readback.

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

## Protected runtime snapshot contract

The broker admits only a private fixed-provenance record at
`build/runtime-component-reports/trusted-nginx-broker-provenance.json` and its
matching private snapshot. The snapshot contains exactly these three values,
and no others:

- `NGINX_BINARY`
- `NGINX_MODULE`
- `MODSECURITY_SHARED_PREFIX`

Before admission, the broker validates the record's paths, digests, metadata,
and Parent and Framework identities. A generic runtime snapshot, or a direct
harness environment override, is not accepted at the broker boundary. The
active caller pins the broker revision that contains this protected
snapshot contract, so a resulting-Parent-master dispatch selects it directly.

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

The pinned CRS tree contains one intentionally empty plugin leaf,
`plugins/empty-after.conf`. The broker admits that zero-byte leaf only when
the protected Git object at
`55b09f5acfd16413e7b31041100711ceb7adc89c:plugins/empty-after.conf` is exactly
the Git blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` and the materialized
regular `0644` file has SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Any
other empty CRS file, a non-regular file, a symlink, a changed mode, a changed
digest, or a changed pinned tag/commit fails closed. This is a fixed
provenance check, not a general empty-file allowance.

The root-to-runner evidence limits remain exactly
`MAX_EVIDENCE_FILE_BYTES = 8 * 1024 * 1024` and
`MAX_EVIDENCE_TOTAL_BYTES = 20 * 1024 * 1024`; this repair does not widen
either limit for logs, JSON evidence, manifests, CRS bundles, or NGINX
artifacts. Only the canonical, provenance-bound regular
`prefix/lib/libmodsecurity.so.3` uses the separate fixed broker-policy ceiling
`MAX_TRUSTED_MODSECURITY_LIBRARY_BYTES = 64 * 1024 * 1024`. It is a code
constant, never a caller input, environment value, or manifest field. A
retained protected producer record measured the reviewed library at 60,085,848
bytes, leaving 7,023,016 bytes of bounded build-variance headroom. The ceiling
is enforced both while validating the producer record and again on the opened
source descriptor before hashing or copying; NGINX binary and module retain
the 8 MiB ceiling.

The broker-owned outer build mode remains `umask 077`. Only the fixed
`sh modules/ModSecurity-test-Framework/ci/provisioning/fetch-crs.sh` invocation
runs in a subshell at `umask 022`, with an explicit outer `077` check before
the subshell and after either its success or failure. The checks accept the
canonical shell renderings `077` and `0077` (and correspondingly `022` and
`0022`) rather than depending on one spelling. The fetch status is then
re-thrown unchanged. The checked-out CRS source root and required `rules`
directory, plus `plugins` when it exists, must be exact `0755`
directories; selected regular CRS
files must be exact `0644`. No global `022`, recursive `chmod`, caller command,
or relaxation of private manifests, snapshots, evidence, broker state, audit,
or root-admission files is part of this contract.

### Active ABI loader contract

The ordinary ModSecurity prefix may retain Libtool's unversioned linker alias
`libmodsecurity.so`, but that alias is normally a symlink and is not a trusted
runtime artifact. The active immutable broker revision resolves the Libtool
aliases descriptor-relatively and requires each expected alias to contain a
direct basename target. Both aliases must resolve to the same regular terminal
object. The regular `prefix/lib/libmodsecurity.so.3` protected copy is created
from the descriptor tied to that validated terminal, so a nested-symlink
escape or replacement cannot redirect the copy. The producer provenance,
candidate manifest, root-owned artifact directory, and `LD_LIBRARY_PATH` then
all bind that ABI SONAME name. No symlink is admitted at the protected
producer, candidate, or root boundary.

For this protected build only, the fixed workflow value
`NGX_IGNORE_RPATH=YES` prevents the explicitly supplied ModSecurity library
directory from becoming an NGINX-module dynamic search path. Before candidate
creation, the broker inspects both the verified module and the verified
`libmodsecurity.so.3` with the fixed absolute tool `/usr/bin/readelf` and an
empty `PATH`, bounded output, and a real bounded deadline. For either ELF,
`DT_RPATH`, `DT_RUNPATH`, a slash-bearing `DT_NEEDED`, or any `DT_AUDIT`,
`DT_DEPAUDIT`, `DT_FILTER`, or `DT_AUXILIARY` entry blocks admission, as does a
failed or non-text inspection. This inspection is unprivileged and completes
before candidate creation and every root action. These checks are active in
the selected broker, but are not evidence that the repinned caller has
completed a runtime lifecycle. A new protected-master run remains required.

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

The only directories with the narrow `root:worker` `0730` layout are the
broker-created log and state directories and, for `owasp-crs`, the CRS audit
directory. Each must remain root-owned, belong to the admitted worker GID, have
exact mode `0730`, and have an entirely non-symlink path. The allowance exists
only so the admitted worker can write these broker-created runtime outputs; it
does not relax the existing directory-metadata validation for any other path.
All other root-bound ownership, mode, path, manifest, artifact, and
pre-root/root-action controls remain unchanged.

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
descriptor-relative cleanup. After the initial loader repair, 83 focused tests
passed. After the expanded security remediation, a later broker/CRS suite
passed 43 tests, the focused remediation passed 2 tests, and the producer
focused matrix passed 5 tests. The full owning cache module passed 38 tests and
had one known isolated-worktree fixture error. Phase-B local validation then
passed 109 tests in 9.253s across the protected caller, broker, workflow, CI
security-workflow, and Python-version-contract test modules. The Phase-B CI
security contract also passed its 26 CI security tests plus validate-only
actionlint/zizmor/gitleaks locks. The standalone Python-version-contract check
exited 2 only for unchanged current-`master` inventory violations in
`verified-report-governance`, `ci-security-codeql` trusted-go-version,
Apache/HAProxy, and `update-workflow-tools`; it is nonpassing baseline evidence
and not a Phase-B pin violation. These are local source/static results. A
protected-master hosted invocation remains required to prove GitHub
reusable-workflow context semantics, a real root master/non-root worker, real
CRS execution, audit output, listener release, and final uploaded cleanup
evidence. This document is a security contract, not that runtime evidence.

Run `31368594208` is retained pre-fix failure evidence only: its no-CRS leg
rejected the genuine protected library under the generic 8 MiB evidence limit,
and its with-CRS leg rejected fresh checkout files that inherited `umask 077`.
Both legs stopped before candidate admission, every root action, NGINX startup,
evidence projection, and cleanup verification. [PR #274](https://github.com/Easton97-Jens/ModSecurity-conector/pull/274)
merged the prior caller repin at `4749c02c6dd5e285c4309b4e69b0bb28ae459e48`,
selecting broker `7a9240d35e50475cc1a381fa103b0bb5cca2bee3`. [PR #275](https://github.com/Easton97-Jens/ModSecurity-conector/pull/275)
subsequently merged broker commit `49c40779a7b6de9f699391bcd524ea069787df42`,
making the FND-PARENT-0120/FND-PARENT-0121 repair available. This separate
caller-repin patch selects the `49c40779a7b6de9f699391bcd524ea069787df42`/
`03880bf66b3905940466ff10b3a431a27ecc6b26` tuple. Neither those merges nor
this local source/static evidence is runtime proof; a fresh resulting-master
lifecycle remains mandatory.

PR #240 remains blocked until this resulting-master caller is dispatched and
observed to pass both `no-crs` and `owasp-crs` profiles with successful
evidence readback and cleanup. A later dispatch may bind PR #240's final head
only as declarative evidence; it never executes PR #240 code at the root
boundary.

For the Parent-only FND-PARENT-0120/FND-PARENT-0121 repair based at
`4749c02c6dd5e285c4309b4e69b0bb28ae459e48`, failure run `31421851336` remains
failure evidence only. The in-memory compile check passed and the focused
`tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile` suite
passed 55 tests in 11.750 seconds. A direct `py_compile` check was blocked
because this worktree cannot create `__pycache__`. None of this local evidence
proves a hosted run, pull-request state, root/worker lifecycle, CRS execution,
evidence readback, or cleanup success.
