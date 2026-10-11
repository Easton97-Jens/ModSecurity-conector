# Request/response body-limit stack checklist

**Language:** English | [Deutsch](response-limit-stack-checklist.de.md)

## Stack and delivery

[Draft PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
remains on `fix/engine-owned-response-limits-stack-20261011`, stacked on #382
branch `fix/unified-native-results-events-20260921`, exact base `2619b20b9d2e70fa07cbe71f664b48ff3c105380`.
Normal commits/base merges retain published history; no force-push, rewrite or
PR/master merge occurred. Delivered repair head `455944cfff472d6cf47b8ff0bb252d262adaf804`
follows `ef4e90dc`; it changes only test complexity through equivalent eight-case
helper extraction, retaining all assertions and passing genuine focused tests.
The [live PR checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407/checks)
provide the latest exact-head delivery readback. The exact source/test analysis of this head at 2026-10-11T19:13:56Z
passed: check `114552418608` succeeded with zero annotations, zero open/accepted
issues and hotspots, all eight root metrics and all 269 measured component
duplication values zero; Quality Gate OK with no ignored conditions. Four CI
checks were still pending at preparation. This proves that head; later
documentation-only commits use live readback instead of self-referential status
updates.

## Implementation and retained verification

- [x] Trace all ten logical profiles and remove Common/adapter/service request and response body policy, defaults, parser/merge/fallback decisions and connector `body_limit_action`.
- [x] Keep limits/actions native, reject removed keys, preserve operation-specific results, DetectionOnly, pending interventions and once-only completion/cleanup.
- [x] Replace full-body allocation/fallbacks with incremental processing/private spooling and retain technical guards.
- [x] Maintain explicit direction-specific engine policy in inspection fixtures, EN/DE sources, examples and generated references.
- [x] Retain and enforce exact-head zero-new-issue/hotspot/duplication gates; this checkbox describes controls, not a current passing scan.
- [ ] Remove all active full-body/sample restrictions: the concrete constraints below remain.

## Verified local and selected host evidence

Common genuine tests passed 207 native scenarios across 13 methods, covering
request/response boundaries, actions, DetectionOnly, chunks/files, varied native
limits and markers beyond former ceilings. Same-payload/socket tests preserve
native 451/403/allow outcomes and avoid duplicate P2 prefixes. Pending results,
exact EOS and sticky `/dev/full` failure/no-replay paths retain their assertions.

Current repository-native `quick-check` passed 304 reported unittest tests;
separate I09/Apache/SPOP checks passed 33/20/19, totaling 376 test executions for
those four commands. Repeated earlier runs are not added to this total. All eight Envoy Go
packages, real CGo/libModSecurity builds and binaries passed; Apache/NGINX/HAProxy
C17, Traefik Go/C/socket, Common safety/contracts and generated-reference checks
passed. All 21 generated outputs are current, with 22 lighttpd inventory items.

Pinned Envoy 1.39.1 HTTP/1 composite validation passed 14 executed cases with
14 distinct successful terminal cleanups. Nine verifier cases are
`LIFECYCLE_ONLY`; `p4_strict` is `NOT_RUN`. On/DetectionOnly controls with host
request capacity 33 and native limit 4096 reject a 44-byte request with host 413,
zero authorization/native/EOS events and no upstream, followed by a same-process
small-request P1–P4 control. A complete 33-byte sample above explicit native
limit 32 separately produces native 403. Host-only rejection cannot satisfy
native P2 proof. Typed internal host attributes authenticate local-reply
continuation; client headers cannot select it. Lease expiry records typed timeout;
controlled unavailable/restarted companion returns actual host 500 and one
restart cleanup. Missing response metadata/expired leases retain 503.

Stock-sidecar validation passed 57/58; its known RST empty-event failure and
Common legacy lossy-event assertion (exit 134) remain two baseline defects.
Assertions are intact. Selected host evidence is not a complete ten-profile
body-limit matrix.

## Active restrictions

Full removal across all active profiles is not claimed. Envoy composite samples
require `allow_partial_message: false`; partial/malformed/ambiguous completeness
metadata is rejected before Common open/body/EOS/lease creation, without an
adapter size threshold or chosen native action.

| Active route | Remaining limit and actual scope |
| --- | --- |
| Envoy ext_authz | Host `max_request_bytes=4096/33` bounds the complete request sample sent to authorization; its response observer does not make request ingestion incremental. |
| Traefik forwardAuth | Host `maxBodySize=4096/33` bounds the buffered authorization request. |
| Composite Traefik authorization response | Host `maxResponseBodySize=32768` bounds the authorization response, not the upstream application response. |
| HAProxy SPOE/SPOP | One request sample per bounded protocol message/frame; incomplete-sample admission fails with 503 before the engine, not native `BODY_LIMIT`. Native HTX is separate. |

Independent host policies such as lighttpd `server.max-request-size` also remain.

## Technical safety and deployment gaps

Incremental HTTP buffers are 16 KiB, file scratch 32 KiB, and MRC1 frames/body
chunks 64/32 KiB. Pointer/overflow/file-range/descriptor/message/header/event/
timeout checks remain; representational overflow is technical failure. Stock
lighttpd uses bounded RAM and private, immediately unlinked 0600 spool files,
replayed only after native P2 allow. No total-body cap or unlimited full-body RAM
allocation replaces the removed policy. `--spool-directory` optionally selects
storage; default is the validated private parent of `--config`. For `/etc` or
read-only configuration, supply an existing canonical, effective-UID-owned,
writable 0700 directory. Startup checks ancestors, no-follow descriptors and
file creation before readiness; no `TMPDIR`/public fallback exists. UID/mount
adversarial deployment coverage remains missing.

Actual foreign-UID and read-only-mount probes are blocked by this environment:
UID/GID maps contain only root, foreign-UID `chown` returns EINVAL, and isolated
user/mount namespaces return EPERM. Existing cached host binaries do not prove
current module provenance or the complete runtime matrix.

## Missing complete host matrix

All ten profiles still lack the complete current request/response limit matrix,
including protocol lifecycle, host ownership/commit timing and late-abort proof.
The 14 selected Envoy HTTP/1 cases do not close these broader criteria.

- [ ] Apache native.
- [ ] NGINX native, including memory/file buffers.
- [ ] HAProxy native HTX.
- [ ] HAProxy SPOE/SPOP with native-HTX response companion.
- [ ] Envoy ext_proc.
- [ ] Envoy ext_authz with response observer.
- [ ] Traefik native UDS middleware.
- [ ] Traefik forwardAuth with response observer.
- [ ] lighttpd Stock sidecar.
- [ ] lighttpd patched native.

## Sonar and evidence boundaries

Historical analyses are revision-scoped: `cec340f3` reported 32 issues and
seven duplication blocks/65 lines; `dc33ffef` retained six smells;
`ef4e90dc` retained one issue with zero hotspots and duplication. These do not
satisfy the strict zero-new-issue requirement. Repairs retain checks/assertions
and introduce no scanner exceptions or weaker gates. Earlier passed heads do
not verify subsequent changes. Latest exact-head status belongs to live PR checks.

Retained external evidence: `common/sonar-cec/`, `native/sonar-cec/`,
`remaining/sonar-cec/`, `root-checks/ci-fixture-repairs-final.log` and
`root-checks/envoy-completeness/`, including
`host/restart-final-validation-status.json`. See the
[ownership contract](phase4-mode-budget.md) and
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.md).
