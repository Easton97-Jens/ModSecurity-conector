# CI security tooling

**Language:** English | [Deutsch](ci-security-tooling.de.md)

## Scope and status model

This document describes analysis and verification tooling. It does not validate
a vulnerability automatically, update dependencies, rotate a secret, change
repository settings, modify branch protection, or promote a build result to
runtime evidence.

The authoritative metadata is
[security-tools.lock.yml](../../ci/tooling/security-tools.lock.yml). Its
integration status is one of <code>enabled</code>,
<code>documented_only</code>, <code>not_applicable</code>, or
<code>blocked_feature_unavailable</code>. A tool error stays
<code>failed</code>; an unavailable optional GitHub feature is never reported
as passed.

## Approved tools

| Tool | Official upstream | Version | Immutable release SHA | Integration | Status |
| --- | --- | --- | --- | --- | --- |
| actionlint | <code>rhysd/actionlint</code> | <code>v1.7.12</code> | <code>914e7df21a07ef503a81201c76d2b11c789d3fca</code> | Checksum-verified Linux binary | <code>enabled</code> |
| zizmor | <code>zizmorcore/zizmor</code> | <code>v1.27.0</code> | <code>e2627367eb7c917a90503ce05a66872fd91da6fb</code> | Checksum-verified Linux binary, offline mode | <code>enabled</code> |
| Gitleaks CLI | <code>gitleaks/gitleaks</code> | <code>v8.30.1</code> | <code>83d9cd684c87d95d656c1458ef04895a7f1cbd8e</code> | Checksum-verified Linux binary | <code>enabled</code> |
| Gitleaks Action | <code>gitleaks/gitleaks-action</code> | <code>v3.0.0</code> | <code>e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e</code> | Evaluated alternative | <code>documented_only</code> |
| CodeQL | <code>github/codeql-action</code> | <code>v4.37.0</code> | <code>99df26d4f13ea111d4ec1a7dddef6063f76b97e9</code> | Advanced GitHub Actions workflow | <code>enabled</code> |
| Dependency Review | <code>actions/dependency-review-action</code> | <code>v5.0.0</code> | <code>a1d282b36b6f3519aa1f3fc636f609c47dddb294</code> | PR-only GitHub Action | <code>blocked_feature_unavailable</code> |
| Scorecard | <code>ossf/scorecard-action</code> | <code>v2.4.3</code> | <code>4eaacf0543bb3f2c246792bd56e8cdeffafb205a</code> | Scheduled GitHub Action and SARIF | <code>enabled</code> |
| OSV-Scanner | <code>google/osv-scanner-action</code> | <code>v2.3.8</code> | <code>9a498708959aeaef5ef730655706c5a1df1edbc2</code> | PR-diff and scheduled reusable workflows | <code>enabled</code> |

actionlint, zizmor, and the Gitleaks CLI are analysis-only here. Their release
assets are accepted only after the recorded SHA-256 is verified. Gitleaks runs
with full redaction and never deletes or rotates a finding.

The Gitleaks Action remains <code>documented_only</code>: its EULA,
organization-license requirement, default PR reporting behavior, and potential
write/reporting surface are not required when the official CLI is used. The
manifest records this decision without storing credentials.

Each integration has its own <code>evaluated_at</code> value, security-policy
URL or explicit <code>not_published_at_evaluation</code> disposition, supported
runner or verified release asset, and public-repository availability statement.
An absent policy is recorded as an assessment result, never assumed to be an
approval. The versioned <code>pinned_actions</code> map binds every external
<code>uses:</code> reference to its official upstream, release version, and
full commit SHA.

## Workflows and permissions

| Workflow | Trigger | Minimum permissions | Result boundary |
| --- | --- | --- | --- |
| <code>ci-security-workflow-lint.yml</code> | Pull request, protected branch push, manual | <code>contents: read</code> | Separate actionlint and offline zizmor results; synthetic fixtures prove expected detection |
| <code>ci-security-secrets.yml</code> | Pull request diff, scheduled full history, manual | <code>contents: read</code> | Redacted PR commit range and separately reviewed history |
| <code>ci-security-osv.yml</code> | Pull request diff, scheduled full scan, manual | Job-level <code>actions: read</code>, <code>contents: read</code>, <code>security-events: write</code> | SARIF vulnerability scan without a fix command |
| <code>ci-security-codeql.yml</code> | Pull request, protected branch push, schedule, manual | Job-level <code>contents: read</code>, <code>security-events: write</code> | One SARIF upload per language analysis |
| <code>ci-security-scorecard.yml</code> | Protected branch push, schedule, branch-protection event, manual | Job-level <code>contents: read</code>, <code>security-events: write</code> | Heuristic SARIF assessment; no publishing or repository changes |

