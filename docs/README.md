# Documentation Index

Status: implemented

This directory is grouped by topic so connector-owned architecture, roadmap,
and source-attribution docs stay navigable as the framework-owned case corpus
and generated reports grow.

## Main Sections

| Section | Purpose |
| --- | --- |
| `architecture/` | Common C-first model, adapter boundaries, status/capability models, and refactor plans |
| `connectors/` | Apache/NGINX directive/rule-load docs and future connector planning |
| `roadmap/` | Current connector roadmap |
| `licensing/` | License and origin policy for imported connector sources |
| `../reports/testing/` | Connector-owned generated evidence, real-world validation notes, case matrix, and PR/source evidence |
| `../modules/ModSecurity-test-Framework/docs/` | Framework-owned YAML schema, fixtures, case corpus, import analyses, TODO inventory, and reusable testing docs |

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
- Capability model: `architecture/capability-model.md`
- Status model: `architecture/status-model.md`
- Real connector proof mode: `../reports/testing/real-world-connector-validation.md`
- Current compatibility evidence: `../reports/testing/test-coverage-overview.md`
- Case matrix: `../reports/testing/case-matrix.md` and
  `../reports/testing/generated/case-matrix.generated.md`
- Roadmap and open work: `roadmap/roadmap.md` and
  `../modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
- YAML schema and shared fixtures:
  `../modules/ModSecurity-test-Framework/docs/imports/common/schema.md` and
  `../modules/ModSecurity-test-Framework/docs/imports/common/fixtures.md`
- PR/source evidence: `../reports/testing/evidence/pr-evidence-summary.md`
  and `../reports/testing/evidence/raw-args-pr3564.md`
- License and origin: `licensing/license-and-origin.md` and `../licenses/README.md`
