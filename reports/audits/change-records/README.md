# Change Records

- [Parent CI library SonarQube Cloud remediation](CR-20260801-sonar-ci-lib-remediation.md)

**Language:** English | [Deutsch](README.de.md)

Change Records retain the decision, scope, tests, security impact, and known
limitations of non-trivial versioned changes. They are English/German pairs and
must not claim unobserved CI, runtime, review, or delivery results.

- [Parent Common Runtime SonarQube Cloud maintainability remediation](CR-20260801-sonar-common-runtime-maintainability.md)
  — covers the current 18-item `common/runtime/` inventory with bounded
  transaction-state grouping, const-correct parser/runtime views, C17 checks,
  and a finalized local security-diff review; exact-head hosted verification
  remains required before any integration.

- [Parent common/scripts SonarQube Cloud remediation](CR-20260801-sonar-common-scripts-remediation.md)
  — remediates the current local-smoke security and maintainability inventory
  through fixed loopback protocol, verified local execution/output boundaries,
  C++17 RAII cleanup, and decomposed control flow; exact-head hosted
  verification remains required before integration.

- [Parent CI evidence SonarQube Cloud remediation](CR-20260801-sonar-ci-evidence-remediation.md)
  — source-level fixes cover the current `ci/evidence` security, hotspot,
  maintainability, and duplication inventory without scanner workarounds;
  focused local controls passed, while exact-head GitHub Actions and
  SonarQube Cloud verification remain required before any merge decision.

- [Parent Traefik complete SonarQube Cloud remediation](CR-20260801-sonar-traefik-complete-remediation.md)
  — validates local executable and artefact boundaries, preserves native UDS
  lifecycle cleanup, and decomposes the current Traefik runner without scanner
  suppressions; the previous exact head passed hosted verification, while the
  current post-base-refresh head requires its own verification before merging.

- [Parent HAProxy complete SonarQube Cloud remediation](CR-20260801-sonar-haproxy-complete-remediation.md)
  — covers the current 33-item HAProxy inventory with C17, focused contracts,
  and a sealed security-diff review; exact-head hosted/SonarQube Cloud
  verification remains required before it can be considered mergeable.

- [Parent Envoy transaction-opener interface naming](CR-20260801-sonar-envoy-transaction-opener.md)
  — renames the remaining one-method internal Go interface to preserve its
  exact transaction-opening method set while meeting Go naming conventions;
  exact-head hosted/SonarQube Cloud verification remains required before any
  merge decision.

- [Parent Envoy TLS and maintainability remediation](CR-20260801-sonar-envoy-tls-maintainability.md)
  — removes the current five Envoy SonarQube Cloud source rows by preserving
  processor semantics and encrypting the fixture upstream hop; exact-head
  hosted verification remains required before any merge decision.

- [Parent Traefik runtime and lifecycle remediation](CR-20260730-sonar-traefik-runtime-lifecycle.md)
- [Parent CI checks SonarQube Cloud remediation](CR-20260801-sonar-ci-checks-remediation.md)
  — source-level fixes cover the current `ci/checks` security, hotspot, and
  maintainability inventory; focused local checks pass, while exact-head
  GitHub Actions and SonarQube Cloud verification remain required.

- [Parent CI runtime SonarQube Cloud remediation and verified-root hardening](CR-20260730-sonar-ci-runtime-security-root-remediation.md)
  — records the replacement diff’s verified focused local controls and bounded
  security impact; fresh exact-head hosted GitHub Actions and SonarQube Cloud
  verification remains required before integration.

- [Parent Envoy maintainability remediation](CR-20260730-sonar-envoy-maintainability-remediation.md)
  — preserves C17 bridge and ext_proc lifecycle behavior; local source,
  native-build, and loopback-TLS controls passed, while exact-head hosted
  verification remains required.

- [Parent Apache maintainability remediation](CR-20260730-sonar-apache-maintainability.md)
  — remediates the current 13-item Apache SonarQube Cloud maintainability
  inventory with focused C17 and native-harness evidence; exact-head hosted
  verification remains required before integration.

