# Change Record CR-20260919-readiness-b-shared-remediation: shared readiness-B remediation

**Language:** English | [Deutsch](CR-20260919-readiness-b-shared-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260919-readiness-b-shared-remediation |
| Date (UTC) | 2026-09-19 |
| Base revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Scope | Parent-only shared connector remediation, directly affected tests and paired documentation. No Framework, MRTS, Gitlink, dependency, rule-profile, scanner, Quality Gate, workflow, or merge change is included. |
| Delivery status | Draft PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370) from `agent/readiness-b-ten-integrations-20260919`; no merge is authorized. The prior corrective increment reached `18303495bc9bdb64cef74aae0f39e40d29ca5492`; its exact-head hosted Apache run `35445064987` passed the final-status P2 control. The Envoy correction in this record has source, fixture, C17, build, and configuration evidence only; exact current-head and hosted-check status must be verified at delivery and are not inferred here. |
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

The Envoy HTTP `ext_authz` source also had two bounded, Parent-owned contract
gaps: response-phase smoke selected a P1-only rule file and its fixture did not
emit the P3/P4 signals expected by the companion rules; its HTTP authorization
request used a callback `path_prefix` while the C profile could prefer
client-controlled URI-hint headers. The correction restores the matching
fixture and binds P3 to the protected path without trusting a URI override. It
is not a claim of an observed remote bypass or a substitute for a real Envoy
host run.

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
6. For the Envoy `ext_authz` smoke profile, select the matching P1/P3/P4
   fixture only when response smoke is opt-in and `RULES_FILE` is unset; bind
   P3 to `/phase3-block` plus the upstream header; and ensure no
   client-supplied original-URI hint can select the policy target.

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
- Make the Envoy response-phase default select the existing
  `modsecurity_response_companion_smoke.conf` only when the operator has not
  supplied `RULES_FILE`; retain the targeted request-only fixture otherwise.
  The P3 rule chains the exact protected `/phase3-block` request target to the
  server-created `X-Modsec-Upstream: block` response header, while the fixture
  supplies that header and the bounded P4 marker.
- Remove the HTTP `ext_authz` callback `path_prefix` and the profile's
  original-URI header preferences. The Envoy template disallows
  `x-envoy-original-path`, `x-forwarded-uri`, and `x-original-uri` from the
  authorization request as defense in depth; the C profile independently
  consumes none of them. The request target is neither decoded nor normalized
  by this correction.

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
The Envoy correction removes, rather than reprioritizes, client-controlled URI
headers from the authorization service's policy input. The template blocks the
same names if a future header allow-list changes, and the profile's zero-count
setting remains safe independently of template enforcement. Its response
fixture carries only static marker data and the event model remains payload-free.
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
- `connectors/envoy/src/envoy_ext_authz_service_main.c`
- `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/README.md`
- `connectors/envoy/README.de.md`
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
- `common/rules/modsecurity_response_companion_smoke.conf`
- `tests/test_prepare_runtime_components.py`
- `tests/test_apache_request_transaction_cleanup.py`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `tests/test_envoy_transport_hardening_contract.py`
- `tests/transaction_phase_runtime_companion_test.c`
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
| Current Stock-sidecar `c:S1820` refactor | The C17 build and 20 `StockSidecarSourceContractTest` cases passed with `cc`; the C17 build passed with `clang`. The complete local 35-case suite had 34 passes and one `runtime_identity` failure (`runtime-begin-smoke` exited 1 without stderr). That binary is built without `stock_sidecar.c`, so it is a separate failure and is not credited as a pass for this refactor. |
| `python3 -m py_compile ci/provisioning/components/prepare-runtime-components.py` | Passed after the two minimal `python:S1172` signature removals. |
| Current SonarQubeCloud PR #370 issue review | Before this increment, the service reported three task-owned open issues: one `c:S1820` and two `python:S1172`. The local fixes are covered above; zero open issues remains an unverified delivery gate until the analysis of the current PR head completes. |
| Native Traefik Go module `go test -mod=readonly ./...` | Passed. |
| Native Traefik `go vet ./...` and `gofmt -d` review | Passed; `gofmt -d` produced no diff. |
| Native Traefik `FuzzUDSFrameAndResult` for 15 seconds | Passed. |
| `tests.test_envoy_transport_hardening_contract` | Passed: 28 tests, including the response-default, P3/P4 fixture, URI-header, and unsafe-root regression contracts. |
| `make check-remaining-connectors-c17` with `CC=cc` and `CC=clang` | Passed twice; it compiled the changed Envoy C profile under C17 with warnings as errors. |
| Envoy connector build and response-companion rule configuration check | Passed against the cached libModSecurity prefix in a task-owned external build root; libModSecurity accepted the chained P3 rule. |
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
the successor at exact head `18303495bc9bdb64cef74aae0f39e40d29ca5492` passed
hosted run `35445064987`, including final `413`, no handler content, and the
same-process allow follow-up.

