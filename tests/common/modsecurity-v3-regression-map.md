# ModSecurity v3 Regression Map

Status: scaffolded

Source: `/root/conecter/ModSecurity_V3/test/test-cases/regression/`

| Original test path | Purpose | Category | Portable | Capabilities | Known problems | Recommended target |
| --- | --- | --- | --- | --- | --- | --- |
| `operator-rx.json` | Regex operator behavior | engine-core | yes | request headers/body as declared by case | Requires v3 JSON schema mapping | `tests/common/cases/` |
| `operator-*.json` | Operator behavior | engine-core | yes/partial | rule parser, request variables | Some operators require optional libraries | `tests/common/cases/` after capability review |
| `transformation*.json` | Transformation behavior | engine-core | yes | rule parser | Verify v3 expected log matching | `tests/common/cases/` |
| `request-body-parser-*.json` | Request body parser behavior | request-body | partial | request body delivery, body parser | Portable only when driven through v3 public API | `tests/common/cases/` if no connector runtime needed |
| `auditlog.json` | Audit log behavior | audit-log | partial | audit log artifacts | Artifact format normalization unresolved | capability-marked common or connector-specific |
| `debug_log.json` | Debug log behavior | audit-log | partial | debug log artifacts | Debug text is volatile | capability-marked common or connector-specific |
| `variable-*.json` | Variable population | engine-core/request-body/response-body | partial | depends on variable | Some variables depend on connector-supplied data | classify per variable |
| `config-*.json` | Rule/config directives | engine-core | partial | parser, ruleset loading | Some directives depend on files/network | classify per directive |
| `issue-*.json` | Regression for specific bugs | mixed | partial | case-specific | Requires individual review | classify per case |
