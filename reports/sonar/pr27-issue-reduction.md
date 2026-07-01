# PR 27 Sonar issue reduction inventory

SonarCloud API query used before local fixes:

```sh
python3 - <<'PY'
import json, urllib.request
url = 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=27&issueStatuses=OPEN,CONFIRMED&sinceLeakPeriod=true&ps=100&additionalFields=rules'
with urllib.request.urlopen(url, timeout=20) as response:
    data = json.load(response)
print(data['total'])
PY
```

Before count from API: 33 open/confirmed issues.

## Issue inventory

| Issue key | File | Line | Rule/message | Planned fix | Status | Verification |
| --- | --- | ---: | --- | --- | --- | --- |
| AZ8eUBZgE36x1qGA8b86 | common/src/config.c | 39 | c:S3776 cognitive complexity | Split merge/validation helpers and remove macro-heavy merge body | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaIE36x1qGA8b9C | common/src/decision_action.c | 4 | c:S2681 unconditionally executed statement | Expand one-line function into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaIE36x1qGA8b9D | common/src/decision_action.c | 4 | c:S2681 unconditionally executed statement | Expand one-line function into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaIE36x1qGA8b9E | common/src/decision_action.c | 4 | c:S2681 unconditionally executed statement | Expand one-line function into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaIE36x1qGA8b9F | common/src/decision_action.c | 4 | c:S2681 unconditionally executed statement | Expand one-line function into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaIE36x1qGA8b9G | common/src/decision_action.c | 4 | c:S3972 move if/newline or add else | Expand one-line function into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaIE36x1qGA8b9H | common/src/decision_action.c | 4 | c:S3972 move if/newline or add else | Expand one-line function into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaIE36x1qGA8b9I | common/src/decision_action.c | 4 | c:S3972 move if/newline or add else | Expand one-line function into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaAE36x1qGA8b8_ | common/src/directive_spec.c | 19 | c:S5955 declare loop variable in loop | Move loop variable into C17 for-loop declaration | fixed locally | `MSCONNECTOR_C_STD=c17 make check-common-helpers` passed |
| AZ8eUBaAE36x1qGA8b9A | common/src/directive_spec.c | 19 | c:S2681 unconditionally executed statement | Expand function formatting and conditionals | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaAE36x1qGA8b9B | common/src/directive_spec.c | 19 | c:S2681 unconditionally executed statement | Expand function formatting and conditionals | fixed locally | `make check-common-helpers` passed |
| AZ8eUBWXE36x1qGA8b80 | common/src/event.c | 7 | c:S2681 unconditionally executed statement | Expand event init/status/json functions | fixed locally | `make check-common-helpers` passed |
| AZ8eUBWXE36x1qGA8b81 | common/src/event.c | 7 | c:S1659 one identifier per statement | Split local declarations | fixed locally | `make check-common-helpers` passed |
| AZ8eUBZXE36x1qGA8b80-AZ8eUBZXE36x1qGA8b85 | common/src/headers.c | 8-31 | c:S5955/c:S1659 loop variable/declarations | Move loop variables into loops and split declarations | fixed locally | `make check-common-helpers` passed |
| AZ8eUBabE36x1qGA8b9P-AZ8eUBabE36x1qGA8b9S | common/src/json_escape.c | 2-3 | c:S2681/c:S1659 one-line conditionals/declarations | Split JSON escape helpers into structured functions | fixed locally | `make check-common-helpers` passed |
| AZ8eUBZnE36x1qGA8b8--AZ8eUBZnE36x1qGA8b89 | common/src/late_intervention.c | 4 | c:S3972/c:S2681 one-line conditionals | Expand policy helpers into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBaRE36x1qGA8b9J-AZ8eUBaRE36x1qGA8b9O | common/src/path_policy.c | 5 | c:S3972/c:S2681 one-line conditionals | Expand path helper conditionals | fixed locally | `make check-common-helpers` passed |
| AZ8eUBalE36x1qGA8b9T | common/src/transaction_state.c | 3 | c:S2681 unconditionally executed statement | Expand init helper into structured blocks | fixed locally | `make check-common-helpers` passed |
| AZ8eUBalE36x1qGA8b9U | common/src/transaction_state.c | 4 | c:S2681 unconditionally executed statement | Expand phase marking helper into structured blocks | fixed locally | `make check-common-helpers` passed |

After SonarCloud count: NOT VERIFIED. A new SonarCloud analysis result was not available from this local environment after committing changes.
