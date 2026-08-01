# FND-GITHUB-0003 — Framework CodeQL clear-text logging alert #1 is a static checker false positive

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-GITHUB-0003` |
| Category | `static_analysis_finding` |
| Repository | `framework` |
| Ownership | `external_tool` |
| Priority | `P2` |
| Severity | `not_applicable` |
| Confidence | `validated` |
| Status | `not_applicable` |
| Release blocker | `false` |
| Security relevance | `true` |

## Summary

After PR #23 merged, GitHub CodeQL opened High-severity alert #1 (`py/clear-text-logging-sensitive-data`) on Framework master commit `e482549b93d95ba85830a208e99a2ba0331ec351`. Exact source-to-sink triage proves that CodeQL follows the static detector-pattern list at line 8 into the error printer at line 32. The checker reads fixtures only for predicates and never prints a fixture match or file content: its diagnostic strings contain only fixed required paths, fixed phrases, detector-pattern literals, or allow-listed field names. The alert was authoritatively dismissed as `false positive`; no Framework source, Parent gitlink, MRTS state, PR, permission, or branch-protection change was made.

## Observed and expected behavior

Immediately before the authorized PATCH, GitHub showed alert #1 as open on exact master `e482549b93d95ba85830a208e99a2ba0331ec351`, with source `ci/checks/security/check-security-data-flow-cases.py:8:17-8:102` and sink `:32:15-32:32`. Static inspection of identical blob `8d8e273d48bd4cfcd6b59fff99222cb5df12f217` shows `text = p.read_text()` influences only boolean validations. All `errors.append(...)` values are built from a fixed path, a fixed phrase, a detector-pattern literal, or an allow-listed field name. The only sink prints `"\\n".join(errors)` to stderr. GitHub immediately read back state `dismissed`, reason `false positive`, and `fixed_at: null`.

The checker may identify an invalid fixture without writing fixture content, matched secret material, request bodies, or credentials to CI output. CodeQL findings remain open unless an exact current source-to-sink analysis establishes a non-exploitable false positive or a fix is verified.

## Impact and root-cause analysis

No clear-text credential or sensitive fixture content reaches the reported sink in the scoped source. A source-code change to silence the alert would not improve the control and could weaken its diagnostics. The evidence-backed GitHub disposition removes this scanner-only master-integration blocker; the independent master SonarQube blocker remains unchanged.

CodeQL's generic clear-text logging query treats the fixed detector-pattern list as sensitive data when the checker incorporates the currently selected pattern into a static validation diagnostic. The query does not distinguish a pattern literal from a matched credential and does not model that the fixture text is never emitted.

## Affected files and symbols

- `ci/checks/security/check-security-data-flow-cases.py:8`
- `ci/checks/security/check-security-data-flow-cases.py:18-32`
- `Makefile:116,124-125`
- `py/clear-text-logging-sensitive-data`, `SECRET_PATTERNS`, `errors`, `check-security-data-flow-cases`, GitHub Code Scanning alert #1

## Preconditions and reproduction

- Source blob: `8d8e273d48bd4cfcd6b59fff99222cb5df12f217`; master: `e482549b93d95ba85830a208e99a2ba0331ec351`.
- Source remains line 8 and the reported sink remains line 32 of `ci/checks/security/check-security-data-flow-cases.py`.
- The checker is a static `make lint` / `check-security-data-flow-cases` control, not a supported request-processing surface.

```text
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/code-scanning/alerts/1
rtk sed -n '1,40p' ci/checks/security/check-security-data-flow-cases.py
rtk rg -n -C 3 'check-security-data-flow-cases\.py|security-data-flow' Makefile .github ci tests --glob '!tests/mrts/**'
```

## Evidence

- Run `20260718T192214Z-framework-pr-resolution-20260718-b30403da`
  - Static triage: `/var/tmp/codex/ModSecurity-conector/runs/20260718T192214Z-framework-pr-resolution-20260718-b30403da/evidence/codeql-alert-1-triage.json`
  - SHA-256: `c8e8c052add0c6d1d54b152f2ebacf9141d1009aa0e4df8cc95636b0ef664b1b`
  - Type: `static_codeql_source_to_sink_triage`; command: GitHub alert metadata/instances plus static source and source-blob equality readback; working directory: `/var/tmp/codex/worktrees/framework-common-structure`; exit code: `0`; observed: `2026-07-18T19:42:18Z`.
- Run `20260718T192214Z-framework-pr-resolution-20260718-b30403da`
  - Dismissal receipt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T192214Z-framework-pr-resolution-20260718-b30403da/evidence/codeql-alert-1-dismissal-receipt.json`
  - SHA-256: `74882ca084034fb5f9b96949734143d7ec9f30a3927ddc5056dac186cff1f449`
  - Type: `github_code_scanning_alert_pre_patch_and_post_patch_receipt`; command: GitHub `GET/PATCH/GET` alert #1 with exact master SHA, source, and sink readback; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-18T19:45:12Z`.

