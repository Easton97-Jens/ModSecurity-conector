# Change Record: CR-20261010-r17-strict-client-full97

**Language:** English | [Deutsch](CR-20261010-r17-strict-client-full97.de.md)

Documentation closure for the actual local R17 proof; no product fix or Protected PASS.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261010-r17-strict-client-full97 |
| Date (UTC) | 2026-10-10 |
| Base revision | `2f02370b07149265841411894f1a2cf7f1e978ff` |

## Motivation and problem statement

R16 already had Canonical PASS and 97 Required-PASS, but the generic Strict client's precise numeric completion was not persisted. R17 closes that measurement gap with external direct-child instrumentation and one fresh standard Full97. This versioned change records the completed proof; it changes no product, Framework/MRTS pin or Required contract.

## Acceptance criteria

Keep all 97 Required records and original validators unchanged; directly distinguish normal exit, signal and spawn failure; preserve curl arguments/streams/timeouts; retain First-Byte writer measurement; perform bounded controls/focus and exactly one fresh standard Full97; require genuine operation/identity/cleanup evidence, original Canonical PASS and verified hashes. Actual Ready remains a separate Root-owned transition after final documentation quality/publication checks.

## Implementation decision and rationale

Reuse the existing direct Popen/wait mechanism in an external CURL override, pinned to /usr/bin/curl and hash-bound actual case source. Exclusive UUID-bound owner-only start/completion receipts are durably fsynced. TERM/INT/HUP propagate to the actual child; normal 143 is not inferred as a signal. No stderr/HTTP/Make-success inference, argument/environment dump, new timeout, Required reduction or validator weakening. Instrument SHA256: `c4606c146fe0a47ebeb03564505082ee58c075889eae8b8dea4ff6ed401833b5`. Frozen-plan audit supplies exact case/log association; basename alone is not catalog proof.

## Changed files

`docs/pr-396-full97-followup-checklist.md`, `docs/pr-396-full97-followup-checklist.de.md`, `reports/audits/change-records/CR-20261010-r17-strict-client-full97.md`, `reports/audits/change-records/CR-20261010-r17-strict-client-full97.de.md`. External recorder/tests/audits stay in `/var/tmp/codex/ModSecurity-conector/analysis/nginx-strict-client-full97-r17-20261010T193127Z`; no functional checkout files changed in this documentation task.

## Commands executed

All local commands were RTK-wrapped. Native scaffold: `python ci/tools/new-change-record.py create --name r17-strict-client-full97 --base-revision 2f02370b07149265841411894f1a2cf7f1e978ff --date 2026-10-10`, exit 0. Recorder RED before implementation: one missing-measurement test, exit 1. Final direct recorder controls:14 tests, exit 0; paired Python-meter controls8 passed. Root's R17 receipts record71 focused tests and 61 namespace tests without SKIPs, exit 0. The authorized standard `make full-lifecycle-nginx` has actual Make/supervisor exit 0,554.091s; original validator exit 0. Native `make check-bilingual-docs check-doc-links` passed, exit 0 after correcting an initial German heading error. `python -m unittest -v tests.test_change_record tests.test_bilingual_docs tests.test_prepare_reviewed_framework_handoff`: 61 tests, no SKIPs, exit 0. Actual captures are retained under the R17 analysis root, with temporary data there and the exact Framework worktree explicitly selected. This task did not rerun runtime or full local lint.

## Security impact

No secrets or full environments/arguments retained. Fixed binary/hash, root-owned nonsymlink case source and output ancestry, O_NOFOLLOW, exclusive receipt creation and distinct controls scope preserve the existing boundaries. Runtime remains isolated loopback with Root-master/nobody-worker roles. External measurement is local instrumentation, not an independently trusted Protected root checker. Existing source/runtime artifacts remain unchanged.

## Runtime evidence

[Public R17 report](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434), published 2026-10-10T20:21:11Z before this documentation edit. Tested Parent `2f02370b07149265841411894f1a2cf7f1e978ff`, Framework `9f41f80db7bf53b57429457bce0dda675d2ec5d7`, MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`, NGINX 1.31.6; run `nginx_full97_2f02_20261010_r17`. Ubuntu 26.04.1 LTS/kernel 7.0.0-38/KVM. Original Canonical PASS;97/97 Required-PASS, routes14 YAML/42 native/10 config/31 derived. Inventory166:97 PASS/34 unselected NOT_EXECUTED/35 NOT_APPLICABLE. Collector source separately PASS31/NOT_EXECUTED42 placeholders; specialized original receipts are not rewritten. Actual 79 non-readiness HTTP operations including four positive controls;17 readiness;61 lifecycles/cleanup;57 fresh direct root-owned projections. Direct curl 34 pairs:16 primary/1 First-Byte/17 readiness. Generic Strict normal exit 52, no signal, UUID `669ba1b19fc340618d62148d715e5fc3`, PID 10440, Rule 1100301/Phase 4/strict abort; curl HTTP 000 and producer HTTP 200 separate. First-Byte writer exit 0, UUID `1515086ec928494aafd0b0a0fceab107`, PID 12514. All 16 declared program receipts across11 classes normal 0. Runtime 2589 checksums verify0; ledger `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a`. Genuine NGINX binary/module fresh build, Engine cache reuse identity-verified. Initial frozen analyzer exit 1 preserved; new read-only v2/v3 correctly use normalized original TX and scrub log after intentional raw phase4.log scrubbing. Historical R15/R16 unchanged.

## Known limitations

Local H1-only No-CRS proof, not H2/H3, Off, CRS, production, other connectors or Protected. Derived records are not additional HTTP operations. Transport EAGAIN/short-write is not physical event-log sink short-write proof; no universal per-case loaded-inode claim. Additional product ShellCheck 7 warnings/7 infos unchanged; historical16 Apache/MRTS diagnostics not retested. Complete additional local lint not rerun. Actual tested-head CI22 SUCCESS/2 intentional H2/H3 SKIPs; fresh Sonar GateOK/all five conditions passed. Later docs-only head requires separate fresh quality/readback and inherits no runtime PASS.

## Remaining risks

Root must validate/publish this paired documentation, read back final documentation head/CI and perform/read back the conditionally authorized actual Ready transition. No future Ready or own approval is claimed here. PR #382 remains OPEN/DRAFT; broad I09–I12 remain open. Framework PR #137 is CLOSED/MERGED, tested9f pin retained. Ready is not merge permission.

## Checks not run and rationale

No second Full97, Protected dispatch, master/Trusted Base/runner/sudoers/host-gate mutation, merge, retarget, framework repinning or cross-connector overhaul. These are unauthorized or separate scopes. Source-functional changes were unnecessary because external measurement reached the existing actual CURL call. Full additional local lint and historical Apache/MRTS diagnostics were not rerun; final documentation checks/CI are Root-owned and must be reported from actual results.

## Final diff and review status

The change is documentation-only and preserves historical bindings and checkbox IDs. Public/local report precedes these edits. Existing source tests, original runtime statuses and instrumentation remain immutable. Native EN/DE/path/link checks and 61 regression tests passed. Independent review confirmed paired IDs and corrected observed-versus-required exit52 wording; no numeric52 requirement was introduced. Git publication, fresh successor CI and actual PR Ready/readback remain separate Root-owned delivery actions, recorded in public PR metadata. No documentation successor SHA or CI result is invented here.
