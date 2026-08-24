# Change Record CR-20260824: Canonical runtime-observation contract closure

**Language:** English | [Deutsch](CR-20260824-canonical-runtime-observation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260824-canonical-runtime-observation` |
| Date (UTC) | `2026-08-24` |
| Base revision | `e776ab75a4e2689955b9c42df6e962e06598c70b` |
| Repository / scope | Parent-only runtime-observation contract closure for Draft PR #338; no Framework or MRTS source, Gitlink, workflow, pin, permission, coverage-transfer, NGINX broker, HAProxy artifact-upload, dependency, or root-runtime change. |
| Previous verified PR head | `e776ab75a4e2689955b9c42df6e962e06598c70b` |
| Final source revision | Pending the authorized normal, non-rewriting commit and push to `codex/canonical-runtime-observation`. The final SHA is deliberately recorded in the PR rather than creating a self-referential commit loop. |
| Delivery disposition | PR #338 remains Draft. No new branch/PR, merge, auto-merge, Ready-for-review transition, rebase, force-push, or default-branch action is authorized. |

## Motivation and problem statement

The previous Parent contract did not close adapter identity tuples, did not
directly prove every public Framework expectation form, and could mix host
runtime outcomes with Framework-case cardinality. The correction must preserve
the established connector trust boundaries while making every PASS-relevant
fact explicit and auditable.

## Acceptance criteria

Close the shared runtime-observation gaps without importing Framework source:

- make `identity.adapter_id` mandatory and validate a closed
  connector/adapter/integration tuple;
- mirror the public 14-kind Framework expectation union with bounded, closed
  recursive `compound` semantics and no public `rule_id` output;
- require explicit typed host facts for every PASS-relevant assertion;
- prevent producers, raw logs, digests, fixtures, step success, and post-run
  compatibility checks from manufacturing a runtime or Framework PASS;
- use a run aggregate with unique Framework cases and checked cardinality
  equations; and
- retain accurate bilingual traceability, local security evidence, and exact-
  head delivery evidence.

## Implementation decision and rationale

The closed catalog is:

| Connector | `adapter_id` | `integration_mode` |
| --- | --- | --- |
| Apache | `apache-native-httpd-module` | `native-httpd-module` |
| Envoy | `envoy-ext-proc-service` | `ext_proc` |
| Lighttpd | `lighttpd-patched-native-module` | `patched-native-lighttpd` |
| Traefik | `traefik-native-middleware` | `native-traefik-middleware` |
| NGINX | `native-nginx-http-module` | `native-nginx-http-module` |
| HAProxy SPOE/SPOP | `haproxy-spoe-spop-agent` | `spoe-spop-agent` |
| HAProxy native HTX | `haproxy-native-htx-filter` | `native-htx-filter` |

The generic live adapter remains limited to Envoy, Lighttpd, and Traefik.
Apache and both HAProxy paths have canonical fixtures only and fail closed for
live claims; the protected NGINX broker boundary is unchanged. Separate HAProxy
fixtures prevent evidence crossing between SPOE/SPOP and native HTX.

The public expectation union is exactly `http_status`, `intervention`,
`action`, `rule_match`, `event`, `request_headers`, `response_headers`,
`request_body`, `response_body`, `transport`, `lifecycle`, `cleanup`,
`compound`, and `not_applicable`. Legacy `rule_id` is normalized only at the
compatibility boundary to `rule_match`. Schema `oneOf` and
`additionalProperties: false` shape the union; Python remains the authoritative
semantic validator. `compound` limits depth to four and conditions to 2–16,
rejects empty/duplicate/unknown/unsafe members, raw payloads/logs, and absolute
paths.

`StructuredObservationInput` now receives named configuration, start,
reachability, expected/observed status, action, trigger, intervention,
Framework, and cleanup facts. Missing facts remain `PARTIAL` or
`VALIDATION_FAILED`; disagreement remains failed. Digests bind files but never
replace an observation.

For the selected CRS smoke, the Parent normalizer derives one
`crs_sqli_anomaly_block` case only after separately validating the typed live
host facts. It does not copy Framework status from a producer, and the later
public Framework `validate` command is compatibility-only: it cannot promote a
Parent result or claim Framework-source/runner execution. The run aggregate
checks `selected = executed + unsupported + not_applicable + not_executed` and
`executed = passed + failed + cancelled`; Framework scenario category remains
Framework metadata rather than a profile-derived Parent category.

The validator also now fails closed for unhashable closed literals and
excessive/cyclic metadata. Envoy and Lighttpd derive CRS intervention IDs from
validated structured final events instead of summary literals; the normalizer
rechecks them. These focused remediations are tracked locally as
`FND-PARENT-0307`, `FND-PARENT-0308`, and `FND-PARENT-0309`, fixed locally and
pending exact-head verification.

SonarQube Cloud then reported eight task-owned maintainability issues on exact
head `245503cdf75ae58f1077ed4c5679f9640c12ce4a`: six cognitive-complexity
findings and one nested conditional in the contract validator, plus one
cognitive-complexity finding in the normalizer. The successor source change
only extracts the existing metadata traversal, expectation normalization,
case/aggregate validation, and framework-execution predicate into private
helpers; it does not change the closed catalog, evidence reads, PASS rules, or
trust boundaries. `FND-SONAR-0060` tracks this remediation until the exact
successor head proves zero New Issues without a suppression or scanner-control
change.

## Changed files

- `ci/runtime/contracts/README.md` and `ci/runtime/contracts/README.de.md`
- `ci/runtime/contracts/runtime-observation.schema.json`
- `ci/runtime/contracts/runtime_observation.py`
- `ci/runtime/contracts/runtime_observation_adapters.py`
- `ci/runtime/contracts/validate-runtime-observation.py`
- `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py`
- `ci/runtime/lifecycle/run-with-crs-no-mrts.sh`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `tests/fixtures/runtime-observation/apache-no-crs-no-mrts.json`
- deleted `tests/fixtures/runtime-observation/haproxy-no-crs-no-mrts.json`
- added `tests/fixtures/runtime-observation/haproxy-spoe-spop-no-crs-no-mrts.json`
- added `tests/fixtures/runtime-observation/haproxy-native-htx-no-crs-no-mrts.json`
- `tests/test_runtime_observation_contract.py`
- `tests/test_with_crs_no_mrts_runtime.py`
- this Change Record and its German companion.

## Commands executed

| Check | Actual result |
| --- | --- |
| `python3 -m unittest -q tests.test_runtime_observation_contract tests.test_with_crs_no_mrts_runtime` | Passed after the Sonar refactor: `125 tests in 274.202s`. It covers the requested identity, union, compound, explicit-fact, aggregate, HAProxy, NGINX, path/evidence, and no-fabricated-PASS regressions. |
| User-required combined verbose command with `tests.test_ci_security_workflows` | The contract/normalizer cases passed; the command ran `126` entries in `67.036s`, with the final module reported as one import error because the local interpreter lacks `PyYAML`. No dependency was installed or changed. |
| `tests.test_runtime_path_security`, `tests.test_evidence_output_security`, `tests.test_bilingual_docs`, and `tests.test_envoy_transport_hardening_contract` | Passed after the Sonar refactor: `70 tests in 9.723s`. |
| Direct `tests.test_bilingual_docs` confirmation | Passed: `22 tests in 0.312s`. |
| Shell syntax for the CRS/no-MRTS runner script | Passed. |
| Required `py_compile` files | Passed: exit `0`. |
| `python3 -m json.tool ci/runtime/contracts/runtime-observation.schema.json /dev/null` | Passed. |
| `git diff --check` | Passed. |
| Terminal security-diff scan | Completed with complete coverage and zero reportable current findings. The same-UID private-runner writer is an explicit trusted-runner-boundary residual, not a silently suppressed finding. |

The exact local `PyYAML` import limitation is an environment evidence gap, not
a product success or a reason to weaken the CI-security test.

## Checks not run and rationale

`tests.test_ci_security_workflows` was invoked through the user-required
combined command but could not import in this local interpreter because
`PyYAML` is absent. No dependency setup was authorized, so it remains an
honest local limitation rather than a skipped or weakened test. Exact-head
GitHub Actions, SonarQube Cloud, and the terminal connector-runtime workflow
must be checked after each normal push.

## SonarQube Cloud and coverage

Exact head `245503cdf75ae58f1077ed4c5679f9640c12ce4a` passed its Quality Gate
but reported eight New Issues in SonarQube Cloud check `97609857745`. They are
the task-owned maintainability findings remediated by the successor source
change. Prior comments and check runs are not evidence for that successor:
its exact-head Sonar result must show zero New Issues before delivery is
verified. No suppression, `NOSONAR`, exclusion, acceptance, Quality-Gate
change, or coverage workflow change was made.

```text
No Python coverage report is supplied to SonarCloud.
0.0% is not treated as measured test coverage.
```

## Runtime evidence

The local tests validate contracts, structured normalizer behavior, fixture
identity, and file-safety controls. They are not a live host runtime result.

## Known limitations

No Apache or HAProxy live producer was implemented, no live six-connector by
four-profile matrix was claimed, and Framework/MRTS were not initialized or
modified. The terminal exact-head GitHub workflow `Connector runtime with CRS
and no MRTS`, SonarQube Cloud analysis, and all relevant PR checks must be
observed after push; any failure requires log-based diagnosis before another
commit.

## Security impact

The terminal current-local-patch scan used a threat model, candidate discovery,
validation, attack-path analysis, focused regressions, and an independent
read-only review. It found zero reportable current vulnerabilities. No security
control or trust boundary was weakened for this change.

## Remaining risks

The documented same-UID private-root limitation is retained because an actor already
authorized inside that root is within the trusted-runner model; adding
attestation/signatures would be separate scope.

## Final diff and review status

The initial task commit `f2fcb71f47e69f33d888dd89e1b871656e02fc38` was pushed
normally to the existing PR #338 branch. Its exact-head `lint` run identified
this Change Record's missing required template sections; the focused
documentation correction `245503cdf75ae58f1077ed4c5679f9640c12ce4a` was the
resulting remediation, not a blind rerun. That head passed lint but SonarQube
Cloud found eight maintainability issues, so the focused source refactor and
this evidence update precede one normal follow-up commit/push. All exact-head
checks, SonarQube Cloud, and `Connector runtime with CRS and no MRTS` must then
be observed again. PR #338 remains Draft; no merge, auto-merge, Ready
transition, rebase, or force-push is asserted or authorized.
