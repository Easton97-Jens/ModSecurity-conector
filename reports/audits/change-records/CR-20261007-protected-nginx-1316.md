# Change Record: CR-20261007-protected-nginx-1316

**Language:** English | [Deutsch](CR-20261007-protected-nginx-1316.de.md)

User-authorized closed release-contract alignment; no runtime or Full E2E claim.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261007-protected-nginx-1316 |
| Date (UTC) | 2026-10-07 |
| Base revision | `60034d48dcee4ae5225bfaff012c48413cc0acd8` |

## Motivation and problem statement

The current Parent and approved Framework already pin NGINX 1.31.6. The protected
builder, Root launcher and result collector still admitted only 1.31.5, causing
the Parent provenance and release-agreement tests to fail. The user explicitly
authorized the separate protected update; the generic Framework updater remains
excluded from this release contract.

## Acceptance criteria

All three protected boundaries must accept the reviewed 1.31.6 tuple and reject
the complete previous 1.31.5 tuple, crossed version/digest pairs and arbitrary
pins. Existing authorization, path authority, manifest identity and runtime
validation remain strict. Dependency Gitlinks and prior commits remain unchanged.

## Implementation decision and rationale

Change exactly six constants, keeping every other production byte unchanged:
version `1.31.6` and source SHA256
`974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1`.
The existing Parent provenance tuple and Framework `common.sh` agree with the
[official release asset metadata](https://github.com/nginx/nginx/releases/tag/release-1.31.6)
for `nginx-1.31.6.tar.gz` (published 2026-09-15; 1,373,124 bytes).
This metadata check is not downloaded-archive or runtime attestation.

Framework remains `dc41bd22c335156cae02d9049098b92af65b7c57`; MRTS remains
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Changed files

Three production files under `ci/runtime/broker/`:
`protected_nginx_exact_head_builder.py`, `nginx_exact_head_root_launcher.py`,
`nginx_exact_head_result_collector.py`; their three corresponding test modules
under `tests/`; this EN/DE record pair and the EN/DE archive indices.
No Framework, MRTS, Gitlink, generic updater or workflow changes in this commit.

## Commands executed

All shell checks use RTK and the Parent interpreter
`/root/git/ModSecurity-conector/.venv/bin/python`. Temporary files, logs and
bytecode live below `/var/tmp/codex/ModSecurity-conector/analysis`, not the checkout.
Command scope, environment and evidence references are recorded in
`analysis/framework-pr135-sonar-plan.md` under that external root;
exact invocations remain in the task tool history.

The new `test_rejects_previous_release_and_crossed_*_pins` methods at the builder,
launcher and collector boundaries first ran against unchanged production:
three failures, exit 1, because the complete old tuple was accepted. After the
constant patch: three tests PASS, exit 0; all nine negative combinations rejected.
Logs: `analysis/nginx1316-tuple-{red,green}-20261007.log` and `.exit`.
Builder archive tests mock only the observed descriptor hash, not expected pins.
Old archive names reject before hashing; current name/old hash tests digest rejection.

```text
-B -m unittest -v tests.test_protected_nginx_exact_head_builder
  tests.test_nginx_exact_head_root_launcher tests.test_nginx_exact_head_result_collector
-B -m unittest -v tests.test_protected_nginx_exact_head_workflow
  tests.test_protected_nginx_exact_head_dispatcher tests.test_protected_nginx_exact_head_runner_preflight
  tests.test_nginx_exact_head_base_helper tests.test_nginx_exact_head_gate_contract
  tests.test_nginx_exact_head_diagnostics tests.test_protected_nginx_broker_caller
```

Full three boundary suites: 91 tests PASS, no skips, exit 0. Protected neighbors:
76 tests PASS, no skips, exit 0. Current-pin/selection/wiring focus: 31 tests PASS,
no skips, exit 0, including the actual trusted Framework API. Logs:
`analysis/nginx1316-{three-suites,protected-neighbors,current-pins-wiring}-20261007.log`.
The repeated eight C-fixture modules also pass: 59 tests, no skips, exit 0;
`analysis/nginx1316-ci-fixtures-20261007.log`.

Python compilation of all six changed files and `rtk proxy git diff --check`
pass. An exact source comparison confirms only the six approved substitutions.
Native `make check-ci-security-contract`: 219 tests run, 214 passed and five
explicit namespace/identity skips, exit 0; tool-lock validate-only checks pass. Complete
workflow/updater repeat: 69 tests PASS, no skips, exit 0. Logs:
`analysis/nginx1316-{ci-security-contract,workflow-updater}-20261007.log` and `.exit`.
Native `make check-bilingual-docs check-doc-links` and archive-only
`ci/tools/new-change-record.py check` pass. Changed-workflow
`rtk proxy actionlint .github/workflows/run-protected-nginx-exact-head.yml`
(including ShellCheck) passes. Documentation log:
`analysis/nginx1316-docs-20261007.log`, exit 0. The first actionlint attempt used
a nonexistent shortened filename and exited 3; it is not a lint PASS.

## Security impact

No guard, schema, permission, isolation, containment, freshness, no-follow,
evidence validator, warning or test assertion is weakened. The old release is
removed from the closed allowlist, not admitted alongside the new release.
The protected workflow's trusted-tool/master eligibility rules remain unchanged;
updating these constants does not make a stacked PR eligible for protected dispatch.

## Runtime evidence

None produced. Unit manifests, private collector fixtures and mocked source
hashes are contract tests, not real HTTP, Root→nobody or canonical coverage evidence.
No manual lifecycle or protected dispatch was executed.

## Known limitations

A full local Parent lint attempt from the previous repair remains incomplete:
the initial output-root failure and interrupted broad provisioning are not PASS.
Namespace/identity tests may require capabilities unavailable locally; explicit
skips receive no isolation credit. Historical CI and Sonar results do not prove
the new commit. Fresh remote results must be bound to the published successor SHA.

## Remaining risks

The unit and static checks do not establish a new binary or protected runtime
attestation. New-head hosted CI and applicable Sonar readback remain delivery
gates. Broader fresh coverage/MIME work waits for those gates.

## Checks not run and rationale

No Full E2E, protected workflow dispatch, package installation, Framework/MRTS
change, master push or merge is authorized in this bounded follow-up. No archive
download/build is needed to fix and test the closed tuple mismatch.

## Final diff and review status

Six production substitutions and 60 test insertions; no existing assertions
removed. Independent bounded security review found no validated finding.
The original RED evidence is retained. Separate follow-up commit, no amend or
history rewrite; PR #396 remains OPEN/DRAFT. Remote gates are not preclaimed.
