# FND-PARENT-0054 — Exact PR #74 runtime matrix lacked causal hosted output

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0054 |
| Category | evidence_gap |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / validated |
| Status / feasibility | in_progress / blocked_missing_evidence |
| Release blocker / security relevant | false / true |

## Observation, impact, and evidence

At Parent PR #74 head `7238c9d0a0902affbf7dfae1d7f96d6603d80f89`, hosted run `30196090664`, job `89777788658`, passed component preparation and readiness, including the repaired PCRE2/Apache path, then failed at `make runtime-matrix-all-runtime` with `rc=2`.

Parallel matrix and dependent report/layout/lint/quick-check consumers consequently failed or became invalid, and the terminal strict evidence gate was skipped.

The outer log exposed only `$BUILD_ROOT/verified-runs/<validated-run-id>/logs/04-make-runtime-matrix-all-runtime.log`, not causal contents. Retained pre-diagnosis evidence is `.codex/runs/20260726T093511Z-pr74-runtime-matrix-blocker/evidence/hosted-runtime-matrix-failure.md` with SHA-256 `058e7f6654014df476a7ae375c1a938d1cf04ccaf5a4996884919d222c243757`.

The bounded diagnostic on the next historical exact head
`6809e348ad043bf3fcfd9b90d963882cc2fb2` exposed the cause in hosted run
`30197684223`, job `89782035387`: Apache and NGINX cache-backed refreshes
correctly rejected a mismatched owner root. That historical observability result
is retained; `FND-CROSS-0008` owns the separate remediation blocker, and no
failed evidence was accepted.

## Cause, remediation, and validation

The bounded Parent diagnostic established the matrix cause without weakening the strict producer or terminal gate. This is not a duplicate of `FND-PARENT-0053`, whose PCRE2 provenance defect no longer reproduces in the same run, nor of `FND-CROSS-0008`, which owns the Parent/Framework cache owner-root remediation.

The historical Parent-only observability remediation tailed exactly the fixed
run-ID-derived `04` matrix log only after existing run-ID validation, required a
regular non-symlink log, limited output to 300 command-shielded lines, and left
the terminal gate unchanged.

No recursion, glob, broad log search, Framework, MRTS, gitlink, or risk-acceptance action is authorized.

Focused workflow-security and documentation validation passed before publication. The fresh exact hosted producer exposed the true cause while preserving rejection. Related/dependent records are `FND-CROSS-0001`, `FND-PARENT-0053`, `FND-FRAMEWORK-0056`, and `FND-CROSS-0008`.

## History

- 2026-07-26 — Exact hosted producer passed PCRE2/Apache preparation but failed the mandatory matrix without exposing its causal fixed log.
- 2026-07-26 — The bounded next-head diagnostic exposed the cache owner-root cause; this observability finding is verified and the separate repair is tracked as `FND-CROSS-0008`.

## Current reconciliation status — 2026-08-01

The earlier proposed archival disposition is withdrawn. Although
[PR #74](https://github.com/Easton97-Jens/ModSecurity-conector/pull/74) merged
as `0b278f7ef952d5d47a2109ea265a95bf4d887772`, the only commit containing the
bounded diagnostic, `b28b8744765a2cac6e3cf91f7bd3070d49d7774d`, is **not** an
ancestor of current `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`.
The current `verified-report-governance.yml` is deliberately the lightweight
`make report-governance` path, and
`test_verified_report_governance_stays_lightweight` asserts the absence of
`verified-report-run`, the strict evidence gate, and the runtime-matrix terms.

Accordingly, historical PR checks, CodeQL, and SonarCloud evidence do not prove
a current equivalent control. This record is active as `in_progress` pending
either current exact-source evidence for an equivalent bounded fail-closed
control or an authorized, evidence-backed retirement/replacement decision. No
product workflow, Framework, MRTS, gitlink, scanner, gate, or risk control is
changed by this reconciliation; `FND-CROSS-0008` remains separately active.
