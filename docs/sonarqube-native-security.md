# Native target security analysis

**Language:** English | [Deutsch](sonarqube-native-security.de.md)

SDK preparation and all twelve targets use `ubuntu-26.04`; [current readiness](pr-382-merge-readiness.md) binds delivery and outstanding dispositions.
## Scope and current status

The existing [broad Parent analysis](sonarqube-analysis.md) remains authoritative
for Python, Go, Shell, GitHub Actions, JSON/YAML and the complete configured
Parent source scope. Only root `modules/**` and root `reports/**` are excluded.
Its CFamily AutoConfig scan remains in place; it cannot establish C/C++ taint
analysis. The separate [native workflow](../.github/workflows/sonar-native-security.yml)
adds a compilation database for each of twelve real build targets.

At published Parent `011cb197`, [run 40392396874](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40392396874) completed SDK preparation and all twelve native build/capture/index/CTU/taint analyses: 611 aggregate compilation units, zero partial units and 100% indexing in each target. Before individual triage, three native gates passed and nine failed. Twenty of 22 workflows passed; the broad C++17/20/23 gates failed. Source review validated 12 Python security issues and 39 native issue instances as false positives; all 36 main/advisory Python instances and 39 native instances are individually resolved as false positive with fresh readback. Original job conclusions remain unchanged. This analysis predates the finite closure commit and is not final-head acceptance. See [central status](pr-382-merge-readiness.md).

Coverage is outside the user's security and merge criteria.
`sonar.coverage.exclusions=**` changes coverage only. Security rules, source
analysis, Quality Gates and the wait for server processing remain enabled.
Existing organization profiles and gates are not replaced.

## Independent targets

Each target has its own project in organization `easton97-jens`. Its key is
`Easton97-Jens_ModSecurity-conector_native_` followed by the target ID with
hyphens replaced by underscores. Independent executables and modules never
share a combined database: CFamily taint and CTU assume one linked target.

The table retains historical development capture expectations, including Parent include
inputs derived from actual compiler dependencies. These are not server-indexed
counts. The twelve targets contain **611 Parent TU compilations in aggregate**;
Common files recur across targets, so this is not a unique-file count.

| Target ID | Parent TUs | Parent include inputs | Expected Parent indexed inputs | Additional build context |
| --- | ---: | ---: | ---: | --- |
| `traefik-engine-service` | 64 | 75 | 139 | Canonical engine service |
| `haproxy-spoa-runtime` | 50 | 62 | 112 | Canonical SPOA runtime |
| `apache-native-module` | 33 | 46 | 79 | Installed APXS/APR context; bounded GCC LTO limitation below |
| `haproxy-htx` | 44 | 58 | 102 | 179 pinned upstream TUs |
| `envoy-ext-proc` | 64 | 75 | 139 | 22 Go/generated context TUs |
| `envoy-composite` | 64 | 75 | 139 | 22 Go/generated context TUs |
| `lighttpd-patched-module` | 62 | 71 | 133 | Pinned configured host headers |
| `nginx-dynamic-module` | 33 | 51 | 84 | One generated host-glue TU |
| `lighttpd-stock-sidecar` | 61 | 71 | 132 | Split build matches the canonical artifact |
| `envoy-ext-authz` | 67 | 77 | 144 | Canonical service |
| `traefik-forwardauth` | 68 | 78 | 146 | Canonical ForwardAuth service |
| `common-targeted-evaluator` | 1 | 0 | 1 | Original C++17 evaluator; canonical artifact parity |

The C++ target compiles `common/scripts/modsecurity_targeted_eval.cc` with
`-std=c++17 -Wall -Wextra -Werror` and a durable namespace for the selected SDK.
Its development artifact matches the canonical compile/link producer byte for
byte. The evaluator is not executed. No C++23 override is applied to this build.

## Build and source identity

[`prepare-sonar-native-ci.py`](../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_ci/checks/analysis/prepare-sonar-native-ci.py)
checks the exact clean checkout revision. It initializes only the directly
pinned Framework, builds the canonical shared ModSecurity `3.0.17` SDK, and
transfers its prefix and Expat dependency in a same-run archive. Revision,
Framework/source identity, build provenance, archive digest and library digest
must agree. Archive member and link admission constrain restoration to the
fixed external prefix subtree.

