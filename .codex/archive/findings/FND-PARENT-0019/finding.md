# FND-PARENT-0019 — Traefik native Make recipe evaluated caller-controlled socket-parent text before runner validation

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0019 |
| Category | security_validated |
| Repository / ownership | parent / parent |
| Priority | P1 |
| Severity / confidence | medium / confirmed |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | true / true |
| Connector / protocol / profile | Traefik / GNU Make to POSIX-shell forwarding before AF_UNIX pathname validation / native-traefik-middleware |

## Summary and impact

The first explicit-private-parent forwarding implementation placed
caller-controlled values inside shell assignment text in the native Traefik
Make recipe. A quote-and-comment socket-parent payload broke the assignment
quoting and executed before runtime-native-middleware.sh and the Python
private-parent validator.

This demonstrates local/direct or automation-caller code execution in the
security-sensitive native target. No repository workflow mapping an untrusted
remote request into these variables was demonstrated, so remote exploitation
and broader privilege impact are not claimed.

## Observed and expected behavior

Before the repair, the recipe rendered a socket-parent shell assignment from a
Make variable. The controlled payload /tmp/unsafe"; printf
MAKE_INJECTION_REACHED; # executed printf and prevented the wrapper from
running. Direct Make command-line values containing $(shell ...) also need raw
transport so Make cannot evaluate them before the child process exists.

TRAEFIK_BIN, TRAEFIK_NATIVE_RUNTIME_ROOT, TRAEFIK_ENGINE_SOCKET_PARENT,
PYTHON, BUILD_ROOT, MODSECURITY_INCLUDE_DIR, MODSECURITY_LIB_DIR, and
MODSECURITY_PREFIX must cross the affected boundaries as raw
process-environment data. A valid selected private parent remains unchanged.
An invalid or hostile parent reaches the Python runner literally and fails
closed before runtime-root setup or UDS allocation.

## Affected files and symbols

- connectors/traefik/Makefile — runtime-smoke-traefik-native, test-engine-
  service, and the raw export boundary for named affected values.
- ci/runtime/lifecycle/run-connector-stage.sh — explicit socket-parent
  environment forwarding into the remaining-target runner.
- ci/runtime/lifecycle/run-remaining-connector-target.sh — run_remaining_connector
  and run_make_target invocation boundary.
- connectors/traefik/scripts/runtime-native-middleware.sh — native wrapper
  that receives the raw environment.
- connectors/traefik/build/test-engine-service-runtime.sh — focused engine-
  service script that receives the raw PYTHON environment.
- connectors/traefik/scripts/runtime_native_smoke.py — strict private-parent
  validation before runtime-root setup.
- tests/test_no_crs_selected_runner_wiring.py — static and real-Make
  forwarding controls.

Affected symbols are runtime-smoke-traefik-native, run_remaining_connector,
run_make_target, TRAEFIK_ENGINE_SOCKET_PARENT, TRAEFIK_BIN,
TRAEFIK_NATIVE_RUNTIME_ROOT, PYTHON, BUILD_ROOT, MODSECURITY_INCLUDE_DIR,
MODSECURITY_LIB_DIR, MODSECURITY_PREFIX, and test-engine-service.

## Preconditions and reproduction

1. A direct local caller or automation context can set
   TRAEFIK_ENGINE_SOCKET_PARENT or another native-target Make variable.
2. The vulnerable native Make recipe runs before the downstream Python
   validator.
3. Run the pre-fix target with a quote/comment socket-parent payload; logs 154
   and 155 retain the rendered and actual controlled execution evidence.
4. Run the repaired target with literal Make-function values for every named
   affected value and with the quote/comment control; no marker or
   sentinel may run and the runner must return its blocked result.

## Root cause

The first forwarding repair interpolated Make variables into shell source, so
the recipe shell parsed caller text before private-parent validation. Direct
Make command-line assignments can also expose embedded Make syntax. Python
validation cannot protect data that Make or the shell has already interpreted.

## Remediation and validation

The native target freezes each named affected value with GNU Make raw-value
transport, exports it, and runs the wrapper without inline recipe assignments.
The lifecycle target runner exports its Traefik binary/runtime-root and
MODSECURITY values instead of passing them as Make command-line assignments.
The test-engine-service target likewise invokes its script without an inline
PYTHON assignment. The existing strict Python private-parent validation remains
the fail-closed enforcement boundary.

When no caller supplies TRAEFIK_NATIVE_RUNTIME_ROOT, the repository-owned
suffix is assembled from a frozen raw BUILD_ROOT value. A caller-supplied
runtime-root value is instead preserved literally, so the security repair does
not turn the valid default into an unresolved Make expression or evaluate
active syntax in a command-line BUILD_ROOT value.

- logs/154-make-parent-shell-injection-pre-fix-reproduction.log, SHA-256
  8a66165ca568d84aa5d7e9d923dc532c0ecde915bd276962ad5d6af321b1f1ee, exit 0,
  observed 2026-07-17T18:30:50Z: the pre-fix rendered recipe exposes the
  controlled quote/comment injection.
- logs/155-make-parent-shell-injection-controlled-runtime-reproduction.log,
  SHA-256 4e4b6b5c78456dbd201b25519c6ecce5d3ea870c83fb5d549379290cb8e820f7,
  exit 0, observed 2026-07-17T18:31:38Z: controlled printf execution occurred
  before Python validation.
