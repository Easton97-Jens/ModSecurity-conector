# Change Record: CR-20261024-pr410-sonar-remediation

**Language:** English | [Deutsch](CR-20261024-pr410-sonar-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261024-pr410-sonar-remediation |
| Date (UTC) | 2026-10-24 |
| Base revision | `e509db65601057154c184757e2632e65b9dad403` |
| Final repair start | `a1edb5c9b3722eec8c6911345d3315dd82eb145a` |

## Motivation and problem statement

PR #410 retained one Sonar vulnerability, twelve smells, local lifecycle
failures and Apache CI fixture errors. Its accumulated documentation and report
history also obscured the current review surface. After the prior remediation,
one MINOR smell and one local Apache guard ERROR with one dependent NOT_REACHED
case remained for this final targeted repair.

## Acceptance criteria

Repair the identified causes without weaker controls; run one predeclared
selection of at most 100 active scenarios with no retry; reduce the actual PR
diff; preserve Framework/MRTS; publish only truthful exact-head evidence.

## Implementation decision and rationale

Private HAProxy capture output now uses a fixed external boundary, trusted
ancestors, an exclusive 0700 leaf and descriptor-backed 0600 receipts. Focused
refactors remove the twelve smell causes. Test roots and SDK include selection
are corrected at their owners. Historical prose/results are externally archived
instead of retained in the PR. The earlier repair used a behavior-equivalent
dictionary comprehension, which triggered a different Sonar rule. The Apache guard copies the exact registry-hash-bound
Framework case into its private test root; production path admission is unchanged,
and negative assertions now identify their intended rejection branches.

## Changed files

The focused changes cover the HAProxy capture helper, Envoy/Apache/Traefik
harness controls, native observer tests, the Apache C probe, concise EN/DE docs,
and one Change Record. The final repair additionally changes only
`connectors/apache/harness/apache_oracle_overrides.py`,
`tests/test_apache_header_semantics.py`, this concise EN/DE closeout pair and this
Change Record pair. Ten machine-consumed report inputs remain unchanged from the
integrated PR content.

## Commands executed

RTK wrapped Git inspection, Python compilation, Go formatting/listing, C17
syntax checking, JSON/shell preflight, the single coordinated closeout runner,
and documentation/diff checks. The final repair used RTK-wrapped Sonar readback,
Python compilation, JSON/shell/hash/count preflight and exactly one four-method
unittest invocation through
`rtk bash /var/tmp/codex/ModSecurity-conector/pr410-last-repair-20261024/run-closeout.sh`.
No unwrapped fallback was used.

## Security impact

The plausible public-temp-output path is closed without an exclusion or
suppression. Focused static review found no actionable regression. No deep scan,
policy weakening, secret handling change, or new trust root was introduced. The
final test fixture remains under a private test-owned root and validates the real
Framework bytes against the existing registry SHA before use.

## Runtime evidence

The earlier retained run remains 73/75 PASS with one ERROR and one NOT_REACHED.
The separately authorized final repair run
`pr410-last-repair-20261024-final-001` bound starting head
`a1edb5c9b3722eec8c6911345d3315dd82eb145a` to executable patch SHA-256
`2e3681297d924921b82449b82da7675ce4dee0f35d3f968989af0401ec683057`.
All four methods / 13 expanded active scenarios passed, with zero retries. Result
SHA-256: `f6d02a742713a9d1ec8cab5e399cdb52b32e198b798eaae00795940c20ec0fbf`.

## Known limitations

The final targeted local aggregate is `PASS`. This is not full I12/V08–V10 host
acceptance and does not establish repository-wide default-suite cap enforcement.
`verified_pr` still depends on automatic exact-head CI/Sonar and review readback.

## Remaining risks

Automatic final-head CI/Sonar may expose environment-specific or scanner
results. Complete host/protocol and blocked deployment evidence remains outside
this reduced closeout.

## Checks not run and rationale

In the earlier repair run, no second final-repair run, historical matrix, Oracle
campaign, deep security scan, release, deployment or merge was run. Retry count is zero; provider checks
start only from the pushed final head.

## Final diff and review status

Independent static reviews found no source regression after the documentation
corrections. Against the actual PR base, the docs/report portion is reduced
from 193 to 25 changed files. The final targeted local run passes; the PR remains
Draft while automatic exact-head verification is pending.

## Authorized integration follow-up

Starting at `11324289a724b61ab2279f56c16e9185e240ccc9`, replace the redundant
generator/identity-comprehension pair with an explicit parsing loop in
`connectors/apache/harness/apache_oracle_overrides.py`. Full `S7494` and `S7500`
messages were read; first-`=` splitting, duplicate-key precedence and malformed
line rejection are preserved. No suppression, rule exclusion or admission change.
The same four guard methods / 13 expanded scenarios passed once in 0.759 seconds
through the RTK-wrapped Parent interpreter (3.14.4). Selection preflight confirms
that these 13 scenarios are a subset of the existing 75-case inventory.
The task-owned command, selection, patch digest and result are retained at
`/var/tmp/codex/ModSecurity-conector/runs/pr382-integrate410-20261024`.
Hosted Python3.14.7 checks and exact-head Sonar remain separate evidence.
Existing historical results keep their original revision bindings.

The published Apache repair `525d3e5e8a0788c46455b0cab4cd775f2190a325` exposed
`TestMiddlewareCancellationAfterClaimSendsBoundedCancel` failing in hosted
Go1.27.2 (job `120833096999`). A CLAIM cancellation watcher could outlive
`session.exchange` and poison the subsequent CANCEL deadline. The correction in
`observer.go` joins the watcher before unlocking. The new deterministic
`TestSessionExchangeJoinsCanceledDeadlineWriter` fails at its intended assertion
on the original source and passes with the fix; the existing CANCEL case also
passes (two selected unit scenarios, no retries, local Go1.27.3).
Commands, baseline/fixed logs and source digests are retained in the same task
run root. `observer_test.go` adds this regression without removing assertions.
Source head `3d5095e3561df29a217537ab500ce8595e1a5067` subsequently passed
26 checks with two conditional skips. Sonar analysis
`32cca90c-523f-4810-9941-5cfe37314c15` is terminal SUCCESS, Gate OK with zero
open/accepted issues, hotspots and new duplication.

## Joint PR #382 repair and acceptance

Integration uses normal merge commits `86101a0c` and `bba093f5`; original source
`11324289` and updated source `3d5095e3` are ancestors. Master-rule revision
`42fd5a8e` is retained. Framework `99a7985c` and MRTS `8a6bb546` repositories
and gitlinks remain unchanged. The source PR's 25-file docs/report reduction and
machine-consumed inputs remain intact.

The #382 baseline has 95 open findings (two Reliability bugs and 93 smells),
no accepted issues or hotspots, and duplication in four files. Changes cover
Common/NGINX/HAProxy/Traefik source, C fixtures, current-source extraction
dependencies and shared lifecycle stubs. They preserve public APIs, all existing
scenario variants, cleanup ownership, first-error precedence and assertions.
The real Traefik lock-duration defect has a deterministic failing old-source
control; descriptor snapshots and allocation-free expiry cleanup now pass their
focused controls. An independent review caught and removed an intermediate
fd-exhaustion cleanup risk before publication.

The coordinated selection is 100 expanded unit/native/contract scenarios:
Apache13, Traefik native20, HAProxy22, Common9, NGINX10, trusted HTTP12,
native telemetry7, cancellation2, Go provenance4 and scanner control1.
Local result: 98 PASS, no FAIL/ERROR, two foreign UID/GID controls blocked by
the host's `0 0 1` user/group mappings. Their exact Hosted-CI native tests reject
skips; the test child uses the selected interpreter. No connector E2E case or
historical I12 execution was added. Unselected historical cases keep their old
results/revisions; global E2E-cap enforcement remains unproven.

Gitleaks initially found 1,017 immutable prose/hash false positives across the
combined history. Per-finding classification includes source-line/blob digests,
typed consumers and 903 recomputed original source-file digests. The sanitized
triage has zero unresolved items. `.gitleaksignore` contains only exact immutable
fingerprints; all default rules, redaction and the full PR range remain active.
The 253-commit integration scan passes; a new-commit synthetic control remains
detected. This is a proven false-positive disposition, not risk acceptance.

RTK-wrapped checks include the frozen selector/preflight and focused dispatcher,
negative old-source controls, native C17/Wextra/Werror compilation, native
NGINX compile, Go build/test compilation/gofmt, full-range Gitleaks and its
negative control, workflow lint, and paired-document/link/diff validation.
Local Python3.14.4/Go1.27.3 and hosted Python3.14.7/Go1.27.2 remain distinct.
Run evidence, exact commands, digests, skips and publication/readback facts are
retained under `/var/tmp/codex/ModSecurity-conector/runs/pr382-integrate410-20261024`.
Current shared-head CI, Sonar processing/gates and reviews are evaluated at the
published #382 head; source #410's green result does not transfer automatically.
Coverage import and runtime/lifecycle acceptance are separate from these tests.
No master integration, release, deployment or historical qualification is granted.

## Joint Sonar and maintenance follow-up

GitHub records #410 closed/merged at `bba093f5`. Joint head `23c583d8` has
41 successful checks, five conditional skips and two failures sharing Sonar's
99-finding inventory. Go test files were incorrectly MAIN/FIL: `*_test.go` now
remains analyzed as TEST, with production source unchanged. Independent review
validated the permission-rejection and in-memory HTTP test candidates as
non-vulnerable test controls; no provider false-positive marking was used.
Top-level C includes with macro-aware prototypes, two const declarations, Go
parameter grouping and an accurate mutable-error fixture address the small
remaining causes. The 12 trusted-HTTP and three MSE1 unit variants pass using
the isolated, official-checksum-verified Python 3.15.1 runtime.

The user expanded this task to Go 1.27.3, Python 3.15.1, all current Actions and
failed update workflows. All ten external Actions were checked against official
releases and immutable tag commits; setup-python, create-github-app-token and
CodeQL advance, without changed Node runtime or used input contracts. Build
toolchain selectors use `.go-version`; module language minima remain unchanged.
The Go updater's failed old-master socket fixture is already repaired by
`91722137`; two targeted controls pass on Go 1.27.3. Python's static inventory,
setup verification and recognition of fixed self-repository reusable calls are repaired. The protected
lighttpd namespace retains its root-owned system interpreter under its complete
dedicated trust contract. Normal jobs use canonical Python. Action contracts now
read the central lock instead of rejecting valid future candidates via old pins.
Fourteen focused updater controls pass; the metadata publisher-step separation
recheck also passes after the second rate-limit path was corrected.

GitHub metadata authorization is confined to the two fixed-origin resolver
steps; redirects are rejected before credentials can be forwarded, error text
is sanitized, and artifact/Git/PR operations retain their own credentials.
The user explicitly authorized the narrowly hash-bound official PyYAML 6.0.3
source build needed for Python 3.15. Parent owns that runtime artifact; the two
Parent consumers verify the pinned Framework's same dependency version without
altering Framework source, locks or gitlinks. This is no Framework certification.
Initial local 100-case results remain revision-bound; follow-up unit controls
are separately recorded. Existing scaffold CI executed 583 methods in 14 batches
(one SDK class skipped), exceeding the initial 494-method lower bound. New
connector E2E cases remain zero. Live default-branch updater publication is not
executed by this PR task; it requires later trusted master integration/run.
Final exact-head CI/Sonar/review facts remain in the external task evidence and
the current PR checks, without importing #410's earlier green result.

On the isolated Python 3.15.1 environment, the final language selection passes
55 expanded unit variants; the installer passes 20 distinct unit controls.
The first real source build/install, safe mapping load and unknown-tag rejection
all pass, as does `pip check`. The resulting pure wheel has SHA-256
`779a6918447c67ec85d3862ccf51dc57b3ba665c0a50f2955bab850b75c0fc43`;
the official source and all three build-tool digests are retained in the receipt.
The Python updater's candidate-installation contract also passes. These are
separate follow-ups, with their original attempts and source bindings retained.
The real copied-tree maintenance baseline also passes on Python 3.15.1:
311 unit methods, 305 passed and six environment/snapshot skips, no failures.
The skipped controls remain explicit; no connector E2E or host proof is inferred.
