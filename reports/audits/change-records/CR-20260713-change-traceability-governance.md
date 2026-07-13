# Change Record: Versioned change-traceability governance

**Language:** English | [Deutsch](CR-20260713-change-traceability-governance.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Versioned change-traceability governance |
| Change ID | CR-20260713-change-traceability-governance |
| Date (UTC) | 2026-07-13T19:24:43Z |
| Author or executing agent | Codex agent <code>/root</code> |
| Base revision | 056f93232c6f5dba132bfb2204d96ce49707507b |
| Related issue or pull request | None |
| Final revision | Not committed |

## Motivation and problem statement

Establish a binding, versioned way to trace non-trivial repository changes
from motivation and acceptance criteria through decisions, implementation,
tests, documentation, and known limits.

## Affected components and security boundaries

The scoped change affects repository documentation, manual audit records, the
pull-request template, and the locally ignored <code>AGENTS.md</code>
instruction file. The versioned policy and templates preserve the boundary
that secrets, sensitive raw data, runtime data, builds, and caches stay
outside the checkout. The local <code>AGENTS.md</code> change is intentionally
excluded by <code>.git/info/exclude</code> and is not part of the versioned
diff.

The final worktree also contained unrelated connector TODO modifications.
They were not changed or reviewed as part of this record.

During this work, the active bilingual checker was independently extended with
section requirements for files in the Change-Record directory. This record
does not change that checker; the new directory README now documents those
required fields as an index-level guide.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Binding English/German policy and paired Change-Record templates exist | Met | Bilingual documentation check passed after the German links were corrected. |
| Documentation indexes and pull-request template expose the process | Met | Scoped final review and successful bilingual-link validation. |
| Local AGENTS instruction is updated without versioning local Codex files | Met | The local ignored file is updated and absent from Git status. |
| Required documentation, link, whitespace, and status checks are recorded honestly | Met | The final bilingual, repository-link, whitespace, and status checks are recorded with their actual outcomes. |

## Alternatives investigated

- Use only the pull-request template. Rejected because it does not provide a
  durable, discoverable, versioned record alongside the change.
- Put records in <code>reports/testing/generated/</code>. Rejected because that
  directory is generator-managed and not suitable for manual audit documents.
- Store complete command output or raw runtime artifacts. Rejected because
  those can expose sensitive data and conflict with the repository evidence
  boundary.
- Create English-only records. Rejected because manually maintained reports
  require English/German companions.
- Change the concurrently modified checker to exempt the README. Rejected
  because that checker change is outside this record's scope; expanding the
  new README into a useful field guide satisfies the active contract without
  altering independent work.

## Implementation decision and rationale

Add a binding English/German policy under <code>docs/</code> and a manually
maintained, versioned EN/DE record directory under
<code>reports/audits/</code>. The templates require the full decision and
verification trail while limiting retained evidence to concise sanitized
summaries. Index links and the bilingual pull-request template make the
process discoverable at authoring and review time. This setup receives its own
record because it is a non-trivial governance change. The directory README
also summarizes every required record field, so it remains both a navigational
index and compatible with the active documentation contract.

## Changed files

Versioned files in scope:

- <code>.github/pull_request_template.md</code>
- <code>README.md</code> and <code>README.de.md</code>
- <code>docs/README.md</code> and <code>docs/README.de.md</code>
- <code>docs/change-traceability.md</code> and
  <code>docs/change-traceability.de.md</code>
- <code>reports/README.md</code> and <code>reports/README.de.md</code>
- <code>reports/audits/change-records/README.md</code> and
  <code>reports/audits/change-records/README.de.md</code>
- <code>reports/audits/change-records/TEMPLATE.md</code> and
  <code>reports/audits/change-records/TEMPLATE.de.md</code>
- this English/German Change-Record pair

Intentional local, unversioned change: <code>AGENTS.md</code>. It is ignored
and therefore intentionally absent from the Git diff.

## Tests added or changed

None. This change adds documentation and governance artifacts rather than
executable tests.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>rtk make check-bilingual-docs</code> | 2 | Initial validation found two German links that incorrectly pointed to English companions; both were corrected. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Bilingual documentation and local-link validation reported <code>bilingual docs ok</code>. | None | None |
| <code>rtk make check-bilingual-docs</code> | 2 | A later active-checker revision required Change-Record sections in the directory README; the README field guide was expanded without changing that independent checker. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Re-run after the README field-guide update reported <code>bilingual docs ok</code>. | None | None |
| <code>rtk make check-doc-links</code> | 2 | The repository-wide check reports only pre-existing missing <code>AGENTS.de.md</code> targets in <code>README.de.md</code> and <code>docs/reference/variables.de.md</code>. | None | None |
| <code>rtk make check-doc-links</code> | 2 | A later run, after unrelated working-tree edits appeared, passed the root path check but failed the Framework link check on changed local AGENTS anchors and connector TODO language companions. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Final validation reported <code>repository path references: PASS</code> and <code>doc links ok</code>. | None | None |
| <code>rtk git diff --check</code> | 0 | No whitespace diagnostics for tracked worktree changes. | None | None |
| <code>rtk rg -n '[[:blank:]]+$' docs/change-traceability.md docs/change-traceability.de.md reports/audits/change-records .github/pull_request_template.md README.md README.de.md docs/README.md docs/README.de.md reports/README.md reports/README.de.md</code> | 1, expected | No trailing-whitespace matches in scoped files; exit 1 means no match. | None | None |
| <code>rtk git status --short</code> | 0 | Listed the scoped changes and unrelated connector TODO modifications; local ignored <code>AGENTS.md</code> was absent. | None | None |

## Security impact

No connector runtime security behavior changes. The process reduces the risk
of undocumented security decisions and accidental retention of sensitive
evidence by requiring a security-impact section, a runtime-evidence boundary,
and explicit data exclusions. It does not replace code review, secret
scanning, or runtime validation.

## Documentation changes

Added the English/German change-traceability policy, the English/German
Change-Record directory README and templates, and this bootstrap record.
Updated the root, documentation, and reports indexes in both languages.
Expanded both pull-request template sections. Updated the local ignored
<code>AGENTS.md</code> rule without versioning local Codex configuration.

## Runtime evidence

No runtime evidence was collected or claimed for this change. This governance
change does not make a connector runtime claim.

## Known limitations

- Earlier <code>make check-doc-links</code> failures arose while unrelated
  working-tree documentation/configuration edits were in progress. They are
  retained in the command history, but the final repository-wide link check
  passes.
- Change Records are manually maintained. The process relies on author and
  reviewer discipline rather than an automated completeness gate.
- The local <code>AGENTS.md</code> instruction is intentionally unversioned;
  the authoritative process is therefore duplicated in versioned
  documentation.

## Remaining risks

An author can still omit or stale a record until review detects it, and English
and German companions can diverge semantically despite structural checks.
The PR checklist, paired templates, final-diff reconciliation requirement, and
existing bilingual check mitigate but do not eliminate those risks.

## Checks not run and rationale

- <code>make quick-check</code> and <code>make lint</code> were not run. The
  requested validation targets were the focused documentation, link, diff, and
  status checks; the change contains no executable source.
- Connector builds, configuration checks, lifecycle runs, and runtime tests
  were not run because this documentation/governance change makes no runtime
  claim and those commands may create external build/runtime artifacts.

## Final diff and review status

The scoped final diff, including the new untracked Markdown files, was
self-reviewed. <code>git diff --check</code> completed with exit code 0 and
the scoped trailing-whitespace scan found no matches. The bilingual check
passed after a corrected-link iteration and a directory-README field-guide
update required by the active checker. The final repository-wide link check
reported <code>repository path references: PASS</code> and <code>doc links ok</code>.

This record is reconciled with the scoped actual diff and the real outcomes
above. No commit or pull request was created. The required checks are rerun
after this record reconciliation; no test is treated as passed solely because
it was planned.
