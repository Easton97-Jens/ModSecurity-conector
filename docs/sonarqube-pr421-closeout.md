# PR #421: Sonar and CI closeout evidence

**Language:** English | [Deutsch](sonarqube-pr421-closeout.de.md)

This records the targeted continuation of [Draft PR #421](https://github.com/Easton97-Jens/ModSecurity-conector/pull/421). The last fully identified PR analysis is commit `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`; subsequent working-tree repairs require a fresh clean-head analysis. No merge, `master` mutation, issue transition, gate reduction or broad exclusion is claimed. The [Change Record](../reports/audits/change-records/CR-20261025-sonar-setup-remediation.md) preserves development history.

## Main-project security decision records

Fresh complete readback returned exactly three OPEN `pythonsecurity:S2083` vulnerabilities for PR 421. Full flows match the previous exact-head records. Every flow starts at JSON file content in `run-native-case-comparison.py:129`, selects `report["request"]` at 668, passes the return at 726–732, `run_requested_cases:1237`, main 1265–1268, `write_summary:1100–1118`, `reader.file_proof:1122`, `EvidenceInputs.file_proof:93–94`, and `_descriptor:41` before the sinks below.

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

The command used `rtk bypass env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 TMPDIR=/var/tmp/codex/ModSecurity-conector /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v` followed by these nine complete selectors. All byte/stat/JSON/proof reader APIs use `_descriptor`; `path()` alone only grants lexical approval. These tests do not prove protection against privileged mount substitution, hard links, or an authorized writer changing bytes. POSIX backslashes, encoded slashes and Unicode lookalikes are literal names; there is no URL decoding.

Decision ready for an authorized issue administrator, separately for each row: retain the issue ID and its exact flow, attach the corresponding controls and named attack/control results, verify the current source revision, and propose **False Positive** for the reviewed flow. No issue comments or status updates were published. Technical counterevidence does not itself grant transition authority; [Sonar issue editing](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/issues/editing) also requires the relevant issue permission and changes gate metrics.

## Independent advisory decisions

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

## Architecture: reviewed change, blocked application

Fresh server readback of model `cb04d3a3-7c8f-447c-99f0-ca49c97f054f` for project UUID `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2` was compared with [the exact proposal](../config/analysis/sonar-python-architecture.patch.json). Of 46 top-level groups, 44 invalid slash labels are addressed by removing 14 excluded Framework/MRTS groups and renaming 30 Parent labels from `/` to `_`. Parent patterns, four nested groups, metadata and `constraints: []` are preserved; no rules are invented or removed from the retained Parent architecture.

Canonical CLI `1.10.1` exposes `--data` and `--verbose`, but no header/content-type option. A fresh reviewed PATCH through `rtk bypass /usr/local/bin/sonar-with-env` again returned **HTTP 415 Unsupported Media Type**. Before/after readback is identical. No Sonar MCP capability was available. This is a client media-type limitation, not evidence of missing server administration permission. The perspective remains ignored; successful model application and a confirming new analysis are **extern blockiert**.

Supported-access handoff, preserving authentication policy:

1. Back up authenticated `GET /api/v2/architecture/models?projectId=608d0a7b-481a-4f7e-acbf-ae8eb07c3be2` through the canonical wrapper; compare the model ID and entire current model with the reviewed baseline before changing it.
2. Use an authorized supported client that can send `PATCH /api/v2/architecture/models/cb04d3a3-7c8f-447c-99f0-ca49c97f054f` with **`Content-Type: application/merge-patch+json`**, using the exact proposal as its body. The shown paths are the canonical CLI paths; retain the client's documented SonarCloud API-host routing. Approve/integrate that client's authentication with the required wrapper rather than extracting a token or bypassing it.
3. Read back through the approved path and compare the exact 14 removals/30 renames, preserved patterns, nested groups and constraints. If state drifted, review a new diff first.
4. Run a new clean exact-SHA analysis and retain its terminal server task, analysis ID and log demonstrating that this perspective is applied without the 44 invalid-label warnings.

No unverified UI import/editor capability is prescribed. The deprecated `sonar.architecture.configpath` is not a workaround: see [Web API](https://docs.sonarsource.com/sonarqube-cloud/appendices/web-api) and [deprecations](https://docs.sonarsource.com/sonarqube-cloud/deprecations-and-removals).

## Native context and taint limits

At the identified head, all **136 native translation units** remain in scope: quality **91.28/100**, parsing errors **193/2,260 functions**, unresolved project includes **46/1,132**. This improves the baseline 77.52/414/115 but is not a completion criterion. Actual pinned host context is NGINX `1.31.6`, HAProxy `3.2.25`, and patched lighttpd `1.4.85`. NGINX requires real configured `objs/ngx_auto_config.h`/`ngx_auto_headers.h` and its actual include paths; HAProxy's Linux/OpenSSL feature context is target-specific; lighttpd requires matching patched source and generated configuration.

The existing partial compilation database contains NGINX's 33 sources and a single C++ evaluator context, not all Parent units/variants, and filters copied HTX sources without a complete provenance mapping. Replacing AutoConfig with it would lose coverage. The source-pinned native context helper reads existing contracts as data, verifies archive checksums and records generated-header/include provenance. Six focused helper tests passed. A real development probe configured NGINX successfully, then failed because the new lighttpd patch invocation with --fuzz=0 differed from the existing native apply_core_patch.sh path. The second probe passed actual NGINX configure and the unchanged canonical lighttpd patch/stamp/ABI path (its actual fuzz2/fuzz1 applications are retained in the log), then stopped before lighttpd configure because the approved archive contains no configure script. The third real complete header-preparation run passed with exit 0: unchanged upstream autogen with installed tools and Bash for the ERR trap, actual patched-lighttpd configure, and generated header/config hashes. Its manifest records revision `4ec7581056889f8c70f44c6725f6bfa65a7fc45b` with `uncommitted_changes: true`, eleven real include directories, archive/patch/configure provenance and generated-file hashes. This is development evidence, not a new Sonar count. No component-owned script changed. The workflow measures the helper under Python coverage before finalization; the selected suite now contains 75 methods (61 existing, eight marker, six header tests). The fresh instrumented local selection passed all 75 tests in 7.256 s. New-helper development coverage is 82.48% for lines and branches, not a Sonar gate result. Clean-head CI remains required. No fabricated headers, guessed global defines or compiler commands are justified.

The implementation is [prepare-sonar-native-context.py](../ci/checks/analysis/prepare-sonar-native-context.py), with six focused regressions in [test_sonar_native_context.py](../tests/test_sonar_native_context.py). The successful run uses fresh external directories; local development artifacts are not reused as clean CI reports.

[Supported CFamily customization](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis) permits real include properties. **C/C++ taint is unsupported in AutoConfig**, and cross-translation-unit analysis cannot silently treat independently executable connector targets and incompatible variants as one linked program. Complete variant-preserving compilation context and explicit C/C++ taint proof remain **weiterhin offen** / **begründete Analyzergrenze**, respectively.

## Python analyzer boundaries and Shell

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

## Runtime and coverage readback

[Runtime run 40233061042](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061042) is terminal **SUCCESS** for all five connector jobs and the aggregate job. Apache job `121290821692` passed actual `RUN_ONE_CASE=1 make verified-apache-case CASE=crs_sqli_anomaly_block CRS=with-crs MRTS=no-mrts`: selected case denied HTTP 403 with rule `942270`; audit, cleanup, selected-results and artifact validation passed. There is no observed failed Apache job to repair.

Identity: Parent `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`; Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; CRS `e03a4f6dabc7a30ebd8c52c97d28a154f590a48f`; profile `with-crs-no-mrts-40233061042-1`, Apache cell `crs-40233061042-1-apache`, logical profile `native-httpd-module`.

Apache compact artifact `12614940472` was downloaded/read in memory and its SHA-256 matched GitHub's digest: `4da09921b83210e54028d449f33dd544d044e54b7de48caaced00a69de7c8832`. It contains exactly `functional-facts.json`, `manifest.json`, `profile-cell-receipt.json`; raw audit/results are hash references, not included raw evidence. Aggregate artifact `12614138658` reports technical PASS for five cells and functional PASS limited to `selected_crs_block_case_only`: **5 passed, 0 failed, 6 blocked, 13 not_run**, `coverage_complete: false`, `merge_eligible: false`. Apache/HAProxy allow controls are `not_observed`; no-MRTS is workflow/source-declared for them. Other cells retain host/Framework attestation limits. Green CI therefore does not qualify the full runtime matrix.

Actual Python XML, all four Go module reports and 71 native gcov reports were imported. Main PR new-code coverage **80.5%** passes the unchanged 80% condition; advisory branch new-code coverage is **82.7%**. Accumulated `master` previous-version coverage **0.6%** remains a separate baseline claim and has not been repaired or raised to 80% by this PR. All 18 non-Sonar workflows at the identified head are terminal success.

## Exact-head Sonar ledger and remaining work

All rows are historical exact-head evidence for `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`, scanner `8.2.0.6438`, CFamily `6.85.0.102562`, [run 40233061104](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061104). Upload alone is not completion.

| Project | CE task | Analysis ID | Terminal processing / gate |
| --- | --- | --- | --- |
| Main, PR 421 | `AaF03ulBdkEpBguA0oKZ` | `081d99d7-c136-4a67-b039-96507ad472a4` | SUCCESS; ERROR solely new-code Security Rating E / three issues. Coverage, reliability, maintainability, duplication and hotspot review pass. |
| C++20 advisory branch | `AaF03nsWdkEpBguA0oJ9` | `e29a042c-b9e6-4ffa-b6e4-f463dce07c34` | SUCCESS; ERROR. Independent advisory findings remain; new-code coverage 82.7% passes. |
| C++23 advisory branch | `AaF03alqJ8I9a074ReRm` | `0fdc39d6-930f-4ae9-bdf3-876d7670b4d3` | SUCCESS; ERROR. Independent advisory findings remain; new-code coverage 82.7% passes. |

At all three analyses, unchanged gate conditions are `new_reliability_rating <= 1` (actual 1), `new_security_rating <= 1` (actual 5, ERROR), `new_maintainability_rating <= 1` (actual 1), `new_coverage >= 80` (actual main 80.5, advisories 82.7), `new_duplicated_lines_density <= 3` (actual 0.0), and `new_security_hotspots_reviewed >= 100` (actual 100.0). No conditions were ignored.

The eight new marker tests are `test_current_run_marker_rejects_outside_symlink_before_restore`, `test_current_run_marker_fifo_fails_without_waiting_for_a_writer`, `test_current_run_marker_cannot_alias_an_outside_hardlink`, `test_current_run_marker_rejects_oversized_input_without_unbounded_read`, `test_current_run_marker_checks_directory_trust_before_reading`, `test_owned_legacy_marker_preserves_append_and_explicit_id_behavior`, `test_current_run_marker_does_not_accept_a_valid_prefix_after_short_read`, and `test_public_prepare_cannot_overwrite_an_outside_marker_target`, in `tests.test_sonar_evidence_boundaries.SonarEvidenceBoundaryTests`.

The three jobs preserve genuine coverage, 1,345 source/242 test files, 136 native units and four Go modules. The architecture warning, native counts, FIFO parser warning and full-advisory Python warnings above remain attached to this revision. Query exact CE activity/task and analysis IDs with scanner-context SHA; project-latest and unsupported `api/ce/component?pullRequest` filtering are insufficient PR proof.

| Requirement | Disposition at this documentation update |
| --- | --- |
| Three main issues | **weiterhin offen**: precise False Positive decision records prepared; no authorized transitions or green final gate. |
| Advisory marker defect | **weiterhin offen**: reproduced boundary defect; source repair locally verified (16 boundary + 8 related tests, independent 7-case review); final scanner closure pending, separate from main decisions. Other pairs have documented independent counterevidence. |
| Architecture perspective | **extern blockiert**: reviewed exact delta, repeated HTTP 415, unchanged server state; supported-media-type application and rescan required. |
| Native parsing/includes | **weiterhin offen**: real header preparation passed locally; new exact-head parsing/include counts pending, no full-scope compilation database. |
| C/C++ taint / Python cost and predecessor / FIFO | **begründete Analyzergrenze** as scoped above, with residual gaps retained. |
| Previous Apache CI uncertainty | **behoben und nachgewiesen** for the selected runtime run/case; full runtime qualification remains open. |
| Coverage and scope preservation | **behoben und nachgewiesen** at the identified historical head; fresh reports and checks required for the next head. |
| Final completion proof | **weiterhin offen**: obtain new exact-head CE/analysis/gate/coverage/warnings for all three projects and terminal CI after source changes. PR stays Draft. |
