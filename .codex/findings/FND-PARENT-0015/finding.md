# FND-PARENT-0015 — Traefik pathname UDS permits same-UID post-readiness endpoint redirection

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0015` |
| Title / Titel | `Traefik pathname UDS permits same-UID post-readiness endpoint redirection` |
| Category / Kategorie | `security_candidate` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P1` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `probable` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The C listener proves pathname identity only through initial readiness capture.
The Traefik middleware opens a new pathname UDS connection for each transaction
without peer identity verification. A hostile same-UID process that can rebind
`engine.sock` after readiness can redirect later middleware traffic to a fake
endpoint.

## Observed behavior / Beobachtetes Verhalten

The runner waits only for a socket pathname to exist, then starts Traefik with
that path. `unixSocketEngine.Open()` uses `net.Dialer.DialContext("unix",
socketPath)` for each transaction. A protocol-valid RESULT with action allow is
accepted and mapped to `allowDecision()`. Neither runner nor client binds that
connection to the original C listener identity.

## Expected behavior / Erwartetes Verhalten

The pre-capture C self-probe may claim only that a replacement in its bounded
startup window fails closed. Strict live client-to-engine identity requires a
verified client peer-identity or descriptor/abstract-socket boundary; pathname
selection and `0700` permissions do not isolate hostile same-UID processes.

## Impact / Auswirkung

Under the same-UID mutation precondition, a fake listener can return a valid
allow result for newly opened transactions, bypassing the intended ModSecurity
decision path, and receive data sent over that connection. Deployment-specific
exploitability and a real host reproduction were not established, so this stays
medium/probable rather than High or confirmed.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/native_middleware/engine_uds.go`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`

### Symbols / Symbole

- `traefik_engine_capture_bound_socket_identity`
- `wait_for_socket`
- `unixSocketEngine.Open`
- `safeUnixSocketPath`
- `udsResult.decision`

## Preconditions / Voraussetzungen

- A hostile process shares the service effective UID and can mutate the private
  UDS child directory.
- It unlinks the live `engine.sock` after C readiness capture and binds a
  replacement before a later middleware transaction opens.
- The replacement returns a protocol-valid allow result.

## Reproduction / Reproduktion

- Trace C readiness capture and the absence of later pathname watching.
- Trace `wait_for_socket()`: it accepts any existing socket pathname before
  Traefik starts.
- Trace `unixSocketEngine.Open()`: it redials the configured path for each
  transaction; `udsResult.decision()` maps action allow to `allowDecision()`.

## Evidence / Evidence

- Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/063-traefik-live-uds-redirection-static-review.log`, source-to-sink
  review, SHA-256
  `15d453ebcb8e013a3881f2897317ca5dca0f04c69a16920bda3e9137b7bb2406`, exit
  `0`, observed `2026-07-17T14:33:24Z`.
- `logs/062-same-uid-pathname-toctou-static-review.log`, SHA-256
  `2294d4ff41b1266a34a234da0db62072cadd51199efe37db979114ebcafc2dd2`, shows
  the C capture and cleanup boundary.

## Root-cause analysis / Grundursachenanalyse

Trust moves from the C listener to an independently dialing Traefik client
through a mutable pathname. The C-side `SO_PEERCRED` self-probe catches a
replacement before initial identity capture, but no later client peer
validation, descriptor handoff, abstract-socket mode, or live pathname identity
binding exists.

## Proposed remediation / Vorgeschlagene Remediation

Do not claim this boundary fixed without a verified end-to-end design. Future
candidates are Linux-only abstract AF_UNIX support, client-side `SO_PEERCRED`
validation against securely managed expected engine identity, or descriptor
handoff. Each needs compatible Traefik/Yaegi/runtime contracts, restart
semantics, and hostile same-UID validation; none is a current verified fix.

## Acceptance criteria / Akzeptanzkriterien

- A selected client-to-engine identity boundary is validated with hostile
  same-UID post-readiness replacement.
- A fake endpoint cannot receive a newly opened middleware transaction or make
  it accept allow as the intended engine.
- Existing startup collision, path-length, YAML-quoting, Allow, Blocking,
  shutdown, and cleanup-refusal controls remain covered.

## Validation plan / Validierungsplan

- Run a real native Traefik/Yaegi host test with a deterministic post-readiness
  replacement listener and a Blocking request.
- Test engine restart/PID-reuse semantics for any peer-identity approach.
- Validate a Linux-specific or portable fallback without weakening
  unsupported-platform fail-closed behavior.

## Regression tests / Regressionstests

- `connectors/traefik/native_middleware/engine_uds_test.go`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- A future genuine host post-readiness replacement test.

## Legitimate control tests / Legitime Kontrolltests

- Focused C engine protocol/lifecycle and Python runner contracts passed for
  the narrower pre-capture hardening controls.

## Dependencies / Abhängigkeiten

- A verified end-to-end Traefik client/engine identity-bound design and
  compatible host runtime evidence.

## Blockers / Blocker

- No current client peer-identity verification, descriptor handoff, or
  supported abstract-AF_UNIX configuration contract.
- No genuine native Traefik/Yaegi host runtime to validate an architectural
  mitigation.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0008`
- `FND-PARENT-0013`
- `FND-PARENT-0014`

## Residual risk / Restrisiko

The current path and `0700` allocation mitigate cross-UID collision but not a
hostile same-UID endpoint rebind after readiness. No risk has been accepted.

## History / Historie

- `2026-07-17T14:33:24Z`: `current_task_security_boundary_identified` —
  independent source-to-sink review distinguished post-readiness client redial
  and allow-result acceptance from final cleanup. It has conditional integrity
  and confidentiality impact but no current end-to-end identity-bound
  mitigation or host reproduction.
