# Change Record: Apache request transaction cleanup

**Language:** English | [Deutsch](CR-20260714-apache-request-transaction-cleanup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Apache request transaction cleanup |
| Change ID | CR-20260714-apache-request-transaction-cleanup |
| Date (UTC) | 2026-07-14T10:51:57Z |
| Author or executing agent | Codex /root |
| Base revision | db3f1747bddd2d36470f61c9b04029876f864667 |
| Related issue or pull request | None |
| Final revision | f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b (implementation; this Change Record is uncommitted) |

## Motivation and problem statement

The confirmed finding was that an Apache native ModSecurity <code>Transaction</code>
was not released per request. Before this change, <code>create_tx_context</code>
stored the native pointer in request notes but registered no request-pool cleanup,
and the Apache connector had no <code>msc_transaction_cleanup</code> call.

The supplied finding has no scan ID, severity, scanner version, scan timestamp,
original scan commit, or versioned Apache scan report. A matching report was not
found in the repository, so those provenance values are unknown. The finding
title is retained as supplied: <code>Apache transaction is not released per request</code>.

## Affected components and security boundaries

<code>connectors/apache/src/</code> owns the Apache request and APR-pool boundary.
A successfully created native <code>Transaction</code> is now owned by the primary
Apache request pool. Internal redirects and subrequests deliberately continue to
reuse the primary context; separate top-level requests on a keepalive connection
retain separate request pools and transactions.

The native destructor is non-idempotent, so the callback clears the native pointer
and the owner note before calling <code>msc_transaction_cleanup</code>. It does not
change request parsing, rules, logging/redaction, response handling, intervention
cleanup, or any Framework source. The local Apache runtime build and raw logs
were kept under <code>$task_tmp</code> only and are outside the versioned diff.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| A successful native transaction is published only after non-NULL creation and receives one normal cleanup on its primary <code>r-&gt;pool</code>. | met | Source regression test and APR lifecycle harness |
| The callback clears the native pointer and primary-owner note before the non-idempotent native destroy call. | met | Source regression test and APR lifecycle harness |
| Keepalive request pools remain independent; subrequest and redirect lookup retain the existing primary-context ownership model. | met | APR lifecycle harness and source regression test |
| Failed creation, early error/intervention paths, abort, and duplicate callback invocation do not leak or double-destroy the native transaction. | met | APR lifecycle harness |
| The patched module preserves representative normal Apache traffic. | met, bounded | Local Apache smoke observed HTTP 200 and HTTP 403 for the selected No-CRS cases |
| The Apache transaction cleanup contract and its Change Record have English/German companions. | met | <code>make check-bilingual-docs</code>, <code>make check-doc-links</code>, and <code>make check-variable-documentation</code> |

## Alternatives investigated

- Registering module- or process-pool cleanup was rejected because it retains
  request-scoped native transactions beyond their request lifetime.
- Releasing only from the log hook was rejected because early errors, aborts,
  and intervention paths can bypass that hook.
- Using mutable <code>msr-&gt;r</code> in cleanup was rejected because redirect and
  subrequest lookup updates that field; the primary owner must be captured.
- Changing redirect or subrequest reuse semantics was rejected because the
  existing source intentionally shares the primary transaction.
- Changing <code>msc_intervention_cleanup</code> was excluded: it is a separate
  finding and behavior boundary.

## Implementation decision and rationale

<code>msc_t</code> now retains <code>owner_request</code> separately from mutable
<code>r</code>. After successful native creation, the connector stores the
context and registers <code>msc_cleanup_request_transaction</code> as normal APR
cleanup on the primary request pool. The callback snapshots the native pointer,
sets <code>msr-&gt;t</code> and <code>owner_request</code> to NULL, removes
<code>NOTE_MSR</code> from the captured primary request, and then calls
<code>msc_transaction_cleanup</code>. That ordering prevents a stale note and
repeated cleanup from reaching the non-idempotent native destructor.

## Changed files

- <code>connectors/apache/src/mod_security3.c</code>
- <code>connectors/apache/src/mod_security3.h</code>
- <code>connectors/apache/src/msc_utils.c</code>
- <code>connectors/apache/src/msc_utils.h</code>
- <code>ci/checks/connectors/apache/check-apache-c-standards.sh</code>
- <code>ci/checks/connectors/apache/apache_request_transaction_cleanup.c</code>
- <code>ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh</code>
- <code>tests/test_apache_request_transaction_cleanup.py</code>
- <code>Makefile</code>
- <code>docs/connectors/apache.md</code>
- <code>docs/connectors/apache.de.md</code>
- <code>reports/audits/change-records/CR-20260714-apache-request-transaction-cleanup.md</code>
- <code>reports/audits/change-records/CR-20260714-apache-request-transaction-cleanup.de.md</code>
- <code>reports/audits/change-records/README.md</code>
- <code>reports/audits/change-records/README.de.md</code>

No Framework or generated-report source was changed. The implementation files were
included in <code>f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b</code> by an external
working-tree commit during verification; this Change Record and its index rows remain
uncommitted. Existing unrelated working-tree changes were preserved.

## Tests added or changed

- <code>tests/test_apache_request_transaction_cleanup.py</code> checks source
  ordering, owner-pool registration, callback invalidation, and retained
  redirect/subrequest semantics.
- <code>ci/checks/connectors/apache/apache_request_transaction_cleanup.c</code>
  runs the production callback against real APR pools for normal, keepalive,
  failed-create, early-error/intervention, abort/duplicate-cleanup, subrequest,
  and redirect cases.
- <code>ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh</code>
  compiles and runs that harness with the available Apache/APR headers.

## Commands executed

Paths below use the sanitized <code>$task_tmp</code>, <code>$cache</code>, and
<code>$framework</code> placeholders. They do not contain raw logs or complete
environment exports.

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>rtk env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_apache_request_transaction_cleanup</code> | 1 | Pre-fix regression: five errors because the expected cleanup helper did not exist. | None | None |
| <code>rtk env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_apache_request_transaction_cleanup</code> | 1 | First post-patch run exposed a test-parser prototype match; the test helper was corrected. | None | None |
| <code>rtk sh -n ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh</code> | 0 | Shell syntax check passed. | None | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup</code> | non-zero | First harness execution could not load <code>libapr-1.so.0</code>; the runner was corrected to add the APR library directory as rpath. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup</code> | non-zero | An intermediate APR library-directory probe emitted usage text into compiler flags; the runner was corrected to derive <code>-L</code> from APR link flags. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup</code> | 0 | Five source-contract tests and the real APR lifecycle harness passed. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk make check-apache-common-adoption</code> | 0 | Apache Common adoption check passed. | None | None |
| <code>rtk make check-apache-c-standard-wiring</code> | 0 | Apache C-standard wiring check passed. | None | None |
| <code>rtk env CI=true APACHE_C_STANDARDS_OUT="$task_tmp/build/apache-c-standards" make check-apache-c17</code> | 0 | C17 compile, including <code>msc_utils.c</code>, passed. | <code>$task_tmp/build/apache-c-standards</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup-lint</code> | 0 | Lint integration reran the source-contract and APR harness successfully. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk env AUTO_FETCH_SMOKE_SOURCES=0 ... sh $framework/ci/runtime/run-apache-smoke.sh</code> | 77 | First offline module build was blocked by a missing cached HTTPD APR library search path, not by source compilation. | <code>$task_tmp/build/apache-runtime</code> | None |
| <code>rtk env AUTO_FETCH_SMOKE_SOURCES=0 ... sh $framework/ci/runtime/run-apache-smoke.sh</code> | 1 | The patched module built successfully; the selected short case names did not become No-CRS cases because <code>NO_CRS_BASELINE=1</code> was absent. | <code>$task_tmp/build/apache-runtime</code> | None |
| <code>rtk env NO_CRS_BASELINE=1 ... sh connectors/apache/harness/run_apache_smoke.sh</code> | 0, not executable | Both cases lacked the required <code>MODSECURITY_RULE_PREAMBLE_FILE</code>; no traffic result was claimed. | <code>$task_tmp/build/apache-runtime/results-traffic</code> | None |
| <code>rtk env NO_CRS_BASELINE=1 MODSECURITY_RULE_PREAMBLE_FILE="$framework/tests/rules/no-crs-baseline.conf" ... sh connectors/apache/harness/run_apache_smoke.sh</code> | 0 | Fresh patched module passed the local Apache No-CRS traffic cases: <code>allow_without_marker=200</code> and <code>deny_header_marker_403=403</code>. | <code>$task_tmp/build/apache-runtime/results-traffic-verified</code> | None |
| <code>rtk env BUILD_ROOT="$task_tmp/build/final-docs" PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs</code> | 0 | Bilingual documentation check passed. | None | None |
| <code>rtk env BUILD_ROOT="$task_tmp/build/final-docs" PYTHONDONTWRITEBYTECODE=1 make check-doc-links</code> | 0 | Repository paths and documentation links passed. | None | None |
| <code>rtk env BUILD_ROOT="$task_tmp/build/final-docs" PYTHONDONTWRITEBYTECODE=1 make check-variable-documentation</code> | 0 | Variable documentation check passed. | None | None |
| <code>rtk env CI=true BUILD_ROOT="$task_tmp/build/final-lint" PYTHONDONTWRITEBYTECODE=1 make lint</code> | 0 | Full lint passed, including the Apache cleanup lint target and its APR harness. | <code>$task_tmp/build/final-lint</code> | None |
| <code>rtk env CI=true BUILD_ROOT="$task_tmp/build/final-quick" PYTHONDONTWRITEBYTECODE=1 make quick-check</code> | 0 | Quick-check passed and ran its lint and whitespace checks. | <code>$task_tmp/build/final-quick</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/final-target" PYTHONDONTWRITEBYTECODE=1 make check-apache-request-transaction-cleanup</code> | 0 | Post-commit source-contract tests and the APR lifecycle harness passed. | <code>$task_tmp/build/final-target</code> | None |
| <code>rtk git show --check --format=fuller --no-ext-diff f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b</code> | 0 | External implementation commit has no whitespace errors. | None | None |
| <code>rtk git diff --check</code> | 0 | Post-record working-tree diff has no whitespace errors. | None | None |

## Security impact

This closes a per-request native transaction lifetime gap that could accumulate
native state across Apache requests. The security-relevant boundary is the
adapter-to-libmodsecurity ownership transfer: a user request can cause native
transaction allocation, and its primary request pool now releases it exactly
once. No defaults, rule semantics, logging/redaction behavior, or intervention
cleanup behavior changed.

## Documentation changes

- <code>docs/connectors/apache.md</code> and
  <code>docs/connectors/apache.de.md</code> now state the primary-request
  ownership, pool cleanup ordering, and intentional redirect/subrequest reuse.
- This English/German Change Record pair and both Change Record indexes record
  the decision, verification boundary, and limitations.

## Runtime evidence

A local Apache module build and two local HTTP requests were executed with
<code>AUTO_FETCH_SMOKE_SOURCES=0</code>; the patched module observed HTTP 200
and HTTP 403 as described above. The run had no canonical run ID, and its
task-local artifacts are intentionally removed after this task. Therefore no
durable runtime evidence or production claim is made for this change. The
APR lifecycle harness is the direct evidence for cleanup ordering.

## Known limitations

- The APR harness uses the production cleanup callback and real APR pools, but
  it does not run an Apache worker with memory-leak instrumentation.
- The runtime smoke covers normal allow and deny traffic, not a long-running
  keepalive leak measurement, every error route, or every redirect/subrequest
  behavior.
- The original scan provenance and severity are unknown.

## Remaining risks

- A future change could bypass <code>create_tx_context</code> or change the
  primary-request sharing contract. The source regression test and APR harness
  guard the current wiring and ordering.
- <code>msc_intervention_cleanup</code> remains a separate scope and must be
  assessed independently.

## Checks not run and rationale

The network-backed canonical <code>make runtime-smoke-apache</code> target was
not run: without an invocation-local snapshot its wrapper can contact release
APIs during component preparation. The explicit offline module build and local
Apache harness instead used the available cache with
<code>AUTO_FETCH_SMOKE_SOURCES=0</code>. No memory-leak profiler was available;
the APR harness is the focused cleanup verification.

## Final diff and review status

Final review passed: the post-commit targeted cleanup check, bilingual/documentation
checks, <code>make lint</code>, <code>make quick-check</code>,
<code>git show --check</code> for
<code>f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b</code>, and the post-record
<code>git diff --check</code> passed. The implementation is in that external
commit; this Change Record pair and its index rows remain uncommitted. No commit,
staging, reset, Framework edit, or unrelated-worktree cleanup was performed by
this agent.
