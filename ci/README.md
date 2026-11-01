# Connector CI entrypoints

**Language:** English | [Deutsch](README.de.md)

## Ownership and invocation

This directory retains product maintenance/build helpers and small authenticated
CI entrypoints. All tests, fixtures, harnesses, inventories, provisioning,
evidence processing and test-report generators belong to the independent
Framework. See [the interface](../docs/test-ownership-migration.md) and
[testing and evidence](../docs/testing-and-evidence.md).

The Connector root Makefile delegates test targets to
`$FRAMEWORK_ROOT/connector_suite/connector.mk`. CI calls pinned Framework
composite actions or reusable workflows. Supply the explicit Connector checkout,
exact revision, Framework checkout, profile and existing external output root;
do not infer a product checkout from the test script's directory.

## Product and trust boundaries

Product configuration, dependencies, build, installation and deployment remain
Connector-owned. Product binaries have no Framework runtime dependency.
`ci/run-trusted-framework.py` and the gate-required `ci/runtime/broker/`
entrypoints authenticate the protected Parent base and its Framework gitlink
before selecting privileged test code. Candidate source is not trusted code.
The fixed tool allowlist and protected-host gate remain mandatory; an absent
host prerequisite is `BLOCKED`, never an automatic fallback or PASS.

## Selection and evidence

The Framework inventory preserves 100 standard cases / 80 executions and the
original 1893 on-demand cases / 839 executions. New migration regressions remain
on demand. The standard cap is 100; selection is validated before execution.
Retries do not create additional distinct cases. A static check, native suite,
workflow success, build or configuration load does not establish hosted traffic
or product promotion. Keep run artifacts outside both source checkouts.

## Maintenance

Add test implementation and test-only dependencies to Framework. Keep only
small pinned integration calls here. Update both language documents and the
repository's Change Record when these contracts change. Framework and Connector
have separate branches, commits and PRs; integrate Framework first and then the
Connector gitlink and full-SHA CI references. No merge is implied by a test run.
