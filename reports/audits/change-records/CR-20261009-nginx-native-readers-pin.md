# Change Record: CR-20261009-nginx-native-readers-pin

**Language:** English | [Deutsch](CR-20261009-nginx-native-readers-pin.de.md)

Record of the separately published Framework dependency update; no native PASS is claimed.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-native-readers-pin |
| Date (UTC) | 2026-10-09 |
| Base revision | `e319c932db7da011feca54fcb1fc5d2ab5d6018f` |

## Motivation and problem statement

Bind Parent to the proven standalone native-finalizer package bootstrap and strict case/run-bound projection reader. The Parent producer fixes have separate commits.

## Acceptance criteria

Parent records remotely available Framework b283851c1fd70a031832d2e95e10dfcc4bc4f068. MRTS stays 8a6bb546c4c81d8ffc7be801dceac60c6925685f; all 97 selected Required records stay required.

## Implementation decision and rationale

Update only the Framework Gitlink from 7db219af6b6e911b73de8b437f82e63efdb06bde after its normal branch push and fresh branch/PR readback. No merged master dependency, history rewriting or Parent dispatch change is needed in this commit.

## Changed files

modules/ModSecurity-test-Framework Gitlink and this EN/DE Change Record pair.

## Commands executed

All commands RTK-wrapped. At exact b283851, Framework unittest discovery under tests/no_crs passed 405 tests / 182.368s / exit 0; repository make lint terminated 0. Dedicated combined CLI/reader: 32 tests and full four documentation checks exited 0. git push was a normal 7db219a..b283851 fast-forward; git ls-remote and gh pr view 137 independently returned b283851, OPEN/DRAFT/base master. Nested Parent Framework checkout and unchanged actual MRTS HEAD were read back. External task evidence Run-ID: nginx-all-required-20261008T124555Z; files framework-integrated-suite-r1.log/.exit and framework-integrated-lint-r1.log/.exit. These are source gates, not runtime evidence.

## Security impact

Authority, source seals, strict status/evidence checks and projection freshness remain mandatory. No legacy-name fallback, payload synthesis or Required reduction.

## Runtime evidence

The prior f639 local R3 run terminated 2 and finalization did not produce an original Canonical result. Its projection/import failures and all original bytes remain historical diagnostic evidence, not evidence for this pin.

## Known limitations

Fresh Parent post-pin focus, full native lint, new NGINX/module/interposer artifacts and real Root/nobody all 97 lifecycle remain outstanding.

## Remaining risks

Current revision-bound PR CI/Sonar, genuine runtime, complete Canonical proof and checksum validation are still required. Protected Trusted-Base/runner/admin prerequisites are independently blocked.

## Checks not run and rationale

No fresh whole97 native E2E or protected dispatch has run at this pin; prerequisites are checked before those operations. Separate Ruff lint remains unavailable, not waived.

## Final diff and review status

Gitlink-only diff reviewed; Framework normal delivery is verified against current branch and Draft PR #137. Parent PR #396 stays Draft. No MRTS Source/Git changes or merge.
