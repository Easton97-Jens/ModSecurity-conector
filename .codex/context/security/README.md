# Security Assessment System

This directory decomposes deep security work into one generic assessment contract, reusable check modules, and connector-specific deltas.

## Design rule

Do not duplicate the complete scan workflow per connector.

A deep connector assessment loads:

1. `../profiles/connector-security-assessment.md`;
2. `connector-deep-assessment.md`;
3. exactly one connector delta from `connectors/`;
4. only the reusable `checks/` modules named by that delta;
5. the normal core policies routed by `../index.md`.

All-connector and repository-wide profiles reuse the same components.

## Evidence rule

No finding, build, scanner result, capability declaration, or source path is transferable from one logical profile to another unless the current repository contract explicitly defines a shared boundary and the evidence binds that boundary.

Request-only compatibility routes, response companions, native routes, sidecars, and patched routes remain distinct.
