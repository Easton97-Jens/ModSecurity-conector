# Nine-point master reconciliation

**Language:** English | [Deutsch](README.de.md)

Overall outcome: partial. Reviewable corrections are delivered independently; unresolved integrity/runtime/dependency evidence is retained below. Parent PR440 remains unmerged and no repository rule was applied. The separately maintained Framework and MRTS PRs identified below have since been integrated by other work. The configured default inventory remains exactly 100 cases. Existing checkout changes and foreign worktrees were preserved.

## Revisions and delivery

| Repository | Base | Task delivery |
| --- | --- | --- |
| Connector | 430d3194fa04ca4aafcdaef6aeb256d21dc18f0c | [PR440](https://github.com/Easton97-Jens/ModSecurity-conector/pull/440), this task branch |
| Framework | 91145b7ba721bdec4e89af754cf40bf496fd2a08 | [PR159](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/159),99e8d13cc1cf03f42cc887a4d5abf9e7c766e09b |
| MRTS | 8a6bb546c4c81d8ffc7be801dceac60c6925685f | [PR5](https://github.com/Easton97-Jens/MRTS/pull/5),bf756a403ead39863cc15a81b5608e2b6062435d |

The PR440 CI repair selects integrated Framework `03fa02bacfc327863d91723fdc77a4888a33f0a8`. It includes separately merged Framework [PR155](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/155) (`ea442`), [PR159](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/159) (`ff7cae`), [PR162](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/162) (`68ca7`), [PR158](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/158) (squash `92bd636`) and [PR163](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/163). The selected Framework pins MRTS `75394f9a687ca2f09fd7623b23ac527bba10d7d9`, which includes merged [PR5](https://github.com/Easton97-Jens/MRTS/pull/5). The table retains the original task bases and delivered heads as historical identities, not the current integrated revisions.

The repair incorporates Parent master `1a1023b92eb30ef73546cd2a2c3e84b39d34a153` into the existing PR branch without rewriting history. That master incorrectly selected PR158's pre-squash head `a26b028104b28ddd980290b5af7b3fb195c43f9a`, which is not an ancestor of current Framework master. The [reported run/job](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41470651827/job/125363368715) correctly rejects this identity. The repair changes the selected identity and generator-owned projections; the ancestry/admission guard remains intact. The selected integrated revision's candidate verifier passes; new PR-head hosted CI remains pending at this report update.

Framework master `1b0885` from [PR164](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/164) is deliberately not selected: it introduces NGINX1.31.8 while the independently checked handoff still selects1.31.6, and the candidate verifier rejects that mismatch. No Framework/MRTS source changes or competing maintenance repair are introduced here. Framework [PR157](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/157) remains closed unmerged. The separately integrated PRs above were not merged by this task.

## Requirement disposition

| Point | Status and actual evidence | Remaining boundary / next step |
| --- | --- | --- |
|1 Baseline and rules | Local Parent/Framework/MRTS status and worktrees inspected; remote refs, gitlinks and PR coordination refreshed; work isolated. Explicit local Sonar exception honored. | Preserve task branches and external evidence; no destructive cleanup. |
|2 Framework fixes/pin |Original55 pin/toolchain tests pass. CI repair now selects integrated03fa02b in Parent gitlink, versions lock and registered workflow projections; native generator check reports no changes and candidate verification passes. Merged159 includes the common.sh binding repair; merged158 supplies its separate workflow/bootstrap repair. |New PR-head hosted CI must run against this selected pair. Latest164 is excluded because its NGINX tuple conflicts with the independently checked handoff; ancestry/admission guards remain unchanged. |
|3 Traefik auth preparation | Removed Connector-local capture/manifest references use Framework source_path; split-checkout source-location regression passes through real offline admission. | Full preparation still fails Sealed Traefik profile differs;10/19 historical repository objects drifted. Keep registry/profile/export guards; obtain supported archive regeneration and reviewed source contract. No manual archive rewrite or host claim. |
|4 Inheritance and host guide | Five Parent policy bodies substantively reviewed; catalog/templates and Framework inheritance pins refreshed; Parent native inheritance validator passes. Guide records147/437 integrated and436 closed unmerged. Historical November1 receipt is present. | The original cross-repository inheritance check failed against the then-pinned children; current integrated-child qualification must be assessed separately. This task does not edit MRTS child policy digests. No fresh final-pair NGINX/Envoy host run. |
|5 Apache docs | EN/DE architecture and Apache guide now match progressive pre-EOS forwarding, commitment and engine-owned inspection limits. No product source changed. Native bilingual/link checks pass. | Documentation/source evidence only, no new runtime qualification. |
|6 Coverage/dependencies | User-selected targeted measurement delivered: real scoped Python, four Go-module and Common/gcov metrics with branches where available; source hashes/selectors/exclusions recorded. Bounded components and installed-package metadata inventory produced. x/net/html absent from real Envoy compiled graph. | Historical full Python specialist run failed after56 passes; completing or repeating it is outside the selected measurement scope. Later caller-boundary fixture repair has22 passes; generic broker module remains45/46 as an independent defect. Native tuple updates/reachability and exhaustive native/binary/container SBOM stay open. Sonar coverage exception/import unchanged. |
|7 Merge checks | Live before/after JSON and standalone additive master-only create payloads prepared; current protection preserved; events, forks, path filters, duplicate names and advisory/manual boundaries reviewed. | Proposals NOT APPLIED. Separate admin approval required; classic branch-protection reads return403. No manual host/H2/H3 campaign made required. |
|8 FIFO/setup/MRTS | FIFO import startup separated from unchanged2s operation watchdog;27 cold-cache artifact/receipt/fixture tests pass. Original Ubuntu Framework structure validator passes after ignored nonsecret local setup. MRTS exact governance suite30/30 after one-line existing-diagnostic assertion repair; all five returned PR5 checks pass. | Local Python 3.14.4 is not exact MRTS CI3.14.6 parity; GitHub governance lane supplies its own current-head result. No MRTS corpus/product edit; the Parent-selected integrated Framework carries the separately merged MRTS revision. |
|9 Verification/delivery | Separate PRs, paired records, native generators/checks and independent bounded patch review; no introduced material findings. Existing PR440 receives a regular master-to-branch integration; no direct master/main push, force-push, PR merge or protection bypass by this task. | Overall partial; current-head CI must be assessed separately and unresolved items above cannot be closed by broad green CI. |

Current local CI-repair validation: selected Framework03fa02b candidate verification passes with NGINX1.31.6; the native projection generator reports no changes; `check-python-version-contract` passes for Python3.15.1 and53 jobs;94 existing pin/toolchain/projection/candidate regressions pass (133.158s); Parent inheritance validation passes after the reviewed host-guide/catalog update. All active GitHub checks and SonarCloud for selected Framework03fa02b passed. These results do not substitute for the pending new ParentPR440-head checks.

## Actual coverage

The user explicitly selected targeted measurement with documented limitations:
116 named Python tests plus the measured four Go modules and Common/native scope.
These measurements satisfy that selected measurement deliverable. Completing or
rerunning the full977-execution specialist assessment is not a completion
criterion for this coverage scope. Its historical failure and independently
relevant defects remain recorded. Required CI gates and the default100-case
selection remain unchanged.

| Scope | Observed coverage | Meaning |
| --- | --- | --- |
| Parent Python,116 named tests |59/6552 lines(0.90%);16/2240 branches(0.71%) |33 actual Parent files; Framework code excluded, unexecuted Parent operational files retained. |
| Envoy Go |1104/3971 statements(27.80%) |Existing exact selectors, all default-build packages retained. |
| Traefik native Go |586/959 statements(61.11%) |Same scoped selection boundary. |
| Traefik composite Go |383/563 statements(68.03%) |Same scoped selection boundary. |
| Traefik observer Go |300/752 statements(39.89%) |Same scoped selection boundary. |
| Common native |2869/4290 lines(66.88%);1903/3977 branches(47.85%) |Union of real gcov observations by Parent source/line/branch across generated binaries. |

Go profiles provide statement coverage, not branch counts. No arbitrary target was added. The raw coverage run binds Parent 430d3194 and then-dirty Framework 91145 sources by recorded SHA-256; later fixture metadata changes do not retroactively qualify another pair. This closes the absence of actual scoped measurement. Broader Python execution is outside the user-selected measurement scope; host qualification and analyzer import are not established. Existing Sonar coverage exclusion remains intact.

## Validation and evidence

Machine-readable evidence and review rationale: [coverage-summary.json](coverage-summary.json), [component-inventory.json](component-inventory.json), [dependencies.md](dependencies.md), [rules-review.md](rules-review.md). German companions exist for reader-facing reports. Raw artifacts remain in the private configured run area, run master-reconcile-20261102; only bounded summaries are versioned.

### Hosted CI admission blocker

The historical exact-head snapshot [ci-admission-38ebc633.json](ci-admission-38ebc633.json) binds this investigation to Parent38ebc633 and Framework91145. All28 inspected individual failed jobs reject `modules/ModSecurity-test-Framework/ci/lib/common.sh` before the selected tests/build/runtime execute. Framework156 changed canonical Python3.14.8 to3.14.10; its inventory still expects SHA-256 `3aa782dd117fdf66194861e5a1f97e492f13321db77129da79aadcec2e655e2c` while the actual source is `8e39a221e044441e89753bfff64564579dcbc656bccf7d92368e518a2d7a59db`. Exactly one of528 bindings drifts. This is a preexisting Framework generation defect exposed by the Parent pin update; it is distinct from158. Representative immutable logs: [scaffold admission](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41426394389/job/125213928621) and [security admission](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41426394282/job/125213928012).

This snapshot is historical. The existing maintenance generator regenerated that binding in Framework159, now separately merged and included in selected Framework03fa02b. Before this repair, PR440 head b88 still exposed33 stale common.sh-binding failures plus the aggregate failure. The current repair adopts the integrated source and must requalify affected checks at its new PR head. A new failure behind admission remains possible; no new-head green CI is claimed here.

The same early stop leaves no `verified` evidence directory for Envoy/Traefik/lighttpd; their failure-receipt retention also fails. The [five-cell aggregate](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41426394445/job/125215222415) downloads only Apache's failure receipt and rejects a non-directory. These historically observed Framework error-path gaps require current-pair qualification; no successful five-cell execution is inferred. Framework159 active checks passed at624de56a and all five MRTS5 checks passed atbf756a40; a passed broad check does not close the documented local failures or establish zero findings. The subsequent Framework99e8d13 follow-up extracts unchanged witness-path matching after hosted python:S3776 feedback, with42 regressions passing before and after; new-head hosted checks are separate from the old-head snapshot.

The full Python run stopped on the old protected-caller fixture after 56 successful executions. That test input was subsequently repaired with the exact last inline caller from Parent f5523da040bd6325b369269ada074be6ba069c4f, preserving permission expectations. Actual protected runtime remains blocked: the immutable8ae707d72f1a8acb25d239e55e28a73cbc7522b1 broker reads the current thin Parent wrapper but requires the historical inline job/concurrency contract. It rejects before artifact download/build/root admission. Fixing historical tests does not repair that delegation chain.

Local checker/runtime output proves only its stated layer. No fresh host campaign, full H2/H3 acceptance, exhaustive security clearance or final repaired commit-pair qualification is claimed.

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt.