The Envoy follow-up ran the full
`tests.test_envoy_transport_hardening_contract` module, shell syntax checks,
C17 source checks with `cc` and `clang`, a full connector build against the
cached libModSecurity prefix, and an `ext_authz` configuration load using
`common/rules/modsecurity_response_companion_smoke.conf`. The first rule load
exposed a missing explicit action list on the chained second rule; adding
`t:none` caused the same real libModSecurity load to pass. No Envoy binary was
present, so no listener, generated-YAML validation, downstream URI, spoofing,
or P3/P4 host assertion was performed.

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
start by `chown(...)=EINVAL`; the subsequent exact-head hosted run passed the
bounded control. The Lighttpd harness likewise does not dynamically execute
`finish_request_body` or establish the full P2 path.

The following hosted bootstrap at
`56b838ce1fe681e47c8fd3df326dccab8a1c4405` exercised the over-limit request
but stopped its assertion at interim `100 Continue`, rather than the final
response. It is a harness-parsing failure, not evidence that the final result
was `413` and not a refutation of the finite/reject source correction. The
successor at exact head `18303495bc9bdb64cef74aae0f39e40d29ca5492` completed
hosted run `35445064987` successfully, including final `413`, absence of
handler content, and same-process follow-up. This remains bounded Apache P2
evidence, not a ten-path or full Apache-B promotion.

The Envoy correction has no real Envoy host evidence. It validates the
response-companion rule file and source/harness contract, but does not prove
the generated YAML, protected URI including query/percent-encoding, URI-hint
spoof resistance through Envoy, response companion correlation, or P3/P4 host
actions.

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
- The corrected exact-head hosted Apache control passed, but the current Envoy
  source head has no hosted or real-host run: the pinned Envoy binary and
  attested host inputs are unavailable. URI query/encoding and spoofing cases
  therefore remain required host controls. Current CI, SonarQube Cloud,
  review, mergeability, and final PR results must not be inferred from local
  checks. The repository-wide bilingual/link target preconditions are likewise
  blocked by the separately owned unmaterialized Framework Gitlink.
