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
Remote exploitation was not established. The initial review assigned fourteen baseline findings to existing controls/operator authority; its marker judgment was incomplete and is explicitly corrected in the continuation. Remaining
file-content groups require fresh scanner verification. No finding was accepted,
suppressed or marked false positive to change a rating. No credentials or raw
sensitive payloads are stored in this record.

## Exact baseline finding dispositions

These 46 keys belong to baseline analysis `52df415d-2c24-43a3-a63a-de6e79c37d60`
at `9f44647593bac7947113558c6ad183ab118e80af`. Existing controls or intended
operator authority are technical counterevidence, not Sonar false-positive
transitions. A fresh PR analysis does not automatically close old main-branch
issue keys. The first table records 14 initial control/operator judgments, including the explicitly corrected marker judgment; the second accounts for 32 caller-boundary remediation findings.

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
| `AaF0erp1Xd_g6jxuNaGA` | `ci/runtime/lifecycle/run-verified-report-run.py` (`prepare_verified_run_context`) | Earlier counterevidence was incomplete: a canonical destination alone protected neither the early marker read nor leaf symlink/FIFO access. Continuation reproduced the defect and corrects this judgment; see closeout below. |
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

At original preparation, no hosted connector runtime evidence was collected or claimed. The continuation below adds actual runtime readback at `4ec7581056889f8c70f44c6725f6bfa65a7fc45b` with an explicitly bounded scope. Coverage tests,
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
`config/analysis/sonar-python-architecture.patch.json` requires a supported authorized client handling
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

## Targeted PR #421 continuation

The complete [EN/DE closeout](../../../docs/sonarqube-pr421-closeout.md) maps the six current requirements to the exact previous head `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`. Main CE task `AaF03ulBdkEpBguA0oKZ`, analysis `081d99d7-c136-4a67-b039-96507ad472a4`, completed successfully; the gate remains ERROR solely on three OPEN `pythonsecurity:S2083` issues. Complete flows distinguish `request` from invocation-owned `run_dir`; each issue has controls, nine actually passing attack/control tests and a concrete False Positive decision proposal. No issue transition was performed.

The historical 23 findings per advisory were independently reviewed with complete normalized flows: 22 pairs have proposed `not_actionable` counterevidence, one marker pair required renewed review. The earlier claim above for `AaF0erp1Xd_g6jxuNaGA` was incomplete. Before correction, tests reproduced symlink reading and external overwrite through `current-run-id`; legitimate restoration passed. The runner now validates directory trust before marker access, reads bounded data through held no-follow/nonblocking descriptors, checks type/ownership/mode/link count and writes atomically. Sixteen boundary tests and eight related runtime tests passed; independent review passed the previous seven marker cases without a concrete surviving bypass. A final Root check then reproduced, with the eighth marker test, acceptance of a valid prefix when a short os.read preceded invalid trailing bytes. A bounded read loop through EOF or at most 4,097 bytes fixes this; the new test failed before correction and all 16 boundary tests passed afterward. This eighth case was not covered by the previous independent seven-case review. This establishes local boundary control, not a remote exploit or final Sonar closure.

Fresh architecture comparison confirms the unchanged 14 Framework/MRTS removals and 30 Parent-label renames, preserving patterns, four nested groups and constraints. CLI `1.10.1` still has no header option; a repeated authorized PATCH returned HTTP 415, and server readback was identical. The closeout specifies the exact request delta and supported-access steps for `application/merge-patch+json`, without bypassing wrappers or prescribing unverified UI behavior. Perspective application remains externally blocked.

