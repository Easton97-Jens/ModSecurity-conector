# Change Record: CR-20261008-nginx-native-authority-mrts-root

**Language:** English | [Deutsch](CR-20261008-nginx-native-authority-mrts-root.de.md)

Explicit read-only MRTS source selection; unit wiring evidence.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-authority-mrts-root |
| Date (UTC) | 2026-10-08 |
| Base revision | `603e84493dcb51ab72eadb5a7102c4977cab631c` |

## Motivation and problem statement

An isolated Framework worktree may leave tools/MRTS uninitialized. Git then reports the Framework ancestor, not an independent MRTS repository; the authority producer correctly rejects it.

## Acceptance criteria

Honor explicit MRTS_ROOT unchanged, preserve the existing Framework/tools/MRTS default when omitted, and keep producer identity/pin/security validation unchanged.

## Implementation decision and rationale

The baseline producer argument now uses ${MRTS_ROOT:-$FRAMEWORK_ROOT/tools/MRTS}, matching existing run-mrts-native-full.sh. The caller selects an actual initialized read-only repository; no discovery or historical SHA fallback is added.

## Changed files

One baseline argument, focused test_no_crs_native_authority_wiring.py control, and this paired record.

## Commands executed

The explicit override assertion failed before the change (RED). All nine bounded extracted-shell wiring controls then passed in 4.408 seconds. Shell syntax, archive and final whitespace checks are reported in the handoff.

## Security impact

No MRTS checkout, pin or source is modified. Explicit MRTS_ROOT still passes producer checks for exact independent top-level/current HEAD40/clean status and equality to the current Framework gitlink. A receipt cannot supply the SHA.

## Runtime evidence

No native runtime/build. The argument test uses a producer unit double and an empty selected directory; it proves pass-through and absence of source writes, not repository authority or host behavior.

## Known limitations

Read-only inspection confirmed an initialized clean MRTS at current HEAD 8a6bb546c4c81d8ffc7be801dceac60c6925685f and the inspected Framework gitlink matched. This is a point-in-time observation, not a hardcoded expected SHA or retained build authority.

## Remaining risks

Current clean Parent/Framework pins, prepared release/Engine readiness and all five compiled fault libraries remain coordinator prerequisites. The authority producer will recheck actual identities.

## Checks not run and rationale

Build, native runtime, MRTS mutation and source pin updates were outside this slice. No cache/build/release semantics changed.

## Final diff and review status

The final diff is limited to the explicit override, bounded regression and paired record. Producer source/security, original release-1.31.6 behavior and existing commits are preserved.
