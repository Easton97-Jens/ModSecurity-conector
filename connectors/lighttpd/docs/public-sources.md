# lighttpd Public Sources

**Language:** English | [Deutsch](public-sources.de.md)

Status: host API references for a repository-owned native module
Runtime status: `minimal_runtime_smoke` for the pinned Phase-1 header path

These public sources identify the host API and project used for the pinned
native-module build. No upstream connector implementation or lighttpd source is
copied into this connector directory.

- https://raw.githubusercontent.com/lighttpd/lighttpd1.4/master/src/plugin.h
- https://github.com/lighttpd/lighttpd1.4
- https://redmine.lighttpd.net/projects/1/wiki/Docs_ModMagnet

The full-lifecycle profile separately selects a copied, patched 1.4.84 host
through `full-lifecycle-lighttpd-patched`. The patch is repository-owned and
the disposable source tree is not an imported connector implementation; its
Phase-1 host route remains non-promoted.

Any future source import must be documented through
`connectors/lighttpd/ORIGIN.md`, `connectors/lighttpd/SOURCE_MAP.json`, and the
global connector gates in
`reports/archive/template-verification-nginx-apache/connector-scaffold-decisions.md`.
