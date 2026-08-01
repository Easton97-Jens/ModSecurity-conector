# FND-PARENT-0008 — Clang Werror rejects Apache msc_config.c missing field initializer

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0008` |
| Title / Titel | `Clang Werror rejects Apache msc_config.c missing field initializer` |
| Category / Kategorie | `compiler_warning` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `fixed` |
| Feasibility status / Machbarkeitsstatus | `feasible_now` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Historical Apache C17 evidence recorded a Clang Werror missing-field-initializer
failure at the `module_directives` terminator. Exact local commit
`313cae2550bf7c8ff8eadc71065dbd617762c8cc` changes `{NULL}` to
`{ .name = NULL }`; the Parent task reports GCC and Clang compiler, structural,
fresh-DSO, and Apache legitimate controls pass. It is fixed on Draft PR #183's
exact local head only, not verified or closed.

## Observed behavior / Beobachtetes Verhalten

The historical positional `{NULL}` terminator initialized only the first
`command_rec` field. The exact committed candidate has the designated
`{ .name = NULL }` terminator and passed the reported GCC/Clang RulesSet
cleanup harnesses, lint, Apache/Common structural and C-standard wiring,
fresh materialized DSO make, HTTP/1.1 phase-2 403, and SIGUSR1 readiness.

## Expected behavior / Erwartetes Verhalten

The designated terminator must satisfy GCC and Clang C17 warning policy while
preserving normal Apache configuration and request lifecycle behavior. Exact
Draft PR #183 hosted validation and resulting-master reproduction remain due.

## Impact / Auswirkung

The local exact correction removes the recorded warning-policy failure without a
request-facing behavior change. Hosted validation, review, merge, and
resulting-master reproduction have not yet been observed.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `connectors/apache/src/msc_config.c`

### Symbols / Symbole

- `module_directives terminator`

## Preconditions / Voraussetzungen

- The approved Apache/APXS/APR/libModSecurity compiler environment is available.
- Exact Draft PR #183 head `313cae2550bf7c8ff8eadc71065dbd617762c8cc` is the current published head.

## Reproduction / Reproduktion

- Inspect the historical `{NULL}` terminator and the exact candidate's
  `{ .name = NULL }` terminator.
- Rerun GCC/Clang `make check-apache-ruleset-cleanup` and the focused controls
  on Draft PR #183 and resulting master.

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:594-613`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '594,613p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The positional `{NULL}` terminator violates the configured Clang
missing-field-initializer Werror policy. The exact candidate's designated
initializer expresses the intended terminator semantics explicitly.

## Proposed remediation / Vorgeschlagene Remediation

Retain the exact initializer correction in Draft PR #183, collect exact-head
hosted checks and review, then reproduce the original compiler condition on
resulting master before verified or closed status.

## Acceptance criteria / Akzeptanzkriterien

- Both GCC and Clang C17 builds pass with the required warning policy on the
  exact committed PR head.
- Structural, materialized-DSO, and Apache legitimate controls cover the
  affected initialization semantics.
- Hosted exact-head and resulting-master reproduction evidence exists before
  verified or closed status.

## Validation plan / Validierungsplan

- Rerun GCC and Clang compilation on Draft PR #183's exact head.
- Rerun the affected controls and original compiler condition on resulting master.

## Regression tests / Regressionstests

- `tests/test_apache_rules_set_cleanup.py` and the GCC/Clang RulesSet harness.

## Legitimate control tests / Legitime Kontrolltests

- Fresh materialized DSO, HTTP/1.1 phase-2 403, and SIGUSR1 readiness controls.

## Dependencies / Abhängigkeiten

- Draft PR #183 exact-head hosted validation and review.
- Resulting-master compiler reproduction.

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- None / Keine

## Residual risk / Restrisiko

Draft PR #183 has no observed hosted result, review, merge, or resulting-master
reproduction. The finding is fixed only; no risk is accepted.

## Current task update / Aktueller Task-Stand

Exact Draft PR #183 head `313cae2550bf7c8ff8eadc71065dbd617762c8cc` replaces the
terminator with `{ .name = NULL }` and is published as Draft PR #183. The
Parent task reports six focused Python contracts, GCC and Clang RulesSet
harnesses, lint, Apache/Common structural and C-standard wiring, fresh DSO
make, HTTP/1.1 phase-2 403, and SIGUSR1 readiness all passed on that clean
commit. No hosted result, review, merge, or resulting-master claim is made.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — Apache C17 environment prerequisites are absent; no speculative initializer patch was made.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Added the retained active-run source-preflight log to canonical evidence; `blocked_environment` is unchanged.
- `2026-07-29T10:45:45Z`: exact_commit_initializer_repair_locally_validated_and_draft_pr_published — Current Draft PR #183 head `313cae2550bf7c8ff8eadc71065dbd617762c8cc` is fixed locally; its final documentation-only follow-up leaves bounded product/test validation paths unchanged. Hosted and resulting-master evidence remain pending.
