# lighttpd Build

Status: bridge-starter plus pinned local lighttpd build
Runtime status: locally verifiable with a staged lighttpd binary

A repository-owned decision-service bridge starter is implemented. It
compile-checks local bridge-starter source against connector-neutral `common/`
headers only.

The upstream lighttpd runtime component is pinned in `common.sh` and can be
staged locally from the verified source tarball. Source download requires
`ALLOW_RUNTIME_DOWNLOADS=1`; the local build requires `ALLOW_RUNTIME_BUILDS=1`.
Both steps write only under common.sh-managed runtime/component paths.

## Commands

```sh
make -C connectors/lighttpd build-starter
make -C connectors/lighttpd self-test
make -C connectors/lighttpd build-bridge-starter
make -C connectors/lighttpd self-test-bridge
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-lighttpd-runtime
ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
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
$CONNECTOR_COMPONENT_CACHE/lighttpd/
```

Expected bridge-starter artifacts:

- `$BUILD_ROOT/lighttpd-bridge-starter/lighttpd-bridge-starter`
- `$BUILD_ROOT/lighttpd-bridge-starter/self-test.txt`

Expected local lighttpd runtime artifacts:

- `$CONNECTOR_COMPONENT_CACHE/lighttpd/src/lighttpd-$LIGHTTPD_VERSION/`
- `$CONNECTOR_COMPONENT_CACHE/lighttpd/build/lighttpd-$LIGHTTPD_VERSION/`
- `$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd`
- `$VERIFIED_LOG_ROOT/lighttpd-smoke/prepare-runtime/`

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

The starters and pinned runtime build are not:

- a lighttpd native module build;
- a FastCGI protocol implementation;
- an SCGI protocol implementation;
- a ModSecurity API integration build;
- a No-CRS, With-CRS, or RESPONSE_BODY validation.

The pinned runtime build proves only that the local lighttpd binary can be built
and staged from the pinned source. Runtime behavior is proven separately by
`make smoke-lighttpd`.

## Blocked Real Build Dependencies

A real production lighttpd adapter build is still blocked until the selected
production path has repository-backed hardening and broader validation:

- lighttpd headers/SDK/source tree for a native module path, or documented
  bridge dependencies for a FastCGI/SCGI/external-service path;
- build flags and include/library paths for the selected path;
- ModSecurity integration code using real APIs;
- artifact path for the selected adapter or bridge;
- build log path and reproducible command.

The Phase 1 sidecar_proxy runtime smoke deliberately avoids native lighttpd
module headers and FastCGI/SCGI library paths.

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
