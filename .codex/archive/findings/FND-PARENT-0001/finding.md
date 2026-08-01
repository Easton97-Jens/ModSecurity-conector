# FND-PARENT-0001 — Go advisory results require a supported patched Go line decision

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0001` |
| Title / Titel | `Go advisory results require a supported patched Go line decision` |
| Category / Kategorie | `dependency_risk` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P1` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `validated` |
| Status | `closed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Resulting-master OSV workflow run 29783388062 reports 15 unknown vulnerabilities across the Envoy and Traefik Go modules; the 18 Go 1.24.13-compatible occurrences are absent from this result, while every remaining occurrence requires Go 1.25.8 or later and remains decision-gated.

## Observed behavior / Beobachtetes Verhalten

PR #71 head b1eef0a087432aa9bf9bc1243a34b0b0d8f6080e was squash-merged at 2026-07-20T22:16:36Z as master 929fe60dfca30787947027e5bd49003581a5b080, whose tree fae388da52f5d660c8e18f06b058ec67b38adfd7 equals the reviewed head tree. OSV workflow run 29783388062 completed its wrapper successfully but the scanner exited 1 and reports 15 unknown vulnerabilities; the 18 Go 1.24.13-compatible occurrences are absent and all remaining occurrences require Go 1.25.8 or later.

## Expected behavior / Erwartetes Verhalten

A supported Go 1.25.8-or-later compatibility and dependency decision must be made and validated before this validated P1 release blocker can advance.

## Impact / Auswirkung

The validated P1 release blocker remains: 15 scanner-reported unknown vulnerabilities cannot be given a supported disposition without the Go 1.25.8-or-later decision.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `Envoy Go module`
- `Traefik Go module`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '83,86p;216p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:83-86,216-216`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '83,86p;216p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The current reconciliation supersedes the historical baseline above: the Go 1.24.13 change removed the 18 compatible scanner occurrences, but every remaining occurrence requires Go 1.25.8 or later; no product-code root cause is claimed.

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Make an explicit supported Go 1.25.8-or-later compatibility decision, update dependencies only within that decision, and rerun the exact OSV scan plus module tests.

Select a supported fixed Go patch line applicable to the reported advisories and rerun govulncheck plus module tests.

## Acceptance criteria / Akzeptanzkriterien

- A supported Go patch line covers the retained advisory IDs or each remaining item has an explicit supported disposition.
- govulncheck result data and Go tests are retained for the exact toolchain.

## Validation plan / Validierungsplan

- Run govulncheck for Envoy and Traefik with the selected Go version.
- Run go test ./..., go vet ./..., and their legitimate controls.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-PARENT-0003`

## Residual risk / Restrisiko

All 15 remaining scanner-reported vulnerabilities remain open and decision-gated; no risk has been accepted by the current user.

## Resulting Parent master reconciliation after PR #71 / Abgleich des resultierenden Parent-Masters nach PR #71

The retained resulting-master receipt records that PR #71 head b1eef0a087432aa9bf9bc1243a34b0b0d8f6080e was squash-merged at 2026-07-20T22:16:36Z as master 929fe60dfca30787947027e5bd49003581a5b080 and that both trees equal fae388da52f5d660c8e18f06b058ec67b38adfd7. OSV workflow run 29783388062 had advisory-wrapper success, scanner exit 1, and 15 unknown vulnerabilities. The 18 Go 1.24.13-compatible rows are absent from the scanner result; all remaining occurrences require Go 1.25.8 or later and remain decision-gated. Status remains validated and priority remains P1; no risk acceptance, verification, or closure is claimed.

Evidence artifact: /var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/resulting-master-go12413-delivery-and-scan-reconciliation-20260720T221900Z.json. SHA-256: f8e8fa49a9aa8639b61946b49fca49bc0fc06623a80554f4145f78ade6ad71b2. Producer command: RTK-proxied exact resulting-master PR #71 delivery, OSV, secret-wrapper, GitHub security, and SonarQube Cloud reconciliation after squash merge.

## History / Historie

- 2026-07-20T22:19:00Z: post_pr71_resulting_master_osv_reconciled — Resulting-master receipt added; P1 validated status retained, with no verification, closure, or risk acceptance.
- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.

## Current reconciliation — 2026-07-23

This section supersedes the historic Go-1.24 compatibility premise for the
current alert decision. Current master
`a308d7b414f0859490fe7253e0683a4bde80b563` declares Go `1.26.5` for the
Envoy ext_proc module. Its two current Dependabot alerts are independently
confirmed open:

- `golang.org/x/net v0.48.0` (alert #1) is below Dependabot's `v0.55.0`
  advisory fix. The current official OSV response additionally identifies nine
  vulnerable `x/net` IDs; the smallest complete module version is `v0.56.0`.
- Direct runtime `google.golang.org/grpc v1.79.3` (alert #2) is below the
  official OSV/Dependabot fix `v1.82.1`.

Both candidate module releases declare Go `1.25.0`, so the repository's
already-declared Go `1.26.5` baseline is compatible. Local validation cannot
yet start: the installed Go `1.26.0` executable correctly refuses the module
with `GOTOOLCHAIN=local`, and no local `go1.26.5` toolchain exists. The policy
prohibits an implicit download, so explicit current-user authorization is
required for an isolated official Go `1.26.5` acquisition/use in the registered
task cache. No dependency mutation, alert closure, risk acceptance, or
verification occurred.

Retained current evidence:

- gRPC OSV response:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/go/05-osv-grpc-v1.79.3.json`
  (SHA-256 `801a60594f60869ee48033d8bf7d9ad1248c3964752d10b19b143f0e158a4d61`).
