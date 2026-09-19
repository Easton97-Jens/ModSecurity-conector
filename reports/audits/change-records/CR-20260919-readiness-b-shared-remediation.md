# Change Record CR-20260919-readiness-b-shared-remediation: shared readiness-B remediation

**Language:** English | [Deutsch](CR-20260919-readiness-b-shared-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260919-readiness-b-shared-remediation |
| Date (UTC) | 2026-09-19 |
| Base revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Scope | Parent-only shared connector remediation, directly affected tests and paired documentation. No Framework, MRTS, Gitlink, dependency, rule-profile, scanner, Quality Gate, workflow, or merge change is included. |
| Delivery status | Final local candidate in the dedicated worktree, ready for a task-owned initial commit and Draft-PR submission. The exact commit and PR identity are recorded only after they are observed; no hosted check, review result, or merge is asserted here. |
| Policy resolution | The Parent traceability policy requires this paired record for the non-trivial versioned work; the established archive index is updated. |

## Motivation and problem statement

The requested ten-integration readiness review exposed shared remediable gaps
without providing sufficient complete runtime evidence to promote every path to
practice maturity B. This change applies narrow Parent-owned corrections while
retaining the distinction between source/contract evidence and full host,
protocol, rule-profile, restart, lifecycle, and observability evidence.

## Acceptance criteria

1. Resolve the scoped Parent-owned correctness and provenance gaps without
   weakening fail-closed, ownership, or endpoint-validation controls.
2. Keep immutable Expat revision selection, archive extraction ownership,
   Apache APXS output placement, and peer/local endpoint provenance explicit
   and testable.
3. Maintain complete English/German documentation and this paired Change
   Record.
4. Report the actual maturity state truthfully: this scoped remediation alone
   does not demonstrate practice maturity B for all ten paths.

## Implementation decision and rationale

- Require the Expat component resolver to use immutable full Git object IDs in
  both strict and non-strict paths; mutable references and newest-release
  substitution are not accepted as pin evidence.
- Force `TAR_OPTIONS="--no-same-owner"` for NGINX source extraction so archive
  metadata cannot change ownership during a non-root handoff.
- Stage Apache APXS profile-registry inputs beneath a caller-provided external
  build root. The wrapper rejects checkout/root symlinks and a pre-existing
  symlinked `connectors` stage child before copying generated inputs.
- Derive stock Lighttpd client/server endpoint metadata from the accepted
  sidecar TCP socket with `getpeername` and `getsockname`; Unix-domain sockets
  and unusable endpoints are rejected rather than using request-host metadata.
- Derive the native Traefik server endpoint from `http.LocalAddrContextKey`;
  request `Host` remains request metadata and is not trusted as the local
  engine endpoint.

## Security impact

This work affects supply-chain pinning, archive ownership, external build
output boundaries, and untrusted HTTP endpoint provenance. The corrections
retain fail-closed behavior on unavailable or malformed endpoints and prevent
request-controlled host metadata from becoming a local UDS/engine endpoint.
They do not close the separately tracked same-UID UDS pathname-replacement
risk (`FND-PARENT-0015`), and they do not establish effective rule-profile
coverage for the 2026 `t:hexDecode` advisory condition.

## Changed files

- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/apache/build/apxs-wrapper.in`
- `connectors/apache/README.md`
- `connectors/apache/README.de.md`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/README.de.md`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`
- `connectors/traefik/native_middleware/middleware_test.go`
- `connectors/traefik/native_middleware/README.md`
- `connectors/traefik/native_middleware/README.de.md`
- `docs/reference/variables.md`
- `docs/reference/variables.de.md`
- `tests/test_prepare_runtime_components.py`
- `tests/test_apache_request_transaction_cleanup.py`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `reports/audits/change-records/CR-20260919-readiness-b-shared-remediation.md`
- `reports/audits/change-records/CR-20260919-readiness-b-shared-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Tests and actual local results

| Check | Actual result |
| --- | --- |
| `tests.test_prepare_runtime_components` | Passed: 90 tests; five Framework-HEAD mismatch cases were skipped. |
| `tests.test_apache_request_transaction_cleanup` | Passed. |
| `tests.test_apache_apxs_profile_registry_staging` | Passed: 5 cases. |
| Final Apache Autotools host run after hardening with the cached non-root Apache/libModSecurity inputs | Passed locally: module load, allow/block behavior, and the documented transaction-ID controls completed. This is bounded local host evidence, not evidence for every connector or protocol path. |
| HAProxy SPOP-to-HTX combined bounded host run | Passed locally as a non-root, isolated path using the source-built current SPOP adapter and HAProxy HTX. It is bounded evidence for that combined path, not standalone HTX evidence or full B-class G2–G6/54-case evidence. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` with `CC=clang` | Passed: 18 tests. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` with `CC=cc` | Passed: 18 tests. |
| Native Traefik Go module `go test -mod=readonly ./...` | Passed. |
| Native Traefik `go vet ./...` and `gofmt -d` review | Passed; `gofmt -d` produced no diff. |
| Native Traefik `FuzzUDSFrameAndResult` for 15 seconds | Passed. |
| `git diff --check` during the scoped implementation | Passed. |
| `make check-variable-documentation` | Passed: 100 documented variable references scanned. |
| `make check-bilingual-docs` and `make check-doc-links` | Blocked by the unmaterialized Framework Gitlink only; every emitted target is under `modules/ModSecurity-test-Framework`. |

## Commands executed

All commands were run through the repository RTK proxy. The observed local
validation included the focused Python selections
`tests.test_prepare_runtime_components`,
`tests.test_apache_request_transaction_cleanup`, and
`tests.test_apache_apxs_profile_registry_staging`; the Apache Autotools
bootstrap check; `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
with `CC=clang` and `CC=cc`; and the native Traefik commands
`go test -mod=readonly ./...`, `go vet ./...`, `gofmt -d`, and the 15-second
`FuzzUDSFrameAndResult` run. The executed HAProxy host control was
`connectors/haproxy/harness/combined_spop_htx/run_combined_spop_htx.sh` using
an isolated non-root runtime root and the current SPOP-to-HTX combined path.
`git diff --check` and `make check-variable-documentation` passed during
scoped work. The repository-wide bilingual/link targets were run but are
blocked only by the separately owned, unmaterialized Framework Gitlink. The
table above records the actual observed outcomes; no unobserved hosted or
production command is represented as executed.

## Runtime evidence

The final Apache bootstrap and HAProxy SPOP-to-HTX combined runs are actual
local non-root host evidence within their bounded fixtures. The HAProxy run
does not rerun standalone HTX and does not cover the full B-class G2–G6 or
54-case matrix. The Lighttpd and Traefik results are source, contract, and Go
module evidence; they are not substitutes for an independently started
production host with the required rules, lifecycle controls, logs, metrics,
restart, HTTP/1.1, HTTP/2, and HTTP/3 evidence. No assertion is made that all
ten integration paths now have B-class runtime evidence.

## Checks not run and rationale

- A complete ten-path evidence matrix, including all required protocol and
  lifecycle dimensions, is not complete at this record snapshot.
- Effective external rule-profile testing for the `t:hexDecode` advisory
  condition is not run; checked-in source inspection cannot prove deployed
  rule usage.
- Full host evidence for NGINX, both Envoy paths, standalone HAProxy HTX,
  Traefik forwardAuth, stock Lighttpd, and patched Lighttpd is not asserted
  here. The combined HAProxy SPOP-to-HTX run remains short of full B-class
  G2–G6 and 54-case evidence.
- Exact-head hosted CI, SonarQube Cloud, review, mergeability, and PR results
  are not yet available and must not be inferred from local checks. The
  repository-wide bilingual/link target preconditions are likewise blocked by
  the separately owned unmaterialized Framework Gitlink.

## Known limitations

The requested outcome—evidenced B maturity for all ten integration paths—is
unachieved at this snapshot. The corrections address only the listed shared
gaps. FND-PARENT-0015 remains open, host/runtime prerequisites remain blocked
or unverified for several paths, and the effective rule profile needed to
evaluate the `t:hexDecode` condition has not been supplied.

## Remaining risks

The corrected endpoint handling cannot itself prove that every embedding host
supplies a trustworthy local address. The local-address validation therefore
fails closed. Archive and APXS corrections do not replace a fresh host build
under each supported deployment configuration. No vulnerable/affected status
is claimed for the advisory condition without the actual enabled rule profile.

## Final diff and review status

This is a partial, Parent-only remediation record. It describes observed local
evidence and known limits but does not certify the ten-path B objective, a
release, a hosted quality result, a pull request, or a merge. The final scoped
diff and source-local documentation checks are reconciled; repository-wide
documentation targets are truthfully blocked by the missing Framework
Gitlink. The exact commit/PR facts will be added after they are observed, and
the remaining runtime evidence remains a follow-up requirement.
