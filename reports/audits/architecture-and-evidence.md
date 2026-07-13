# Architecture and evidence audit

**Language:** English | [Deutsch](architecture-and-evidence.de.md)

## Scope

This audit consolidates the retained architectural and evidence-relevant
findings for the six selected connectors. It is a source and contract audit;
runtime PASS statements remain limited to the canonical run recorded in
[core completion](../current/core-completion.md).

## Shared architecture contract

The Common SDK exposes one transaction lifecycle: begin, request headers,
request-body append/finish, response headers, response-body append/finish,
and transaction finish/destroy. Host adapters own their hook timing and keep
body chunks borrowed for the call; the Common contract does not authorize
connector-owned full-response buffering.

Runtime roots are derived per connector beneath the caller-selected
`VERIFIED_RUN_ROOT`. Evidence, build, run, and log roots are isolated, while
the reusable component cache is scoped as `cache-v2/shared`. This is path and
cache plumbing, not connector runtime proof by itself.

| Connector | Selected host route | Audit-relevant boundary |
| --- | --- | --- |
| Apache | native httpd module | Host filters determine commitment and EOS timing. |
| NGINX | native HTTP module | Filter order and EOS determine response-body completion. |
| HAProxy | native HTX filter | Native HTX is distinct from the SPOP compatibility route. |
| Envoy | `ext_proc` | Streamed processing is distinct from `ext_authz` compatibility. |
| Traefik | native local-plugin middleware | Native middleware is distinct from `forwardAuth` compatibility. |
| lighttpd | patched native Entity-Body host | The selected response-body path is version-pinned and patched. |

## Evidence and transport boundary

The selected shared HTTP/1.1 core run observed P1--P4 rule handling, Safe
late action, first-byte-before-EOS, no full response buffer, event privacy,
and cleanup for each selected host route. Its complete bounded statement is
kept in [core completion](../current/core-completion.md); the current status
and remaining scope are kept in [readiness](../current/readiness.md).

For the selected Safe evidence, a post-commit requested `deny` resolves to
actual `log_only`, leaves visible HTTP 200, and does not abort the connection.
The audit does not convert that outcome into a pre-commit denial or a strict
transport result. Events are metadata-only: transaction/rule identifiers,
actions, timing and byte counters may be recorded, but request or response
body payloads are not evidence fields.

## Configuration and evidence governance

- Registered connector options, Common Runtime keys, ModSecurity directives,
  and example-rule syntax are tracked by the generated
  [configuration inventory](../connector-configuration-inventory.json).
- Generated runtime reports remain governed by the report registry and the
  `make report-governance` layout check. The generated evidence is not edited
  as a substitute for a new runtime run.
- Compatibility routes are documented as compatibility routes; they do not
  replace the selected native core route or promote its capabilities.

## Historical context

Earlier Common-adoption, local-build, runtime-root, transport, promotion, and
pre-host-integration audits are consolidated here. Their detailed planning,
temporary environment observations, and pre-core status matrices are not
current evidence. Git history retains those snapshots without leaving parallel
current reports.

## Claims deliberately not made

- production readiness, production hardening, runtime security, or security
  verification;
- CRS verification or completeness;
- complete connector-matrix, HTTP/2, or HTTP/3 verification; or
- strict post-commit enforcement beyond the selected core evidence.
