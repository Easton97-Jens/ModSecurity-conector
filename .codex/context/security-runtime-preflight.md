# Host-test execution context and preflight

Load before native host tests that change process identity or use private Unix sockets, including focused security validation. Executable checks belong to the Framework; the maintained profile/CLI reference is [Framework host execution context](../../modules/ModSecurity-test-Framework/docs/host-execution-context.md).

## Choose the actual execution context

Run the preflight inside the same launcher/namespace and approval context that will start the host. Do not reuse a successful preflight from another session, another command sandbox, another profile or the outer side of a protected broker.

The 2026-11-01 comparison found the ordinary Codex command sandbox had UID/GID maps `0 0 1`, zero effective/bounding capabilities, `NoNewPrivs=1` and seccomp enabled. The approved host command had maps `0 0 4294967295`, the initial user namespace, effective identity/ownership capabilities, `NoNewPrivs=0` and seccomp disabled. This explains the reproduced identity-switch blocker; it does not establish a general Ubuntu-host restriction or independently reconstruct the old assessment process.

For an authorized local native run, select the tool's reviewed `require_escalated` command path when the normal sandbox cannot meet the profile. Keep ordinary independent static/unit checks in their usable context. The Framework never escalates automatically. RTK and any broker/authentication wrappers still apply. This is a per-command context choice; do not edit global Codex permissions, host services, UID maps or security controls to obtain a pass.

## Fresh invocation

Use the Framework-owned interpreter and explicit Framework source selection. Choose an existing approved external task parent; all output paths must satisfy the current Framework runtime-path validator.

```sh
rtk bypass env PYTHONPATH="$TEST_ROOT:$TEST_ROOT/connector_suite" \
  "$FRAMEWORK_PYTHON" -P -m modsecurity_connector_ci.runtime.common.hostruntime_preflight \
  --execution-context-only --connector nginx --profile nginx-native-sequence-h1 \
  --runtime-root "$TASK_RUNTIME" --output-dir "$TASK_RUNTIME/preflight" \
  --worker-user nobody --worker-group nogroup \
  --require-root-master --require-chown
```

That example describes the current direct NGINX sequence contract only. Resolve other profiles from their current launchers; never assign UID 65534 to every connector. Add required `--worker-read`, `--worker-write`, `--worker-deny`, `--port` and `--uds-path` inputs from that contract. An explicitly approved shorter private UDS root uses `--uds-root`; it does not authorize shared/public sockets.

The existing `status.json` / `summary.md` use `evidence_kind=preflight`, `runtime_status=NOT_RUN`; exit 77 means `BLOCKED`. `execution_context` retains bounded UID/GID/groups, mappings, user namespace, capability/NoNewPrivs/seccomp indicators and actual probe-child credentials. Preflight PASS proves prerequisites only.

## Profile requirements and integration

- Direct NGINX smoke: distinct configured non-root worker, root master, mapped worker/supplementary groups, actual setgroups/setgid/setuid and ownership hand-off. The Framework harness checks before identity-dependent setup and again for docroot access, worker-state/log writes and denial of access to private logs/rules/evidence. It preserves its existing independent `runuser` and path-isolation checks.
- NGINX sequence: the checked-in contract specifically requires `nobody:nogroup` (UID/GID 65534), independent static-docroot projection, private master output and real process/cleanup evidence. Identity and access gates run before configuration/start. The bounded `multiple_sequential_requests` operation supplies legitimate/block/follow-up traffic; it is explicitly on demand, not a historical-matrix run.
- Envoy ext_authz plus response observer: children inherit launcher credentials. Validate private UDS ownership/mode, byte-length, fresh bind/connect and cleanup; no unrelated NGINX identity/capability requirement. A shorter external socket root retains the same privacy and path checks.
- Protected NGINX exact-head/root broker and trusted Lighttpd remain separate trusted-source/authorization contracts. The exact-head namespace master may map to the host runner rather than host UID 0. Preserve admission, namespace, sealed-source, ownership and independent observation controls. An outer successful preflight is not inner namespace evidence; these protected paths are not repaired by running candidate code as unrestricted root.

## Distinguish blockers

- `worker_identity_unmapped`: selected UID or GID is absent from the current namespace map; compare the approved host context before attributing this to Ubuntu.
- `worker_transition_capabilities_missing`, `chown_capability_missing` or actual transition failure: effective UID 0 is insufficient; inspect the exact child capabilities/NoNewPrivs and launcher restrictions.
- Worker path/access failures: inspect ownership, modes, symlinks and every ancestor of the selected build/runtime/log/docroot path. Only repair task-owned paths within the existing contract.
- UDS failures: check the actual encoded pathname length, separately approved private root, ownership, existing endpoint and client credentials. Shorten only within authorized external storage.
- Binary/library/tool/config failures remain dependency/artifact blockers. Successful identity probes do not satisfy them. A preflight cannot classify an unexecuted connector as a product failure.

Before retrying, retain a fresh same-context status, exact selected profile/source/artifact identity, path ownership/access evidence and the corrected invocation. Then run only the affected real checks and verify cleanup. Continue independent executable checks while reporting blocked ones concretely. Do not substitute root workers, permissive modes, disabled namespace checks, fabricated identity changes or synthetic runtime evidence.

## Task evidence and limits

The task-owned evidence root is `/var/tmp/codex/ModSecurity-conector/runs/20261101-connector-context`; its reviewable bounded receipt is `private/verification.json`. It records current source/artifact hashes, observed process credentials, HTTP sequence, additional launcher probes and cleanup. Read it as dated evidence, never as permission to skip a new preflight.
