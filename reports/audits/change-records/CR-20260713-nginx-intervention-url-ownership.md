# Change Record: NGINX intervention URL ownership and native cleanup

**Language:** English | [Deutsch](CR-20260713-nginx-intervention-url-ownership.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | NGINX intervention URL ownership and native cleanup |
| Change ID | CR-20260713-nginx-intervention-url-ownership |
| Date (UTC) | 2026-07-14T07:56:59Z |
| Author or executing agent | Codex agent <code>/root</code> |
| Base revision | 0fec00442b0031c206b627a44735f1eb07534d51 |
| Related issue or pull request | None; confirmed finding supplied in the task attachment |
| Severity | Not stated in the supplied finding material (confirmed) |
| Final revision | Not committed |

## Motivation and problem statement

Fix only the confirmed finding: “NGINX retains a borrowed intervention URL and
does not clean native intervention completely.” The supplied finding identifies
<code>connectors/nginx/src/ngx_http_modsecurity_module.c</code>. The affected
function was unchanged from scan revision
<code>056f93232c6f5dba132bfb2204d96ce49707507b</code> before this fix.

The former redirect path stored native <code>intervention.url</code> directly
in NGINX's <code>Location</code> header while the native intervention was not
comprehensively cleaned. Cleanup after that assignment would leave a dangling
header pointer; omitting cleanup retained native resources. No versioned report
or severity was supplied, so this record preserves that fact.

## Affected components and security boundaries

The change is limited to the NGINX intervention bridge, a focused production
source-contract test, and this English/German Change-Record pair. The security
boundary is native libmodsecurity intervention storage versus NGINX
request-pool storage: native <code>url</code> and <code>log</code> are
temporary and must be released by <code>msc_intervention_cleanup</code>, while
the emitted header must point to memory owned by <code>r-&gt;pool</code>.

No Framework source or submodule pointer, other connector, workflow,
configuration default, or runtime fixture changed. Temporary header sources
and compile objects were confined below
<code>/var/tmp/codex/ModSecurity-conector</code> and are not versioned.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| A redirect header never retains a borrowed native URL pointer | Met | URL is length-checked, copied, and NUL-terminated in <code>r-&gt;pool</code> before header assignment; focused contract test passes. |
| Native intervention cleanup runs exactly once on every function exit | Met | Full zero initialization, one cleanup label, one cleanup call, and one return; focused contract test and independent review pass. |
| Overflow and allocation failures are deterministic | Met | Overflow, request-pool allocation, and header-list allocation return <code>NGX_HTTP_INTERNAL_SERVER_ERROR</code> and reach cleanup. |
| Valid redirects and non-redirect statuses preserve behavior | Met | Nonempty URLs keep the intervention status; non-redirect status processing is retained; C17 compilation and source contract pass. |
| Empty or absent URLs create no empty or borrowed Location header | Met | Redirect handling requires a nonempty URL; normal status handling and cleanup remain active. |
| Required static verification is real and scoped | Met | Focused test, actual NGINX/Common C17 compilation with <code>-Werror</code>, NGINX checks, CI-mode lint, and quick-check pass. |

## Alternatives investigated

- Retain the borrowed URL and defer cleanup. Rejected because the header lives
  for the NGINX request, not for the native intervention record.
- Copy only the URL and retain the direct
  <code>free(intervention.log)</code>. Rejected because it leaves ownership
  split and conflicts with complete native cleanup.
- Add a header without allocation checks. Rejected because intervention
  failures must be deterministic and still release native resources.
- Run a NGINX runtime/lifecycle test. Not selected: no eligible host
  environment was already present, and the task authorizes this only when one
  is present.

## Implementation decision and rationale

The intervention structure is fully zeroed and its status set to
<code>200</code>. Every exit funnels through a single <code>cleanup</code>
label, which calls <code>msc_intervention_cleanup(&amp;intervention)</code>
exactly once and returns the selected result. The missing-context path also
uses this cleanup; its record is known zero-initialized and no native query has
yet occurred.

For a nonempty redirect URL, the code obtains its length, rejects an overflow
of the terminating-byte allocation, allocates <code>length + 1</code> bytes
from <code>r-&gt;pool</code>, copies and NUL-terminates the URL, then creates
and publishes the NGINX <code>Location</code> header. It clears an old
Location only after header-list allocation succeeds. Native cleanup occurs
only after the request-pool copy becomes the header value.

<code>url == ""</code> is treated as no redirect: no empty Location header is
created, and the normal intervention-status path is used. This does not alter a
valid redirect, which requires a nonempty target.

## Changed files

- <code>connectors/nginx/src/ngx_http_modsecurity_module.c</code>
- <code>tests/test_nginx_intervention_url_ownership.py</code>
- <code>reports/audits/change-records/CR-20260713-nginx-intervention-url-ownership.md</code>
- <code>reports/audits/change-records/CR-20260713-nginx-intervention-url-ownership.de.md</code>

No Framework submodule file or pointer changed. Temporary sources, configured
NGINX headers, compile objects, and logs are local and unversioned only.

## Tests added or changed

Added <code>tests/test_nginx_intervention_url_ownership.py</code>. It parses
the production <code>ngx_http_modsecurity_process_intervention</code> function
and verifies full zero initialization, exactly one cleanup and return, removal
of the direct log free, a request-pool URL copy before cleanup, NUL
termination, no borrowed URL assignment, overflow protection, and cleanup
routing for missing context/configuration, sent headers, and both allocation
failures. It is a production-source contract test, not a substitute NGINX
implementation.

## Commands executed

<code>$TASK_ROOT</code> denotes
<code>/var/tmp/codex/ModSecurity-conector/tmp/task.nginx-intervention.ZzgRxQ</code>.
No command produced a canonical runtime-evidence artifact.

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>rtk proxy git diff 056f93232c6f5dba132bfb2204d96ce49707507b..HEAD -- connectors/nginx/src/ngx_http_modsecurity_module.c</code> | 0 | Target source was unchanged from the supplied scan revision before the fix. | None | None |
| <code>rtk proxy env ... PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_nginx_intervention_url_ownership</code> | 1, before fix | Seven expected assertions failed against the former borrowed-pointer/incomplete-cleanup implementation. | None | None |
| <code>rtk proxy env VERIFIED_RUN_ROOT=$TASK_ROOT RUNNER_TEMP=$TASK_ROOT SOURCE_ROOT=$TASK_ROOT/sources MODSECURITY_V3_SOURCE_DIR=$TASK_ROOT/sources/ModSecurity_V3 sh modules/ModSecurity-test-Framework/ci/provisioning/fetch-smoke-sources.sh v3</code> | 0 | Fetched temporary libmodsecurity headers for compilation only; no runtime was built or run. | None | None |
| <code>rtk proxy env TMPDIR=$TASK_ROOT/tmp ./auto/configure --with-compat</code> in temporary NGINX <code>release-1.31.2</code> source | 0 | Generated NGINX configuration headers only; no NGINX binary was built or started. | None | None |
| <code>rtk proxy env ... make check-nginx-c17</code> | 2 (underlying check 77), before header preparation | Correctly blocked because NGINX headers/source were absent. | None | None |
| <code>rtk proxy env ... MODSECURITY_INCLUDE_DIR=$TASK_ROOT/sources/ModSecurity_V3/headers NGINX_SOURCE_DIR=$TASK_ROOT/sources/nginx-1.31.2 make check-nginx-c17</code> | 0 | All listed NGINX/Common units compiled under C17 with <code>-Wall -Wextra -Werror</code>. | <code>$TASK_ROOT/build/nginx-c-standards/</code> | None |
| <code>rtk proxy env ... PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_nginx_intervention_url_ownership</code> | 0 | Three focused ownership, cleanup, and failure-path contract tests passed. | None | None |
| <code>rtk proxy env ... make check-nginx-common-adoption</code> | 0 | NGINX Common-adoption structure checks passed. | None | None |
| <code>rtk proxy env ... make check-nginx-c-standard-wiring</code> | 0 | NGINX C-standard target/source wiring checks passed. | None | None |
| <code>rtk proxy env ... MODSECURITY_INCLUDE_DIR=$TASK_ROOT/sources/ModSecurity_V3/headers NGINX_SOURCE_DIR=$TASK_ROOT/sources/nginx-1.31.2 make check-nginx-c17-lint</code> | 0 | Lint-integrated NGINX C17 compilation passed with prepared headers. | <code>$TASK_ROOT/build/nginx-c-standards/</code> | None |
| <code>rtk proxy env ... make lint</code> | 130 | Stopped when an unrelated Apache check began local runtime provisioning; its task-local cache was removed. | None | None |
| <code>rtk proxy env CI=true ... make lint</code> | 0 | Full static lint passed; unavailable Apache/HAProxy host C17 checks were skipped rather than provisioned. | None | None |
| <code>rtk proxy env CI=true ... make quick-check</code> | 0 | Quick-check passed, including lint, framework Python compilation, and whitespace checks. | None | None |
| <code>rtk proxy env ... make check-bilingual-docs</code> in the main worktree | 2 | Blocked by unrelated untracked <code>docs/decisions/</code> files with missing local link targets; no task file was changed to address them. | None | None |
| <code>rtk proxy env ... make check-bilingual-docs &amp;&amp; make check-doc-links</code> in a clean temporary Git worktree containing the versioned base and this record pair | 0 | Bilingual-pair and document-link checks passed for the versioned base plus this change. | None | None |
| <code>rtk proxy git diff --check &amp;&amp; git diff --check -- connectors/nginx/src/ngx_http_modsecurity_module.c &amp;&amp; git diff --submodule=log -- modules/ModSecurity-test-Framework</code> | 0 | Full tracked and scoped whitespace checks passed; no Framework submodule diff was present. | None | None |

## Security impact

The redirect header now crosses the ownership boundary by copying the native URL
into NGINX request-pool memory before native cleanup. The intervention is
released in one place, removing retained native URL/log allocations and
avoiding a cleanup-induced dangling Location pointer. There is no separate
direct free of <code>intervention.log</code>. Overflow and allocation failures
return an internal-server status after cleanup rather than exposing a partially
initialized redirect.

## Documentation changes

Added this English/German Change-Record pair. No connector guide changed:
there is no user-facing configuration, directive, or supported runtime behavior
change beyond this implementation-level security fix.

## Runtime evidence

No runtime evidence was collected or claimed for this change. Temporary NGINX
source was configured only to provide headers for the C17 compile check; no
NGINX server, request lifecycle, allocator-failure injection, or redirect
response was executed.

## Known limitations

- The focused test is a static contract over the production C function. It
  cannot prove NGINX's live request-pool lifetime or force a real
  <code>ngx_pnalloc</code> failure.
- Temporary headers enable compilation but do not constitute a linked module,
  host lifecycle, or runtime compatibility result.
- The supplied finding material had no versioned report or severity.

## Remaining risks

- A future libmodsecurity ownership-contract change requires revalidation of
  this bridge. The implementation confines native pointers to the interval
  before the single cleanup call.
- A live NGINX integration test could expose host-specific behavior absent from
  the source contract. This is mitigated by compiling the actual NGINX module
  against configured NGINX headers and by making no runtime claim.

## Checks not run and rationale

- NGINX runtime/lifecycle and real allocator-failure tests were not run because
  no eligible host environment was already present, and the task authorizes
  them only in that case. No server was installed, built, or started.
- Optional C23/future-C NGINX checks, sanitizers, and unrelated security scans
  were not run because the confirmed finding is scoped to the required C17
  path and the user requested no scope expansion.
- No Framework fixture/source changed: its existing redirect fixture does not
  observe Location and cannot prove this property without forbidden Framework
  changes.

## Final diff and review status

The focused test, real C17 compilation, NGINX adoption/wiring checks, CI-mode
lint, and quick-check pass. The direct main-worktree documentation check is
blocked by unrelated untracked documentation; the same bilingual and link
checks pass in a clean temporary Git worktree with the versioned base plus this
record pair. The final full tracked and scoped whitespace checks pass; the
Framework submodule diff and its worktree status are empty. An independent
read-only review found no blocking ownership, cleanup, C-compatibility, or
behavior-regression issue and confirmed the empty-URL behavior as a safe
deterministic refinement. The final status also contains unrelated user changes
in <code>Makefile</code>, <code>ci/checks/analysis/</code>, and
<code>docs/</code>; they were neither inspected for modification nor changed.
The intended outcome is <code>fixed</code>. No commit or pull request has been
created.
