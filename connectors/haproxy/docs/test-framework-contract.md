# HAProxy Test Framework Contract

Status: documentation only

No tests are stored in this connector repository.

All test definitions, test execution, runners, and generated reports belong to
Easton97-Jens/ModSecurity-test-Framework.

This repository may only document the contract expected by the central
framework.

runtime_verified must remain false in this repository until external framework
evidence is produced.

## Contract Surface (documentation only)

The HAProxy connector area may provide only non-test artifacts for framework
consumption, for example:

- connector metadata and status documentation
- example-only configuration placeholders
- harness contract documentation (no runner implementation)
- evidence notes and open questions

## Explicit Ownership Boundary

- Connector repo: no test cases, no local test plans, no test runners, no test
  implementations, no generated reports.
- Central framework repo: owns all executable tests, test plans, runners,
  orchestration, and generated report outputs.
