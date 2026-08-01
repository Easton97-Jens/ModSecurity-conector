# FND-PARENT-0016 — SonarCloud rejected the original Traefik UDS hardening because public-root allocation was on the PR path

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0016` |
| Category | `sonarqube_finding` |
| Repository / ownership | `parent` / `parent` |
| Priority | `P1` |
| Severity / confidence | `high` / `confirmed` |
| Status / feasibility | `fixed` / `feasible_now` |
| Release blocker / security relevant | `true` / `true` |
| Connector / protocol / profile | Traefik / AF_UNIX pathname / native-traefik-middleware |

## Summary

The first SonarCloud analysis of Parent Draft PR #51 failed its new-code
Security Rating (D). Direct raw PR evidence classifies public-root UDS
allocation/fallback code, a generic inherited `TMPDIR` selector, and a
process-global `umask` as vulnerabilities. Scanner-visible test negative cases
and code smells are task-owned, but they do not justify a scanner suppression
or an automatic risk decision. The final implementation requires the explicit
private-parent variable and the exact pushed PR head passed SonarCloud without
a suppression or risk acceptance.

## Observed behavior

Check run `87922216387` for PR #51/head
`48198b50357cf24fd59b1aad39d99ef407b3d890` failed because
`new_security_rating=4` exceeded the A threshold. The direct issue export
contains critical/high `python:S5443` and `c:S5443` vulnerability issues,
`c:S5849`, `python:S2612`, and related task-owned maintainability issues.

The first post-remediation exact-head check, `87949565401` for
`56e35eb5e6ff52e0ec84f08807f767acc890ae9e`, closed 14 task-owned issues.
Its one open vulnerability was `python:S5443` at the Python runner's
inherited `TMPDIR` fallback. No scanner control was changed; the source
follow-up removed that fallback.

The subsequent head `2ad97e0e4c7defd0d7d0aa30b8603d59dacbed85` exposed
thirteen task-owned `python:S5443` annotations only in hostile `/tmp` test
fixture values. The focused follow-up derives those values from a private
`TemporaryDirectory`. Final exact head
`6e73dc97eba8b503d7d88f7feb3c43ef14132083` passed SonarCloud check
`87978528103` with zero annotations, zero open PR issues, and Quality Gate
status `OK`.

A documentation-only follow-up then produced current exact Draft PR head
`ef2f5755c29c5bc8f452290a14389fe8822e0709`. It changes only the bilingual
Change Record indexes to avoid the independent CodeQL-record insertion on
current `master`. SonarCloud check `87983807169` passed with Quality Gate
`OK`, zero unresolved PR issues, and no hotspots requiring review. GitHub
reports this head as Draft and `MERGEABLE`/`CLEAN`; its 33 successful check
runs and six workflow-declared skips contain no failed, cancelled, or pending
run.

## Expected behavior

The runner, shell harness, and C engine must require an existing absolute,
canonical, current-user-owned, exact-`0700`, non-symlink socket parent whose
full ancestor chain prevents cross-UID replacement before allocation or bind.
No runtime or self-test path may silently select `/tmp` or `/var/tmp`. The
listener uses that verified directory boundary rather than a process-global
`umask` or pathname-permission claim. A re-run on the updated exact PR head
must meet the SonarCloud new-code Security Rating threshold without a
suppression or risk acceptance.

The native runner accepts only an explicit `TRAEFIK_ENGINE_SOCKET_PARENT`; it
must not select a generic inherited temporary-directory variable.

## Impact

The exact Draft-PR head now satisfies its external security gate, but this
finding remains `fixed` rather than `verified` or `closed` because no master
integration is authorized or performed. In the pre-remediation implementation,
an elevated or otherwise sensitive native
runner that inherited an attacker-selected absolute `TMPDIR` could create a
named UDS child outside the intended private boundary. This scanner evidence does
not validate the distinct same-UID endpoint-redirection or final-cleanup
races; they remain `FND-PARENT-0013`, `FND-PARENT-0014`, and
`FND-PARENT-0015`.

## Affected files and symbols

- `connectors/traefik/scripts/runtime_native_smoke.py` —
  `resolve_engine_socket_parent`, full ancestor validation.
- `connectors/traefik/src/traefik_engine_service.c` — self-test parent,
  listener setup, global `umask` wrapper.
- `connectors/traefik/build/test-engine-service-runtime.sh` and
  `connectors/traefik/build/build-engine-service.sh` — test-parent contract.
- `tests/test_traefik_native_local_plugin.py` — negative and legitimate
  private-parent controls.
- `ci/runtime/lifecycle/run-connector-stage.sh` and
  `ci/runtime/lifecycle/run-remaining-connector-target.sh` — preserve the
  caller-supplied parent through the canonical native lifecycle path.
- `connectors/traefik/Makefile` and
  `tests/test_no_crs_selected_runner_wiring.py` — forward and verify the
  exact caller value without synthesizing a runtime-root parent.
- `common/scripts/modsecurity_targeted_eval.cc` — isolated C++17
  maintainability adjustment.

## Preconditions and reproduction

1. SonarCloud analyzes PR #51 at the recorded head.
2. The prior runner has no selected private parent, or the C self-test inherits
   an unsuitable absolute `TMPDIR`.
3. Retrieve the check-run annotations and SonarCloud issues/quality-gate JSON
   with the exact retained commands.
4. Trace the former public fallback/default and global-`umask` paths, then the
   fixed immediate-parent and ancestor controls.

## Evidence

- Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`, GitHub
  annotation export `evidence/draft-pr-51-sonar-annotations.json`, SHA-256
  `96885558996384b6f17e83a5d4452413ef6c2c2ff04b19441f1753aae4cbb2c8`, log
  `089-draft-pr-51-sonar-annotations.log`, exit `0`, observed
  `2026-07-17T15:27:12Z`.