- [Parent CI GitHub URL-validation unused-parameter cleanup for SonarQube Cloud S1172](CR-20260730-sonar-ci-github-url-unused-label.md)

- [Parent HAProxy runtime maintainability remediation](CR-20260730-sonar-haproxy-runtime-maintenance.md)
  — table-driven SPOP parsing, explicit HTX EOS helpers, deterministic overlay
  artifact hashing, and CRS-load cleanup passed focused local controls. The
  Draft PR retains historical baseline work; exact-head hosted/SonarQube Cloud
  verification remains required before it can be considered mergeable.

- [Parent Common event JSON optional-field decomposition](CR-20260730-sonar-common-event-json-complexity.md)

- [Parent Common HTTP authorization-service const correctness](CR-20260730-sonar-common-http-auth-maintenance.md)

- [Parent CI tools output containment and native oracle decomposition for SonarQube Cloud](CR-20260730-sonar-ci-tools-output-oracle.md)
  — local containment, generator-compatibility, C17, native-oracle, and
  focused security-diff controls passed; fresh exact-head hosted and
  SonarQube Cloud verification remains required before any master integration.

- [Parent CI runtime-path-policy fixed-fixture literal ownership for SonarQube Cloud S1192](CR-20260729-sonar-ci-runtime-path-policy-literals.md)

- [Parent CI repository-path-reference complexity remediation](CR-20260729-sonar-ci-repository-path-reference-complexity.md)
  — a private per-document diagnostic seam preserves link/path validation;
  six direct tests passed, while the isolated whole-tree checker remains
  blocked only by absent Parent-pinned Framework link targets.
- [Parent CI runtime-cache four-column Markdown separator for SonarQube Cloud S1192](CR-20260730-sonar-ci-runtime-cache-separator.md)
  — one private separator preserves the component-cache and cache-index table
  output; the direct presentation regression passed locally, while hosted
  exact-head evidence remains pending.

- [Parent CI bounded bilingual design-route matcher for SonarQube Cloud S8786](CR-20260729-sonar-ci-bilingual-route-regex.md)
  — preserves padded and unpadded route keys while rejecting malformed
  no-closing-delimiter route rows with long whitespace without
  backtracking-heavy matching.

- [Parent CI Apache config-reference condition remediation](CR-20260729-sonar-ci-apache-config-reference-condition.md)
  — the source/minimal/safe Apache example-file partition now uses explicit
  branches; focused partition and non-writing reference controls passed
  locally. Exact-head hosted verification remains required before integration.

- [Parent CI generated-report literal deduplication](CR-20260729-sonar-ci-generated-report-literals.md)
  — five static local-path/provenance literals now have single private owners;
  focused portable-path and generator-registry controls plus the full
  generated-report evidence suite passed locally. Exact-head hosted verification
  remains required before integration.
- [Parent CI Nolog and response-header report-lifecycle deduplication](CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.md)
- [Parent CI NGINX HTTP-500 literal deduplication](CR-20260729-sonar-ci-nginx-http500-literal-deduplication.md)
- [Parent NGINX maintainability remediation](CR-20260730-sonar-nginx-maintainability.md)
- [Parent CI case-metadata parsing deduplication](CR-20260729-sonar-ci-case-metadata-duplication.md)

- [Parent CI No-CRS missing-case diagnostic literal deduplication for SonarQube Cloud S1192](CR-20260730-sonar-ci-no-crs-diagnostic-literal.md)

- [Parent Lighttpd runtime-output containment](CR-20260729-sonar-lighttpd-runtime-output-containment.md)

- [Parent HAProxy binding body-phase deduplication](CR-20260729-sonar-haproxy-binding-body-phase-deduplication.md)

- [Parent CI verified-runtime-mismatch control-evidence deduplication](CR-20260729-sonar-ci-verified-runtime-mismatch-duplication.md)

- [Parent Common blocked-runtime-smoke default dispatch for SonarQube Cloud S131](CR-20260729-sonar-common-blocked-smoke-default.md)
  — the tracked configuration case and unknown connectors now take controlled
  blocked-dependency paths; focused dispatch/default-structure controls and
  POSIX shell syntax passed locally.