The new native context helper and six passing tests add real contract pins, archive checksums and configure provenance. A real development probe configured NGINX successfully, then failed because the new lighttpd patch invocation differed from the existing Parent patch path. The second probe passed the unchanged canonical patch/stamp/ABI path but stopped before lighttpd configure because the approved archive has no configure script. The third complete header-preparation development run passed with exit 0, unchanged upstream autogen under Bash and actual patched-lighttpd configure. The manifest records `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`, `uncommitted_changes: true`, eleven include directories and archive/patch/configure/generated-file hashes. New Sonar counts remain unproved. `ci/checks/analysis/prepare-sonar-native-context.py` and `tests/test_sonar_native_context.py` add the implementation; workflow measurement occurs before the coverage finalizer. The selected suite now contains 75 methods (61 existing, eight marker, six header tests); the fresh instrumented local selection passed all 75 tests in 7.256 s; helper development coverage is 82.48% for lines and branches, not a Sonar gate result. Clean-head CI remains pending. No component-owned script changed. No partial compilation database replaces AutoConfig. Parsing errors 193/2,260 and unresolved includes 46/1,132 remain historical head values, and C/C++ taint is explicitly unproved.

The Python simulation-cost boundary at `runtime_path_utils.py:69` and both predecessor messages demonstrably existed in the baseline main project and both baseline advisories. Current full advisories repeat them; their absence in cached main-PR analysis proves no repair. FIFO `exec 8<>` retains its semantics. These documented analyzer boundaries are neither excluded nor asserted to be PR regressions.

Runtime run `40233061042` actually completed successfully for five connectors and aggregate, including Apache job `121290821692`: selected SQLi block case HTTP 403/rule `942270`, audit and cleanup passed. Compact artifact `12614940472` was content/digest verified; aggregate `12614138658` reports only the selected case with 5 passed/0 failed/6 blocked/13 not_run, `coverage_complete: false`, `merge_eligible: false`. This does not qualify the complete runtime matrix. PR coverage 80.5%, advisory branch coverage 82.7% and accumulated master baseline 0.6% remain distinct.

After the source changes this development state requires a new clean head, terminal CI and exact CE/analysis/gate/coverage/warning proof for all three projects. The PR remains Draft; no merge or `master` change occurred. Complete IDs, gate conditions, limitations and remaining dispositions are in the closeout. The new files are hand-maintained technical documentation, not canonical scanner artifacts.

### Observed source-change head

Clean source commit `59bc0842cea90d4052c0d005218fae3aca14c2b2` was analyzed in run `40238653971`. Exact scanner-context/CE/analysis readback is recorded in the closeout: all three server tasks SUCCESS, all gates ERROR solely Security Rating E. Actual PR new-code coverage is 82.3%; advisory branch new-code coverage is 83.7%, with Python XML, four Go reports and 71 gcov reports imported. All 136 native units remain; actual host headers improve parsing to 2/2,263 erroneous functions and resolve every project include (0/1,132), quality 95.81. One external include and aggregate class/statement errors remain unlocated; AutoConfig explicitly still disables C/C++ taint.

Complete vulnerability inventories are main 8, C++20 27 and C++23 24. The repaired marker finding disappears in both advisories; C++23 also omits three unchanged evidence-reader findings retained in the other projects, without an established reason or status mutation. Five new helper findings per project received independent full-flow review, six passing helper tests, eight rejected output attacks, allowed private-root control and actual literal-argv/sentinel control. Each has an individual False Positive proposal, with limits against concurrent same-user replacement and upstream pathname behavior stated. No server issues were changed. Both full advisories retain the baseline Python cost/predecessor warnings; the main architecture perspective is still ignored and FIFO semantics preserved.

Five non-Sonar CI workflows failed the developer-path documentation check at this source head. Both reader documents now use the portable interpreter form; local variable documentation (101 references), bilingual, path and link checks pass. No validator was weakened. This documentation-only correction needs a new final-head CI/Sonar run, whose current evidence is reconciled in the PR to avoid a self-referencing documentation commit. Earlier successful runtime evidence remains explicitly tied to its own SHA and selected case. Overall outcome remains partial; architecture application, issue decisions, residual native/taint gaps and final current-head readback retain their documented dispositions.

## Complete New Code issue continuation, 2026-10-26

This phase supersedes the earlier restricted security-only inventory and
no-transition disposition. The starting clean PR head is
`1aa9646a65e5b3bd85b911c99ff40be73eee2cd3`; the local source corrections below
are uncommitted development changes at preparation. Exact-head closure requires
new CI and server analysis after committing them. Evidence for this phase is
retained under `/var/tmp/codex/ModSecurity-conector/runs/pr421-all-findings-20261026`.
The per-issue inventory, source/flow controls, individual actions and readbacks
remain distinct from scanner warnings, annotations, hotspots and coverage.

