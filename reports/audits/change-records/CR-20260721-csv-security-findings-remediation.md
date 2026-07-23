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
- The resulting PR is Draft/open and is not merged.

## Finding dispositions

| CSV row | Disposition |
| --- | --- |
| CSV-01 | Already fixed by Parent commit 1fc2321 (Apache phase-4 bypass); no duplicate patch. |
| CSV-02 | Already fixed by Parent commit 63819e4 (privileged submodule workflow); no duplicate patch. |
| CSV-03 | Implemented pinned and verified libmodsecurity tag/commit instructions before detached checkout, submodule update, build, test, and install. |
| CSV-04 | Implemented nonblocking authorization clients, monotonic deadline, bounded polling, and 408 for a slow client. |
| CSV-05 | Already fixed by Parent commit 63819e4 (updated-submodule workflow write token); no duplicate patch. |
| CSV-06 | Implemented strict verified-report provenance/evidence gate. Current evidence intentionally fails it, so final provenance is blocked_missing_evidence, not passed. |
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
| Strict generated-report layout checker against current evidence | expected failure: incomplete/stale evidence was rejected. This demonstrates CSV-06 fail-closed behavior and is not a passing provenance result. |
| make check-bilingual-docs and the canonical Framework-backed HAProxy harness | blocked: the Framework gitlink is intentionally absent in this Parent-only checkout and was not initialized or changed. |
| Final git diff --check after Change Record completion | passed: no whitespace errors in the task worktree. |
| Current-master continuation: `tests.test_runtime_path_security`, `tests.test_local_runtime_smoke_request_body`, `tests.test_haproxy_htx_transaction_id`, and `tests.test_generated_report_evidence_integrity` | passed: 90 tests, including symlink/ownership, request-framing, ASCII content-length, HTX-ID, and report-integrity controls. |
| Current-master continuation: `tests.test_resolve_runtime_paths` | passed: 8 tests. |
| Current-master continuation: workflow-security and compiler-guide suites | passed: 37 tests after the conflict union. |
| Current-master continuation: authorization-timeout smoke | passed with GCC and Clang using isolated external build roots; Common C17 helper check and shell syntax check also passed. |
| Current-master continuation: focused security-diff review | passed: no new plausible security regression in the reviewed ten-file remediation diff. |
| Exact-head Sonar `S3415` assertion-order follow-up | passed: 92 focused runtime-path, bilingual-documentation, and generated-report-evidence tests after all 22 actual/expected order corrections. |
| Current-master continuation: behaviorful timeout-smoke fake lifecycle | passed: GCC/Clang timeout-smoke compilation and execution exercise normal begin/finish ownership and count bookkeeping without changing the Common runtime ABI. |

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

No full host/connector matrix was available. The local helper test proves that
TE+CL or repeated CL/TE input receives 400 and is not forwarded to its test backend; it does not
establish Apache, NGINX, Lighttpd, HAProxy, HTTP/2, or HTTP/3 runtime behavior.
No Lighttpd queue/multi-chunk remediation evidence was available for CSV-10.

## Checks not run and rationale

- The strict verified-report gate cannot pass until current authentic runtime
  evidence is produced; missing/stale evidence was deliberately preserved as
  a failed control.
- Framework-backed canonical connector checks were not run because the
  Framework gitlink is absent and out of scope. It was not initialized,
  changed, staged, or committed.
- No MRTS work, deployment, production-host, full connector-matrix, HTTP/2,
  or HTTP/3 check was performed.

## Known limitations and follow-up

CSV-06 remains blocked_missing_evidence until authentic current verified
runtime reports satisfy the strict gate. CSV-10 remains blocked_missing_evidence
pending a pinned affected Lighttpd environment and queue/multi-chunk test
evidence. Both remain visible in the Draft PR and are not presented as solved.
The local S5443 source remediation is `fixed`, but it is not `verified` or
`closed` until a normal follow-up push receives a fresh exact-head SonarQube
Cloud Quality Gate and filtered issue readback. The shared root-local canonical
finding store is read-only, so its required incremental FND-SONAR-0010 import
is `blocked_permissions`; the retained task record does not claim to replace
that import. The exact PR head still needs ordinary CI, review, and
resulting-master evidence before any future integration decision.

The behaviorful `c:S995` timeout-smoke remediation requires a fresh hosted
exact-head Sonar readback. It does not suppress either warning or change the
public runtime declarations solely for a style rule.

## Remaining risks

The local controls cannot establish the missing Framework-backed canonical
connector checks, an affected Lighttpd runtime, a full host/connector matrix,
or remote PR CI status. Existing incomplete report evidence remains a
deliberate blocking condition. Descriptor metadata cannot prove host ACL
semantics or protect against a same-UID attacker after descriptors close; a
dir_fd-retaining sink refactor is outside this focused change. No control,
test, scanner, branch protection, or evidence requirement was weakened to
obtain a passing result.

## Delivery status

This record supports the existing Parent-only Draft PR #74. It deliberately
does not declare a current published head: every local continuation requires a
normal commit and push followed by a fresh exact-head check snapshot. It does
not authorize a merge, direct master push, Framework/MRTS work, history
rewrite, or a claim that remote CI passed.

## Final diff and review status

The current local whitespace review passed with git diff --check. The focused
security regression/control tests, 146-test selected Parent suite, four
runtime-path policy controls, and bilingual Change Record tests passed. One
Framework-backed policy checker is blocked by the intentionally absent
Framework gitlink, and Ruff is unavailable in the selected venv. A focused
security diff review, normal commit/push, fresh exact-head Sonar result,
remote CI, and human review remain separate observations until they occur.
