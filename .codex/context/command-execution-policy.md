# Command Execution and RTK Policy

## Purpose and ownership

This file is the primary owner for local shell-command execution and RTK use in the Parent control plane.

It defines **how** an authorized command is invoked. It does not grant repository writes, network access, package installation, service changes, Git delivery, merge authority, SonarQube authentication, or any other material action that is not already authorized by the current task and its owning policy.

## Mandatory RTK execution path

RTK is the mandatory local execution proxy for project commands issued through the shell.

A request to use a repository-native command directly means using that native command **through RTK**. Examples:

```text
rtk git status
rtk make quick-check
rtk make build-nginx
```

Do not silently drop the RTK layer merely because the underlying native command is known, appears harmless, or is read-only.

Do not invent RTK subcommands, flags, environment semantics, or wrapper behavior. When the exact RTK invocation for a command class is not established by the current installation/configuration, inspect the available RTK help/configuration or existing known-good usage first.

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