## Remediation, acceptance criteria, and validation

No Framework code remediation is required. Preserve the checker and its secret-pattern control, retain the exact static triage and GitHub receipt, and dismiss alert #1 only with reason `false positive` plus the source-to-sink rationale. Reopen/retriage if the alert's analyzed SHA, source/sink coordinates, or emitted dataflow changes.

- The exact source blob and alert coordinates match the retained triage.
- Fixture text, match objects, request bodies, and credential values never enter `errors` or the printer.
- GitHub alert #1 reads back as `dismissed` with reason `false positive`, exact SHA `e482549b93d95ba85830a208e99a2ba0331ec351`, and `fixed_at: null`.
- No source, Parent gitlink, MRTS, branch, PR, permission, rule, or security-control change obtains the disposition.

For a later source change, compare SHA/source/sink to this evidence, reinspect every `errors.append(...)` and the printer, then read back the GitHub alert. The existing `make lint` invocation remains the regression control. A safe fixture set emits only the bounded count; a violation emits its fixed path and diagnostic category, not matched fixture text.

## Dependencies, blockers, related finding, and residual risk

There are no dependencies or blockers. Related finding: `FND-SONAR-0002` remains the unrelated blocked Framework master SonarQube quality-gate failure.

The scoped checker may disclose a fixed workspace path, detector-pattern literal, or allow-listed field name in CI diagnostics, but it does not disclose matched fixture content or a credential. A future code change that appends text, a match object, or an untrusted path to `errors` invalidates this disposition and requires fresh triage.

## Current GitHub reconciliation for archive — 2026-07-26

Read-only GitHub reconciliation at 2026-07-26T13:29:40Z returns Code Scanning
alert #1 as `dismissed`, reason `false positive`; its current instance remains on
the master checker path at line 32. The current Framework source still holds
SECRET_PATTERNS as a static tuple, uses fixture text only for validation
predicates, constructs diagnostics only from bounded paths, fixed phrases,
static patterns, or allow-listed field names, and prints only that bounded
diagnostic list to stderr.

No Framework source, workflow, Gitlink, Parent source, permission, or security
control was changed in this reconciliation. This remains a validated scanner
false positive, not a code fix. Its canonical status remains
`not_applicable`, and the retained EN/DE/JSON triplet is archived. Reopen and
retriage before reuse if fixture text, a match object, or an untrusted path can
reach the diagnostic list or its output sink.

## GitHub disposition and history

GitHub Code Scanning alert #1 is `dismissed` at `2026-07-18T19:45:12Z` by `Easton97-Jens`, reason `false positive`, with `fixed_at: null`. The documented dismissal comment is: `Exact master e482549b93d95ba85830a208e99a2ba0331ec351: source is a hard-coded detector-pattern list. Diagnostics emit fixed paths, pattern literals, and allow-listed names--never fixture matches or content. Static source-to-sink triage: false positive.`

- `2026-07-18T19:15:30Z` — GitHub CodeQL opened High-severity alert #1 for `py/clear-text-logging-sensitive-data` at master `e482549b93d95ba85830a208e99a2ba0331ec351`; it was a master-integration blocker pending validation.
- `2026-07-18T19:42:18Z` — Exact static source-to-sink triage found only fixed paths, phrases, detector-pattern literals, and allow-listed field names can reach the printer. Verdict: `not_actionable`, high confidence.
- `2026-07-18T19:45:12Z` — GitHub dismissed the matching open alert as `false positive`; `fixed_at` remains null. No Framework/Parent/MRTS source, gitlink, branch, PR, permission, rule, or security-control change occurred.
