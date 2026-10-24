# Phase-4 Target Migration Assessment

## Command execution

Load `../command-execution-policy.md` before issuing local shell/project commands.

## Purpose

Compare current implementation/configuration/documentation/evidence against `../phase4-target-semantics.md` without silently treating target semantics as current behavior.

## Scope

Assess Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd plus Common Runtime and relevant Framework contracts.

For every affected logical profile inventory:

- accepted Phase-4 mode values and defaults;
- config inheritance/merge semantics;
- connector-owned MIME/content-type controls;
- engine `SecResponseBody*` interaction;
- body/resource limits;
- response commit boundary;
- Safe and Strict requested/actual actions;
- parser/serialization/binding consistency;
- documentation/current examples;
- current runtime evidence and unsupported claims.

Classify each item as current-compatible, migration-required, obsolete-compatibility, target-unsupported-by-host, or evidence-gap with concrete source/evidence references.

No code change is implied unless the user separately requests implementation.
