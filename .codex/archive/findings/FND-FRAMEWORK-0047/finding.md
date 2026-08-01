# FND-FRAMEWORK-0047 — Quoted YAML `uses` key bypasses reviewed action-lock binding for a write-capable Framework publisher

- Category: `security_validated`
- Repository / ownership: `framework` / `framework`
- Priority / severity / confidence: `P1` / `high` / `reproduced`
- Status / feasibility: `fixed` / `feasible_now`
- Release blocker / security relevance: `true` / `true`

## Summary

Framework PR #40 adds a reviewed action lock for workflow tooling. Its lock-
equality checker parses only source lines beginning with literal unquoted
`uses:`. A YAML-legal quoted key such as:

```yaml
"uses": actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
```

is parsed as the same `uses` field but bypasses that source-line parser. The
other mandatory validators require a full immutable SHA but do not compare it
with the reviewed lock. The exact PR #40 validator chain therefore accepts a
lock-divergent publisher action reference.

## Impact and boundaries

The publisher later runs with `contents: write` and `pull-requests: write` and
uses its scoped GitHub token. The finding does not claim that an unauthenticated
party can create a commit in an official `actions/*` repository. It proves the
Framework reviewed-lock provenance boundary can be bypassed before a token-
bearing publisher runs after a change is accepted into the trusted default
branch.

Mutable tags remain rejected; this is a distinct full-SHA lock-equality bypass.
It is a P1 high-severity release blocker until repaired and regression-tested.

## Exact evidence and reproduction

- Base: `f73f8842f45318e2df8aff1d31855eeb7c20a22f`
- Affected head: `c274460a3e27b9fc0dfe904e1ce5eba33042f444`
- Run: `20260722T145132Z-framework-pr-39-41-master-integration-9a3c7dc7`
- Evidence: `CAND-FW40-QUOTED-USES/validation_report.md`
- SHA-256: `a7f5df22d62985136dede2c12d775da8d80661646e24e11a57ff45941dd46b8c`

The evidence-only harness mutated a detached exact-head worktree, ran the same
three static validators used by the read-only `validator` job, and restored the
workflow after every case. The normal workflow and mutable-tag negative control
behaved correctly. The quoted different full SHA passed all three validators.

The publisher depends on the successful validator and has no `always()`
override, so this successful case can reach it under normal trusted
schedule/dispatch conditions. No publisher, network action, or token-bearing
command was invoked for this reproduction.

## Required remediation and validation

Bind every parsed external `uses` reference to the reviewed action lock
regardless of YAML spelling. Preserve local-action behavior, version-comment
checks, least-privilege permissions, publisher dependency, and branch
condition. Add focused quoted-key and flow-mapping full-SHA regressions plus a
legitimate current-lock control.

Before this finding can be closed, the consolidation branch must pass focused
tests plus all three static validators; its exact PR head must then pass the
applicable hosted security, CI, and Sonar controls. `FND-FRAMEWORK-0046` and
`FND-SONAR-0002` remain separate blockers.

The consolidation is locally `fixed`: its contract recursively compares parsed
external `uses` references with the reviewed lock, while focused tests reject
both quoted-key and flow-mapping lock-divergent full SHAs. The publisher's
least-privilege permissions and validator dependency are unchanged. Hosted
exact-head workflow-security and quality evidence remains required before
verification.

The locally fixed repair is bound to Framework commit
`22747d460a9f7be02760edf05c311be376492457`; clean-worktree, exact-range
whitespace, and native `make lint` checks passed. Hosted exact-head evidence
remains required.

Open Framework PR #42 at
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` has passed all applicable hosted
security and quality controls, including CodeQL and the Sonar PR Quality Gate.
This strengthens the `fixed` disposition, but the finding is neither
`verified` nor closed until normal master integration and resulting-master
evidence.
