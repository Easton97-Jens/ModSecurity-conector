# Change Record: Traefik UDS and C++ evaluator hardening

**Status:** local remediation and focused validation are complete; delivery
disposition remains a Parent-only Draft PR with no merge. SonarCloud rejected
the first Draft-PR head with Security Rating D; the scoped follow-up revision
awaits its own exact-head analysis.

**Language:** English | [Deutsch](CR-20260717-traefik-uds-cpp17-hardening.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260717-traefik-uds-cpp17-hardening` |
| Date (UTC) | `2026-07-17` |
| Base revision | `02f9f98cdbbdd70bbc530ac1399974e53884f4e9` |
| Scope | Parent repository only |
| Related findings | `FND-FRAMEWORK-0008`, `FND-PARENT-0012`, `FND-PARENT-0013`, `FND-PARENT-0014`, `FND-PARENT-0015`, `FND-PARENT-0016`, `FND-PARENT-0017` |

## Motivation and problem statement

The native Traefik smoke runner could force a Unix-domain socket pathname that
was too long and did not offer a validated short parent selection. Its UDS
lifecycle also needed explicit collision, path, identity, and cleanup controls.
Separately, the C++ targeted evaluator exposed internal same-type string
interfaces that made future argument-order errors unnecessarily easy.

## Acceptance criteria

- A native runner selects a short task-owned UDS parent through an explicit
  value or `TMPDIR`, and fails closed before host setup when neither supplies a
  valid private parent with a cross-UID-safe ancestor chain.
- Focused tests cover length, relative paths, symlinks, existing sockets,
  parallel allocation, setup failure, YAML quoting, and cleanup refusal.
- The C17 service refuses an unsafe private-parent topology and pre-bind,
  post-bind, and post-probe pathname replacements before recording listener
  ownership.
- The existing protocol lifecycle retains Allow and Blocking controls; ordinary
  focused cleanup is covered without claiming same-UID race-proof deletion or
  live endpoint identity.
- The evaluator compiles under C++17 `-Wall -Wextra -Werror` and preserves the
  direct Allow/Block result while making internal inputs less swappable.

## Implementation decision and rationale

The Python runner gives `TRAEFIK_ENGINE_SOCKET_PARENT` precedence over
`TMPDIR`. It validates an existing absolute, canonical, current-user-owned,
exact-`0700` parent outside the checkout, rejects symlink components/control
characters, and verifies every ancestor to root against cross-UID replacement.
A group- or other-writable ancestor is accepted only when it is sticky and its
next child entry belongs to the effective UID. It fails before host setup if
neither source supplies that boundary. It JSON-quotes generated YAML and
records directory identity before cleanup checks. Those checks refuse observed
mismatch or residual contents; they are not an atomic same-UID deletion
guarantee.

The C service independently enforces the same immediate-private-parent and
cross-UID-safe ancestor-chain contract, so it needs no process-global `umask`
or path-based permission mutation. Before it publishes readiness on Linux, it
performs a bounded nonblocking local UDS probe and requires the accepted
`SO_PEERCRED` peer to be the engine process. It compares `lstat()` identity
immediately before and after that probe. Deterministic self-test hooks cover
unsafe-ancestor rejection and replacement before bind, after bind, and after
the probe; the C self-test requires an explicit private `--socket-parent`.

The evaluator uses `std::string_view` for immutable bracket-parser inputs and a
named `DecisionLogInput` value for the decision-log call. This changes internal
interfaces only; it does not change public APIs or emitted decision behavior.

## Changed files

- `common/scripts/modsecurity_targeted_eval.cc`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/build/build-engine-service.sh`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/README.md` and `connectors/traefik/README.de.md`
- `docs/connectors/README.md` and `docs/connectors/README.de.md`
- `docs/reference/variables.md` and `docs/reference/variables.de.md`
- This bilingual Change Record and its bilingual index entries in
  `reports/audits/change-records/README.md` and
  `reports/audits/change-records/README.de.md`

## Commands executed

All commands ran from `/root/git/ModSecurity-conector` with task-owned output
under `/var/tmp/codex/ModSecurity-conector/runs/20260717T114213Z-feasibility-runtime-remediation-838d9adc/`.

- `make -C connectors/traefik test-engine-service` with explicit task-owned
  build/socket roots and verified local libmodsecurity include/library paths —
  passed; retained as `logs/056-traefik-engine-service-double-observation-race-regression.log`
  (SHA-256 `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`).
- `python -B -m unittest -v tests.test_traefik_native_local_plugin` — passed
  13 tests; retained as
  `logs/057-traefik-native-local-plugin-double-observation-contract.log`
  (SHA-256 `8103a918dbb83bd07437f347cf9d30c6484391821b8459a8e5510fd05ad15dae`).
- The same focused Python contract suite was rerun after a portability-only
  test correction — passed 14 tests; retained as
  `logs/073-traefik-native-local-plugin-portable-contract-final-rerun.log`
  (SHA-256 `fc511f1554f3cb31ae1105854cdb6b82d51476139f41189cb73e10b48b40adcb`).
- The canonical raw C++ evidence manifest is
  `evidence/cpp17-revalidation-evidence-manifest.json`. It records the exact
  command, CWD, start/end UTC, exit result, raw-log path, SHA-256, and summary
  for each completed current verification. Current C++17 compilation (`074`),
  compilation database (`075`), diagnostics contracts (`080`, five tests), and
  Allow/Block controls (`081`) passed. The current swappable-parameter
  reanalysis was stopped by the repository storage gate (`076`, exit `77`) and
  was not bypassed; because that gate stopped the wrapper before it emitted an
  end timestamp, the manifest records the raw-log mtime as explicitly labelled
  end evidence. Retained historical `031`/`032` static-analysis evidence is
  likewise marked with its older missing-end-timestamp schema limitation rather
  than claimed as a new successful run.
- The Sonar remediation reran 14 Python runner contracts (`103`), the C17
  build and explicit-private-parent self-test (`105`), local engine Allow/
  Blocking protocol and replacement-sentinel controls (`106`), unsafe-parent
  rejection (`107`), and C++17 evaluator compilation, diagnostics, and
  Allow/Block controls (`109`–`111`). The exact commands, CWD, timestamps, exit
  results, and raw logs are retained under the same task run. The first attempt
  used an overlong generated test-parent path (`094`) and the first runtime
  mode assertion (`101`) showed that a pathname socket mode is not the chosen
  cross-UID boundary; both were corrected by retaining the exact-`0700` parent
  contract rather than reintroducing a global `umask` or path-based chmod.
- The final ancestor-remediation evidence records the pre-fix immediate-parent
  acceptance gap (`119`, SHA-256
  `25a6728bca11448352bd922384e22749570e7d453e393f6dd1092cec1abfeee7`), 16
  Python contracts (`120`, SHA-256
  `1bf27a75961e8aec742448899c4e2e648ad1ea4bf6af1fdc9b33440c9d4620f2`),
  Clang and GCC C17 build/self-tests (`121`/`122`, SHA-256
  `6d044ad0eb36b861fefe8e1d36b28ae6a59d91b48da5c14aca3b73e416612d80` and
  `8c6ff06096212dde3a1f272f00b9ed7492c33bef35cfc820f0df074910605156`),
  negative controls through Python, shell, and C (`123`, SHA-256
  `0cc657a4a58763b44070215e7c354027c12688a1eb248e21cb9a76c9c4a2868c`), and
  valid runtime Allow/Blocking plus cleanup-sentinel controls (`125`, SHA-256
  `c35d629326601b521feeb92953f7f43526cad2bc5b9d7e6c7316d22e85c0cb36`).
  Hardened diagnostic (`126`), ASan+UBSan build/runtime (`127`/`128`), and
  GCC `-fanalyzer` (`129`) all passed; their exact command, CWD, UTC timing,
  exit result, and raw output are retained in the named run.

## Security impact

The change strengthens path validation, YAML serialization, UDS collision
handling, replacement detection, and cleanup refusal. The modeled pre-capture
post-`bind` identity race is closed: a replacement before, during, or
immediately after the self-probe is not recorded as engine-owned.

`FND-PARENT-0016` records the confirmed SonarCloud Quality-Gate failure on the
first Draft-PR head. The remediation removes public-root/default allocation,
requires validated private parents and safe ancestor chains at the Python,
shell, and C boundaries, and removes process-global `umask` state. It does not
claim that the separate same-UID endpoint or cleanup races are fixed.

`FND-PARENT-0017` records the independently reproduced cross-UID ancestor
replacement gap: an exact-`0700` child below a non-sticky writable ancestor
was accepted before the repair. The task-owned reproduction could not use a
live foreign UID under a public root because the storage policy requires a
private external root; the accepted topology and source-to-`bind` path were
nevertheless concrete. The current Python, shell, and C boundaries reject it.

`FND-PARENT-0013` remains open: POSIX/Linux has no atomic conditional
unlink-by-expected-inode operation. A hostile process sharing the service UID
and mutable-directory authority can still race the final `lstat()` to
`unlink()` interval. This record makes no claim that the final cleanup is
same-UID race-proof.

`FND-PARENT-0014` separately records the analogous final manifest leaf
validation-to-removal interval. `FND-PARENT-0015` is more consequential for
the native host path: after readiness, a same-UID mutator can rebind the
pathname before a later middleware dial. The client opens a fresh UDS
connection for each transaction and currently has no verified peer-identity
binding, so a fake protocol-valid allow endpoint could divert that transaction.
This is source-backed but has no genuine host reproduction; it is recorded as
P1/medium/probable rather than as High or confirmed.

## Runtime evidence

The compiled C17 service passed its protocol self-test, safe-ancestor
socket-ownership self-test, normal local protocol lifecycle, and deliberate
replacement-sentinel negative control. In the negative control,
`socket_cleanup` is the expected fail-closed service outcome and the test
itself passed. The separate ancestor negative controls confirmed that an
explicit test parent is now required and that a non-sticky writable ancestor is
rejected before allocation or bind.

No genuine Traefik/libmodsecurity host lifecycle was run: the necessary host
binary/runtime inputs were unavailable, so that evidence remains
`blocked_environment`.

## Known limitations

- The native pathname listener fails closed outside the Linux peer-credential
  mechanism used for verified ownership capture.
- `FND-PARENT-0013` blocks a strict same-UID no-foreign-socket-cleanup claim.
- `FND-PARENT-0014` blocks a strict same-UID no-foreign-manifest-leaf-deletion
  claim.
- `FND-PARENT-0015` blocks a strict same-UID live client-to-engine endpoint-
  identity claim; the existing self-probe applies only before readiness.
- `0700` protects across UIDs; it is not isolation among hostile processes
  sharing the owner UID.

## Remaining risks

The final pathname and manifest-leaf deletion limits have not been risk
accepted. A future solution must either avoid automatic pathname deletion,
introduce separately trusted cleanup boundaries, or prove a compatible atomic
expected-object deletion mechanism. The live endpoint-redirection limit also
needs a verified end-to-end client/engine identity design; abstract AF_UNIX,
client peer credentials, and descriptor handoff are future candidates, not
current verified fixes.

## Checks not run and rationale

- Real native Traefik host lifecycle and its full CRS/MRTS profile matrix were
  not run because required host/runtime inputs were unavailable; no download,
  installation, build, or retest was used to force them.
- NGINX, Apache, and MRTS blocked items remain in their own feasibility
  dispositions; no Framework or MRTS files were changed.
- The repository CI lane uses Python 3.13, which is unavailable in this host.
  The focused Python contracts passed with the available interpreter, but that
  is not claimed as a Python-3.13 CI-lane result.
- H3 was intentionally not investigated in this remediation task because no approved compatible client solution is currently available.

## Final diff and review status

The scoped local source/test/documentation remediation is complete, but the
overall security posture is intentionally not described as complete:
`FND-PARENT-0013`, `FND-PARENT-0014`, and `FND-PARENT-0015` remain blocked
without risk acceptance. Parent Draft PR #51 exists and its first head was
rejected by the SonarCloud Security Rating D gate; the follow-up revision must
be pushed and observed at its exact SHA before this record can describe remote
CI as passing. The focused test compatibility change is intentional:
`make -C connectors/traefik test-engine-service` now requires an existing
`TRAEFIK_ENGINE_SOCKET_TEST_PARENT` and exits `77` without it. No configured
CI caller was found for that focused target. The delivery disposition remains
Parent-only Draft PR with no merge authority.
