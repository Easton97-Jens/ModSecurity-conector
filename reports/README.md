# Reports

**Language:** English | [Deutsch](README.de.md)

Reports are organized by evidence role. They are not a substitute for the
run-local artifacts from which a claim was validated.

| Area | Contents | Source of truth |
| --- | --- | --- |
| [`current/`](current/) | Current manually maintained six-connector status and readiness reports | Current selected HTTP/1.1 core and its linked evidence boundary |
| [`audits/`](audits/) | Contract, runtime-root, promotion, transport, and organization audits | The named audit inputs and date |
| [`evidence/`](evidence/) | Human-readable summaries of selected No-CRS evidence | Canonical result/event artifacts, not raw local runs |
| [`archive/`](archive/README.md) | Superseded planning, readiness, and historical analysis | Banner at the beginning of each report |
| [`testing/`](testing/) | Existing detailed testing index and generated-report layout | Its generator registry and Framework sources |

`testing/generated/` remains the established generated-report location because
the report registry, path-safety checks, and generators use it as their source
contract. Regenerate it with `make refresh-all-reports`; do not edit generated
Markdown by hand.

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

The Phase-1 organization inventory and plan are retained at the report root:
[inventory](repository-organization-inventory.json) and
[plan](repository-organization-plan.md). They record the pre-move state and
are not current runtime evidence.
