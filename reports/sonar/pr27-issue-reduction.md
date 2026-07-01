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

Before count from API for this cleanup: 1 open/confirmed issue.

## Issue inventory

| Issue key | Rule | Severity | Type | File | Line | Message | Local fix | Verification |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| AZ8eutpSXijY4QmtfWjQ | c:S1905 | MINOR | CODE_SMELL | common/src/config.c | 198 | Remove this redundant cast. | Added an explicit `MSCONNECTOR_PHASE4_MODE_UNSET` enum value and removed the redundant enum-bound casts in validation. | `make check-common-helpers`, `MSCONNECTOR_C_STD=c17 make check-common-helpers`, and `make check-common-helpers-c17` passed locally. |

After SonarCloud count: NOT VERIFIED. A new SonarCloud analysis result was not available from this local environment after committing changes.

## C standard policy

The common SDK defaults to C17.

C23 is optional and may use `c23` or `c2x` depending on compiler support detected by `ci/detect-c-standard.py`.

Future C checks are optional and may use `c2y` or `gnu2y` where supported by the compiler.

C20 and C26 are not treated as mandatory C compiler modes. The Makefile targets for those names print explicit `SKIPPED` messages instead of pretending to compile C20 or C26.

C++20, C++23, and C++26 apply only to C++ wrapper checks, not C `.c` files. No new C++ wrapper standard smoke check was added in this cleanup.
