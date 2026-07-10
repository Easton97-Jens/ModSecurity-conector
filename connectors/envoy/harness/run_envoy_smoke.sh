#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)

# Framework-facing compatibility entrypoint. Build/provisioning remains a
# separate target; this script exercises only the built connector host path.
exec sh "$SCRIPT_DIR/run_envoy_connector_runtime.sh" "$@"
