# Change Record: CR-20261007-pr396-ci-fixture-contracts

**Language:** English | [Deutsch](CR-20261007-pr396-ci-fixture-contracts.de.md)

Scoped CI remediation for existing Draft PR #396, not a new runtime claim.
Separate source commits: `cee4cdfe191045296f2388e4529e1d4337273a3d`,
`ab7db2dd3be6e10b5bb6a83fc8b7f56949dcb7f7`,
`7da51a310fe7a6a366017f58f556f54bc48bd162`.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261007-pr396-ci-fixture-contracts |
| Date (UTC) | 2026-10-07 |
| Base revision | `1f68c3742bd29b23a6938b36816adff4524944c7` |

## Motivation and problem statement

The resumed PR head has four failed workflow runs: scaffold lint, workflow
security lint, and Envoy on pull-request and push events. Their reproducible
causes are incomplete source-extraction fixtures, a default-deny/publisher-path
contract mismatch, and an overlong Unix socket test path. Current source fixes
and the externally advanced dependency pins must be preserved.

## Acceptance criteria

The old failures reproduce before repair; affected tests and integrated CI
contracts pass without weakening assertions, warnings or guardrails. Preserve
Framework `dc41bd22c335156cae02d9049098b92af65b7c57` and MRTS
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`, as explicitly selected by the user.
Keep PR #396 OPEN/DRAFT/unmerged. Newly published SHA-bound CI/Sonar must pass
before fresh coverage measurement or MIME/Required continuation.

## Implementation decision and rationale

Three independent causes receive separate follow-up commits:

- C test fixtures include the real integrity-emission callee and required POSIX
  headers; the NGINX fixture implements the direct context getter used by the
  current extracted source. No production source or assertion changes.
- The protected workflow denies permissions globally and grants its resolver
  only `contents: read`. Its single exact path is added to both existing closed
  updater allowlists. Actor, protected-master, SHA and privilege controls stay intact.
- The Envoy peer-credential test uses the existing private short-directory
  helper instead of the long test-name directory. Freshness, cleanup and UID
  mismatch rejection before any claim bytes remain intact.

## Changed files

`tests/test_runtime_event_sink_failures.py`,
`tests/test_nginx_request_error_events.py`,
`connectors/envoy/ext_proc/internal/responseobserver/peercred_linux_test.go`,
`.github/workflows/run-protected-nginx-exact-head.yml`,
`.github/workflows/update-workflow-tools.yml`, `ci/tools/update-workflow-tools.py`,
this EN/DE record pair and `reports/audits/change-records/README.md` / `README.de.md`.
No production C/Go, dependency, Framework/MRTS source or Gitlink change.

## Commands executed

Artifacts prefixed `analysis/` resolve under the approved external root
`/var/tmp/codex/ModSecurity-conector`, not the checkout. Exact environment-bound
commands, ownership and results are retained in
`analysis/framework-pr135-sonar-plan.md`. All shell checks used RTK.

Parent interpreter: `/root/git/ModSecurity-conector/.venv/bin/python`.
The integrated C test payload was `-B -m unittest -v` with these modules:

```text
tests.test_runtime_event_sink_failures tests.test_runtime_host_action_validation
tests.test_nginx_request_error_events tests.test_c_source_contract
tests.test_nginx_request_native_results tests.test_nginx_request_phase_completion
tests.test_runtime_transaction_snapshot_contract tests.test_event_runtime_security_contract
```

Baseline: three fixture compilation errors, exit 1. Repaired combined run:
59 tests PASS, no skips, exit 0. Log:
`analysis/pr396-ci-fixtures-integrated-20261007.log` and `.exit`.
Workflow baseline: two exact regressions fail, exit 1. Repaired workflow suite:
31 tests PASS; updater suite: 38 tests PASS. Root native
`rtk proxy env ... make check-ci-security-contract` passed: 219 tests, six
explicit skips, exit 0; tool-lock validate-only checks also passed. Log:
`analysis/pr396-ci-contract-env-bound-20261007.log` and `.exit`. After preparing
the unchanged nested Framework checkout, the same native check passed again:
219 tests, five namespace/identity skips, exit 0; the real reviewed Framework
fixture now ran. Log: `analysis/pr396-ci-contract-nested-20261007.log` and `.exit`.
Root also repeated both complete workflow/updater suites together: 69 tests
PASS, no skips, exit 0; `analysis/pr396-workflow-updater-integrated-20261007.log`.
The initial native invocation exited 2 because a command-line `BUILD_ROOT`
was inherited through `MAKEFLAGS`; the unchanged retry supplied roots through
the environment, like CI. That first failure is retained, not reported as PASS.

Go checks used local Go 1.27.1, external caches, `GOPROXY=off`, `-mod=readonly`
and the same deliberately long external temp root. Test/vet commands ran from
`connectors/envoy/ext_proc`; gofmt ran from the Parent root. An immutable old-source
overlay reproduces `bind: invalid argument`, exit 1. Current commands:

```text
go test -mod=readonly -count=1 -timeout=120s ./internal/responseobserver
go test -mod=readonly -race -count=1 -timeout=120s ./internal/responseobserver
go vet -mod=readonly ./internal/responseobserver
go test -mod=readonly -count=1 -run 'a^' ./cmd/msconnector-envoy-response-observer
gofmt -l connectors/envoy/ext_proc/internal/responseobserver/peercred_linux_test.go
```

All current commands passed through `rtk proxy` with exit 0; the command-package
check is compile-only, not runtime evidence. Logs:
`analysis/pr396-envoy-peercred-{baseline,current,race}-20261007.log` and `.exit`.
Changed-workflow `rtk proxy actionlint` (including ShellCheck) and
`rtk proxy git diff --check` passed. Native bilingual/path/link checks passed,
exit 0: `analysis/pr396-ci-docs-nested-20261007.log` and `.exit`. Initial docs
checks correctly rejected links through an empty nested Framework directory.
An additional full Parent lint attempt exited 2 at the Apache checker's output
default outside the authorized Codex root. The retry uses its existing
`APACHE_C_STANDARDS_OUT` override under the task build root, with unchanged checks;
it reached missing HAProxy headers and broad automatic runtime provisioning, so
it was stopped with exit 130. Neither full lint attempt is PASS. Logs:
`analysis/pr396-parent-lint-20261007.log` and
`analysis/pr396-parent-lint-root-bound-20261007.log`; the latter `.exit` records
the tool-observed interruption, not a completed wrapper receipt. Exact
commands/cwd are retained in the plan. Changed Python files also compiled
successfully with external bytecode output.

## Security impact

No validator, containment, freshness, peer-authentication, event, canonical
status, compiler warning or security assertion is relaxed. The publisher gains
one exact authorized workflow path, not a wildcard or arbitrary write authority.
The existing socket helper creates a private fresh directory and registers cleanup.

## Runtime evidence

No manual host lifecycle, HTTP request, protected-workflow dispatch, new canonical
runtime evidence or Full Exact-Head E2E is executed in this remediation step.
Unit-test sockets and fixture compilations do not prove NGINX runtime coverage.

## Known limitations

The initial six integrated-test skips included an uninitialized Framework fixture;
after its unchanged checkout was prepared, five nobody/mount/PID namespace skips
remain. These are not passing isolation tests.
An arbitrarily long temp-root path itself can still exceed the Unix socket limit.
Historical coverage counts and older CI/Sonar results are not current-head proof.

## Remaining risks

Full local Parent lint remains incomplete; new-head hosted CI and Sonar
readback remain delivery gates. Missing required
runtime evidence remains missing; these fixture/workflow repairs grant no coverage.

## Checks not run and rationale

Full E2E is explicitly prohibited in this step. Protected dispatch and live
publisher execution are not needed for the bounded fixture/allowlist changes.
Fresh coverage/MIME work waits for new-head remote gates. No master merge is authorized.

## Final diff and review status

The scoped six code/test/workflow paths contain 14 insertions and four deletions.
Independent static security review found no validated finding; existing negative
controls remain active. Independent EN/DE review confirmed parity and exact-command
traceability; native documentation checks passed. The final scoped diff is clean;
SHA-bound remote delivery checks remain required. No history rewrite, merge or secret staging.
