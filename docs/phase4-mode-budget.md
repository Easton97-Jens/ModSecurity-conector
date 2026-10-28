# Body-limit ownership and Phase-4 mode

**Language:** English | [Deutsch](phase4-mode-budget.de.md)

## Ownership

Request inspection limit and action belong to `SecRequestBodyLimit` and
`SecRequestBodyLimitAction`; the independent native `SecRequestBodyNoFilesLimit`
also applies to non-file request data. Response inspection limit and action
belong to `SecResponseBodyLimit` and `SecResponseBodyLimitAction`.
The connector must not supply a body-limit default, infer one from rule text,
inject directives, choose Reject/ProcessPartial, or truncate a body before the
engine. Omitted directives retain native libModSecurity semantics.

| Concern | Owner | Behavior |
| --- | --- | --- |
| P2/P4 inspection and limit actions | libModSecurity | Native directives, results and interventions govern inspection. DetectionOnly retains actual engine semantics. |
| Access and response MIME scope | libModSecurity | `SecRequestBodyAccess`, `SecResponseBodyAccess` and response MIME directives remain native configuration. |
| Input and phase completion | Connector | Offer complete valid chunks, capture native results at every append, retain a disruptive result through EOS, and complete each phase once. |
| Late P4 handling | Connector/host | `off`, `safe`, `strict` select supported host intervention handling, never a body size or limit action. |
| Safety | Connector/host | Retain checked arithmetic, valid pointers, bounded individual frames/messages, descriptors, file ranges, metadata, timeouts and bounded working memory. |

## Removed configuration

Remove `request_body_limit`, `body_limit_action`,
`modsecurity_request_body_limit`, `modsecurity_body_limit_action`,
HAProxy `request-body-limit`, Envoy `max_request_body_bytes`, and Traefik
`maxRequestBodyBytes`. The previously removed response options remain removed:
`response_body_limit`, `modsecurity_response_body_limit`,
`modsecurity_phase4_body_limit`, HAProxy `response-body-limit`, and Envoy
`max_response_body_bytes`. Removed options fail configuration rather than being
silently ignored. There is no replacement cumulative connector size option.
Operators use their normal engine rule configuration; no additional connector
limit is required.

## Working memory and transport

An incremental work buffer is reused until EOS; its capacity does not determine
the allowed total body size. NGINX file input retains descriptor, regular-file,
range and checked-read validation. MRC1 uses individual 32-KiB body chunks and
64-KiB frames; Traefik UDS and Envoy gRPC retain message controls. Header/event
metadata, correlation registries and inactivity/lifetime timeouts remain bounded.
Private file spooling allows the stock lighttpd sidecar to inspect incrementally
while withholding upstream replay until native P2 allows it. Disk errors remain
technical failures, rather than selecting an inspection prefix or limit action.

For requests, `bytes_inspected=0` means unknown/unproven; retained bytes do not
prove inspection. For responses it counts bytes offered to the engine, not the
native ProcessPartial prefix. An append return value of 0 is operation-specific and must not be
misreported as allocation or file failure when native ProcessPartial permits it.
Native Request Reject may report HTTP 403 during append, whereas another native
path may report 413; the connector preserves the actual result through EOS.

## Active total-body limitations

Full removal is not claimed for authorization profiles with bounded host buffers.
These constraints remain distinct from native engine policy and are not renamed
as working-buffer capacity:

| Active path | Actual scope | Limitation |
| --- | --- | --- |
| Envoy ext_authz request authorization | Host `max_request_bytes` in selected templates (4096 or 33 bytes) | A bounded full request sample reaches authorization; a response observer does not make request ingestion incremental. |
| Traefik forwardAuth request authorization | Host `maxBodySize` in selected templates (4096 or 33 bytes) | The host buffers the forwarded request body; the observer cannot remove this request ceiling. |
| Composite Traefik authorization response | Host `maxResponseBodySize=32768` | Bounds the authorization response, not the upstream application's response body. |
| HAProxy SPOE/SPOP request sample | One bounded protocol message containing `req.body` | An incomplete sample cannot establish complete P2 inspection; native HTX is a separate profile. |

The native streaming profiles do not inherit these authorization limits.
Envoy ext_authz templates use `allow_partial_message: false`; explicit partial
or ambiguous `x-envoy-auth-partial-body` metadata is rejected before native
transaction creation. This checks transport completeness, not a connector
inspection size or action. The host sample ceiling remains an open limitation.
For the composite profile, a pre-authorization host buffer rejection remains
413 only with internal host provenance; it creates no native decision or EOS.
Changing an authorization profile into native streaming would change its host
contract and requires separate evidence. Independent host request-size controls,
such as lighttpd `server.max-request-size`, remain host configuration.

## Verification

Inspection fixtures explicitly select native limits/actions, including the
request no-files limit; helpers supply no implicit defaults. HAProxy samples use
`req.body_size` and `http_version=req.ver`; incomplete or contradictory samples
fail before engine admission. Unknown/chunked framing and unframed HTTP/2 remain
unsupported on that sample route; native HTX provides streaming. Apache preserves
native response Reject at append, including prior FLUSH/body commitment, and
withholds the rejected brigade under Safe log_only.

Builds and component contracts do not establish complete hosted HTTP/1–HTTP/3,
buffer-ownership or late-abort acceptance. See the
[ten-profile matrix](body-inspection-review-matrix.md) for route boundaries and
the [current PR #382 closeout](pr-382-merge-readiness.md) for current results.
