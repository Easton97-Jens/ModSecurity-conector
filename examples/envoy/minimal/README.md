# Minimal ext_proc reference

**Language:** English | [Deutsch](README.de.md)

The selected Envoy core needs streamed ext_proc input in both directions. This
directory therefore supplies a complete minimal transport shape in
[envoy-ext-proc-streaming.yaml.in](envoy-ext-proc-streaming.yaml.in), its
validated service contract, and a paired Common Runtime file with
`phase4_mode=minimal`. It is not a request-only native path: the bridge still
requires STREAMED request and response body modes. The separate ext_authz
request-only material remains under
[compatibility-ext-authz](../compatibility-ext-authz/README.md).
