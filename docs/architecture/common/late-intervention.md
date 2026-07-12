<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Late intervention

**Language:** English | [Deutsch](late-intervention.de.md)

## Scope

Before commitment a host may apply a supported deny action. After commitment, Safe mode records a `log_only` outcome; it must not be represented as a rewritten client status.

Strict behavior is a separate host capability and is not claimed for every connector.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
