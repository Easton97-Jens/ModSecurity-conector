# Reports

**Language:** English | [Deutsch](README.de.md)

Reports are organized by current evidence role. They do not replace the
run-local artifacts from which a claim was validated.

| Area | Canonical source | Purpose |
| --- | --- | --- |
| Current core evidence | [current/core-completion.md](current/core-completion.md) | Bounded selected six-connector HTTP/1.1 core evidence. |
| Current readiness | [current/readiness.md](current/readiness.md) | Current status, boundaries, and deliberately unmade claims. |
| Architecture and evidence audit | [audits/architecture-and-evidence.md](audits/architecture-and-evidence.md) | Consolidated architecture, runtime-root, transport, and evidence contract. |
| Change Records | [audits/change-records/README.md](audits/change-records/README.md) | Versioned, manually maintained records for non-trivial changes. |
| Configuration inventory | [connector-configuration-inventory.json](connector-configuration-inventory.json) | Generated source-backed connector, Common Runtime, and engine option inventory. |
| Testing and generated reports | [testing/README.md](testing/README.md) | Generator-managed runtime, coverage, cache, and evidence reports. |

`testing/generated/` remains the established generated-report location because
the report registry, path-safety checks, and generators use it as their source
contract. Regenerate it with `make refresh-all-reports`; do not edit generated
Markdown by hand. The refresh manifest is the canonical generated-report
catalog; separate dependency, lineage, path-migration, roadmap, and
generator-summary views are intentionally not retained.

Regenerate the configuration inventory and its paired example references with
`make generate-connector-config-reference`; verify source/documentation parity
with `make check-connector-config-reference`.

## Portable path notation

Committed reports never rely on a particular workstation's directory layout.
When a retained record needs to name a runtime location, it uses one of these
display-only references; the run ID, hashes, and repository-relative artifact
names remain the provenance contract.

| Reference | Meaning |
| --- | --- |
| `<repository-root>` | The checkout containing this report. |
| `<verified-run-root>` | The configured root of a verified runtime run; it contains `build/`, logs, and the component cache for that run. |
| `BUILD_ROOT:<relative-path>` | A path below the configured `BUILD_ROOT` environment variable. |
| `<historical-run-root:run-id>` | A retained historical workspace identified by `run-id`; it is not a path readers should recreate. |
| `<local-state-root>` | Non-contract, developer-local state retained only in historical evidence descriptions. |
| `<temporary-work-root>` | Disposable temporary workspace used during a command or comparison. |
| `<local-home-root>` | A home-directory-relative location whose concrete user or host path is intentionally omitted. |
| `<external-source-root>` | An externally supplied source checkout, never a required location in this repository. |
