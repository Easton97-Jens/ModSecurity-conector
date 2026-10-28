# Change Record: CR-20261028-sonar-connectors-followup

**Language:** English | [Deutsch](CR-20261028-sonar-connectors-followup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-sonar-connectors-followup |
| Date (UTC) | 2026-10-28 |
| Base revision | `c5993ed9a7b59fc0bd58f105595ec79f596c88d6` |

## Motivation and problem statement

The user requested a new PR for the Sonar directory table, then explicitly excluded `tests/` and `ci/`. Current main analysis at the base contains 35 connector findings: 34 `c:S995` API-const suggestions and one `pythonsecurity:S8707` operator-input-path report. They are the already-reviewed candidates remaining after merged PR #430. The user initially directed documentation only, then explicitly requested removing these reviewed connector findings from scoring. This newer instruction authorizes individual False Positive transitions for exactly these 35 main-project issues; ci/ and tests/ remain excluded.

## Acceptance criteria

Reconcile all 35 authenticated current positions individually; preserve ABI and supported CLI behavior. Record both user exclusions without changing analysis scope. Keep product source unchanged; classify only the 35 individually reviewed connector findings as FALSE_POSITIVE with technical comments. Verify zero remaining connector issues and unchanged unrelated issue states. State the original and remaining master gate failure accurately. Validate the report and paired records, then deliver a new Draft PR with current-head checks truthfully reported. This is an authorized false-positive disposition, not a claim that 35 code defects were fixed or vulnerabilities risk-accepted.

## Implementation decision and rationale

Fresh independent source/header/registration review confirms 18 Apache, seven NGINX and nine HAProxy parameter positions require the current mutable host callback types. Adding pointee const would violate these signatures. The new master HTX issue ID represents the already-reviewed `haproxy_modsecurity_htx_filter_http_payload/msg` function, not a new cause.

The lighttpd first-byte helper intentionally accepts separately selected event input. Its existing positive test `connectors/lighttpd/tests/test_patched_event_validation.py::test_first_byte_writer_accepts_phase_aliases_and_preserves_schema` places input outside `--runtime-output-root` and expects success. The actual hosted runner supplies a fixed private snapshot. Sonar describes local `argparse.parse_args()` as an HTTP source; no new exploitable boundary was established. Mandatory output-root containment would break the demonstrated contract. Optional new input-root behavior would be a separate feature and would not eliminate the generic input branch, so it is not added.

After the newer user authorization, all 35 findings were individually transitioned with the existing authenticated API and their specific technical counterevidence. Independent readback verified exactly 35 FALSE_POSITIVE states and exact comments. Product source remains unchanged.

## Changed files

`reports/audits/sonar-connectors-followup-20261028.json`, this English record and its German companion. The JSON retains the original 35-position snapshot and adds the authorized disposition/readback. No connector, CI or test source, source binding, generated test archive, gitlink, dependency, rule, gate, suppression or analysis exclusion changes.

## Commands executed

PASS: authenticated read-only issue/hotspot/metric/analysis/gate snapshot via RTK and `/usr/local/bin/sonar-with-env`, bound to the exact base. Complete main inventory has 59 open issues; connector selection is 35, with zero hotspots. PASS: `rtk bypass python3.15 /var/tmp/codex/ModSecurity-conector/analysis/sonar-directory-followup-20261028/connector-only/verify-connector-report.py` confirms every ID/rule/type/path/line/message, 34 API plus one CLI case, both exclusions, zero source changes and exactly 35 authorized server dispositions. Independent source/contract review completed. PASS: `rtk bypass python3.15 ci/tools/new-change-record.py check`, `rtk make check-bilingual-docs PYTHON=/usr/local/bin/python3.15`, `rtk make check-doc-links PYTHON=/usr/local/bin/python3.15 FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/sonar-directory-followup-20261028/modules/ModSecurity-test-Framework`, staged `git diff --check` and default Gitleaks8.30.1 staged scan with `--redact=100`. PASS: 35 sequential `/api/issues/do_transition` requests with `transition=falsepositive` through RTK and `/usr/local/bin/sonar-with-env`, each with individual technical comment. Independent readback/peer verification confirms all 35 FALSE_POSITIVE, zero open connector issues, zero Bugs/Vulnerabilities/Code Smells/Hotspots and all connector ratings 1.0 (A). Exactly 24 unrelated open states remain unchanged: ci/ 15, tests/ 6, common/ 3. New current-head CI/Cloud is not yet claimed.

## Security impact

No security control or runtime behavior changes. Review evidence is bounded to the selected findings. The failing master gate remains recorded as ERROR: `new_security_rating=5`, required maximum `1`, new-code period starting `2026-05-14T18:30:31+0000`. The authorized False Positive disposition excludes these reports from connector scoring. It is not a source security fix, risk acceptance or passing master analysis. No rules or gates were changed.

## Runtime evidence

No runtime evidence was collected or claimed for this documentation-only PR. Source and existing tests were read as contract evidence only.

## Known limitations

All 35 reviewed findings are now FALSE_POSITIVE after the newer explicit user instruction. Open connector issue metrics are zero; other main-project components and separate native/advisory projects were not dispositioned. No safe source-only correction preserving the demonstrated APIs and CLI behavior was found. A new changed-code PR gate, if green, does not clear the unchanged master inventory. The analysis snapshot is exact-revision evidence, not a promise about later analyses.

## Remaining risks

Unsupported callback changes or arbitrary restrictions on separately selected operator inputs would introduce compatibility regressions. Those approaches are not implemented. Only the 35 reviewed main-project connector statuses changed. The remaining 24 unrelated open states were independently verified unchanged. `ci/` and root `tests/` findings remain outside this task, not removed from analysis.

## Checks not run and rationale

No product tests, builds, additional I12 campaign, runtime matrix, deployment or merge: no product code changes. Existing positive tests were inspected as contract evidence, not executed or newly passed. Both configured Sonar workflows still apply to docs-only PRs; exact-head results must be read after creation. Framework remains at the existing exact gitlink for Parent link checks, with no Framework/MRTS change.

## Final diff and review status

The requested scope is connector findings only. This PR delivers the current 35-position reconciliation and audit of the newer authorized False Positive transitions. Source corrections remain zero; connector scoring is cleared while the global master gate remains ERROR. Local data, structure, bilingual/link, staged whitespace and secret checks passed; independent EN/DE/data review found no material inaccuracies. New Draft PR/current-head CI results must be read in the PR. No merge is authorized.
