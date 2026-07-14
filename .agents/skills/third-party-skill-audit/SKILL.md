---
name: third-party-skill-audit
description: Audit a proposed Codex skill, plugin, or MCP integration before installation, activation, or vendoring.
---

# Audit a third-party extension

Use this repository-authored adapter before introducing or updating an external
Codex skill, plugin, MCP server, tool, or marketplace source.

## Trigger conditions

- The user asks to add, update, enable, or review a third-party Codex
  extension.
- A skill/plugin/MCP source has scripts, dependencies, network calls, secrets,
  data egress, write capabilities, or paid-service behavior.
- A lock manifest entry needs an evidence-backed status or re-review.

## Do not use when

- The change is solely a repository-authored skill with no external content or
  runtime integration beyond normal documentation review.
- A full product security scan is requested; use the repository security
  workflow instead of conflating extension provenance with code scanning.
- The source cannot be resolved to an immutable revision; report it blocked
  rather than continuing installation.

## Local procedure

1. Resolve an official source URL, immutable commit or package version,
   path-level license, maintainer/version, and update mechanism.
2. Inspect manifests, scripts, dependencies, network destinations, local file
   and process effects, credential handling, data egress, costs, write
   capabilities, and supported tool filtering.
3. Analyze trigger and negative-trigger overlap against existing local skills,
   installed plugins, and system/user/repository policies. Compare the result
   with security, storage, delivery, and privacy rules. Do not run an
   unreviewed extension.
4. Record a precise status in `ci/tooling/codex-extensions.lock.yml` and
   document approvals, boundaries, omissions, revalidation requirements, and a
   deinstallation or recovery path.
5. Add deterministic contract tests for provenance, secret absence, relative
   links, routing declarations, and unsafe automation rejection.

## Safety boundary

No extension is safe merely because it is popular, listed in a marketplace, or
has a familiar name. Never place a secret in a repository file, enable a paid
service without authorization, or claim tool filtering that the client cannot
enforce.

## Provenance

Repository-authored. The discovery-only source is recorded in
[UPSTREAM.md](UPSTREAM.md); no third-party audit text, scripts, or dependencies
are imported.
