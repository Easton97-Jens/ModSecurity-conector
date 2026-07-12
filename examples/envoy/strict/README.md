# Envoy Strict profile boundary

**Language:** English | [Deutsch](README.de.md)

## Status

The ext_proc service accepts `late_action_policy: strict`, but currently
records `strict_abort_not_attempted` after the commit boundary. Strict is
optional and no late-reset configuration is claimed.

## Use

Use the Safe ext_proc template and service contract, validate the generated
YAML and service JSON, and add host evidence before relying on a strict
transport outcome.
