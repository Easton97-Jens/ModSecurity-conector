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
