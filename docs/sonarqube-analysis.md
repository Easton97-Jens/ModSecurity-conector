# SonarQube Cloud analysis

**Language:** English | [Deutsch](sonarqube-analysis.de.md)

## Project and analysis method

The Parent repository uses one SonarQube Cloud project,
`Easton97-Jens_ModSecurity-conector`, in organization `easton97-jens`. The
organization key was read from the authenticated project API, not derived from
the GitHub account name. One scan covers the maintained Parent components.
Framework and MRTS remain independent repositories and analysis boundaries.

These four similarly named mechanisms are distinct:

| Mechanism | Configuration and decision |
| --- | --- |
| Cloud Automatic Analysis | Runs on Sonar's infrastructure; reads `.sonarcloud.properties`, ignores `sonar-project.properties`, and cannot import coverage. Keep disabled for this project. |
| CI-based SonarScanner CLI analysis | The selected method: `.github/workflows/sonarqube.yml` runs the full Parent scan using `sonar-project.properties`. |
| CLI automatic configuration | `sonar.scanner.autoconfig.enabled=false` preserves explicit source/test classification. Enabling it would ignore the manual source/test settings and generate warnings. |
| CFamily AutoConfig / Compilation Database | C/C++ analyzer modes within the CI scan. AutoConfig deduces compilation options; Compilation Database consumes real build commands through `sonar.cfamily.compile-commands`. This project selects AutoConfig. |

The workflow pins the official scan action to
`d209202bc7d53ff1cc128f7f907dac145c9d6ae9` (`v8.3.0`) and explicitly selects
SonarScanner CLI `8.1.0.6389`. Scanner signature verification stays enabled.
The scanner configuration is manual; CFamily AutoConfig remains independent of
`sonar.scanner.autoconfig.enabled`.

Authenticated discovery on 2026-10-25 found Cloud Automatic Analysis explicitly
disabled and CLI automatic configuration disabled through the effective default.
An earlier default-branch analysis that day used automatic analysis with scanner
`7.2.0.5079` and reported both missing Python-version and test-scope warnings.
Those historical results do not validate the new configuration. This change does
not alter external project settings, rules, profiles, or Quality Gates.

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

The existing `make compile-db-nginx-c17` and `make compile-db-cpp17` capture
NGINX/Common and the targeted evaluator respectively. They do not provide a
complete six-family compilation database or every C test/fixture translation
unit. Selecting that incomplete database would silently narrow analysis to its
intersection with the source scope. AutoConfig therefore preserves the broader
Parent translation-unit scope without inventing compiler commands or adding
host toolchains merely for scanning. See the [build guide](build/README.md).

Current build contracts predominantly use C17; the targeted evaluator uses
C++17 and legacy `connectors/traefik/build/build-starter.sh` uses C99. Host
includes, generated headers, feature defines, cgo flags, and optional C23/future-C
profiles vary by build. AutoConfig infers options and cannot prove that its
configuration matches every host/profile. The C++ reporting standard is pinned
to C++17; this controls rule applicability, not a successful C++ build. Do not
claim exact C17 compilation fidelity or inject one shared set of incompatible
host macros. Review AutoConfig quality warnings and the understood-code score.

Headers are analyzed only through source files that include them. Multiple
independent connector executables are presented as one project: CFamily assumes
one linked target for whole-project reasoning. Full-project rules, taint analysis,
and cross-translation-unit reasoning can consequently lose precision. No
per-connector scans overwrite the same project's apparent overall result.
A future database migration must capture the real commands, compare all intended
translation units against its entries, retain required includes/generated files,
and document supported variants and any omitted units before switching modes.

## CI, tests, and coverage

The workflow checks out the analyzed revision with full Git history. It uses the
existing `SONAR_TOKEN` secret name; discovery established the secret's presence,
not its value, validity, or analysis permissions. Keep the token in the scanner
step's environment only. Fork pull requests cannot receive repository secrets;
the privileged scan is skipped for them rather than executing untrusted code
through `pull_request_target`.

Test classification, test execution, test-execution-report import, and coverage
import are separate operations. A `sonar.tests` value does not run tests. Only
reports produced for the checked-out revision may be imported. Coverage reports
must exist, use a supported format, and reference files under this project base;
never generate empty replacement reports. Python and C/C++ coverage are not
claimed: no new Python coverage dependency or full native host coverage pipeline
is introduced by this configuration. Existing runtime tests remain separate
evidence and are not implied by a static-analysis result.

CI runs four existing single-scenario Go tests, one per module, after verifying
that each exact test name still exists. It writes native `go test -coverprofile`
reports below `$RUNNER_TEMP/sonar-coverage`, validates them with `go tool cover`
inside their modules, then imports the four real paths through
`sonar.go.coverage.reportPaths`. This is intentionally sparse package coverage:

| Module | Package / selected test | Report |
| --- | --- | --- |
| `connectors/envoy/ext_proc` | `./internal/responseobserver` / `TestClientFramesBoundedOrderedOperations` | `envoy.out` |
| `connectors/traefik/native_middleware` | `.` / `TestMiddlewareForwardsRequestAuthorityAsHostHeader` | `traefik-native.out` |
| `connectors/traefik/composite_middleware` | `.` / `TestStripInternalHeadersRemovesTrailerForms` | `traefik-composite.out` |
| `connectors/traefik/response_observer` | `.` / `TestResponseHeaderEncodingUsesLengthThenBytesOrder` | `traefik-observer.out` |

These four cases do not exercise all module packages, Envoy's `libmodsecurity`
build-tagged CGo integration, alternate platforms, or every connector runtime.
No test-execution reports are imported. A measured zero or low coverage remains
visible; no coverage exclusion or Quality-Gate threshold is relaxed.

## Validation and maintenance

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

The scope checker compares the Python minor, preserves all maintained code and
C/C++ tests, checks all four `go.mod` files, and emits full tracked path lists.
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

## Official references

- [SonarScanner CLI and automatic configuration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/scanners/sonarscanner-cli)
- [Cloud Automatic Analysis](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/automatic-analysis)
- [Initial scope](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/setting-analysis-scope/setting-initial-scope) and [path patterns](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/setting-analysis-scope/excluding-files-based-on-patterns)
- [CFamily modes](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/analysis-modes), [configuration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis), and [actual analysis scope](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/understanding-the-analysis)
- [Python](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/python), [Go](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/go), and [Shell](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/shell)
- [GitHub Actions](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/github-actions), [JSON](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/json), and [YAML](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/yaml)
- [Coverage](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/overview) and [coverage import parameters](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/test-coverage-parameters)
- [Pinned scan action](https://github.com/SonarSource/sonarqube-scan-action/tree/d209202bc7d53ff1cc128f7f907dac145c9d6ae9)
