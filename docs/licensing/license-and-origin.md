# License And Origin

Status: implemented

This repository contains controlled imports of Apache-2.0 licensed connector
code. The imported source files remain connector-specific and are documented in:

- `connectors/apache/ORIGIN.md`
- `connectors/nginx/ORIGIN.md`

The central attribution index is stored under `licenses/`. It mirrors the
upstream license and attribution files for quick review, but it does not replace
the upstream-adjacent copies in `connectors/*/upstream/`.

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

Central attribution copies:

- `licenses/apache/LICENSE`
- `licenses/apache/AUTHORS`
- `licenses/apache/CHANGES`
- `licenses/apache/ORIGIN.md`

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

Central attribution copies:

- `licenses/nginx/LICENSE`
- `licenses/nginx/AUTHORS`
- `licenses/nginx/CHANGES`
- `licenses/nginx/ORIGIN.md`

## ModSecurity Engine References

ModSecurity v2 and v3 are read-only reference repositories, not imported engine
source trees. Their observed local revisions and license observation are
documented in `licenses/modsecurity/README.md`.

## Rules

- Do not import upstream `.git` directories or generated build artifacts.
- Do not claim imported code works unless the smoke harness builds and runs it.
- Do not move code into `common/` without a separate proof and review step.
- Keep origin maps updated whenever imported files are added, removed, or
  refreshed from upstream.
- Keep `licenses/` synchronized with imported source origins and license files.

## Pruning Review

The current imported connector trees were reviewed in
`docs/upstream-pruning-analysis.md` and summarized in
`docs/minimal-upstream-file-set.md`.

No imported files were removed in that review. The remaining Apache and NGINX
files are classified as required, build-only, or documentation-only. A future
removal must be documented in the relevant `ORIGIN.md`, retain license and
attribution coverage, and pass an isolated `$BUILD_ROOT` build/smoke probe
before being committed.
