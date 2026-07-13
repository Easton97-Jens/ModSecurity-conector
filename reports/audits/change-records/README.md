# Change Records

**Language:** English | [Deutsch](README.de.md)

This directory contains manually maintained, versioned Change Records for
every feature, bug fix, security fix, and other non-trivial repository change.
A record supplements the commit and pull request with the requirement,
decision trail, actual verification outcomes, evidence boundary, and remaining
limitations. It is not a generated runtime report and does not promote a build
or test result into a runtime claim.

Read the binding [change traceability policy](../../../docs/change-traceability.md)
before creating or updating a record.

## Create or update a record

1. A Change Record is required for every feature, bug fix, security fix, and
   other non-trivial repository change. Choose a unique stable ID of the form
   <code>CR-YYYYMMDD-short-slug</code>; append <code>-01</code>,
   <code>-02</code>, and so on if necessary.
2. Copy [TEMPLATE.md](TEMPLATE.md) and
   [TEMPLATE.de.md](TEMPLATE.de.md) to matching files named
   <code>&lt;change-id&gt;.md</code> and
   <code>&lt;change-id&gt;.de.md</code>; the descriptive <code>short-slug</code>
   is part of the Change ID, not a language-specific filename.
3. Complete both language companions. A manually maintained record in
   <code>reports/</code> must remain an English/German pair with the same
   technical facts, results, evidence, limitations, and risks. Keep commands,
   paths, file names, Change IDs, commit hashes, Run IDs, status values, and
   configuration keys unchanged in both versions.
4. Record only commands that actually ran and their actual results, including
   failures. Planned tests must not be documented as passed; keep skipped and
   not-run checks visible with their rationale. Reconcile the completed pair
   with the final intended diff before finishing the work.

## Identity

Use the template identity table for the title, unique Change ID, Date (UTC),
author or executing agent, Base revision, and related issue or pull request
when one exists. Record the Final revision when it becomes available, and keep
the corresponding technical values identical in both language companions.

## Motivation and problem statement

Explain the task, affected users or maintainers, and why the change is needed.
The record should make the intended outcome understandable without relying
only on the commit subject.

## Affected components and security boundaries

List the changed components, interfaces, trust or data boundaries, and any
intentional local unversioned configuration that remains outside the versioned
diff. State the relevant boundary even when the change does not alter it.

## Acceptance criteria

Use observable criteria and give each one a status and supporting evidence.
Separate implemented behavior from deferred work and explicitly bounded scope.

## Alternatives investigated

Record the alternatives that were considered and why they were rejected or not
selected, so the chosen approach can be reviewed in its original context.

## Implementation decision and rationale

Summarize alternatives, the selected approach, and its technical or
security-relevant tradeoffs. Link to a more detailed decision record when one
exists.

## Changed files

List the actual final versioned files. Identify intentional local,
unversioned configuration separately so it is not confused with the Git diff.

## Tests added or changed

List tests that were added or changed, or state <code>None</code>. Distinguish
this inventory from commands that were actually executed and their results.

## Commands executed

Use the template table for every verification command that actually ran:
exact command, exit code or result, concise sanitized summary, canonical
evidence location, and run ID where available. Record failed commands and
their actual results visibly; planned, skipped, or not-run commands belong in
“Checks not run and rationale,” not among passing results.

## Security impact

Describe changed security boundaries, validation, defaults, logging, or threat
exposure. State explicitly when the change does not alter security behavior.

## Documentation changes

List updated documentation or examples and their language companions, or state
<code>None</code>. Keep generated documentation and reports distinct from
manually maintained Change Records: update generated material through its
generator or source data, and do not present generated evidence as a manually
maintained record.

## Runtime evidence

Runtime claims require a matching sanitized canonical run, including its run
ID, profile/scope, and evidence location. Otherwise state explicitly that no
runtime evidence was collected or claimed.

## Known limitations

List known limitations, unsupported paths, and bounded assumptions.

## Remaining risks

Record unresolved risks and mitigations so they remain reviewable after merge.

## Checks not run and rationale

List every relevant check that was not run and why. Planned, skipped, or
assumed commands must not be represented as passing results.

## Final diff and review status

Before completion, record the final diff/whitespace review, review status, and
confirmation that the record matches the actual final diff and real outcomes.

## Data and evidence boundary

Do not store complete logs, raw runtime data, builds, caches, secrets,
complete environment variables, cookies, tokens, bodies, private keys, or
operator-specific absolute paths here. Store only concise sanitized summaries,
portable canonical evidence locations, and run IDs where available. Runtime
raw data and build output remain outside the checkout.

## Records

| Change ID | UTC date | Topic | Record |
| --- | --- | --- | --- |
| CR-20260713-change-traceability-governance | 2026-07-13 | Versioned change-traceability governance | [English](CR-20260713-change-traceability-governance.md) / [Deutsch](CR-20260713-change-traceability-governance.de.md) |
| CR-20260713-bilingual-policy-enforcement | 2026-07-13 | Bilingual policy enforcement | [English](CR-20260713-bilingual-policy-enforcement.md) / [Deutsch](CR-20260713-bilingual-policy-enforcement.de.md) |