- The current local Stock-sidecar suite is not fully green: 34 of 35 cases
  passed, while `test_runtime_identity_smoke_accepts_the_canonical_profile`
  observed `runtime-begin-smoke` exit 1 without stderr. That independently
  built binary does not compile `stock_sidecar.c`; the failure is not used as
  validation of the `c:S1820` refactor and remains a separate diagnosis item.
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
merge. The corrected Apache host rerun passed; the Envoy source/harness repair
still needs real-host evidence. Repository-wide documentation targets remain
truthfully blocked by the missing Framework Gitlink. The open Draft PR is
[#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370). The
remaining runtime evidence remains a follow-up requirement.

## Follow-up C regression evidence — 2026-09-19

This Parent-only, test-only follow-up makes the focused C companion test
truthful and directly protects the buffered `traefik-forwardauth` lifecycle.
It does not change Common runtime behavior, a Traefik configuration, a host
binary, or any readiness classification.

- The test fixture now creates its private event directory from an absolute
  current-working-directory path. The test binary runs from its registered
  external build child; this preserves the product event sink's deliberate
  rejection of relative/no-follow parent components.
- A bounded raw invalid client-address byte (`0x80`) is correctly JSON escaped
  as `\u0080`, written as one event without a raw invalid byte, and followed
  by a transaction whose `previous_event_hash` equals the first event hash.
  A 63-byte escaping-expanding address instead fails with
  `MSCONNECTOR_ERROR_EVENT_TOO_LARGE` before a write or hash-chain advance; a
  subsequent ordinary event starts with `previous_event_hash` zero.
- The exact `traefik-forwardauth` profile in `forwardAuth` plus `buffered`
  mode now has direct C coverage for explicit empty and bounded non-empty
  bodies. It checks finished P2 metadata/counters, `P1|P2`, no truncation,
  rejection of a second P2 finalization, opaque response-companion transfer,
  and P3/P4 completion. A non-empty null body pointer is rejected fail closed.

Strict C17 full-test builds and executions passed with both `cc` and `clang`,
using `-Wall -Wextra -Werror`, task-owned external output, and 120-second
limits. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
tests.test_traefik_forwardauth_p2_contract` passed 7/7; `make
check-common-security-contract` and `git diff --check` passed. Independent
security and test reviews found no plausible finding in this test diff.

This is Common-runtime regression evidence only: it deliberately bypasses
Traefik HTTP parsing and therefore proves neither `Content-Length` handling,
an actual Traefik host result, nor B-class readiness.

## NGINX native receipt-identity correction — 2026-09-19

The exact-head NGINX workflow, archive digest, and shared fixture source root
bind NGINX `1.31.5`, but both separately generated native response-body-buffer
and P3-header receipts incorrectly declared `1.31.4`. That was an
evidence-identity defect: it did not alter the built binary, connector
behavior, request processing, or the existing bounded fixture results, but it
prevented those receipts from being used as precise G1 identity evidence.

The shared fixture now has one `EXPECTED_NGINX_VERSION = "1.31.5"`, derives
its expected source root from it, and both receipt writers emit that same
constant. New focused assertions first failed because the version identity was
absent or stale; after the correction the body-buffer fixture contract passed
8/8 and the P3-header fixture contract passed 4/4. The affected NGINX contract
set passed 48 tests, with three expected skips caused only by the separate
Framework Gitlink HEAD mismatch; `git diff --check` passed.

The correction has no fresh hosted receipt yet and does not close NGINX G2--G9
or promote NGINX to B. The existing non-root worker, no-follow path,
body-boundary, fail-closed error, and cleanup controls remain unchanged.

## SonarQube Cloud new-code duplication follow-up — 2026-09-19

PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370)
reported `new_duplicated_lines_density=2.5337837837837838` (30 lines and four
blocks) solely in `tests/transaction_phase_runtime_companion_test.c`. This
Parent-only change removes that real test-code duplication without a
suppression, exclusion, Quality-Gate change, or product-behavior change.

- `read_event_jsonl()` now owns the bounded, checked event-file read and
  NUL-termination used by every event assertion in this companion test.
  `assert_completed_denied_block()` owns only the identical ordinary
  `/blocked` follow-up transaction lifecycle.
- The controlled malformed-address starts remain explicit. The test still
  proves lossless `0x80` escaping with a nonzero event hash and chained valid
  follow-up; it also still proves an escape-expanding address fails
  `MSCONNECTOR_ERROR_EVENT_TOO_LARGE` without an event or chain advance, then
  accepts an independent valid follow-up with zero previous hash.
- The direct Common-runtime companion binary passed before and after the
  refactor with both `cc` and `clang`, each under strict C17
  `-Wall -Wextra -Werror` and a 120-second bound in a private external build
  child. `git diff --check` passed before this record update. An independent
  focused security review classified this as a security-relevant regression
  boundary and found no candidate or validated finding.

This is test-maintenance evidence only. It neither changes an integration
runtime nor promotes any of the ten paths to readiness B. The required final
exact-head SonarQube Cloud measure and PR checks are recorded from the live PR
after the normal push; no merge is authorized.
