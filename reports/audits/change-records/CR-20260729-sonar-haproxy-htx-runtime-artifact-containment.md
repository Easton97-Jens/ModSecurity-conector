# Change Record: Parent HAProxy HTX runtime-artifact containment

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-htx-runtime-artifact-containment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-htx-runtime-artifact-containment |
| Date (UTC) | 2026-07-29 |
| Base revision | Original change base `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`; synchronized candidate base `200712b4dcede1caccc753a572e1e754a5de3e8b` |
| Tracking | Current HAProxy HTX harness path, localhost-client, and complexity SonarQube Cloud candidates. |
| Boundary | Parent `ci/lib/`, HAProxy and Envoy harness facades, focused Parent tests, and paired indexes only. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

## Motivation and problem statement

The local HTX smoke helper accepted command-line paths after checking only that they were absolute.

Its output and evidence reads could therefore name a different filesystem location.

Its client helpers also accepted clear-text HTTP although the harness topology is exclusively local and can authenticate a temporary TLS endpoint.

## Acceptance criteria

- Every CLI artifact read and write is absolute, non-symlink, and strictly below one private runtime root before filesystem access.
- Output writes use no-follow descriptors and append safely or replace atomically; a caller cannot redirect an artifact through a symlink.
- Client connections accept only credential-free `https://127.0.0.1` endpoints with ports in `1..65535`, and verify a regular private-root certificate file.
- Existing HTX configuration, evidence schemas, no-body-payload rule, and static lifecycle controls remain unchanged.
- A future exact-head hosted analysis must show zero new issues and zero New-Code duplicate lines.

## Implementation decision and rationale

The shared Parent `runtime_path_utils.py` layer verifies one private root, opens parent directories without following links, and reads or writes only regular files through descriptors. HAProxy and Envoy retain small connector-local facades, including their existing JSON serialization and evidence formats, rather than copying the descriptor protocol.

The common atomic writer creates `0600` temporary files through the opened parent descriptor, rechecks the destination as regular immediately before `replace`, and removes only a temporary name that it successfully created. A collision with an existing temporary name is retried without deleting that pre-existing file.

The helper now requires `--runtime-root` for each artifact-bearing command, and the shell runner validates that root before its first own write.

For each run the runner creates a short-lived `127.0.0.1` certificate and private bundle only under that root; HAProxy binds the TLS frontend to the bundle, while the client trusts the separate regular certificate file through an explicit Python TLS-client context requiring certificate verification and TLS 1.2 or later.

A command map and a separate release wait preserve behavior while removing the two current complexity rows.

## Changed files

