# MRTS package integration

**Language:** English | [Deutsch](mrts-package-integration.de.md)

The native MRTS caller consumes the Framework package interface at
`ci/provisioning/mrts-package.py`. MRTS remains a pinned, read-only generator:
neither MRTS sources nor either repository gitlink change in this task.
The general test-ownership migration is separate.

## Preparation and private handoff

Pass explicit `FRAMEWORK_ROOT`, `MRTS_ROOT`, `CONNECTOR_ROOT`, and external
`BUILD_ROOT` paths. The Framework CLI accepts `prepare`, `verify`, and
`materialize`, each with `--framework-root`, `--mrts-root`, `--connector-root`,
`--build-root`, `--package-root`, and `--include-feature-demo 0|1`.
All actions accept `--upstream-definitions` and `--feature-demo-definitions`;
the native caller forwards `MRTS_UPSTREAM_DEFINITIONS` and
`MRTS_FEATURE_DEMO_DEFINITIONS` consistently when supplied.
`materialize` additionally requires a new `--output-root` below `--build-root`
and accepts `--port` for the private request destination.

The Framework stages generation, strict import/validation and `mrts.load`
before publication. Its manifest binds revisions, selected corpora, unique
case IDs, definitions, artifact hashes and preparation status. Demo flag `0`
excludes optional demo generation and strict import; flag `1` validates demo
content and rule-ID collisions. Numeric header names and YAML-special strings
retain their types through import and materialization.

`run-mrts-native-full.sh` prepares one package per invocation and verifies it
before reuse by another target. With `MODSECURITY_MRTS_PREPARED=1`, an explicit
`MRTS_PACKAGE_ROOT` is required and is verified; the flag alone is insufficient.
The default package is a new private child under `MRTS_BUILD_ROOT`.
Each target receives `$MRTS_NATIVE_ROOT/<target>/package`; FTW ports and load
paths belong to that copy. The shared package remains unchanged. Preparation
or materialization failure stops that target before host execution.
The native runner combines only the selected private FTW subtrees under
`<target>/selected-ftw/<corpus>` and includes each selected corpus load file;
corpus-specific counts and outcomes remain available in result JSON.

## Result integrity and output

Native go-ftw uses `--output json --file <target>/go-ftw.json`. The shared
Framework result reader counts explicit outcomes for unique selected FTW case
IDs: selected, executed, PASS, FAIL, skipped, ignored, forced and missing.
Duplicate/conflicting IDs, unknown results and inconsistent totals are errors;
forced PASS is not observed runtime PASS. A zero process exit cannot supply
missing results. Empty required selections, skipped or missing required cases
produce `INCOMPLETE`, and writer errors propagate as execution errors.
The Apache single-case and case-loop caller also stops on result-publication
failure before printing PASS. This closes the required generic Apache MRTS
error path without changing the selected CRS publication contract.

The native report revalidates the private FTW selection and structured result;
legacy log totals cannot manufacture PASS counts. Report counts retain the
selection and execution distinction. Package preparation does not prove host
behavior. Native MRTS evidence remains separate from connector qualification.

`MRTS_NATIVE_ROOT` must be below `BUILD_ROOT`. `MRTS_NATIVE_REPORT_ROOT` defaults
to `$MRTS_NATIVE_ROOT/reports` and must also remain below `BUILD_ROOT`.
Generated reports are written below
`$MRTS_NATIVE_REPORT_ROOT/reports/testing/generated/`, outside the source
checkout. Keep build/log/runtime roots in approved external storage. No full
historical MRTS or H2/H3 matrix is required by this change.

## Integration order and compatibility

1. Review the independent Framework MRTS package PR and its focused tests.
2. Integrate Framework only with separate merge authorization.
3. In a separately authorized Parent pin-update task, select the verified
   Framework `master` SHA that contains the package API. Preserve the MRTS pin.
4. Integrate the Parent native caller with that dependency available. For local
   cross-PR verification, select the proposed Framework checkout explicitly
   through `FRAMEWORK_ROOT`; this does not update the Parent gitlink.

The current Parent pin predates this interface, so the caller PR is dependent
and remains Draft until the Framework integration and explicit pin update.
The test-ownership migration may touch the same Parent entry point or generated
on-demand archive; reconcile those interfaces without copying the importer or
moving the corpus again. HTTP/2, HTTP/3, coverage and dependency-matrix expansion
remain separate work.

See the [Parent Change Record](../../reports/audits/change-records/CR-20261028-mrts-package-integration.md)
for actual checks and runtime limitations.
