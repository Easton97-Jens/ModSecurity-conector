---
name: bilingual-changelog-generator
description: Draft or update paired English and German change documentation from verified repository evidence.
---

# Draft paired change documentation

Use this repository-authored adapter only for an explicit bilingual changelog,
release-note, or release-summary request backed by verified repository evidence.

## Trigger conditions

- The user explicitly asks for a bilingual changelog, release note, or release
  summary and provides or approves a commit/tag range.
- A Change Record must be reconciled into an explicitly requested release or
  changelog range after the final diff and actual checks are known.

## Do not use when

- The requested file is local Codex/RTK configuration, which has no German
  companion requirement.
- A material change needs ordinary project documentation but no explicit
  release/changelog request.
- The source is generated documentation with a separate generator contract.
- Verification results are still unknown; draft a clearly marked plan instead
  of claiming completion.

## Local procedure

1. Require an explicit commit/tag range and read `docs/change-traceability.md`
   plus the Change Records in that range as the primary evidence.
2. Trace every entry to its supporting commit and classify it as a feature,
   fix, security change, breaking change, or internal change. Do not market an
   internal refactor as a user feature.
3. Build the English technical primary text from actual file scope, commands,
   result statuses, limitations, and security impact.
4. Create the German companion with equivalent headings, examples, links,
   warnings, commands, hashes, paths, and result scope. Do not translate code
   or machine-readable material.
5. Update the documentation and Change Record indexes, then run bilingual,
   link, whitespace, and final-diff checks.

## Safety boundary

Do not invent a passed check, minimize a remaining risk, translate an exact
technical identifier, or use documentation to conceal an incomplete delivery.
Do not automatically create a tag, release, or publication, and do not claim
release readiness without the repository's separately required evidence.

## Provenance

Repository-authored. It applies the repository's bilingual and change
traceability requirements; [UPSTREAM.md](UPSTREAM.md) records that no external
skill text or generator was imported.
