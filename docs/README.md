# Documentation Index

**Language:** English | [Deutsch](README.de.md)


Status: implemented

This directory is grouped by topic so connector-owned architecture, roadmap,
and source-attribution docs stay navigable as the framework-owned case corpus
and generated reports grow.

## Main Sections

| Section | Purpose |
| --- | --- |
| `architecture/` | Common C-first model, adapter boundaries, status/capability models, and refactor plans |
| `connectors/` | Apache/NGINX directive/rule-load docs and future connector planning |
| `testing/` | Verified-run runtime environment, worker-access preflights, and generated-report workflow notes |
| `roadmap/` | Current connector roadmap |
| `licensing/` | License and origin policy for imported connector sources |
| `../reports/testing/` | Connector-owned generated evidence, real-world validation notes, case matrix, and PR/source evidence |
| `../modules/ModSecurity-test-Framework/docs/` | Framework-owned YAML schema, fixtures, case corpus, import analyses, TODO inventory, and reusable testing docs |

## Source References

| Repository | Repo-local purpose | Upstream | Observed version/tag | License |
| --- | --- | --- | --- | --- |
| ModSecurity v2 | Historical/source comparison reference only | https://github.com/owasp-modsecurity/ModSecurity | `v2.9.13` | Apache-2.0 |
| ModSecurity v3 | libmodsecurity runtime/API reference | https://github.com/owasp-modsecurity/ModSecurity | `v3.0.15` | Apache-2.0 |
| ModSecurity-apache | Apache adapter behavior/source attribution reference | https://github.com/owasp-modsecurity/ModSecurity-apache | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |
| ModSecurity-nginx | NGINX adapter behavior/source attribution reference | https://github.com/owasp-modsecurity/ModSecurity-nginx | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

CI, local development, and report refreshes should use repository-relative
paths, submodules, and environment variables rather than machine-specific source
locations.

## First Reads

- Architecture boundary: `architecture/architecture.md`
- Capability model: `architecture/capability-model.md`
- Status model: `architecture/status-model.md`
- Real connector proof mode: `../reports/testing/real-world-connector-validation.md`
- Testing report index: `../reports/testing/README.md`
- Verified run environment: `testing/verified-run-environment.md`
- Merge readiness: `../reports/testing/generated/canonical/final-consistency-audit.generated.md`
- Current compatibility evidence: `../reports/testing/test-coverage-overview.md`
- Case matrix: `../reports/testing/case-matrix.md` and
  `../reports/testing/generated/coverage/case-matrix.generated.md`
- Roadmap and open work: `roadmap/roadmap.md` and
  `../modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
- YAML schema and shared fixtures:
  `../modules/ModSecurity-test-Framework/docs/imports/common/schema.md` and
  `../modules/ModSecurity-test-Framework/docs/imports/common/fixtures.md`
- PR/source evidence: `../reports/testing/evidence/pr-evidence-summary.md`
  and `../reports/testing/evidence/raw-args-pr3564.md`
- License and origin: `licensing/license-and-origin.md` and `../licenses/README.md`
