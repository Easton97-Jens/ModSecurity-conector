# Evidence and Claim Integrity Assessment

## Trigger

Use when the user asks whether reports, capability statements, matrices, or runtime/security claims are trustworthy and correctly bound.

## Load

- `../command-execution-policy.md` for every local shell/project command;

- `../testing-and-evidence.md`
- `../security/checks/evidence-integrity.md`
- `../architecture-and-boundaries.md`
- affected connector delta(s)
- `../connector-matrix.md` when matrix claims are involved

## Check

Reconcile source revision, Framework/MRTS gitlinks, logical profile, run ID, rules/effective configuration, host/tool versions, transport, artifact hashes, cleanup state, generated-report source, and status semantics.

Flag stale/mixed/misbound evidence, source/build/config promotion, cross-profile result transfer, generated-report drift, wrong revision, and missing evidence provenance.
