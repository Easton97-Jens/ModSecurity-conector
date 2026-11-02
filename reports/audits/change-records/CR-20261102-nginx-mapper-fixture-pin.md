# Change Record: CR-20261102-nginx-mapper-fixture-pin

**Language:** English | [Deutsch](CR-20261102-nginx-mapper-fixture-pin.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261102-nginx-mapper-fixture-pin |
| Date (UTC) | 2026-11-02 |
| Base revision | `97dfcaddb698d5b95c3f78531eb81803699ffbe1` |

## Motivation and problem statement

Existing Connector Draft [#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348)
pins Framework b852802. Its standalone NGINX mapper status fixture omits the
real header-defined authority helper now called by the actual mapper. Before:
C17/-Wall/-Wextra/-Werror emits implicit declaration and incompatible
ngx_str_t-from-int errors in setUpClass; zero methods execute.
External Framework [#153](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/153)
fixes only fixture dependencies and necessary generated descriptions/EN/DE record.
It is based on current masterbc08ee7 and preserves independent merged#151.
This Parent change pins its locally verified remote commit
`34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747`, not an old snapshot or uncommitted work.

## Acceptance criteria

Pin the same tested remote SHA in gitlink, lock and every registered action/
workflow projection. Preserve MRTS and independent versions. Repeat all five
existing mapper methods with all existing subcases and zero skips at the final
committed pair, plus relevant projection/provenance/generator/docs/secrets/
adjacent NGINX checks. Publish only a normal additive commit to existing#348.
Current-head CI/CodeQL/Sonar must be evaluated separately; no old green is reused.

## Implementation decision and rationale

The current dependent-PR contract in `docs/test-ownership-migration.md`
permits a published Framework PR SHA as a provisional pin and requires Framework
integration before eventual Connector integration. No merge is authorized here.
Use native candidate verifier and component-version synchronizer, not manual
hash edits. Extract only exact committed Framework `ci/lib/common.sh` through
`git archive` to the external RUNNER_TEMP input; do not execute that shell data.
Old pinned context verifies the pre-transition; new pinned context verifies
post-transition. No product-code fix or context-PR#436 integration.

## Changed files

Framework gitlink; `ci/tooling/project-versions.lock.json`;22registered workflows
with54Framework identity references; this EN/DE Change Record. All changed
workflow bytes are only b852802→34dc7f9 revision replacements.
MRTS remains `8a6bb546c4c81d8ffc7be801dceac60c6925685f`,
Python3.15.1 and Go1.27.3 lock values remain unchanged. Product source,
independent dependency versions and trusted broker ownership do not change.
Compiler-guide generator ran; all existing generated guides remain unchanged.

## Commands executed

RTK required throughout. Parent Python is `$PARENT_PYTHON`; existing Framework
Python is `$FRAMEWORK_PYTHON`, both locally observed3.14.4; this is not evidence
of execution on the independently pinned hosted Python versions.
Explicit TEST_ROOT/FRAMEWORK_ROOT select the nested pinned Framework,
CONNECTOR_ROOT/CONNECTOR_REVISION select this exact task checkout/HEAD, profile
protocol-integrity, and RUNNER_TEMP/output/temp/cache roots are external.
Run: `nginx-mapper-fixture-20261102`.

| Actual command / procedure | Exit code | Observed result |
| --- | --- | --- |
| `ci/tools/new-change-record.py create --name nginx-mapper-fixture-pin --base-revision 97dfcaddb698d5b95c3f78531eb81803699ffbe1 --date 2026-11-02` with explicit Framework import context | 0 | Native paired scaffold created |
| `ci/tools/verify-framework-candidate-contract.py --repo-root "$CONNECTOR_ROOT" --candidate-sha 34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747 --framework-common "$EXACT_COMMON" --candidate-framework-root "$CANDIDATE_FRAMEWORK" --expected-parent-framework-sha b85280278310f4034af78149ac13671438965c7b` | 0 | Verified before transition with old pinned context |
| `ci/tools/sync-framework-component-versions.py --sync --repo-root "$CONNECTOR_ROOT" --framework-common "$EXACT_COMMON" --framework-sha 34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747` | 0 |23native projection paths changed |
| Same synchronizer `--check` | 0 | changed=[] |
| Candidate verifier with new pinned context and `--expected-parent-framework-sha 34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747` | 0 | New pair verified |
| Synchronizer `--verify-primary --base 97dfcaddb698d5b95c3f78531eb81803699ffbe1` with same repo/common/SHA | 0 | FRAMEWORK_PRIMARY_VERIFIED |
| `scripts/generate_compiler_guides.py` | 0 | No generated-guide drift |
| Framework `-m unittest -v modsecurity_connector_tests.test_nginx_request_mapper_status` with nested pinned fix | 0 |5PASS before Parent commit |

Initial setup failures are not concealed: native record creation without explicit
Framework imports failed1; candidate check using candidate context against old
action pins failed2; synchronizer rejected common.sh outside its authorized
RUNNER_TEMP root with2. Each failed before writing product projections, and the
correct explicit import/context and native archive input resolved it without
weakening validation. External exact commands and final-pair receipts remain
under the approved run; delivery/current-head facts are recorded when observed.

## Security impact

Integrity maintenance, not remediation of a validated product vulnerability.
The external fixture extracts actual next_header and authority bodies with
correct signatures, dependency order, host types/macros and both compile-time
HTTP/3 branches. Its five methods/probe ASTs,14probes,10named subtests, failure
injections, header boundaries and strict compiler flags are unchanged.
No source stub, collector exemption, gate/protection weakening or MRTS write.

## Runtime evidence

None newly collected. Standalone C17 fixture/contract checks prove only that
layer, not hosted NGINX/TLS/H2/H3 qualification. No full campaign is in scope.

## Known limitations

Framework153 remains Draft/unmerged. It must be integrated before eventual
Connector348 merge, not automatically by this task. Parent's final committed
pair and new-head hosted checks remain separate delivery steps.
Nested MRTS is uninitialized locally; the strict independent-MRTS-HEAD provenance
check cannot be claimed passed on this host. Preserve this boundary and use
actual fresh hosted evidence if available, without changing MRTS locally.

## Remaining risks

Future master integration changes commit identity and needs its own verified pin
follow-up. Mandatory current-head CI/CodeQL/Sonar findings may require focused
follow-up commits; none are pre-accepted or suppressed.

## Checks not run and rationale

No broad default/historical suite, MRTS execution, installed host campaign or full
H2/H3 qualification. Final committed-pair and new-head hosted gates are pending
at this preparation checkpoint, not replaced by earlier head results.

## Final diff and review status

Task-owned projection/record preparation only. Final staged whitespace,
independent diff/EN-DE review, secret scan, final-pair verification and normal
additive push are required before claiming the delivery endpoint.
No credentials, private payloads, inherited environment dump or unrestricted logs
are included. Main checkout/foreign work and separate contextPR436 stay untouched.

### Local preparation verification

Native `new-change-record.py check`, `make check-project-versions check-bilingual-docs check-doc-links`,
staged `--verify-primary`, public inventory admission and native archive `--check`
passed (exit0each). Admission remains100active/limit100 and2586on-demand,
inventory SHA-256 `fc007bdea733980700a74609acb41e5332977516b19f2f6e2823ecb5860557fd`.
The initial archive-structure check rejected the new German language-switch
format; restoring the exact native format corrected only this record.
Redacted staged-diff Gitleaks passed (40444bytes,no leaks) and whitespace passed.
Independent staged-diff/EN-DE review confirmed only22workflow/54identity
substitutions, framework_sha-only lock change, exact remote gitlink and records.
Final committed-pair receipts and fresh hosted analysis remain required.
