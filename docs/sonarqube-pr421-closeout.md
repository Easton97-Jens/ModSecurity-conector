# PR #421: Sonar and CI closeout evidence

**Language:** English | [Deutsch](sonarqube-pr421-closeout.de.md)

## Current measured source closure — 2026-10-26

Source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8`. All three CI analysis jobs and terminal server tasks succeeded; all gates are `OK`. This is exact source closure before the documentation commit. The following documentation head needs its own fresh CI/Sonar proof in the PR; these results are not transferred to it.

| Project | CE task | Analysis ID | Processing / gate | New-code coverage |
| --- | --- | --- | --- | --- |
| Easton97-Jens_ModSecurity-conector | `AaF2d1wrF1KaAz-ccYSb` | `5ca2a23e-9296-4c2d-8fbc-fa4d9a6b97eb` | `SUCCESS` / `OK` | 83.5% |
| Easton97-Jens_ModSecurity-conector_cpp20_advisory | `AaF2dvPAk-m4lzyjm-LE` | `fd25c86a-c9f5-4cb3-8cd5-6e2a3e59ba69` | `SUCCESS` / `OK` | 84.6% |
| Easton97-Jens_ModSecurity-conector_cpp23_advisory | `AaF2dqhewSmsgR9Bx97p` | `085ce801-0376-4963-9864-25391aae003b` | `SUCCESS` / `OK` | 84.6% |

| Project | Reviewed IDs | `FIXED` | `FALSE_POSITIVE` | OPEN/CONFIRMED | Hotspots |
| --- | ---: | ---: | ---: | ---: | ---: |
| Main PR 421 | 152 | 143 | 9 | 0 | 0 |
| C++20 advisory | 33 | 24 | 9 | 0 | 0 |
| C++23 advisory | 18 | 12 | 6 | 0 | 0 |
| Total | 203 | 179 | 24 | 0 | 0 |

The 203 distinct IDs comprise fully paginated starting inventories 150/31/16 plus six discoveries. Every ID was separately read back. All types in the New Code OPEN/CONFIRMED scope return zero, as do separate hotspot queries. The three new complexity IDs are actually `FIXED`; the three new Git-security IDs remain `FALSE_POSITIVE` with individually verified comments. No risk was accepted; no rule, threshold, gate condition or New Code requirement was weakened and no broad exclusion introduced.

All six unchanged gate conditions pass: reliability/security/maintainability each 1 against at most 1; `new_coverage` 83.5/84.6/84.6 against at least 80; `new_duplicated_lines_density` 0.0 against at most 3; `new_security_hotspots_reviewed` 100.0 against at least 100. No condition was ignored. The 83.5% is PR coverage, 84.6% advisory branch new-code coverage. Fresh separate master readback still confirms 0.6% overall coverage; this PR does not repair it.

All three scans retain 1,350 sources, 243 tests, 136 native translation units and four Go modules; one Python XML, four Go reports and 71 gcov reports were imported per project. Native quality remains 100/100: parsing errors in 0/2,263 functions, 0/6 classes, 0/33,778 statements; 0/1,132 unresolved project includes and zero external include residuals. This proves measured parsing/include closure, not C/C++ taint.

Remaining scanner warnings are separate from the 203 IDs: main 46 WARNs (44 architecture labels, FIFO parser, TLS file without changed lines), each advisory four WARNs (FIFO parser, two predecessor, FIFO syntax) plus the INFO simulation-cost skip at `ci/lib/runtime_path_utils.py:69`. C/C++ taint remains explicitly disabled in AutoConfig; multiple variants/independent targets remain separate limits. Missing TLS blame has disappeared, while the changed-lines warning remains. Python/FIFO limits have baseline counterevidence and are not asserted as PR regressions.

Terminal runtime proof belongs separately to source `900dddb49c43ec4479c4b75a91071cadb97893c4`, run `40267347652`: all six jobs succeeded including Apache; selected 403/CRS/audit/cleanup proof, not full matrix qualification. Details and artifact limits remain in the 900 section. The source scan does not transfer runtime proof to another head.

| Remaining item | Disposition after source proof |
| --- | --- |
| 203 issue IDs | 179 `behoben und nachgewiesen`, 24 proven false positives |
| Measured native parsing/include residuals | `behoben und nachgewiesen` |
| C/C++ taint, Python simulation-cost/predecessor, valid FIFO | `begründete Analyzergrenze` |
| Architecture model with 44 labels, repeated HTTP 415 and unchanged readback | `extern blockiert` |
| Remaining TLS changed-lines warning, final CI/Sonar at documentation head | `weiterhin offen` |

Source issues/gates are therefore closed; external architecture application and final-head verification still prevent a complete technical closure claim. PR #421 remains Draft, overall status **teilweise abgeschlossen/blockiert**. No merge or master change. Sources: `d545-evidence-summary.json`, `d545-analysis-bindings.json`, `d545-*-baseline-readback.json`, `d545-*-log-evidence.json` and separate hotspot readbacks in run `pr421-all-findings-20261026`.

<!-- source-900-evidence -->
Historical intermediate state: pending/gate-ERROR statements throughout this 900 block are superseded by d545 closure above.

## Historical measured 900 source scan before correction

As of source `900dddb49c43ec4479c4b75a91071cadb97893c4`. This supersedes earlier pending statements for the 197 starting IDs and native parsing residuals. It is not evidence for a later documentation/correction head; the final exact head is read back in the PR after push.

| Project | CE task | Analysis ID | Processing / gate | Coverage |
| --- | --- | --- | --- | --- |
| Easton97-Jens_ModSecurity-conector | `AaF2aMqHwSmsgR9Bx9Lu` | `aed6171b-c278-4868-8f8c-ade346d8c306` | `SUCCESS` / `ERROR` | 83.3% |
| Easton97-Jens_ModSecurity-conector_cpp20_advisory | `AaF2aiZ-wSmsgR9Bx9Pa` | `683e6e06-c8f5-49a7-b495-541a0e637fb9` | `SUCCESS` / `ERROR` | 84.4% |
| Easton97-Jens_ModSecurity-conector_cpp23_advisory | `AaF2aeHVF1KaAz-ccXOp` | `37a38445-53d1-46e6-99d9-98ff4ffaea0e` | `SUCCESS` / `ERROR` | 84.4% |

Every starting ID was read back individually: main 142 `FIXED` + 8 `FALSE_POSITIVE`, C++20 23 `FIXED` + 8 `FALSE_POSITIVE`, C++23 11 `FIXED` + 5 `FALSE_POSITIVE`. Two distinct new IDs appeared in each project; the six new findings are separate in the per-issue triage. Complete closure of all 203 IDs is not yet claimed.

At this scan the gates were ERROR only for `new_security_rating` 3 against at most 1. Other conditions passed: reliability/maintainability 1, duplication 0.0%, hotspot review 100.0%, coverage at least 80%; no condition was ignored. The 83.3% is main PR coverage, 84.4% advisory branch new-code coverage; accumulated master coverage remains separate.

All three scans imported one Python XML, four Go reports and 71 gcov reports. Scope remains 1,350 sources, 243 tests, 136 native translation units and four Go modules. Actual native results: quality 100/100, errors in 0/2,263 functions, 0/6 classes, 0/33,778 statements; 0/1,132 unresolved project includes and zero external include residuals. This proves the measured parsing/include closure; independent targets/variants and C/C++ taint disabled in AutoConfig remain separate limits.

Main warnings retain the 44 invalid architecture labels, the valid FIFO parser case and the TLS “changed but without having changed lines” message. Missing TLS blame is no longer reported; the remaining changed-lines warning prevents a complete TLS warning-closure claim. Both advisories retain four WARN messages (FIFO parser, two predecessor, FIFO syntax) and the INFO simulation-cost skip at `ci/lib/runtime_path_utils.py:69`; these are not six extra issue IDs.

Both former CodeQL missing-root-go.mod warnings are resolved. A different Traefik log warning remains: the module-cache directory does not exist because the selected module uses only the standard library and needs no dependencies. No artificial cache directory or cache disabling was introduced. Go overlay-cache misses and C/C++ fallback to a normal full database remain separate notices with successful analysis.

The new `python:S3776` contract-decoder complexity is locally decomposed in the next correction head; eleven tests including two passive invalid contract values passed in 0.035 s. The three new `pythonsecurity:S8705` Git findings were separately reviewed, transitioned as FP with their own comments and read back; details follow below. Rescan remains pending; the bounded runtime at source 900 is now terminal and evidenced. Architecture remains externally blocked, PR Draft.

Evidence files: `900-evidence-summary.json`, `900-analysis-bindings.json`, `900-*-baseline-readback.json`, `900-*-log-evidence.json`, `900-github-codeql-warnings.json` under external run `pr421-all-findings-20261026`.

### New Git FPs: applied individual decisions

All three new `pythonsecurity:S8705` IDs were separately reviewed against complete
20-location flows and ten actual call sites. Five real Git-argument probes plus
one allowed and four rejected output-root controls passed; security-relevant
controls are AST-identical in the next candidate. Git global config, PATH,
templates and `GIT_*` are explicitly not isolated; this review does not prove
protection against an already compromised execution user or tool configuration.

Each finding received its own concrete FP comment and `FALSE_POSITIVE`
transition; status and exact comment were read back individually. Evidence:
`900-new-security-triage.json`, `900-new-fp-actions.json`,
`main-900-fp-readback.json`, `cpp20-900-fp-readback.json`,
`cpp23-900-fp-readback.json`. Thus 24 FPs are applied in total (9/9/6);
176 starting IDs are `FIXED`, while three new complexity IDs remain locally
corrected before fresh scanner proof.

### Terminal runtime proof at source 900

[Runtime run 40267347652](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40267347652)
is terminal SUCCESS at source `900dddb49c43ec4479c4b75a91071cadb97893c4` for
all six jobs, including Apache `121392518485` and aggregate `121396280699`.
Actual Apache case `crs_sqli_anomaly_block`: HTTP 403, deny, CRS rule `942270`,
profile `native-httpd-module`, complete cleanup, Apache validation passed.
Read artifact JSON confirms exactly five technical PASS cells and functional
scope only `selected_crs_block_case_only`: 24 contract rows, five passed,
zero failed, six blocked and thirteen not run; `coverage_complete: false`,
`merge_eligible: false`.

Identity: Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`, MRTS
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`, CRS
`e03a4f6dabc7a30ebd8c52c97d28a154f590a48f`, profile
`with-crs-no-mrts-40267347652-1`. Apache/HAProxy allow control remains
`not_observed`, no-MRTS is `workflow/source_declared`; Envoy/lighttpd/Traefik
have allow 200, block 403 and no-MRTS `runtime_observed`. Raw Apache audit and
results are only hash references here. Artifact JSON was read from managed
ZIP-download bytes in memory; no independently verified ZIP digest is claimed.
This is not full runtime-matrix qualification or proof for a later source head.
Sources: `900-runtime-terminal.json`, `900-runtime-apache-artifact-json.json`,
`900-runtime-aggregate-artifact-json.json`.

### Separate fresh master-coverage readback

Authenticated readback on 2026-10-26 at 04:25 UTC still confirms master coverage
0.6% and master new-code coverage 0.6345357841049332%. The latest master
analysis `52df415d-2c24-43a3-a63a-de6e79c37d60` dates from
`2026-10-25T19:08:47+0000`, revision
`9f44647593bac7947113558c6ad183ab118e80af`: 91,169 lines to cover,
90,641 uncovered lines, 394 conditions and 341 uncovered conditions.
`master-coverage-readback.json` is the separate current read evidence;
improved PR/advisory percentages do not repair these master metrics.

<!-- source-900-evidence-end -->

## Historical implementation phase before the 900 scan — 2026-10-26

This entire section describes starting source `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3` and its then-local corrections before the source scan. Its pending/include/warning statements are historical development states; the measured results and later individual decisions above supersede them. The subsections below are not a current closure ledger.

The current request expands review to **all 150 main-project New-Code issues**, rather than only eight security issues. [Complete individual triage](sonarqube-pr421-triage.md) retains every issue once, its direct link, rule/language, starting file/line, exact message, severity/quality impacts, code/flow context, action and bounded proof. The immutable starting source and all three fresh analysis bindings are `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3`.

| Project/scope | Unique starting issues | Individually proven/transitioned false positives | Local corrections awaiting fresh scan |
| --- | ---: | ---: | ---: |
| Main PR 421, New Code OPEN/CONFIRMED | 150 | 8 | 142 |
| C++20 advisory master, New Code OPEN/CONFIRMED | 31 | 8 | 23 |
| C++23 advisory master, New Code OPEN/CONFIRMED | 16 | 5 | 11 |

Main pagination is exactly 100+50 = 150 server-reported/unique IDs, without security/severity/language/rule filters. Main impacts: 141 maintainability, 8 security, 1 reliability; 122 Shell/28 Python. Legacy severities: 6 MINOR, 116 MAJOR, 25 CRITICAL, 3 BLOCKER. Advisory New-Code inventories are separate from the earlier total vulnerability inventories of 27/24.

The new explicit user authority permits individual proven false positives with reasons. All **21** such transitions were actually applied through `rtk bypass /usr/local/bin/sonar-with-env`, each with its own complete-flow counterevidence and named attack/allowed controls. `FALSE_POSITIVE` and the exact submitted comment were read back for every issue. These are not blanket acceptance or risk deferrals. The previous no-transition records below are historical, before this authority/action.

The 142 main source corrections comprise all 122 Shell findings and 20 Python findings. POSIX argument bindings, intentional no-op defaults and condition merges preserve quoting, status and cleanup boundaries; no Bash-only local, exclusion or suppression is introduced. Python changes isolate metadata/coverage responsibilities, preserve same-descriptor evidence and invocation-only component approvals, keep ASCII validation explicit, and isolate the intended exception call in tests. At that development point, fresh scan closure remained required; local correction alone was not “Behoben”. Later measured closure is recorded above.

### Historical native causes and development probes

The full current scanner log identifies missing `ngx_http_v2.h`. Actual CI installed `libmodsecurity-dev` 3.0.12; its headers lack `msc_rules_error_cleanup` and `msc_intervention_cleanup`, used by unchanged `common/scripts/modsecurity_targeted_eval.cc` at 391/456. An authentic upstream 3.0.12-header negative probe reproduces those failures in `RuleErrorCleanup`/`main`; the exact Framework-approved 3.0.17 headers compile the same evaluator with C++17 and warnings as errors. This proves an SDK/header incompatibility, not a product-cleanup defect.

The new header acquisition reads passive source data from exact Framework gitlink `99a7985c1be92a2297b1b59208f64df6768f2cbf`, blob `496b5d8e0ec70d6d31f91aeaf08024050a5698ea`, which approves official ModSecurity commit `1925753989ccce977cdaae417b55c9726c7cf02c` / `v3.0.17`. The materialized headers tree is `8daab1d1734506b687b21efd44169c273eabca6a`. Private external filtered Git stores validate commit/blob identities; only required contract/header data is materialized. Framework/MRTS checkouts and gitlinks are not changed. Actual approved headers precede generic system includes; actual pinned `src/http/v2` supplies the conditional dependency without inventing `NGX_HTTP_V2` or altering H1 configure behavior.

The complete development preparation passed: real NGINX configure, canonical patched-lighttpd bootstrap/configure, approved SDK and unchanged evaluator syntax probe; 13 include directories and 11 file hashes recorded. Its source is dirty development at `1aa9646a`, not clean-head CI. Remaining aggregate parsing/include closure must come from the next scan. No partial compilation database replaces AutoConfig; independent targets and stock/patched/feature variants retain their explicit limits. C/C++ taint is unsupported in AutoConfig and when analyzing multiple variants; a higher parsing score cannot prove it ran. [Official CFamily limits](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis#taint-analysis).

### Verification and separate diagnostics before the source scan

The measured Python producer passed 80 methods in 7.829 s; 44 affected metadata/boundary/coverage/report methods passed in 4.711 s. Native helper validation passed 11 methods. Independent security validation passed 15 attack/allowed groups on both immutable and frozen candidate source, plus malformed Git-identity/nonliteral-contract and literal real-Git argument controls. Shell batches passed 17 Envoy and 12 host methods, 42 Envoy before/after cases and nine lighttpd behavior cases. Syntax passed; ShellCheck retains six existing Envoy and twelve existing HAProxy diagnostics, so no whole-ShellCheck-green claim is made.

Hotspots are completely zero in the main PR and both advisory branches. All GitHub annotation pages reconcile **92/92**: 50 Sonar inline issue references, 36 runner-image notices, two actual Go-cache configuration warnings, three scanner-exit annotations and one CodeQL overlay/full-database fallback warning. These are separate from the 150 issues. The two Go jobs now key cache data from their actual module files; Actionlint, Zizmor and three existing CodeQL trusted-version/lock/permission checks passed. Current CI is needed to prove those warnings gone.

The missing-blame file is a normal tracked file, not an omitted source or shallow-checkout assumption. It contains one literal CR inside a valid Shell pattern: Git counts 28 LF lines while universal readers count 29. Representing that same CR with quoted `$(printf '\r')` yields 28/28 without changing matching. Twelve actual old/new Shell cases have identical status/stdout/stderr; the real TLS materializer tests pass for allowed escaped paths and rejected LF/CR without output. This is a pre-existing source-encoding compatibility correction; a new analysis must confirm blame recovery. FIFO `exec 8<>` remains unchanged. Python sink-cost/predecessor messages have already been demonstrated in baseline scans; they remain separately bounded analyzer gaps, not an asserted PR regression.

Official source verification confirms signed scan Action `v8.3.0`, Scanner `8.2.0.6438`, Python 3.14, current Go, Bash/POSIX, Actions and generic JSON/YAML interfaces and genuine Python/four-module Go/gcov import parameters. The rolling scanner documentation index lagging at 8.1 is not evidence that the official stable 8.2 release is unsupported. [Scanner release](https://github.com/SonarSource/sonar-scanner-cli/releases/tag/8.2.0.6438), [Action interface](https://github.com/SonarSource/sonarqube-scan-action/blob/v8.3.0/action.yml), [coverage parameters](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/test-coverage-parameters).

### Architecture application remains externally blocked

Fresh full server comparison reproduces exactly 14 Framework/MRTS-group removals and 30 Parent-label renames, preserving other model fields, nested groups and constraints. The canonical PATCH again returns HTTP 415 and full readback is unchanged. Installed CLI `1.10.1.16776` is also the latest official released client, commit `ef0f792b7c4bb18d2432015baae4984a6cd50d99`: its API options expose only data/verbose, and transport supports JSON/form without header override. `application/merge-patch+json` cannot be selected. Unreleased master architecture commands are not an installed/released supported route. No client update, raw-token operation or alternate credential wrapper is used. [Exact released API implementation](https://github.com/SonarSource/sonarqube-cli/blob/ef0f792b7c4bb18d2432015baae4984a6cd50d99/src/commands/api/api.ts), [transport](https://github.com/SonarSource/sonarqube-cli/blob/ef0f792b7c4bb18d2432015baae4984a6cd50d99/src/core/server/http-client.ts).

The supported external handoff remains: back up/review current model, integrate an authorized supported merge-patch-capable client with the required authentication path, PATCH the exact prepared body, compare readback, then run a new exact-head analysis showing the perspective applied. No unverified UI editor/import capability is prescribed. The 44 ignored labels remain an external technical blocker.

### Readiness requirements and pending closure before the source scan

Active master ruleset `19138299` requires exactly `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, `zizmor`, strict up-to-date base and resolved review threads. Required approvals are zero; current reviews/threads are empty. The installed GitHub CLI's supported authenticated GET resolves the connector's initial access limit: classic protection returns 404 “Branch not protected”; the active ruleset remains authoritative. Sonar is not a GitHub ruleset-required context, but repository delivery policy requires the applicable current-head Sonar gate to pass. Advisory names alone do not make them GitHub-required.

