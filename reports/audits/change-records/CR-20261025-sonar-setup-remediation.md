# Change Record: CR-20261025-sonar-setup-remediation

**Language:** English | [Deutsch](CR-20261025-sonar-setup-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261025-sonar-setup-remediation |
| Date (UTC) | 2026-10-25 |
| Base revision | `9f44647593bac7947113558c6ad183ab118e80af` |

## Motivation and problem statement

The full Parent Sonar setup exposed accumulated coverage and security findings,
incomplete native build context, six Shell parser warnings, an ignored Python
architecture perspective and missing independent JSON/YAML/workflow scope guards.
Fresh authenticated baseline readback confirmed analysis
`52df415d-2c24-43a3-a63a-de6e79c37d60` at the base SHA: main gate `ERROR`,
Security Rating E and new-code coverage 0.6% against unchanged A/80% requirements.
The `previous_version` period starts on 2026-05-14. The paginated inventory of
663 files contains new lines to cover: Python 57,281; C 27,420; C++ 184; Go 6,284.
A PR changed-line result must not be conflated with that accumulated main gate.

## Acceptance criteria

Preserve Parent source/test and independent repository boundaries, Python/Go
pins, all maintained language scopes, CFamily test sources, main/advisory
separation and exact-SHA provenance. Generate genuine broader coverage; reject
unsafe evidence-derived read paths; guard maintained JSON/YAML/workflows;
resolve or precisely classify each Shell/native/architecture issue. Final
completion requires the final SHA's scanner, terminal server processing, main
and advisory gates, language execution, coverage import and warning readback.
These final server criteria are not established by this development record.

## Implementation decision and rationale

The requested Scanner CLI update pins `8.2.0.6438` for all three jobs. The official release and Linux x64 archive/checksum/signature endpoints were verified; Action signature verification remains enabled. Historical baseline results still refer to `8.1.0.6389`. Reverting only `scannerVersion` restores the previous binary pin.

The coverage helper selects meaningful provenance, artifact, lifecycle and
security tests; Python measurement spans production namespaces and subprocesses,
Go covers default-build packages of all four modules with 37 named scenarios,
and instrumented Common tests produce real gcov reports. Fresh directories,
clean-checkout and SHA checks prevent reuse; finalization combines all producer
process coverage and validates resolvable Python paths. No gate, profile,
new-code definition or production coverage exclusion was changed.

The scope guard now independently protects maintained JSON/YAML and executable
workflows, retains explicit negative-fixture treatment, and requires analyzable
component content rather than a README. Five POSIX Shell files use equivalent
arithmetic, heredoc/process ownership and case syntax. The scheduler `ci/runtime/lifecycle/run-full-matrix-parallel.sh` retains its
required `exec 8<>` FIFO operation pending analyzer-specific verification.

AutoConfig remains because existing real compilation databases omit Parent
units. CI supplies actual Apache/APR/ModSecurity headers via supported include
properties and a compiler probe. Full native host/generated-header coverage and
C/C++ taint remain incomplete; copied HTX sources require provenance-preserving
mapping before any database migration.

Evidence readers bind to invocation-owned roots and no-follow regular-file
descriptors. File-content roots cannot widen access; private-job summaries,
retained logs, native metadata inputs and report/cache paths are treated at
their consumer boundaries. Legitimate configured external paths and canonical
read-only fixtures remain distinct approved inputs.

The exact architecture proposal removes 14 excluded Framework/MRTS groups and
renames 30 Parent labels containing `/`, preserving Parent patterns, four nested
groups, metadata and the existing empty `constraints` list. The authorized CLI
update failed HTTP 415; readback proved the server model unchanged.

## Changed files

- `.github/workflows/sonarqube.yml`, `ci/sonar-coverage.ini`, `ci/checks/analysis/run-sonar-coverage.py`.
- `ci/checks/analysis/check-sonar-scope.py`, `tests/test_sonar_scope.py`, `tests/test_sonar_coverage.py`.
- `ci/lib/evidence_inputs.py`, the affected evidence report generators, lifecycle consumers and trusted component postprocess invocation in `ci/provisioning/components/prepare-runtime-components.py`, `tests/test_evidence_input_security.py`, `tests/test_sonar_evidence_boundaries.py`.
- `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`, `connectors/envoy/harness/run_envoy_composite_matrix.sh`, `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`, `connectors/haproxy/htx-overlay/resolve-modsecurity.sh`, `connectors/haproxy/harness/run_haproxy_smoke.sh`.
- `config/analysis/sonar-python-architecture.patch.json`, `docs/sonarqube-analysis.md`, `docs/sonarqube-analysis.de.md`, and this Change Record pair.

## Commands executed

Additional current verification: all 82 existing generated-evidence-integrity tests passed. The final selected Python suite passed 61 tests after metadata parser/status and source/build lookup controls were added. The measured bootstrap, Go/native runs, measured finalizer and post-exit merge sequence passed locally; all four module reports and 71 native reports remain genuine development evidence.

Independent security candidate review identified metadata pathname reopening and missing configured-component approvals. Both were reproduced and corrected; 41 focused tests passed, including full generator output, actual postprocessor invocation, staleness and authorized SONAME controls. The integrated selected Python coverage run then passed 54 tests. Final CI must regenerate all reports from its clean analyzed SHA.

Observed development evidence, not final-head or hosted-runtime qualification:

| Command or procedure | Observed result |
| --- | --- |
| `rtk bypass python3 ci/tools/new-change-record.py create --name sonar-setup-remediation --date 2026-10-25 --base-revision 9f44647593bac7947113558c6ad183ab118e80af` | Created both native record scaffolds. |
| Focused `tests.test_sonar_scope` suite and real scope checker | 18 tests passed; 136 CFamily units and four Go modules retained. |
| `sh -n`, `bash -n`, `shellcheck --severity=error` on all six reported scripts | Passed; does not prove Sonar parsing. |
| Focused Shell-related Python suites | 65 tests initially ran with seven missing-Framework skips; all 12 scheduler tests subsequently passed using the clean exact Framework gitlink. |
| Coverage producer development trials | Python: 33 tests passed, 185 production files represented; Go: all 37 selected cases passed; native: 71 gcov reports over 62 repository files, including all 58 Common C files. |
| `tests.test_sonar_coverage` | Six provenance/report regressions passed. |
| Existing Apache C17 source compile with installed Apache/APR/ModSecurity headers | Passed; compilation evidence only. |
| Canonical-wrapper authenticated issue/gate/model readback | Baseline gate/finding/model state confirmed; 46 vulnerability issues triaged, no issue transitions. |
| Canonical-wrapper model PATCH with CLI `1.10.1` | HTTP 415; follow-up readback confirmed no server mutation. |
| `rtk bypass python3 ci/tools/new-change-record.py check` | PASS for structure, not evidence validation. |
| `rtk make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` | PASS after initializing the task-owned exact Framework checkout; initial missing-Framework link errors were resolved. |
| `rtk make check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/sonar-setup-remediation/modules/ModSecurity-test-Framework` | PASS; repository path references and documentation links. |
| Targeted scope/coverage/evidence/native-reader suites | 67 tests passed before final review corrections. |
| Eight selected `tests.test_ci_security_workflows.CiSecurityWorkflowTest` Sonar/PR-boundary methods; `rtk bypass actionlint .github/workflows/sonarqube.yml`; `rtk bypass zizmor --offline .github/workflows/sonarqube.yml` | PASS; Zizmor retains one existing configured suppression. |
| Focused guide-link/model-payload validation | All changed guide links resolve; payload equals prepared proposal with 32 unique slash-free labels and unchanged constraints. |

Local coverage development used Python `3.14.4` and Go `1.27.3`; CI pins remain
Python `3.14.7` and Go `1.27.1`. Final integrated command results and actual
current-head links require coordinator reconciliation after source integration.

## Security impact

Stored JSON evidence could select unrelated host files for summaries, excerpts,
refresh classification or hashes. Corrections enforce caller-owned input roots
and descriptor-based regular-file reads, including symlink/traversal controls,
while preserving legitimate private-runtime/cache and canonical source inputs.
Remote exploitation was not established. Fourteen baseline findings have
concrete existing-control/operator-authority counterevidence; remaining
file-content groups require fresh scanner verification. No finding was accepted,
suppressed or marked false positive to change a rating. No credentials or raw
sensitive payloads are stored in this record.

## Runtime evidence

First PR-head CI at `d094e1dacd1f540b1ffcf35b7da5bd4b3c255665`, [run 40230520936](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40230520936), passed canonical Python setup and all 61 selected Python tests. Go setup selected `1.27.1`, then the coverage step failed before scanning because setup-go restored a global Python ahead of the venv on PATH (`No module named coverage`). The workflow now names the dedicated venv interpreter for every coverage producer/merge/finalizer. No scanner upload or gate result is claimed for that failed attempt.

Final integrated local coverage pipeline: Python54tests, Go37tests and native Common tests all passed; finalization merged the real Go/native producer-process coverage into Python XML and validated all report paths. Reports are explicitly marked as development evidence from uncommitted changes; final CI must regenerate them for the clean commit. Local source, workflow, bilingual, link, archive and whitespace checks passed. No full hosted runtime qualification is claimed.

No hosted connector runtime evidence was collected or claimed. Coverage tests,
source compilation, static checks and scanner readback prove their respective
layers only. Historical baseline CI:
[run 40224506735](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40224506735).
The final commit's CI/Sonar processing and main/advisory results are not yet
available in this record.

## Known limitations

| Original finding | Disposition at preparation |
| --- | --- |
| Security Rating E | `weiterhin offen`: source fixes and technical triage do not establish fresh rating/issue closure. |
| New-code coverage 0.6% | `weiterhin offen`: real measurement broadened; accumulated main-branch 80% is not demonstrated. |
| Native missing includes/parsing errors | `weiterhin offen`: real header context improved; final scanner deltas are unverified. |
| Full-Parent C/C++ taint in AutoConfig | `begründete Analyzergrenze`: unsupported mode and independent executable targets remain. |
| Ignored Python model | `extern blockiert`: media-type capability missing in authorized CLI; exact proposal supplied. |
| Six Shell parser warnings | `weiterhin offen`: local equivalent rewrites and syntax checks need fresh per-file Sonar confirmation. |
| Missing JSON/YAML/workflow scope guard | `behoben und nachgewiesen`: focused local guard regressions passed. |

The model's main project UUID is `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2`; model ID
is `cb04d3a3-7c8f-447c-99f0-ca49c97f054f`. Effective `architectureadmin`/`admin`
roles were present. Applying the exact body in
`config/analysis/sonar-python-architecture.patch.json` requires the intended
architecture editor or an authorized client supporting
`application/merge-patch+json` at
`PATCH /api/v2/architecture/models/cb04d3a3-7c8f-447c-99f0-ca49c97f054f`, followed
by a scan proving perspective application. Both advisory projects have zero
models and were unchanged.

## Remaining risks

Native connector-host paths, `libmodsecurity` Go tags and alternate platforms
remain unmeasured. AutoConfig still lacks complete host/generated-header
contexts and C/C++ taint support. The accumulated coverage gate can remain red
even if a PR changed-line gate passes. Repository-wide compact default-suite
enforcement is not claimed. Fresh analyzer imports,
per-file parsing and terminal gates remain necessary.

## Checks not run and rationale

Final integrated source checks and current-head CI/Sonar verification were still
being coordinated when this record was prepared. Full native host/runtime
matrices and all historical tests were not run by the documentation work; its
scope is truthful documentation of the selected assessment. No Framework/MRTS
source or Gitlink was changed. The architecture update cannot be completed with
the current canonical CLI's supported interface. The full bilingual and native documentation-link checks passed after the exact pinned Framework checkout was initialized. The Parent native documentation target uses its declared Parent interpreter for the Framework-owned standard-library-only link script; no Framework package environment was changed.

## Final diff and review status

Documentation and the prepared model payload describe the reviewable patch.
The final integrated diff, exact task SHA, PR link and terminal checks must be
reconciled by the coordinator. This record does not claim `complete`,
`verified_pr`, merge or any change to `master`.
