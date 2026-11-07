# Sonar Free Access and Cloud Quality Gate Policy

## Purpose and primary ownership

This file owns the Parent's Sonar Free procedure: SSH CLI access, Secrets before
file reads, automatic hook boundaries, explicit project binding, Cloud readback
and Quality-Gate semantics. Other policies delegate these rules here.

## Existing installation and execution boundaries

Use the existing `sonar` command or canonical `/usr/local/bin/sonar-with-env`
starter. Project files, Codex and Git remain on 192.168.189.173; native CLI and
Secrets scanning run through SSH on 192.168.193.59:2222. Consult the installed
`/usr/local/lib/sonar-remote/README.md` for implemented capabilities and blockers.
Do not install a native CLI here or change global installation, hooks, trust,
authentication, SSH keys, firewall or subscriptions as part of project setup.

Before first use, verify the existing starter's executable identity and supported
mode from current documentation and actual execution evidence. A documented
launcher symlink is expected; reject an unexpected substitution. Help/version
output and capabilities establish no successful scan or authentication result.
Never discover credentials or supply them as a replacement for the starter.
Do not store credentials in configuration, arguments, logs or evidence.

For agent-issued local shell commands, retain RTK and the starter together:

```sh
rtk bypass /usr/local/bin/sonar-with-env remote project
rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin < path/to/file > /dev/null 2>&1
```

The installed global Codex Sonar hooks and their scanner children use the direct
starter **without RTK**. This accepted integration boundary does not exempt
agent-issued shell commands from `command-execution-policy.md`. Keep the existing
project RTK `PreToolUse/Bash` hook independent; do not duplicate global Sonar
registrations in project configuration.

## Mandatory Secrets before reading

Before reading file contents, including content searches, explicitly run
`analyze secrets` on the selected file or feed the exact selected bytes to
`analyze secrets --stdin`. Filename-only discovery may precede the scan.
Recheck changed content before reading it again. Keep raw scanner findings and
credentials out of tool output, logs and reports; suppress scanner output and
inspect the actual process exit status.

Continue only after a completed Secrets scan with exit code 0. A finding,
scanner error, unavailable scan or incomplete result stops further file reads
and changes until resolved. Do not read a file with a Secrets finding. Never
convert an error, empty selection or missing output into a successful scan.
A manual successful scan establishes only the selected content's Secrets result.

## Automatic checks and Free-only local use

The existing global `UserPromptSubmit` and `PostToolUse/apply_patch` hooks perform
deterministic Secrets checks only; the latter selects the actually edited files.
Existing Git Secrets checks remain effective. Do not alter global hook
definitions or trust to implement this project policy.

No successful Vortex, STANDARD or DEEP analysis is a prerequisite for continuing
development after a clean Secrets check. Do not automatically invoke aggregate
`sonar analyze`, Vortex/agentic analysis, paid remediation or Advanced-Security/SCA.
Use only available free functions. Sonar MCP remains disabled; do not configure,
activate or use it.

Prior installation reports and manually invoked scanners/handlers do not prove
a new automatic event. A fresh hook claim needs current event/session evidence.
Scanner-child exit 0 does not establish a handler-process exit when that exit
was not recorded.

## Project binding and available Cloud reads

Resolve the current repository's key from its own `.sonar-config.json`
(`project.projectKey`) or `sonar-project.properties` (`sonar.projectKey`).
If both exist they must agree for the selected project. If binding is missing
or ambiguous, ask for the key before project-specific queries; standalone
file/stdin Secrets checks remain possible. Never invent a global project default
or borrow a sibling repository or advisory/native target key.

After resolving the binding, pass that exact key explicitly:

```sh
rtk bypass /usr/local/bin/sonar-with-env list projects
rtk bypass /usr/local/bin/sonar-with-env list issues -p "$SONAR_PROJECT_KEY"
rtk bypass /usr/local/bin/sonar-with-env quality-gate status -p "$SONAR_PROJECT_KEY"
```

Here `SONAR_PROJECT_KEY` denotes the verified current local binding, not a preset
global value. Use read-only `api get` with that same explicit project identity
in the API's project parameter for available metrics, coverage and duplication.
Check current command help/capabilities before constructing an API query; do not
invent endpoint or parameter support.

## Preserve CI analysis and independent PR gates

Cloud queries describe the **last analyzed Cloud revision**, not unchecked local
modifications. A successful Secrets check is not a full code-quality analysis
and does not replace CI or an independently applicable PR Quality Gate.

