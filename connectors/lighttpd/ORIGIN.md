# lighttpd Connector Origin

Status: repository-owned native module; `minimal_runtime_smoke`

No upstream connector implementation is imported into this directory. The
module, mapper, build scripts, and native harness are repository-owned source.

The host ABI is compiled against the pinned lighttpd 1.4.84 release source and
its generated `config.h`. The test framework downloads/builds that release in a
managed component cache; the upstream source and generated headers are not
committed into this connector tree. The module links against a locally managed
libmodsecurity installation.

| Item | Value |
| --- | --- |
| Connector source | repository-owned files under `connectors/lighttpd/` |
| Upstream connector source imported | none |
| Host source | lighttpd 1.4.84 release tarball |
| Host source URL | `https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.84.tar.xz` |
| Host commit | release tarball; no Git commit selected |
| Generated host ABI input | lighttpd build-tree `config.h` |
| Native output | `mod_msconnector.so` |
| Runtime status | `minimal_runtime_smoke` for the Phase-1 header path |

The committed connector source does not copy lighttpd implementation code or
headers. Public host API references are listed in `docs/public-sources.md`.
Any future source import must update this file, `SOURCE_MAP.json`, and the
repository-level attribution before a broader claim is made.