- x/net OSV response:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/go/06-osv-x-net-v0.48.0.json`
  (SHA-256 `b8f11f2a4b68c905d803f0d23e32666866935fe5a09a905518ed425841ec0a18`).
## Draft-PR remediation update — 2026-07-23

The user approved an official Go 1.26.5 side-by-side toolchain inside the
registered task run only. Its verified archive SHA-256 is
5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053; it did
not alter the host/system toolchain or the repository Go baseline.

Draft PR [#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99)
at exact head 2f0d8a234f984b731229aca01d43caf2749a7d61 selects gRPC v1.82.1,
x/net v0.56.0, x/sys v0.46.0, and x/text v0.39.0. Resolver/tidy/verify, test,
vet, build, govulncheck, a 17-test dependency-floor contract, and all
exact-head PR checks passed. The independent scoped security review found no
reportable new finding.

The finding remains validated: current master still selects the vulnerable
versions and GitHub still reports both Dependabot alerts. The PR is open Draft
and is not authorization to merge or close an alert. The isolated worktree
runtime-config and bilingual limitations remain recorded controls rather than
failed remediation evidence.

Retained delivery evidence:
 /var/tmp/codex/ModSecurity-conector/runs/20260723T165434Z-github-alert-remediation-go1265-4fc93743/evidence/delivery/20260723-draft-pr-delivery-alert-state.md
(SHA-256 7508110eef978259f0b9757df675844535b44bd5e6a4dc30c92d265da05110de).

## Current-master verification — 2026-07-24

The historical Go-advisory condition is verified as remediated on current
Parent master `8e36b86ac17bce06003b0505fe26f6bb60c3cec7`.

- PR [#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99)
  was merged from exact head
  `2f0d8a234f984b731229aca01d43caf2749a7d61` as
  `5b8db00d44ab24f3a9f4216a00f7edee977b6898`; its exact-head checks were 33
  successful and six scope-appropriate skips.
- PR [#100](https://github.com/Easton97-Jens/ModSecurity-conector/pull/100)
  was merged from exact head
  `dace5ca118a89a91c33fde952a6282f9c391ee10` as
  `6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d`; its exact-head checks were also
  33 successful and six scope-appropriate skips.
- GitHub independently reports Dependabot #1 (`golang.org/x/net`) and #2
  (`google.golang.org/grpc`) as `fixed` at `2026-07-23T20:14:31Z`, with
  `dismissed_at = null`; the current open-Dependabot inventory is empty.
  Current master selects `x/net v0.56.0` and `grpc v1.82.1`.
- Using the retained official task-local `go1.26.5 linux/amd64` toolchain with
  task-owned caches, Envoy and Traefik `go test ./...` and `go vet ./...`
  passed. Both `govulncheck -show verbose ./...` runs reported `No
  vulnerabilities found.` The bounded current-master Traefik fuzz control also
  passed (99,749 executions in 15 seconds, one worker).

This establishes the original reproduction is no longer present while the
legitimate module/test controls remain functional. The separate current
Scorecard alerts, including its PyYAML report, are not part of this Go finding
and remain tracked by `FND-GITHUB-0001`; none was dismissed or risk-accepted.

Retained evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/github-alert-closure-verification.md`
(SHA-256 `20ea82fbd04cc7ea672a644c4c5c5621b38b6fc29ce76ed9c54f028ca458afdf`).

