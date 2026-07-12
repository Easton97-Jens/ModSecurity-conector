<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Transaction lifecycle

**Language:** English | [Deutsch](transactions.de.md)

## Scope

P1 processes request headers, P2 processes request body and ends at request EOS, P3 processes response headers, and P4 receives response body chunks and ends at response EOS.

Append and finish are distinct operations. A chunk is borrowed while it is forwarded; EOS performs the one guarded finalization for that body direction.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
