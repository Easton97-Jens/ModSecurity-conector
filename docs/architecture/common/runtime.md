<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Runtime contract

**Language:** English | [Deutsch](runtime.de.md)

## Scope

Runtime roots are explicit and outside the checkout. Cache-v2 is reusable only for matching identity inputs; build, log, and evidence roots are run-local.

Use `BUILD_ROOT`, `CACHE_ROOT`, and `EVIDENCE_ROOT` through Make targets; their defaults and safety rules are documented centrally.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
