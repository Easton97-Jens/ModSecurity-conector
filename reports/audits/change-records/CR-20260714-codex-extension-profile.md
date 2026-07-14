# Change Record: Controlled Codex extension profile

**Language:** English | [Deutsch](CR-20260714-codex-extension-profile.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Controlled Codex extension profile |
| Change ID | CR-20260714-codex-extension-profile |
| Date (UTC) | 2026-07-14 |
| Author or executing agent | Codex agent <code>/root</code> |
| Base revision | <code>be0356af96ef582c3a7dbc0169c7c8b27b7b6b34</code> |
| Related issue or pull request | Pending draft pull request |
| Final revision | Pending final delivery commit |

## Motivation and problem statement

Establish a controlled, auditable Codex extension profile for the Parent
repository. The profile must preserve fixed provenance and license information,
provide repository-local policy adapters and deterministic checks, install only
a reviewed official plugin, and leave unverified or unsafe external MCP
services disabled.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Every considered extension has source URL, fixed revision or truthful blocked state, version, license, capability boundary, and update policy | Met | <code>ci/tooling/codex-extensions.lock.yml</code> and extension contract tests |
| Requested repository-local skills are present with frontmatter, provenance, and required licenses | Met | Eight skill directories and focused contract tests |
| Superpowers is installed only from the official curated snapshot and constrained by an ignored local compatibility policy | Met, pending session reload | Plugin inventory reports version snapshot <code>bd2122cb</code>; local policy is not staged |
| Existing Codex Security remains an official enabled plugin without a scan being implied | Met | Plugin inventory and documented no-scan boundary |
| Morph/WarpGrep and Valyu MCP candidates are not configured, enabled, or called without verifiable source/tool/secret controls | Met | Lock statuses, documentation, absent-key presence check, and no paid calls |
| English/German documentation and Change Record companions remain aligned | Met | Bilingual and link checks |
| Parent-only scope preserves Framework source and gitlink | Met | Final Framework status was empty and the Parent gitlink remained unchanged |

## Implementation decision and rationale

Vendor only adapted guidance that has a fixed source and license: historical
OpenAI <code>create-plan</code>, two OpenAI GitHub workflow skills, and
<code>stop-slop</code>. Omit their authenticated GitHub helper scripts to avoid
adding a review/check-log data channel. Implement four repository-authored
skills for bounded research, migration planning, paired documentation, and
future extension auditing.

Record all considered items in one lock manifest and verify frontmatter,
provenance, license presence, source pins, relative links, secret absence,
declared positive/negative routing, and unsafe-automation rejection with a
deterministic root test. Make the check part of <code>lint</code> and therefore
<code>quick-check</code>.

Use the already available official curated plugin snapshot at
<code>bd2122cb92f2ade874d8c2b1d00383976ab9415b</code> for Superpowers version
<code>5.1.3</code> and Codex Security version <code>0.1.11</code>. The
Superpowers compatibility policy gives system/user/repository rules priority
and blocks its worktree, process-control, cleanup, automatic publication, and
policy-bypass behavior unless separately authorized.

### Extension disposition

The lock manifest contains the exact source URLs, paths, capability fields, and
update/removal disposition. This table records every reviewed extension's
fixed source/version, license decision, and integration outcome.

| Extension | Fixed source/version | License | Integration outcome and imported material |
| --- | --- | --- | --- |
| `create-plan` | `openai/skills@a5119697b819090e00e5d11ee1d86834d7c1043a` | Apache-2.0 | Adapted/vendored `SKILL.md`, full license, provenance; no scripts |
| `gh-fix-ci` | `openai/plugins@11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` / `0.1.6` | Apache-2.0 | Adapted/vendored guidance and license; authenticated check-log helper omitted |
| `gh-address-comments` | `openai/plugins@11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` / `0.1.6` | Apache-2.0 | Adapted/vendored guidance and license; authenticated GraphQL helper omitted |
| `stop-slop` | `hardikpandya/stop-slop@8da1f030185bdfe8471220585162991eaeb970e9` | MIT | Adapted/vendored guidance and license; no scripts |
| `valyu-research` | repository-authored | repository-owned | Enabled planning adapter; it does not enable Valyu |
| `modsecurity-codebase-migrate` | repository-authored | repository-owned | Enabled bounded migration-planning adapter |
| `bilingual-changelog-generator` | repository-authored | repository-owned | Enabled explicit release/changelog adapter |
| `third-party-skill-audit` | repository-authored | repository-owned | Enabled pre-install audit adapter |
| Superpowers | `openai/plugins@bd2122cb92f2ade874d8c2b1d00383976ab9415b` / `5.1.3` | MIT | Official plugin installed in user profile; `installed_pending_reload`; no plugin content vendored |
| Codex Security | `openai/plugins@bd2122cb92f2ade874d8c2b1d00383976ab9415b` / `0.1.11` | Proprietary | Existing official plugin retained enabled; no content vendored and no scan run |
| Morph/WarpGrep | `@morphllm/morphmcp@0.8.206`, git head `ac38aadb555519751cee042a77f0d2cd5e9b01e1` | MIT metadata | `blocked_source_unverified`; no MCP configuration or request |
| Valyu hosted MCP | official hosted documentation, unversioned | unknown | `blocked_source_unverified`; URL-secret transport and inventory mismatch prevent configuration |
| `valyuAI/valyu-mcp` | `valyuAI/valyu-mcp@546c3d2f2a113f0c97007eb21da0f168387bbcef` | unknown | `blocked_license_unknown`; not vendored or run |
| Composio `pr-review-ci-fix` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `rejected_due_to_overlap` |
| Composio `connect-apps` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `rejected_due_to_permissions` |
| Composio `skill-share` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `rejected_due_to_overlap` |
| Composio `mcp-builder` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `documented_only` |
| Composio frontend/webapp | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `not_applicable` |

## Changed files

Versioned files in scope are:

- <code>.agents/skills/</code> with the eight local skills, upstream records,
  and required license files for adapted sources
- <code>ci/tooling/codex-extensions.lock.yml</code>
- <code>tests/test_codex_extensions.py</code> and <code>Makefile</code>
- English/German pairs <code>docs/development/codex-extensions.*</code> and
  <code>docs/security/external-agent-services.*</code>
- English/German documentation indexes and operations/security cross-links
- this English/German Change Record pair and its indexes

Ignored local-only files add the Superpowers compatibility policy and an
<code>AGENTS.md</code> reference. They are intentionally not staged. No
product C/C++ source, connector configuration, Framework file, Framework
gitlink, workflow, generated artifact, or secret is changed.

## Commands executed

| Sanitized command | Result | Evidence boundary |
| --- | --- | --- |
| <code>rtk curl -fsSL ...fixed raw source URLs...</code> | 0 | Downloaded reviewed upstream text only below the task temporary root |
| <code>rtk codex plugin marketplace add openai/plugins --ref &lt;fixed-commit&gt; --json</code> | Controlled refusal | The built-in <code>openai-curated</code> marketplace is reserved; no marketplace was added |
| <code>rtk codex plugin add superpowers@openai-curated --json</code> | 0 | Installed Superpowers from curated snapshot <code>bd2122cb</code> outside the repository |
| <code>rtk codex plugin list --json</code> | 0 | Superpowers, Codex Security, and existing plugins reported installed/enabled; no credential values shown |
| <code>rtk proxy /bin/bash -lc '&lt;presence-only checks for MORPH_API_KEY and VALYU_API_KEY&gt;'</code> | 0 | Both names were absent; no values were printed |
| <code>rtk make check-codex-extension-contract</code> | 0 | Twelve extension contract tests passed after final coverage expansion |
| <code>rtk make check-bilingual-docs</code> | 0 | Bilingual document validation passed |
| <code>rtk make check-doc-links</code> | 0 | Repository and Framework documentation links passed |
| <code>rtk git diff --check</code> | 0 | No whitespace errors reported |
| <code>rtk git check-ignore -v AGENTS.md .codex/config.toml .codex/context/superpowers-compatibility-policy.md</code> | 0 | Local compatibility policy and Codex configuration confirmed ignored |
| <code>rtk git -C modules/ModSecurity-test-Framework status --short</code> | 0 | Framework worktree status was empty |
| <code>rtk proxy /bin/bash -lc 'BUILD_ROOT=&lt;task-temp-root&gt;/build ... make lint'</code> | 2 | Blocked by missing local <code>apxs</code>/<code>apxs2</code> while preparing the Apache C17 check |
| <code>rtk proxy /bin/bash -lc 'CI=true BUILD_ROOT=&lt;task-temp-root&gt;/build ... make lint'</code> | 2 | Apache C17 check was truthfully marked <code>SKIPPED</code>, but the recursive Apache cleanup target converted its documented <code>77</code> blocker to Make exit <code>2</code> |
| <code>rtk proxy /bin/bash -lc 'CI=true BUILD_ROOT=&lt;task-temp-root&gt;/build ... make quick-check'</code> | 2 | Reached the same Apache cleanup prerequisite/recursive-Make blocker through <code>lint</code> |

The initial focused contract run failed only because its negative-route fixture
looked for the phrase <code>sensitive data</code> while the skill correctly
uses the stricter phrase <code>sensitive code</code>. The test was corrected
and the subsequent focused contract run passed. Full lint and quick-check were
attempted and are reported as blocked rather than passing because the local
Apache prerequisite is absent and the cleanup lint wrapper does not preserve
the documented blocked exit through recursive Make.

## Security impact

The change improves extension supply-chain control by pinning sources, keeping
licenses/provenance locally reviewable, omitting authenticated helper scripts,
checking versioned material for common literal secret forms, and documenting
network/data/cost/write boundaries. No full Codex Security scan was initiated:
this task changes extension governance rather than product source and no scan
was requested.

A pre-existing user-scoped extension credential was observed as inline local
configuration outside the repository. It was not echoed, copied, normalized,
or modified. It remains a credential-hygiene risk for its owner to remediate
through approved secret storage and rotation/revocation procedures.

Morph and Valyu remain blocked. No key, paid call, code search, external data
transfer, or external MCP tool enumeration was performed. Node.js is absent,
so bundled local Node-backed MCP runtime behavior was not exercised.

## Runtime evidence

No connector runtime, protocol, CRS/MRTS, lifecycle, production, or security
scan evidence was collected or claimed. This task changes repository extension
governance and documentation only; C17/C23/C2y compilation and hardened builds
are not applicable because no repository-owned C/C++ code changed.

## Known limitations

- Superpowers is installed in the user profile but requires a fresh Codex
  session before its skills can be treated as active in this session.
- The Superpowers source contains helper scripts with process and temporary
  directory effects; the local compatibility policy forbids their implicit use.
- Codex Security's local Node-backed MCP has no runtime evidence because
  Node.js is unavailable.
- Morph source behavior/tool filtering and Valyu safe secret transport/tool
  inventory are not proven, so neither service is configured.

## Remaining risks

- The pre-existing user-scoped inline credential configuration remains outside
  this task's modification authority and should be migrated/rotated by its
  owner.
- A future Codex or plugin update can alter extension behavior; the lock
  manifest requires a renewed immutable-source audit before update.
- The desired Morph tool allowlist is documented but not an enforced control;
  its candidate must stay blocked until an actual client/server filter is
  proven.
- Valyu's documented URL-secret format and tool-name mismatch remain unresolved.

## Checks not run and rationale

- No external Morph/WarpGrep or Valyu request, key validation, paid call, or
  tool-list smoke test ran: the integrations are blocked before a safe secret
  and enforceable tool boundary exist.
- No Codex Security scan ran: it is outside this governance-only task and the
  user expressly excluded a full security scan.
- No connector build, configuration, H1/H2/H3, CRS/MRTS, lifecycle, C17/C23/C2y,
  sanitizer, or hardened build ran: no product/connector/runtime code changed.
- No Framework task, commit, push, or CI ran: the Framework was out of scope.

## Final diff and review status

The focused extension contract, bilingual documentation, and documentation-link
validations passed. The final whitespace check passed; local compatibility
policy/configuration remained ignored; the Framework worktree and Parent
gitlink remained unchanged. Both full lint and quick-check were attempted but
are locally blocked by missing Apache host prerequisites; the CI-mode cleanup
wrapper further exposes an existing recursive-Make exit-status issue. No green
lint/quick-check claim is made. This record matches the final intended diff
before commit and push; the task-generated runtime-cache reports and snapshot
scripts were restored/removed and are absent from that diff. Exact-final-SHA
remote CI remains the delivery gate.
