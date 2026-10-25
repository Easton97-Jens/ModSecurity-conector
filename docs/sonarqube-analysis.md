# SonarQube Cloud analysis

**Language:** English | [Deutsch](sonarqube-analysis.de.md)

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
| Python | `ci/`, `scripts/`, `common/`, connector tools, tracked `.codex/bin/`, `tests/` | Python files under `tests/`, distributed connector test modules, and their test helpers are tests; operational tools remain sources. | `.python-version` pins `3.14.7`; `sonar.python.version=3.14` uses Sonar's required major/minor format. |
| Go | `connectors/envoy/ext_proc`, `connectors/traefik/native_middleware`, `connectors/traefik/composite_middleware`, `connectors/traefik/response_observer` | `**/*_test.go` are tests; other Go files and each `go.mod` stay in source scope. | Four modules; `.go-version` is `1.27.1`, while the module language directives are `1.26.5`. Coverage generation must run inside each module. |
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

CI now installs the existing Apache/APR/ModSecurity header prerequisites and
compiles a C17 header probe. Supported `sonar.cfamily.customCIncludes` and
`sonar.cfamily.customCppIncludes` supply `/usr/include`, `/usr/include/apache2`
and `/usr/include/apr-1.0` to AutoConfig. A local real Apache C17 source compile
also passed during remediation development. These checks establish installed
header/build context, not resolved Sonar includes or hosted runtime behavior.
NGINX, HAProxy and lighttpd generated host contexts remain incomplete in this
scan; inspect fresh parsing/include diagnostics before claiming improvement.

Headers are analyzed through including translation units. CFamily whole-project
reasoning assumes a single linked target, while this Parent contains independent
connector executables. AutoConfig also does not support C/C++ taint analysis.
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
Python `3.14.4` and Go `1.27.3`; CI pins remain Python `3.14.7` and Go `1.27.1`.
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
| Python | `sonar.python.version=3.14` uses major.minor; genuine Cobertura XML uses relative source filenames with branch and subprocess measurement. |
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

| Original finding | Current disposition before final-head server verification |
| --- | --- |
| Main Security Rating E | `weiterhin offen`: confirmed input-boundary causes are being repaired; issue/rating closure needs fresh readback. |
| Main new-code coverage 0.6% | `weiterhin offen`: genuine broader producers exist; 80% on the accumulated baseline is not established. |
| Missing native includes / parsing errors | `weiterhin offen`: installed Apache/APR/ModSecurity headers and real build checks improve available context; fresh analyzer deltas remain unverified. |
| Full-Parent C/C++ taint under AutoConfig | `begründete Analyzergrenze`: unsupported mode and independent-target assumptions remain explicit. |
| Python intended model ignored | `extern blockiert`: exact model correction is prepared; required PATCH media type is unsupported by the authorized CLI. |
| JSON/YAML/workflow scope loss | `behoben und nachgewiesen`: targeted local regressions prove the guard; analyzer execution remains a separate check. |
| Six Shell parse warnings | `weiterhin offen`: five files have equivalent rewrites; all six parse locally, but fresh Sonar acceptance is required. |

Every reported Shell file uses `#!/bin/sh` and passed `sh -n`, `bash -n` and
ShellCheck's error-level check. Dynamic octal expressions in Apache cleanup
were rewritten through explicit octal variables. Background heredoc producers
in Envoy, lighttpd and HAProxy now use a subshell with `exec`, preserving `$!`
process identity. HAProxy architecture case patterns have explicit no-op arms.
The scheduler's `exec 8<>"$candidate"` retains its necessary read/write FIFO
semantics.

| File | Local classification and change |
| --- | --- |
| `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh` | Valid POSIX octal arithmetic; explicit octal variable preserves permission masks. Sonar result unverified. |
| `connectors/envoy/harness/run_envoy_composite_matrix.sh` | Valid background heredoc; subshell plus `exec` preserves arguments, redirections and PID. Sonar result unverified. |
| `ci/runtime/lifecycle/run-full-matrix-parallel.sh` | Valid read/write FIFO redirection; unchanged because separate opens alter blocking/EOF behavior. Sonar result unverified. |
| `connectors/lighttpd/harness/run_patched_full_lifecycle.sh` | Valid background heredoc; equivalent subshell/`exec` form. Sonar result unverified. |
| `connectors/haproxy/htx-overlay/resolve-modsecurity.sh` | Valid quoted case patterns; equivalent combined patterns and explicit `:` bodies. Sonar result unverified. |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | Valid background heredoc; subshell/`exec` preserves optional `setsid` and PID. Sonar result unverified. |

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
readback confirmed no mutation. An administrator must apply the prepared model
through the intended-architecture editor or an authorized client supporting that
media type, then rerun analysis and confirm perspective application. No wrapper,
credential or authentication workaround is authorized by this document.

Final-head CI/Sonar links, terminal processing, main/advisory gates, language
execution, report imports and per-warning after-results must be recorded in the
Change Record when observed. A successful upload, an older green result,
`warningCount=0` or an advisory job conclusion alone is insufficient.

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
