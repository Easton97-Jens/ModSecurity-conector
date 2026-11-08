# External Analysis Services Policy

## Principle

External security/quality services are analysis inputs, not automatic truth. Use only currently configured, authorized, and technically verified access paths. Authentication, tool availability, or a successful upload is not itself a security/quality result.

This file owns **assessment composition** across external analysis services. It does not own SonarQube authentication, scanner, MCP, readback, or Quality-Gate rules.

## OpenAI security analysis / TAC

When the current assessment explicitly requires the configured OpenAI security-analysis capability, resolve the actual active access path from current local control information and official current product guidance. Do not invent a local TAC daemon, CLI command, endpoint, model name, job API, or result identifier.

Record the actual selected scope/revision, files or bounded context analyzed, invocation/interface actually used, returned candidate findings, available run/request/session identifiers, and limitations. Validate candidates against current source and local evidence.

Do not send secrets, `.codex` credentials, unrelated private data, raw customer payloads, or a broader repository scope than required.

## SonarQube

For **all** SonarQube local access, authentication/environment preparation, Secrets/CI SonarScanner/CLI execution and disabled MCP, SonarQube Cloud analysis/readback, findings, exact-SHA binding, and Quality-Gate semantics, load and follow:

`../sonarqube-policy.md`

Do not duplicate or override its wrapper, credential, RTK-composition, scanner, MCP, readback, or delivery rules here.

When an assessment requires a fresh complete Sonar analysis, use the existing suitable CI SonarScanner within Free-plan limits and reconcile that exact-revision evidence with the other analysis sources. A clean Secrets scan permits development to continue but does not satisfy a complete code-quality requirement. This policy does not require Vortex/STANDARD/DEEP or authorize paid analysis or MCP activation.

## Reconciliation

Keep OpenAI/TAC candidates, SonarQube findings, repository tests, compiler/static-analysis results, and runtime evidence as distinct sources.

Deduplicate by root cause only after preserving provenance, revision, location, and validation evidence. A missing scanner/AI finding does not disprove a locally demonstrated issue. A successful external analysis does not substitute for builds, tests, runtime evidence, or another required analysis source.

Where two services disagree, record the disagreement and validate the underlying code/control path rather than selecting the more favorable result.