### Inventory and initial analysis binding

The main query used `sinceLeakPeriod=true`, `issueStatuses=OPEN,CONFIRMED`,
`ps=100` and pages 1/2 without a type filter: 100 plus 50 results, exactly
150 unique issues. Language counts are 122 Shell and 28 Python; qualities are
141 maintainability, eight security and one reliability. Legacy severity counts
are six MINOR, 116 MAJOR, 25 CRITICAL and three BLOCKER. Main security hotspots
were independently queried and numbered zero. The advisory queries use the same
New Code/status scope: C++20 31 and C++23 16 unique issues. The former total
vulnerability counts 27/24 are a different scope.

| Project | Initial CE task | Initial analysis | Observed binding |
| --- | --- | --- | --- |
| Main | `AaF1LkTSF1KaAz-ccMvg` | `3a8694d2-6375-45ed-8133-f6506f4c9533` | `SUCCESS`, source `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3` |
| C++20 | `AaF1LUoAdkEpBguA0qDb` | `64b9b52e-649f-4b38-ba7e-3a88825baad0` | `SUCCESS`, source `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3` |
| C++23 | `AaF1LYWYZaGJAnPJkfuW` | `d8e56714-5881-4d40-bd7c-5cb51d3a1dee` | `SUCCESS`, source `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3` |

All three gates initially read ERROR before the individual decisions, with
security ratings E/E/C; other gate conditions passed and none was ignored.
Imported coverage was 82.3% main PR new-code coverage and 83.7% advisory branch
new-code coverage. Python XML, four Go reports and native gcov import remain
required; development coverage is not a CI/server import. These percentages do
not repair accumulated master coverage. `main-initial-inventory.json`,
`main-initial-summary.json` and `analysis-bindings-initial.json` retain the
inventory/binding evidence; subsequent scans must be compared against it.

### Individual security decisions and local nonsecurity repairs

Independent review retained 21 separate full-flow decisions, complete call
sites, source/sink counterevidence, attack/allowed controls and per-issue
comments in `current-security-triage.json`. Fifteen attack/allowed groups passed
against both the initial source and frozen corrected candidate. Descriptor
ownership/no-follow/regular-file protections remain intact. The request payload
does not choose the invocation-owned reader root; the helper's output paths
come from the explicit operator invocation or fixed private CI children.
Literal-argv and rejected Git-identity/nonliteral-contract controls also passed;
new Git-related findings are not preclassified by this review.

The current user explicitly authorized proven False Positive decisions. Each of
the 21 issues received its own `FALSE_POSITIVE` transition and precise comment:
eight main, eight C++20, five C++23. `security-fp-actions.json` and the three
project status readbacks confirm every status and matching comment. No risk was
accepted; no gate, rule profile, coverage threshold, New Code requirement or
scope exclusion was relaxed. Advisory decisions have their own flow evidence.

All 142 main nonsecurity issues have local code corrections pending a fresh
scan; overlapping advisory nonsecurity repairs cover 23/11 issues. Envoy has
87 local issue corrections, including POSIX-safe named function arguments and
explicit no-op defaults. The three HAProxy/lighttpd scripts have 35 corrections,
including equivalent branch simplification, named arguments and centralized
cleanup wording. Python corrections decompose complex receipt/coverage/report
functions, preserve ASCII identity validation, and make intended exception
boundaries explicit. Security-relevant descriptor and configured-approval
controls are preserved. The changed files and individual proof are recorded in
`envoy-shell-triage.json`, `host-shell-triage.json` and the Python/native triage
records. No scanner closure is inferred from these code edits.

