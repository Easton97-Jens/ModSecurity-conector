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

This repository cannot prove installation or behavior of the host bootstrap
from a normal checkout. A protected exact-head run therefore requires a
dedicated ephemeral runner with the gate installed and reviewed by its host
owner; a generic or self-hosted runner without that prerequisite is a blocked
hosted-gate validation, not runtime evidence.
