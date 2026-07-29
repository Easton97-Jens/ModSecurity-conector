# Change Record: Parent HAProxy HTX runtime-artifact containment

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-htx-runtime-artifact-containment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-htx-runtime-artifact-containment |
| Date (UTC) | 2026-07-29 |
| Base revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | Current HAProxy HTX harness path, localhost-client, and complexity SonarQube Cloud candidates. |
| Boundary | Parent `connectors/haproxy/` harness, focused Parent tests, and paired indexes only. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

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

`runtime_artifacts.py` builds on the existing Parent runtime-path policy to verify one private root, open parent directories without following links, and read or write only regular files through descriptors.

The helper now requires `--runtime-root` for each artifact-bearing command, and the shell runner validates that root before its first own write.

For each run the runner creates a short-lived `127.0.0.1` certificate and private bundle only under that root; HAProxy binds the TLS frontend to the bundle, while the client trusts the separate regular certificate file through an explicit Python TLS-client context requiring certificate verification and TLS 1.2 or later.

A command map and a separate release wait preserve behavior while removing the two current complexity rows.

## Changed files

- `connectors/haproxy/harness/runtime_artifacts.py` — descriptor-confined private-root artifact helpers.
- `connectors/haproxy/harness/haproxy_htx_smoke_helper.py` — root-bound paths, TLS-only loopback client endpoints with certificate verification, and lower-complexity command dispatch.
- `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` — validates the runtime root before writes, creates a private per-run TLS certificate/bundle, and supplies it to every artifact command.
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` and `tests/test_haproxy_htx_transaction_id.py` — updated call contract and negative outside-root, symlink, and non-loopback tests.
- This English/German Change Record pair and indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `python3 -m unittest tests.test_haproxy_htx_transaction_id` | passed: transaction-ID behavior plus outside-root, symlink, loopback, and runner-root negative controls. |
| `python3 -m py_compile` for both changed helper modules | passed. |
| Focused temporary TLS server and helper-client regression | passed: a verified `https://127.0.0.1` certificate chain succeeds; `http` is rejected before a client connection. |
| `sh -n` and `shellcheck` on the runtime shell runner | passed. |
| `make check-haproxy-htx-overlay` | passed: existing HTX lifecycle and host-action source contract remains satisfied. |
| `make check-haproxy-common-adoption` | passed. |
| HAProxy GCC C17 lint and C23 advisory checks | passed with temporary output below `/var/tmp/codex`. |
| `git diff --check` | passed. |

## Security impact

The harness processes CLI paths and opens loopback sockets.

A private-root invariant now precedes every dynamic artifact sink or source; final files are opened with `O_NOFOLLOW`, and writers require regular files.

The smoke client now permits only local `https://127.0.0.1` and verifies the per-run certificate before it exchanges HTTP data with HAProxy. A caller cannot select either a remote destination or clear-text transport.

No authorization, validation, isolation, evidence redaction, Quality Gate, or CI control is weakened.

## Runtime evidence

Focused tests prove the path and URL contracts. Static HTX controls prove that the harness still expresses its existing lifecycle requirements.

They are not a live HAProxy/libmodsecurity runtime result and make no promotion claim.

## Known limitations

- The worktree has no initialized Framework submodule, so the focused HTX helper test cannot load its Framework synchronized-upstream fixture locally. Its syntax compiles; the independent Parent transaction-ID/security test is the strongest runnable focused control.
- The HAProxy-to-Python upstream remains a separate private local backend. This record claims only the repaired client-to-HAProxy TLS boundary; a different deployment topology needs its own upstream-transport review.
- Hosted checks and a fresh exact-head SonarQube Cloud analysis are pending.

## Remaining risks

The root is private to the invoking user. A future cross-user artifact producer needs a new ownership and descriptor-protocol review rather than a broader root.

## Checks not run and rationale

No live HAProxy/libmodsecurity HTX runtime or complete Framework-backed helper test was run because the version-pinned HAProxy build and Framework fixture are absent from this temporary worktree.

The source and focused Parent controls above are the strongest available local evidence.

## Final diff and review status

The candidate is confined to the Parent HAProxy harness and bilingual traceability.

Local validation is complete for the implemented path, TLS loopback-client, and complexity repairs.

It is not committed, pushed, published, hosted-verified, or merged at record authoring.
