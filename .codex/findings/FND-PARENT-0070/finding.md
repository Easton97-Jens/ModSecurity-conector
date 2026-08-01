# FND-PARENT-0070 — Apache APXS wrapper omits a private common header from fresh DSO materialization

## Identity

- Category: build_defect
- Repository / ownership: parent / parent
- Priority / severity / confidence: P1 / not_applicable / validated
- Status / feasibility: fixed / feasible_now
- Release blocker / candidate-integration blocker / security relevance: true / false / true
- Scope: resulting Parent master 154ee724eba4653fa6378fc3c8729ae433e65697, tree-identical to final PR #183 head 4e4dfb36e1b05f7eda38450fd3710e3a04905118

## Summary

**Current resulting-master disposition — 2026-07-29T11:27:25Z.** PR #183
merged as master `154ee724eba4653fa6378fc3c8729ae433e65697`; tree
`c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0` equals final head
`4e4dfb36e1b05f7eda38450fd3710e3a04905118`, and all 14 master-SHA workflows
succeeded. Detached-master focused Apache/MIME unit checks and
`make check-apache-common-adoption` passed. These facts supersede the historic
candidate-only wording below but do not replace a fresh resulting-master
APXS/DSO/HTTP run; the finding remains `fixed`, not `verified` or `closed`.

A fresh Apache connector DSO materialization staged request_helpers.c but
omitted its quoted private header header_validation_internal.h. The retained
pre-fix tree confirms the header was absent while the source header exists, and
the APXS wrapper copied the C source list without this header.

A mutable task-worktree repair now adds the header to that copy list. Its fresh
materialized tree contains the header and produced a DSO at SHA-256
`fdaf666fccde82299a028f7c593412c379a61ea0e5a2074398d5a6994656919b`; the
Parent task reports the corresponding clean DSO make passed. This is therefore
**fixed locally only**, not verified or closed: the repair still needs an
independently committed PR exact head and a resulting-master reproduction.

The P1 release-blocker flag remains active for normal Apache connector builds
until that delivery evidence exists. The defect is baseline-existing, not
introduced by selective #94A, and therefore is not that candidate's
integration blocker.

## Evidence and boundary

| Artifact | SHA-256 or result | Evidence |
| --- | --- | --- |
| Materialized source manifest | 65523487c8135066604a68c283217b34f00f241fe67ce241db1d8b65ecdaf4ff | Wrapper is adapter-owned from Parent apxs-wrapper.in. |
| Materialized wrapper template | 35103aa90e4dea20a36ef8e84b659ebdde28f9bd68456ecf1460bc47be9a8d02 | Copy loop stages request_helpers.c but omits header_validation_internal.h. |
| Staged request_helpers.c | e7c5473ce0228084bc2407548af20dbdb93f7ca2ba9c7757b60bbd93f2511659 | Includes header_validation_internal.h at line 4. |
| Parent source header | b9ca7130e184913c10b3b24cfae18415eef411a908b1af5f926af6b695ed11e7 | Required header exists in common/src. |
| Staged private header | absent; test -e exits 1 | Required sibling header is missing in build/common-src. |
| Mutable repaired wrapper | 723148f1b635b4d33c80b13860e1c8d3b6be4c984bde2400ad086b9c7501ed1f | Uncommitted task-worktree snapshot adds header_validation_internal.h. |
| Repaired staged header | b9ca7130e184913c10b3b24cfae18415eef411a908b1af5f926af6b695ed11e7 | Fresh repaired tree contains the required header. |
| Repaired DSO | fdaf666fccde82299a028f7c593412c379a61ea0e5a2074398d5a6994656919b | Fresh repaired tree produced mod_security3.so. |

The selected candidate commit is exactly 9f23ae2c5fe908cef38f203be03f93fda75a8dd7
for the original affected-path comparison, with an empty base-to-HEAD diff. The
repair is an uncommitted working-tree delta on that checkout, so it is not an
exact committed PR head. Parent task evidence reports the original make failure
and the repaired make success; raw command/stdout/stderr receipts tied to a
committed PR head remain required verification artifacts.

## Root cause and remediation direction

The Parent APXS wrapper copies a curated common C-source list into a fresh
build/common-src directory but does not copy private local headers those sources
quote. Framework materialization does not own or remove that wrapper contract.
The demonstrated repair belongs in the Parent wrapper: stage the private header
and add a focused completeness contract for every quoted local header required
by a staged common source. Promote it through an independent committed PR, then
run a clean fresh APXS DSO make with raw command/stdout/stderr/exit evidence and
Apache configuration/load plus selected HTTP legitimate controls on the exact
head and resulting master. Do not suppress the failure or use a pre-existing
source-tree header as a fallback.

## Acceptance and distinctness

Acceptance requires the private header to appear in fresh build/common-src, the
clean DSO make to exit 0, Apache to load/configure normally, and a negative
contract that rejects omission of a required local header. The demonstrated
local repair still needs its own committed exact head, fresh evidence, and a
resulting-master reproduction.

This record is distinct from FND-PARENT-0008 (historical Clang initializer),
FND-PARENT-0064 (RulesSet lifecycle cleanup), FND-PARENT-0068 (cleanup-runner
TOCTOU), and FND-PARENT-0069 (GCC C17 warning group). It establishes no
attacker-controlled exploit path, but does block normal Apache connector build
delivery until remediated.

## History

- 2026-07-29T11:27:25Z: the resulting-master delivery facts above were
  reconciled; fresh master APXS/DSO/HTTP validation remains required.

- 2026-07-29T10:25:19Z: retained post-sentinel materialization evidence created
  the canonical Parent build-defect record.
- 2026-07-29T10:33:55Z: the mutable wrapper repair was materialized afresh;
  the staged header and resulting DSO are retained, and the Parent task reports
  a passing clean DSO make. Status is fixed locally only, pending committed
  exact-head and resulting-master validation.
