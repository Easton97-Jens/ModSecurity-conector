# Change Record: CR-20261001-pr370-refresh-relevance

**Language:** English | [Deutsch](CR-20261001-pr370-refresh-relevance.de.md)

PR maintenance, not a ten-profile readiness promotion.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261001-pr370-refresh-relevance |
| Date (UTC) | 2026-10-01 |
| Base revision | `e0b6cab3f46d73da0a10d7b4afca73e0cb584448` |

## Motivation and problem statement

The user requested an update and relevance assessment of existing Draft PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370). Its published head conflicted with master and its description was stale. Two independent source audits found Apache P2/APXS, Envoy ext_authz path, Stock-lighttpd endpoints, Traefik native endpoints and NGINX receipt corrections still absent from master.

## Acceptance criteria

Preserve published history; normally integrate observed master `b0f3bdab429717b5b0311c30c5b4d1153c672ac0`; retain current pins and security/Phase-4 behavior; resolve conflicts; rerun relevant checks; publish exact-head CI/Sonar and bilingual delivery status. No merge is authorized.

## Implementation decision and rationale

The earlier worktree is absent, so use a new task-owned worktree from the published head. Resolve the two NGINX conflicts with `EXPECTED_NGINX_VERSION = "1.31.6"`, shared by the source-root and both receipts; preserve HAProxy `3.2.25`. Remove only two unused `read_event_jsonl` result assignments (`c:S1854`). Adapt the Stock assertion to the mode-dependent Phase-4 budget. Restore necessary Apache bootstrap P2 marker/default-limit, audit-redaction, recovery and non-root controls; retain final curl status rather than first-header parsing (`100 Continue`). Keep all other published fixes and incoming master security/Phase-4 changes.

## Changed files

- `tests/run_nginx_body_buffer_fixture.py`, `tests/test_nginx_body_buffer_fixture.py`
- `tests/transaction_phase_runtime_companion_test.c`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`, `tests/test_apache_request_transaction_cleanup.py`
- This EN/DE record, EN/DE archive index and cross-references in the earlier EN/DE readiness record. Other incoming master files are integration history, not separately selected edits.

## 2026-10-03 scope reconciliation

The NGINX statements above describe the October 1 intermediate head. The user
subsequently excluded NGINX. All four NGINX fixture/contract-test paths now
match `origin/master`; the final PR neither delivers nor credits that receipt
identity correction. The remaining nine-profile work is independent of those
files.

## Commands executed

All shell commands were RTK-wrapped. Existing `python3` is exact `3.14.7`; no dependency installation. Task output: `/var/tmp/codex/ModSecurity-conector/runs/pr370-refresh-20261001`.

| Check | Observed pre-delivery result |
| --- | --- |
| Focused Python suite including current security regressions | 224 cases: 217 passed, six skipped, one environment error at the hardcoded `/tmp` fixture's `mkdtemp`, before product execution. |
| Stock/pins/body-buffer/Phase-4/forwardAuth suite | 143 cases: 137 passed, six prerequisite skips. |
| Apache bootstrap source regression and shell syntax | 21/21 passed; `sh -n` passed. |
| `make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-apache-common-adoption` | Passed; Apache adoption also ran 12 focused cases. |
| `make check-apache-c17 check-remaining-connectors-c17` | Passed with warnings as errors and explicit external output. Initial Apache default-output attempt failed on a read-only unapproved path; rerun used task-owned output. |
| Direct companion C test with `cc` and `clang` | Both strict C17 builds and executions passed against system libmodsecurity, each bounded by 120 seconds. |
| `make -C connectors/traefik test-native-middleware` | Go tests and vet passed. |
| `python3 ci/tools/generate-connector-config-reference.py --check` | Passed: 21 generated files current. |
| `git diff --check` | Passed before record authoring. |
| `make check-apache-autotools-bootstrap` | Module build/configuration passed; non-root startup blocked by task-directory `chown` returning `EINVAL`. No host runtime pass. |
| `make check-bilingual-docs` and `make check-doc-links` | Attempted; only missing local Framework link targets were reported. The new record/archive structure check passed. |

## Security impact

No suppression, exclusion, Quality-Gate relaxation, dependency change or compiler-warning reduction. Trusted socket/path and body-limit controls remain protected. Independent merged-source review confirmed Apache P4 effective budgets and Stock P4 OFF/LOG_ONLY/shutdown alongside retained PR fixes. No Framework/MRTS source writes; their Gitlinks only follow incoming master history.

## Runtime evidence

The direct Common companion binary validates escaped-event hashing and buffered forwardAuth P2-to-P3/P4 transfer against libmodsecurity. It bypasses host HTTP parsing, uses `safe`, and is not a host/readiness-B result. It is not wired into routine CI. Final-head Apache, NGINX and runtime-cell results are recorded in PR #370 after push, not inferred from historical September runs.

## Known limitations

The worktree has no materialized Framework checkout. Five pin-bound cases and the Stock runtime-identity prerequisite skip are explicit local gaps. The newer directory regression cannot create its hardcoded `/tmp` fixture in this sandbox. Full local framework-dependent lint/docs and all-ten-profile G1–G9 evidence are not established.

## Remaining risks

Hosted checks and Sonar must bind to the delivered SHA. Old green runtime cells and old 0.0% duplication do not validate the successor. The broader readiness-B objective remains incomplete; the PR is still a scoped corrective increment.

## Checks not run and rationale

No all-ten-profile G1–G9 campaign, dependency installation, Framework/MRTS write, direct master push, merge or force push. Exact-head CI is only available after push; its live results are published in PR #370 at handoff. Full local framework-dependent lint was not run; local native Apache startup and repository-wide docs attempts have the environment limitations listed above, never credited as passes.

## Final diff and review status

Relevance was independently audited against current master; merged Apache/Stock overlap was independently reviewed. Main owns final diff, bilingual review, delivery and CI/Sonar reconciliation. Observed delivery results are maintained in PR #370 rather than a self-referential commit SHA in this record.
