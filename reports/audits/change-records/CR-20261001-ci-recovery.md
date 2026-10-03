# Change Record: CR-20261001-ci-recovery

**Language:** English | [Deutsch](CR-20261001-ci-recovery.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261001-ci-recovery |
| Date (UTC) | 2026-10-01 |
| Base revision | `b0f3bdab429717b5b0311c30c5b4d1153c672ac0` |

## Motivation and problem statement

Recover the failures reported in Parent run [36906913089](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36906913089) and Framework run [36703337419](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/36703337419), and inspect current CI for related failures. Parent maintenance wrongly applied the single-bot-commit rule to a reviewed, merged maintenance branch. Additional gaps included long Unix socket paths, rejection of the provisioned Traefik host stage, broker permission/tag-fetch contracts, incomplete updater inventory/copied-tree inputs, and transient artifact cleanup API failures.

The user subsequently requested one maintained location for `FRAMEWORK_SHA`,
other ordinary revision pins, component selections and toolchains. This extends
the requested repair scope; it does not authorize Framework/MRTS source edits
or protected broker activation.

## Acceptance criteria

Regression checks must cover the original defects without weakening publisher identity, runtime isolation, immutable pins, or deny-default permissions. Current hosted Framework publication and its PR checks must succeed. Parent hosted validation and protected broker activation remain required before claiming all workflows work.

Ordinary revision and toolchain consumers must use one strict Parent record;
independent gitlink/commit provenance, component ownership and narrow updater
field scopes must remain enforced.

## Implementation decision and rationale

Keep open maintenance branches constrained to the configured App; allow reuse of reviewed merged remediation history only after checking PR identity, merge ancestry, and current branch guards. Allocate private, short socket directories while retaining revision-bound artifact roots. Admit only the exact provisioned Traefik host path. Accept the broker caller's exact empty permission mapping and independently acquire/check the approved CRS tag. Complete the explicit updater publisher inventory and read-only copied baseline; run focused inventory coverage in Make and the full suite in CI to avoid recursive candidate validation. Derive action-pin assertions from the central lock. Retry artifact cleanup API calls three times.

The socket wrapper's follow-up interface correction preserves private `0700` roots, ownership/safe-ancestor checks, socket byte limits, termination verification, and retention on unsafe cleanup. Its low-level command runner remains an internal test API rather than CLI command input. Fresh-head hosted/quality evidence is required after this source change.

Fresh hosted Apache CRS job `110539160124` in [run 36912740744](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912740744) exposed another required repair: the pinned HTTPD `2.4.68` URL `https://downloads.apache.org/httpd/httpd-2.4.68.tar.bz2` returned `404`, while the identical official archive URL `https://archive.apache.org/dist/httpd/httpd-2.4.68.tar.bz2` returned `200`. The literal SHA-256 stays `68c74d4df38c26bed4dfbdb8f3baf1eb532f3872357becc1bba5d136f6b63c06`. Parent provisioning independently implements the exact direct-404, same-basename official archive recovery already present in reviewed Framework master. It requires explicit HTTPD opt-in, forbids redirect/authentication/timeout/foreign-component fallbacks, verifies the literal digest before archive listing, and preserves canonical cache identity with actual-download metadata. The selected Framework gitlink is synchronized into the CRS workflow and its contract fixture; `common.sh`, `.gitmodules`, and the MRTS revision remain unchanged.

The canonical Traefik No-CRS host built and started but its route failed because
Yaegi disabled the observer's `syscall` import. The pinned Traefik `3.7.13`
loader reproduced this failure. The fixed observer manifest now declares
`useUnsafe: true`, and only its per-plugin operator settings explicitly enable
that requirement; both declarations are necessary. Static configuration and
both smoke entry points enable `experimental.abortOnPluginFailure` to fail
startup when loading fails. The source remains the fixed checked-in observer,
staged without symlinks in a private workspace. No global/other-plugin opt-in
is introduced, and the Linux `SO_PEERCRED` UID/GID authentication remains
intact rather than being removed to bypass the import failure.

Centralize ordinary selections in the exact five-field data record
`ci/tooling/project-versions.lock.json`: schema `1`, Framework/MRTS revisions,
Python `3.14.7` and Go `1.27.1`. Generated `.python-version`/`.go-version`
views remain compatible with setup actions; the Go module floor `1.26.5`
remains distinct. Component definitions continue to belong to the selected
Framework's `ci/lib/common.sh`; the immutable Framework pin selects that source
without duplicating component authority. Protected broker tuples remain
independent. The reader checks the exact Parent Git blob, recorded gitlinks and
materialized independent repository HEADs with replacement objects disabled.
Updaters preserve unrelated central fields, validate existing and new candidates,
and share a directory `flock`. Identity/content checks and replacement tracking
before directory fsync guard rollback without claiming crash-atomic multi-file
updates. The paired [version-pins reference](../../../docs/reference/version-pins.md)
explains these controls and native view synchronization.

A further real-host Traefik failure returned `503`/`403` instead of the allow
control: Yaegi selected the non-Linux peer-credential stub when only modern
`//go:build` constraints were present. Matching legacy `// +build linux` and
`// +build !linux` lines now accompany both modern constraints. This preserves
the non-Linux fail-closed behavior and Linux UID/GID authentication.

The sequential smoke report failure was a producer/input mismatch: its native
Apache/NGINX producer cannot supply the full-matrix/MRTS inputs expected by the
general strict refresh. Dedicated `test-smoke-sequential-no-crs` and
`test-smoke-sequential-with-crs` targets now invoke `bounded-smoke` only for that
workflow. General `test-no-crs`/`test-with-crs` and the complete
`refresh-all-reports` (`--strict-inputs`) catalog remain intact. Current native
case discovery supplies Apache 54 and NGINX 60 cases in the diagnosed scope;
validation discovers exact variant-specific sets instead of hardcoding counts.
Fresh same-run coverage and runtime-cache reports are mandatory. A private
receipt is bound through exact Parent blob/gitlink checks to Framework/MRTS,
the fixed module path, run identity and native case selection. All rows must
match variant/connector, be live and pass without exceptions. Missing/extra
cases, revision/variant drift, stale/symlinked inputs and failed/blocked producer
return codes fail. The snapshot generator must produce fresh Parent-owned,
run-bound output; generated reports are not staged. This aligns validation with
the real producer and does not weaken the full gate or promote full-matrix,
MRTS or response-body evidence.

A required With-CRS bootstrap correction follows the report profile: superseded
`5605febc` job `111165203104` genuinely failed at `08:43` UTC because
`prepare-fresh-crs-source.sh` called `ci_require_absolute_path` before the
Framework `ci/lib/common.sh` was loaded. This failure occurred despite a
cancellation request; it is not classified as cancellation-only. Runtime
returned `77` before producer inputs existed, and the fresh-input gate correctly
rejected the missing Apache result. The bounded recipe now sources the actual
Framework common helper before the Parent CRS helper. Executed shell regression
covers both variants, a fresh `RESULTS_DIR`, empty inherited scope flags, and
fetch-before-producer ordering and actual relative-path rejection before
fetching. The 18-test profile run passed in 9.315 seconds. Full report/case validation remains intact.

## Changed files

- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/cleanup-artifacts.yml`
- `.github/workflows/nginx-root-broker.yml`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `.github/workflows/test-full-smoke-sequential.yml`
- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-traefik.yml`
- `.github/workflows/update-go-version.yml`
- `.github/workflows/update-python-version.yml`
- `.github/workflows/update-submodules.yml`
- `.github/workflows/update-workflow-tools.yml`
- `Makefile`
- `ci/lib/framework_revision_pins.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/evidence/reports/refresh-connector-reports.py`
- `ci/runtime/broker/nginx_root_broker.py`
- `ci/runtime/lifecycle/run-connector-stage.sh`
- `ci/runtime/lifecycle/with-private-sockets.py`
- `ci/tooling/project-versions.lock.json`
- `ci/tools/read-framework-revisions.py`
- `ci/tools/sync-framework-component-versions.py`
- `ci/tools/sync-project-versions.py`
- `ci/tools/update-workflow-tools.py`
- `ci/tools/verify-framework-candidate-contract.py`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/start_envoy_connector.sh`
- `connectors/traefik/config/traefik-response-observer-static.yaml`
- `connectors/traefik/response_observer/.traefik.yml`
- `connectors/traefik/response_observer/peercred_linux.go`
- `connectors/traefik/response_observer/peercred_other.go`
- `connectors/traefik/scripts/runtime_smoke.py`
- `connectors/apache/src/mod_security3.c`
- `connectors/apache/src/msc_filters.c`
- `connectors/nginx/config`
- `connectors/traefik/scripts/start-smoke.sh`
- `docs/reference/variables.de.md`
- `docs/reference/variables.md`
- `docs/reference/version-pins.de.md`
- `docs/reference/version-pins.md`
- `docs/security/ci-security-tooling.de.md`
- `docs/security/ci-security-tooling.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- `docs/security/trusted-nginx-root-broker.md`
- `modules/ModSecurity-test-Framework`
- `reports/audits/change-records/CR-20261001-ci-recovery.de.md`
- `reports/audits/change-records/CR-20261001-ci-recovery.md`
- `scripts/version_updater_common.py`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/framework_sha_fixture.py`
- `tests/test_apache_intervention_cleanup.py`
- `tests/test_c_cpp_diagnostics.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_full_smoke_workflow_contract.py`
- `tests/test_framework_revision_pins.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_private_runtime_sockets.py`
- `tests/test_project_toolchain_pins.py`
- `tests/test_runtime_env_snapshot_contract.py`
- `tests/test_traefik_runtime_smoke_security.py`
- `tests/test_update_framework_versions.py`
- `tests/test_update_go_version.py`
- `tests/test_update_python_version.py`
- `tests/test_update_submodules_local_git.py`
- `tests/test_verify_framework_candidate_contract.py`
- `tests/version_updater_test_support.py`

## Commands executed

All local command entry points used RTK. `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract`: PASS, 175 tests, five existing environment skips, plus actionlint/zizmor/gitleaks provenance validation. The updater suite passed 38 tests, including real proposed-tree validation; workflow contracts passed 31 tests. Coordinated integrated regression validation passed 118 tests. Actionlint passed all 31 workflows. Quick-check timed out after 600 seconds at the HAProxy check; this is not a full quick-check pass.

```sh
rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_private_runtime_sockets tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_nginx_root_broker_crs_profile tests.ci_security.test_update_workflow_tools
rtk proxy bash -c '/root/go/bin/actionlint .github/workflows/*.yml'
```

The integrated 118-test run completed in 98.147 seconds. Task evidence is retained in `/var/tmp/codex/ModSecurity-conector/ci-recovery-inventory.md`, `/var/tmp/codex/ModSecurity-conector/ci-recovery-20261001-plan.md`, and `/var/tmp/codex/ModSecurity-conector/ci-recovery-ci-contract.log`.

The bounded repeat of `rtk proxy env CI=true ... timeout 600 make quick-check`, using the same external build/log roots and interpreters, passed (exit 0, 275 tests). Native lint explicitly skipped NGINX and HAProxy C17 compilation because their headers were absent. The earlier local timeout occurred during automatic prerequisite provisioning before HAProxy compiler probes. These results do not prove the two skipped compiler checks. The repeat log is `/var/tmp/codex/ModSecurity-conector/ci-recovery-quick-check-ci.log`.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links
rtk git diff --check
```

Record structure, bilingual documentation, repository path references, documentation links, and diff whitespace checks passed.

The closed-CLI integrated validation snapshot passed 121 tests in 101.701 seconds. The Framework-owned Python 3.14.7 `test-httpd-source-recovery` target passed 18 tests in 57.008 seconds on selected master `6948ec5b916e400c4fcaa1b6ccfa64251f606f8d`; candidate contract verification and native synchronization check passed. The Parent preparation suite passed 95 tests with five existing skips; the generic cache contract passed 45 tests. Live Parent HTTPD acquisition recovered the same official archive after the canonical 404 and verified SHA-256 `68c74d4df38c26bed4dfbdb8f3baf1eb532f3872357becc1bba5d136f6b63c06` before archive listing. Before committing the selected gitlink, a further CI-mode native quick-check passed (exit 0, 280 tests) after the HTTPD/Framework changes, with nine fixture skips because the selected Framework checkout was newer than the still-committed Parent gitlink, plus the two missing-header compiler skips. The log is `/var/tmp/codex/ModSecurity-conector/ci-recovery-quick-check-final.log`. These checks prove acquisition and their respective local contracts; they do not constitute a fresh Parent hosted HTTPD runtime pass or a new Sonar pass.

The hash-verified Traefik 3.7.13 host passed all 20 runtime-security tests, including real route loading and startup rejection when either import declaration is missing. The observer's native Go unit tests and vet also passed with the existing Go 1.27.1 toolchain. These checks prove loader behavior and observer source checks; complete hosted engine transactions remain separate evidence.

The coordinated central-lock regression snapshots passed 18 reader tests,
16 toolchain tests, an 83-test combined suite and 55 Framework synchronizer tests.
These are scoped snapshots; final integrated and hosted evidence for the new
source head remains required. Hash-verified Traefik host/engine validation passed
29 tests without skips, including authenticated `MRC1` `CLAIM` success for the
same UID and rejection of a wrong UID before frame bytes. Observer Go unit/vet
checks passed and the non-Linux stub remained fail-closed. A real current C
service plus pinned Traefik local runtime observed allow `200` and deny `403`.
These local checks do not replace final-head hosted engine evidence.

The subsequent native centralization validation passed 216 CI-security-contract
tests with five existing environment/privilege skips, 38 full workflow/tool
updater tests, and 74 updater/language-contract tests. The 19 reader and 16
central-toolchain tests are included in the 216-test contract result. Actionlint
passed all 31 workflows; bilingual, link, variable and connector configuration
checks passed, with 21 generated configuration files current. These checks do
not establish hosted runtime success. The legacy event-path and full-NGINX profile-registry-root source repairs are
now implemented as described below; the Apache `413` source repair is also implemented, with separate local evidence below.
No all-workflow pass is claimed.

The legacy Traefik smoke starter now materializes only its checked-in default
configuration into the private run directory with a run-local `event_path`;
an explicitly supplied configuration remains unchanged. Staged NGINX config
resolves a missing profile registry only from a supplied canonical
`common/include` layout containing the SDK header. Explicit registry-root
priority is retained, and invalid or unrelated roots fail. The diagnostics
regression executed four positive/negative config-prefix cases. Traefik
security validation passed 31 tests with two missing-host skips in that local
run; a separate actual C service plus pinned-host startup check passed.
A native quick-check after these completed fixes passed (exit 0, 280 tests,
no unit skips), with only the two explicit missing-header NGINX/HAProxy C17
compiler skips. This preceded the still-pending Apache repair and does not
validate it. The fixture grammar correction covers stable Go `1.0.0`/`2.0.1`;
its additional 32-test Framework run passed.

The Apache correction resolves global Common-config defaults locally in
`connectors/apache/src/mod_security3.c` and `connectors/apache/src/msc_filters.c`,
preserving explicit configured limits instead of treating unset limits as zero.
All 12 previously failing cases passed with real local Apache `2.4.66` and engine
`3.0.14`. Small-body allow returned `200`; an oversized `1048577`-byte body
returned `413` with accurate counters. The 22 targeted tests and C17 compilation
with `-Wall -Wextra -Werror` passed. Hosted selected Apache `2.4.68`/engine
`3.0.16` runtime still requires fresh-head evidence.

The full workflow/tool suite passed 38 tests again with the native Make
prerequisite, and root host-enabled Traefik/engine/C++ validation passed 38 tests
without skips. The bounded report source correction described below is implemented; its
final focused regressions passed as recorded below; fresh-head hosted validation
remains outstanding.
No full-workflow success is claimed.

Follow-up source validation passed 35 reader/toolchain tests, 34 Framework-sync
tests, 219 CI-contract tests with five existing environment/privilege skips,
and 38 full workflow/tool tests. The synchronizer production CLI is now bound
to its own Parent repository; fixture APIs remain separate. A partial callback,
ASCII-preserving regex cleanup, isolated exception assertions and status
refactoring resolve the observed findings without suppression. The final bounded-profile suite passed 16 tests after clearing `FORCE_ALL_CASES`
and adding fixed CLI-root, path and timeout guards. The combined report/reader/
integrity suite passed 116 tests before those last guards; that earlier combined
result does not cover them. Final actionlint passed all 31 workflows. The next
exact-head Sonar and hosted runtime results remain required.

## Security impact

Publisher identity, merged-PR ancestry, explicit write scope, deny-default permissions, immutable action pins, and runtime isolation remain enforced. The Traefik stage admission is exact rather than a general build-directory trust extension. Socket roots are private and validated. The restricted Yaegi import opt-in is scoped to the fixed local observer and retains Linux peer-credential authentication; loader failure aborts startup. No Framework/MRTS source edits are part of this change. Only the task Parent Framework gitlink is advanced from `9181dc77dfb0685d87fa109e6800dc6052d77cc9` to reviewed Framework master `6948ec5b916e400c4fcaa1b6ccfa64251f606f8d`; the original working checkouts are preserved and MRTS remains `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. Framework PR 133 was already merged before selection; this task performs no Framework merge.

## Runtime evidence

Framework fresh publisher run [36908638390](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/36908638390) succeeded from master `6948ec5` and created Draft [PR 134](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/134), head `51c70128693f0e836d8bff8af947232bca0691fc`. All 20 checks finished without failures, with three advisory skips; Sonar reported OK. This is Framework publisher/PR evidence, not fresh Parent connector runtime evidence. At initial source delivery, Parent hosted validation was still pending.

Initial Parent delivery used [PR 400](https://github.com/Easton97-Jens/ModSecurity-conector/pull/400), head `35259700fcf0558e430f5fc78cc4f7c3920e92ce`. Normal GitHub checks were green while runtime checks were still running; the exact Sonar result was `ERROR`, with security findings for `S5443` (temporary-path selection from the environment) and `S8705` (generic CLI command), plus five maintainability findings. The subsequent source correction restricts the CLI to fixed Envoy/Traefik lifecycle selectors and an explicitly supplied, validated socket parent. This initial-head failure is historical; the published corrective-head result is recorded below. Findings were not suppressed or classified as false positives, and gates were not weakened.

Manual runs of the initial head: [36912803996](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912803996) (canonical No-CRS), [36912808790](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912808790) (legacy Open Connectors), and [36912813685](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912813685) (full smoke with cleanup disabled). The first hosted round is now terminal: canonical No-CRS Envoy, HAProxy and lighttpd passed; CRS Envoy, Traefik, HAProxy and lighttpd passed; exact-head NGINX passed. The canonical Apache job, legacy Open Connectors and full smoke were blocked by the HTTPD 404. Canonical No-CRS Traefik failed at route readiness, exposing the observer loader defect described above. These initial-head results are historical; no all-workflow pass is claimed. Hosted results always bind to their exact SHA; final delivery and CI readback are tracked in PR 400 and the task execution plan.

The corrective commit `e240bb2d4e21da9eb832c94dec7df672167b6636` was published in PR 400. Its exact Sonar analysis at `2026-10-03T06:35:23+0000` reported Quality Gate `OK` and zero vulnerabilities, with four maintainability findings: three regex `S6353` findings and one `prepare_archive` complexity `S3776` finding. The follow-up simplifies that existing helper and uses `re.ASCII` to preserve ASCII-only matching; HTTPD recovery policy and runtime contracts remain unchanged. That follow-up will have a new head, so this Sonar result does not validate it.

Post-commit CI-mode native quick-check on `e240bb2d4e21da9eb832c94dec7df672167b6636` passed (exit 0, 280 tests) with no unit-test skips: the nine earlier gitlink-fixture skips were resolved by committing the selected gitlink. Only the two explicitly reported NGINX/HAProxy compiler checks remained skipped for missing headers.

Fresh corrective-head runtime runs [37103593221](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103593221) (canonical No-CRS), [37103594952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103594952) (legacy Open Connectors), [37103596368](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103596368) (full smoke with cleanup disabled), and [37103555691](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103555691) (CRS) were running without an observed failure at this snapshot. Running jobs are not passes. Final-head delivery, checks and Sonar readback remain tracked in PR 400 and the external task plan, avoiding a documentation-only CI loop.

The maintainability correction was published as `f986fe7ef8e46a0a838a8937b2986d6ffd564208`.
Its exact Sonar analysis at `2026-10-03T06:43:34+0000` reported Quality Gate `OK`,
zero bugs, zero vulnerabilities and zero code smells, with no suppression or
gate weakening. The preceding `e240bb2` heavy runs were superseded/cancelled;
their running-state snapshot above is historical and cannot satisfy completion.
The `f986fe7` CRS round passed all five selected connector jobs and aggregate.
Subsequent centralization and Yaegi build-constraint fixes require a new exact
head and fresh hosted/Sonar evidence; neither earlier green scan validates them.

The next delivered commit `1ca0d4be9f008f30344a46bb084f324e8fd8f496` passed the
strict post-commit reader against its actual committed lock blob/gitlinks;
remote task branch and PR 400 head matched that exact SHA. All automatic checks on this exact head are now terminal and successful,
including the previously running CRS and exact-head NGINX checks.
Sonar analysis at `2026-10-03T07:42:59+0000` reported `ERROR`, with one `S8707`
finding and six maintainability findings. The subsequent source changes above
address those findings, but their new-head Sonar result remains pending. Earlier
green scans are historical and do not establish the next head's quality.

The bounded-profile correction was published as
`5605febc27dd741a561ede13003a7b47cedce5ae` with the observed 16-test profile
validation. Its exact Sonar analysis at `2026-10-03T08:27:06+0000` reported
Quality Gate `ERROR`, zero bugs, one vulnerability and one code smell. All seven
previous `1ca0d4b` findings were resolved. The new `S8705` finding concerns the
variant interpolated into metadata command arguments: the variant already has
argparse/identity allowlists and no shell execution, so this observation does
not validate an injection path. The focused correction selects only literal
internal commands, and the `S9073` correction splits a composite test assertion;
neither finding is suppressed. The corrected profile suite passed 17 tests in 9.514 seconds; the added
pipeline-argument assertion test also passed afterward. The helper returns only
two internal literal commands, and an invalid variant stops before the generator.
A new exact-head Sonar analysis remains required.

Normal checks on `5605febc` were successful so far; the five CRS and five No-CRS
connector runtimes, legacy smoke and sequential full smoke were still pending.
These partial results are not a full runtime pass and do not validate the
subsequent command-selection correction.

The literal-label correction was published as
`a0ad0ef7de7ca4aa197705760c0932d68fbb3949`. Exact Sonar analysis at
`2026-10-03T08:33:53+0000` reported Quality Gate `OK`, zero bugs, vulnerabilities
and code smells, with all findings resolved without suppression. Normal checks
are all successful; CRS Envoy/Traefik/lighttpd succeeded, while remaining heavy and
exact-head runtime checks were pending at this snapshot. The earlier `5605febc`
No-CRS diagnostic was still active. The bootstrap source correction above will
have a new head and needs fresh CI/Sonar evidence; `a0ad0ef7` success does not
verify it or establish that all runtime workflows pass.

## Known limitations

Local privilege-dependent namespace integration had five existing skips. CI-mode quick-check passed with the two missing-header compiler skips; the ordinary local attempt timed out. The protected broker caller remains pinned to `49c40779a7b6de9f699391bcd524ea069787df42`; the updated broker source is not activated by this patch alone.

## Remaining risks

A reviewed protected broker activation/repin and real evidence for both selected broker profiles are still required. Hosted Parent execution may expose additional runner-specific failures. Current explicit updater inventory prevents silent publication gaps; new workflows must be reviewed and added to both inventory and staging.

## Checks not run and rationale

A full Parent hosted pass and both protected broker runtime profiles are outstanding. Parent master integration was not authorized, so neither integration nor protected activation/repin was performed. NGINX and HAProxy C17 compiler checks lack local header prerequisites.

## Final diff and review status

Initial and corrective changes were delivered in PR 400. The latest published `a0ad0ef7` head has successful normal checks and exact Sonar `OK`, with runtime evidence still incomplete. The required With-CRS bootstrap correction passed local validation and needs delivery and fresh exact-head hosted/Sonar evidence. Overall recovery remains partial pending that evidence and protected activation. Original working checkouts are preserved; only the task Parent Framework gitlink is changed as documented above. No Parent master integration or Framework/MRTS source edit is claimed. Both record language versions preserve the same values and limitations.
