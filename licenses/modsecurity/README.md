# ModSecurity engine origin references

**Language:** English | [Deutsch](README.de.md)

The ModSecurity engine entries in this directory are provenance/reference
information only. This directory does not contain a copied ModSecurity engine
source tree.

## Reference basis

| Engine reference | Upstream | Branch | Commit | Observed version | Observed upstream license |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | https://github.com/owasp-modsecurity/ModSecurity | `v2/master` | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Apache License 2.0 |
| ModSecurity v3 | https://github.com/owasp-modsecurity/ModSecurity | `v3/master` | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Apache License 2.0 |

## Relationship to this repository

ModSecurity v3 is the primary libmodsecurity API/architecture reference used by
the connector project. ModSecurity v2 is retained as a compatibility,
regression, semantic, and historical reference.

The referenced engine source is external to this repository. The fact that the
referenced upstream versions contain an Apache License 2.0 `LICENSE` file does
not make that license a repository-wide license declaration for this project.

Connector code and other files in this repository have their own provenance.
Where imported or derived source is present, use its connector origin/source
map to determine the relevant source basis.
