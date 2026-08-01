# Finding FND-SONAR-0028: Common runtime contains eighteen current SonarQube Cloud maintainability findings

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `maintainability` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `not_applicable` / `confirmed` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / candidate integration blocker / security relevant | no / no / yes |
| Sonar inventory | Initial: 1 × `c:S1820`, 1 × `c:S107`, 2 × `c:S995`, 10 × `c:S5350`, 3 × `c:S3776`, 1 × `c:S1912`; final resulting master: zero retained findings. |

## Summary, behavior, and impact

At Parent master `979e50b9d7d9a914e102465814e7f2fd4cd853eb`, the scoped
`common/runtime/` inventory had 18 open C code smells, zero bugs,
vulnerabilities, security hotspots, and duplicate lines. The runtime combined
configuration dispatch, lifecycle validation, decision-event serialization, and
transaction start work in a small number of long functions. It also represented
cohesive private transaction data as many independent fields and used mutable
pointers for read-only HTTP parsing.

PR #216 was then normal-merged as Parent master
`63f6baed5ea6f650aeb5372e148b32aa062a326b`, with a tree identical to its
reviewed final head `2c49e0de7aa163252e2105a916c3bfca530cc1a7`. The PR has
Quality Gate `OK`, zero new issues, zero new violations, and `0.0%` / zero
New-Code duplication. However, a direct resulting-master query still finds
historical issue `AZ9MwjLo-bUaKQ_zSGBC` (`c:S3776`) in
`load_runtime_config`; its creation and last-update dates precede this task.
That issue is not new PR code, but it means the initial 18-finding scope is not
yet completely remediated.

This is not an evidenced security vulnerability. However, the code handles HTTP
input and ModSecurity enforcement state, so the remediation is subject to a
complete security-diff review and exact-head hosted verification.

## Scope, remediation, and controls

- Scope is the two listed Parent Common Runtime C sources, their direct SDK
  source-contract control, bilingual Change Record, paired indexes, and local
  finding evidence.
- The C17-compatible remediation groups cohesive private state, extracts
  narrowly named lifecycle helpers, and makes read-only parsing const-correct.
- Configuration semantics, body limits, native phase order, request/response
  enforcement, event fields, integrity chaining, and HTTP parsing behavior
  remain unchanged.
- Sonar rules, Quality Gates, exclusions, suppressions, `NOSONAR`, Framework,
  MRTS, Gitlinks, master, and security controls are outside scope and unchanged.

## Retained evidence

Run ID: `common-runtime-sonar-maintainability-20260801`.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `evidence/sonar-current-runtime-inventory.md` | `b955ad65a2e36748344a39362178a2e46fd72297b7d18a1ddf55d42b0b6c962f` | 18 current open code smells; zero directory bugs, vulnerabilities, hotspots, and duplicate lines. |
| `security-diff-scan/report.md` | `72989b19f803956b284f04ce8fc24b6bb52f95d7413ddbeed26cdd226c10d01d` | Complete source and direct-control coverage; no reportable diff-induced security finding. |
| `security-diff-scan-amendment/report.md` | `a061e8aa74e838e2bbc9e7450b794f1944edf5ff9110d4c70f6bca6d87e4d8ea` | Final const-correctness delta reduces write capability and has no reportable security finding. |
| `evidence/pr-216-exact-head-verification.md` | `36f9d8c1584b3e3f6506f2ca147829164ddb8b6720fbf355ad416f1659cd6185` | Exact Draft PR #216 head: Quality Gate OK, zero PR issues/new violations/duplicate lines, 0.0% duplication, 33 passed checks. |
| `evidence/pr-216-merge-master-verification.md` | `f3ba578d29e255b93342d79d6faaead84a49e66dc4a767f53d865d5b4ed34661` | Final PR head has 33 successes / six scoped skips; normal merge has an identical tree, 14 successful exact-master workflows, and one retained historical `c:S3776` source issue. |
| `../../runs/parent-common-sonar-remediation-20260801/evidence/pr221-exact-head-verification.md` | `3420784833530d12802cebd9f98825eaa8e3cd45f584b6502ff3c22269db7efb` | Exact Draft PR #221 head has zero open PR issues/new violations, `0.0%` New-Code duplication, all applicable hosted checks passed, and a complete security-diff review with zero findings. |
| `../../runs/parent-common-sonar-remediation-20260801/evidence/pr221-merge-master-verification.md` | `c852730b467d505652414dd68124de553991efe9c46a8a67b45fbe9c1b014f17` | Exact PR #221 head normal-merged as `3270ab5…`; all 14 master workflows succeed and the original `c:S3776` is `FIXED/CLOSED`. |

