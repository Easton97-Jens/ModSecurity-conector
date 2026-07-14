# Change Record: Codex extensions and CI security tooling

**Language:** English | [Deutsch](CR-20260714-codex-security-tooling.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Codex extensions and CI security tooling |
| Change ID | CR-20260714-codex-security-tooling |
| Date (UTC) | 2026-07-14T00:00:00Z |
| Author or executing agent | Codex |
| Base revision | be0356af96ef582c3a7dbc0169c7c8b27b7b6b34 |
| Related issue or pull request | [Draft PR #44](https://github.com/Easton97-Jens/ModSecurity-conector/pull/44) |
| Final revision | Delivery candidate <code>8a3982d29b5007e7c421a193933a18cc1ba3696b</code>; evidence-record commit pending |

## Motivation and problem statement

The Parent needed a shared, maintainable Codex skill layer and narrowly scoped
local extensions, plus independently verifiable CI security analysis. The
design must preserve the Framework boundary, avoid credentials in configuration,
and not turn analysis results into automatic remediation or runtime claims.

## Affected components and security boundaries

Versioned scope includes <code>.agents/skills/</code>, skill and security-tool
validators, focused unit tests, a checksum-verifying binary fetch helper,
workflows, immutable Action pins, documentation, and this record. The Framework
worktree and Gitlink remain outside the scope.

Ignored local scope includes <code>.codex/agents/</code>,
<code>.codex/hooks.json</code>, and local hook scripts. The local documents MCP
is configured without a repository credential; GitHub MCP remains
<code>documented_only</code>. Local files are intentionally outside the Git
diff and do not replace the sandbox, approval policy, or managed requirements.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Eight shared skills follow the current documented format and validate | Met locally | Skill validator and focused tests |
| Local read-only agents and deterministic hooks are syntactically valid and ignored | Met locally | TOML/JSON/Python checks, synthetic hook decisions, <code>git check-ignore</code> |
| Security metadata records approved upstreams, policy dispositions, releases, immutable SHAs, checksums, permissions, platforms, availability, and status | Met locally | Security-tools manifest validator |
| actionlint and zizmor analyze all workflows independently | Met locally and for the delivery candidate | Checksum-verified local tools; unsafe fixture rejected and safe fixture accepted; run <code>29357810936</code> passed |
| Gitleaks uses redacted PR-range semantics without remediation | Met locally and for the delivery candidate | 13-commit redacted base-to-candidate range found no leaks; run <code>29357811166</code> passed |
| Dependency Review is not enabled without the required GitHub feature | Met | <code>blocked_feature_unavailable</code> disposition |
| CodeQL, Scorecard, and OSV workflows use minimal documented permissions and immutable caller pins | Met for the delivery candidate | CodeQL <code>29357810753</code>, Scorecard <code>29357810737</code>, and OSV PR comparison <code>29357812062</code> passed |
| Framework and Gitlink remain unchanged | Met for the delivery candidate | <code>make check-framework</code>; Framework SHA <code>aac462cf217cdd5d09a56e3029c279459158f3ac</code>; no Gitlink diff |

## Alternatives investigated

The Gitleaks Action was not selected because its current EULA, organization
license requirement, default reporting behavior, and potential write surface
are unnecessary for the official CLI. A direct OSV CLI from a separate
repository was not installed because the approved integration is the listed
official GitHub Action. Dependency Review was not replaced with a weaker
substitute while the dependency-graph feature is unavailable. Artifact
attestations were not added because no real release workflow exists.

## Selected upstream and trust assessment

All selected repositories are in the task's approved upstream set. Each record
was evaluated on 2026-07-14; the versioned manifest records the official owner,
release date, full release commit SHA, security-policy disposition, supported
integration platform, public-repository availability, minimal permissions,
secrets, and automated-fix behavior.

| Tool | Official upstream and policy disposition | License | Release and full SHA | Verified platform / public availability | Integration and status |
| --- | --- | --- | --- | --- | --- |
| actionlint | <code>rhysd/actionlint</code>; <code>rhysd/actionlint/security/policy</code> | MIT | <code>v1.7.12</code>; <code>914e7df21a07ef503a81201c76d2b11c789d3fca</code> | Verified Linux x86_64 asset; free, no credential | Checksum-verified binary; <code>enabled</code> |
| zizmor | <code>zizmorcore/zizmor</code>; <code>zizmorcore/zizmor/security/policy</code> | MIT | <code>v1.27.0</code>; <code>e2627367eb7c917a90503ce05a66872fd91da6fb</code> | Verified Linux x86_64 asset; free, no credential | Checksum-verified binary; <code>enabled</code> |
| Gitleaks CLI | <code>gitleaks/gitleaks</code>; <code>gitleaks/gitleaks/security/policy</code> | MIT | <code>v8.30.1</code>; <code>83d9cd684c87d95d656c1458ef04895a7f1cbd8e</code> | Verified Linux x86_64 asset; free, no credential | Checksum-verified binary; <code>enabled</code> |
| Gitleaks Action | <code>gitleaks/gitleaks-action</code>; <code>gitleaks/gitleaks-action/security/policy</code> | Gitleaks Action EULA | <code>v3.0.0</code>; <code>e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e</code> | GitHub-hosted Linux; organization license required | Evaluated only; <code>documented_only</code> |
| CodeQL | <code>github/codeql-action</code>; <code>github/codeql-action/security/policy</code> | MIT Action; CodeQL CLI terms apply | <code>v4.37.0</code>; <code>99df26d4f13ea111d4ec1a7dddef6063f76b97e9</code> | GitHub-hosted Linux; open-source GitHub repositories supported | SHA-pinned Action; <code>enabled</code> |
| Dependency Review | <code>actions/dependency-review-action</code>; <code>actions/dependency-review-action/security/policy</code> | MIT | <code>v5.0.0</code>; <code>a1d282b36b6f3519aa1f3fc636f609c47dddb294</code> | GitHub-hosted Linux; required graph/SBOM capability unavailable here | Not enabled; <code>blocked_feature_unavailable</code> |
| Scorecard | <code>ossf/scorecard-action</code>; <code>ossf/scorecard-action/security/policy</code> | Apache-2.0 | <code>v2.4.3</code>; <code>4eaacf0543bb3f2c246792bd56e8cdeffafb205a</code> | GitHub-hosted Linux; free for public repositories | SHA-pinned Action; <code>enabled</code> |
| OSV-Scanner | <code>google/osv-scanner-action</code>; <code>google/osv-scanner-action/security/policy</code> | Apache-2.0 | <code>v2.3.8</code>; <code>9a498708959aeaef5ef730655706c5a1df1edbc2</code> | GitHub-hosted Linux; no repository secret | SHA-pinned direct PR leaf actions and scheduled reusable workflow; <code>enabled</code> |

## Implementation decision and rationale

The implementation pins Actions by full release commit SHA, verifies binary
downloads against recorded SHA-256 values, keeps scanners analysis-only, and
uses job-level <code>security-events: write</code> only for SARIF upload.
actionlint and zizmor are distinct jobs; Gitleaks separates PR diff from
scheduled full history. CodeQL keeps C/C++ bounded to a real common C17 build
and scans the two Go modules separately.

Existing mutable Actions references were pinned in a distinct change wave.
The workflow lint revealed a pre-existing ShellCheck style diagnostic and a
template-injection path; both were corrected as necessary prerequisites for a
meaningful all-workflow gate. Credential persistence is disabled for checkout
steps where it is not required.

The pin validator validates every <code>.yml</code> and <code>.yaml</code>
workflow recursively against a versioned official-release map, not merely a
40-character SHA and version-shaped comment.

The published OSV <code>v2.3.8</code> PR reusable workflow exceeded GitHub's
1 MiB job-output limit while its scanner, reporter, SARIF upload, and
base-versus-PR comparison all succeeded. The release-pinned PR path therefore
mirrors its scanner/reporter steps without exporting complete JSON as job
outputs; the scheduled full scan remains on the official reusable workflow.
This resolves the task-owned <code>workflow_configuration_failure</code>
without using an unreleased upstream commit or weakening
<code>--fail-on-vuln=true</code>.

## Changed files

Versioned files include all eight <code>.agents/skills/</code> directories,
<code>ci/checks/documentation/check_codex_skills.py</code>,
<code>ci/checks/security/codex_hook_policy.py</code>,
<code>ci/checks/security/check_security_tools_manifest.py</code>,
<code>ci/tooling/security-tools.lock.yml</code>,
<code>ci/tools/fetch_security_tool.py</code>, focused tests, zizmor fixtures,
the security workflows, existing workflow pins, <code>Makefile</code>, paired
documentation, and this paired Change Record.

Local unversioned files include the five read-only agent definitions and the
session, pre-tool, and permission-request hooks under <code>.codex/</code>.
They are not staged or committed.

## Tests added or changed

- <code>tests/test_codex_skills.py</code>
- <code>tests/test_codex_hook_policy.py</code>
- <code>tests/test_security_tools_manifest.py</code>
- <code>tests/test_fetch_security_tool.py</code>
- zizmor safe and intentionally insecure fixtures
- focused Make targets for Codex skills and security tooling

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>python3 ci/checks/documentation/check_codex_skills.py</code> | 0 | All required skills valid | None | None |
| <code>make check-codex-skills</code> | 0 | Versioned skill target passed | None | None |
| <code>python3 ci/checks/security/check_security_tools_manifest.py</code> | 0 | Manifest and workflow pins valid | None | None |
| <code>make check-security-tools</code> | 0 | Manifest, release map, and all workflow pins valid | None | None |
| <code>python3 -m unittest -v tests.test_codex_skills tests.test_codex_hook_policy tests.test_security_tools_manifest tests.test_fetch_security_tool</code> | 0 | Twenty-two focused tests passed | None | None |
| <code>actionlint -shellcheck=/usr/bin/shellcheck</code> | 0 | All discovered workflows valid with ShellCheck integration | None | None |
| <code>zizmor --offline .github/workflows</code> | 0 | All workflows report no findings | None | None |
| <code>zizmor --offline ci/fixtures/zizmor/insecure.yml</code> | Nonzero as expected | Dangerous trigger and template injection were detected | None | None |
| <code>zizmor --offline ci/fixtures/zizmor/safe.yml</code> | 0 | Safe fixture accepted | None | None |
| <code>gitleaks git --redact=100 --log-opts="--all" .</code> | 1 | 83 historical candidates; no baseline was created and this is not treated as a task regression | None | None |
| <code>gitleaks git --redact=100 --log-opts="be0356af96ef582c3a7dbc0169c7c8b27b7b6b34..HEAD" .</code> | 0 | Thirteen delivery-candidate commits scanned; no leaks found | None | None |
| <code>make check-bilingual-docs</code> | 0 | Paired documentation valid | None | None |
| <code>make check-doc-links</code> | 0 | Links and repository path references valid | None | None |
| <code>make quick-check</code> | 2 | Incomplete: local DNS could not resolve the ModSecurity upstream during provisioning, so the Apache/APXS prerequisite remained unavailable; no task-source defect demonstrated | None | None |
| <code>make lint</code> | 2 | Incomplete: local Apache/APXS provisioning reported <code>missing_local_httpd_build</code>; no task-source defect demonstrated | None | None |
| GitHub Actions security workflow lint | 0 | actionlint and zizmor passed | GitHub Actions | <code>29357810936</code> |
| GitHub Actions secret scan | 0 | Pull-request commit-range scan passed | GitHub Actions | <code>29357811166</code> |
| GitHub Actions CodeQL | 0 | Actions, Go Envoy, Go Traefik, and bounded C/C++ jobs passed | GitHub Actions | <code>29357810753</code> |
| GitHub Actions Scorecard | 0 | Same-repository pull-request job passed; default-branch job skipped by design | GitHub Actions | <code>29357810737</code> |
| GitHub Actions OSV PR comparison | 0 | Base/PR scans, reporter, SARIF, and artifacts passed without job-output export | GitHub Actions | <code>29357812062</code> |
| SonarCloud quality gate | 0 | New reliability, security, and maintainability ratings passed | SonarCloud PR #44 | None |

The delivery candidate was pushed to <code>origin</code>; its remote SHA matched
<code>8a3982d29b5007e7c421a193933a18cc1ba3696b</code>, and Draft PR #44 remains
open with no merge or auto-merge. The evidence-record commit still requires its
own exact-SHA verification; no unexecuted command is represented as passed.

## Security impact

The change adds deterministic local guardrails and CI analysis without granting
new broad write permissions. It removes mutable caller references, makes
binary provenance auditable, checks workflow injection and permission risks,
and redacts Gitleaks output. It does not automatically validate a finding,
modify dependencies, remove secrets, rotate credentials, alter branch
protection, or collect runtime evidence.

## Documentation changes

Added paired Codex-extension and CI-security-tooling documents; updated the
paired documentation index and operations/security references; added this
paired Change Record. The documents record upstream selection, licensing,
update process, false-positive triage, secrets/redaction rules, limits, and
local-only configuration.

## Runtime evidence

No runtime evidence was collected or claimed for this change. Builds, static
analysis, lint, unit tests, and CI workflow configuration are not connector
runtime evidence.

## Matrix and protocol disposition

| Dimension | Status | Rationale |
| --- | --- | --- |
| H1 | <code>not_applicable</code> | This scope changes skills, documentation, and CI security tooling only |
| H2 | <code>not_applicable</code> | This scope changes skills, documentation, and CI security tooling only |
| H3 | <code>not_applicable</code> | This scope changes skills, documentation, and CI security tooling only |
| no_crs_no_mrts | <code>not_applicable</code> | No connector lifecycle behavior changed |
| with_crs_no_mrts | <code>not_applicable</code> | No connector lifecycle behavior changed |
| no_crs_with_mrts | <code>not_applicable</code> | No connector lifecycle behavior changed |
| with_crs_with_mrts | <code>not_applicable</code> | No connector lifecycle behavior changed |

## Known limitations

OSV local execution is <code>not_executed</code>; no unlisted direct CLI was
installed. Its approved GitHub PR comparison passed for the delivery candidate,
while the scheduled full scan remains future evidence. Dependency Review is
<code>blocked_feature_unavailable</code>. CodeQL does not claim complete
external connector C/C++ coverage. Local hooks require a trusted project,
<code>/hooks</code> review, and session restart/resume to become active.
<code>pull_request</code> analysis avoids the unsafe
<code>pull_request_target</code> context but is not a standalone
tamper-resistant merge gate; an external protected required workflow or ruleset
is required for that guarantee.

## Remaining risks

Scorecard and OSV retain nested mutable Docker/action references beyond the
caller SHA pin. Gitleaks full-history results may need separately reviewed
baseline handling. Scheduled CodeQL/OSV/SARIF availability remains subject to
actual future GitHub workflow execution. Scanner reports require reachability
and false-positive triage before remediation. These risks are documented rather
than automatically suppressed.

Scorecard's experimental exact-head PR path deliberately runs only for
same-repository pull requests with <code>contents: read</code>; fork PRs skip
it because the upstream action does not support them. The default-branch path
retains the SARIF upload.

The redacted local full-history Gitleaks run reported 83 historical candidates.
No baseline, suppression, deletion, or rotation was created in this task. The
redacted base-to-delivery-candidate range scanned 13 commits and found no leaks.

## Checks not run and rationale

No large connector build, connector runtime, CRS/MRTS matrix, or H1/H2/H3
transport test ran because no connector behavior changed. A direct local OSV
CLI did not run because it is outside the approved upstream integration. The
scheduled OSV and default-branch Scorecard scans did not run for a pull request;
their skipped status is expected. The requested
<code>make check-repository-path-references</code> target does
not exist; <code>make check-doc-links</code> invoked its underlying repository
path-reference checker and passed. A <code>SKIP_RUNTIME_COMPONENT_PREPARE=1
make lint</code> retry was not run because that switch does not cover lint's
direct Apache/APXS provisioning path and could rewrite generated runtime
reports without adding evidence.

## Final diff and review status

The delivery candidate <code>8a3982d29b5007e7c421a193933a18cc1ba3696b</code>
is pushed and remote-SHA verified. All task-owned security and quality runs
passed. Five existing structure/lint jobs failed because the runner lacks
usable Apache <code>apxs</code>/headers; comparison with <code>master</code>
confirmed the same independent failure class. They are
<code>unrelated_repository_failure</code>, so the candidate delivery status is
<code>ci_blocked_unrelated_failure</code>. This evidence-only record update
must be committed, pushed, and verified for its own exact SHA. No merge or
auto-merge is authorized.
