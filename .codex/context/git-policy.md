# Parent Git Policy

## Safety

Preserve pre-existing tracked/untracked user work. Git writes require current task authority and the applicable execution contract.

Parent, Framework, and MRTS are separate repositories. A Git action in one never authorizes a Gitlink or delivery action in another.

## Worktrees and branches

For non-trivial versioned Parent work, prefer a task-owned external worktree and task branch based on current verified `origin/master`, unless the current user explicitly directs use of the existing checkout.

Before staging inspect status, unstaged diff, and staged diff. Stage only explicit task-owned files:

`git add -- <task-files>`

Do not use broad staging in a mixed/unclear worktree.

## Prohibited history/destructive shortcuts

Do not:

- commit directly on `master`;
- force-push;
- amend/rebase published task history;
- `git reset --hard`, `git clean`, forced checkout, or broad stash as task cleanup;
- change Git configuration/remotes to bypass a mismatch;
- stage Framework/MRTS files in a Parent commit.

## Remote preflight

Before creating a delivery branch, pushing, PR actions, or remote-branch deletion, verify current `origin` fetch/effective-push destination, repository identity, writable non-archived state, and default branch against the expected Parent repository `Easton97-Jens/ModSecurity-conector`.

A mismatch is `blocked_remote_mismatch`; do not rewrite the remote or choose an alternate destination automatically.

After push, delivery evidence must bind local HEAD, remote task branch, and PR head to the same current SHA.
