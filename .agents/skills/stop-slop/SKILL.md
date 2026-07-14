---
name: stop-slop
description: Perform a focused quality pass that removes vague, unsupported, or needlessly inflated repository prose and implementation claims.
---

# Perform a focused quality pass

Use this adapter to improve clarity after facts, scope, and evidence have been
established.

## Trigger conditions

- A user asks for a quality, clarity, concision, or unsupported-claim review.
- A draft Change Record, documentation update, or pull-request description is
  hard to verify because it is vague or repetitive.
- A completed implementation needs a final focused writing and claim check.

## Do not use when

- The task is to establish a fact, conduct a security audit, or make an
  architecture decision; obtain evidence first.
- The user asks for a stylistic rewrite that would remove required technical
  detail, bilingual parity, or safety caveats.
- The text is generated evidence that must be changed through its generator.
- The input is C/C++ code, a shell script, JSON, a verbatim quotation, or a
  normative status value rather than explanatory prose.

## Local procedure

1. Identify the authoritative source, actual command results, and intended
   audience before editing.
2. Remove unsupported certainty, filler, duplicated claims, and vague status
   labels while retaining commands, paths, limits, risks, and result scope.
3. Preserve normative terms, security severity, status values, commands,
   paths, quotations, API names, Change Record and test evidence, hashes, run
   IDs, URLs, code, identifiers, configuration keys, and machine-readable data
   exactly.
4. Review English and German separately and language-appropriately while
   preserving equivalent technical meaning and literal material.
5. Perform a semantic-diff review after every proposed text edit and before
   accepting it. Do not alter a commit message as part of this skill.
6. Run the required documentation checks for any accepted reader-facing change.

## Safety boundary

This is a quality adapter, not an authority to reduce evidence requirements,
hide a failure, change generated output manually, or delete a required warning.
Repository policy has priority.

## Provenance

Adapted from the MIT-licensed source recorded in [UPSTREAM.md](UPSTREAM.md).
No upstream scripts, dependencies, network behavior, or command automation is
included.
