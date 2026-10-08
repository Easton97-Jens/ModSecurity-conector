# Change record

**Language:** English | [Deutsch](CR-20261008-nginx-native-response-limit-classification.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-response-limit-classification |
| UTC date | 2026-10-08 |
| Parent base revision | `8b575c09` |

## Motivation and problem statement

A native response-body Reject has no rule correlation and must not enter SAFE's rule-only log-only path or claim Engine EOS.

## Affected components and security boundaries

NGINX native intervention collector, context observation fields, materialization map and controlled C17 tests. Framework, MRTS, generic validators and Gitlinks are unchanged.

## Acceptance criteria

Accept only the exact native response-limit signature; seal BODY_LIMIT without a rule, suppress downstream forwarding and reject unexpected append-time rule decisions before actual Engine completion.

## Alternatives considered

Treating any no-rule403 as a body limit or borrowing SAFE semantics would misclassify arbitrary Engine responses.

## Implementation decision

Use the existing closed native predicate; classify before rule-only dispatch. Record request ownership in the actual context and materialize the existing response-limit/P4 observation headers.

## Changed files and tests

SOURCE_MAP, common context fields, module native intervention flow, twelve actual-source C17 collector controls and this paired record.

## Commands and results

Twelve focused collector tests freshly pass with C17 -Wall -Wextra -Werror. Valid SAFE/STRICT/off controls and wrong-signature, early-rule, invalid-result and missing-correlation negatives remain covered.

## Security impact

No synthetic rule or EOS; no body forwarding after technical Reject. Framework containment/freshness, Required selection and strict event validators unchanged.

## Documentation and runtime evidence

This is a source-state/serializer unit proof, not a fresh artifact or native request result.

## Checks not run

Fresh complete module/binary build, integrated native requests, full Required canonical validation and remote CI/Sonar.

## Limitations and residual risk

Engine-specific signature and actual body completion need genuine new-build runtime validation. Concurrent budget/cleanup changes are not part of this commit.

## Final diff and review status

Focused staged slice reviewed; unrelated orchestration and unstaged source work preserved.

