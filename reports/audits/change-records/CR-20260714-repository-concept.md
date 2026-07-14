# Change Record: Repository product-monorepo concept

**Language:** English | [Deutsch](CR-20260714-repository-concept.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Repository product-monorepo concept |
| Change ID | CR-20260714-repository-concept |
| Date (UTC) | 2026-07-14T08:14:32Z |
| Author or executing agent | Codex agent /root |
| Base revision | 0fec00442b0031c206b627a44735f1eb07534d51 |
| Related issue or pull request | None |
| Final revision | not committed |

## Motivation and problem statement

The repository needed a durable, bilingual target concept that distinguishes
the product monorepo from the independent Framework, makes connector and Common
ownership reviewable, and prevents checked-in reports from being mistaken for
new runtime proof. Existing architecture, connector, Common, Framework,
capability, and evidence documentation describes important parts of the current
state, but it did not provide one binding target-state decision surface.

## Affected components and security boundaries

The versioned change is documentation-only. It affects repository navigation,
architecture guidance, a new target concept, ADR guidance, and this traceability
record. It documents the boundary between Parent-owned product code, connector
adapters, Common runtime code, and the independent reusable-test Framework.
It neither changes request/response handling, security defaults, host failure
behavior, runtime storage, nor connector binaries.

The local ignored <code>AGENTS.md</code> was updated with compact repository
concept discipline. It is intentionally outside the versioned diff and has no
German companion. Pre-existing or concurrent working-tree changes outside the
files listed below were preserved and are not part of this Change Record.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| A bilingual target concept states the Parent, connector, Common, and Framework boundary. | met | <code>docs/repository-concept.md</code> and <code>docs/repository-concept.de.md</code> |
| Finished-product expectations, lifecycle ownership, configuration boundaries, and extension rules are explicit. | met | Concept sections “Product contract”, “Lifecycle”, “Configuration”, and “Extension rules” |
| Current capability/report conflicts and Framework-boundary deviations remain visible rather than being rewritten. | met | Concept section “Documented deviations and follow-up boundaries” |
| Claim labels distinguish verified, documented_not_runtime_verified, compatibility_only, unknown, and out_of_scope. | met | Concept section “Claim labels” |
| ADR process and five suggested decision topics are available in both languages. | met | <code>docs/decisions/README.md</code> and <code>docs/decisions/README.de.md</code> |
| No product source, test, generator, workflow, or Framework/submodule file is changed by this documentation change. | met | Changed-files inventory and final diff review |

## Alternatives investigated

Retrofitting the current-state architecture document as the only target-state
authority was not selected because it would blur observed source ownership with
future binding decisions. Updating stale generated evidence or capability
manifests was not selected because this documentation task collected no fresh
runtime evidence and must not relabel historical output as current proof.
Moving Parent or Framework code was also out of scope; the concept instead
makes the existing split and deviations explicit for follow-up decisions.

## Implementation decision and rationale

Add a paired, manually maintained repository concept under <code>docs/</code>,
link it from the root and documentation navigation, and provide a paired ADR
entry point. The concept establishes a source hierarchy and explicit claim
labels before describing the desired product-monorepo boundary: Parent owns
the product and host-specific seams, Framework owns reusable test logic, and
Common remains transport-neutral runtime code.

The design deliberately records current evidence as
<code>documented_not_runtime_verified</code> where raw artifacts were not
revalidated and records stale generated reports as <code>unknown</code> for
current promotion. This preserves traceability without making a production,
availability, complete-coverage, or runtime security claim.

## Changed files

Versioned documentation files:

- <code>README.md</code> and <code>README.de.md</code>
- <code>docs/README.md</code> and <code>docs/README.de.md</code>
- <code>docs/architecture.md</code> and <code>docs/architecture.de.md</code>
- <code>docs/repository-concept.md</code> and
  <code>docs/repository-concept.de.md</code>
- <code>docs/decisions/README.md</code> and
  <code>docs/decisions/README.de.md</code>
- The <code>CR-20260714-repository-concept</code> entries in
  <code>reports/audits/change-records/README.md</code> and
  <code>reports/audits/change-records/README.de.md</code>
- This English/German Change Record pair

Intentional local unversioned configuration: <code>AGENTS.md</code> only.
The shared Change Record index may also contain preserved concurrent entries;
this record covers only the entries named above.

## Tests added or changed

None. Existing repository documentation and quick-check validations were run;
no test, generator, workflow, product source, or Framework file was changed by
this Change Record.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>rtk make check-bilingual-docs</code> | 0 | English/German documentation pairing and Change Record structure passed. | None; command-only validation | None |
| <code>rtk make check-doc-links</code> | 0 | Repository-relative documentation links passed. | None; command-only validation | None |
| <code>rtk make check-variable-documentation</code> | 0 | Documented variable references passed. | None; command-only validation | None |
| <code>rtk git diff --check</code> | 0 | No whitespace errors in the reviewed working-tree diff. | None; command-only validation | None |
| <code>rtk env CODEX_TEMP_ROOT=&lt;task-local-root&gt; TMPDIR=&lt;task-local-root&gt;/tmp BUILD_ROOT=&lt;task-local-root&gt;/build TMP_ROOT=&lt;task-local-root&gt;/tmp LOG_ROOT=&lt;task-local-root&gt;/logs VERIFIED_RUN_ROOT=&lt;task-local-root&gt;/verified EVIDENCE_ROOT=&lt;task-local-root&gt;/evidence make quick-check</code> | 143 (terminated) | Initial static and contract portions passed, but Apache C17-lint provisioning exceeded the task temporary-storage limit and the incomplete run was stopped. It is not a passing result or runtime evidence. | None; cleaned task-local temporary root | None |

## Security impact

No security behavior changes. The concept documents existing security-relevant
boundaries, including ownership, bounded transaction state, configuration
defaults, and the limit of connector-specific failure semantics. It reduces the
risk of overstating historical evidence, but it does not validate a new runtime
security property, alter a default, or disclose sensitive data.

## Documentation changes

Added the paired repository concept and ADR guide; linked the concept from
root, documentation, and architecture navigation; updated the local ignored
agent guidance; and added this paired Change Record and its index entry.

## Runtime evidence

No runtime evidence was collected or claimed for this change. The existing
six-connector core-completion report remains
<code>documented_not_runtime_verified</code> in the concept because its raw
artifacts were not independently revalidated here. Generated freshness output
marked stale is <code>unknown</code> for current promotion.

## Known limitations

- Connector capability manifests use historical/compatibility profiles for
  several connectors while the current architecture selects native product
  paths; the mismatch is documented, not corrected.
- Current generated freshness and full-run summaries are stale and were not
  regenerated.
- Several generic lifecycle/evidence utilities remain Parent-resident and
  Framework contains some host-oriented provisioning; the target boundary is
  therefore documented rather than mechanically enforced.
- The repository's raw historical evidence and all connector runtimes were not
  re-executed for this documentation-only change.

## Remaining risks

The target boundary can drift until ownership checks are automated and the
documented capability/evidence discrepancies are reconciled. The ADR process,
explicit claim labels, local agent guidance, and future Change Records mitigate
that risk but do not replace an evidence refresh or architectural migration.

## Checks not run and rationale

No connector build, configuration, lifecycle, release-evidence regeneration,
capability-manifest refresh, or full Framework migration was completed. The
required <code>make quick-check</code> was initiated with isolated roots, but
was terminated with exit code <code>143</code> when Apache C17-lint provisioning
exceeded the task temporary-storage limit; it must be re-run with an approved
larger isolated budget to obtain a complete result. Those actions are outside a
documentation-only scope, can require external dependencies and sanitized
runtime artifacts, and would create or reinterpret evidence beyond what this
task verified. No raw historical runtime artifact was independently
revalidated.

## Final diff and review status

Manual review confirms that this record describes only the documentation and
local guidance work listed above, preserves unrelated working-tree changes, and
does not represent static checks as runtime proof. The final whitespace check
passed. The intended commit subject is <code>Document connector monorepo
concept</code>; no commit or pull request was created by this task.
