# lighttpd Build

Status: native module compile/link verified against pinned lighttpd 1.4.84

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
