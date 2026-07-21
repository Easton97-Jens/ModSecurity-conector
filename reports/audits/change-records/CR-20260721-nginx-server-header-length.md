# Change Record: NGINX Server header byte-length correction

**Language:** English | [Deutsch](CR-20260721-nginx-server-header-length.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260721-nginx-server-header-length` |
| Date (UTC) | `2026-07-21` |
| Base revision | `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` |
| Scope | Parent repository only; Framework and MRTS source and gitlinks are unchanged. |
| Related finding | `FND-PARENT-0044` is retained as a pending canonical EN/DE/JSON import because the local `.codex` mount is read-only. |

## Motivation and problem statement

`ngx_http_modsecurity_resolv_header_server()` supplies the NGINX default
`Server` value to libModSecurity when `r->headers_out.server == NULL`. Its two
connector-owned C arrays were passed through the explicit-length
`msc_add_n_response_header()` API with bare `sizeof(...)`, which includes each
literal's terminal NUL. An exact or end-anchored Phase-3
`RESPONSE_HEADERS:Server` policy can therefore evaluate a byte that is not part
of the semantic HTTP header value and fail to intervene.

The related candidate was statically validated as reportable `low` / `P3`.
The fault is distinct from response-body inspection limits: it is a narrow
response-header byte-length canonicalization boundary.

## Acceptance criteria

- The `server_tokens` and non-tokenized default Server literal branches pass
  `sizeof(...)-1U` as `value.len`; no bare default `sizeof(...)` assignment
  remains.
- The custom `r->headers_out.server` path retains `h->value.len` without a
  subtraction, `strlen`, or `ngx_strlen` conversion.
- The resolver retains the explicit
  `msc_add_n_response_header(..., value.data, value.len)` sink.
- The focused source contract fails before the source correction for the two
  default lengths and passes after it, including custom-header and sink
  controls.
- No Framework, MRTS, or gitlink change occurs, and no compiler, test,
  scanner, or Quality Gate control is weakened.

## Implementation decision and rationale

Only the two literal-storage lengths subtract their terminal byte:

```c
value.len = sizeof(ngx_http_server_full_string) - 1U;
value.len = sizeof(ngx_http_server_string) - 1U;
```

The existing custom branch remains `value.len = h->value.len;`. NGINX already
owns that explicit `ngx_str_t` length; subtracting or applying C-string
semantics there would corrupt valid custom values. The header resolver's
selection, visible values, and explicit-length API sink are unchanged.

The existing lint-wired NGINX Common-adoption check now locks this boundary:
it requires both corrected literal branches, rejects their former bare
assignments, requires the custom length control, and verifies the sink.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `reports/audits/change-records/CR-20260721-nginx-server-header-length.md`
- `reports/audits/change-records/CR-20260721-nginx-server-header-length.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Local, ignored evidence also retains the complete pending canonical
`FND-PARENT-0044` EN/DE/JSON record and required finding-system update plan;
it is not a substitute for versioned source, tests, or this Change Record.

## Commands executed

Before source correction, the added contract exited `1` with exactly the two
default-length assertions failing; its custom-header and explicit-sink
controls passed. After the correction, the following results were observed:

```text
rtk run env PYTHONDONTWRITEBYTECODE=1 python3 ci/checks/connectors/nginx/check-nginx-common-adoption.py
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-nginx-common-adoption
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-nginx-c-standard-wiring
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-nginx-c17-lint
rtk env PYTHONDONTWRITEBYTECODE=1 FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework CONNECTOR_COMPONENT_CACHE=/var/tmp/codex/ModSecurity-conector/cache/shared BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/c17-check-gcc NGINX_SOURCE_DIR=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/nginx-c17/nginx-1.31.2 CC=gcc make check-nginx-c17
rtk env PYTHONDONTWRITEBYTECODE=1 FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework CONNECTOR_COMPONENT_CACHE=/var/tmp/codex/ModSecurity-conector/cache/shared BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/c17-check-clang NGINX_SOURCE_DIR=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/nginx-c17/nginx-1.31.2 CC=clang make check-nginx-c17
rtk run env PYTHONDONTWRITEBYTECODE=1 make lint
rtk git -C /var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/worktree diff --check
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-doc-links
rtk run env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs
```

The direct focused check passed all existing assertions plus the four new
default/custom/sink assertions. `make check-nginx-common-adoption` and
`make check-nginx-c-standard-wiring` passed. `git diff --check` passed.
`make check-nginx-c17-lint` initially returned `0` while reporting an
environment block and skip; that pre-provisioning wrapper result is documented
below and is not counted as a native C compilation pass. After a task-owned,
signed and SHA-256-pin-verified NGINX 1.31.2 source setup and normal NGINX
configuration, the actual `make check-nginx-c17` target passed with both GCC
15.2 and Clang 21.1, compiling the complete NGINX/Common source list with
`-std=c17 -Wall -Wextra -Werror`. The complete Parent `make lint` attempt
exited `2` before its NGINX lint stages at `make check-apache-c17-lint`.
Apache/APXS provisioning invoked the all-component runtime preparer, which
failed closed on a distinct NGINX archive SHA-256 mismatch and missing runtime
prerequisites. This is not a passing full-lint result or evidence against the
focused NGINX controls; its separate provisioning blocker is documented below.

`make check-bilingual-docs` and `make check-doc-links` passed in the delivery
clone using a task-owned detached copy of the exact master-pinned Framework
gitlink; its nested MRTS submodule remained uninitialized. The Change Record
pair was also manually checked for matching required headings, identity fields,
language switches, tables, and technical literals.

## Security impact

The correction restores the intended semantic length at the NGINX-to-
libModSecurity response-header boundary. It lets an exact or anchored
`RESPONSE_HEADERS:Server` policy compare the default value without a hidden
terminator. It does not broaden parsing, change policy selection, alter the
client-visible default Server text, or weaken the correctly length-delimited
custom-header path.

The static source-to-sink and attack-path evidence identifies a remote ordinary
request as the entry point when an operator uses the default Server path and a
relevant response-header policy. No secret, authorization, sensitive-content,
or demonstrated client-visible integrity impact was found; the validated
severity remains `low` / `P3`.

## Runtime evidence

There is no native NGINX/libModSecurity runtime confirmation for the
`r->headers_out.server == NULL` default branch. In particular, no captured
default-header run has yet proven an exact or end-anchored Phase-3 policy
intervention for both `server_tokens` values. The C17 checks compile the
connector and Common sources against a task-owned normal NGINX 1.31.2
configuration, but do not run a NGINX host or libModSecurity transaction. A
proxied custom response header would exercise `h->value.len`, not the faulty
default-literal branch, and was not substituted as equivalent evidence.

The retained final validation receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/evidence/nginx-server-header-nul-validation-20260721T005556Z-final.json`
with SHA-256
`01a2cb1a836c08b34537e2bc2aa13949600679d29b255f1600b7e4f8c6bec6da`.

## Known limitations

A task-owned, signed and checksum-pinned NGINX 1.31.2 source tree with normal
generated headers is available for C17 compilation. The host still lacks a
compatible runnable NGINX/libModSecurity integration environment. The original
static regression and real C17 compiles prove the source invariant and the
legitimate custom/header-sink controls, but not a deployed rule decision or
client-visible response behavior.

New-directory allocation beneath `.codex/findings` is denied in this session:
`mkdir -p .codex/findings/FND-PARENT-0044` returned `Read-only file system`.
The canonical FND-0044 directory, indexes, backlog, roadmap, and reconciliation
report therefore cannot be synchronized as a new canonical record. Its complete
pending EN/DE/JSON import package is hash-retained under the task run.

The distinct gzip-disabled C17 warning is triaged separately as
`FND-PARENT-0045` (`compiler_warning`, P2, non-security). It does not alter the
Server-header correction or its normal GCC/Clang controls and is deliberately
not combined into this change.

## Remaining risks

Under the mandatory security workflow, the related finding remains `blocked`,
not `fixed`, `verified`, or `closed`, until relevant native behavioral proof is
available. An integration-specific NGINX/libModSecurity behavior could remain
undiscovered until default-header exact/end-anchored, custom-header, and
non-match controls run in a native environment. No risk has been accepted.

The source correction is local at record authoring. Commit, push, Draft PR,
exact-head hosted checks, review, SonarQube Cloud, merge, and resulting-master
scan facts do not yet exist and are not claimed here.

## Checks not run and rationale

`make check-nginx-c17-lint` initially printed `BLOCKED: missing NGINX
headers/source for NGINX connector C checks` and `SKIPPED: nginx C17 compile
check blocked in lint environment`. Its wrapper exit `0` does not establish
a C compilation pass. This was superseded for C17 evidence by the actual
`make check-nginx-c17` runs against the task-owned normal NGINX 1.31.2 source,
which passed with GCC and Clang.

The complete `make lint` attempt exited `2` before the NGINX lint stages at
`make check-apache-c17-lint`. With no local APXS, the Framework helper requested
all-component runtime provisioning. Its NGINX path downloaded a GitHub tag
archive while applying the checksum pinned for the distinct nginx.org release
archive, so the integrity check correctly failed closed; Apache/APXS and the
NGINX runtime module remained unavailable. The Framework boundary and Parent
gitlink are outside this remediation's write scope, so no Framework workaround
or checksum weakening was made.

Native NGINX/libModSecurity rule verification, sanitizer coverage, hosted PR
checks, SonarQube Cloud analysis, review, and resulting-master revalidation
are not run because there is not yet a committed or pushed PR head. The
repository bilingual/documentation checks ran after this record pair was
created and passed in the task-owned delivery clone with the exact Framework
gitlink. That isolated Framework copy did not initialize or modify MRTS.

## Final diff and review status

An independent focused review of the two source/test files passed with no
blocking security or compatibility issue. It confirmed both literal corrections,
the unchanged custom `h->value.len` path, and the preserved explicit sink.

At record authoring the task worktree contains only the two source/test edits
and this EN/DE Change Record plus README index pair. It is based on
`0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`; no commit, push, PR, review,
hosted check, Sonar result, merge, or master scan is claimed. The final local
diff and the real GCC/Clang C17 checks passed. Full bilingual/documentation
checks passed in the delivery clone; broad `make lint` remains a documented
non-passing check because of the separate, fail-closed Framework provisioning
blocker.
