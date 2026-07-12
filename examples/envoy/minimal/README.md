# Minimal ext_proc reference

**Language:** English | [Deutsch](README.de.md)

The selected Envoy core needs one streamed ext_proc configuration to cover all
four phases, so it has no second request-only native configuration here. Start
with [the Safe template](../safe/envoy-ext-proc-streaming.yaml.in) and keep its
Safe policy. The separate ext_authz request-only material is under
[compatibility-ext-authz](../compatibility-ext-authz/README.md).
