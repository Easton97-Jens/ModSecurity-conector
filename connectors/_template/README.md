# Connector Template

**Language:** English | [Deutsch](README.de.md)

Status:

- template: yes
- scaffolded: yes
- suitable_scaffold: yes
- implemented: no
- build_verified: no
- runtime_verified: no
- promoted: no

## Purpose

This directory is a repeatable documentation scaffold for future
`connectors/<name>/` implementations. It describes what a new connector must
fill in before it may claim build or runtime behavior.

It is not a productive connector implementation. It intentionally contains no
productive adapter code, no local test suite, and no server-specific runtime
claims.

Template status: suitable scaffold, not runtime-verified.

Deutsch: geeignet als Scaffold-Vorlage, nicht runtime-verifiziert.

## When to use this template

Use this template when creating a new connector tree that still needs
repository-backed evidence for origin, metadata, build integration, runtime
behavior, and promotion status.

Do not use this template to claim that Apache, NGINX, or any other connector
behavior is automatically portable to a new server. Server lifecycle, hook
model, request/response body handling, logging, and intervention mapping must
be proven for each connector.

## Files to create for a new connector

Copy this structure into `connectors/<name>/` and replace placeholders only
with evidence found in the repository or produced by executed commands:

```text
connectors/<name>/
|-- README.md
|-- TODO.md
|-- ORIGIN.md
|-- SOURCE_MAP.json
|-- metadata.c or metadata.*
|-- harness/
|   `-- README.md
`-- src/
    `-- README.md
