# lighttpd examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Stock uses the repository sidecar to own the client-to-private-backend exchange.
Patched uses `mod_msconnector` with the matching Framework-synchronized patched
lighttpd host. Both provide P1--P4 inputs through their own integration.

## Profiles

### Logical solution bundles

| Solution | Off | Safe | Strict | All | Host requirements |
| --- | --- | --- | --- | --- | --- |
| Stock | [bundle](stock/off/) | [bundle](stock/safe/) | [bundle](stock/strict/) | [bundle](stock/all/) | Native sidecar, private backend, runtime file, and `stock-sidecar.args`. |
| Patched | [bundle](patched/off/) | [bundle](patched/safe/) | [bundle](patched/strict/) | [bundle](patched/all/) | Matching patched host/module pair, host configuration, and runtime file. |

Stock examples listen on `127.0.0.1:8080` and forward to the private backend
at `127.0.0.1:8081`. Patched examples select
`msconnector.request-body-gate = "pre-upstream"` and inspect identity HTTP/1.1
entities through `mod_proxy`. Their scope excludes compressed, HTTP/2, HTTP/3,
file, and zero-copy responses.

### P1-P4 contract

P1/P2 are request headers/body and P3/P4 are response headers/body. Common
Runtime selects the decision and the adapter applies the supported host action.

### DetectionOnly profile

The older [detection-only runtime file](detection-only/msconnector-runtime.conf)
is a native compatibility example. Its [DetectionOnly rules](rules/detection-only.conf)
evaluate and record matches with disruptive engine actions disabled. Use the
Stock or Patched bundles above for the complete topology.

### Disabled profile

[disabled/lighttpd.conf](disabled/lighttpd.conf) sets
`msconnector.enabled = "disable"` and requires no runtime file. The
[Engine-Off rules](rules/engine-off.conf) keep the connector active with engine
rule evaluation disabled.

## Values to adapt

Adapt module ABI and installation paths, document root, logs, PID/upload paths,
listeners, upstreams, runtime files, and reviewed rules paths. Create runtime
and event directories with service-appropriate permissions. Activate one rule
source and use transaction-specific IDs. Keep event JSONL limited to metadata.

## Configuration reference

The generated [configuration reference](configuration-reference.md) documents
host directives, Common Runtime fields, and compatibility configuration. Choose
body modes supported by the selected host. Configure body inspection limits
and actions in engine rules using [Configuration](../../docs/configuration.md).

## P1--P4 Safe intent

Safe selects streaming input with `phase4_mode=safe` and log-only handling of
P4 decisions after response output starts. `off` disables the additional late
policy while preserving native intervention/error handling. `all` uses the
existing `strict` policy. Validate client-visible behavior in a matching host run.

## No-CRS rules

Install a reviewed rules file and select it in the runtime configuration. The
[No-CRS baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
is the repository test-profile source. Phase IDs and engine modes are explained
in the [examples overview](../README.md) and [rule examples](../common/rule-examples.md).

## Sidecar compatibility

The older [host-only proxy example](compatibility-sidecar/lighttpd-sidecar-proxy.conf)
illustrates routing to an operator-supplied sidecar. Adapt its listener, backend,
module and log paths. Choose a complete Stock or Patched bundle above for
connector lifecycle configuration.

## Stock service setup

The launcher reads fixed `stock-sidecar.args` records and executes the installed
native component at `/usr/libexec/msconnector/lighttpd-stock-sidecar`. The records
supply `--config`, `--listen`, `--upstream`, and `--timeout-ms`. Both endpoints
must be literal loopback addresses. From the repository root, launch as the
service UID after installing the component and adapting rules/event paths.

~~~sh
python3 connectors/lighttpd/launch_stock_sidecar.py --profile safe
~~~

The accepted profiles are `all`, `off`, `safe`, and `strict`. `--install-root`
relocates the fixed component, absolute config, and spool paths for staged
installations. Stage external builds at the fixed component path. The launcher
validates ownership, permissions, and native artifact type, then executes
through a pinned descriptor.

Spool directories under `/var/lib/msconnector/lighttpd-stock/{all,off,safe,strict}`
must be owned by the effective UID with mode 0700. The launcher creates missing
children where its UID has write permission and rejects unsafe existing paths.
An administrator can provision the ancestors and selected profile directory
with the service's actual UID/GID. These commands describe initial provisioning.

~~~sh
install -d -o root -g root -m 0755 /var/lib/msconnector /var/lib/msconnector/lighttpd-stock
install -d -o SERVICE_UID -g SERVICE_GID -m 0700 /var/lib/msconnector/lighttpd-stock/safe
~~~

Configuration parents such as `/etc/lighttpd` may retain mode 0755. Spool
admission defaults to `--spool-capacity-bytes` 268435456 (256 MiB) of aggregate
outstanding reservations and `--spool-free-reserve-bytes` 67108864 (64 MiB) of
available free space. After P1 allows, the service preallocates the declared
request using `posix_fallocate` and rechecks free space before body inspection.
Allocation failures return 503 with a connector resource error. Reservations
last until descriptor close, and a directory lifetime lock prevents concurrent
sidecars sharing a spool. Synchronous allocation can outlast deadline checks.

## Validation

For Patched, install the matching host/module pair, adapt its configuration,
and check the installed host file. For Stock, check the private backend
configuration and the sidecar setup above. The path below is an installation
example.

~~~sh
lighttpd -tt -f /etc/lighttpd/lighttpd.conf
~~~

This checks syntax and readable inputs. Use the [testing guide](../../docs/testing-and-evidence.md)
for runtime validation.

## Strict profile boundary <a id="strict-profile-boundary"></a>

Common Runtime admits `phase4_mode=strict` for Stock, whose sidecar profile has
a tested post-commit socket shutdown. Patched rejects it at startup because its
required host action is unproven. The Strict and `all` bundles expose the
respective admission behavior.

## Related material

- [lighttpd connector guide](../../connectors/lighttpd/README.md)
- [Repository examples overview](../README.md)
