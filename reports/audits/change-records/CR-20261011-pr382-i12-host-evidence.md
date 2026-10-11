# Change Record: CR-20261011-pr382-i12-host-evidence

**Language:** English | [Deutsch](CR-20261011-pr382-i12-host-evidence.de.md)

Manual documentation/evidence update. I12 NOT COMPLETE; no complete required route leg PASS.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-pr382-i12-host-evidence |
| Date (UTC) | 2026-10-11 |
| Base revision | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |

## Motivation and problem statement

Historical R17 and compiled tests did not establish I12 on the tested PR #382 source tuple. Record independent host/client/backend/transport/physical-log/cleanup evidence, actual failures and precise gaps.

## Acceptance criteria

Bind the run `20261011T063350Z-0df51024008f-i12` to tested Parent `0df51024008fc84f0a6820f3b011055b69c3a3e2`, Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` and MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. Separate thirteen required legs plus one advisory diagnostic control, preserve R17, maintain complete EN/DE parity and leave I12 unchecked for failures or missing required proof. Complete-leg PASS count is 0; broad I12 criteria are not met.

## Implementation decision and rationale

Documentation only: external private fixtures, immutable sources, build artifacts and raw receipts are excluded from the proposed eight-file atomic commit. No product/test/dependency/gitlink change. Preserve official bwrap/AppArmor isolation and unprivileged host identities; keep missing observations null and physical sink faults separate from transport faults.

## Changed files

Four pairs: `docs/pr-382-checklist.md` / `docs/pr-382-checklist.de.md`; `docs/pr-382-i09-i12-rest-matrix.md` / `docs/pr-382-i09-i12-rest-matrix.de.md`; `docs/pr-382-i12-host-evidence-20261011.md` / `docs/pr-382-i12-host-evidence-20261011.de.md`; `reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.md` / `reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.de.md`. Historical I12b/R17 and the 56 source-matrix rows remain unchanged.

## Commands executed

RTK wraps all shell commands. `make test-hostruntime-preflight`: exit 0, 27 tests. `make check-common-helpers-c17`: exit 0. `make check-ci-security-contract`: exit 2, 177 tests, three import errors, six skips. `make check-bounded-smoke-runtime-contract`: exit 2, 119 tests, four assertion/subtest failures, 12 errors. Native event/sink/lifecycle batch: exit 1, 74 tests, 15 assertion/subtest failures, two errors. actionlint 1.7.12: exit 0 on 32 workflows plus permission fixtures. zizmor 1.29.0 offline: workflows/safe controls exit 0, unsafe controls expected exit 14. Explicit Parent Python is `/usr/local/bin/python3` 3.14.7; exact commands/results remain in `verification/results.json`. `rtk gain`: exit 0. Final native bilingual, link, Change Record and diff checks exit 0; receipts are retained in document-mount-checks-02/results.json.

## Security impact

No product security behavior changed. Apache physical-sink propagation failures and historical focused Traefik Native/UDS `protocol_error` remain visible. Latest Native/UDS full observations have normal Allow and stay BLOCKED for missing receipts. No isolation/validation weakening, package/toolchain installation, sensitive payload publication or production deployment. Unrelated main-checkout changes remain preserved. Controlled APR FD faults do not prove natural filesystem exhaustion or every concurrent FD schedule.

## Runtime evidence

The [host report](../../../docs/pr-382-i12-host-evidence-20261011.md) records provenance, thirteen required legs and gaps. Local retention root: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261011T063350Z-0df51024008f-i12`; not a downloadable GitHub artifact. Closed Apache inventory: 21 cases, 9 full-contract PASS, 5 physical-sink FAIL, 7 full-contract NOT_EXECUTED. Actual direct curl exits/bytes, backend counts, native committed actions, genuine recovery logs and independent cleanup are observed. This is not the complete required case inventory. NGINX identity admission is BLOCKED. libModSecurity 3.0.14 SHA256 `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407`.

Latest Envoy/Traefik closed inventory: 27 cases, 0 PASS, 0 FAIL, 27 BLOCKED. Later PR #382 head `498653c2a193d34b7b25b2903b1e4db1c45e7f73` has documentation/B09-test-only delta; evidence remains bound to tested `0df51024008fc84f0a6820f3b011055b69c3a3e2`, with no PASS inheritance. Parent/Apache/native wrappers use Python 3.14.7; Envoy/Traefik native helpers explicitly use `/usr/bin/python3` 3.14.4.

Native review through Stock full06 retains 262 hash references. HTX full02 has eight actual cases; SPOP full03 six plus separately assessed response-companion evidence; both remain BLOCKED for independent client/sink/transaction-cleanup gaps. Patched staticfile focus02 is bounded curl0/200/32 bytes, full03 trusted-directory reject77. Stock06 retains 16 verified raw files and actual two-Allow backend logs, with no /p1-block arrival. Native engine_decision actual_action="" fails the unchanged harness enum; same-TX request_blocked is actual_action=deny, HTTP451, transport_result=http_status, Rule9821001 with hash chain. Direct deny client proof remains null; later four cases NOT_EXECUTED. Stock05 raw loss stays historical. No product regression or independent client enforcement failure is inferred. Final selected inventory in `matrix.final.json`: 79 records, 9 PASS, 6 FAIL, 53 BLOCKED, 11 NOT_EXECUTED; advisory extra excluded. Whole thirteen legs: 0 PASS, 2 FAIL, 11 BLOCKED. This is not complete required case coverage. `normalized/` retains original-bound per-leg receipts; no physical events are fabricated. Independent rehash confirms 791 references (529 Apache + 262 native). Preliminary doc checks failed on absent Framework/Git metadata; final real read-only mount checks exit 0 with private read-only Git-path aliases, unchanged original files and unchanged validators.

## Known limitations

No complete required route leg PASS. Seven bounded Apache MIME/EOS observations do not prove the full scope/exactly-once contract. Missing timestamps/sequence/hash observations remain unsynthesized. Driver exit is not client completion; companion halves need separate receipts. Historical R17 does not prove this tested tuple or H2/H3/CRS/Off/production.

## Remaining risks

Required route cases and I11 Apache/SPOP physical sink propagation work remain. Failed broader verification is retained, not converted to green CI. No Sonar, Protected Exact-Head or release-ready claim. Local raw retention is not portable published evidence.

## Checks not run and rationale

Complete NGINX runtime is blocked by required root-master/nobody-worker identity handoff. Complete all-route acceptance remains unavailable. Broader checks encounter missing PyYAML, hardcoded uninitialized worktree Framework paths, missing `python` alias and sandbox UID limitations; no weakening or dependency installation forced a pass. Final bilingual/link/Change Record checks pass; hosted delivery CI/Sonar for the publication commit remain pending and do not inherit local results.

## Final diff and review status

One atomic eight-document commit is recommended. Scoped diff, native finished report/record checks and independent read-only documentation review passed; no material review findings remain. User-authorized delivery is a stacked Draft PR on `fix/unified-native-results-events-20260921`; no publication outcome/PR number, merge or deployment is invented. I12 NOT COMPLETE.
