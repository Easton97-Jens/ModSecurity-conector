# Finding FND-SONAR-0027: NGINX connector contains sixteen current SonarQube Cloud maintainability findings

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `maintainability` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `not_applicable` / `confirmed` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / candidate integration blocker / security relevant | no / no / yes |
| Sonar inventory | 3 × `c:S3776`, 1 × `c:S134`, 2 × `c:S3358`, 6 × `c:S1134`, 4 × `c:S1135` |

## Summary, behavior, and impact

At Parent master `caddd86d1eede95de53aa1bc971dd26d875df21c`, the scoped `connectors/nginx/` inventory has 16 open C code smells, zero bugs, vulnerabilities, security hotspots, and duplicate lines. The four affected sources contain over-complex lifecycle functions, nested header-list control, nested Phase-4 value selection, and non-actionable deferred-work markers.

This is not an evidenced security vulnerability, but the code handles HTTP request, response, and ModSecurity intervention state. The remediation preserves phase markers, call order, returns, event reasons, redirect/status behavior, cleanup, and metadata-only logging. Exact-head security, hosted, and Sonar evidence verified the PR result before the authorized squash merge; resulting-master workflow evidence is now bound to the actual merge revision.

## Scope, remediation, and controls

- Scope is the four Parent NGINX C sources, their direct source-contract check, bilingual Change Record, paired indexes, and local finding evidence.
- Decompose lifecycle functions, replace nested selection with explicit helpers, make header-part advance explicit, and replace stale markers with accurate lifecycle comments.
- Do not change Sonar rules, Quality Gates, exclusions, suppressions, `NOSONAR`, Framework, MRTS, Gitlinks, or a security control. A direct master change remains prohibited; the only master action was the separately authorized squash merge of this exact PR.
- Required controls are NGINX Common-adoption, C-standard wiring, C17 lint, feasible native C17 compile, focused security-diff review, and exact-head hosted Sonar verification.

## Retained evidence

Run ID: `nginx-sonar-remediation-20260730`.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `evidence/sonar-nginx-initial.md` | `315a16d71c558cfa6a87d2a4917ae31e714751f50da308f65cff7b722c2546b6` | Exact 16-key current-master NGINX inventory and zero directory bugs, vulnerabilities, hotspots, and duplicate lines. |
| `evidence/security-diff-review.md` | `f002a267559d7ad916e6e6e94ab6a08707f78944395aaa0df220b5fe3d16ce8c` | Focused security-sensitive diff review found no plausible new candidate. |
| `evidence/sonar-pr206-final.md` | `0fbddb8d4f8514f5a71054705518acf1eb1943b92f0aa12e4d5102aeedb1f0c8` | On exact Draft PR #206 head, Quality Gate `OK`, zero OPEN/CONFIRMED PR issues, zero New-Code violations, and `0.0%` / zero New-Code duplication. |
| `evidence/hosted-pr206-final.md` | `93805e39cb8561a732c73f0851b9173a7d8345706e7dea69f6bb54e80141db5e` | Exact head has 33 passed, zero failed hosted checks, zero reviews, and zero review threads. |
| `evidence/pr-206-merge-and-master-validation-20260801.md` | `0ebea887fdd26634aede6b01e9785cc156419c72b71c385378ca1ba24870a948` | Final head, protected squash result, 14 successful master workflows, separate master Sonar baseline, and retained-worktree disposition. |

The artifact is retained under `/var/tmp/codex/ModSecurity-conector/runs/nginx-sonar-remediation-20260730/`. It records no credential and changes no SonarQube Cloud status or control.

## Acceptance and disposition

All remediation acceptance criteria are verified on [PR #206](https://github.com/Easton97-Jens/ModSecurity-conector/pull/206)'s final exact head `eb1f199815b6ed3bc4ecd53bc3fd78a39629d198`: all 16 retained issue keys are absent from the PR readback; Quality Gate is `OK`; zero OPEN/CONFIRMED PR issues, zero New-Code violations, and `0.0%` / zero New-Code duplication remain; direct source controls, the focused security-diff review, and all 34 hosted checks pass. No review thread exists. GitHub squash-merged that exact PR into `master` at `e870e8fbd1a31d43156d0baa79dc6d86b4e21bd3` on `2026-08-01T07:15:29Z`; all 14 applicable master workflows then passed.

Local native C17 translation-unit compilation remains blocked because task-local NGINX/libmodsecurity header provisioning did not establish usable headers. No foreign cache or global installation is used as a substitute. This task does not claim a resulting-master NGINX runtime. The exact resulting-master Sonar analysis remains `ERROR` only on the independently tracked, project-wide `FND-SONAR-0001` baseline (New Security Rating `5`, hotspot review `0%`); it is not a PR #206 regression, and no external disposition, suppression, or risk acceptance occurred.

## History

- `2026-07-30T15:00:00Z`: source-file-keyed current-master evidence confirmed all 16 in-scope issues and allocated the distinct Parent NGINX remediation finding. No scanner configuration, PR, merge, or master change occurred.
- `2026-07-30T15:55:23Z`: Draft PR #206 exact head `9746d81cd73c54300d709357db453a93f4f358df` verified: 33 passed / zero failed hosted checks, zero reviews and review threads, SonarQube Cloud Quality Gate `OK`, zero OPEN/CONFIRMED PR issues, zero New-Code violations, and `0.0%` / zero New-Code duplication. No master integration was authorized or performed.
- `2026-08-01T07:15:29Z`: after final exact-head verification (`eb1f199815b6ed3bc4ecd53bc3fd78a39629d198`, 34 passed / zero failed checks, no review threads, PR Quality Gate `OK`), the user-authorized squash merge produced Parent master `e870e8fbd1a31d43156d0baa79dc6d86b4e21bd3`. All 14 master workflows passed. The analysis for that exact master revision still reports the pre-existing `FND-SONAR-0001` Quality-Gate baseline, not a PR #206 new issue.
