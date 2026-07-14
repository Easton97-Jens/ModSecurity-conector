# External agent services

**Language:** English | [Deutsch](external-agent-services.de.md)

## Scope

This document sets the privacy, secret, data-egress, cost, and activation
boundary for Codex extensions that communicate with an external service. It is
not a service endorsement, does not configure a credential, and does not prove
that a remote service or tool filter is safe.

The current extension inventory and immutable provenance are in
[`ci/tooling/codex-extensions.lock.yml`](../../ci/tooling/codex-extensions.lock.yml).
The current overall posture is `partial_extension_integration`: repository
skills and documented plugin controls exist, while external MCP candidates
remain blocked.

## Non-negotiable controls

- Store no API key, bearer token, OAuth material, cookie, private key,
  certificate, request payload, response payload, or private host path in the
  repository, a versioned test fixture, documentation, or a lock manifest.
- Use only a secret reference from the approved runtime environment after the
  service's secret-transport design and tool inventory are verified. Never put
  a key into a URL.
- Treat source code, repository structure, query text, review data, paths, and
  search results as externally processed data when a hosted MCP is involved.
- Obtain explicit authority before a paid request, a new third-party
  application connection, or a service that can write outside the task scope.
- Use an allowlist only when the client and service provide a documented,
  verifiable enforcement point. A desired list is not a security control by
  itself.
- Log only minimum non-secret metadata needed to explain a decision. Do not
  retain remote payloads in evidence files.

## Morph / WarpGrep candidate

| Attribute | Reviewed value |
| --- | --- |
| Candidate | `@morphllm/morphmcp@0.8.206` |
| Package source revision | `ac38aadb555519751cee042a77f0d2cd5e9b01e1` |
| Package license metadata | MIT |
| Documented credential name | `MORPH_API_KEY` |
| Status | `blocked_source_unverified` |
| Paid-service behavior | No request was made; the service has usage-priced external processing |

The package metadata was pinned and its integrity data was recorded during
review. That is insufficient to establish the behavior of all effective MCP
tools or a Codex-side filter. The public documentation describes a command that
uses a package runner and `MORPH_API_KEY`; Node.js is unavailable in the current
runtime, so no package execution, key check, tool-list call, or paid request was
performed.

The requested future exposure is limited to `codebase_search` and
`github_codebase_search`. The names were recorded as a desired allowlist, but
no configuration claims to enforce them. The documented server behavior also
requires scrutiny for editing or other non-search tools. Until immutable source
behavior and a real enforcement mechanism are independently verified, the MCP
is not configured, enabled, or run.

Using such a service could transmit repository structure, search questions, and
relevant code snippets to Morph. The reviewed pricing information reported
`$0.80` per million input/output tokens; a task must treat that as an external
cost boundary, not as permission to call the service.

## Valyu candidates

### Hosted MCP

The official hosted documentation uses an endpoint shaped like
`https://mcp.valyu.ai/mcp?valyuApiKey=...&maxPrice=50`. A credential in the URL
violates this repository's secret boundary because URLs can enter process
arguments, diagnostics, history, proxies, or logs. Therefore the hosted MCP is
not configured.

The documented inventory includes tools such as `valyu_search`,
`valyu_academic_search`, and `valyu_contents`. It does not establish tools
named `knowledge` or `feedback`; this integration does not silently map either
requested name to a different service operation. Valyu documents paid searches
with a minimum price of `$0.01` per search. No key validation, tool list, or
paid request was performed.

### Local repository candidate

The reviewed `valyuAI/valyu-mcp` candidate at
`546c3d2f2a113f0c97007eb21da0f168387bbcef` has no verified license in the
reviewed source. Its setup writes a local environment file and its behavior can
log queries and full responses. It is `blocked_license_unknown`, is not
vendored, and has no approved tools.

## Official plugin boundaries

| Extension | Current control |
| --- | --- |
| Superpowers | Installed only from the fixed official `openai/plugins` revision. Its local compatibility policy gives system/user/repository rules priority and disallows unreviewed MCP, destructive cleanup, automatic publication, and policy bypass. A session reload is still required. |
| Codex Security | Official plugin inventory only. The bundled Node-backed MCP has no runtime evidence because Node.js is absent. No security scan or write-capable application action was initiated by this work. |
| GitHub workflow adapters | Versioned local adaptations. They omit upstream scripts that fetch authenticated check logs or review comments and do not copy user-scoped configuration or credentials. |

The existing user-scoped extension configuration is outside this repository
scope. It must be treated as secret-bearing configuration and is neither copied
nor normalized by this change.

## Revalidation and incident response

Before enabling a blocked candidate, complete all of the following:

1. Re-resolve official immutable source, license, maintainer, version, and
   package integrity.
2. Audit scripts, dependencies, subprocesses, network endpoints, data egress,
   credential handling, logging, write actions, and cost behavior.
3. Prove the actual Codex/MCP allowlist and disable mechanism using documented
   tool names. Do not infer an allowlist from prose.
4. Keep the credential in an approved environment-only reference; verify only
   presence/non-presence without printing its value.
5. Obtain separate authority for paid calls or new external connections, make a
   bounded non-sensitive smoke test, and record exact scope/result evidence.
6. Update the lock manifest, tests, English/German documentation, and Change
   Record before reporting the candidate enabled.

If a credential is observed in a repository-controlled or command-visible
location, stop handling it, avoid echoing or copying it, remove it only with
appropriate authority, rotate/revoke it through the credential owner, and
record a non-secret remediation status. A blocked service remains blocked until
that response and revalidation are complete.

## Related references

- [Codex extensions](../development/codex-extensions.md)
- [Operations and security](../operations-and-security.md)
- [Change traceability](../change-traceability.md)
