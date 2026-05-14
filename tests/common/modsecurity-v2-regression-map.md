# ModSecurity v2 Regression Map

Status: scaffolded

Source: `/root/conecter/ModSecurity_V2/tests/`

| Original test path | Purpose | Category | Portable | Capabilities | Known problems | Recommended target |
| --- | --- | --- | --- | --- | --- | --- |
| `tests/op/*.t` | Operator semantics | engine-core | partially | rule parser/operator execution | Perl format must be converted to v3-style cases | `tests/common/cases/` after v3 parity review |
| `tests/tfn/*.t` | Transformation semantics | engine-core | partially | transformation execution | Perl format must be converted | `tests/common/cases/` after v3 parity review |
| `tests/regression/misc/00-phases.t` | Phase behavior | engine-core/connector-specific | partially | all transaction phases | Depends on HTTP server and logs in v2 harness | split portable phase expectations from connector tests |
| `tests/regression/config/*.t` | Configuration directives | engine-core | partially | ruleset loading, files, logs | Some directives are environment-specific | classify per directive |
| `tests/regression/action/*.t` | Action behavior | engine-core/audit-log | partially | interventions, logs | Exact log text may be v2-specific | common only with normalization |
| `tests/regression/rule/*.t` | Rule behavior | engine-core | partially | parser, variables | Some tests require server context | classify per case |
| `tests/regression/misc/*multipart*.t` | Multipart parser behavior | request-body | partially | request body parser | Must compare against v3 parser behavior | common only if v3 public API can drive it |
| `tests/run-regression-tests.pl.in` | Apache/httpd regression harness | connector-specific | no | Apache runtime | v2 architecture and Apache assumptions | documentation only or `tests/apache/` reference |
