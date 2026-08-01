# FND-PARENT-0044 — Python workflow-security contract rejects the current immutable setup-python v7 pin

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0044 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity | P1 / not_applicable |
| Confidence / status | confirmed / fixed |
| Feasibility | feasible_now |
| Release blocker | yes |
| Security relevant | yes |

## Observation and impact

Current master `2ade0d40983b7af21a65b8cd2884866b85626393` correctly pins every
active `actions/setup-python` use and its reviewed lock entry to
`5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0`. The stricter Python
workflow checker instead still requires
`ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0`.

The retained clean-master command

```text
rtk proxy env PYTHON=/root/git/ModSecurity-conector/.venv/bin/python PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract
```

therefore exits `2`. It rejects the approved v7 pin, reports zero recognized
setup steps, and cascades into false setup-before-use errors. This is a CI
supply-chain-control availability and integrity issue; no mutable action
execution, credential exposure, repository-write bypass, or connector runtime
exploit was demonstrated.

## Evidence, cause, and intended repair

- Run: `20260721T101749Z-parent-python314-go126-upgrade-8add1076`
- Retained artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T101749Z-parent-python314-go126-upgrade-8add1076/evidence/python-contract-prechange-failure.md`
- SHA-256:
  `461d1710225eb8f79008308ebbc168fab50d968dc2e9ea8e55da5e1e1b3fb921`
- Exit status: `2`
- Post-remediation retained artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T101749Z-parent-python314-go126-upgrade-8add1076/evidence/python-go-toolchain-final-local-validation.md`
- Post-remediation SHA-256:
  `2dca237a075dd15f7e7e5a90e26bca8328a88bb89076063856a21ccb15bb3dbd`

The v7 workflows and `ci/tooling/security-tools.lock.yml` entry are already
correct and must not be changed. The prior v7 transaction left this
Python-specific checker, its valid fixtures, and expected test strings on the
old v6 identity. The narrow repair updates exactly those checker/test/fixture
expectations to the existing v7 SHA and comment while preserving immutable
pins, lock membership, permissions, triggers, checkout behavior,
`check-latest: false`, and setup-before-use validation.

The same atomic candidate also moves the requested Python series to exact
`3.14.6`. The updater continues to accept only stable exact `3.14.N` patches;
it must not become a cross-minor or floating-version updater.

## Required controls and disposition

The repaired checker must accept a valid exact v7 reference and continue to
reject a mutable tag, short SHA, missing comment, wrong comment, and a
lock-mismatched SHA. The original contract and its unit suite must pass, as
must the independent CI-security workflow contract. A diff review must confirm
that actual workflow pins and the reviewed lock remain unchanged.

The local outcome is `confirmed` and `fixed`, not verified or closed. The
original contract now passes for Python `3.14.6` and 25 Python jobs; 98 focused
unit tests, the independent CI-security contract, compiler-guide check,
compileall, and scoped lock/diff controls also pass. Exact Python `3.14.6`
action resolution and exact Go `1.26.5` CodeQL execution still need final
candidate-head hosted evidence. The full bilingual target is blocked only by
the intentionally uninitialized Framework gitlink; Framework and MRTS remain
unchanged. No staging, commit, push, pull request, merge, Framework change, or
MRTS action has occurred.

## History

- 2026-07-21T10:17:49Z — clean current-master reproduction retained the v6/v7
  mismatch and exit `2`.
- 2026-07-21T10:28:55Z — distinct Parent CI supply-chain contract finding
  allocated after deduplication against FND-PARENT-0018; atomic local
  remediation began without changing live action pins or locks.
- 2026-07-21T11:07:03Z — remediation and legitimate controls passed locally:
  the original contract, 98 focused unit tests, CI-security contract,
  compiler-guide check, compileall, and scoped lock/diff review passed; exact
  target-runtime and exact-head hosted evidence remain required.
