# Protected exact-head host gate

**Language:** English | [Deutsch](protected-exact-head-host-gate.de.md)

The privileged job is intentionally dependent on a preinstalled host bootstrap
at:

`/usr/local/libexec/modsecurity-protected-exact-head/run-exact-base-launcher`

The bootstrap is platform infrastructure, not pull-request code. Before it
executes any Base-owned launcher it MUST:

1. be a regular `root:root` file with mode `0755` and no symlinked path
   component;
2. read each Python entrypoint from the protected Base checkout by the
   supplied `--trusted-base-sha` and `--entrypoint-relative-path`, verify the
   Git object and the checkout commit, and copy it to a root-owned private
   snapshot;
3. scrub the environment and execute the snapshot as root, forwarding only
   the arguments after `--`;
4. refuse missing, malformed, mismatched, writable, or mutable inputs.

The gate's entrypoint allowlist is exact and closed:

- `ci/runtime/broker/nginx_exact_head_root_launcher.py`
- `ci/runtime/broker/nginx_exact_head_result_collector.py`

It MUST reject every other `--entrypoint-relative-path`, including paths that
merely normalize to an allowed path. The supplied Base repository root MUST be
an absolute, normalized, symlink-free directory whose verified Git `HEAD`
equals `--trusted-base-sha`. The gate MUST parse and validate all forwarded
options before snapshotting, reject unknown gate options, and forward only the
arguments after the standalone `--` separator.

The workflow invokes the same gate for both
`ci/runtime/broker/nginx_exact_head_root_launcher.py` and
`ci/runtime/broker/nginx_exact_head_result_collector.py`, always with the
exact Base SHA. It never grants `sudo` permission to a checkout- or task-root-
resident Python path, and it performs no post-collector privileged path
operation. The runner preflight also fails closed when this gate is absent or
has the wrong owner, group, mode, or file type.

The two allowlisted Parent paths are now small source-integration shims. The
large launcher, collector, dispatcher and cell driver belong to the pinned
Test-Framework under `connector_suite/modsecurity_connector_ci/runtime/broker/`.
The shims authenticate `ci/run-trusted-framework.py` against their reviewed
`BRIDGE_SHA256` before executing its bytes. That bridge resolves the Framework
revision only from the exact trusted Parent Base gitlink
`modules/ModSecurity-test-Framework`, verifies both checkout identities, and
compares the requested implementation with its exact Framework Git blob.
Candidate-selected Framework revisions, changed implementation bytes, symlinked
source paths, nonregular files and oversized sources are rejected.

When invoked as root, Git inspection runs as the explicitly supplied nonroot
`--runner-uid` and `--runner-gid` through `/usr/bin/setpriv`, with supplemental
groups and all capability sets cleared and `--no-new-privs`. Authenticated
Python bytes enter a sealed `memfd` and a fresh isolated interpreter; neither
candidate imports nor changes to `sys.path` or `sys.modules` are needed. The
launcher separately binds the shell cell driver to the trusted Parent
gitlink's Framework blob and retains its descriptor across sandbox setup.

Both shim invocation envelopes explicitly carry `--base-repo-root` and
`--trusted-dispatcher-base-sha` after the gate's `--` separator, in addition to
the entrypoint's existing evidence and runner arguments. The collector shim
consumes those two source-binding options before calling the Framework
collector. Host owners must review the installed gate's forwarded-option
validation against this envelope. A gate that rejects these options remains
blocked; the workflow must never bypass it or execute a checkout-resident
launcher directly. The closed gate entrypoint allowlist above is unchanged.

Current workflow orchestration lives in the Framework reusable workflow
`connector-protected-nginx-exact-head.yml`; the Parent retains its small
`run-protected-nginx-exact-head.yml` dispatch entrypoint with an exact Framework
commit pin. Protected branch, actor, environment, runner, manifest and artifact
guards remain in the called workflow. Historical NGINX root-broker callers
retain their immutable Parent `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` and
Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` contracts. These historical
calls do not qualify the migrated source revision.

This repository cannot prove installation or behavior of the host bootstrap
from a normal checkout. A protected exact-head run therefore requires a
dedicated ephemeral runner with the gate installed and reviewed by its host
owner; a generic or self-hosted runner without that prerequisite is a blocked
hosted-gate validation, not runtime evidence.
