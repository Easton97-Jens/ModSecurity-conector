# SonarQube Local Access and Cloud Quality Gate Policy

## Purpose and primary ownership

This file is the single primary owner for SonarQube local access, authentication/environment setup, SonarScanner/CLI/MCP invocation boundaries, SonarQube Cloud readback, findings, and Quality-Gate semantics.

Other assessment or delivery policies may require SonarQube, but they must reference this file instead of duplicating its authentication or wrapper rules.

## Canonical local authentication path

For every local SonarQube access path, including SonarQube CLI, SonarScanner, SonarQube helpers, local scripts that call Sonar APIs/scanners, and SonarQube MCP, use only:

`/usr/local/bin/sonar-with-env`

Do not provide or set Sonar credentials directly as a replacement for this wrapper.

Do not store Sonar credential values in Codex, MCP, TOML, YAML, JSON, `.env`, command arguments, logs, reports, or task evidence. Do not create another wrapper whose purpose is to bypass `/usr/local/bin/sonar-with-env`.

## Required preflight

Before first use in a task, establish that the wrapper:

1. exists at the canonical path;
2. is a regular executable file;
3. is not an unexpected symlink or path substitution;
4. supports the required real execution mode;
5. can establish the required authentication without printing secrets.

Inspect current wrapper documentation/help or existing known-good local usage before constructing the first invocation. Do not invent wrapper arguments, scanner modes, MCP arguments, project identifiers, or authentication variables.

## RTK composition

Local shell-command execution is governed by `command-execution-policy.md`.

RTK and `/usr/local/bin/sonar-with-env` are separate mandatory controls where both apply:

- RTK governs local shell command execution;
- `/usr/local/bin/sonar-with-env` governs SonarQube authentication/environment preparation.

Neither may bypass the other. Determine the supported combined invocation from the current interfaces; do not invent wrapper ordering or flags.

## CLI and scanner use

Do not launch `sonar-scanner`, another Sonar scanner binary, or a credential-dependent Sonar CLI directly when the wrapper is required.

A tool name does not establish its role. Distinguish scanner, query/administration CLI, helper, and MCP server by current installed behavior/documentation. If a query CLI cannot perform analysis, use the actual configured scanner path through the canonical wrapper rather than assigning fictional scan functionality to the query CLI.

## MCP use

A SonarQube MCP server that requires SonarQube credentials must receive its authentication environment through `/usr/local/bin/sonar-with-env`.

Do not place raw token values in MCP configuration and do not configure a credential-dependent MCP server binary directly in a way that bypasses the wrapper.

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
- `sonarqube_mcp_unavailable`;
- `sonarqube_service_unreachable`;
- `sonarqube_analysis_failed`;
- `sonarqube_readback_incomplete`.

These are reason codes, not alternative success states. Do not fall back to direct credential discovery, raw token injection, or an unwrapped scanner.

## Evidence record

Record only the minimum secret-free Sonar evidence required by the task, such as:

- mechanism used (scanner/CLI/MCP/readback);
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
