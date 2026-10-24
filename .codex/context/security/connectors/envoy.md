# Envoy Deep Security Delta

## Logical profiles

- `envoy-ext-proc`: direct streamed ext_proc route
- `envoy-ext-authz`: request authorization plus mandatory private response observer

Do not present direct ext_authz request authorization as ext_proc P3/P4 evidence.

## Host-specific boundaries

Assess Envoy filter-chain selection, ext_proc gRPC stream lifecycle, streamed request/response headers/body, message ordering, per-stream session mapping, cancellation/deadlines, partial messages, backpressure, `failure_mode_allow`, service restart, response commit and reset semantics, generated configuration, local ports/UDS paths, and Common/libmodsecurity service mapping.

For `envoy-ext-authz`, assess the opaque response-handle transfer, bounded/TTL registry, single claim, mandatory response observer, internal header removal before real upstream, private MRC1 UDS, and fail-closed behavior for malformed/missing/expired/replayed handles.

Pay special attention to:

- gRPC stream cancellation and stale response after reconnect;
- transaction/session mix-up across concurrent streams;
- header/body truncation and body range identity;
- service error interpreted as Allow;
- public listener or TCP fallback where private IPC is required;
- UDS length/containment before native runtime start;
- H2/H3 transport claims only with actual selected evidence.

## Required common checks

Load all common modules including `filesystem-ipc.md` and `protocol-framing.md`.

## Envoy-specific validation seeds

Where repository-native targets support them, exercise ext_proc message ordering, request/response streaming, cancellation, deadline, malformed response, concurrent streams, reconnect, service restart, ext_authz handle missing/duplicate/expired/replay, observer unavailability, and legitimate follow-up traffic.
