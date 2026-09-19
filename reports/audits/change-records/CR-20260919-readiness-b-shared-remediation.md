# Change Record CR-20260919-readiness-b-shared-remediation: shared readiness-B remediation

**Language:** English | [Deutsch](CR-20260919-readiness-b-shared-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260919-readiness-b-shared-remediation |
| Date (UTC) | 2026-09-19 |
| Base revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Scope | Parent-only shared connector remediation, directly affected tests and paired documentation. No Framework, MRTS, Gitlink, dependency, rule-profile, scanner, Quality Gate, workflow, or merge change is included. |
| Delivery status | Draft PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370) from `agent/readiness-b-ten-integrations-20260919`; commits `43d9003fc986a36441c9d83bb26e746cfbe10a8c`, `aac89c4f2982d6faf91351fc6809cedfce5c9256`, `466a776347e35405e9875190ae9912a827e56f6a`, and `56b838ce1fe681e47c8fd3df326dccab8a1c4405` were pushed. The remote and PR head were verified at `56b838ce1fe681e47c8fd3df326dccab8a1c4405`; its hosted Apache bootstrap built and loaded the module, but its over-limit harness read interim `100 Continue` from the first header line instead of the final response status. That observation neither proves final `413` nor a source-policy regression. The corrective fallback has local validation; the final-status assertion and its post-fix exact-head hosted rerun remain pending. No review result or merge is asserted here. |
| Policy resolution | The Parent traceability policy requires this paired record for the non-trivial versioned work; the established archive index is updated. |

## Motivation and problem statement

The requested ten-integration readiness review exposed shared remediable gaps
without providing sufficient complete runtime evidence to promote every path to
practice maturity B. This change applies narrow Parent-owned corrections while
retaining the distinction between source/contract evidence and full host,
protocol, rule-profile, restart, lifecycle, and observability evidence.

The exact hosted Apache bootstrap failure now identifies a further
Parent-owned P2 availability defect: its initial Apache directory configuration
reaches the input filter with an unset Common request-body limit/action, so the
Common planner rejects a small body before libModSecurity can evaluate the P2
rule. The correction must preserve a finite, reject-by-default bound rather
than remapping the resulting `413`, treating a zero limit as unlimited, or
accepting an unsupported action.

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
5. For the bounded Apache bootstrap profile, retain distinct small P2 rule
   block (`403`), real over-limit rejection (`413` without handler content),
   and same-process allow follow-up (`200`) controls.

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
- Resolve only Apache input-filter consumption of a zero request-body limit or
  unset/unsupported body-limit action to Common's finite `1048576`-byte default
  and `reject` action. This preserves a merged explicit policy, does not apply
  defaults at per-directory creation, does not expose a new Apache directive
  surface, and does not permit partial inspection.
- Extend the isolated Apache bootstrap fixture with a fixed synthetic P2 body
  marker, `RelevantOnly` serial audit logging limited to `ABFZ`, a raw-marker
  exclusion assertion, a bounded 1049600-byte over-limit body that must return
  `413` before static handler content, and a same-process allow follow-up.
  This is a bounded regression/harness control; it is not proof of the full
  historical FND-1098 terminal sequence or Apache B readiness.
- Replace the timing-dependent stock Lighttpd loopback TCP-reset test with a
  compiled source-contract harness. A static assertion anchors the
  post-`finish_request_body` P2 branch to `sidecar_finish_decision`; the
  harness then invokes that production terminal function with a constructed P2
  decision and asserts the real abort host action, rule correlation, and
  transaction finalization. It does not dynamically execute the full P2
  pipeline.

## Security impact

This work affects supply-chain pinning, archive ownership, external build
output boundaries, and untrusted HTTP endpoint provenance. The corrections
retain fail-closed behavior on unavailable or malformed endpoints and prevent
request-controlled host metadata from becoming a local UDS/engine endpoint.
The new Apache P2 fixture intentionally limits serial audit parts to `ABFZ`
and rejects retention of its fixed synthetic request-body marker. It does not
change the production audit configuration or authorize logging request bodies.
The Apache correction keeps every nonempty body within a finite cap and uses
`reject` for a zero initial limit or unsupported action; it neither creates an
unlimited path nor exposes partial inspection that could forward an uninspected
tail. Focused review found no validated security finding in these bounded
harness and availability changes; the Lighttpd test's constructed decision
remains an explicit evidence limitation.
These corrections do not close the separately tracked same-UID UDS
pathname-replacement risk (`FND-PARENT-0015`), and they do not establish
effective rule-profile coverage for the 2026 `t:hexDecode` advisory condition.

## Changed files

- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/apache/build/apxs-wrapper.in`
- `connectors/apache/src/msc_filters.c`
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
| `tests.test_apache_request_transaction_cleanup` and `tests.test_apache_apxs_profile_registry_staging` after the P2 bootstrap-harness update | Passed: 24 cases, including a static P2/audit/no-raw-marker/follow-up harness contract. |
| `tests.test_apache_request_transaction_cleanup` after the P2 policy fallback and over-limit control | Passed: 21 cases, including finite-default/reject source wiring and marker/over-limit/follow-up harness ordering. |
| `sh -n ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh` | Passed. |
| `ci/checks/connectors/apache/check-apache-common-adoption.py` and `tests.test_apache_common_adoption` | Passed: Apache P2 structure/adoption checks and 12 focused Python cases. |
| `make check-common-helpers-c17` | Passed with the Common body-policy helper smoke in a task-owned external build root. |
| `make check-apache-c17` with `CC=cc` and `CC=clang` | Passed twice with explicit `-std=c17 -Wall -Wextra -Werror` compilation in separate task-owned external output roots. |
| Final Apache Autotools host run after hardening with the cached non-root Apache/libModSecurity inputs | Passed locally: module load, allow/block behavior, and the documented transaction-ID controls completed. This is bounded local host evidence, not evidence for every connector or protocol path. |
| Current Apache P2 bootstrap host control | Blocked before `httpd` start: `chown` of the task-owned non-root runtime directories/files returned `EINVAL` on the current idmapped filesystem. No root-worker substitute was used. |
| HAProxy SPOP-to-HTX combined bounded host run | Passed locally as a non-root, isolated path using the source-built current SPOP adapter and HAProxy HTX. It is bounded evidence for that combined path, not standalone HTX evidence or full B-class G2–G6/54-case evidence. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` with `CC=clang` | Passed: 18 tests. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` with `CC=cc` | Passed: 18 tests. |
| `connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest` after the deterministic P2 delivery-failure replacement | Passed: 19 tests. It statically anchors the post-`finish_request_body` P2 branch and executes the terminal handoff with a constructed decision; it is not a dynamic P2 or Stock-host runtime proof. |
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

The follow-up validation ran `sh -n
ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`, `python3 -m
unittest -v tests.test_apache_request_transaction_cleanup
tests.test_apache_apxs_profile_registry_staging`, and `python3 -m unittest -v
connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest`.
The attempted bounded non-root Apache P2 bootstrap reached configuration syntax
but stopped before server start when the task-owned runtime ownership handoff
returned `EINVAL`; it is recorded as blocked rather than passed.

After the hosted `466a776347e35405e9875190ae9912a827e56f6a` Apache failure,
the follow-up local validation ran `python3 -m unittest -v
tests.test_apache_request_transaction_cleanup`, `sh -n
ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`,
`ci/checks/connectors/apache/check-apache-common-adoption.py`, `python3 -m
unittest -v tests.test_apache_common_adoption`, `make
check-common-helpers-c17`, and `make check-apache-c17` with `CC=cc` and
`CC=clang`. The C outputs and Common helper outputs were directed to the
registered task-owned external run root. All listed local checks passed; none
substitutes for the pending corrected exact-head host run.

The hosted Apache bootstrap at exact head
`56b838ce1fe681e47c8fd3df326dccab8a1c4405` advanced to the over-limit P2
assertion but read `100 Continue` with its first-header-line parser. A large
HTTP/1.1 upload may receive that interim response before its final status, so
this harness observation does not establish whether the final response was
`413` and does not establish a new source-policy failure. The correction keeps
the header and response artifacts but captures curl's final `%{http_code}`;
its exact-head hosted rerun remains required.

## Runtime evidence

The final Apache bootstrap and HAProxy SPOP-to-HTX combined runs are actual
local non-root host evidence within their bounded fixtures. The HAProxy run
does not rerun standalone HTX and does not cover the full B-class G2–G6 or
54-case matrix. The Lighttpd and Traefik results are source, contract, and Go
module evidence; they are not substitutes for an independently started
production host with the required rules, lifecycle controls, logs, metrics,
restart, HTTP/1.1, HTTP/2, and HTTP/3 evidence. No assertion is made that all
ten integration paths now have B-class runtime evidence.

The hosted Apache bootstrap at exact head
`466a776347e35405e9875190ae9912a827e56f6a` built the current module, completed
configuration/module-load checks, and then reproduced the small P2 marker as
`413` rather than `403`. That is real-host negative evidence for the
pre-correction source and identifies the first terminal condition; it is not a
passing Apache runtime claim. The local P2 host attempt remains blocked before
start by `chown(...)=EINVAL`, and the corrected exact-head hosted rerun remains
required. The Lighttpd harness likewise does not dynamically execute
`finish_request_body` or establish the full P2 path.

The following hosted bootstrap at
`56b838ce1fe681e47c8fd3df326dccab8a1c4405` exercised the over-limit request
but stopped its assertion at interim `100 Continue`, rather than the final
response. It is a harness-parsing failure, not evidence that the final result
was `413` and not a refutation of the finite/reject source correction. The
next exact-head hosted run must still verify the final `413`, absence of
handler content, and same-process follow-up.

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
- The pre-correction exact-head hosted Apache check is observed failed; the
  corrected exact-head hosted CI, SonarQube Cloud, review, mergeability, and
  final PR results remain pending and must not be inferred from local checks.
  The repository-wide bilingual/link target preconditions are likewise blocked
  by the separately owned unmaterialized Framework Gitlink.
- The current Apache P2 bootstrap host control is not run to completion because
  the necessary task-root `www-data` ownership handoff fails with `EINVAL` on
  the current idmapped filesystem. A root-worker substitute is prohibited.

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
evidence, a hosted pre-correction failure, and known limits but does not
certify the ten-path B objective, a release, a hosted quality result, or a
merge. The final scoped diff and source-local documentation checks still need
reconciliation after the pending corrected-host rerun; repository-wide
documentation targets remain truthfully blocked by the missing Framework
Gitlink. The open Draft PR is
[#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370). The
remaining runtime evidence remains a follow-up requirement.
