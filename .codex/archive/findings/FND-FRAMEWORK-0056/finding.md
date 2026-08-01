# FND-FRAMEWORK-0056 — PCRE2 archive-digest regression fixture omits the ModSecurity v3 provenance manifest

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0056 |
| Category | test_failure |
| Repository / ownership | framework / framework |
| Priority / severity / confidence | P1 / not_applicable / reproduced |
| Status / feasibility | closed / feasible_now |
| Release blocker / security relevant | false / true |
| Affected revision | `77d73decd094a8f289fbe0ef2582f12430923e24` |
| Parent/MRTS disposition | no Parent gitlink or MRTS action; Framework remains unmodified |

## Summary, observed and expected behavior, and impact

The focused PCRE2 archive-digest fixture creates `MODSECURITY_V3_SOURCE_DIR` with only `v3-source/.git`. The current Framework provenance guard correctly requires a regular non-symlink `.gitmodules` manifest before Apache PCRE2 setup. All four invalid-digest subcases therefore assert the wrong blocker, and the matching-digest legitimate control exits `77` before its PCRE2 tar marker.

The fixture must instead model the smallest valid non-network ModSecurity v3 source contract required by the current provenance guard, then exercise invalid PCRE2 digest rejection before tar extraction and the matching-digest extraction control. The production provenance control must not be weakened, bypassed, or stubbed out.

The real V3 guard remains fail-closed, but this focused security-regression test no longer covers its intended PCRE2 archive-integrity controls dynamically. This is not evidence of a new source-provenance bypass and does not block Parent PR #74's independently required hosted producer evidence.

## Affected files, symbols, preconditions, and reproduction

Affected Framework files are `tests/security_regression/test_pcre2_archive_digest.py`, `ci/lib/common.sh`, and `ci/provisioning/prepare-apache-build.sh`. Relevant symbols are `Pcre2ArchiveDigestTests._run_case`, `ci_require_approved_modsecurity_v3_checkout`, and `ensure_modsecurity_v3_source`.

At the recorded Framework revision, the fixture supplies an existing V3 source directory containing only `.git`; the Apache builder calls the current V3 provenance guard before it verifies the PCRE2 digest. Reproduce with:

```sh
rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests/security_regression -p test_pcre2_archive_digest.py -v
```

The run has exit status `1`: empty, whitespace, invalid, and mismatching digest subcases report an unapproved V3 source, and the matching control exits `77` with the missing `.gitmodules` blocker.

## Evidence and root cause

Retained evidence: `.codex/runs/20260726T084657Z-framework-pcre2-fixture-regression/evidence/framework-pcre2-fixture-failure.md` (SHA-256 `b11ecbb1a4a0f95a8c2427db3033e1a00d72ddc10ab5356dc27720111a657dac`).

`FND-FRAMEWORK-0030` intentionally hardened the V3 topology guard to require an approved non-symlink `.gitmodules` manifest. The older PCRE2 fixture represents a source root only by creating `.git`, so it no longer reaches the archive-digest verifier. The production guard behaves as designed; the test fixture contract is stale.

## Proposed remediation and acceptance criteria

In a separately authorized Framework task, update only the PCRE2 test fixture to model the smallest valid approved V3 source topology required by the current guard. Do not change, relax, or mock away `ci_require_approved_modsecurity_v3_checkout`.

1. The fixture includes a non-symlink `.gitmodules` manifest and required mocked topology/Git behavior.
2. Each invalid PCRE2 digest again exits `77` because of the digest verifier and proves the archive never reaches tar.
3. The matching digest control reaches the local PCRE2 archive-extraction marker and completes its expected path.
4. Focused PCRE2 archive-digest and V3 provenance regressions pass without a production guard regression.

## Validation, dependencies, blocker, and residual risk

Before any Framework write, read the active Framework instructions and create a separate Framework delivery plan. Then run `tests/security_regression/test_pcre2_archive_digest.py` and `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py`, review the exact Framework PR head, and use the Framework's protected delivery lifecycle if the user authorizes one.

Dependencies are `FND-FRAMEWORK-0030` and `FND-FRAMEWORK-0005`; related records are those two findings and `FND-PARENT-0053`. This is not a duplicate of `FND-FRAMEWORK-0030`, which owns the former production-guard false rejection of the real approved recursive topology. The current correction is blocked from this Parent task by the need for separate Framework-scoped authorization and delivery lifecycle.

The real V3 guard remains fail-closed. The residual risk is lost dynamic PCRE2 regression coverage until a separately authorized fixture correction is verified; no risk is accepted.

## History

- 2026-07-26 — Reproduced three focused tests with five failures before the intended digest verifier because the synthetic V3 source lacks `.gitmodules`.
- 2026-07-26 — Deduplicated from `FND-FRAMEWORK-0030`; this is a separate stale fixture contract, not a reason to weaken the production topology guard.
- 2026-07-26 — `remediation_fixed` and `resulting_master_verified_and_closed`: Framework PR #50 updated only the PCRE2 fixture contract. Exact Framework master `de705a5efb872f95f010346fe2e6143c88876ad4` passed all 3 PCRE2 archive-digest and all 18 V3 provenance tests; the production guard remains fail-closed. Receipt: `.codex/runs/20260726T160903Z-framework-pr50-pr51-master-verification/finding-closure-evidence.md` (SHA-256 `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`).
