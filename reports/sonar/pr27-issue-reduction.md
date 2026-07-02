**Language:** English | [Deutsch](pr27-issue-reduction.de.md)

# PR 27 Sonar issue reduction inventory

SonarCloud API query used before this cleanup:

```sh
python3 - <<'PY'
import json, os, urllib.request
url = 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=27&issueStatuses=OPEN,CONFIRMED&sinceLeakPeriod=true&ps=100&additionalFields=rules'
request = urllib.request.Request(url)
# If SONAR_TOKEN is present, use it without printing it.
with urllib.request.urlopen(request, timeout=20) as response:
    data = json.load(response)
print(data['total'])
PY
```

Before count from API for the previous C-standard cleanup: 1 open/confirmed issue.

Current SonarCloud count before this cleanup: 5 open/confirmed issues. Additional issues addressed in this cleanup: duplicated `-std=c17`, duplicated `-std=c2x`, `[0-9]` regex digit-class findings, and `pythonsecurity:S8701` in `ci/detect-c-standard.py` from the latest SonarCloud screenshot/context.

## Issue inventory

| Issue key | Rule | Severity | Type | File | Line | Message | Local fix | Verification |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| AZ8eutpSXijY4QmtfWjQ | c:S1905 | MINOR | CODE_SMELL | common/src/config.c | 198 | Remove this redundant cast. | Added an explicit `MSCONNECTOR_PHASE4_MODE_UNSET` enum value and removed the redundant enum-bound casts in validation. | `make check-common-helpers`, `MSCONNECTOR_C_STD=c17 make check-common-helpers`, and `make check-common-helpers-c17` passed locally. |
| AZ8e0c2868MLw0jos7KS | python:S1192 | UNKNOWN | CODE_SMELL | ci/detect-c-standard.py | standard flag constants | Define a constant instead of duplicating `-std=c17`. | Added `STD_C17` and reused it in profiles, allow-list, and self-test. | `python3 ci/detect-c-standard.py --self-test` and `python3 ci/check-common-sdk-contract.py` passed locally; SonarCloud after-count NOT VERIFIED. |
| AZ8e0c2868MLw0jos7KR | python:S1192 | UNKNOWN | CODE_SMELL | ci/detect-c-standard.py | standard flag constants | Define a constant instead of duplicating `-std=c2x`. | Added `STD_C2X` and reused it in profiles, allow-list, and self-test. | `python3 ci/detect-c-standard.py --self-test` and `python3 ci/check-common-sdk-contract.py` passed locally; SonarCloud after-count NOT VERIFIED. |
| AZ8e0c2868MLw0jos7KT/AZ8e0c2868MLw0jos7KU | python:S6353 | UNKNOWN | CODE_SMELL | ci/detect-c-standard.py | compiler validation regex | Use concise character class syntax `\d` instead of `[0-9]`. | Removed the compiler basename regex by replacing arbitrary command validation with fixed compiler-id choices. | `python3 ci/detect-c-standard.py --self-test` and `python3 ci/check-common-sdk-contract.py` passed locally; SonarCloud after-count NOT VERIFIED. |
| AZ8eyFH9F6pdaofMWPVp | pythonsecurity:S8701 | UNKNOWN | VULNERABILITY | ci/detect-c-standard.py | around subprocess.run | LLMs running this code with faulty CLI arguments can escape from shell sandboxes. | Removed arbitrary `--cc` command/path support, added allow-listed `--compiler` choices, resolved only fixed compiler ids, retained internal standard-flag validation, retained `shell=False`, added subprocess timeout and a conservative environment, and updated `--self-test` malicious-input checks. | `python3 ci/detect-c-standard.py --self-test` and common SDK checks passed locally; SonarCloud after-count NOT VERIFIED. |

After SonarCloud count: NOT VERIFIED. A new SonarCloud analysis result was not available from this local environment after committing changes.

## C standard policy

The common SDK defaults to C17.

C23 is optional and may use `c23` or `c2x` depending on compiler support detected by `ci/detect-c-standard.py`.

Future C checks are optional and may use `c2y` or `gnu2y` where supported by the compiler.

C20 and C26 are not treated as mandatory C compiler modes. The Makefile targets for those names print explicit `SKIPPED` messages instead of pretending to compile C20 or C26.

C++20, C++23, and C++26 apply only to C++ wrapper checks, not C `.c` files. No new C++ wrapper standard smoke check was added in this cleanup.

## Event model Sonar cleanup

| Issue key | Rule | Severity | Type | File | Line | Message | Local fix | Verification |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| NOT VERIFIED | c:S1820-equivalent struct-size finding | UNKNOWN | CODE_SMELL | common/include/msconnector/event.h | struct definition | Refactor this structure so it has no more than 20 fields. | Grouped event metadata into nested connector-neutral structs (`meta`, `decision`, `http`, `request`, and `flags`) while preserving the Phase 4 hard-abort-after-HTTP-200 semantics. | Local smoke and contract checks run in this PR update; SonarCloud after-count NOT VERIFIED. |
| NOT VERIFIED | c:S1066-equivalent nested-if finding | UNKNOWN | CODE_SMELL | common/src/event.c | escape helper | Merge this `if` statement with the enclosing one. | Merged the truncation-condition check with the null-output-parameter check in `escape_field()`. | Local smoke and contract checks run in this PR update; SonarCloud after-count NOT VERIFIED. |

