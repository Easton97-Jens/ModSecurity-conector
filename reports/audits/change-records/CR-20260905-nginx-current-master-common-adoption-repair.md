# Change Record: NGINX current-master Common-adoption contract repair

**Language:** English | [Deutsch](CR-20260905-nginx-current-master-common-adoption-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260905-nginx-current-master-common-adoption-repair |
| Date (UTC) | 2026-09-05 |
| Base revision | b779167ff979aa73cdd9321a829f9c693d943760 |
| Delivery status | Local checker repair on an authorized focused branch. No commit, push, pull request, Ready-for-Review action, or merge is asserted by this record. A normal Draft PR is authorized only after fresh delivery preflight and final local evidence. |

## Motivation and problem statement

After the authorized PR #356 squash merge, 14 resulting-master workflows on
`b779167ff979aa73cdd9321a829f9c693d943760` became terminal: nine succeeded
and five stopped at the same two NGINX Common-adoption checker assertions. The
Apache Common-adoption assertion passed in the failed Apache workflow.

The two assertions were stale checker shapes, not evidence of an NGINX runtime
defect. The live request mapper is fail-closed, while the Server response
header resolver now delegates to a bounded Common wrapper instead of calling
the raw response-header sink directly. `FND-PARENT-1010` remains in progress
pending this successor's exact-head delivery evidence.

## Acceptance criteria

- The checker requires failed request mapping to return `NGX_HTTP_BAD_REQUEST`
  and requires the initializer's exact fail-closed propagation before hostname
  and request-header processing.
- The checker requires the Server resolver to preserve its explicit length,
  call `ngx_http_modsecurity_add_n_response_header`, and contain no raw
  `msc_add_n_response_header` call.
- The checker requires the Common response-header wrapper to reject validation
  failure with `NGX_ERROR` before the raw sink.
- Isolated negative controls reject altered mapper return, mapper propagation,
  Server raw-sink, and response-validation branches.
- The affected mapper, Server-resolver, and Common-wrapper predicates use a
  C-translation-phase-normalized lexical view: trigraph conversion,
  backslash-newline splicing, and `%:` directive digraphs occur before
  comments, strings, character literals, and conditional branches are
  excluded. A UCN escape in a checked code or macro source boundary is
  rejected. An inactive branch—including the outer include guard's `#else`—cannot furnish a
  fail-closed branch or raw-sink marker; only the verified primary branch of
  the Common header's canonical outer include guard is structurally retained.
- The repaired mapper, initializer, and Common-wrapper predicates require one
  exact direct failure/sink shape and reject nested, unbraced, or non-linear
  control flow around it. This is a conservative static-contract constraint,
  not a claim of complete C control-flow proof.
- The checker fails closed when a source-level macro directive redefines,
  undefines, supplies a checked token, contains a UCN, token-pasting, or a
  control-flow token in its replacement list. The only control-flow exception
  is the existing function-like `dd*` diagnostic form whose replacement is
  exactly `do { ... } while (0)` and whose body has no control-flow token. A
  function-like macro is otherwise allowed only when it is one of the exact
  existing empty `dd(...)` or PCRE allocation-shim forms. A
  quoted local include is rejected when dynamic, path-unsafe, or outside the
  scanned NGINX, Common, and profile source set. The explicitly modeled
  external `stdio.h` exception is allowed only when no local candidate can
  shadow it. An angle-bracket include must use the fixed current external-
  header allowlist and satisfy the same local-shadow check; nonstandard
  `#include_next` and `#import` are rejected.
- The Common response-header wrapper has exactly two lexical `return` tokens:
  its direct validation-failure return and its final direct raw-sink return.
  An earlier macro-mediated return or an unreachable raw-sink decoy cannot
  satisfy the bounded response-header contract.
- No NGINX C runtime source, Framework, MRTS, Gitlink, workflow, ruleset,
  branch protection, required check, Quality Gate, exclusion, suppression,
  source-lock, provenance, PR #346, or `master` change is included.

## Implementation decision and rationale

The repair changes only
`ci/checks/connectors/nginx/check-nginx-common-adoption.py`. It scopes the
existing source checks to the two relevant C functions and requires exact
fail-closed mapper, initializer-propagation, and Common response-header
validation branches. The source view normalizes C trigraphs, line splicing,
and `%:` preprocessing digraphs before masking comments, strings, character
literals, and inactive preprocessor branches. A comment-masked companion view
retains the real mapper diagnostic literal without allowing non-code text to
supply it.

The checker permits only the verified primary branch of the Common header's
canonical outer include guard; its `#else` is masked along with every other
conditional branch. It rejects UCN escapes in the checked code and complete
macro source boundary before directive matching, and requires one direct
branch/call/sink shape while rejecting nested, unbraced, and non-linear control
flow. Required controls must therefore be unconditional and structurally direct
source code; a future legitimate conditional or control-flow refactor requires
an intentional contract and negative-control update. The forbidden direct raw
response-header sink remains checked across all lexical code, including
conditional branches.

The checker also treats source-level macro and include integrity as
prerequisites for both repaired assertions. It scans the local NGINX source
set, Common C/C++ headers, and the current `connectors/profile_registry.h`
quoted include; rejects `#undef`, unapproved names, critical macro
redefinitions, UCNs in the complete non-comment/non-literal macro source view,
replacement lists containing security-critical or control-flow tokens, and
token pasting. The only permitted control-flow replacement is the structurally
bounded function-like `dd*` diagnostic `do { ... } while (0)` form with no
control-flow token in its body. A quoted local include is accepted only if it
is a regular C/C++ header at a safe path that resolves to that input set.
Dynamic include forms are rejected. Angle-bracket includes require the fixed
external-header allowlist and are rejected if an existing local candidate does
not resolve to that input set. The existing quoted `stdio.h` is a fixed
external exception only without a local candidate at the modeled search roots.
Nonstandard `#include_next` and `#import` directives are rejected.

Function-like macros are accepted only for the existing empty `dd(...)` form,
the bounded `dd*` diagnostic form, and the two exact PCRE allocation shims.
This rejects parameter substitution that could otherwise turn a caller-supplied
identifier into a raw response-header sink before validation.

For the Common response-header wrapper, the checker also requires exactly two
lexical `return` tokens: the direct validation-failure return followed by the
terminal direct raw-sink return. This rejects an early permitted-macro return,
a parameterized macro-mediated raw-sink return, or an unreachable raw-sink
decoy, rather than merely accepting a later raw-sink occurrence.

This preserves the current restrictive C behavior rather than restoring the
obsolete warning-only mapper expectation or a direct raw Server sink.
Independent read-only source-to-sink reviews found no current runtime bypass
on these paths. They also identified successive checker-control false-pass
opportunities now covered by the exact branch predicates, macro restrictions,
include resolution, and negative controls.

## Changed files

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Check | Actual result |
| --- | --- |
| Pre-patch `make check-nginx-common-adoption` | Reproduced exactly the stale mapper-nonfatal and Server-direct-raw-sink assertions on `b779167ff979aa73cdd9321a829f9c693d943760`. |
| Post-patch `make check-nginx-common-adoption` | Passed all 60 NGINX Common-adoption assertions on the current expanded revision. |
| `python -B -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Passed. |
| Two explicit `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q` selections covering `tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests` | Passed: 44 isolated checker cases in bounded 22/22 invocations—one legitimate positive and 43 negative controls. The one-shot invocation exceeds the local command time limit. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Passed: 54 companion NGINX contract tests; 98 selected passing tests in aggregate. |
| Earlier four isolated source-only mutation fixtures | Each exited `1` at exactly its expected changed contract label; the positive hotfix-worktree checker exited `0`. The payload-free receipt SHA-256 is `244fad874b3b6fc4e1044caa03908e5ad005262a1d14a2449651a6d5b5677aab`. |
| Isolated C-comment-decoy fixture | With the pre-hardening checker, a malformed mapper return plus a synthetic fail-closed block inside a C comment exited `0`. The hardened checker exited `1` at `NGINX request mapper validation fails closed before request-header initialization`; a synthetic commented signature before the real function remained rejected. The payload-free receipt SHA-256 is `d4af6ebda9b256030f775d38260e5b0686412939806f062ec7e30c211e75c501` and is retained with the task manifest. |
| Earlier `tests.test_nginx_common_adoption` preprocessor receipt | Passed: four isolated checker runs. The legitimate helper-aware source passed; three `#if 0` twins paired with malformed live mapper, initializer, or response-wrapper code each failed at the corresponding repaired contract label. |
| Historical final translation/control receipt | Passed: 16 isolated checker cases—one legitimate helper-aware positive and 15 negative controls for ordinary, phase-spliced, trigraph, digraph, and outer-guard decoys; mapper binding; nested/unbraced control flow; and line-spliced/UCN raw sinks. Receipt SHA-256: `d83c042215792b836de7c275f678683a281ac2ad8ec507af590f8dae9f40be13`. |
| Historical final macro-control receipt | Passed: 24 isolated checker cases—one legitimate helper-aware positive and 23 negative controls. Receipt SHA-256: `dd64ddf7217297afc0ded5f215a10e93ecc8fce506adec2ea4b1fd60328cc1b6`. |
| Historical final macro-and-include-control receipt | Passed: 29 isolated checker cases—one legitimate helper-aware positive and 28 negative controls. Receipt SHA-256: `0c62ddfce3e2e962cdcb167a78c196269d2b374671c84fd8392e97ea8764e968`. |
| Historical final macro-and-include-control receipt with angle boundary | Passed: 31 isolated checker cases—one legitimate helper-aware positive and 30 negative controls. Receipt SHA-256: `08ef383d8f861aea50af98dfcf30b3b2b582f46f5d7c186867126aa268c22d14`. |
| Historical final macro-and-include-control receipt with directive boundary | Passed: 32 isolated checker cases—one legitimate helper-aware positive and 31 negative controls, including macro redefinition/undefinition, unapproved macro names, token pasting, alternate-extension, traversal, out-of-root, macro-expanded, local-shadow, unknown-angle, and `#include_next` include controls. Receipt SHA-256: `d8d298beb742f7d00ddd3cc4a73e0d3dd8b5cdd1a8965d755987f5d01a4f296f`. |
| Historical final macro-alias and terminal-return control receipt | Passed: 35 isolated checker cases—one legitimate helper-aware positive and 34 negative controls, including `#import`, a permitted Common-header raw-sink alias, and an early permitted-macro return followed by an unreachable raw-sink decoy. Receipt SHA-256: `2c945c7e01d9c69d8ae0ad8daf17559226859dee13dd491f4ae96e2daecb4192`. |
| Current final function-macro control receipt | Passed: 44 isolated checker cases—one legitimate helper-aware positive and 43 negative controls, including macro early-return, control-flow capture, UCN macro-name, parameterized raw-sink-return, and parameterized prevalidation raw-sink controls. Receipt SHA-256: `43cef8d34b51febb4eb5286a4ff3ba5d899bb33e44f4f0bdacc8623efa4767dc`. |
| `make check-bilingual-docs` and `make check-doc-links` | Blocked by the uninitialized `modules/ModSecurity-test-Framework` gitlink: existing repository links to Framework files are absent. Neither command reported a task-owned Change Record link failure. The new pair has 12 required headings in each language and identical backtick-delimited technical literals. |
| `git diff --check` | Passed. |
| Initial security diff scan | Completed for the preceding comment-decoy revision: no reportable finding remained in that snapshot. It is retained as historical evidence only. |
| Final function-macro security diff scan | Completed at `2026-09-05T10:22:18.683709Z`: all six current changed paths were accounted for with complete coverage and zero reportable findings. The sealed report SHA-256 is `7ff57a88702a922644dc0d3ebca96d3bbbf19e3a0ca9031b656cdf7b9e00d9ae`; it is static checker/test/documentation evidence only. |

## Security impact

The request boundary flows from `ngx_http_request_t` through
`ngx_http_modsecurity_validate_common_request_mapper()` into request
initialization and later request-header processing. The source requires mapper
failure to stop before that header path.

The response-header boundary flows from `r->headers_out.server` through
`ngx_http_modsecurity_resolv_header_server()` into
`ngx_http_modsecurity_add_n_response_header()`, then through
`ngx_http_modsecurity_validate_header()` before the raw
`msc_add_n_response_header()` sink. The repair asserts this bounded,
explicit-length route and the rejecting validation branch.

The checker-integrity boundary now applies the documented translation-phase
normalization before masking non-code C text and conditional preprocessor
branches, rejects UCN escapes in the checked code and macro source boundary,
and requires direct structural paths and the exact terminal response return for
these repaired source contracts. It rejects the reproduced comment,
inactive-preprocessor/function-directive, control-flow, raw-sink spelling,
macro replacement-list, macro-mediated early-return, UCN macro-name,
parameterized raw-sink, quoted-local-include, unknown-angle-include, and
nonstandard-include-directive decoys without changing the NGINX runtime path.

No C runtime behavior, body/event payload handling, remote-rule policy,
filesystem behavior, network endpoint, or secret flow changes. The reviewed
source is already fail-closed; this is a static-contract repair, not a claimed
runtime vulnerability remediation.

## Runtime evidence

No native NGINX server, proxy, request, response, sanitizer, or host matrix
was started for this checker-only change. No request or response body was
retained. Static source-to-sink evidence and isolated checker mutation
controls do not substitute for native runtime validation.

## Known limitations

The checker is a deliberately narrow source contract, not a complete C parser
or a proof of arbitrary compiler or runtime reachability semantics. Its lexical
view normalizes only the documented trigraph, line-splicing, and `%:` directive
forms, deliberately rejects UCN escapes and unstructured control flow, and
masks conditional branches except for the verified primary branch of the
Common header's canonical outer include guard. It checks source-level macro
directives, constrains function-like macro forms, rejects `##`, UCNs, and
security-critical/control-flow replacement tokens, and checks quoted local
include syntax/path/resolution/scanned-source membership plus the fixed current
angle-include allowlist. It does not evaluate external compiler `-D` inputs,
expansion inside allowlisted third-party/system headers, unmodeled compiler
include roots, other compiler macro semantics outside that restricted local
surface, or native runtime reachability. A future legitimate refactor can
require a deliberate checker and negative-control update.

## Remaining risks

`FND-PARENT-1010` is not closed by local evidence. Exact successor-head hosted
checks, SonarQube Cloud analysis, reviews, and any resulting-master evidence
remain separate delivery obligations. This task does not claim complete P1–P4
acceptance or a complete native 17×10 host matrix. PR #346 remains an
independent, untouched Draft and must be integrated separately against the new
`master`.

## Checks not run and rationale

No native NGINX runtime replay, full P1–P4 acceptance, full native 17×10 host
matrix, ASan, UBSan, TSan, leak check, or C compilation was run because the
delivery diff contains no NGINX C runtime change. No hosted workflow, SonarQube
Cloud analysis, review, push, or pull request exists yet for this successor
head. The unavailable local `ruff` executable was not installed or replaced.

## Final diff and review status

At this record revision the worktree contains the checker repair, its targeted
checker mutation test, and this paired traceability update only. Independent
read-only reviews confirmed the current C source-to-sink controls, then found
branch-binding, inactive-preprocessor, translation-phase, raw-sink-spelling,
control-flow, macro replacement-list, macro-mediated early-return,
UCN macro-name, function-macro parameter substitution, quoted-local-include,
angle-include, and nonstandard-include-directive checker bypasses in successive
candidate revisions. The current lexical control rejects 43 bounded negative
controls; the 44-case focused suite and the four companion modules (54 tests)
passed in the repository virtual environment, for 98 selected passing tests in
aggregate. The task-owned mutation fixtures were deleted after payload-free
receipts were retained.
`git diff --check` passed; the repository-wide documentation commands are
environment-blocked by the absent Framework checkout, while the new pair's
required headings and technical literals match. The final independent diff
review found no reproducible current checker false pass in the scoped mapper
or response-header path, and the final function-macro security diff scan
completed with complete six-path coverage and zero reportable findings.
Commit, normal push, Draft PR creation, exact-head hosted checks, SonarQube
Cloud, and review evidence remain pending.
