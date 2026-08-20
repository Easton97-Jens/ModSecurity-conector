# lighttpd Harness

**Language:** English | [Deutsch](README.de.md)

Status: native config-load, start, and minimal runtime-smoke paths

The connector owns four native harness scripts:

- `prepare_native_smoke.sh` writes temporary Common and lighttpd configs below
  `BUILD_ROOT` with both body modes disabled;
- `check_lighttpd_config.sh` loads the real module through real `lighttpd -tt`;
- `start_lighttpd_smoke.sh` starts, checks, and stops lighttpd without requests;
- `runtime_lighttpd_smoke.sh` separately sends an allowed and a blocked request.

The corresponding targets are:

```sh
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd
```

The runtime smoke uses `OPTIONS *` so lighttpd core can return the allowed 200
without loading unrelated stock modules from the temporary connector module
directory. Adding `X-Modsec-Smoke: block` must return 403 from rule `1000001`.
The script also verifies the narrow Common JSONL decision metadata.

`start-smoke-lighttpd` deliberately sends zero requests and reports that count.
The bridge self-test is separate and is never used as host evidence.

`run_lighttpd_smoke.sh` remains the entrypoint for the older framework-owned
`sidecar_proxy` path. It is an alternative path and its evidence must not be
mixed with the native-module evidence.

The full-lifecycle dispatcher does not reuse the generic stock No-CRS runner.
It invokes `runtime-smoke-lighttpd-patched` through
`full-lifecycle-lighttpd-patched`, which builds and loads only a matched patched
Framework-synchronized lighttpd core/module pair. The isolated target sends the same narrow
Phase-1 200/403 requests with both body modes disabled; it is not request-body,
response-body, Phase-4, or capability-promotion evidence.

Request/response body evidence, CRS, production hardening, security
verification, and full-matrix evidence are not provided by this harness.

## No-CRS fixture isolation and cleanup

The No-CRS baseline uses the trusted namespace runner
`run_no_crs_fixture_trusted_namespace.py`. The runner rejects a host-root or
set-id caller and starts the trusted setup chain through root-owned
`/usr/bin/unshare`, fixed `/usr/bin/dash` and `/usr/bin/mount`, and then
`/usr/bin/bwrap`. The shell setup makes mount propagation private and mounts a
private `nosuid,nodev,noexec` tmpfs at `/tmp` before entering bwrap. Bwrap
exposes only the minimal read-only system and runtime binds needed by the
harness plus the exact task-owned smoke root as the sole writable bind. The
fixture root itself is mode-0700.

The setup component is the only component that may require namespace and
mount capabilities. It attests the capability state after setup; the harness
continues only when all effective, permitted, inheritable, ambient, and
bounding capabilities are zero and `no_new_privs` is enabled. The test
process does not retain setup capabilities. Missing namespace support,
unexpected capability state, or an unavailable execution-isolation control
fails closed; there is no fallback to the former path-check-then-`rmdir`
cleanup.

Fixture lifetime is tied to the private namespace. Normal completion,
fixture creation failure, test failure, timeout, signal termination, helper
failure, and partial initialization all tear down the child process group and
private namespace. The final namespace-state verifier checks only the
capability sets, `no_new_privs`, mount state, and fixed fixture-root
device/inode (`dev:ino`) identity. The descriptor-I/O cleanup command separately
verifies the allowlisted fixture-leaf inventory, retains every leaf, and does
not unlink or re-resolve the fixture pathname. All leaves and the directory
disappear when the private tmpfs namespace is torn down. Mount propagation is
explicitly private, so fixture mounts are not propagated to the host mount
namespace.

Threat model: a same-UID process may rename, replace, or recreate the old
fixture pathname while a test is running. The security boundary therefore
does not rely on an inode check followed by a pathname deletion. The fixture
is created and used in a private mount namespace, the writable root is
controlled by the runner, and namespace release removes the private mounts.
This prevents a replaced host pathname from becoming the cleanup target.

The local nested container has only a one-entry UID/GID map, so it cannot
exercise the complete non-root production entry path. That limitation blocks
the local production integration claim; it does not authorize a less secure
fallback.
