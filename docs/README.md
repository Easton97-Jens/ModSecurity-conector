# Documentation Index

Status: implemented

This directory is grouped by topic so the framework can stay navigable as the
connector evidence grows.

## Main Sections

| Section | Purpose |
| --- | --- |
| `architecture/` | Common C-first model, adapter boundaries, status/capability models, and refactor plans |
| `connectors/` | Apache/NGINX PoCs, real-world connector validation, and future connector planning |
| `testing/` | YAML smoke cases, compatibility evidence, case matrix, and xfail investigations |
| `imports/` | Source inventories, connector code import plans, import analyses, and pruning evidence |
| `roadmap/` | Current roadmap and TODO inventory |
| `licensing/` | License and origin policy for imported connector sources |
| `evidence/` | PR-focused evidence summaries and mapped-only feature evidence |
| `quality/` | SonarCloud and maintenance remediation tracking |

## Source References

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `/root/conecter/ModSecurity_V2` | https://github.com/owasp-modsecurity/ModSecurity | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Apache-2.0 |
| ModSecurity v3 | `/root/conecter/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Apache-2.0 |
| ModSecurity-apache | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |
| ModSecurity-nginx | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Local paths are examples only. CI and other machines should use environment
variables and the upstream URLs above.

## First Reads

- Architecture boundary: `architecture/architecture.md`
- Real connector proof mode: `connectors/real-world-connector-validation.md`
- Current compatibility evidence: `testing/compatibility.md`
- Roadmap and open work: `roadmap/roadmap.md` and `roadmap/todo-inventory.md`
- License and origin: `licensing/license-and-origin.md` and `../licenses/README.md`
