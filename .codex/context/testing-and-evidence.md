# Parent Testing and Evidence Policy

## Source of truth

Select commands from the current root `Makefile`, component build files, current versioned testing/connector documentation, `ci/README.md`, `tests/README.md`, and affected connector documentation. Do not maintain a second static target catalog here.

## Evidence layers

Treat these as separate claims:

1. documentation/schema/contract check;
2. compilation/build;
3. configuration parsing/loading;
4. focused unit/contract/self-test;
5. process/service start/readiness;
6. host/client smoke;
7. full lifecycle/runtime execution;
8. canonical evidence finalization/validation;
9. report generation/scanner readback.

A pass at one layer does not imply another layer passed.

## Result statuses

For normal repository validation items use `passed`, `failed`, `blocked`, `not_run`, or `not_applicable`. Record exact command/action, scope, relevant revisions/profile, output/evidence class, observed result, and limitation.

A deep assessment may separately track an applicable target that never reached execution as a coverage gap rather than inventing a target-test status. Prerequisite/setup checks receive their own result IDs.

## Parent versus Framework

Parent tests protect Parent contracts and host/runtime integration. Reusable catalog cases, schemas, runner/normalizer logic, and cross-connector reusable validation belong in Framework.

Framework selection/report generation cannot by itself prove a Parent hosted runtime lifecycle.

## Logical profile boundary

Host-family results do not automatically apply to sibling logical profiles. Keep HAProxy HTX versus SPOE/SPOP companion, Envoy ext_proc versus ext_authz+observer, Traefik native UDS versus forwardAuth+observer, and lighttpd Stock versus patched-native evidence separate.

## Runtime claims

A runtime claim binds to the applicable connector logical profile, rules/effective configuration, transport where relevant, Parent/Framework/MRTS revisions where required, run ID, host/tool identity, and validated evidence contract. Stale/generated evidence is not a new execution.
