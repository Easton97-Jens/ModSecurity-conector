# Parent Testing and Evidence Policy

## Source of truth

Select commands from the current root `Makefile`, component build files, current versioned testing/connector documentation, `ci/README.md`, `tests/README.md`, and affected connector documentation. Do not maintain a second static target catalog here.

## Compact default test suite: at most 100 active cases

### Binding scope and counting

The project-wide default suite must contain at most **100 active test cases**.
This is one shared inventory across Common, all connectors and logical profiles,
unit/integration/runtime tests, and tests of harnesses, validators and evidence
infrastructure. Cases selected from Framework or MRTS by Parent default
validation count in the same inventory; this rule grants no write authority in
those repositories. The limit is not per agent, task, language, runner or CI job,
and 100 is a ceiling, not a target to fill.

An active case is an independently selected behavioral scenario in normal local
or CI validation. Count each independently executed parameter, connector,
profile and scenario variant after expansion. Several assertions about the same
scenario can remain one case. Renaming independent scenarios as a single test,
hiding them in loops or bundling them into a collector does not reduce the count.
Repeating the same case locally, in CI or during a justified retest does not add
another active case, but remains additional execution cost.

Builds, formatting, linting and static-analysis/scanner gates are separate
validation operations. Functional test cases invoked by such operations still
count; moving tests behind a build or scanner command must not bypass the limit.

### Selection and maintenance

- Keep one authoritative inventory of active case IDs, their requirements,
  applicable profiles and execution selectors. Local default validation and CI
  must derive their case selection from this same inventory.
- Before execution, resolve variants and validate the complete inventory.
  More than 100 active cases is a selection error: fail visibly before running.
  Never silently take the first 100 cases or report a truncated suite as complete.
- Select cases by distinct behavior and material regression risk. Prefer
  observable requirements, meaningful boundary/error behavior and proven
  regressions; share setup and fixtures and consolidate genuine duplication.
- At capacity, adding an active case requires a named replacement or consolidation
  in the same change, with the affected requirement coverage explained. Replacing
  a failing case solely to obtain a pass is not an acceptable consolidation.
- Preserve useful historical/specialist tests and evidence outside every automatic
  default selection path. Execute or maintain them only for an explicit user
  request covering that additional assessment. Do not silently turn scheduled
  jobs, another agent or a separate runner into an extra default test catalogue.
- Report active, archived/on-demand and retired cases separately. Record lost
  coverage; an unselected historical requirement is not a new PASS.

### Routine product work and stop rule

For a scoped feature, bugfix, refactor or documentation task, select only the
affected active cases and the checks needed for its concrete acceptance criteria.
Do not run all 100 cases merely because they are available. Once those criteria
are sufficiently verified, stop test/evidence work and finish the product task.

Do not autonomously expand routine work into full I12 qualification, all-connector
matrices, historical Oracle reconciliation, new test frameworks or additional
evidence campaigns. A broader assessment must be explicitly requested and scoped;
it does not enlarge the standing default inventory. Do not repeatedly ask for
more testing solely to exhaust a historical backlog.

Historical Matrix/Oracle/evidence gaps outside the current task do not by
themselves prevent completion of that scoped product task. A missing validation
criterion necessary for the changed behavior must still be reported under
`definition-of-done.md`; it is never silently passed or declared inapplicable.
Existing mandatory CI, security and release gates remain binding. If a required
check exceeds the agreed scope or is unavailable, report the specific limitation
without weakening the gate or claiming a verified PR/release.

### Transition and evidence boundary

This policy establishes the binding target and work-selection rules. It does
not assert that existing tests or workflows already implement the 100-case cap.
Inventory creation, case consolidation/archive selection and runner/CI wiring
are a separately scoped migration; a policy-only change must not perform them
implicitly. Until that migration is verified, disclose the actual suite state
and do not claim that the technical cap is enforced or that the full old matrix
has been accepted.

The migration must demonstrate that every automatic default selection path uses
the authoritative inventory, the expanded active count is at most 100, and an
over-limit selection fails before test execution. Document the retained and
removed coverage. These are future implementation acceptance criteria, not new
test results or commands supplied by this policy.

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
