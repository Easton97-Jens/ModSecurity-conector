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

The optional patched-host target creates a separate copied 1.4.84 source tree,
out-of-source core build, staged binary and staged ABI-matched module below the
managed build root. It records the local patch SHA-256 and binary/module hashes
before a real `lighttpd -tt` load. This is still only a narrow Phase-1
build/load/runtime path: the patch's response callback observes HTTP/1.x wire
output and is not a decoded response-body integration.

The committed connector source does not copy lighttpd implementation code or
headers. Public host API references are listed in `docs/public-sources.md`.
Any future source import must update this file, `SOURCE_MAP.json`, and the
repository-level attribution before a broader claim is made.
