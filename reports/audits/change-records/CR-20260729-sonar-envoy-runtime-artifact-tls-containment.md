# Change Record: Parent Envoy runtime-artifact containment and loopback TLS

**Language:** English | [Deutsch](CR-20260729-sonar-envoy-runtime-artifact-tls-containment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-envoy-runtime-artifact-tls-containment |
| Date (UTC) | 2026-07-29 |
| Base revision | `5bf35f7f50f2ff9ed8b17f538d8043b3909b945b` |
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

## Changed files

- `connectors/envoy/harness/envoy_smoke_helper.py` — root-confined artifact
  helpers, verified loopback TLS client paths, and smaller command/evidence
  functions.
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` — private
  certificate generation, TLS listener wiring, and root arguments for every
  artifact-bearing helper call.
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in` and
  `connectors/envoy/config/prepare_envoy_ext_proc_config.sh` — required
  certificate/key placeholders and downstream TLS transport socket.
- `connectors/envoy/Makefile` and `connectors/envoy/build/test_ext_proc.sh` —
  temporary certificate/key configuration plumbing and generated-config
  assertions.
- `tests/test_envoy_transport_hardening_contract.py` — real temporary TLS
  legitimate controls plus plaintext, remote-host, credential, outside-root,
  and symlink-descendant negative controls.
- `scripts/generate_compiler_guides.py`, generated English/German Envoy
  compiler guides, `examples/envoy/README.md`, and
  `examples/envoy/README.de.md` — valid private TLS materialization examples.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `python3 -m unittest tests.test_envoy_transport_hardening_contract` | passed; ten focused tests exercised real temporary TLS probe, client-cancel, and phase-4 paths plus negative path and endpoint controls. |
| `python3 -m py_compile connectors/envoy/harness/envoy_smoke_helper.py tests/test_envoy_transport_hardening_contract.py` | passed. |
| `sh -n connectors/envoy/harness/run_envoy_ext_proc_runtime.sh connectors/envoy/config/prepare_envoy_ext_proc_config.sh` | passed. |
| `shellcheck -S error` on the changed Envoy shell scripts | passed; pre-existing advisory diagnostics were not converted into an Error-level failure. |
| `make -C connectors/envoy … prepare-envoy-ext-proc-config` with a temporary `BUILD_ROOT` | passed; output contains the TLS transport socket and the expected certificate/key paths. |
| `make -C connectors/envoy … test-envoy-ext-proc` with temporary Go caches | Go package tests passed; the later Common/libmodsecurity step is blocked by the absent Framework rule file. |
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
certificate and observed the intended client paths. Config materialization
produced the Envoy downstream TLS transport socket. These controls are not a
full Envoy plus ext_proc plus libmodsecurity runtime; no production topology or
full-lifecycle promotion is claimed.

## Known limitations

- No `envoy` binary is installed in this environment, so an Envoy config
  validation or full ext_proc runtime smoke cannot run locally.
- The Framework submodule rule file required by the existing ext_proc test is
  absent; it is not replaced with a local fixture.
- A full Codex Security scan is unavailable in this runtime because its
  required delegated-worker mode is disabled. Focused source-to-sink and
  negative/legitimate controls are the strongest available evidence.

## Remaining risks

- Before integration, the PR's exact current head must independently confirm
  that the fifteen selected SonarQube Cloud candidates are removed without
  new issues or duplication; the hosted PR status, not this historical record,
  is the evidence for that gate.
- Future Envoy configuration consumers must continue to pass certificate and
  private-key paths; the materializer now rejects their omission.

## Checks not run and rationale

No full Envoy/ext_proc/libmodsecurity runtime, Envoy binary validation, or
complete connector matrix was run because the required Envoy binary and
Framework rule fixture are unavailable locally. Hosted Actions, SonarQube
Cloud analysis, review/thread state, and the merge operation are delivery
evidence read from the PR at its exact current head immediately before
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
and the required bilingual traceability/documentation. This record captures
the final versioned source/documentation scope, local controls, and runtime
limitations. Delivery evidence is deliberately obtained from the PR's exact
current head immediately before any integration; it is not self-asserted for
later documentation or lifecycle commits. No `master` merge is recorded by
this Change Record.
