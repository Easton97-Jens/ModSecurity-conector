# Change Record: Parent Envoy TLS and maintainability remediation

**Language:** English | [Deutsch](CR-20260801-sonar-envoy-tls-maintainability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-envoy-tls-maintainability` |
| Date (UTC) | 2026-08-01 |
| Base revision | `3ff87de53df34cecbc9c6489c858e64bdf3fd198` |
| Tracking | Five current master rows below `connectors/envoy/`: `go:S3776` `AZ9cRyqvHhV2CayPTP0G`, `godre:S8193` `AZ9cRyq6HhV2CayPTP0I` and `AZ9cRyq6HhV2CayPTP0J`, `godre:S8196` `AZ9cRyqvHhV2CayPTP0H`, and `python:S5332` `AZ9MwivX-bUaKQ_zSGAh`; plus PR-specific `python:S1192` `AZ-8cqgs_sm3M2mrbmAj`, discovered by the first exact-head analysis. |
| Boundary | Parent Envoy processor, smoke-helper, Envoy fixture configuration, focused Parent tests, and this paired Change Record/index documentation only. Framework, MRTS, and gitlinks remain unchanged. |

## Motivation and problem statement

The current Envoy component has four maintainability rows and one security row.
The processor metadata decoder exceeds the cognitive-complexity threshold, a
single-method interface is not named with the Go `-er` convention, and two
test-only values are unnecessary. The upstream fixture server still accepts
cleartext HTTP even though the downstream client probes already require
certificate-verified loopback HTTPS.

The first exact-head analysis also identified one task-owned new
`python:S1192` row because the TLS certificate label was introduced as a
duplicate literal. It is remediated immediately through named constants; no
suppression or baseline change is used.

## Acceptance criteria

- All six listed rows have repository-native source remediations without a
  scanner suppression, `NOSONAR`, Quality Gate change, rule exclusion, or
  external false-positive disposition.
- Request pseudo-header/attribute mapping, bounded metadata errors, response
  commit bookkeeping, and trailer handling retain their current semantics.
- The fixture accepts only TLS 1.2-or-newer connections using regular,
  runtime-root-confined certificate and private-key files; Envoy validates the
  same per-run certificate on its upstream hop.
- The focused Go, C17/native, shell, TLS positive, TLS plaintext-negative,
  symlink-negative, and documentation controls pass before delivery.
- A Draft PR receives fresh exact-head GitHub and SonarQube Cloud evidence
  before any merge decision.

## Implementation decision and rationale

`requestMetadataFromEnvoy` now applies text and port attributes through small
typed helpers and assignment tables. The header mapping remains in its
existing owner, while the helpers preserve absent values and return the same
bounded-input errors. `ResponseCommitter` states the one-method capability in
the standard Go form; the existing Common Runtime test continues to exercise
that assertion. The two trailer assertions invoke their expressions directly.

The fixture server now uses `http.server.ThreadingHTTPSServer` rather than a
plain HTTP server. It accepts only regular certificate and key files confined
below the already-validated private runtime root, then sets TLS 1.2 as its
minimum protocol. Both Envoy runtime launchers pass the ephemeral pair to the
fixture. Both local Envoy templates configure `UpstreamTlsContext` with the
per-run certificate as `trusted_ca`, so the Envoy-to-fixture hop is encrypted
and certificate-validated as well.

The certificate and private-key diagnostic labels are named once and reused
across the client and server validation paths, removing the PR-specific
duplicate-literal row without changing any validation or error meaning.

## Changed files

- `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- `tests/test_envoy_transport_hardening_contract.py`
- `reports/audits/change-records/README.md`, `README.de.md`, and this
  English/German Change Record pair.

## Commands executed

| Command or procedure | Result |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_envoy_transport_hardening_contract` | passed: 17 tests, including the regular-file legitimate control and the symlink alternate-bypass rejection. |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go test -mod=readonly ./...` in `connectors/envoy/ext_proc` with task-owned `GOPATH`, `GOMODCACHE`, and `GOCACHE` | passed. |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go vet -mod=readonly ./...` in `connectors/envoy/ext_proc` with the same task-owned paths | passed. |
| `ENVOY_EXT_PROC_COMMON_TEST=1 ... CFLAGS=-std=c17 sh connectors/envoy/build/build_ext_proc.sh` with the installed libmodsecurity headers/library and task-owned build/cache paths | passed: module verification, processor tests, strict C17 Common bridge build, and ext_proc binary build. |
| `shellcheck -S error -x` and `sh -n` for the two changed runtime launchers and the ext_proc config materializer | passed. |
| `gofmt -d` for the changed Go files | passed with no output. |
| Direct task-owned fixture smoke using `serve-upstream`, a one-day loopback certificate, and `probe` | passed: the HTTPS legitimate control returned `200`; a direct plaintext `http://127.0.0.1` request was rejected. |
| `check-bilingual-docs.py` with the repository Python | blocked only by 20 pre-existing missing links into the unpopulated Framework gitlink; it reported no record-pair or structural error for this change. |
| Focused transport contract and `py_compile` after the `python:S1192` follow-up | passed: 17 tests and Python syntax compilation. |

## Security impact

The relevant boundary is the Envoy-to-local-fixture upstream hop. The fixture
now rejects a certificate/key path outside its private runtime root or through
a final symlink, accepts only a regular in-root pair, and does not expose a
cleartext HTTP listener. The Envoy configuration trusts that ephemeral
certificate only for this loopback upstream and does not add any public
listener, redirect, insecure TLS override, path acceptance, scanner
suppression, or Quality Gate change. The downstream HTTPS-only probe policy,
bounded metadata handling, response-commit boundary, and event-redaction
controls remain intact.

## Runtime evidence

No promotion-grade runtime evidence is collected or claimed. The task-owned
loopback smoke constructed a self-signed certificate with an IP SAN for
`127.0.0.1`, started the changed helper, completed a certificate-verifying
HTTPS request, and rejected a cleartext HTTP request; it is recorded as a
focused local test rather than a substitute for an Envoy runtime matrix. The
focused transport contract also checks a symlinked key path as an alternate
bypass class while preserving the valid regular-file control.

## Known limitations

No complete Envoy process/runtime matrix, production deployment, HTTP/2 or
HTTP/3 downstream run, Framework test, or MRTS test was run. This is a
Parent-only Envoy-local remediation; none of those sources changed.

## Checks not run and rationale

The real pinned Envoy binary is not available locally, so an Envoy
configuration-load/runtime execution could not be run. The full connector
matrix is outside this connector-local source change. Hosted GitHub Actions,
review state, and SonarQube Cloud analysis cannot be checked until the Draft
PR exists at its exact remote head. The full bilingual checker is blocked by
20 existing links into the intentionally unpopulated Framework gitlink; it
does not establish a problem in this Parent-only Change Record pair.

## Remaining risks

The six task-associated source rows are externally closed only when SonarQube Cloud
analyses the exact PR head and reports no task-owned new issue or duplication.
The local TLS smoke demonstrates the helper boundary, but it is not a
substitute for the unavailable pinned Envoy runtime or a full transport matrix.

## Final diff and review status

The candidate remains within the Parent Envoy boundary. It contains no
Framework/MRTS/Gitlink, dependency, workflow, scanner-configuration,
suppression, or `master` modification. Local source and focused security
validation are complete. The repository bilingual checker reached only its
pre-existing missing-Framework-link blocker; final diff review, commit, push,
Draft PR, and exact-head hosted verification remain pending at record
authoring.
