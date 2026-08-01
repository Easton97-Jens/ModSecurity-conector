# FND-PARENT-0052 — Full evidence producer accepts mutable supply-chain inputs

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0052` |
| Category | `dependency_risk` |
| Repository / ownership | Parent / Parent |
| Priority / severity / confidence | P1 / medium / confirmed |
| Status | `fixed` |
| Release blocker | `true` |
| Security relevant | `true` |

## Summary

The proposed PR #74 full verified-report producer made two mutable external
inputs mandatory: Expat was resolved from GitHub's latest-release endpoint and
the workflow used a bootstrap that upgraded Pip and installed a range-based
PyYAML dependency. Either input could vary while the Parent and Framework
revisions remain unchanged, so their resulting runtime evidence would not be
reproducibly provenance-bound.

## Evidence and source-to-sink path

1. `.github/workflows/verified-report-governance.yml` invokes the strict/full
   `make verified-report-run` producer.
2. `ci/runtime/lifecycle/run-verified-report-run.py` requires
   `make prepare-runtime-components`.
3. `ci/provisioning/components/prepare-runtime-components.py` previously used
   `prepare_release_git_component` for mandatory Expat, resolving GitHub's
   current `releases/latest` tag at execution time before checkout.
4. The proposed workflow previously invoked `make setup-dev`; the Framework
   bootstrap upgrades Pip and installs `requirements-dev.txt`, whose PyYAML
   declaration is range-based.

The strict evidence gate itself remains fail-closed; this finding concerns the
trustworthiness of the newly required producer inputs, not a gate bypass.

## Remediation and acceptance criteria

- The strict evidence Expat path accepts only a reviewed full immutable commit
  ID, never a branch, tag, abbreviated SHA, or latest-release lookup, and
  verifies the resolved checkout against it. The non-strict compatibility path
  remains release-backed and cannot mint strict evidence.
- The workflow supplies the reviewed Expat commit for the verified release
  `R_2_8_2` and records that configuration as an exact workflow input.
- Python tooling for this producer is installed with the selected Python,
  Framework `requirements-ci.lock`, `--require-hashes`, and `--only-binary`;
  it neither upgrades Pip nor consumes `requirements-dev.txt`.
- Focused unit and workflow-contract tests reject mutable Expat refs and the
  former unpinned bootstrap path.
- A fresh exact-head full runtime run and terminal strict gate pass with the
  resulting revision-bound evidence chain.

## Current status and residual risk

The Parent source remediation is implemented and passed focused local controls
in the isolated PR #74 worktree: strict Expat dispatch, mutable-ref rejection,
checkout-head mismatch rejection, non-strict compatibility, the workflow/tool
contract, bilingual documentation, and whitespace validation. No branch has
been pushed and no protected merge occurred after discovery. The full runtime
producer and both PR integrations remain blocked until exact-head hosted
validation completes. No risk is accepted.

## History

- `2026-07-26T06:32:35Z`: Independent security review validated the mutable Expat and
  Python-bootstrap inputs in the newly activated full producer. The proposed
  push was suspended before publication; the strict gate was not weakened.
- `2026-07-26T06:44:31Z`: The Parent-only strict-path remediation and focused
  validation passed. The retained validation artifact records the commands and
  results; hosted full evidence remains pending.
