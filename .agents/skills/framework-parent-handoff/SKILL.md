---
name: framework-parent-handoff
description: "Coordinate a deliberate change that spans the independent ModSecurity test Framework and this Parent repository. Use when reusable Framework work must precede a Parent Gitlink or handoff; do not use for Parent-only work or to change the Framework Gitlink without completed Framework delivery."
---

# Framework Parent handoff

The Parent and Framework are separate repositories with separate source,
testing, delivery, and CI evidence.

## Required inputs

- The proposed reusable Framework change, Parent consumer change, and ownership
  justification.
- Framework and Parent base revisions, branches, tests, remotes, and CI
  requirements.
- The intended Framework commit and the authorized Parent Gitlink update.

## Repository boundary

Read the active `AGENTS.md` in both repositories and the current repository
concept. Keep connector product code, configuration, and Parent contracts in
the Parent. Keep reusable cases, normalizers, schemas, and runners in the
Framework. This skill never authorizes an implicit Framework change.

## Workflow

1. Confirm that the behavior belongs in the Framework rather than the Parent.
2. Change and test the Framework in its own task branch.
3. Commit and push the Framework change, then verify Framework CI for its final
   SHA.
4. Confirm the Framework commit is remotely reachable.
5. Update the Parent Gitlink only in a separately authorized Parent change.
6. Update the Parent Change Record and verify Parent CI for the final Parent
   SHA.

## Status model

Report `parent_only`, `framework_pending`, `framework_delivered`,
`parent_handoff_pending`, `parent_delivered`, or a transparent delivery or
security blocking status. A local Framework checkout is not
`framework_delivered`.

## Expected result

Return the ownership decision, Framework and Parent SHAs, separate tests and CI
results, Gitlink disposition, linked Change Records, and open follow-up work.

## Safety and stop conditions

Stop if the owner is unclear, the Framework is dirty, the Gitlink would move to
an unverified commit, or the Parent and Framework changes cannot be reviewed
separately. Do not rewrite either repository history or combine their commits.

## Definition of done

The Framework is independently delivered before a Parent Gitlink moves, both
repositories have their own final-SHA evidence, and the Parent record names the
exact Framework handoff.

## References

- [Repository concept](../../../docs/repository-concept.md)
- [Testing and evidence](../../../docs/testing-and-evidence.md)
- [Change traceability](../../../docs/change-traceability.md)
