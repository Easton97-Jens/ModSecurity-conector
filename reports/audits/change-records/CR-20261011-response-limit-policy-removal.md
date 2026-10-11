# Change Record: CR-20261011-response-limit-policy-removal

**Language:** English | [Deutsch](CR-20261011-response-limit-policy-removal.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-response-limit-policy-removal |
| Date (UTC) | 2026-10-11 |
| Base revision | `2619b20b9d2e70fa07cbe71f664b48ff3c105380` |


## Motivation and problem statement

The user extends #407 to both directions and explicitly supersedes request-policy preservation. Connector size policy must not decide before libModSecurity. Request limits/actions belong to `SecRequestBodyLimit`, `SecRequestBodyNoFilesLimit` and `SecRequestBodyLimitAction`; response policy belongs to `SecResponseBodyLimit`/`SecResponseBodyLimitAction`.

## Acceptance criteria

Remove connector fields/defaults/merge/parser/fallback gates, injected directives, inferred engine limits and connector-selected prefixes/actions. Preserve native results, DetectionOnly, phase completion, cleanup and technical safeguards. Fixtures explicitly choose applicable engine policy; removed keys fail configuration. Maintain EN/DE/generated references and strict exact-head Sonar gates. Report active caps and host gaps without claiming full removal.

## Implementation decision and rationale

Common `request_body_limit`, `response_body_limit`, `body_limit_action`, request/response default macros and corresponding adapter/service options are removed. Native append results and pending interventions survive EOS; `bytes_inspected` means offered bytes, not the native partial prefix. Incremental socket/file processing and private spool replay replace full-body fallbacks. Complete authorization samples are required before native P2; typed local-reply and terminal transitions preserve actual host outcomes.

## Changed files

Common contracts/runtime/authorization transport; Apache, NGINX, HAProxy, Envoy, Traefik and lighttpd ingestion/services/harnesses/tests; configuration/compiler generators and generated EN/DE references; examples, connector README pairs and ownership/stack documentation. No Framework/MRTS source or dependency manifests are changed.

## Commands executed

Repository-native `make quick-check`, `check-i09-native-routes`, `check-apache-event-sink` and `check-haproxy-spop-event-sink` passed with the counts below. Genuine engine, Go/C build, host harness and fixture checks retain external run logs. Documentation validation uses RTK-wrapped `make check-bilingual-docs check-doc-links check-connector-config-reference`, `ci/tools/new-change-record.py check` and `git diff --check`. Repeated historical runs are not summed.

## Security impact

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

## Runtime evidence

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

## Known limitations

| Active route | Remaining limit and actual scope |
| --- | --- |
| Envoy ext_authz | Host `max_request_bytes=4096/33` bounds the complete request sample sent to authorization; its response observer does not make request ingestion incremental. |
| Traefik forwardAuth | Host `maxBodySize=4096/33` bounds the buffered authorization request. |
| Composite Traefik authorization response | Host `maxResponseBodySize=32768` bounds the authorization response, not the upstream application response. |
| HAProxy SPOE/SPOP | One request sample per bounded protocol message/frame; incomplete-sample admission fails with 503 before the engine, not native `BODY_LIMIT`. Native HTX is separate. |

These remain concrete active restrictions, not renamed working-buffer capacities. Envoy `allow_partial_message: false` and completeness rejection prevent incomplete samples from being finalized as full P2. Independent host controls such as lighttpd `server.max-request-size` remain.

## Remaining risks

Complete current ten-profile hosted body-limit evidence, `p4_strict`, and adversarial UID/mount deployment checks remain missing. Two baseline failures remain. Local/component/selected-host success does not establish complete removal or fully verified delivery.

## Checks not run and rationale

Historical analyses are revision-scoped: `cec340f3` reported 32 issues and
seven duplication blocks/65 lines; `dc33ffef` retained six smells;
`ef4e90dc` retained one issue with zero hotspots and duplication. These do not
satisfy the strict zero-new-issue requirement. Repairs retain checks/assertions
and introduce no scanner exceptions or weaker gates. Earlier passed heads do
not verify subsequent changes. Latest exact-head status belongs to live PR checks.

`p4_strict` is `NOT_RUN`; nine host cases are only `LIFECYCLE_ONLY`. Cached host
binaries exist, but current module provenance and complete profile runtime
evidence are missing. Actual foreign-UID/read-only-mount probes are blocked by
root-only UID/GID maps, foreign-UID `chown` EINVAL and isolated user/mount namespace
EPERM. Latest exact-head CI/Sonar is read from the PR rather than treating this
source document as a live status feed.

## Final diff and review status

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

Independent source/P2/P4/EOS/sticky-IO reviews found no concrete open finding. Final local validation is retained separately from exact-head remote checks. See the [stack checklist](../../../docs/response-limit-stack-checklist.md).
