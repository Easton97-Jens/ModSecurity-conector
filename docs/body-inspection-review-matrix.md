# Body-inspection review matrix

**Language:** English | [Deutsch](body-inspection-review-matrix.de.md)

This is the concise current route map for PR #410. It distinguishes source and
component evidence from complete hosted HTTP acceptance; no row claims a full
I12 or V08–V10 matrix.

| Profile | Request / response route | Current boundary |
| --- | --- | --- |
| Apache native | Memory/file request chunks reach P2; APR response brigades reach P4 and preserve native Reject through EOS. | Component/APR controls exist; a complete current httpd protocol/commit matrix is not established. |
| NGINX native | Validated memory/file input is incremental; response chunks and once-only EOS reach P4. | Source/contracts exist; a complete current hosted memory/file and late-abort matrix is not established. |
| HAProxy native HTX | Borrowed HTX request/response blocks and EOS use the native streaming path. | Separate integrated qualification is required for the full protocol/Strict matrix. |
| HAProxy SPOE/SPOP | A complete frame-representable request sample is admitted only when typed total, framing and sample length agree; the native HTX companion owns response streaming. | Unknown/chunked or unframed HTTP/2 samples are unsupported here; use native HTX for full streaming. |
| Envoy ext_proc | Streamed request and response messages reach P2/P4; capacity is per message. | Source and native/CGo component evidence does not replace the full ext_proc host matrix. |
| Envoy ext_authz + observer | The host buffers one authorization request sample; the independent observer supplies response chunks and EOS. | `max_request_bytes` is a host sample limit; partial or ambiguous metadata fails before native allocation. |
| Traefik native UDS | Incremental request and application-response chunks use the engine UDS path. | Component/protocol evidence exists; full hosted protocol/commit acceptance remains separate. |
| Traefik forwardAuth + observer | Authorization requests are host-buffered; the observer independently handles the application response. | `maxBodySize` is a host request limit; `maxResponseBodySize=32768` bounds only the authorization reply. |
| lighttpd stock sidecar | Incremental input is privately spooled with bounded RAM and replayed only after native Allow; response failures do not replay. | Current component evidence includes an unchanged RST-delivery gap; full deployment probes remain separate. |
| lighttpd patched native | Validated memory/file chunks reach P2 and response chunks/EOS reach P4. | Source/contracts exist; a complete current patched-host matrix is not established. |

## Shared contract

- Native engine directives own inspection limits and actions. The connectors do
  not infer limits from rules, inject directives, or choose inspection prefixes.
- Offered, retained, and proven inspected bytes are different facts.
  DetectionOnly does not manufacture a disruptive result.
- Common completes P2/P4 once, preserves the first technical error, and rejects
  re-entry after terminal failure. EOS is recorded only when supplied by the host.
- Pointer, range, descriptor, frame, timeout and correlation bounds are safety
  controls, not cumulative body budgets.

## Remaining limits

| Limit | Meaning |
| --- | --- |
| `SecRequestBody*` / `SecResponseBody*` | Native engine policy. |
| Envoy `max_request_bytes` | Complete authorization-sample ceiling; use ext_proc for streaming. |
| Traefik `maxBodySize` | Complete authorization-request ceiling; use native UDS for streaming. |
| Traefik `maxResponseBodySize=32768` | Authorization-reply memory protection, not application-response inspection. |
| HAProxy SPOP frame/message size | One bounded complete sample; inconsistent or unsupported framing fails before the engine. |

Builds, static contracts and component tests prove only their own layers. The
current delivery result and open evidence boundaries are recorded once in the
[current PR #382 closeout](pr-382-merge-readiness.md).
