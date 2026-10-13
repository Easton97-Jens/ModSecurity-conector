# Apache connector origin and license reference

**Language:** English | [Deutsch](ORIGIN.de.md)

## Origin

| Field | Reference |
| --- | --- |
| Upstream repository | https://github.com/owasp-modsecurity/ModSecurity-apache |
| Branch | `master` |
| Source basis | `0488c77f69669584324b70460614a382224b4883` |
| Observed version | `v0.0.9-beta1-26-g0488c77` |
| Observed upstream license | Apache-2.0 |

The local Apache connector uses this upstream source as a provenance basis.

## What is retained here

| File | Origin | Purpose |
| --- | --- | --- |
| `licenses/apache/LICENSE` | Upstream `LICENSE` | Preserve the upstream Apache-2.0 license text |
| `licenses/apache/AUTHORS` | Upstream `AUTHORS` | Preserve upstream attribution |
| `licenses/apache/CHANGES` | Upstream `CHANGES` | Preserve upstream change history/context |

## Difference from the local repository

The Apache connector under `connectors/apache/` is not an unchanged checkout
of ModSecurity-apache. It contains imported/derived upstream material together
with repository-local adaptations and repository-authored support files.

The authoritative per-file provenance is
`connectors/apache/SOURCE_MAP.json`. It records which files are based on the
upstream source, which local changes or additional source bases apply, and
which files are repository-authored.

The files in this directory document the upstream origin and upstream license
basis for relevant material. They do not define a license for unrelated files
or for the repository as a whole.
