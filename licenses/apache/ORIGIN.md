# Apache Connector License Origin

Status: implemented

This directory mirrors the upstream license and attribution files for the
controlled Apache connector source import. Phase 11 migrated the active build
source into `connectors/apache/src/` and removed the former
`connectors/apache/upstream/` reference tree after a materialized Apache build
and smoke run passed. Phase 12 removed duplicate attribution/history files from
the active source tree; this directory is now the durable home for those files.

Local reference: `/root/conecter/ModSecurity-apache`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-apache
Source branch: `master`
Source commit: `0488c77f69669584324b70460614a382224b4883`
Source describe: `v0.0.9-beta1-26-g0488c77`
License: Apache-2.0

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-apache | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

## Files

| Central path | Source path | Purpose |
| --- | --- | --- |
| `licenses/apache/LICENSE` | Upstream `LICENSE` | Apache-2.0 license text for adapter-owned Apache connector source |
| `licenses/apache/AUTHORS` | Upstream `AUTHORS` | Upstream attribution |
| `licenses/apache/CHANGES` | Upstream `CHANGES` | Upstream change context |

## Imported Source Map

The full file-by-file source map remains in
`connectors/apache/ORIGIN.md` and `connectors/apache/SOURCE_MAP.json`.
This central license directory is an attribution index and does not replace the
functional Apache source files required by the adapter-owned Apache Autotools
source tree.
