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

- `.gitleaksignore` for the two exact public-issue-ID documentation fingerprints.
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main_test.go`.

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

## Exact baseline finding dispositions

These 46 keys belong to baseline analysis `52df415d-2c24-43a3-a63a-de6e79c37d60`
at `9f44647593bac7947113558c6ad183ab118e80af`. Existing controls or intended
operator authority are technical counterevidence, not Sonar false-positive
transitions. A fresh PR analysis does not automatically close old main-branch
issue keys. The first table accounts for 14 existing-control/operator-authority
findings; the second accounts for 32 caller-boundary remediation findings.

| Exact baseline key(s) | Source boundary | Technical disposition |
| --- | --- | --- |
| `AaF0eroXXd_g6jxuNaF2` | `ci/lib/framework_revision_pins.py` (`_sha`, `_git`) | Lowercase ASCII SHA-1 validation precedes Git argv construction; no shell. |
| `AaF0erogXd_g6jxuNaF3` | `ci/tools/prepare-reviewed-framework-handoff.py` | Operator selects a new output patch; `open("x")` prevents overwrite. No narrower privilege boundary identified. |
| `AaF0errHXd_g6jxuNaGG` | `ci/runtime/common/hostruntime_preflight.py` (`_approved_lock_path`) | Runtime/source ownership is checked before reading the lock. |
| `AaF0erquXd_g6jxuNaGE` | `ci/runtime/lifecycle/write-transport-lifecycle-artifacts.py` | Configuration hash inputs pass runtime/source or canonical Framework source validation. |
| `AaF0erqkXd_g6jxuNaGD` | `ci/runtime/lifecycle/resolve-full-lifecycle-profile.py` | Manifest input passes `runtime_or_source_artifact_path` before loading. |
| `AaF0erq1Xd_g6jxuNaGF` | `ci/runtime/lifecycle/run-full-matrix-job.py` | Canonical repositories, approved runtime paths and validated run ID feed an argv subprocess without a shell. |
| `AaF0erqcXd_g6jxuNaGC`, `AaF0erqcXd_g6jxuNaGB` | `ci/runtime/lifecycle/run-full-matrix-resume.py` | Canonical roots, allowlisted connector/CRS/MRTS tokens, bounded numeric timeout and `shell=False`. |
| `AaF0erpfXd_g6jxuNaF6`, `AaF0erpfXd_g6jxuNaF7` | `ci/runtime/lifecycle/run-verified-case.py` (`write_json`) | `runtime_artifact_path` checks the destination immediately before writing. |
| `AaF0erp1Xd_g6jxuNaGA` | `ci/runtime/lifecycle/run-verified-report-run.py` (`prepare_verified_run_context`) | The `current-run-id` destination is constructed from validated runtime paths. |
| `AaF0erp1Xd_g6jxuNaF8` | `ci/runtime/lifecycle/run-verified-report-run.py` | Manifest output uses canonical `report_path`; JSON supplies payload rather than destination authority. |
| `AaF0erpTXd_g6jxuNaF5` | `ci/runtime/lifecycle/write-engine-lifecycle-artifacts.py` | Rules/source paths are validated; hashing uses `O_NOFOLLOW` and a regular-file descriptor check. |
| `AaF0erukXd_g6jxuNaGe` | `connectors/lighttpd/harness/patched_event_validation.py` | Explicit operator-selected events input; no additional HTTP or privileged authority boundary established. |

| Exact baseline key(s) | Source boundary | Technical disposition |
| --- | --- | --- |
| `AaF0ersUXd_g6jxuNaGb`, `AaF0ersUXd_g6jxuNaGc`, `AaF0ersUXd_g6jxuNaGa` | `generate-nginx-mrts-http500-cluster-analysis.py` | JSON/JSONL and excerpt/body reads use invocation-owned `EvidenceInputs`; metadata cannot reopen rejected paths. |
| `AaF0errtXd_g6jxuNaGR`, `AaF0errtXd_g6jxuNaGO`, `AaF0errtXd_g6jxuNaGP`, `AaF0errtXd_g6jxuNaGN`, `AaF0errtXd_g6jxuNaGU`, `AaF0errtXd_g6jxuNaGM`, `AaF0errtXd_g6jxuNaGV`, `AaF0errtXd_g6jxuNaGQ`, `AaF0errtXd_g6jxuNaGL`, `AaF0errtXd_g6jxuNaGS`, `AaF0errtXd_g6jxuNaGK`, `AaF0errtXd_g6jxuNaGT` | `generate-verified-runtime-mismatch-analysis.py` | Invocation-owned roots constrain recorded evidence, nested includes, stats, fingerprints and reads. |
| `AaF0erkjXd_g6jxuNaFz`, `AaF0erkjXd_g6jxuNaFv`, `AaF0erkjXd_g6jxuNaFt`, `AaF0erkjXd_g6jxuNaFw`, `AaF0erkjXd_g6jxuNaFx`, `AaF0erkjXd_g6jxuNaFy`, `AaF0erkjXd_g6jxuNaFu`, `AaF0erkjXd_g6jxuNaFs`, `AaF0erkjXd_g6jxuNaFr` | `generated_report_utils.py` sinks via `run-native-case-comparison.py` | Retain the actual loaded run directory, derive canonical fixture identity and pass confined byte receipts to metadata. Generic helper policy remains unchanged. |
| `AaF0erp1Xd_g6jxuNaF-`, `AaF0erp1Xd_g6jxuNaF9`, `AaF0erp1Xd_g6jxuNaF_` | `run-verified-report-run.py` | Confine private summary reads and retained refresh logs to invocation `VERIFIED_RUN_LOG_ROOT`; unsafe input cannot forge `consumer_stale`. |
| `AaF0eroJXd_g6jxuNaF1`, `AaF0eroJXd_g6jxuNaF0` | `best_effort_evidence_readers.py` sinks via report consumers | Affected callers use `EvidenceInputs.json/jsonl`; generic best-effort reader behavior remains unchanged. |
| `AaF0errYXd_g6jxuNaGH`, `AaF0errYXd_g6jxuNaGI`, `AaF0errYXd_g6jxuNaGJ` | `update-runtime-reports.py` (`file_proof`) | Only cache roots or explicit invocation-approved component leaves authorize hashes; final SONAME targets must independently qualify. |

Attack/control regressions are in `tests/test_evidence_input_security.py` and
`tests/test_sonar_evidence_boundaries.py`; the SHA/lock controls also have tests
in `tests/test_framework_revision_pins.py` and `tests/test_hostruntime_preflight.py`.
No remote exploitation or absolute same-UID concurrent-mutation protection is
claimed. Operator-input dispositions do not authorize future privileged-service
callers to accept arbitrary paths.

## Runtime evidence

Observed intermediate PR head: `13b17cbedaa8b7d7fe382ae500052f1cac4ded16`,
[run 40231379831](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40231379831),
[Draft PR #421](https://github.com/Easton97-Jens/ModSecurity-conector/pull/421).
This clean canonical CI passed all 61 selected Python tests, 37 Go scenarios and
the native Common tests, and imported the genuine Python XML, four Go reports
and native gcov reports. Scanner CLI `8.2.0.6438` and CFamily `6.85.0.102562`
executed. Main Compute Engine task `AaF0ymveZaGJAnPJkdcR` finished `SUCCESS`;
analysis ID: `d812ee4b-6300-430f-89e9-11f7eb7b7745`.

The [main PR gate](https://sonarcloud.io/dashboard?id=Easton97-Jens_ModSecurity-conector&pullRequest=421)
was `ERROR` solely on new Security Rating E. New-code coverage **80.5%** passed
the unchanged 80% threshold; reliability, maintainability, duplication and
hotspot-review conditions also passed. Three open `pythonsecurity:S2083` findings
point to the three `os.open` operations in `EvidenceInputs._descriptor`.
Independent source investigation and focused negative/control probes found the
reported paths already constrained: lexical approval precedes opening; every
component uses no-follow directory descriptors, and the final descriptor must be
regular. Outside/sibling paths, parent traversal, relative paths and NUL input
are rejected before opening. Native comparison overwrites stored `run_dir` with
the directory actually loaded. The three main keys are
`AaF0ynIMY4cSrRUGTduD`, `AaF0ynIMY4cSrRUGTduC` and `AaF0ynIMY4cSrRUGTduB`.
They remain open on the server; no false-positive transition or suppression was
applied. Their technical disposition is `no_change`, candidate analyzer false
positives, rather than a demonstrated boundary bypass.

Both C++20 and C++23 advisory scanner jobs failed their actual gates, each
`ERROR`; C++20 new-code coverage was 82.7%. Their independent full-branch results
do not replace the main PR result. Fresh advisory analysis also exposed four
`c:S5782` findings at HAProxy's `bounded_cstring_length`/maximum-length `memchr`
call. Independent investigation found the reported short string literals and
directory-entry names are NUL terminated. The [C committee draft N1570,
section 7.24.5.1 paragraph 2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)
specifies sequential `memchr` behavior ending at the first match; a bound larger
than the terminated string does not itself prove an overread. The
[GNU C Library search-function contract](https://snapshots.sourceware.org/glibc/trunk/latest/manual/html_node/Search-Functions.html)
also describes first-match search. These four findings are candidate analyzer
false positives with `no_change`, not confirmed buffer overflows or server
transitions. C++20 issue identifiers include `AaF0yz5SaVChWkKVlx_W`, `AaF0yz5SaVChWkKVlx_X`,
`AaF0yz5SaVChWkKVlx_Z`, `AaF0yz5SaVChWkKVlx_Y`.

An exact-source standalone helper probe compiled with C17, warnings as errors,
AddressSanitizer and UndefinedBehaviorSanitizer passed the three reported
literals, a terminated 256-byte buffer with bound 4096, NUL at the last allowed
byte, bounded unterminated rejection and unchanged output on invalid arguments.
No sanitizer finding occurred. The production helper remains unchanged.

The PR-range Gitleaks check at `8f632bdd` reported two generic-API-key matches
on the public Sonar issue identifiers above, one per language record. The exact
commit/path/rule/line fingerprints are recorded in `.gitleaksignore`; no file,
rule or credential pattern is broadly excluded. The wording avoids implying
credential material. This technical non-secret disposition does not change any
Sonar issue status. The full four-commit PR range and current record content
passed with no unreviewed matches; synthetic credential-shaped controls still
triggered the GitHub PAT and generic-API-key rules, with full redaction.

A follow-up cache regression distinguishes authority from existence: an outside
SONAME target must yield the same rejected/no-digest proof whether present or
absent. Non-strict resolution avoids the former early missing-target status;
the 19 evidence-input tests passed. Resolution can still consult link metadata;
this is not a claim of zero observation outside approved roots.

All 136 native units remained in scope. Quality improved from 77.52 to
**91.28/100**, and functions with parsing errors fell from 414 to **193/2,260**.
Unresolved project includes fell from 115 to **46/1,132**; no external includes,
module imports or header units remained unresolved in that scan.
Missing host/generated headers still include NGINX, HAProxy and lighttpd;
C/C++ taint remains disabled in AutoConfig. Four original Shell warnings were
absent (Apache cleanup, Envoy harness, lighttpd harness and HAProxy harness).
The scheduler's valid `8<>` FIFO redirection and HAProxy resolver's case patterns
still produced warnings at this SHA. A further equivalent resolver spelling is
locally validated: shell syntax, ShellCheck, five resolver tests and nine
before/after architecture cases passed. The 44 invalid architecture labels still caused the intended
perspective to be ignored. These observations are bound to this intermediate
SHA; subsequent source changes require a new clean scan and exact-head readback.

Follow-up source head `8f632bdd45f117ba7e8b025c1fbfac37cdad8cef`,
[run 40232441972](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40232441972),
completed server processing: task `AaF01odhZaGJAnPJkdwU`, analysis
`6759e9c6-2376-41a9-85cd-2df9de1d0ca6`, status `SUCCESS`. The resolver warning
is now absent: **five of six original Shell warnings are resolved and measured**;
the unchanged valid scheduler FIFO syntax remains the documented analyzer limit.
Main PR coverage remains 80.5%, native metrics remain 91.28/193/46 as above,
and the gate remains `ERROR` solely on the three descriptor-open findings.
Both advisory jobs still failed their real gates. The two public-ID Gitleaks
false positives described above require a follow-up documentation-only commit;
that head's terminal CI/Sonar evidence will be attached to PR #421.

Second CI attempt at `161bfd7118b7480d0d997ff1bd4a5157f97ca1d8`, [run 40230777535](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40230777535), passed canonical Python/Go setup but exposed a pre-existing filesystem-dependent Go fixture: deleting and recreating a closed regular file allowed immediate inode reuse in the replacement-during-close test. The fixture now renames the original before creating the replacement, guaranteeing a distinct live inode; the replacement-preservation assertion and production listener are unchanged. Independent source review supported the diagnosis; the targeted replacement and real-socket cleanup tests passed 20 repetitions locally. This is a test determinism correction, not a claim of absolute same-UID race immunity.

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
| Security Rating E | `weiterhin offen`: intermediate PR gate remains E on three technically constrained descriptor findings; no server transitions. |
| New-code coverage 0.6% | `behoben und nachgewiesen` for intermediate PR coverage 80.5%; accumulated main-branch 80% remains `weiterhin offen`. |
| Native missing includes/parsing errors | `weiterhin offen`: intermediate quality 91.28 and 193/2,260 function errors show improvement; NGINX/HAProxy/lighttpd context gaps remain. |
| Full-Parent C/C++ taint in AutoConfig | `begründete Analyzergrenze`: unsupported mode and independent executable targets remain. |
| Ignored Python model | `extern blockiert`: media-type capability missing in authorized CLI; exact proposal supplied. |
| Six Shell parser warnings | Five `behoben und nachgewiesen` at `8f632bdd`; valid scheduler FIFO syntax is a `begründete Analyzergrenze`. |
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