- SonarCloud issue export `evidence/draft-pr-51-sonar-issues.json`, SHA-256
  `361370c72e7d4e965695c823cdac616a3404dcf3fa2f3441d3446fe850317d7c`, log
  `090-draft-pr-51-sonar-issues.log`, exit `0`, observed
  `2026-07-17T15:29:31Z`.
- SonarCloud Quality-Gate export
  `evidence/draft-pr-51-sonar-quality-gate.json`, SHA-256
  `b6348c561174b598ec56ec596a106179cb12f4e8c75654fb61b0f7143538debe`, log
  `091-draft-pr-51-sonar-quality-gate.log`, exit `0`, observed
  `2026-07-17T15:32:26Z`.
- Final focused Python contract run
  `logs/120-private-parent-ancestor-python-contracts-final.log`, SHA-256
  `1bf27a75961e8aec742448899c4e2e648ad1ea4bf6af1fdc9b33440c9d4620f2`,
  16 tests, exit `0`, observed `2026-07-17T16:19:10Z`–`16:19:11Z`.
- Clang and GCC C17 self-test builds (`logs/121` and `122`) passed, as did the
  mutable-ancestor rejection control (`logs/123`), valid Allow/Blocking runtime
  control (`logs/125`), hardened diagnostic build (`logs/126`), ASan+UBSan
  runtime (`logs/128`), and GCC `-fanalyzer` (`logs/129`). Their exact
  command/CWD/timestamp/exit records and SHA-256 values are retained in the
  current run and the related `FND-PARENT-0017` record.
- Follow-up exact-head issue export
  `evidence/pr-51-head-56e35eb-sonar-issues.json`, SHA-256
  `5561b1461984c8b7375def710bfaca9ac31bf466b24fad750f0c7b1c348e78da`, shows
  14 `CLOSED/FIXED` task-owned issues and the one remaining `python:S5443`
  before this final source change.
- Follow-up 16-contract Python validation is retained as
  `logs/144-explicit-private-parent-python-contracts.log`, SHA-256
  `712fa2f1ac323a17d9c569fd8f8396eafceda7f6e28b18df61a6a502580dbc37`, exit
  `0`, observed `2026-07-17T17:34:11Z`. The changed English/German pairs passed
  the checker-equivalent focused documentation validation in
  `logs/148-explicit-private-parent-targeted-bilingual-docs.log`, SHA-256
  `a26471edca192db542c117efe00e6aaae1ed44ea2518e5b2b3d59b6aaa17bdf8`, exit
  `0`, observed `2026-07-17T17:42:13Z`.
- Earlier explicit-parent forwarding validation is retained as
  `logs/150-explicit-parent-forwarding-final-validation.log`, SHA-256
  `139dba675ef96bf6c8c3e0bb2b0624949f208ba5cd14f982933fde80fb244221`,
  exit `0`, observed `2026-07-17T18:18:17Z`–`18:18:18Z`. It records ordinary
  explicit-parent forwarding only and predates the separately reproduced
  Make/shell interpretation defect in `FND-PARENT-0019`; it is not final
  hostile-input evidence.
- The synchronized Change Record then passed a final changed-pair documentation
  validation in `logs/152-change-record-forwarding-docs-validation.log`,
  SHA-256 `2199e4d1cdffede8f66e3a19dabbf3806e5afbddd25719c4d87c59705d878d6b`,
  exit `0`, observed `2026-07-17T18:26:44Z`–`18:26:45Z`.
- Raw Make/environment forwarding closure is retained in
  `logs/159-final-make-raw-forwarding-security-validation.log`, SHA-256
  `faab9a431c6964e40f0aab0731884dd049b22a998935fffa2ff436a05f63e51d`,
  exit `0`, observed `2026-07-17T18:56:13Z`. It proves literal direct Make
  function values for all four forwarded variables, no quote/comment shell
  sentinel, Python rejection before runtime-root setup, and 22 focused
  contracts. The distinct pre-validation interpretation path is tracked and
  repaired as `FND-PARENT-0019`.
