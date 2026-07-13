# lighttpd Connector Origin

**Language:** English | [Deutsch](ORIGIN.de.md)

Status: repository-owned native module; stock `minimal_runtime_smoke` plus a
non-promoted patched-host full-lifecycle probe

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
| Runtime status | stock `minimal_runtime_smoke` plus a full-lifecycle-selected patched Phase-1 host probe |

The full-lifecycle profile selects `patched-native` through
`full-lifecycle-lighttpd-patched`. That target creates a copied 1.4.84 source
tree, out-of-source core build, staged binary and staged ABI-matched module
below the managed build root. It records the local patch SHA-256 and
binary/module hashes before a real `lighttpd -tt` load. This is still only a
narrow Phase-1 build/load/runtime path: the host smoke uses both body modes as
`none`. The patch's response callback receives a borrowed HTTP/1.1 identity
entity range before transfer framing rather than socket-wire output, but that
source/build contract remains non-promoted without a streaming host run.

The committed connector source does not copy lighttpd implementation code or
headers. Public host API and build boundaries are summarized in the
[canonical lighttpd guide](../../docs/connectors/lighttpd.md). Any future
source import must update this file, `SOURCE_MAP.json`, and the
repository-level attribution before a broader claim is made.
