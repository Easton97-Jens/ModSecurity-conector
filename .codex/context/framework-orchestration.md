# Parent / Framework / MRTS Orchestration

## Boundaries

Parent, Framework, and MRTS are separate source, Git, test, and delivery units:

- Parent: `/root/git/ModSecurity-conector`
- Framework: `modules/ModSecurity-test-Framework`
- MRTS: `modules/ModSecurity-test-Framework/tools/MRTS`

A Parent-root session may coordinate necessary Framework work without requiring the user to change the VS Code root, but Framework work remains a separate repository scope.

## Before Framework investigation or change

1. establish from repository evidence that Framework ownership is required;
2. read the active Framework `AGENTS.override.md` if present, otherwise `AGENTS.md`;
3. load its applicable Framework-local policies;
4. inspect Parent, Framework, and MRTS Git state separately;
5. record Framework goal/owned files/Parent impact/MRTS impact/delivery state in the task plan.

Do not copy reusable Framework logic into Parent merely to avoid crossing the repository boundary.

## Git and delivery

Parent and Framework changes never share a commit. Framework branch/commit/push/PR/CI/delivery use Framework-local policy and explicit Framework paths. Framework delivery never automatically updates the Parent gitlink.

If the current Parent task includes a Parent gitlink update, Framework change must first be remotely available and, when Parent integration depends on Framework `master`, the separately authorized Framework merge and exact Framework `master` SHA must be verified before the Parent change.

## No Parent pointer update

When Framework task work is delivered but a Parent gitlink update is out of scope, preserve the Framework task branch/PR and, when safe and non-forcing, return the Framework worktree to the exact commit recorded by Parent. If local state prevents safe restoration, preserve it and report `framework_restoration_blocked`.

## MRTS

During Parent/Framework work, MRTS is organizationally read-only by default. Inspecting it does not grant write authority. A current user may separately select MRTS and enumerate permitted action classes; that starts an independent MRTS task under MRTS-local instructions and never implies a Framework or Parent gitlink update.

Do not claim filesystem-enforced MRTS denial unless current configuration/runtime evidence proves it.
