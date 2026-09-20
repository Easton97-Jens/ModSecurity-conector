# Local Resources and Storage Policy

## Authority

Concrete machine paths and numeric storage thresholds come from the active project `.codex/config.toml` and its exported environment variables. Do not duplicate those numeric limits in policy prose.

The canonical heavy-work area is the configured `/var/tmp/codex/ModSecurity-conector` tree. Use the configured variables such as:

- `CODEX_TEMP_ROOT`, `CODEX_RUN_ROOT`, `STATE_HOME`
- `BUILD_ROOT`, `TMP_ROOT`, `LOG_ROOT`, `CACHE_ROOT`
- `ANALYSIS_ROOT`, `EVIDENCE_ROOT`, `MATRIX_ROOT`, `MRTS_BUILD_ROOT`
- `CODEX_STORAGE_WARN_GIB`, `CODEX_STORAGE_NORMAL_BUDGET_GIB`, `CODEX_STORAGE_HARD_LIMIT_GIB`
- `CODEX_STORAGE_MIN_FREE_START_GIB`, `CODEX_STORAGE_MIN_FREE_RUNTIME_GIB`, `CODEX_STORAGE_FINAL_TARGET_GIB`
- `STORAGE_BUDGET_BIN`, `STORAGE_CLEANUP_BIN`, `CODEX_CLEANUP_ARCHIVE_ROOT`

## Source-filesystem protection

The source checkout is not overflow storage. Put large builds, downloads, caches, runtime state, logs, evidence, matrices, compiler databases, scanner output, and temporary files under the configured external Codex roots.

Do not redirect heavy output to `/tmp`, `$HOME`, user-global caches, or the source checkout merely because another root is full.

## Capacity preflight

Before substantial build/download/runtime/matrix/analysis work:

1. inspect actual free capacity of the configured filesystem;
2. run the configured storage-budget preflight when the task contract requires it;
3. estimate task-owned peak usage conservatively;
4. refuse to start work that would violate the configured hard/free-space limits;
5. never delete foreign data to create space.

During large work, re-check capacity and stop/reduce work before crossing configured runtime free-space or hard-limit boundaries.

## CPU and memory

For parallel-safe CPU-bound compilation/analysis, detect logical CPUs dynamically (`nproc --all`) and prefer using all available cores when RAM and target semantics permit.

Do not set a repository-wide `MAKEFLAGS=-j...` merely to consume all cores. Many Parent targets orchestrate ports, services, mutable runtimes, evidence paths, or nested tools and must use their own concurrency model.

Agent-thread concurrency (`[agents]`) is independent from compiler/build concurrency.

Before very heavy parallel work, inspect available memory. Reduce simultaneous heavy jobs when full CPU concurrency would cause swap/OOM/host instability or invalidate tests.

## Parallel runtime work

Run runtime/connector/matrix jobs concurrently only when ports, build roots, runtime roots, temporary paths, logs, evidence, process ownership, and run IDs are disjoint. Shared mutable state requires sequencing unless the repository provides a safe isolation mechanism.

## Worktrees and cleanup

Use task-owned external worktrees under the configured `/var/tmp/codex/worktrees/...` convention. Register task-owned data and delete only data whose ownership and retention disposition are proven.

Unknown/foreign paths are preserved. Broad deletion and `git clean` are never storage shortcuts.

If `CODEX_CLEANUP_ARCHIVE_ROOT` resides on a constrained filesystem, do not move large task data there merely as “cleanup”; report the configuration mismatch or retain the data until a safe archive destination is selected.
