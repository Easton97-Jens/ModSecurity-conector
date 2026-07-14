# Codex extensions

**Language:** English | [Deutsch](codex-extensions.de.md)

## Purpose and scope

This document describes the controlled Codex extension profile for the Parent
repository. It records repository-local skills, reviewed official plugins, and
external MCP candidates. It does not transfer an extension to the
`modules/ModSecurity-test-Framework` submodule, enable a network service, or
claim that an installed extension has completed a runtime smoke test.

The machine-readable source of truth is
[`ci/tooling/codex-extensions.lock.yml`](../../ci/tooling/codex-extensions.lock.yml).
It pins every reviewed upstream source or marks a repository-authored entry,
records data/secret/write boundaries, and carries a status rather than an
assumption of safety.

## Authority and source policy

The following precedence order applies to every extension:

1. System and user instructions.
2. `AGENTS.md` and repository policies, including security, storage, delivery,
   bilingual documentation, and Parent/Framework boundaries.
3. Repository-owned local skills in `.agents/skills/`.
4. Security and compatibility adapters for installed plugins.
5. Third-party skill, plugin, MCP, marketplace, and general guidance.

An extension is considered only after its official source, immutable revision,
license, scripts, dependencies, network behavior, credential flow, data
egress, cost model, write capability, and update path have been reviewed. A
directory or marketplace listing is discovery material, not installation
authority. The repository does not vendor opaque binaries or helper scripts
that retrieve authenticated GitHub review/check data.

Repository-local skills are versioned under `.agents/skills/`; their
`UPSTREAM.md` files preserve source URL, commit, imported-file scope, local
adaptation, and update procedure. Required upstream license text is retained
with the adapted material. A source without a verified license is not vendored.

## Repository-local skills

| Local skill | Status | Intended use | Deliberate boundary |
| --- | --- | --- | --- |
| `create-plan` | `adapted_and_vendored` | Evidence-backed plans for material changes | Planning neither publishes nor expands scope |
| `gh-fix-ci` | `adapted_and_vendored` | Exact-SHA task-owned GitHub Actions triage | No vendored log-retrieval helper or credential output |
| `gh-address-comments` | `adapted_and_vendored` | Classifying and addressing current PR feedback | No vendored authenticated review-data helper |
| `stop-slop` | `adapted_and_vendored` | Final prose-only clarity and unsupported-claim review | Does not change technical literals, evidence, or safety caveats |
| `valyu-research` | `enabled` | Bounded research planning | Does not enable or invoke Valyu |
| `modsecurity-codebase-migrate` | `enabled` | Parent/Framework-aware migration planning | Does not authorize a Framework change |
| `bilingual-changelog-generator` | `enabled` | Explicit paired English/German release/changelog documentation | Does not invent verification results or create releases |
| `third-party-skill-audit` | `enabled` | Pre-install provenance and behavior review | Does not execute an unreviewed extension |