- `ci/lib/runtime_path_utils.py` — shared descriptor-confined private-root artifact primitives for the Parent harnesses.
- `connectors/haproxy/harness/runtime_artifacts.py` — HAProxy-compatible facade over the shared artifact primitives.
- `connectors/envoy/harness/envoy_smoke_helper.py` — Envoy-compatible facade over the shared primitives while preserving JSON/event serialization.
- `connectors/haproxy/harness/haproxy_htx_smoke_helper.py` — root-bound paths, TLS-only loopback client endpoints with certificate verification, and lower-complexity command dispatch.
- `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` — validates the runtime root before writes, creates a private per-run TLS certificate/bundle, and supplies it to every artifact command.
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py`, `tests/test_haproxy_htx_transaction_id.py`, and `tests/test_runtime_artifact_utils.py` — updated call contract and negative outside-root, symlink, no-follow, nonregular-target, atomic-recheck, collision-cleanup, and non-loopback tests; the metadata-event test now binds its temporary private root before using it.
- This English/German Change Record pair and indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_htx_transaction_id` | passed: 3 transaction-ID, outside-root, symlink, loopback-TLS, and runner-root controls. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_runtime_artifact_utils tests.test_haproxy_htx_transaction_id tests.test_envoy_transport_hardening_contract tests.test_runtime_path_security` | passed: 42 shared-helper, HAProxy, Envoy, loopback-TLS, private-root, descriptor, atomic-recheck, and collision-cleanup controls. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m py_compile` for the changed helpers and focused tests | passed. |
| Focused direct temporary-root metadata-event control using `haproxy_htx_smoke_helper.py` | passed: metadata-only event and host evidence are written below the bound private root. |
| Static AST binding control for `test_event_contains_only_metadata` | passed: its loaded `root` is bound locally before use. |
| Focused temporary TLS server and helper-client regression | passed: a verified `https://127.0.0.1` certificate chain succeeds; `http` is rejected before a client connection. |
| `sh -n` and `shellcheck` on the runtime shell runner | passed. |
| `make check-haproxy-htx-overlay` | passed: existing HTX lifecycle and host-action source contract remains satisfied. |
| `make check-haproxy-common-adoption` | passed. |
| `make check-envoy-common-adoption` | passed. |
| HAProxy GCC C17 lint and C23 advisory checks | not rerun after the one-line Python test repair; no C source changed. |
| `git diff --check` | passed. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_bilingual_docs` | passed: 21 bilingual-documentation checker tests. |
| `make check-bilingual-docs` | blocked_environment: the Change Record identity mismatch is repaired; remaining failures are only links into the deliberately uninitialized Framework submodule. |
| `make check-doc-links` | blocked_environment: every reported missing target is inside the deliberately uninitialized Framework submodule. |
| `tests.test_runtime_path_policy` | blocked_environment: its shell self-test sources the deliberately uninitialized Framework `ci/lib/common.sh`; this is not a failure of the shared Parent artifact helper. |
| `ruff` and `pyright` | not_run: neither executable nor module is present in the selected Parent virtual environment; no tool provisioning is authorized for this remediation. |

## Security impact

The harness processes CLI paths and opens loopback sockets.

A private-root invariant now precedes every dynamic artifact sink or source; final files are opened with `O_NOFOLLOW`, and writers require regular files. The common primitive keeps descriptor-relative append, `0600` modes, same-directory atomic replacement, and cleanup confined to successfully created temporary names.

Envoy now also rechecks a pre-existing destination as regular immediately before its descriptor-relative replacement, matching the stronger HAProxy contract. The change does not claim directory `fsync` crash durability.

The smoke client now permits only local `https://127.0.0.1` and verifies the per-run certificate before it exchanges HTTP data with HAProxy. A caller cannot select either a remote destination or clear-text transport.

No authorization, validation, isolation, evidence redaction, Quality Gate, or CI control is weakened.

## Runtime evidence

Focused tests prove the path and URL contracts. Static HTX controls prove that the harness still expresses its existing lifecycle requirements.

They are not a live HAProxy/libmodsecurity runtime result and make no promotion claim.

## Known limitations

- The worktree has no initialized Framework submodule, so the complete focused HTX helper test cannot load its Framework synchronized-upstream fixture locally. Its syntax compiles; the independent Parent transaction-ID/security test and direct metadata-event control are the strongest runnable focused controls.
- The HAProxy-to-Python upstream remains a separate private local backend. This record claims only the repaired client-to-HAProxy TLS boundary; a different deployment topology needs its own upstream-transport review.
- The previous exact head was blocked only by SonarQube Cloud New-Code duplication; the shared extraction and its new direct controls require a fresh exact-head hosted analysis before any merge claim.

## Remaining risks

The root is private to the invoking user. A future cross-user artifact producer needs a new ownership and descriptor-protocol review rather than a broader root.

## Checks not run and rationale

No live HAProxy/libmodsecurity HTX runtime or complete Framework-backed helper test was run because the version-pinned HAProxy build and Framework fixture are absent from this temporary worktree.

The HAProxy GCC C17 lint and C23 advisory checks were not rerun after the one-line Python test repair because no C source changed.

The source and focused Parent controls above are the strongest available local evidence.

## Final diff and review status

The candidate is confined to Parent common-path and HAProxy/Envoy harness code plus bilingual traceability.

The original candidate was committed and published as PR #182. This local follow-up synchronizes it with `200712b4dcede1caccc753a572e1e754a5de3e8b`, repairs the metadata-event test binding, and reruns the focused local controls stated above.

The prior refreshed candidate was pushed as PR #182 head `85995befd19dcac4ab159ec05ee511b891981296`; its GitHub Actions passed but SonarQube Cloud rejected 36 duplicate New-Code lines in the newly added HAProxy artifact module. This local shared-helper follow-up has not yet been pushed, hosted-verified, reviewed, or merged. A new exact-head GitHub Actions and SonarQube Cloud cycle remains required before integration.
