# Change Record: CR-20261009-nginx-input-fault-inherited-fd-20261009

**Language:** English | [Deutsch](CR-20261009-nginx-input-fault-inherited-fd-20261009.de.md)

Bounded isolated patch; no native runtime or scanner closure evidence.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-input-fault-inherited-fd-20261009 |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

The driver created and closed a private ledger before the C fixture reopened an environment path. Leaf O_NOFOLLOW plus a lexical prefix did not bind the created inode; traversal/intermediate symlinks and multiple links were not excluded. Ordinary unprivileged reachability through the validated0700 workflow is unproven.

## Acceptance criteria

Consume only a genuine inherited writable FD>=3 for a root-owned0600 empty regular single-link inode. Preserve own-worker UID/PPID, exact transaction/URI/POST, one-time trigger and actual Common validator return. Never reopen legacy paths.

## Implementation decision and rationale

Use MSCONNECTOR_OWNED_INPUT_FD with strict bounded decimal parsing, F_GETFL and fstat checks. Descriptor lifetime belongs to the coordinated driver. Align the ID parameter and callback typedef with the selected Engine header's const char * contract; C17 generic static assertions check callback/export compatibility without casts.

## Changed files

`tests/fixtures/nginx_common_input_fault.c`, `tests/fixtures/nginx_common_input_fault_scope.c`, `tests/test_nginx_common_input_fault_scope.py`, and this EN/DE pair. Driver integration is separately owned.

## Commands executed

Final additional checks:all seven affected C fixture/cleanup files C17 syntax exit0; three changed Python files py_compile exit0; `tests.test_change_record` and `tests.test_prepare_reviewed_framework_handoff`:39 tests, exit0; record archive check exit0; path/link diagnostics on the four new records:0 errors. `make check-bilingual-docs` and `make check-doc-links` failed on existing submodule links because the isolated worktree's Framework directory is unpopulated. Explicit external FRAMEWORK_ROOT does not replace those relative links. No missing dependency was changed or check weakened.

RTK-wrapped FD-only legitimate control on the original constructor:two failures (actual1 1 instead of0 1). After migration:seven scope tests, exit0; final combined seven-suite run:34 tests, exit0. Negative cases cover malformed/invalid FD, read-only, hardlink, nonregular, nonempty, wrong mode/owner and legacy path. Rename/replacement plus legacy symlink alias writes only the original retained inode.

## Security impact

Closes the fixture create-close-reopen boundary by removing C path resolution. Independent pre-patch review confirmed the gap but did not prove ordinary attacker reachability or HTTP/RCE exploitation. The actual private inode checks and process/transaction scope remain mandatory.

## Runtime evidence

None. Worker roles and foreign-owner metadata are controlled C17 inputs; actual Common validation is linked. The filesystem rejected an attempted chown control with EINVAL, so owner rejection uses an explicit controlled fstat owner field.

## Known limitations

Python driver migration and combined independent candidate review are separate ownership boundaries. No integrated native proof or Sonar closure is claimed.

## Remaining risks

A stale or invalid original receipt cannot be repaired by these tests. Fresh driver/fixture integration, strict source capture and genuine native rerun remain required.

## Checks not run and rationale

Native build/runtime, fresh scanner closure and coordinated driver integration were not executed by this worker.

## Final diff and review status

RED-to-GREEN controls and inode-alias checks passed. No Git write or shared Root source edit occurred. The separate independent candidate review remains pending with the coordinator.