All new <code>uses:</code> references are full 40-character commit SHAs with a
stable-version comment. Existing mutable Actions references were pinned in a
separate change wave using the same rule. The manifest check validates the
recorded upstream/release mapping for every <code>.yml</code> and
<code>.yaml</code> workflow, not just the SHA shape.

Analysis workflows use <code>pull_request</code>, not
<code>pull_request_target</code>, receive no repository secrets from forks, and
set checkout credential persistence to false where no write is required. This
avoids the unsafe target-repository execution context. It also means a PR can
modify its own workflow or downloader: configure a protected required workflow
or ruleset outside this repository before treating these jobs as a
tamper-resistant merge gate. No repository setting was changed here; the
read-only PR jobs remain useful analysis evidence.

## Coverage and boundaries

CodeQL scans GitHub Actions, each existing Go module separately, and a bounded
C/C++ scope that builds the repository-owned common C17 helpers. It does not
claim complete connector C/C++ coverage: external host headers and real
connector build capture are a separate follow-up requirement.

OSV scans recursively through the reusable official workflow, covering Go
module files and detected supported lock, vendored, container, and package
definitions when present. It does not replace <code>govulncheck</code> for Go
call-path evidence. The approved integration is the listed GitHub Action;
therefore a direct local CLI from a separate repository is not installed.
Local OSV status before GitHub execution is <code>not_executed</code>, while
the scheduled and PR workflow is the enabled execution path. Never use an OSV
fix command in this repository.

Dependency Review is intentionally not replaced while the dependency-graph/SBOM
capability is unavailable. Recheck that GitHub feature before enabling its
conservative PR-only workflow. It must remain
<code>blocked_feature_unavailable</code> rather than silently skipped or
reported as passed.

Scorecard is heuristic evidence, not a branch-protection decision. Its caller
is SHA-pinned, but its Docker metadata can still select a mutable GHCR tag.
The OSV reusable workflow likewise retains nested Docker/action references.
These residual risks are recorded for review rather than hidden.

Artifact attestations are
<code>not_applicable_until_release_workflow_exists</code>: this repository has
no real release tags, release artifacts, checksums, or documented release
workflow. No artificial release pipeline was created.

## Local verification

Use a task-scoped temporary destination:

```sh
python3 ci/tools/fetch_security_tool.py --tool actionlint --destination "$CODEX_TEMP_ROOT/tmp/security-tools"
python3 ci/tools/fetch_security_tool.py --tool zizmor --destination "$CODEX_TEMP_ROOT/tmp/security-tools"
python3 ci/tools/fetch_security_tool.py --tool gitleaks_cli --destination "$CODEX_TEMP_ROOT/tmp/security-tools"
"$CODEX_TEMP_ROOT/tmp/security-tools/actionlint" -shellcheck="$(command -v shellcheck)"
"$CODEX_TEMP_ROOT/tmp/security-tools/zizmor" --offline .github/workflows
"$CODEX_TEMP_ROOT/tmp/security-tools/gitleaks" git --redact=100 --log-opts="<base-sha>..HEAD" .
make check-security-tools
```

With no path argument, actionlint discovers the repository workflows. CI uses
an explicit recursive <code>find</code> for both <code>.yml</code> and
<code>.yaml</code>; the manifest validator covers the same set. The unsafe
zizmor fixture must exit nonzero; the safe fixture must exit zero.
Do not add <code>--fix</code>, create an unreviewed Gitleaks baseline, or run a
package manager merely to make a scanner appear complete. Review a finding for
directness, indirectness, and reachability before opening a separate
remediation task.

## Triage and updates

Treat scanner output as a candidate. Record the exact commit, tool version,
workflow/job URL, sanitized result, affected dependency or code path, and
whether it is direct, indirect, reachable, or not reachable. A false-positive
or accepted-risk decision needs a documented rationale and expiry/review point;
do not globally suppress an audit to obtain a green run.

For every update, verify the official owner, license, security policy, stable
release, release date, full release SHA, binary digest when applicable,
permissions, secrets, public-repository availability, and automated-fix
behavior. Update the manifest, immutable workflow comments, focused tests,
English/German documentation, and Change Record together. No token or secret
value belongs in any of those files.

## Related references

- [Security tools manifest](../../ci/tooling/security-tools.lock.yml)
- [Codex extensions](../development/codex-extensions.md)
- [Operations and security](../operations-and-security.md)
- [Change Records](../../reports/audits/change-records/README.md)