- [Parent CI capability-state map deduplication](CR-20260729-sonar-ci-capability-state-map-deduplication.md)

- [Parent HAProxy SPOP body-parser deduplication](CR-20260729-sonar-haproxy-spop-body-parser-deduplication.md)

- [Parent Common event-provenance serialization decomposition for SonarQube Cloud c:S3776](CR-20260729-sonar-common-event-provenance-complexity.md)
  — protocol-provenance preservation and negative controls are documented;
  before integration, the synchronized exact head must pass GCC and Clang C17
  Common-helper controls, applicable Common contracts, and fresh hosted
  review/Actions/SonarQube Cloud verification.

- [Parent Common smoke-writer output-path containment for SonarQube Cloud security findings](CR-20260729-sonar-common-smoke-writer-path-security.md)
  — focused pre-/post-fix boundary checks, symlink and traversal negative
  controls, the legitimate private-runtime-root control, and related runtime
  smoke security tests passed locally. Open-PR delivery remains pending;
  exact-head hosted verification is required before master integration.

- [Parent Apache smoke-harness literal ownership and diagnostic streams](CR-20260729-sonar-apache-smoke-harness-maintenance.md)
  — six fixed Shell literals now have readonly owners, four diagnostics use
  stderr, and focused syntax, ShellCheck, Apache-contract, and bilingual
  checks passed. Before integration, hosted status must be read at the PR's
  exact current head.

- [Parent Apache RulesSet configuration-pool cleanup](CR-20260729-apache-ruleset-pool-cleanup.md)
  — selected upstream #94A cleanup, focused GCC/Clang APR harnesses, fresh
  APXS-header materialization, private HTTP/1.1 and graceful-restart controls
  are recorded locally; exact-head delivery, hosted checks, and resulting-master
  evidence remain pending.

- [Parent Envoy runtime-artifact containment and loopback TLS](CR-20260729-sonar-envoy-runtime-artifact-tls-containment.md)
  — focused temporary TLS, artifact-containment, config-materialization, Go,
  and Common-adoption controls passed where their prerequisites are available;
  the native Envoy/ext_proc runtime is blocked locally by the absent Envoy
  binary and Framework rule fixture. Before integration, hosted status must be
  read at the PR's exact current head.

- [Parent HAProxy HTX runtime-artifact containment](CR-20260729-sonar-haproxy-htx-runtime-artifact-containment.md)
  — synchronized to the current master base, restores the metadata-event test's
  private-root binding, and moves the duplicated HAProxy/Envoy descriptor
  protocol into one tested Parent primitive without changing connector-local
  serialization. The previous exact head failed only the New-Code duplication
  gate; fresh exact-head hosted verification remains required before master
  integration.

- [Parent CI focused-report helper deduplication and request-body path containment](CR-20260729-sonar-ci-focused-report-safety.md)
  — local traversal/symlink regression and legitimate in-root controls passed;
  the combined security review found no reportable regression. Exact-head
  hosted GitHub Actions and SonarQube Cloud evidence remain pending.

- [Parent CI runtime-readiness remediation-label deduplication for SonarQube Cloud S1192](CR-20260729-sonar-ci-runtime-readiness-fix-label.md)

- [Parent Common targeted-evaluator C++17 remediation](CR-20260729-sonar-common-targeted-evaluator-cpp17.md)

- [Parent HAProxy HTX payload-iterator deduplication](CR-20260729-sonar-haproxy-htx-payload-iterator-duplication.md)

- [Parent CI best-effort evidence-reader deduplication for SonarQube Cloud](CR-20260729-sonar-ci-best-effort-evidence-readers.md)
- [Parent CI block-status generator preprocessor-end literal for SonarQube Cloud S1192](CR-20260729-sonar-ci-generator-endif.md)
- [Parent HAProxy SPOE header-parser deduplication and SonarQube Cloud reliability remediation](CR-20260729-sonar-haproxy-spop-header-parser-duplication.md)
  — local C17 parser-harness, HAProxy adoption, standards-wiring, and C17 lint
  checks passed; a focused security diff review found no reportable regression.
  Hosted CI and exact-head SonarQube Cloud evidence remain pending.

