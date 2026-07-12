# HAProxy SPOE/SPOA PoC Scaffold

**Language:** English | [Deutsch](README.de.md)

documentation only

## Status
- documentation_only: true
- implementation_status: not_started
- runtime_verified: false
- decision_status: undecided
- promoted: false

## Purpose
This directory serves exclusively as a documentary placeholder for
a later HAProxy-SPOE/SPOA-PoC as part of the existing one
Evidence documents.

This directory does not contain a runnable HAProxy SPOE/SPOA PoC.

## Planned but not created artifacts (planned only)
- `connectors/haproxy/poc/spoe/haproxy.cfg.example` (planned only)
- `connectors/haproxy/poc/spoe/spoe-agent.conf.example` (planned only)
- Framework-side tests: planned in ModSecurity-test-Framework, not in this repository.
- Framework-side report outputs: planned in ModSecurity-test-Framework, not in this repository.

The example configuration files are illustrative only and not runtime verified.

## Test and report ownership
No tests are stored in this connector repository.

All test definitions, test execution, runners, and generated reports belong to
Easton97-Jens/ModSecurity test framework.

runtime_verified must remain false in this repository until external framework
evidence is produced.

## Non-targets
- No runtime implementation.
- No C code.
- No Python/Shell scripts.
- No HAProxy configuration in this directory.
- No SPOE agent configuration in this directory.
- No statement that SPOE/SPOA is functional.

## Open points
- Exact SPOE/SPOP configuration details: To be verified externally.
- Full ModSecurity semantics: Not provable from current repository.
- Request/Response/Intervention Details: To be checked.
