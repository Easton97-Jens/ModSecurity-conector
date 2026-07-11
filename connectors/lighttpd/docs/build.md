# lighttpd Build

Status: native module compile/link verified; patched-host target builds a
matched lighttpd 1.4.84 core and module below an isolated build root

## Inputs

`build/build_module.sh` requires absolute paths:

- `LIGHTTPD_SOURCE_DIR`: pinned lighttpd source root containing `src/plugin.h`;
- `MODSECURITY_INCLUDE_DIR`: prefix containing `modsecurity/modsecurity.h`;
- `MODSECURITY_LIB_DIR`: directory containing `libmodsecurity.so`.

The exact lighttpd ABI version comes from a generated `config.h`. The script
searches `LIGHTTPD_CONFIG_DIR`, `LIGHTTPD_BUILD_DIR`,
`LIGHTTPD_BUILD_ROOT`, and the source tree in that order. It does not invent a
`LIGHTTPD_VERSION_ID` from a filename.

All artifacts are written below an absolute `BUILD_ROOT` outside the checkout.
The module defaults to:

```text
$BUILD_ROOT/lighttpd-connector/modules/mod_msconnector.so
```

`LIGHTTPD_MODULE_DIR` can select another absolute managed output directory.

## Native build

```sh
make -C connectors/lighttpd build-lighttpd-connector
```

The script compiles every `common/src/*.c`,
`common/runtime/msconnector_runtime.c`, the lighttpd mapper, and the module as
PIC, then links them into the shared object with libmodsecurity. Required C
flags include:

```text
-std=c17 -fPIC -Wall -Wextra -Werror
```

The host-specific objects additionally use the pinned source headers,
generated `config.h`, and `MSCONNECTOR_LIGHTTPD_HOST_API`. Unresolved lighttpd
host symbols in the shared object are intentional and resolve when lighttpd
loads the module.

The build is compile/link only. It never loads or executes the resulting
module.

## Patched 1.4.84 core and matched module

Stock mode remains the default and continues to compile only against an
unmodified lighttpd ABI:

```sh
make -C connectors/lighttpd build-lighttpd-connector
```

The repository carries a versioned 1.4.84 patch for a local streaming-hook
ABI. It never edits the supplied source tree. `build-lighttpd-patched-core`
copies the source into `BUILD_ROOT/lighttpd-core-patched/lighttpd-1.4.84`,
records the patch SHA-256, configures an out-of-source build, runs `make` and
`make install`, and stages the binary below `stage/bin/lighttpd`.

```sh
make -C connectors/lighttpd check-lighttpd-core-patch
make -C connectors/lighttpd apply-lighttpd-core-patch
make -C connectors/lighttpd build-lighttpd-patched-core
make -C connectors/lighttpd build-lighttpd-patched-host
make -C connectors/lighttpd check-lighttpd-patched-host
```

The matched-host build invokes `build_module.sh` with the generated `config.h`,
the copied patched headers, and `LIGHTTPD_MSCONNECTOR_CORE_MODE=patched`, then
stages `mod_msconnector.so` in `stage/modules`. The core and host manifests
contain the patch SHA-256 and binary/module SHA-256 values. The check target
requires the staged binary to report 1.4.84, verifies both hook symbols with
`nm -D`, and performs a real `lighttpd -tt` module load from the isolated
module directory.

The ABI tag rejects accidental stock/patched dynamic-module mixing. The patch
exposes HTTP/1.x request ranges and bounded pre-socket-write HTTP/1.x output/EOS
ranges; the latter are wire output, not decoded response entities. HTTP/2 is
deliberately excluded because its connection queue is multiplexed and framed.
Consequently this target is a patched-host build/load path and does not establish
response-body, Phase-4, or late-intervention evidence.

## Separate operations

```sh
make -C connectors/lighttpd build-lighttpd-bridge
make -C connectors/lighttpd self-test-lighttpd-bridge
make -C connectors/lighttpd build-lighttpd-connector
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd
```

- Bridge build only compiles the historical bridge binary.
- Bridge self-test explicitly executes that binary with `--self-test`.
- Native build only compiles and links.
- Config check runs the real `LIGHTTPD_BIN -tt` and loads the real module.
- Start smoke starts and stops lighttpd without network requests.
- Runtime smoke alone sends two real host requests.

`runtime-smoke-lighttpd-patched` is a separate, isolated Phase-1 smoke. It
loads only the staged patched module, enforces `request_body_mode=none` and
`response_body_mode=none`, and checks baseline 200 plus rule-backed 403. It
never invokes the generic No-CRS selected-case consumer and its PASS output
states `phase4=not-executed`.

## Verified local result

Using the framework-managed lighttpd 1.4.84 build and local libmodsecurity, the
native module compiled and linked with C17 and `-Werror`; the loader accepted
its ABI and configuration. This establishes link/config-load evidence for the
pinned build only, not portability across arbitrary lighttpd releases.

## Unverified build/runtime scope

No build result establishes body processing, CRS completeness, production
hardening, security verification, or full-matrix compatibility. C23 and newer
standards may be checked as optional repository compile lanes, but C17 is the
required module standard.