- [Parent deterministic GitHub Actions `uses:` prefix parser for SonarQube Cloud S8786](CR-20260729-sonar-scripts-uses-prefix-parser.md)
  — focused updater tests, a non-writing parser comparison, syntax validation,
  and the complete current-diff security review passed locally; Draft-PR
  delivery and exact-head hosted/SonarQube Cloud evidence remain pending.
- [Parent Common runtime-smoke result-object refactor](CR-20260729-sonar-common-runtime-result.md)
  — local runtime-writer, CRS/path-security, and loopback request-body controls
  passed; the 52-line Common CPD block and two baseline `python:S107` rows are
  selected for hosted verification. No commit, push, PR, hosted analysis, or
  merge is claimed at record authoring.
- [Parent Common header validation and NGINX strict JSONL-tail deduplication](CR-20260728-sonar-common-nginx-strict-jsonl-duplication.md)
  — local Common C17, security, flow, and NGINX source-contract checks passed;
  memory safety passed outside the LeakSanitizer-incompatible sandbox, while
  NGINX C17 compilation is blocked_external_dependency by missing NGINX
  headers/source. No commit, push, PR, hosted analysis, or merge is claimed.
- [Parent NGINX response-mapper validation-tail deduplication candidate (36 Parent duplicate lines)](CR-20260728-sonar-nginx-response-mapper-duplication.md)
  — local source-contract and scoped whitespace validation passed; the exact
  C17 control is blocked_external_dependency by absent NGINX headers/source
  (script exit 77, make exit 2), and no host runtime, commit, push, PR, or
  hosted closure is claimed.
- [Parent CI marker-section and script-literal deduplication for SonarQube Cloud](CR-20260728-sonar-ci-marker-script-deduplication.md)
- [Parent Traefik start-smoke diagnostic-literal cleanup for SonarQube Cloud S1192](CR-20260728-sonar-traefik-start-smoke-literal.md)
- [Parent Apache Phase-4 control-literal ownership for SonarQube Cloud S1192](CR-20260728-sonar-apache-phase4-literals.md)
- [Parent Apache H2 transport-result literal ownership for SonarQube Cloud S1192](CR-20260728-sonar-apache-h2-transport-s1192.md)
- [Parent Envoy lifecycle literal ownership for SonarQube Cloud S1192](CR-20260728-sonar-s1192-envoy-lifecycle.md)
- [Parent Common event provenance short-circuit refactor for SonarQube Cloud c:S1066](CR-20260728-sonar-common-event-s1066.md)
- [Parent HTTP authorization CLI loop control for SonarQube Cloud c:S5955, c:S886, and c:S3776](CR-20260728-sonar-http-authorization-cli-scope.md)
- [Traefik result optional-text nullability remediation for SonarQube Cloud](CR-20260728-sonar-traefik-result-nullability.md)
- [Parent `tools/MRTS` literal extraction and direct Git-fixture coverage for SonarQube Cloud S1192](CR-20260728-sonar-bilingual-tools-mrts-s1192.md)
- [Parent HAProxy HTX diagnostic-range literal for SonarQube Cloud shelldre:S1192](CR-20260728-sonar-haproxy-htx-diagnostic-s1192.md)
- [Parent HAProxy append-string preflight for SonarQube Cloud c:S3519](CR-20260727-sonar-haproxy-append-string-s3519.md)
- [Parent common error duplicate-mapping refactor](CR-20260727-sonar-common-error-duplication.md)
- [Parent NGINX event metadata and JSONL writer deduplication: second-head Quality Gate and local S1192 follow-up](CR-20260727-sonar-nginx-event-metadata-duplication.md)
- [Parent report-generator conditionals and access-log regex for SonarQube Cloud](CR-20260727-sonar-report-conditionals-regex.md)
- [Parent Python generator conditionals for SonarQube Cloud python:S3358](CR-20260727-sonar-generator-conditionals.md)
- [Parent generated-report layout decomposition for SonarQube Cloud](CR-20260728-sonar-generated-report-layout-decomposition.md)
- [Parent runtime-mismatch control-path deduplication for SonarQube Cloud](CR-20260728-sonar-runtime-mismatch-control-path-deduplication.md)
- [Parent Lighttpd lifecycle literal deduplication for SonarQube Cloud](CR-20260728-sonar-lighttpd-lifecycle-literals.md)
- [Parent repository inventory complexity remediation for SonarQube Cloud S3776](CR-20260727-sonar-s3776-repository-inventory.md)
- [Parent shell dispatch-rule remediation for SonarQube Cloud S131 and S7679](CR-20260727-sonar-shell-dispatch-rules.md)
The leading entry records Draft PR #131's initial exact-head SonarQube Cloud
result—Quality Gate `OK` with zero new duplication and one task-owned
`python:S3358`—its local normal nested-conditional correction, and the absence
of a post-correction remote analysis or merge.