Validation observed before publication: 19 baseline evidence tests passed in
3.696 s; the focused integrated selection passed 44 methods in 4.711 s; the
instrumented integrated selection passed 80 Python methods in 7.829 s using
pinned coverage 7.17.0. Eleven actual case-identity controls passed. Envoy's
17 existing tests and 42 before/after characterization cases passed; all
20 embedded Python heredocs were byte-identical. Host-shell validation passed
12 selected tests and nine Lighttpd equivalence cases over 18 executions.
Shell syntax passed for the changed scripts. ShellCheck retained six existing
Envoy warnings and twelve existing HAProxy warnings; no blanket ShellCheck pass
is claimed. The valid scheduler `exec 8<>` FIFO semantics remain unchanged.

### Real native context and remaining analyzer boundaries

The complete scanner log identified the remaining external include as
`ngx_http_v2.h`. The distribution ModSecurity SDK `3.0.12` lacked
`msc_rules_error_cleanup` and `msc_intervention_cleanup`, used by the unchanged
C++ evaluator. A real negative syntax probe reproduced those API failures;
the exact approved `3.0.17` public headers compiled the unchanged evaluator
under C++17 with warnings as errors. No cleanup call was removed, no header or
compiler command fabricated, and no feature define invented.

The immutable provenance chain is Framework gitlink
`99a7985c1be92a2297b1b59208f64df6768f2cbf`, contract blob
`496b5d8e0ec70d6d31f91aeaf08024050a5698ea`, approved official ModSecurity commit
`1925753989ccce977cdaae417b55c9726c7cf02c` and public-header tree
`8daab1d1734506b687b21efd44169c273eabca6a`. Source-data acquisition does not
initialize or write the Framework/MRTS worktrees. Approved headers precede
apt headers; the real NGINX `src/http/v2` include path is added without enabling
an HTTP/2 feature profile. The helper's passive contract parser and Git-object
identity checks reject unsupported contract data.

Eleven native-context test methods passed in 0.033 s. The full real development
preparation passed exit 0: NGINX 1.31.6, HAProxy 3.2.25, lighttpd 1.4.85,
ModSecurity 3.0.17, 13 actual include directories and 11 generated/source hashes,
including actual NGINX configure and the unchanged canonical lighttpd patch,
Bash autogen and configure path. `native-context-integrated1/manifest.json`
records development source and dirty status. This does not prove new zero
parsing/include counts. All independent connector targets and required variants
must remain covered; no partial Compilation Database was substituted.

Official CFamily documentation excludes C/C++ taint in AutoConfig and with
multiple code variants; whole-project reasoning also assumes one linked target.
A reporting-standard override or improved score does not prove taint coverage.
The Python simulation-cost boundary and both predecessor warnings retain their
baseline counterevidence and are not claimed as PR regressions. Scanner CLI
8.2.0.6438 and scan action 8.3.0 were checked against their official release and
input contracts; signed scanner installation and the language/report parameter
contracts remain in place.

### Architecture capability and readiness

A fresh model read confirmed the exact versioned patch: remove 14 excluded
Framework/MRTS groups, rename 30 Parent labels, retain Parent patterns,
metadata, four nested groups and constraints. The authorized retry again
returned HTTP 415 and readback remained identical, recorded in
`architecture-application-result.json`. The required media type is
`application/merge-patch+json`. Installed/latest published CLI `1.10.1.16776`
at `ef0f792b7c4bb18d2432015baae4984a6cd50d99` only supports JSON/form in its
released API and HTTP client; architecture commands in unreleased source are
not an installed supported route. The reviewed body needs a supported,
authorized merge-patch client integrated with the mandatory wrapper, followed
by exact model readback and a fresh scan proving perspective application.
No unverified UI import/editor route or credential-wrapper bypass is prescribed.
The architecture result remains `extern blockiert`.

Active master ruleset `19138299` requires `actions`, `bounded-c-cpp`,
`envoy-go`, `traefik-go`, `actionlint` and `zizmor`, all passed at the initial
head; strict current-base status and resolved review threads are required.
Required approvals are zero, reviews/threads were empty, and no CODEOWNERS was
found in the inspected locations. Classical branch-protection detail returned
403; this is not proof of absent ruleset enforcement. Local delivery policy
still requires the applicable current main Sonar gate.

