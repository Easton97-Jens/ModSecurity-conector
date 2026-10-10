# Third-party origin and license references

**Language:** English | [Deutsch](README.de.md)

This directory documents where selected external material in this repository
comes from and which upstream license information was observed for that
material.

It is **not** a repository-wide license declaration. The repository contains
upstream-derived connector code, repository-authored code, local adaptations,
documentation, tests, CI support, examples, and generated material. Those
categories do not all have the same origin.

## Origin overview

| Component | Upstream | Reference basis | Relationship to this repository | Upstream license reference |
| --- | --- | --- | --- | --- |
| Apache connector | https://github.com/owasp-modsecurity/ModSecurity-apache | `master` at `0488c77f69669584324b70460614a382224b4883` (`v0.0.9-beta1-26-g0488c77`) | Parts of the local Apache connector are imported or derived from this upstream and have repository-local changes. | Upstream Apache-2.0 `LICENSE`, retained under `licenses/apache/` |
| NGINX connector | https://github.com/owasp-modsecurity/ModSecurity-nginx | `master` at `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` (`v1.0.4-14-g9eb44fd`) | Parts of the local NGINX connector are imported or derived from this upstream and have additional upstream-derived and repository-local changes recorded in its source map. | Upstream Apache-2.0 `LICENSE`, retained under `licenses/nginx/` |
| ModSecurity v2 | https://github.com/owasp-modsecurity/ModSecurity | `v2/master` at `02eed22d74667b32091eece088a8ebdf64b6ba67` (`v2.9.13`) | Read-only engine reference; engine source is not copied into this repository by this reference directory. | Apache License 2.0 observed at the referenced upstream source |
| ModSecurity v3 | https://github.com/owasp-modsecurity/ModSecurity | `v3/master` at `0fb4aff98b4980cf6426697d5605c424e3d5bb60` (`v3.0.15`) | Primary libmodsecurity API/architecture reference; engine source is not copied into this repository by this reference directory. | Apache License 2.0 observed at the referenced upstream source |

## Important boundary

The files under `licenses/apache/` and `licenses/nginx/` preserve upstream
license, author, and change information for the upstream material used as a
source basis.

The local connector trees are **not identical copies** of those upstream
repositories. They contain repository-local adaptations and, in some cases,
additional upstream-derived changes. The per-file provenance is recorded in:

- `connectors/apache/SOURCE_MAP.json`
- `connectors/nginx/SOURCE_MAP.json`

Files elsewhere in this repository must not be assumed to originate from these
upstreams or to be covered by these upstream license copies merely because
they are stored in the same repository.

There is no top-level `LICENSE` file in the repository at this revision.
Use the relevant origin/source map and file-level information when determining
where a particular file came from.
