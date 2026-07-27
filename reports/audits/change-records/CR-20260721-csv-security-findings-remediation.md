# Change Record: CSV security findings remediation

**Language:** English | [Deutsch](CR-20260721-csv-security-findings-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260721-csv-security-findings-remediation |
| Date (UTC) | 2026-07-21 |
| Base revision | 5fa90474a79eaee2df034bf1c4389572fdcca42f |
| Boundary | Parent source, Parent tests, Parent CI/runtime tooling, Parent documentation, and this Change Record/index pair only. The branch retains the current Parent-master Framework gitlink, but this task does not modify Framework or MRTS. |
| Finding linkage | Imported Codex Security CSV rows CSV-01 through CSV-19; task-owned SonarQube Cloud S5443 follow-up FND-SONAR-0010. |

## Motivation and problem statement

The supplied Codex Security summary contains 19 findings spanning existing
remediations, build provenance, request parsing, runtime artifact confinement,
workflow evidence, generated reports, and connector-helper safety. This change
reconciles every row against the current Parent base, implements applicable
Parent-only remediation, and makes unresolved evidence gaps explicit.

## Acceptance criteria

- CSV-01 through CSV-19 each have an explicit disposition.
- Applicable Parent-only fixes have focused regression coverage; prior fixes
  are neither reverted nor duplicated.
- Ambiguous Transfer-Encoding plus Content-Length framing is rejected before
  a backend request is issued.
- Every configured runtime write root, including MATRIX_ROOT, is
  descriptor-confined and ownership-validated before use.
- A public writable runtime ancestor is accepted only after its opened
  descriptor proves root ownership and sticky semantics.
- Build and report-evidence controls fail closed.
- English/German documentation remains paired.
- The PR is eligible for protected integration only after a fresh exact-head
  full evidence run, all applicable checks, review/thread, and ruleset
  requirements pass; no direct `master` write or bypass is used.

## Finding dispositions

| CSV row | Disposition |
| --- | --- |
| CSV-01 | Already fixed by Parent commit 1fc2321 (Apache phase-4 bypass); no duplicate patch. |
| CSV-02 | Already fixed by Parent commit 63819e4 (privileged submodule workflow); no duplicate patch. |
| CSV-03 | Implemented pinned and verified libmodsecurity tag/commit instructions before detached checkout, submodule update, build, test, and install. |
| CSV-04 | Implemented nonblocking authorization clients, monotonic deadline, bounded polling, and 408 for a slow client. |
| CSV-05 | Already fixed by Parent commit 63819e4 (updated-submodule workflow write token); no duplicate patch. |
| CSV-06 | Implemented strict verified-report provenance/evidence gate. The workflow now provisions controlled local dependencies and runs the existing strict/full Parent producer before its terminal gate; its fresh exact-head outcome remains pending and is not claimed as passed here. |
| CSV-07 | Implemented descriptor-safe, no-follow, ownership-validated handling for all configured write roots, including MATRIX_ROOT. |
| CSV-08 | Already fixed by Parent commit a73c335 (blocked-status marker); no duplicate patch. |
| CSV-09 | Implemented Markdown fence marker/length validation for generated reports. |
| CSV-10 | No Lighttpd source change: blocked_missing_evidence. No pinned affected Lighttpd source/host/module or queue/multi-chunk client evidence is available in this isolated Parent checkout. |
| CSV-11 | Already fixed by Parent commit aabde81 (mutable project roots); no duplicate patch. |
| CSV-12 | Implemented remote-rule merging: blank remote values inherit local values; partial remote credential configuration is rejected. |
| CSV-13 | Implemented bounded local smoke request-body/chunk/trailer parsing and deadlines; TE+CL and repeated CL/TE framing are rejected before forwarding. |
| CSV-14 | Implemented validated verified-run identifiers for runtime artifact paths. |
| CSV-15 | Implemented strict BUILD_ROOT evidence propagation for report layout/provenance checks. |
| CSV-16 | Implemented random task-owned safe temporary writers instead of predictable paths. |
| CSV-17 | Implemented HAProxy HTX transaction identifiers bounded to the native 127-character payload limit, with a Parent-only regression. |
| CSV-18 | Implemented validation for German generated-report companions and their layout/evidence rules. |
| CSV-19 | Already fixed by Parent commit 0f82f74 (action majors); no duplicate patch. |

## Implementation decision and rationale

Only unresolved Parent-owned behavior changes. The authorization service now
uses monotonic timeout/nonblocking polling; the smoke helper rejects TE+CL and
repeated CL/TE framing before forwarding; all lifecycle write roots are descriptor-confined rather
than only the default root; run IDs, no-follow directory operations, and
random task-owned temporary directories prevent traversal, symlink, and
collision paths. Generated reports now require immutable build provenance,
strict layout/evidence, and structurally valid bilingual content. HAProxy
helper identifiers stay within the native buffer boundary. The Sonar follow-up
replaces pathname-only trust for public temporary roots with descriptor-based
directory, UID-0, sticky-bit, and writable-mode proof while retaining the
existing no-follow, descendant-owner, and final-root checks.

## Changed files

- compiler-guide generation and English/German compiler guides;
- verified-report workflow, evidence receipt/layout checks, and report
  generators;
- report-governance full-evidence orchestration and its focused CI-security
  regression contract, including failure-only bounded diagnostic paths;
- runtime path, run-ID, and temporary-directory helpers plus direct
  write-capable lifecycle entry points;
- local smoke request parsing, authorization timeout, remote-rule merging, and
  HAProxy HTX helper behavior;
- focused Python, shell, C, workflow, documentation, and evidence tests;
- this English/German Change Record pair and index pair.

## Current-master continuation (2026-07-23)

The Draft was refreshed from Parent `master`
`b37aa629398501f83750d6454f5f6a27eb614818` with an intentional union
resolution. The current immutable action pins, Go-version contract, strict
verified-report evidence gate, authorization-timeout check, and both language
indexes are retained together.

The continuation then resolves the locally remediable Sonar findings without
weakening a control: descriptor traversal and chunk parsing are split into
smaller helpers with the same guards, the content-length parser remains
ASCII-only, the authorization service binds per-connection state in a private
context, and the regression tests avoid nested/multiple-call assertion forms.
The timeout-smoke fake retains the non-const signatures declared by
`msconnector_runtime.h`, because its production implementations mutate those
objects; no scanner suppression or public ABI change was used.
An exact-head Sonar detail readback then identified 22 `python:S3415` test
assertion-order smells. They are corrected to the native `actual, expected`
order without changing any test condition or protected control. The two
`c:S995` timeout-smoke notices were genuine fake-lifecycle gaps rather than
const-correctness opportunities: the fake runtime now tracks active
transactions, and the fake transaction stores its owner and completion state.
The fake `begin` records a valid owner and increments its count; its idempotent
`finish` validates, decrements, and marks completion. This preserves the
shared non-const ABI and makes the smoke lifecycle behaviorful without a
scanner suppression.

The branch was then refreshed normally from current Parent `master`
`a308d7b414f0859490fe7253e0683a4bde80b563`. That inherited only the current
Framework gitlink update; no Framework or MRTS working tree was initialized,
modified, staged, or committed by this task.

## Integration remediation (2026-07-26)

The prior workflow ran a governance-only report check and then correctly
failed the strict consumer because no current runtime evidence had been
produced in its ephemeral runner. This remediation preserves the fail-closed
terminal gate and adds the existing Parent strict/full producer instead of
copying reports or receipts. The job creates a virtual environment using the
selected CPython 3.14 interpreter and installs the existing Framework
`requirements-ci.lock` with `--require-hashes`, `--only-binary`, and
`pip check`; it does not upgrade Pip or install `requirements-dev.txt`. It
enables the strict runtime-component path and supplies the reviewed immutable
Expat commit `c61098da494eea1cbd091118118dcee417faacea`, resolved from the
verified upstream `R_2_8_2` release. The Parent strict path rejects a branch,
tag, abbreviated SHA, or latest-release lookup and verifies the checkout head
before it can feed the producer. This is tracked as `FND-PARENT-0052`.

The job also grants the already-supported runtime download/build opt-ins and
has a 360-minute timeout matching the producer's documented 345-minute
maximum internal budget. The sequence is the hash-locked installation,
`make report-governance`, `make verified-report-run`, and the terminal
`make verified-report-evidence-gate`; the focused workflow-security test locks
that sequence, the strict mode, the provenance inputs, both opt-ins, and the
budget.

The isolated task worktree materializes the Parent-recorded Framework and MRTS
revisions only as runtime dependencies. No Framework/MRTS source change,
branch, commit, push, pull request, or Parent gitlink update is part of this
remediation. The published exact head
`28a4a1af5e764860d27ecb670bd82283e7b1aa74` reached the full producer in its
hosted push and pull-request runs, then correctly failed with
`apache_httpd: missing_local_httpd_build`. This record makes no fresh-runtime
success, SonarCloud, or merge claim: the hardened next exact head must run in
hosted CI before any such result can be asserted.

The prior failure-only diagnostic printed only the outer producer log, so it
showed the Apache classification but not the inner build cause. It now reads
only the regular, non-symlink
`$BUILD_ROOT/verified-runs/current-run-id` pointer; rejects an empty identifier,
one longer than 128 characters, one without an initial alphanumeric character,
or one containing characters outside `[A-Za-z0-9._-]`; and constructs exactly
`$BUILD_ROOT/verified-runs/$run_id/logs/02-make-prepare-runtime-components.log`.
It tails that path and the additional fixed
`$BUILD_ROOT/logs/runtime-components/apache-build.log` only when each is a
regular, non-symlink file, with each tail limited to 300 lines. It does not
recurse, glob, or expose a broad log root. Each raw-log tail is surrounded by a
fresh `uuidgen` GitHub `::stop-commands::` token and its matching resume token,
so log content cannot be interpreted as a workflow command. The diagnostic
neither accepts the failed producer nor changes the terminal gate; it only
makes the legitimate Apache remediation observable on the next exact-head run.

+## PCRE2 digest remediation (2026-07-26)

The fresh hosted bounded diagnostic at exact head `d93446a1b53be344f5599c48272060e2c664ae86` exposed the inner failure in run `30193495484`, job `89770795068`:

```text
apache_poc: blocked missing required SHA256 digest for pcre2
```

The Parent `Makefile` unconditionally exported an otherwise undefined `PCRE2_SHA256`. GNU Make consequently passed an explicit empty value to the Framework and suppressed its deliberate unset-only default. The Parent archive prefetch path also treated PCRE2's digest as optional, allowing checksum-URL fallback, download, archive parsing, and cache publication before Framework correctly rejected an empty digest before extraction.

The Parent-only correction does not duplicate the Framework pin. It exports `PCRE2_SHA256` only when GNU Make reports an actual caller-provided value and requires a literal 64-hex digest before Parent creates archive/cache state. Valid input is normalized to lowercase; empty, whitespace-only, malformed, and mismatching input remains fail-closed, and `PCRE2_SHA256_URL` cannot repair a missing literal digest. Framework remains the single default-pin authority and its extraction-time verifier is unchanged. This correction is tracked by `FND-PARENT-0053`.

Focused local evidence passed: 33 cache-contract/cache-identity tests, 20 CI-security tests, 18 runtime-component tests, `make check-ci-security-contract`, variable-documentation validation, bilingual-documentation validation, and `git diff --check`. The direct Framework PCRE2 archive-digest fixture did not pass: its synthetic V3 source lacks the current required non-symlink `.gitmodules` manifest and is rejected before it reaches its intended PCRE2 assertions. That separate Framework fixture regression is recorded as `FND-FRAMEWORK-0056`; no Framework or MRTS source, branch, gitlink, or delivery action is included here.

These local controls are not hosted runtime evidence. A fresh exact-head hosted strict/full producer and unchanged terminal evidence gate must pass after normal PR-branch publication before SonarCloud, review, integration, or resulting-master success is claimed.

## Runtime-matrix diagnostic follow-up (2026-07-26)

At exact head `7238c9d0a0902affbf7dfae1d7f96d6603d80f89`, hosted run `30196090664`, job `89777788658` passed component preparation, runtime-producer readiness, and the bounded Apache control; `apache_poc` reported the built module. The strict/full producer then failed at `make runtime-matrix-all-runtime` with `rc=2`, and dependent matrix, report-refresh, layout, lint, and quick-check consumers also failed or became invalid. The outer job log retained the fixed nested path `verified-runs/<validated-run-id>/logs/04-make-runtime-matrix-all-runtime.log` but not its causal content.

The Parent-only follow-up adds no acceptance path and does not change the terminal evidence gate. On failure it derives that one fixed matrix log only after validating the existing regular non-symlink run-ID pointer, requires the log itself to be a regular non-symlink file, emits at most 300 lines, and shields raw content with a fresh GitHub `stop-commands` token. It retains the existing bounded preparation and Apache diagnostics. The next exact hosted head must supply the matrix cause; no matrix, SonarQube Cloud, review, integration, or resulting-master success is claimed here. This opaque evidence gap is tracked as `FND-PARENT-0054`.

## SonarQube Cloud follow-up (2026-07-26)

The SonarQube Cloud PR analysis for exact head `b28b8744765a2cac6e3cf91f7bd3070d49d7774d` passed its Quality Gate but still reported 22 OPEN task-owned findings and 59 new duplicated lines (1.6638465877044557%). This does not meet the current delivery acceptance criterion of zero open PR findings and zero new-code duplication.

The focused Parent-only remediation puts the observed value before the expected value in the affected `unittest` equality assertions, reuses the existing compiled immutable-Git-commit expression instead of repeating its literal, and removes duplicate transaction-ID boundary coverage from the helper-local test because the dedicated Parent regression test already owns that behavior. It changes no SonarQube Cloud rule, Quality Gate, exclusion, suppression, coverage threshold, scanner configuration, Framework, MRTS, or gitlink.

Fresh exact-head SonarQube Cloud analysis is still required after publication. No zero-issue, zero-duplication, CI, review, integration, or resulting-master success is claimed by this record before that analysis completes.

## Payload-safe hosted evidence retention follow-up (2026-07-26)

An exact-head review of Parent PR #74 found that `make verified-report-run`
does create the current `verified-run-manifest.generated.json`,
`report-freshness.generated.json`, `report-refresh-manifest.generated.json`,
`verified-commands.json`, `full-matrix-aggregate-receipt.json`, the raw
`full-runtime-matrix-runs.jsonl` index, and the twelve job-local `job.json`
records. They are created only in the ephemeral GitHub-hosted runner, however:
the workflow had no artifact-upload step and its successful logs expose only
command outcomes rather than the complete machine-readable receipt chain.
That does not meet FND-CROSS-0001's retained freshness-manifest acceptance
criterion.

The first artifact-retention successor was not accepted as evidence: a review
found that its shell pathname checks did not bind the later upload action to
the checked files. The two task-owned runs for that unsafe successor were
cancelled before upload; no artifact was created or inspected from them.

The corrective Parent-only follow-up keeps the full producer and initial
strict gate. It stages the fixed eighteen-file structured allowlist through
descriptor-relative `O_NOFOLLOW` traversal, stable regular-file reads, and
exclusive writes into a new random child of a private runner-owned staging
parent. The upload action receives only that staged root. A final strict gate
then runs again and the same descriptor-safe code compares every staged digest
and byte count with the live source set, rejecting additions, symlinks,
replacement, or a changed source before upload. The artifact retains for ten
days and fails when the staged root is missing. It contains the three generated
manifest JSON files, the current run's command and aggregate receipts, the raw
matrix index, and all twelve job JSON records. It deliberately excludes build
trees, raw logs, `run.log`, result JSONL, request/response payloads, headers,
and cookies.

The workflow also removes duplicate expensive PR work without shortening the
runtime proof: automatic pushes are limited to `master`, every pull request
still receives one full producer, and a same-PR/ref concurrency group cancels
only superseded runs. A separate short read-only contract preflight runs
`make check-ci-security-contract` before the 360-minute producer job. Both
jobs check out the exact pull-request head (or the event SHA outside a PR), so
the artifact identity uses that same revision. The workflow keeps
`permissions: contents: read`, does not use `pull_request_target`, does not
receive secrets, and gains no write permission. After its setup-python
interpreter verifier, the preflight explicitly sets `PYTHON=python3`, so Make
cannot select a repository-local `.venv` supplied by an untrusted pull request.

This is a descriptor-safe staged snapshot, not a transactional filesystem
snapshot or a protection against an arbitrary surviving same-UID process that
can modify a runner path after the final comparison. The retained-evidence
claim therefore requires the hosted runner to have no such untrusted surviving
process from final comparison through upload; a stronger model would require a
separate identity or an uploader consuming a protected descriptor/stream.

The active pre-retention runs cannot be retroactively supplied with this
artifact. A successor exact PR head must pass the complete hosted producer,
both strict-gate observations, the staged-source binding, and the new
payload-safe upload before the artifact can be downloaded and checked for one
matching run ID, current Parent and Framework revisions, declared hashes, and
no stale or unexplained mismatch.
No FND-CROSS-0001 closure, SonarQube Cloud result, review result, or protected
integration success is claimed here.

## Commands executed

| Command or control | Result |
| --- | --- |
| Focused Parent unittest suite for compiler guides, workflow security, bilingual documentation, generated-report evidence, runtime paths, path resolution, smoke request bodies, and HAProxy HTX IDs | passed: 146 tests after the S5443 follow-up (the earlier rebased suite contained 144 tests). |
| Pre-fix S5443 regression trio for root-owned/sticky, unsafe-root, and foreign-owner paths | expected failure: the old pathname allowlist rejected the synthetic safe root before it could exercise the intended ownership path. |
| Post-fix S5443 regression trio | passed: root-owned sticky shared root succeeds; non-sticky/non-root shared roots and foreign-owned descendants fail before final-root creation. |
| Four focused runtime-path policy controls | passed: mutable-root, broad-parent, selected Python policy, and system-root rejection controls remain passing. |
| Complete runtime-path policy unittest module | blocked_environment for one Framework-backed shell checker: the intentionally uninitialized Framework gitlink lacks `ci/lib/common.sh`; the other four controls passed. |
| Ruff check / format check for the two Python files | not_run: the selected Parent virtual environment has no `ruff` executable; no dependency installation was performed. |
| make check-http-authorization-service-timeout with GCC and with Clang | passed for both compilers. |
| make check-common-helpers-c17 with GCC and with Clang | passed for both compilers. |
| Common SDK and common security source-contract controls | passed. |
| sh -n for three changed runtime lifecycle shell entry points | passed. |
| Pre-remediation strict generated-report layout checker against the then-current evidence | expected failure: incomplete/stale evidence was rejected. This demonstrates CSV-06 fail-closed behavior and is not a passing provenance result. |
| make check-bilingual-docs and the canonical Framework-backed HAProxy harness | blocked: the Framework gitlink is intentionally absent in this Parent-only checkout and was not initialized or changed. |
| Final git diff --check after Change Record completion | passed: no whitespace errors in the task worktree. |
| Current-master continuation: `tests.test_runtime_path_security`, `tests.test_local_runtime_smoke_request_body`, `tests.test_haproxy_htx_transaction_id`, and `tests.test_generated_report_evidence_integrity` | passed: 90 tests, including symlink/ownership, request-framing, ASCII content-length, HTX-ID, and report-integrity controls. |
| Current-master continuation: `tests.test_resolve_runtime_paths` | passed: 8 tests. |
| Current-master continuation: workflow-security and compiler-guide suites | passed: 37 tests after the conflict union. |
| Current-master continuation: authorization-timeout smoke | passed with GCC and Clang using isolated external build roots; Common C17 helper check and shell syntax check also passed. |
| Current-master continuation: focused security-diff review | passed: no new plausible security regression in the reviewed ten-file remediation diff. |
| Exact-head Sonar `S3415` assertion-order follow-up | passed: 92 focused runtime-path, bilingual-documentation, and generated-report-evidence tests after all 22 actual/expected order corrections. |
| Current-master continuation: behaviorful timeout-smoke fake lifecycle | passed: GCC/Clang timeout-smoke compilation and execution exercise normal begin/finish ownership and count bookkeeping without changing the Common runtime ABI. |
| Historical hosted exact-head CI and SonarCloud for `95c59343dca602b8b6412b307b0d0002a3dca91d` | passed for SonarCloud Quality Gate and every non-evidence GitHub check; the filtered Sonar issue query returned zero open issues. `report-governance` correctly failed only on missing/stale runtime receipts and downstream evidence. |
| Integration remediation: focused `tests.test_prepare_runtime_components` and `tests.test_ci_security_workflows` with the task-local Python environment | passed: 37 tests cover strict immutable-Expat dispatch, mutable-ref rejection before source preparation, checkout-head mismatch rejection, non-strict compatibility, accurate runtime guardrail descriptions, and the workflow contract. |
| Integration remediation: `make check-ci-security-contract` with the task-local Python environment | passed: 19 workflow-security tests plus actionlint, zizmor, and gitleaks lock validation. |
| Integration remediation: `ci/checks/documentation/check-bilingual-docs.py` with the task-local Python environment | passed: the updated English/German Change Record pair remains structurally paired. |
| Integration remediation: `git diff --check` | passed: no whitespace error in the scoped PR #74 worktree. |
| PR #74 bounded-diagnostic hardening: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 .venv/bin/python -m unittest -v tests.test_ci_security_workflows` | passed: 19 tests, including the exact current-run pointer, identifier validation, two fixed log paths, regular/non-symlink gate, 300-line bound, command shielding, and preserved terminal-gate ordering. |
| PR #74 bounded-diagnostic hardening: `rtk proxy env PYTHON=.venv/bin/python PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make check-ci-security-contract` | passed: the same 19 workflow-security tests plus actionlint, zizmor, and gitleaks lock validation. |
| PR #74 bounded-diagnostic hardening: `rtk proxy env PYTHON=.venv/bin/python PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make check-bilingual-docs` | passed: the English/German Change Record pair remains structurally paired after the two-path diagnostic update. |
| PR #74 bounded-diagnostic hardening: `rtk git diff --check -- .github/workflows/verified-report-governance.yml tests/test_ci_security_workflows.py reports/audits/change-records/CR-20260721-csv-security-findings-remediation.md reports/audits/change-records/CR-20260721-csv-security-findings-remediation.de.md` | passed: no whitespace error in the scoped four-file diff. |
| Payload-safe hosted-evidence retention: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_ci_security_workflows` | passed: 20 tests, including strict-gate ordering, immutable action pin, SHA/run-bound artifact name, complete 12-job allowlist, and exclusion of logs and result payload paths. |
| Payload-safe hosted-evidence retention: `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | passed: the same 20 workflow-security tests plus actionlint, zizmor, and gitleaks lock validation. |
| Payload-safe hosted-evidence retention: `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | passed: the English/German Change Record pair is structurally paired. |
| Payload-safe hosted-evidence retention: `git diff --check -- .github/workflows/verified-report-governance.yml tests/test_ci_security_workflows.py reports/audits/change-records/CR-20260721-csv-security-findings-remediation.md reports/audits/change-records/CR-20260721-csv-security-findings-remediation.de.md` | passed: no whitespace error in the scoped four-file diff. |
| Artifact-retention security correction and runtime-efficiency follow-up: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_generated_report_evidence_integrity tests.test_ci_security_workflows tests.test_python_version_contract` | passed: 117 tests cover descriptor-relative staging of all 18 allowlisted records, intermediate/final symlink rejection, source replacement and mutation checks, staged-source binding, the exact workflow order, and the Python workflow inventory. |
| Artifact-retention security correction and runtime-efficiency follow-up: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | passed: 20 workflow-security tests plus actionlint, zizmor, and gitleaks lock validation. |
| Artifact-retention security correction and runtime-efficiency follow-up: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract` | passed: canonical Python 3.14.6 and 29 Python-executing workflow jobs; the staged workflow uses static, previously verified `python3` command heads and a private virtual-environment PATH. |
| Artifact-retention security correction and runtime-efficiency follow-up: `rtk proxy timeout 180s env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/checks/documentation/check-bilingual-docs.py` | passed: `bilingual docs ok`. |
| Artifact-retention security correction and runtime-efficiency follow-up: Framework workflow-YAML checker and `git diff --check` | passed: the Parent workflow parses and the scoped diff has no whitespace error. |

## Security impact

This is defense-in-depth work across request processing, local runtime tools,
CI/report provenance, and a connector helper. It closes a tested local-helper
forwarding case for ambiguous TE+CL and repeated CL/TE framing and a plausible configured-MATRIX_ROOT
containment gap found during review. The S5443 follow-up also rejects a
root-owned but non-sticky public ancestor instead of accepting it by pathname.
The bounded failure diagnostic is additional defense in depth, not a validated
vulnerability: it treats raw local build logs as untrusted workflow output and
prevents their content from becoming GitHub workflow commands while preserving
the producer's nonzero failure.
The hosted-evidence continuation is similarly allowlisted and success-only:
it descriptor-opens every source component without following symlinks, makes a
stable read of each of the fixed eighteen structured records, and writes an
exclusive staged copy under a private runner-owned root. The upload receives
only that staged root. After the second unchanged strict gate, the same
descriptor-safe logic compares every staged digest and byte count with the
current source set and rejects an addition, symlink, replacement, or changed
source before upload. It does not upload logs, result payloads, build trees,
credentials, or broad directories, and it preserves the existing read-only
workflow permission model. This protects the normal runner boundary; it is not
a transactional filesystem snapshot against an arbitrary surviving same-UID
process after the final comparison.
It does not claim production-host exposure,
a complete connector matrix, or production exploitability beyond the controls
that were tested.

## Runtime evidence

Before the integration remediation, no full host/connector matrix was
available. The local helper test proves that
TE+CL or repeated CL/TE input receives 400 and is not forwarded to its test backend; it does not
establish Apache, NGINX, Lighttpd, HAProxy, HTTP/2, or HTTP/3 runtime behavior.
No Lighttpd queue/multi-chunk remediation evidence was available for CSV-10.

The updated unprivileged workflow now runs the existing strict/full Parent
producer in the ephemeral checkout and retains the terminal strict consumer.
The exact head `28a4a1af5e764860d27ecb670bd82283e7b1aa74` reached that producer
but failed with `apache_httpd: missing_local_httpd_build`; the outer
`prepare-runtime-components` summary did not include the Apache build cause.
The hardened two-path diagnostic is not runtime evidence and does not repair
Apache. A subsequent exact-head hosted run must show the bounded Apache-build
tail, re-exercise the unchanged strict producer and terminal consumer, and
provide a revision-bound receipt chain before any success is claimed. The
strict producer's Python and Expat inputs remain immutable/reviewed before it
can mint that evidence; its non-strict compatibility path is not an evidence
substitute.

## Checks not run and rationale

- The fresh exact-head full runtime run and terminal strict gate are pending
  publication of this remediation. They must run in hosted CI; missing/stale
  evidence is still rejected rather than accepted as a substitute.
- Framework-backed canonical connector checks remain outside the source-change
  scope. The task-owned isolated worktree materialized the recorded Framework
  and MRTS revisions read-only for runtime dependency preflight; neither
  repository was changed, staged, committed, pushed, or made a PR target.
- No MRTS work, deployment, production-host, full connector-matrix, HTTP/2,
  or HTTP/3 check was performed.

## Known limitations and follow-up

CSV-06 remains blocked_missing_evidence until the updated workflow's
authentic current verified-runtime reports satisfy the strict gate. CSV-10
remains blocked_missing_evidence pending a pinned affected Lighttpd environment
and queue/multi-chunk test evidence. Neither condition is presented as solved
before a fresh exact-head result. `FND-PARENT-0052` remains in progress until
the updated exact head demonstrates the hash-locked Python install, immutable
Expat checkout, full producer, and terminal gate in hosted CI.
The local S5443 source remediation and the behaviorful `c:S995` timeout-smoke
remediation are verified on published exact head
`95c59343dca602b8b6412b307b0d0002a3dca91d`: SonarCloud completed its new
analysis at 2026-07-23T14:14:56Z with an `OK` Quality Gate and a filtered
open-issue count of zero. The shared root-local canonical finding store is
read-only, so its required incremental FND-SONAR-0010 import is
`blocked_permissions`; this retained Change Record does not claim to replace
that import. The exact head has passing hosted non-evidence CI, while the
strict report-evidence gate remains intentionally blocked. Human review and
resulting-master evidence remain required before any future integration
decision.

## Remaining risks

The local controls cannot establish the missing Framework-backed canonical
connector checks, an affected Lighttpd runtime, or a full host/connector
matrix. The earlier hosted exact-head snapshot is historical; the updated
full-evidence run remains a blocking condition until its new exact-head result
is observed. Incomplete report evidence remains rejected.
Descriptor metadata cannot prove host ACL semantics or protect against a
same-UID attacker after descriptors close; a dir_fd-retaining sink refactor is
outside this focused change. No control, test, scanner, branch protection, or
evidence requirement was weakened to obtain a passing result.

## Delivery status

This record supports the current Parent-only PR #74 remediation. The current
user has authorized protected integration after all exact-head prerequisites,
but this record itself does not authorize a direct master push, bypass,
Framework/MRTS work, history rewrite, or a claim that the strict
report-evidence gate passed. The updated head must be published and verified
before the PR is made ready or integrated.

## Final diff and review status

The current local whitespace review and the updated bilingual Change Record
check passed. The focused 19-test workflow-security contract and tool-lock
validation passed, while full runtime evidence, fresh SonarCloud, fresh hosted
CI, human review, and resulting-master evidence remain separate requirements.
Historical focused security regression/control tests, the 146-test selected
Parent suite, and four runtime-path policy controls remain recorded above.

## CPU-aware full-matrix scheduling follow-up (2026-07-26)

The full runtime matrix now defaults its isolated runtime-job cap to the
online processor count detected by `nproc`, then
`getconf _NPROCESSORS_ONLN`, with a safe fallback of one. An explicit positive
`FULL_MATRIX_MAX_PARALLEL_JOBS` value remains an upper bound for shared
runners. In the observed task environment both commands report 12, so a
fully prepared twelve-job matrix can admit all twelve jobs without a manual
cap override.

Preparation remains serial to avoid concurrent cache refreshes. Only after all
requested cache-backed connector artifacts are ready does the Parent scheduler
admit globally planned jobs through a completion-driven worker pool. It refills
each freed slot immediately rather than waiting for a slow batch sibling, and
the Parent alone writes the manifest in plan order. If an artifact is not
prepared, execution remains serial. A dependency-free planner reserves and
validates disjoint Apache, NGINX, and HAProxy listener-search windows in the
unprivileged port range before any runtime command starts.

The completion path is fail-closed. A regular non-symlink FD-9 `flock` keeps
competing matrix runs out, while a private FIFO associates each completion with
one tracked child PID. A generation-bound watchdog uses the existing positive
`VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS` limit: if a wrapper dies before
reporting completion, the scheduler exits 77 rather than waiting forever.
The watchdog closes FD 9 before sleeping, so it cannot prolong the lock after
a killed parent; real job descendants continue to hold the lock until their
own exit. A completion exactly at the timeout boundary may conservatively
produce exit 77, which preserves the evidence and isolation controls.

Local validation passed `sh -n`, `git diff --check`, the 107-test selected
Python regression command with `-W error::ResourceWarning`,
`make check-ci-security-contract`, variable and bilingual documentation
checks, the Python-version contract, pinned Actionlint, and offline Zizmor.
Focused controls prove the detected default cap, cap-two work conservation,
port-plan rejection, live-lock rejection, parent-kill lock reuse, and the
bounded lost-wrapper failure followed by lock reuse. These local checks do not
replace the new exact-head hosted producer, GitHub, SonarQube Cloud, review,
or integration evidence required before this Draft PR can be verified or
merged.

## Exact-head SonarQube Cloud correction (2026-07-26)

The direct PR #74 readback for published head
`a9086a4527d7c82fa4657d229099b1ef2fe12f9c` reported four task-owned `OPEN`
issues despite an `OK` Quality Gate: unused `build_root` in
`_current_verified_run_id_for_staging`, inconsistent listener-offset return
shape, and cognitive-complexity reports for the port planner and exact staged
tree reader. The same readback reported `new_duplicated_lines=38` and
`new_duplicated_lines_density=0.5794449527294907`, all from the two
same-file scheduler lock-reuse test blocks. That does not meet this task's
stricter zero-open/zero-duplication acceptance criterion.

The follow-up makes only behavior-preserving Parent changes. The receipt
reader no longer receives an unused path and splits its descriptor-relative,
`O_NOFOLLOW`, exact-allowlist traversal into small helpers without changing
the path-containment checks. The port planner builds one typed offset sequence
and delegates uniqueness, ordering, and allocation while retaining its
fail-closed collision and range checks. The scheduler tests share their
post-descendant lock-reuse retry helper, preserving the individual assertions.
No SonarQube Cloud rule, Quality Gate, exclusion, suppression, coverage
setting, Framework, MRTS, Gitlink, or master branch was changed.

The selected local 107-test regression command with
`-W error::ResourceWarning` passed after these corrections. The next normal
follow-up commit still requires fresh exact-head hosted CI and a direct
SonarQube Cloud readback before zero open issues, zero duplication, PR
verification, or integration can be claimed; PR #74 remains Draft.

## Superseding slim hosted-workflow continuation (2026-07-27)

This continuation supersedes only the hosted-delivery expectation in the
earlier entries. It preserves their chronology: the former strict/full
producer, twelve-cell runtime matrix, report refresh/generation, staged
artifact, and their failed hosted runs remain historical diagnostic evidence,
but they are no longer prerequisites for the slim successor of Parent PR #74.
In particular, their Apache, PCRE2, and matrix failures do not fail the new
hosted workflow and are not presented as resolved by this decision.

The required hosted configuration is the exact current-`master` report
governance workflow: one read-only `report-governance` job, a 20-minute
timeout, and `make report-governance`. GitHub must not run
`verified-report-run`, an `all`/runtime-all or twelve-cell matrix, report
refresh or generation, the strict evidence gate, runtime downloads or builds,
or an artifact upload. The full producer, twelve-cell matrix, and report
generators remain available solely as intentional, manual local work; this
continuation neither removes nor treats them as GitHub PR evidence.

The PR #55 provenance source bridge is transferred separately into #74. Its
former strict hosted gate is not retained on either slim PR; this record makes
no claim that #55 has been closed or that either PR has been merged.

The bounded baseline-Sonar objective is 103 `python:S3415`
assertion-order corrections plus two pre-existing `S5443` secure-temporary
file fixes. It uses real source/test corrections, not an exclusion,
suppression, Quality-Gate change, or scanner weakening. A final reduction of
the Sonar main-branch baseline is deliberately pending post-merge master
analysis; PR analysis alone cannot establish that result.

No post-supersession exact-head GitHub run, Sonar PR analysis, or Sonar
main-branch analysis is claimed here. Historical local passes and historical
full-runtime outcomes above do not validate this successor configuration. The
remaining evidence is focused local testing of the transferred source and
Sonar corrections, a fresh exact-head 20-minute GitHub governance run, a
fresh Sonar PR readback with no new-code regression, normal review/ruleset
checks, and, after an authorized merge, the master Sonar analysis that measures
the bounded baseline reduction.

## Final exact-head continuation (2026-07-27)

This continuation adds final PR-head evidence without revising the chronology
above: the immediately preceding statement that no post-supersession exact-head
run or analysis was claimed was accurate at that time. At
`975c9f6e7fbe192346c253d1d68faac360e75ee1`, the hosted-delivery scope remains
the slim GitHub workflow described above; the former full producer, runtime
matrix, report refresh/generation, strict evidence gate, downloads/builds, and
artifacts remain outside hosted PR execution.

The baseline-Sonar remediation now totals 128 `python:S3415` assertion-order
corrections: the initial 103 plus 25 exact-head follow-up corrections. It also
retains the two existing `S5443` secure-temporary-file fixes. These remain
source/test corrections, not an exclusion, suppression, Quality-Gate change,
or scanner weakening.

For that exact PR head, Sonar PR analysis has a passed Quality Gate, zero new
`OPEN`/`CONFIRMED` issues, zero new security hotspots, and zero new-code
duplication. All required GitHub checks passed on the same head; configured
non-applicable checks remain intentionally skipped.

Those are PR-head results only. PR #74 is open at this point; this continuation
claims neither a merge nor a master result, including no post-merge master
Sonar baseline reduction. Such a result remains contingent on an authorized
integration and subsequent master analysis.
