# All-Connectors Deep Security Assessment Profile

## Trigger

Use when the user requests deep security coverage across all Parent connector families.

## Mode

`analysis_only`


## Command execution

Load `../command-execution-policy.md` before issuing local shell/project commands.
## Required connector sequence

Assess independently:

1. Apache (`apache`)
2. NGINX (`nginx`)
3. HAProxy (`haproxy-htx`, `haproxy-spoe-spop`)
4. Envoy (`envoy-ext-proc`, `envoy-ext-authz`)
5. Traefik (`traefik-native-uds`, `traefik-forwardauth`)
6. lighttpd (`lighttpd-stock`, `lighttpd-patched`)

Load `connector-deep-assessment.md`, then each connector delta in turn. Reuse common check definitions but keep connector/profile evidence, coverage, candidate IDs, findings, and runtime claims separate.

## Cross-cutting analysis

After per-connector work, reconcile shared root causes in Common, Framework, MRTS, CI, libmodsecurity, host/toolchain dependencies, and common evidence/phase contracts. Do not merge independently reachable connector instances merely because they share a helper.

## Resources

Sequence host-runtime work by default. Parallelize only when ports, runtimes, build/output roots, evidence, processes, and memory/storage budgets are disjoint. Compilation/static analysis may use full safe CPU parallelism.

## Output

Use one parent run root with connector children and a cross-cutting summary. Keep the ten logical profiles visible in the final coverage ledger.
