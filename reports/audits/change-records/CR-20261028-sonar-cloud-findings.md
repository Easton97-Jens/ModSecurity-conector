# Change Record: CR-20261028-sonar-cloud-findings

**Language:** English | [Deutsch](CR-20261028-sonar-cloud-findings.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-sonar-cloud-findings |
| Date (UTC) | 2026-10-28 |
| Base revision | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |

## Motivation and problem statement

The requested remediation covers all 15 configured Parent Cloud projects (main C++17, two advisory standard projects, twelve native security projects). Complete authenticated paginated issue/hotspot readback found 909 open occurrences, 261 distinct file/line/rule/message positions, and zero hotspots. Main contributes 223 issues. Main/native analyses bind to the base above; advisory readback separately binds to `1d161212124ad882064f8acfcefb721c67bc3d1d`. These are baseline counts, not results for this change.

## Acceptance criteria

Preserve C17/C++17 compatibility and host callback ABI, correct applicable source findings, verify affected behavior and create a Draft PR. Source corrections target 180 positions; 81 individually investigated candidates remain pending Cloud confirmation or explicit false-positive disposition. No server-side transitions were performed. Full closure requires current-head CI/Cloud evidence and resolution of those candidates; it is not claimed.

## Implementation decision and rationale

Apache stores mutable transaction pointers in its module `request_config` vector instead of a string table, preserving current/main/previous-request lookup and owner cleanup. NGINX preserves host-result width, bounds status before conversion, and uses a const allocator snapshot only for no-op PCRE2/disabled hooks; real PCRE1 retains its mutable restoration pointer. HAProxy bounds the original response-header count before narrowing and checks header allocation capacity before second-pass writes. Private pointers/loops are const/scoped; APR time formatting follows its type contract. The evaluator cleanup owner cannot copy/move.

Python simplifies archive canonicalization while retaining original bytes on semantic no-ops, uses function type parameters and specific assertions, and splits equivalent timeout/error expressions. Shell selections explicitly reject unsupported values. Three test-only SDK observers conditionally use modern `contains` while retaining C++17 fallbacks. This source maintenance does not resume I12 qualification.

## Changed files

Affected native Apache/NGINX/HAProxy/lighttpd files and fixtures; `common/scripts/modsecurity_targeted_eval.cc`; reported Python/Shell helpers under `ci/`; `scripts/version_updater_common.py`; three SDK observer sources; affected Apache/NGINX tests and Framework-updater assertion. Only twelve reviewed digests change in `config/testing/active-cases.json`; definitions/selection are unchanged. `reports/testing/test-selection-archive.generated.json` is regenerated through its existing generator. Reader-facing documentation is this record and its German companion. The manually reviewed decision source [triage JSON](../sonarqube-cloud-20261028-triage.json) enumerates all 81 candidate positions and their original project/issue IDs. Framework/MRTS, gitlinks, dependencies, analysis scope, rules and gates are unchanged.

## Commands executed

All commands used RTK and external task-owned build/output roots; detailed argv/exit records are retained in task evidence.

| Command/procedure | Observed result |
| --- | --- |
| `/usr/local/bin/sonar-with-env auth status` and paginated issue/hotspot/analysis/gate/rule queries | Connected; all 15 projects read; no status writes |
| `make check-apache-c17` | PASS, C17 `-Wall -Wextra -Werror`; original read-only Framework selected |
| Three Apache harness/cleanup sources with `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only` | PASS |
| NGINX production/fixtures, GCC/Clang, `MODSECURITY_SANITY_CHECKS=0/1` | PASS, 36 C17 compilations; production also passes Clang `-Wshorten-64-to-32 -Werror` |
| `make check-targeted-evaluator-cpp17` | PASS, compile/link with installed SDK |
| `sh connectors/lighttpd/build/build_module.sh` with pinned patched headers | PASS, real C17 module compile/link |
| `sh connectors/haproxy/htx-overlay/build-overlay.sh` with pinned source and eight workers | PASS, native build; existing warnings in untouched binding/Common remain |
| SPOP source C17 warning-as-error syntax; `make check-haproxy-htx-overlay` | PASS |
| Three SDK observers, C++17/20/23 warning-as-error syntax | PASS, nine compilations |
| Six explicitly selected updater unittest methods | PASS, archive idempotence/admission and Python/Go update behavior; default suite unchanged |
| Changed Python `ast.parse`; legacy smoke script `sh -n`; `shellcheck -x` | PASS |
| `ci/tools/run-active-tests.py --group apache --group null-guard --execution common.targeted-cpp-allow --group nginx --group haproxy` with private external roots | PASS, 15 selected active cases, including actual evaluator allow execution |
| `make check-bilingual-docs`; `make check-doc-links`; Change Record archive check | PASS |
| `make check-active-inventory PYTHON=/usr/local/bin/python3.15` | PASS, 100 standard cases / 80 executions; 1,893 on-demand cases separate; archive matches |

The first active-runner attempt rejected a missing output parent before cases; the next rejected a final whitespace edit's stale source digest. Bindings/archive were refreshed before the final run. Neither rejected attempt is success. Native-context preparation configured and checksum-verified host sources but its final unchanged-checkout guard rejected concurrent edits. Strict ISO C17 parsing of HAProxy's upstream GNU extensions failed; the actual native host build above passed. Documentation checks initially failed because the pinned Framework was not materialized in the new worktree. After initializing the exact existing gitlink, bilingual/link gates passed and `shellcheck -x` passed; no diagnostic was suppressed. The active NGINX extraction fixture initially lacked the new private snapshot type; eight affected fixtures were synchronized, the exact active case passed, and seven sibling setups compiled without executing their scenarios. The subsequent evaluator selection required explicit `RUNNER_TEMP`; the missing-variable failure was retained and the final selection rerun with a private external root. Final selected-run/documentation results belong to the PR after execution.

## Security impact

Controls, callback ABI, ownership checks, JSON escaping, rules and gates remain active. Independent read-only investigation traced Python path/argv and native taint candidates; no supplied flow established a remaining exploitable vulnerability. A fresh independent candidate reviewer found no concrete bypass/regression. This is bounded review, not repository-wide assurance.

The 81 remaining candidates comprise 20 Apache and 15 NGINX host/API callback parameters; eight HAProxy callbacks and three C struct-member namespace reports; nine bounded/escaped native reports; twenty Python path/argument/content-flow reports; three intentional HTTP fixture references; three bounded in-memory text copies reported as logging. Existing root checks, strict SHA/variant validation, JSON escaping and allocation bounds remain. Explicit operator-selected paths are not silently restricted. Server candidates remain open; false-positive approval or risk acceptance is not inferred.

## Runtime evidence

No hosted connector runtime evidence was collected or claimed. Native builds, syntax, selected unit/contract cases and the targeted evaluator remain separate evidence layers. Historical I12 results do not qualify this revision.

## Known limitations

Local Python is 3.15.2 rather than pinned 3.15.1; the existing virtual environment is 3.14.4. No toolchain installation/change. Real PCRE1 headers are unavailable: its pointer/signature compatibility was source-reviewed, while PCRE2 builds passed. Extra fixture-only Clang precision warnings predate this change; production precision checks and ordinary warning-as-error fixture builds pass. Current-head CI/Cloud proof is required for verified delivery.

## Remaining risks

Unit fixtures do not prove actual hosted Apache redirect/subrequest lookup: some substitute module-vector lookup, while the cleanup harness exercises real vector storage and owner cleanup. All 81 candidate positions and any new Cloud findings require follow-through. A source correction alone does not close a Cloud issue.

## Checks not run and rationale

No full default suite, all-connector runtime matrix, historical I12 campaign, real PCRE1 build, or production deployment. Only affected checks were selected. Pending current-head CI/Sonar is not a pass. No merge is authorized.

## Final diff and review status

Independent bounded candidate review found no concrete bypass/regression; scoped worker whitespace checks passed. Final integrated selected checks, documentation gates and delivery facts must be read at the current PR head. Prepared for a Draft PR; all-findings task closure remains partial until remaining candidates and current-head evidence are resolved.
