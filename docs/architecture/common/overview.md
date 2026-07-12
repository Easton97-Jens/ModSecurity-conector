<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Common architecture overview

**Language:** English | [Deutsch](overview.de.md)

## Scope

The Common layer defines connector-neutral contracts. Host structures, host memory management, and host callbacks remain in each connector.

The selected core is HTTP/1.1 P1–P4. It borrows chunks from a host and never makes Common own host body storage.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
