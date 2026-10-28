# Command Execution and RTK Policy

## Purpose and ownership

This file is the primary owner for local shell-command execution and RTK use in the Parent control plane.

It defines **how** an authorized command is invoked. It does not grant repository writes, network access, package installation, service changes, Git delivery, merge authority, SonarQube authentication, or any other material action that is not already authorized by the current task and its owning policy.

## Mandatory RTK execution path

RTK is the mandatory local execution proxy for project commands issued through the shell.

A request to use a repository-native command directly means using that native command **through RTK**. Use a supported filtered command for normal inspection/build output:

```text
rtk git status
rtk make quick-check
rtk make build-nginx
```

For machine-readable output, complete diffs, or evidence that must retain the original output, use the current unfiltered execution command:

```text
rtk bypass git diff --check
rtk bypass python3 .codex/bin/validate-v32-structure.py
```

`rtk bypass <command> [args...]` still executes through RTK and tracks usage; it disables output filtering. Since RTK v1.0.0, `bypass` is the canonical name for the deprecated `proxy` alias. Use `bypass` in new commands. Preserve historical command/evidence records as executed. `rtk llm-proxy` is a separate provider-API proxy and is not the shell-command wrapper. The removed `--ultra-compact` option must not be used.

`rtk make <target>` remains supported by RTK's built-in Make filter; do not replace every filtered invocation with `bypass`. Commands without a matching filter can pass through unchanged, so an RTK prefix alone does not prove output compression.

Do not silently drop the RTK layer merely because the underlying native command is known, appears harmless, or is read-only.

Do not invent RTK subcommands, flags, environment semantics, or wrapper behavior. When the exact RTK invocation for a command class is not established by the current installation/configuration, inspect the available RTK help/configuration or existing known-good usage first.

## Native Codex hook schema

