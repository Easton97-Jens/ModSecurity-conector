---
name: bilingual-change-record
description: "Create or review a complete English/German Change Record pair and its documentation companions for a material repository change. Use when versioned reader-facing content or a Change Record changes; do not use for ignored local Codex/RTK configuration alone."
---

# Bilingual Change Record

Keep English technically primary and German fully equivalent. Treat commands,
paths, hashes, URLs, configuration keys, machine-readable content, and exact
error messages as technical literals rather than translation targets.

## Required inputs

- Change ID, base revision, task scope, final file list, and actual checks.
- All affected English/German documents and the intended runtime/evidence claim.
- Known limitations, residual risks, and intentionally local unversioned files.

## Repository boundary

Read the active `AGENTS.md` and traceability policy before editing. Create
both language companions together under the documented Change Record location.
Do not create a German companion for `AGENTS.md`, `RTK.md`, `.codex/`, or
`.rtk/`.

## Workflow

1. Identify every affected reader-facing English/German pair before editing.
2. Create or update both records with the same Change ID, base revision,
   acceptance criteria, security boundary, limitations, and actual results.
3. Preserve all technical literals unchanged in both versions.
4. List local ignored configuration separately from versioned files.
5. Record only commands that actually ran; put planned or unrun checks in the
   explicit non-run section.
6. Reconcile both records with the final diff and run bilingual, link, and
   whitespace checks.

## Status model

Use `draft`, `paired`, `validated`, `needs_reconciliation`, or a
transparent blocking status. A paired record without actual outcomes is not
`validated`.

## Expected result

Produce equivalent EN/DE records that include motivation, acceptance criteria,
technical decisions, security impact, changed files, actual tests, runtime
evidence or its absence, checks not run, limitations, residual risks, and final
review status.

## Safety and stop conditions

Stop if an outcome, final SHA, security claim, or companion document is
unknown. Do not invent a passing result, translate a technical literal, hand
edit generated evidence, or place secrets and raw payloads in a record.

## Definition of done

Both companions contain the same material facts, all required links resolve,
the final diff matches the records, and actual verification is clearly
distinguished from planned or unavailable work.

## References

- [Change traceability](../../../docs/change-traceability.md)
- [Operations and security](../../../docs/operations-and-security.md)
- [Change Record index](../../../reports/audits/change-records/README.md)