- [Parent connector-config-reference literal deduplication and SonarQube Cloud S3358 follow-up](CR-20260727-sonar-config-reference-literal-deduplication.md)
- [Parent compiler-guide literal deduplication for SonarQube Cloud S1192](CR-20260727-sonar-compiler-guides-literal-deduplication.md)
- [Parent test assertion-order remediation for SonarQube Cloud S3415](CR-20260727-sonar-s3415-parent-test-assertions.md)
- [Parent test-fixture duplication reduction for SonarQube Cloud](CR-20260727-sonar-parent-test-duplication.md)
- [Parent focused report-utility duplication reduction for SonarQube Cloud](CR-20260727-sonar-focused-report-utility-duplication.md)
- [Parent response-header fixture containment for SonarQube Cloud S8707](CR-20260727-sonar-response-header-fixture-containment.md)
- [Parent Apache/NGINX commented-code cleanup for SonarQube Cloud C:S125](CR-20260727-sonar-c-commented-code-cleanup.md)
- [Parent HAProxy accept-loop error-path cleanup for SonarQube Cloud C:S134](CR-20260727-sonar-haproxy-accept-loop-s134.md)
- [Parent bilingual-documentation checker PR-template literal extraction and diagnostic-order preservation for SonarQube Cloud S1192 and S3776](CR-20260727-sonar-bilingual-doc-checker.md)
- [Parent Lighttpd harness JSONL validation deduplication candidate](CR-20260727-sonar-lighttpd-harness-duplication.md)
  — local source, lifecycle-contract, documentation, and whitespace validation
  `passed`; `Draft` delivery remains pending.
