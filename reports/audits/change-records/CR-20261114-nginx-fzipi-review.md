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
| 1 | Redirect loses source audit; every target reprocesses | Request-owned, policy-aware recovery; each native transaction audits once before cleanup | Compiled real Common/audit tests and native H1 ownership counts passed |
| 2 | Preserved deny header blocks error page again | Capture and match the configured WAF error-page destination/status | Native H1 custom403/header/original native403 audit and generic-error negative case passed |
| 3 | Safe optional event failure poisons transaction/connection | Diagnose optional event failure; preserve real errors and Strict abort | Compiled controlled event-error, actual metadata-allocation and genuine EOS-error controls passed; no host sink-fault claim |
| 4 | size_t observation overflow rejects >4 GiB on 32-bit | Saturating uint64 counters through Common/events; bounded full-file streaming | Compiled UINT32/UINT64 and modeled >4 GiB file checks |
| 5 | Emptied original data links reach writer | Consume payload, forward owned control buffers, one termination | 9 compiled controls and native rogue two-data-plus-NULL handler passed; no writer errors/body leak |
| 6 | Free payload can supply a rule ID | Full ordered/escaped Engine record with ambiguity rejection | 28 scenarios including real Engine 3.0.14; old parser reproduced three faults |
| 7 | Native response Reject requires exact English log | Validated append state and rule-free disruptive403 shape | Real compiled collector/append/P4 caller:18 Reject and18 ProcessPartial mode/commit/prose variants passed |
| 8 | Same-context mode duplicate accepted | Duplicate sentinel check; Common mode validation/inheritance retained | Compiled setter/merge and real nginx -t duplicate/off/strict child cases passed |
| 9 | Earlier file/JSON improvements exist | Preserve same append path, structured events and escaping | Common helper smoke and affected compiled paths passed; original improved helpers retained |

The explicit supersede_response lifecycle operation retires only healthy completed P1/P2 owners after response policy transfer; phase masks remain unchanged and no P3/P4 is fabricated.

The C callback supplies text. Newer C logged-ID lists omit causal disruptive-rule attribution; taking their first/last member is unsafe. The parser therefore validates the entire supported native record and leaves ambiguous IDs unknown. Native NGINX decisions requiring correlation fail closed.

## Changed files

`connectors/nginx/src/ngx_http_modsecurity_{access,body_filter,common,log,module}.*`, `ngx_http_modsecurity_phase4_observation.h`, `ngx_http_modsecurity_response_body_limit.h`; Common `rule_id.c/.h`, `transaction_contract.h`, `transaction_state.c`; paired connector/Common READMEs, paired connector guide and this record. Regression tests remain in a separately authorized Framework branch `test/nginx-fzipi-review`; Parent gitlink and MRTS remain unchanged.

## Commands executed

`rtk make check-nginx-c17` passed against real NGINX1.31.8 configured headers and matching libModSecurity3.0.17 SDK with C17/Wall/Wextra/Werror. `rtk make build-nginx` passed the native dynamic component build. A fresh static NGINX1.31.8 plus test-only addon build also passed with8 logical CPUs and the pinned archive SHA256 `0652b760b3b772d2ec17b47c2fc15d9a95e6fe35cd5b877eadc1a62d9bc75af1`.

The final explicit Framework unittest selection passed75 methods across10 affected modules at product source `b478aeb02c26bf6e44627f43b49678f1abc3081b` (`focused-final.json`). Parser tests include28 scenarios and genuine Engine3.0.14 messages. Four additional existing request-native test methods and two direct existing-helper scenarios passed: memory and temp-file append0 ProcessPartial reaches EOS, while short/failed/changed file state remains terminal. The updated Common adoption gate passed and its11 mutation methods rejected28 negative variants without disabling checks.

Original-code negative controls reproduced the parser, counter, Safe sink, audit/recovery and discarded-buffer failures; they compiled successfully before producing intended runtime assertion failures.

`rtk make check-common-helpers ON_DEMAND_TESTS=1`, `rtk make check-bilingual-docs check-doc-links`, selected canonical Secrets scans and final whitespace checks passed. The initial isolated-worktree docs failure was resolved by read-only materialization of its exact pinned Framework link targets. Two trailing record blank lines were corrected. An initial short-revision unittest command failed at source admission before execution; the corrected full-SHA run passed.

Full actual command arrays/environment and receipts are retained under `/var/tmp/codex/ModSecurity-conector/runs/20261114-fzipi-review`; `run-focused.py` selects the10 test modules explicitly. Native execution used `rtk bypass env ... python .../run_nginx_fzipi_review.py --connector-root <Parent worktree> --expected-head b478aeb02c26bf6e44627f43b49678f1abc3081b --artifact-manifest <static-fixture-v2>/artifact-manifest.json --nginx-binary <static-fixture-v2>/nginx-1.31.8/objs/nginx --output-root <run>/native-host-v2` in the reviewed escalated local context. No security controls or mandatory gates were disabled.

## Security impact

No generic error-page or internal-redirect exemption. No unknown metadata becomes an allow. Optional late Safe observability cannot abort delivery; native Reject and genuine processing errors remain failures. Body data is never placed in the new event records. No security gate, compiler warning or validation was weakened.

## Runtime evidence

Native H1 passed9 scenarios at product source `b478aeb02c26bf6e44627f43b49678f1abc3081b`: Phase2 header block→configured403 page with the trigger preserved and exactly one original native403 audit; ordinary try_files→one audit; changed target rules→two independently owned audits; disabled target→one source audit; ordinary host403 error page→WAF still blocks; replaced response→two stale body callbacks plus NULL, zero leaked bytes/no empty-writer diagnostics; duplicate mode rejected and inherited Safe child off/strict accepted.

Same-context Framework identity/access preflights passed. Observed master UID/GID0 and worker UID/GID65534; private output denied to worker. Master exit0/reaped, process group absent and listener closed. Receipt `/var/tmp/codex/ModSecurity-conector/runs/20261114-fzipi-review/native-host-v2/private/result.json`, SHA256 `0364231b54ca098f69666f52777bb0162460b1b1f5ae39001789f0c92388738b`. The first native candidate exposed an empty downstream writer call; that production error and a too-narrow relative Location test expectation were corrected, followed by the fresh passing build/run. Native audit evidence is read from libModSecurity JSON, not substituted event JSONL.

## Known limitations

Text metadata with ambiguous raw framing remains unknown and required rule correlation fails closed. Saturation retains a lower bound beyond UINT64_MAX. The32-bit boundaries are realistic compiled type/arithmetic models, not a native32-bit host build or multi-GiB download. Safe sink faults and Reject/ProcessPartial prose/mode/commit variants are compiled actual-product seams, not additional live-host fault campaigns. No H2/H3 or full-matrix qualification is claimed.

## Remaining risks

Framework regression delivery is separate; the Parent gitlink is unchanged. Current-head remote CI/Sonar and PR review remain delivery checks. No merge or deployment is authorized.

## Checks not run and rationale

No all-connector or historical I12 matrix, production deployment, H2/H3 qualification or merge: outside this focused request. No current-head remote CI/Sonar pass is claimed in this recording; consult the PR for live delivery checks.

## Final diff and review status

All eight applicable corrections and preservation point9 have source, focused-test and documented evidence. Independent source review findings were corrected and six independent re-review tests passed. The real empty-writer regression was subsequently fixed and the fresh native run passed. Task source commits02ca6440/48c4a996/b478aeb0 exist on `fix/nginx-fzipi-review`; this documentation reconciliation contains no further product-source changes. Remote delivery is still to be read back at its actual head; no merge occurred.