- logs/159-final-make-raw-forwarding-security-validation.log, SHA-256
  faab9a431c6964e40f0aab0731884dd049b22a998935fffa2ff436a05f63e51d, exit 0,
  observed 2026-07-17T18:56:13Z: all four literal $(shell ...) values remained
  literal without a marker; a quote/comment payload created no sentinel,
  reached Python literally, returned BLOCKED/Make Error 77, and did not create
  a runtime root; 22 focused native/lifecycle contracts passed.
- logs/160-final-named-make-forwarding-security-validation.log, SHA-256
  8be26ef3b432fc17c6bb8a6b6127c7199ebe114d8b5bc0a668fd7b10dcee4d7a, exit 0,
  observed 2026-07-17T19:29:10Z: all eight named values (BUILD_ROOT, the three
  MODSECURITY values, and the four Traefik values) remained literal without a
  marker; the default runtime path remained correct; the test-engine-service
  dry run rendered no hostile PYTHON assignment; diff/shell checks and 22
  focused contracts passed.
- logs/164-final-exact-pr-head-delivery-and-sonar.log, SHA-256
  1a70d77d83673c68017fc466f0fbf8c57bd91fe3145c806568fc908bcd63b7d3, exit 0,
  observed 2026-07-17T19:49:34Z: exact Draft PR #51 head `6e73dc9…` matched
  local and remote state; all applicable GitHub checks and SonarCloud check
  `87978528103` passed with zero annotations, zero open PR issues, and Quality
  Gate `OK`.
- logs/167-final-conflict-free-draft-pr-delivery-and-sonar.log, SHA-256
  `22c69a59ee5a962354f360fd1a02ac099d148c5e76a3ccb248761a379b8e1aa7`, exit
  `0`, observed `2026-07-17T20:18:08Z`: documentation-only current exact
  Draft PR #51 head `ef2f575…` matched local and remote state; GitHub reports
  Draft `MERGEABLE`/`CLEAN`; 33 exact-head check runs passed and six declared
  runs skipped. SonarCloud check `87983807169` passed with Quality Gate `OK`,
  zero unresolved PR issues, and no hotspots requiring review.

The regression suite is tests/test_no_crs_selected_runner_wiring.py and
tests/test_traefik_native_local_plugin.py. Legitimate controls preserve a safe
direct parent byte-for-byte and preserve the normal valid-private-parent path.

## Validation plan and tests

1. Run focused lifecycle/wiring tests with safe-parent, quote/comment, and
   Make-function controls.
2. Run a real native Make quote/comment control and verify no sentinel is
   created.
3. Run direct Make-function controls for every named affected value and verify
   they remain literal.
4. Verify the default runtime root resolves from a safe BUILD_ROOT and keeps a
   hostile command-line BUILD_ROOT literal when no caller provides a root; then
   obtain exact Draft PR #51 head evidence after push.

## Acceptance criteria, dependencies, and residual risk

- No caller-controlled inline shell interpolation remains in a hardened
  Traefik recipe.
- Each named affected value uses raw GNU Make transport and environment export.
- Literal $(shell ...) values in named affected inputs execute no Make function.
- A quote/comment parent has no shell effect and fails closed in Python before
  runtime-root setup.
- With no caller-provided runtime root, the repository-owned BUILD_ROOT default
  resolves to the normal runtime path without evaluating hostile Make syntax;
  a caller-provided root remains raw.
- No scanner suppression, risk acceptance, Framework/MRTS change, H3 work, or
  merge is introduced.

Exact-head Draft PR #51 and SonarCloud verification passed for
`6e73dc97eba8b503d7d88f7feb3c43ef14132083`, including the separate
FND-PARENT-0016 delivery dependency. Post-merge master verification remains
outside the current authorization. Related findings are
FND-PARENT-0016 and FND-PARENT-0017. This repair does not resolve the same-UID
UDS pathname risks in FND-PARENT-0013 through FND-PARENT-0015; no risk is
accepted. It does not claim to change GNU Make handling for arbitrary unrelated
command-line variables.

The current exact Draft PR #51 head is
`ef2f5755c29c5bc8f452290a14389fe8822e0709`; its documentation-only conflict
follow-up is `MERGEABLE`/`CLEAN` without a rebase or merge and repeated the
exact-head GitHub/SonarCloud pass. Post-merge master verification remains
outside the current authorization.

## History

- 2026-07-17T18:30:50Z: controlled pre-fix recipe injection observed.
- 2026-07-17T18:31:38Z: controlled shell execution before Python validation
  confirmed.
- 2026-07-17T18:56:13Z: raw Make transport, literal fail-closed handling, and
  focused controls passed.
- 2026-07-17T19:29:10Z: the named lifecycle MODSECURITY values, BUILD_ROOT
  default, and sibling test-engine-service PYTHON recipe were hardened and
  covered by final literal-value controls.
- 2026-07-17T19:49:34Z: Exact Draft PR #51 head `6e73dc9…` matched local and
  remote state; all applicable GitHub checks and SonarCloud check `87978528103`
  passed with zero annotations, zero open PR issues, and Quality Gate `OK`.
  The finding remains `fixed` until separately authorized post-merge master
  verification.
- 2026-07-17T20:18:08Z: The documentation-only conflict follow-up produced
  exact Draft PR #51 head `ef2f575…` without a rebase or merge. GitHub reports
  it Draft `MERGEABLE`/`CLEAN`; 33 checks passed with six declared skips, and
  SonarCloud check `87983807169` returned Quality Gate `OK`, zero unresolved
  PR issues, and no hotspots requiring review. The finding remains `fixed`
  until separately authorized post-merge master verification.
