# Common Cases

Status: scaffolded

Only portable engine/rule/behavior cases belong here.

Do not add cases that require a specific server/proxy runtime.

`minimal/phase2_args_block.yaml` is a portable rule/request/expectation model.
It becomes a connector pass only when a connector-specific harness executes it
and observes the expected result.

`imported/` contains source-derived portable cases from the local Apache and
NGINX connector test suites. Each imported YAML must include `origin`,
`category`, `capabilities`, `portable: true`, and `status: imported`.
