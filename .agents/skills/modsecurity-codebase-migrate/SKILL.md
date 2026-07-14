---
name: modsecurity-codebase-migrate
description: Plan a bounded ModSecurity-conector migration while preserving component ownership, compatibility, and evidence boundaries.
---

# Plan a codebase migration

Use this repository-authored adapter for a proposed source, connector,
configuration, lifecycle, or test-boundary migration.

## Trigger conditions

- The user asks to migrate a connector, common component, configuration model,
  test boundary, or build/lifecycle workflow.
- A change may move ownership between Parent, Framework, common runtime, and a
  host connector.
- An upstream or dependency change needs a compatibility and rollback plan.

## Do not use when

- The task is a small localized defect with no migration or ownership change.
- The request proposes changing the Framework without its own authorized
  Framework task and delivery process.
- Product evidence cannot yet identify a source/consumer boundary.

## Local procedure

1. Read `docs/repository-concept.md`, architecture, connector documentation,
   testing/evidence documentation, and the applicable local workflow.
2. Map current owner, source of truth, external interfaces, persisted data,
   configuration, test evidence, and rollback point.
3. Keep host-specific logic under the relevant connector and common runtime
   free of host SDK dependencies. Do not silently move reusable tests out of
   the Framework boundary.
4. Define a phased compatibility plan with explicit C17, build, contract,
   runtime, protocol, and CRS/MRTS dispositions as applicable.
5. Require bilingual documentation and a Change Record for a material change.

## Per-batch migration checklist

For every reviewable batch, document the exact transformation and blast radius,
use a disjoint file scope, and define clear acceptance criteria. Prefer a
codemod before manual follow-up where it is applicable. Include positive and
synthetic negative tests, make the batch independently revertible, and obtain
review before proceeding to the next batch. Do not use automatic merge as a
migration mechanism.

## Safety boundary

No migration is authorized merely by this planning skill. Preserve Parent and
Framework delivery boundaries, avoid destructive cleanup, and ask for a
decision when compatibility, security, resource use, or public behavior is
materially ambiguous.

## Provenance

Repository-authored. The migration concepts were independently derived from
the repository architecture and the discovery source documented in
[UPSTREAM.md](UPSTREAM.md); no external text or automation was imported.
