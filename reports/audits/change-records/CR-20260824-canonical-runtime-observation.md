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
rechecks them. `FND-PARENT-0307` remains fixed pending final exact-head
evidence. The first exact runtime observation reopened `FND-PARENT-0308` and
`FND-PARENT-0309` as in-progress follow-up findings rather than treating a
locally passing unit test as host-runtime proof.

SonarQube Cloud then reported eight task-owned maintainability issues on exact
head `245503cdf75ae58f1077ed4c5679f9640c12ce4a`: six cognitive-complexity
findings and one nested conditional in the contract validator, plus one
cognitive-complexity finding in the normalizer. The normal successor
`a7b8cc199e01f6403616792c598068d24ff645ee` extracted only the existing
metadata traversal, expectation normalization, case/aggregate validation, and
framework-execution predicate into private helpers. Its exact check
`97619927966` passed the Quality Gate but still reported three task-owned
issues: metadata and expectation-dispatch complexity plus an unused private
case parameter. The second narrow successor
`ee7585250f2d7af6279a5fd1b847b76a87a15c99` split those remaining private paths
and removed that unused parameter without changing the closed catalog,
evidence reads, PASS rules, or trust boundaries. Its exact SonarQube Cloud
check `97624800934` passed with zero New Issues. The terminal runtime workflow
then exposed two separate Parent-only integration defects: Common emits Envoy
`rule_id` as canonical JSON text, while the harness accepted only Python
integers; and the legacy external `event.json` leaked the internal
`framework_case` aggregate into a strict Framework compatibility shape. The
third narrow successor `efc2505b76734c19a0ca5766dabb268678dabc12` accepts
only canonical bounded decimal text (or an integer), preserves the exact
`949110` check, and keeps the aggregate solely in the canonical runtime
observation. Its exact SonarQube Cloud check `97632932827` again had zero New
Issues, but its terminal runtime workflow `32791114544` exposed one remaining
external-shape incompatibility: after the Envoy, Lighttpd, and Traefik host
runtimes and Parent normalizer each reported PASS, the strict consumer
rejected `event.host_configuration.reachability_status`. Apache and HAProxy
succeeded. The fourth narrow Parent-only correction omitted that Parent-only
field from the external event while retaining it in the original host producer
summary and canonical runtime observation. Its exact SonarQube Cloud check
`97639330346` for `50955796133b7b29ab601f86e4fe5ffa7030f707` again had zero
New Issues, but terminal workflow `32793251039` exposed the next strict
compatibility mismatch: external host-configuration and cleanup values must
be lowercase `passed`, while Parent's typed/canonical facts remain `PASS`.
The public contract also exact-binds the raw compatibility records, which must
not carry Parent-only adapter, reachability, or intervention fields. This fifth
narrow Parent-only correction maps only already verified Parent PASS facts to
the Framework literal in the external and raw compatibility views; it retains
the original producer summary, canonical assertions, and top-level event
`status: "PASS"`. `FND-SONAR-0060` remains tracked until the new exact pushed
head again proves zero New Issues without a suppression or scanner-control
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
| `python3 -m unittest -q tests.test_runtime_observation_contract tests.test_with_crs_no_mrts_runtime` | Passed after the fifth runtime follow-up: `127 tests in 62.442s`. It covers the requested identity, union, compound, explicit-fact, aggregate, HAProxy, NGINX, path/evidence, exact external-record, and no-fabricated-PASS regressions. |
| Focused runtime-follow-up regression (`test_envoy_intervention_rule_id_accepts_only_canonical_json_values` plus the all-connector normalizer realization) | Passed: `2 tests in 8.541s`. It executes the exact Envoy inline parser with the production JSON-text form and rejects non-canonical or unbounded forms; it also confirms the external event omits `framework_case` while the canonical aggregate remains valid. |
| Focused fourth runtime-follow-up regression (all-connector normalizer realization and exact external-event records) | Passed: `2 tests in 10.843s`. It confirms that the canonical runtime observation retains `reachability.observed == {"status": "PASS"}` while the external `event.host_configuration` omits `reachability_status`. |
| Focused fifth runtime-follow-up regression (all-connector external event, exact raw records, and PASS-to-`passed` mapper) | Passed: `3 tests in 10.173s`. It proves the canonical reachability fact remains `PASS`, the strict external values are `passed`, the raw compatibility records have exactly the published fields, and an unverified value cannot be mapped to `passed`. |
| User-required combined verbose command with `tests.test_ci_security_workflows` | The `127` contract/normalizer cases passed; the command ran `128` entries in `42.928s`, with the final module reported as one import error because the local interpreter lacks `PyYAML`. No dependency was installed or changed. |
| `tests.test_runtime_path_security`, `tests.test_evidence_output_security`, `tests.test_bilingual_docs`, and `tests.test_envoy_transport_hardening_contract` | Passed after the fifth runtime follow-up: `70 tests in 7.575s`. |
| Direct `tests.test_bilingual_docs` confirmation | Passed again after the final Change Record update: `22 tests in 0.274s`. |
| Shell syntax for the CRS/no-MRTS runner and Envoy harness scripts | Passed. |
| Required `py_compile` files | Passed: exit `0`. |
| `python3 -m json.tool ci/runtime/contracts/runtime-observation.schema.json /dev/null` | Passed. |
| `git diff --check` | Passed. |
| Security-diff review | The sealed scan for `a7b8cc19` completed with zero reportable findings. A subsequent focused delta review of the residual semantic-only refactor and the third/fourth compatibility follow-ups found no reportable finding. The fresh review of this fifth exact-record/mapping delta found no reportable finding or false-PASS path: the mapper rejects every non-`PASS` value; canonical assertions, original producer summaries, and digest bindings remain active. The same-UID private-runner writer is an explicit trusted-runner-boundary residual, not a silently suppressed finding. |

