# PR #382: bounded closure record

**Language:** English | [Deutsch](pr-382-merge-readiness.de.md)

## Requested follow-up: the remaining 25 Sonar findings

On 2026-10-27 the user separately authorized fixing the 25 remaining maintainability findings at base `0867713`. Six existing native-analysis helpers and one test receive behavior-preserving extractions, constants, comprehensions, ASCII-equivalent regex shorthand and an unambiguous exception assertion. The 29 selected existing on-demand executors / 38 expanded cases passed with zero skips. The automatic inventory remains 100 cases / 80 executions; no case, workflow, gate or source scope is added or weakened. The [follow-up Change Record](../reports/audits/change-records/CR-20261027-sonar25-maintainability.md) describes scope and proof. Fresh published-head CI/Sonar and the final review state are recorded on the linked PR; the earlier closure below stays bound to its named revisions.

## Integration and authority

[PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) is the authority for the final published head, terminal checks and review state. This record documents the finite closure changes following checkpoint `011cb197a82801c2c3eada073eb6847899c44933`; results from earlier heads are not transferred.

#410 and master `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` (#422) are integrated. The independently reviewed #422 merge was explicitly authorized and completed before the latest scope stop; its six ruleset checks and three Sonar jobs passed. The protected NGINX caller pins that broker and Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`. Parent's Framework gitlink and MRTS remain unchanged. No further master merge, new PR/project, migration, release or deployment is authorized.

Coverage was first targeted for improvement, then explicitly removed by the user from security and merge acceptance. `sonar.coverage.exclusions=**` changes coverage applicability only. The five remaining built-in gate conditions, security rules, source analysis, exact-revision checks and secret isolation remain.

## Final automatic selection

**100 expanded active cases / 80 executions** share one standard inventory across `make test`, the no-argument runner, normal Python discovery and every automatic CI group. A shared group cannot pull archived cases into that selection. Full source/selector admission and pre-child rejection of more than 100 remain; no truncation or assertion removal is used.

**1893 specialist cases / 839 executions** remain in source and the inventory, outside every default path. They require explicit `--on-demand` with a group/case/execution selector, or the existing explicit module-wide opt-in. The previous automatic offline exception is superseded by the final user instruction. Sonar's fixed Python/Go/Common coverage catalogs are retained on demand and no longer run automatically; the source/scanner/native-context/gate pipeline remains. The [archive](../reports/testing/test-selection-archive.generated.json) is generated from that boundary.

Connector E2E remains **26**. The existing eight counted offline I12 cases stay within the shared standard budget; historical I12 host/matrix/oracle campaigns remain closed, with no `I12_COMPLETE` claim. Three narrowly selected guard controls complete the existing 97-case standard selection; two already existed in the retained catalog.

## Verification and remaining publication criterion

The closure selection passed **11 guard executions / 11 expanded cases, zero skips**. Check-only admission and all 37 standard groups resolved within the same 100-case inventory; real Python discovery enumerated exactly 44 selected methods without running them. `make -n test` resolves to the inventory runner. Two explicit C null checks preserve the earlier helper-proven rejection directly at the reported sinks; both touched C units passed strict C17 syntax compilation. No full offline catalog was rerun.

At checkpoint `011cb197`, all **22** automatic workflows were terminal: **20 successful**, broad and native Sonar failed solely at their server gates. Native SDK and all twelve actual target builds/capture validators succeeded; **611 aggregate compilation units fully analyzed, zero partial**, with 100% CFamily indexing in each project, CTU and successful taint execution. These are analyzer/build proofs, not host runtime qualification. Original native job conclusions were three successful gates and nine failed gates. No failed job was blindly rerun.

The twelve new Python security findings were individually source-traced through private build/output ownership, fixed caller choices and actual producer provenance; each main/advisory issue instance receives its own reason and readback. Native findings were likewise individually reviewed, including exact receive-buffer bounds, finite-string guards, real data-versus-path operands and the NGINX callback ABI. No blanket exclusion, rule suppression, accepted-risk waiver or fabricated PASS is used. The two broad null-propagation reports receive explicit source guards. Historical job failures remain failures; final delivery requires fresh terminal analysis of the published closure head.

The existing separate [Framework PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) finished at `03da9353561bf632a1f7bfc71b0a2671ec7aa257`: all twelve workflows, Ruff/Pyright and actual SDK/C/CLI Sonar gate passed. No new Framework work or Parent gitlink import follows from this result.

## Acceptance and stop

Normal targeted commit/push must preserve `local HEAD = remote branch = PR head`. `verified_pr` and Ready require all applicable exact-head checks/Sonar terminal and passing, actionable review feedback handled, documentation aligned and task-owned processes stopped. Otherwise the PR must disclose the concrete failing check and missing prerequisite without claiming readiness. Current terminal publication evidence is maintained on the linked PR, avoiding a documentation-only push that would invalidate that same evidence.

Earlier 94/342, 79/298, C++17/20/23, coverage and No-CRS results retain their original revisions. They are not new-head acceptance. See the [remediation record](../reports/audits/change-records/CR-20261026-pr382-sonar-remediation.md), [native security guide](sonarqube-native-security.md), [testing guide](testing-and-evidence.md) and [historical handoff](pr-382-i12-handoff.md). Stop after this finite acceptance decision; no further improvement campaign is part of the task.