The initial-head runtime workflow `40239931958` completed successfully for five
connectors and aggregate; Apache job `121309664630` proved the selected SQLi
HTTP 403/audit/cleanup result. Aggregate contract coverage was five passed,
zero failed, six blocked and thirteen not run, with `coverage_complete: false`
and `merge_eligible: false`. This is not a full matrix qualification. Current
artifact ZIP contents were not independently verified. All 18 initial-head
non-Sonar PR workflows passed; those results cannot validate the next head.

The source fixes are locally validated, the individual False Positive decisions
are applied and read back, native scanner closure remains `weiterhin offen`,
and documented taint/Python/FIFO limits remain `begründete Analyzergrenze`.
Final clean-head issue inventories, per-project source SHA/analysis/terminal
processing/gates/imports/warnings and CI are still required. PR #421 remains
Draft while required proof or architecture application is missing. No merge,
master change, gate relaxation or broad exclusion occurred. The coordinator
records the eventual exact final source/head results in the PR and current
closeout; this development-phase record does not claim completion.

### Documentation validation for this phase

The four documentation edits passed the following actual commands in the task
worktree. Variable references: 101; bilingual checks, repository paths and
Framework-owned native link checker: passed. The Change Record check proves
structure only, and whitespace passed. A separate comparison confirmed identical
technical inline-literal counts and fenced code blocks in both EN/DE pairs.
These documentation checks do not establish final CI, Sonar closure or runtime
qualification; those remain the coordinator's exact-head verification work.

```text
rtk make check-variable-documentation check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
rtk bypass /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check
rtk bypass git diff --check
```

### Complete triage and annotation/source-encoding follow-up

The [complete individual triage](../../../docs/sonarqube-pr421-triage.md) records all 150 main issues and separate 31/16 advisory New-Code issues, including code/flow context, quality/severity, action and proof. These totals reconcile every unique ID with the API page totals; they are not a Security-only selection. The current closeout supersedes older no-transition/current-count wording while retaining its dated evidence.

All 92 GitHub annotations were actually retrieved and reconciled using the installed authenticated GitHub CLI after the plugin rejected that endpoint. Categories are 50 Sonar inline issue references, 36 runner-image notices, two Go-cache warnings, three scanner-exit annotations and one CodeQL fallback warning. Annotation levels/counts are not additional Sonar issues or CI-job conclusions. The same supported CLI read proves classic branch protection absent (404); active ruleset `19138299` is authoritative.

The two cache warnings correspond to actual missing-root-module lookup. `.github/workflows/ci-security-codeql.yml` now uses existing Envoy `go.mod`/`go.sum` and Traefik native `go.mod` through `cache-dependency-path`, without manufacturing a root module/checksum or disabling caching. Trusted Go-version resolution, CodeQL lock/build/permissions are unchanged. Actionlint and Zizmor passed for both modified workflows; three existing CodeQL version/lock/permission methods passed in 0.005 s. Current-head CI must confirm warning closure.

`connectors/envoy/config/lib/tls_yaml_render.sh` had a literal CR inside its valid rejection pattern: Git blame enumerated 28 LF lines, universal readers 29. Representing that same byte via quoted `$(printf '\r')` leaves matching/escaping/status unchanged and gives 28/28 source lines. Twelve actual before/after Shell controls match status/stdout/stderr; two existing TLS methods passed in 0.088 s. `tests/test_envoy_transport_hardening_contract.py` now exercises both rejected LF and CR paths without output. This fixes source representation, not runtime acceptance; the next scanner must prove blame recovery. No new PR-caused regression is asserted. The native test's unused-path fixture was also moved before `assertRaises`; its existing negative method passed in 0.001 s.

Local real full header preparation and the 80-method measured Python producer passed; all such development evidence is marked dirty and is not a clean-head coverage import. Independent full diff review covered all 37 changed paths before the new triage pair; no confirmed code/test regression was found. Final documentation checks now include 103 variable references. All source corrections still require a new exact-head scan, full old/new issue comparison and terminal CI; no merge or readiness claim is inferred from these local results.
