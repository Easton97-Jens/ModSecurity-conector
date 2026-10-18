# Change Record: CR-20261018-haproxy-original-oracle-sources

**Language:** English | [Deutsch](CR-20261018-haproxy-original-oracle-sources.de.md)

Source-only oracle delivery; no host acceptance is claimed.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-original-oracle-sources |
| Date (UTC) | 2026-10-18 |
| Base revision | `fc7e0d25c6ed3240d6e257e92f25475e63f150c8` |

## Motivation and problem statement

The original HAProxy oracle subset contains 124 expectations across three distinct routes. 34 had historical source resolutions; 90 remained open. Root independently reviewed 31 additional exact source expectations through the existing reconciliation API. Recording these source approvals makes the remaining 59 explicit without manufacturing host lifecycle evidence.

## Acceptance criteria

Copy the exact Root-approved 124-record artifact; preserve all original IDs, values, selected-contract hashes, revisions and 34 historical records. Reproduce the 31 approved source reviews with the frozen existing API, verify physical source hashes, and retain separate route counts. Give no new host credit, retest, runtime-absence waiver or lifecycle PASS.

## Implementation decision and rationale

Only the HAProxy-owned fixture JSON is replaced with the exact approved artifact SHA256 d3a917eec9ac60d5dd23a2d61f6acefc1efd6f52d9c66127a6a93cc05fa90f3e. The original v1 bytes remain externally preserved as source-proposals-v1.json (SHA256 2e1358250894569b2cb25a0c8409bea95606d4fd48bd1bcc0026bd2847fef05a). SDK 3.0.14, official HAProxy 3.2.25 documentation and the versioned normative phase contract are independent sources; Framework rules, declarative inputs and fixture implementation remain separately identified. Approved fixture history binds native v7, SPOP v4 and companion v5; later fixture changes require separate binding. The inherited candidate schema identifier is preserved byte-for-byte; embedded Root approvals establish the actual source-review status.

## Changed files

connectors/haproxy/harness/fixtures/i12-oracles-20261015.json and this English/German Change Record pair. No central matrix, shared capture object, generator, other connector, Common implementation or product file changes belong to this delivery.

## Commands executed

All commands used RTK. The task-local Python 3.14.7 verifier approved-source-delivery-20261018/verify.py passed: original 1484-contract identity, 124 original oracle records, 34 unchanged historical records, 31 reproduced Root-approved reviews and 138 physical source-reference hash/length bindings. The standard bilingual documentation, documentation-link and Change Record structure checks passed. Exact argv/cwd/exits and raw hashes are retained under /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/oracles/approved-source-delivery-20261018/. The structure checker validates structure only; both language texts were manually read for matching facts.

## Security impact

Bounded defensive evidence maintenance within the user-authorized scope. Validation, source independence, original contracts, isolation and host qualification remain intact. No deep security scan or exploit investigation was performed.

## Runtime evidence

No new runtime observation is claimed. Source-resolved totals are 65/124 with 59 open: native HTX 31/48 with 17 open; SPOP request 21/44 with 23 open; response companion 13/32 with 19 open. These counts describe original oracle expectations, not the 112/94/72 route obligations or independent host executions. New host credit is 0 and full lifecycle qualification was not performed. A SPOP ACK cannot qualify the independent response companion.

## Known limitations

The 31 source approvals have no retest receipt or lifecycle PASS. Native P3 redirect retains the required 302 and the historical v7 fixture 503 conflict; it is not corrected to green. Connection reuse requires the predeclared allow/deny/allow sequence with HTTP [200,403,200], phases [2,1,2], EOS [1,0,1], three allocations/frees and two backend requests. SPOP is a finite complete-sample authorization route; no unlimited stream or unsupported HTTP/2 mapping is declared fully inspected. Historical 34 records are preserved rather than requalified.

## Remaining risks

The 59 exact source-oracle gaps still require their own selected fixture/fault/scope resolution. Current product fixes and later fixtures cannot retroactively change approved source history. Physical native events, first cause, response commit, real client/backend transport, EOS and once-only cleanup require separate current-build host evidence. Fixed 500 contract conflicts remain unchanged.

## Checks not run and rationale

No host runtime, package installation, product change, Common change, matrix generation, Git commit/push/merge or broad security scan was performed. A source-only JSON delivery does not establish the runtime layers those actions would test; the coordinator owns subsequent host acceptance and delivery.

## Final diff and review status

The approved JSON is byte-identical to Root’s current-source-inventory124.json, all original and historical preservation checks passed, and the two language records contain the same counts, hashes, scope and limitations. Root already approved the 31 source expectations through the existing API. This Change Record documents source delivery only; it grants no host or merge approval.