All 18 non-Sonar workflows and selected Apache/CRS runtime at starting `1aa9646a` were terminal success. That selected-block/audit/cleanup proof is not a complete runtime matrix; current artifact ZIP bytes were not independently downloaded/verified. Historical PR coverage 82.3%, advisory new-code coverage 83.7% and accumulated master coverage 0.6% remain separate. New reports, gate conditions, native warning results and full old/new issue comparison must be bound to the new clean final head.

Overall status remains **teilweise abgeschlossen/blockiert**, Draft, until current-head validation and required technical criteria are satisfied. No merge, master push, force-push, threshold/profile reduction or broad exclusion is authorized or performed. The measured source ledger above supersedes this earlier development status. The final clean-head tasks, analyses, conditions and CI outcomes are reconciled in the PR after each push; an older scan never substitutes for them.

## Historical evidence before the full-inventory continuation

The following records describe earlier source/analysis snapshots and the former absence of issue-transition authority. They are retained as history, not current issue counts or current OPEN/authorization claims.

### Main-project security decision records

Complete readback at `59bc0842` retains the three original OPEN `pythonsecurity:S2083` vulnerabilities for PR 421; five new helper findings are assessed separately below. The three full flows match the previous exact-head records. Every flow starts at JSON file content in `run-native-case-comparison.py:129`, selects `report["request"]` at 668, passes the return at 726–732, `run_requested_cases:1237`, main 1265–1268, `write_summary:1100–1118`, `reader.file_proof:1122`, `EvidenceInputs.file_proof:93–94`, and `_descriptor:41` before the sinks below.

