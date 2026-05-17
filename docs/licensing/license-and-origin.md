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

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-apache | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

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

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

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
- Treat `connectors/*/upstream/` as a temporary import/reference basis. Do not
  remove files from it for cosmetic cleanup; remove only after replacement,
  retained attribution, and passing smoke evidence.

## Pruning Review

The current imported connector trees were reviewed in
`docs/imports/upstream-pruning-analysis.md` and summarized in
`docs/imports/minimal-upstream-file-set.md`.

No imported files were removed in that review. The remaining Apache and NGINX
files are classified as required, build-only, or documentation-only. A future
removal must be documented in the relevant `ORIGIN.md`, retain license and
attribution coverage, and pass an isolated `$BUILD_ROOT` build/smoke probe
before being committed.
