# Repository contract tests

**Language:** English | [Deutsch](README.de.md)

## Purpose and boundary

\`tests/\` contains focused Python tests and native fixtures for root orchestration, configuration,
artifact layout, lifecycle wiring, capability boundaries, and path/security
contracts. They provide fast regression coverage for repository behavior that
can be checked without presenting a synthetic host run as evidence.

These tests are not the Framework case catalog, a replacement for connector
harnesses, or canonical runtime evidence. Passing unit tests do not establish
production readiness, CRS completeness, HTTP/2 or HTTP/3 verification, a
complete matrix, or strict verification for all connectors.

## One automatic active inventory

[config/testing/active-cases.json](../config/testing/active-cases.json) selects **100 expanded standard cases / 80 executions** across all automatic local, CI and scheduled functional checks. The earlier additional-offline authorization is superseded for automatic selection by the user's final scope stop. Connector E2E remains 26 cases; historical I12 host/matrix/oracle campaigns remain closed.

The same schema-3 inventory retains **1893 on-demand cases / 839 executions** outside every default path. `make test`, the no-argument inventory runner, Python discovery and automatic group filters use only the standard section. A shared group cannot activate archived rows. Full schema/source/selector admission remains mandatory; an expanded standard inventory above 100 fails before a child starts. Selection is never silently truncated.

`make check-active-inventory` admits without executing. For an explicitly requested specialist assessment use an exact selector, for example `python3 ci/tools/run-active-tests.py --on-demand --execution <archived-execution-id> --output-root <existing-external-parent>`. The opt-in alone without a group/case/execution selector fails. Retained module-wide commands require explicit `ON_DEMAND_TESTS=1`; keep it unset in defaults and schedules. Neither mechanism authorizes a historical I12 campaign, elevation or cross-repository work.

Sonar keeps exact-head source analysis, native context, the required/advisory matrix, secret isolation and real gate waiting. Its specialist Python/Go/Common coverage collections no longer execute automatically. The retained collector requires explicit `--on-demand` before any output or test command. Coverage is irrelevant to security and merge decisions by the user's later instruction; no security rule, remaining gate condition or functional assertion is removed.

The generated [archive disposition](../reports/testing/test-selection-archive.generated.json) lists retained definitions outside standard selection. Definition counts are not expanded case counts and do not establish a PASS. Regenerate it through `ci/tools/update-test-archive.py`. Static compilation, CodeQL, actionlint, zizmor, OSV and secret scanning retain their independent controls. See [testing and evidence](../docs/testing-and-evidence.md) and [PR #382 status](../docs/pr-382-merge-readiness.md).

## Structure and source of truth

| Path pattern | Purpose | Source of truth / placement rule |
| --- | --- | --- |
| \`test_*.py\` | Root-level Python unit and contract tests | Each test is authoritative for its explicit assertion; the implementation and root Makefile remain authoritative for behavior and target wiring. |
| \`test_*lifecycle*.py\` | Lifecycle artifact/profile/wiring checks | Keep these focused on run metadata and contracts, not fabricated runtime success. |
| \`test_*capabilit*.py\` and \`test_*evidence*.py\` | Capability/evidence boundary checks | Assert schema and claim rules; do not encode a broader capability than recorded evidence supports. |
| \`test_*path*.py\`, \`test_*cache*.py\`, and \`test_*component*.py\` | Path, cache, and component-preparation contracts | Keep paths portable and test the safety boundary rather than relying on a developer workspace. |

The Framework submodule owns reusable YAML cases, normalizers, and runner
tests. Root \`tests/\` owns only connector-repository contracts. The root
[Makefile](../Makefile) is authoritative for target names; the current
[testing guide](../docs/testing-and-evidence.md) explains the test levels.

## Adding or changing tests

Place a new root contract test at \`tests/test_<area>.py\`. Here, \`<area>\` is
a documentation placeholder: replace it with a concise lowercase identifier
such as \`runtime_path_policy\`, producing the literal file
\`tests/test_runtime_path_policy.py\`. Do not create a file literally named
\`test_<area>.py\`.

Core additions still need a named replacement at capacity. Explicit offline exception additions need their own reviewed source-bound Python selector and fully enumerated variants; the user exception is not an uncounted second catalog.

A new automatically selected behavior needs a stable case ID, requirement,
profile and executable selector in the active inventory. At core capacity, name the
replaced or genuinely consolidated behavior and document lost coverage; adding
a method or hiding independent scenarios in a loop does not avoid counting.

Keep fixtures self-contained, portable, and non-secret. Test the smallest root
behavior that protects a contract; put reusable catalog cases, normalizer
changes, and Framework runner tests in \`modules/ModSecurity-test-Framework/\`.
Do not commit \`__pycache__/\`, generated reports, real runtime output,
downloads, build trees, credentials, or copied evidence to this directory.

## Variables and placeholders

The root Makefile owns the relevant values. See the central
[variables and placeholders reference](../docs/reference/variables.md)
and [glossary](../docs/reference/glossary.md) for definitions beyond this local
test scope.

| Name | Local meaning | Requiredness, format, and example |
| --- | --- | --- |
| \`PYTHON\` | Python executable used by Make targets and checks | Optional; the root Makefile uses \`.venv/bin/python\` when present, otherwise \`python3\`. Use an installed executable or executable path, not a shell fragment. |
| \`PYTHONDONTWRITEBYTECODE\` | Controls Python bytecode creation during checks | Optional; repository default is \`1\`. Keep it at \`1\` for clean source-tree checks unless a diagnostic explicitly needs bytecode. |
| \`BUILD_ROOT\` | Disposable workspace for checks that create artifacts | Optional and root-derived. An override must be an absolute writable path outside the checkout, such as \`/srv/modsecurity-work/build\`; it is not a fixture directory. |
| \`FRAMEWORK_ROOT\` | Framework checkout used when a root target delegates | Required for delegated Make targets. Its repository default is \`modules/ModSecurity-test-Framework\`; an override must name an existing trusted checkout. |
| \`<repository-root>\` | Documentation-only absolute root of this checkout | Use a real directory such as \`/srv/src/ModSecurity-conector\` only when a command needs one. Do not copy the angle brackets into Python or a shell command. |

No test variable is a secret. Never put tokens, cookies, authorization headers,
private keys, or real customer payloads in a test name, fixture, command
argument, or expected artifact.

## Relevant commands and targets

| Command or target | Purpose and outcome boundary |
| --- | --- |
| <code>make check-active-inventory</code> | Admits the complete expanded inventory and prints its actual count without running cases. |
| <code>make test</code>, <code>make test-active</code> | Runs the full admitted selection, including native and runtime prerequisites; this is not a lightweight host-free check. |
| <code>python3 ci/tools/run-active-tests.py --group inventory --output-root /srv/modsecurity-work/tests</code> | Runs one admitted group with the canonical project Python; the existing output parent must be trusted, owned, canonical and external. |
| <code>python3 -m unittest discover -v tests</code> | Runs only admitted Python definitions through the shared discovery hooks. It does not cover the Go/native/runtime selections or run the Framework catalog. |
| <code>ON_DEMAND_TESTS=1 python3 -m unittest -v tests.test_runtime_path_policy</code> | Explicitly requests the retained specialist module; its wider assertions are outside automatic selection and may require separately scoped maintenance. |
| <code>make check-framework-fixture-syntax</code> | Static Framework fixture syntax/contract validation, not a runtime result. |
| <code>make check-test-matrix</code> | Checks generated matrix consistency and ownership; generating a matrix does not execute its cases. |
| <code>make quick-check</code>, <code>make lint</code> | Retains static/configuration/documentation/governance checks; functional portions select the same active inventory and create no general host qualification. |
| <code>ON_DEMAND_TESTS=1 make check-native-engine-body-inspection</code> | Retained full native limits/serialization/phase suite; requires the real C17 compiler and selected SDK. Without the flag, this alias selects the active Common group, not that complete specialist suite. |
| <code>ON_DEMAND_TESTS=1 make check-native-lifecycle-observer</code> | Retained full GNU-linker observer suite with explicit <code>NATIVE_OBSERVER_TEST_OUT</code>, <code>MODSECURITY_INCLUDE_DIR</code> and <code>MODSECURITY_LIB_DIR</code>. Without the flag, this alias selects the active Common group after its existing SDK/output preflight. |

The on-demand native suite accepts the existing `MODSECURITY_PREFIX`,
`MODSECURITY_INCLUDE_DIR`, `MODSECURITY_LIB_FILE` and `MODSECURITY_LIB_DIR`
SDK selection; invalid explicit paths fail before compilation. With an external
library, executables use its directory as their runtime search path. Inspection
fixtures set native limits/actions explicitly. Lossless byte escapes must retain
phase and event integrity; escaped-field overflow must neither write nor advance
the hash chain. Lightweight event-protocol tests retain their separate dependency
boundary.

The on-demand lifecycle observer records actual API entry/return pairs, separate host and
canonical transaction IDs, Common state snapshots and per-process final receipts.
Link it only into test artifacts with the fourteen `--wrap` symbols listed in
`tests/test_native_lifecycle_observer.py`. A supervisor supplies a private inherited
append descriptor and retains its original JSONL. Same-object internal calls can
bypass wrapping; missing receipts or outstanding mappings leave cleanup unqualified.
Native MIME selection and actual host EOS remain `null`. Successful component
tests or API counts alone do not establish a host lifecycle result.
Native append records include actual byte counts and null/non-null input kinds;
these APIs expose no EOS argument, so empty appends cannot qualify host EOS.

The optional `ci/runtime/lifecycle/native-lifecycle-sdk.cpp` helper reads the
selected C++ SDK's public transaction ID after rejecting a runtime version
mismatch. Bind the exact headers/library hashes and qualify both real constructors
before linking it into a host test artifact. This includes anonymous native IDs;
the caller's input ID remains separate and no Common/native correlation is inferred.
The version check alone does not qualify an arbitrary ABI-compatible-looking build.
Without this helper the observer retains its opaque native ABI behavior. Rejected
or oversized IDs invalidate measurement while preserving the native call and errno.

Use [test levels](../docs/testing-and-evidence.md),
[core lifecycle testing](../docs/testing-and-evidence.md), and the
[evidence guide](../docs/testing-and-evidence.md) to choose a test level and report
its result accurately.
