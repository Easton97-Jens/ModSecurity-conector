# Change Record: Apache RulesSet configuration-pool cleanup

**Language:** English | [Deutsch](CR-20260729-apache-ruleset-pool-cleanup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-apache-ruleset-pool-cleanup` |
| Date (UTC) | `2026-07-29` |
| Assessment baseline | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Boundary | Parent Apache connector source, its focused checks and harnesses, source provenance, and this English/German Change Record/index pair. Framework and MRTS are read-only build context only; neither repository, Gitlink, dependency, CI policy, nor runtime matrix is changed. |
| Finding linkage | `FND-PARENT-0064` (RulesSet lifecycle), `FND-PARENT-0008` (C17 sentinel), `FND-PARENT-0068` (new runner output confinement), `FND-PARENT-0069` (separate inherited aggregate C17 diagnostic), `FND-PARENT-0070` (APXS header materialization), and `FND-PARENT-0071` (isolated MIME artifact layout). |
| Upstream reference | Selective adaptation of `owasp-modsecurity/ModSecurity-apache` PR #94 commit `5ea3fc9da876195706375cf35f321de2a1f35ce1`; no other upstream PR #91–#94 change is included. |

## Decision and scope

Apache creates one `RulesSet` for every per-directory configuration object.
Before this change, a successful `msc_create_rules_set()` result was not
registered with its owning APR configuration pool. The selected upstream #94A
change adds the corresponding APR cleanup callback immediately after a
non-null allocation. APR therefore owns exactly one cleanup for that object;
request, merge, and global module teardown do not gain a competing manual
cleanup path.

Current-Parent comparison excluded the remaining upstream material:

- #91 is an incompatible handler/body architecture, while Parent already has
  its own stronger EOS/drain boundary.
- #92 is Docker/Compose build-stack work and is not applicable here.
- #93 is a possible future local evidence method, not a demonstrated product
  delta.
- #94's intervention-string portion is already covered by Parent's distinct
  request-owned intervention cleanup.

Exact-candidate validation also exposed two independent, inherited Parent
build/harness defects that otherwise stop the normal Apache control before the
selected lifecycle change can be exercised. Their narrow repairs are included
in this Parent delivery:

- The APXS wrapper now copies the fixed private
  `header_validation_internal.h` alongside existing Common C sources. A fresh
  materialized build otherwise compiles `request_helpers.c` without its quoted
  sibling header.
- The isolated Apache smoke harness now creates the same generated MIME file
  at both `$ServerRoot/mime.types` and `$ServerRoot/conf/mime.types`. This
  matches supported Apache default resolution without changing configuration
  text, rules, or request behavior.

The directive-table terminator becomes the behavior-equivalent `{ .name =
NULL }` sentinel. This is required for the changed translation unit to pass
normal strict C17 compilation with both available compilers; it does not alter
Apache directive dispatch.

## Acceptance criteria

- A successful Apache `msc_create_rules_set()` allocation registers exactly
  one cleanup with its owning APR configuration pool; a null allocation
  registers none.
- Pool clear/destruction calls `msc_rules_cleanup()` once for each owned
  non-null RulesSet, including independently created merge configurations and
  their failure paths.
- No manual RulesSet cleanup is added to request, merge, or global module
  teardown paths.
- The changed translation unit passes the real APR harness under GCC and
  Clang C17 with `-Wall -Wextra -Werror` without a warning suppression or a
  production compiler-flag change.
- A fresh materialized APXS build contains the private header needed by staged
  Common sources and produces the Apache DSO.
- A normal isolated Apache HTTP/1.1 control loads that exact DSO, returns the
  expected `403` for `phase2_args_block`, and survives a `SIGUSR1` graceful
  restart with readiness before and after the signal.
- The focused runner retains its private-output and unsafe-parent protections;
  no workflow, runtime matrix, scanner, quality gate, or branch-protection
  control is weakened.

## Implementation

`msc_config.c` defines `msc_rules_set_cleanup()` and registers it with
`apr_pool_cleanup_register()` only after `msc_create_rules_set()` succeeds.
The APR harness uses real APR pools and deterministic RulesSet stubs to cover
normal construction, null construction, pool clearing, successful merge, and
every merge failure path. The source-contract test protects callback placement
and forbids a future competing manual cleanup.

The native harness runner uses a validated temporary-parent chain, `umask
077`, and a new private `mktemp -d` leaf. It verifies ownership and mode before
compilation, ignores legacy caller-selected output paths, and removes only the
exact generated binary and leaf directory non-recursively.

The APXS wrapper correction is a literal-header staging change with a focused
Apache/Common structural assertion. The MIME correction copies or creates the
same artifact at both conventional locations; it introduces no request-derived
path, shell evaluation, dynamic configuration directive, or new executable
input.

## Changed files

- `connectors/apache/src/msc_config.c`
- `connectors/apache/SOURCE_MAP.json`
- `connectors/apache/build/apxs-wrapper.in`
- `connectors/apache/harness/run_apache_smoke.sh`
- `ci/checks/connectors/apache/apache_rules_set_cleanup.c`
- `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `tests/test_apache_rules_set_cleanup.py`
- `tests/test_apache_smoke_mime_types.py`
- `Makefile`
- `reports/audits/change-records/README.md`, `README.de.md`, and this paired
  Change Record

## Validation evidence

| Command or control | Result |
| --- | --- |
| Focused source contracts | passed: six Python tests cover RulesSet ownership, the designated C17 sentinel, private runner output, and both MIME locations. |
| Shell syntax | passed for the RulesSet runner, Apache smoke harness, and APXS wrapper template. |
| Focused Apache/Common structure check | passed, including the private-header materialization assertion. |
| GCC C17 APR lifecycle harness | passed with `-Wall -Wextra -Werror`. |
| Clang C17 APR lifecycle harness | passed with `-Wall -Wextra -Werror`. |
| `make check-apache-ruleset-cleanup-lint` | passed; its status receipt reports `apache_rules_set_cleanup` as `passed`. |
| Apache C-standard wiring and JSON source-map validation | passed. |
| Fresh materialization, Autotools configuration, and APXS DSO build | passed after the literal private-header staging correction; the exact candidate DSO was produced. |
| Isolated Apache `phase2_args_block` HTTP/1.1 control | passed: the exact DSO loaded and the configured request returned `403`. |
| Isolated Apache graceful-restart control | passed: readiness succeeded before and after `SIGUSR1`. |
| Focused post-scan security review of the C17 sentinel, APXS header staging, and MIME correction | passed: no new reportable security finding. |
| Aggregate `make check-apache-c17` | failed identically on the assessment baseline and candidate in unchanged `connectors/apache/src/mod_security3.c`; it is tracked separately as `FND-PARENT-0069` and is not claimed as a passing result. |

The original baseline APR harness failed as expected because its first
non-null RulesSet had no pool cleanup. The original freshly materialized APXS
tree lacked the private header, and the original isolated runtime stopped
before request handling because Apache could not resolve the root-level MIME
file. Those retained failures are the respective pre-fix evidence for the
included repairs.

## Security impact

This is a native C configuration-lifecycle and availability remediation.
Rules are trusted Apache operator configuration rather than direct untrusted
HTTP input. The cleanup callback is registered only after successful
allocation, calls its matching native cleanup function, and avoids early or
duplicate cleanup boundaries.

The earlier candidate security review was retained under the registered task
root. A focused follow-up review of the three later deltas found no new
reportable candidate: the designated sentinel is data-independent, header
staging is a fixed literal copy, and the second MIME artifact is deterministic
under the pre-existing validated runtime root. Functional smoke execution is
recorded separately in the validation evidence above.

## Protocol and runtime limits

The evidence establishes the affected Apache configuration-pool lifecycle,
fresh DSO materialization, and one normal HTTP/1.1 control. HTTP/2, HTTP/3,
the full connector matrix, and a Valgrind leak-free certification were not run;
they do not substitute for the specific APR ownership proof. A diagnostic
Valgrind run observed no invalid free or use-after-free in its exercised path,
but an independent `name_for_debug` leak remains outside this delivery scope.

## Delivery status

At record update time, this is a local task-owned Parent commit and its task
PR has not yet been published. The current user authorized one new Parent PR
and protected `master`
integration after exact-head validation. Parent PRs #123/#124 are source
references only and are not merged wholesale. Hosted checks, SonarQube Cloud,
review/thread state, mergeability, protected integration, and resulting-master
verification must be recorded only after they are actually observed.
