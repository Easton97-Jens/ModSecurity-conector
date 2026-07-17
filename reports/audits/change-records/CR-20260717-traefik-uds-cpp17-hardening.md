# Change Record: Traefik UDS and C++ evaluator hardening

**Status:** local implementation and focused validation are partial; delivery disposition is a Parent-only Draft PR with no merge; remote CI and review remain pending

**Language:** English | [Deutsch](CR-20260717-traefik-uds-cpp17-hardening.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260717-traefik-uds-cpp17-hardening` |
| Date (UTC) | `2026-07-17` |
| Base revision | `02f9f98cdbbdd70bbc530ac1399974e53884f4e9` |
| Scope | Parent repository only |
| Related findings | `FND-FRAMEWORK-0008`, `FND-PARENT-0012`, `FND-PARENT-0013`, `FND-PARENT-0014`, `FND-PARENT-0015` |

## Motivation and problem statement

The native Traefik smoke runner could force a Unix-domain socket pathname that
was too long and did not offer a validated short parent selection. Its UDS
lifecycle also needed explicit collision, path, identity, and cleanup controls.
Separately, the C++ targeted evaluator exposed internal same-type string
interfaces that made future argument-order errors unnecessarily easy.

## Acceptance criteria

- A native runner selects a short task-owned UDS parent through an explicit
  value, `TMPDIR`, or a generated private fallback, rejecting unsafe paths.
- Focused tests cover length, relative paths, symlinks, existing sockets,
  parallel allocation, setup failure, YAML quoting, and cleanup refusal.
- The C17 service refuses pre-bind, post-bind, and post-probe pathname
  replacements before recording listener ownership.
- The existing protocol lifecycle retains Allow and Blocking controls; ordinary
  focused cleanup is covered without claiming same-UID race-proof deletion or
  live endpoint identity.
- The evaluator compiles under C++17 `-Wall -Wextra -Werror` and preserves the
  direct Allow/Block result while making internal inputs less swappable.

## Implementation decision and rationale

The Python runner now gives `TRAEFIK_ENGINE_SOCKET_PARENT` precedence over
`TMPDIR`, then creates a short private fallback. It validates absolute,
current-user-owned `0700` parents outside the checkout, rejects symlink
components/control characters, JSON-quotes generated YAML, and records
directory identity before cleanup checks. Those checks refuse observed mismatch
or residual contents; they are not an atomic same-UID deletion guarantee.

The C service uses descriptor-based permissions and records socket identity.
Before it publishes readiness on Linux, it performs a bounded nonblocking
local UDS probe and requires the accepted `SO_PEERCRED` peer to be the engine
process. It compares `lstat()` identity immediately before and after that
probe. Deterministic self-test hooks cover replacement before bind, after bind,
and after the probe.

The evaluator uses `std::string_view` for the immutable field key and a named
`DecisionLogInput` value for the decision-log call. This changes internal
interfaces only; it does not change public APIs or emitted decision behavior.

## Changed files

- `common/scripts/modsecurity_targeted_eval.cc`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/src/traefik_engine_service.c`
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

## Security impact

The change strengthens path validation, YAML serialization, UDS collision
handling, replacement detection, and cleanup refusal. The modeled pre-capture
post-`bind` identity race is closed: a replacement before, during, or
immediately after the self-probe is not recorded as engine-owned.

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

The compiled C17 service passed its protocol self-test, socket-ownership
self-test, normal local protocol lifecycle, and deliberate replacement-sentinel
negative control. In the negative control, `socket_cleanup` is the expected
fail-closed service outcome and the test itself passed.

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
- H3 was intentionally not investigated in this remediation task because no approved compatible client solution is currently available.

## Final diff and review status

The local source/test/documentation diff is partial, not security-complete:
pre-capture hardening, short parent selection, and focused controls are ready
for delivery review, while `FND-PARENT-0013`, `FND-PARENT-0014`, and
`FND-PARENT-0015` remain blocked without risk acceptance. At record
preparation, it had not yet been committed, pushed, or submitted as a Draft
PR. The delivery disposition is a Parent-only Draft PR with no merge
authority; it is not represented as passing remote CI or review.
