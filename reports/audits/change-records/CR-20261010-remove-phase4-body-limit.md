# Change Record: CR-20261010-remove-phase4-body-limit

**Language:** English | [Deutsch](CR-20261010-remove-phase4-body-limit.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261010-remove-phase4-body-limit |
| Date (UTC) | 2026-10-10 |
| Base revision | `b4044d10682cb2881c218fe84cebe41e61b235c2` |

## Motivation and problem statement

The user explicitly requested repository-wide removal of `modsecurity_phase4_body_limit`, including Apache and Common, before resuming the existing NGINX Exact-Head work. The obsolete compatibility setting was already not an engine WAF inspection policy.

## Acceptance criteria

No active parser, registration, configuration field, supported example or generated configuration inventory retains the removed setting. The Required ID `invalid_size` remains and explicitly tests genuine unknown-directive rejection of the formerly valid input `modsecurity_phase4_body_limit 1048576;`. Engine response-limit cases and independent resource guards remain unchanged.

## Implementation decision and rationale

Remove the public directive rather than silently ignoring it. Keep `SecResponseBodyLimit` and `SecResponseBodyLimitAction` as engine policy. Retain independent request/response storage defaults of 1048576 bytes under dedicated names, plus overflow, chunk/file-read, allocation and host guards. Framework contract migration is separately owned; MRTS is unchanged.

## Changed files

Common configuration, directive specification/adapter and mode accounting; Apache/NGINX registrations and harness configuration; dependent host callers and affected tests. Documentation pairs: connectors/apache/README, connectors/nginx/README, docs/phase4-mode-budget, docs/testing-and-evidence, examples/apache/README and examples/nginx/README. Remove eight example directives. Update ci/checks/documentation/connector_config_reference.py and regenerate both Apache/NGINX configuration-reference pairs and reports/connector-configuration-inventory.json. Keep historical Change Records intact.

## Commands executed

`rtk proxy python3 -B -m unittest tests.test_logical_connector_all_examples.LogicalConnectorAllExamplesTests.test_removed_phase4_body_limit_is_absent_from_host_examples`: initially exit 1 with eight expected example failures. After removal, `rtk proxy python3 -B -m unittest tests.test_logical_connector_all_examples`: exit 0, 12 tests. `rtk proxy make generate-connector-config-reference`: exit 0, five generated files updated. `rtk proxy make check-connector-config-reference`: exit 0, all 21 generated files current. `rtk proxy make check-bilingual-docs`: exit 0. Further integrated verification is recorded separately by the coordinator; it is not claimed here.

Coordinator precommit checks on the removal workingtree based on the revision above: configtest driver24 + selected wiring17 + collection/dispatch58 tests exit0; product-focused45 tests exit0; Common C17 and compiled hardcap/default assertions exit0; four adoption targets exit0. Full native Parent `make lint` exit0 in166.955s, with four temporary clean-Framework-root SKIPs to be rerun after Framework commit. The unrelated broad77 test selection retains three failures and one error, independently reproduced on frozen b404; no assertions were weakened. Assigned shell syntax passes; ShellCheck retains16 identical baseline findings. These are workingtree checks, not a clean new-head runtime claim.

## Security impact

Intentional breaking configuration/API removal; existing operators must remove the directive. This does not disable engine response inspection or authorize unbounded allocation. Existing independent resource protections remain required. Required selection is not reduced and missing evidence cannot become PASS.

## Runtime evidence

No fresh removal-head HTTP/configtest runtime or Full97 result is claimed by this documentation checkpoint. Prior b404 runtime evidence proves only its historical source tuple.

## Known limitations

Formerly valid configurations using the removed directive now fail configuration loading. The four engine response-limit cases remain independent and required.

## Remaining risks

Integrated cross-connector compilation and fresh source-bound config/runtime checks must confirm the final delivered tuple; documentation and unit-test success alone are not that proof.

## Checks not run and rationale

Full97 and Protected Exact-Head were not run for this removal. They remain separate readiness/authorization gates. CI, Sonar, delivery and final source-bound runtime results are not inferred from prior heads.

## Final diff and review status

Scoped documentation/generator and combined source diff inspected by the coordinator and an independent read-only reviewer; no introduced regression identified. Generated files changed through the native generator. The existing Apache duplicate-field absence guard remains active. No commit, push, merge or PR state change was performed by the documentation worker; coordinator delivery and genuine new-head runtime remain separate.