## History update — 2026-07-24

- `2026-07-24T15:39:43Z`: `current_master_go_dependency_remediation_verified`
  — merged-master Dependabot re-evaluation, selected-toolchain tests, vet,
  govulncheck, and the bounded fuzz control passed. The finding transitions
  from `validated` to `verified`; its lifecycle close follows only after
  EN/DE/JSON parity validation.

## Closure — 2026-07-24

At `2026-07-24T15:43:59Z`, the English/German/JSON record parity and retained
evidence checksum were validated. The finding transitions from `verified` to
`closed`: current master no longer reproduces the original Go dependency
condition, the legitimate controls pass, and GitHub independently reports both
scoped Dependabot alerts fixed without manual dismissal. The active Scorecard
alerts remain outside this finding and stay tracked by `FND-GITHUB-0001`.

## Post-closure authoritative master recheck — 2026-07-24

After the closure evidence was retained, the authoritative Parent `master`
advanced by one commit from `8e36b86ac17bce06003b0505fe26f6bb60c3cec7` to
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0`. The GitHub comparison contains
only the bilingual Change Record/index and
`tests/test_full_lifecycle_evidence.py`; it does not change either affected Go
module or the Traefik `FuzzUDSFrameAndResult` target. A fresh authoritative
read still shows Dependabot #1/#2 as `fixed`, `dismissed_at = null`, and no
open Dependabot alerts. All 14 observed current-master push workflows are
successful. The original condition therefore remains non-reproducible and the
closed disposition remains current.

Retained recheck evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-advance-recheck.md`
(SHA-256 `c099c32564c1a78e60f98a61ba350904669d9c7231459c4109587088e31f915f`).

- `2026-07-24T15:55:37Z`: `post_closure_authoritative_master_rechecked` —
  one documentation/test-only master advance was compared and the relevant Go
  remediation, authoritative Dependabot state, and successful workflow set
  remained unchanged.

## Second post-closure authoritative master recheck — 2026-07-24

Parent `master` then advanced one further commit to
`185fd358bcfabe63464ab0e135eecedf24c9a699`. Its comparison from
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` changes only a bilingual Change
Record/index and `tests/test_full_lifecycle_profiles.py`; it does not change
the affected Envoy Go modules or the Traefik `FuzzUDSFrameAndResult` target.
Dependabot #1/#2 remain `fixed` with `dismissed_at = null`, and the open
Dependabot inventory remains empty.

The new master has 14 completed push-workflow runs: 13 successes and one
failed OpenSSF Scorecard run (`default-branch`, run `30107490735`); its check
inventory also reports a failed SonarCloud Code Analysis check. Those external
workflow/quality states are retained under their existing GitHub/Sonar follow-
up records. They do not reintroduce the independently remediated Go dependency
condition, so this finding remains closed.

Retained second-recheck evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-second-advance-recheck.md`
(SHA-256 `17f4abdf4be2939aca498746e9e345d0e33566580adbee0b6e92427bf73b1c8b`).

- `2026-07-24T16:07:44Z`: `post_closure_second_authoritative_master_rechecked`
  — the second scope-irrelevant master advance, fixed Dependabot state, and
  current external workflow failures were recorded without reopening or
  weakening the closed Go remediation.

## Final current-master recheck after Scorecard retry — 2026-07-24

Parent `master` remains `185fd358bcfabe63464ab0e135eecedf24c9a699`; its
scoped Go-module and Traefik-fuzz-target state is unchanged. Dependabot #1/#2
remain `fixed` with `dismissed_at = null`, and the open Dependabot inventory is
empty. OpenSSF Scorecard run `30107490735`, attempt 3, succeeded at
`2026-07-24T16:14:21Z`, leaving all 14 observed GitHub Actions push workflows
successful.

GitHub has refreshed all six Scorecard alert instances to this exact current
master; they remain separately open. SonarCloud Code Analysis also remains a
failed separate check. Neither condition reintroduces the remediated Go
dependency state, so `FND-PARENT-0001` remains closed without any alert
dismissal or control weakening.

Retained final recheck evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-scorecard-retry-final-recheck.md`
(SHA-256 `2a788454ba88bcd90add62b5eae3545d83a53180f7aefe8c72ffc864a2959746`).

- `2026-07-24T16:14:53Z`: `post_closure_final_current_master_rechecked` —
  all current Actions workflows now pass after the Scorecard retry; refreshed
  Scorecard alerts and the failed SonarCloud check remain separate follow-up.
