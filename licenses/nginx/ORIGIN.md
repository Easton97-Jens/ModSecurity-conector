# NGINX connector origin and license reference

**Language:** English | [Deutsch](ORIGIN.de.md)

## Origin

| Field | Reference |
| --- | --- |
| Upstream repository | https://github.com/owasp-modsecurity/ModSecurity-nginx |
| Branch | `master` |
| Source basis | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` |
| Observed version | `v1.0.4-14-g9eb44fd` |
| Observed upstream license | Apache-2.0 |

The local NGINX connector uses this upstream source as its base provenance.
Additional upstream-derived changes and repository-local adaptations are
recorded separately in the source map.

## What is retained here

| File | Origin | Purpose |
| --- | --- | --- |
| `licenses/nginx/LICENSE` | Upstream `LICENSE` | Preserve the upstream Apache-2.0 license text |
| `licenses/nginx/AUTHORS` | Upstream `AUTHORS` | Preserve upstream attribution |
| `licenses/nginx/CHANGES` | Upstream `CHANGES` | Preserve upstream change history/context |

## Difference from the local repository

The NGINX connector under `connectors/nginx/` is not an unchanged checkout of
ModSecurity-nginx. The local tree includes upstream-derived source, selected
additional upstream changes, repository-local hardening/adaptations, and
repository-authored support files.

The authoritative per-file provenance is
`connectors/nginx/SOURCE_MAP.json`. It records the base source and any
additional source/patch provenance for individual files.

The files in this directory document the upstream origin and upstream license
basis for relevant material. They do not define a license for unrelated files
or for the repository as a whole.