- Final named Make/environment forwarding closure is retained in
  `logs/160-final-named-make-forwarding-security-validation.log`, SHA-256
  `8be26ef3b432fc17c6bb8a6b6127c7199ebe114d8b5bc0a668fd7b10dcee4d7a`,
  exit `0`, observed `2026-07-17T19:29:10Z`. It verifies literal handling of
  the named lifecycle-forwarded BUILD_ROOT, MODSECURITY, and Traefik values,
  no marker execution, syntax/diff checks, and 22 focused contracts.
- Final exact-head delivery and SonarCloud validation is retained in
  `logs/164-final-exact-pr-head-delivery-and-sonar.log`, SHA-256
  `1a70d77d83673c68017fc466f0fbf8c57bd91fe3145c806568fc908bcd63b7d3`, exit
  `0`, observed `2026-07-17T19:49:34Z`. It records matching local/remote/PR
  head `6e73dc9…`, all applicable GitHub checks, SonarCloud check `87978528103`
  with zero annotations and open issues, and Quality Gate `OK`.
- Final conflict-free Draft-PR delivery and SonarCloud validation is retained
  in `logs/167-final-conflict-free-draft-pr-delivery-and-sonar.log`, SHA-256
  `22c69a59ee5a962354f360fd1a02ac099d148c5e76a3ccb248761a379b8e1aa7`, exit
  `0`, observed `2026-07-17T20:18:08Z`. It records matching local, remote,
  and Draft PR #51 head `ef2f575…`, GitHub `MERGEABLE`/`CLEAN`, 33 successful
  and six workflow-declared skipped exact-head runs, SonarCloud check
  `87983807169`, Quality Gate `OK`, zero unresolved PR issues, and no
  hotspots requiring review. It also retains the read-only conflict-free
  three-way result for the bilingual Change Record indexes.

## Root cause analysis

The former Python runner retained automatic `/var/tmp` allocation; the C
self-test accepted inherited `TMPDIR` after an absolute-path check and then
fell back to `/var/tmp`; a temporary global `umask` was used for a boundary
whose effective cross-UID protection is a private pathname parent. The first
remediation review also showed that immediate-parent-only validation accepted a
mode-`0700` child below a non-sticky mutable ancestor (`FND-PARENT-0017`). Test
negative cases and repeated literals produced incidental scanner findings. The
first exact-head reanalysis proved that the generic Python `TMPDIR` fallback
was the sole remaining active vulnerability, so the final source follow-up
removes that optional selector rather than relying on later manual validation.
Once the runner became strict, the supported dispatcher and Make invocation
chain also had to preserve that caller-supplied boundary. Deriving a new parent
below the canonical runtime or temporary root would exceed the 100-byte UDS
path budget, so it is neither a safe fallback nor a compatible repair.
The gate failure is confirmed, while whether every scanner issue represents a
separately exploitable product vulnerability remains bounded by the stated
source/runtime evidence.

## Proposed remediation

Replace public-root/default allocation with explicitly supplied existing
private parents. Enforce absolute, canonical, current-user-owned, exact-`0700`,
non-symlink checks and a cross-UID-safe ancestor chain in the runner, C
listener, C self-test, and shell harness. Remove global-`umask` reliance and
avoid pathname-permission claims, retain fail-closed behavior, and apply only
behavior-preserving task-owned refactors for related maintainability items.
The final runner selection requires only `TRAEFIK_ENGINE_SOCKET_PARENT` and
does not inherit `TMPDIR`. The central dispatcher and native Make target
forward only the caller's exact explicit value; they do not derive one below a
runtime or temporary root.

## Acceptance criteria

- No production runner or C self-test silently allocates below `/tmp` or
  `/var/tmp`.
- The production runner does not accept a generic inherited temporary-directory
  fallback; it requires `TRAEFIK_ENGINE_SOCKET_PARENT` before host setup.
- The canonical dispatcher and native Make target preserve only the caller's
  exact explicit parent; neither derives one below a runtime or temporary root.
- Missing, relative, symlinked, foreign-owned, or non-`0700` parents fail
  before allocation/bind; a valid private parent succeeds.
- The verified immediate-parent/ancestor boundary is the cross-UID control; no
  global `umask` wrapper or pathname-permission claim remains.
- Focused Python contracts, C17 build/self-test/runtime Allow/Blocking controls,
  and C++ evaluator checks pass.
- The updated exact PR head meets SonarCloud's security threshold without a
  suppression, configuration change, or risk acceptance.

## Validation plan and tests

- Static assertions for the explicit-private-parent contract and absence of
  public fallback/`umask` use.