The four adapted skills retain fixed source commits: OpenAI's historical
`create-plan` source at `a5119697b819090e00e5d11ee1d86834d7c1043a`, the
OpenAI GitHub plugin sources at
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`, and `stop-slop` at
`8da1f030185bdfe8471220585162991eaeb970e9`. The historical origin of
`create-plan` is intentionally labeled as historical rather than treated as a
current moving upstream branch.

## Routing contract

The contract tests validate declared routing text; they do not prove an
interactive Codex router's dispatch behavior. The expected positive and
negative boundaries are:

| Extension or service | Use when | Do not use when |
| --- | --- | --- |
| `create-plan` | A material implementation needs an evidence and verification plan | A one-step factual answer needs no repository plan |
| `gh-fix-ci` | A task-owned GitHub Actions check failed | There is no exact failed PR check |
| `gh-address-comments` | Existing PR feedback needs a scoped response | A broad review is requested without existing comments |
| `stop-slop` | Draft prose contains vague or unsupported claims | Facts/security conclusions have not been established |
| `valyu-research` | Current authoritative external research is necessary | Sensitive data would leave the repository or Valyu activation is requested |
| `modsecurity-codebase-migrate` | Ownership or compatibility may move across components | A local defect has no migration boundary |
| `bilingual-changelog-generator` | An explicit bilingual release/changelog request has a commit/tag range | Ordinary project documentation is needed without a release/changelog request |
| `third-party-skill-audit` | An external skill, plugin, or MCP is proposed | The source cannot be fixed to an auditable revision |
| WarpGrep/Morph | A later approved codebase-search integration is needed | Tool filtering and source behavior remain unverified |
| Valyu MCP | A later approved external-research integration is needed | Its secret transport and effective tool inventory remain unsafe/unverified |

## Reviewed plugins

| Plugin | Fixed official source | Observed version | Status | Boundary |
| --- | --- | --- | --- | --- |
| Superpowers | `openai/plugins` curated snapshot at `bd2122cb92f2ade874d8c2b1d00383976ab9415b` | `5.1.3` | `installed_pending_reload` | Local compatibility policy overrides any conflicting generic workflow; no unreviewed MCP, destructive cleanup, autonomous publish, or policy bypass is allowed |
| Codex Security | `openai/plugins` curated snapshot at `bd2122cb92f2ade874d8c2b1d00383976ab9415b` | `0.1.11` | `enabled` | Its local Node-backed MCP runtime was not exercised; no security scan is implied by this integration |

Superpowers is installed only from the reviewed official plugin source at the
fixed commit. Its repository-local compatibility policy is ignored local
configuration, so it is intentionally not a versioned product contract. A
fresh Codex session is required before an `installed_pending_reload` state can
be treated as active.

The reviewed Superpowers manifest at that snapshot declares its skill bundle
and no MCP-server, application, or hook declaration. Its bundled helper
scripts were reviewed separately; process-control and temporary-directory
cleanup are prohibited unless a bounded task separately authorizes them.

Codex Security was already an installed official plugin. This task inventories
its source and boundaries only. It neither triggers a repository scan nor
enables write-capable tracker or GitHub application actions. The available
runtime lacks Node.js, so its bundled local MCP server has no runtime evidence.

The GitHub workflow adapters above are versioned local skills. They do not copy
user-scoped GitHub configuration or credentials into this repository and they
do not replace the repository's PR and delivery policies.

## External MCP candidates

| Candidate | Status | Reason | Approved interface claim |
| --- | --- | --- | --- |
| Morph `@morphllm/morphmcp@0.8.206` | `blocked_source_unverified` | Package metadata is pinned, but independently auditable effective source behavior and Codex-side tool filtering were not established | Requested future allowlist: `codebase_search`, `github_codebase_search`; not configured or asserted effective |
| Valyu hosted MCP | `blocked_source_unverified` | Documentation passes the API key in a URL and lists tools different from the requested names | No mapping from `knowledge` or `feedback`; not configured |
| `valyuAI/valyu-mcp` candidate | `blocked_license_unknown` | No verified license; setup/logging behavior increases secret and query-data risk | No tools approved |

No Morph or Valyu key is stored in a repository file, local project
configuration, documentation example, or test fixture. No request was made to
either paid external service during this integration. See
[External agent services](../security/external-agent-services.md) for data,
cost, credential, and revalidation details.

If Morph is later approved, use it only for semantic exploration of unknown
large code paths, distributed implementations, or architecture/call-path
questions. Treat its results as search hints and validate every finding locally.
Use `rg` for an exact string, exact symbol, known regular expression, or a small
local search; do not route those cases to an external codebase service.

## Framework disposition

This change modifies only the Parent repository. It does not edit, commit,
push, or advance the Framework gitlink. A globally installed official plugin
may be visible to a separate Framework session, but repository-local adapters
are not transferred by this change. Any Framework adoption needs its own task,
provenance audit, tests, documentation, commit, push, and CI evidence.

## Update, rollback, and removal

1. Re-run the third-party skill audit before changing an external extension.
2. Resolve a new immutable revision, license, behavior, data/secret flow, and
   tool boundary; do not substitute a moving branch or a similarly named tool.
3. Update the lock manifest, local provenance, contract tests, English/German
   documentation, and Change Record together.
4. Remove or disable the affected extension when a boundary cannot be proven;
   retain the lock entry with its truthful blocked/rejected status.
5. Verify the focused contract target and the normal documentation/diff checks
   before ordinary repository delivery.

The extension profile is intentionally conservative: a documented blocked
candidate is a successful control outcome, not an invitation to bypass it.
