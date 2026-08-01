# FND-PARENT-0072 — Draft PR #183 has an open Sonar c:S1186 issue for an intentional no-op wrapper

- Category / priority: `sonarqube_finding` / `P3`
- Status / feasibility: `fixed` / `feasible_now`
- Release blocker / candidate-integration blocker / security relevance: `false` / `false` / `false`

SonarQube Cloud historically reported `c:S1186` as **OPEN** at
`ci/checks/connectors/apache/apache_rules_set_cleanup.c:173`: the required
`__wrap_ap_log_perror_` APR-harness linker stub has an intentionally empty body.
Final PR #183 head `4e4dfb36e1b05f7eda38450fd3710e3a04905118` added a
behavior-neutral explanatory comment; its Quality Gate was `OK` and its direct
PR issue API total was `0`.

PR #183 merged as Parent master `154ee724eba4653fa6378fc3c8729ae433e65697`
with equal tree `c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0`; all 14 master-SHA
workflows succeeded. This record is `fixed` and no longer candidate-integration
blocking. It is not `verified` or `closed`: a direct Sonar master analysis and
master issue query remain required and cannot be inferred from the PR receipt,
tree identity, or workflow success.
