<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Test levels and statuses

**Language:** English | [Deutsch](test-levels.de.md)

## Scope

Build, configuration parsing, start smoke, runtime smoke, and full-lifecycle evidence are distinct levels. A successful build or start is not a rule-engine PASS.

Build, configuration parsing, start smoke, runtime smoke, and full-lifecycle evidence are distinct levels. A successful build or start is not a rule-engine PASS.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Status and exit values

`PASS` means a checked claim was met; `FAIL` a negative check; `BLOCKED` a missing prerequisite; `NOT EXECUTED` no execution; `NOT APPLICABLE` no applicability; and `UNSUPPORTED` no host-provided capability. Process code `0` means technical completion, `1` a general error, `2` a validation/aggregate error, and `77` a declared missing optional prerequisite.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
