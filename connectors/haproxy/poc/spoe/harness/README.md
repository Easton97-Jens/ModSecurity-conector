# SPOE PoC Harness Placeholder

**Language:** English | [Deutsch](README.de.md)

documentation only

This directory only documents planned hooks for a later PoC
(planned only). It does not contain a harness code.

## Planned hooks (planned only)

### prepare
- Purpose: Prepare test environment.
- Status: planned only
- Open points: Artifact paths and prerequisites still to be checked.

### start
- Purpose: Start HAProxy and external component.
- Status: planned only
- Open points: Starting order and health check to be verified externally.

### send_request
- Purpose: Trigger benign/malicious requests.
- Status: planned only
- Open points: Request data and expected values still to be checked.

### collect_logs
- Purpose: Collect runtime logs.
- Status: planned only
- Open points: Log sources/format and correlation still to be checked.

### stop
- Purpose: Stop processes in a controlled manner.
- Status: planned only
- Open points: Abort/timeout behavior to be verified externally.

### cleanup
- Purpose: Clean up PoC artifacts.
- Status: planned only
- Open points: scope and limits still to be examined.
