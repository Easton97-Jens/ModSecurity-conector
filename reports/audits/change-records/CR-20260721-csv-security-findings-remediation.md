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
  regression contract;
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
remediation. This record makes no fresh-runtime, SonarCloud, or merge claim:
the updated exact head must be published and run in hosted CI before those
results can be asserted.

If the full producer fails, a failure-only diagnostic now prints the bounded
tail of its fixed `prepare-runtime-components` log from the task-owned verified
run root. It neither accepts the failed run nor changes the terminal gate; it
only makes a legitimate CI blocker observable for a focused follow-up.

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

## Security impact

This is defense-in-depth work across request processing, local runtime tools,
CI/report provenance, and a connector helper. It closes a tested local-helper
forwarding case for ambiguous TE+CL and repeated CL/TE framing and a plausible configured-MATRIX_ROOT
containment gap found during review. The S5443 follow-up also rejects a
root-owned but non-sticky public ancestor instead of accepting it by pathname.
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
The only acceptable fresh proof is its exact-head hosted result and its
revision-bound runtime receipt chain; that run is pending publication of this
change and is not substituted by the local static-contract checks above. The
strict producer's Python and Expat inputs are now immutable/reviewed before it
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