The field distinction matters: `request` is data, while consumed `run_dir` is constructed from invocation context at 658 and private runtime directories at 433–436. No assignment from the tainted request to `run_dir` was found. `latest_case_runs:866` replaces stored `run_dir` with the actual loaded directory. The caller independently authorizes `native-case-runs` at 1109 and fixes the leaf `native-case-run.json` at 1118.

| Issue | Complete flow | Concrete controls and attack/control pairing | Proposed decision |
| --- | --- | --- | --- |
| `AaF0ynIMY4cSrRUGTduD` | 1 flow, 44 locations; `evidence_inputs.py:47` | `_absolute` rejects relative paths, `..` and NUL; `path()` checks invocation-owned roots/files. `path.anchor` is only POSIX `/` or `//`, opened with `O_NOFOLLOW\|O_DIRECTORY`. External stored `run_dir`/root-grant attacks are rejected; legitimate confined metadata remains readable. No protected file bytes are read at this anchor. | False Positive candidate, high confidence for reviewed Linux/POSIX contract; status remains OPEN. |
| `AaF0ynIMY4cSrRUGTduC` | 1 flow, 47 locations; `evidence_inputs.py:51` | Each intermediate component is a single name relative to a held directory descriptor, with `O_NOFOLLOW\|O_DIRECTORY`; unsupported platform flags fail closed. Intermediate links, sibling-prefix and traversal attacks fail; nested regular records succeed. | False Positive candidate, high confidence; status remains OPEN. |
| `AaF0ynIMY4cSrRUGTduB` | 1 flow, 44 locations; `evidence_inputs.py:54` | Fixed leaf uses `O_NOFOLLOW\|O_NONBLOCK`; `fstat` requires a regular file. Hashing reads the same descriptor without reopening. Final-link and replacement-before-open attacks fail; regular input produces the expected hash. | False Positive candidate, high confidence; status remains OPEN. |

