# FND-MRTS-0003 — MRTS runner-profile contract contradicted a user-approved local configuration

## Identity

| Field | Value |
| --- | --- |
| ID | \`FND-MRTS-0003\` |
| Category | \`documentation_drift\` |
| Repository | \`mrts\` |
| Ownership | \`mrts_explicit_user_task\` |
| Priority | \`P2\` |
| Severity | \`not_applicable\` |
| Confidence | \`confirmed\` |
| Status | \`not_applicable\` (archived) |
| Feasibility | \`not_applicable\` |
| Release blocker | \`false\` |
| Security relevant | \`false\` |
| Profile | \`MRTS shared local Codex runner profile\` |

## Current disposition

**Verdict: `not_applicable` as a product-security finding.** The current user
confirmed that the retained Framework-style MRTS configuration is the intended
trusted local runner profile. Parent and Framework use the same profile type;
the MRTS-specific restrictive contract was documentation/validator drift.

### Observed and expected behavior

The live configuration matches retained snapshot SHA-256
`ee2e0437e2c5c3b8926b96ff68b617197140bea2602a8b8e094d4c1686ec0cfb`.
It declares the active MRTS workspace plus four exact writable support roots,
network access, slash-TMP exclusion, the explicit MRTS TMPDIR path map,
`inherit = "all"`, default secret exclusions, and a non-secret environment
map. The structure manifest declares the same profile; the native validator
rejects drift from it rather than prohibiting the intended configuration.

### Boundary, impact, and evidence

The ignored local configuration is trusted operator input. No evidence shows a
less-privileged or remote writer, a supported product boundary, or a live
sandbox escape. The retained profile snapshot and the static comparison to
Parent/Framework therefore defeat the original security claim. This remains
local declarative evidence, not proof of runtime filesystem or network
enforcement.

Affected files/symbols remain `.codex/config.toml`,
`.codex/structure-manifest.toml`, the directly contradictory MRTS governance
policies, `tools/validate-governance.py`,
`tools/test_validate_governance.py`, and the sandbox/environment settings they
validate. No product generator, dependency, Git, Gitlink, remote, or delivery
surface changed.

### Resolution and validation

The exact retained profile was restored and the manifest, validator, focused
tests, and directly contradictory documentation were aligned. Explicit secret
exclusions, no-MCP/plugin checks, `on-request`, disabled login shells, and the
separate task-authorization/Gitlink boundaries remain enforced.

- MRTS config and manifest TOML parsing passed.
- The native MRTS governance validator passed.
- Six focused MRTS governance tests passed, including profile-drift and
  manifest-controlled environment-map cases.
- The Parent MRTS-scoped and all-root inheritance validators passed; the
  all-root result retained only four pre-existing documented Parent warnings.
- The Parent control-plane suite passed 133 tests.

Residual risk: the user-approved profile declares network access and support
roots for trusted local work. It does not prove that a runtime enforced those
settings, and unrelated concurrent workspace changes still prevent a complete
whole-workspace continuity claim.

## Historical record — superseded restrictive-contract evidence

An ignored MRTS local Codex configuration was replaced by a broader Framework-style configuration. The native governance validator reproduced six violations: network enabled, broad writable roots, inherited TMPDIR allowed, full environment inheritance, an injected environment table, and an explicit network-enable marker. A configuration-only restoration returned the documented default-deny contract. The original native validator, its five focused regression tests, and the Parent scoped inheritance validator now pass. This is verified static control recovery, not proof that a live session applied or bypassed the declared sandbox.

## Observed and expected behavior

Before the repair, MRTS \`.codex/config.toml\` had \`network_access = true\`, four non-MRTS writable roots, \`exclude_tmpdir_env_var = false\`, \`inherit = "all"\`, and a \`[shell_environment_policy.set]\` table. The native \`tools/validate-governance.py\` exited \`1\` with six configuration errors; the Parent validator separately emitted \`mrts:config_environment_inherit\` and exited \`1\`.

The expected configuration is the restrictive declarative contract in current MRTS policy: disabled network; exactly \`/var/tmp/codex/ModSecurity-conector/mrts-sandbox\` as the declared external writable root; slash-TMP and inherited-TMPDIR exclusions; \`inherit = "core"\`; and no injected environment table. The declaration neither grants extra task authority nor proves runtime enforcement.

## Impact and scope

If a Codex session resolves and consumes the broadened local configuration, it can conditionally gain network egress, writes beyond the MRTS boundary, full inherited-environment visibility, and injected tool/path state. No evidence shows an untrusted remote actor controlled this ignored local file, that this Parent-root session loaded it, or that a live sandbox escape occurred.

Affected control-plane files and symbols:

- \`.codex/config.toml\`, \`.codex/structure-manifest.toml\`, \`.codex/context/security.md\`, \`.codex/context/read-only-policy.md\`, and \`.codex/context/governance-validation.md\`;
- \`tools/validate-governance.py\` and \`tools/test_validate_governance.py\`;
- \`sandbox_workspace_write.network_access\`, \`sandbox_workspace_write.writable_roots\`, \`sandbox_workspace_write.exclude_tmpdir_env_var\`, \`shell_environment_policy.inherit\`, and \`shell_environment_policy.set\`.

## Preconditions and reproduction

The condition requires a principal or process able to modify ignored local MRTS \`.codex/config.toml\`, followed by a Codex session that resolves and consumes that configuration.

1. Inspect the retained pre-remediation snapshot with SHA-256 \`2eb63d56f02fa9b76a35f5b6b21916bf6b47d9d8ab594d0230b573374c18ea4b\`.
2. From the MRTS root, run \`rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python tools/validate-governance.py\`. The pre-remediation configuration exits \`1\` with the six declared contract violations.
3. From the Parent root, run \`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python .codex/bin/validate-codex-inheritance.py --check --repository mrts --json --explain\`. The pre-remediation configuration exits \`1\` with \`config_environment_inherit\`.

## Evidence

| Artifact | SHA-256 | Command / result |
| --- | --- | --- |
| \`/var/tmp/codex/ModSecurity-conector/runs/20260726T041432Z-codex-control-plane-unification-d42a1961/evidence/security-remediation/mrts-config-before-remediation.toml\` | \`2eb63d56f02fa9b76a35f5b6b21916bf6b47d9d8ab594d0230b573374c18ea4b\` | Native MRTS validator, MRTS root, exit \`1\`, observed \`2026-07-26T05:15:58Z\`. |
| \`/var/tmp/codex/ModSecurity-conector/runs/20260726T041432Z-codex-control-plane-unification-d42a1961/evidence/security-remediation/mrts-config-after-remediation.toml\` | \`c8897b0c3489e145b2bb7b1a9b103638bbe8217233e9bc8e6ca0fa79af523a85\` | Native MRTS validator and Parent MRTS-scoped validator, exit \`0\`, observed \`2026-07-26T05:23:33Z\`. |

Both are retained task evidence for run \`20260726T041432Z-codex-control-plane-unification-d42a1961\`.

## Root cause and remediation

A concurrent local overwrite substituted Framework-style configuration values for the MRTS-specific declared sandbox contract. The config is ignored and has no tracked Git baseline, so a Git restore was neither available nor appropriate.

The minimal remediation changed only the violated configuration controls: network disabled, the approved single external root, both temporary-root exclusions, \`core\` inheritance, and removal of the injected environment table. It preserved unrelated current top-level feature and agent declarations and did not change policy, validator, product, Git, Gitlink, remote, dependency, or delivery state.

## Acceptance criteria and validation

- \`network_access = false\` and exactly \`/var/tmp/codex/ModSecurity-conector/mrts-sandbox\` are declared.
- Both temporary-root exclusions, \`inherit = "core"\`, and no \`[shell_environment_policy.set]\` table are declared.
- The original MRTS governance validator exits \`0\`.
- The Parent MRTS-scoped inheritance validator exits \`0\` without configuration violations.
- \`tools/test_validate_governance.py::GovernanceValidatorTests.test_workspace_sandbox_contract_rejects_broader_settings\` is covered by the five passing focused tests.
- No product source, test source, Git, Gitlink, remote, dependency, or delivery action changed.

The security closure was shown by rerunning the original native validator and the Parent MRTS-scoped validator after the configuration repair. Legitimate control behavior was shown by the native validator’s normal success message and its five focused tests, which exercise broader roots, network access, temporary-root exclusions, \`inherit = "all"\`, and environment injection.

## Dependencies, blockers, and residual risk

There are no remediation dependencies or blockers. Related finding: \`FND-MRTS-0002\`.

Configuration and validators remain local governance evidence only. A separate environment-level investigation is required before claiming that a Codex runtime loaded the MRTS config or that filesystem/network enforcement was active. Concurrent non-task Parent, Framework, MRTS, and ignored-control-plane changes still prevent a whole-workspace continuity claim.

## History

- \`2026-07-26T05:15:58Z\` — static control regression observed.
- \`2026-07-26T05:23:33Z\` — minimal configuration restoration verified.
