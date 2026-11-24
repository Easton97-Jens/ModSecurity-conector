# Traefik examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

The native profile uses the repository-owned local plugin and a persistent
private Unix-domain-socket engine service. The forwardAuth profile combines
request authorization with a private response observer.

## Complete logical-solution matrix

| Solution | Off | Safe | Strict | All | Phase input |
| --- | --- | --- | --- | --- | --- |
| Native UDS | [bundle](native-uds/off/) | [bundle](native-uds/safe/) | [bundle](native-uds/strict/) | [bundle](native-uds/all/) | `modsecurityNative` streams P1--P4 in one transaction. |
| forwardAuth + observer | [bundle](forwardauth/off/) | [bundle](forwardauth/safe/) | [bundle](forwardauth/strict/) | [bundle](forwardauth/all/) | forwardAuth supplies P1/P2; `modsecurityResponseObserver` supplies P3/P4. |

The forwardAuth middleware must be followed immediately by the private-UDS
observer. Request bodies use bounded buffering with `forwardBody: true` and
`maxBodySize: 4096`. The observer claims the opaque transaction handle.
Missing handles and observer timeouts fail closed and clean up the transaction.

## Files

The standalone [Off static file](off/traefik-static.yaml),
[dynamic file](off/traefik-dynamic.yaml), and
[engine file](off/traefik-engine-service.conf) show local-plugin registration,
File Provider wiring, and UDS service configuration. The [Safe dynamic file](safe/traefik-dynamic.yaml)
and [engine file](safe/traefik-engine-service.conf) select streaming bodies
and `phase4_mode=safe`.

### DetectionOnly profile

[detection-only/traefik-engine-service.conf](detection-only/traefik-engine-service.conf)
selects [DetectionOnly rules](rules/detection-only.conf) with the UDS middleware.
Matches are evaluated and recorded with disruptive engine actions disabled.

### Disabled profile

[disabled/traefik-engine-service.conf](disabled/traefik-engine-service.conf)
sets `enabled=off`. [Engine-Off rules](rules/engine-off.conf) keep the connector
active with engine rule evaluation disabled.

## Values to adapt

- Stage the matching `github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware`
  source in the installed Traefik local-plugin workspace.
- Adapt `entryPoints.web.address`, router rules, upstream URL, and
  `providers.file.filename`. Relative File Provider paths resolve from the
  Traefik working directory.
- Set `engineMode: uds` and a private `engineSocketPath` such as
  `/run/traefik-msconnector/engine.sock`. Protect its parent directory and
  give the trusted service ownership. Legacy `passthrough` is rejected.
- Install reviewed rules and adapt `rules_file`, event destinations, and
  permissions. Activate one rule source and use transaction-specific IDs.
  Event JSONL contains metadata only.

The native service applies one monotonic deadline per complete frame. Its
`--max-workers N` CLI option bounds workers to 64 by default and 256 maximum.
Shutdown signals active sockets and waits for workers before finalization.

## Configuration reference

The generated [configuration reference](configuration-reference.md) describes
static/dynamic YAML, plugin defaults, Common Runtime fields, and header/chunk/
inactivity controls. Body inspection limits and actions belong in engine rules.
See [Configuration](../../docs/configuration.md).

## P1--P4 Safe intent

The native HTTP/1.1 reference uses streaming body modes and Safe log-only
handling for P4 decisions after response commit. `phase4_mode=off` disables the
additional late policy while preserving native handling. `all` selects the
existing `strict` value. Client-visible behavior requires a matching host run.

## No-CRS rules

Install the reviewed [No-CRS baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
selected by the engine service. Phase IDs and engine modes are explained in
the [examples overview](../README.md) and [rule examples](../common/rule-examples.md).

## forwardAuth compatibility

The older [dynamic](compatibility-forwardauth/traefik-dynamic.yaml) and
[static](compatibility-forwardauth/traefik-static.yaml) files illustrate
request authorization only. Adapt both files together, including the File
Provider path, listener, router, trusted authorization URL, and application
upstream. Keep credentials out of URLs. Changing `trustForwardHeader: false`
requires an explicit proxy-header trust policy. Choose the complete
`forwardauth/` bundles above for response inspection.

## Validation

Copy the selected static/dynamic files to the File Provider locations, adapt
paths and endpoints, then validate the installed static configuration.
`/etc/traefik/traefik.yaml` is an installation example.

~~~sh
traefik check --configFile=/etc/traefik/traefik.yaml
~~~

Verify plugin loading, a private engine socket, and service access to the rules
file. A configuration check establishes loading. Use the [testing guide](../../docs/testing-and-evidence.md)
for runtime validation.

## Strict profile boundary <a id="strict-profile-boundary"></a>

Common Runtime rejects `phase4_mode=strict` for both profiles at startup because
the required `strict_post_commit_action` is unproven. The Strict and `all`
bundles expose this admission boundary. Off and Safe are runtime-admissible.

## Related material

- [Traefik connector guide](../../connectors/traefik/README.md)
- [Repository examples overview](../README.md)