The nine named existing tests below were actually run by the independent security reviewer: **9 passed, 0.350 s, exit 0**. Prefix each indented method with its preceding class selector:

```text
tests.test_evidence_input_security.EvidenceInputSecurityTests.
  test_read_and_hash_use_a_regular_file_in_an_explicit_root
  test_rejects_sibling_prefix_traversal_and_final_or_intermediate_links
  test_replacement_before_final_open_cannot_follow_a_link
  test_empty_or_filesystem_root_allowlists_cannot_grant_arbitrary_access
  test_jsonl_parser_keeps_valid_objects_and_ignores_malformed_rows
tests.test_sonar_evidence_boundaries.SonarEvidenceBoundaryTests.
  test_latest_native_record_retains_its_actual_loaded_directory
  test_supplied_native_records_cannot_authorize_external_metadata_inputs
  test_native_metadata_uses_fixture_identity_and_confined_record_bytes
  test_latest_native_record_does_not_follow_a_link
```

The repository-relative command form is `rtk bypass env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 TMPDIR=/var/tmp/codex/ModSecurity-conector .venv/bin/python -m unittest -v` followed by these nine complete selectors. The executed command selected the Parent virtual environment by its absolute path; its local location is not a reader prerequisite. All byte/stat/JSON/proof reader APIs use `_descriptor`; `path()` alone only grants lexical approval. These tests do not prove protection against privileged mount substitution, hard links, or an authorized writer changing bytes. POSIX backslashes, encoded slashes and Unicode lookalikes are literal names; there is no URL decoding.

Decision ready for an authorized issue administrator, separately for each row: retain the issue ID and its exact flow, attach the corresponding controls and named attack/control results, verify the current source revision, and propose **False Positive** for the reviewed flow. No issue comments or status updates were published. Technical counterevidence does not itself grant transition authority; [Sonar issue editing](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/issues/editing) also requires the relevant issue permission and changes gate metrics.

### Independent advisory decisions

The table concerns the **complete historical 23-issue snapshots per advisory at `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`**, independently reviewed against source. All 23 pairs have equal rule, path, line, message and complete normalized flows, differing only by project prefix. Their judgments were not inherited from the three main issues. Proposed outcomes are **22 pairs `not_actionable`, one pair `needs_review`**, with no server transitions. This was a source review; the advisory reviewer ran no tests and does not establish per-pair dynamic coverage.