SonarCloud after-count: NOT VERIFIED.

## Common SDK expansion after review

This update adds connector-neutral helper modules for header duplicate and
Set-Cookie/Content-Length policy, the common decision model, common error model,
rule-loader backend orchestration, a ModSecurity engine facade, and a
transaction-ID resolver. These modules are common SDK scaffolding only and do not
change connector runtime behavior.

SonarCloud after-count: NOT VERIFIED.

## Common SDK merge-blocker completion

Local fixes added for Windows absolute/UNC path rejection, safe versioned
compiler IDs, empty adapter metadata fields, leading OWS Content-Type matching,
event truncation-marker recomputation, bilingual documentation/report companions,
and error/unsupported status validation.

Common-only infrastructure added: adapter interface, adapter contract foundation,
capability-to-test matrix, JSONL event writer, runtime artifact layout, runtime
path joining, common harness helpers, generated common docs, and new connector
contract documentation.

SonarCloud after-count: NOT VERIFIED.

## Common SDK package completion

Added local common-only helpers for config parsing, request/response validation,
rule merge/error/event modeling, test-result JSON, connector manifests, runtime
report skeletons, origin governance, build contracts, C++ wrappers, limits,
rule-ID extraction, log sanitizing, and body-snippet redaction.

SonarCloud after-count: NOT VERIFIED.

## PR 27 SonarCloud and Codex review cleanup

SonarCloud issue retrieval: VERIFIED locally through the SonarCloud issues API for pull request 27 on 2026-07-02.

