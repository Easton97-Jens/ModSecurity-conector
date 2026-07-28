# Change Record: Parent Apache/NGINX commented-code cleanup for SonarQube Cloud C:S125

**Language:** English | [Deutsch](CR-20260727-sonar-c-commented-code-cleanup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260727-sonar-c-commented-code-cleanup` |
| Date (UTC) | `2026-07-27` |
| Base revision | `1b0f8825f3510b99b603bb6cd6f0777e1710358e` |
| Tracking | Parent SonarQube Cloud `c:S125` Code Smells `AZ4114xeBrFcw9uE-s22`, `AZ4114yYBrFcw9uE-s3E`, `AZ4114y-BrFcw9uE-s3S`, `AZ4114yiBrFcw9uE-s3F`, `AZ43WgS3BO_6kV5uFeJy`, and `AZ43WgS3BO_6kV5uFeJz`. |
| Boundary | Five Parent Apache/NGINX source files, this English/German Change Record pair, and its paired indexes only. Framework and MRTS source, Gitlinks, workflow, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |
| Delivery status | Local candidate only. No commit, push, pull request, hosted CI, SonarQube Cloud PR analysis, review, merge, or default-branch update has occurred. |

## Motivation and problem statement

The six receipt-backed `c:S125` findings identify disabled macro, guard,
assignment, and initialization-list comments in Parent Apache/NGINX source.
They do not establish a runtime defect. Keeping them makes the current
behavior harder to distinguish from old, intentionally inactive behavior at
request-method, response-framing, and configuration-initialization boundaries.

## Acceptance criteria

- Remove or rephrase only the six receipt-backed comments at the audited
  Parent locations.
- Do not activate a GET/POST/HEAD guard, a Content-Length rewrite, or a
  configuration initialization path.
- Preserve HTTP method forwarding, existing response framing, and active
  `NGX_CONF_UNSET*` merge-sentinel initialization.
- Pass the existing Apache/NGINX Common-adoption and C-standard-wiring checks.
- Record normal C17 evidence truthfully as `blocked_environment` when required
  host SDK prerequisites are unavailable, without triggering local provisioning.
- Maintain this complete English/German Change Record pair and its indexes.

## Implementation decision and rationale

The patch deletes the inactive `REQUEST_EARLY` macro, the receipt-backed
method guard comments in the access and log handlers, and the disabled
Content-Length assignment. The header-filter narrative is replaced with a
current statement that this filter preserves the existing Content-Length and
does not rewrite response framing. The two `ngx_pcalloc()` assignment-shaped
lists are replaced with prose that describes the real zero-initialization and
the later active NGINX sentinel assignments.

A separate non-receipt disabled method guard at
`connectors/nginx/src/ngx_http_modsecurity_access.c:403-415` remains
unchanged. The change does not alter a preprocessor condition, executable
statement, request/response flow, configuration value, or ABI.

## Changed files

- `connectors/apache/src/mod_security3.h`
- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260727-sonar-c-commented-code-cleanup.md`
- `reports/audits/change-records/CR-20260727-sonar-c-commented-code-cleanup.de.md`

## Commands executed

| Command or evidence | Result |
| --- | --- |
| `rtk proxy git -C <candidate> submodule update --init --checkout modules/ModSecurity-test-Framework` | passed as a read-only test/documentation dependency checkout at Parent-recorded `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; Framework source remained clean and nested MRTS stayed uninitialized. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-apache-common-adoption check-nginx-common-adoption` | passed. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-apache-c-standard-wiring check-nginx-c-standard-wiring` | passed. |
| `rtk proxy env CI=true PYTHONDONTWRITEBYTECODE=1 APACHE_C_STANDARDS_OUT=<task-owned external root> BUILD_ROOT=<task-owned external root> CC=cc make check-apache-c17` | blocked_environment: the underlying check returned `77` for missing `apxs`/`apxs2`; `make` returned `2`, and no C source compiled. |
| `rtk proxy env CI=true PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<task-owned external root> CC=cc make check-nginx-c17` | blocked_environment: the underlying check returned `77` for missing NGINX headers/source; `make` returned `2`, and no C source compiled. |
| The same two C17 checks with `CC=clang` | blocked_environment for the same missing Apache and NGINX host prerequisites; Clang `21.1.8` was present, but no source compiled. |
| `rtk proxy git diff --check` | passed after the complete tracked source/index diff review; it is rerun once more after this final record text update. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` | passed: `bilingual docs ok`, `repository path references: PASS`, and `doc links ok`. |

## Security impact

Security classification: `not_applicable` as a security finding. The patch
changes no executable control, attacker-controlled input, sink, authorization,
parser, or memory-management behavior. The adjacent protocol invariants were
reviewed nevertheless: no HTTP method guard is re-enabled, no response
Content-Length is rewritten, and active NGINX merge-sentinel initialization is
unchanged. The remaining disabled non-receipt guard is explicitly retained,
not silently changed.

## Runtime evidence

No Apache, NGINX, connector, CRS, MRTS, or network runtime was executed. This
is source-only comment cleanup; the passed adoption and wiring checks are
structural evidence, not runtime evidence.

## Known limitations

Both normal C17 command paths are `blocked_environment` by missing host SDK
prerequisites. `CI=true` was deliberately supplied only to prevent the Apache
script from attempting unauthorized local runtime provisioning; it does not
turn the blocked checks into a pass. An exact delivered-head SonarQube Cloud
analysis remains required before the six external issue keys can be considered
resolved.

## Remaining risks

The residual risk is documentation/history clarity rather than a behavioral
change: a future maintainer could misread the removed historical snippets as
an omitted feature. The concise current prose records the live framing and
initialization behavior, while the Change Record retains the exact receipt
scope and inactive-control rationale.

## Checks not run and rationale

No runtime matrix, connector build, sanitizer, or hosted check was run because
the patch contains no executable behavior change and the C17 host prerequisites
are unavailable. No Framework or MRTS source check was selected: Framework was
used only at the Parent-recorded Gitlink for documentation/test dependencies,
and MRTS remained uninitialized.

## Final diff and review status

The candidate is local and uncommitted. Its reviewed source diff is limited to
the six receipt-backed comment changes in five Parent files; this pair and the
two indexes provide traceability. The documentation validation and final
tracked-diff check passed. No external delivery or SonarQube Cloud issue state
is asserted.
