# Change Record: Trusted NGINX physical-event provenance

**Language:** English | [Deutsch](CR-20261022-nginx-trusted-event-provenance.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261022-nginx-trusted-event-provenance` |
| Date (UTC) | `2026-10-22` |
| Base revision | `c03352ba160675a94bf63125cceaa25367f52c27` |
| Pull request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation and problem statement

The selected NGINX timeout and transport contracts require `run_id`,
`transport_case_id`, and `connection_id` in the same physical JSONL event.
The native NGINX adapter wrote no such fields. Controller receipts could not
repair that producer gap without inventing event content.

## Acceptance criteria

- Provenance comes only from administrator-controlled process configuration,
  never from HTTP headers.
- Run and case identifiers are both absent or both valid 1–128 byte ASCII
  tokens from `[A-Za-z0-9_.:-]`.
- The connection identifier comes from NGINX's actual connection number and
  reuse reflects the request count on that connection.
- Both real JSONL writers project provenance onto their private event copy
  before Common serialization; the caller's event remains unchanged.
- Invalid or partial provenance produces no unbound physical event and retains
  each writer's existing failure contract.
- The integrated Root-master/Nobody-worker host campaign proves the fields in
  the actual physical event before any I12 acceptance claim.

## Implementation decision and rationale

Both native writer tails use one bounded helper. A fully absent pair preserves
the optional existing behavior. When configured, the helper validates the two
process-environment values without an unbounded pre-validation read, derives
`nginx-<connection-number>`, and sets the reuse flag before the strict Common
serializer runs. NGINX must explicitly retain both variables with main-context
`env` directives. This keeps the trust boundary at administrator-owned process
configuration and makes the producer, rather than a report, own the fields.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_bounded_event_uri.py`
- `tests/test_nginx_common_adoption.py`
- focused P1/P3/request/cleanup extraction fixtures
- `connectors/nginx/README.md` and `connectors/nginx/README.de.md`
- this English/German Change Record pair

## Commands executed

All commands were RTK-wrapped. Raw evidence is retained below
`/var/tmp/codex/ModSecurity-conector/runs/pr416-nginx-complete-20261022/product-382/provenance`.

| Check | Observed result |
| --- | --- |
| Exact-writer regression before the product change | Exit 1: nine tests with 46 expected subtest failures because the physical JSONL events lack the required provenance. `pre-fix.log`, SHA-256 `0e1f9f9af6e805490a4afa5d0bb53a666c5ca3ddb3152fed51d059dde5514913`. |
| Focused writer, P1/P3/request and adoption mutation tests after the change | Exit 0: 36 tests pass. `post-fix.log`, SHA-256 `4d53de0f0ca1ec1986cb5527c93d12fb79a228dd9445c2dea90c7c28ef9dfc53`. |
| Final exact-writer suite | Exit 0: ten tests pass, covering absent, paired, partial, invalid, 128/129-byte, connection-number, reuse and source-event immutability behavior. |
| `make check-nginx-c17` | Exit 0; the NGINX/Common C17 warnings-as-errors compilation passes. |
| Final NGINX product regression sets | Exit 0: two disjoint final runs pass 165 and 82 tests (247 total), including exact writer, adoption, security boundary, native result, mutation and cleanup coverage. |
| Final `make build-nginx` | Exit 0 against pinned NGINX 1.31.6 and the prepared libModSecurity runtime cache from the final product source under `product-382/runtime-final`. This is build evidence only. |
| NGINX C-standard wiring, repository-path, bilingual-document, Change Record and diff checks | Exit 0; the Change Record result is structural only. |

Live Root/Nobody inheritance and physical-event results remain downstream I12
work; no pending check is reported as PASS.

## Security impact

The change adds a narrow trusted metadata ingress. Values are accepted only as
a validated pair from the process environment that NGINX administrators choose
to preserve. No request-controlled header, URI or body supplies the fields.
Invalid configuration fails the event write instead of emitting falsely bound
evidence. The work stays within the user-approved TAC1 focused-review boundary.

## Runtime evidence

Compiled fixtures prove the real writer and Common serializer boundaries. They
do not prove worker inheritance or a live host event. The downstream #416 I12
campaign must run a Root master with Nobody workers, explicit `env` retention,
the loaded connector and libModSecurity, and verify all three identifiers in
the physical event together with native/client/cleanup evidence.

## Known limitations

The two environment identifiers are process-level campaign identity. They do
not vary between requests on one keepalive connection. Independent case IDs
therefore require independent NGINX process runs. Connection numbers are scoped
to the declared run and are not presented as globally unique. A failed host
inheritance or physical-event check blocks I12 acceptance.

## Remaining risks

The integrated host run must still prove that a Root master retains both
variables for Nobody workers and that the exact run, case and connection values
reach each physical event. Any mismatch blocks NGINX acceptance rather than
being repaired in a receipt or report.

## Checks not run and rationale

Exact-head #410/#416 host, report, Sonar and GitHub checks are not run at this
product-stage checkpoint because the product change has not yet been committed
and integrated. Deployment and master merge are outside the authorized task.

## Final diff and review status

The product change is limited to NGINX event projection and NGINX-owned checks,
fixtures and paired documentation. Final commit/remote revision and exact-head
host evidence remain pending. This record does not authorize merge.