The verified upstream reference for this integration is [RTK v1.0.1](https://github.com/rtk-ai/rtk/releases/tag/v1.0.1). The versioned `.codex/hooks.json` uses the project-local schema produced by `rtk init --codex`:

- event: `hooks.PreToolUse`;
- matcher: `Bash`;
- command handler: `type = "command"`, `command = "rtk hook codex"`.

Codex presents shell commands, including its unified `exec_command` path, to this hook as `Bash`. The hook reads `tool_input.command` and a supported `permission_mode` from stdin JSON. A successful rewrite returns `hookSpecificOutput` with `hookEventName = "PreToolUse"`, `permissionDecision = "allow"`, and `updatedInput.command`. Other `tool_input` fields are preserved. `updatedInput` belongs in the hook response, not in `.codex/hooks.json`; do not substitute another agent's response schema.

This repository keeps its execution instructions in this policy. Do not blindly run mutating `rtk init --codex` over the control plane: it also creates `RTK.md` and appends `@RTK.md` to `AGENTS.md`. Preview upstream setup with `rtk init --codex --dry-run`, preserve existing independent hooks, and keep one RTK registration per active configuration layer. Do not duplicate this JSON registration as inline hooks in the same layer's `config.toml`.

### Host activation and verification

1. Confirm the intended `rtk-ai/rtk` executable is available on the Codex process's `PATH` with `rtk --version` and `rtk hook codex --help`.
2. Use a Codex version supporting native `PreToolUse` command rewriting. Current Codex enables hooks by default; an explicit local/admin disable remains authoritative. Do not overwrite local `config.toml`, managed settings, or sandbox permissions to activate RTK.
3. In Codex, review the trusted project configuration and the exact RTK hook through `/hooks`. New or changed non-managed hooks are skipped until trusted. Hook trust is host-local and is not granted by committing this file.
4. Confirm that the active hook rewrites a supported command such as `git status` to `rtk git status`. A valid JSON file alone does not prove activation in a running session.

The native hook fails open for unsupported commands, unsupported/missing permission modes, malformed input, and shell constructs it cannot safely rewrite. It also leaves already RTK-prefixed commands alone. An empty hook response is not proof of RTK execution. Where interception is unavailable or a command is not rewritten, explicitly use the applicable `rtk <command>` or `rtk bypass <command>` invocation to retain the mandatory execution path. Do not prepend RTK repeatedly or turn a compound shell command into a differently interpreted argument string.

Codex requires the hook's `permissionDecision = "allow"` to apply `updatedInput`; its normal command approvals and sandbox checks still apply to the rewritten command. The command safety classifier may classify the wrapped command differently because it does not unwrap RTK. This protocol field never substitutes for the action's required authority.

Upstream contracts: [RTK Codex integration](https://github.com/rtk-ai/rtk/blob/v1.0.1/hooks/codex/README.md), [RTK v1 migration](https://github.com/rtk-ai/rtk/releases/tag/v1.0.0), and [Codex hook configuration, trust, and output schema](https://developers.openai.com/codex/hooks).

## RTK configuration boundaries

`.codex/hooks.json` registers the Codex hook; RTK's own `config.toml`, custom `filters.toml`, and optional `pipeline.toml` are separate formats. This repository uses the upstream command filters and does not require a custom pipeline or provider-API proxy for this integration.

If a task explicitly introduces project-local `.rtk/filters.toml`, use the [v1 filter schema](https://github.com/rtk-ai/rtk/blob/v1.0.1/src/core/toml_filter.rs): root `schema_version = 1`, named `[filters.<name>]` tables, and anchored `match_command` patterns. Validate the actual filters with `rtk verify`; review their content before `rtk trust`, and re-review changed content. Filter trust is separate from Codex hook trust. Do not create or trust custom filters merely to enable the native hook.

## Scope

The RTK requirement applies to local project command execution including, when applicable:

- Git inspection and authorized Git actions;
- Make and repository-native build/test targets;
- compiler, language-tool, and static-analysis commands;
- project Python/Go/Shell command entry points;
- local runtime and diagnostic commands;
- local scanner/helper commands;
- cleanup commands already authorized by their owning policy.

Non-shell connector/plugin/API actions are governed by their own interface and are not converted into fictional RTK shell commands.

## Authority does not expand through RTK

RTK is an execution wrapper, not an authorization source.

RTK never grants permission to:

- install or update packages;
- change system services or global configuration;
- write outside the current task/repository/storage authority;
- perform a Git write that the Git policy does not allow;
- commit, push, create/update a PR, merge, release, or deploy without the corresponding authority;
- bypass Framework or MRTS repository boundaries;
- expose or inject credentials;
- weaken tests, scanners, warnings, branch protection, or quality gates.

The owning domain policy remains authoritative for the action itself.

## Tool-specific wrappers

When another mandatory wrapper also applies, **both boundaries remain active**.

For SonarQube, the authentication/environment owner is `sonarqube-policy.md` and the required local launcher is `/usr/local/bin/sonar-with-env`. RTK must not bypass that launcher, and the Sonar launcher must not bypass the RTK execution requirement.

Do not invent the combined wrapper syntax. Determine the supported composition from the current RTK and Sonar wrapper interfaces before first use.

The same rule applies to any future task-specific authentication, sandbox, or provenance wrapper: command execution and tool authentication are separate controls and neither substitutes for the other.

## Environment and secret handling

RTK use does not permit environment dumping or secret discovery. Follow the active shell-environment and security policies.

Do not place secret values in:

- command arguments;
- logs or evidence records;
- wrapper configuration;
- task plans;
- reports.

Record only the minimum command/evidence needed to reproduce or explain the action.

## Failure and fallback behavior

If RTK is required but unavailable, invalid, or incompatible with the required command path:

1. inspect the installed RTK path/interface and current project configuration;
2. diagnose the actual failure;
3. use the task's normal feasibility/status model;
4. do **not** silently fall back to the unwrapped command.

If a higher-priority current instruction explicitly conflicts with the repository RTK requirement, treat it as an instruction conflict under `policy-precedence.md` and `task-workflow.md`; do not silently choose one interpretation.

## Evidence

When command evidence is required, record the actual wrapped command/procedure, working directory, relevant scope, exit status, and limitation. Do not rewrite an RTK-wrapped action in the report as though a different direct command had been executed.
