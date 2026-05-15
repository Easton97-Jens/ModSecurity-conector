# Apache Regression Map

Status: scaffolded

Sources:

- `/root/conecter/ModSecurity-apache/t/`
- `/root/conecter/ModSecurity-apache/tests/`
- historical `/root/conecter/ModSecurity_V2/tests/`

| Original test path | Purpose | Category | Portable | Capabilities | Known problems | Recommended target |
| --- | --- | --- | --- | --- | --- | --- |
| `ModSecurity-apache/t/load-modsec.t` | Apache module loads and serves a file | connector-specific | no | Apache module load | Apache::Test/httpd required | `tests/apache/` |
| `ModSecurity-apache/t/simple-block.t` | Apache location and blocking behavior | connector-specific | no | Apache hooks, intervention | Hook timing is Apache-specific | `tests/apache/` |
| `ModSecurity-apache/t/very-simple-test.t` | Basic Apache request path | connector-specific | no | Apache runtime | Harness-specific | `tests/apache/` |
| `ModSecurity-apache/tests/regression/**/*.t` | v3 Apache regression harness | mixed | partial/no | Apache runtime plus engine | Split only portable rule semantics; keep runtime behavior here | `tests/apache/` or common after review |
| `ModSecurity-apache/tests/regression/rule/00-basics.t` | `ARGS:test` phase:2 deny/status behavior | engine-core via Apache runtime | yes | query args, phase:2, intervention | Log/debug assertions remain Apache-regression-specific | `tests/common/cases/minimal/phase2_args_block.yaml` |
| `ModSecurity-apache/tests/regression/rule/15-json.t` | Content-Type header gating and JSON/body parser coverage | request-body/engine-core via Apache runtime | partial | request headers, request body access | Parsed JSON collection assertions are not in the shared case | `tests/common/cases/minimal/phase1_header_block.yaml`; `tests/common/cases/minimal/request_body_json_block.yaml` |
| `ModSecurity-apache/tests/regression/target/00-targets.t` | ARGS_POST parsing for form bodies | request-body/engine-core via Apache runtime | yes | form body parsing, phase:2 | Shared case asserts HTTP intervention only, not debug-log collection messages | `tests/common/cases/minimal/request_body_urlencoded_block.yaml` |
| `ModSecurity-apache/tests/regression/misc/00-phases.t` | phase execution, including response phase behavior | engine-core via Apache runtime | partial | response header phase | Exact phase/log sequencing remains connector-specific | `tests/common/cases/minimal/response_header_basic.yaml` |
| `ModSecurity_V2/tests/run-regression-tests.pl.in` | historical Apache-v2 harness | connector-specific | no | Apache/httpd | v2 architecture only | documentation reference |
