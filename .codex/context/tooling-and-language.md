# Tooling and Language Policy

## General

Command invocation itself is owned by `command-execution-policy.md`; this file selects tools/language checks but does not override RTK execution requirements.

Project-native Make targets and scripts take priority over generic helper commands. Discover availability from the current checkout/environment; do not install a missing auxiliary tool automatically unless another specific policy grants that action.

Tool/editor/static-analysis output is scoped evidence, not a substitute for real compilation/tests/runtime.

## C and C++

Repository production baselines remain C17 and C++17 when the current component contracts require them. Validate changed relevant code with the real component/build flags, including the required standard mode and warnings. Newer C/C++ standards are separate advisory diagnostics unless the repository explicitly changes its production baseline.

Compilation databases must come from real supported builds and remain outside the checkout. Static-analysis findings are leads requiring validation. Sanitizers/hardening are diagnostic and must not leak into production configuration.

## Go

Each actual `go.mod` owns its module language/dependency contract. Run Go commands from the actual module directory. Do not create a root `go.work`, implicitly download another toolchain, or accept incidental `go.mod`/`go.sum` changes during analysis.

Keep `go test`, `go vet`, Staticcheck, vulnerability analysis, and race evidence separate.

## Shell

Use repository-native shell checks first. ShellCheck/shfmt/language-server output is additional scoped evidence. Review formatting diffs before any formatting write.

## Generic helpers

Prefer installed `rg`, file-discovery tools, `jq`, GitHub CLI, compiler tools, and other helpers when they improve the task without changing repository contracts. A tool inventory is point-in-time; re-check the environment when a task depends on a tool.

## Tool updates

Do not update Codex, compilers, Go, Python tools, analyzers, formatters, or other development tools as incidental work. A permitted update must identify its official source, current/target version, installation origin, compatibility, rollback, and validation, and must not silently change project dependencies or language baselines.
