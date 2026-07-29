# Change Record: Parent Envoy runtime-artifact containment and loopback TLS

**Language:** English | [Deutsch](CR-20260729-sonar-envoy-runtime-artifact-tls-containment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-envoy-runtime-artifact-tls-containment |
| Date (UTC) | 2026-07-29 |
| Base revision | `964630d34d0b87e9066d03131e445eeb3677956d` |
| Tracking | Fifteen current SonarQube Cloud candidates in `connectors/envoy/harness/envoy_smoke_helper.py`: `pythonsecurity:S8703` ×3, `pythonsecurity:S8707` ×6, `python:S5332` ×1, and five cognitive-complexity rows. |
| Boundary | Parent Envoy harness, configuration materializer/template, connector test, required reader-facing documentation, and paired Change Record indexes. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

## Motivation and problem statement

The Envoy ext_proc smoke helper accepted CLI-controlled URLs, host/port pairs,
and evidence paths at network and filesystem sinks. Its runner served the
downstream listener over clear-text HTTP. Lexical absolute-path checks do not
prove private runtime-root containment, and a loopback-only HTTP endpoint still
does not provide transport confidentiality or integrity.

## Acceptance criteria

- Every helper-created or helper-read runtime artifact is an absolute,
  non-symlink descendant of one verified private runtime root and is accessed
  through descriptor-safe read/write operations.
- Envoy smoke client endpoints are credential-free HTTPS on exactly
  `127.0.0.1`, use a certificate-verifying client context, and require TLS 1.2
  or later.
- The generated Envoy listener uses the per-run private certificate and key;
  ordinary phase, probe, and client-cancel evidence remains payload-free.
- Existing legitimate loopback probes, phase-4 barrier behavior, and optional
  client-cancel behavior continue to work in focused temporary TLS tests.
- The generated Envoy 1.38 configuration uses the current typed upstream
  HTTP/2 and Admin/FileAccessLog APIs rather than deprecated fields, without
  broadening the listener or persisting an admin access log.
- Startup-readiness requests use a transaction identity distinct from the one
  bound to the P1 legitimate control, so retries cannot create ambiguous
  completion evidence for that control.
- Config materialization, tests, English/German documentation, and the hosted
  analysis for the PR's exact current head must preserve zero New-Code issues
  and duplicate lines before integration.

## Implementation decision and rationale

The helper reuses the Parent `runtime_path_utils` private-root policy and adds
no-follow descriptor helpers for JSON and JSONL artifacts. The `probe`,
`client-cancel`, and phase-4 client paths now reject non-loopback, plaintext,
credential-bearing, fragmented, and invalid-port targets before a network
sink. The runner creates a one-day self-signed SAN certificate only below its
verified private root, supplies it to Envoy's downstream TLS transport socket,
and uses the matching certificate as the Python client trust anchor.

The standard-library Python upstream remains an internal loopback fixture
behind Envoy. This change makes no claim that it models a production upstream
TLS topology. The optional full-lifecycle evidence handoff remains supported
only through a separately verified private output root outside the checkout;
it never accepts an arbitrary output path.

Native Envoy 1.38 validation identified deprecated
`Cluster.http2_protocol_options`, `Admin.access_log_path`, and the old
FileAccessLog formatting path in the rendered configuration. The template now
uses the documented `HttpProtocolOptions` typed extension for the ext_proc
gRPC upstream and a `FileAccessLog` with an empty current-format field writing
to `/dev/null`. This preserves explicit upstream HTTP/2 and the prior
no-persisted-admin-log behavior.

The first exact-head rerun also showed that a retrying readiness probe could
reuse the P1 allow transaction ID. The evidence binder correctly rejected two
otherwise valid completions with that same ID. The runner now uses a separate
readiness ID and evidence receipt, then performs exactly one dedicated P1
allow probe for the causal binding.

## Changed files

- `connectors/envoy/harness/envoy_smoke_helper.py` — root-confined artifact
  helpers, verified loopback TLS client paths, and smaller command/evidence
  functions.
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` — private
  certificate generation, TLS listener wiring, root arguments for every
  artifact-bearing helper call, and separate readiness/P1-control identities.
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in` and
  `connectors/envoy/config/prepare_envoy_ext_proc_config.sh` — required
  certificate/key placeholders, downstream TLS transport socket, and current
  Envoy 1.38 upstream/Admin logging fields.
- `connectors/envoy/Makefile` and `connectors/envoy/build/test_ext_proc.sh` —
  temporary certificate/key configuration plumbing and generated-config
  assertions.
- `tests/test_envoy_transport_hardening_contract.py` — real temporary TLS
  legitimate controls plus plaintext, remote-host, credential, outside-root,
  and symlink-descendant negative controls; it also pins the non-deprecated
  Envoy template shape and the distinct readiness/P1 transaction identities.
- `scripts/generate_compiler_guides.py`, generated English/German Envoy
  compiler guides, `examples/envoy/README.md`, and
  `examples/envoy/README.de.md` — valid private TLS materialization examples.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| Isolated `python -m unittest -v` for Envoy transport, compiler-guide, and bilingual-documentation contracts | passed; 54 tests, including twelve focused tests for real temporary TLS probe, client-cancel, phase-4 paths, negative endpoint/path controls, the current Envoy 1.38 template fields, and unambiguous readiness/P1 identities. |
| `sh -n` on the ext_proc runner, template materializer, and ext_proc test script | passed. |
| Isolated `make -C connectors/envoy build-envoy-ext-proc` with Go 1.26.5 and the verified host libmodsecurity headers/library | passed; module verification and the Go processor package tests passed. |
| Isolated `make -C connectors/envoy runtime-smoke-envoy-ext-proc` with Envoy 1.38.2, the Parent-Gitlink-pinned no-CRS rule file, and loopback TLS | passed; Envoy accepted the generated configuration without deprecation diagnostics and the full bounded smoke summary is `PASS` / non-promoted. |
| `make check-envoy-common-adoption` | passed. |
| `git diff --check` | passed. |

## Security impact

This change is at a network-client, local-listener, filesystem-artifact, and
runtime-evidence boundary. It removes clear-text client-to-Envoy transport,
rejects remote/credential-bearing endpoints, and confines dynamic artifacts to
private no-symlink roots. TLS verification is explicit (`ssl.PROTOCOL_TLS_CLIENT`,
certificate verification, private trust anchor, and minimum TLS 1.2). The
change does not weaken validation, logging, evidence, Quality Gates, or any
CI control.

## Runtime evidence

Focused Python controls started real local TLS servers with a temporary SAN
certificate and observed the intended client paths. In addition, the exact
candidate was built with Go 1.26.5 against the verified host libmodsecurity
installation and exercised by the official Envoy 1.38.2 binary over loopback
TLS. The read-only no-CRS fixture came from the Parent-pinned Framework
revision. Envoy accepted the materialized configuration with no warning,
deprecation, error, or fatal diagnostic. The bounded runtime observed the
legitimate P1 `200`, streamed `200`, P1/P2/P3 denials `403`, P3 redirect
`302`, all phase-4 safe/barrier controls `200`, request and response streaming,
and `processes_stopped=yes`. The dedicated P1 transaction has exactly one
normal completion. The run remains `common_libmodsecurity_nonpromoted` with
`capability_promotion=not_permitted`; it does not claim production readiness.

## Known limitations

- The smoke is an isolated loopback HTTP/1.1 downstream proof. It does not
  cover production network topology, HTTP/2 or HTTP/3 downstream traffic, or
  the complete connector matrix.
- The optional cancellation diagnostic was intentionally not executed and is
  neither promoted nor used to infer a client/upstream reset cause.
- The Framework input is read only at the Parent-pinned revision; this change
  neither modifies Framework/MRTS nor substitutes a locally invented rule
  fixture.

## Remaining risks

- Before integration, the PR's new exact head must independently confirm that
  the selected SonarQube Cloud candidates remain removed without new issues or
  duplication; the hosted PR status, not this local record, is the evidence
  for that gate.
- Future Envoy configuration consumers must continue to pass certificate and
  private-key paths; the materializer now rejects their omission.

## Checks not run and rationale

No production deployment, complete connector matrix, downstream HTTP/2/HTTP/3
exercise, or enabled cancellation diagnostic was run. Each is outside this
bounded loopback proof and must not be inferred from it. Hosted Actions,
SonarQube Cloud analysis, review/thread state, and the merge operation remain
delivery evidence read from the PR at its exact current head immediately before
integration. This record makes no assertion for a future head and records no
`master` merge.

## Hosted-feedback follow-up

The initial exact PR head `b4401deec9bce94a806dd56f1cc0215431881f93` received
an `OK` SonarQube Cloud Quality Gate with 0.0% New-Code duplication but five
task-owned new Code Smells: two duplicated literals and three exception-test
forms. Its push-triggered `scaffold-lint` run also failed because the generated
Envoy compiler guide did not list the newly used `TLS_CERTIFICATE` and
`TLS_PRIVATE_KEY` placeholders; the OpenSSL `CN` and `subjectAltName` tokens
are fixed option names, not placeholders. The focused follow-up extracts the
literals, precomputes exception-test arguments, documents the two variables in
both generated guides, and makes the placeholder test distinguish fixed
OpenSSL option names. The 52 focused Envoy transport, compiler-guide, and
bilingual tests pass locally. Follow-up commit
`1b6cc0372f6d5b9ba175fc9e22b61e3ba84bd0c5` completed its exact-head hosted
cycle successfully; no failure was waived or marked accepted.

## Final diff and review status

The candidate is restricted to the Parent Envoy connector, its direct tests,
and the required bilingual traceability/documentation. It contains no
Framework/MRTS/Gitlink, workflow, Sonar-configuration, suppression, or
`master` modification. This record captures the versioned source/documentation
scope, the non-deprecated Envoy configuration, local controls, and runtime
limitations. Delivery evidence is deliberately obtained from the PR's exact
current head immediately before any integration; it is not self-asserted for
later documentation or lifecycle commits. No `master` merge is recorded by
this Change Record.
