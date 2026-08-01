# Change Record: Parent Lighttpd runtime-input containment

**Language:** English | [Deutsch](CR-20260730-sonar-lighttpd-runtime-input-containment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260730-sonar-lighttpd-runtime-input-containment |
| Date (UTC) | 2026-07-30 |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | One current SonarQube Cloud `pythonsecurity:S8707` finding at `connectors/lighttpd/harness/write_patched_lifecycle_results.py:208`. |
| Boundary | Parent Lighttpd harness source and tests, plus paired Change Record indexes. No Framework, MRTS, Gitlink, workflow, SonarQube Cloud configuration, suppression, or `master` change. |

## Motivation and problem statement

`--entity-fixture-result` reached `Path.read_text()` without establishing that
the file belonged to the verified private runtime root. The canonical shell
runner constructs the fixture result below its private smoke directory, but a
direct helper invocation could choose an unrelated readable path. The other
data-bearing lifecycle CLI inputs had the same missing containment invariant.

## Acceptance criteria

- Every data-bearing lifecycle input is an absolute, existing, regular,
  non-symlink runtime artifact strictly below the verified private root before
  the helper reads or uses it.
- The fixture JSON is read through the established descriptor-confined,
  no-follow runtime-artifact reader.
- Escaped paths, symlink escapes, missing files, and non-regular fixture paths
  fail before a lifecycle output, projection, or summary exists.
- The existing legitimate lifecycle control retains its schema, selected-case
  result, projection, and summary behavior.
- Exact-head hosted checks and SonarQube Cloud must still prove zero New Issues
  and zero New-Code duplication before any merge consideration.

## Implementation decision and rationale

`safe_runtime_output.py` now exposes a Lighttpd-local adapter over existing
Parent runtime-path primitives. `safe_input_path()` delegates to
`runtime_artifact_path(..., must_exist=True)`, preserving absolute-path,
below-root, no-symlink, safe-parent, and regular-file requirements.
`read_runtime_input_text()` delegates fixture reads to the existing
descriptor-confined `read_runtime_artifact_text()` control. The lifecycle
writer validates its events, phase-4 barrier, first-byte evidence,
Content-Length events, chunked events, and fixture result before processing;
existing atomic output handling is unchanged.

## Security impact

The controlled source is a local caller-controlled CLI path, not a proven
remote HTTP input. The affected sink was the fixture `Path.read_text()` call.
The repaired invariant confines all lifecycle data inputs to the private
per-run root and rejects symlink or type substitutions before processing. The
canonical runner remains compatible because it already places these artifacts
under that root. No request-body, rule, event, authorization, runtime-claim,
Quality Gate, or existing output protection is weakened.

## Changed files

- `connectors/lighttpd/harness/safe_runtime_output.py`
- `connectors/lighttpd/harness/write_patched_lifecycle_results.py`
- `connectors/lighttpd/tests/test_patched_event_validation.py`
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| Focused escape/symlink input regression | passed: all six data-bearing input options reject an outside-root file and an in-root symlink that resolves outside. |
| `python3 connectors/lighttpd/tests/test_patched_event_validation.py -v` with bytecode disabled and task-owned temporary storage | passed: 8 tests, including legitimate lifecycle behavior, escaped/symlink paths, and missing/non-regular fixture controls. |
| `python3 -m py_compile` for the changed Python modules and test | passed. |
| `python3 connectors/lighttpd/tests/test_patched_host_contract.py -v` with bytecode disabled and task-owned temporary storage | passed: 17 tests. |
| `git diff --check` | passed. |
| `make check-bilingual-docs` | blocked outside this diff: the new Change Record pair satisfies its required section headings, but the isolated worktree lacks the Parent-pinned Framework checkout required by 20 pre-existing local links. |

## Runtime evidence

The focused suite invokes the real lifecycle-writer CLI and the same
runtime-artifact helpers used by the patched lifecycle runner. It proves the
malicious local CLI-path conditions and the valid in-root control without
claiming a built Lighttpd host or HTTP runtime result.

## Checks not run and rationale

No live patched-Lighttpd/libmodsecurity build, runtime smoke, full lifecycle,
or connector matrix ran. This Python-only input-artifact containment change
does not alter C code, HTTP transport, host configuration, or protocol logic;
the focused real-CLI regression is the proportionate direct check. Those
separate host prerequisites were not required for this file-system boundary.

## Known limitations

- The finding is a high-confidence missing local CLI containment control, not
  a validated remote-Lighttpd arbitrary-file-read exploit.
- Hosted CI and the exact-head SonarQube Cloud analysis are not yet available;
  they remain required delivery evidence.
- The whole-tree bilingual documentation checker cannot pass in this isolated
  worktree because its Framework Gitlink checkout is intentionally absent;
  the reported missing link targets pre-date this diff.

## Remaining risks

Future Lighttpd lifecycle readers must use the same verified private root and
descriptor-confined input helper. A new reader that bypasses this boundary
requires a focused path-security review.

## Final diff and review status

The candidate is confined to Parent Lighttpd runtime-input containment,
focused tests, and bilingual traceability. Local verification passed. At
record authoring, no commit, push, pull request, hosted check, SonarQube Cloud
reanalysis, or merge is claimed.
