# Change Record: CR-20261011-response-limit-policy-removal

**Language:** English | [Deutsch](CR-20261011-response-limit-policy-removal.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-response-limit-policy-removal |
| Date (UTC) | 2026-10-11 |
| Base revision | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |

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
without force-push, history rewrite or merge.

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

Observed current checks and retained artifacts are under `/var/tmp/codex/ModSecurity-conector/runs/body-policy-removal-20261011/`:
`common/real-engine.log` (nine methods, 193 scenarios), Common combined final
run (30 tests), `root-checks/common-contracts.log` (all selected Common targets)
and `root-checks/docs.log` (21 generated references, EN/DE/path/link checks and
22 compiler tests). Six configuration-reference unit tests passed. Component
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
MRC1 retains individual 64 KiB frames and 32 KiB body chunks. Pointer/integer
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

Current Common real-library validation passed nine methods: 112 native request
and 81 response scenarios (193 total). A later combined run passed 30 tests.
Four real authorization-socket cases use a 2 MiB body: a tail marker produces
native 451 under a high limit, the same payload under a low ProcessPartial limit
produces 200, low Reject produces native 403, and a marker-free body is allowed.
The callback completes P2 before handoff without offering a prefix twice.

Common helper/SDK/security/memory/flow/adapter/directive checks passed. Six
configuration-reference tests passed; all 21 generated files are current.
EN/DE, path/link checks and 22 compiler-guide tests passed. Apache C17 passed;
HAProxy binding/self-test/SPOP C builds and 104 tests with 119 subtests passed,
with the final genuine request/response suite passing 13 methods in 13.62 seconds. Envoy passed eight Go
packages and its real CGo build. Traefik Go/C builds and socket-protocol self-tests
passed. lighttpd C build, 15 gate tests and two isolated Envoy tests passed.
Stock-sidecar validation passed 35/36; its unchanged RST empty-event base defect
remains open. The Common legacy lossy-event assertion and two old SPOP source
assertions also remain unchanged base failures; assertions are preserved.

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
Common lossy-event failure and two old SPOP source-assertion failures remain
unchanged baseline defects; their assertions are not weakened.

## Remaining risks

The active authorization profiles do not provide unrestricted incremental
request ingestion. Pinned current host evidence is missing for all ten profiles,
including buffer ownership, protocol lifecycle and late intervention delivery.
Local native reconciliation and full quick-check passed. Changed-head CI/Sonar
and expanded PR delivery verification remain open. Overall verification is partial.

## Checks not run and rationale

No complete current request/response ten-profile hosted matrix was run; required
pinned host environments and run evidence are unavailable. The renewed full
quick-check passed after checker repairs. Current changed-head CI/Sonar is
pending. Historical response-only checks and starting-head Sonar results apply
only to their revisions and are not evidence for the current expanded diff.

## Final diff and review status

Existing [Draft PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
remains on `fix/engine-owned-response-limits-stack-20261011`, stacked on #382.
The expanded task starts at `6576661724841e26802a93b19d8bbfbdb5c8235a` and retains the exact base above.
Its expanded changes are not yet pushed at this snapshot. No new PR, force-push,
history rewrite or merge is performed. Final scoped review/diff validation and
current-head readback remain delivery prerequisites. See the
[stack checklist](../../../docs/response-limit-stack-checklist.md) and
[ownership contract](../../../docs/phase4-mode-budget.md).
