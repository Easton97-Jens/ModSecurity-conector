**Language:** English | [Deutsch](new-connector-contract.de.md)

# New connector contract

A future connector should declare complete metadata, connector capabilities,
configuration mapping, request/response mapping, decision mapping, event/log
mapping, and artifact layout before claiming support.

This document is a contract guide only. It does not migrate any existing
connector and does not claim runtime behavior, capability support, or production
readiness.

## Common package expectations

Future connector adoption should map host requests/responses through the common
request and response helpers, expose manifests and origin governance, use the
build-contract target vocabulary where adopted, and keep runtime reports honest.
No existing connector is adopted by this documentation-only update.

## Directive, mapper, and CRS setup contracts

New connectors should consume the global common contracts before making runtime claims:

- Register host directives from the connector-neutral `directive_adapter` model, while keeping concrete server types such as `ngx_command_t` and Apache `command_rec` inside the connector.
- Implement request mappers from host requests such as `ngx_http_request_t`, Apache `request_rec`, or equivalent APIs into `msconnector_request` and validate the output against `request_mapper_contract`.
- Implement response mappers into `msconnector_response` and validate the output against `response_mapper_contract`; do not log body payloads through this contract.
- Describe CRS/ruleset setup with `crs` configuration only as a setup convention. A valid CRS config is not a CRS PASS claim.

This guide does not require or assert adoption by existing NGINX, Apache, HAProxy, Envoy, lighttpd, or Traefik runtimes. Host-specific request chains, APR pools, bucket brigades, server hooks, filters, and body buffers remain connector-owned.

## Existing Apache connector note

The Apache connector is an example of a host-specific adapter beginning this
adoption: Common owns semantic config/directives/mapper contracts/events, while
Apache-owned code keeps Apache API access and filter/hook mechanics. This note
is not a production, CRS, full-matrix, or runtime verification claim.

## NGINX/Common adoption precedent

A connector may keep server-native registration and request/filter APIs while
embedding or mapping `msconnector_config` and using Common directive specs,
request/response mapper contracts, headers, events, and limits. Compile-only C17
checks should distinguish real compilation from blocked environments with exit
77, and optional future-standard checks must not claim production or runtime
coverage.

## HAProxy adoption note

The HAProxy connector is expected to consume the Common SDK for connector-neutral semantics: configuration, directive specs/adapters, primitive parsers, mapper contracts, event JSONL, redaction, resource limits, guards, CRS setup contracts, artifact/test-result contracts, and status/error mapping. HAProxy-specific SPOE/SPOP protocol code, HAProxy cfg glue, runtime process handling, frame parsing, socket handling, and build integration remain adapter-owned. C17 compile evidence is structural only and must not be described as production, CRS, full-matrix, or runtime verification.

## Starter/not_verified connector rule

A starter connector may add thin adapter mappers to Common SDK request/response/config contracts, but it must keep metadata at `runtime_status=not_verified` and `verification_status=connector-gap` until runtime evidence exists. Do not log body payloads. Do not add server-specific types to `common/`. Keep host API glue, runtime lifecycle, build glue, and protocol/frame handling in the connector tree.

## Generic mapper adoption

Starter connectors should prefer the connector-neutral generic mapper helper when their local source can be expressed as `msconnector_generic_request_source` or `msconnector_generic_response_source`. Local files should stay thin adapters and must not duplicate header mapping, Host fallback, Common validation, or ownership cleanup logic. This does not imply runtime verification.
The remaining starter connectors now avoid connector-local mapper source copies by aliasing their map entry points to the connector-neutral generic mapper; this keeps duplicated Host lookup, validation, and body metadata assignment in one Common implementation only.

Generic mapper callers must pass `hostname` as a NUL-terminated string when it is set; header value slices are never exposed as C-string hostnames. Nonzero body sizes require non-NULL body data and remain metadata-only unless the caller owns safe body bytes.
