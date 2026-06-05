# lighttpd Build

Status: bridge-starter
Runtime status: not-verified

A repository-owned decision-service bridge starter is implemented. It
compile-checks local bridge-starter source against connector-neutral `common/`
headers only.

## Commands

```sh
make -C connectors/lighttpd build-starter
make -C connectors/lighttpd self-test
make -C connectors/lighttpd build-bridge-starter
make -C connectors/lighttpd self-test-bridge
```

Equivalent scripts:

```sh
connectors/lighttpd/build/build_starter.sh
connectors/lighttpd/build/bridge_starter.sh
```

Default output paths:

```text
$BUILD_ROOT/lighttpd-build-starter/
$BUILD_ROOT/lighttpd-bridge-starter/
```

Expected bridge-starter artifacts:

- `$BUILD_ROOT/lighttpd-bridge-starter/lighttpd-bridge-starter`
- `$BUILD_ROOT/lighttpd-bridge-starter/self-test.txt`

## What These Builds Prove

The starter builds prove only that these repository-owned files compile and pass
local self-tests with shared common helpers:

- `connectors/lighttpd/metadata.c`
- `connectors/lighttpd/metadata.h`
- `connectors/lighttpd/src/lighttpd_build_starter.c`
- `connectors/lighttpd/src/lighttpd_bridge.h`
- `connectors/lighttpd/src/lighttpd_bridge.c`
- `connectors/lighttpd/src/lighttpd_bridge_main.c`
- `common/include/msconnector/capabilities.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/origin.h`
- `common/include/msconnector/request.h`
- `common/include/msconnector/status.h`
- `common/src/capabilities.c`
- `common/src/intervention.c`
- `common/src/origin.c`
- `common/src/status.c`

## What These Builds Do Not Prove

The starters are not:

- a lighttpd native module build;
- a FastCGI protocol implementation;
- an SCGI protocol implementation;
- a real external service deployment;
- a ModSecurity API integration build;
- a runtime harness;
- a No-CRS, With-CRS, or RESPONSE_BODY validation.

## Blocked Real Build Dependencies

A real lighttpd adapter build is blocked until at least one selected production
integration path has repository-backed dependencies:

- lighttpd headers/SDK/source tree for a native module path, or documented
  bridge dependencies for a FastCGI/SCGI/external-service path;
- build flags and include/library paths for the selected path;
- ModSecurity integration code using real APIs;
- artifact path for the selected adapter or bridge;
- build log path and reproducible command.

No lighttpd-specific include path or library path is currently documented
because no lighttpd build dependency has been selected or imported.

## Last Local Starter Checks

Commands executed in this repository workspace:

```sh
connectors/lighttpd/build/build_starter.sh
make -C connectors/lighttpd build-bridge-starter
make -C connectors/lighttpd self-test-bridge
```

Result: PASS for metadata/probe and bridge-starter compile/self-test checks
only. The bridge self-test reports the probe decision as `blocked` because no
lighttpd runtime hook, FastCGI/SCGI protocol adapter, or libmodsecurity
integration exists.
