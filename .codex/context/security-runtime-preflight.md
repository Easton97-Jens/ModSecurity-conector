# Native NGINX and Envoy Security Runtime Preflight

Read this only when a Parent security scan/focused security validation needs native NGINX or Envoy runtime evidence.

## Common requirements

Use a task-owned configured external runtime root. Validate containment, ownership/mode requirements, no-symlink conditions, safe ports, and payload-safe evidence before start. A missing host prerequisite is `blocked_environment`, not permission to weaken the harness.

## NGINX

Resolve the worker identity required by the checked-in harness. Native coverage requires a non-root worker distinct from the launcher/master and a proven task-owned ownership hand-off where the harness requires it.

Do not run the worker as root, collapse identities, skip ownership/ACL/mode/symlink checks, or apply broad ownership changes.

If required ownership/capability hand-off cannot be performed safely, record `blocked_environment` and limit any remaining claim to its actual static/unit scope.

## Envoy

Resolve actual private UDS paths from the selected runtime root and verify Unix-socket path length before launch. A shorter root is allowed only when it remains task-owned, contained, private, and symlink-safe.

Do not fall back to shared/public paths or weaken private-socket checks.

Response-phase validation requires a ruleset and expected event contract that actually exercise the selected P3/P4 behavior. Static URI/header checks do not by themselves prove end-to-end callback/original-request correlation.