- Focused Python contracts with valid and invalid parent controls.
- Shell syntax, native Make dry-run, and lifecycle-wiring controls for forwarding
  the caller-supplied parent without a generated temporary-root parent.
- C17 warnings-as-errors build, self-test, and native UDS protocol controls.
- C++17 evaluator compile, diagnostics, and Allow/Blocking controls.
- Push only the focused Parent repair and retrieve exact-head SonarCloud raw
  issues and Quality-Gate JSON.

Relevant regression tests are `tests/test_traefik_native_local_plugin.py`,
the two Traefik build/runtime scripts, `check-targeted-evaluator-cpp17.sh`, and
`tests/test_c_cpp_diagnostics.py`. Legitimate controls require a valid private
parent and safe ancestor chain, SO_PEERCRED self-probe, Allow `200`, and
Blocking `403`.

## Dependencies, blockers, related findings, and residual risk

The exact pushed PR head has passed its SonarCloud analysis. There is no
current implementation blocker; post-merge master verification requires
separate authorization. Related findings are
`FND-PARENT-0013`, `FND-PARENT-0014`, `FND-PARENT-0015`, `FND-PARENT-0017`,
`FND-PARENT-0019`, and `FND-SONAR-0001`. This work cannot by itself resolve
the same-UID pathname endpoint-redirection or non-atomic cleanup races. No
risk has been accepted.

## History

The earlier non-hostile forwarding validation predates the separately
reproduced Make/shell interpretation finding FND-PARENT-0019. Its hostile-input
closure evidence is log 159: all four raw Make values remained literal, the
quote/comment sentinel was absent, Python failed closed, and 22 focused
contracts passed.

- `2026-07-17T15:35:00Z`: Direct GitHub and SonarCloud raw exports confirmed a
  PR-head Security Rating D gate failure. Active remediation began; no scanner
  rule, Quality-Gate configuration, or risk disposition was changed.
- `2026-07-17T16:58:45Z`: Local remediation is fixed after focused Python,
  C17, shell/runtime, hardened, ASan+UBSan, and GCC analyzer controls. The
  exact-head external SonarCloud reanalysis remains required before verification.
- `2026-07-17T17:42:13Z`: Exact-head check `87949565401` showed that only the
  generic Python `TMPDIR` selector remained open; the final source follow-up
  removed it. Sixteen focused Python contracts and changed-pair bilingual
  validation passed. The finding remains `fixed` locally pending a new
  exact-head SonarCloud reanalysis.
- `2026-07-17T18:18:18Z`: The canonical stage dispatcher, remaining-target
  runner, and native Make target were wired to forward only the caller-provided
  explicit parent. The fresh 22-contract/syntax/documentation/Make-dry-run
  validation passed; a parent derived from the canonical runtime or temporary
  root was deliberately rejected because it would exceed the UDS path budget.
- `2026-07-17T18:26:45Z`: The bilingual Change Record was synchronized
  with the final forwarding validation, and its selected changed-pair checker
  rerun passed. The finding remains `fixed` locally pending a new
  exact-head SonarCloud reanalysis.
- `2026-07-17T18:56:13Z`: The earlier log 150 was reclassified as non-hostile
  forwarding evidence only. `FND-PARENT-0019` records the separately
  reproduced Make/shell interpretation defect; raw environment forwarding and
  focused hostile-input controls passed in log 159. This finding remains fixed
  locally pending exact-head SonarCloud reanalysis.
- `2026-07-17T19:29:10Z`: The final named Make/environment controls covered
  BUILD_ROOT, the lifecycle-forwarded MODSECURITY values, and the Traefik
  values without marker execution. The shared interpretation boundary remains
  tracked by `FND-PARENT-0019`; this finding remains fixed locally pending
  exact-head SonarCloud reanalysis.
- `2026-07-17T19:49:34Z`: Exact Draft PR #51 head
  `6e73dc97eba8b503d7d88f7feb3c43ef14132083` passed SonarCloud check
  `87978528103` with zero annotations, zero open PR issues, and Quality Gate
  `OK`. The focused `TemporaryDirectory` fixture follow-up removed the 13
  intermediate test-only S5443 annotations without suppression or risk
  acceptance. The finding remains `fixed` until a separately authorized
  post-merge master verification.
- `2026-07-17T20:18:08Z`: The documentation-only conflict follow-up produced
  exact Draft PR #51 head `ef2f5755c29c5bc8f452290a14389fe8822e0709` without
  a rebase or merge. Its local/remote/PR head matched, GitHub reported
  `MERGEABLE`/`CLEAN`, all 33 applicable checks passed with six declared
  skips, and SonarCloud check `87983807169` returned Quality Gate `OK`, zero
  unresolved PR issues, and no hotspots requiring review. The finding remains
  `fixed` until separately authorized post-merge master verification.
