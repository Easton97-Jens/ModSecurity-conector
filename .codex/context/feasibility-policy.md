# Feasibility and Execution Gate

Apply this policy before non-trivial implementation and before builds, runtime work, downloads, installations, security scans, Git/GitHub writes, external services, or cross-repository work.

## Assess each requested work item

Check:

- desired outcome is technically clear;
- current prompt authorizes the scope;
- owning repository is known;
- relevant files/symbols/current behavior are identified;
- required compiler/runtime/host/test prerequisites exist;
- permissions, network, ports, storage, CPU/memory, and process requirements are safe;
- no security control must be weakened;
- a realistic validation path exists;
- a legitimate control case is identifiable;
- regression testing is feasible;
- the condition is not already fixed or explicitly out of scope.

## Feasibility statuses

Use exactly one per work item:

- `feasible_now`
- `feasible_after_local_setup`
- `requires_user_decision`
- `blocked_environment`
- `blocked_external_dependency`
- `blocked_permissions`
- `blocked_missing_evidence`
- `already_fixed`
- `not_applicable`
- `unsupported_with_evidence`
- `out_of_scope`

Only `feasible_now` and `feasible_after_local_setup` permit implementation. Local setup must be reversible, task-owned, and already authorized.

A missing local tool or environment alone does not prove a feature is unsupported. `unsupported_with_evidence` needs concrete source/build/config/runtime evidence.

When evidence changes, update the feasibility status before continuing.
