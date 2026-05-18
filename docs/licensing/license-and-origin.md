# License And Origin

Status: implemented

This repository contains controlled imports of Apache-2.0 licensed connector
code. The imported source files remain connector-specific and are documented in:

- `connectors/apache/ORIGIN.md`
- `connectors/nginx/ORIGIN.md`

The central attribution index is stored under `licenses/`. It mirrors the
upstream license and attribution files for quick review. Apache and NGINX now
build from adapter-owned source trees; their former local `upstream/` reference
trees have been removed after materialized builds and real-world smoke proof.

## Apache Connector

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-apache | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

Observed source revision:

- branch: `master`
- commit: `0488c77f69669584324b70460614a382224b4883`
- describe: `v0.0.9-beta1-26-g0488c77`
- license: Apache License 2.0

The upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are retained in
`licenses/apache/`. Apache source and Autotools/APXS build inputs are
adapter-owned under `connectors/apache/src`, with source provenance recorded in
`connectors/apache/src/SOURCE_MAP.json` and `connectors/apache/ORIGIN.md`. The
former `connectors/apache/upstream/` tree was removed in phase 11.

Central attribution copies:

- `licenses/apache/LICENSE`
- `licenses/apache/AUTHORS`
- `licenses/apache/CHANGES`
- `licenses/apache/ORIGIN.md`

## NGINX Connector

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Observed source revision:

- branch: `master`
- commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
- describe: `v1.0.4-14-g9eb44fd`
- license: Apache License 2.0

The upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are retained in
`licenses/nginx/`. The NGINX module `config` and source files are adapter-owned
under `connectors/nginx/src`, with source provenance recorded in
`connectors/nginx/src/SOURCE_MAP.json` and `connectors/nginx/ORIGIN.md`. The
former `connectors/nginx/upstream/` tree was removed in phase 10.

ModSecurity-nginx PR #377
(https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377) source
changes at commit `3d72b004ff27a78ea19c6b945870e2cae62a97ac` are recorded for
the adapter-owned phase-4 files. This does not promote `RESPONSE_BODY` to a
verified variable.

Central attribution copies:

- `licenses/nginx/LICENSE`
- `licenses/nginx/AUTHORS`
- `licenses/nginx/CHANGES`
- `licenses/nginx/ORIGIN.md`

## ModSecurity Engine References

ModSecurity v2 and v3 are read-only reference repositories, not imported engine
source trees. Their observed local revisions and license observation are
documented in `licenses/modsecurity/README.md`.

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `/root/conecter/ModSecurity_V2` | https://github.com/owasp-modsecurity/ModSecurity | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Apache-2.0 |
| ModSecurity v3 | `/root/conecter/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Apache-2.0 |

## Rules

- Do not import upstream `.git` directories or generated build artifacts.
- Do not claim imported code works unless the smoke harness builds and runs it.
- Do not move code into `common/` without a separate proof and review step.
- Keep origin maps updated whenever imported files are added, removed, or
  refreshed from upstream.
- Keep `licenses/` synchronized with imported source origins and license files.
- Do not remove adapter-owned source files for cosmetic cleanup; reduce only
  after replacement, retained attribution, and passing smoke evidence. Apache
  and NGINX no longer keep local `upstream/` trees; durable attribution lives
  under `licenses/apache/` and `licenses/nginx/`.

## Pruning Review

The current imported connector trees were reviewed in
`docs/imports/upstream-pruning-analysis.md` and summarized in
`docs/imports/minimal-upstream-file-set.md`.

Later replace-and-reduce phases removed the imported NGINX debug helper,
migrated NGINX `config`/`src/*` into adapter-owned source, and then removed the
remaining NGINX upstream reference tree after smoke proof. Phase 11 migrated
Apache source, Autotools/APXS inputs, and required `.in` templates into
`connectors/apache/src`, proved a materialized build and smoke run, and removed
the former Apache upstream tree. Any future reduction must be documented in the
relevant `ORIGIN.md`, retain license and attribution coverage, and pass an
isolated `$BUILD_ROOT` build/smoke probe before being committed.
