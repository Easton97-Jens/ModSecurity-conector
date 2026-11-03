# Change Record: CR-20261103-explicit-mrts-handoff

**Language:** English | [Deutsch](CR-20261103-explicit-mrts-handoff.de.md)

Enable an explicit reviewed handoff of the nested MRTS pin.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261103-explicit-mrts-handoff |
| Date (UTC) | 2026-11-03 |
| Base revision | `0a7fae33cd9ccb09c11ca58ea6c13d206cfff478` |

## Motivation and problem statement

The existing synchronizer changed the Framework selection while retaining the nested MRTS lock. The candidate verifier correctly rejected a candidate with a different MRTS gitlink. The explicitly approved joint integration therefore needed a guarded handoff rather than a manual lock edit.

## Acceptance criteria

Require an explicit exact lowercase 40-character MRTS approval with the Framework SHA. Validate the old lock against the old Framework Git object and the approved MRTS against the candidate object before writes. Preserve default selection behavior, closed lock keys, toolchains, protected broker identities and transactional publication.

## Implementation decision and rationale

Add synchronizer --mrts-sha and verifier --expected-candidate-mrts-sha, propagated through API, CLI and verify-primary. The existing immutable Git reader proves both gitlinks. Explicit approval requires a real Framework object directory; malformed, missing, mismatched or dishonest provenance fails closed. Without approval the synchronizer retains the locked MRTS and the candidate verifier still requires that locked selection. The option is a reviewed input, not remote approval authority.

## Changed files

Parent ci/tools/sync-framework-component-versions.py and ci/tools/verify-framework-candidate-contract.py; docs/security/ci-security-tooling.md and its German companion; this Change Record pair. Existing Framework test_update_framework_versions.py and test_verify_framework_candidate_contract.py receive scoped regressions in their separate repository.

## Commands executed

RTK-wrapped explicit Framework CPython3.15.2 ran unittest modules modsecurity_connector_tests.test_update_framework_versions and modsecurity_connector_tests.test_verify_framework_candidate_contract: 79 tests PASS in 158.096s. Actual candidate 00de6d61122c85120c3a06e84e46906f87165744 / MRTS ee2174431c4edf97e66afe32558ce8454deb2397 passed dry rendering and the public verifier; every original Parent primary byte remained unchanged. Default verifier rejection was retained. Exact commands, results and immutable fixture provenance are in the integration task parent-mrts-handoff directory. Ruff retained 17 pre-existing diagnostics across the four sources, with no new diagnostics against exact Parent/F bases.

## Security impact

No automatic MRTS adoption or arbitrary lock write is introduced. Missing approval, malformed input, candidate mismatch, dishonest old lock, missing objects and symlink authority have no-write regressions. Existing protected identities and transactional locking remain enforced. Three existing fixture assumptions were corrected using exact baseline bytes: one closed inline-caller registry entry, renderer keyword forwarding while retaining the flock assertion, and one real caller Git SHA used consistently through rendering and publication verification.

## Runtime evidence

No hosts were launched. This source-level contract proof does not replace the coordinator-owned final integrated protocol executions.

## Known limitations

The actual candidate proof uses a pre-merge Framework commit, not the future merge SHA. The coordinator must bind the actual Framework merge and approved MRTS merge through the native tools and regenerate dependent inventories and archives.

## Remaining risks

Current-head hosted checks, final pin application, metadata regeneration and final integrated runtime evidence remain coordinator-owned delivery gates. Independent historical findings remain separate.

## Checks not run and rationale

No full suite, local Sonar scan, installation/authentication repair, publisher or protected broker dispatch, administrative action, commit or Git delivery was performed by this worker. Local Sonar operations remain suspended by user instruction.

## Final diff and review status

The bounded source/test diff passed all 79 affected regressions. Independent read-only review found no material issue. Final metadata and exact-head hosted validation remain the coordinator responsibility.