| Issue key | Rule | Severity | Type | File | Line | Message | Local fix |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| AZ8h0PV7RDWH5g0oIri2 | c:S1659 | MINOR | CODE_SMELL | common/src/connector_manifest.c | 14 | Define each identifier in a dedicated statement. | Split combined local declarations. |
| AZ8h0PV7RDWH5g0oIri0 | c:S3972 | CRITICAL | CODE_SMELL | common/src/connector_manifest.c | 15 | Move this `if` to a new line or add the missing `else`. | Expanded compact statements into explicit blocks. |
| AZ8h0PV7RDWH5g0oIri1 | c:S3972 | CRITICAL | CODE_SMELL | common/src/connector_manifest.c | 19 | Move this `if` to a new line or add the missing `else`. | Expanded compact statements into explicit blocks. |
| AZ8h0PUFRDWH5g0oIrit | c:S3972 | CRITICAL | CODE_SMELL | common/src/log_sanitize.c | 5 | Move this `if` to a new line or add the missing `else`. | Expanded compact sanitizer control flow. |
| AZ8h0PUFRDWH5g0oIriu | c:S3972 | CRITICAL | CODE_SMELL | common/src/log_sanitize.c | 5 | Move this `if` to a new line or add the missing `else`. | Expanded compact sanitizer control flow. |
| AZ8h0PUFRDWH5g0oIriv | c:S2681 | MAJOR | CODE_SMELL | common/src/log_sanitize.c | 6 | This statement will not be executed conditionally. | Split loop body into explicit conditional blocks. |
| AZ8h0PUFRDWH5g0oIriw | c:S3972 | CRITICAL | CODE_SMELL | common/src/log_sanitize.c | 10 | Move this `if` to a new line or add the missing `else`. | Expanded redaction helper control flow. |
| AZ8h0PUFRDWH5g0oIrix | c:S1066 | MAJOR | CODE_SMELL | common/src/log_sanitize.c | 13 | Merge this `if` statement with the enclosing one. | Merged truncation condition. |
| AZ8h0PQORDWH5g0oIrio | c:S3972 | CRITICAL | CODE_SMELL | common/src/rule_id.c | 6 | Move this `if` to a new line or add the missing `else`. | Expanded validation loop control flow. |
| AZ8h0PQORDWH5g0oIrip | c:S3358 | MAJOR | CODE_SMELL | common/src/rule_id.c | 14 | Extract this nested conditional operator into an independent statement. | Replaced nested conditional expression with explicit helper logic. |
| AZ8h0PT1RDWH5g0oIris | c:S1659 | MINOR | CODE_SMELL | common/src/runtime_report.c | 9 | Define each identifier in a dedicated statement. | Split combined declarations. |
| AZ8h0PT1RDWH5g0oIriq | c:S3972 | CRITICAL | CODE_SMELL | common/src/runtime_report.c | 10 | Move this `if` to a new line or add the missing `else`. | Expanded compact statements into explicit blocks. |
| AZ8h0PT1RDWH5g0oIrir | c:S3972 | CRITICAL | CODE_SMELL | common/src/runtime_report.c | 14 | Move this `if` to a new line or add the missing `else`. | Expanded compact statements into explicit blocks. |
| AZ8h0PUYRDWH5g0oIriz | c:S1659 | MINOR | CODE_SMELL | common/src/test_result_json.c | 7 | Define each identifier in a dedicated statement. | Split combined declarations. |
| AZ8h0PUYRDWH5g0oIriy | c:S3972 | CRITICAL | CODE_SMELL | common/src/test_result_json.c | 8 | Move this `if` to a new line or add the missing `else`. | Expanded compact statements into explicit blocks. |
| AZ8hZiJnK0SfOljMWPbQ | c:S107 | MAJOR | CODE_SMELL | common/src/event.c | 17 | This function has 31 parameters, which is greater than the 7 authorized. | Replaced the long formatter parameter list with grouped JSON parts. |
| AZ8hZiFPK0SfOljMWPbH | shelldre:S7679 | MAJOR | CODE_SMELL | ci/common-harness.sh | 5 | Assign this positional parameter to a local variable. | Assigned positional parameter before use. |
| AZ8hZiFPK0SfOljMWPbI | shelldre:S7679 | MAJOR | CODE_SMELL | ci/common-harness.sh | 13 | Assign this positional parameter to a local variable. | Assigned positional parameter before use. |
| AZ8hZiFPK0SfOljMWPbJ | shelldre:S7679 | MAJOR | CODE_SMELL | ci/common-harness.sh | 20 | Assign this positional parameter to a local variable. | Assigned positional parameters before use. |
| AZ8hZiFPK0SfOljMWPbK | shelldre:S7679 | MAJOR | CODE_SMELL | ci/common-harness.sh | 21 | Assign this positional parameter to a local variable. | Assigned positional parameters before use. |
| AZ8hZiFPK0SfOljMWPbL | shelldre:S7679 | MAJOR | CODE_SMELL | ci/common-harness.sh | 21 | Assign this positional parameter to a local variable. | Assigned positional parameters before use. |
| AZ8hZiFPK0SfOljMWPbM | shelldre:S7682 | MAJOR | CODE_SMELL | ci/common-harness.sh | 26 | Add an explicit return statement at the end of the function. | Added explicit returns to status helpers. |
| AZ8hZiFPK0SfOljMWPbN | shelldre:S7682 | MAJOR | CODE_SMELL | ci/common-harness.sh | 27 | Add an explicit return statement at the end of the function. | Added explicit returns to status helpers. |
| AZ8hZiFPK0SfOljMWPbO | shelldre:S7682 | MAJOR | CODE_SMELL | ci/common-harness.sh | 28 | Add explicit return statement at the end of the function. | Added explicit returns to status helpers. |
| AZ8hZiFPK0SfOljMWPbP | shelldre:S7682 | MAJOR | CODE_SMELL | ci/common-harness.sh | 29 | Add an explicit return statement at the end of the function. | Added explicit returns to status helpers. |
| AZ8fMphbXWdE1DtM8Ybj | c:S1659 | MINOR | CODE_SMELL | common/src/headers.c | 62 | Define each identifier in a dedicated statement. | Split combined declarations. |
| AZ8fMpmSXWdE1DtM8Ybr | c:S954 | MAJOR | CODE_SMELL | common/include/msconnector/transaction.h | 30 | Move this `#include` directive to the top of the file. | Removed the late include and included the needed decision header directly where used. |
| AZ8fMplZXWdE1DtM8Ybk | c:S3358 | MAJOR | CODE_SMELL | common/src/error.c | 69 | Extract this nested conditional operator into an independent statement. | Replaced nested conditional expression with explicit branch selection. |
| AZ8fMplZXWdE1DtM8Ybl | c:S3358 | MAJOR | CODE_SMELL | common/src/error.c | 69 | Extract this nested conditional operator into an independent statement. | Replaced nested conditional expression with explicit branch selection. |
| AZ8fMplvXWdE1DtM8Ybm | c:S995 | MINOR | CODE_SMELL | common/src/modsecurity_engine.c | 5 | Make the type of this parameter a pointer-to-const. | Made the readiness helper transaction parameter const. |
| AZ8fMplvXWdE1DtM8Ybn | c:S3972 | CRITICAL | CODE_SMELL | common/src/modsecurity_engine.c | 37 | Move this `if` to a new line or add the missing `else`. | Expanded compact ModSecurity facade control flow. |
| AZ8fMplvXWdE1DtM8Ybo | c:S3972 | CRITICAL | CODE_SMELL | common/src/modsecurity_engine.c | 43 | Move this `if` to a new line or add the missing `else`. | Expanded compact ModSecurity facade control flow. |
| AZ8fMplvXWdE1DtM8Ybp | c:S3972 | CRITICAL | CODE_SMELL | common/src/modsecurity_engine.c | 53 | Move this `if` to a new line or add the missing `else`. | Expanded compact ModSecurity facade control flow. |
| AZ8fMplvXWdE1DtM8Ybq | c:S3972 | CRITICAL | CODE_SMELL | common/src/modsecurity_engine.c | 53 | Move this `if` to a new line or add the missing `else`. | Expanded compact ModSecurity facade control flow. |

SonarCloud after-count: NOT VERIFIED. Local checks do not trigger a new SonarCloud analysis.
