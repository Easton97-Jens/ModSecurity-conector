# Repository contract tests

**Language:** English | [Deutsch](README.de.md)

## Purpose and boundary

\`tests/\` contains focused Python tests for root orchestration, configuration,
artifact layout, lifecycle wiring, capability boundaries, and path/security
contracts. They provide fast regression coverage for repository behavior that
can be checked without presenting a synthetic host run as evidence.

These tests are not the Framework case catalog, a replacement for connector
harnesses, or canonical runtime evidence. Passing unit tests do not establish
production readiness, CRS completeness, HTTP/2 or HTTP/3 verification, a
complete matrix, or strict verification for all connectors.

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
[testing guide](../docs/testing/README.md) explains the test levels.

## Adding or changing tests

Place a new root contract test at \`tests/test_<area>.py\`. Here, \`<area>\` is
a documentation placeholder: replace it with a concise lowercase identifier
such as \`runtime_path_policy\`, producing the literal file
\`tests/test_runtime_path_policy.py\`. Do not create a file literally named
\`test_<area>.py\`.

Keep fixtures self-contained, portable, and non-secret. Test the smallest root
behavior that protects a contract; put reusable catalog cases, normalizer
changes, and Framework runner tests in \`modules/ModSecurity-test-Framework/\`.
Do not commit \`__pycache__/\`, generated reports, real runtime output,
downloads, build trees, credentials, or copied evidence to this directory.

## Variables and placeholders

The root Makefile owns the relevant values. See the central
[variables and placeholders reference](../docs/configuration/variables.md)
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
| \`.venv/bin/python -m unittest -v tests.test_runtime_path_policy\` | Runs one focused test module when \`.venv/bin/python\` exists. Replace the module suffix with a literal checked-in test name; this is unit coverage, not host evidence. |
| \`python3 -m unittest discover -v tests\` | Discovers root Python tests with the system Python when it satisfies project dependencies. It does not run the Framework suite. |
| \`make check-framework-fixture-syntax\` | Validates Framework fixture syntax from the root target; it is a syntax/contract check, not a runtime result. |
| \`make check-test-matrix\` | Checks generated test-matrix consistency and ownership boundaries. |
| \`make quick-check\` | Runs the repository's focused quick contract checks. It does not create canonical runtime evidence. |
| \`make lint\` | Runs broad syntax, contract, documentation, and governance checks, including root test-related contracts. |

Use [test levels](../docs/testing/test-levels.md),
[core lifecycle testing](../docs/testing/core-lifecycle.md), and the
[evidence guide](../docs/evidence/README.md) to choose a test level and report
its result accurately.
