# License And Origin

Status: implemented

This repository contains controlled imports of Apache-2.0 licensed connector
code. The imported source files remain connector-specific and are documented in:

- `connectors/apache/ORIGIN.md`
- `connectors/nginx/ORIGIN.md`

## Apache Connector

Source repository: `/root/conecter/ModSecurity-apache`

Observed source revision:

- branch: `master`
- commit: `0488c77f69669584324b70460614a382224b4883`
- describe: `v0.0.9-beta1-26-g0488c77`
- license: Apache License 2.0

The upstream `LICENSE` file is imported into
`connectors/apache/upstream/LICENSE`. Source and build files are copied only
into the Apache-specific `upstream/` area.

## NGINX Connector

Source repository: `/root/conecter/ModSecurity-nginx`

Observed source revision:

- branch: `master`
- commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
- describe: `v1.0.4-14-g9eb44fd`
- license: Apache License 2.0

The upstream `LICENSE` file is imported into
`connectors/nginx/upstream/LICENSE`. Source and build files are copied only into
the NGINX-specific `upstream/` area.

## Rules

- Do not import upstream `.git` directories or generated build artifacts.
- Do not claim imported code works unless the smoke harness builds and runs it.
- Do not move code into `common/` without a separate proof and review step.
- Keep origin maps updated whenever imported files are added, removed, or
  refreshed from upstream.

## Pruning Review

The current imported connector trees were reviewed in
`docs/upstream-pruning-analysis.md` and summarized in
`docs/minimal-upstream-file-set.md`.

No imported files were removed in that review. The remaining Apache and NGINX
files are classified as required, build-only, or documentation-only. A future
removal must be documented in the relevant `ORIGIN.md`, retain license and
attribution coverage, and pass an isolated `$BUILD_ROOT` build/smoke probe
before being committed.
