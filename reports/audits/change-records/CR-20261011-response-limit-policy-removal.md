# Change Record: CR-20261011-response-limit-policy-removal

**Language:** English | [Deutsch](CR-20261011-response-limit-policy-removal.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-response-limit-policy-removal |
| Date (UTC) | 2026-10-11 |
| Base revision | `2619b20b9d2e70fa07cbe71f664b48ff3c105380` |

## Motivation and problem statement

The current user instruction expands existing Draft PR #407 to both body
directions and explicitly supersedes request-policy preservation. Connector
policy could reject/truncate before native inspection. Request policy belongs
to `SecRequestBodyLimit`, `SecRequestBodyNoFilesLimit` and
`SecRequestBodyLimitAction`; response policy belongs to `SecResponseBodyLimit`
and `SecResponseBodyLimitAction`. Full removal is not claimed while the active
authorization/sample constraints listed below remain.

## Acceptance criteria

Remove connector request/response options, defaults, merges/parsers, fallbacks
and cumulative pre-engine decisions. Do not infer engine limits, inject rules,
choose actions, truncate or replace caps with unlimited full-body allocation.
Preserve native operation results, intervention/phase completion, DetectionOnly,
error propagation and cleanup. Inspection fixtures explicitly supply their
direction's engine limits/actions; helpers have no policy defaults. Prove
boundaries, actions, chunks/files, identical payloads under different limits and
markers beyond former ceilings. Reject removed options; maintain EN/DE sources
and generated references. Preserve technical safeguards and zero-new-code Sonar
gates. Report active caps and missing hosts separately; deliver to existing #407
without force-push, history rewrite or PR/master merge. Subsequent user authorization
permits regular #382 base merges into the existing #407 branch.

## Implementation decision and rationale

Remove `MSCONNECTOR_DEFAULT_REQUEST_BODY_LIMIT`, `request_body_limit`,
`body_limit_action`, corresponding adapter options, HAProxy `request-body-limit`,
Envoy `max_request_body_bytes` and Traefik `maxRequestBodyBytes`, together with
the previously removed response policy. Native results govern P2/P4, including
append zero under valid native ProcessPartial and pending disruptive outcomes
through EOS; actual native status is preserved. `bytes_inspected` counts bytes
offered to the engine, not its internal partial prefix. Incremental socket/file
processing and private sidecar spooling replace full-body fallbacks. Tests
without body inspection need no artificial native policy.

## Changed files

Common configuration/body/resource/mapper/transaction contracts, native runtime
and authorization transport; Apache/NGINX/HAProxy/Envoy/Traefik/lighttpd ingestion,
services, middleware, harnesses, fixtures and tests; configuration-reference and
compiler-guide generators with generated EN/DE output; example configurations,
connector README pairs and body-ownership documentation. This stack checklist
and Change Record pair track current scope. No Framework/MRTS source or dependency
manifest changes are included.

## Commands executed

Observed earlier expanded-task checks and retained artifacts are under `/var/tmp/codex/ModSecurity-conector/runs/body-policy-removal-20261011/`:
`common/real-engine.log` (nine methods, 193 scenarios), Common combined final
run (30 tests), `root-checks/common-contracts.log` (all selected Common targets)
and `root-checks/docs.log` (21 generated references, EN/DE/path/link checks and
22 compiler tests). Seven configuration-reference unit tests passed. Component
build/test results are described below. The terminal `root-checks/quick-check.log` records `make quick-check` exit 0:
ten unittest groups with 302 tests plus lint, contracts, security, memory,
documentation, generated references, helpers, actionlint and diff checks.

Documentation validation uses the repository-native payloads through RTK:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check
rtk proxy make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
rtk proxy git diff --check
```

## Security impact

Incremental HTTP work buffers are 16 KiB; file-read scratch is 32 KiB.
MRC1 retains individual 64 KiB frames and 32 KiB body chunks. Counters retain
their integer representation (`SIZE_MAX`, or `INT64_MAX` for signed counters/file
offsets); overflow ends as a technical failure without engine append/truncation. Pointer/integer
checks, descriptors/file ranges, message controls, header/event metadata and
timeouts remain. Stock lighttpd uses private unlinked spooling with bounded RAM
and withholds upstream replay until native P2 allows it; disk failures remain
technical failures. The legacy full-body fallback is removed. These controls
are scoped operations/storage safeguards, not replacement inspection limits.

No authentication, isolation, warnings, assertions, scanner exceptions or
Quality Gates are weakened. Native configuration retains native defaults when
omitted; the connector supplies none. Authorization host buffers remain concrete
constraints requiring migration/evidence, not relabeling as technical capacity.
Independent focused source-safety review found no concrete finding; this does
not establish hosted runtime safety.

## Runtime evidence

Earlier expanded-task Common real-library validation passed nine methods: 112 native request
and 81 response scenarios (193 total). A later combined run passed 30 tests.
Four real authorization-socket cases use a 2 MiB body: a tail marker produces
native 451 under a high limit, the same payload under a low ProcessPartial limit
produces 200, low Reject produces native 403, and a marker-free body is allowed.
The callback completes P2 before handoff without offering a prefix twice.

Common helper/SDK/security/memory/flow/adapter/directive checks passed. Seven
configuration-reference tests passed; all 21 generated files are current.
EN/DE, path/link checks and 22 compiler-guide tests passed. Apache C17 passed;
HAProxy binding/self-test/SPOP C builds and 104 tests with 119 subtests passed,
with the final genuine request/response suite passing 13 methods in 13.62 seconds. Envoy passed eight Go
packages and its real CGo build. Traefik Go/C builds and socket-protocol self-tests
passed. lighttpd C build, 15 gate tests and two isolated Envoy tests passed.
Stock-sidecar validation passed 35/36; its unchanged RST empty-event base defect
remains open. The Common legacy lossy-event assertion remains a baseline failure. The two old
SPOP source assertions pass after integrating the upstream I09 fixes. Assertions
are preserved.

The terminal native `make quick-check` passed (exit 0): ten unittest groups
with 302 tests plus lint, contracts, security, memory, documentation, generated
references, helpers, actionlint and diff checks.

Final Common native validation passed 13 methods and 168 subtests in 14.34
seconds (`root-checks/final-common-native.log`), including the four HTTP cases.
HAProxy's genuine suite passed 13 methods in 13.62 seconds; Response DetectionOnly
preserved the actual native 65536-byte prefix for a 120000-byte body in four
chunks: Reject append results `[1,1,1,1]`, ProcessPartial `[1,1,0,0]`, EOS `1`.
Seven configuration-reference tests passed, including strict removed-key tombstone
mutations. All NGINX adoption/mutation checks passed. A combined four-file sweep
passed 145 tests and 163 subtests with two stale Apache planner expectations;
after correcting those expectations, all six Apache checks passed and preserve
native append `0`/`1` continuation and exact EOS `1` guards. Independent review
identified case-alias/JSON-null removed-key acceptance; EqualFold matching and
24 negative cases now pass with the entire Traefik Go suite. Seven additional
Traefik forwardAuth tests passed. No review finding remains open.

Current changed-head CI/Sonar and zero-new-code
issues/hotspots/duplication verification are pending; live results are linked in
[PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407).

The Common native tests use explicit 128/1024 boundaries, Reject/ProcessPartial,
request On/DetectionOnly with buffered/streaming modes and memory/file input;
response `off`/`safe`/`strict` cases are retained. Explicit 1.5/3 MiB policies with
2 MiB bodies exercise markers beyond the former 1 MiB connector ceiling. Same
payloads under two native limits distinguish permitted inspection from native
partial behavior; no connector action/prefix is selected. All results above are
engine/socket/component evidence rather than a current ten-host matrix.

## Known limitations

| Active route | Remaining limit and actual scope |
| --- | --- |
| Envoy ext_authz | Host `max_request_bytes=4096/33` bounds the complete request sample sent to authorization; its response observer does not make request ingestion incremental. |
| Traefik forwardAuth | Host `maxBodySize=4096/33` bounds the buffered authorization request. |
| Composite Traefik authorization response | Host `maxResponseBodySize=32768` bounds the authorization response, not the upstream application response. |
| HAProxy SPOE/SPOP | One request sample per bounded protocol message/frame; incomplete-sample admission fails with 503 before the engine, not native `BODY_LIMIT`. Native HTX is separate. |

These active sample/full-body constraints prevent claiming complete removal
across all profiles. Independent host configuration, including lighttpd
`server.max-request-size`, also remains distinct. The stock RST event defect,
Common lossy-event failure remain baseline defects. The two historical SPOP
source-assertion failures are resolved by the upstream I09 fixes; assertions are
not weakened.

## Remaining risks

The active authorization profiles do not provide unrestricted incremental
request ingestion. Pinned current host evidence is missing for all ten profiles,
including buffer ownership, protocol lifecycle and late intervention delivery.
Local native I09 reconciliation and full quick-check passed. Final I11 affected/
full validation passed. Changed-head CI/Sonar and expanded PR delivery remain
open at this local snapshot. Overall verification is partial.

## Checks not run and rationale

No complete current request/response ten-profile hosted matrix was run; required
pinned host environments and run evidence are unavailable. The renewed full
quick-check passed on the recorded I09 base after checker repairs. Final I11
affected/full validation passed with exit 0; the additional combined NGINX/
bounded-URI/bridge run passed 130 tests. Current changed-head CI/Sonar is
pending. Historical response-only checks and starting-head Sonar results apply
only to their revisions and are not evidence for the current expanded diff.

## Current base reconciliation

The selected current #382 base is `2619b20b9d2e70fa07cbe71f664b48ff3c105380` (I11).
The ordinary I09 integration is committed as `2bb1a1e0`; authorized ordinary
I11 base integration is locally complete and source is frozen. Published history
is retained; no PR/master merge or force-push is performed.

On integrated I09 base `492663334d89428dce084792145ef94e91579788`, `check-i09-native-routes`
passed 33 tests and native `make quick-check` passed with exit 0, including ten
unittest groups totaling 302 tests (`root-checks/resume-base492-check.log`).
The old SPOP source assertions pass with upstream I09 fixes. Earlier Common
reconciliation passed 30 focused tests including 13 genuine engine tests;
Traefik Go packages, I09 lighttpd/Traefik tests and both C builds passed.
Stock-sidecar remains 35/36 due to unchanged RST empty-event behavior; rebuilt
Common legacy lossy-event validation exits 134 at assertion 209. Assertions are
retained.

On selected I11 base `2619b20b9d2e70fa07cbe71f664b48ff3c105380`,
final native selection passed 20 modules with 212 tests and 201 subtests in
58.51 seconds, including 13 genuine engine methods. Apache C17, APR/LTO cleanup
and adoption checks passed, as did genuine HAProxy binding/build/self-test/SPOP
protocol checks. Additional real APR-bucket and production-append regressions
for P2/P4 passed 20 methods and ten subtests: native pending 403 through EOS,
and sticky `/dev/full` IO failure with 500 and no replay. Independent review
found no finding. All eight Envoy packages passed pure Go and real
CGo/libModSecurity validation, and its binary built. Evidence:
`native/base261/validation-status.json` and `remaining/base261/validation.md`.

The final aggregate native Make run on I11 passed with exit 0:
`check-i09-native-routes` with 33 tests, `check-apache-event-sink` with 20 tests,
`check-haproxy-spop-event-sink` with 19 tests and `quick-check` with ten unittest
groups and 304 tests. Security/memory/flow/helper/documentation checks,
21 generated files and diff checks passed. Actual Apache, NGINX and HAProxy
C17 compilation passed; earlier local compilation evidence gaps are closed,
while hosted matrix evidence remains missing. Evidence:
`root-checks/base261-final-make.log`. The additional combined NGINX adoption/
bounded-URI/Envoy-bridge run passed 130 tests in 694.670 seconds
(`root-checks/base261-root-targeted.log`). Final targeted inventory, including
hidden files in Common, all connectors and examples, found no additional active
own cumulative body cap, directive injection or fallback beyond the disclosed
authorization/sample constraints; no hidden plugin manifest contains a retired
key. Independent P2/P4 EOS and sticky-IO review found no finding. The later analyzed #407 head is `cec340f3`; follow-up commit, push/readback
and renewed exact-head CI/Sonar after its repairs remain pending.

## Current Sonar repair snapshot

The first completed analysis of `cec340f3` reported 32 issues (one bug,
two vulnerabilities, 29 code smells), zero hotspots and seven new duplication
blocks totaling 65 lines. This analysis is not a passing Gate result. Source
repairs are locally frozen; they retain checks and assertions and alter no
scanner exceptions or Gate controls. Renewed exact-head CI/Sonar and follow-up
commit/push remain pending; live status is in
[PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407).

Current local reruns passed: Common with 207 native scenarios and 13 genuine
methods, native selection with 131 tests/185 subtests, Go/C builds and security
checks, and 16 root CI fixture tests covering pending-request state/counts,
runtime construction and modeled NGINX intervention. The earlier 212-test/
201-subtest selection is a separate run; repeated checks are not added into a
combined test total. Current stock-sidecar validation passed 57/58; only its
known RST empty-event defect remains open there. Together with the Common legacy
lossy-event assertion, two baseline defects remain open. Evidence is under
`common/sonar-cec/`, `native/sonar-cec/`, `remaining/sonar-cec/` and
`root-checks/ci-fixture-repairs-final.log` in the external task run directory.
Generated references now inventory 22 lighttpd items.

The optional technical CLI argument `--spool-directory` selects private request
spooling. The default is the validated private parent of `--config`. For `/etc`
or read-only configuration storage, explicitly select an existing canonical,
effective-service-UID-owned, writable 0700 directory. Startup checks ancestors,
no-follow directory descriptors and file creation before readiness. Request
files are exclusively created 0600 files and immediately unlinked. Startup,
descriptor and disk failures remain technical failures. No `TMPDIR` or public
fallback, total-body cap or unlimited full-body RAM allocation is introduced.
Operators whose configuration parent is not private must supply this storage
argument.

The disclosed active authorization/sample caps and ten missing host-profile
proofs remain; complete removal or fully verified delivery is not claimed.

## Final diff and review status

Existing [Draft PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
remains on `fix/engine-owned-response-limits-stack-20261011`, stacked on #382.
The expanded task starts at `6576661724841e26802a93b19d8bbfbdb5c8235a` and integrates the advanced base above.
The expansion has since been delivered through analyzed head `cec340f3`;
the subsequent repair follow-up is not yet committed/pushed at this snapshot. No new PR, force-push,
history rewrite or PR/master merge is performed. Regular base integration into
#407 is explicitly authorized. Final scoped review/diff validation and
current-head readback remain delivery prerequisites. See the
[stack checklist](../../../docs/response-limit-stack-checklist.md) and
[ownership contract](../../../docs/phase4-mode-budget.md).
