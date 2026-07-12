<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Envoy operations

**Language:** English | [Deutsch](operations.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Start and stop

Use matching Make targets for local harnesses. Operator-managed services use their own service manager and host configuration check.

## Logs, rotation, and health

Use host error/access logs and payload-free connector/evidence logs. Rotate logs through the host facility rather than renaming open files. Health means reachability and a loaded configuration; it is not a security or lifecycle PASS.

## Timeouts and resources

Set host timeouts, worker/file/memory limits, and runtime roots for the target host's boundaries. Repository timeout variables bound jobs but do not replace production sizing. Keep secrets out of paths, processes, events, and canonical evidence.

## Diagnosis and updates

Check endpoint reachability, module/service load, rules-file readability, runtime-root permissions, and the selected integration mode before treating a missing result as a rule failure. Host, module, patchset, and source-revision changes create a new build/cache identity; rerun the selected evidence target afterward.
