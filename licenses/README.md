# Central License And Attribution Index

Status: implemented

This directory is a central index for third-party source attribution in this
repository. It does not replace license and attribution files that must remain
beside imported upstream source trees.

## Included Source Imports

| Area | Local reference | Upstream | Imported code in repo | License | Details |
| --- | --- | --- | --- | --- | --- |
| Apache connector | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `connectors/apache/upstream/` | Apache-2.0 | `licenses/apache/ORIGIN.md` |
| NGINX connector | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `connectors/nginx/upstream/` | Apache-2.0 | `licenses/nginx/ORIGIN.md` |

## Read-only Reference Sources

| Area | Local reference | Upstream | Imported code in repo | License note | Details |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `/root/conecter/ModSecurity_V2` | https://github.com/owasp-modsecurity/ModSecurity | none | Apache-2.0 observed in source | `licenses/modsecurity/README.md` |
| ModSecurity v3 | `/root/conecter/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | none | Apache-2.0 observed in source | `licenses/modsecurity/README.md` |

## Rules

- Keep the original `LICENSE`, `AUTHORS`, and `CHANGES` files in
  `connectors/*/upstream/` when they belong to imported source code.
- Update this directory when imported source files are refreshed, removed, or
  added.
- Do not copy build artifacts, generated runtime files, or external repository
  metadata into this directory.
