# HAProxy SPOE/SPOA Harness Design Plan

**Language:** English | [Deutsch](design.de.md)

## Status

documentation_only: true
implementation_status: not_started
runtime_verified: false
harness_executed: false
decision_status: undecided
promoted: false

## Purpose
This document only describes what tasks a later harness will perform
HAProxy would have to meet SPOE/SPOA-PoC. It does not contain any implementation and
does not prove runtime capability.

## Role of Harness
- The harness would later prepare the PoC environment.
- He would later start HAProxy and an external SPOA component.
- He would send test requests later.
- He would collect logs later.
- He would generate a report later.
- Everything is planned only / Still to be checked.

The harness contract would be consumed by the central ModSecurity-test-Framework; no tests are stored here.

## Non-targets
- No executable harness.
- No process control.
- No network test.
- No HAProxy startup.
- No agent start.
- No request test.
- No block/allow proof.
- No runtime report.
- No CI integration.

## Planned harness hooks

| Hook | Purpose | Planned inputs | Planned outputs | Success criterion | Status |
|---|---|---|---|---|---|
| prepare | Prepare PoC directories/placeholder state | Planned paths, planned config placeholders | Planned work area | Still to be checked. | planned only |
| start | Planned launch phase for HAProxy and SPOA component | Planned config paths, planned process parameters | Planned process states | Still to be checked. | planned only |
| send_request | Benign/malicious requests to be triggered by the framework | Planned request definitions from central framework | Scheduled allow/block signals | Still to be checked. | planned only |
| collect_logs | Scheduled Log Collection for Framework Evidence | Scheduled log sources | Scheduled Log Artifacts | Still to be checked. | planned only |
| stop | Planned stopping of processes | Planned Process References | Scheduled stop state | Still to be checked. | planned only |
| cleanup | Scheduled cleanup of temporary artifacts | Scheduled Artifact List | Planned cleaned state | Still to be checked. | planned only |
| generate_report | Framework-side report generation | Scheduled test results/log references | Planned report path in the central framework | Still to be checked. | planned only |

## Hook details

### prepare
- Purpose: Planned preparation phase for PoC workspaces.
- Required artifacts: To be checked.
- Open points: path model, minimum requirements, error behavior. Still to be checked.
- Status: planned only.

### start
- HAProxy launch planned but not implemented.
- SPOA agent launch planned but not implemented.
- Process/port/timeout behavior: To be checked.
- Exact startup order and dependencies: To be verified externally.
- Status: planned only.

### send_request
- benign request planned.
- malicious request planned.
- expected results: allow/block-signal planned only.
- no verification currently.
- Request metadata completeness: Not available from the current repository.
- Status: planned only.

### collect_logs
- HAProxy logs planned only.
- Agent logs planned only.
- Correlation via transaction_id planned only.
- no log scheme proven yet.
- Log field semantics and completeness: To be checked.
- Status: planned only.

### stop
- Process stop planned only.
- Error behavior open.
- Fail-open/fail-closed relevant stop scenarios: To be verified externally.
- Status: planned only.

### cleanup
- temporary files/processes planned only.
- open.
- Boundaries between PoC artifacts and external resources: To be reviewed.
- Status: planned only.

### generate_report
- Planned report is exclusively in the central test framework.
- currently not available.
- runtime_verified must remain false until real execution occurs.
- Report field semantics: To be checked.
- Status: planned only.

## Scheduled report schema
Only planned only; the actual production takes place centrally
ModSecurity testing framework.

## Limits / Not documented
- That this harness is executable: Not verifiable from the current repository.
- That HAProxy/SPOA interacts correctly with these planned steps: To be verified externally.
- That block/allow/redirect semantics are fully covered: To be checked.
- That response headers/response bodies can be reliably verified: Still to be checked.
