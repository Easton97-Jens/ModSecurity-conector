# Connector Security Assessment Profile

## Trigger

Use when the user requests a deep/security review of one Parent connector host family or one logical connector profile.

## Mode

`analysis_only`

## Load

- `../command-execution-policy.md` for every local shell/project command;

1. `../security/connector-deep-assessment.md`
2. exactly one connector delta under `../security/connectors/`
3. only the check modules named by that delta
4. `../security-policy.md`, `../testing-and-evidence.md`, `../resources-and-storage.md`, `../architecture-and-boundaries.md`, `../findings-policy.md`, `../protocol-and-hardening.md`, and `../definition-of-done.md`
5. Framework instructions/policies only when Framework material is actually needed

## Scope

The connector delta defines direct paths, logical profiles, host-specific boundaries, and validation seeds. Supporting Common/CI/Framework material is read-only and included only when a concrete control/dataflow requires it.

## Writes

No product/source/test/delivery writes. Durable assessment output goes to `$CODEX_RUN_ROOT/security/<connector>/<RUN_ID>/`. Large temporary execution artifacts use configured external roots.

## Completion

Apply the generic deep assessment completion contract. A complete security assessment may report validated findings and failed product tests; it is not a production approval.
