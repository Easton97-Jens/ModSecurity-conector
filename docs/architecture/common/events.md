<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Event and evidence contract

**Language:** English | [Deutsch](events.de.md)

## Scope

Events carry bounded metadata such as phase, rule ID, message ID, action, commit state, and lifecycle counters. They must not carry request or response payloads.

A result and an event are different evidence records; a result alone cannot infer a causal host event.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