```

Do not create `connectors/<name>/tests`. Executable connector tests are
framework-owned, not connector-local.

## Required metadata

Required per connector. This is not a Template defect. Every new connector must
create `metadata.*` or the metadata form expected by this repository.

- [ ] `metadata.*` created.
- [ ] Connector name is unique.
- [ ] Upstream project and version documented.
- [ ] Build mode documented.
- [ ] Maintainer or ownership documented.
- [ ] Status vocabulary used consistently.

## Required origin/license evidence

Required per connector. This is not a Template defect. Every new connector must
document `ORIGIN.md`, license/origin evidence, and imported files.

- [ ] `ORIGIN.md` created.
- [ ] Upstream source documented.
- [ ] License documented.
- [ ] Imported files documented.
- [ ] Local changes documented.
- [ ] Source map or equivalent provenance file documented.

No upstream source, file, license, or version may be guessed. If it is not
found, write `Nicht im Repository gefunden` or keep the item open.

## Required build evidence

- [ ] Build command documented.
- [ ] Include paths documented.
- [ ] Library paths documented.
- [ ] Build artifacts documented.
- [ ] Build log path documented.
- [ ] Clean or refresh behavior documented.
- [ ] External dependency versions or pins documented when found.

A build claim requires the exact command, result, and log path. Static file
presence alone is not build verification.

## Required runtime evidence

Not applicable to template. Runtime evidence requires concrete connectors and
actually executed profiles. Standard aliases use
[config/testing/active-cases.json](../../config/testing/active-cases.json),
not a new local catalog: at most 100 fully expanded active behavioral cases
project-wide. New active requirements need stable IDs, profiles and executable
selectors; at capacity, name the replacement or genuine consolidation and its
lost coverage.

- [ ] Record admitted No-CRS case IDs and actual connector/profile scope; <code>make test-no-crs</code> selects only its active subset.
- [ ] Record admitted CRS case IDs and actual connector/profile scope; <code>make test-with-crs</code> selects only its active subset.
- [ ] Run broader specialists such as <code>ON_DEMAND_TESTS=1 make smoke-common</code> only when a current additional request explicitly covers them.
- [ ] Apache/NGINX or connector-specific scope documented.
- [ ] PASS/FAIL/BLOCKED counts documented.
- [ ] Summary JSON paths documented.
- [ ] RESPONSE_BODY blocking checked.
- [ ] Negative/pass-through checked.
- [ ] Audit/log evidence checked.

Runtime claims require executed commands and result files. Generated coverage
reports can support planning, but they are not runtime proof by themselves.

RESPONSE_BODY blocking is a runtime promotion gate. Concrete connectors may
mark it verified only after repository-backed runtime evidence proves a
blocking response-body trigger and blocking result.

Harness contract is documented by the Template. Harness implementation is
required per connector.

## No-CRS validation

The standard <code>make test-no-crs</code> alias runs only the admitted runtime
group and proves neither a complete catalog nor a new connector. Record exact
case IDs and profile evidence. The retained broader example requires a
separately authorized specialist request:


```sh
ON_DEMAND_TESTS=1 SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-no-crs
```

Record:

- command and exit code
- connector scope
- PASS/FAIL/BLOCKED counts
- relevant case-level expected and actual statuses
- summary JSON paths

A No-CRS PASS does not imply a With-CRS PASS.

## With-CRS validation

The standard <code>make test-with-crs</code> alias runs only the admitted CRS
runtime group. It does not establish exhaustive CRS or profile qualification.
Record exact case IDs. The retained broader example requires a separately
authorized specialist request:


```sh
ON_DEMAND_TESTS=1 SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-with-crs
```

Record:

- command and exit code
- CRS source path
- CRS runtime preamble path
- connector scope
- PASS/FAIL/BLOCKED counts
- CRS-specific case evidence
- summary JSON paths

If a case has different valid expectations in No-CRS and With-CRS modes, the
expectation model must keep those variants separate. Do not change a base
No-CRS expectation to satisfy a With-CRS result.

## Coverage decision matrix

The following criteria apply to an explicitly requested promotion assessment,
not automatic default selection or routine changes. They do not require
reopening closed I12 matrix/oracle/host campaigns. A specialist opt-in
<code>ON_DEMAND_TESTS=1</code> grants neither privileges nor Framework/MRTS
writes; historical evidence retains its revision. Sibling profiles do not
qualify one another.

Each concrete connector must complete the canonical
[new-connector contract](../../docs/connectors/README.md#new-connector-evidence-contract)
and its flat guide under `docs/connectors/`. Its review matrix must separate:

- framework case availability
- No-CRS runtime result
- With-CRS runtime result
- evidence path
- promotion decision

The matrix must cover at least phase 1, phase 2, phase 3, phase 4,
RESPONSE_BODY blocking, negative/pass-through behavior, audit/log evidence,
startup/reload validation, and remaining FAIL/BLOCKED rows.

## Promotion gates

`scaffolded`:

- structure exists
- documentation foundation exists
- no runtime claims

`adapter-owned`:

- source, build, metadata, and origin files exist
- provenance and local changes are documented

`runtime-smoke-verified`:

- current PASS for the exact admitted No-CRS case IDs and claimed connector/profile
- current actual connector host-smoke PASS for that same connector/profile
- command and result paths documented

`crs-verified`:

- current PASS for the exact admitted CRS case IDs and claimed connector/profile
- CRS loaded/effective evidence documented
- CRS-specific expectations documented

`more-than-partial`:

- No-CRS PASS
- With-CRS PASS
- phase 1/2/3/4 minimum matrix PASS
- negative/pass-through PASS
- audit/log evidence present
- RESPONSE_BODY blocking verified, or explicitly documented as unsupported or
  a known gap with evidence
- no open FAIL/BLOCKED rows in the defined minimum matrix

## Status vocabulary

- `template`: generic starting point, not an implementation.
- `scaffolded`: structure exists, no repository-backed adapter implementation
  is proven.
- `adapter-owned`: productive connector code lives in the connector tree with
  provenance and metadata.
- `runtime-smoke-verified`: only specific smoke cases with recorded command and
  result are verified.
- `crs-verified`: With-CRS target or case claim has recorded command, CRS
  evidence, and result.
- `partial`: structure or partial runtime evidence exists, but full validation
  is not proven.
- `not-verified`: insufficient runtime evidence.

## What must not be claimed

- Do not claim a local `connectors/<name>/tests` suite exists.
- Do not claim runtime PASS without a command, exit code, and result path.
- Do not claim With-CRS PASS from No-CRS evidence.
- Do not claim RESPONSE_BODY blocking from pass-through or log-only evidence.
- Do not claim a connector is more than `partial` while the minimum matrix has
  unaddressed FAIL/BLOCKED rows.
- Do not invent upstream source, license, build flags, APIs, tests, or
  framework paths.

## External framework tests

Repository-backed framework paths used by connector documentation:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Make targets must be cited only when present in the parent `Makefile`.
