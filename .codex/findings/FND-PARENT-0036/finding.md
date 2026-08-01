# Finding: Native Oracle append-error path double-frees a request body

**Language:** English | [Deutsch](finding.de.md)

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0036` |
| Category | `sanitizer_finding` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `medium` / `confirmed` |
| Status | `fixed` |
| Release blocker / security relevant | no / yes |

## Summary, behavior, and impact

The historical nonempty-body branch freed `body.data` when
`msc_append_request_body(...) == 0`, then reached common cleanup with the
pointer still non-null. Cleanup freed it a second time. ASan against real
LibModSecurity 3.0.16 reported `attempting double-free` when a narrow
one-symbol interposer forced that library error. This proves a short-lived
Oracle process memory-safety/availability defect, not ordinary remote-input
reachability.

Expected behavior releases the allocation once and clears pointer/size before
the shared cleanup guard.

## Affected scope and preconditions

- File/symbols: `ci/tools/native_modsecurity_oracle.c`,
  `msc_append_request_body`, `cleanup_error`, `cleanup_oracle`, and `body.data`.
- A nonempty body is allocated and `msc_append_request_body` returns zero.

## Reproduction and evidence

1. Build the historical Oracle with ASan and use the retained one-symbol
   `LD_PRELOAD` interposer to return zero from `msc_append_request_body`.
2. Run a nonempty body and observe the historical double-free; replay the
   patch-equivalent branch without an ASan diagnostic.
3. The retained evidence has the historical path
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/native-oracle-lifetime-revalidation.md`
   (not distributed in this reconciliation checkout),
   SHA-256 `5d676317ed37403f1eae272c23f3c93e744e1fad9cbc2366fdd67a832fb8a7b5`.
   The exact PR-D head `5704905c5337f9dcfe8c08a78a7e482ecd72bbf7` passed its
   focused regression and Clang/GCC static controls.
4. Current task run `ci-tools-sonar-remediation-20260730` refactors current
   teardown through `cleanup_oracle`. Its sealed focused security-diff report
   is SHA-256 `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7`;
   C17 GCC/Clang and real-libmodsecurity 200/403/setup-error controls passed.
   A natural `msc_append_request_body` failure was not reproduced, so this is
   one-owner source/control evidence rather than a new reachability claim.

## Root cause and remediation

The branch-local `free(body.data)` did not establish the shared cleanup
invariant. PR D sets `body.data = NULL` and `body.size = 0` immediately after
the append-error free and retains the existing guarded cleanup path plus a
focused regression test. The current ci/tools refactor additionally routes
current teardown through `cleanup_oracle`, leaving one owner for `body.data`
without claiming a naturally reproduced append failure.

## Acceptance, validation, and controls

- The append-error branch clears pointer/size before common cleanup.
- `tests/test_native_oracle_memory_safety.py` passes.
- Historical ASan replay distinguishes the old double-free from the
  patch-equivalent clean replay; C17 Clang/GCC fanalyzer controls pass.
- Current C17 GCC/Clang warning-as-error and real-libmodsecurity 200/403/
  setup-error controls retain result and cleanup behavior after the one-owner
  refactor.

## Dependencies, blockers, related findings, and residual risk

Protected-squash PR #200 delivered the one-owner refactor to resulting Parent
master `13890da56ad19a105629243349f39ea8c084f396`; exact-master workflow and
source-identity evidence is retained. `FND-PARENT-0035` is separate rule/output
authority. A realistic non-synthetic Library append failure is unavailable, so
production/remote reachability remains unverified and is not an exploit claim.
The current refactor also did not reproduce that natural failure. The remaining
limitation is the unavailable strongest historical ASan/one-symbol-interposer
replay and referenced harness; no risk acceptance was made.

## History

- `2026-07-18T14:46:42Z`: historical ASan error path confirmed; exact PR-D
  focused control passed; status set to `fixed` pending verified PR.
- `2026-07-30T11:07:21Z`: current one-owner cleanup refactor revalidated with
  sealed security review, compiler/runtime controls, and the exact Draft-PR
  #200 hosted-check/SonarQube Cloud receipt. No natural append failure was
  reproduced, so status remains `fixed`, not `verified`.
- `2026-07-30T11:33:48Z`: refreshed Draft-PR #200 exact head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` against master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` passed required GitHub checks and SonarQube Cloud Quality Gate/readbacks. This delivery evidence does not newly reproduce a natural append failure, so the historical finding remains `fixed`, not `verified`.

## Resulting-master disposition

Protected-squash PR #200 exact head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` produced Parent master
`13890da56ad19a105629243349f39ea8c084f396` at `2026-07-30T12:11:32Z`.
The native Oracle blob equals the reviewed candidate and all 14 master
workflows passed. This confirms delivery of the one-owner source refactor, but
does not recreate the required historical ASan/one-symbol-interposer
append-failure replay. The referenced strongest harness/evidence is absent in
this workspace; no natural reachability is inferred. Status remains `fixed`,
not `verified` or `closed`. Receipt SHA-256:
`69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