The retained artifacts live below
`/var/tmp/codex/ModSecurity-conector/runs/common-runtime-sonar-maintainability-20260801/`.
They retain no credential and do not alter any scanner control.

## Acceptance and current disposition

The focused local C17, contract, security, memory-safety, flow-integrity, and
HTTP-authorization controls pass. On final [PR #216](https://github.com/Easton97-Jens/ModSecurity-conector/pull/216)
head `2c49e0de7aa163252e2105a916c3bfca530cc1a7`, SonarQube Cloud reports
Quality Gate `OK`, zero OPEN/CONFIRMED PR issues, zero new violations, and
`0.0%` / zero New-Code duplication. Its 39 terminal GitHub check-runs are 33
successes and six scoped skips, with zero failures. The normal merge's
resulting-master tree is identical and all 14 master-SHA workflows succeed.

GitHub normal-merged [PR #221](https://github.com/Easton97-Jens/ModSecurity-conector/pull/221)
at its exact reviewed head `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d`, producing
Parent master `3270ab5bdcc86ddab50e9be00db7611aae7fd937` at
`2026-08-01T13:36:33Z`. All 14 push workflows for that exact master revision
completed successfully. The direct resulting-master SonarQube Cloud recheck at
`2026-08-01T13:39:56Z` reports original issue
`AZ9MwjLo-bUaKQ_zSGBC` as `FIXED/CLOSED` at `2026-08-01T13:37:19Z`.

The finding is therefore `verified`. The global master Quality Gate remains
`ERROR` because the separate `FND-SONAR-0001` new-security-rating baseline is
still `5`; no Sonar policy or security control changed here.

## History

- `2026-08-01T10:12:24Z`: retained current-master evidence confirmed the 18
  coherent in-scope maintainability findings and allocated this Parent finding.
  Remediation and local validation began; no scanner policy, PR, merge, or
  master state changed.
- `2026-08-01T10:29:10Z`: exact Draft PR #216 head
  `ad2f8e9a90af8981c060fe025b8ef5705556b9cf` verified for the task scope:
  33 passed / zero failed terminal GitHub checks, SonarQube Cloud Quality Gate
  `OK`, zero OPEN/CONFIRMED PR issues, zero new violations, and `0.0%` / zero
  New-Code duplication. The no-write `header_end` const amendment cleared the
  sole transient `c:S5350` result. No merge or master action occurred.
- `2026-08-01T11:01:02Z`: PR #216 normal-merged as Parent master
  `63f6baed5ea6f650aeb5372e148b32aa062a326b`; its tree is identical to final
  head `2c49e0de7aa163252e2105a916c3bfca530cc1a7`, and all 14 master-SHA
  workflows succeeded. The PR's zero-new Sonar result remains valid, but the
  direct resulting-master source query retains historical
  `AZ9MwjLo-bUaKQ_zSGBC` / `c:S3776` in `load_runtime_config`, so the finding
  remains in progress. The unrelated global Quality-Gate security rating is
  retained under `FND-SONAR-0001`.
- `2026-08-01T13:12:18Z`: exact Draft PR #221 head
  `482ba035ed53b3668009b7158c656214d6924e6f` extracts the retained parser
  without changing its validation or close contracts. Applicable hosted checks
  passed; SonarQube Cloud reports zero open PR issues, zero new violations, and
  `0.0%` New-Code duplication; the complete security-diff review has zero
  reportable findings. The finding is `fixed`, pending an authorized merge and
  resulting-master reproduction before `verified` or `closed`.
- `2026-08-01T13:39:56Z`: GitHub normal-merged exact PR #221 head
  `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d` as resulting master
  `3270ab5bdcc86ddab50e9be00db7611aae7fd937`; all 14 exact-master workflows
  succeeded. The direct SonarQube Cloud recheck records original
  `AZ9MwjLo-bUaKQ_zSGBC` / `c:S3776` as `FIXED/CLOSED` at
  `2026-08-01T13:37:19Z`. The finding is `verified`; the unrelated global
  Quality-Gate security-rating baseline remains under `FND-SONAR-0001`.