The matrix downloads the exact artifact ID and reuses the SDK producer's
external root through job outputs. A failed-native-job retry therefore keeps
the successful SDK's identity instead of inventing a new `run_attempt` path.
Builds, caches, compilation databases and scanner work remain outside the
checkout. Existing shared-write ancestry is rejected before output creation or
permission changes.

The helpers in [`sonar-native-security/`](../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_ci/checks/analysis/sonar-native-security/)
capture successful real compiler invocations, dependencies, compiler identity,
object/archive inputs and the declared link graph. Export requires the exact
Parent TU closure and its actual included Parent headers. External upstream or
Go-generated TUs remain verified build context; their presence in a database
does not claim their indexing as Parent source.

Producer-owned source mapping changes the compiler operand before execution
and verifies equal ordered include contents. It does not rewrite a captured
database to pretend copied files were original inputs. CGo provenance retains
the official Go link/FIPS/build-ID producer chain. The Apache exception admits
only observed GCC internal LTO/debug temporaries inside the invocation's
private temporary directory; original Parent objects still require producers.
Their transient bytes are not retained, so this is not a complete final-ELF
provenance claim. Host runtime qualification is outside these build proofs.

## Analysis and credential boundary

Both jobs restrict execution to this repository's master pushes and
same-repository PRs. Checkout uses the exact analyzed SHA, read-only GitHub
permissions, no persistent credentials and no recursive submodules.
`SONAR_TOKEN` exists only on the official scan step. The reviewed whole-workflow
contract binds steps, scripts, defaults, environment, matrix, project and SCM
identity; canonical Action updates must match the lock.

The official scan Action is pinned to `v8.3.0`; CLI `8.2.0.6438` retains signature
verification and JRE provisioning. Generated `project.settings` preserves the
exact Parent TU/header scope without inheriting the root source/test layout.
The scanner runs from the verified checkout root. The configuration requests:

- `sonar.cfamily.taintAnalysis=true` and no explicit taint timeout;
- `sonar.cfamily.ctuAnalysis.branchSubstring=all branches` with filesystem cache;
- at most two analyzer threads, memory-pressure failure at `95`, and disk/RAM
  preflight based on captured units;
- terminal Quality Gate waiting with a `600` second server timeout.

The published run above proved actual CTU/taint and indexing for all twelve targets. A successful upload alone remains insufficient; later revisions require their own analyzer/server results. The first native PR analysis completed successfully; no baseline prerequisite blocked it.

## Remaining depth and evidence limits

Header-only C++ wrappers without a captured real consumer and the three I12
instrumentation C++ sources remain in the broad AutoConfig source scope;
this workflow does not establish taint analysis for them. External SDK/upstream
implementation, Go/C cross-language flows, unsupported file formats and actual
host behavior are not qualified by these target captures.

Historical I12 host, matrix and Oracle campaigns stay closed. Connector E2E
selection remains `26`; no `I12_COMPLETE` or runtime promotion is produced.
Framework CLI/updater work is separate in
[Framework PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138).
Framework revision `03da9353561bf632a1f7bfc71b0a2671ec7aa257` passed all twelve CI workflows and Sonar and is Ready; no Framework merge was performed. Parent Framework gitlink `99a7985c1be92a2297b1b59208f64df6768f2cbf` and MRTS remain unchanged. Broker #422 is already authorized and merged at `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`; no further master merge is authorized.

The automatic selection is now 100 expanded cases / 80 executions, including three guard controls. A further 1893 cases / 839 executions are available only through explicit on-demand selection. Automatic coverage catalogue commands were removed; the retained collector requires `--on-demand`. Coverage is irrelevant to merge by user instruction. Broad source/scanner/gate analysis remains enabled, with only root `modules/**` and root `reports/**` excluded.

Individual false-positive disposition readback and final-head acceptance remain in [central status](pr-382-merge-readiness.md); the observed run is not transferred to unpublished changes.

## References

- [CFamily analysis modes](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/analysis-modes), [target scope](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/understanding-the-analysis), [taint and CTU configuration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis).
- [Deprecation announcements](https://docs.sonarsource.com/sonarqube-cloud/deprecations-and-removals#deprecation-announcements); current language and toolchain limits remain in the [broad guide](sonarqube-analysis.md).
- [Change Record](../reports/audits/change-records/CR-20261026-sonar-native-security.md).
