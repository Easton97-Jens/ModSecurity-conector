# FND-PARENT-0069 — Apache mod_security3.c has a baseline-identical GCC C17 Werror failure group

## Identity

- Category: compiler_hardening_gap
- Repository / ownership: parent / parent
- Priority / severity / confidence: P2 / not_applicable / reproduced
- Status / feasibility: validated / feasible_now
- Release blocker / candidate-integration blocker / security relevance: false / false / true
- Scope: master and selective #94A task-candidate baseline comparison

## Summary

The mandatory GCC C17 check with -std=c17 -Wall -Wextra -Werror exits 1 for
connectors/apache/src/mod_security3.c in both retained master and selective
#94A candidate runs. The source is byte-identical at SHA-256
8b21b64c95a1f1cb98ac05437e60e5d5ab8124e363cd2784b7c800e65449f8d7, and
the two 114-line stderr logs normalize to SHA-256
34b8bbdfcda5e8420a33ac99eaf57a1283388ec7f87d104b1ee36093744eacc6.

This is a validated pre-existing compiler-hardening gap, not a regression
caused by selective #94A. It is therefore neither a release blocker nor a
candidate-integration blocker for that candidate. No fix, PR, merge, master,
verified, closed, or delivery claim is made.

## Observed behavior and boundary

The header probe passes, but the separate module translation-unit compilation
fails in both retained directories. The diagnostic group includes unused
parameters and variables, pointer signedness at the libModSecurity
request-header API, a missing Apache module flags initializer, static
msc_config.h declarations without definitions in this translation unit, and a
non-void cleanup path reaching its end. The raw logs differ in absolute source
and build prefixes only; the recorded normalized digest proves the same
114-line group.

This is a compiler-hardening and assurance boundary, not an established
attacker-controlled runtime boundary. It must not be resolved by warning
suppression, -Wno-error, source-list removal, or a scanner/gate exception.

## Evidence

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| Master GCC C17 stderr | 1d40b8f49f4d38f09f8cfce6266f59fc963cd64d2268dbefe3ce5e66f19f6cde | Retained 114-line log; recorded compiler exit 1. |
| Candidate GCC C17 stderr | 634475cf310eb274e3825549cdeed62bb58d865a3a2dd97444da7b354885196e | Retained 114-line log; recorded compiler exit 1. |
| Master and candidate mod_security3.c | 8b21b64c95a1f1cb98ac05437e60e5d5ab8124e363cd2784b7c800e65449f8d7 | Byte-identical source, so the candidate did not introduce the group. |
| Normalized retained stderr comparison | 34b8bbdfcda5e8420a33ac99eaf57a1283388ec7f87d104b1ee36093744eacc6 | Parent-supplied normalization after environment-only absolute-path-prefix removal. |

The raw retained logs are:

- /var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-c17-baseline-master/connectors_apache_src_mod_security3_c.c17.o.err
- /var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-c17-baseline-candidate/connectors_apache_src_mod_security3_c.c17.o.err

## Remediation direction and controls

Use a separate Parent source-remediation task. Classify each diagnostic before
correcting it: intentionally unused callback inputs, genuinely dead variables,
header linkage, cleanup return status, Apache module ABI initialization, and
semantics-reviewed unsigned-byte API conversion. Preserve the required C17
flags and source-contract wiring.

Acceptance requires the existing GCC C17 check to exit 0 without warning
suppression, focused Apache/APXS/APR legitimate controls for affected
semantics, and a fresh source/log comparison. Run approved Clang C17 controls
as a complementary check when available. The selective #94A candidate remains
evaluated only against relevant change-introduced findings.

## Deduplication and residual risk

This is not FND-PARENT-0008: that record is a historical Clang
missing-field-initializer observation in apache2/msc_config.c. It is not
FND-PARENT-0043: that record owns intervention-buffer lifecycle and ownership
safety in mod_security3.c. Shared C17 wiring or a shared Apache area is not a
shared root cause or remediation boundary.

The unresolved group prevents a clean GCC C17 assurance claim for this
translation unit, but it establishes no remote or local attacker-controlled
runtime exploit. It remains validated and feasible now, with no source change
made by this local finding task.

## History

- 2026-07-29T10:13:10Z: master and selective-candidate retained GCC C17 logs
  were recorded as one baseline-identical compiler-hardening group under a new
  canonical ID.
