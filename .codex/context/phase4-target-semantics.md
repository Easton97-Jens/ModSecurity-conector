# Phase-4 Target Semantics

## Status of this document

This is a target/migration contract. It defines the desired Phase-4 semantics and is not proof that the current checkout already implements them. When current code differs, treat that as implementation/migration work rather than silently redefining the target.

## Scope

The target applies to Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd across Common Runtime, native integrations, bridges/sidecars, and response observers, subject to actual host capabilities.

## Response inspection versus intervention

Keep these decisions separate:

1. which response content ModSecurity inspects;
2. how the connector applies an engine-requested intervention.

The Phase-4 mode controls the additional intervention policy. It is not a switch that disables response inspection.

## MIME selection target

The ModSecurity Engine decides response MIME inspection through its own configuration, including `SecResponseBodyAccess`, `SecResponseBodyMimeType`, and `SecResponseBodyMimeTypesClear`.

Target state: no separate connector-owned Phase-4 MIME allowlist and no separate `phase4_content_types_file` selection affecting inspection/intervention. A connector must not exclude response data from ModSecurity or weaken an intervention solely because of such a connector MIME list.

Removing connector MIME selection does not remove body/resource limits, configured body modes, engine settings, or transport limits.

## Response-body limit ownership target

The ModSecurity Engine owns WAF response-inspection scope and byte-limit
policy through `SecResponseBodyAccess`, `SecResponseBodyMimeType`,
`SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit`, and
`SecResponseBodyLimitAction`.

Target state: no Phase-4 mode adds a connector-owned cumulative response-body
inspection budget. A connector must not reject, truncate, reset, or abort a
response solely because a connector-specific Phase-4 inspection byte count is
exceeded, including in `safe` or `strict`.

Legacy `modsecurity_phase4_body_limit` or Common response-budget settings may
remain parseable during compatibility migration, but they are not WAF policy
and must not reintroduce mode-specific response rejection. Removal from public
configuration can happen separately as an explicitly breaking migration.

Independent host and transport resource controls remain valid: fixed chunk or
frame caps, bounded sidecar storage, allocation ceilings, timeouts, correlation
limits, file metadata/read validation, and integer-overflow guards. Such limits
must be documented as host/transport capacity, not as ModSecurity inspection
policy, and must not become stricter merely because Phase-4 mode is `safe` or
`strict`.

Streaming/native connectors should not add whole-response buffering solely to
support Phase 4. File-backed bodies may be materialized through a fixed,
reusable scratch buffer before `msc_append_response_body`; that scratch size is
a working-buffer bound, not a response-body inspection limit.

## Target Phase-4 modes

Valid target values are exactly:

- `off`
- `safe`
- `strict`

Target default: `off`.

`minimal` is not a target mode or alias.

### off

The additional Phase-4 intervention policy is disabled. The evidenced native/historical intervention path for that integration remains, while configured response inspection, Phase-4 rule evaluation, and normal audit/error handling continue.

`off` does not mean ModSecurity/SecRuleEngine/SecResponseBodyAccess off, response-body mode none, or blanket allow.

### safe

Explicit opt-in. Enforce a requested intervention while the response can still be changed correctly. If it is too late, truthfully record that it was not enforced and do not abort the response solely because of that late rule intervention.

### strict

Explicit opt-in. Enforce while possible. After response commit, use only a host/stream abort mechanism that is actually supported and appropriate. If no such mechanism exists, expose that limitation and actual result; do not silently downgrade while claiming strict success.

## Commit and errors

Already-sent status/headers/bytes cannot be taken back. Keep detection, requested action, actual action, and client-visible result separate in evidence/logging.

Real engine, memory, transport, and processing failures remain failures. Safe late-rule behavior must not convert genuine errors into success.

Independent body/resource safety limits, bounded memory, streaming properties, and exactly-once finalization remain required in all modes. Connector-owned WAF inspection byte policy is not.

## Configuration and inheritance

`UNSET` and explicit `off` are different states. Explicit `off` overrides inherited `safe`/`strict`.

Parser/defaults/bindings/serialization/runtime must share the same semantics. Removed modes/options must not be silently ignored or remapped; invalid configuration should fail clearly.

## Documentation and evidence

Documentation must distinguish current behavior, target semantics, and unsupported capabilities. EN/DE product documentation remains equivalent where versioned docs are affected.

Parser acceptance, build success, or static checks do not prove a real client intervention. Claims about detection, enforcement, abort/transport behavior, and client outcome are limited to actually tested evidence.
