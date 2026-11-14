# Change Record: CR-20261114-nginx-fzipi-review

**Language:** English | [Deutsch](CR-20261114-nginx-fzipi-review.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261114-nginx-fzipi-review |
| Date (UTC) | 2026-11-14 |
| Base revision | `5672c5ff562495ddbc47a1932b1641e0073746f5` |

## Motivation and problem statement

Correct the still applicable fzipi review of [upstream PR #377](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377). The current remote master equals the supplied comparison revision. Preserve request-file ProcessPartial, structured events and JSON escaping.

## Acceptance criteria

Preserve native audit and original block status, deliver the configured WAF error page without a general redirect exemption, continue late Safe responses on optional event failure, preserve Strict/native-limit/technical errors, avoid observation overflow limits and invalid downstream empty buffers, identify real rule metadata, classify native Reject without prose, reject duplicate modes.

## Implementation decision and rationale

| Point | Previous behavior | Change | Executed evidence / limit |
| --- | --- | --- | --- |
| 1 | Redirect loses source audit; every target reprocesses | Request-owned, policy-aware recovery; each native transaction audits once before cleanup | Compiled audit/recovery tests; native host run still pending |
| 2 | Preserved deny header blocks error page again | Capture and match the configured WAF error-page destination/status | Compiled positive/negative routing tests; native delivery still pending |
| 3 | Safe optional event failure poisons transaction/connection | Diagnose optional event failure; preserve real errors and Strict abort | Compiled failed-sink controls; integrated final rerun pending |
| 4 | size_t observation overflow rejects >4 GiB on 32-bit | Saturating uint64 counters through Common/events; bounded full-file streaming | Compiled UINT32/UINT64 and modeled >4 GiB file checks |
| 5 | Emptied original data links reach writer | Consume payload, forward owned control buffers, one termination | Compiled memory/file/subrequest/NULL/reentry controls; host handler pending |
| 6 | Free payload can supply a rule ID | Full ordered/escaped Engine record with ambiguity rejection | 28 scenarios including real Engine 3.0.14; old parser reproduced three faults |
| 7 | Native response Reject requires exact English log | Validated append state and rule-free disruptive403 shape | C17 predicate positive/negative log/state cases |
| 8 | Same-context mode duplicate accepted | Duplicate sentinel check; Common mode validation/inheritance retained | Compiled setter/merge test; native nginx -t pending |
| 9 | Earlier file/JSON improvements exist | Preserve same append path, structured events and escaping | Required affected checks selected; final results below |

The explicit supersede_response lifecycle operation retires only healthy completed P1/P2 owners after response policy transfer; phase masks remain unchanged and no P3/P4 is fabricated.

The C callback supplies text. Newer C logged-ID lists omit causal disruptive-rule attribution; taking their first/last member is unsafe. The parser therefore validates the entire supported native record and leaves ambiguous IDs unknown. Native NGINX decisions requiring correlation fail closed.

## Changed files

`connectors/nginx/src/ngx_http_modsecurity_{access,body_filter,common,log,module}.*`, `ngx_http_modsecurity_phase4_observation.h`, `ngx_http_modsecurity_response_body_limit.h`; Common `rule_id.c/.h`, `transaction_contract.h`, `transaction_state.c`; paired connector/Common READMEs, paired connector guide and this record. Regression tests remain in a separately authorized Framework branch `test/nginx-fzipi-review`; Parent gitlink and MRTS remain unchanged.

## Commands executed

`rtk make build-nginx FRAMEWORK_ROOT=<Framework task worktree> ...`: passed first native build, NGINX1.31.8 and matching cached libModSecurity3.0.17; later source corrections require fresh build verification. `rtk bypass env ... python -m unittest ...test_nginx_response_body_limit`: passed. Focused parser tests passed4 methods/28 scenarios. Actual selected-file Secrets scans passed0 via `rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin`. Full commands and receipts retained under `/var/tmp/codex/ModSecurity-conector/runs/20261114-fzipi-review`.

## Security impact

No generic error-page or internal-redirect exemption. No unknown metadata becomes an allow. Optional late Safe observability cannot abort delivery; native Reject and genuine processing errors remain failures. Body data is never placed in the new event records. No security gate, compiler warning or validation was weakened.

## Runtime evidence

The first native build completed; it is compilation evidence only. The targeted host receipt is not yet available. No native audit/error-page/streaming or H2/H3 runtime success is claimed at this stage.

## Known limitations

Text metadata containing ambiguous raw framing is intentionally unknown. Saturated observations retain a lower bound, not an exact count beyond UINT64_MAX. Required final integrated build/runtime/documentation checks remain in progress.

## Remaining risks

Targeted internal-routing and writer behavior still require the real host run. New Framework tests are separate delivery and do not update the Parent pin automatically.

## Checks not run and rationale

No all-connector or historical I12 matrix, production deployment, H2/H3 qualification or merge: outside this focused request. Current-head PR CI/Sonar results do not yet exist.

## Final diff and review status

Independent source review found EOS-validation, superseded-scope and event-allocation diagnostic gaps; all three source corrections are applied. Full native C17 compile with warnings-as-errors, Common helper smoke, bilingual docs/link checks and whitespace passed. Branch `fix/nginx-fzipi-review`; source commit is being prepared for clean-checkout native validation. No push/PR/merge yet. Final observed runtime and delivery facts will be reconciled before delivery.