The exact local `PyYAML` import limitation is an environment evidence gap, not
a product success or a reason to weaken the CI-security test.

## Checks not run and rationale

`tests.test_ci_security_workflows` was invoked through the user-required
combined command but could not import in this local interpreter because
`PyYAML` is absent. No dependency setup was authorized, so it remains an
honest local limitation rather than a skipped or weakened test. Exact-head
GitHub Actions, SonarQube Cloud, and the terminal connector-runtime workflow
must be checked after each normal push.

`make check-doc-links` was also run and reports only the pre-existing sixteen
links into the deliberately uninitialized Framework gitlink; it reports no
task Change Record defect. Initializing or changing that separate repository is
outside this Parent-only task.

## SonarQube Cloud and coverage

Exact head `245503cdf75ae58f1077ed4c5679f9640c12ce4a` passed its Quality Gate
but reported eight New Issues in SonarQube Cloud check `97609857745`. The first
normal successor `a7b8cc199e01f6403616792c598068d24ff645ee` reduced those to
three in exact check `97619927966`, while still passing the Quality Gate. The
second narrow successor `ee7585250f2d7af6279a5fd1b847b76a87a15c99` passed
exact check `97624800934` with zero New Issues. The third narrow successor
`efc2505b76734c19a0ca5766dabb268678dabc12` passed exact check `97632932827`
with zero New Issues and zero annotations. The fourth narrow successor
`50955796133b7b29ab601f86e4fe5ffa7030f707` passed exact check `97639330346`
with zero New Issues, zero Accepted Issues, zero Security Hotspots, zero
annotations, and zero duplication on new code. That result does not prove this
fifth corrective successor: its own exact-head Sonar result must again show
zero New Issues before delivery is verified. No suppression, `NOSONAR`,
exclusion, acceptance, Quality-Gate change, or coverage workflow change was
made.

```text
No Python coverage report is supplied to SonarCloud.
0.0% is not treated as measured test coverage.
```

## Runtime evidence

The local tests validate contracts, structured normalizer behavior, fixture
identity, and file-safety controls. They are not a live host runtime result.
Exact workflow `32788272062` for `ee758525` reached a terminal failure after
Apache and HAProxy succeeded: Envoy rejected the valid structured string
`"949110"`; Lighttpd and Traefik completed their host paths but the strict
compatibility consumer rejected the extra external `framework_case` key. These
are log-derived causes, not retried or inferred failures.

The exact successor workflow `32791114544` for `efc2505b` also reached a
terminal failure without a retry. Apache and HAProxy succeeded; Envoy,
Lighttpd, and Traefik each recorded a successful host runtime and Parent
normalization before the same strict compatibility consumer rejected the
schema-forbidden external field `host_configuration.reachability_status`.
This is a downstream external-event shape defect, not evidence that
reachability failed or that a PASS was fabricated.

The exact successor workflow `32793251039` for `50955796` then reached a
terminal failure without a retry: Apache and HAProxy succeeded; Envoy,
Lighttpd, and Traefik each again reported host runtime and Parent normalization
PASS before the strict consumer rejected
`host_configuration.config_test_status` because it was `PASS` rather than the
published external constant `passed`. Read-only public interface inspection
also proves exact raw compatibility-record fields and lowercase cleanup status;
the fifth correction addresses those known strict-shape mismatches together.

## Known limitations

No Apache or HAProxy live producer was implemented, no live six-connector by
four-profile matrix was claimed, and Framework/MRTS were not initialized or
modified. The fifth Parent-only repair now requires a new normal push and
fresh exact-head GitHub workflow, SonarQube Cloud analysis, and applicable PR
checks. Any failure requires log-based diagnosis before another commit.

## Security impact

The sealed `a7b8cc19` local scan used a threat model, candidate discovery,
validation, attack-path analysis, focused regressions, and an independent
read-only review; it found zero reportable findings. The later focused delta
review for the residual semantic-only refactor also found no reportable
finding. A focused review of the parser and compatibility-shape follow-up also
found no reportable security finding or false-PASS bypass. The fresh review of
this fourth external-field omission likewise found no reportable finding or
false-PASS path; canonical reachability, raw evidence, digest binding, and
fail-closed validation remain active. The fresh review of this fifth
exact-record/mapping delta also found no reportable finding or false-PASS path:
the mapper rejects every non-`PASS` value, while canonical assertions,
original producer summaries, and digest bindings remain active. No security
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
Cloud found eight maintainability issues. Normal successors `a7b8cc19` and
`ee758525` reduced those to three and then zero. The latter's terminal runtime
failure was diagnosed from the exact Envoy, Lighttpd, and Traefik logs; this
third narrow Parent-only correction reached zero exact-head Sonar issues but
its own terminal runtime failure was again diagnosed from the exact Envoy,
Lighttpd, and Traefik logs. This fourth narrow Parent-only correction precedes
the normal commit/push `50955796`, whose exact Sonar check again reached zero
New Issues but whose terminal runtime failure was diagnosed from the same three
logs. This fifth narrow Parent-only correction precedes the next normal
follow-up commit/push. All exact-head checks, SonarQube Cloud, and `Connector
runtime with CRS and no MRTS` must then be observed again. PR #338 remains
Draft; no merge, auto-merge, Ready transition, rebase, or force-push is
asserted or authorized.
