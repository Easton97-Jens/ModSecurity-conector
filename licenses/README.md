# Central License And Attribution Index

Status: implemented

This directory is a central index for third-party source attribution in this
repository. It preserves durable attribution even after an imported upstream
reference tree is reduced or removed.

## Included Source Imports

| Area | Local reference | Upstream | Imported code in repo | License | Details |
| --- | --- | --- | --- | --- | --- |
| Apache connector | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `connectors/apache/src/` with attribution in `licenses/apache/` and `connectors/apache/src/SOURCE_MAP.json` | Apache-2.0 | `licenses/apache/ORIGIN.md` |
| NGINX connector | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `connectors/nginx/src/` with attribution in `licenses/nginx/` and `connectors/nginx/src/SOURCE_MAP.json` | Apache-2.0 | `licenses/nginx/ORIGIN.md` |

## Read-only Reference Sources

| Area | Local reference | Upstream | Imported code in repo | License note | Details |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `/root/conecter/ModSecurity_V2` | https://github.com/owasp-modsecurity/ModSecurity | none | Apache-2.0 observed in source | `licenses/modsecurity/README.md` |
| ModSecurity v3 | `/root/conecter/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | none | Apache-2.0 observed in source | `licenses/modsecurity/README.md` |

## Rules

- Keep the original `LICENSE`, `AUTHORS`, and `CHANGES` files in this central
  attribution tree. For connector imports that still retain upstream source
  trees, keep upstream-adjacent copies when required by the import plan.
- Update this directory when imported source files are refreshed, removed, or
  added.
- Do not copy build artifacts, generated runtime files, or external repository
  metadata into this directory.
