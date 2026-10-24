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
has been accepted. The I12 instruction to stop additional work applies when this
policy is active; this alone does not stop already configured automatic jobs or
prove that their selection has changed.

The migration must demonstrate that every automatic default selection path uses
the authoritative inventory, the expanded active count is at most 100, and an
over-limit selection fails before test execution. Document the retained and
removed coverage. These are future implementation acceptance criteria, not new
test results or commands supplied by this policy.

## I12 closeout for PRs #382 and #410: existing evidence only

### Binding work stop

The user-directed I12 closeout replaces the previous full-matrix qualification
mission for product PR #382, related harness/evidence PR #410 and their stacked
I12 evidence work. Apply this reduced scope to
continuations, delegated work and old task/checklist instructions. Older demands
to exhaust all I12 IDs, Oracles or evidence packets do not reopen the campaign.
Only a new explicit user request for additional I12 assessment can reopen it.

Do not create additional I12 tests, fixtures, Oracles, harness extensions or
qualification campaigns. Do not execute or re-execute existing tests to complete
I12, fill an evidence gap, refresh a historical PASS or reach the 100-case limit.
The remaining I12 work is limited to reading, selecting and consolidating
existing evidence and recording the closure.

### Frozen selection and proof

Freeze at most 100 already evidenced cases within the single project-wide active
inventory above. This is not an additional I12 allowance: other active Common,
connector and infrastructure cases consume the same budget. A smaller supported
selection is valid; never add cases or launch runs to fill unused places.

Each selected case must have a stable ID, requirement, connector/profile,
precisely stated evidence layer, actual result, relevant source/build revisions,
configuration identity, run identity/date and an accessible retained evidence
reference. Preserve available artifact digests. A summary's PASS label without
adequate underlying evidence is not enough. Select by distinct behavior and
material risk, not by taking the first 100 green records.

Keep evidence bound to the revision and claim it actually proves. An older PASS
does not qualify the current head of PR #382 or #410. Without existing proof of
applicability, retain the historical result and mark the current-head claim as
not verified.
Unavailable or incomplete evidence stays explicitly unqualified. These limits
must be recorded, not repaired through another I12 test campaign.

### Finite closure deliverables

Close the reduced I12 work after producing:

1. one frozen selection, its actual expanded count of at most 100, the retained
   requirements and the existing evidence references;
2. an archive disposition for the remaining historical cases and gaps, retaining
   their original results and references; existing ledgers may be linked rather
   than copied, regenerated or revalidated;
3. one concise closure report stating the selected scope, evidence revisions,
   uncovered requirements, known relevant product defects and current PR #382 / #410
   delivery/check limitations from existing records.

Report I12 work as closed at the user-reduced scope only when these deliverables
exist. This is not full historical-matrix acceptance and must not redefine an
existing full-acceptance flag such as `I12_COMPLETE`. Preserve failed and
unqualified results; excluding a known defect from the active selection does not
resolve it. Archived gaps create no automatic follow-up work or repeated requests
to continue testing.

### PR #382 / #410 delivery boundary

Incomplete historical I12 coverage alone must not keep the scoped product
delivery open. Evaluate PRs #382 and #410 at their respective heads against their
changed behavior, known relevant defects and mandatory current-head CI, security
and release requirements. Limit any separately authorized remediation to the concrete
remaining issue; it must not reactivate the historical I12 matrix.

The I12 work stop does not bypass a mandatory gate or authorize additional test
execution for its remediation. If necessary validation cannot be completed
within the current authority, report that specific criterion and stop. In that
case, do not claim merge readiness, current-head runtime qualification or release
approval.
Use `delivery-and-ci.md` for delivery; merge still needs its own authorization.

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