| C++20 issue | C++23 issue | Sink | Independent counterevidence / decision |
| --- | --- | --- | --- |
| `AaF0yzxvaVChWkKVlx8R` | `AaF0y14uF0XFUMkHWcpz` | `evidence_inputs.py:47` | Absolute root allowlist; directory anchor with no-follow. |
| `AaF0yzxvaVChWkKVlx8Q` | `AaF0y14uF0XFUMkHWcp0` | `evidence_inputs.py:51` | Single-component traversal relative to held no-follow directory descriptors. |
| `AaF0yzxvaVChWkKVlx8S` | `AaF0y14uF0XFUMkHWcpy` | `evidence_inputs.py:54` | Fixed leaf, no-follow/nonblocking, regular-file fstat and same-descriptor proof. |
| `AaF0ZnLmLhxv2LRQWeOE` | `AaF0Zlbb7GRUxAPzGll5` | `framework_revision_pins.py:106` | ASCII lowercase 40-hex SHA before fixed Git argv; no shell. |
| `AaF0ZnLpLhxv2LRQWeOF` | `AaF0Zlbd7GRUxAPzGll6` | `prepare-reviewed-framework-handoff.py:292` | Explicit operator output; exclusive creation, never applies the patch. |
| `AaF0ZnM8Lhxv2LRQWeOX` | `AaF0Zlcx7GRUxAPzGlmM` | `hostruntime_preflight.py:169` | Approved runtime/source lock before descriptor-backed read; rejected input fails closed. |
| `AaF0ZnMyLhxv2LRQWeOU` | `AaF0Zlco7GRUxAPzGlmJ` | `write-transport-lifecycle-artifacts.py:487` | Config hash inputs restricted to runtime/source or invocation-selected canonical Framework root. |
| `AaF0ZnMuLhxv2LRQWeOT` | `AaF0Zlcj7GRUxAPzGlmI` | `resolve-full-lifecycle-profile.py:243` | Input passes runtime_or_source_artifact_path before loading. |
| `AaF0ZnM0Lhxv2LRQWeOV` | `AaF0Zlcq7GRUxAPzGlmK` | `run-full-matrix-job.py:139` | Canonical runtime context, validated run ID, fixed subprocess argv. |
| `AaF0ZnMrLhxv2LRQWeOS` | `AaF0Zlch7GRUxAPzGlmH` | `run-full-matrix-resume.py:88` | Canonical roots, runtime ownership and run ID before fixed completeness command. |
| `AaF0ZnMrLhxv2LRQWeOR` | `AaF0Zlch7GRUxAPzGlmG` | `run-full-matrix-resume.py:165` | Allowlisted connector/CRS/MRTS and bounded decimal timeout; shell=False. |
| `AaF0ZnMCLhxv2LRQWeOK` | `AaF0Zlb57GRUxAPzGll_` | `run-verified-case.py:85` | Stored JSON is payload; generated case-run.json destination checked immediately before writing. |
| `AaF0ZnMCLhxv2LRQWeOL` | `AaF0Zlb57GRUxAPzGlmA` | `run-verified-case.py:85` | CLI tokens, owned runtime root and generated timestamped directory constrain destination. |
| `AaF0ZnMPLhxv2LRQWeOQ` | `AaF0ZlcF7GRUxAPzGlmF` | `run-verified-report-run.py:1838` | needs_review: current-run-id read preceded runtime ownership validation; leaf symlink/FIFO read was unguarded. |
| `AaF0ZnL-Lhxv2LRQWeOJ` | `AaF0Zlb07GRUxAPzGll-` | `write-engine-lifecycle-artifacts.py:59` | Approved Framework/rules or runtime/source input, no alias, no-follow regular-file hashing. |
| `AaF0yz5SaVChWkKVlx_W` | `AaF0y2C0F0XFUMkHWcs4` | `bounded_cstring_length:52` | NUL-terminated literal crs-setup.conf reaches sequential memchr through join_path. |
| `AaF0yz5SaVChWkKVlx_X` | `AaF0y2C0F0XFUMkHWcs5` | `bounded_cstring_length:52` | Same independent flow check for literal crs-setup.conf.example. |
| `AaF0yz5SaVChWkKVlx_Z` | `AaF0y2C0F0XFUMkHWcs7` | `bounded_cstring_length:52` | Same independent flow check for literal rules. |
| `AaF0ZnPCLhxv2LRQWeOv` | `AaF0Zlex7GRUxAPzGlmk` | `patched_event_validation.py:17` | Explicit --events operator input; harness supplies fixed SMOKE_DIR/phase4-barrier-events.jsonl. |
| `AaF0ZnM4Lhxv2LRQWeOW` | `AaF0Zlct7GRUxAPzGlmL` | `HTTP fixture:212` | Backend binds literal 127.0.0.1; no wider-bind option. |
| `AaF0ZnPdLhxv2LRQWeOw` | `AaF0ZlfL7GRUxAPzGlml` | `HTX helper:414` | Validated port and loopback backend; frontend TLS configured separately. |
| `AaF0ZnMPLhxv2LRQWeON` | `AaF0ZlcF7GRUxAPzGlmB` | `run-verified-report-run.py:1743` | Stored JSON is manifest payload; canonical registry report_path selects output. |
| `AaF0yz5SaVChWkKVlx_Y` | `AaF0y2C0F0XFUMkHWcs6` | `bounded_cstring_length:52` | POSIX readdir d_name terminator; suffix check, no intervening readdir before use. |

The marker pair exposes an incomplete earlier counterclaim: canonical `current-run-id` construction did not establish leaf safety or validation order. Harmless regression probes reproduced a symlink read and an external overwrite through public preparation; a legitimate regular marker control passed. The source repair now checks directory trust before reading, holds a no-follow/nonblocking parent/leaf descriptor, requires an owned regular non-group/world-writable single-link file, bounds reads to 4,096 bytes, validates the ID before environment mutation, and writes atomically as 0600. Legacy owned 0644 markers, 0755 directories, surrounding whitespace, missing-marker behavior, append phases and explicit-ID priority are preserved. Sixteen evidence-boundary tests and eight affected runtime security/ID/atomic-write tests passed; an independent reviewer ran the previous seven marker cases successfully and found no concrete surviving bypass in those cases. A final Root check then reproduced, with the eighth marker test, acceptance of a valid prefix when a short os.read preceded invalid trailing bytes. A bounded read loop through EOF or at most 4,097 bytes fixes this; the new test failed before correction and all 16 boundary tests passed afterward. This eighth case was not covered by the previous independent seven-case review. This is local boundary verification, not final-head Sonar closure, concurrent-race execution or a remote-exploit claim. Fixed basename, later strict run-ID validation, explicit `VERIFIED_RUN_ID` precedence and later root checks are relevant counterevidence but did not cover the earlier operation.

