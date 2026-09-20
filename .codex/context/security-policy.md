# Security Policy and Workflow

## Trigger

Assess security relevance for every non-trivial change. This policy applies when work touches authentication/authorization, isolation, parsers/serialization, request/response/protocol handling, network/socket/TLS boundaries, files/paths/archives/temp files, commands/subprocesses/plugins, secrets/logs/private data, cryptography/downloads/dependencies, memory/lifetime/concurrency, sandbox/privileges, CI permissions, or deployment configuration.

## Core invariant

Untrusted or externally controlled input must not escape its approved boundary, execute unintended behavior, disclose protected data, consume unbounded resources, or convert a failed control into false success.

## Normal security check

For relevant work:

1. define the security invariant;
2. identify controlled/trusted inputs, assets, trust boundaries, sinks, failure modes, and existing controls;
3. select negative tests/reproducers through the affected boundary;
4. check relevant alternate encodings/paths/lifecycle transitions/bypass classes;
5. preserve legitimate behavior;
6. record actual security impact, residual risk, and evidence limits.

A scanner/static-analysis signal is a lead, not a validated finding.

## Security scan / finding fix

Use the available Codex Security scan workflow for explicit broad/security-readiness scans. Use the focused finding-fix workflow for one plausible/validated finding. Do not patch speculative source patterns before establishing reachability or a broken control.

A fixed finding requires rerunning the original attack/strongest proof, a legitimate same-boundary control, a relevant alternate bypass review, and focused regression validation.

## Secrets and evidence

Never expose/store tokens, passwords, private keys, credential-bearing URLs, Authorization headers, raw sensitive payloads, complete inherited environments, or unrestricted logs. Retain only bounded redacted evidence.

## Delivery blocker

A reportable high/critical-impact finding blocks `complete`, `verified_pr`, and master integration until it is fixed and verified, proven inapplicable/already safe, or explicitly deferred/risk-accepted by the current user with the residual risk recorded.

Security work never grants installation, Git, GitHub, merge, system, service, or deployment authority.
