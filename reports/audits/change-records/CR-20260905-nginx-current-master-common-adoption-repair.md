# Change Record: NGINX current-master Common-adoption contract repair

**Language:** English | [Deutsch](CR-20260905-nginx-current-master-common-adoption-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260905-nginx-current-master-common-adoption-repair |
| Date (UTC) | 2026-09-05 |
| Base revision | b779167ff979aa73cdd9321a829f9c693d943760 |
| Delivery status | Validated implementation and hosted-evidence head: `672d5aa22a94640f50aea191885f991b0d8f45c3`, with parent `8af044dd9d801f4edf163971088fd25795dc578f` and base `b779167ff979aa73cdd9321a829f9c693d943760`. At the validated head, PR #357 was open, Ready for Review, unmerged, auto-merge disabled, mergeable, and `clean`. Its exact-head evidence recorded 36 terminal checks (30 successful and six documented skips), Sonar Quality Gate `OK`, zero `OPEN`/`CONFIRMED` issues, bugs, vulnerabilities, code smells, and `TO_REVIEW` hotspots, plus A new-code ratings and 0.0% new duplication; the API supplied no `new_coverage` value, so no coverage pass is asserted. The documentation-reconciliation successor containing this record has parent `672d5aa22a94640f50aea191885f991b0d8f45c3` and changes only the four delivery-documentation files in this scope. Checker, tests, and product source are byte-identical to the validated parent. No merge, direct `master` push, PR #346 action, or governance change is asserted; Ready for Review is not merge authorization. |

## Motivation and problem statement

After the authorized PR #356 squash merge, 15 resulting-master workflows on
`b779167ff979aa73cdd9321a829f9c693d943760` became terminal: ten succeeded
and five stopped at the same two NGINX Common-adoption checker assertions. The
Apache Common-adoption assertion passed in the failed Apache workflow.

The two assertions were stale checker shapes, not evidence of an NGINX runtime
defect. The live request mapper is fail-closed, while the Server response
header resolver now delegates to a bounded Common wrapper instead of calling
the raw response-header sink directly. `FND-PARENT-1010` is `fixed_in_branch`,
but remains unverified and unclosed until a separately authorized merge and
resulting-master reproduction.

The following exact-head hosted analysis of
`8af044dd9d801f4edf163971088fd25795dc578f` is historical predecessor evidence.
It reported no bugs, vulnerabilities, or security hotspots, but six task-owned
open code smells in the checker: three `python:S6353` character-class
observations, one `python:S8786` regex-resource observation, and two
`python:S1192` duplicate-signature observations. They are checker quality
findings, not established NGINX runtime vulnerabilities. H13 preserves the
ASCII C-identifier grammar without changing the surrounding Unicode-aware word
boundaries, replaces the broad fallback-definition regex with a bounded
non-regex fallback proof, and shares the repeated function-selector literals.
The proof rejects a normalized `ddebug.h` source view longer than 4,096
characters, requires exactly two exact inert fallback definitions, masks only
those definitions, and then rejects remaining active `dd` identifiers except
in separately validated macro directives. It also rejects nonallowlisted
directives and active `_Pragma`, `asm`, `__asm`, or `__asm__` operators. The
later validated successor outcome is recorded in the H15 section below.

The H13 follow-up reproduced macro-alias, empty trailing-macro-suffix,
parenthesized-declarator, function-pointer, GNU `#pragma weak`, and C
`_Pragma` weak-alias false passes in bounded copied checker sources. Each is a
PR-controlled static-checker-integrity class: the pre-fix checker could accept
a non-inert `dd` callable while literal inert decoys remained. No mutated NGINX
runtime was built or executed, so these are not asserted as deployed NGINX
runtime vulnerabilities. `FND-PARENT-1051`, `FND-PARENT-1052`, and
`FND-PARENT-1053` retain their separate evidence and delivery status.

`FND-PARENT-1054` then reproduced a related checker-integrity false pass in
four owned diagnostic format literals. In bounded copied sources, replacing
the header diagnostic `%p`, the `dd(...)` prefix, or either event-handler
diagnostic `%s` literal with `%n` retained the relevant checker `PASS` before
the H14 repair. H14 also binds and regresses the existing `dd(...)` suffix
format, so five exact visible literals now have current mutation coverage. The
active checker view masks C string literals, so its former structural forms
alone could not bind the visible format text. This is a static-contract defect
under PR-controlled source changes, not a demonstrated NGINX runtime or remote
exploit; no mutated native runtime was built or run. The later validated
successor outcome is recorded below.

During the successor's Sonar remediation, `FND-PARENT-1039` reproduced a
separate static-checker control bypass: raw function extraction could stop at
a brace in a comment, literal, or inactive branch before a forbidden lifecycle
or unbounded response-body append. This is not evidence of a current NGINX
runtime vulnerability; the follow-up repairs the shared checker boundary. The
later validated successor outcome is recorded below.

`FND-PARENT-1042` then reproduced a distinct macro-integrity bypass in the
same checker boundary. An allowlisted object-like macro could alias a forbidden
mapper lifecycle, processing, filter-chain, allocation, or Phase-4 pre-gate
response-body route while the assertions continued to inspect only the alias.
`FND-PARENT-1040` also reproduced an ordinary newly named helper call before
the same scope gate. The local repair therefore rejects the complete mapper
marker set and all five reachable pre-gate body routes in permitted macro
replacement lists, and requires the chain-buffer helper itself to retain one
complete direct gate-only form. This is again static-checker evidence, not a
current NGINX runtime vulnerability; the later validated successor evidence is
recorded below.

The H11 control review next reproduced three representation and reachability
gaps in the same static boundary. `FND-PARENT-1043` showed that `c_function`'s
visible view allowed string literals to satisfy executable Phase-4 scope and
cumulative body-limit assertions. `FND-PARENT-1044` showed that an unreachable
response-mapper call could satisfy a textual caller predicate. `FND-PARENT-1045`
showed that legal whitespace in `ctx -> processed` evaded an exact member
literal. The local successor uses `c_checked_function` for executable
contracts, requires direct mapper caller shapes, and normalizes protected
member access in direct and macro-replacement checks.

H12 then reproduced further checker-control paths: state or return changes
before the first approved header guard; side effects in the permitted
`dd(..., ctx)` argument; a state change or return between the required header
mapper call and the processed guard; mutable-memory use against the mapper's
`const` context; direct, static-fallback, or indirect-call side effects in the
locally modeled diagnostic forms; an object-like `dd` redirect to a mutating
header helper; an additional conditional non-inert `static dd` fallback; and
object-like PCRE allocator-shim replacements that form typed null
function-pointer calls. The successor now requires the complete approved
header prefix and the empty mapper-to-validation-to-processed-guard corridor,
the exact immutable mapper-helper form, one `(void)ctx` use in
`map_response_from_ctx`, the exact current diagnostic macro names and
parameter lists, exactly two non-directive inert `dd` function definitions,
and the exact function-like PCRE shim forms. These remain checker-control
findings, not current NGINX runtime vulnerabilities; independent review,
fresh scoped security scanning, and exact successor-head evidence were then
due. The current scoped static scan result is recorded below.

A subsequent blind H12 source-to-sink review reproduced four additional
checker-only bypasses: omitting the response-body loop's bounded-wrapper call,
routing that loop through a new raw body-sink helper, omitting the outer
response-header collection call, and routing collection through a new raw
header-sink helper. Independent follow-up controls also showed that the
collection's generic validated-wrapper call and its synthetic-resolver loop
could each be removed while the old checker still passed. The successor now
requires the exact body-loop call corridor, the sole raw body sink in the
bounded chunk helper, the header filter's exact collection corridor before
metadata processing, the complete current collection traversal/wrapper
surface, and the sole raw header sink in the canonical validated Common
wrapper. These are static-checker trust-boundary findings only: the current
NGINX C sources retain all reviewed paths, and no mutated or production runtime
was executed.

The one permitted fresh post-patch source-to-sink review then reproduced five
additional checker-only false passes in isolated source copies: an intermediate
body-filter caller before the reviewed chain, a memory-buffer route that called
the raw chunk helper, an unconditional Phase-4 scope predicate, a synthetic
`Date` resolver/table route that no longer used the bounded Common wrapper, and
an early return in the shared chained-header iterator. A follow-up direct
source inspection also established that the limited-memory helper could ignore
the Common-planned `allowed` value and pass `len` to the raw chunk helper. The
local checker now requires the complete current direct form of each of those
functions and the current synthetic-resolver table. The evidence is solely
static checker acceptance/rejection; it does not establish a current NGINX
runtime vulnerability or execute a mutated runtime path.

## Acceptance criteria

- The checker requires failed request mapping to return `NGX_HTTP_BAD_REQUEST`
  and requires the initializer's exact fail-closed propagation before hostname
  and request-header processing.
- The checker requires the Server resolver to preserve its explicit length,
  call `ngx_http_modsecurity_add_n_response_header`, and contain no raw
  `msc_add_n_response_header` call.
- The checker requires the Common response-header wrapper to reject validation
  failure with `NGX_ERROR` before the raw sink.
- The public body filter retains only the reviewed prepare/declined/error/direct
  chain route. Its memory buffer route delegates to the limited helper; that
  helper passes the Common-planned `allowed` value, not input `len`, to the raw
  chunk helper. The Phase-4 scope predicate, synthetic resolver table and
  `Date` wrapper, and chained-header iterator retain their reviewed direct
  current forms.
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
- Every remaining `c_function` extract selects its bounds from the same active
  translation-phase-normalized lexical view and returns the corresponding
  visible view for legitimate diagnostic literals. Comments, strings,
  character literals, and noncanonical conditional branches cannot terminate
  an extract or supply a required security marker.
- The repaired mapper, initializer, and Common-wrapper predicates require one
  exact direct failure/sink shape and reject nested, unbraced, or non-linear
  control flow around it. This is a conservative static-contract constraint,
  not a claim of complete C control-flow proof.
- The checker fails closed when a source-level macro directive redefines,
  undefines, supplies a checked token, contains a UCN, token-pasting, or a
  control-flow token in its replacement list. The only control-flow exception
  is an exact current diagnostic macro form with its exact function-like
  parameter list: empty or the three-`fprintf` variadic `dd(...)` body, or a
  reviewed `dd_check_*(r)` ternary or `(void)(r)` body. A PCRE shim is allowed
  only as the exact
  `ngx_http_modsecurity_pcre_malloc_init(x)`/`NULL` or
  `ngx_http_modsecurity_pcre_malloc_done(x)`/`(void)x` function-like form. A
  quoted local include is rejected when dynamic, path-unsafe, or outside the
  scanned NGINX, Common, and profile source set. The explicitly modeled
  external `stdio.h` exception is allowed only when no local candidate can
  shadow it. An angle-bracket include must use the fixed current external-
  header allowlist and satisfy the same local-shadow check; nonstandard
  `#include_next` and `#import` are rejected.
- The `ddebug.h` fallback proof applies to a translation-normalized source
  view of at most 4,096 characters. It requires exactly two exact inert
  nonvariadic `dd` definitions, masks those ranges, and then rejects each
  remaining active `dd` token unless it is on a separately validated macro
  directive. Only the current `define`, `if`, `ifndef`, `else`, `endif`, and
  `include` directive forms are admitted; `_Pragma`, `asm`, `__asm`, and
  `__asm__` are rejected. This is a narrow callable/fallback source contract,
  not a general C-source allowlist.
- The response-mapper all-branch forbidden-marker set and all five reachable
  pre-gate chain-buffer response-body routes are one source of truth for the
  permitted macro-replacement matcher. Every allowlisted object-like
  replacement containing `common_response_validated`, a forbidden `ctx` state
  marker, forbidden processing/filter/allocation marker, or a body route is
  rejected. A terminal protected definition also rejects a chained alias;
  harmless object-like constants remain accepted.
- The chain-buffer helper itself must match the complete direct gate-only form:
  its unique `phase4_in_scope == 0` `NGX_OK` return followed by the one approved
  `ngx_http_modsecurity_append_response_body_buffer` return. An earlier direct,
  helper, macro-helper, indirect, state-changing, or conditional path fails
  closed rather than relying on a partial call graph.
- `ngx_http_modsecurity_process_response_body_chain()` must retain exactly one
  direct call to that reviewed chain-buffer wrapper in its scope-assignment and
  loop corridor, followed immediately by its error propagation. Across the
  scanned NGINX/Common source surface, `msc_append_response_body()` must occur
  only in the bounded chunk helper with its exact current transaction/data/byte
  arguments.
- The header filter must retain its direct
  `ngx_http_modsecurity_add_response_headers(r, ctx)` failure path after the
  processed guard and before response metadata. The collection helper must
  retain its current synthetic-resolver loop, chained-list traversal, sanity
  block, direct validated-wrapper/error path, and return surface; all ten
  reviewed `ngx_http_modsecurity_add_n_response_header(ctx, ...)` call sites
  remain present. Across the scanned NGINX/Common source surface,
  `msc_add_n_response_header()` must occur only in the canonical validated
  Common wrapper.
- The Common response-header wrapper has exactly two lexical `return` tokens:
  its direct validation-failure return and its final direct raw-sink return.
  An earlier macro-mediated return or an unreachable raw-sink decoy cannot
  satisfy the bounded response-header contract.
- Phase-4 scope, response-body planner/counter, and direct caller controls use
  active executable source rather than a visible lexical slice, so strings,
  comments, and masked branches cannot supply a semantic statement.
- The body and header response-mapper callers must match their reviewed direct
  validation assignment/guard/call shape at top-level depth; an unreachable,
  conditional, nested, or unbraced call cannot satisfy the contract. The header
  form has one declaration-only prefix, one direct context acquisition, the
  one reviewed diagnostic call, only the null/intervention guards and returns
  before mapping, and no executable or preprocessor content from mapper through
  `common_response_validated` to the processed guard; the one direct processed
  assignment follows that guard.
- Forbidden response-mapper `ctx` members are recognized with legal whitespace
  around `->`, parenthesized, dereferenced, and indexed forms in active direct
  source and in permitted macro replacements;
  object-like aliases of protected member components are rejected without
  weakening the existing constrained diagnostic and PCRE macro exceptions.
- The response-mapper helper must retain its complete normalized immutable
  mapping-and-warning form. `map_response_from_ctx` must retain exactly its
  one `(void)ctx` use; direct, nested-cast, indexed, member, macro, or other
  indirect invocation syntax cannot extend either boundary.
- The checker uses inline-ASCII `\w` only for the three C-identifier suffix
  fragments while retaining the surrounding default word boundaries. Its
  non-directive `dd` definition count is a bounded linear scan: an oversized
  or unclassifiable declaration fails closed, and exactly two inert static
  fallback definitions remain required.
- No NGINX C runtime source, Framework, MRTS, Gitlink, workflow, ruleset,
  branch protection, required check, Quality Gate, exclusion, suppression,
  source-lock, provenance, PR #346, or `master` change is included.

## Implementation decision and rationale

The implementation logic changes only
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

The remaining `c_function` consumers now use that same active lexical
selection for brace bounds and return the matching visible slice. This keeps
real diagnostics available to the existing source assertions but prevents a
comment, literal, or inactive branch from hiding a later lifecycle token or an
unbounded response-body append. The change covers the shared extraction helper
rather than applying individual per-contract exceptions.

The checker also treats source-level macro and include integrity as
prerequisites for both repaired assertions. It scans the local NGINX source
set, Common C/C++ headers, and the current `connectors/profile_registry.h`
quoted include; rejects `#undef`, unapproved names, critical macro
redefinitions, UCNs in the complete non-comment/non-literal macro source view,
replacement lists containing security-critical or control-flow tokens, and
token pasting. The only permitted control-flow replacement is an exact current
function-like diagnostic body with its current parameter list: the reviewed
`dd(...)` `fprintf` form, the reviewed `dd_check_*(r)` forms, or the empty
nondebug `dd(...)` form. Exactly two total non-directive `dd` function
definitions must match the inert static fallback form. The two PCRE shims must
retain their exact function-like definitions, so an object-like definition
cannot turn their existing calls into a typed indirect call. A quoted local include is accepted only if it
is a regular C/C++ header at a safe path that resolves to that input set.
Dynamic include forms are rejected. Angle-bracket includes require the fixed
external-header allowlist and are rejected if an existing local candidate does
not resolve to that input set. The existing quoted `stdio.h` is a fixed
external exception only without a local candidate at the modeled search roots.
Nonstandard `#include_next` and `#import` directives are rejected.

The macro boundary now also consumes the complete mapper marker tuple and all
five reachable pre-gate chain-buffer body routes: buffer, limited, file, chunk,
and raw append. Thus an otherwise allowed object-like macro cannot hide a
mapper lifecycle/state/processing/filter/allocation marker or a body route from
the source contract. The matcher sees a terminal protected definition in a
local alias chain, but it does not attempt external compiler-definition or
arbitrary third-party-header expansion.

The chain-buffer helper is independently constrained to its complete normalized
direct gate-only form. Its only executable outcomes are the `phase4_in_scope`
`NGX_OK` return and the approved direct bounded-buffer return; any new
pre-gate helper, macro-helper, indirect call, state mutation, or conditional
branch fails the source contract without attempting partial call-graph
resolution.

The caller and sink proof now extends to the reviewed source-to-sink edges.
The body-processing loop must make its one direct bounded-wrapper call in the
exact scope-assignment/loop/error corridor, while the raw body append is
permitted only in the bounded chunk helper. The header filter must make its
one collection call between the processed guard and response metadata. The
collection helper is constrained to its current synthetic and chained
traversals, optional sanity-only block, error returns, and validated-wrapper
surface; the raw response-header sink is permitted only in the canonical
Common wrapper. These intentionally exact lexical contracts reject a future
alternate helper, an unused safe decoy, or a removed collection path rather
than attempting a whole-program C call graph.

Function-like macros are accepted only for the existing empty `dd(...)` form,
the bounded current-name/current-parameter diagnostic form, and the two exact
PCRE allocation shims. Object-like forms of those identifiers are rejected.
This rejects parameter substitution or an object-like redirection that could
otherwise change the existing diagnostic or allocator call targets.

For the Common response-header wrapper, the checker also requires exactly two
lexical `return` tokens: the direct validation-failure return followed by the
terminal direct raw-sink return. This rejects an early permitted-macro return,
a parameterized macro-mediated raw-sink return, or an unreachable raw-sink
decoy, rather than merely accepting a later raw-sink occurrence.

For H11/H12 executable contract checks, `c_checked_function` supplies the
active non-code-masked function view; `c_function` remains limited to the
matching visible slice for diagnostic literals. The response-mapper caller
contracts require their complete direct top-level shape and reject unstructured
control flow around that shape. The header contract additionally fixes the
reviewed declaration/acquisition/diagnostic/guard sequence and requires an
empty mapper-to-validation-to-processed-guard corridor. The mapper helper must
match its complete normalized immutable mapping/warning form, while
`map_response_from_ctx` retains its one `(void)ctx` use. The shared
forbidden-member patterns recognize legal spacing, parenthesized,
dereferenced, and indexed forms; exact diagnostic macro parameter/body forms,
the complete static-fallback-definition count, and exact PCRE shim forms
prevent direct, indirect, or object-like call-target changes from being
smuggled through the allowlisted debug/allocator boundary. This is a
conservative lexical source contract, not a full C parser or
compiler-preprocessor proof.

For H13, the `phase4_`, `response_body_`, and `ngx_http_next_` suffixes use an
inline-ASCII `\w` fragment rather than a broad Unicode character class, while
their original outer word boundaries remain unchanged. The diagnostic fallback
definition check no longer relies on overlapping unbounded regex classes. Its
4,096-character normalized source view must contain exactly two exact inert
fallbacks; after masking them, remaining active `dd` tokens, nonallowlisted
directives, and `_Pragma`/assembly operators fail closed. This closes the
reproduced macro, declarator, pointer, pragma, and operator representations
without claiming to interpret arbitrary external compiler state. Shared
signature constants preserve a single selector for each checked mapper and
header-filter source boundary.

This preserves the current restrictive C behavior rather than restoring the
obsolete warning-only mapper expectation or a direct raw Server sink. The
successive independent read-only source-to-sink reviews identified
checker-control false-pass opportunities and drove the direct, corridor,
immutable-helper, and diagnostic-form controls. No native runtime was
executed; final independent post-patch review and security-scan evidence remain
separate delivery gates.

## H15 Sonar remediation, validated head, and historical local evidence

The `8af044dd9d801f4edf163971088fd25795dc578f` preflight and its six `OPEN`
SonarQube Cloud issues are historical predecessor evidence. Those checker-only
issues were three `python:S6353` character-class observations, one
`python:S8786` regex-resource observation, and two `python:S1192`
duplicate-signature observations. They are not asserted as native NGINX
runtime vulnerabilities.

The validated implementation and hosted-evidence head is
`672d5aa22a94640f50aea191885f991b0d8f45c3`, with parent
`8af044dd9d801f4edf163971088fd25795dc578f`. The H15 remediation uses a scoped
ASCII `(?a:\w*)` fragment for C-identifier suffixes, a bounded 4,096-character
fallback proof, and shared selectors only for semantically identical source
boundaries. It adds no `NOSONAR`, suppression, exclusion, acceptance, rule,
Quality Gate, or workflow change.

At the validated head, PR #357 was open, Ready for Review, unmerged,
auto-merge disabled, mergeable, and `clean`; `master` remained
`b779167ff979aa73cdd9321a829f9c693d943760`. Its exact-head rollup was
terminal: 36 checks total, 30 `SUCCESS`, six documented `SKIPPED`, and none
failed, cancelled, queued, or active. There were no submitted reviews or review
threads. The hosted SonarQube Cloud Quality Gate was `OK`, with zero
`OPEN`/`CONFIRMED` issues, bugs, vulnerabilities, code smells, and `TO_REVIEW`
security hotspots; new reliability, security, and maintainability ratings were
A and new duplication was 0.0%. The API supplied no `new_coverage` value, so
this record does not assert a coverage pass. PR #346 was inspected read-only
only and remains an independent Draft.

On the validated local source/test tree, Python compilation passed; the direct
checker and `make check-nginx-common-adoption` each passed all 74 assertions;
92 isolated mutation and legitimate-control tests passed; and the repository
virtualenv ran all 54 companion tests. The two final-tree static security-diff
reviews bound to the validated patch reported zero reportable findings. The
four-file binary patch SHA-256 for the validated H14/H15 successor is
`9edcc00d0250fa3ec222753a41388d884ec6b6eb42b1e72be2f871466b451843`. A
system-Python companion attempt was environment-blocked solely by its missing
`yaml` module and was not replaced by an installation. The local Vortex/Sonar
query remained HTTP-403 environment-blocked; hosted SonarQube Cloud is the
relevant exact-head evidence.

## Changed files

Validated PR #357 file set at implementation head
`672d5aa22a94640f50aea191885f991b0d8f45c3` (six tracked paths):

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

The documentation-reconciliation successor containing this record has parent
`672d5aa22a94640f50aea191885f991b0d8f45c3` and changes exactly these four
delivery-documentation paths:

- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

It changes no checker, test, or product-source path; those paths are
byte-identical to the validated parent.

## Commands executed

| Check | Actual result |
| --- | --- |
| Pre-patch `make check-nginx-common-adoption` | Reproduced exactly the stale mapper-nonfatal and Server-direct-raw-sink assertions on `b779167ff979aa73cdd9321a829f9c693d943760`. |
| Earlier post-patch `make check-nginx-common-adoption` | Passed all 61 NGINX Common-adoption assertions at that historical revision. |
| FND-PARENT-1039 pre-fix raw-extraction controls | Four isolated temporary-repository controls each failed as expected because the then-current checker returned zero: comment and string braces hid a forbidden response-mapper lifecycle call, while comment and `#if 0` braces hid a direct full-buffer response-body append. Payload-free receipt SHA-256: `966aebb8a3b62777fd9c2c198c285bdd1a6f523d084a39f27f9bf96735757ffa`. |
| FND-PARENT-1039 successor lexical-extraction controls | Passed: all four previously bypassed mutations are rejected after bounds are selected from the active lexical view, and the native checker target still passes all 61 assertions. |
| `python -B -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Passed. |
| Pre-H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_common_adoption` | Passed: 56 isolated checker tests in `96.176s`, including the direct gate-only wrapper and macro-replacement regressions. |
| H11 focused literal/caller/member/macro controls | Passed: the first six focused mutation methods in `60.382s`, then the macro-component alias method in `2.629s`. |
| Observed H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_common_adoption` | Passed: 63 isolated checker tests in `132.067s`, including every H11 literal-only, unreachable-caller, member-spacing, and macro-component regression. |
| Earlier H12 focused caller/member controls | Passed: four focused test methods in `19.294s`, rejecting preprocessor or structured early mapper returns and indexed/dereferenced protected member forms. |
| Earlier H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_common_adoption` | Passed: 65 isolated checker tests in `149.256s`. |
| FND-PARENT-1040/-1042 focused direct-function and macro selection | Passed in `20.523s`: five test methods reject all five direct pre-gate routes, response-body/harmless/object-macro helper calls, an active-conditional direct append, and object aliases of all five routes; a harmless macro control remains accepted. The payload-free pre-fix receipt SHA-256 is `53edc252ab3ab4893501ab93b4b71f4f6f29d08b8bb3c9542c8ad3e2ee403f6b`; its task-owned fixture was removed. |
| Pre-H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Passed: 54 companion NGINX contract tests in `2.139s`; 110 selected passing tests in aggregate. |
| Observed H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Passed: 54 companion NGINX contract tests in `2.972s`; 117 selected passing tests in aggregate with the H11 focused suite. |
| Earlier H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Passed: 54 companion NGINX contract tests in `2.696s`; 119 selected passing tests in aggregate with that earlier focused suite. |
| Current five-case macro-rebinding regression selection | Passed in `4.768s`: checked mapper, request-validator, response-validator, `NGX_HTTP_BAD_REQUEST`, and token-pasted raw-sink mutations are each rejected. |
| Earlier four isolated source-only mutation fixtures | Each exited `1` at exactly its expected changed contract label; the positive hotfix-worktree checker exited `0`. The payload-free receipt SHA-256 is `244fad874b3b6fc4e1044caa03908e5ad005262a1d14a2449651a6d5b5677aab`. |
| Isolated C-comment-decoy fixture | With the pre-hardening checker, a malformed mapper return plus a synthetic fail-closed block inside a C comment exited `0`. The hardened checker exited `1` at `NGINX request mapper validation fails closed before request-header initialization`; a synthetic commented signature before the real function remained rejected. The payload-free receipt SHA-256 is `d4af6ebda9b256030f775d38260e5b0686412939806f062ec7e30c211e75c501` and is retained with the task manifest. |
| Earlier `tests.test_nginx_common_adoption` preprocessor receipt | Passed: four isolated checker runs. The legitimate helper-aware source passed; three `#if 0` twins paired with malformed live mapper, initializer, or response-wrapper code each failed at the corresponding repaired contract label. |
| Historical final translation/control receipt | Passed: 16 isolated checker cases—one legitimate helper-aware positive and 15 negative controls for ordinary, phase-spliced, trigraph, digraph, and outer-guard decoys; mapper binding; nested/unbraced control flow; and line-spliced/UCN raw sinks. Receipt SHA-256: `d83c042215792b836de7c275f678683a281ac2ad8ec507af590f8dae9f40be13`. |
| Historical final macro-control receipt | Passed: 24 isolated checker cases—one legitimate helper-aware positive and 23 negative controls. Receipt SHA-256: `dd64ddf7217297afc0ded5f215a10e93ecc8fce506adec2ea4b1fd60328cc1b6`. |
| Historical final macro-and-include-control receipt | Passed: 29 isolated checker cases—one legitimate helper-aware positive and 28 negative controls. Receipt SHA-256: `0c62ddfce3e2e962cdcb167a78c196269d2b374671c84fd8392e97ea8764e968`. |
| Historical final macro-and-include-control receipt with angle boundary | Passed: 31 isolated checker cases—one legitimate helper-aware positive and 30 negative controls. Receipt SHA-256: `08ef383d8f861aea50af98dfcf30b3b2b582f46f5d7c186867126aa268c22d14`. |
| Historical final macro-and-include-control receipt with directive boundary | Passed: 32 isolated checker cases—one legitimate helper-aware positive and 31 negative controls, including macro redefinition/undefinition, unapproved macro names, token pasting, alternate-extension, traversal, out-of-root, macro-expanded, local-shadow, unknown-angle, and `#include_next` include controls. Receipt SHA-256: `d8d298beb742f7d00ddd3cc4a73e0d3dd8b5cdd1a8965d755987f5d01a4f296f`. |
| Historical final macro-alias and terminal-return control receipt | Passed: 35 isolated checker cases—one legitimate helper-aware positive and 34 negative controls, including `#import`, a permitted Common-header raw-sink alias, and an early permitted-macro return followed by an unreachable raw-sink decoy. Receipt SHA-256: `2c945c7e01d9c69d8ae0ad8daf17559226859dee13dd491f4ae96e2daecb4192`. |
| Initial successor function-macro control receipt | Passed: 44 isolated checker cases—one legitimate helper-aware positive and 43 negative controls, including macro early-return, control-flow capture, UCN macro-name, parameterized raw-sink-return, and parameterized prevalidation raw-sink controls. Receipt SHA-256: `43cef8d34b51febb4eb5286a4ff3ba5d899bb33e44f4f0bdacc8623efa4767dc`. |
| `make check-bilingual-docs` and `make check-doc-links` | Blocked by the uninitialized `modules/ModSecurity-test-Framework` gitlink: existing repository links to Framework files are absent. Neither command reported a task-owned Change Record link failure at that historical checkpoint. The pair had 13 required headings in each language; that historical checkpoint did not establish equality of every backtick-delimited literal. |
| `git diff --check` | Passed. |
| Initial security diff scan | Completed for the preceding comment-decoy revision: no reportable finding remained in that snapshot. It is retained as historical evidence only. |
| Historical final function-macro security diff scan | Completed at `2026-09-05T10:22:18.683709Z`: the preceding six-path snapshot had complete coverage and zero reportable findings. Its sealed report SHA-256 is `7ff57a88702a922644dc0d3ebca96d3bbbf19e3a0ca9031b656cdf7b9e00d9ae`; it did not cover the then-current FND-PARENT-1040/-1042 successor scope and is retained as historical evidence only. The later final-tree scans for the validated head are documented in the H15 section. |
| Earlier H12 `python3 -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Passed. |
| Earlier H12 targeted diagnostic/indirect-call controls | Passed: `test_diagnostic_macro_side_effect_is_rejected` and `test_indirect_calls_are_rejected` completed in `10.500s` after the earlier exact-form repair; direct, non-call, nested-cast, indexed, and member forms were rejected in isolated copies. |
| Earlier H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_nginx_common_adoption` | Passed: 71 isolated checker tests in `178.460s`. |
| Earlier H12 companion `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Passed: 54 companion tests in `2.092s`; 125 selected tests passed in aggregate. |
| Current H12 object-like `dd` pre-fix control | The expected-rejection test failed in `4.558s`: the copied checker returned zero for the object-like diagnostic redirect. |
| Current H12 conditional static-fallback and object-like PCRE pre-fix controls | The two expected-rejection methods failed in `4.916s`: three copied checker runs returned zero. |
| Current H12 isolated C syntax harnesses | `cc -std=c11 -Wall -Wextra -Werror -fsyntax-only` passed for the object-like `dd` redirect and for the conditional static fallback plus typed PCRE object-like forms; neither harness was executed. |
| Current H12 `python3 -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Passed. |
| Current H12 focused diagnostic/fallback/PCRE controls | Passed: four focused methods completed in `10.020s`; all copied mutations were rejected. |
| Current H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_nginx_common_adoption` | Passed: 73 isolated checker tests in `178.357s`. |
| Current H12 companion `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Passed: 54 companion tests in `2.123s`; 127 selected tests passed in aggregate. |
| Current H12 `make check-nginx-common-adoption` | Passed all 62 NGINX Common-adoption assertions. |
| Current H12 caller/raw-sink pre-fix copied-source controls | Independently reproduced: removing the body loop wrapper, removing the header collection call, routing the loop through a raw body helper, and routing collection through a raw header helper each made the then-current copied checker exit `0` with all 62 assertions reported as `PASS`. The copied sources are bounded task-run fixtures; no NGINX runtime was built or executed. |
| Current H12 collection-wrapper/traversal pre-fix controls | Each expected-rejection test failed because the then-current copied checker returned `0`: generic validated-wrapper removal in `2.304s`, and synthetic-resolver-loop removal in `2.205s`. |
| Current H12 caller/sink focused controls | Passed: six focused mutation methods completed in `13.189s`; all body-loop, raw-body, outer-collection, raw-header, generic-wrapper, and synthetic-traversal mutations were rejected. |
| Current H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_nginx_common_adoption` | Passed: 79 isolated checker tests in `249.299s`. |
| Current H12 companion `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Passed: 54 companion tests in `2.090s`; 133 selected tests passed in aggregate with the current focused suite. |
| Current H12 `make check-nginx-common-adoption` after caller/sink repair | Passed all 68 NGINX Common-adoption assertions. |

| Fresh post-patch source-to-sink review | Validated five additional static-checker false passes in isolated source copies: a body-filter intermediate caller, memory-buffer raw chunk route, unconditional Phase-4 scope predicate, synthetic `Date` resolver/table route, and early chained-header iterator return. The reviewer made no runtime claim. |
| Post-review limited-helper pre-fix control | Reproduced: replacing planned `allowed` with `len` in `ngx_http_modsecurity_append_limited_response_body()` made the copied checker exit `0`; the new regression therefore failed as expected before the contract was added. |
| Current focused caller/sink/helper controls | Passed: 11 targeted mutation methods in `26.271s`, including the five review candidates and the bounded-allowance regression. |
| Current full `tests.test_nginx_common_adoption` suite | Passed: 90 isolated checker mutation tests in `307.948s`; the bounded task-owned process exited `0`. |
| Current companion suite | Passed: 54 companion NGINX contract tests in `2.126s`; 144 selected static-contract tests passed in aggregate with the current full suite. |
| Current `make check-nginx-common-adoption` and `py_compile` | Passed: all 74 current NGINX Common-adoption assertions and Python syntax validation for the checker and focused test module. |
| H12 post-patch scoped security diff scan | Completed at `2026-09-05T19:43:13Z`: all four reconciled local changed paths were reviewed with complete static coverage. Ten retained copied-source checker-integrity candidates were rejected by the current exact contracts; zero reportable current product findings survived. Sealed report SHA-256: `7c86a8a875c6636a22ba5c1b2b080eb6a89ca39190d345585e84a160b693e04b`. This is static checker/test/traceability evidence only; the current Vortex/Sonar request remains HTTP-403-blocked and no native runtime or delivery result is claimed. |
| Earlier H13 pre-representation controls | Historical only: five focused methods and the preceding 90-test/54-companion/74-assertion snapshot passed before the later macro, declarator, pointer, pragma, and `_Pragma` false-pass classes were discovered. They are not final-tree evidence. |
| H13 ddebug representation pre-fix controls | Each bounded copied-source class caused checker exit `0` before its corresponding repair: macro alias, empty macro suffix, parenthesized declarator, function-pointer binding, `#pragma weak`, and `_Pragma` weak alias. No mutated NGINX runtime was built or executed. |
| H13 current ddebug regression method | Passed: `test_additional_conditional_diagnostic_fallback_is_rejected` completed in `20.232s`; it rejects multiline, oversized, alias, suffix, declarator, pointer, direct pragma, direct `_Pragma`, and macro-wrapped `_Pragma` controls. |
| H13 current full checker mutation suite | Passed: 90 isolated checker mutation tests in `322.007s`; the bounded task-owned process exited `0`. |
| H13 current companion suite | Passed: 54 companion NGINX contract tests in `1.912s`. |
| H13 current checker target and syntax | Passed: all 74 `make check-nginx-common-adoption` assertions and `python3 -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py`. No native NGINX runtime was built or executed. |
| H13 independent post-fix fallback review | No concrete source-valid `dd` alias or fallback bypass remained in the scoped local source. The review retains external compiler definitions, toolchain predefined macros, and transitive system headers as explicit unmodeled limits. |
| H13 terminal scoped security diff scan | Completed at `2026-09-06T09:41:20Z`: the exact four-path local patch had complete coverage, four candidate rows (three rejected and one not applicable), and zero reportable findings. Sealed report SHA-256: `36f8f21464a56842cd9b60507fc4050fc2c08a9dab2a2fe817ea5866bb3b9346`. This is static checker/test/traceability evidence only; no native-runtime, hosted, or Sonar result is claimed. |
| H14 diagnostic-format pre-fix controls | In four bounded copied-source cases, changing the header diagnostic `%p`, the `dd(...)` prefix, the read-event diagnostic, or the write-event diagnostic to `%n` made the pre-fix checker retain the relevant `PASS`. This confirms a checker-integrity false pass only; no mutated NGINX runtime was built or executed. |
| Earlier H14 targeted diagnostic-format regression | Historical before suffix coverage: `test_diagnostic_format_literal_side_effect_is_rejected` completed one test in `8.371s`, rejecting the four pre-fix `%n` mutations in isolated copied sources. |
| Earlier H14 combined focused regression group | Historical before suffix coverage: the current positive control, pre-guard bypasses, existing macro-side-effect control, and the diagnostic-format regression completed four tests in `32.648s`. |
| H14 current targeted diagnostic and source-path regressions | Passed: `test_diagnostic_format_literal_side_effect_is_rejected` rejects all five current `%n` literal mutations, including the suffix that was not a pre-fix reproduction; paired with `test_critical_macro_source_symlink_is_rejected`, the two tests completed in `11.969s`. The latter confirms that the critical macro-source input rejects a symbolic `ddebug.h` rather than silently treating its target as the scanned source. |
| H14 current full checker mutation suite | Passed: 92 isolated checker mutation tests in `336.194s`; the bounded task-owned process exited `0`. |
| H14 current companion suite | Passed: 54 companion NGINX contract tests in `2.039s`. |
| H14 current checker target, syntax, and diff hygiene | Passed: all 74 `make check-nginx-common-adoption` assertions, `python -m py_compile` for the checker and focused test module, and `git diff --check`. No native NGINX runtime was built or executed. |
| H14 independent post-fix diagnostic review | The four pre-fix `%n` mutations, the fifth `dd(...)` suffix control, escaped-percent spelling, and literal-concatenation variants were rejected. The copied-source symlink regression independently covers the checker input type. A `%n` in an otherwise uncontracted `dd()` call remains outside this five-literal contract and is a residual candidate for separately scoped general format-string analysis, not a demonstrated bypass of the H14 controls. |
| H14 terminal scoped security diff scan | Completed at `2026-09-06T11:25:34Z`: the then-current exact four-path local snapshot had complete coverage, four candidate rows (two rejected and two not applicable), and zero reportable findings. Sealed report SHA-256: `35dfd937600e3f2a6f47b72ff5c919e168bb47aca8d8adf0d827685eec4e8a5d`. This is static checker/test/traceability evidence only; no native-runtime, hosted, or Sonar result is claimed. |

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

The reviewed response-body path flows from each `ngx_chain_t` element in
`ngx_http_modsecurity_process_response_body_chain()` through the Phase-4
scope-gate wrapper, the bounded memory/file/planner chain, and the one raw
`msc_append_response_body()` call in the bounded chunk helper. The reviewed
response-header path flows from the header filter through
`ngx_http_modsecurity_add_response_headers()`, both synthetic and chained
header traversals, the validated Common wrapper, and the one raw
`msc_add_n_response_header()` call. The new contracts bind these current
caller and sink edges so an unused safe helper cannot by itself make a changed
source path appear compliant.

The checker-integrity boundary now applies the documented translation-phase
normalization before masking non-code C text and conditional preprocessor
branches, rejects UCN escapes in the checked code and macro source boundary,
and requires direct structural paths and the exact terminal response return for
these repaired source contracts. It rejects the reproduced comment,
inactive-preprocessor/function-directive, control-flow, raw-sink spelling,
macro replacement-list, macro-mediated early-return, UCN macro-name,
parameterized raw-sink, quoted-local-include, unknown-angle-include, and
nonstandard-include-directive decoys without changing the NGINX runtime path.

The FND-PARENT-1039 repair extends the same boundary to every remaining raw
function extract: active lexical code supplies brace structure, while the
matching visible view retains legitimate diagnostic literals. The four
reproduced comment, string, and inactive-branch decoys therefore cannot hide
either the response-mapper lifecycle action or an unbounded response-body
append from the static contract.

For FND-PARENT-1042, the same boundary treats the complete mapper all-branch
forbidden-marker tuple plus all five reachable chain-buffer body routes as
forbidden macro replacement content. For FND-PARENT-1040, the direct
gate-only-function proof rejects arbitrary helper indirection before the gate.
Together these preserve the source invariant for local object-like aliases,
terminal local alias-chain definitions, and unrecognized local helper names
without relying on a partial call graph.

For H12, the checker-integrity boundary also covers the exact header-prefix
diagnostic, `ddebug.h` fallback, and PCRE-shim call-target forms. A
PR-controlled object-like `dd` definition could otherwise redirect the
existing `dd(..., ctx)` call before the header guards; an extra conditional
fallback or object-like PCRE replacement could likewise alter an existing
call target while leaving old textual matches elsewhere. The repaired static
contract rejects those local forms before it emits a trusted `PASS`. The
isolated syntax harnesses establish C syntax only; no mutated runtime path was
executed.

For H13, the diagnostic-fallback control now binds the `dd` callable rather
than merely counting familiar declaration text. Macro aliases, trailing macro
suffixes, parenthesized declarators, function-pointer bindings, direct or
macro-wrapped `_Pragma` aliases, and GNU pragma aliases cannot leave a hidden
non-inert callable behind two literal decoys. The scan remains deliberately
source-local: it does not claim to model external compiler definitions,
toolchain-predefined macros, transitive system headers, or arbitrary code added
elsewhere in `ddebug.h`. An arbitrary unrelated constructor is not a `dd`
fallback bypass and is not promoted into a general C-source allowlist by this
checker.

For H14, the checker keeps its masked structural views but separately requires
the exact visible current format literal at the header diagnostic and the four
owned `ddebug.h` macro sites: five literals in total. This closes the pre-fix
`%n` false pass before a trusted checker `PASS`. Under the optional variadic
debug macro, the literal is forwarded to `fprintf(stderr, __VA_ARGS__)`; the
source-to-sink observation motivates the static control, but does not establish
debug-enabled native runtime reachability or a remote exploit. Its critical
macro source inputs also reject symlinks, so the checked `ddebug.h` path cannot
silently redirect to an unscanned target in the copied-source contract.

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
security-critical/control-flow and complete mapper/body forbidden-marker
replacement tokens, and checks quoted local
include syntax/path/resolution/scanned-source membership plus the fixed current
angle-include allowlist. It does not evaluate external compiler `-D` inputs,
expansion inside allowlisted third-party/system headers, unmodeled compiler
include roots, other compiler macro semantics outside that restricted local
surface, or native runtime reachability. Its exact local `ddebug.h` and PCRE
forms bound the modeled source surface but do not prove debug-enabled runtime
behavior, compiler configuration, or external-header expansion. The minimal
C harnesses prove only syntax. A future legitimate refactor can require a
deliberate checker and negative-control update.

The H13 `ddebug.h` proof has a 4,096-character normalized-view bound and is
intentionally limited to the fallback callable, approved local directives, and
compiler/linkage operators that can alter that callable. It does not police
arbitrary unrelated C definitions in the header; such an edit is ordinary
source-code integrity risk outside this checker contract and would need a
different repository-wide control.

The H14 visible-literal control deliberately protects only the five current
owned diagnostic sites; it is not a general C format-string analyzer. A `%n`
introduced in a different uncontracted `dd()` call is outside the H14
invariant and needs separate scope and evidence before it is treated as an
actionable product issue. The checker models the repository's C17 source
surface; a hypothetical C23 `#embed` extension is not part of this contract or
evidence and is not classified as a current bypass.

The reviewed body/header caller and raw-sink counts are intentionally exact
for the current scanned local source surface. They do not prove behavior in
unscanned generated code, external compiler definitions, third-party headers,
or a native NGINX execution; a legitimate source-topology change must refresh
the contract and its isolated controls rather than rely on a stale count.

## Remaining risks

`FND-SONAR-0079`, `FND-SONAR-0080`, and `FND-SONAR-0081` are
`fixed_in_branch` at the validated head. `FND-PARENT-1010` is also
`fixed_in_branch`, but remains unverified and unclosed until the separately
authorized merge and resulting-master reproduction. Local `FND-PARENT-1054`
and `FND-PARENT-1055` remain local tracking, not part of this PR diff. No
finding is closed solely by this documentation-reconciliation successor.

The H13 terminal scan is historical for the changed H14 tree. The H14 full
mutation and companion runs, independent post-fix review, and terminal scoped
static scans passed locally; the validated implementation head also has its
own hosted checks, SonarQube Cloud analysis, and review evidence. This task
does not claim native NGINX runtime validation, complete P1–P4 acceptance, or
a complete native 17×10 host matrix. PR #346 remains an independent, untouched
Draft and must be integrated separately against a later `master` state.

## Checks not run and rationale

No native NGINX runtime replay, full P1–P4 acceptance, full native 17×10 host
matrix, ASan, UBSan, TSan, leak check, or native NGINX C compilation was run
because the delivery diff contains no NGINX C runtime change. Two isolated
minimal C syntax harnesses were compiled with `-fsyntax-only`; they do not
exercise NGINX or a mutated runtime call. Hosted workflow and SonarQube Cloud
evidence exists for the validated implementation head
`672d5aa22a94640f50aea191885f991b0d8f45c3`; this documentation-only successor
does not transfer that evidence to its own, intentionally unrecorded commit
SHA. The H12 and H13 post-patch scans are historical evidence only. The H14
full mutation and companion suites, independent post-fix review, terminal
scoped security-diff scans, direct paired-document suite, and diff hygiene have
completed locally. The repository-wide bilingual and path-reference make
targets are environment-blocked solely by absent Framework Gitlink targets;
they are not reported as passes. The unavailable local `ruff` executable was
not installed or replaced.

## Final diff and review status

The validated implementation and hosted-evidence head for PR #357 is
`672d5aa22a94640f50aea191885f991b0d8f45c3`, with parent
`8af044dd9d801f4edf163971088fd25795dc578f`. Its H14/H15 checker and test
patch has the documented local, independent-review, and hosted evidence above.
The documentation-reconciliation successor containing this record has that
validated head as its parent and changes only the paired Change Record and
README index paths. It changes no NGINX runtime C, checker, focused test,
`.github/**`, PR #346, or `master` path; those non-documentation paths are
byte-identical to the validated parent.

H13's six `ddebug.h` representation repairs and terminal scan remain historical
evidence. H14 retains the exact five visible diagnostic-literal contract and
the targeted literal and source-symlink regressions, full current suites,
independent post-fix review, direct bilingual document suite, diff hygiene, and
terminal scans. Repository-wide documentation commands are environment-blocked
solely by absent Framework targets and are not represented as passes. This
documentation reconciliation is not a merge, and Ready for Review is not merge
authorization. The new documentation-only successor requires its own exact-head
checks, SonarQube Cloud analysis, and review readback after a normal push; the
validated parent evidence is retained only as parent evidence.
