# Change Record: CR-20261008-common-mapper-body-pointer-invariant

**Language:** English | [Deutsch](CR-20261008-common-mapper-body-pointer-invariant.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-common-mapper-body-pointer-invariant |
| Date (UTC) | 2026-10-08 |
| Base revision | `85397f4d621c568316566faccac6c217fc5315d8` |

## Motivation and problem statement

Actual Common request_validate rejected nonzero body size with null data, but exported request_mapper_validate_output incorrectly accepted the same malformed request.

## Acceptance criteria

Reject that already-defined invariant at the actual mapper boundary; preserve valid/empty requests and unsupported/oversized error precedence.

## Implementation decision and rationale

Add one bounded body-pointer consistency guard after existing body-policy guards. No new host policy or synthetic runtime observation.

## Changed files

common/src/request_mapper_contract.c; tests/fixtures/nginx_common_input_validation.c; tests/test_nginx_common_input_validation.py; EN/DE record.

## Commands executed

Actual-source C11 Wall/Wextra/Werror compiled probe RED1 (mapper1 vs request-validator0), then GREEN4; native make check-common-helpers (C17) and check-adapter-contracts exit0. Diff and record structure checks before commit.

## Security impact

Malformed adapter output now fails closed consistently with the existing request helper. Header guard and all previous body-policy errors remain unchanged.

## Runtime evidence

Compiled real Common validators only; no HTTP/native daemon/canonical PASS claimed. Fresh integrated NGINX fault invocation still required.

## Known limitations

Catalog and native fault wiring are coordinator-owned. Existing native NGINX mapper rejection is phase1/HTTP400, not fabricated phase2/500.

## Remaining risks

Interposer must bind exact own worker, native transaction and URI; fault rejection and cleanup must be observed before coverage promotion.

## Checks not run and rationale

Full lint, rebuilt native connector fault run and remote CI/Sonar remain pending. No old binary is relabeled.

## Final diff and review status

One product guard plus focused tests and bilingual record; separate local commit, no push, history rewrite, gitlink or MRTS changes.
