# Versioned configuration

**Language:** English | [Deutsch](README.de.md)

## Purpose and boundary

\`config/\` contains small, versioned machine-readable inputs used by repository
checks, harnesses, and report generators. It is for declarative test and
contract configuration, not for environment-specific host configuration or
runtime output.

Configuration presence or JSON validity is not runtime evidence. In
particular, this directory makes no production, CRS-completeness, HTTP/2,
HTTP/3, complete-matrix, or strict-for-all-connectors claim.

## Structure and source of truth

| Path | Purpose | Source of truth / consumer |
| --- | --- | --- |
| \`testing/capability-contract.json\` | Connector-neutral capability contract used by contract/evidence checks | The checked-in JSON is the source of truth for this contract; its \`runtime_claim\` value is intentionally not a runtime promotion. |
| \`testing/import-status.json\` | Classification of imported, mapped, blocked, and connector-specific test material | The checked-in JSON is consumed by Apache, NGINX, and HAProxy harness/report paths. It must reflect reviewed repository status, not an optimistic runtime result. |

The consumer code and the root [Makefile](../Makefile) define validation and
target behavior. Generated reports are derived artifacts, not a replacement for
these source files.

## Adding or changing configuration

Place a new versioned input in a named domain directory such as
\`config/testing/\`, and add a validator or an existing consumer in the same
change. Use explicit JSON values and stable schema keys. Update the source
contract, its tests, and any generator that derives documentation or reports.

Do not place per-machine host configuration, generated JSON, build/cache paths,
runtime logs, result files, source downloads, passwords, tokens, private keys,
certificates, cookies, or authorization headers under \`config/\`. Do not add an
unimplemented setting merely because another connector exposes a similarly
named capability.

## Variables and placeholders

The tracked JSON in this directory is deliberately literal: it does not expand
shell variables or documentation placeholders. The commands that consume it may
receive the following root inputs. Their complete definitions are in the
[variables and placeholders reference](../docs/configuration/variables.md).

| Name | Local meaning | Requiredness, format, and example |
| --- | --- | --- |
| \`NO_CRS_RULES_FILE\` | Rule file selected by No-CRS lifecycle commands that also consume configuration-derived contracts | Optional for configuration validation; the root default is the Framework baseline. An override must be an existing absolute rule file, for example \`/srv/modsecurity-work/rules/no-crs-baseline.conf\`. It is not a JSON field. |
| \`NO_CRS_CONNECTORS\` | Bounded connector selection for aggregate targets | Optional; its repository default is \`apache nginx haproxy envoy traefik lighttpd\`. Use only those space-separated names unless a target documents another scope. |
| \`NO_CRS_RUN_ID\` | Aggregate evidence namespace used by lifecycle/report commands | Required for an aggregate evidence run, no default, filesystem-safe token such as \`six-core-20260712T120000Z\`. It must not contain secrets or personal information. |
| \`<repository-root>\` | Documentation-only placeholder for the checkout containing \`config/\` | It must be replaced with a real absolute root such as \`/srv/src/ModSecurity-conector\` only when a command asks for one; the angle brackets are not executable input. |
| \`<external-source-root>\` | Documentation-only placeholder for a trusted checkout outside this repository | An example is \`/srv/src/ModSecurity-test-Framework\`. It is not an output/cache path and does not make external inputs verified. |

Never substitute \`REPLACE_ME\`, \`CHANGE_ME\`, \`$VAR\`, or another informal token
into JSON. There is no interpolation phase; use a documented concrete schema
value or add a reviewed consumer contract instead.

## Relevant targets

| Target | Purpose and outcome boundary |
| --- | --- |
| \`make check-common-sdk-contract\` | Checks that the capability contract is present and structurally consistent with SDK/Common expectations. |
| \`make lint\` | Validates \`config/testing/import-status.json\` as JSON and runs its broader contract consumers. A passing lint does not prove a host run. |
| \`make report-governance\` | Checks generated-report governance and source/derived boundaries. It does not refresh runtime evidence. |
| \`make refresh-all-reports\` | Regenerates report artifacts from their documented sources; review its changes rather than editing generated output by hand. |
| \`make full-lifecycle-all-connectors\` | Uses lifecycle inputs and writes run-scoped evidence; provide a safe \`NO_CRS_RUN_ID\` when creating an aggregate candidate. |

Read [Testing](../docs/testing/README.md), [Evidence](../docs/evidence/README.md),
and the [glossary](../docs/reference/glossary.md) before changing a status or
capability term.