- [Traefik UDS header-serialization deduplication for SonarQube Cloud](CR-20260728-sonar-traefik-uds-header-serialization-duplication.md)
- [Parent PR #128 residual SonarQube Cloud and workflow remediation](CR-20260727-sonar-pr128-residual-remediation.md)
- [Parent Apache output-filter status shadowing for SonarQube Cloud C:S1117](CR-20260727-sonar-apache-output-filter-status-shadowing.md)
- [Parent compiler-guide metadata literals for SonarQube Cloud S1192](CR-20260727-sonar-compiler-guide-metadata-literals.md)
- [Parent repository-organization regex and routing for SonarQube Cloud](CR-20260727-sonar-organization-regex-routing.md)
- [Parent full-runtime-matrix UTC offset for SonarQube Cloud S1192](CR-20260727-sonar-full-runtime-matrix-utc-offset.md)
- [Parent report-presentation literals for SonarQube Cloud S1192](CR-20260727-sonar-report-presentation-literals.md)
- [Parent bilingual Markdown suffix ownership for SonarQube Cloud S1192](CR-20260727-sonar-bilingual-markdown-suffix.md)
- [Parent remaining-failure analysis discarded-read cleanup for SonarQube Cloud S1481](CR-20260727-sonar-remaining-failure-analysis-discarded-read.md)
- [Parent analysis-helper unused-parameter cleanup for SonarQube Cloud S1172](CR-20260727-sonar-parent-analysis-unused-parameters.md)
- [Parent NGINX MRTS HTTP-500 report unused-parameter cleanup for SonarQube Cloud S1172](CR-20260727-sonar-nginx-mrts-http500-unused-parameter.md)
- [Parent report-generator unused-local cleanup for SonarQube Cloud S1481](CR-20260727-sonar-report-generators-unused-locals.md)
- [Parent NGINX MRTS HTTP-500 report unused-local cleanup for SonarQube Cloud S1481](CR-20260727-sonar-nginx-mrts-http500-unused-locals.md)
- [Parent prepare-runtime-components provenance-guard assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-prepare-runtime-components-assert-order.md)
- [Parent full-lifecycle evidence follow-up assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-full-lifecycle-evidence-followup-assert-order.md)
- [Parent connector-capabilities terminal assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-connector-capabilities-terminal-assert-order.md)
- [Parent connector-capabilities follow-up assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-connector-capabilities-followup-assert-order.md)
- [Parent transport-lifecycle artifacts assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-transport-lifecycle-artifacts-assert-order.md)
- [Parent no-CRS selected-runner assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-no-crs-selected-runner-assert-order.md)
- [Parent Apache request-transaction cleanup assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-apache-request-transaction-cleanup-assert-order.md)
- [Parent connector-capabilities assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-connector-capabilities-assert-order.md)
- [Parent response-header backend assertion order for SonarQube Cloud S3415](CR-20260727-sonar-tests-response-header-backend-assert-order.md)
- [Parent compiler-guide unused-parameter cleanup for SonarQube Cloud S1172](CR-20260727-sonar-compiler-guides-unused-parameters.md)
- [Parent runtime-matrix cache owner-root hand-off](CR-20260726-runtime-matrix-cache-owner-root.md)
- [OpenSSF Scorecard Action v2.4.4 immutable-lock synchronization](CR-20260726-scorecard-action-v2-4-4-lock.md)
- [Parent adapter-helper explicit default case for SonarQube Cloud S131](CR-20260724-sonar-ci-adapter-helpers-default-case.md)
- [Parent NGINX intervention URL ownership assertion order for SonarQube Cloud S3415](CR-20260724-sonar-tests-nginx-intervention-url-assertions.md)
- [Scorecard fuzzing and PyYAML remediation](CR-20260724-scorecard-fuzzing-pyyaml-remediation.md)
- [Parent full-lifecycle profile assertion order for SonarQube Cloud S3415](CR-20260724-sonar-tests-full-lifecycle-profiles-assertions.md)
- [Parent full-lifecycle evidence assertion order for SonarQube Cloud S3415](CR-20260724-sonar-tests-full-lifecycle-evidence-assertions.md)
- [Parent CI/Common SonarQube Cloud hygiene remediation](CR-20260724-sonar-ci-common-hygiene.md)
- [Runtime-test assertion order for SonarQube Cloud S3415](CR-20260723-sonar-tests-runtime-assertions.md)
- [Engine lifecycle assertion order for SonarQube Cloud S3415](CR-20260723-sonar-tests-engine-lifecycle-assert-order.md)
- [GitHub Actions updater parser and complexity remediation](CR-20260723-sonar-actions-updater-parser.md)
- [Parent Envoy transport assertion order for SonarQube Cloud S3415](CR-20260723-sonar-tests-envoy-transport-assert-order.md)
- [Parent Apache intervention-cleanup assertion order for SonarQube Cloud S3415](CR-20260723-sonar-tests-apache-intervention-cleanup-assert-order.md)
- [Parent runtime-producer-readiness assertion order for SonarQube Cloud S3415](CR-20260723-sonar-tests-runtime-producer-readiness-assert-order.md)
- [CI connector-profile literal deduplication for SonarQube Cloud](CR-20260723-sonar-ci-connector-profile-literals.md)
- [Optional-prerequisite assertion diagnostic order for SonarQube Cloud](CR-20260723-sonar-tests-optional-prerequisite-assert-order.md)
- [Parent Python-version assertion order for SonarQube Cloud S3415](CR-20260723-sonar-tests-python-version-assert-order.md)
- [Traefik UDS parser fuzzing](CR-20260723-traefik-uds-parser-fuzzing.md)
- [Envoy Go dependency security floors](CR-20260723-envoy-go-dependency-security-floors.md)
- [Parent connector-guide renderer decomposition for SonarQube Cloud S3776 and S1481](CR-20260723-sonar-scripts-connector-guides-refactor.md)
- [Framework gitlink update to 935cf14](CR-20260723-framework-gitlink-935cf14.md)
- [CI compile-database capture-input confinement for SonarQube Cloud](CR-20260723-sonar-ci-compile-db-input-confinement.md)
- [Read-only Update-submodules runtime-path validation repair](CR-20260723-update-submodules-runtime-path-validation.md)
- [Parent tests and Lighttpd assertion order for SonarQube Cloud S3415](CR-20260722-sonar-tests-connectors-assert-order.md)
- [Scripts workflow and report path confinement for SonarQube Cloud security findings](CR-20260722-sonar-scripts-path-confinement.md)
- [Read-only Update-submodules validation dependency repair](CR-20260723-update-submodules-validation-dependency.md)
- [Parent CI and scripts literal deduplication for SonarQube Cloud S1192](CR-20260722-sonar-ci-scripts-literals.md)
- [Parent NGINX Phase-4 assertion ordering for SonarQube Cloud S3415](CR-20260722-sonar-s3415-nginx-phase4-assert-order.md)
- [CodeQL Action 4.37.3 batch](CR-20260722-codeql-action-4-37-3-batch.md)
- [Central Go toolchain and Update-submodules validation repair](CR-20260722-central-go-toolchain-submodule-validation.md)
- [CodeQL Action 4.37.2 batch](CR-20260722-codeql-action-4-37-2-batch.md)
- [NGINX Server header byte-length correction](CR-20260721-nginx-server-header-length.md)
- [Parent readiness-path constant for SonarQube Cloud S1192](CR-20260721-sonar-s1192-readiness-path.md)
- [Python 3.14.6 and Go 1.26.5 toolchain baseline](CR-20260721-python314-go1265-toolchain-baseline.md)
- [GitHub Actions checkout v7.0.1 immutable-lock synchronization](CR-20260721-actions-checkout-v7-lock.md)
- [GitHub Actions setup-python v7 immutable-lock synchronization](CR-20260721-actions-setup-python-v7-lock.md)
- [CSV security findings remediation](CR-20260721-csv-security-findings-remediation.md)
- [Parent Python 3.13 workflow contract and safe patch updater](CR-20260720-python-313-workflow-contract.md)
- [Apache intervention ownership cleanup](CR-20260720-apache-intervention-ownership.md)
- [Go 1.24.13 security baseline](CR-20260720-go12413-security-baseline.md)
- [SonarQube Cloud reliability bug remediation](CR-20260720-sonar-reliability-remediation.md)
- [Portable C secure-zero hardening for SonarQube Cloud c:S5798](CR-20260721-sonar-c-s5798-zeroization.md)
- [Explicit Parent analysis-output containment defaults for SonarQube Cloud S131](CR-20260721-sonar-s131-containment-defaults.md)
- [SonarQube Cloud new-code duplication remediation](CR-20260719-sonar-new-code-duplication.md)
- [Phase-4 evidence identity binding](CR-20260718-phase4-evidence-identity-binding.md)
- [Apache Phase-4 response enforcement](CR-20260718-apache-phase4-response.md)
- [Runtime path-confinement hardening](CR-20260718-runtime-path-confinement.md)
- [Detached Parent aggregate receipt for full-matrix evidence](CR-20260718-detached-aggregate-receipt.md)
- [Descriptor-confined aggregate receipt publication](CR-20260719-aggregate-receipt-toctou-confinement.md)
- [Strict runtime result-file authenticity](CR-20260718-result-file-authenticity.md)
- [Security policy and governance baseline](CR-20260718-security-policy-governance.md)
- [Traefik UDS and C++ evaluator hardening](CR-20260717-traefik-uds-cpp17-hardening.md)
- [CI security hardening](CR-20260716-ci-security-hardening.md)
- [CodeQL Action 4.37.1 batch](CR-20260717-codeql-action-4-37-1-batch.md)
- [GitHub workflow permission hardening](CR-20260718-harden-workflow-permissions.md)
- [CI status-channel integrity](CR-20260718-status-channel-integrity.md)