Fresh complete analysis belongs to the existing suitable CI SonarScanner
workflows within Free-plan limits. Preserve their source scope, independent
projects, supported analyzer modes, secret handling and gate waits. Do not
replace them with Secrets-only checks or launch a local aggregate/agentic scan
to obtain a quality result. CI's existing scanner action and CI-managed
authentication remain their own execution context; do not rewrite CI to use
the local SSH starter or RTK.

## Environment hygiene

Never dump or log the full inherited environment for Sonar diagnosis. Do not print credential variables, authorization headers, cookies, or token-bearing URLs.

When existence must be checked, record only a value-free result such as `present` / `absent`.

Do not enable shell tracing or debug modes that can expose secrets while the Sonar environment is active.

## SonarQube Cloud applicability and exact-revision binding

SonarQube Cloud is required for a PR delivery decision only when the current repository/PR actually exposes an applicable SonarQube Cloud analysis or Quality Gate.

Do not assume that every repository, branch, or task has SonarQube Cloud configured. Determine applicability from current workflow, PR, scanner, and project evidence.

For PR delivery, use only SonarQube results that belong to the **current PR head SHA**. A Quality Gate from an older head is stale evidence.

For a standalone assessment, bind scan inputs and readback to the exact analyzed revision/worktree and record that identity.

## Discovery and readback

Use the current available Sonar sources appropriate to the task, such as:

- current PR checks and their links;
- PR decoration/comments and inline annotations;
- scanner output and server-side analysis identifiers;
- authenticated SonarQube Cloud project/readback interfaces;
- current Quality Gate, issues/hotspots, metrics, coverage, and duplication data.

A successful scanner process or upload does not prove that server-side processing completed or that the Quality Gate passed. Read back the terminal analysis result when the task depends on it.

Where result sets are paginated or split across categories, do not treat a partial readback as complete.

## Finding treatment

Treat SonarQube findings as technical evidence requiring validation, not automatic truth.

At minimum distinguish findings affecting:

- reliability;
- security;
- security hotspots;
- maintainability;
- duplication;
- coverage;
- configuration/analysis failure;
- candidate false positives;
- unrelated baseline findings.

Before treating a finding as task-owned, verify that it applies to the current source/diff/revision and affected execution path.

Security findings and hotspots follow the repository security/finding policies before remediation or disposition.

## Prohibited shortcuts

Without the separate authority and technical basis required by the owning policies, do not:

- disable Sonar rules;
- change a Quality Gate;
- lower coverage thresholds;
- add broad file/directory exclusions;
- add broad suppressions or `NOSONAR` merely to become green;
- mark a finding false positive;
- mark a security hotspot reviewed/safe;
- fabricate a passing analysis when scanner/server processing failed;
- reuse stale analysis for a different SHA.

A narrowly justified source suppression is a code/change decision governed by the normal security/change/documentation policies; this Sonar policy does not authorize it.

## Delivery semantics

When an applicable SonarQube Cloud Quality Gate is required for the current PR, `verified_pr` requires that the terminal gate for the current PR head SHA has passed and that required task-owned findings/feedback have been truthfully resolved or dispositioned under the owning policies.

Pending, failed, cancelled, unknown, inaccessible, or stale required analysis cannot be translated into a pass.

After every follow-up push, resolve the new PR head SHA and evaluate the new Sonar analysis for that head.

## Failure handling

If Sonar access or analysis cannot proceed, retain the normal technical status model and record a precise reason code where useful, for example:

- `sonarqube_wrapper_missing`;
- `sonarqube_wrapper_invalid`;
- `sonarqube_authentication_failed`;
- `sonarqube_project_binding_missing_or_ambiguous`;
- `sonarqube_service_unreachable`;
- `sonarqube_analysis_failed`;
- `sonarqube_readback_incomplete`.

These are reason codes, not alternative success states. Do not fall back to direct credential discovery, raw token injection, or an unwrapped scanner.

## Evidence record

Record only the minimum secret-free Sonar evidence required by the task, such as:

- mechanism used (Secrets/CI scanner/CLI/readback);
- canonical wrapper use;
- repository/project identity;
- branch and exact commit SHA;
- analysis/task identifier when available;
- analyzed scope/languages/exclusions when material;
- terminal Quality-Gate status;
- relevant metrics/findings;
- tool/exit/readback status;
- limitations.

Never record credential values.
