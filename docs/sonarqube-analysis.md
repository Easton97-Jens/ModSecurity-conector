# SonarQube Cloud analysis

**Language:** English | [Deutsch](sonarqube-analysis.de.md)

## Integration into PR #382

Master `7a44f18edac729291d6551d068da64fa3fec4e1e` (PR #421) remains authoritative. Its fixed 13-entry `PYTHON_TESTS`, 37 Go selectors and native Common assessment are retained. Python additionally measures admitted offline exact IDs with actual branch tracing in guarded children; only selected children receive `ON_DEMAND_TESTS=1`. This preserves process/network guards and does not reopen historical I12 campaigns or restore the removed PR-specific collector/custom gates. All CFamily inputs remain MAIN; 16 actual CI Python unittest modules are TEST, with scope-guard evidence separate from analyzer execution. The workflow budget increases to 60 minutes after the measured offline collection/reporting interval alone was at least 1216.9 seconds.

The [current PR #382 status](pr-382-merge-readiness.md) owns current counts, measurements, pending raw-retention rerun and delivery limits. Published head `67e363d44d5f6be7119eb6d76ade11ac75e95f42` failed required Sonar with 118 new findings and 0.81499% New-Code coverage against 80%; local remediation has no new published-head gate proof. A first genuine local Python XML covers 374 files; local changed-Python coverage is 24.791%, not a Sonar result. `xml --keep-combined` and independent SHA/size-bound raw child-witness copies address implicit-combine deletion; a fresh full retention measurement is still required. No exclusion, baseline, threshold or gate condition is weakened.

The PR #421 source/server/runtime records below, including sections labelled current measured closure, are historical for their explicitly named revisions, especially `d5450cd3`; their 80 Python methods are not current expanded case counts and their successful gates do not qualify PR #382. Toolchain remains Python `3.15.1`, Go `1.27.3`, module language `1.26.9`, setup-python `7.1.0` and Scanner CLI `8.2.0.6438`.

## Project and analysis method

The Parent repository uses one SonarQube Cloud project,
`Easton97-Jens_ModSecurity-conector`, in organization `easton97-jens`. The
organization key was read from the authenticated project API, not derived from
the GitHub account name. Every standard variant scans the same maintained Parent components.
Framework and MRTS remain independent repositories and analysis boundaries.

These four similarly named mechanisms are distinct:

| Mechanism | Configuration and decision |
| --- | --- |
| Cloud Automatic Analysis | Runs on Sonar's infrastructure; reads `.sonarcloud.properties`, ignores `sonar-project.properties`, and cannot import coverage. Keep disabled for this project. |
| CI-based SonarScanner CLI analysis | The selected method: `.github/workflows/sonarqube.yml` runs three full Parent scans using the same `sonar-project.properties`. |
| CLI automatic configuration | `sonar.scanner.autoconfig.enabled=false` preserves explicit source/test classification. Enabling it would ignore the manual source/test settings and generate warnings. |
| CFamily AutoConfig / Compilation Database | C/C++ analyzer modes within the CI scan. AutoConfig deduces compilation options; Compilation Database consumes real build commands through `sonar.cfamily.compile-commands`. This project selects AutoConfig. |

The workflow pins the official scan action to
`d209202bc7d53ff1cc128f7f907dac145c9d6ae9` (`v8.3.0`) and explicitly selects
SonarScanner CLI `8.2.0.6438`. Scanner signature verification stays enabled.
The scanner configuration is manual; CFamily AutoConfig remains independent of
`sonar.scanner.autoconfig.enabled`.

Authenticated discovery on 2026-10-25 found Cloud Automatic Analysis explicitly
disabled and CLI automatic configuration disabled through the effective default.
An earlier default-branch analysis that day used automatic analysis with scanner
`7.2.0.5079` and reported both missing Python-version and test-scope warnings.
Those historical results do not validate the new configuration. Existing canonical project settings, rules, profiles and Quality Gates remain
unchanged; the two new unbound advisory projects are described below.

## Language and component inventory

The initial source scope and test scope both start at `.`. Narrow test-inclusion
patterns distinguish the categories; Sonar also applies those patterns as source
exclusions. Paths resolve from the repository root. Initial scope paths contain
no wildcards; the inclusion/exclusion parameters support patterns.

| Language / analyzer | Maintained components | Source / test classification | Build information and limits |
| --- | --- | --- | --- |
| Python | `ci/`, `scripts/`, `common/`, connector tools, tracked `.codex/bin/`, `tests/` | Python files under `tests/`, distributed connector test modules, and their test helpers are tests; operational tools remain sources. | `.python-version` pins `3.15.1`; `sonar.python.version=3.15` uses Sonar's required major/minor format. |
| Go | `connectors/envoy/ext_proc`, `connectors/traefik/native_middleware`, `connectors/traefik/composite_middleware`, `connectors/traefik/response_observer` | `**/*_test.go` are tests; other Go files and each `go.mod` stay in source scope. | Four modules; `.go-version` is `1.27.3`, while the module language directives are `1.26.9`. Coverage generation must run inside each module. |
| C / C++ | `common/`, all six connector families, `tests/`, `fuzz/` | All C/C++ code, including tests, fixture modules, and fuzz harnesses, remains source code because CFamily does not support `sonar.tests`. | AutoConfig analyzes scoped translation units; headers require an including translation unit. The targeted evaluator uses C++17. |
| Shell | `ci/`, `scripts/`, `common/`, connector build/harness scripts | Maintained `.sh` scripts stay sources, including scripts under connector `build/` directories. | Bash/POSIX supported. Automatic recognition of `connectors/apache/build/apxs-wrapper.in` is not established; a scope entry alone does not prove shell analysis. |
| GitHub Actions | `.github/workflows/` and applicable action definitions | Real workflows are sources; intentionally invalid workflow fixtures are test data. | Dedicated Actions analyzer; generic YAML is not a substitute for workflow semantics. |
| JSON / YAML | `config/`, examples, workflow and runtime configuration | Maintained configuration stays in scope; negative fixture directories are test data. | The language API advertises both analyzers. `sonar.featureflag.cloud-security-enable-generic-yaml-and-json-analyzer=true` enables their documented opt-in; confirm execution in scanner logs. Generic analysis does not understand every host-specific schema or embedded language. |
| Other formats | Host `.conf`/`.cfg`, `.yaml.in`, Make/Autotools, TOML, Markdown, patches | Retained unless specifically excluded below. | No claim of dedicated semantic analysis for these formats. Secrets/text inspection, when applicable, does not replace a language analyzer. |

The inventory at base `9913026c1feec85a1862d22987689a1ebcef6d97` found 398 Python,
135 C, one C++, 103 `.h`, eight `.hpp`, 51 Go (23 Go test files), and 100 `.sh`
files. Counts describe tracked Parent files, not server-confirmed analyzed files.
No generated Go source or vendored source tree was found. Future file counts
must be derived from the current checkout rather than copied from this snapshot.

## Scope exclusions and defaults

| Area | Reason and treatment |
| --- | --- |
| `modules/ModSecurity-test-Framework/**` | Independent Git submodule, including nested MRTS; Parent analysis does not import or modify its code. |
| `reports/testing/generated/**` | Generated evidence; maintained generators remain in scope. Other reports and attribution files are not explicitly excluded. |
| `build/**`, `dist/**`, `ci-artifacts/**`, `verified-runs/**`; local outputs and caches | Root `/build/`, `/dist/`, `/compile_commands.json`, environments, dependency caches, and runtime outputs are already SCM-ignored. Keep SCM exclusions enabled. |
| Python / Go test inclusion patterns | Classification excludes these files from source indexing and avoids duplicate indexing; it does not exclude them from analysis. |
| `tests/fixtures/python-version-contract/*.yml`, `tests/fixtures/python-version-contract/*.yaml`, `ci/fixtures/zizmor/*.yml`, `ci/fixtures/workflow-permission-contract/*.yml` | Invalid/unsafe workflow samples and their controls are test data, not executable production workflows. Only these YAML files are excluded; Python/C fixtures remain in scope. |

Do not introduce `**/build/**`: it would hide maintained connector build scripts.
No connector or complete language is excluded to suppress findings. Go's analyzer
excludes `vendor` by default; no such maintained tree was found. Scanner defaults,
SCM ignore rules, file suffixes, size limits, inherited global settings, and
unreferenced headers can still reduce the actual analyzed set. Inspect scanner
logs and server file/language metrics rather than equating initial scope with
confirmed analysis. CI command-line properties override configuration-file
values, which in turn override project UI values; organization/global exclusions
must also be checked when troubleshooting missing files.

## CFamily build fidelity

The tracked Parent inventory at `9f44647593bac7947113558c6ad183ab118e80af`
contains 136 native translation units: 135 C and one C++. This includes native
tests, fixtures, fuzz code and CI probes. Existing `make compile-db-nginx-c17`
and `make compile-db-cpp17` capture only the NGINX/Common declaration and targeted
evaluator. Selecting those partial databases would remove other Parent units
from CFamily analysis. AutoConfig and the scope guard's database restriction
therefore remain until a real full-Parent build contract can be verified.

| Component | Real build context that a complete database must retain |
| --- | --- |
| Common | `ci/checks/common/check-common-helpers.sh` compiles all 58 `common/src/*.c` and runs helper, constructor and intervention tests. |
| NGINX | `make check-nginx-c17` needs configured host headers, including `objs/ngx_auto_config.h`, ModSecurity headers and connector/Common include paths. |
| Apache | `make check-apache-c17` obtains real options from `apxs` and APR configuration, then compiles the five connector sources and declared Common subset. |
| HAProxy | The C17 source check does not capture the HTX filter. `connectors/haproxy/htx-overlay/build-overlay.sh` builds it in a real host tree with host defines and ModSecurity. |
| Envoy | Connector/composite service builds use C17, pthread and ModSecurity; `ext_proc` uses the `libmodsecurity` CGo build tag and its Common runtime bridge. |
| Traefik | Engine-service builds use C17, pthread and ModSecurity with the C++ linker. The starter retains its separate C99 contract. |
| lighttpd | Module builds need generated `config.h`, `HAVE_CONFIG_H`, host API defines and pinned host headers. Stock sidecar and patched native contexts remain distinct. |

HTX's existing build copies Parent sources into an external host worktree. A
naive capture records those copied paths, which do not match Parent source
paths. Any mapping must prove identical source content while retaining the real
compiler arguments and headers; invented compiler rows are not acceptable.

CI installs the existing Apache/APR header prerequisites and compiles a C17
header probe. `ci/checks/analysis/prepare-sonar-native-context.py` prepares real
pinned NGINX and HAProxy source trees and the canonically patched lighttpd tree,
runs the actual required configure/autogen steps, and records archive, patch,
configuration and generated-header hashes. Supported
`sonar.cfamily.customCIncludes` and `sonar.cfamily.customCppIncludes` consume
those host paths alongside `/usr/include`, `/usr/include/apache2` and
`/usr/include/apr-1.0`.

The 2026-10-26 development correction also obtains official ModSecurity public
headers from the version approved by the pinned Framework contract and places
them before distribution headers. The distribution SDK `3.0.12` lacks cleanup
APIs used by the unchanged C++ evaluator; an actual negative syntax probe
confirmed that mismatch. The approved `3.0.17` headers passed the corresponding
syntax probe. The actual NGINX `src/http/v2` dependency directory is included
without inventing feature defines or changing the configured host profile.
The complete development preparation passed with 13 include directories and
11 generated/source hashes. This proves header preparation and the selected
compiler probe; fresh scanner diagnostics must establish the remaining parsing
and include counts. It does not establish hosted runtime behavior.

Headers are analyzed through including translation units. CFamily whole-project
reasoning assumes a single linked target, while this Parent contains independent
connector executables. AutoConfig and multiple code variants do not support C/C++ taint analysis.
Neither a higher quality score nor the C++ reporting-standard override proves
those analyses ran. A future database strategy must preserve every intended
unit and required host/profile context and account for the independent targets;
see the [build guide](build/README.md).

## Full-repository C++ standard scans

The workflow runs the complete Parent source/test scope three times. It does
not narrow newer-standard runs to the evaluator, a connector, or C++ files.
Python, Go, C, Shell, Actions, JSON and YAML retain the same configuration and
coverage producers in every variant. CFamily AutoConfig's documented
`sonar.cfamily.reportingCppStandardOverride` selects C++17, C++20 or C++23 rule
applicability and standard-dependent suggestions. Other languages retain their
own language contracts; this is static analysis, not a native compiler build.

| C++ target | Sonar project | Decision |
| --- | --- | --- |
| `c++17` | `Easton97-Jens_ModSecurity-conector` | Required canonical PR/main-branch result. |
| `c++20` | `Easton97-Jens_ModSecurity-conector_cpp20_advisory` | Full-Parent advisory result. |
| `c++23` | `Easton97-Jens_ModSecurity-conector_cpp23_advisory` | Full-Parent advisory result. |

The two public advisory projects were manually created in `easton97-jens` and
verified unbound to a DevOps repository, with Automatic Analysis already false.
They use their own `master` analysis branch explicitly, avoiding automatic PR
routing. They cannot replace the canonical project's PR result. Their relevant
quality-profile keys and `Sonar way` Quality Gate match the canonical project;
no rules, profiles or thresholds were weakened. C++20/23 support is not as
complete as C++17 support; retain analyzer limitations and failures visibly.

Only the two higher-standard jobs use `continue-on-error: true` through the
fixed matrix; `fail-fast: false` preserves all runs. Every scanner still waits
for its real server-side gate. The bilingual job summary records the actual
scanner/gate outcome, revision, project and Compute Engine task link, including
failures. Advisory projects hold the latest serialized snapshot per standard;
retain each task/analysis ID and exact SHA when comparing PRs. The authoritative
project alone retains normal PR decoration. The superseded evaluator-only
compiler jobs are removed.

## CI, tests, and coverage

The workflow checks out `${{ github.event.pull_request.head.sha || github.sha }}`
with full history and uses that revision for `sonar.scm.revision`. The existing
`SONAR_TOKEN` is exposed only to the scanner step. Fork pull requests cannot
receive it; no privileged `pull_request_target` execution is introduced.

Test classification, test execution, coverage generation and analyzer import
remain separate operations. `ci/checks/analysis/run-sonar-coverage.py` produces
real reports in fresh per-language directories below an external `--output-root`.
It records the SHA, checks checkout stability and requires a clean checkout for
CI. `--allow-dirty` is only for local development and marks reports as containing
uncommitted changes. No empty replacement reports or coverage exclusions hide
production-code gaps. A short external `--temp-root` avoids Unix-socket path
limits in tests.

Python uses the existing hash-pinned `coverage==7.17.0` dependency in an isolated
`$RUNNER_TEMP/sonar-python` environment. `ci/sonar-coverage.ini` measures Parent
production Python across the repository, including namespace directories and
subprocesses, with relative file paths. Its omissions follow independent
repository, test and generated-output ownership. Explicit scope, provenance,
artifact and report-security tests select meaningful behavior; the helper's
`PYTHON_TESTS` inventory is authoritative for this assessment. The XML validator
requires actual execution and resolvable repository files, and normalizes its
source root to `.` without modifying counters.

Go uses 37 named lifecycle/security scenarios from the helper's `GO_TESTS`
inventory. Each module runs `-mod=readonly -coverpkg=./... ./...`, retaining
unexecuted default-build packages in the measurement. `go tool cover` validates
each report. Missing selected test names fail visibly.

| Module | Report below `$RUNNER_TEMP/sonar-coverage/go` |
| --- | --- |
| `connectors/envoy/ext_proc` | `envoy.out` |
| `connectors/traefik/native_middleware` | `traefik-native.out` |
| `connectors/traefik/composite_middleware` | `traefik-composite.out` |
| `connectors/traefik/response_observer` | `traefik-observer.out` |

Native coverage comes from the existing Common helper, constructor and
intervention tests compiled with `-std=c17 -Wall -Wextra -Werror --coverage -O0`.
Actual `.gcda` execution counters are required. The matching GCC `gcov` generates
unique reports per instrumented object so independently compiled binaries do
not overwrite each other's measurements. All 58 Common C source files must be
represented; connector-host runtime coverage is not implied.

The Go and native producer processes themselves run under Python coverage.
`--language finalize-python` checks all three language manifests against the
same SHA, combines subprocess data with `--append`, regenerates and validates
the Python XML. The scanner imports `python/python.xml`, the four Go reports and
`native/gcov` using `sonar.python.coverage.reportPaths`,
`sonar.go.coverage.reportPaths` and `sonar.cfamily.gcov.reportsPath` respectively.
Only fresh scanner readback establishes successful import.

Development trials reported 185 production Python files, including honest
zeroes, and 71 gcov reports across 62 repository files, including all 58 Common
C files. The selected Go tests passed with module coverage of 27.5%, 65.3%,
69.0% and 61.6% in table order. Repeated Go block rows from different test
binaries must be merged rather than summed. These observations used local
Python `3.14.4` and Go `1.27.3`; that PR #421 source used CI pins Python
`3.14.7` and Go `1.27.1`. The PR #382 integration pins are listed above.
They are development evidence, not final-commit import or gate proof.

The selection does not execute every Parent test, alternate platform,
`libmodsecurity`-tagged Go integration or connector runtime. It does not establish
that the repository-wide compact default-suite target is already enforced.
No test-execution reports are imported, and coverage thresholds stay unchanged.

## Evidence input security

The baseline returned 46 unresolved vulnerability findings. Triage found
concrete controls or intended operator authority for 14; the remaining 32 trace
file-content paths requiring caller-side validation. A rating alone is not a
vulnerability proof, and no issue was accepted, suppressed or transitioned to
false positive merely to change the gate.

Confirmed gaps included JSON-selected private-job summaries, retained refresh
logs, NGINX report excerpts and manifest-selected cache hashes. Evidence must
not grant itself access to another host path. Consumers bind reads to roots
selected by the trusted invocation and use regular-file descriptors without
following links. Canonical read-only source fixtures and explicitly configured
external runtime/cache paths remain distinct allowed inputs. Report-provided
`build_root` or `log_root` cannot extend the allowlist. The exact changed
consumers, regression evidence and remaining limitations are recorded in the
[Change Record](../reports/audits/change-records/CR-20261025-sonar-setup-remediation.md).
Fresh Sonar issue/rating readback is still required to establish scanner closure.

Cache proofs accept a final SONAME alias only when its physical target is independently authorized inside the configured cache or as an exact approved file. The normal component producer forwards its trusted configured overrides to `update-runtime-reports.py --approved-component-file`; direct invocations can repeat this option for explicitly chosen installed files. A manifest cannot approve a file or a root for itself. Rejected references retain a visible `rejected` status and no digest.

## Validation and maintenance

The workflow follows the [official scan Action interface](https://github.com/SonarSource/sonarqube-scan-action#configuration): `scannerVersion=8.2.0.6438`, supported `args`, full checkout history and default OpenPGP verification. Report properties use paths relative to the project root, computed from the external runner directory; the reports themselves remain outside the checkout.

| Language | Applied documentation contract |
| --- | --- |
| C / C++ | Supported AutoConfig include settings and native `.gcov` import; partial compilation databases are not substituted for full Parent scope. AutoConfig cannot provide C/C++ taint analysis. |
| Go | The pinned Go 1.27 toolchain is supported. Each module keeps its `go.mod`, `*_test.go` classification and standard `-coverprofile` reports generated before scanning. |
| Python | `sonar.python.version=3.15` uses major.minor; genuine Cobertura XML uses relative source filenames with branch and subprocess measurement. |
| Shell | Bash and POSIX are the officially supported dialects. Retain actual shebangs, `.sh`/`.bash` source scope and behavior checks; local syntax success does not prove Sonar parsing. |
| Workflows / JSON / YAML | Dedicated Actions analysis and the documented generic JSON/YAML opt-in remain enabled; negative workflow fixtures retain their bounded treatment. |

When changing `.python-version`, update `sonar.python.version` to its major/minor
value in the same change when the minor changes; patch-only updates preserve it. Recheck all modules when updating `.go-version` or
`go.mod`; keep each module descriptor inside source scope. When adding tests or
fixture directories, review the classification patterns without moving CFamily
files into test scope. Run the repository's Sonar configuration validation and
the bilingual documentation/link checks through the required local execution
wrapper; record their actual results in the Change Record:

```sh
rtk bypass .venv/bin/python ci/checks/analysis/check-sonar-scope.py --json
rtk bypass .venv/bin/python -m unittest -v tests.test_sonar_scope
rtk make check-bilingual-docs
rtk make check-doc-links
```

The scope checker compares the Python minor, independently protects maintained
JSON/YAML and real workflows, preserves connector build scripts, C/C++ test
sources and distributed Python/Go test classification, checks all four `go.mod`
files, and emits full tracked path lists. Only the existing immediate negative
workflow-fixture directories receive their explicit separate treatment. A README
cannot substitute for analyzable component code or configuration.
It does not prove scanner execution or reproduce every SCM/analyzer default.
The central workflow/tool updater maintains the scan Action pin; review the
explicit `scannerVersion` separately when changing Scanner CLI.

Before enabling or rerunning CI, verify that Administration → Analysis Method
still has Automatic Analysis disabled. If it has been re-enabled, an authorized
project administrator must disable it before the CI scan; never run both modes
concurrently. Confirm the existing `SONAR_TOKEN` can execute analysis. No secret
rotation or external setting change is implied by this repository change.

For the actual PR head, retain the commit SHA, scanner version, Compute Engine
task ID and analysis ID. Wait for server processing to finish, then read the
Quality Gate for that exact analysis. Inspect the resulting warnings for the two
original Python messages and for new ignored-parameter, source/test, AutoConfig,
or missing-report warnings. A successful upload, local scope check, historical
analysis, or passing gate at another revision is not this confirmation. Keep
remaining findings and an inaccessible/pending/failed gate visible; never weaken
rules or thresholds to obtain a pass.

## Observed Cloud limits and external follow-up

The [PR #421 closeout](sonarqube-pr421-closeout.md) records the independent
issue-by-issue decisions, current-run marker repair, real pinned host-header
preparation, baseline analyzer-limit comparison and final runtime evidence.
Its revision-bound results and external actions supplement the historical
observations below; PR coverage does not qualify accumulated master coverage.

Authenticated readback reconfirmed baseline revision
`9f44647593bac7947113558c6ad183ab118e80af`, analysis
`52df415d-2c24-43a3-a63a-de6e79c37d60`, from
[run 40224506735](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40224506735).
The main gate was `ERROR`: new-code Security Rating E and coverage 0.6%, with
thresholds A and 80%. The `previous_version` period starts on 2026-05-14.
Paginated file readback contained 663 files and these new lines to cover:
Python 57,281; C 27,420; C++ 184; Go 6,284. This accumulated main-branch baseline
is different from a PR's changed-line gate. A green PR cannot be presented as
repair of the accumulated main-branch coverage.

The baseline used Scanner CLI `8.1.0.6389` and CFamily `6.85.0.102562`, reported
136 native units, quality 77.52/100, parsing errors in 414/2,260 functions and
115/1,132 unresolved project includes. C/C++ taint analysis was disabled by
AutoConfig. Python, Go, CFamily, Shell, GitHub Actions, YAML and JSON sensors
executed; the original missing Python-version/test-scope warnings were absent.
These are baseline observations, not results for a later SHA.

The first completed PR scan at `13b17cbedaa8b7d7fe382ae500052f1cac4ded16`
used Scanner `8.2.0.6438` and CFamily `6.85.0.102562`.
[Run 40231379831](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40231379831)
imported genuine Python, four-module Go and Common gcov reports. Server task
`AaF0ymveZaGJAnPJkdcR` completed `SUCCESS`, analysis
`d812ee4b-6300-430f-89e9-11f7eb7b7745`. The PR gate remained `ERROR` solely
on Security Rating E: three `S2083` findings at the descriptor reader's opens.
Independent attack/control review confirmed the configured-root, no-follow and
regular-descriptor controls; no server issue transition was made. New-code
coverage was 80.5%, passing 80%. Both advisory scans had failed gates.
All 136 native units remained analyzed; quality improved to 91.28/100, with
193/2,260 functions still having parsing errors and 46/1,132 project includes
still unresolved (previously 115). Missing NGINX, HAProxy and
lighttpd host/generated headers and the AutoConfig taint limit remain.
The Change Record contains complete baseline-finding dispositions and measured
results; follow-up head results must be verified separately in the PR.

The follow-up scan of `8f632bdd` in [run 40232441972](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40232441972)
also completed server processing and confirmed the resolver warning absent.
Five original Shell warnings are therefore resolved; the valid scheduler FIFO
form remains the single documented Shell parser limit. Gate and coverage remain
ERROR/E and 80.5%. Final documentation-only follow-up results are recorded in PR #421.

The following table is historical evidence for `13b17c` / `8f632bdd`, not the
current issue inventory. The complete 2026-10-26 continuation below and the
[closeout](sonarqube-pr421-closeout.md) supersede its open-issue decisions.

| Original finding | Historical disposition at those heads |
| --- | --- |
| Main Security Rating E | `weiterhin offen`: source fixes have regressions; PR gate remains E on three guarded descriptor opens. Counterevidence is documented without server transitions. |
| Main new-code coverage 0.6% | PR import `behoben und nachgewiesen` at 80.5%; accumulated master coverage remains `weiterhin offen` until a corresponding main analysis. |
| Missing native includes / parsing errors | Measured improvement to 91.28 quality and 193/2,260 functions with errors; remaining host contexts `weiterhin offen`. |
| Full-Parent C/C++ taint under AutoConfig | `begründete Analyzergrenze`: unsupported mode and independent-target assumptions remain explicit. |
| Python intended model ignored | `extern blockiert`: exact model correction is prepared; required PATCH media type is unsupported by the authorized CLI. |
| JSON/YAML/workflow scope loss | `behoben und nachgewiesen`: targeted local regressions prove the guard; analyzer execution remains a separate check. |
| Six Shell parse warnings | Five `behoben und nachgewiesen` at `8f632bdd`; scheduler `begründete Analyzergrenze`. |

Every reported Shell file uses `#!/bin/sh` and passed `sh -n`, `bash -n` and
ShellCheck's error-level check. Dynamic octal expressions in Apache cleanup
were rewritten through explicit octal variables. Background heredoc producers
in Envoy, lighttpd and HAProxy now use a subshell with `exec`, preserving `$!`
process identity. HAProxy architecture case patterns use separate arms, escaped
spaces and explicit no-op bodies.
The scheduler's `exec 8<>"$candidate"` retains its necessary read/write FIFO
semantics.

| File | Local classification and change |
| --- | --- |
| `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh` | Valid POSIX octal arithmetic; explicit octal variable preserves permission masks. Warning absent at `13b17c`. |
| `connectors/envoy/harness/run_envoy_composite_matrix.sh` | Valid background heredoc; subshell plus `exec` preserves arguments, redirections and PID. Warning absent at `13b17c`. |
| `ci/runtime/lifecycle/run-full-matrix-parallel.sh` | Valid read/write FIFO redirection; unchanged because separate opens alter blocking/EOF behavior. Warning persists at `13b17c`. |
| `connectors/lighttpd/harness/run_patched_full_lifecycle.sh` | Valid background heredoc; equivalent subshell/`exec` form. Warning absent at `13b17c`. |
| `connectors/haproxy/htx-overlay/resolve-modsecurity.sh` | Valid quoted case patterns still warned at `13b17c`; separate escaped-space patterns preserve behavior and removed the warning at `8f632bdd`. |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | Valid background heredoc; subshell/`exec` preserves optional `setsid` and PID. Warning absent at `13b17c`. |

The scheduler's minimal parser reproducer is:

```sh
#!/bin/sh
prepare() {
    if exec 8<>"$1"; then
        :
    fi
}
```

Do not replace that FIFO open with separate blocking opens or exclude its file.
The fresh scan must individually confirm the six files listed in the Change
Record; local syntax success alone is insufficient.

The server model `py Intended Model` contains 46 top-level groups. Its 44
invalid labels contain `/`: 30 belong to Parent and 14 refer to excluded
Framework/MRTS. The exact reviewable request body is
[`config/analysis/sonar-python-architecture.patch.json`](../config/analysis/sonar-python-architecture.patch.json).
It removes only those 14 external groups, renames the 30 Parent labels with `_`,
and retains all Parent patterns, metadata, four nested groups and the existing
empty `constraints` list. It does not delete the perspective or invent new
architecture constraints. Both advisory projects currently have zero models.

Main project UUID: `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2`; model ID:
`cb04d3a3-7c8f-447c-99f0-ca49c97f054f`. Authenticated reads use
`/api/v2/architecture/models?projectId=608d0a7b-481a-4f7e-acbf-ae8eb07c3be2`.
The authorized update through `/usr/local/bin/sonar-with-env` and CLI `1.10.1`
returned HTTP 415: `PATCH /api/v2/architecture/models/cb04d3a3-7c8f-447c-99f0-ca49c97f054f`
requires `application/merge-patch+json`, while this CLI has no supported media-type
option. Effective `architectureadmin`/`admin` roles were present; subsequent
readback confirmed no mutation. The repeated authorized request on 2026-10-26 again returned HTTP 415; readback
confirmed the model unchanged. Installed CLI `1.10.1.16776` is the latest
published release. Its released API implementation supports JSON/form content
types, with no header override; architecture commands on unreleased upstream
code do not provide a supported installed route. Apply the exact reviewed body
through a supported, authorized client with that media type integrated with the
mandatory authentication wrapper; read back the unchanged Parent patterns,
nested groups and constraints, then run a fresh analysis proving perspective
application. No verified UI editor/import route is asserted. No wrapper,
credential or authentication workaround is authorized by this document.

Final-head CI/Sonar links, terminal processing, main/advisory gates, language
execution, report imports and per-warning after-results must be recorded in the
Change Record when observed. A successful upload, an older green result,
`warningCount=0` or an advisory job conclusion alone is insufficient.

## Current measured source closure — 2026-10-26

Source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8`. All three CI analysis jobs and terminal server tasks succeeded; all gates are `OK`. This is exact source closure before the documentation commit. The following documentation head needs its own fresh CI/Sonar proof in the PR; these results are not transferred to it.

| Project | CE task | Analysis ID | Processing / gate | New-code coverage |
| --- | --- | --- | --- | --- |
| Easton97-Jens_ModSecurity-conector | `AaF2d1wrF1KaAz-ccYSb` | `5ca2a23e-9296-4c2d-8fbc-fa4d9a6b97eb` | `SUCCESS` / `OK` | 83.5% |
| Easton97-Jens_ModSecurity-conector_cpp20_advisory | `AaF2dvPAk-m4lzyjm-LE` | `fd25c86a-c9f5-4cb3-8cd5-6e2a3e59ba69` | `SUCCESS` / `OK` | 84.6% |
| Easton97-Jens_ModSecurity-conector_cpp23_advisory | `AaF2dqhewSmsgR9Bx97p` | `085ce801-0376-4963-9864-25391aae003b` | `SUCCESS` / `OK` | 84.6% |

| Project | Reviewed IDs | `FIXED` | `FALSE_POSITIVE` | OPEN/CONFIRMED | Hotspots |
| --- | ---: | ---: | ---: | ---: | ---: |
| Main PR 421 | 152 | 143 | 9 | 0 | 0 |
| C++20 advisory | 33 | 24 | 9 | 0 | 0 |
| C++23 advisory | 18 | 12 | 6 | 0 | 0 |
| Total | 203 | 179 | 24 | 0 | 0 |

The 203 distinct IDs comprise fully paginated starting inventories 150/31/16 plus six discoveries. Every ID was separately read back. All types in the New Code OPEN/CONFIRMED scope return zero, as do separate hotspot queries. The three new complexity IDs are actually `FIXED`; the three new Git-security IDs remain `FALSE_POSITIVE` with individually verified comments. No risk was accepted; no rule, threshold, gate condition or New Code requirement was weakened and no broad exclusion introduced.

All six unchanged gate conditions pass: reliability/security/maintainability each 1 against at most 1; `new_coverage` 83.5/84.6/84.6 against at least 80; `new_duplicated_lines_density` 0.0 against at most 3; `new_security_hotspots_reviewed` 100.0 against at least 100. No condition was ignored. The 83.5% is PR coverage, 84.6% advisory branch new-code coverage. Fresh separate master readback still confirms 0.6% overall coverage; this PR does not repair it.

All three scans retain 1,350 sources, 243 tests, 136 native translation units and four Go modules; one Python XML, four Go reports and 71 gcov reports were imported per project. Native quality remains 100/100: parsing errors in 0/2,263 functions, 0/6 classes, 0/33,778 statements; 0/1,132 unresolved project includes and zero external include residuals. This proves measured parsing/include closure, not C/C++ taint.

Remaining scanner warnings are separate from the 203 IDs: main 46 WARNs (44 architecture labels, FIFO parser, TLS file without changed lines), each advisory four WARNs (FIFO parser, two predecessor, FIFO syntax) plus the INFO simulation-cost skip at `ci/lib/runtime_path_utils.py:69`. C/C++ taint remains explicitly disabled in AutoConfig; multiple variants/independent targets remain separate limits. Missing TLS blame has disappeared, while the changed-lines warning remains. Python/FIFO limits have baseline counterevidence and are not asserted as PR regressions.

Terminal runtime proof belongs separately to source `900dddb49c43ec4479c4b75a91071cadb97893c4`, run `40267347652`: all six jobs succeeded including Apache; selected 403/CRS/audit/cleanup proof, not full matrix qualification. Details and artifact limits remain in the 900 section. The source scan does not transfer runtime proof to another head.

| Remaining item | Disposition after source proof |
| --- | --- |
| 203 issue IDs | 179 `behoben und nachgewiesen`, 24 proven false positives |
| Measured native parsing/include residuals | `behoben und nachgewiesen` |
| C/C++ taint, Python simulation-cost/predecessor, valid FIFO | `begründete Analyzergrenze` |
| Architecture model with 44 labels, repeated HTTP 415 and unchanged readback | `extern blockiert` |
| Remaining TLS changed-lines warning, final CI/Sonar at documentation head | `weiterhin offen` |

Source issues/gates are therefore closed; external architecture application and final-head verification still prevent a complete technical closure claim. PR #421 remains Draft, overall status **teilweise abgeschlossen/blockiert**. No merge or master change. Sources: `d545-evidence-summary.json`, `d545-analysis-bindings.json`, `d545-*-baseline-readback.json`, `d545-*-log-evidence.json` and separate hotspot readbacks in run `pr421-all-findings-20261026`.

## Historical source 900 state before final complexity closure

The source scan of `900dddb49c43ec4479c4b75a91071cadb97893c4` confirms
all 197 starting IDs: 176 analysis-`FIXED`, 21 individually justified
`FALSE_POSITIVE`. Six new IDs (one Git argument-injection and contract-decoder
complexity issue per project) remain separate in the
[per-issue triage](sonarqube-pr421-triage.md); the three new security IDs now have individually verified FP transitions
and the three complexity IDs still await rescan proof. Native parsing/include residuals are measurably repaired:
quality 100/100, 0/2,263 functions, 0/6 classes, 0/33,778 statements,
0/1,132 project includes and zero external include residuals with all
136 translation units retained. C/C++ taint remains explicitly disabled.

All three scans imported Python XML, four Go reports and 71 gcov reports.
PR coverage 83.3% and advisory branch new-code coverage 84.4% remain distinct
from accumulated master coverage. Fresh authenticated readback on 2026-10-26
at 04:25 UTC independently confirms master coverage 0.6%; the detailed
master-analysis binding remains in the closeout. The [closeout](sonarqube-pr421-closeout.md)
contains exact CE/analysis bindings, gate conditions and limits. At that scan,
gates were ERROR only for security rating 3. Architecture remains externally
blocked. Missing TLS blame is no longer reported; the changed-file-without-
changed-lines warning remains. Both CodeQL root-go.mod warnings are resolved;
a different Traefik module-cache log warning remains with successful analysis.
A later correction/documentation head needs its own current PR proof.
PR #421 remains Draft.

The development/older-scan sections below remain historical; their pending
statements for starting IDs and parsing residuals are superseded by this
source state.

## Complete PR issue continuation, 2026-10-26

The freshly paginated main-project query for PR #421 used
`sinceLeakPeriod=true`, `issueStatuses=OPEN,CONFIRMED` and all issue types:
100 plus 50 results, 150 distinct issues. This is 122 Shell and 28 Python
issues: 141 maintainability, eight security and one reliability issue. Legacy
severity counts are six MINOR, 116 MAJOR, 25 CRITICAL and three BLOCKER. The
separate advisory inventories under the same New Code/status scope are 31 and
16 issues; they are not the older total-vulnerability counts of 27 and 24.
Main security hotspots were separately checked: zero.

The verified starting source is `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3`.
All three corresponding server tasks completed successfully; before the new
individual decisions, their gates were ERROR. Genuine report imports yielded
82.3% main PR coverage and 83.7% advisory branch new-code coverage. Neither
value repairs accumulated master coverage. Later uncommitted development
changes and their local coverage cannot replace a clean-head CI import.

After independent complete-flow/source review and attack/allowed controls,
the newly explicit user authorization was used for 21 individual
`FALSE_POSITIVE` transitions with issue-specific comments: eight main, eight
C++20 and five C++23. Every status and matching comment was read back. No risk
was accepted and no rule, profile, gate or threshold was weakened. These
server decisions supersede the historical no-transition statements above;
new findings require their own review. The 142 main nonsecurity issues and
23/11 advisory nonsecurity issues have local code corrections pending a fresh
scan. Named POSIX function arguments, equivalent control-flow simplification
and Python complexity/test corrections preserve the relevant interfaces and
security controls. Actual before/after Shell characterization and the
instrumented 80-method Python selection passed. Six existing Envoy and twelve
HAProxy ShellCheck warnings remain unchanged; this is not a clean overall
ShellCheck result. The scheduler retains `exec 8<>` FIFO behavior.

The architecture application remains externally blocked as described above.
Native scanner closure, new-code issue counts and final-head CI/Sonar remain
open until a new clean source revision has terminal evidence for all three
projects. The Python simulation-cost and predecessor messages remain bounded
analyzer limitations with baseline evidence. PR #421 stays Draft while
required criteria are missing. The [Change Record](../reports/audits/change-records/CR-20261025-sonar-setup-remediation.md)
and [closeout](sonarqube-pr421-closeout.md) distinguish local repairs, actual
server decisions and remaining proof. No merge or master change is claimed.

## Official references

- [SonarScanner CLI and automatic configuration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/scanners/sonarscanner-cli)
- [Cloud Automatic Analysis](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/automatic-analysis)
- [Initial scope](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/setting-analysis-scope/setting-initial-scope) and [path patterns](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/setting-analysis-scope/excluding-files-based-on-patterns)
- [CFamily modes](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/analysis-modes), [configuration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis), and [actual analysis scope](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/understanding-the-analysis)
- [Python](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/python), [Go](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/go), and [Shell](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/shell)
- [GitHub Actions](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/github-actions), [JSON](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/json), and [YAML](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/yaml)
- [Coverage](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/overview) and [coverage import parameters](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/test-coverage-parameters)
- [Pinned scan action](https://github.com/SonarSource/sonarqube-scan-action/tree/d209202bc7d53ff1cc128f7f907dac145c9d6ae9)

- [Pinned Python coverage release and universal wheel](https://pypi.org/project/coverage/7.17.0/)
- [Python coverage import](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/python-test-coverage)

- [Manual project creation](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/administering-your-projects/setting-up-project)
- [DevOps binding](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/about-sonarqube-cloud-solution/resources-structure/binding-with-dop)

- [Native C/C++ coverage / Native C/C++-Coverage](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/c-c-objective-c-test-coverage)

- [Scanner CLI 8.2.0.6438](https://github.com/SonarSource/sonar-scanner-cli/releases/tag/8.2.0.6438)
- [CFamily taint analysis](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis#taint-analysis)
- [CLI 1.10.1.16776](https://github.com/SonarSource/sonarqube-cli/releases/tag/1.10.1.16776), [released API command](https://github.com/SonarSource/sonarqube-cli/blob/ef0f792b7c4bb18d2432015baae4984a6cd50d99/src/commands/api/api.ts), [released HTTP client](https://github.com/SonarSource/sonarqube-cli/blob/ef0f792b7c4bb18d2432015baae4984a6cd50d99/src/core/server/http-client.ts)
