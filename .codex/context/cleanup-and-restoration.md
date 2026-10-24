# Cleanup and Parent Workspace Restoration

## Objects stay separate

A PR, remote branch, local branch, task worktree, external clone, authoritative checkout, GitHub repository, and Gitlink are distinct objects. Authority/disposition for one does not transfer to another.

Authoritative Parent, Framework, MRTS checkouts and GitHub repositories are never ordinary cleanup targets.

## Worktree cleanup

Before removing a task-owned worktree prove:

- exact registered path/owner/repository;
- clean tracked/staged/untracked state;
- no unique/unpublished required work;
- remote/PR disposition and current SHA evidence;
- no active process/lock;
- retained evidence does not depend on the worktree;
- no dependent PR/worktree needs it.

If uncertain, preserve it and report cleanup blocked. Never force-remove a worktree or manually delete a registered worktree.

## Branch cleanup

Use only safe local deletion (`git branch -d`) when no registered worktree uses the branch and no unique work remains. Do not force-delete.

An open PR keeps its remote branch. Remote deletion is a separate verified action only after merge or evidenced close-without-merge and a fresh expected-`origin` preflight.

## Parent restoration after verified integration

After an authorized verified Parent integration and only when the Parent worktree can switch safely:

1. use the explicit Parent root;
2. inspect status/current branch/root;
3. preserve any foreign or uncommitted work;
4. verify current expected remote identity;
5. switch to `master` non-forcing;
6. update with `git pull --ff-only origin master`;
7. verify Parent HEAD equals `origin/master`;
8. inspect submodule state.

Never restore with hard reset, forced checkout, broad clean, or automatic stash.

Nested Framework/MRTS normally remain at the exact gitlink recorded by their parent; detached HEAD is valid. Do not switch nested repositories to their own `master` merely for appearance.

When a Parent-session Framework PR exists but the Parent gitlink update is out of scope, `framework-orchestration.md` owns the no-pointer Framework restoration behavior.
