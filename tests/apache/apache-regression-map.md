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
| `ModSecurity_V2/tests/run-regression-tests.pl.in` | historical Apache-v2 harness | connector-specific | no | Apache/httpd | v2 architecture only | documentation reference |
