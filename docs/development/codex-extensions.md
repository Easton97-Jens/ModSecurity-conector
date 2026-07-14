# Codex extensions

**Language:** English | [Deutsch](codex-extensions.de.md)

## Scope

This repository shares focused workflow guidance under
<code>.agents/skills/</code>. Local Codex settings remain excluded from Git:
they protect one trusted checkout without becoming a product configuration or a
substitute for repository policies.

Read the active <code>AGENTS.md</code> and applicable repository policies
before using an extension. The Parent owns these skills and checks; the
Framework remains a separate repository and is never changed by this layer.

## Shared repository skills

| Skill | Use for | Do not use for |
| --- | --- | --- |
| <code>security-finding-lifecycle</code> | Evidence-backed finding capture, validation, reachability, fix, and regression work | An unvalidated scan result or automatic remediation |
| <code>ci-failure-triage</code> | Exact-SHA GitHub Actions investigation with a comparable <code>master</code> run | Preemptive workflow changes or an older run |
| <code>delivery-ci</code> | Scoped delivery from final diff through draft PR and final-SHA CI | Direct <code>master</code> delivery or an unverified result |
| <code>bilingual-change-record</code> | English/German parity and Change Record reconciliation | Translating source code or inventing evidence |
| <code>connector-test-matrix</code> | Separate CRS/MRTS and H1/H2/H3 assessment | Treating one transport/profile result as all coverage |
| <code>framework-parent-handoff</code> | A real Framework-to-Parent handoff | Parent-only work or a Framework Gitlink change without Framework delivery |
| <code>dependency-security-update</code> | Small, separated dependency security updates | Broad dependency refreshes without renewed verification |
| <code>optional-prerequisite-ci</code> | Honest optional-prerequisite status handling | Hiding real failures with blanket success behavior |

Each skill has a concise <code>SKILL.md</code> and generated
<code>agents/openai.yaml</code>. The versioned validator checks frontmatter,
unique names, required workflow sections, relative links, user-specific paths,
secret-shaped content, and unsafe default command examples.

## Local read-only agents

The following ignored files use the current project-local Codex agent schema and
set <code>sandbox_mode = "read-only"</code>:

| Local agent | Review boundary |
| --- | --- |
| <code>repo-explorer</code> | Architecture, call paths, and Parent/Framework ownership |
| <code>security-reviewer</code> | Memory, privacy, path, supply-chain, protocol, and reachable dependency risks |
| <code>test-evidence-reviewer</code> | Acceptance criteria, test gaps, and evidence limits |
| <code>bilingual-doc-reviewer</code> | Semantic EN/DE parity of paths, commands, statuses, limits, and risks |
| <code>ci-triager</code> | Final SHA, PR/push runs, and comparable <code>master</code> evidence |

They do not edit, stage, commit, push, delete, retry CI, change branch
protection, or make a finding valid by assertion. There are intentionally no
German copies of local agent files. Their empty <code>[mcp_servers]</code>
table prevents inherited MCP servers from widening a read-only review.

## Local hooks

<code>.codex/hooks.json</code> uses the official project-local hook schema.
Codex must review and trust changed non-managed hooks through
<code>/hooks</code>; restart or resume the session after local hook changes.

| Event | Deterministic check | Decision |
| --- | --- | --- |
| <code>SessionStart</code> | Expected Git root, trusted project configuration, <code>on-request</code>, <code>workspace-write</code>, requirements exclusions, temporary root, and Parent/Framework presence | Adds an explicit configured or blocked diagnostic; it does not replace Codex enforcement |
| <code>PreToolUse</code> for <code>Bash</code> | Broad staging, force push, hard reset, direct <code>master</code> push, recursive deletion outside the temporary root, and protected staging paths | Denies the supported dangerous tool call without echoing its command |
| <code>PermissionRequest</code> for <code>Bash</code> | Rechecks the same dangerous command categories before an escalation prompt | Denies the request when the category is blocked |

The hook policy never downloads data, prints tokens or command contents,
commits, pushes, deletes product files automatically, or replaces the Codex
sandbox, approval policy, or <code>requirements.toml</code>. It is a
deterministic command guardrail, not a product-security verdict.

The versioned contract tests use synthetic commands for the local policy:
dangerous Git commands are denied, read-only commands remain allowed, protected
paths are excluded from staging, and output does not contain a synthetic secret.

## MCP disposition

| MCP capability | Status | Rationale |
| --- | --- | --- |
| Official OpenAI developer documentation MCP | Locally configured; session reload required | It provides authoritative read/search material for Codex schema questions without a repository credential |
| Official GitHub MCP server | <code>documented_only</code> | Existing <code>gh</code> access already covers the required read operations; no additional configured read surface was proven necessary |

No token, access credential, or broad write tool allowlist is stored in a
repository or local extension file. The documentation MCP is read-only by
selection. A GitHub MCP may be reconsidered only after a documented, read-only
gap is shown and a safe authentication mechanism is available.

## Validation and maintenance

Run the shared checks from the repository root:

```sh
make check-codex-skills
python3 -m unittest -v tests.test_codex_skills tests.test_codex_hook_policy
python3 -m json.tool .codex/hooks.json
```

The last command is local-only and applies only after the ignored hook files
have been installed. Do not stage <code>.codex/</code>, <code>.rtk/</code>,
<code>AGENTS.md</code>, <code>RTK.md</code>, local analysis output, temporary
or build trees, or possible secret files.

When Codex changes its documented skill, agent, or hook schema, review the
official documentation, update the versioned skill contract first, update
ignored local files only after that review, run the focused tests, inspect
<code>/hooks</code>, and restart the trusted session. Do not copy local
configuration into a commit.

## Related references

- [Repository concept](../repository-concept.md)
- [Architecture](../architecture.md)
- [Change traceability](../change-traceability.md)
- [CI security tooling](../security/ci-security-tooling.md)
- [Official Codex documentation](https://developers.openai.com/codex/)