Operator-selected output/Framework roots do not authorize arbitrary paths for a future privileged wrapper. Loopback binding is not isolation from other local principals or production HTTP qualification. The four `memchr` cases rely on the actual NUL-terminated literals/`dirent` names and sequential first-match semantics, not on the quality score: [C N1570 §7.24.5.1 ¶2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [POSIX dirent](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/dirent.h.html).

A later live project snapshot belongs to unrelated revision `209ab41a16cc34c88e3dc23d312eada0a38a8169`: C++20 analysis `bd46227f-a29a-4e0b-8a4c-4f9c70499854`, C++23 `93ef6dc3-f223-42a4-a0cf-38c31cdf851d`. Its issue result reports total 110 but contains only the first 100. That partial, unrelated snapshot cannot prove PR 421's current count, disposition or closure.

### Architecture: reviewed change, blocked application

Fresh server readback of model `cb04d3a3-7c8f-447c-99f0-ca49c97f054f` for project UUID `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2` was compared with [the exact proposal](../config/analysis/sonar-python-architecture.patch.json). Of 46 top-level groups, 44 invalid slash labels are addressed by removing 14 excluded Framework/MRTS groups and renaming 30 Parent labels from `/` to `_`. Parent patterns, four nested groups, metadata and `constraints: []` are preserved; no rules are invented or removed from the retained Parent architecture.

Canonical CLI `1.10.1` exposes `--data` and `--verbose`, but no header/content-type option. A fresh reviewed PATCH through `rtk bypass /usr/local/bin/sonar-with-env` again returned **HTTP 415 Unsupported Media Type**. Before/after readback is identical. No Sonar MCP capability was available. This is a client media-type limitation, not evidence of missing server administration permission. The perspective remains ignored; successful model application and a confirming new analysis are **extern blockiert**.

Supported-access handoff, preserving authentication policy:

1. Back up authenticated `GET /api/v2/architecture/models?projectId=608d0a7b-481a-4f7e-acbf-ae8eb07c3be2` through the canonical wrapper; compare the model ID and entire current model with the reviewed baseline before changing it.
2. Use an authorized supported client that can send `PATCH /api/v2/architecture/models/cb04d3a3-7c8f-447c-99f0-ca49c97f054f` with **`Content-Type: application/merge-patch+json`**, using the exact proposal as its body. The shown paths are the canonical CLI paths; retain the client's documented SonarCloud API-host routing. Approve/integrate that client's authentication with the required wrapper rather than extracting a token or bypassing it.
3. Read back through the approved path and compare the exact 14 removals/30 renames, preserved patterns, nested groups and constraints. If state drifted, review a new diff first.
4. Run a new clean exact-SHA analysis and retain its terminal server task, analysis ID and log demonstrating that this perspective is applied without the 44 invalid-label warnings.

No unverified UI import/editor capability is prescribed. The deprecated `sonar.architecture.configpath` is not a workaround: see [Web API](https://docs.sonarsource.com/sonarqube-cloud/appendices/web-api) and [deprecations](https://docs.sonarsource.com/sonarqube-cloud/deprecations-and-removals).

### Native context and taint limits

At historical `4ec75810`, all **136 native translation units** remain in scope: quality **91.28/100**, parsing errors **193/2,260 functions**, unresolved project includes **46/1,132**. This improves the baseline 77.52/414/115 but is not a completion criterion. Actual pinned host context is NGINX `1.31.6`, HAProxy `3.2.25`, and patched lighttpd `1.4.85`. NGINX requires real configured `objs/ngx_auto_config.h`/`ngx_auto_headers.h` and its actual include paths; HAProxy's Linux/OpenSSL feature context is target-specific; lighttpd requires matching patched source and generated configuration.

The existing partial compilation database contains NGINX's 33 sources and a single C++ evaluator context, not all Parent units/variants, and filters copied HTX sources without a complete provenance mapping. Replacing AutoConfig with it would lose coverage. The source-pinned native context helper reads existing contracts as data, verifies archive checksums and records generated-header/include provenance. Six focused helper tests passed. A real development probe configured NGINX successfully, then failed because the new lighttpd patch invocation with --fuzz=0 differed from the existing native apply_core_patch.sh path. The second probe passed actual NGINX configure and the unchanged canonical lighttpd patch/stamp/ABI path (its actual fuzz2/fuzz1 applications are retained in the log), then stopped before lighttpd configure because the approved archive contains no configure script. The third real complete header-preparation run passed with exit 0: unchanged upstream autogen with installed tools and Bash for the ERR trap, actual patched-lighttpd configure, and generated header/config hashes. Its manifest records revision `4ec7581056889f8c70f44c6725f6bfa65a7fc45b` with `uncommitted_changes: true`, eleven real include directories, archive/patch/configure provenance and generated-file hashes. This is development evidence, not a new Sonar count. No component-owned script changed. The workflow measures the helper under Python coverage before finalization; the selected suite now contains 75 methods (61 existing, eight marker, six header tests). The fresh instrumented local selection passed all 75 tests in 7.256 s. New-helper development coverage is 82.48% for lines and branches, not a Sonar gate result. Clean-head CI remains required. No fabricated headers, guessed global defines or compiler commands are justified.

The implementation is [prepare-sonar-native-context.py](../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_ci/checks/analysis/prepare-sonar-native-context.py), with six focused regressions in [test_sonar_native_context.py](../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_tests/test_sonar_native_context.py). The successful run uses fresh external directories; local development artifacts are not reused as clean CI reports.

[Supported CFamily customization](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis) permits real include properties. **C/C++ taint is unsupported in AutoConfig**, and cross-translation-unit analysis cannot silently treat independently executable connector targets and incompatible variants as one linked program. Complete variant-preserving compilation context and explicit C/C++ taint proof remain **weiterhin offen** / **begründete Analyzergrenze**, respectively.

### Python analyzer boundaries and Shell

Both full advisory scans emit these exact messages during Python security analysis:

```text
Too high simulation costs for sink in ci/lib/runtime_path_utils.py:69. This sink will not be analyzed any further.
'21' appears to be a predecessor of '20' but this has already been handled.
'15' appears to be a predecessor of '14' but this has already been handled.
```

The same three messages already occurred for baseline `9f44647593bac7947113558c6ad183ab118e80af` in [run 40224506735](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40224506735), main job `121262911582`, C++20 `121262911602`, C++23 `121262911515`. They recur in the exact-head full advisories, jobs `121288719031`/`121288718833` of [run 40233061104](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061104). `runtime_path_utils.py` is unchanged between these revisions. This is a demonstrated pre-existing boundary, not an established PR regression.

The sink is `_contains_symbolic_link`'s `absolute.resolve(strict=False) != absolute`, reached through runtime-path/ownership validation and callers such as `prepare-verified-runtime-paths.py` and compilation capture. Full advisories retain 5,253 UCFGs/166 entry points from 15,724 total and apply 32 taint rules; baseline retained 5,227/169 from 15,660. The main PR's absence of these messages only reflects a cached analysis of 16 changed/new files, 12 entry points and 1,187 retained UCFGs. It does not demonstrate repair. The cost guard skips further analysis of this sink, not the whole file/language or all 32 rules; its exact missed paths and rule are unquantified. Predecessor node numbers cannot be mapped to source from these INFO/WARN messages alone.

SonarSource describes a hardcoded guard against exponential branch exploration with no configurable disable switch: [cost-limit explanation](https://community.sonarsource.com/t/how-to-avoid-high-simulation-costs-for-sink-in-error/107841/3). A [related predecessor discussion](https://community.sonarsource.com/t/warnings-during-taint-analysis-for-java/141163) requests verbose diagnostics; it concerns Java and is not a proven Python remedy. No heap/timeout change is established as a fix. Controlled, secret-safe debug capture would be a separate diagnostic step and was not enabled. These are **begründete Analyzergrenze** with a residual taint-coverage gap.

Five of six original Shell parser cases are absent at the identified head. `ci/runtime/lifecycle/run-full-matrix-parallel.sh` retains valid `exec 8<>` bidirectional FIFO semantics; the remaining parser warning is a **begründete Analyzergrenze**. No file exclusion or semantically different redirection is applied.

### Runtime and coverage readback

[Runtime run 40233061042](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061042) is terminal **SUCCESS** for all five connector jobs and the aggregate job. Apache job `121290821692` passed actual `RUN_ONE_CASE=1 make verified-apache-case CASE=crs_sqli_anomaly_block CRS=with-crs MRTS=no-mrts`: selected case denied HTTP 403 with rule `942270`; audit, cleanup, selected-results and artifact validation passed. There is no observed failed Apache job to repair.

Identity: Parent `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`; Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; CRS `e03a4f6dabc7a30ebd8c52c97d28a154f590a48f`; profile `with-crs-no-mrts-40233061042-1`, Apache cell `crs-40233061042-1-apache`, logical profile `native-httpd-module`.

Apache compact artifact `12614940472` was downloaded/read in memory and its SHA-256 matched GitHub's digest: `4da09921b83210e54028d449f33dd544d044e54b7de48caaced00a69de7c8832`. It contains exactly `functional-facts.json`, `manifest.json`, `profile-cell-receipt.json`; raw audit/results are hash references, not included raw evidence. Aggregate artifact `12614138658` reports technical PASS for five cells and functional PASS limited to `selected_crs_block_case_only`: **5 passed, 0 failed, 6 blocked, 13 not_run**, `coverage_complete: false`, `merge_eligible: false`. Apache/HAProxy allow controls are `not_observed`; no-MRTS is workflow/source-declared for them. Other cells retain host/Framework attestation limits. Green CI therefore does not qualify the full runtime matrix.

Actual Python XML, all four Go module reports and 71 native gcov reports were imported. Main PR new-code coverage **80.5%** passes the unchanged 80% condition; advisory branch new-code coverage is **82.7%**. Accumulated `master` previous-version coverage **0.6%** remains a separate baseline claim and has not been repaired or raised to 80% by this PR. All 18 non-Sonar workflows at the identified head are terminal success.

### Historical exact-head Sonar ledger

All rows are historical exact-head evidence for `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`, scanner `8.2.0.6438`, CFamily `6.85.0.102562`, [run 40233061104](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061104). Upload alone is not completion.

| Project | CE task | Analysis ID | Terminal processing / gate |
| --- | --- | --- | --- |
| Main, PR 421 | `AaF03ulBdkEpBguA0oKZ` | `081d99d7-c136-4a67-b039-96507ad472a4` | SUCCESS; ERROR solely new-code Security Rating E / three issues. Coverage, reliability, maintainability, duplication and hotspot review pass. |
| C++20 advisory branch | `AaF03nsWdkEpBguA0oJ9` | `e29a042c-b9e6-4ffa-b6e4-f463dce07c34` | SUCCESS; ERROR. Independent advisory findings remain; new-code coverage 82.7% passes. |
| C++23 advisory branch | `AaF03alqJ8I9a074ReRm` | `0fdc39d6-930f-4ae9-bdf3-876d7670b4d3` | SUCCESS; ERROR. Independent advisory findings remain; new-code coverage 82.7% passes. |

At all three analyses, unchanged gate conditions are `new_reliability_rating <= 1` (actual 1), `new_security_rating <= 1` (actual 5, ERROR), `new_maintainability_rating <= 1` (actual 1), `new_coverage >= 80` (actual main 80.5, advisories 82.7), `new_duplicated_lines_density <= 3` (actual 0.0), and `new_security_hotspots_reviewed >= 100` (actual 100.0). No conditions were ignored.

The eight new marker tests are `test_current_run_marker_rejects_outside_symlink_before_restore`, `test_current_run_marker_fifo_fails_without_waiting_for_a_writer`, `test_current_run_marker_cannot_alias_an_outside_hardlink`, `test_current_run_marker_rejects_oversized_input_without_unbounded_read`, `test_current_run_marker_checks_directory_trust_before_reading`, `test_owned_legacy_marker_preserves_append_and_explicit_id_behavior`, `test_current_run_marker_does_not_accept_a_valid_prefix_after_short_read`, and `test_public_prepare_cannot_overwrite_an_outside_marker_target`, in `tests.test_sonar_evidence_boundaries.SonarEvidenceBoundaryTests`.

The historical three jobs preserve genuine coverage, 1,345 source/242 test files, 136 native units and four Go modules. The architecture warning, native counts, FIFO parser warning and full-advisory Python warnings above remain attached to that revision. Query exact CE activity/task and analysis IDs with scanner-context SHA; project-latest and unsupported `api/ce/component?pullRequest` filtering are insufficient PR proof.

### Source-change scan and new decisions

All three jobs in [run 40238653971](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40238653971) completed against clean `59bc0842cea90d4052c0d005218fae3aca14c2b2`, with scanner `8.2.0.6438` and CFamily `6.85.0.102562`. Server processing is terminal SUCCESS; all actual gates remain ERROR solely on Security Rating E. The unchanged other conditions pass: reliability/maintainability 1, duplication 0.0%, hotspot review 100%, coverage at least 80%. No conditions were ignored.

| Project | CE task | Analysis ID | New-code coverage / open vulnerabilities |
| --- | --- | --- | --- |
| Main PR 421 | `AaF1HfLSwSmsgR9Bxyj2` | `cb8fbb9c-1342-45f1-9b45-fb7f427d7a8c` | 82.3% PR coverage; 8 issues |
| C++20 advisory | `AaF1JGXMnC1ELI2PKeSx` | `b7c0cc6c-1f55-4195-81be-bbc6e01cf13b` | 83.7% branch new-code coverage; 27 issues |
| C++23 advisory | `AaF1INr6oFotzZs8r-QJ` | `bb234bff-19a3-4929-8eaf-df9f71b6ade4` | 83.7% branch new-code coverage; 24 issues |

Each job passed its real header-preparation and coverage producers, imported Python XML, four Go reports and 71 gcov reports, and retained **1,348 source/243 test files, 136/136 native units and four Go modules**. Real host context reduces native function errors to **2/2,263**, unresolved project includes to **0/1,132**, with quality **95.81/100**. The logs additionally report one class with errors out of six, seven statements out of 33,762 and one unresolved external include. They expose no source locations for these remaining aggregate failures; those locations and complete target/variant context remain open. C/C++ taint is still explicitly disabled in AutoConfig: the higher score proves no taint closure.

Both advisories still report the Python cost skip and two predecessor warnings: 15,738 total UCFGs, 167 entry points, 5,269 retained, 32 Python taint rules. Main PR analysis retains 1,207/13 from the same total, with 18 changed/new files; its absence of these messages proves no repair. The FIFO warning persists in all three. Main still ignores the architecture perspective because of 44 labels. Both advisories also report missing blame for `connectors/envoy/config/lib/tls_yaml_render.sh`; this tracked file's last local commit is `75ea06c3cbcf1f909dae9e101faa528229316b80`. No coverage-import warning was observed.

The repaired marker issue `AaF0ZnMPLhxv2LRQWeOQ` / `AaF0ZlcF7GRUxAPzGlmF` is absent from both complete advisory inventories without a status mutation. Together with the regression tests, this proves the scoped marker repair. The separate manifest issue `AaF0ZnMPLhxv2LRQWeON` / `AaF0ZlcF7GRUxAPzGlmB` remains at 1745: the loaded JSON affects payload bytes, while `report_path(connector_root, "verified_run_manifest", "json")` fixes the destination. No additional dynamic manifest attack test was run. C++23 additionally omits the three unchanged evidence-reader findings still retained by C++20/main; this difference does not establish why they disappeared and is not treated as an authorized closure or equivalent current inventories.

Five new helper flows were independently reviewed in full, starting at explicit CLI `--output-root` and `fresh_root`; they are not inferred from the original three issues. Each row is a separate False Positive proposal for the fixed CI caller and validated operator-output contract, with no status change:

| Sink / rule / flow locations | Main issue | C++20 issue | C++23 issue | Concrete counterevidence |
| --- | --- | --- | --- | --- |
| 86 / S8707 / 9 | `AaF1HfgA7GRUxAPzPdPg` | `AaF1JG-OgQ6c6GT2j3RO` | `AaF1IOniIES1tmkRWQi0` | Absolute, narrow, fresh external root; rejects traversal, system/source/broad paths, existing paths and symlinks; creates mode 0700. |
| 119 / S8707 / 18 | `AaF1HfgA7GRUxAPzPdPh` | `AaF1JG-OgQ6c6GT2j3RM` | `AaF1IOniIES1tmkRWQi2` | Fixed sources child, SHA-256-verified archive, expected top-level and no absolute/traversal members, `data` extraction filter. |
| 129 / S8705 / 18 | `AaF1HfgA7GRUxAPzPdPe` | `AaF1JG-OgQ6c6GT2j3RK` | `AaF1IOniIES1tmkRWQiz` | Fixed executable/argv without shell; output occurs inside a single `--prefix=` or equivalent destination argument. |
| 180 / S8707 / 17 | `AaF1HfgA7GRUxAPzPdPi` | `AaF1JG-OgQ6c6GT2j3RL` | `AaF1IOniIES1tmkRWQi1` | Fixed sources/downloads/logs children of validated private root. |
| 211 / S8707 / 13 | `AaF1HfgA7GRUxAPzPdPf` | `AaF1JG-OgQ6c6GT2j3RN` | `AaF1IOniIES1tmkRWQi3` | Fixed lighttpd-build child of that root. |

The six named tests in `tests.test_sonar_native_context.SonarNativeContextTests` pair invalid archive hash/traversal, redirected/source/existing output, missing/link artifacts and ambiguous includes with allowed regular archives/private output/configured headers. An independent run passed all six (0.020 s). Additional bounded probes rejected eight roots (relative, dot-dot, `/etc`, `/usr`, newline, comma, NUL, source tree); an allowed root passed mode 0700. A real Python child received spaces, semicolon and command-substitution text as one literal prefix argument; no sentinel was created. The workflow fixes output to invocation-owned `RUNNER_TEMP/sonar-native-context`. These checks do not prove protection against hostile same-user concurrent path replacement or every upstream configure pathname behavior.

Five non-Sonar workflows at `59bc0842` failed solely because both new closeout documents contained a local developer path. The portable correction passes `check-variable-documentation` locally (101 references), bilingual, path and link checks. A fresh documentation-head run is required; the failure is not hidden by changing the validator. The current final-head CI/server ledger belongs in the PR readback, rather than treating this source-change run as final proof.

| Requirement | Disposition at this documentation update |
| --- | --- |
| Three main issues | **weiterhin offen**: precise False Positive decision records prepared; no authorized transitions or green final gate. |
| Five new helper findings per project | **weiterhin offen**: independent full-flow counterevidence and attack/control probes support individual False Positive proposals; no transitions. |
| Advisory marker defect | **behoben und nachgewiesen** at the source-change head: regression controls pass and the specific issue is absent in both fresh advisories. Other issues retain independent decision proposals. |
| Architecture perspective | **extern blockiert**: reviewed exact delta, repeated HTTP 415, unchanged server state; supported-media-type application and rescan required. |
| Native parsing/includes | Project includes **behoben und nachgewiesen**, 0/1,132; parsing **weiterhin offen**, 2/2,263 functions, unlocated aggregate failures and incomplete target/variant context. |
| C/C++ taint / Python cost and predecessor / FIFO | **begründete Analyzergrenze** as scoped above, with residual gaps retained. |
| Previous Apache CI uncertainty | **behoben und nachgewiesen** for the selected runtime run/case; full runtime qualification remains open. |
| Coverage and scope preservation | **behoben und nachgewiesen** at the source-change head, 82.3% PR / 83.7% advisory new-code coverage and real imports; no accumulated master-coverage claim. |
| Final completion proof | **weiterhin offen**: obtain new exact-head CE/analysis/gate/coverage/warnings for all three projects and terminal CI after source changes. PR stays Draft. |
