# Change Record: CR-20261015-i12-nginx-native-evidence

**Language:** English | [Deutsch](CR-20261015-i12-nginx-native-evidence.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-nginx-native-evidence |
| Date (UTC) | 2026-10-15 |
| Base revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |
| Latest integrated PR #410 revision | `a2d545ac7ec4abce23595e1c033f094104617201` |

## Motivation and problem statement

Preserve and extend NGINX-only I12 evidence from PR #410 while separating original host execution, fixture failures, oracle conflicts and fully qualified lifecycle results.

## Acceptance criteria

Exactly 140 original selected IDs, immutable selected contracts and historical revisions; independent per-ID physical proof; no PASS from aliases, candidates or unresolved oracles. New evidence and remaining gaps must be reported in both languages.

## Implementation decision and rationale

NGINX-specific capture/harness and ledger/report emitters extend evidence without changing shared source capture, the shared oracle generator, the central matrix or production connector code. The current-source adapter exports the exact Git tree, validates its complete inventory, and reconstructs only the pinned historical NGINX observer sources through an unchanged private copy of the shared registry. Historical staging is marked non-current and cannot qualify runtime evidence. The report verifies the immutable baseline SHA256 and original rows; candidate observations cannot approve a lifecycle.

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
- `tests/test_i12_nginx_security_boundaries.py`
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

Final RTK-proxied AST, JSON, exact-140-ID, outcome-count and EN/DE heading/table-structure checks passed. Both missing-key and extra-key mutations of the 69-ID gap mapping were rejected. Scoped `git diff --check` passed. Final repository-wide variable-documentation, bilingual, repository-reference, and link checks passed against the pinned Framework revision.

The NGINX I12 harness now rejects unowned, group/world-writable, symlinked, nonregular, traversing, or out-of-bound evidence paths before reads, publication, configuration execution, and loaded-image hashing. Build outputs are created fresh and private; worker scratch directories additionally use unpredictable names inside their admitted storage boundary. Report publication remains limited to the three task-owned tracked files. Seventy focused I12 tests, including 18 persistent boundary regressions, passed. The original hardened replay proposed all 93 retained candidates without approval and rematerialized all 71 reviewed records with 71 unique physical request paths.

PR #410 advanced to `a2d545ac7ec4abce23595e1c033f094104617201`; that head was integrated with the normal merge commit `d7a1ea30f38a77801f6b31c0f3325d33791461c9`. The exact current-source build at `d69fb1a08e582c6c255da94b3e5a9922c3a492a5` exported 2,121 regular Parent files plus Framework gitlink `99a7985c1be92a2297b1b59208f64df6768f2cbf`. Its source manifest is `8205cd30899e93992e061f92d1f9dd6a3b0697306c181a6d8ae67a2f7dbec384`; ordinary and observed module SHA256 values are `15a7e8d8c4e9e0ff8efc10cf5c4b62a09d2b954e0e94fca211d3132f01e30849` and `bd6e1e077134485ddc8e1c6b50df26d5b1d169fa39c92bfb38fd834b467ac872`. Shared verification and application both returned zero inside the frozen unchanged registry. Current source stayed current-v2; the historical compatibility stage was explicitly excluded from runtime qualification. Fresh configuration controls retained both expected historical load failures and accepted supported Safe and Strict configurations.

A fresh sealed compatibility retest, `attempt-1792079470951070559`, exercised `NEED-request-file` and `NEED-response-file` through the current harness: controller and driver exited zero, Root master and Nobody worker were observed, all four selected/follow-up clients exited zero with complete framing, both owned masters waited with cleanup verified, and the controller reported no timeout, resource violation, surviving namespace process, or mount leak. Each selected/follow-up allocation recorded P1, P2, P3 and P4 exactly once with native return 1, plus one Common finish, native logging and native cleanup call; the request used a 65,553-byte temporary-file body and the response used an actual file buffer ending at byte 36. Earlier blocked packaging attempts and one controller cleanup-race observation remain retained and are not counted as successful host evidence.

A second sealed current-head retest, `attempt-1792315527242854317`, bound the exact observed module above and NGINX binary `0d2287b344a1af4c6cc986dd915c09c60f3c942ec8ae76f8bdc5456506939746`. Controller and driver exited zero without timeout, resource violation, survivors or mount leaks. All three Root-master/Nobody-worker cases had directly waited selected and neighboring clients, complete HTTP/1.1 framing, null signals, verified listener/process cleanup, and observer finals with zero pending calls and live mappings. `NEED-request-file` appended 32,768 + 32,768 + 17 bytes from an actual 65,553-byte temporary file; `NEED-response-file` observed an actual file buffer from offset 0 to 36. Both reached P1-P4 once with native result 1, terminal-to-P2/P4 pairing exactly once, HTTP 200, and one Common finish, native logging and native cleanup call. `NEED-request-empty` again received a legitimate empty terminal chain but returned HTTP 500 after P1 and before P2/P3/P4 or any native body append; the first physical connector error remained `invalid request body buffer range`, and the following request returned HTTP 200. This retest confirms the separate #382 product defect without adding a lifecycle PASS.

The retained candidate summary and reviewed decisions still replay through the current qualifier as exactly 71 records, and deterministic report regeneration remains byte-identical. A new review of the old 93-case host attempt correctly refuses current loaded-image identity because the host's `/usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.4.8.0` was replaced after collection (inode and SHA256 changed). The original review-time identity evidence remains hash-bound; this later host mutation is recorded as a historical replay limit and is not bypassed or converted into PASS. The fresh three-case retest above validates loaded images against the current host state.

The versioned artifact embeds only projected public summaries and readable projections of original selected contracts. Full candidate lists, per-case decisions/body checks, verification environment mappings, and per-path input/source-hash inventories remain external, bound by input path/SHA256/size. The public projections retain each inventory count and one canonical SHA256 for its complete mapping; every selected requirement also retains the canonical hash of the unprojected contract and an external baseline locator. A recursive fail-closed check rejects body hex, environment mappings and sensitive key names; commands, statuses, log digests, counts and oracle correction reasons remain inspectable. Public command summaries replace local developer checkout paths deterministically while the referenced raw verification receipt retains the exact invocation.

## Known limitations

A selected case requires its own reviewed complete lifecycle packet. Candidate observations, builds, configuration checks and native tests alone cannot qualify it. Client EOF and zero-byte append cannot substitute for native EOS. HTTP/1 evidence makes no HTTP/2 reset claim. SDK 3.0.14 MIME fixture09 is not silently replaced by fixture08 or an invented Clear reset.

## Remaining risks

All rows without full lifecycle qualification remain incomplete. The body-null fixture reaches P1 despite its original P2 oracle; the HTTP 500 status repair does not resolve that phase mismatch. The separately confirmed empty-request production defect rejects NGINX's valid empty terminal buffer before P2; the ordinary module reproduces it. Its productive fix belongs separately to #382. No master merge or release is part of this task.

## Checks not run and rationale

Final hosted CI/Sonar status is established separately from local evidence after each push. Ruff was unavailable in the selected Parent `.venv` (`No module named ruff`); no package was installed. Report syntax and behavior/negative checks passed. Missing per-case lifecycle measurements remain explicit in the generated report and ledger. Repository variable-documentation, bilingual, reference and link checks passed in an external immutable view containing the exact 2,121-file Parent tree and Framework pin `99a7985c1be92a2297b1b59208f64df6768f2cbf`; the task worktree's intentionally empty submodule cannot provide those link targets directly.

## Final diff and review status

Changes are restricted to NGINX-specific I12 tests/harness/fixtures and this evidence/report scope. Draft PR #416 targets `work/pr382-i12-host-evidence-20261011` from `codex/i12-nginx-410-20261015`; delivery uses normal commits and normal pushes only. No master merge is part of this record.
