# FND-PARENT-0022 — CodeQL reflected-XSS alerts #14 and #15 lack a connector-owned request-header-to-body path

| Field | Record |
| --- | --- |
| Priority / status | P2 / closed (archived) |
| Ownership | Parent / Traefik native middleware |
| Scope | `connectors/traefik/native_middleware` at `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| GitHub state | #14 and #15 are dismissed as `false positive`; neither is marked fixed. |
| Final disposition | `false_positive_in_connector_scope` |
| Feasibility | `not_applicable` for a connector patch; the only remaining risk is an external downstream renderer outside this connector scope. |

## Current alert evidence

| Alert | GitHub source | GitHub sink | Component disposition |
| --- | --- | --- | --- |
| #14 | `middleware.go:356:40-54` | `middleware.go:656:30-37` | Already safe at this sink: the call is guarded by `len(payload) == 0` and forwards zero body bytes. |
| #15 | `middleware.go:356:40-54` | `middleware.go:688:42-47` | No connector-owned reflection: it forwards a nonempty chunk supplied by an external downstream handler. |

Immediately before their authorized disposition, both were current, open
CodeQL 2.26.1 `go/reflected-xss` results with `error` / high security severity
in Traefik Go analysis `1495452276`. The GitHub REST response identifies source
and sink but did not return an expanded intermediate `codeFlows` sequence; no
workflow artifact was available.

## GitHub disposition

Immediately before each PATCH, the alert number, `go/reflected-xss` rule ID,
open state, `c8ca0d92b630c18232b881855c4f5d1482568ea6` revision, source link,
file/sink, and the matching retained evidence were rechecked. GitHub then
returned the following final alert state:

| Alert | State / reason | Timestamp | Analyzed source and sink | `fixed_at` |
| --- | --- | --- | --- | --- |
| #14 | `dismissed` / `false positive` | `2026-07-18T08:55:32Z` | `middleware.go:356:40-54` → `middleware.go:656:30-37` | `null` |
| #15 | `dismissed` / `false positive` | `2026-07-18T08:58:49Z` | `middleware.go:356:40-54` → `middleware.go:688:42-47` | `null` |

GitHub comment for #14 (verbatim):

> The reported sink is reachable only when len(payload) == 0 and therefore
> writes no response-body bytes. The reported source cannot be reflected
> through this sink. Focused boundary tests confirmed a zero-byte body.

GitHub comment for #15 (verbatim):

> The connector forwards bytes produced by an externally supplied downstream
> handler. It does not render the reported source into an HTML or browser
> execution context. Context-specific encoding remains the responsibility of
> any downstream renderer that constructs such content.

## Administrative closure

At `2026-07-18T09:43:15Z`, this finding was administratively closed with
`final_disposition: false_positive_in_connector_scope`. The current alert
record, exact analyzed SHA, source and sink locations, `fixed_at: null`, and
all five retained evidence artifacts support that closure. This is a
connector-scope false-positive disposition, not a claim that either alert was
fixed and not a risk acceptance for a downstream deployment.

The separate temporary-root finalization condition is tracked as
[`FND-HOST-0005`](../FND-HOST-0005/finding.md) with
`blocked_environment` / `temporary_exceed`. It has no bearing on the GitHub
alert state or this connector-scope closure, and no cleanup was performed.

## Source-to-response analysis

The request header is bounded and passed to `Transaction.ProcessHeaders`:

```text
request.Header → boundedHeaders → processHeaders → Engine decision
```

A disruptive request-header decision returns before construction of the wrapped
response writer or invocation of `next.ServeHTTP`. Middleware-generated failure
and denial responses clear headers, set `text/plain; charset=utf-8`, and write
fixed literals. The engine result contains only action, status, and optional
redirect location; it cannot supply the reported response-body bytes.

For #14, `responseWriter.Write` is in the empty-payload branch, so `target.Write`
receives no bytes. For #15, the response writer chunk comes from the
Traefik-provided `next` handler. The connector does not assign request headers,
metadata, or an engine result to that chunk.

An application-level reflection needs an additional external path:

```text
request header → downstream handler reads it → handler renders unsafe browser context
→ transparent middleware forwards handler bytes
```

That handler was not found in the authorized Parent connector source.

## Controls, compatibility, and test evidence

- The task-owned Go boundary probe passed with HTML, attribute, script, URL,
  encoded, double-encoded, empty, Unicode, and invalid-UTF-8 variants.
- A safe downstream HTML response never contained the controlled header.
- The #14 empty-write branch committed a zero-byte body.
- A pre-request denial emitted only `request rejected\n` with fixed text/plain
  and never called the downstream handler.
- A deliberately unsafe downstream HTML echo preserved input exactly. This is
  a control proving the output-context ownership belongs to that handler, not
  a connector vulnerability or a middleware sanitizer.
- `make -C connectors/traefik test-native-middleware` and
  `build-native-middleware` both passed with task-owned caches/build output.

Global HTML escaping or forcing `text/plain` in the streaming adapter is not a
safe remediation: it would corrupt HTML, JSON, binary, already-encoded, and
streaming response semantics, and would not establish a context-correct output
encoder.

## Required next action

Do not change or suppress the connector for these dismissed connector-local
false positives. If a specific deployment’s downstream handler becomes in
scope, trace that handler and apply context-specific encoding at its actual
HTML/attribute/JavaScript/URL renderer, then add renderer-owned regression,
legitimate-control, and bypass tests. The dismissal does not assess, remediate,
or risk-accept that downstream deployment path.

## Evidence and residual risk

The canonical JSON record lists checksummed current GitHub inventory, probe,
connector validation, and disposition artifacts under runs
`20260718T074759Z-codeql-xss-alerts-14-15-87ada941` and
`20260718T084215Z-github-code-scanning-disposition-14-15-babc842c`.

#14 has no component-local reflected-body path. #15 can participate in a real
application-level XSS only if an external downstream handler renders an unsafe
reflection into an HTML, script, attribute, or URL context without
context-correct encoding. That deployment path is not proven, assessed,
remediated, or risk-accepted by this task. No product code, product test,
Framework, MRTS, gitlink, commit, or pull request changed.

## History

- `2026-07-18T08:18:55Z`: current alerts were triaged with retained
  connector-boundary evidence; no state change was made.
- `2026-07-18T09:02:09Z`: GitHub recorded #14 and #15 as dismissed / `false
  positive`; `fixed_at` remains `null` for both.
- `2026-07-18T09:43:15Z`: administratively closed as
  `false_positive_in_connector_scope`; the only retained risk is an external
  downstream renderer that emits unsafe context-dependent output.
