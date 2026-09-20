# Definition of Done

## Individual criterion statuses

Use: `passed`, `failed`, `blocked`, `not_run`, `not_applicable`.

## Overall task outcome

Use exactly one:

- `complete`: every mandatory applicable criterion is `passed` or properly `not_applicable`; no mandatory failure/blocker/hidden required `not_run` remains;
- `partial`: useful work exists but a required criterion/deliverable/evidence remains incomplete or not run;
- `blocked`: a mandatory prerequisite/decision/permission/safe environment prevents progress;
- `failed`: validation disproved the requested result or a mandatory criterion failed.

## Universal completion invariants

Before `complete`:

- original prompt and requirement inventory are reconciled;
- requested deliverables exist;
- no silent scope expansion/reduction occurred;
- material decisions are resolved or correctly block completion;
- implementation is complete for the scoped behavior, with legitimate existing behavior preserved;
- applicable validation actually ran or has a truthful non-pass disposition;
- no build/static/report result is promoted beyond its evidence layer;
- final diff/changed files are reviewed and `git diff --check` is addressed for versioned changes;
- security applicability and findings are resolved under `security-policy.md`;
- applicable EN/DE docs and Change Record are current;
- Parent/Framework/MRTS boundaries are respected;
- no required background process/subagent remains active;
- task-owned storage/worktree/branch objects have a safe retained/cleaned disposition;
- no unauthorized Git/delivery/system action occurred.

## Domain completion

Do not copy domain checklists here. Apply the relevant primary owner(s):

- change behavior: `change-workflow.md`
- testing/evidence: `testing-and-evidence.md`
- matrix: `connector-matrix.md`
- transports/hardening: `protocol-and-hardening.md`
- Python: `python-policy.md`
- security/findings: `security-policy.md`, `findings-policy.md`
- Framework/cross-repo: `framework-orchestration.md`
- delivery/merge: `delivery-and-ci.md`, `master-integration.md`
- docs/traceability: `documentation-and-traceability.md`
- cleanup/restoration: `cleanup-and-restoration.md`

## Final report

State the overall outcome, requirement-by-requirement disposition, significant checks/results, blockers/limitations, delivery state, and whether any commit/push/PR/merge/master change occurred.
