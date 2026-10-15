# Change Record: CR-20261015-i12-nginx-native-evidence

**Language:** English | [Deutsch](CR-20261015-i12-nginx-native-evidence.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-nginx-native-evidence |
| Date (UTC) | 2026-10-15 |
| Base revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation and problem statement

Preserve and extend NGINX-only I12 evidence from PR #410 while separating original host execution, fixture failures, oracle conflicts and fully qualified lifecycle results.

## Acceptance criteria

Exactly 140 original selected IDs, immutable selected contracts and historical revisions; independent per-ID physical proof; no PASS from aliases, candidates or unresolved oracles. New evidence and remaining gaps must be reported in both languages.

## Implementation decision and rationale

NGINX-specific capture/harness and ledger/report emitters extend evidence without changing shared source capture, the shared oracle generator, the central matrix or production connector code. The report verifies immutable baseline SHA256 and original rows; candidate observations cannot approve a lifecycle.

## Changed files

- `ci/runtime/lifecycle/i12/nginx/build_capture.py`
- `ci/runtime/lifecycle/i12/nginx/config_controls.py`
- `ci/runtime/lifecycle/i12/nginx/host_state.h`
- `ci/runtime/lifecycle/i12/nginx/invalid_return.c`
- `ci/runtime/lifecycle/i12/nginx/ledger.py`
- `ci/runtime/lifecycle/i12/nginx/qualify.py`
- `ci/runtime/lifecycle/i12/nginx/report.py`
- `ci/runtime/lifecycle/i12/nginx/review_observations.py`
- `ci/runtime/lifecycle/i12/nginx/run_cases.py`
- `ci/runtime/lifecycle/i12/nginx/scenarios.py`
- `ci/runtime/lifecycle/i12/nginx/wire_client.py`
- `tests/test_nginx_native_cleanup_bridge.py`
- `tests/test_i12_nginx_invalid_return.py`
- `tests/test_i12_nginx_ledger.py`
- `tests/test_i12_nginx_qualify.py`
- `tests/test_i12_nginx_wire_client.py`

New report pair: [English](../../../docs/pr-410-i12-nginx-evidence-20261015.md) / [Deutsch](../../../docs/pr-410-i12-nginx-evidence-20261015.de.md); compact machine artifact: `ci/runtime/lifecycle/i12/nginx/evidence-20261015.json`. This Change Record pair.

## Commands executed

`rtk proxy python3 ci/tools/new-change-record.py create --name i12-nginx-native-evidence --base-revision f27eb59b53beff6f65384fc2e5037881a3052c01 --date 2026-10-15`: scaffold pair created. RTK-proxied report AST and baseline/negative checks passed: 140 unique IDs, baseline lifecycle PASS 1, remaining original open oracles 42; altered original oracle and duplicate ID rejected. Build/native/adoption/security/mutation commands and actual exit results are retained in the generated report and its hash-bound verification inputs; failed initial setups are retained.

## Security impact

Production code and security controls are unchanged. Host identity, physical client bytes, native observations and cleanup are checked at their own boundaries. Existing release secret blocker remains unresolved; no release authorization is implied.

## Runtime evidence

External run root: `/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015`. The generated report and compact ledger bind each supplied ledger/observation/verification input by SHA256. Original 42 native and 14 canonical executions retain their original revisions; 31 derived rows and reused YAML are not additional requests. Historical 60-case batches retain two config failures and one stale oracle independently.

The final ledger contains exactly 140 original IDs: 71 complete lifecycle qualifications (67 PASS, four FAIL), 69 without complete qualification, and ten historical config PASS results retained at their own layer. There are 70 newly qualified original IDs and one retest. Of 43 originally open oracle expectations, one was resolved at baseline and 33 are newly resolved; nine remain open. All 93 fresh host cases retain direct client PID/wait binding, real root-master/nobody-worker identity and verified cleanup; candidate coverage alone does not qualify all 93 cases.

The four qualified FAIL outcomes are the body-null fixture's original P2/observed P1 conflict, the separately confirmed empty-request product defect, and both timeout cases lacking original `run_id`/`transport_case_id`/`connection_id` event metadata. Corrections preserve original mandatory event fields; `phase4_body_reject` passes with those fields. Request ProcessPartial records native append returns 0/0 and native process-request-body return 1.

Report generation used `rtk proxy python3 ci/runtime/lifecycle/i12/nginx/report.py` with `ledger/nginx-140-final.json`, `review-suite04-v2/candidate-summary.json`, `final-provenance.json`, `verification-native/verification-summary.json` and `sdk-mime/receipt.json` from that run root. Exit 0 produced the machine artifact and both language reports. The generator fails closed unless the reviewed remaining-gap mapping covers exactly the unqualified original IDs.

Final RTK-proxied AST, JSON, exact-140-ID, outcome-count and EN/DE heading/table-structure checks passed. Both missing-key and extra-key mutations of the 69-ID gap mapping were rejected. Scoped `git diff --check` passed. Final repository-wide documentation/link checks remain the integrating task's responsibility.

## Known limitations

A selected case requires its own reviewed complete lifecycle packet. Candidate observations, builds, configuration checks and native tests alone cannot qualify it. Client EOF and zero-byte append cannot substitute for native EOS. HTTP/1 evidence makes no HTTP/2 reset claim. SDK 3.0.14 MIME fixture09 is not silently replaced by fixture08 or an invented Clear reset.

## Remaining risks

All rows without full lifecycle qualification remain incomplete. The body-null fixture reaches P1 despite its original P2 oracle; the HTTP 500 status repair does not resolve that phase mismatch. The separately confirmed empty-request production defect rejects NGINX's valid empty terminal buffer before P2; the ordinary module reproduces it. Its productive fix belongs separately to #382. No master merge or release is part of this task.

## Checks not run and rationale

Final hosted CI/Sonar and delivery status are not established by local evidence. Ruff was unavailable in the selected Parent `.venv` (`No module named ruff`); no package was installed. Report syntax and behavior/negative checks passed. Missing per-case lifecycle measurements remain explicit in the generated report and ledger. Local documentation/link checks are separately run by the integrating task; no result is inferred here.

## Final diff and review status

Changes are restricted to NGINX-specific I12 tests/harness/fixtures and this evidence/report scope. The integrating task owns final diff review, normal commits and Draft-PR delivery against `work/pr382-i12-host-evidence-20261011`; this record does not claim a commit, PR number or merge.
